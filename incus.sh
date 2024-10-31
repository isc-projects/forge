#!/bin/bash
export LANGUAGE="C"
export LC_ALL="C"

usedSystem=""
osVersion=""
# For now, we assume that this script is only running on debian based systems
# and launched containers will always have the same architecture as the host
arch=$(uname -m)

# change this to your needs, but on jenkins we will run with /dev/null
# logFile="/tmp/incus_$(date +'%Y_%m_%d_%H_%M_%S')_.log"
# logFile="/dev/stdout"
logFile="/dev/null"


if [[ $(tput colors 2> /dev/null) -ge 8 ]]; then
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
    printf "${BLUE}[INCUS] %s >>>> $*${NC}\n" "$(date +'%Y-%m-%d %H:%M:%S')"
}

function log_error() {
    printf "${RED}[INCUS] %s >>>> $*${NC}\n" "$(date +'%Y-%m-%d %H:%M:%S')"
}

function install_base_pkgs() {
    # pkgs names may differ between systems like rhel and fedora
    # let's check it when we gonna need it
    case "$usedSystem" in
        "ubuntu"|"debian")
            install_pkgs "$1" bind9 ccache curl freeradius gnupg net-tools openssh-server socat tcpdump vim
            ;;
        "fedora"|"rhel")
            install_pkgs "$1" bind ccache freeradius net-tools openssh-server socat tcpdump vim
            ;;
        "alpine")
            install_pkgs "$1" bash bind ccache curl freeradius gnupg net-tools openssl openssh python3 socat sudo tcpdump vim
            ;;
        *)
        printf "Not in the list"
        ;;
    esac
}

function prepare_freeradius() {
    node=$1
    if [[ "$usedSystem" == "fedora" ]]; then
        log "Preparing FreeRadius Certificates on $node - $usedSystem $osVersion"
        incus exec "$node" -- mkdir -p /etc/raddb/certs/dh
        incus exec "$node" -- /etc/raddb/certs/bootstrap
    fi
}

function get_os() {
    # The first argument is OS name/OS version
    oldIFS=$IFS
    IFS='/' read -r usedSystem osVersion <<< "$1"
    IFS=$oldIFS
}

function prepare_node() {
    # The first argument is the OS name/OS version
    # The second argument is the number of kea nodes
    # The third argument is the number of internal testing networks
    if [[ "$2" != "forge" ]]; then
        get_os "$1"
    fi
    log "Creating kea-$2 node - $1"
    incus launch images:"$1" kea-"$2"
    sleep 3

    if [[ "$2" == "forge" ]]; then
        # This is always ubuntu
        incus exec kea-"$2" -- apt update > "$logFile" 2>&1
        incus exec kea-"$2" -- apt install python3 python3-venv g++ python3-dev libpcap-dev git tcpdump openssh-server -y > "$logFile" 2>&1
        # let's edit ssh config here as well
        printf "Host *\n    StrictHostKeyChecking no\n" > my.conf
        incus file push my.conf kea-forge//etc/ssh/ssh_config.d/my.conf
    else
        update kea-"$2"
        install_base_pkgs kea-"$2"
        prepare_freeradius kea-"$2"
        # TODO take hammer from any branch
        incus exec kea-"$2" -- curl -s -L https://gitlab.isc.org/isc-projects/kea/-/raw/master/hammer.py -o /tmp/hammer.py
        log "Running hammer, output in /tmp/kea-$2-hammer.log"
        # This is a neat trick, commands executed by hammer are still printed to stdout
        incus exec kea-"$2" -- python3 /tmp/hammer.py prepare-system -p local -w mysql pgsql forge shell gssapi netconf > /tmp/kea-"$2"-hammer.log
    fi
}

function create_networks() {
    # The first argument is the number of internal networks
    for i in $(seq 0 $(("$1"-1))); do
        log "Creating network internal-net-$i"
        incus network create internal-net-"$i" ipv4.nat=false ipv6.nat=false ipv4.dhcp=false ipv6.dhcp=false ipv4.firewall=false ipv6.firewall=false
    done
    incus network list
}

function install_pkgs() {
    # The first argument is a node name
    node=$1
    shift
    log "On $node - $usedSystem $osVersion installing packages $*"
    case "$usedSystem" in
        "ubuntu"|"debian")
            incus exec "$node" -- apt install "$@" -y > "$logFile" 2>&1
            ;;
        "rhel"|"fedora")
            incus exec "$node" -- dnf install -y "$@" > "$logFile" 2>&1
            ;;
        "alpine")
            incus exec "$node" -- apk add "$@" > "$logFile" 2>&1
            ;;
        *)
        printf "Not in the list"
        ;;
    esac
}

function update() {
    # The first argument is a node name
    log "Updating $1 - $usedSystem $osVersion"
    case "$usedSystem" in
        "ubuntu"|"debian")
            incus exec "$1" -- apt update  > "$logFile" 2>&1
            incus exec "$1" -- DEBIAN_FRONTEND=noninteractive apt dist-upgrade -y  > "$logFile" 2>&1
            ;;
        "rhel"|"fedora")
            incus exec "$1" -- dnf update -y  > "$logFile" 2>&1
            ;;
        "alpine")
            incus exec "$1" -- apk update  > "$logFile" 2>&1
            incus exec "$1" -- apk upgrade  > "$logFile" 2>&1
            ;;
        *)
        printf "Not in the list"
        ;;
    esac
}

function remove_pkg() {
    # The first argument is a node name
    node=$1
    shift
    log "Removing package on $node - $usedSystem $osVersion"
    case "$usedSystem" in
        "ubuntu"|"debian")
            incus exec "$node" -- apt remove "$@" -y  > "$logFile" 2>&1
            ;;
        "rhel"|"fedora")
            incus exec "$node" -- dnf remove "$@" -y  > "$logFile" 2>&1
            ;;
        "alpine")
            incus exec "$node" -- apk del "$@"  > "$logFile" 2>&1
            ;;
        *)
        printf "Not in the list"
        ;;
    esac
}

function update_nodes() {
    # The first argument is the number of nodes
    for i in $(seq 1 "$1"); do
        update kea-"$i"
    done
}

function attach_node_to_network() {
    # The first argument is network name
    # The second argument is node name
    # The third argument is interface name
    log "Attaching $2 to $1 on interface $3"
    incus network attach "$1" "$2" "$3"
}

function remove_incus_containers() {
    # The first argument is the number of kea nodes
    log "Deleting containers"
    for i in $(seq 1 "$1"); do
        incus delete kea-"$i" --force
    done
    incus delete kea-forge --force
}

function remove_incus_network() {
    # The first argument is the number of internal networks
    for i in $(seq 0 $(("$1"-1))); do
        log "Deleting network internal-net-$i"
        incus network delete internal-net-"$i"
    done
}

function enable_ssh() {
    # The first argument is a node name
    if [[ "$1" == "kea-forge" ]]; then
        incus exec "$1" -- systemctl enable ssh
        incus exec "$1" -- systemctl start ssh
    else
        case "$usedSystem" in
            "ubuntu"|"debian")
                log "Enabling SSH on $1 - ubuntu"
                incus exec "$1" -- systemctl enable ssh
                incus exec "$1" -- systemctl start ssh
                ;;
            "rhel"|"fedora")
                log "Enabling SSH on $1 - fedora"
                incus exec "$1" -- systemctl enable sshd
                incus exec "$1" -- systemctl start sshd
                ;;
            "alpine")
                log "Enabling SSH on $1 - alpine"
                incus exec "$1" -- rc-update add sshd
                incus exec "$1" -- rc-service sshd start
                ;;
            *)
            printf "Not in the list"
            ;;
        esac
    fi
}

function create_user() {
    # The first argument is a node name
    # The second argument is the OS name/OS version, if not provided $usedSystem will be used
    local system=$usedSystem
    if [[ -n "$2" ]]; then
        local system="$2"
    fi
    log "Creating user forge in $1 - $system"
    if [[ "$system" == "fedora" ]]; then
        incus exec "$1" -- useradd -m -s /bin/bash forge
        (printf "test0test1") | incus exec "$1" -- passwd --stdin forge
    else
        incus exec "$1" -- adduser --disabled-password --gecos "" forge
        echo 'forge:test0test1' | incus exec "$1" -- chpasswd
    fi
    enable_ssh "$1"
    printf "forge ALL=(ALL) NOPASSWD:ALL" > nopasswd
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
    log "Checking SSH connection from kea-forge to IP: $1"
    incus exec kea-forge -- sudo -u forge ssh -o StrictHostKeyChecking=accept-new forge@"$1"
}

function migrate_rsa_key() {
    # The first argument is a node name
    log "Migrating RSA key to kea-$1"
    incus exec "$1" -- mkdir -p /home/forge/.ssh
    incus exec "$1" -- chown -R forge:forge /home/forge/.ssh
    incus exec "$1" -- chmod 700 /home/forge/.ssh
    incus file push kea-forge.pub "$1"/home/forge/.ssh/authorized_keys
    incus exec "$1" -- chown forge:forge /home/forge/.ssh/authorized_keys
    incus exec "$1" -- chmod 600 /home/forge/.ssh/authorized_keys
}

function set_address() {
    # The first argument is an address
    # The second argument is an interface name
    # The third argument is a node name
    log "Configuring address $1 for interface $2 on node $3"
    incus exec "$3" -- ip addr add "$1" dev "$2"
    incus exec "$3" -- ip link set "$2" up
}

function configure_internal_network(){
    # The first argument is the number of kea nodes
    # The second argument is the number of internal networks
    for interface in $(seq 1 "$2"); do
        set_address 192.168.5$((interface-1)).240/24 eth"$interface" kea-forge
        set_address 2001:db8:"$interface"::1000/64 eth"$interface" kea-forge
        incus exec kea-forge -- sudo ip -6 route add 2001:db8:"$interface"::/64 dev eth"$interface"
        for node in $(seq 1 "$1"); do
            set_address 192.168.5$((interface-1)).24"$node"/24 eth"$interface" kea-"$node"
            set_address 2001:db8:"$interface"::100"$node"/64 eth"$interface" kea-"$node"
            incus exec kea-"$node" -- sudo ip -6 route add 2001:db8:"$interface"::/64 dev eth"$interface"
        done
    done
}

function add_ip_route() {
    # The first argument is a node name
    # We assume that no matter of the network configuration DNS traffic always
    # goes through first testing network that is using eth1 interface (eht0 is ssh)
    incus exec "$2" -- ip -6 route add 2001:db8:1::/64 dev eth1
    incus exec "$2" -- ip route add 192.168.50.0/24 dev eth1
}

function install_nexus_repo() {
    log "Installing Nexus repository on node $1"
    case "$usedSystem" in
            "ubuntu"|"debian")
                printf "deb https://packages.aws.isc.org/repository/kea-%s/ kea main" "$usedSystem-$osVersion" > kea.list
                incus file push kea.list "$1"/etc/apt/sources.list.d/kea.list
                incus exec kea-"$node" -- curl https://packages.aws.isc.org/repository/repo-keys/repo-key.gpg -o key
                incus exec kea-"$node" -- apt-key add key
                update kea-"$node"
                ;;
            "rhel"|"fedora")
cat << EOF > kea.repo
[nexus]
name=ISC Repo
baseurl=https://packages.aws.isc.org/repository/kea-${usedSystem}-${osVersion}/
enabled=1
gpgcheck=0
EOF
                incus file push kea.repo "$1"/etc/yum.repos.d/kea.repo
                update kea-"$node"
                ;;
            "alpine")
                log_error "Alpine repo in Nexus is not supported, packages will be downloaded and installed locally"
                ;;
            *)
            printf "Not in the list"
            ;;
    esac
}

function install_cloudsmith_repo() {
    log "Installing Cloudsmith repository on node $1"
    log_error "Not implemented yet"
}

function install_kea_pkgs() {
    # The first argument is the number of nodes
    # The second argument is the OS name/OS version
    # The third argument is the kea pkgs version

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

    get_os "$1"
    for node in $(seq 1 "$2"); do
        install_nexus_repo kea-"$node"
        log "Installing kea packages version $pkg_version on node kea-$node on system $usedSystem version $osVersion"
        case "$usedSystem" in
            "ubuntu"|"debian")
                incus exec kea-"$node" -- apt install isc-kea-*="$pkg_version" -y
                ;;
            "rhel"|"fedora")
                local suffix="fc${osVersion}"
                if [[ "$usedSystem" == "rhel" ]]; then
                    suffix="el${osVersion}"
                fi
                incus exec kea-"$node" -- dnf install isc-kea-*-"$pkg_version"."$suffix" -y
                ;;
            "alpine")
                # this is bad, nexus do not provide alpine repo, just raw, we need to first download all pkgs and than install them
                pkg_version=${pkg_version/isc/r}
                local
                rm -rf alpine_pkgs
                mkdir alpine_pkgs
                pkgs=(
                    "isc-kea-dhcp4"
                    "isc-kea-dhcp6"
                    "isc-kea-dhcp-ddns"
                    "isc-kea-hooks"
                    "isc-kea-admin"
                    "isc-kea-ctrl-agent"
                    "isc-kea-common"
                    "isc-kea-mysql"
                    "isc-kea-pgsql"
                    "isc-kea-premium-cb-cmds"
                    "isc-kea-premium-class-cmds"
                    "isc-kea-premium-ddns-tuning"
                    "isc-kea-premium-flex-id"
                    "isc-kea-premium-forensic-log"
                    "isc-kea-premium-gss-tsig"
                    "isc-kea-premium-host-cache"
                    "isc-kea-premium-host-cmds"
                    "isc-kea-premium-lease-query"
                    "isc-kea-premium-limits"
                    "isc-kea-premium-radius"
                    "isc-kea-premium-rbac"
                    "isc-kea-premium-subnet-cmds"
                    "isc-kea-premium-ping-check"
                )
                for pkg in "${pkgs[@]}"; do
                    wget -P alpine_pkgs https://packages.aws.isc.org/repository/kea-"$usedSystem"-"$osVersion"/isc"${pkg_version: -14}"/v"$osVersion"/"$arch"/"$pkg"-"$pkg_version".apk
                done
                incus file push -q -p -r alpine_pkgs kea-"$node"//tmp/.
                for i in "${!pkgs[@]}"; do
                    pkgs[i]="${pkgs[$i]}-${pkg_version}.apk"
                done
                all_pkgs=$(printf "%s " "${pkgs[@]}")
                # this interesting
                # I can't put $all_pkgs in quotes because than command fails
                incus exec kea-"$node" --cwd=/tmp/alpine_pkgs -- apk add $all_pkgs --allow-untrusted
                ;;
            *)
            printf "Not in the list"
            ;;
        esac
    done
    printf '\nINSTALL_METHOD="native"\n' >> init_all.py
}

function remove_kea_pkgs() {
    # The first argument the number of nodes
    for node in $(seq 1 "$1"); do
        log "Removing kea packages on node kea-$node"
        remove_pkg kea-"$node" isc-kea-*
    done
}

function mount_ccache() {
    # The first argument is a node name
    log "Mounting ccache on node $1 using path /mnt/ccache/${usedSystem}/${osVersion}"
    case "$usedSystem" in
        "alpine")
        incus config device add "$1" ccache disk source=/mnt/ccache-alp-bsd/"${usedSystem}/${osVersion}"/amd64 path=/ccache readonly=false
        ;;
        *)
        incus config device add "$1" ccache disk source=/mnt/ccache/"${usedSystem}/${osVersion}"/amd64 path=/ccache readonly=false
        ;;
    esac
    cat << EOF > ccache.conf
cache_dir = /ccache
temporary_dir = /tmp/ccache/
compiler_check = content
EOF
    incus exec "$1" -- mkdir -p .ccache
    incus file push -q ccache.conf "$1"//root/.ccache/ccache.conf
}

function install_kea_tarball() {
    # The first argument is the number of nodes
    # The second argument is the path to directory with kea source code - jenkins is providing kea source code in ~/kea with hammer.
    # it's just needs to be copied to the kea nodes and installed
    for node in $(seq 1 "$1"); do
        log "Installing kea from the source code on node kea-$node - $usedSystem $osVersion"
        incus exec kea-"$node" -- rm -rf /tmp/kea
        incus file push -r -q "$2" kea-"$node"//tmp/.
        incus exec kea-"$node" --cwd=/tmp/kea -- python3 hammer.py build -p local -w ccache,forge,install,mysql,pgsql,shell,gssapi,netconf -x docs,perfdhcp,unittest --ccache-dir /ccache #
    done
    printf '\nINSTALL_METHOD="make"\n' >> init_all.py
}

function print_summary() {
    log "Testing setup summary:"
    incus image list
    incus list -cns46tSDM
    incus network list
}

function check_installed_kea() {
    # The first argument is a node name
    for node in $(seq 1 "$1"); do
        log "Checking kea-dhcp4 on kea-$node"
        incus exec kea-"$node" -- kea-dhcp4 -V
        log "Checking kea-dhcp6 on kea-$node"
        incus exec kea-"$node" -- kea-dhcp6 -V
        log "Checking kea-dhcp-ddns on kea-$node"
        incus exec kea-"$node" -- kea-dhcp-ddns -V
    done
}

function get_kea_pkg_version() {
    # TODO detect version from a file or just use major versioning e.g. 2.6.1; 2.7.8
    # use: pkg_version=$(get_kea_pkg_version)
    # printf head -n1 ubuntu-22.04-amd64-pkgs.txt | perl -nle 'm/([0-9\\.]+-isc[0-9]+)/; print \$1'
    printf ''
}

function upload_pytest() {
    # no arguments needed
    rm -rf tests_results
    incus file push -r -q . kea-forge//home/forge/.
}

function setup_forge() {
    # no arguments needed
    log "Setting up forge in kea-forge - ubuntu"
    upload_pytest
    incus exec kea-forge -- sudo -u forge python3 -m venv /home/forge/venv-client-node
    incus exec kea-forge -- sudo -u forge /home/forge/venv-client-node/bin/pip install -r /home/forge/requirements.txt
    create_forge_init
    python3 modify_init_all.py
}

function run_pytest() {
    # Check arguments, if --upload-pytest is present, upload the pytest files to kea-forge
    # than run pytest with the rest of the arguments

    local args=("$@")
    local new_args=()

    for arg in "${args[@]}"; do
        if [[ "$arg" == "--upload-pytest" ]]; then
            log "Uploading forge source code to kea-forge"
            upload_pytest
        else
            new_args+=("$arg")
        fi
    done
    incus file push init_all.py kea-forge/home/forge/init_all.py
    log "Running pytest.."
    incus exec kea-forge --cwd=/home/forge -- sudo /home/forge/venv-client-node/bin/pytest "${new_args[@]}"
    get_results
}

function get_results() {
    log "Downloading results from kea-forge"
    incus file pull -r -q kea-forge/home/forge/tests_results .
}

function get_from_kea_forge() {
    log "Downloading $1 from kea-forge"
    rm -rf "$1"
    incus file pull -r kea-forge//home/forge/"$1" .
}

function create_forge_init() {
    log "Creating partial forge init script"

cat << EOF > init_all.py
LOGLEVEL = "info"
IFACE = "eth1"
SERVER_IFACE = "eth1"
SERVER2_IFACE = "eth1"
SOFTWARE_UNDER_TEST = "kea4_server", "bind9_server",
SOFTWARE_INSTALL_PATH = "/usr/local"
DB_TYPE = "memfile"
SHOW_PACKETS_FROM = ""
REL4_ADDR = "0.0.0.0"
CLI_LINK_LOCAL = ""
copylist = []
removelist = []
OUTPUT_WAIT_INTERVAL = 2
OUTPUT_WAIT_MAX_INTERVALS = 3
PACKET_WAIT_INTERVAL = 3
HISTORY = True
TCPDUMP = True
TCPDUMP_PATH = ""
TCPDUMP_ON_REMOTE_SYSTEM = False
SAVE_CONFIG_FILE = True
AUTO_ARCHIVE = False
SLEEP_TIME_1 = 2
SLEEP_TIME_2 = 4
MGMT_USERNAME = "forge"
MGMT_PASSWORD = "test0test1"
MGMT_PASSWORD_CMD = ""
SAVE_LOGS = True
BIND_LOG_TYPE = "ERROR"
BIND_LOG_LVL = 0
BIND_MODULE = "*"
SAVE_LEASES = True
DNS_IFACE = "eth1"
DNS_PORT = 53
DNS_SERVER_INSTALL_PATH = "/usr/sbin/"
ISC_DHCP_LOG_FACILITY = "local7"
ISC_DHCP_LOG_FILE = "/var/log/forge_dhcpd.log"
DB_NAME = "keadb"
DB_USER = "keauser"
DB_PASSWD = "keapass"
DB_HOST = ""
FABRIC_PTY = False
MULTI_THREADING_ENABLED = True
FORGE_VERBOSE = False
DISABLE_DB_SETUP = False
EOF

if [[ "$usedSystem" == "fedora" ]]; then
    printf "DNS_DATA_PATH = \"/etc/\"" >> init_all.py
else
    printf "DNS_DATA_PATH = \"/etc/bind/\"" >> init_all.py
fi
}

function help() {
    printf "Usage: %s {prepare-env|delete|stop} [arguments...]\n" "$0"
    printf "       %s prepare-env <OS-name/OS-version> <number-of-kea-nodes> <number-of-internal-networks>\n" "$0"
    printf "            %s prepare-env ubuntu/24.04 2 2\n" "$0"
    printf "       %s clear-all <number-of-kea-nodes> <number-of-internal-networks>\n" "$0"
    printf "            %s clear-all 2 1\n" "$0"
    printf "       %s install-kea-pkgs <OS-name/OS-version> <number-of-kea-nodes> <kea-pkgs-version>\n" "$0"
    printf "            %s install-kea-pkgs ubuntu/24.04 2 2.7.3-isc20240903092214\n" "$0"
    printf "       %s install-kea-tarball <number-of-kea-nodes> <path-to-source-code>\n" "$0"
    printf "            %s install-kea-tarball 2 ~/kea\n" "$0"
    printf "       %s update-pytest\n" "$0"
    printf "       %s run-pytest <pytest-arguments>\n" "$0"
    printf "            %s run-pytest -vv tests/dhcp/test_options.py::test_v4_never_send_various_combinations\n" "$0"
    printf "            to reupload forge before executing tests add --upload-pytest option to run-pytest\n"
    printf "            %s run-pytest -vv tests/dhcp/test_options.py::test_v4_never_send_various_combinations --upload-pytest\n" "$0"
    exit 1
}

if [[ $# -lt 1 ]]; then
    help
fi

command=$1
shift
case "$command" in
    cache-images)
        # let's download images to cache it locally
        incus image copy images:ubuntu/24.04 local:
        incus image copy images:fedora/40 local:
        incus image copy images:alpine/3.20 local:
        incus image list
        ;;
    prepare-env)
        # print incus configuration
        incus admin init --dump
        # start kea nodes kea-1 kea-2 etc
        startTime=$(date +%s)
        osName=$1
        numberOfNodes=$2
        numberOfNetworks=$3
        for i in $(seq 1 "$numberOfNodes"); do
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
        for i in $(seq 1 "$numberOfNodes"); do
            for x in $(seq 1 "$numberOfNetworks"); do
                attach_node_to_network internal-net-$((x-1)) kea-"$i" eth"$x"
            done
        done
        # create main user in kea-forge and generate key
        create_user kea-forge ubuntu
        generate_rsa_key
        # create users in other nodes and migrate key
        for i in $(seq 1 "$numberOfNodes"); do
            create_user kea-"$i"
            migrate_rsa_key kea-"$i"
            mount_ccache kea-"$i"
        done
        configure_internal_network "$numberOfNodes" "$numberOfNetworks"
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
    check-ssh)
        check_ssh "$@"
        ;;
    check-kea)
        check_installed_kea "$@"
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
    update-pytest)
        rm -rf tests_results
        incus file push -r -q . kea-forge/home/forge/
        ;;
    run-pytest)
        run_pytest "$@"
        ;;
    get-from-kea-forge)
        get_from_kea_forge "$@"
        ;;
    *)
        printf "Unknown command: %s\n" "$command"
        help
        ;;
esac
