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

import sys
import json

from forge_cfg import world


def add_ddns_server(address, port):
    world.ddns_enable = True  # flag for ddns
    world.ddns_add = {}  # part of the config which is added to dhcp config section

    if address == "default":
        address = "127.0.0.1"
    if port == "default":
        port = 53001

    world.ddns_main = {"ip-address": address,
                       "port": int(port),  # this value is passed as string
                       "dns-server-timeout": 100,
                       "reverse-ddns": {'ddns-domains': []},
                       "forward-ddns": {'ddns-domains': []},
                       "tsig-keys": [],
                       "ncr-format": "JSON",  # default value
                       "ncr-protocol": "UDP"}  # default value

    add_ddns_server_options("server-ip", address)
    add_ddns_server_options("enable-updates", False)


def add_ddns_server_options(option, value):
    # function test_define_value return everything as string, until this function will be rewritten
    # we will have to have such combinations as below
    if value in ["true", "True", "TRUE"]:
        value = True
    if value in ["false", "False", "FALSE"]:
        value = False
    world.ddns_add[option] = value


def add_forward_ddns(name, key_name, ip_address, port, hostname=""):
    world.ddns_main["forward-ddns"] = {"ddns-domains": [{
        "name": name,
        "key-name": key_name,
        "dns-servers": [{
            "hostname": hostname,
            "ip-address": ip_address,
            "port": port
        }]
    }]
    }

    if key_name == "EMPTY_KEY":
        del world.ddns_main["forward-ddns"]["ddns-domains"][0]["key-name"]


def add_reverse_ddns(name, key_name, ip_address, port, hostname=""):
    world.ddns_main["reverse-ddns"] = {"ddns-domains": [{
        "name": name,
        "key-name": key_name,
        "dns-servers": [{
            "hostname": hostname,
            "ip-address": ip_address,
            "port": port
        }]
    }]
    }

    if key_name == "EMPTY_KEY":
        del world.ddns_main["reverse-ddns"]["ddns-domains"][0]["key-name"]


def add_keys(secret, name, algorithm):
    world.ddns_main["tsig-keys"].append({
        "secret": secret,
        "name": name,
        "algorithm": algorithm,
        "digest-bits": 0  # default value
    })


def ddns_open_control_channel_socket(socket_name=None):
    if socket_name is not None:
        socket_path = world.f_cfg.run_join(socket_name)
    else:
        socket_path = world.f_cfg.run_join('ddns_control_socket')

    world.ddns_main["control-socket"] = {"socket-type": "unix", "socket-name": socket_path}


def build_ddns_config():
    # let's for now don't change how config is saved to the file
    world.ddns = ',"DhcpDdns":' + json.dumps(world.ddns_main)
