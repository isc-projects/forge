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

from softwaresupport.multi_server_functions import fabric_run_command, fabric_send_file, remove_local_file, \
    copy_configuration_file, fabric_sudo_command, fabric_download_file, fabric_remove_file_command,\
    check_local_path_for_downloaded_files

from lettuce import world
from logging_facility import *

from logging_facility import get_common_logger

from softwaresupport.bind9_server.bind_configs import config_file_set, keys


def make_file(name, content):
    configfile = open(name, 'w')
    configfile.write(content)
    configfile.close()


def add_defaults(ip_type, address, port, direct):
    world.cfg["named.conf"] = 'options {'
    if ip_type == 'v4':
        listen = 'listen-on'
    elif ip_type == 'v6':
        listen = 'listen-on-v6'
    else:
        assert False, "IP type can be set to: v4 or v6"

    pointer_s = "{"
    pointer_e = "}"
    world.cfg["named.conf"] += 'directory "{direct}";' \
                               ' listen-on-v6 port {port} {pointer_s} {address}; {pointer_e};'.format(**locals())
    world.cfg["named.conf"] += 'allow-query-cache { none; }; ' \
                               'allow-update { any; }; allow-query { any; }; recursion no; };'


def add_zone(zone, zone_type, file_nem, key):
    if not "named.conf" in world.cfg:
        assert False, 'Please start configuring DNS server with step: DNS server is configured on...'

    world.cfg["named.conf"] += 'zone "{zone}"'.format(**locals())
    world.cfg["named.conf"] += '{'
    world.cfg["named.conf"] += 'type {zone_type}; file "{file_nem}"; notify no;'.format(**locals())
    world.cfg["named.conf"] += 'allow-update {'
    if key in ['EMPTY_KEY', 'ANY_KEY']:
        world.cfg["named.conf"] += 'any;'
    else:
        world.cfg["named.conf"] += 'key {key};'.format(**locals())
    world.cfg["named.conf"] += '}; allow-query { any; };};'


def add_key(key_name, algorithm, key_value):
    if not "named.conf" in world.cfg:
        assert False, 'Please start configuring DNS server with step: DNS server is configured on...'

    pointer_s = "{"
    pointer_s = "}"
    world.cfg["named.conf"] += 'key "{key_name}" {pointer_s} algorithm {algorithm};' \
                               'secret "{key_value}";{pointer_e};'.format(**locals())


def add_rndc(address, port, alg, value):
    if not "named.conf" in world.cfg:
        assert False, 'Please start configuring DNS server with step: DNS server is configured on...'

    world.cfg["named.conf"] += 'key "rndc-key" {'
    world.cfg["named.conf"] += 'algorithm {alg}; secret "{value}";'.format(**locals())
    world.cfg["named.conf"] += '}; controls {'

    pointer_s = '{'
    pointer_e = '}'
    world.cfg["named.conf"] += 'inet {address} port {port} allow {pointer_s} {address};'.format(**locals())
    world.cfg["named.conf"] += '} keys { "rndc-key"; };};'

    world.cfg["rndc-key"] = 'key "rndc-key" {'
    world.cfg["rndc-key"] += 'algorithm {alg}; secret "{value}";'.format(**locals())
    world.cfg["rndc-key"] += '}; options { default-key "rndc-key";'
    world.cfg["rndc-key"] += 'default-server {address};	default-port 953;{pointer_e};'.format(**locals())


def use_config_set(number):
    if not number in config_file_set:
        assert False, "There is no such config file set"
    make_file('named.conf', config_file_set[number][0])
    make_file('rndc.conf', config_file_set[number][1])
    make_file('fwd.db', config_file_set[number][2])
    make_file('rev.db', config_file_set[number][3])
    world.cfg["dns_log_file"] = '/tmp/dns.log'
    make_file('bind.keys', keys)

    fabric_send_file('named.conf', world.f_cfg.dns_data_path + 'named.conf')
    copy_configuration_file('named.conf', 'dns/DNS_named.conf')
    remove_local_file('named.conf')

    fabric_send_file('rndc.conf', world.f_cfg.dns_data_path + 'rndc.conf')
    copy_configuration_file('rndc.conf', 'dns/DNS_rndc.conf')
    remove_local_file('rndc.conf')

    fabric_send_file('fwd.db', world.f_cfg.dns_data_path + 'namedb/fwd.db')
    copy_configuration_file('fwd.db', 'dns/DNS_fwd.db')
    remove_local_file('fwd.db')

    fabric_send_file('rev.db', world.f_cfg.dns_data_path + 'namedb/rev.db')
    copy_configuration_file('rev.db', 'dns/DNS_rev.db')
    remove_local_file('rev.db')

    fabric_send_file('bind.keys', world.f_cfg.dns_data_path + 'managed-keys.bind')
    copy_configuration_file('bind.keys', 'dns/DNS_managed-keys.bind')
    remove_local_file('bind.keys')


def stop_srv(value=False, destination_address=world.f_cfg.mgmt_address):
    fabric_sudo_command('(killall named & ); sleep ' + str(world.f_cfg.sleep_time_1),
                        hide_all=value, destination_host=destination_address)


def restart_srv(destination_address=world.f_cfg.mgmt_address):
    stop_srv()
    start_srv(True, None)


def start_srv(success, process, destination_address=world.f_cfg.mgmt_address):
    fabric_sudo_command('(' + world.f_cfg.dns_server_install_path + 'named -c ' +
                        world.f_cfg.dns_data_path + 'named.conf & ); sleep ' + str(world.f_cfg.sleep_time_1),
                        destination_host=destination_address)


def save_leases(destination_address=world.f_cfg.mgmt_address):
    # pointless here, but we don't want import error here.
    pass


def reconfigure_srv(destination_address=world.f_cfg.mgmt_address):
    # TODO implement this when needed
    pass


def save_logs(destination_address=world.f_cfg.mgmt_address):
    fabric_download_file('/tmp/dns.log',
                         check_local_path_for_downloaded_files(world.cfg["dir_name"],
                                                               '/dns/dns_log_file', destination_address),
                         destination_host=destination_address)


def clear_all(destination_address=world.f_cfg.mgmt_address):
    stop_srv(value=True, destination_address=destination_address)
    fabric_remove_file_command('/tmp/dns.log', destination_host=destination_address)
    fabric_remove_file_command(world.f_cfg.dns_data_path + 'namedb/*', destination_host=destination_address)
    fabric_remove_file_command(world.f_cfg.dns_data_path + '/*', destination_host=destination_address)
