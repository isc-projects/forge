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

import logging

from forge_cfg import world

from softwaresupport.multi_server_functions import fabric_run_command, fabric_sudo_command, locate_entry

from softwaresupport.kea import build_and_send_config_files
from softwaresupport.kea import clear_all, clear_logs, clear_leases, start_srv
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
from softwaresupport.kea import prepare_cfg_add_option_shared_subnet, config_client_classification
from softwaresupport.kea import add_option_to_defined_class, config_require_client_classification
from softwaresupport.kea import host_reservation, host_reservation_extension

log = logging.getLogger('forge')


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


def add_siaddr(addr, subnet_number):
    if subnet_number is None:
        world.dhcp_main["next-server"] = addr
    else:
        world.dhcp_main["subnet4"][int(subnet_number)]["next-server"] = addr


def disable_client_echo():
    # after using it, we should revert that at the end!
    # keep that in mind when first time using it.
    world.dhcp_main["echo-client-id"] = False


def config_srv_id(id_type, id_value):
    assert False, "Not yet available for Kea4"


def prepare_cfg_prefix(prefix, length, delegated_length, subnet):
    assert False, "This function can be used only with DHCPv6"
