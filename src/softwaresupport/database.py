# Copyright (C) 2025 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Classes and functions that help with setting up database servers."""

import os

import pytest

from src import srv_msg

from src.forge_cfg import world
from src.softwaresupport.multi_server_functions import add_line_if_not_exists, fabric_sudo_command


def clear_database(destination_host=world.f_cfg.mgmt_address):
    """Clear database configuration files.

    :param destination_host: the host of the database server
    :type destination_host: str
    """
    my_cnf_d = mysql_cnf_d()
    fabric_sudo_command(f'rm -f {my_cnf_d}/forge-ssl.cnf', destination_host=destination_host)
    fabric_sudo_command('rm -f /var/lib/postgres/data/conf.d/forge-ssl.conf', destination_host=destination_host)


def configure_tls_on_the_database_server(backend, certificates):
    """Configure TLS on the database server.

    :param backend:
    :type backend: str
    :param certificates: certificate object
    :type certificates: Certificates
    """
    if backend == 'mysql':
        fabric_sudo_command('rm -fr /etc/mysql/tls')
        certs = certificates.copy('/etc/mysql/tls')
        fabric_sudo_command('chown -R mysql:mysql /etc/mysql/tls')
        my_cnf_d = mysql_cnf_d()
        with open(os.path.join(my_cnf_d, 'forge-ssl.cnf'), 'w', encoding='utf-8') as file:
            file.write(f"""\
[mysqld]
require_secure_transport = ON
ssl_ca = {certs['ca_cert']}
ssl_cert = {certs['server_cert']}
ssl_key = {certs['server_key']}

[client-mariadb]
ssl_ca = {certs['ca_cert']}
ssl_cert = {certs['client_cert']}
ssl_key = {certs['client_key']}
""")

    elif backend == 'postgresql':
        conf = postgresql_conf()
        add_line_if_not_exists(conf, "include_dir = 'conf.d'")
        fabric_sudo_command('mkdir -p /var/lib/postgres/data/conf.d')
        fabric_sudo_command('mkdir -p /var/lib/postgres/ssl')
        for file in [certificates.ca_cert, certificates.server_cert, certificates.server_key]:
            basename = os.path.basename(file)
            fabric_sudo_command(f'cp "{file}" /var/lib/postgres/ssl/{basename}')
            fabric_sudo_command(f'chmod 600 /var/lib/postgres/ssl/{basename}')
        fabric_sudo_command('chown -R postgres:postgres /var/lib/postgres/ssl')
        with open('/var/lib/postgres/data/conf.d/forge-ssl.conf', 'w', encoding='utf-8') as file:
            file.write("""\
ssl = on
ssl_ca_file = '/var/lib/postgres/ssl/ca_cert.pem'
ssl_cert_file = '/var/lib/postgres/ssl/server_cert.pem'
ssl_key_file = '/var/lib/postgres/ssl/server_key.pem'
""")

    else:
        pytest.fail(f'backend {backend}?')

    restart_database(backend)


def mysql_cnf_d():
    """Get the directory which holds global custom configuration files for MySQL.

    :return: the path to the global cnf.d directory
    :rtype: str
    """
    mysql_help = fabric_sudo_command('mysql --help --verbose', hide_all=True)
    lines = iter(mysql_help.splitlines())
    my_cnf = None
    for line in lines:
        if line == 'Default options are read from the following files in the given order:':
            my_cnf = next(lines).split(' ')[0]
    assert my_cnf is not None
    my_cnf_d = f"{my_cnf}.d"
    os.makedirs(my_cnf_d, exist_ok=True)
    return my_cnf_d


def postgresql_conf():
    """Get the path to PostgreSQL's configuration file.

    :return: the path to postgresql.conf
    :rtype: str
    """
    return fabric_sudo_command("sudo -u postgres psql -A -t -c 'SHOW config_file;'")


def service_action_on_database(database, action, destination_address=world.f_cfg.mgmt_address):
    """Service action on database.

    :param database:
    :type database: str
    :param action:
    :type action: str
    :param destination_address: (Default value = world.f_cfg.mgmt_address)
    :type destination_address: str
    """
    database = 'mariadb' if database == 'mysql' else database
    if world.server_system == 'alpine':
        cmd = f'sudo rc-service {database} {action}'
    else:
        cmd = f'sudo systemctl {action} {database}'
    srv_msg.execute_shell_cmd(cmd, dest=destination_address, save_results=False)


def restart_database(database, destination_address=world.f_cfg.mgmt_address):
    """Restart database.

    :param database:
    :type database: str
    :param destination_address: (Default value = world.f_cfg.mgmt_address)
    :type destination_address: str
    """
    service_action_on_database(database, 'restart',  destination_address)


def restart_databases(destination_address=world.f_cfg.mgmt_address):
    """Restart all databases.

    :param destination_address: (Default value = world.f_cfg.mgmt_address)
    :type destination_address: str
    """
    for database in ['mysql', 'postgresql']:
        restart_database(database, destination_address)


def start_database(database, destination_address=world.f_cfg.mgmt_address):
    """Start database.

    :param database:
    :type database: str
    :param destination_address: (Default value = world.f_cfg.mgmt_address)
    :type destination_address: str
    """
    service_action_on_database(database, 'start',  destination_address)


def start_databases(destination_address=world.f_cfg.mgmt_address):
    """Start all databases.

    :param destination_address: (Default value = world.f_cfg.mgmt_address)
    :type destination_address: str
    """
    for database in ['mysql', 'postgresql']:
        start_database(database, destination_address)


def stop_database(database, destination_address=world.f_cfg.mgmt_address):
    """Stop database.

    :param database:
    :type database: str
    :param destination_address: (Default value = world.f_cfg.mgmt_address)
    :type destination_address: str
    """
    service_action_on_database(database, 'stop',  destination_address)


def stop_databases(destination_address=world.f_cfg.mgmt_address):
    """Stop all databases.

    :param destination_address: (Default value = world.f_cfg.mgmt_address)
    :type destination_address: str
    """
    for database in ['mysql', 'postgresql']:
        stop_database(database, destination_address)
