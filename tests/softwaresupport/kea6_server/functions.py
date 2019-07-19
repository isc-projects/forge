# Copyright (C) 2013-2018 Internet Systems Consortium.
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

from forge_cfg import world

from softwaresupport.multi_server_functions import locate_entry

from softwaresupport.kea import build_and_send_config_files
from softwaresupport.kea import clear_all, clear_logs, clear_leases
from softwaresupport.kea import start_srv, stop_srv, restart_srv, reconfigure_srv
from softwaresupport.kea import agent_control_channel, save_logs, save_leases
from softwaresupport.kea import ha_add_parameter_to_hook, add_hooks, add_parameter_to_hook, add_logger
from softwaresupport.kea import open_control_channel_socket, create_new_class, add_test_to_class
from softwaresupport.kea import set_logger, set_time, add_line_in_global, config_srv_another_subnet
from softwaresupport.kea import prepare_cfg_add_custom_option, add_interface, add_pool_to_subnet
from softwaresupport.kea import set_conf_parameter_global, set_conf_parameter_subnet, add_line_in_subnet
from softwaresupport.kea import add_line_to_shared_subnet, add_to_shared_subnet, set_conf_parameter_shared_subnet
from softwaresupport.kea import prepare_cfg_subnet_specific_interface, prepare_cfg_subnet
from softwaresupport.kea import prepare_cfg_add_option, prepare_cfg_add_option_subnet
from softwaresupport.kea import prepare_cfg_add_option_shared_subnet
from softwaresupport.kea import kea_otheroptions

world.kea_options6 = {
    "client-id": 1,
    "server-id": 2,
    "IA_NA": 3,
    "IN_TA": 4,
    "IA_address": 5,
    "preference": 7,
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


def config_srv_id(id_type, id_value):
    id_value = id_value.replace(":", "")
    if id_type == "EN":
        world.cfg["server-id"] = '"server-id": {"type": "EN", "enterprise-id": ' + str(int(id_value[4:12], 16)) \
                                 + ', "identifier":" ' + id_value[12:] + ' "},'
    elif id_type == "LLT":
        world.cfg["server-id"] = '"server-id": {"type": "LLT", "htype": ' + str(int(id_value[4:8], 16))\
                                 + ', "identifier": "' + id_value[16:]\
                                 + '", "time": ' + str(int(id_value[8:16], 16)) + ' },'
    elif id_type == "LL":
        world.cfg["server-id"] = '"server-id": {"type": "LL", "htype": ' + str(int(id_value[4:8], 16)) \
                                 + ', "identifier": "' + id_value[8:] + ' "},'
    else:
        assert False, "DUID type unknown."


# =============================================================
# ================ PREPARE CONFIG BLOCK START =================
#  world.subcfg - is prepare for multi-subnet configuration
#  it's concatenated lists:
#  world.subcfg[0] - default subnet
#  each another subnet is append to world.subcfg


def config_client_classification(subnet, option_value):
    subnet = int(subnet)
    if len(world.subcfg[subnet][3]) > 2:
        world.subcfg[subnet][3] += ', '
    world.subcfg[subnet][3] += '"client-class": "{option_value}"\n'.format(**locals())


def config_require_client_classification(subnet, option_value):
    subnet = int(subnet)
    if len(world.subcfg[subnet][3]) > 2:
        world.subcfg[subnet][3] += ', '
    world.subcfg[subnet][3] += '"require-client-classes": ["{option_value}"]\n'.format(**locals())


def prepare_cfg_prefix(prefix, length, delegated_length, subnet):
    subnet = int(subnet)
    pointer_start = "{"
    pointer_end = "}"
    world.subcfg[subnet][1] += """
        "pd-pools": [
        {pointer_start}"delegated-len": {delegated_length},
        "prefix": "{prefix}",
        "prefix-len": {length} {pointer_end}]""".format(**locals())


def host_reservation(reservation_type, reserved_value, unique_host_value_type, unique_host_value, subnet):
    if len(world.subcfg[subnet][5]) > 20:
        world.subcfg[subnet][5] += ','

    world.subcfg[subnet][5] += "{"
    if reservation_type == "address":
        world.subcfg[subnet][5] += '"{unique_host_value_type}":"{unique_host_value}",' \
                                   '"ip-addresses":["{reserved_value}"]'.format(**locals())
    elif reservation_type == "prefix":
        world.subcfg[subnet][5] += '"{unique_host_value_type}":"{unique_host_value}",' \
                                   '"prefixes":["{reserved_value}"]'.format(**locals())
    elif reservation_type == "hostname":
        world.subcfg[subnet][5] += '"{unique_host_value_type}":"{unique_host_value}",' \
                                   '"hostname":"{reserved_value}"'.format(**locals())
    world.subcfg[subnet][5] += "}"


def host_reservation_extension(reservation_number, subnet, reservation_type, reserved_value):
    pointer = locate_entry(world.subcfg[subnet][5], '}', reservation_number)

    if reservation_type == "address":
        tmp = world.subcfg[subnet][5][:pointer] + ',"ip-addresses":["{reserved_value}"]'.format(**locals())
        tmp += world.subcfg[subnet][5][pointer:]
    elif reservation_type == "prefix":
        tmp = world.subcfg[subnet][5][:pointer] + ',"prefixes":["{reserved_value}"]'.format(**locals())
        tmp += world.subcfg[subnet][5][pointer:]
    elif reservation_type == "hostname":
        tmp = world.subcfg[subnet][5][:pointer] + ',"hostname":"{reserved_value}"'.format(**locals())
        tmp += world.subcfg[subnet][5][pointer:]
    else:
        assert False, "Not supported"
        # TODO implement this if we needs it.
    world.subcfg[subnet][5] = tmp


def add_option_to_defined_class(class_no, option_name, option_value):
    space = world.cfg["space"]
    option_code = world.kea_options6.get(option_name)
    if option_code is None:
        option_code = kea_otheroptions.get(option_name)

    pointer_start = "{"
    pointer_end = "}"

    assert option_code is not None, "Unsupported option name for other Kea6 options: " + option_name
    if len(world.classification[class_no-1][2]) > 10:
        world.classification[class_no-1][2] += ','

    world.classification[class_no-1][2] += '''
            {pointer_start}"csv-format": true, "code": {option_code}, "data": "{option_value}",
            "name": "{option_name}", "space": "{space}"{pointer_end}'''.format(**locals())


def add_option_to_main(option, value):
    pass
    # if value in ["True", "true", "TRUE", "False", "FALSE", "false"]:
    #     world.cfg["main"] += ',"{option}":{value}'.format(**locals())
    # else:
    #     world.cfg["main"] += ',"{option}":"{value}"'.format(**locals())
