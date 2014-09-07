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

from softwaresupport.multi_server_functions import fabric_run_command, fabric_send_file, remove_local_file,\
    copy_configuration_file
from lettuce import world
from logging_facility import *
from textwrap import dedent
from logging_facility import get_common_logger
from init_all import SERVER_INSTALL_DIR, SERVER_IFACE, SAVE_LOGS

from softwaresupport.kea6_server_bind.functions import search_for_errors, parsing_bind_stdout, prepare_config_file,\
    set_logger, cfg_write, set_time, save_leases, save_logs, clear_all

kea_options4 = {"subnet-mask": 1, # ipv4-address (array)
                "time-offset": 2, 
                "routers": 3, # ipv4-address (single)
                "time-servers": 4, # ipv4-address (single)
                "name-servers": 5, # ipv4-address (array)
                "domain-name-servers": 6, # ipv4-address (array)
                "log-servers": 7, # ipv4-address (single)
                "cookie-servers": 8,  # ipv4-address (single)
                "lpr-servers": 9, # ipv4-address (single)
                "impress-servers": 10, # ipv4-address (single)
                "resource-location-servers": 11, # ipv4-address (single)
                "host-name": 12, # string 
                "boot-size": 13,
                "merit-dump": 14, # string 
                "domain-name": 15, # fqdn (single)
                "swap-server": 16, # ipv4-address (single)
                "root-path": 17, # string 
                "extensions-path": 18, # string 
                "ip-forwarding": 19, # boolean
                "non-local-source-routing": 20, # boolean
                "policy-filter": 21, # ipv4-address (single)
                "max-dgram-reassembly": 22,
                "default-ip-ttl": 23,
                "path-mtu-aging-timeout": 24,
                "path-mtu-plateau-table": 25,
                "interface-mtu": 26,
                "all-subnets-local": 27, # boolean
                "broadcast-address": 28, # ipv4-address (single)
                "perform-mask-discovery": 29, # boolean
                "mask-supplier": 30, # boolean
                "router-discovery": 31, # boolean
                "router-solicitation-address": 32, # ipv4-address (single)
                "static-routes": 33, # ipv4-address (array)
                "trailer-encapsulation": 34, # boolean
                "arp-cache-timeout": 35,
                "ieee802-3-encapsulation": 36,
                "default-tcp-ttl": 37,
                "tcp-keepalive-internal": 38,
                "tcp-keepalive-garbage": 39, # boolean
                "nis-domain": 40, # string (single)
                "nis-servers": 41, # ipv4-address (array)
                "ntp-servers": 42, # ipv4-address (array)
                "vendor-encapsulated-options": 43, # empty
                "netbios-name-servers": 44, # ipv4-address
                "netbios-dd-server": 45, # ipv4-address
                "netbios-node-type": 46, # uint8
                "netbios-scope": 47, # string
                "font-servers": 48, # ipv4-address
                "x-display-manager": 49, # ipv4-address
                "dhcp-requested-address": 50, # ipv4-address
                "dhcp-option-overload": 52, # uint8
                "server_id": 54,
                "dhcp-message": 56, # string
                "dhcp-max-message-size": 57, # uint16
                "vendor-class-identifier": 60, # binary
                "client_id": 61,
                "nwip-domain-name": 62, # string
                "nwip-suboptions": 63, # binary
                "boot-file-name": 67, #string
                "user-class": 77, # binary
                "fqdn": 81, # record
                "dhcp-agent-options": 82, # empty
                "authenticate": 90, # binary
                "client-last-transaction-time": 91, # uint32
                "associated-ip": 92, # ipv4-address
                "subnet-selection": 118, # ipv4-address
                "domain-search": 119, # binary
                "vivco-suboptions": 124, # binary
                "vivso-suboptions": 125, # binary
                "end": 255}


def check_empty_value(val):
    return ("false", "") if val == "<empty>" else ("true", val)


def prepare_cfg_subnet(step, subnet, pool):
    if not "conf" in world.cfg:
        world.cfg["conf"] = ""

    eth = SERVER_IFACE
    # subnet defintion Kea4
    t1 = world.cfg["server_times"]["renew-timer"]
    t2 = world.cfg["server_times"]["rebind-timer"]
    t3 = world.cfg["server_times"]["valid-lifetime"]

    subnetcfg = '''
        config set Dhcp4/renew-timer {t1}
        config set Dhcp4/rebind-timer {t2}
        config set Dhcp4/valid-lifetime {t3}
        config add Dhcp4/subnet4
        config set Dhcp4/subnet4[0]/subnet "{subnet}"
        config set Dhcp4/subnet4[0]/pool [ "{pool}" ]
        '''.format(**locals())

    if eth != "":
        world.cfg["conf"] += '''
            config add Dhcp4/interfaces "{eth}"
            '''.format(**locals())

    world.cfg["conf"] += dedent(subnetcfg)
    world.kea["subnet_cnt"] += 1


def config_srv_another_subnet(step, subnet, pool, interface):
    count = world.kea["subnet_cnt"]

    subnetcfg = '''
        config add Dhcp4/subnet4
        config set Dhcp4/subnet4[{count}]/subnet "{subnet}"
        config set Dhcp4/subnet4[{count}]/pool [ "{pool}" ]
        '''.format(**locals())

    if interface is not None:
        world.cfg["conf"] += '''
                config add Dhcp4/interfaces "{interface}"
                '''.format(**locals())

    world.cfg["conf"] += dedent(subnetcfg)
    world.kea["subnet_cnt"] += 1


def config_client_classification(step, subnet, option_value):
    world.cfg["conf"] += '''
        config set Dhcp4/subnet4[{subnet}]/client-class "{option_value}"
        '''.format(**locals())


def prepare_cfg_add_custom_option(step, opt_name, opt_code, opt_type, opt_value, space):
    if not "conf" in world.cfg:
        world.cfg["conf"] = ""

    number = world.kea["option_cnt"]
    number_def = world.kea["option_usr_cnt"]
    csv_format, opt_value = check_empty_value(opt_value)
    world.cfg["conf"] += '''config add Dhcp4/option-def
        config set Dhcp4/option-def[{number_def}]/name "{opt_name}"
        config set Dhcp4/option-def[{number_def}]/code {opt_code}
        config set Dhcp4/option-def[{number_def}]/type "{opt_type}"
        config set Dhcp4/option-def[{number_def}]/array false
        config set Dhcp4/option-def[{number_def}]/record-types ""
        config set Dhcp4/option-def[{number_def}]/space "{space}"
        config set Dhcp4/option-def[{number_def}]/encapsulate ""
        config add Dhcp4/option-data
        config set Dhcp4/option-data[{number}]/name "{opt_name}"
        config set Dhcp4/option-data[{number}]/code {opt_code}
        config set Dhcp4/option-data[{number}]/space "{space}"
        config set Dhcp4/option-data[{number}]/csv-format {csv_format}
        config set Dhcp4/option-data[{number}]/data "{opt_value}"
        '''.format(**locals())

    world.kea["option_usr_cnt"] += 1
    world.kea["option_cnt"] += 1


def add_siaddr(step, addr, subnet_number):
    if subnet_number is None:
        world.cfg["conf"] += '''
            config set Dhcp4/next-server "{addr}"
            '''.format(**locals())
    else:
        world.cfg["conf"] += '''
            config set Dhcp4/subnet4[{subnet_number}]/next-server "{addr}"
            '''.format(**locals())


def prepare_cfg_add_option_subnet(step, option_name, subnet, option_value):
    assert option_name in kea_options4, "Unsupported option name " + option_name
    option_code = kea_options4.get(option_name)
    csv_format, option_value = check_empty_value(option_value)
    
    # need to have numbers for multiple options for each subnet! 
    world.cfg["conf"] += '''
        config add Dhcp4/subnet4[{subnet}]/option-data
        config set Dhcp4/subnet4[{subnet}]/option-data[0]/name "{option_name}"
        config set Dhcp4/subnet4[{subnet}]/option-data[0]/code {option_code}
        config set Dhcp4/subnet4[{subnet}]/option-data[0]/space "dhcp4"
        config set Dhcp4/subnet4[{subnet}]/option-data[0]/csv-format {csv_format}
        config set Dhcp4/subnet4[{subnet}]/option-data[0]/data "{option_value}"
        '''.format(**locals())


def run_command(step, command):
    world.cfg["conf"] += ('\n'+command+'\n')


def disanable_client_echo(step):
    # after using it, we should revert that at the end!
    # keep that in mind when first time using it.
    world.cfg["conf"] += '''
        config set Dhcp4/echo-client-id False
        config commit
        '''.format(**locals())


def add_interface(step, interface):
    # not jet tested!
    world.cfg["conf"] += '''
        config add Dhcp4/interfaces {interface}
        '''.format(**locals())


def prepare_cfg_add_option(step, option_name, option_value, space):
    if not "conf" in world.cfg:
        world.cfg["conf"] = ""

    assert option_name in kea_options4, "Unsupported option name " + option_name
    option_code = kea_options4.get(option_name)
    csv_format, option_value = check_empty_value(option_value)
    option_cnt = world.kea["option_cnt"]

    options = '''
    config add Dhcp4/option-data
    config set Dhcp4/option-data[{option_cnt}]/name "{option_name}"
    config set Dhcp4/option-data[{option_cnt}]/code {option_code}
    config set Dhcp4/option-data[{option_cnt}]/space "{space}"
    config set Dhcp4/option-data[{option_cnt}]/csv-format {csv_format}
    config set Dhcp4/option-data[{option_cnt}]/data "{option_value}"
    '''.format(**locals())
    world.cfg["conf"] += dedent(options)
    world.kea["option_cnt"] += 1


def prepare_cfg_kea4_for_kea4_start(filename):
    """
    config file for kea4 start
    """
    config = '''
        # This config file starts b10-dhcp4 server.
        config add Init/components b10-dhcp4
        config set Init/components/b10-dhcp4/kind dispensable
        config commit
        '''
    cfg_file = open(filename, "w")
    cfg_file.write(config)
    cfg_file.close()


def prepare_cfg_kea4_for_kea4_stop(filename):
    """
    config file for kea4 clear configuration and stopping
    """
    config = '''
        # This config file stops b10-dhcp4 server and removes its configuration.
        # Get rid of any subnets
        config set Dhcp4/subnet4 []
        # Get rid of any option format definitions
        config set Dhcp4/option-def []
        # Get rid of any option values
        config set Dhcp4/option-data []
        # clear loggers
        config set Logging/loggers []
        #config set Dhcp4/echo-client-id True
        config set Dhcp4/next-server ""
        config set Dhcp4/interfaces []
        config commit
        # Stop b10-dhcp4 server from starting again
        config remove Init/components b10-dhcp4
        config commit
        # And stop it
        Dhcp4 shutdown
        '''
    cfg_file = open(filename, "w")
    cfg_file.write(config)
    cfg_file.close()


def run_bindctl(succeed, opt):
    """
    Run bindctl with prepered config file
    """    
    world.cfg['leases'] = SERVER_INSTALL_DIR + 'var/bind10/kea-leases4.csv'
    
    if opt == "clean":
        get_common_logger().debug('cleaning kea configuration')
        cfg_file = 'kea4-stop.cfg'
        prepare_cfg_kea4_for_kea4_stop(cfg_file)
        prepare_config_file(cfg_file)
        fabric_send_file(cfg_file + '_processed', cfg_file + '_processed')
        remove_local_file(cfg_file + '_processed')
        
    if opt == "start":
        if SAVE_LOGS:
            set_logger()
        
        get_common_logger().debug('starting fresh kea')
        cfg_file = 'kea4-start.cfg'
        prepare_cfg_kea4_for_kea4_start(cfg_file)
        prepare_config_file(cfg_file)
        fabric_send_file(cfg_file + '_processed', cfg_file + '_processed')
        remove_local_file(cfg_file + '_processed')
        
    if opt == "configuration":
        get_common_logger().debug('kea configuration')
        cfg_file = world.cfg["cfg_file"]
        prepare_config_file(cfg_file)
        add_last = open(cfg_file + "_processed", 'a')

        # add 'config commit' we don't put it before
        add_last.write("config commit")
        add_last.close()

        fabric_send_file(cfg_file + '_processed', cfg_file + '_processed')
        copy_configuration_file(cfg_file + '_processed')
        remove_local_file(cfg_file + '_processed')
        world.cfg["conf"] = ""
        
    if opt == "restart":
        restart_srv()
    
    result = fabric_run_command('(echo "execute file ' + cfg_file + '_processed" | '
                                + SERVER_INSTALL_DIR + 'bin/bindctl ); sleep 1')
    
    search_for_errors(succeed, opt, result, ["ImportError:", '"config revert".', "Error"])
    parsing_bind_stdout(result.stdout, opt, ['Broken pipe'])


def start_srv(start, process):
    configuration = True
    start = True
    clean = True

    # Switch one of three processess to false, which? That is decided in 
    # Server failed to start. During (\S+) process.) step.    
    if process is None and start:
        pass
    elif process == 'configuration':
        configuration = False
    elif process == 'start':
        start = False
    elif process == 'clean':
        clean = False
    else:
        assert False, "Process: '" + process + "' not supported."
        
    cfg_write()
    get_common_logger().debug("Bind10, dhcp4 configuration procedure:")
    run_bindctl(clean, 'clean')  # clean and stop
    run_bindctl(start, 'start')  # start
    run_bindctl(configuration, 'configuration')  # conf


def stop_srv(value = False):
    # value not used but have to be here
    run_bindctl(True, 'clean')


def restart_srv():
    # can't be less then 7, server needs time to restart.
    fabric_run_command('(echo "Dhcp4 shutdown" | ' + SERVER_INSTALL_DIR + 'bin/bindctl ); sleep 10') 


def prepare_cfg_prefix(step, prefix, length, delegated_length, subnet):
    assert False, "This function can be used only with DHCPv6"