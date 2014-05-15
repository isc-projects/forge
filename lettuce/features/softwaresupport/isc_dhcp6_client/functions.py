from features.softwaresupport.multi_server_functions import fabric_sudo_command, \
    fabric_send_file, fabric_run_command, fabric_remove_file_command
from logging_facility import *
from lettuce.registry import world
from init_all import SOFTWARE_INSTALL_DIR, IFACE

def prepare_default_command():
    build_leases_path()
    build_config_path()
    world.clntCfg["command"] = SOFTWARE_INSTALL_DIR + 'sbin/dhclient -6 -v ' + IFACE + " -lf " + \
                               world.clntCfg["leases"] + " -cf " + world.clntCfg["confpath"]


def build_leases_path():
    world.clntCfg["leases"] = SOFTWARE_INSTALL_DIR + "dhclient.leases"

def build_config_path():
    world.clntCfg["confpath"] = SOFTWARE_INSTALL_DIR + "dhclient.conf"


def clean_leases():
    fabric_run_command('echo y | rm ' + world.clntCfg['leases'])
    fabric_run_command('touch ' + world.clntCfg['leases'])


def create_clnt_cfg():
    # generate a default config for client
    world.clntCfg["config"] = "# Config file for ISC-DHCPv6 client\n"
    openBracket = "{"
    closeBracket = "}"
    eth = IFACE
    world.clntCfg["config"] += """interface "{eth}" {openBracket} \n\trequest;""".format(**locals())


def write_clnt_cfg_to_file():
    # check if there are equal count of open/closing brackets
    openCount = world.clntCfg["config"].count("{")
    closeCount = world.clntCfg["config"].count("}")
    if openCount == closeCount + 1:
        world.clntCfg["config"] += "\n}\n"
    # write generated config to a file
    world.clntCfg["Filename"] = "temp"
    cfgFile = open(world.clntCfg["Filename"], "w")
    cfgFile.write(world.clntCfg["config"])
    cfgFile.close()


def restart_clnt(step):
    stop_clnt()
    # clean_leases()  ## ?
    fabric_sudo_command('(rm nohup.out; nohup ' + world.clntCfg["command"] + ' & ); sleep 1;')


def stop_clnt():
    fabric_run_command("sudo killall dhclient &>/dev/null")


# release message; work on it!
def release_command():
    fabric_sudo_command('(rm nohup.out; nohup ' + world.clntCfg["command"] + ' -r & ); sleep 1;')


def client_option_req(step, opt):
    if opt == "IA_PD":
        if "command" not in world.clntCfg.keys():
            prepare_default_command()
        world.clntCfg["command"] += " -P"
    elif opt == "rapid_commit":
        world.clntCfg["config"] += "\n  send dhcp6.rapid-commit;"

def client_setup(step):
    prepare_default_command()
    create_clnt_cfg()


def make_script():
    world.clntCfg["content"] = "!#/bin/sh\nsleep 10;\n"
    world.clntCfg["content"] += world.clntCfg["command"] + " &\n"
    world.clntCfg["script"] = "temp1"
    script = open(world.clntCfg["script"], "w")
    script.write(world.clntCfg["content"])
    script.close()


def start_clnt(step):
    write_clnt_cfg_to_file()
    make_script()
    get_common_logger().debug("Start dhclient6 with generated config:")
    clean_leases()
    fabric_send_file(world.clntCfg["Filename"], SOFTWARE_INSTALL_DIR + "dhclient.conf")
    fabric_send_file(world.clntCfg["script"], SOFTWARE_INSTALL_DIR + "comm.sh")
    fabric_remove_file_command(world.clntCfg["Filename"])
    # fabric_sudo_command('(rm nohup.out; nohup ' + world.clntCfg["command"] + ' & ); sleep 1;')
    fabric_sudo_command('(rm nohup.out; nohup bash ' + SOFTWARE_INSTALL_DIR + 'comm.sh &); sleep 1;')