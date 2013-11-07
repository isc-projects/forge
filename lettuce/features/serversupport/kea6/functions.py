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


from serversupport.multi_server_functions import fabric_run_command, fabric_send_file, remove_local_file 
from logging_facility import *
from lettuce.registry import world
from init_all import SERVER_INSTALL_DIR, SAVE_BIND_LOGS, BIND_LOG_TYPE, BIND_LOG_LVL, BIND_MODULE, SERVER_IFACE


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
                 "information-refresh-time": 32
                  }
# kea_otheoptions was originally designed for vendor options
# because codes sometime overlap with basic options
kea_otheroptions = {"tftp-servers": 32,
                    "config-file": 33,
                    "syslog-servers": 34,
                    "time-servers": 37,
                    "time-offset": 38
                    }

def set_time(step, which_time, value):
    if which_time in world.cfg["server_times"]:
            world.cfg["server_times"][which_time] = value
    else:
        assert which_time in world.cfg["server_times"], "Unknown time name: %s" % which_time

## =============================================================
## ================ PREPARE CONFIG BLOCK START =================

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
    t1 = world.cfg["server_times"]["renew-timer"]
    t2 = world.cfg["server_times"]["rebind-timer"]
    t3 = world.cfg["server_times"]["preferred-lifetime"]
    t4 = world.cfg["server_times"]["valid-lifetime"]
    eth = SERVER_IFACE
    world.cfg["conf"] = '''\
        # subnet defintion Kea 6
        config add Dhcp6/subnet6
        config set Dhcp6/subnet6[0]/subnet "{subnet}"
        config set Dhcp6/subnet6[0]/pool [ "{pool}" ]
        config set Dhcp6/renew-timer {t1} 
        config set Dhcp6/rebind-timer {t2}
        config set Dhcp6/preferred-lifetime {t3} 
        config set Dhcp6/valid-lifetime {t4}
        '''.format(**locals())
    if eth is not None:
        world.cfg["conf"] += '''\
            config set Dhcp6/subnet6[0]/interface "{eth}"
            '''.format(**locals())

    world.kea["subnet_cnt"] = world.kea["subnet_cnt"] + 1

def config_srv_another_subnet(step, subnet, pool, interface):
    count = world.kea["subnet_cnt"]
    world.cfg["conf"] += '''\
        # subnet defintion Kea 6
        config add Dhcp6/subnet6
        config set Dhcp6/subnet6[{count}]/subnet "{subnet}"
        config set Dhcp6/subnet6[{count}]/pool [ "{pool}" ]
        '''.format(**locals())
    if interface is not None:
        world.cfg["conf"] += '''\
                config set Dhcp6/subnet6[{count}]/interface "{interface}"
                '''.format(**locals())

    world.kea["subnet_cnt"] = world.kea["subnet_cnt"] + 1
    
def prepare_cfg_prefix(step, prefix, length, delegated_length, subnet):

    world.cfg["conf"] += '''
        config add Dhcp6/subnet6[{subnet}]/pd-pools
        config set Dhcp6/subnet6[{subnet}]/pd-pools[0]/prefix "{prefix}"
        config set Dhcp6/subnet6[{subnet}]/pd-pools[0]/prefix-len {length}
        config set Dhcp6/subnet6[{subnet}]/pd-pools[0]/delegated-len {delegated_length}
        '''.format(**locals())

def prepare_cfg_add_option(step, option_name, option_value, space):
#     if (not "conf" in world.cfg):
#         world.cfg["conf"] = ""
    
    option_code = kea_options6.get(option_name)
    
    if option_code == None:
        option_code = kea_otheroptions.get(option_name)
    
    assert option_code != None, "Unsupported option name for other Kea6 options: " + option_name
    number = world.kea["option_cnt"]
    
    world.cfg["conf"] += '''config add Dhcp6/option-data
        config set Dhcp6/option-data[{number}]/name "{option_name}"
        config set Dhcp6/option-data[{number}]/code {option_code}
        config set Dhcp6/option-data[{number}]/space "{space}"
        config set Dhcp6/option-data[{number}]/csv-format true
        config set Dhcp6/option-data[{number}]/data "{option_value}"
        '''.format(**locals())

    world.kea["option_cnt"] = world.kea["option_cnt"] + 1

def prepare_cfg_add_custom_option(step, opt_name, opt_code, opt_type, opt_value, space):
    if (not "conf" in world.cfg):
        world.cfg["conf"] = ""
        
    number = world.kea["option_cnt"]
    number_def = world.kea["option_usr_cnt"]
    world.cfg["conf"] += '''config add Dhcp6/option-def
        config set Dhcp6/option-def[{number_def}]/name "{opt_name}"
        config set Dhcp6/option-def[{number_def}]/code {opt_code}
        config set Dhcp6/option-def[{number_def}]/type "{opt_type}"
        config set Dhcp6/option-def[{number_def}]/array false
        config set Dhcp6/option-def[{number_def}]/record-types ""
        config set Dhcp6/option-def[{number_def}]/space "{space}"
        config set Dhcp6/option-def[{number_def}]/encapsulate ""
        config add Dhcp6/option-data
        config set Dhcp6/option-data[{number}]/name "{opt_name}"
        config set Dhcp6/option-data[{number}]/code {opt_code}
        config set Dhcp6/option-data[{number}]/space "{space}"
        config set Dhcp6/option-data[{number}]/csv-format true
        config set Dhcp6/option-data[{number}]/data "{opt_value}"
        '''.format(**locals())
        
    world.kea["option_usr_cnt"] = world.kea["option_usr_cnt"] + 1
    world.kea["option_cnt"] = world.kea["option_cnt"] + 1
    
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
        # clear loggers
        config set Logging/loggers []
        # Clear all library hooks
        config set Dhcp6/hooks-libraries []
        # Stop b10-dhcp6 server from starting again
        config remove Init/components b10-dhcp6
        config commit
        # And stop it
        Dhcp6 shutdown
        '''
    cfg_file = open("kea6stop.cfg", "w")
    cfg_file.write(config)
    cfg_file.close()

def run_command(step, command):
    world.cfg["conf"] += ('\n'+command+'\n') 

def set_logger():
    file_name = world.name.replace(".","_")
    type = BIND_LOG_TYPE 
    lvl = BIND_LOG_LVL
    module = BIND_MODULE 
    
    logger_str ='''
    config add Logging/loggers
    config set Logging/loggers[0]/name "{module}"
    config set Logging/loggers[0]/severity "{type}"
    config set Logging/loggers[0]/debuglevel {lvl}
    config add Logging/loggers[0]/output_options
    config set Logging/loggers[0]/output_options[0]/destination file
    config set Logging/loggers[0]/output_options[0]/output log_file
    config commit
    '''.format(**locals())

    cfg_file = open("logger.cfg", "w")
    cfg_file.write(logger_str)
    cfg_file.close()

    cfg_file = 'logger.cfg'
    prepare_config_file(cfg_file)

    fabric_send_file(cfg_file + '_processed', cfg_file + '_processed')
    
    fabric_run_command('(rm -f log_file | echo "execute file ' + cfg_file + '_processed" | ' + SERVER_INSTALL_DIR + 'bin/bindctl ); sleep 1')

def prepare_config_file(cfg):
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

    remove_local_file(cfg)

def cfg_write():
    cfg_file = open(world.cfg["cfg_file"], 'w')
    cfg_file.write(world.cfg["conf"])
    cfg_file.close()

## =============================================================
## ================ PREPARE CONFIG BLOCK END  ==================

## =============================================================
## ================ REMOTE SERVER BLOCK START ==================

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

def stop_srv():
    run_bindctl ('clean')

def restart_srv():
    fabric_run_command('(echo "Dhcp6 shutdown" | ' + SERVER_INSTALL_DIR + 'bin/bindctl ); sleep 10') # can't be less then 7, server needs time to restart.


def parsing_bind_stdout(stdout, opt, search = []):
    """
    Modify this function if you wont react to some bind stdout
    """
    #search = []
    for each in search: 
        if each in stdout:
            print "RESTART BIND10, found ", each 
            from serversupport.bind10 import kill_bind10, start_bind10 #Bind10 needs to be restarted after error, can be removed after fix ticket #3074
            kill_bind10()
            start_bind10()
            run_bindctl (True, opt)

def run_bindctl (succeed, opt):
    """
    Run bindctl with prepered config file
    """    
    
    if opt == "clean":
        get_common_logger().debug('cleaning kea configuration')
        # build configuration file with for:  
        #  - stopping Kea
        #  - cleaning configuration
        #  - default logging
        prepare_cfg_kea6_for_kea6_stop()
        cfg_file = 'kea6stop.cfg'
        prepare_config_file(cfg_file)
        # send file
        fabric_send_file(cfg_file + '_processed', cfg_file + '_processed')
        remove_local_file(cfg_file + '_processed')
        
    elif opt == "start":
        # build configuration file with for:  
        #  - clean start Kea
        get_common_logger().debug('starting fresh kea')
        prepare_cfg_kea6_for_kea6_start()
        cfg_file = 'kea6start.cfg'
        prepare_config_file(cfg_file)
        # send file
        fabric_send_file(cfg_file + '_processed', cfg_file + '_processed')
        remove_local_file(cfg_file + '_processed')
        
    elif opt == "configuration":
        # start logging on different file:
        if SAVE_BIND_LOGS:
            set_logger()
        # build configuration file with for:  
        #  - configure all needed to test features
        get_common_logger().debug('kea configuration')
        cfg_file = world.cfg["cfg_file"]
        prepare_config_file(cfg_file)
        add_last = open (cfg_file + "_processed", 'a')

        # add 'config commit' we don't put it before
        add_last.write("config commit")
        add_last.close()
        # send file
        fabric_send_file(cfg_file + '_processed', cfg_file + '_processed')
        remove_local_file(cfg_file + '_processed')
        
    elif opt == "restart":
        # restart server without changing it's configuration
        restart_srv()
        
    result = fabric_run_command('(echo "execute file ' + cfg_file + '_processed" | ' + SERVER_INSTALL_DIR + 'bin/bindctl ); sleep 1')
    
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

## =============================================================
## ================ REMOTE SERVER BLOCK END ====================