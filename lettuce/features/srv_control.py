# Copyright (C) 2013 Internet Systems Consortium.
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
#

from lettuce import *
import re
import subprocess
#import StringIO
import os
#from subprocess import call, Popen, PIPE, STDOUT
from textwrap import dedent
from fabric.api import run, sudo, settings, put

USERNAME='root'
PASSWORD='m'
IP_ADDRESS='192.168.50.50:22'


def prepare_cfg_dibbler(step, config_file):
    world.cfg["conf"] = "iface " + world.cfg["iface"] + "\n" + \
    "    class {\n" + \
    "        pool 2001:db8:1::/64\n" + \
    "    }\n" + \
    "}\n"

def prepare_cfg_isc_dhcp(step):
    # TODO: Implement me
    print("TODO: Config generation for ISC DHCP is not implemented yet.")

def prepare_cfg_kea6_default(step):
    world.cfg["conf"] = "# Default server config for Kea6 is just empty string\n"

def prepare_cfg_kea6_subnet(step, subnet, pool):
    print("#### subnet")
    if (not "conf" in world.cfg):
        world.cfg["conf"] = ""
    if (subnet == "default"):
        subnet = "2001:db8:1::/64"
    if (pool == "default"):
        pool = "2001:db8:1::0 - 2001:db8:1::ffff"
    world.cfg["conf"] = '''\
        # subnet defintion Kea 6
        config add Dhcp6/subnet6
        config set Dhcp6/subnet6[0]/subnet "{subnet}"
        config set Dhcp6/subnet6[0]/pool [ "{pool}" ]
        config commit
        '''.format(**locals())
   
    #world.cfg["conf"] = dedent(world.cfg["conf"])
kea_options6 = { "preference": 7,
                 "sip-server-dns": 21,
                 "sip-server-addr": 22,
                 "dns-servers": 23,
                 "domain-search": 24,
                 "nis-servers": 27,
                 "nisp-servers": 28,
                 "nis-domain-name": 29,
                 "nisp-domain-name": 30,
                 "sntp-servers": 31,
                 "information-refresh-time": 32 }

def prepare_cfg_kea6_add_option(step, option_name, option_value):
    if (not "conf" in world.cfg):
        world.cfg["conf"] = ""

    assert option_name in kea_options6, "Unsupported option name " + option_name
    option_code = kea_options6.get(option_name)

    world.cfg["conf"] += '''config add Dhcp6/option-data
        config set Dhcp6/option-data[0]/name "{option_name}"
        config set Dhcp6/option-data[0]/code {option_code}
        config set Dhcp6/option-data[0]/space "dhcp6"
        config set Dhcp6/option-data[0]/csv-format true
        config set Dhcp6/option-data[0]/data "{option_value}"
        config commit
        '''.format(**locals())
    #world.cfg["conf"] = dedent(world.cfg["conf"])
    
def prepare_cfg_kea6_add_custom_option(step, opt_name, opt_code, opt_type, opt_value):
    if (not "conf" in world.cfg):
        world.cfg["conf"] = ""
    world.cfg["conf"] += '''config add Dhcp6/option-def
        config set Dhcp6/option-def[0]/name "{opt_name}"
        config set Dhcp6/option-def[0]/code {opt_code}
        config set Dhcp6/option-def[0]/type "{opt_type}"
        config set Dhcp6/option-def[0]/array false
        config set Dhcp6/option-def[0]/record-types ""
        config set Dhcp6/option-def[0]/space "dhcp6"
        config set Dhcp6/option-def[0]/encapsulate ""
        config add Dhcp6/option-data
        config set Dhcp6/option-data[0]/name "{opt_name}"
        config set Dhcp6/option-data[0]/code {opt_code}
        config set Dhcp6/option-data[0]/space "dhcp6"
        config set Dhcp6/option-data[0]/csv-format true
        config set Dhcp6/option-data[0]/data "{opt_value}"
        config commit
        '''.format(**locals())
    #world.cfg["conf"] = dedent(world.cfg["conf"])

def prepare_cfg_kea6_add_option_subnet(step, option_name, subnet, option_value):
    if (not "conf" in world.cfg):
        world.cfg["conf"] = ""

    assert option_name in kea_options6, "Unsupported option name " + option_name
    option_code = kea_options6.get(option_name)
    world.cfg["conf"] += '''
        config add Dhcp6/subnet6[{subnet}]/option-data
        config set Dhcp6/subnet6[{subnet}]/option-data[0]/name "{option_name}"
        config set Dhcp6/subnet6[{subnet}]/option-data[0]/code {option_code}
        config set Dhcp6/subnet6[{subnet}]/option-data[0]/space "dhcp6"
        config set Dhcp6/subnet6[{subnet}]/option-data[0]/csv-format true
        config set Dhcp6/subnet6[{subnet}]/option-data[0]/data "{option_value}"
        config commit
        '''.format(**locals())
    #world.cfg["conf"] = dedent(world.cfg["conf"])


def prepare_cfg_kea6_for_kea6_start():
    """
    config file for kea6 start
    """
    config = '''
        # This config file starts b10-dhcp6 server.
        config add Init/components b10-dhcp6
        config set Init/components/b10-dhcp6/kind dispensable
        config commit
        '''
    file = open("kea6-start.cfg", "w")
    file.write(config)
    file.close()


def prepare_cfg_kea6_for_kea6_stop():
    """
    config file for kea6 clear configuration and stopping
    """
    config = '''
        # This config file stops b10-dhcp6 server and removes its configuration.
        # Get rid of any subnets
        config set Dhcp6/subnet6 []
        # Get rid of any option format definitions
        config set Dhcp6/option-def []
        # Get rid of any option values
        config set Dhcp6/option-data []
        # Stop b10-dhcp6 server from starting again
        config remove Init/components b10-dhcp6
        config commit
        # And stop it
        Dhcp6 shutdown
        '''
    file = open("kea6-stop.cfg", "w")
    file.write(config)
    file.close()

def cfg_write(step):
    file = open(world.cfg["cfg_file"], 'w')
    file.write(world.cfg["conf"])
    file.close()

def start_srv_dibbler(step):
    args = [ 'dibbler-server', 'run' ]
    world.processes.add_process(step, "dhcpv6-server", args)
    # check output to know when startup has been completed
    (message, line) = world.processes.wait_for_stdout_str("dhcpv6-server",
                                                     ["Accepting connections.",
                                                      "Critical"])
    assert message == "Accepting connections.", "Got: " + str(line)

def start_srv_isc_dhcp(step, config_file):
    args = ['dhcpd' , '-d', '-cf', config_file ]

    world.processes.add_process(step, "dibbler-server", args)
    # check output to know when startup has been completed
    # TODO: Replace accepting connections.
    (message, line) = world.processes.wait_for_stderr_str(process_name,
                                                     ["Accepting connections.",
                                                      "exiting"])
    assert message == "Accepting connections.", "Got: " + str(line)
    
def pepere_config_file(cfg):
    """
    Prepere config file from generated world.cfg["cfg_file"] or START/STOP
    """
    tmpfile = cfg + "_processed"
    conf = open(cfg, "rt")
    process = open(tmpfile, "w")
    # Copy input line by line, but skip empty and comment lines
    for line in conf:
        line = line.strip()
        if len(line)<2:
            continue
        if (line[0] == "#"):
            continue
        process.write(line+"\n")
    conf.close()
    process.close()
    try:
        os.remove(cfg)
    except OSError:
        print ('File %s cannot be removed' % cfg)
        
#    tmpfile = cfg + ".c"
#    fin = open(cfg, "rt")
#    fphase1 = open(tmpfile, "w")
#    # Copy input line by line, but skip empty and comment lines
#    for line in fin:
#        if len(line)<1:
#            continue
#        if (line[:2] == "# "):
#            continue
#        fphase1.write(line)
#    fin.close()
#    fphase1.close()
#    # tmpfile (*.c) now contains our script with # comments removed
#    # This will be out output file with all #include expanded
#    outfile = cfg + ".expanded"
#    # Create the gcc command line.
#    gcc_cmd_line = ["gcc", "-E", tmpfile];
#    # Run gcc preprocessor.
#    preproc = subprocess.Popen(gcc_cmd_line, stdin=PIPE, stdout=PIPE)
#    tmp = StringIO.StringIO(preproc.communicate()[0])
#    # tmp now contains gcc preprocessor output. It contains some garbage
#    # comments starting with #. We'll get rid of those. Empty lines have
#    # to go as well.
#    fout = open(outfile, "w")
#    for line in tmp:
#        if len(line)<1:
#            continue
#        if line[:1] == "#":
#            continue
#        fout.write(line)
#    fout.close()
#
#    try:
#        os.remove(tmpfile)
#    except OSError:
#        print ('File %s cannot be removed' % tmpfile)

def fabric_send_file (file_local):
    """
    Send file to remote virtual machine
    """
    file_remote = file_local
    with settings(host_string=IP_ADDRESS, user=USERNAME, password=PASSWORD):
        put(file_local, file_remote)
    try:
        os.remove(file_local)
    except OSError:
        print ('File %s cannot be removed' % file_local)
        


def fabric_run_bindctl (opt):
    """
    Run bindctl with prepered config file
    """    
    if opt == "clean":
        print ('------------ cleaning kea configuration ----------')
        prepare_cfg_kea6_for_kea6_stop()
        cfg_file = 'kea6-stop.cfg'
        pepere_config_file(cfg_file)
        fabric_send_file (cfg_file+"_processed")
    if opt == "start":
        print ('------------ starting fresh kea ------------------')
        prepare_cfg_kea6_for_kea6_start()
        cfg_file = 'kea6-start.cfg'
        pepere_config_file(cfg_file)
        fabric_send_file (cfg_file+"_processed")
    if opt == "conf":
        print ('------------ kea configuration -------------------')
        cfg_file = world.cfg["cfg_file"]
        pepere_config_file(cfg_file)
        fabric_send_file (cfg_file+"_processed")
    
    cmd='(echo "execute file '+cfg_file+'_processed" | bindctl ); sleep 1'
    with settings(host_string=IP_ADDRESS, user=USERNAME, password=PASSWORD):
        sudo(cmd)

def start_srv_kea(step):
    """
    Start kea with generated config
    """
    fabric_run_bindctl ('clean')#clean and stop
    fabric_run_bindctl ('start')#start clean
    fabric_run_bindctl ('conf')#conf
    
    

#@step('have bind10 running(?: with configuration ([\S]+))?' +\
#      '(?: with cmdctl port (\d+))?' +\
#      '(?: as ([\S]+))?')
#def have_bind10_running(step, config_file, cmdctl_port, process_name):
#    """
#    Compound convenience step for running bind10, which consists of
#    start_bind10 and wait_for_auth.
#    Currently only supports the 'with configuration' option.
#    """
#    start_step = 'start bind10 with configuration ' + config_file
#    wait_step = 'wait for bind10 auth to start'
#    if cmdctl_port is not None:
#        start_step += ' with cmdctl port ' + str(cmdctl_port)
#   if process_name is not None:
#        start_step += ' as ' + process_name
#        wait_step = 'wait for bind10 auth of ' + process_name + ' to start'
#    step.given(start_step)
#    step.given(wait_step)

@step('Server is configured with (\S+) subnet with (\S+) pool.')
def config_srv_subnet(step, subnet, pool):
    """
    Adds server configuration with specified subnet and pool.
    subnet may define specific subnet or use the word "default"
    pool may define specific pool range or use the word "default"
    """
    if (world.cfg["server_type"] == "kea6"):
        prepare_cfg_kea6_subnet(step, subnet, pool)
    else:
        assert False, "Unsupported server type: %s" % world.cfg["server_type"]

@step('Server is configured with (\S+) option with value (\S+).')
def config_srv_opt(step, option_name, option_value):
    """
    Prepare server configuration with the specified option.
    option_name name of the option, e.g. dns-servers (number may be used here)
    option_value value of the configuration
    """
    if (world.cfg["server_type"] == "dibbler"):
        prepare_cfg_dibbler_add_option(step, option_name, option_value)
    elif (world.cfg["server_type"] == "isc-dhcp"):
        prepare_cfg_isc_dhcp(step, config_file)
    elif (world.cfg["server_type"] == 'kea6'):
        prepare_cfg_kea6_add_option(step, option_name, option_value)
    else:
        assert false, "Unsupported server type: %s" % world.cfg["server_type"]

@step('Server is configured with custom option (\S+)/(\d+) with type (\S+) and value (\S+).')
def config_srv_custom_opt(step, opt_name, opt_code, opt_type, opt_value):
    """
    Prepare server configuration with the specified custom option.
    opt_name name of the option, e.g. foo
    opt_code code of the option, e.g. 100
    opt_type type of the option, e.g. uint8 (see bind10 guide for complete list)
    opt_value value of the option, e.g. 1
    """
    if (world.cfg["server_type"] == "dibbler"):
        prepare_cfg_dibbler_add_custom_option(step, opt_name, opt_code, opt_type, opt_value)
    elif (world.cfg["server_type"] == "isc-dhcp"):
        prepare_cfg_isc_add_custom_option
    elif (world.cfg["server_type"] == 'kea6'):
        prepare_cfg_kea6_add_custom_option(step, opt_name, opt_code, opt_type, opt_value)
    else:
        assert false, "Unsupported server type: %s" % world.cfg["server_type"]


@step('Server is configured with (\S+) option in subnet (\d+) with value (\S+).')
def config_srv(step, option_name, subnet, option_value):
    """
    Prepare server configuration with the specified option.
    option_name name of the option, e.g. dns-servers (number may be used here)
    option_value value of the configuration
    """
    if (world.cfg["server_type"] == "dibbler"):
        prepare_cfg_dibbler_add_option_subnet(step, option_name, subnet, option_value)
    elif (world.cfg["server_type"] == "isc-dhcp"):
        prepare_cfg_isc_add_option_subnet(step, option_name, subnet, option_value)
    elif (world.cfg["server_type"] == 'kea6'):
        prepare_cfg_kea6_add_option_subnet(step, option_name, subnet, option_value)
    else:
        assert false, "Unsupported server type: %s" % world.cfg["server_type"]


@step('Server is started.')
def start_srv(step):

    # Write prepared config to a file
    cfg_write(step)

    if (world.cfg["server_type"] == "dibbler"):
        start_srv_dibbler(step)
    elif (world.cfg["server_type"] == "isc-dhcp"):
        start_srv_isc_dhcp(step)
    elif (world.cfg["server_type"] in ['kea', 'kea4', 'kea6']):
        start_srv_kea(step)
    else:
        assert false, "Unsupported server type: %s" % world.cfg["server_type"]

@step('Restart DHCPv6 server')
def restart_srv(step):
    pass

@step('stop DHCPv6 server')
def stop_srv(step):
    """
    For test that demands turinig off server in the middle
    """
    if (world.cfg["server_type"] == "dibbler"):
        pass
    elif (world.cfg["server_type"] == "isc-dhcp"):
        pass
    elif (world.cfg["server_type"] in ['kea', 'kea4', 'kea6']):
        start_srv_kea(step)
    else:
        assert false, "Unsupported server type: %s" % world.cfg["server_type"]
