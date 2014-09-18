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
from init_all import SOFTWARE_INSTALL_DIR, IFACE
from features.softwaresupport.core import *


def prepare_default_command():
    """
    This function stores a command that is used to run a dhclient on DUT.
    It specifies a lease file and a config file.
    """
    build_leases_path()
    build_config_path()
    world.clntCfg["log_file"] = SOFTWARE_INSTALL_DIR + "dhclient.log"
    world.clntCfg["command"] = SOFTWARE_INSTALL_DIR + 'sbin/dhclient -6 -v ' \
                               + IFACE + " -lf " +  world.clntCfg["leases"] + \
                               " -cf " + world.clntCfg["confpath"] + " -P &> " + \
                               world.clntCfg["log_file"] + " &"


def build_leases_path():
    """
    This small function stores in variable a path for leases file.
    """
    world.clntCfg["leases"] = SOFTWARE_INSTALL_DIR + "dhclient.leases"


def build_config_path():
    """
    This small function stores in variable a path for config file.
    """
    world.clntCfg["confpath"] = SOFTWARE_INSTALL_DIR + "dhclient.conf"


def clean_leases():
    """
    Function that executes command on DUT, which removes the old lease
    file and creates an empty, new one.
    """
    fabric_run_command('echo y | rm ' + world.clntCfg['leases'])
    fabric_run_command('touch ' + world.clntCfg['leases'])


def create_clnt_cfg():
    """
    Function that stores in variable a template for config file
    that is being generated.
    """
    world.clntCfg["config"] = "# Config file for ISC-DHCPv6 client\n"
    openBracket = "{"
    closeBracket = "}"
    eth = IFACE
    world.clntCfg["config"] += """interface "{eth}" {openBracket} \n\trequest;""".format(**locals())


def write_clnt_cfg_to_file():
    """
    Function creates a config file from previously specified template.
    It checks whether there are equal count of open/closing brackets.
    """
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
    """
    This function shut downs and later starts dhclient on DUT.
    @step("Restart client.")
    """
    stop_clnt()
    # clean_leases()  ## ?
    fabric_sudo_command('(rm nohup.out; nohup ' + \
                        world.clntCfg["command"] + ' & ); sleep 1;')


def stop_clnt():
    """
    This function destroys every running instance of dhclient on DUT.
    """
    fabric_run_command("sudo killall dhclient &>/dev/null")


def kill_clnt():
    """
    Same as stop_clnt().
    """
    stop_clnt()


def release_command():
    """
    Function that executes a previously generated command with "-r" 
    option, which results in sending by dhclient RELEASE repeatedly, until
    REPLY is received. There's no need to execute it with delay like in
    dibbler-client's case, since message will being retransmitted.
    """
    fabric_sudo_command('(rm nohup.out; nohup ' + \
                        world.clntCfg["command"] + ' -r & ); sleep 1;')


def client_option_req(step, another1, opt):
    """
    @step("Client is configured to include (another )?(\S+) option.")

    Lettuce step for adding particular option to dhclient's config file.
    Currently only supported options are IA_PD and rapid_commit.
    """
    if opt == "IA_PD":
        if "command" not in world.clntCfg.keys():
            prepare_default_command()
        world.clntCfg["command"] += " -P"
    elif opt == "rapid_commit":
        world.clntCfg["config"] += "\n  send dhcp6.rapid-commit;"


def client_setup(step):
    """
    @step("Setting up test.")

    This function provides a lettuce step for initializing clients' config.
    """
    prepare_default_command()
    create_clnt_cfg()


def make_script():
    """
    Function creates a script file that will execute a previously created
    command with delay. Execution will take place on DUT. It is important
    to sniff first SOLICIT message sent by client, hence the delay.
    See also more detailed description of it in dibbler_client/functions.py.
    """
    world.clntCfg["content"] = "!#/bin/sh\nsleep 10;\n"
    world.clntCfg["content"] += world.clntCfg["command"] + " &\n"
    world.clntCfg["script"] = "temp1"
    script = open(world.clntCfg["script"], "w")
    script.write(world.clntCfg["content"])
    script.close()

def client_parse_config(step, contain):
    """
    @step("Client MUST (NOT )?use prefix with values given by server.")

    Step firstly downloads a lease file from DUT. Then, the needed parts
    are further parsed and specific lease structure is created. 
    """
    world.clntCfg["lease_file"] = world.cfg["dir_name"] + "/dhclient.leases"
    fabric_download_file(world.clntCfg["leases"], world.clntCfg["lease_file"])
    file_ = open(world.clntCfg["lease_file"],"r").readlines()
    count = 0
    # remove things that we do not want
    for line in list(file_):
        if "lease6" not in line:
            del(file_[count])
            count += 1
        else:
            break
    count = 0
    for line in list(file_):
        if "option" in line:
            del(file_[count])
        else:
            count += 1

    # add required quotes and semicolons to file;
    # it needs to have a dhcpd.conf syntax in order
    # to got accepted by ParseISCString function;
    copied = []
    for line in file_:
        line = line.lstrip().rstrip("\n")
        line = line.split(" ")
        if len(line) > 1:
            if line[1][0].isdigit():
                if line[1][-1] is ";":
                    line[1] = '''"''' + line[1][:len(line[1])-1] + '''"''' + line[1][-1]
                else:
                    line[1] = '''"''' + line[1] + '''"'''
        elif line[0] == "}":
            line[0] += ";"
        copied.append(line)
    
    copied = [" ".join(line) + "\n" for line in copied]
    result = " ".join(copied)
    parsed = ParseISCString(result)
    if 'lease6' in parsed:
        del(parsed['lease6']['interface'])
        for entry in parsed['lease6'].keys():
            if entry.startswith("ia-pd"):
                del(parsed['lease6'][entry]['starts'])
                for key in parsed['lease6'][entry].keys():
                    if key.startswith('iaprefix'):
                        del(parsed['lease6'][entry][key]['starts'])
   
    world.clntCfg["real_lease"] = parsed 
    """
    print "\n\n\n"
    print world.clntCfg["real_lease"] 
    print "\n\n\n"
    print world.clntCfg['scapy_lease']
    print "\n\n\n"
    """
    if contain:
        assert world.clntCfg["real_lease"] == world.clntCfg['scapy_lease'], \
               "leases are different."
    else:
        assert world.clntCfg["real_lease"] != world.clntCfg['scapy_lease'], \
               "leases are the same, but they should not be."


def start_clnt(step):
    """
    @step("Client is started.")

    Lettuce step for writing config to file, sending it and starting client.
    """
    write_clnt_cfg_to_file()
    make_script()
    get_common_logger().debug("Start dhclient6 with generated config:")
    clean_leases()
    world.clntCfg["keep_lease"] = False
    fabric_send_file(world.clntCfg["Filename"], SOFTWARE_INSTALL_DIR + "dhclient.conf")
    fabric_send_file(world.clntCfg["script"], SOFTWARE_INSTALL_DIR + "comm.sh")
    fabric_remove_file_command(world.clntCfg["Filename"])
    fabric_remove_file_command(world.clntCfg["log_file"])
    fabric_sudo_command('(rm nohup.out; nohup bash ' + \
                        SOFTWARE_INSTALL_DIR + 'comm.sh &); sleep 1;')


def save_leases():
    world.clntCfg["keep_lease"] = True


def save_logs():
    fabric_download_file(world.clntCfg["log_file"], world.cfg["dir_name"] + \
                         "/dhclient.log")


def clear_all():
    fabric_remove_file_command(SOFTWARE_INSTALL_DIR + 'comm.sh')
    fabric_remove_file_command(SOFTWARE_INSTALL_DIR + 'dhclient.conf')
    fabric_remove_file_command(SOFTWARE_INSTALL_DIR + 'dhclient.leases')
    remove_local_file(world.clntCfg["Filename"])
    remove_local_file(world.clntCfg["script"])
    if not world.clntCfg["keep_lease"] and world.clntCfg['lease_file'] is not "":
        remove_local_file(world.clntCfg['lease_file'])


