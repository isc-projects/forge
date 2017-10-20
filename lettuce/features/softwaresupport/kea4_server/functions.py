# Copyright (C) 2013-2017 Internet Systems Consortium.
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

from softwaresupport.multi_server_functions import fabric_run_command, fabric_send_file, remove_local_file,\
    copy_configuration_file, fabric_sudo_command, fabric_download_file, locate_entry
from lettuce import world
from logging_facility import *
from time import sleep
from logging_facility import get_common_logger

from softwaresupport.kea6_server.functions import stop_srv, restart_srv, set_logger, cfg_write, set_time, \
    add_line_in_global, config_srv_another_subnet, prepare_cfg_add_custom_option, set_kea_ctrl_config,\
    check_kea_status, check_kea_process_result, save_logs, clear_all, add_interface, add_pool_to_subnet, clear_leases,\
    add_hooks, save_leases, add_logger, open_control_channel_socket, set_conf_parameter_global, \
    set_conf_parameter_subnet, add_line_in_subnet, add_line_to_shared_subnet, add_to_shared_subnet,\
    set_conf_parameter_shared_subnet

kea_options4 = {
    "subnet-mask": 1,  # ipv4-address (array)
    "time-offset": 2,
    "routers": 3,  # ipv4-address (single)
    "time-servers": 4,  # ipv4-address (single)
    "name-servers": 5,  # ipv4-address (array)
    "domain-name-servers": 6,  # ipv4-address (array)
    "log-servers": 7,  # ipv4-address (single)
    "cookie-servers": 8,  # ipv4-address (single)
    "lpr-servers": 9,  # ipv4-address (single)
    "impress-servers": 10,  # ipv4-address (single)
    "resource-location-servers": 11,  # ipv4-address (single)
    "host-name": 12,  # string
    "boot-size": 13,
    "merit-dump": 14,  # string
    "domain-name": 15,  # fqdn (single)
    "swap-server": 16,  # ipv4-address (single)
    "root-path": 17,  # string
    "extensions-path": 18,  # string
    "ip-forwarding": 19,  # boolean
    "non-local-source-routing": 20,  # boolean
    "policy-filter": 21,  # ipv4-address (single)
    "max-dgram-reassembly": 22,
    "default-ip-ttl": 23,
    "path-mtu-aging-timeout": 24,
    "path-mtu-plateau-table": 25,
    "interface-mtu": 26,
    "all-subnets-local": 27,  # boolean
    "broadcast-address": 28,  # ipv4-address (single)
    "perform-mask-discovery": 29,  # boolean
    "mask-supplier": 30,  # boolean
    "router-discovery": 31,  # boolean
    "router-solicitation-address": 32,  # ipv4-address (single)
    "static-routes": 33,  # ipv4-address (array)
    "trailer-encapsulation": 34,  # boolean
    "arp-cache-timeout": 35,
    "ieee802-3-encapsulation": 36,
    "default-tcp-ttl": 37,
    "tcp-keepalive-interval": 38,
    "tcp-keepalive-garbage": 39,  # boolean
    "nis-domain": 40,  # string (single)
    "nis-servers": 41,  # ipv4-address (array)
    "ntp-servers": 42,  # ipv4-address (array)
    "vendor-encapsulated-options": 43,  # empty
    "netbios-name-servers": 44,  # ipv4-address
    "netbios-dd-server": 45,  # ipv4-address
    "netbios-node-type": 46,  # uint8
    "netbios-scope": 47,  # string
    "font-servers": 48,  # ipv4-address
    "x-display-manager": 49,  # ipv4-address
    "dhcp-requested-address": 50,  # ipv4-address
    "dhcp-option-overload": 52,  # uint8
    "server_id": 54,
    "dhcp-message": 56,  # string
    "dhcp-max-message-size": 57,  # uint16
    "vendor-class-identifier": 60,  # binary
    "client_id": 61,
    "nwip-domain-name": 62,  # string
    "nwip-suboptions": 63,  # binary
    "nisplus-domain-name": 64,  # string
    "nisplus-servers": 65,  # ipv4-address (array)
    "boot-file-name": 67,  # string
    "mobile-ip-home-agent": 68,  # ipv4-address (array)
    "smtp-server": 69,  # ipv4-address (array)
    "pop-server": 70,  # ipv4-address (array)
    "nntp-server": 71,  # ipv4-address (array)
    "www-server": 72,  # ipv4-address (array)
    "finger-server": 73,  # ipv4-address (array)
    "irc-server": 74,  # ipv4-address (array)
    "streettalk-server": 75,  # ipv4-address (array)
    "streettalk-directory-assistance-server": 76,  # ipv4-address (array)
    "user-class": 77,  # binary
    "fqdn": 81,  # record
    "dhcp-agent-options": 82,  # empty
    "authenticate": 90,  # binary
    "client-last-transaction-time": 91,  # uint32
    "associated-ip": 92,  # ipv4-address
    "subnet-selection": 118,  # ipv4-address
    "domain-search": 119,  # binary
    "vivco-suboptions": 124,  # binary
    "vivso-suboptions": 125,  # binary
    "end": 255
}


def check_empty_value(val):
    return ("false", "") if val == "<empty>" else ("true", val)


def add_defaults():
    eth = world.f_cfg.server_iface
    t1 = world.cfg["server_times"]["renew-timer"]
    t2 = world.cfg["server_times"]["rebind-timer"]
    t3 = world.cfg["server_times"]["valid-lifetime"]

    pointer_start = "{"
    pointer_end = "}"

    world.cfg["main"] = '{"Dhcp4" :{'
    if t1 != "":
        world.cfg["main"] += '"renew-timer": {t1},'.format(**locals())
    if t2 != "":
        world.cfg["main"] += '"rebind-timer": {t2},'.format(**locals())
    if t3 != "":
        world.cfg["main"] += '"valid-lifetime": {t3},'.format(**locals())

    if "global_parameters" in world.cfg:
        world.cfg["main"] += world.cfg["global_parameters"]

    if eth is not None and not eth in world.cfg["interfaces"]:
        add_interface(eth)

    #world.cfg["conf"] += dedent(subnetcfg)
    #world.dhcp["subnet_cnt"] += 1


def prepare_cfg_subnet(step, subnet, pool, eth = None):
    # world.subcfg[0] = [subnet, client class/simple options, options, pools, host reservation]
    if subnet == "default":
        subnet = "192.168.0.0/24"
    if pool == "default":
        pool = "192.168.0.1 - 192.168.0.254"
    if eth is None:
        eth = world.f_cfg.server_iface

    if not "interfaces" in world.cfg:
        world.cfg["interfaces"] = ''

    pointer_start = "{"
    pointer_end = "}"

    if subnet is not "":
        world.subcfg[world.dhcp["subnet_cnt"]][0] += '''{pointer_start} "subnet": "{subnet}"
             '''.format(**locals())
    else:
        world.subnet_add = False
    if pool is not "":
        world.subcfg[world.dhcp["subnet_cnt"]][4] += '{pointer_start}"pool": "{pool}" {pointer_end}'.format(**locals())

        # if eth is not None:
        #     # world.subcfg[world.dhcp["subnet_cnt"]][0] += ', "interface": "{eth}" '.format(**locals())
        #
        #     print "\n"
        #     print "\n\n\n\nabc\n1\n"
        #     print "\n"

    if not eth in world.cfg["interfaces"]:
        add_interface(eth)


def config_client_classification(step, subnet, option_value):
    subnet = int(subnet)
    if len(world.subcfg[subnet][1]) > 2:
        world.subcfg[subnet][1] += ', '
    world.subcfg[subnet][1] += '"client-class": "{option_value}"\n'.format(**locals())


def prepare_cfg_add_option(step, option_name, option_value, space,
                           option_code = None, type = 'default', where = 'options'):
    if not where in world.cfg:
        world.cfg[where] = '"option-data": ['
    else:
        world.cfg[where] += ","

    # check if we are configuring default option or user option via function "prepare_cfg_add_custom_option"
    if type == 'default':
        option_code = kea_options4.get(option_name)

    pointer_start = "{"
    pointer_end = "}"
    csv_format, option_value = check_empty_value(option_value)

    assert option_code is not None, "Unsupported option name for other Kea4 options: " + option_name

    world.cfg[where] += '''
            \t{pointer_start}"csv-format": {csv_format}, "code": {option_code}, "data": "{option_value}",
            \t"name": "{option_name}", "space": "{space}"{pointer_end}'''.format(**locals())


def prepare_cfg_add_option_subnet(step, option_name, subnet, option_value):
    # check if we are configuring default option or user option via function "prepare_cfg_add_custom_option"
    space = world.cfg["space"]
    subnet = int(subnet)
    option_code = kea_options4.get(option_name)

    pointer_start = "{"
    pointer_end = "}"

    assert option_code is not None, "Unsupported option name for other Kea4 options: " + option_name
    if len(world.subcfg[subnet][2]) > 10:
        world.subcfg[subnet][2] += ','

    world.subcfg[subnet][2] += '''
            \t{pointer_start}"csv-format": true, "code": {option_code}, "data": "{option_value}",
            \t"name": "{option_name}", "space": "{space}"{pointer_end}'''.format(**locals())


def prepare_cfg_add_option_shared_subnet(step, option_name, shared_subnet, option_value):
    # check if we are configuring default option or user option via function "prepare_cfg_add_custom_option"
    space = world.cfg["space"]
    shared_subnet = int(shared_subnet)
    option_code = kea_options4.get(option_name)

    pointer_start = "{"
    pointer_end = "}"

    assert option_code is not None, "Unsupported option name for other Kea4 options: " + option_name
    if len(world.shared_subcfg[shared_subnet][0]) > 10:
        world.shared_subcfg[shared_subnet][0] += ','

    world.shared_subcfg[shared_subnet][0] += '''
            {pointer_start}"csv-format": true, "code": {option_code}, "data": "{option_value}",
            "name": "{option_name}", "space": "{space}"{pointer_end}'''.format(**locals())


def add_siaddr(step, addr, subnet_number):
    if subnet_number is None:
        if not "simple_options" in world.cfg:
            world.cfg["simple_options"] = ''
        else:
            world.cfg["simple_options"] += ','
        world.cfg["simple_options"] += '"next-server": "{addr}"'.format(**locals())
    else:
        subnet = int(subnet_number)
        if len(world.subcfg[subnet][1]) > 2:
            world.subcfg[subnet][1] += ', '
        world.subcfg[subnet][1] += '"next-server": "{addr}"\n'.format(**locals())


def disanable_client_echo(step):
    # after using it, we should revert that at the end!
    # keep that in mind when first time using it.
    if not "simple_options" in world.cfg:
        world.cfg["simple_options"] = ''
    else:
        world.cfg["simple_options"] += ','
    world.cfg["simple_options"] += '"echo-client-id": "False"'.format(**locals())


def host_reservation(reservation_type, reserved_value, unique_host_value_type, unique_host_value, subnet):
    if len(world.subcfg[subnet][5]) > 20:
        world.subcfg[subnet][5] += ','

    world.subcfg[subnet][5] += "{"
    if reservation_type == "address":
        world.subcfg[subnet][5] += '"{unique_host_value_type}":"{unique_host_value}","ip-address":"{reserved_value}"'.format(**locals())
    elif reservation_type == "hostname":
        world.subcfg[subnet][5] += '"{unique_host_value_type}":"{unique_host_value}","hostname":"{reserved_value}"'.format(**locals())
    else:
        assert False, "Not supported yet."
        # if reservation will allow on another value - add it here

    world.subcfg[subnet][5] += "}"


def host_reservation_extension(reservation_number, subnet, reservation_type, reserved_value):
    pointer = locate_entry(world.subcfg[subnet][5], '}', reservation_number)
    if reservation_type == "address":
        tmp = world.subcfg[subnet][5][:pointer] + ',"ip-address":"{reserved_value}"'.format(**locals())
        tmp += world.subcfg[subnet][5][pointer:]
    elif reservation_type == "hostname":
        tmp = world.subcfg[subnet][5][:pointer] + ',"hostname":"{reserved_value}"'.format(**locals())
        tmp += world.subcfg[subnet][5][pointer:]
    else:
        assert False, "Not supported"
        # if reservation will allow on another value - add it here

    world.subcfg[subnet][5] = tmp


def config_srv_id(id_type, id_value):
    assert False, "Not yet available for Kea4"

## =============================================================
## ================ PREPARE CONFIG BLOCK END  ==================

## =============================================================
## ================ REMOTE SERVER BLOCK START ==================


def build_and_send_config_files(connection_type, configuration_type="config-file"):
    if configuration_type == "config-file" and connection_type == "SSH":
        world.cfg['leases'] = world.f_cfg.software_install_path + 'var/kea/kea-leases4.csv'
        add_defaults()
        set_kea_ctrl_config()
        cfg_write()
        fabric_send_file(world.cfg["cfg_file"], world.f_cfg.software_install_path + "etc/kea/kea.conf")
        fabric_send_file(world.cfg["cfg_file_2"], world.f_cfg.software_install_path + "etc/kea/keactrl.conf")
        copy_configuration_file(world.cfg["cfg_file"])
        copy_configuration_file(world.cfg["cfg_file_2"], "kea_ctrl_config")
        remove_local_file(world.cfg["cfg_file"])
        remove_local_file(world.cfg["cfg_file_2"])
    elif configuration_type == "config-file" and connection_type is None:
        world.cfg['leases'] = world.f_cfg.software_install_path + 'var/kea/kea-leases4.csv'
        add_defaults()
        set_kea_ctrl_config()
        cfg_write()
        copy_configuration_file(world.cfg["cfg_file"])
        remove_local_file(world.cfg["cfg_file"])


def reconfigure_srv():
    #build_and_send_config_files()
    result = fabric_sudo_command('(' + world.f_cfg.software_install_path + 'sbin/keactrl reload '
                                 + ' & ); sleep ' + str(world.f_cfg.sleep_time_1))
    check_kea_process_result(True, result, 'reconfigure')


def start_srv(start, process):
    """
    Start kea with generated config
    """
    #build_and_send_config_files() it's now separate step
    world.cfg['leases'] = world.f_cfg.software_install_path + 'var/kea/kea-leases4.csv'
    v6, v4 = check_kea_status()

    if process is None:
        process = "starting"
    # check process - if None add some.
    if not v4:
        result = fabric_sudo_command('( ' + world.f_cfg.software_install_path + 'sbin/keactrl start '
                                     + ' & ); sleep ' + str(world.f_cfg.sleep_time_1))
        check_kea_process_result(start, result, process)
    else:
        result = fabric_sudo_command('(' + world.f_cfg.software_install_path + 'sbin/keactrl stop '
                                     + ' & ); sleep ' + str(world.f_cfg.sleep_time_1))
        #check_kea_process_result(start, result, process)
        result = fabric_sudo_command('(' + world.f_cfg.software_install_path + 'sbin/keactrl start '
                                     + ' & ); sleep ' + str(world.f_cfg.sleep_time_1))
        check_kea_process_result(start, result, process)
        sleep(2)


def prepare_cfg_prefix(step, prefix, length, delegated_length, subnet):
    assert False, "This function can be used only with DHCPv6"