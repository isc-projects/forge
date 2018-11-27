# Copyright (C) 2014 Internet Systems Consortium.
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND INTERNET SYSTEMS CONSORTIUM
# DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# INTERNET SYSTEMS CONSORTIUM BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
# FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
# WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# Author: Maciek Fijalkowski


from features.softwaresupport.multi_server_functions import fabric_sudo_command, \
    fabric_send_file, fabric_run_command, fabric_remove_file_command, fabric_download_file, \
    remove_local_file
from logging_facility import *
from lettuce.registry import world
############################################################################
#from init_all import  IFACE
#TODO That import have to be switched to ForgeConfiguration class, world.f_cfg
IFACE = ""
DHCP = ""
############################################################################


try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def restart_clnt(step):
    """
    This function shut downs and later starts dibbler-client on DUT.
    @step("Restart client.")
    """
    fabric_sudo_command("(" + os.path.join(world.f_cfg.software_install_path, "dibbler-client") + " stop); sleep 1;")
    fabric_sudo_command("(" + os.path.join(world.f_cfg.software_install_path, "dibbler-client") + " start); sleep 1;")


def stop_clnt():
    """
    Command that shut downs one instance of running dibbler-client on DUT.
    """
    fabric_sudo_command("(" + os.path.join(world.f_cfg.software_install_path, "dibbler-client") + " stop); sleep 1;")

def kill_clnt():
    """
    Command that stops every instance of dibbler-client being run on a
    DUT.
    """
    fabric_run_command("sudo killall dibbler-client &>/dev/null")

def create_clnt_cfg():
    """
    This command generates a starting template for dibbler-client config
    file. Config is stored in variable and will be handled by other
    functions.
    """
    openBracket = "{"
    closeBracket = "}"
    eth = IFACE
    world.clntCfg["config"] = """log-level 8
log-mode precise
duid-type duid-llt
iface {eth} {openBracket}""".format(**locals())


def release_command():
    """
    This command is used when there's a need to sniff a RELEASE message
    sent by dibbler client. That happens when, for example, client is
    shut down. So This is basically the same as starting dibbler-client -
    running a script that executes a command with some delay. Whole thing
    is necessary, because firstly we need to start sniffing for particular
    message. On shutdown, dibbler-client sends exactly one RELEASE message.
    """
    world.clntCfg["script"] = ""
    make_script("stop")
    get_common_logger().debug("Stopping Dibbler Client and waiting for RELEASE.")
    fabric_send_file(world.clntCfg["script"], os.path.join(world.f_cfg.software_install_path, 'comm.sh'))
    fabric_run_command ('(rm nohup.out; nohup bash ' \
                        + os.path.join(world.f_cfg.software_install_path, 'comm.sh') + ' &); sleep 3;')


def client_option_req(step, another1, opt):
    """
    @step("Client is configured to include (another )?(\S+) option.")

    This function adds option that client requests to default interface
    in order to add another IA_PD option to client's config,
    another1 flag must be set to true; it's not needed for adding
    next ia_prefix options.
    Supported options:
    - IA_PD
    - IA_Prefix
    - rapid_commit
    - insist_mode

    """
    openBracket = "{"
    closeBracket = "}"
    t1 = world.clntCfg["values"]["T1"]
    t2 = world.clntCfg["values"]["T2"]
    preflft = world.clntCfg["values"]["preferred-lifetime"]
    validlft = world.clntCfg["values"]["valid-lifetime"]
    prefix = world.clntCfg["values"]["prefix"]
    prefix_len = world.clntCfg["values"]["prefix-len"]
    assert opt is not None, "No option given."

    if another1:
        world.clntCfg["config"] += """\n{closeBracket}\n""".format(**locals())
    if opt == "IA_PD":
        world.clntCfg["config"] += """\n    pd {openBracket}
        T1 {t1}
        T2 {t2}
        """.format(**locals())
    elif opt == "IA_Prefix":
        world.clntCfg["config"] += """
        prefix {prefix} / {prefix_len} {openBracket}
            preferred-lifetime {preflft}
            valid-lifetime {validlft}
        {closeBracket}
        """.format(**locals())
    elif opt == "rapid_commit":
        world.clntCfg["config"] += """  rapid-commit yes"""
    elif opt == "insist_mode":
        world.clntCfg['insist'] = True


def make_script(option):
    """
    This function generates a script that will be executed on DUT.
    It is used for starting client and when there's a need to sniff
    a RELEASE message. Without the delay provided by this script, dibbler-client
    was starting before sniffing was started. It resulted in sniffing not
    first SOLICIT sent by client, but the second one. Later, client was
    ignoring any preference options in ADVERTISE messages.
    option argument can be equal to "start" or "stop".
    """
    world.clntCfg["content"] = "!#/bin/sh\nsleep 10;\n"
    world.clntCfg["content"] += "sudo " + os.path.join(world.f_cfg.software_install_path, "dibbler-client") + " " + str(option) + "&\n"
    world.clntCfg["script"] = "temp1"
    script = open(world.clntCfg["script"], "w")
    script.write(world.clntCfg["content"])
    script.close()


def write_clnt_cfg_to_file():
    """
    This function creates a valid config file from config template
    stored in variable. It also checks for equal count of brackets,
    in order to satisfy a config parser.
    """
    # check if there are equal count of open/closing brackets
    openCount = world.clntCfg["config"].count("{")
    closeCount = world.clntCfg["config"].count("}")
    # write generated config to a file
    world.clntCfg["Filename"] = "temp"
    cfgFile = open(world.clntCfg["Filename"], "w")
    cfgFile.write(world.clntCfg["config"])
    # check for insist-mode in dibbler
    if world.clntCfg['insist']:
        cfgFile.seek(0,0)
        cfgFile.write("insist-mode\n")
        world.clntCfg['insist'] = False
    while closeCount < openCount:
        cfgFile.seek(0,2)
        cfgFile.write("\n}\n")
        closeCount += 1
    cfgFile.close()


def client_setup(step):
    """
    @step("Setting up test.")

    This function provides a lettuce step for initializing clients' config.
    """
    create_clnt_cfg()


def client_parse_config(step, contain):
    """
    @step("Client MUST (NOT )?use prefix with values given by server.")
    This step creates a structure similar to structure returned
    by iscpy.ISCParseString function; it is easier to
    play with parsing xml, so we won't touch that much
    isc's dhclient dict;
    """
    result = {}
    result['lease6'] = {}
    world.clntCfg['lease_file'] = world.cfg["dir_name"] + "/dibbler_lease.xml"
    fabric_download_file("/var/lib/dibbler/client-AddrMgr.xml", world.clntCfg['lease_file'])
    tree = ET.ElementTree(file=world.clntCfg['lease_file'])
    root = tree.getroot()
    pdList = [iapd for iapd in root.iter() if iapd.tag == "AddrPD"]
    if len(pdList) > 0:
        for pd in pdList:
            pdDict = {}
            pdDict['renew'] = "\"" + pd.attrib['T1'] + "\""
            pdDict['rebind'] =  "\"" + pd.attrib['T2'] + "\""
            prefixList = [prefix for prefix in pd.getchildren() if prefix.tag == "AddrPrefix"]
            for prefix in prefixList:
                prefixDict = {}
                prefixDict['preferred-life'] ="\"" + prefix.attrib['pref'] + "\""
                prefixDict['max-life'] = "\"" + prefix.attrib['valid'] + "\""
                pdDict['iaprefix ' + "\"" + prefix.text + '/' + prefix.attrib['length'] +
                       "\""] = dict(prefixDict)
            result['lease6']['ia-pd ' + "\"" + pd.attrib['IAID'] + "\""] = dict(pdDict)
    """
    print result
    print "\n\n\n"
    print world.clntCfg['scapy_lease']
    print "\n\n\n"
    """
    if contain:
        assert result == world.clntCfg['scapy_lease'], "leases are different."
    else:
        assert result != world.clntCfg['scapy_lease'], "leases are the same," \
                                                       " but they should not be."


def start_clnt(step):
    """
    @step("Client is started.")

    Lettuce step for writing config to file, sending it and starting client.
    """
    world.clntCfg["keep_lease"] = False
    world.clntCfg["log_file"] = "/var/log/dibbler/dibbler-client.log"
    write_clnt_cfg_to_file()
    make_script("start")
    get_common_logger().debug("Starting Dibbler Client with generated config:")
    fabric_send_file(world.clntCfg["Filename"], '/etc/dibbler/client.conf')
    fabric_send_file(world.clntCfg["script"], os.path.join(world.f_cfg.software_install_path, 'comm.sh'))
    fabric_remove_file_command(world.clntCfg["Filename"])
    # start client with clean log file
    fabric_remove_file_command(world.clntCfg["log_file"])
    fabric_run_command ('(rm nohup.out; nohup bash ' \
                        + os.path.join(world.f_cfg.software_install_path, 'comm.sh') + ' &); sleep 3;')


# that could be use for making terrain.py even more generic ;)
def stop_srv():
    stop_clnt()


# We probably should use those functions
def save_leases():
    world.clntCfg["keep_lease"] = True


def save_logs():
    fabric_download_file(world.clntCfg["log_file"], world.cfg["dir_name"] + \
                         "/dibbler-client.log")


def clear_all():
    fabric_remove_file_command(os.path.join(world.f_cfg.software_install_path, 'comm.sh'))
    fabric_remove_file_command('/etc/dibbler/client.conf')
    remove_local_file(world.clntCfg["Filename"])
    remove_local_file(world.clntCfg["script"])
    if not world.clntCfg["keep_lease"] and world.clntCfg['lease_file'] is not "":
        remove_local_file(world.clntCfg['lease_file'])
