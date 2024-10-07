# Copyright (C) 2024 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Marcin Godzina

"""Test database connection features"""

import pytest

from src import srv_control
from src import misc
from src import srv_msg
from src.forge_cfg import world
from src.protosupport.multi_protocol_functions import log_contains_n_times, log_doesnt_contain, \
    wait_for_message_in_log


def _start_database(database, destination_address=world.f_cfg.mgmt_address):
    database = database.lower()
    if world.server_system == 'alpine':
        # We use mariadb on Alpine instead of mysql
        database = 'mariadb' if database == 'mysql' else database
        cmd = f'sudo rc-service {database} start'
    else:
        cmd = f'sudo systemctl start {database}'
    srv_msg.execute_shell_cmd(
        cmd, dest=destination_address, save_results=False)


def _stop_database(database, destination_address=world.f_cfg.mgmt_address):
    database = database.lower()
    if world.server_system == 'alpine':
        # We use mariadb on Alpine instead of mysql
        database = 'mariadb' if database == 'mysql' else database
        cmd = f'sudo rc-service {database} stop'
    else:
        cmd = f'sudo systemctl stop {database}'
    srv_msg.execute_shell_cmd(
        cmd, dest=destination_address, save_results=False)


def _confirm_no_dhcp_service(dhcp_version):
    if dhcp_version == 'v4':
        srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
        srv_msg.client_send_msg('DISCOVER')
        srv_msg.send_dont_wait_for_message()
    else:
        srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_does_include('Client', 'IA-NA')
        srv_msg.client_send_msg('SOLICIT')
        srv_msg.send_dont_wait_for_message()


@pytest.fixture()
def _restart_databases(backend):
    """Restart database even if test fails.
    """
    yield
    _start_database(backend, destination_address=world.f_cfg.mgmt_address)


@pytest.mark.usefixtures('_restart_databases')
@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_db_retry_lease_stop_retry_exit(backend, dhcp_version):
    """Test starts Kea without lease DB connection and checks it's behavior according to `on-fail`.
    stop-retry-exit - Kea should stop and not serve any clients after not being able to connect to DB.
    After exhausting retries Kea should shutdown.
    Testing steps:
    Forge starts Kea, confirms it is waiting for DB connection and not serving any Clients
    (both Discover and other messages).
    Then Kea is restarted and DB is reconnected after Kea starts to check if service is restored.
    Leases db is checked to confirm Kea is using it.
    """
    retries = 5
    wait_time = 2000
    misc.test_setup()
    # Stop database engine so Kea does not have anything to connect to.
    _stop_database(backend)
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    world.dhcp_cfg["lease-database"] = {"type": backend,
                                        "name": world.f_cfg.db_name,
                                        "host": world.f_cfg.db_host,
                                        "user": world.f_cfg.db_user,
                                        "password": world.f_cfg.db_passwd,
                                        "retry-on-startup": True,
                                        "max-reconnect-tries": retries,
                                        "reconnect-wait-time": wait_time,
                                        "on-fail": "stop-retry-exit"}
    srv_control.add_database_hook(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()

    # Start Kea
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    misc.test_procedure()

    # Confirm Kea is waiting for DB
    # Kea#3223 - It is not decided yet how Kea should report to status-get when there is no DB connection,
    # so we use version-get.
    cmd = {"command": "version-get", "arguments": {}}
    srv_msg.send_ctrl_cmd(cmd, 'http')
    log_contains_n_times('DHCPSRV_LEASE_MGR_DB_OPEN_CONNECTION_WITH_RETRY_FAILED Failed to connect to database:', 1)
    log_doesnt_contain(f'DHCP{dhcp_version[1]}_SHUTDOWN server shutdown')

    # Confirm Kea is NOT serving Clients non lease messages
    if dhcp_version == 'v4':
        srv_msg.client_requests_option(1)
        srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.1')
        srv_msg.client_send_msg('INFORM')
        srv_msg.send_wait_for_message('MUST', 'ACK', expect_response=False)
    else:
        srv_msg.client_requests_option(7)
        srv_msg.client_send_msg('INFOREQUEST')
        srv_msg.send_wait_for_message('MUST', 'REPLY', expect_response=False)

    # Confirm Kea is NOT serving Clients
    _confirm_no_dhcp_service(dhcp_version)

    # Wait for kea shutdown after exhausting retries
    wait_for_message_in_log(f'DHCP{dhcp_version[1]}_SHUTDOWN server shutdown', count=1,
                            timeout=retries*wait_time/1000+1)

    # Confirm Kea is done waiting before shutdown
    cmd = {"command": "version-get", "arguments": {}}
    srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=1)
    log_contains_n_times(
        f'DHCP{dhcp_version[1]}_DB_RECONNECT_FAILED maximum number of database reconnect attempts: '
        f'{retries}, has been exhausted without success', 1)

    # Start Kea again (logs are cleared)
    srv_control.clear_some_data('logs')
    srv_control.start_srv('DHCP', 'restarted')

    # Confirm Kea is waiting for DB
    # Kea#3223 - It is not decided yet how Kea should report to status-get when there is no DB connection,
    # so we use version-get.
    cmd = {"command": "version-get", "arguments": {}}
    srv_msg.send_ctrl_cmd(cmd, 'http')
    log_contains_n_times('DHCPSRV_LEASE_MGR_DB_OPEN_CONNECTION_WITH_RETRY_FAILED Failed to connect to database:', 1)
    log_doesnt_contain(f'DHCP{dhcp_version[1]}_SHUTDOWN server shutdown')

    # Start DB
    _start_database(backend)

    # Wait for Kea to recover connection to DB
    wait_for_message_in_log(
        f'DHCP{dhcp_version[1]}_DB_RECONNECT_SUCCEEDED database connection recovered.', count=1,
        timeout=retries*wait_time/1000+1)

    # Confirm Kea is started and connected to DB
    if dhcp_version == 'v4':
        srv_msg.DORA('192.168.50.1')
        srv_msg.check_leases({'address': '192.168.50.1'}, backend)
    else:
        srv_msg.SARR('2001:db8:1::50')
        srv_msg.check_leases({'address': '2001:db8:1::50'}, backend)


@pytest.mark.disabled  # This on-fail setting with lease db is strongly discouraged in Kea ARM
@pytest.mark.usefixtures('_restart_databases')
@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_db_retry_lease_serve_retry_exit(backend, dhcp_version):
    """Test starts Kea without lease DB connection and checks it's behavior according to `on-fail`.
    It is highly recommended not to use this on fail setting for the lease manager by Kea ARM.
    serve-retry-exit - Kea should still serve clients traffic other than lease related after
    not being able to connect to DB.
    After exhausting retries Kea should shutdown.
    Testing steps:
    Forge starts Kea, confirms it is waiting for DB connection and not serving any Clients lease related traffic.
    Other traffic should be served. After exhausting retries Kea should shutdown.
    Then Kea is restarted and DB is reconnected after Kea starts to check if service is restored.
    Leases db is checked to confirm Kea is using it.
    """
    retries = 5
    wait_time = 2000
    misc.test_setup()
    # Stop database engine so Kea does not have anything to connect to.
    _stop_database(backend)
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
        srv_control.config_srv_opt('subnet-mask', '255.255.255.0')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
        srv_control.config_srv_opt('preference', '123')
    world.dhcp_cfg["lease-database"] = {"type": backend,
                                        "name": world.f_cfg.db_name,
                                        "host": world.f_cfg.db_host,
                                        "user": world.f_cfg.db_user,
                                        "password": world.f_cfg.db_passwd,
                                        "retry-on-startup": True,
                                        "max-reconnect-tries": retries,
                                        "reconnect-wait-time": wait_time,
                                        "on-fail": "serve-retry-exit"}
    srv_control.add_database_hook(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()

    # Start Kea
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    misc.test_procedure()

    # Confirm Kea is waiting for DB
    # Kea#3223 - It is not decided yet how Kea should report to status-get when there is no DB connection,
    # so we use version-get.
    cmd = {"command": "version-get", "arguments": {}}
    srv_msg.send_ctrl_cmd(cmd, 'http')
    log_contains_n_times('DHCPSRV_LEASE_MGR_DB_OPEN_CONNECTION_WITH_RETRY_FAILED Failed to connect to database:', 1)
    log_doesnt_contain(f'DHCP{dhcp_version[1]}_SHUTDOWN server shutdown')

    # Confirm Kea is serving Clients non lease messages
    if dhcp_version == 'v4':
        srv_msg.client_requests_option(1)
        srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.1')
        srv_msg.client_send_msg('INFORM')
        srv_msg.send_wait_for_message('MUST', 'ACK')
        srv_msg.response_check_include_option(1)
        srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    else:
        srv_msg.client_requests_option(7)
        srv_msg.client_send_msg('INFOREQUEST')
        srv_msg.send_wait_for_message('MUST', 'REPLY')
        srv_msg.response_check_include_option(7)
        srv_msg.response_check_option_content(7, 'value', 123)

    # Wait for kea shutdown after exhausting retries
    wait_for_message_in_log(f'DHCP{dhcp_version[1]}_SHUTDOWN server shutdown', count=1,
                            timeout=retries*wait_time/1000+1)

    # Confirm Kea is done waiting before shutdown
    cmd = {"command": "version-get", "arguments": {}}
    srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=1)
    log_contains_n_times(
        f'DHCP{dhcp_version[1]}_DB_RECONNECT_FAILED maximum number of database reconnect attempts: '
        f'{retries}, has been exhausted without success', 1)

    # Start Kea again (logs are cleared)
    srv_control.clear_some_data('logs')
    srv_control.start_srv('DHCP', 'restarted')

    # Confirm Kea is waiting for DB
    # Kea#3223 - It is not decided yet how Kea should report to status-get when there is no DB connection,
    # so we use version-get.
    cmd = {"command": "version-get", "arguments": {}}
    srv_msg.send_ctrl_cmd(cmd, 'http')
    log_contains_n_times('DHCPSRV_LEASE_MGR_DB_OPEN_CONNECTION_WITH_RETRY_FAILED Failed to connect to database:', 1)
    log_doesnt_contain(f'DHCP{dhcp_version[1]}_SHUTDOWN server shutdown')

    # Start DB
    _start_database(backend)

    # Wait for Kea to recover connection to DB
    wait_for_message_in_log(
        f'DHCP{dhcp_version[1]}_DB_RECONNECT_SUCCEEDED database connection recovered.', count=1,
        timeout=retries*wait_time/1000+1)

    # Confirm Kea is started and connected to DB
    if dhcp_version == 'v4':
        srv_msg.DORA('192.168.50.1')
        srv_msg.check_leases({'address': '192.168.50.1'}, backend)
    else:
        srv_msg.SARR('2001:db8:1::50')
        srv_msg.check_leases({'address': '2001:db8:1::50'}, backend)


@pytest.mark.disabled  # This on-fail setting with lease db is strongly discouraged in Kea ARM
@pytest.mark.usefixtures('_restart_databases')
@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_db_retry_lease_serve_retry_continue(backend, dhcp_version):
    """Test starts Kea without lease DB connection and checks it's behavior according to `on-fail`.
    It is highly recommended not to use this on fail setting for the lease manager by Kea ARM.
    serve-retry-continue - Kea should still serve clients traffic other than lease related after
    not being able to connect to DB.
    After exhausting retries Kea should continue to serve clients non lease related traffic.
    Testing steps:
    Forge starts Kea, confirms it is waiting for DB connection and not serving any Clients lease related traffic.
    Other traffic should be served.
    Then Kea is restarted and DB is reconnected after Kea starts to check if service is restored.
    Leases db is checked to confirm Kea is using it.
    """
    retries = 5
    wait_time = 2000
    misc.test_setup()
    # Stop database engine so Kea does not have anything to connect to.
    _stop_database(backend)
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
        srv_control.config_srv_opt('subnet-mask', '255.255.255.0')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
        srv_control.config_srv_opt('preference', '123')
    world.dhcp_cfg["lease-database"] = {"type": backend,
                                        "name": world.f_cfg.db_name,
                                        "host": world.f_cfg.db_host,
                                        "user": world.f_cfg.db_user,
                                        "password": world.f_cfg.db_passwd,
                                        "retry-on-startup": True,
                                        "max-reconnect-tries": retries,
                                        "reconnect-wait-time": wait_time,
                                        "on-fail": "serve-retry-continue"}
    srv_control.add_database_hook(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()

    # Start Kea
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    misc.test_procedure()

    # Confirm Kea is waiting for DB
    # Kea#3223 - It is not decided yet how Kea should report to status-get when there is no DB connection,
    # so we use version-get.
    cmd = {"command": "version-get", "arguments": {}}
    srv_msg.send_ctrl_cmd(cmd, 'http')
    log_contains_n_times('DHCPSRV_LEASE_MGR_DB_OPEN_CONNECTION_WITH_RETRY_FAILED Failed to connect to database:', 1)
    log_doesnt_contain(f'DHCP{dhcp_version[1]}_SHUTDOWN server shutdown')

    # Confirm Kea is serving Clients non lease messages
    if dhcp_version == 'v4':
        srv_msg.client_requests_option(1)
        srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.1')
        srv_msg.client_send_msg('INFORM')
        srv_msg.send_wait_for_message('MUST', 'ACK')
        srv_msg.response_check_include_option(1)
        srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    else:
        srv_msg.client_requests_option(7)
        srv_msg.client_send_msg('INFOREQUEST')
        srv_msg.send_wait_for_message('MUST', 'REPLY')
        srv_msg.response_check_include_option(7)
        srv_msg.response_check_option_content(7, 'value', 123)

    # Wait for Kea to be done waiting
    wait_for_message_in_log(f'DHCP{dhcp_version[1]}_DB_RECONNECT_FAILED maximum number of database reconnect attempts: '
                            f'{retries}, has been exhausted without success', count=1,
                            timeout=retries*wait_time/1000+1)

    # Confirm Kea is still serving Clients non lease messages
    if dhcp_version == 'v4':
        srv_msg.client_requests_option(1)
        srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.1')
        srv_msg.client_send_msg('INFORM')
        srv_msg.send_wait_for_message('MUST', 'ACK')
        srv_msg.response_check_include_option(1)
        srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    else:
        srv_msg.client_requests_option(7)
        srv_msg.client_send_msg('INFOREQUEST')
        srv_msg.send_wait_for_message('MUST', 'REPLY')
        srv_msg.response_check_include_option(7)
        srv_msg.response_check_option_content(7, 'value', 123)

    # Start Kea again (logs are cleared)
    srv_control.start_srv('DHCP', 'stopped')
    srv_control.clear_some_data('logs')
    srv_control.start_srv('DHCP', 'started')

    # Confirm Kea is waiting for DB
    # Kea#3223 - It is not decided yet how Kea should report to status-get when there is no DB connection,
    # so we use version-get.
    cmd = {"command": "version-get", "arguments": {}}
    srv_msg.send_ctrl_cmd(cmd, 'http')
    log_contains_n_times('DHCPSRV_LEASE_MGR_DB_OPEN_CONNECTION_WITH_RETRY_FAILED Failed to connect to database:', 1)
    log_doesnt_contain(f'DHCP{dhcp_version[1]}_SHUTDOWN server shutdown')

    # Start DB
    _start_database(backend)

    # Wait for Kea to recover connection to DB
    wait_for_message_in_log(
        f'DHCP{dhcp_version[1]}_DB_RECONNECT_SUCCEEDED database connection recovered.', count=1,
        timeout=retries*wait_time/1000+1)

    # Confirm Kea is started and connected to DB
    if dhcp_version == 'v4':
        srv_msg.DORA('192.168.50.1')
        srv_msg.check_leases({'address': '192.168.50.1'}, backend)
    else:
        srv_msg.SARR('2001:db8:1::50')
        srv_msg.check_leases({'address': '2001:db8:1::50'}, backend)


@pytest.mark.usefixtures('_restart_databases')
@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_db_retry_reservation_stop_retry_exit(backend, dhcp_version):
    """Test starts Kea without reservation DB connection and checks it's behavior according to `on-fail`.
    stop-retry-exit - Kea should stop and not serve any clients after not being able to connect to DB.
    After exhausting retries Kea should shutdown.
    Testing steps:
    Forge starts Kea, confirms it is waiting for DB connection and not serving any Clients.
    After exhausting retries Kea should shutdown.
    Then Kea is restarted and DB is reconnected after Kea starts to check if service is restored.
    DHCP traffic is send to confirm Kea is using reservations.
    """
    retries = 5
    wait_time = 2000
    misc.test_setup()
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
        srv_control.new_db_backend_reservation(backend, 'hw-address', 'ff:01:02:03:ff:04')
        srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, backend, 1)
        srv_control.update_db_backend_reservation("ipv4_address", "192.168.50.100", backend, 1)
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
        srv_control.new_db_backend_reservation(backend, 'hw-address', 'f6:f5:f4:f3:f2:01')
        srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, backend, 1)
        srv_control.ipv6_address_db_backend_reservation('2001:db8:1::100', '$(EMPTY)', backend, 1)
    srv_control.upload_db_reservation(backend)

    world.reservation_backend = None  # Allow to override hosts-database settings
    world.dhcp_cfg["hosts-database"] = {"type": backend,
                                        "name": world.f_cfg.db_name,
                                        "host": world.f_cfg.db_host,
                                        "user": world.f_cfg.db_user,
                                        "password": world.f_cfg.db_passwd,
                                        "retry-on-startup": True,
                                        "max-reconnect-tries": retries,
                                        "reconnect-wait-time": wait_time,
                                        "on-fail": "stop-retry-exit"}
    srv_control.add_database_hook(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()

    # Stop database engine so Kea does not have anything to connect to.
    _stop_database(backend)
    # Start Kea
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    misc.test_procedure()

    # Confirm Kea is waiting for DB
    # Kea#3223 - It is not decided yet how Kea should report to status-get when there is no DB connection,
    # so we use version-get.
    cmd = {"command": "version-get", "arguments": {}}
    srv_msg.send_ctrl_cmd(cmd, 'http')
    log_contains_n_times('DHCPSRV_HOST_MGR_DB_OPEN_CONNECTION_WITH_RETRY_FAILED Failed to connect to database:', 1)
    log_doesnt_contain(f'DHCP{dhcp_version[1]}_SHUTDOWN server shutdown')

    # Confirm Kea is not serving Clients
    _confirm_no_dhcp_service(dhcp_version)

    # Wait for kea shutdown
    wait_for_message_in_log(f'DHCP{dhcp_version[1]}_SHUTDOWN server shutdown', count=1,
                            timeout=retries*wait_time/1000+1)

    # Confirm Kea is done waiting before shutdown
    cmd = {"command": "version-get", "arguments": {}}
    srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=1)
    log_contains_n_times(
        f'DHCP{dhcp_version[1]}_DB_RECONNECT_FAILED maximum number of database reconnect attempts: '
        f'{retries}, has been exhausted without success', 1)

    # Start Kea again (logs are cleared)
    srv_control.clear_some_data('logs')
    srv_control.start_srv('DHCP', 'restarted')

    # Confirm Kea is waiting for DB
    # Kea#3223 - It is not decided yet how Kea should report to status-get when there is no DB connection,
    # so we use version-get.
    cmd = {"command": "version-get", "arguments": {}}
    srv_msg.send_ctrl_cmd(cmd, 'http')
    log_contains_n_times('DHCPSRV_HOST_MGR_DB_OPEN_CONNECTION_WITH_RETRY_FAILED Failed to connect to database:', 1)
    log_doesnt_contain(f'DHCP{dhcp_version[1]}_SHUTDOWN server shutdown')

    # Start DB
    _start_database(backend)

    # Wait for Kea to recover connection to DB
    wait_for_message_in_log(
        f'DHCP{dhcp_version[1]}_DB_RECONNECT_SUCCEEDED database connection recovered.', count=1,
        timeout=retries*wait_time/1000+1)

    if dhcp_version == 'v4':
        srv_msg.DORA('192.168.50.100', chaddr='ff:01:02:03:ff:04')
    else:
        srv_msg.SARR('2001:db8:1::100', duid='00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')


@pytest.mark.usefixtures('_restart_databases')
@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_db_retry_reservation_serve_retry_exit(backend, dhcp_version):
    """Test starts Kea without reservation DB connection and checks it's behavior according to `on-fail`.
    serve-retry-exit - Kea should still serve clients after not being able to connect to DB.
    After exhausting retries Kea should shutdown.
    Forge starts Kea, confirms it is waiting for DB connection and serving any Clients.
    After exhausting retries Kea should shutdown.
    Then Kea is restarted and DB is reconnected after Kea starts to check if service is restored.
    DHCP traffic is send to confirm Kea is using reservations.
    """
    retries = 5
    wait_time = 2000
    misc.test_setup()
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
        srv_control.new_db_backend_reservation(backend, 'hw-address', 'ff:01:02:03:ff:04')
        srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, backend, 1)
        srv_control.update_db_backend_reservation("ipv4_address", "192.168.50.100", backend, 1)
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
        srv_control.new_db_backend_reservation(backend, 'hw-address', 'f6:f5:f4:f3:f2:01')
        srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, backend, 1)
        srv_control.ipv6_address_db_backend_reservation('2001:db8:1::100', '$(EMPTY)', backend, 1)
    srv_control.upload_db_reservation(backend)

    world.reservation_backend = None  # Allow to override hosts-database settings
    world.dhcp_cfg["hosts-database"] = {"type": backend,
                                        "name": world.f_cfg.db_name,
                                        "host": world.f_cfg.db_host,
                                        "user": world.f_cfg.db_user,
                                        "password": world.f_cfg.db_passwd,
                                        "retry-on-startup": True,
                                        "max-reconnect-tries": retries,
                                        "reconnect-wait-time": wait_time,
                                        "on-fail": "serve-retry-exit"}
    srv_control.add_database_hook(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()

    # Stop database engine so Kea does not have anything to connect to.
    _stop_database(backend)
    # Start Kea
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    misc.test_procedure()

    # Confirm Kea is waiting for DB
    # Kea#3223 - It is not decided yet how Kea should report to status-get when there is no DB connection,
    # so we use version-get.
    cmd = {"command": "version-get", "arguments": {}}
    srv_msg.send_ctrl_cmd(cmd, 'http')
    log_contains_n_times('DHCPSRV_HOST_MGR_DB_OPEN_CONNECTION_WITH_RETRY_FAILED Failed to connect to database:', 1)
    log_doesnt_contain(f'DHCP{dhcp_version[1]}_SHUTDOWN server shutdown')

    # Confirm Kea is serving Clients
    if dhcp_version == 'v4':
        srv_msg.DORA('192.168.50.1')
    else:
        srv_msg.SARR('2001:db8:1::50')

    # Wait for kea shutdown after exhausting retries
    wait_for_message_in_log(f'DHCP{dhcp_version[1]}_SHUTDOWN server shutdown', count=1,
                            timeout=retries*wait_time/1000+1)

    # Confirm Kea is done waiting before shutdown
    cmd = {"command": "version-get", "arguments": {}}
    srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=1)
    log_contains_n_times(
        f'DHCP{dhcp_version[1]}_DB_RECONNECT_FAILED maximum number of database reconnect attempts: '
        f'{retries}, has been exhausted without success', 1)

    # Start Kea again (logs are cleared)
    srv_control.clear_some_data('logs')
    srv_control.start_srv('DHCP', 'restarted')

    # Confirm Kea is waiting for DB
    # Kea#3223 - It is not decided yet how Kea should report to status-get when there is no DB connection,
    # so we use version-get.
    cmd = {"command": "version-get", "arguments": {}}
    srv_msg.send_ctrl_cmd(cmd, 'http')
    log_contains_n_times('DHCPSRV_HOST_MGR_DB_OPEN_CONNECTION_WITH_RETRY_FAILED Failed to connect to database:', 1)
    log_doesnt_contain(f'DHCP{dhcp_version[1]}_SHUTDOWN server shutdown')

    # Start DB
    _start_database(backend)

    # Wait for Kea to recover connection to DB
    wait_for_message_in_log(
        f'DHCP{dhcp_version[1]}_DB_RECONNECT_SUCCEEDED database connection recovered.', count=1,
        timeout=retries*wait_time/1000+1)

    if dhcp_version == 'v4':
        srv_msg.DORA('192.168.50.100', chaddr='ff:01:02:03:ff:04')
    else:
        srv_msg.SARR('2001:db8:1::100', duid='00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')


@pytest.mark.usefixtures('_restart_databases')
@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_db_retry_reservation_serve_retry_continue(backend, dhcp_version):
    """Test starts Kea without reservation DB connection and checks it's behavior according to `on-fail`.
    serve-retry-continue - Kea should still serve clients traffic after not being able to connect to DB.
    After exhausting retries Kea should continue to serve clients non lease related traffic
    Testing steps:
    Forge starts Kea, confirms it is waiting for DB connection and serving Clients.
    Test waits for Kea to be done waiting and check if Kea is still serving Clients.
    Then Kea is restarted and DB is reconnected after Kea starts to check if service is restored.
    DHCP traffic is send to confirm Kea is using reservations.
    """
    retries = 5
    wait_time = 2000
    misc.test_setup()
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
        srv_control.new_db_backend_reservation(backend, 'hw-address', 'ff:01:02:03:ff:04')
        srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, backend, 1)
        srv_control.update_db_backend_reservation("ipv4_address", "192.168.50.100", backend, 1)
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::60')
        srv_control.new_db_backend_reservation(backend, 'hw-address', 'f6:f5:f4:f3:f2:01')
        srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, backend, 1)
        srv_control.ipv6_address_db_backend_reservation('2001:db8:1::100', '$(EMPTY)', backend, 1)
    srv_control.upload_db_reservation(backend)

    world.reservation_backend = None  # Allow to override hosts-database settings
    world.dhcp_cfg["hosts-database"] = {"type": backend,
                                        "name": world.f_cfg.db_name,
                                        "host": world.f_cfg.db_host,
                                        "user": world.f_cfg.db_user,
                                        "password": world.f_cfg.db_passwd,
                                        "retry-on-startup": True,
                                        "max-reconnect-tries": retries,
                                        "reconnect-wait-time": wait_time,
                                        "on-fail": "serve-retry-continue"}
    srv_control.add_database_hook(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()

    # Stop database engine so Kea does not have anything to connect to.
    _stop_database(backend)
    # Start Kea
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    misc.test_procedure()

    # Confirm Kea is waiting for DB
    # Kea#3223 - It is not decided yet how Kea should report to status-get when there is no DB connection,
    # so we use version-get.
    cmd = {"command": "version-get", "arguments": {}}
    srv_msg.send_ctrl_cmd(cmd, 'http')
    log_contains_n_times('DHCPSRV_HOST_MGR_DB_OPEN_CONNECTION_WITH_RETRY_FAILED Failed to connect to database:', 1)
    log_doesnt_contain(f'DHCP{dhcp_version[1]}_SHUTDOWN server shutdown')

    # Confirm Kea is serving Clients
    if dhcp_version == 'v4':
        srv_msg.DORA('192.168.50.1')
    else:
        srv_msg.SARR('2001:db8:1::50')

    # Wait for Kea to be done waiting
    wait_for_message_in_log(f'DHCP{dhcp_version[1]}_DB_RECONNECT_FAILED maximum number of database reconnect attempts: '
                            f'{retries}, has been exhausted without success', count=1,
                            timeout=retries*wait_time/1000+1)

    # Confirm Kea is still started and serves clients
    if dhcp_version == 'v4':
        srv_msg.DORA('192.168.50.2', chaddr='ff:01:02:03:ff:05')
    else:
        srv_msg.SARR('2001:db8:1::51', duid='00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:05')

    # Start Kea again (logs are cleared)
    srv_control.start_srv('DHCP', 'stopped')
    srv_control.clear_some_data('logs')
    srv_control.start_srv('DHCP', 'started')

    # Confirm Kea is waiting for DB
    # Kea#3223 - It is not decided yet how Kea should report to status-get when there is no DB connection,
    # so we use version-get.
    cmd = {"command": "version-get", "arguments": {}}
    srv_msg.send_ctrl_cmd(cmd, 'http')
    log_contains_n_times('DHCPSRV_HOST_MGR_DB_OPEN_CONNECTION_WITH_RETRY_FAILED Failed to connect to database:', 1)
    log_doesnt_contain(f'DHCP{dhcp_version[1]}_SHUTDOWN server shutdown')

    # Start DB
    _start_database(backend)

    # Wait for Kea to recover connection to DB
    wait_for_message_in_log(
        f'DHCP{dhcp_version[1]}_DB_RECONNECT_SUCCEEDED database connection recovered.', count=1,
        timeout=retries*wait_time/1000+1)

    if dhcp_version == 'v4':
        srv_msg.DORA('192.168.50.100', chaddr='ff:01:02:03:ff:04')
    else:
        srv_msg.SARR('2001:db8:1::100', duid='00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')


@pytest.mark.usefixtures('_restart_databases')
@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_db_retry_legallog_stop_retry_exit(backend, dhcp_version):
    """Test starts Kea without legallog DB connection and checks it's behavior according to `on-fail`.
    stop-retry-exit - Kea should stop and not serve any clients after not being able to connect to DB.
    After exhausting retries Kea should shutdown.
    Testing steps:
    Forge starts Kea, confirms it is waiting for DB connection and not serving any Clients.
    After exhausting retries Kea should shutdown.
    Then Kea is restarted and DB is reconnected after Kea starts to check if service is restored.
    Legal log is checked to confirm Kea is using DB.
    """
    retries = 5
    wait_time = 2000
    misc.test_setup()
    # Stop database engine so Kea does not have anything to connect to.
    _stop_database(backend)
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')

    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook(1, 'name', world.f_cfg.db_name)
    srv_control.add_parameter_to_hook(1, 'password', world.f_cfg.db_passwd)
    srv_control.add_parameter_to_hook(1, 'type', backend)
    srv_control.add_parameter_to_hook(1, 'user', world.f_cfg.db_user)
    srv_control.add_parameter_to_hook(1, 'retry-on-startup', True)
    srv_control.add_parameter_to_hook(1, 'max-reconnect-tries', retries)
    srv_control.add_parameter_to_hook(1, 'reconnect-wait-time', wait_time)
    srv_control.add_parameter_to_hook(1, 'on-fail', 'stop-retry-exit')
    srv_control.add_database_hook(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()

    # Start Kea
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    misc.test_procedure()

    # Confirm Kea is waiting for DB
    # Kea#3223 - It is not decided yet how Kea should report to status-get when there is no DB connection,
    # so we use version-get.
    cmd = {"command": "version-get", "arguments": {}}
    srv_msg.send_ctrl_cmd(cmd, 'http')
    log_contains_n_times('LEGAL_LOG_DB_OPEN_CONNECTION_WITH_RETRY_FAILED Failed to connect to database:', 1)
    log_doesnt_contain(f'DHCP{dhcp_version[1]}_SHUTDOWN server shutdown')

    # Confirm Kea is not serving Clients
    _confirm_no_dhcp_service(dhcp_version)

    # Wait for kea shutdown after exhausting retries
    wait_for_message_in_log(f'DHCP{dhcp_version[1]}_SHUTDOWN server shutdown', count=1,
                            timeout=retries*wait_time/1000+1)

    # Confirm Kea is done waiting before shutdown
    cmd = {"command": "version-get", "arguments": {}}
    srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=1)
    log_contains_n_times(
        f'DHCP{dhcp_version[1]}_DB_RECONNECT_FAILED maximum number of database reconnect attempts: '
        f'{retries}, has been exhausted without success', 1)

    # Start Kea again (logs are cleared)
    srv_control.clear_some_data('logs')
    srv_control.start_srv('DHCP', 'restarted')

    # Confirm Kea is waiting for DB
    # Kea#3223 - It is not decided yet how Kea should report to status-get when there is no DB connection,
    # so we use version-get.
    cmd = {"command": "version-get", "arguments": {}}
    srv_msg.send_ctrl_cmd(cmd, 'http')
    log_contains_n_times('LEGAL_LOG_DB_OPEN_CONNECTION_WITH_RETRY_FAILED Failed to connect to database:', 1)
    log_doesnt_contain(f'DHCP{dhcp_version[1]}_SHUTDOWN server shutdown')

    # Start DB
    _start_database(backend)

    # Wait for Kea to recover connection to DB
    wait_for_message_in_log(
        f'DHCP{dhcp_version[1]}_DB_RECONNECT_SUCCEEDED database connection recovered.', count=1,
        timeout=retries*wait_time/1000+1)

    # Confirm Kea is started and connected to DB
    if dhcp_version == 'v4':
        srv_msg.DORA('192.168.50.1', chaddr='ff:01:02:03:ff:04')
        srv_msg.table_contains_line_n_times('logs', backend, 2,
                                            'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs '
                                            'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04')
    else:
        srv_msg.SARR('2001:db8:1::50', duid='00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')
        srv_msg.table_contains_line_n_times('logs', backend, 2,
                                            'Address: 2001:db8:1::50 has been assigned for 0 hrs 10 mins 0 secs '
                                            'to a device with DUID: 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01 '
                                            'and hardware address: hwtype=1 f6:f5:f4:f3:f2:01 (from DUID)')


@pytest.mark.usefixtures('_restart_databases')
@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_db_retry_legallog_serve_retry_exit(backend, dhcp_version):
    """Test starts Kea without legallog DB connection and checks it's behavior according to `on-fail`.
    serve-retry-exit - Kea should still serve clients after not being able to connect to DB.
    After exhausting retries Kea should shutdown.
    Testing steps:
    Forge starts Kea, confirms it is waiting for DB connection and serving any Clients.
    After exhausting retries Kea should shutdown.
    Then Kea is restarted and DB is reconnected after Kea starts to check if service is restored.
    Legal log is checked to confirm Kea is using DB.
    """
    retries = 5
    wait_time = 2000
    misc.test_setup()
    # Stop database engine so Kea does not have anything to connect to.
    _stop_database(backend)
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::100')

    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook(1, 'name', world.f_cfg.db_name)
    srv_control.add_parameter_to_hook(1, 'password', world.f_cfg.db_passwd)
    srv_control.add_parameter_to_hook(1, 'type', backend)
    srv_control.add_parameter_to_hook(1, 'user', world.f_cfg.db_user)
    srv_control.add_parameter_to_hook(1, 'retry-on-startup', True)
    srv_control.add_parameter_to_hook(1, 'max-reconnect-tries', retries)
    srv_control.add_parameter_to_hook(1, 'reconnect-wait-time', wait_time)
    srv_control.add_parameter_to_hook(1, 'on-fail', 'serve-retry-exit')
    srv_control.add_database_hook(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()

    # Start Kea
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    misc.test_procedure()

    # Confirm Kea is waiting for DB
    # Kea#3223 - It is not decided yet how Kea should report to status-get when there is no DB connection,
    # so we use version-get.
    cmd = {"command": "version-get", "arguments": {}}
    srv_msg.send_ctrl_cmd(cmd, 'http')
    log_contains_n_times('LEGAL_LOG_DB_OPEN_CONNECTION_WITH_RETRY_FAILED Failed to connect to database:', 1)
    log_doesnt_contain(f'DHCP{dhcp_version[1]}_SHUTDOWN server shutdown')

    # Confirm Kea is started and serves clients
    if dhcp_version == 'v4':
        srv_msg.DORA('192.168.50.1', chaddr='ff:01:02:03:ff:04')
    else:
        srv_msg.SARR('2001:db8:1::50', duid='00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')

    # Wait for kea shutdown
    wait_for_message_in_log(f'DHCP{dhcp_version[1]}_SHUTDOWN server shutdown', count=1,
                            timeout=retries*wait_time/1000+1)

    # Confirm Kea is done waiting before shutdown
    cmd = {"command": "version-get", "arguments": {}}
    srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=1)
    log_contains_n_times(
        f'DHCP{dhcp_version[1]}_DB_RECONNECT_FAILED maximum number of database reconnect attempts: '
        f'{retries}, has been exhausted without success', 1)

    # Start Kea again (logs are cleared)
    srv_control.clear_some_data('logs')
    srv_control.start_srv('DHCP', 'restarted')

    # Confirm Kea is waiting for DB
    # Kea#3223 - It is not decided yet how Kea should report to status-get when there is no DB connection,
    # so we use version-get.
    cmd = {"command": "version-get", "arguments": {}}
    srv_msg.send_ctrl_cmd(cmd, 'http')
    log_contains_n_times('LEGAL_LOG_DB_OPEN_CONNECTION_WITH_RETRY_FAILED Failed to connect to database:', 1)
    log_doesnt_contain(f'DHCP{dhcp_version[1]}_SHUTDOWN server shutdown')

    # Confirm Kea is started and serves clients
    if dhcp_version == 'v4':
        srv_msg.DORA('192.168.50.1', chaddr='ff:01:02:03:ff:04')
    else:
        srv_msg.SARR('2001:db8:1::50', duid='00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')

    # Start DB
    _start_database(backend)

    # Wait for Kea to recover connection to DB
    wait_for_message_in_log(
        f'DHCP{dhcp_version[1]}_DB_RECONNECT_SUCCEEDED database connection recovered.', count=1,
        timeout=retries*wait_time/1000+1)

    # Confirm Kea is started and connected to DB
    if dhcp_version == 'v4':
        srv_msg.DORA('192.168.50.2', chaddr='ff:01:02:03:ff:05')
        srv_msg.table_contains_line_n_times('logs', backend, 2,
                                            'Address: 192.168.50.2 has been assigned for 0 hrs 10 mins 0 secs '
                                            'to a device with hardware address: hwtype=1 ff:01:02:03:ff:05')
    else:
        srv_msg.SARR('2001:db8:1::51', duid='00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:05')
        srv_msg.table_contains_line_n_times('logs', backend, 2,
                                            'Address: 2001:db8:1::51 has been assigned for 0 hrs 10 mins 0 secs '
                                            'to a device with DUID: 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:05 '
                                            'and hardware address: hwtype=1 f6:f5:f4:f3:f2:05 (from DUID)')


@pytest.mark.usefixtures('_restart_databases')
@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_db_retry_legallog_serve_retry_continue(backend, dhcp_version):
    """Test starts Kea without legallog DB connection and checks it's behavior according to `on-fail`.
    serve-retry-continue - Kea should still serve clients traffic after not being able to connect to DB.
    After exhausting retries Kea should continue to serve clients non lease related traffic
    Testing steps:
    Forge starts Kea, confirms it is waiting for DB connection and serving Clients.
    Test waits for Kea to be done waiting and check if Kea is still serving Clients.
    Then Kea is restarted and DB is reconnected after Kea starts to check if service is restored.
    Legal log is checked to confirm Kea is using DB.
    """
    retries = 5
    wait_time = 2000
    misc.test_setup()
    # Stop database engine so Kea does not have anything to connect to.
    _stop_database(backend)
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::100')

    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook(1, 'name', world.f_cfg.db_name)
    srv_control.add_parameter_to_hook(1, 'password', world.f_cfg.db_passwd)
    srv_control.add_parameter_to_hook(1, 'type', backend)
    srv_control.add_parameter_to_hook(1, 'user', world.f_cfg.db_user)
    srv_control.add_parameter_to_hook(1, 'retry-on-startup', True)
    srv_control.add_parameter_to_hook(1, 'max-reconnect-tries', retries)
    srv_control.add_parameter_to_hook(1, 'reconnect-wait-time', wait_time)
    srv_control.add_parameter_to_hook(1, 'on-fail', 'serve-retry-continue')
    srv_control.add_database_hook(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()

    # Start Kea
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    misc.test_procedure()

    # Confirm Kea is waiting for DB
    # Kea#3223 - It is not decided yet how Kea should report to status-get when there is no DB connection,
    # so we use version-get.
    cmd = {"command": "version-get", "arguments": {}}
    srv_msg.send_ctrl_cmd(cmd, 'http')
    log_contains_n_times('LEGAL_LOG_DB_OPEN_CONNECTION_WITH_RETRY_FAILED Failed to connect to database:', 1)
    log_doesnt_contain(f'DHCP{dhcp_version[1]}_SHUTDOWN server shutdown')

    # Confirm Kea is started and serves clients
    if dhcp_version == 'v4':
        srv_msg.DORA('192.168.50.1', chaddr='ff:01:02:03:ff:04')
    else:
        srv_msg.SARR('2001:db8:1::50', duid='00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')

    # Wait for Kea to be done waiting
    wait_for_message_in_log(f'DHCP{dhcp_version[1]}_DB_RECONNECT_FAILED maximum number of database reconnect attempts: '
                            f'{retries}, has been exhausted without success', count=1,
                            timeout=retries*wait_time/1000+1)

    # Confirm Kea is still started and serves clients
    if dhcp_version == 'v4':
        srv_msg.DORA('192.168.50.2', chaddr='ff:01:02:03:ff:05')
    else:
        srv_msg.SARR('2001:db8:1::51', duid='00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:05')

    # Start Kea again (logs are cleared)
    srv_control.start_srv('DHCP', 'stopped')
    srv_control.clear_some_data('logs')
    srv_control.start_srv('DHCP', 'started')

    # Confirm Kea is waiting for DB
    # Kea#3223 - It is not decided yet how Kea should report to status-get when there is no DB connection,
    # so we use version-get.
    cmd = {"command": "version-get", "arguments": {}}
    srv_msg.send_ctrl_cmd(cmd, 'http')
    log_contains_n_times('LEGAL_LOG_DB_OPEN_CONNECTION_WITH_RETRY_FAILED Failed to connect to database:', 1)
    log_doesnt_contain(f'DHCP{dhcp_version[1]}_SHUTDOWN server shutdown')

    # Confirm Kea is started and serves clients
    if dhcp_version == 'v4':
        srv_msg.DORA('192.168.50.1', chaddr='ff:01:02:03:ff:04')
    else:
        srv_msg.SARR('2001:db8:1::50', duid='00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')

    # Start DB
    _start_database(backend)

    # Wait for Kea to recover connection to DB
    wait_for_message_in_log(
        f'DHCP{dhcp_version[1]}_DB_RECONNECT_SUCCEEDED database connection recovered.', count=1,
        timeout=retries*wait_time/1000+1)

    # Confirm Kea is started and connected to DB
    if dhcp_version == 'v4':
        srv_msg.DORA('192.168.50.2', chaddr='ff:01:02:03:ff:05')
        srv_msg.table_contains_line_n_times('logs', backend, 2,
                                            'Address: 192.168.50.2 has been assigned for 0 hrs 10 mins 0 secs '
                                            'to a device with hardware address: hwtype=1 ff:01:02:03:ff:05')
    else:
        srv_msg.SARR('2001:db8:1::51', duid='00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:05')
        srv_msg.table_contains_line_n_times('logs', backend, 2,
                                            'Address: 2001:db8:1::51 has been assigned for 0 hrs 10 mins 0 secs '
                                            'to a device with DUID: 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:05 '
                                            'and hardware address: hwtype=1 f6:f5:f4:f3:f2:05 (from DUID)')
