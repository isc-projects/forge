# Copyright (C) 2013-2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Wlodzimierz Wencel

# pylint: disable=consider-using-f-string
# pylint: disable=line-too-long
# pylint: disable=possibly-unused-variable
# pylint: disable=redundant-keyword-arg
# pylint: disable=unnecessary-pass
# pylint: disable=unspecified-encoding
# pylint: disable=unused-argument

import os
import time
import base64
import string

from src.forge_cfg import world
from src.softwaresupport.bind9_server.bind_configs import config_file_set
# from src.softwaresupport.bind9_server.bind_configs import keys  # those are needed for managed-keys.bind
from src.softwaresupport.multi_server_functions import fabric_sudo_command, fabric_download_file
from src.softwaresupport.multi_server_functions import fabric_remove_file_command
from src.softwaresupport.multi_server_functions import check_local_path_for_downloaded_files, send_content


def make_file(name, content):
    with open(name, 'w') as f:
        f.write(content)


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
    if "named.conf" not in world.cfg:
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
    if "named.conf" not in world.cfg:
        assert False, 'Please start configuring DNS server with step: DNS server is configured on...'

    pointer_s = "{"
    pointer_s = "}"
    world.cfg["named.conf"] += 'key "{key_name}" {pointer_s} algorithm {algorithm};' \
                               'secret "{key_value}";{pointer_e};'.format(**locals())


def add_rndc(address, port, alg, value):
    if "named.conf" not in world.cfg:
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


def _patch_config(cfg, override_dns=None):
    tpl = string.Template(cfg)
    if override_dns is not None:
        dns_addr = override_dns
    elif world.f_cfg.proto == 'v4':
        dns_addr = world.f_cfg.dns4_addr
    else:
        dns_addr = world.f_cfg.dns6_addr
    return tpl.safe_substitute(data_path=os.path.join(world.f_cfg.dns_data_path, 'namedb'),
                               dns_addr=dns_addr,
                               dns_port=world.f_cfg.dns_port)


def use_config_set(number, override_dns=None):
    if number not in config_file_set:
        assert False, "There is no such config file set"

    world.cfg["dns_log_file"] = '/tmp/dns.log'

    namedb_dir = os.path.join(world.f_cfg.dns_data_path, 'namedb')
    fabric_sudo_command('mkdir -p %s' % namedb_dir)
    fabric_sudo_command('chmod a+w %s' % namedb_dir)

    send_content('named.conf', os.path.join(world.f_cfg.dns_data_path, 'named.conf'),
                 _patch_config(config_file_set[number][0], override_dns), 'dns')

    send_content('rndc.conf', os.path.join(world.f_cfg.dns_data_path, 'rndc.conf'),
                 config_file_set[number][1], 'dns')

    send_content('fwd.db', os.path.join(namedb_dir, 'fwd.db'),
                 config_file_set[number][2], 'dns')

    send_content('rev.db', os.path.join(namedb_dir, 'rev.db'),
                 config_file_set[number][3], 'dns')

    if len(config_file_set[number]) == 8:
        send_content('fwd2.db', os.path.join(namedb_dir, 'fwd2.db'),
                     config_file_set[number][4], 'dns')

        send_content('rev2.db', os.path.join(namedb_dir, 'rev2.db'),
                     config_file_set[number][5], 'dns')

        send_content('fwd3.db', os.path.join(namedb_dir, 'fwd3.db'),
                     config_file_set[number][6], 'dns')

        send_content('rev3.db', os.path.join(namedb_dir, 'rev3.db'),
                     config_file_set[number][7], 'dns')

    # needed for dns sec validation
    # send_content('managed-keys.bind', os.path.join(world.f_cfg.dns_data_path, 'managed-keys.bind'),
    #              keys, 'dns')


def upload_dns_keytab(dns_keytab):
    content = base64.decodebytes(bytes(dns_keytab, 'ascii'))
    namedb_dir = os.path.join(world.f_cfg.dns_data_path, 'namedb')
    p = os.path.join(namedb_dir, 'dns.keytab')
    fabric_sudo_command("cp /tmp/dns.keytab %s" % p)
    send_content('dns.keytab', p, content, 'dns')
    if world.f_cfg.dns_data_path.startswith('/etc'):
        # when installed from pkg
        fabric_sudo_command('chmod 440 %s' % p)
        if world.server_system == 'redhat':
            fabric_sudo_command('chown root:named %s' % p)
        else:
            fabric_sudo_command('chown root:bind %s' % p)
    else:
        # when compiled and installed from sources
        fabric_sudo_command('chmod 400 %s' % p)
        fabric_sudo_command('chown root:root %s' % p)


def stop_srv(value=False, destination_address=world.f_cfg.mgmt_address):
    if world.server_system == 'redhat':
        srv_name = 'named'
    else:
        srv_name = 'bind9'

    if world.f_cfg.dns_data_path.startswith('/etc'):
        fabric_sudo_command('systemctl stop %s' % srv_name,
                            hide_all=value, destination_host=destination_address)
    else:
        fabric_sudo_command('killall named',
                            hide_all=value, destination_host=destination_address, ignore_errors=True)
    time.sleep(world.f_cfg.sleep_time_1)


def restart_srv(destination_address=world.f_cfg.mgmt_address):
    stop_srv(destination_address=destination_address)
    start_srv(True, None, destination_address=destination_address)


def start_srv(success, destination_address=world.f_cfg.mgmt_address):
    if world.server_system == 'redhat':
        srv_name = 'named'
    else:
        srv_name = 'bind9'

    if world.f_cfg.dns_data_path.startswith('/etc'):
        fabric_sudo_command('systemctl restart %s' % srv_name,
                            destination_host=destination_address)
    else:
        fabric_sudo_command('(' + os.path.join(world.f_cfg.dns_server_install_path, 'named') + ' -c ' +
                            os.path.join(world.f_cfg.dns_data_path, 'named.conf') + ' & )',
                            destination_host=destination_address)

    time.sleep(world.f_cfg.sleep_time_1 + 4)

    if world.f_cfg.dns_data_path.startswith('/etc'):
        fabric_sudo_command("systemctl status %s | grep 'Active: active (running)'" % srv_name,
                            destination_host=destination_address)
    else:
        fabric_sudo_command("ps ax | grep 'named -c'",
                            destination_host=destination_address)


def save_leases(destination_address=world.f_cfg.mgmt_address):
    # pointless here, but we don't want import error here.
    pass


def reconfigure_srv(should_succeed: bool = True,
                    destination_address: str = world.f_cfg.mgmt_address):
    """
    Reconfigure the BIND9 server.
    :param should_succeed: whether the reconfiguration is supposed to succeed or fail
    :param destination_address: management address of server
    """
    # TODO implement this when needed
    pass


def save_logs(destination_address=world.f_cfg.mgmt_address):
    fabric_download_file('/tmp/dns.log',
                         check_local_path_for_downloaded_files(world.cfg["test_result_dir"],
                                                               'dns/dns_log_file',
                                                               destination_address),
                         destination_host=destination_address, ignore_errors=True,
                         hide_all=not world.f_cfg.forge_verbose)


def clear_all(destination_address=world.f_cfg.mgmt_address, remove_logs=True):
    stop_srv(value=True, destination_address=destination_address)
    if remove_logs:
        fabric_remove_file_command('/tmp/dns.log', destination_host=destination_address)
    fabric_remove_file_command(os.path.join(world.f_cfg.dns_data_path, 'namedb/*'), destination_host=destination_address)
    fabric_remove_file_command(os.path.join(world.f_cfg.dns_data_path, '*.conf'), destination_host=destination_address)
    # fabric_remove_file_command(os.path.join(world.f_cfg.dns_data_path, 'managed-keys.bind'), destination_host=destination_address)
