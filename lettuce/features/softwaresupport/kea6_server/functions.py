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

# Author: Wlodzimierz Wencel


from softwaresupport.multi_server_functions import fabric_run_command, fabric_send_file,\
    remove_local_file, cpoy_configuration_file, fabric_sudo_command

from logging_facility import *
from lettuce.registry import world
from init_all import SERVER_INSTALL_DIR, SAVE_BIND_LOGS, BIND_LOG_TYPE, BIND_LOG_LVL,\
    BIND_MODULE, SERVER_IFACE, SLEEP_TIME_2


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


def add_defaults():
    t1 = world.cfg["server_times"]["renew-timer"]
    t2 = world.cfg["server_times"]["rebind-timer"]
    t3 = world.cfg["server_times"]["preferred-lifetime"]
    t4 = world.cfg["server_times"]["valid-lifetime"]
    eth = SERVER_IFACE
    pointer_start = "{"
    pointer_end = "}"

    world.cfg["main"] = '''
        {pointer_start} "Dhcp6" :

        {pointer_start}
        "renew-timer": {t1},
        "rebind-timer": {t2},
        "preferred-lifetime": {t3},
        "valid-lifetime": {t4},
        '''.format(**locals())

    if eth is not None:
        world.cfg["main"] += '''"interfaces": ["{eth}"],
        '''.format(**locals())


def prepare_cfg_subnet(step, subnet, pool, eth = None):
    if not "add_subnet" in world.cfg:
        world.cfg["add_subnet"] = '"subnet6": [ '
    else:
        world.cfg["add_subnet"] += ',\n'
    if subnet == "default":
        subnet = "2001:db8:1::/64"
    if pool == "default":
        pool = "2001:db8:1::1 - 2001:db8:1::ffff"
    if eth is None:
        eth = SERVER_IFACE

    pointer_start = "{"
    pointer_end = "}"

    world.cfg["add_subnet"] += '\n\t\t{pointer_start} "pool": [ "{pool}" ], "subnet": "{subnet}"'.format(**locals())
    if eth is not None:
        world.cfg["add_subnet"] += ', "interface": "{eth}" '.format(**locals())

    world.kea["subnet_cnt"] += 1


def config_srv_another_subnet(step, subnet, pool, interface):
    pass
    # TODO: implement this!


def config_client_classification(step, subnet, option_value):
    # TODO: implement this!
    pass


def prepare_cfg_prefix(step, prefix, length, delegated_length, subnet):
    if not "add_subnet" in world.cfg:
        assert False, "First you need to configure subnet."

    pointer_start = "{"
    pointer_end = "}"

    world.cfg["add_subnet"] += ',\n'
    world.cfg["add_subnet"] += '''\t\t"pd-pools": [
            \t\t{pointer_start}"delegated-len": {delegated_length}, "prefix": "{prefix}", "prefix-len": {length} {pointer_end}]'''\
        .format(**locals())


def prepare_cfg_add_option(step, option_name, option_value, space, option_code=None, type='default', where='options'):
    if not where in world.cfg:
        world.cfg[where] = '\n\t"option-data": ['
    else:
        world.cfg[where] += ","

    # check if we are configuring default option or user option via function "prepare_cfg_add_custom_option"
    if type == 'default':
        option_code = kea_options6.get(option_name)
        if option_code is None:
            option_code = kea_otheroptions.get(option_name)

    pointer_start = "{"
    pointer_end = "}"

    assert option_code is not None, "Unsupported option name for other Kea6 options: " + option_name

    world.cfg[where] += '''
            \t{pointer_start}"csv-format": true, "code": {option_code}, "data": "{option_value}",
            \t"name": "{option_name}", "space": "{space}"{pointer_end}'''.format(**locals())


def prepare_cfg_add_custom_option(step, opt_name, opt_code, opt_type, opt_value, space):
    pointer_start = "{"
    pointer_end = "}"

    if not "option_def" in world.cfg:
        world.cfg["option_def"] = '\n\t"option-def": ['
    else:
        world.cfg["option_def"] += ","

    # make definition of the new option
    world.cfg["option_def"] += '''
            \t{pointer_start}"code": {opt_code}, "name": "{opt_name}", "space": "{space}",
            \t"encapsulate": "", "record-types": "", "array": false, "type": "{opt_type}"{pointer_end}'''\
        .format(**locals())

    # add defined option
    prepare_cfg_add_option(step, opt_name, opt_value, space, opt_code, 'user')


def prepare_cfg_add_option_subnet(step, option_name, subnet, option_value):
    if not "add_subnet" in world.cfg:
        assert False, "First you need to configure subnet."

    prepare_cfg_add_option(step, option_name, option_value, 'dhcp6', option_code = None,
                           type = 'default', where = 'add_subnet_options')


def run_command(step, command):
    pass
    # world.cfg["conf"] += ('\n'+command+'\n')


def set_logger():
    pass
    assert False, "For now option unavailable!"


def cfg_write():
    cfg_file = open(world.cfg["cfg_file"], 'w')
    cfg_file.write(world.cfg["main"])
    if "add_subnet" in world.cfg:
        cfg_file.write(world.cfg["add_subnet"])

    if "add_subnet_options" in world.cfg:
        cfg_file.write("," + world.cfg["add_subnet_options"] + " ] \n\t\t}]")
    else:
        cfg_file.write(" }]")

    if "options" in world.cfg:
        cfg_file.write(',' + world.cfg["options"])
        cfg_file.write("]")

    if "option_def" in world.cfg:
        cfg_file.write(',' + world.cfg["option_def"])
        cfg_file.write("]")
    # TODO make available different database backends!
    cfg_file.write(',\n\n\t"lease-database":{"type": "memfile"}\n\t}\n\n\t}\n')
    cfg_file.close()

## =============================================================
## ================ PREPARE CONFIG BLOCK END  ==================

## =============================================================
## ================ REMOTE SERVER BLOCK START ==================


def start_srv(start, process):
    """
    Start kea with generated config
    """
    world.cfg['leases'] = SERVER_INSTALL_DIR + 'var/bind10/kea-leases6.csv'
    add_defaults()
    cfg_write()
    fabric_send_file(world.cfg["cfg_file"], world.cfg["cfg_file"])
    cpoy_configuration_file(world.cfg["cfg_file"])
    remove_local_file(world.cfg["cfg_file"])
    fabric_run_command('(rm nohup.out; nohup ' + SERVER_INSTALL_DIR + 'libexec/bind10/b10-dhcp6 -c '
                       + world.cfg["cfg_file"] + '&); sleep 1')


def stop_srv():
    pass


def restart_srv():
    pass

## =============================================================
## ================ REMOTE SERVER BLOCK END ====================
