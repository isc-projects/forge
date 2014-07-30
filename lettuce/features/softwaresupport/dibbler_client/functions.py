from features.softwaresupport.multi_server_functions import fabric_sudo_command, \
    fabric_send_file, fabric_run_command, fabric_remove_file_command
from logging_facility import *
from lettuce.registry import world
from init_all import DIBBLER_INSTALL_DIR, IFACE


def restart_clnt():
    fabric_sudo_command("("+DIBBLER_INSTALL_DIR+"dibbler-client stop); sleep 1;")
    fabric_sudo_command("("+DIBBLER_INSTALL_DIR+"dibbler-client start); sleep 1;")


def stop_clnt():
    fabric_sudo_command ("("+DIBBLER_INSTALL_DIR+"dibbler-client stop); sleep 1;")


def create_clnt_cfg():
    # generate a default config for client
    openBracket = "{"
    closeBracket = "}"
    eth = IFACE
    world.clntCfg["config"] = """log-level 8
log-mode syslog
duid-type duid-llt
iface {eth} {openBracket}
{closeBracket}""".format(**locals())


def client_option_req(step, opt):
    # add option that client requests to default interface
    openBracket = "{"
    closeBracket = "}"
    assert opt is not None, "No option given."

    # delete closing bracket from iface scope,
    # then add proper option and close the iface scope
    input_idx = len(world.clntCfg["config"])-1
    world.clntCfg["config"] = world.clntCfg["config"][:input_idx]
    if opt == "IA_PD":
        world.clntCfg["config"] += """    pd {openBracket}
        prefix {openBracket}
            preferred-lifetime 1000
            valid-lifetime 2000
        {closeBracket}
    {closeBracket}
{closeBracket}""".format(**locals())


def write_clnt_cfg_to_file():
    # write generated config to a file
    world.clntCfg["Filename"] = "temp"
    cfgFile = open(world.clntCfg["Filename"], "w")
    cfgFile.write(world.clntCfg["config"])
    cfgFile.close()


def client_setup(step):
    # step for initializing client config
    create_clnt_cfg()


def start_clnt(step):
    # step for writing config to file, send it and start client
    write_clnt_cfg_to_file()
    get_common_logger().debug("Starting Dibbler Client with generated config:")
    fabric_send_file(world.clntCfg["Filename"], '/etc/dibbler/client.conf')
    fabric_remove_file_command(world.clntCfg["Filename"])
    fabric_run_command ('(rm nohup.out; nohup '+DIBBLER_INSTALL_DIR+'dibbler-client start & ); sleep 2;')


# that could be use for making terrain.py even more generic ;)
def stop_srv():
    stop_clnt()


# We probably should use those functions
def save_leases():
    assert False, "TODO!"


def save_logs():
    assert False, "TODO!"


def clear_all():
    assert False, "TODO!"
