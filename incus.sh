#!/bin/bash
export LANGUAGE="C"
export LC_ALL="C"

usedSystem=""
osVersion=""

if [[ $(tput colors) -ge 8 ]]; then
    RED='\033[0;31m'
    # GREEN='\033[0;32m'
    BLUE='\033[0;34m'
    NC='\033[0m'
else
    RED=''
    BLUE=''
    NC=''
fi

function log() {
    echo -e "${BLUE}[INCUS] $(date +'%Y-%m-%d %H:%M:%S') >>>> $*${NC}"
}
function log_error() {
    echo -e "${RED}[INCUS] $(date +'%Y-%m-%d %H:%M:%S') >>>> $*${NC}"
}

function prepare_node() {
    # first argument is OS name/OS version
    # second argument is number of kea nodes
    # third argument is number of internal testing networks
    oldIFS=$IFS
    IFS='/' read -r usedSystem osVersion <<< "$1"
    IFS=$oldIFS
    log "Creating kea-$2 node on system $usedSystem version $osVersion"
    incus launch images:"$1" kea-"$2"
    sleep 3
    incus exec kea-"$2" -- apt update > /dev/null 2>&1
    if [[ "$2" == "forge" ]]; then
        incus exec kea-"$2" -- apt install python3 python3-venv g++ python3-dev libpcap-dev git tcpdump openssh-server -y > /dev/null 2>&1
    else
        incus exec kea-"$2" -- apt install vim git curl openssh-server socat gnupg freeradius bind9 net-tools tcpdump -y > /dev/null 2>&1
        # TODO take hammer from any branch
        mount_ccache kea-"$2"
        incus exec kea-"$2" -- curl -L https://gitlab.isc.org/isc-projects/kea/-/raw/master/hammer.py -o /tmp/hammer.py
        log "Running hammer, output in /tmp/kea-$2-hammer.log"
        # this is a neat trick, commands executed by hammer are still printed to stdout
        incus exec kea-"$2" -- python3 /tmp/hammer.py prepare-system -p local -w mysql pgsql forge shell > /tmp/kea-"$2"-hammer.log # tls netconf gssapi
    fi
}

function create_networks() {
    # first argument is number of internal networks
    for i in $(seq 0 $(("$1"-1))); do
        log "Creating network internal-net-$i"
        incus network create internal-net-"$i" ipv4.nat=false ipv6.nat=false ipv4.dhcp=false ipv6.dhcp=false ipv4.firewall=false ipv6.firewall=false
    done
    incus network list
}

function update_nodes() {
    # first argument is number of nodes
    log "Updating nodes"
    for i in $(seq 1 "$1"); do
        incus exec kea-"$i" -- apt update
        incus exec kea-"$i" -- DEBIAN_FRONTEND=noninteractive apt dist-upgrade -y
    done
}

function attach_node_to_network() {
    # first argument is network name
    # second argument is node name
    # third argument is interface name
    log "Attaching $2 to $1 on interface $3"
    incus network attach "$1" "$2" "$3"
}

function remove_incus_containers() {
    # first argument is number of kea nodes
    log "Deleting containers"
    for i in $(seq 1 "$1"); do
        incus delete kea-"$i" --force
    done
    incus delete kea-forge --force
}

function remove_incus_network() {
    # first argument is number of internal networks
    for i in $(seq 0 $(("$1"-1))); do
        log "Deleting network internal-net-$i"
        incus network delete internal-net-"$i"
    done
}

function create_user() {
    # first argument is a node name
    log "Creating user forge in $1"
    (echo "forge"; echo "forge") | incus exec "$1" -- adduser --gecos "" forge
    incus exec "$1" -- systemctl enable ssh
    incus exec "$1" -- systemctl start ssh
    echo "forge ALL=(ALL) NOPASSWD:ALL" > nopasswd
    incus file push nopasswd "$1"//etc/sudoers.d/forge
    incus exec "$1" -- chmod 440 /etc/sudoers.d/forge
    incus exec "$1" -- chown root:root /etc/sudoers.d/forge
}

function generate_rsa_key() {
    # no arguments needed
    log "Generating RSA key for kea-forge"
    # we need this just in kea-forge, it will ssh into other nodes
    incus exec kea-forge -- sudo -u forge ssh-keygen -t rsa -N "" -f /home/forge/.ssh/id_rsa
    incus exec kea-forge -- cat /home/forge/.ssh/id_rsa.pub > kea-forge.pub
    cat kea-forge.pub
}

function check_ssh() {
    log "Checking SSH connection from kea-forge to kea-$1"
    incus exec kea-forge -- sudo -u forge ssh -o StrictHostKeyChecking=accept-new forge@IP
}

function migrate_rsa_key() {
    # first argument is a node name
    log "Migrating RSA key to kea-$1"
    incus exec "$1" -- mkdir -p /home/forge/.ssh
    incus exec "$1" -- chown -R forge:forge /home/forge/.ssh
    incus exec "$1" -- chmod 700 /home/forge/.ssh
    incus file push kea-forge.pub "$1"/home/forge/.ssh/authorized_keys
    incus exec "$1" -- chown forge:forge /home/forge/.ssh/authorized_keys
    incus exec "$1" -- chmod 600 /home/forge/.ssh/authorized_keys
}

function set_address() {
    # first argument is an address
    # second argument is an interface name
    # third argument is a node name
    log "Configuring address $1 for interface $2 on node $3"
    incus exec "$3" -- ip addr add "$1" dev "$2"
    incus exec "$3" -- ip link set "$2" up
}

function configure_internal_network(){
    # first argument is number of kea nodes
    # second argument is number of internal networks
    for interface in $(seq 1 "$2"); do
        set_address 192.168.5$((interface-1)).200/24 eth"$interface" kea-forge
        set_address 2001:db8:$((interface-1))::1000/64 eth"$interface" kea-forge
        for node in $(seq 1 "$1"); do
            set_address 192.168.5$((interface-1)).20"$node"/24 eth"$interface" kea-"$node"
            set_address 2001:db8:$((interface-1))::100"$node"/64 eth"$interface" kea-"$node"
        done
    done
}

function install_kea_pkgs() {
    # first argument is number of nodes
    # second argument is OS name/OS version
    # third argument is kea pkgs version

    # Check if the third argument ($3) is empty
    if [ -z "$3" ]; then
        pkg_version=$(get_kea_pkg_version)
    else
        pkg_version=$3
    fi

    if [ -z "$pkg_version" ]; then
        log_error "PKG version is empty and couldn't be determined"
        exit 1
    fi

    oldIFS=$IFS
    IFS='/' read -r usedSystem osVersion <<< "$2"
    IFS=$oldIFS
    echo "deb https://packages.aws.isc.org/repository/kea-$usedSystem-$osVersion/ kea main" > kea.list
    for node in $(seq 1 "$1"); do
        log "Installing kea packages version $pkg_version on node kea-$node on system $usedSystem version $osVersion"
        incus file push kea.list kea-"$node"/etc/apt/sources.list.d/kea.list
        incus exec kea-"$node" -- curl https://packages.aws.isc.org/repository/repo-keys/repo-key.gpg -o key
        incus exec kea-"$node" -- apt-key add key
        incus exec kea-"$node" -- apt update
        incus exec kea-"$node" -- apt install isc-kea-*="$pkg_version"
    done
    echo -e '\nINSTALL_METHOD="native"' >> init_all.py
    incus exec kea-forge -- sudo rm -f /home/forge/init_all.py
    incus file push init_all.py kea-forge/home/forge/init_all.py
}

function remove_kea_pkgs() {
    # first argument number of nodes
    for node in $(seq 1 "$1"); do
        log "Removing kea packages on node kea-$node"
        incus exec kea-"$node" -- apt remove isc-kea-* -y
    done
}

function mount_ccache() {
    # first argument is a node name
    log "Mounting ccache on node $1 using path /mnt/ccache/${usedSystem}/${osVersion}"
    incus config device add "$1" ccache disk source=/mnt/ccache/"${usedSystem}/${osVersion}"/amd64 path=/ccache readonly=true

}

function install_kea_tarball() {
    # first argument is number of nodes
    # second argument is path to directory with kea source code - jenkins is providing kea source code in ~/kea with hammer.
    # it's just needs to be copied to the kea nodes and installed
    for node in $(seq 1 "$1"); do
        log "Installing kea from the source code on node kea-$node"
        incus exec kea-"$node" -- rm -rf /tmp/kea
        incus file push -r -q "$2" kea-"$node"//tmp/.
        incus exec kea-"$node" --cwd=/tmp/kea -- python3 hammer.py build -p local -w ccache,forge,install,mysql,pgsql,shell -x docs,perfdhcp,unittest --ccache-dir /ccache # ,gssapi,netconf,tls
    done
    echo -e '\nINSTALL_METHOD="make"' >> init_all.py
    incus exec kea-forge -- sudo rm -f /home/forge/init_all.py
    incus file push init_all.py kea-forge/home/forge/init_all.py
}

function print_summary() {
    log "Testing setup summary:"
    incus list -cns46tSDM
    incus network list
}

function get_kea_pkg_version() {
    # use: pkg_version=$(get_kea_pkg_version)
    # echo head -n1 ubuntu-22.04-amd64-pkgs.txt | perl -nle 'm/([0-9\\.]+-isc[0-9]+)/; print \$1'
    echo ''
}

function setup_forge() {
    # no arguments needed
    log "Setting up forge in kea-forge"
    incus file push -r -q . kea-forge/home/forge/
    incus exec kea-forge -- sudo -u forge python3 -m venv /home/forge/venv
    incus exec kea-forge -- sudo -u forge /home/forge/venv/bin/pip install -r /home/forge/requirements.txt
    create_forge_init
    python3 modify_init_all.py
}

function run_pytest() {
    # first argument is a node name
    log "Running pytest"
    incus exec kea-forge --cwd=/home/forge -- sudo /home/forge/venv/bin/pytest "$@"
}

function create_forge_init() {
    log "Creating partial forge init script"
    # missing from this solution:
    # WIN_DNS_ADDR_2016 = "{WIN_DNS_ADDR_2016}"
    # WIN_DNS_ADDR_2019 = "{WIN_DNS_ADDR_2019}"

cat << EOF > init_all.py
LOGLEVEL = "info"
IFACE = "eth1"
SERVER_IFACE = "eth1"
SERVER2_IFACE = "eth1"
SOFTWARE_UNDER_TEST = "kea4_server", "bind9_server",
SOFTWARE_INSTALL_PATH = "/usr/local"
DB_TYPE = "memfile"
SHOW_PACKETS_FROM = "both"
REL4_ADDR = "0.0.0.0"
CLI_LINK_LOCAL = ""
copylist = []
removelist = []
OUTPUT_WAIT_INTERVAL = 1
OUTPUT_WAIT_MAX_INTERVALS = 2
PACKET_WAIT_INTERVAL = 1
HISTORY = True
TCPDUMP = True
TCPDUMP_PATH = ""
TCPDUMP_ON_REMOTE_SYSTEM = False
SAVE_CONFIG_FILE = True
AUTO_ARCHIVE = False
SLEEP_TIME_1 = 1  # wait after starting remote server
SLEEP_TIME_2 = 2  # wait after all others commands
MGMT_USERNAME = "forge"
MGMT_PASSWORD = "forge"
MGMT_PASSWORD_CMD = ""
SAVE_LOGS = True
BIND_LOG_TYPE = "ERROR"
BIND_LOG_LVL = 0
BIND_MODULE = "*"
SAVE_LEASES = True
DNS_IFACE = "eth0"
DNS_PORT = 53
DNS_SERVER_INSTALL_PATH = "/usr/sbin/"
DNS_DATA_PATH = "/etc/bind/"
ISC_DHCP_LOG_FACILITY = "local7"
ISC_DHCP_LOG_FILE = "/var/log/forge_dhcpd.log"
DB_NAME = "keadb"
DB_USER = "keauser"
DB_PASSWD = "keapass"
DB_HOST = ""
FABRIC_PTY = ""
MULTI_THREADING_ENABLED = True
FORGE_VERBOSE = True
EOF
}

function help() {
    echo "Usage: $0 {prepare-env|delete|stop} [arguments...]"
    echo "       $0 prepare-env OS-name/OS-version <number-of-kea-nodes> <number-of-internal-networks>"
    echo "            $0 prepare-env ubuntu/24.04 2 2"
    echo "       $0 clear-all <number-of-kea-nodes> <number-of-internal-networks>"
    echo "       $0 install-kea-pkgs <number-of-kea-nodes> <kea-pkgs-version> <OS-name/OS-version>"
    echo "            $0 install-kea-pkgs 2 ubuntu/24.04 2.7.3-isc20240903092214"
    echo "       $0 install-kea-tarball <number-of-kea-nodes> <path-to-source-code>"
    echo "            $0 install-kea-tarball 2 ~/kea"
    echo "       $0 run-pytest <pytest-arguments>"
    echo "            $0 run-pytest -vv tests/dhcp/test_options.py::test_v4_never_send_various_combinations"


    exit 1
}

if [[ $# -lt 1 ]]; then
    help
fi

command=$1
shift
case "$command" in
    prepare-env)
        # print incus configuration
        incus admin init --dump
        # start kea nodes kea-1 kea-2 etc
        startTime=$(date +%s)
        osName=$1
        numberOfNoders=$2
        numberOfNetworks=$3
        for i in $(seq 1 "$numberOfNoders"); do
            prepare_node "$osName" "$i"
        done
        # start forge node
        prepare_node "ubuntu/24.04" "forge"
        create_networks "$numberOfNetworks"
        # connect kea-forge to all networks
        for i in $(seq 1 "$numberOfNetworks"); do
            attach_node_to_network internal-net-$((i-1)) kea-forge eth"$i"
        done
        # connect all nodes to all networks
        for i in $(seq 1 "$numberOfNoders"); do
            for x in $(seq 1 "$numberOfNetworks"); do
                attach_node_to_network internal-net-$((x-1)) kea-"$i" eth"$x"
            done
        done
        # create main user in kea-forge and generate key
        create_user kea-forge
        generate_rsa_key
        # create users in other nodes and migrate key
        for i in $(seq 1 "$numberOfNoders"); do
            create_user kea-"$i"
            migrate_rsa_key kea-"$i"
        done
        configure_internal_network "$numberOfNoders" "$numberOfNetworks"
        incus list --format json | jq > incus.json
        setup_forge
        elapsed_time=$(($(date +%s) - startTime))
        print_summary
        log "Testing environment created in: $elapsed_time seconds"
        log "Python init script created in: init_all.py"
        log "Testing environment configuration saved in: incus.json file"
        ;;
    delete)
        remove_incus_containers "$@"
        ;;
    create-networks)
        create_networks "$@"
        ;;
    update)
        update_nodes "$@"
        ;;
    setup-forge)
        setup_forge
        ;;
    configure-networks)
        configure_internal_network "$@"
        ;;
    clear-all)
        remove_incus_containers "$1"
        remove_incus_network "$2"
        print_summary
        ;;
    install-kea-pkgs)
        install_kea_pkgs "$@"
        ;;
    install-kea-tarball)
        install_kea_tarball "$@"
        ;;
    run-pytest)
        run_pytest "$@"
        ;;
    *)
        echo "Unknown command: $command"
        help
        ;;
esac