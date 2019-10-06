# Copyright (C) 2013-2019 Internet Systems Consortium.
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
from softwaresupport.kea import set_time, add_line_in_global, config_srv_another_subnet
from softwaresupport.kea import prepare_cfg_add_custom_option, add_interface, add_pool_to_subnet
from softwaresupport.kea import set_conf_parameter_global, set_conf_parameter_subnet, add_line_in_subnet
from softwaresupport.kea import add_line_to_shared_subnet, add_to_shared_subnet, set_conf_parameter_shared_subnet
from softwaresupport.kea import prepare_cfg_subnet_specific_interface, prepare_cfg_subnet
from softwaresupport.kea import prepare_cfg_add_option, prepare_cfg_add_option_subnet
from softwaresupport.kea import prepare_cfg_add_option_shared_subnet, config_require_client_classification
from softwaresupport.kea import kea_otheroptions, config_client_classification, add_option_to_defined_class
from softwaresupport.kea import host_reservation, host_reservation_extension

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
    if id_type == "EN":
        world.dhcp_main["server-id"] = {"type": "EN",
                                        "enterprise-id": int(id_value[4:12], 16),
                                        "identifier": id_value[12:]}
    elif id_type == "LLT":
        world.dhcp_main["server-id"] = {"type": "LLT",
                                        "htype": int(id_value[4:8], 16),
                                        "identifier": id_value[16:],
                                        "time": int(id_value[8:16], 16)}
    elif id_type == "LL":
        world.dhcp_main["server-id"] = {"type": "LL",
                                        "htype": int(id_value[4:8], 16),
                                        "identifier": id_value[8:]}

# =============================================================
# ================ PREPARE CONFIG BLOCK START =================
#  world.subcfg - is prepare for multi-subnet configuration
#  it's concatenated lists:
#  world.subcfg[0] - default subnet
#  each another subnet is append to world.subcfg


def prepare_cfg_prefix(prefix, length, delegated_length, subnet):
    sub = "subnet%s" % world.proto[1]
    world.dhcp_main[sub][subnet] = {"pd-pools": [{"delegated-len": delegated_length,
                                                  "prefix": prefix,
                                                  "prefix-len": length}]}
