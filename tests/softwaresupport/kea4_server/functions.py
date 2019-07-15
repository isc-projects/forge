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

import logging

from forge_cfg import world

from softwaresupport.multi_server_functions import fabric_run_command, fabric_sudo_command, locate_entry

from softwaresupport.kea import build_and_send_config_files
from softwaresupport.kea import clear_all, clear_logs, clear_leases, start_srv
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


def config_client_classification(subnet, option_value):
    subnet = int(subnet)
    if len(world.subcfg[subnet][1]) > 2:
        world.subcfg[subnet][1] += ', '
    world.subcfg[subnet][1] += '"client-class": "{option_value}"\n'.format(**locals())


def add_siaddr(addr, subnet_number):
    if subnet_number is None:
        if "simple_options" not in world.cfg:
            world.cfg["simple_options"] = ''
        else:
            world.cfg["simple_options"] += ','
        world.cfg["simple_options"] += '"next-server": "{addr}"'.format(**locals())
    else:
        subnet = int(subnet_number)
        if len(world.subcfg[subnet][1]) > 2:
            world.subcfg[subnet][1] += ', '
        world.subcfg[subnet][1] += '"next-server": "{addr}"\n'.format(**locals())


def disable_client_echo():
    # after using it, we should revert that at the end!
    # keep that in mind when first time using it.
    if "simple_options" not in world.cfg:
        world.cfg["simple_options"] = ''
    else:
        world.cfg["simple_options"] += ','
    world.cfg["simple_options"] += '"echo-client-id": "False"'


def host_reservation(reservation_type, reserved_value, unique_host_value_type, unique_host_value, subnet):
    if len(world.subcfg[subnet][5]) > 20:
        world.subcfg[subnet][5] += ','

    world.subcfg[subnet][5] += "{"
    if reservation_type == "address":
        world.subcfg[subnet][5] += '"{unique_host_value_type}":"{unique_host_value}","ip-address":"{reserved_value}"'.format(**locals())
    elif reservation_type == "hostname":
        world.subcfg[subnet][5] += '"{unique_host_value_type}":"{unique_host_value}","hostname":"{reserved_value}"'.format(**locals())
    else:
        assert False, "Not supported yet."
        # if reservation will allow on another value - add it here

    world.subcfg[subnet][5] += "}"


def host_reservation_extension(reservation_number, subnet, reservation_type, reserved_value):
    pointer = locate_entry(world.subcfg[subnet][5], '}', reservation_number)
    if reservation_type == "address":
        tmp = world.subcfg[subnet][5][:pointer] + ',"ip-address":"{reserved_value}"'.format(**locals())
        tmp += world.subcfg[subnet][5][pointer:]
    elif reservation_type == "hostname":
        tmp = world.subcfg[subnet][5][:pointer] + ',"hostname":"{reserved_value}"'.format(**locals())
        tmp += world.subcfg[subnet][5][pointer:]
    else:
        assert False, "Not supported"
        # if reservation will allow on another value - add it here

    world.subcfg[subnet][5] = tmp


def config_srv_id(id_type, id_value):
    assert False, "Not yet available for Kea4"


def add_option_to_defined_class(class_no, option_name, option_value):
    space = world.cfg["space"]
    option_code = world.kea_options4.get(option_name)
    # if option_code is None:
    #     option_code = kea_otheroptions.get(option_name)

    pointer_start = "{"
    pointer_end = "}"

    assert option_code is not None, "Unsupported option name for other Kea4 options: " + option_name
    if len(world.classification[class_no-1][2]) > 10:
        world.classification[class_no-1][2] += ','

    world.classification[class_no-1][2] += '''
            {pointer_start}"csv-format": true, "code": {option_code}, "data": "{option_value}",
            "name": "{option_name}", "space": "{space}"{pointer_end}'''.format(**locals())

# =============================================================
# ================ PREPARE CONFIG BLOCK END  ==================

# =============================================================
# ================ REMOTE SERVER BLOCK START ==================


def prepare_cfg_prefix(prefix, length, delegated_length, subnet):
    assert False, "This function can be used only with DHCPv6"


def db_setup():
    if world.f_cfg.disable_db_setup:
        return

    db_name = world.f_cfg.db_name
    db_user = world.f_cfg.db_user
    db_passwd = world.f_cfg.db_passwd

    # MYSQL
    # cmd = "mysql -u root -N -B -e \"DROP DATABASE IF EXISTS '{db_name}';\"".format(**locals())
    # result = fabric_sudo_command(cmd)
    cmd = "mysql -u root -N -B -e \"SHOW DATABASES LIKE '{db_name}';\"".format(**locals())
    result = fabric_sudo_command(cmd)
    if result == db_name:
        # db exsists, so try migration
        cmd = "kea-admin db-upgrade mysql -u {db_user} -p {db_passwd} -n {db_name}".format(**locals())
        fabric_run_command(cmd)
    else:
        # no db, create from scratch
        cmd = "mysql -u root -e 'CREATE DATABASE {db_name};'".format(**locals())
        fabric_sudo_command(cmd)
        cmd = "mysql -u root -e \"CREATE USER IF NOT EXISTS '{db_user}'@'localhost' IDENTIFIED BY '{db_passwd}';\"".format(**locals())
        fabric_sudo_command(cmd)
        cmd = "mysql -u root -e 'GRANT ALL ON {db_name}.* TO {db_user}@localhost;'".format(**locals())
        fabric_sudo_command(cmd)
        cmd = "kea-admin db-init mysql -u {db_user} -p {db_passwd} -n {db_name}".format(**locals())
        fabric_run_command(cmd)

    # POSTGRESQL
    # cmd = "psql -U postgres -t -c \"DROP DATABASE IF EXISTS {db_name}\"".format(**locals())
    # result = fabric_sudo_command(cmd, sudo_user='postgres')
    cmd = "psql -U postgres -t -c \"SELECT datname FROM pg_database WHERE datname = '{db_name}'\"".format(**locals())
    result = fabric_sudo_command(cmd, sudo_user='postgres')
    if result.strip() == db_name:
        # db exsists, so try migration
        cmd = "kea-admin db-upgrade pgsql -u {db_user} -p {db_passwd} -n {db_name}".format(**locals())
        fabric_run_command(cmd)
    else:
        # no db, create from scratch
        cmd = "psql -U postgres -c \"CREATE DATABASE {db_name};\"".format(**locals())
        fabric_sudo_command(cmd, sudo_user='postgres')
        cmd = "psql -U postgres -c \"DROP USER IF EXISTS {db_user};\"".format(**locals())
        fabric_sudo_command(cmd, sudo_user='postgres')
        cmd = "psql -U postgres -c \"CREATE USER {db_user} WITH PASSWORD '{db_passwd}';\"".format(**locals())
        fabric_sudo_command(cmd, sudo_user='postgres')
        cmd = "psql -U postgres -c \"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};\"".format(**locals())
        fabric_sudo_command(cmd, sudo_user='postgres')
        cmd = "kea-admin db-init pgsql -u {db_user} -p {db_passwd} -n {db_name}".format(**locals())
        fabric_run_command(cmd)
