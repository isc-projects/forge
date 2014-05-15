from features.softwaresupport.multi_server_functions import fabric_sudo_command, \
    fabric_send_file, fabric_run_command, fabric_remove_file_command
from logging_facility import *
from lettuce.registry import world
from init_all import DIBBLER_INSTALL_DIR, IFACE


def restart_clnt(step):
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
iface {eth} {openBracket}""".format(**locals())


# release message; work on it!
def release_command():
    fabric_sudo_command("("+DIBBLER_INSTALL_DIR+"dibbler-client stop); sleep 1;")


def client_option_req(step, opt):
    # add option that client requests to default interface
    openBracket = "{"
    closeBracket = "}"
    t1 = world.clntCfg["values"]["T1"]
    t2 = world.clntCfg["values"]["T2"]
    preflft = world.clntCfg["values"]["preferred-lifetime"]
    validlft = world.clntCfg["values"]["valid-lifetime"]
    prefix = world.clntCfg["values"]["prefix"]
    prefix_len = world.clntCfg["values"]["prefix-len"]
    assert opt is not None, "No option given."


    if opt == "IA_PD":
        world.clntCfg["config"] += """\n    pd {openBracket}
        T1 {t1}
        T2 {t2}
    {closeBracket}""".format(**locals())
    elif opt == "IA_Prefix":
        world.clntCfg["config"] += """\n    pd {openBracket}
        T1 {t1}
        T2 {t2}
        prefix {openBracket}
            preferred-lifetime {preflft}
            valid-lifetime {validlft}
        {closeBracket}
    {closeBracket}""".format(**locals())
    elif opt == "rapid_commit":
        world.clntCfg["config"] += """  rapid-commit yes"""


def make_script():
    world.clntCfg["content"] = "!#/bin/sh\nsleep 10;\n"
    world.clntCfg["content"] += "sudo " + DIBBLER_INSTALL_DIR + "dibbler-client start &\n"
    world.clntCfg["script"] = "temp1"
    script = open(world.clntCfg["script"], "w")
    script.write(world.clntCfg["content"])
    script.close()


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


def client_setup(step):
    # step for initializing client config
    create_clnt_cfg()


def start_clnt(step):
    # step for writing config to file, send it and start client
    write_clnt_cfg_to_file()
    make_script()
    get_common_logger().debug("Starting Dibbler Client with generated config:")
    fabric_send_file(world.clntCfg["Filename"], '/etc/dibbler/client.conf')
    fabric_send_file(world.clntCfg["script"], DIBBLER_INSTALL_DIR+'comm.sh')
    fabric_remove_file_command(world.clntCfg["Filename"])
    fabric_run_command ('(rm nohup.out; nohup bash '+DIBBLER_INSTALL_DIR+'comm.sh &); sleep 1;')