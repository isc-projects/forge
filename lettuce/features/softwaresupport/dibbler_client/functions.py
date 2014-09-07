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
    fabric_send_file, fabric_run_command, fabric_remove_file_command, fabric_download_file
from logging_facility import *
from lettuce.registry import world
from init_all import DIBBLER_INSTALL_DIR, IFACE
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

def restart_clnt(step):
    fabric_sudo_command("("+DIBBLER_INSTALL_DIR+"dibbler-client stop); sleep 1;")
    fabric_sudo_command("("+DIBBLER_INSTALL_DIR+"dibbler-client start); sleep 1;")


def stop_clnt():
    fabric_sudo_command ("("+DIBBLER_INSTALL_DIR+"dibbler-client stop); sleep 1;")

def kill_clnt():
    fabric_run_command("sudo killall dibbler-client &>/dev/null")

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


def client_option_req(step, another1, opt):
    # add option that client requests to default interface
    # in order to add another IA_PD option to client's config,
    # another1 flag must be set to true; it's not needed for adding
    # next ia_prefix options.
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
    # step for initializing client config
    create_clnt_cfg()


def client_parse_config(step, contain):
    # create a structure similar to structure returned
    # by iscpy.ISCParseString function; it is easier to
    # play with parsing xml, so we won't touch that much
    # isc's dhclient dict; 
    # it looks ugly, but it works...
    result = {}
    result['lease6'] = {}
    fabric_download_file("/var/lib/dibbler/client-AddrMgr.xml", "prefix_file")
    tree = ET.ElementTree(file='prefix_file')
    root = tree.getroot()
    pdList = [iapd for iapd in root.iter() if iapd.tag == "AddrPD"]
    if len(pdList) > 0:
        for pd in pdList:
            pdDict = {}
            pdDict['renew'] = '''"''' + pd.attrib['T1'] + '''"'''
            pdDict['rebind'] =  '''"''' + pd.attrib['T2'] + '''"'''
            prefixList = [prefix for prefix in pd.getchildren() if prefix.tag == "AddrPrefix"]
            for prefix in prefixList:
                prefixDict = {}
                prefixDict['preferred-life'] ='''"''' + prefix.attrib['pref'] + '''"'''
                prefixDict['max-life'] = '''"''' + prefix.attrib['valid'] + '''"'''
                pdDict['iaprefix ' + '''"''' + prefix.text + '/' + prefix.attrib['length'] +
                       '''"'''] = dict(prefixDict)
            result['lease6']['ia-pd ' + '''"''' + pd.attrib['IAID'] + '''"'''] = dict(pdDict)
    print result
    print "\n\n\n"
    print world.clntCfg['scapy_lease'] 
    print "\n\n\n"
    if contain:
        assert result == world.clntCfg['scapy_lease'], "leases are different."
    else:
        assert result != world.clntCfg['scapy_lease'], "leases are the same, but they should not be."


def start_clnt(step):
    # step for writing config to file, send it and start client
    write_clnt_cfg_to_file()
    make_script()
    get_common_logger().debug("Starting Dibbler Client with generated config:")
    fabric_send_file(world.clntCfg["Filename"], '/etc/dibbler/client.conf')
    fabric_send_file(world.clntCfg["script"], DIBBLER_INSTALL_DIR+'comm.sh')
    fabric_remove_file_command(world.clntCfg["Filename"])
    fabric_run_command ('(rm nohup.out; nohup bash '+DIBBLER_INSTALL_DIR+'comm.sh &); sleep 1;')


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
