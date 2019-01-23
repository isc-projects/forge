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

import sys

if 'pytest' in sys.argv[0]:
    from features.lettuce_compat import world
else:
    from lettuce import world


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

    world.ddns_main += ',\n"DhcpDdns": {pointer_start} "ip-address": "{address}","dns-server-timeout": 100,' \
                       ' "port": {port},'.format(**locals())

    add_ddns_server_options("server-ip", address)


def add_ddns_server_options(option, value):
    pointer_start = "{"
    pointer_end = "}"
    if world.ddns_add == "":
        world.ddns_add += '"dhcp-ddns":{'
    else:
        world.ddns_add += ","
    if value in ["true", "false", "True", "False", "TRUE", "FALSE"]:
        world.ddns_add += '"{option}": {value}'.format(**locals())
    else:
        world.ddns_add += '"{option}": "{value}"'.format(**locals())


def add_forward_ddns(name, key_name, ip_address, port):
    pointer_start = "{"
    pointer_end = "}"

    if key_name == "EMPTY_KEY":
        world.ddns_forw.append('''{pointer_start} "name": "{name}",
                                "dns-servers": [ {pointer_start}
                                    "ip-address": "{ip_address}",
                                    "port": {port} {pointer_end}
                                    ]
                                {pointer_end} '''.format(**locals()))
    else:
        world.ddns_forw.append('''{pointer_start} "name": "{name}", "key-name": "{key_name}",
                                "dns-servers": [ {pointer_start}
                                    "ip-address": "{ip_address}",
                                    "port": {port} {pointer_end}
                                    ]
                                {pointer_end} '''.format(**locals()))


def add_reverse_ddns(name, key_name, ip_address, port):
    pointer_start = "{"
    pointer_end = "}"

    if key_name == "EMPTY_KEY":
        world.ddns_rev.append('''{pointer_start} "name": "{name}",
                                "dns-servers": [ {pointer_start}
                                    "ip-address": "{ip_address}",
                                    "port": {port} {pointer_end}
                                    ]
                                {pointer_end} '''.format(**locals()))
    else:
        world.ddns_rev.append('''{pointer_start} "name": "{name}", "key-name": "{key_name}",
                                "dns-servers": [ {pointer_start}
                                    "ip-address": "{ip_address}",
                                    "port": {port} {pointer_end}
                                    ]
                                {pointer_end} '''.format(**locals()))


def add_keys(secret, name, algorithm):
    pointer_start = "{"
    pointer_end = "}"

    world.ddns_keys.append('''
    {pointer_start}
        "secret": "{secret}",
        "name": "{name}",
        "algorithm": "{algorithm}"
      {pointer_end}'''.format(**locals()))


def build_ddns_config():
    # TODO multiple domains - now that configuration allow to make one of each
    world.ddns = world.ddns_main
    world.ddns += ' "reverse-ddns": {'
    for each in world.ddns_rev:
        world.ddns += '"ddns-domains": [' + each + ']'
    world.ddns += '}'
    world.ddns += ' ,"forward-ddns": {'
    for each in world.ddns_forw:
        world.ddns += '"ddns-domains": [' + each + ']'
    world.ddns += '}'
    world.ddns += ',"tsig-keys": ['
    if len(world.ddns_keys) > 0:
        world.ddns += world.ddns_keys[0]
        for each in world.ddns_keys[1:]:
            world.ddns += ',' + each
    world.ddns += ']'
    world.ddns += '}'
