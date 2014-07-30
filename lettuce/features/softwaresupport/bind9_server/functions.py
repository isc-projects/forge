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

from softwaresupport.multi_server_functions import fabric_run_command, fabric_send_file, remove_local_file, \
    copy_configuration_file, fabric_sudo_command, fabric_download_file, fabric_remove_file_command

from lettuce import world
from logging_facility import *

from logging_facility import get_common_logger
from init_all import DNS_SERVER_INSTALL_DIR, DNS_DATA_DIR, SLEEP_TIME_1

from softwaresupport.bind9_server.bind_configs import config_file_set


def make_file(name, content):
    configfile = open(name, 'w')
    configfile.write(content)
    configfile.close()


def use_config_set(number):
    if not number in config_file_set:
        assert False, "There is no such config file set"
    make_file('named.conf', config_file_set[number][0])
    make_file('rndc.conf', config_file_set[number][1])
    make_file('fwd.db', config_file_set[number][2])
    make_file('rev.db', config_file_set[number][3])

    fabric_send_file('named.conf', DNS_DATA_DIR + 'named.conf')
    copy_configuration_file('named.conf', 'dns/DNS_named.conf')
    remove_local_file('named.conf')

    fabric_send_file('rndc.conf', DNS_DATA_DIR + 'rndc.conf')
    copy_configuration_file('rndc.conf', 'dns/DNS_rndc.conf')
    remove_local_file('rndc.conf')

    fabric_send_file('fwd.db', DNS_DATA_DIR + 'namedb/fwd.db')
    copy_configuration_file('fwd.db', 'dns/DNS_fwd.db')
    remove_local_file('fwd.db')

    fabric_send_file('rev.db', DNS_DATA_DIR + 'namedb/rev.db')
    copy_configuration_file('rev.db', 'dns/DNS_rev.db')
    remove_local_file('rev.db')


def stop_srv(value = False):
    fabric_sudo_command('(killall named & ); sleep ' + str(SLEEP_TIME_1), value)


def restart_srv():
    stop_srv()
    start_srv(True, None)


def start_srv(success, process):
    fabric_sudo_command('(' + DNS_SERVER_INSTALL_DIR + 'named -c ' +
                        DNS_DATA_DIR + 'named.conf & ); sleep ' + str(SLEEP_TIME_1))


def save_leases():
    pass


def save_logs():
    fabric_download_file('/tmp/dns.log', world.cfg["dir_name"] + '/dns/dns_log_file')


def clear_all():
    fabric_remove_file_command('/tmp/dns.log')
