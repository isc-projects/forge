# Copyright (C) 2017-2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# pylint: disable=invalid-name,line-too-long,unused-argument
# Author: Wlodzimierz Wencel

from src.forge_cfg import world
from src.protosupport.multi_protocol_functions import test_define_value


def add_ddns_server(address, port):
    world.ddns_enable = True  # flag for ddns
    world.ddns_add = ""  # part of the config which is added to dhcp config section
    world.ddns_main = ""
    world.ddns_forw = []
    world.ddns_rev = []
    world.ddns_keys = []

    if address == "default":
        address = "127.0.0.1"
    if port == "default":
        port = "53001"

    world.ddns_main += '\nddns-updates on;\nauthoritative;'

    # add_ddns_server_options("server-ip", address) # don't need it in isc-dhcp


def add_ddns_server_options(option, value):
    world.ddns_add += option + " " + value + ";\n"


def add_forward_ddns(name, key_name, ip_address):
    ip_address = test_define_value(ip_address)[0]
    version = "" if world.proto == 'v4' else 6
    world.ddns_domainname = name
    if key_name == "EMPTY_KEY":
        world.ddns_forw.append(f'\nzone {name} {{ primary{version} {ip_address}; }}')
    else:
        world.ddns_forw.append(f'\nzone {name} {{ key {key_name}; primary{version} {ip_address}; }}')


def add_reverse_ddns(name, key_name, ip_address):
    ip_address = test_define_value(ip_address)[0]
    version = "" if world.proto == 'v4' else 6
    tmp = []
    for each in name.split(".")[::-1]:
        if each.isdigit():
            break
        tmp.append(each)
    world.ddns_rev_domainname = ".".join(tmp[::-1])

    if key_name == "EMPTY_KEY":
        world.ddns_rev.append(f'\nzone {name} {{ primary{version} {ip_address}; }}')
    else:
        world.ddns_rev.append(f'\nzone {name} {{key {key_name}; primary{version} {ip_address};}}')


def add_keys(secret, name, algorithm):
    world.ddns_keys.append(f'\nkey {name} {{algorithm {algorithm};secret {secret};}}')


def build_ddns_config():
    world.ddns = world.ddns_main
    world.ddns += world.ddns_add
    for each in world.ddns_keys:
        world.ddns += each
    for each in world.ddns_rev:
        world.ddns += each
    for each in world.ddns_forw:
        world.ddns += each
