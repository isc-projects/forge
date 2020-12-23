# Copyright (C) 2013-2020 Internet Systems Consortium.
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

import os
import json
import logging

from forge_cfg import world
from protosupport.multi_protocol_functions import add_variable, execute_shell_cmd, substitute_vars
from softwaresupport.multi_server_functions import fabric_run_command, fabric_send_file, remove_local_file
from softwaresupport.multi_server_functions import copy_configuration_file, fabric_sudo_command, fabric_download_file
from softwaresupport.multi_server_functions import fabric_remove_file_command
from softwaresupport.multi_server_functions import check_local_path_for_downloaded_files

log = logging.getLogger('forge')


# kea_otheroptions was originally designed for vendor options
# because codes sometime overlap with basic options
kea_otheroptions = {
    "tftp-servers": 32,
    "config-file": 33,
    "syslog-servers": 34,
    "device-id": 36,
    "time-servers": 37,
    "time-offset": 38
}

world.kea_options6 = {
    "client-id": 1,
    "server-id": 2,
    "IA_NA": 3,
    "IN_TA": 4,
    "IA_address": 5,
    "preference": 7,
    "elapsedtime": 8,
    "relay-msg": 9,
    "unicast": 12,
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
    "bcmcs-server-dns": 33,
    "bcmcs-server-addr": 34,
    "pana-agent": 40,
    "new-posix-timezone": 41,
    "new-tzdb-timezone": 42,
    "lq-client-link": 48,
    "bootfile-url": 59,
    "bootfile-param": 60,
    "erp-local-domain-name": 65
}

world.kea_options4 = {
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
    "dhcp-server-identifier": 54,
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


def _check_value(value):
    # test_define_value from protosupport.multi_protocol_functions mostly return strings
    # we want to check if string should be boolean or digit and correct type, if not return unchanged value
    if isinstance(value, str):
        if value.isdigit():
            return int(value)
        if value.lower() == "true":
            return True
        if value.lower() == "false":
            return False
    return value


def add_defaults4():
    eth = world.f_cfg.server_iface
    # TODO for now I will just change if condition but the way to go is remove pre-setting timers!
    # although it could affect to many tests, at this point I wont do it
    if "renew-timer" not in world.dhcp_cfg:
        world.dhcp_cfg["renew-timer"] = world.cfg["server_times"]["renew-timer"]
    if "rebind-timer" not in world.dhcp_cfg:
        world.dhcp_cfg["rebind-timer"] = world.cfg["server_times"]["rebind-timer"]
    if "valid-lifetime" not in world.dhcp_cfg:
        world.dhcp_cfg["valid-lifetime"] = world.cfg["server_times"]["valid-lifetime"]

    add_interface(eth)


def add_defaults6():
    if "renew-timer" not in world.dhcp_cfg:
        world.dhcp_cfg["renew-timer"] = world.cfg["server_times"]["renew-timer"]
    if "rebind-timer" not in world.dhcp_cfg:
        world.dhcp_cfg["rebind-timer"] = world.cfg["server_times"]["rebind-timer"]
    if "preferred-lifetime" not in world.dhcp_cfg:
        world.dhcp_cfg["preferred-lifetime"] = world.cfg["server_times"]["preferred-lifetime"]
    if "valid-lifetime" not in world.dhcp_cfg:
        world.dhcp_cfg["valid-lifetime"] = world.cfg["server_times"]["valid-lifetime"]
    eth = world.f_cfg.server_iface
    add_interface(eth)


def add_logger(log_type, severity, severity_level, logging_file=None):
    if world.f_cfg.install_method == 'make':
        if logging_file is None:
            logging_file = 'kea.log'
        logging_file_path = world.f_cfg.log_join(logging_file)
    else:
        if logging_file is None or logging_file == 'stdout':
            logging_file_path = 'stdout'
        else:
            logging_file_path = world.f_cfg.log_join(logging_file)

    logger = {"name": log_type,
              "output_options": [{"output": logging_file_path}],
              "severity": severity}
    if severity_level != "None":
        logger["debuglevel"] = int(severity_level)

    if "loggers" not in world.dhcp_cfg:
        world.dhcp_cfg["loggers"] = []
    world.dhcp_cfg["loggers"].append(logger)


def open_control_channel_socket(socket_name=None):
    if socket_name is not None:
        socket_path = world.f_cfg.run_join(socket_name)
    else:
        socket_path = world.f_cfg.run_join('control_socket')
    world.dhcp_cfg["control-socket"] = {"socket-type": "unix", "socket-name": socket_path}


def create_new_class(class_name):
    if "client-classes" not in world.dhcp_cfg:
        world.dhcp_cfg["client-classes"] = []
    world.dhcp_cfg["client-classes"].append({"name": class_name})


def add_test_to_class(class_number, parameter_name, parameter_value):
    if parameter_name == "option-def":
        if "option-def" not in world.dhcp_cfg["client-classes"][class_number - 1]:
            world.dhcp_cfg["client-classes"][class_number - 1]["option-def"] = []
        world.dhcp_cfg["client-classes"][class_number - 1][parameter_name].append(parameter_value)
    elif parameter_name == "option-data":
        if "option-data" not in world.dhcp_cfg["client-classes"][class_number - 1]:
            world.dhcp_cfg["client-classes"][class_number - 1]["option-data"] = []
        world.dhcp_cfg["client-classes"][class_number - 1][parameter_name].append(parameter_value)
    else:
        world.dhcp_cfg["client-classes"][class_number - 1][parameter_name] = _check_value(parameter_value)


def add_option_to_defined_class(class_no, option_name, option_value):
    space = world.cfg["space"]
    if world.proto == 'v4':
        option_code = world.kea_options4.get(option_name)
    else:
        option_code = world.kea_options6.get(option_name)
        if option_code is None:
            option_code = kea_otheroptions.get(option_name)

    if "option-data" not in world.dhcp_cfg["client-classes"][class_no - 1]:
        world.dhcp_cfg["client-classes"][class_no - 1]["option-data"] = []
    world.dhcp_cfg["client-classes"][class_no - 1]["option-data"].append({"csv-format": True,
                                                                          "code": int(option_code),
                                                                          "data": option_value,
                                                                          "name": option_name,
                                                                          "space": space})


def config_client_classification(subnet, option_value):
    sub = "subnet%s" % world.proto[1]
    world.dhcp_cfg[sub][int(subnet)]["client-class"] = option_value


def config_require_client_classification(subnet, option_value):
    sub = "subnet%s" % world.proto[1]
    subnet = int(subnet)
    if "require-client-classes" not in world.dhcp_cfg[sub][subnet]:
        world.dhcp_cfg[sub][subnet]["require-client-classes"] = []

    world.dhcp_cfg[sub][subnet]["require-client-classes"].append(option_value)


def set_time(which_time, value, subnet=None):
    assert which_time in world.cfg["server_times"], "Unknown time name: %s" % which_time
    value = int(value)
    if subnet is None:
        world.dhcp_cfg[which_time] = value
    else:
        subnet = int(subnet)
        sub = "subnet%s" % world.proto[1]
        world.dhcp_cfg[sub][subnet][which_time] = value


def add_line_in_global(additional_line):
    world.dhcp_cfg.update(additional_line)


def add_line_to_shared_subnet(subnet_id, additional_line):
    world.dhcp_cfg["shared-networks"][subnet_id].update(additional_line)


def add_line_in_subnet(subnet_id, additional_line):
    sub = "subnet%s" % world.proto[1]
    world.dhcp_cfg[sub][subnet_id].update(additional_line)


def prepare_cfg_subnet(subnet, pool, eth=None):
    if world.proto == 'v4':
        if subnet == "default":
            subnet = "192.168.0.0/24"
        if pool == "default":
            pool = "192.168.0.1 - 192.168.0.254"
    else:
        if subnet == "default":
            subnet = "2001:db8:1::/64"
        if pool == "default":
            pool = "2001:db8:1::1 - 2001:db8:1::ffff"
    if eth is None:
        eth = world.f_cfg.server_iface

    sub = "subnet%s" % world.proto[1]
    if sub not in world.dhcp_cfg.keys() and subnet is not "":
        world.dhcp_cfg[sub] = [{}]
    elif sub in world.dhcp_cfg.keys() and subnet is not "":
        world.dhcp_cfg[sub].append({})

    if subnet is not "":
        world.dhcp_cfg[sub][world.dhcp["subnet_cnt"]] = {"subnet": subnet,
                                                         "pools": [],
                                                         "interface": eth}
    if pool is not "":
        world.dhcp_cfg[sub][world.dhcp["subnet_cnt"]]["pools"].append({"pool": pool})
    add_interface(eth)


def config_srv_another_subnet(subnet, pool, eth):
    world.dhcp["subnet_cnt"] += 1
    prepare_cfg_subnet(subnet, pool, eth)


def prepare_cfg_subnet_specific_interface(interface, address, subnet, pool):
    if subnet == "default":
        subnet = "2001:db8:1::/64"
    if pool == "default":
        pool = "2001:db8:1::1 - 2001:db8:1::ffff"

    # This is weird, it's not used in any test looks like we have some errors because it was used
    # TODO write missing tests using specific interface!
    sub = "subnet%s" % world.proto[1]
    if sub not in world.dhcp_cfg.keys():
        world.dhcp_cfg[sub] = [{}]

    if subnet is not "":
        world.dhcp_cfg[sub][world.dhcp["subnet_cnt"]] = {"subnet": subnet,
                                                         "pools": [],
                                                         "interface": interface}
    if pool is not "":
        world.dhcp_cfg[sub][world.dhcp["subnet_cnt"]]["pools"].append({"pool": pool})

    add_interface(interface + "/" + address)


def prepare_cfg_add_custom_option(opt_name, opt_code, opt_type, opt_value, space):
    prepare_cfg_add_option(opt_name, opt_value, space, opt_code, 'user')

    if "option-def" not in world.dhcp_cfg.keys():
        world.dhcp_cfg["option-def"] = []

    world.dhcp_cfg["option-def"].append({"code": int(opt_code), "name": opt_name,
                                         "space": space, "encapsulate": "", "record-types": "",
                                         "array": False, "type": opt_type})


def add_interface(eth):
    if "interfaces-config" not in world.dhcp_cfg.keys():
        world.dhcp_cfg["interfaces-config"] = {"interfaces": []}

    if eth is not None and eth not in world.dhcp_cfg["interfaces-config"]["interfaces"]:
        world.dhcp_cfg["interfaces-config"]["interfaces"].append(eth)


def add_pool_to_subnet(pool, subnet):
    sub = "subnet%s" % world.proto[1]
    world.dhcp_cfg[sub][subnet]["pools"].append({"pool": pool})


def set_conf_parameter_global(parameter_name, value):
    world.dhcp_cfg[parameter_name] = value


def set_conf_parameter_subnet(parameter_name, value, subnet_id):
    sub = "subnet%s" % world.proto[1]
    world.dhcp_cfg[sub][subnet_id][parameter_name] = _check_value(value)
    if parameter_name in ["interface-id", "relay"]:
        world.dhcp_cfg[sub][subnet_id].pop("interface", None)


def add_to_shared_subnet(subnet_def, shared_network_id):
    sub = "subnet%s" % world.proto[1]
    if len(world.dhcp_cfg["shared-networks"]) <= shared_network_id:
        world.dhcp_cfg["shared-networks"].append({})
    if sub not in world.dhcp_cfg["shared-networks"][shared_network_id]:
        world.dhcp_cfg["shared-networks"][shared_network_id][sub] = []

    for i in range(len(world.dhcp_cfg[sub])):
        if world.dhcp_cfg[sub][i]["subnet"] == subnet_def:
            world.dhcp_cfg["shared-networks"][shared_network_id][sub].append(world.dhcp_cfg[sub][i])
            del world.dhcp_cfg[sub][i]
            world.dhcp["subnet_cnt"] -= 1
            break  # removing one from the list will cause error at the end of the loop


def set_conf_parameter_shared_subnet(parameter_name, value, network_id):
    # magic for backward compatibility, was easier than editing all tests we already have.
    value = value.strip("\"")
    if len(value) > 0:
        if value[0] == "{":
            value = json.loads(value)
    if parameter_name == "option-data":
        if "option-data" not in world.dhcp_cfg["shared-networks"][network_id]:
            world.dhcp_cfg["shared-networks"][network_id]["option-data"] = []
        world.dhcp_cfg["shared-networks"][network_id][parameter_name].append(value)
    else:
        world.dhcp_cfg["shared-networks"][network_id][parameter_name] = _check_value(value)

    if parameter_name in ["interface-id", "relay"]:
        world.dhcp_cfg["shared-networks"][network_id].pop("interface", None)
        for subnet in world.dhcp_cfg["shared-networks"][network_id]["subnet%s" % world.proto[1]]:
            subnet.pop("interface", None)


def _check_empty_value(val):
    return (False, "") if val == "<empty>" else (True, val)


def prepare_cfg_add_option(option_name, option_value, space,
                           option_code=None, opt_type='default', where='options'):
    # check if we are configuring default option or user option via function "prepare_cfg_add_custom_option"
    if opt_type == 'default':
        if world.proto == 'v4':
            option_code = world.kea_options4.get(option_name)
        else:
            option_code = world.kea_options6.get(option_name)
            if option_code is None:
                option_code = kea_otheroptions.get(option_name)

    if world.proto == 'v4':
        csv_format, option_value = _check_empty_value(option_value)
    else:
        csv_format = True
    world.dhcp_cfg["option-data"].append({"csv-format": csv_format, "code": int(option_code),
                                          "data": option_value, "name": option_name, "space": space})


def prepare_cfg_add_option_subnet(option_name, subnet, option_value):
    # check if we are configuring default option or user option via function "prepare_cfg_add_custom_option"
    space = world.cfg["space"]
    subnet = int(subnet)
    if world.proto == 'v4':
        option_code = world.kea_options4.get(option_name)
    else:
        option_code = world.kea_options6.get(option_name)
        if option_code is None:
            option_code = kea_otheroptions.get(option_name)

    if world.proto == 'v4':
        csv_format, option_value = _check_empty_value(option_value)
    else:
        csv_format = True

    sub = "subnet%s" % world.proto[1]
    if "option-data" not in world.dhcp_cfg[sub][subnet]:
        world.dhcp_cfg[sub][subnet]["option-data"] = []
    world.dhcp_cfg[sub][subnet]["option-data"].append({"csv-format": csv_format, "code": int(option_code),
                                                       "data": option_value, "name": option_name, "space": space})


def prepare_cfg_add_option_shared_subnet(option_name, shared_subnet, option_value):
    # check if we are configuring default option or user option via function "prepare_cfg_add_custom_option"
    space = world.cfg["space"]
    shared_subnet = int(shared_subnet)
    if world.proto == 'v4':
        option_code = world.kea_options4.get(option_name)
    else:
        option_code = world.kea_options6.get(option_name)
        if option_code is None:
            option_code = kea_otheroptions.get(option_name)

    assert option_code is not None, "Unsupported option name for other Kea4 options: " + option_name

    if "option-data" not in world.dhcp_cfg["shared-networks"][shared_subnet]:
        world.dhcp_cfg["shared-networks"][shared_subnet]["option-data"] = []
    world.dhcp_cfg["shared-networks"][shared_subnet]["option-data"].append({"csv-format": True,
                                                                            "code": int(option_code),
                                                                            "data": option_value,
                                                                            "name": option_name,
                                                                            "space": space})


def host_reservation(reservation_type, reserved_value, unique_host_value_type, unique_host_value, subnet):
    sub = "subnet%s" % world.proto[1]
    if "reservations" not in world.dhcp_cfg[sub][subnet]:
        world.dhcp_cfg[sub][subnet]["reservations"] = []

    # v6 for ip-address reservation and prefixes using different format and names:
    if world.proto[1] == '6':
        if reservation_type in ["ip-address", "prefix", "prefixes"]:
            if reservation_type[-2:] != "es":
                # in tests there are "prefixes", "prefix" and "ip-address", but we need "es" at the end
                reservation_type += "es"
            # add reservation as list if it's prefix or address
            world.dhcp_cfg[sub][subnet]["reservations"].append({unique_host_value_type: unique_host_value,
                                                                reservation_type: [reserved_value]})
        else:
            world.dhcp_cfg[sub][subnet]["reservations"].append({unique_host_value_type: unique_host_value,
                                                                reservation_type: reserved_value})
    else:
        world.dhcp_cfg[sub][subnet]["reservations"].append({unique_host_value_type: unique_host_value,
                                                            reservation_type: reserved_value})


def host_reservation_extension(reservation_number, subnet, reservation_type, reserved_value):
    sub = "subnet%s" % world.proto[1]
    if world.proto[1] == '6':
        if reservation_type in ["ip-address", "prefix", "prefixes"]:
            if reservation_type[-2:] != "es":
                reservation_type += "es"
            if not reservation_type in world.dhcp_cfg[sub][subnet]["reservations"][reservation_number]:
                world.dhcp_cfg[sub][subnet]["reservations"][reservation_number][reservation_type] = []
            world.dhcp_cfg[sub][subnet]["reservations"][reservation_number][reservation_type].append(reserved_value)
        else:
            world.dhcp_cfg[sub][subnet]["reservations"][reservation_number].update({reservation_type: reserved_value})
    else:
        world.dhcp_cfg[sub][subnet]["reservations"][reservation_number].update({reservation_type: reserved_value})


def _config_db_backend():
    if world.f_cfg.db_type == "" or world.f_cfg.db_type == "memfile":
        world.dhcp_cfg["lease-database"] = {"type": "memfile"}
    else:
        world.dhcp_cfg["lease-database"] = {"type": world.f_cfg.db_type,
                                            "name": world.f_cfg.db_name,
                                            "host": world.f_cfg.db_host,
                                            "user": world.f_cfg.db_user,
                                            "password": world.f_cfg.db_passwd}
        if world.f_cfg.db_type in ["cql"]:
            if "keyspace" not in world.dhcp_cfg["lease-database"].keys():
                world.dhcp_cfg["lease-database"] = {"keyspace": "keatest"}

    # set reservations
    if world.reservation_backend in ["mysql", "postgresql", "cql"]:
        world.dhcp_cfg["hosts-database"] = {"type": world.reservation_backend,
                                            "name": world.f_cfg.db_name,
                                            "host": world.f_cfg.db_host,
                                            "user": world.f_cfg.db_user,
                                            "password": world.f_cfg.db_passwd}

        if world.reservation_backend in ["cql"]:
            # if value is not given in the test - use default (backward compatibility)
            if "keyspace" not in world.dhcp_cfg["hosts-database"].keys():
                world.dhcp_cfg["hosts-database"] = {"keyspace": "keatest"}


def add_hooks(library_path):
    if "libdhcp_ha" in library_path:
        world.dhcp_cfg["hooks-libraries"].append({"library": library_path,
                                                  "parameters": {
                                                      "high-availability": [{"peers": [],
                                                                             "state-machine": {"states": []}}]}})
    else:
        world.dhcp_cfg["hooks-libraries"].append({"library": library_path})


def add_parameter_to_hook(hook_no, parameter_name, parameter_value):
    if "parameters" not in world.dhcp_cfg["hooks-libraries"][hook_no-1].keys():
        world.dhcp_cfg["hooks-libraries"][hook_no - 1]["parameters"] = {}
    if parameter_value in ["True", "true"]:
        parameter_value = True
    elif parameter_value in ["False", 'false']:
        parameter_value = False
    world.dhcp_cfg["hooks-libraries"][hook_no-1]["parameters"][parameter_name] = parameter_value


def ha_add_parameter_to_hook(parameter_name, parameter_value):
    # First let's find HA hook in the list:
    # btw.. I wonder why "high-availability" is list of dictionaries not dictionary
    # and it's just for current backward compatibility, I will change it when I will get back to HA tests
    for hook in world.dhcp_cfg["hooks-libraries"]:
        if "libdhcp_ha" in hook["library"]:
            if parameter_name == "machine-state":
                hook["parameters"]["high-availability"][0]["state-machine"]["states"].append(parameter_value)
            elif parameter_name == "peers":
                if isinstance(parameter_value, str):
                    parameter_value.strip("'")
                    parameter_value = json.loads(parameter_value)
                hook["parameters"]["high-availability"][0]["peers"].append(parameter_value)
            elif parameter_name == "lib":
                pass
            else:
                if parameter_value.isdigit():
                    parameter_value = int(parameter_value)
                else:
                    parameter_value = parameter_value.strip("\"")
                hook["parameters"]["high-availability"][0][parameter_name] = parameter_value


def update_ha_hook_parameter(param):
    assert isinstance(param, dict), "pass just dict as parameter"
    for hook in world.dhcp_cfg["hooks-libraries"]:
        if "libdhcp_ha" in hook["library"]:
            hook["parameters"]["high-availability"][0].update(param)


def agent_control_channel(host_address, host_port, socket_name='control_socket'):
    if world.f_cfg.install_method == 'make':
        logging_file = 'kea.log-CA'
        logging_file_path = world.f_cfg.log_join(logging_file)
    else:
        logging_file_path = 'stdout'

    world.ctrl_enable = True
    server_socket_type = "dhcp%s" % world.proto[1]
    world.ca_cfg["Control-agent"] = {'http-host': host_address,
                                     'http-port':  int(host_port),
                                     'control-sockets': {server_socket_type: {"socket-type": "unix",
                                                                              "socket-name": world.f_cfg.run_join(socket_name)}},
                                     "loggers": [
                                         {"debuglevel": 99, "name": "kea-ctrl-agent",
                                          "output_options": [{"output": logging_file_path}],
                                          "severity": "DEBUG"}]}


def config_srv_id(id_type, id_value):
    if world.proto == 'v4':
        assert False, "Not yet available for Kea4"

    id_value = id_value.replace(":", "")
    if id_type == "EN":
        world.dhcp_cfg["server-id"] = {"type": "EN",
                                       "enterprise-id": int(id_value[4:12], 16),
                                       "identifier": id_value[12:]}
    elif id_type == "LLT":
        world.dhcp_cfg["server-id"] = {"type": "LLT",
                                       "htype": int(id_value[4:8], 16),
                                       "identifier": id_value[16:],
                                       "time": int(id_value[8:16], 16)}
    elif id_type == "LL":
        world.dhcp_cfg["server-id"] = {"type": "LL",
                                       "htype": int(id_value[4:8], 16),
                                       "identifier": id_value[8:]}


def prepare_cfg_prefix(prefix, length, delegated_length, subnet):
    if world.proto == 'v4':
        assert False, "Not available for DHCPv4"

    sub = "subnet%s" % world.proto[1]
    world.dhcp_cfg[sub][int(subnet)].update({"pd-pools": [{"delegated-len": int(delegated_length),
                                                           "prefix": prefix,
                                                           "prefix-len": int(length)}]})


def add_siaddr(addr, subnet_number):
    if world.proto == 'v6':
        assert False, "Not available for DHCPv6"

    if subnet_number is None:
        world.dhcp_cfg["next-server"] = addr
    else:
        world.dhcp_cfg["subnet4"][int(subnet_number)]["next-server"] = addr


def disable_client_echo():
    if world.proto == 'v6':
        assert False, "Not available for DHCPv6"
    world.dhcp_cfg["echo-client-id"] = False


def _set_kea_ctrl_config():
    if world.f_cfg.software_install_path.endswith('/'):
        path = world.f_cfg.software_install_path[:-1]
    else:
        path = world.f_cfg.software_install_path

    kea6 = 'no'
    kea4 = 'no'
    ddns = 'no'
    ctrl_agent = 'no'
    if "kea6" in world.cfg["dhcp_under_test"]:
        kea6 = 'yes'
    elif "kea4" in world.cfg["dhcp_under_test"]:
        kea4 = 'yes'
    if world.ddns_enable:
        ddns = 'yes'
    if world.ctrl_enable:
        ctrl_agent = 'yes'
    world.cfg["keactrl"] = '''kea_config_file={path}/etc/kea/kea.conf
    dhcp4_srv={path}/sbin/kea-dhcp4
    dhcp6_srv={path}/sbin/kea-dhcp6
    dhcp_ddns_srv={path}/sbin/kea-dhcp-ddns
    ctrl_agent_srv={path}/sbin/kea-ctrl-agent
    netconf_srv={path}/sbin/kea-netconf
    kea_dhcp4_config_file={path}/etc/kea/kea-dhcp4.conf
    kea_dhcp6_config_file={path}/etc/kea/kea-dhcp6.conf
    kea_dhcp_ddns_config_file={path}/etc/kea/kea-dhcp-ddns.conf
    kea_ctrl_agent_config_file={path}/etc/kea/kea-ctrl-agent.conf
    kea_netconf_config_file={path}/etc/kea/kea-netconf.conf
    dhcp4={kea4}
    dhcp6={kea6}
    dhcp_ddns={ddns}
    kea_verbose=no
    netconf=no
    ctrl_agent={ctrl_agent}
    '''.format(**locals())


def _cfg_write():
    # For now let's keep to old system of sending config file
    cfg_file = open(world.cfg["cfg_file_2"], 'w')
    cfg_file.write(world.cfg["keactrl"])
    cfg_file.close()

    if world.f_cfg.install_method == 'make':
        logging_file = world.f_cfg.log_join('kea.log')
    else:
        logging_file = 'stdout'

    add_logger('kea-dhcp%s' % world.proto[1], "DEBUG", 99, logging_file)

    _config_db_backend()

    dhcp = "Dhcp%s" % world.proto[1]
    # hooks that are not MT compatible (ever or at this moment)
    list_of_non_mt_hooks = ["libdhcp_host_cache.so", "libdhcp_legal_log.so", "libdhcp_radius.so", "libdhcp_user_chk.so"]

    # all configured hooks
    list_of_used_hooks = []
    for hooks in world.dhcp_cfg["hooks-libraries"]:
        list_of_used_hooks.append(hooks["library"].split("/")[-1])

    # if any of configured hooks is not working with multi-threading then do NOT enable multi-threading in kea config
    if len(set(list_of_used_hooks).intersection(list_of_non_mt_hooks)) == 0 and world.f_cfg.multi_threading_enabled:
        world.dhcp_cfg.update({"multi-threading": {"enable-multi-threading": True, "thread-pool-size": 2,
                                                   "packet-queue-size": 16}})

    world.dhcp_cfg = {dhcp: world.dhcp_cfg}

    if world.ddns_enable:
        world.ddns_cfg = {"DhcpDdns": world.ddns_cfg}
        add_variable("DDNS_CONFIG", json.dumps(world.ddns_cfg), False)
        with open("kea-dhcp-ddns.conf", 'w') as conf_file:
            conf_file.write(json.dumps(world.ddns_cfg, indent=4, sort_keys=True))

    if world.ctrl_enable:
        add_variable("AGENT_CONFIG", json.dumps(world.ca_cfg), False)
        with open("kea-ctrl-agent.conf", 'w') as conf_file:
            conf_file.write(json.dumps(world.ca_cfg, indent=4, sort_keys=True))

    add_variable("DHCP_CONFIG", json.dumps(world.dhcp_cfg), False)

    with open("kea-dhcp%s.conf" % world.proto[1], 'w') as conf_file:
        conf_file.write(json.dumps(world.dhcp_cfg, indent=4, sort_keys=True))


def _write_cfg2(cfg):
    log.info('provisioned cfg:\n%s', cfg)
    if "Control-agent" in cfg:
        with open("kea-ctrl-agent.conf", 'w') as cfg_file:
            json.dump({"Control-agent": cfg["Control-agent"]}, cfg_file, sort_keys=True,
                      indent=4, separators=(',', ': '))
    if "Dhcp%s" % world.proto[1] in cfg:
        with open("kea-dhcp%s.conf" % world.proto[1], 'w') as cfg_file:
            json.dump({"Dhcp%s" % world.proto[1]: cfg["Dhcp%s" % world.proto[1]]},
                      cfg_file, sort_keys=True, indent=4, separators=(',', ': '))

    if "DhcpDdns" in cfg:
        with open("kea-dhcp-ddns.conf", 'w') as cfg_file:
            json.dump({"DhcpDdns": cfg["DhcpDdns"]}, cfg_file, sort_keys=True, indent=4, separators=(',', ': '))

    cfg_file = open(world.cfg["cfg_file_2"], 'w')
    cfg_file.write(world.cfg["keactrl"])
    cfg_file.close()


def build_and_send_config_files(connection_type, configuration_type="config-file",
                                destination_address=world.f_cfg.mgmt_address, cfg=None):
    """
    Generate final config file, save it to test result directory
    and send it to remote system unless testing step will define differently.
    :param connection_type: for now two values expected: SSH and None for stating if files should be send
    :param configuration_type: for now supported just config-file, generate file and save to results dir
    :param destination_address: address of remote system to which conf file will be send,
    default it's world.f_cfg.mgmt_address
    """

    # generate config files content
    if destination_address not in world.f_cfg.multiple_tested_servers:
        world.multiple_tested_servers.append(destination_address)

    substitute_vars(world.dhcp_cfg)
    if world.proto == 'v4':
        add_defaults4()
    else:
        add_defaults6()

    _set_kea_ctrl_config()

    if cfg is None:
        _cfg_write()
    else:
        _write_cfg2(cfg)

    kea_conf_files = ["kea-dhcp%s.conf" % world.proto[1],
                      "kea-dhcp-ddns.conf",
                      'kea-ctrl-agent.conf']

    # send to server if requested
    if connection_type == "SSH":
        if world.f_cfg.install_method == 'make':
            fabric_send_file(world.cfg["cfg_file_2"],
                             world.f_cfg.etc_join("keactrl.conf"),
                             destination_host=destination_address)

        fabric_send_file("kea-dhcp%s.conf" % world.proto[1],
                         world.f_cfg.etc_join("kea-dhcp%s.conf" % world.proto[1]),
                         destination_host=destination_address)

        if world.ctrl_enable:
            fabric_send_file("kea-ctrl-agent.conf",
                            world.f_cfg.etc_join("kea-ctrl-agent.conf"),
                            destination_host=destination_address)

        if world.ddns_enable:
            fabric_send_file("kea-dhcp-ddns.conf",
                            world.f_cfg.etc_join("kea-dhcp-ddns.conf"),
                            destination_host=destination_address)

    # store files for debug purposes
    if world.f_cfg.install_method == 'make':
        copy_configuration_file(world.cfg["cfg_file_2"], "kea_ctrl_config", destination_host=destination_address)
        remove_local_file(world.cfg["cfg_file_2"])

    copy_configuration_file("kea-dhcp%s.conf" % world.proto[1],
                            "kea-dhcp%s.conf" % world.proto[1], destination_host=destination_address)
    remove_local_file("kea-dhcp%s.conf" % world.proto[1])

    if world.ctrl_enable:
        copy_configuration_file("kea-ctrl-agent.conf", "kea-ctrl-agent.conf", destination_host=destination_address)
        remove_local_file("kea-ctrl-agent.conf")

    if world.ddns_enable:
        copy_configuration_file("kea-dhcp-ddns.conf", "kea-dhcp-ddns.conf", destination_host=destination_address)
        remove_local_file("kea-dhcp-ddns.conf")


def clear_logs(destination_address=world.f_cfg.mgmt_address):
    fabric_remove_file_command(world.f_cfg.log_join('kea.log*'),
                               destination_host=destination_address)


def clear_leases(db_name=world.f_cfg.db_name, db_user=world.f_cfg.db_user, db_passwd=world.f_cfg.db_passwd,
                 destination_address=world.f_cfg.mgmt_address):

    if world.f_cfg.db_type == "mysql":
        # that is tmp solution - just clearing not saving.
        command = 'for table_name in dhcp4_options dhcp6_options ipv6_reservations hosts lease4 lease6 logs; ' \
                  'do mysql -u {db_user} -p{db_passwd} -e' \
                  ' "SET foreign_key_checks = 0; delete from $table_name" {db_name}; done'.format(**locals())
        fabric_run_command(command, destination_host=destination_address)
    elif world.f_cfg.db_type == "postgresql":
        command = 'for table_name in dhcp4_options dhcp6_options ipv6_reservations hosts lease4 lease6 logs;' \
                  ' do psql -U {db_user} -d {db_name} -c "delete from $table_name" ; done'.format(**locals())
        fabric_run_command(command, destination_host=destination_address)
    elif world.f_cfg.db_type == "cql":
        # TODO: hardcoded passwords for now in cassandra, extend it in some time :)
        command = 'for table_name in dhcp_option_scope host_reservations lease4 lease6 logs;' \
                  ' do cqlsh --keyspace=keatest --user=keatest --password=keatest -e "TRUNCATE $table_name;"' \
                  ' ; done'.format(**locals())
        fabric_run_command(command, destination_host=destination_address)
    elif world.f_cfg.db_type in ["memfile", ""]:
        fabric_remove_file_command(world.f_cfg.get_leases_path(), destination_host=destination_address)
    else:
        raise Exception('Unsupported db type %s' % world.f_cfg.db_type)


def clear_pid_leftovers(destination_address):
    # we are using rm -f for files so command always succeed, so let's download it first than remove and rise error
    result = fabric_download_file(world.f_cfg.run_join('kea.kea-dhcp*.pid'),
                                  check_local_path_for_downloaded_files(world.cfg["test_result_dir"],
                                                                        'PID_FILE',
                                                                        destination_address),
                                  destination_host=destination_address, ignore_errors=True)
    if result.succeeded:
        fabric_remove_file_command(world.f_cfg.run_join('kea.kea-dhcp*.pid'),
                                   destination_host=destination_address)

        assert False, "KEA PID FILE FOUND! POSSIBLE KEA CRASH"


def clear_all(tmp_db_type=None, destination_address=world.f_cfg.mgmt_address):
    clear_logs(destination_address)

    # remove pid files
    clear_pid_leftovers(destination_address=destination_address)

    # remove other kea runtime data
    fabric_remove_file_command(world.f_cfg.data_join('*'), destination_host=destination_address)
    fabric_remove_file_command(world.f_cfg.run_join('*'), destination_host=destination_address)

    # use kea script for cleaning mysql
    cmd = 'bash {software_install_path}/share/kea/scripts/mysql/wipe_data.sh '
    cmd += ' `mysql -u{db_user} -p{db_passwd} {db_name} -N -B'
    cmd += '   -e "SELECT CONCAT_WS(\'.\', version, minor) FROM schema_version;" 2>/dev/null` -N -B'
    cmd += ' -u{db_user} -p{db_passwd} {db_name}'
    cmd = cmd.format(software_install_path=world.f_cfg.software_install_path,
                     db_user=world.f_cfg.db_user,
                     db_passwd=world.f_cfg.db_passwd,
                     db_name=world.f_cfg.db_name)
    fabric_run_command(cmd, destination_host=destination_address)

    # use kea script for cleaning pgsql
    cmd = 'PGPASSWORD={db_passwd} bash {software_install_path}/share/kea/scripts/pgsql/wipe_data.sh '
    cmd += ' `PGPASSWORD={db_passwd} psql --set ON_ERROR_STOP=1 -A -t -h "localhost" '
    cmd += '   -q -U {db_user} -d {db_name} -c "SELECT version || \'.\' || minor FROM schema_version;" 2>/dev/null`'
    cmd += ' --set ON_ERROR_STOP=1 -A -t -h "localhost" -q -U {db_user} -d {db_name}'
    cmd = cmd.format(software_install_path=world.f_cfg.software_install_path,
                     db_user=world.f_cfg.db_user,
                     db_passwd=world.f_cfg.db_passwd,
                     db_name=world.f_cfg.db_name)
    fabric_run_command(cmd, destination_host=destination_address)


def _check_kea_status(destination_address=world.f_cfg.mgmt_address):
    v4 = False
    v6 = False
    result = fabric_sudo_command(os.path.join(world.f_cfg.software_install_path, "sbin/keactrl") + " status",
                                 destination_host=destination_address)
    # not very sophisticated but easiest fastest way ;)
    if "DHCPv4 server: inactive" in result:
        v4 = False
    elif "DHCPv4 server: active" in result:
        v4 = True
    if "DHCPv6 server: inactive" in result:
        v6 = False
    elif "DHCPv6 server: active" in result:
        v6 = True
    return v4, v6


def _restart_kea_with_systemctl(destination_address):
    cmd_tpl = 'systemctl restart {service} &&'
    cmd_tpl += ' ts=`systemctl show -p ActiveEnterTimestamp {service}.service | awk \'{{print $2 $3}}\'`;'  # get time of log beginning
    cmd_tpl += ' ts=${{ts:-$(date +"%Y-%m-%d%H:%M:%S")}};'  # if started for the first time then ts is empty so set to current date
    cmd_tpl += ' SECONDS=0; while (( SECONDS < 4 )); do'  # watch logs for max 4 seconds
    cmd_tpl += ' journalctl -u {service}.service --since $ts |'  # get logs since last start of kea service
    cmd_tpl += ' grep "server version .* started" 2>/dev/null;'  # if in the logs there is given sequence then ok
    cmd_tpl += ' if [ $? -eq 0 ]; then break; fi done'

    if world.server_system == 'redhat':
        service_name = 'kea-dhcp%s' % world.proto[1]
    else:
        service_name = 'isc-kea-dhcp%s-server' % world.proto[1]

    cmd = cmd_tpl.format(service=service_name)
    fabric_sudo_command(cmd, destination_host=destination_address)

    if world.ctrl_enable:
        if world.server_system == 'redhat':
            service_name = 'kea-ctrl-agent'
        else:
            service_name = 'isc-kea-ctrl-agent'
        cmd = cmd_tpl.format(service=service_name)
        fabric_sudo_command(cmd, destination_host=destination_address)

    if world.ddns_enable:
        if world.server_system == 'redhat':
            service_name = 'kea-dhcp-ddns'
        else:
            service_name = 'isc-kea-dhcp-ddns-server'
        cmd = cmd_tpl.format(service=service_name)
        fabric_sudo_command(cmd, destination_host=destination_address)


def _reload_kea_with_systemctl(destination_address):
    cmd_tpl = 'systemctl reload {service} &&'
    cmd_tpl += ' ts=`systemctl show -p ExecReload {service}.service | sed -E -n \'s/.*stop_time=\\[(.*)\\].*/\\1/p\'`;'  # get time of log beginning
    cmd_tpl += ' ts=${{ts:-$(date +"%Y-%m-%d%H:%M:%S")}};'  # if started for the first time then ts is empty so set to current date
    cmd_tpl += ' SECONDS=0; while (( SECONDS < 4 )); do'  # watch logs for max 4 seconds
    cmd_tpl += ' journalctl -u {service}.service --since "$ts" |'  # get logs since last start of kea service
    cmd_tpl += ' grep "{sentence}" 2>/dev/null;'  # if in the logs there is given sequence then ok
    cmd_tpl += ' if [ $? -eq 0 ]; then break; fi done'

    if world.server_system == 'redhat':
        service_name = 'kea-dhcp%s' % world.proto[1]
    else:
        service_name = 'isc-kea-dhcp%s-server' % world.proto[1]

    cmd = cmd_tpl.format(service=service_name, sentence='initiate server reconfiguration')
    fabric_sudo_command(cmd, destination_host=destination_address)

    if world.ctrl_enable:
        if world.server_system == 'redhat':
            service_name = 'kea-ctrl-agent'
        else:
            service_name = 'isc-kea-ctrl-agent'
        cmd = cmd_tpl.format(service=service_name, sentence='reloading configuration')
        fabric_sudo_command(cmd, destination_host=destination_address)

    if world.ddns_enable:
        if world.server_system == 'redhat':
            service_name = 'kea-dhcp-ddns'
        else:
            service_name = 'isc-kea-dhcp-ddns-server'
        cmd = cmd_tpl.format(service=service_name, sentence='reloading configuration')
        fabric_sudo_command(cmd, destination_host=destination_address)


def start_srv(start, process, destination_address=world.f_cfg.mgmt_address):
    """
    Start kea with generated config
    """
    if destination_address not in world.f_cfg.multiple_tested_servers:
        world.multiple_tested_servers.append(destination_address)

    if world.f_cfg.install_method == 'make':
        v4_running, v6_running = _check_kea_status(destination_address)

        if process is None:
            process = "starting"
        # check process - if None add some.

        if v4_running and world.proto == 'v4' or v6_running and world.proto == 'v6':
            result = _stop_kea_with_keactrl(destination_address)  # TODO: check result

        result = _start_kea_with_keactrl(destination_address)
        _check_kea_process_result(start, result, process)
    else:
        _restart_kea_with_systemctl(destination_address)


def stop_srv(value=False, destination_address=world.f_cfg.mgmt_address):
    if world.f_cfg.install_method == 'make':
        # for now just killall kea processes and ignore errors
        execute_shell_cmd("killall -q kea-ctrl-agent  kea-dhcp-ddns  kea-dhcp4  kea-dhcp6 || true",
                          save_results=False, dest=destination_address)

    else:
        if world.server_system == 'redhat':
            service_names = 'kea-dhcp4 kea-dhcp6 kea-ctrl-agent kea-dhcp-ddns'
        else:
            service_names = 'isc-kea-dhcp4-server isc-kea-dhcp6-server isc-kea-ctrl-agent isc-kea-dhcp-ddns-server'

        cmd = 'systemctl stop %s' % service_names
        fabric_sudo_command(cmd, destination_host=destination_address)


def _check_kea_process_result(succeed, result, process):
    errors = ["Failed to apply configuration", "Failed to initialize server",
              "Service failed", "failed to initialize Kea"]

    if succeed:
        if any(error_message in result for error_message in errors):
            assert False, 'Server operation: ' + process + ' failed! '
    if not succeed:
        if not any(error_message in result for error_message in errors):
            assert False, 'Server operation: ' + process + ' NOT failed!'


def _start_kea_with_keactrl(destination_host):
    # Start kea services and check if they started ok.
    # - nohup to shield kea services from getting SIGHUP from SSH
    # - in a loop check if there is 'server version .* started' expression in the logs;
    #   repeat the loop only for 4 seconds
    # - sync to disk any logs traced by keactrl or kea services
    # - display these logs to screen using cat so forge can catch errors in the logs
    start_cmd = 'nohup ' + os.path.join(world.f_cfg.software_install_path, 'sbin/keactrl')
    start_cmd += " start  < /dev/null > /tmp/keactrl.log 2>&1; SECONDS=0; while (( SECONDS < 4 ));"
    start_cmd += " do tail %s/var/kea/kea.log 2>/dev/null | grep 'server version .* started' 2>/dev/null;" % world.f_cfg.software_install_path
    start_cmd += " if [ $? -eq 0 ]; then break; fi done;"
    start_cmd += " sync; cat /tmp/keactrl.log"
    return fabric_sudo_command(start_cmd, destination_host=destination_host)


def _stop_kea_with_keactrl(destination_host):
    stop_cmd = os.path.join(world.f_cfg.software_install_path, 'sbin/keactrl') + ' stop'
    return fabric_sudo_command(stop_cmd, destination_host=destination_host)


def _reload_kea_with_keactrl(destination_host):
    stop_cmd = os.path.join(world.f_cfg.software_install_path, 'sbin/keactrl') + ' reload'
    return fabric_sudo_command(stop_cmd, destination_host=destination_host)


def reconfigure_srv(destination_address=world.f_cfg.mgmt_address):
    if world.f_cfg.install_method == 'make':
        result = _reload_kea_with_keactrl(destination_address)
        _check_kea_process_result(True, result, 'reconfigure')
    else:
        _reload_kea_with_systemctl(destination_address)


def restart_srv(destination_address=world.f_cfg.mgmt_address):
    if world.f_cfg.install_method == 'make':
        result = _stop_kea_with_keactrl(destination_address)  # TODO: check result
        result = _start_kea_with_keactrl(destination_address)
    else:
        _restart_kea_with_systemctl(destination_address)


def save_leases(tmp_db_type=None, destination_address=world.f_cfg.mgmt_address):
    if world.f_cfg.db_type in ["mysql", "postgresql", "cql"]:
        # TODO
        pass
    else:
        fabric_download_file(world.f_cfg.get_leases_path(),
                             check_local_path_for_downloaded_files(world.cfg["test_result_dir"],
                                                                   'leases.csv',
                                                                   destination_address),
                             destination_host=destination_address, ignore_errors=True)


def save_logs(destination_address=world.f_cfg.mgmt_address):
    fabric_download_file(world.f_cfg.log_join('kea.log*'),
                         check_local_path_for_downloaded_files(world.cfg["test_result_dir"],
                                                               '.',
                                                               destination_address),
                         destination_host=destination_address, ignore_errors=True)


def db_setup(dest=world.f_cfg.mgmt_address):
    if world.f_cfg.install_method != 'make':
        if world.server_system == 'redhat':
            fabric_sudo_command("rpm -qa '*kea*'", destination_host=dest)
        else:
            fabric_sudo_command("dpkg -l '*kea*'", destination_host=dest)

    if world.f_cfg.disable_db_setup:
        return

    db_name = world.f_cfg.db_name
    db_user = world.f_cfg.db_user
    db_passwd = world.f_cfg.db_passwd

    kea_admin = world.f_cfg.sbin_join('kea-admin')

    # MYSQL
    cmd = "mysql -u root -N -B -e \"DROP DATABASE IF EXISTS {db_name};\"".format(**locals())
    result = fabric_sudo_command(cmd, destination_host=dest)
    assert result.succeeded
    cmd = "mysql -u root -e 'CREATE DATABASE {db_name};'".format(**locals())
    fabric_sudo_command(cmd, destination_host=dest)
    cmd = "mysql -u root -e \"CREATE USER '{db_user}'@'localhost' IDENTIFIED BY '{db_passwd}';\"".format(**locals())
    fabric_sudo_command(cmd, ignore_errors=True, destination_host=dest)
    cmd = "mysql -u root -e \"set global log_bin_trust_function_creators=1;\""
    fabric_sudo_command(cmd, ignore_errors=True, destination_host=dest)
    cmd = "mysql -u root -e 'GRANT ALL ON {db_name}.* TO {db_user}@localhost;'".format(**locals())
    fabric_sudo_command(cmd, destination_host=dest)
    cmd = "{kea_admin} db-init mysql -u {db_user} -p {db_passwd} -n {db_name}".format(**locals())
    result = fabric_run_command(cmd, destination_host=dest)
    assert result.succeeded

    # POSTGRESQL
    cmd = "cd /; psql -U postgres -t -c \"DROP DATABASE {db_name}\"".format(**locals())
    fabric_sudo_command(cmd, sudo_user='postgres', ignore_errors=True, destination_host=dest)
    cmd = "cd /; psql -U postgres -c \"CREATE DATABASE {db_name};\"".format(**locals())
    fabric_sudo_command(cmd, sudo_user='postgres', destination_host=dest)
    cmd = "cd /; psql -U postgres -c \"DROP USER IF EXISTS {db_user};\"".format(**locals())
    fabric_sudo_command(cmd, sudo_user='postgres', destination_host=dest)
    cmd = "cd /; psql -U postgres -c \"CREATE USER {db_user} WITH PASSWORD '{db_passwd}';\"".format(**locals())
    fabric_sudo_command(cmd, sudo_user='postgres', destination_host=dest)
    cmd = "cd /; psql -U postgres -c \"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};\"".format(**locals())
    fabric_sudo_command(cmd, sudo_user='postgres', destination_host=dest)
    cmd = "{kea_admin} db-init pgsql -u {db_user} -p {db_passwd} -n {db_name}".format(**locals())
    result = fabric_run_command(cmd, destination_host=dest)
    assert result.succeeded
