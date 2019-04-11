# Copyright (C) 2017 Internet Systems Consortium.
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

from forge_cfg import world


def add_ddns_server(address, port):
    world.ddns_enable = True  # flag for ddns
    world.ddns_add = ""  # part of the config which is added to dhcp config section
    world.ddns_main = ""
    world.ddns_forw = []
    world.ddns_rev = []
    world.ddns_keys = []

    pointer_start = "{"
    pointer_end = "}"

    if address == "default":
        address = "127.0.0.1"
    if port == "default":
        port = "53001"

    world.ddns_main += '\nddns-updates on;\n'

    # add_ddns_server_options("server-ip", address) # don't need it in isc-dhcp


def add_ddns_server_options(option, value):
    world.ddns_add += option + " " + value + ";\n"


def add_forward_ddns(name, key_name, ip_address, port):
    pointer_start = "{"
    pointer_end = "}"
    world.ddns_domainname = name
    if key_name == "EMPTY_KEY":
        world.ddns_forw.append('''\nzone {name}
                                {pointer_start}
                                primary {ip_address};
                                {pointer_end}'''.format(**locals()))
    else:
        world.ddns_forw.append('''\nzone {name}
                                {pointer_start}
                                key {key_name};
                                primary {ip_address};
                                {pointer_end}'''.format(**locals()))


def add_reverse_ddns(name, key_name, ip_address, port):
    pointer_start = "{"
    pointer_end = "}"
    tmp = []
    for each in name.split(".")[::-1]:
        if each.isdigit():
            break
        else:
            tmp.append(each)
    world.ddns_rev_domainname = ".".join(tmp[::-1])

    if key_name == "EMPTY_KEY":
        world.ddns_rev.append('''\nzone {name}
                                {pointer_start}
                                primary {ip_address};
                                {pointer_end}'''.format(**locals()))
    else:
        world.ddns_rev.append('''\nzone {name}
                                {pointer_start}
                                key {key_name};
                                primary {ip_address};
                                {pointer_end}'''.format(**locals()))


def add_keys(secret, name, algorithm):
    pointer_start = "{"
    pointer_end = "}"

    world.ddns_keys.append('''\nkey {name}
                        {pointer_start}
                        secret {secret};
                        algorithm {algorithm};
                        {pointer_end}'''.format(**locals()))


def build_ddns_config():
    world.ddns = world.ddns_main
    world.ddns += world.ddns_add
    for each in world.ddns_keys:
        world.ddns += each
    for each in world.ddns_rev:
        world.ddns += each
    for each in world.ddns_forw:
        world.ddns += each
