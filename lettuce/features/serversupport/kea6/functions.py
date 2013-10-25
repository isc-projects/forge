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


from fabric.api import run, settings, put, hide
from logging_facility import *
from lettuce.registry import world
from init_all import SERVER_INSTALL_DIR, MGMT_ADDRESS
import os

def fabric(cmd):
    with settings(host_string = world.cfg["mgmt_addr"], user = world.cfg["mgmt_user"], password = world.cfg["mgmt_pass"]):
    #    with hide ('stdout','stderr'): #remove stdout if you want to see command stdout. good move to debug.
        result = run(cmd)
    return result

def parsing_bind_stdout(stdout, opt, search = []):
    """
    Modify this function if you wont react to some bind stdout
    """
    #search = []
    for each in search: 
        if each in stdout:
            print "RESTART BIND10, found ", each 
            from serversupport.bind10 import kill_bind10, start_bind10 #Bind10 needs to be restarted after error, can be removed after fix ticket #3074
            kill_bind10(MGMT_ADDRESS)
            start_bind10(MGMT_ADDRESS)
            run_bindctl (True, opt)

def restart_srv():
    cmd = '(echo "Dhcp6 shutdown" | ' + SERVER_INSTALL_DIR + 'bin/bindctl ); sleep 10' # can't be less then 7, server needs time to restart.
    fabric(cmd)

def stop_srv():
    run_bindctl ('clean')
    
def prepare_cfg_default(step):
    world.cfg["conf"] = "# Default server config for Kea6 is just empty string\n"
    
def prepare_cfg_subnet(step, subnet, pool):
    get_common_logger().debug("Configure subnet...")
    if (not "conf" in world.cfg):
        world.cfg["conf"] = ""
    if (subnet == "default"):
        subnet = "2001:db8:1::/64"
    if (pool == "default"):
        pool = "2001:db8:1::1 - 2001:db8:1::ffff"
    world.cfg["conf"] = '''\
        # subnet defintion Kea 6
        config add Dhcp6/subnet6
        config set Dhcp6/subnet6[0]/subnet "{subnet}"
        config set Dhcp6/subnet6[0]/pool [ "{pool}" ]
        '''.format(**locals())

kea_options6 = { "client-id": 1,
                 "server-id" : 2,
                 "IA_NA" : 3,
                 "IN_TA": 4,
                 "IA_address" : 5,
                 "preference": 7,
                 "relay-msg": 9,
                 "status-code": 13,
                 "rapid_commit": 14,
                 "interface-id": 18,
                 "sip-server-dns": 21,
                 "sip-server-addr": 22,
                 "dns-servers": 23,
                 "domain-search": 24,
                 "IA_PD": 25,
                 "IA-Prefix": 26,
                 "nis-servers": 27,
                 "nisp-servers": 28,
                 "nis-domain-name": 29,
                 "nisp-domain-name": 30,
                 "sntp-servers": 31,
                 "information-refresh-time": 32,
                  }
# kea_otheoptions was originally designed for vendor options
# because codes sometime overlap with basic options
kea_otheroptions = {"tftp-servers": 32,
                    "config-file": 33,
                    "syslog-servers": 34,
                    "time-servers": 37,
                    "time-offset": 38
                    }

# Dhcp6/renew-timer    1000    integer    (default)
# Dhcp6/rebind-timer    2000    integer    (default)
# Dhcp6/preferred-lifetime    3000    integer    (default)
# Dhcp6/valid-lifetime    4000    integer    (default)
kea_ times = {"renew-timer": 1000,
              "rebind-timer": 2000,
              "preferred-lifetime": 3000,
              "valid-lifetime": 4000
              }

def prepare_cfg_add_option(step, option_name, option_value, space):
#     if (not "conf" in world.cfg):
#         world.cfg["conf"] = ""
    
    if space == 'dhcp6':
        option_code = kea_options6.get(option_name)
        assert option_name in kea_options6, "Unsupported option name for basic Kea6 options: " + option_name
    else:
        option_code = kea_otheroptions.get(option_name)
        assert option_name in kea_otheroptions, "Unsupported option name for other Kea6 options: " + option_name
    number = world.kea["option_cnt"]
    
    world.cfg["conf"] += '''config add Dhcp6/option-data
        config set Dhcp6/option-data[{number}]/name "{option_name}"
        config set Dhcp6/option-data[{number}]/code {option_code}
        config set Dhcp6/option-data[{number}]/space "{space}"
        config set Dhcp6/option-data[{number}]/csv-format true
        config set Dhcp6/option-data[{number}]/data "{option_value}"
        '''.format(**locals())

    world.kea["option_cnt"] = world.kea["option_cnt"] + 1

def prepare_cfg_prefix(step, prefix, length, delegated_length, subnet):

    world.cfg["conf"] += '''
        config add Dhcp6/subnet6[{subnet}]/pd-pools
        config set Dhcp6/subnet6[{subnet}]/pd-pools[0]/prefix "{prefix}"
        config set Dhcp6/subnet6[{subnet}]/pd-pools[0]/prefix-len {length}
        config set Dhcp6/subnet6[{subnet}]/pd-pools[0]/delegated-len {delegated_length}
        '''.format(**locals())
    
def prepare_cfg_add_custom_option(step, opt_name, opt_code, opt_type, opt_value):
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
        '''.format(**locals())

def prepare_cfg_add_option_subnet(step, option_name, subnet, option_value):
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

        '''.format(**locals())

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
    cfg_file = open("kea6start.cfg", "w")
    cfg_file.write(config)
    cfg_file.close()


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
    cfg_file = open("kea6stop.cfg", "w")
    cfg_file.write(config)
    cfg_file.close()


def cfg_write():
    cfg_file = open(world.cfg["cfg_file"], 'w')
    cfg_file.write(world.cfg["conf"])
    cfg_file.close()
 
def pepere_config_file(cfg):
    """
    Prepare config file from generated world.cfg["cfg_file"] or START/STOP
    """
    tmpfile = cfg + "_processed"
    conf = open(cfg, "rt")
    process = open(tmpfile, "w")
    # Copy input line by line, but skip empty and comment lines
    for line in conf:
        line = line.strip()
        if len(line) < 2:
            continue
        if (line[0] == "#"):
            continue
        process.write(line + "\n")
    conf.close()
    process.close()
    try:
        os.remove(cfg)
    except OSError:
        get_common_logger().error('File %s cannot be removed' % cfg)
        

def fabric_send_file (file_local):
    """
    Send file to remote virtual machine
    """
    file_remote = file_local
    with settings(host_string = world.cfg["mgmt_addr"], user = world.cfg["mgmt_user"], password = world.cfg["mgmt_pass"]):
        with hide('running', 'stdout'):
            put(file_local, file_remote)
    try:
        os.remove(file_local)
    except OSError:
        get_common_logger().error('File %s cannot be removed' % file_local)
        
def run_bindctl (succeed, opt):
    """
    Run bindctl with prepered config file
    """    
    
    if opt == "clean":
        get_common_logger().debug('cleaning kea configuration')
        prepare_cfg_kea6_for_kea6_stop()
        cfg_file = 'kea6stop.cfg'
        pepere_config_file(cfg_file)
        fabric_send_file (cfg_file + "_processed")
    elif opt == "start":
        get_common_logger().debug('starting fresh kea')
        prepare_cfg_kea6_for_kea6_start()
        cfg_file = 'kea6start.cfg'
        pepere_config_file(cfg_file)
        fabric_send_file (cfg_file + "_processed")
    elif opt == "configuration":
        get_common_logger().debug('kea configuration')
        cfg_file = world.cfg["cfg_file"]
        pepere_config_file(cfg_file)
        add_last = open (cfg_file + "_processed", 'a')
        add_last.write("config commit")
        add_last.close()
        fabric_send_file (cfg_file + "_processed")
    elif opt == "restart":
        restart_srv()
        
    cmd = '(echo "execute file ' + cfg_file + '_processed" | ' + SERVER_INSTALL_DIR + 'bin/bindctl ); sleep 1'
    result = fabric(cmd)
    
    # now let's test output, looking for errors, 
    # some times clean can fail, so we wanna test only start and conf
    # for now we fail test on any presence of stderr, probably this will
    # need some more specific search.
    search = ["ImportError:",'"config revert".',"Error"]
    if opt is not "clean":
        if succeed:
            for each in search: 
                if each in result.stdout or each in result.stderr:
                    assert False, 'Server operation: ' + opt + ' failed! '
        if not succeed:
            for each in search: 
                if each in result.stdout or each in result.stderr:
                    break
            else:
                assert False, 'Server operation: ' + opt + ' not failed!'

    # Error 32: Broken pipe
    # this error needs different aproach then others. Bind10 needs to be restarted.
    parsing_bind_stdout(result.stdout, opt, ['Broken pipe'])

def start_srv(start, process):
    """
    Start kea with generated config
    """

    # All 3 available processess set to 'True' it means that they should to succeed
    configuration = True
    start = True
    clean = True

    # Switch one of three processess to false, which? That is decided in 
    # Server failed to start. During (\S+) process.) step.    
    if process == None and start:
        pass
    elif process == 'configuration':
        configuration = False
    elif process == 'start':
        start = False
    elif process == 'clean':
        clean = False
    else:
        assert False, "Process: '"+process+"' not supported."

    cfg_write() 
    get_common_logger().debug("Bind10, dhcp6 configuration procedure:")
    run_bindctl (clean, 'clean')#clean and stop
    run_bindctl (start, 'start')#start
    run_bindctl (configuration,'configuration')#conf
