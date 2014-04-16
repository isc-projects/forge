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


def prepare_cfg_default_clnt():
   world.clntCfg = {}
   world.clntCfg["Filename"] = "temp"
   cfgFile = open(world.clntCfg["Filename"], "w")
   openBracket = "{"
   closeBracket = "}"
   eth = IFACE
   config = """log-level 8
log-mode syslog
duid-type duid-llt
iface {eth} {openBracket}
    pd {openBracket}
    {closeBracket}
{closeBracket}
   """.format(**locals())
   cfgFile.write(config)
   cfgFile.close()


def start_clnt():
   # stop_clnt()
   prepare_cfg_default_clnt()
   get_common_logger().debug("Starting Dibbler Client with generated config:")
   fabric_send_file(world.clntCfg["Filename"], '/etc/dibbler/client.conf')
   fabric_remove_file_command(world.clntCfg["Filename"])
   fabric_run_command ('(rm nohup.out; nohup '+DIBBLER_INSTALL_DIR+'dibbler-client start & ); sleep 2;')
   # stop_clnt()
