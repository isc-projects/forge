# Copyright (C) 2025-2026 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Classes and functions that help with setting up database servers."""

import os

import pytest

from src.forge_cfg import world
from src.softwaresupport.multi_server_functions import (
    add_line_if_not_exists,
    fabric_is_command,
    fabric_sudo_command,
    write_to_file,
)


def clear_database(host=world.f_cfg.mgmt_address):
    """Clear database configuration files.

    :param host: the host of the database server
    :type host: str
    """
    my_cnf_d = mysql_cnf_d(host=host)
    fabric_sudo_command(f'rm -f {my_cnf_d}/forge-tls.cnf', destination_host=host)
    pgsql_conf_d = postgresql_conf_d(host=host)
    fabric_sudo_command(f'rm -f {pgsql_conf_d}/forge-tls.conf', destination_host=host)


def configure_tls_on_the_database_server(backend, certificates, host=world.f_cfg.mgmt_address):
    """Configure TLS on the database server.

    :param backend:
    :type backend: str
    :param certificates: certificate object
    :type certificates: Certificates
    :param host: the host of the database server
    :type host: str
    """
    certificates.change_access([certificates.client_key, certificates.ca_key, certificates.server_key], '600')
    if backend == 'mysql':
        fabric_sudo_command('rm -fr /etc/mysql/tls', destination_host=host)
        certs = certificates.copy('/etc/mysql/tls')  # TODO host
        fabric_sudo_command('chown -R mysql:mysql /etc/mysql/tls', destination_host=host)
        my_cnf_d = mysql_cnf_d(host=host)
        content = f"""\
[mysqld]
require_secure_transport = ON
ssl_ca = {certs['ca_cert']}
ssl_cert = {certs['server_cert']}
ssl_key = {certs['server_key']}

[client-mariadb]
ssl_ca = {certs['ca_cert']}
ssl_cert = {certs['client_cert']}
ssl_key = {certs['client_key']}
"""
        write_to_file(os.path.join(my_cnf_d, 'forge-tls.cnf'), content, host=host)

    elif backend == 'postgresql':
        conf = postgresql_conf(host=host)
        pgsql_conf_d = postgresql_conf_d(host=host)
        add_line_if_not_exists(conf, "include_dir = 'conf.d'", host=host)
        fabric_sudo_command(f'mkdir -p {pgsql_conf_d}', destination_host=host)
        fabric_sudo_command('mkdir -p /var/lib/postgres/tls', destination_host=host)
        for file in [certificates.ca_cert, certificates.server_cert, certificates.server_key]:
            basename = os.path.basename(file)
            fabric_sudo_command(f'cp "{file}" /var/lib/postgres/tls/{basename}', destination_host=host)
            fabric_sudo_command(f'chmod 600 /var/lib/postgres/tls/{basename}', destination_host=host)
        fabric_sudo_command('chown -R postgres:postgres /var/lib/postgres/tls', destination_host=host)
        content = """\
ssl = on
ssl_ca_file = '/var/lib/postgres/tls/ca_cert.pem'
ssl_cert_file = '/var/lib/postgres/tls/server_cert.pem'
ssl_key_file = '/var/lib/postgres/tls/server_key.pem'
"""
        write_to_file(f'{pgsql_conf_d}/forge-tls.conf', content, host=host)
        fabric_sudo_command(f'chown -R postgres:postgres {conf} {pgsql_conf_d}')
        fabric_sudo_command(f'chmod 600 {conf} {pgsql_conf_d}/forge-tls.conf')
        fabric_sudo_command(f'chmod 700 {pgsql_conf_d}')
        # If SELinux is enabled, restore PostgreSQL file types.
        if fabric_is_command('restorecon'):
            fabric_sudo_command(f'restorecon -Rv {pgsql_conf_d}')

    else:
        pytest.fail(f'backend {backend}?')

    restart_database(backend, host=host)


def mysql_cnf_d(host=world.f_cfg.mgmt_address):
    """Get the directory which holds global custom configuration files for MySQL.

    :param host: the host of the database server
    :type host: str
    :return: the path to the global cnf.d directory
    :rtype: str
    """
    mysql_help = fabric_sudo_command('mysql --help --verbose', hide_all=True, destination_host=host)
    lines = iter(mysql_help.splitlines())
    my_cnf = None
    for line in lines:
        if line == 'Default options are read from the following files in the given order:':
            my_cnf = next(lines).split(' ')[0]
    assert my_cnf is not None
    my_cnf_d = f"{my_cnf}.d"
    fabric_sudo_command(f'mkdir -p {my_cnf_d}', destination_host=host)
    return my_cnf_d


def postgresql_conf(host=world.f_cfg.mgmt_address):
    """Get the path to PostgreSQL's configuration file.

    :param host: the host of the database server
    :type host: str
    :return: the path to postgresql.conf
    :rtype: str
    """
    return fabric_sudo_command("cd /tmp; sudo -u postgres psql -A -t -c 'SHOW config_file;'", destination_host=host)


def postgresql_conf_d(host=world.f_cfg.mgmt_address):
    """Get the path to PostgreSQL's configuration include directory.

    :param host: the host of the database server
    :type host: str
    :return: the path to conf.d
    :rtype: str
    """
    conf = postgresql_conf(host=host)
    dirname = fabric_sudo_command(f"dirname '{conf}'", destination_host=host)
    conf_d = os.path.join(dirname, 'conf.d')
    return conf_d


def service_action_on_database(database, action, host=world.f_cfg.mgmt_address):
    """Service action on database.

    :param database:
    :type database: str
    :param action:
    :type action: str
    :param host: (Default value = world.f_cfg.mgmt_address)
    :type host: str
    """
    database = 'mariadb' if database == 'mysql' else database
    if world.server_system == 'alpine':
        cmd = f'rc-service {database} {action}'
    else:
        cmd = f'systemctl {action} {database}'
    fabric_sudo_command(cmd, destination_host=host)


def restart_database(database, host=world.f_cfg.mgmt_address):
    """Restart database.

    :param database:
    :type database: str
    :param host: (Default value = world.f_cfg.mgmt_address)
    :type host: str
    """
    service_action_on_database(database, 'restart', host=host)


def restart_all_databases(host=world.f_cfg.mgmt_address):
    """Restart all databases.

    :param host: (Default value = world.f_cfg.mgmt_address)
    :type host: str
    """
    for database in ['mysql', 'postgresql']:
        restart_database(database, host=host)


def start_database(database, host=world.f_cfg.mgmt_address):
    """Start database.

    :param database:
    :type database: str
    :param host: (Default value = world.f_cfg.mgmt_address)
    :type host: str
    """
    service_action_on_database(database, 'start', host=host)


def start_all_databases(host=world.f_cfg.mgmt_address):
    """Start all databases.

    :param host: (Default value = world.f_cfg.mgmt_address)
    :type host: str
    """
    for database in ['mysql', 'postgresql']:
        start_database(database, host=host)


def stop_database(database, host=world.f_cfg.mgmt_address):
    """Stop database.

    :param database:
    :type database: str
    :param host: (Default value = world.f_cfg.mgmt_address)
    :type host: str
    """
    service_action_on_database(database, 'stop', host=host)


def stop_all_databases(host=world.f_cfg.mgmt_address):
    """Stop all databases.

    :param host: (Default value = world.f_cfg.mgmt_address)
    :type host: str
    """
    for database in ['mysql', 'postgresql']:
        stop_database(database, host=host)
