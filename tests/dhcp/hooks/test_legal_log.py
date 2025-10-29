# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea6 Legal logging hook"""

# pylint: disable=line-too-long

from datetime import datetime
import pytest

from src import misc
from src import srv_control
from src import srv_msg
from src.forge_cfg import world
from src.protosupport.multi_protocol_functions import file_contains_line_n_times, file_doesnt_contain_line
from src.protosupport.multi_protocol_functions import log_contains, log_doesnt_contain, log_contains_n_times
from src.softwaresupport.multi_server_functions import fabric_sudo_command, fabric_download_file
from src.softwaresupport.multi_server_functions import verify_file_permissions


# number of messages that the client will send in each test
MESSAGE_COUNT = 3


def _send_client_requests(count, ia_pd=False, duid='00:03:00:01:f6:f5:f4:f3:f2:04'):
    for _ in range(count):
        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'DUID', duid)
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_does_include('Client', 'IA-NA')
        if ia_pd:
            srv_msg.client_does_include('Client', 'IA-PD')
        srv_msg.client_send_msg('SOLICIT')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
        srv_msg.response_check_include_option(1)
        srv_msg.response_check_include_option(2)
        srv_msg.response_check_include_option(3)
        srv_msg.response_check_option_content(3, 'sub-option', 5)

        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'DUID', duid)
        srv_msg.client_copy_option('server-id')
        srv_msg.client_copy_option('IA_NA')
        if ia_pd:
            srv_msg.client_does_include('Client', 'IA-PD')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_send_msg('REQUEST')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'REPLY')
        srv_msg.response_check_include_option(3)
        srv_msg.response_check_option_content(3, 'sub-option', 5)


def _send_client_renews(count, duid='00:03:00:01:f6:f5:f4:f3:f2:04'):
    for _ in range(count):
        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'DUID', duid)
        srv_msg.client_copy_option('server-id')
        srv_msg.client_copy_option('IA_NA')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_send_msg('RENEW')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'REPLY')
        srv_msg.response_check_include_option(1)
        srv_msg.response_check_include_option(2)
        srv_msg.response_check_include_option(3)
        srv_msg.response_check_option_content(3, 'sub-option', 5)


def _send_client_rebinds(count, duid='00:03:00:01:f6:f5:f4:f3:f2:04'):
    for _ in range(count):
        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'DUID', duid)
        srv_msg.client_copy_option('server-id')
        srv_msg.client_copy_option('IA_NA')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_send_msg('RENEW')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'REPLY')
        srv_msg.response_check_include_option(1)
        srv_msg.response_check_include_option(2)
        srv_msg.response_check_include_option(3)
        srv_msg.response_check_option_content(3, 'sub-option', 5)


def _send_client_requests_with_docsis(count):
    for _ in range(count):
        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_does_include('Client', 'IA-NA')
        srv_msg.client_send_msg('SOLICIT')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
        srv_msg.response_check_include_option(1)
        srv_msg.response_check_include_option(2)
        srv_msg.response_check_include_option(3)
        srv_msg.response_check_option_content(3, 'sub-option', 5)

        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
        srv_msg.client_does_include('Client', 'vendor-class')
        srv_msg.add_vendor_suboption('Client', 36, 'f6:f5:f4:f3:f2:01')
        srv_msg.client_does_include('Client', 'vendor-specific-info')
        srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
        srv_msg.client_copy_option('server-id')
        srv_msg.client_copy_option('IA_NA')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_send_msg('REQUEST')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'REPLY')
        srv_msg.response_check_include_option(3)
        srv_msg.response_check_option_content(3, 'sub-option', 5)


def _send_relayed_client_requests_with_docsis(count):
    for _ in range(count):
        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_does_include('Client', 'IA-NA')
        srv_msg.client_send_msg('SOLICIT')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

        misc.test_procedure()
        srv_msg.client_copy_option('IA_NA')
        srv_msg.client_copy_option('server-id')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_send_msg('REQUEST')

        srv_msg.client_sets_value('RelayAgent', 'enterprisenum', '4491')
        srv_msg.client_does_include('RelayAgent', 'vendor-class')
        srv_msg.add_vendor_suboption('RelayAgent', 1026, '00:f5:f4:00:f2:01')
        srv_msg.client_does_include('RelayAgent', 'vendor-specific-info')
        srv_msg.client_does_include('RelayAgent', 'interface-id')
        srv_msg.create_relay_forward()

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
        srv_msg.response_check_include_option(18)
        srv_msg.response_check_include_option(9)


def _send_relayed_client_requests(count):
    for _ in range(count):
        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'DUID', '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')
        srv_msg.client_requests_option(7)
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_does_include('Client', 'IA-NA')
        srv_msg.client_send_msg('SOLICIT')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

        misc.test_procedure()
        srv_msg.client_copy_option('IA_NA')
        srv_msg.client_sets_value('Client', 'DUID', '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')
        srv_msg.client_copy_option('server-id')
        srv_msg.client_requests_option(7)
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_send_msg('REQUEST')

        srv_msg.client_sets_value('Client', 'enterprisenum', 666)
        srv_msg.client_sets_value('Client', 'subscriber_id', 50)
        srv_msg.client_does_include('Client', 'remote-id')
        srv_msg.client_does_include('Client', 'subscriber-id')
        srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8:1::1005')
        srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'abc')
        srv_msg.client_does_include('RelayAgent', 'interface-id')
        srv_msg.create_relay_forward(5)

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
        srv_msg.response_check_include_option(18)
        srv_msg.response_check_include_option(9)


def _send_client_requests_for_flex_id(count):
    for _ in range(count):
        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
        srv_msg.client_does_include('Client', 'vendor-class')
        srv_msg.add_vendor_suboption('Client', 1026, '01:02:03:04:05:06')
        srv_msg.client_does_include('Client', 'vendor-specific-info')

        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_does_include('Client', 'IA-NA')
        srv_msg.client_send_msg('SOLICIT')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
        srv_msg.response_check_include_option(3)
        srv_msg.response_check_option_content(3, 'sub-option', 5)
        srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')

        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
        srv_msg.client_does_include('Client', 'vendor-class')
        srv_msg.add_vendor_suboption('Client', 1026, '01:02:03:04:05:06')
        srv_msg.client_does_include('Client', 'vendor-specific-info')
        srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
        srv_msg.client_copy_option('server-id')
        srv_msg.client_copy_option('IA_NA')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_send_msg('REQUEST')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'REPLY')
        srv_msg.response_check_include_option(3)
        srv_msg.response_check_option_content(3, 'sub-option', 5)


def _send_client_requests4(count, client_id=True):
    for _ in range(count):
        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
        if client_id:
            srv_msg.client_does_include_with_value('client_id', '00010203040506')
        srv_msg.client_requests_option(1)
        srv_msg.client_send_msg('DISCOVER')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'OFFER')
        srv_msg.response_check_content('yiaddr', '192.168.50.1')
        srv_msg.response_check_include_option(1)
        srv_msg.response_check_include_option(54)
        srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
        if client_id:
            srv_msg.response_check_include_option(61)
            srv_msg.response_check_option_content(61, 'value', '00010203040506')

        misc.test_procedure()
        if client_id:
            srv_msg.client_does_include_with_value('client_id', '00010203040506')
        srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
        srv_msg.client_copy_option('server_id')
        srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
        srv_msg.client_requests_option(1)
        srv_msg.client_send_msg('REQUEST')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'ACK')
        srv_msg.response_check_content('yiaddr', '192.168.50.1')
        srv_msg.response_check_include_option(1)
        srv_msg.response_check_include_option(54)
        srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
        if client_id:
            srv_msg.response_check_include_option(61)
            srv_msg.response_check_option_content(61, 'value', '00010203040506')


def _send_client_requests_via_relay4(count, address='192.168.50.1'):
    for _ in range(count):
        misc.test_procedure()
        srv_msg.client_does_include_with_value('client_id', '00010203040577')
        srv_msg.network_variable('source_port', 67)
        srv_msg.network_variable('source_address', '$(GIADDR4)')
        srv_msg.network_variable('destination_address', '$(SRV4_ADDR)')
        srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:05')
        srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
        srv_msg.client_sets_value('Client', 'hops', 1)
        srv_msg.client_requests_option(1)
        srv_msg.client_send_msg('DISCOVER')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'OFFER')
        srv_msg.response_check_include_option(1)
        srv_msg.response_check_content('yiaddr', address)
        srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

        misc.test_procedure()
        srv_msg.client_does_include_with_value('client_id', '00010203040577')
        srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:05')
        srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
        srv_msg.client_sets_value('Client', 'hops', 1)
        srv_msg.client_copy_option('server_id')
        srv_msg.client_does_include_with_value('requested_addr', address)
        srv_msg.client_requests_option(1)
        srv_msg.client_send_msg('REQUEST')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'ACK')
        srv_msg.response_check_content('yiaddr', address)
        srv_msg.response_check_include_option(1)
        srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


def _send_client_requests_in_renew_state4(count):
    _send_client_requests4(count)

    # make sure that T1 time expires and client will be in RENEWING state.
    srv_msg.forge_sleep(3, 'seconds')

    for _ in range(count):
        misc.test_procedure()
        srv_msg.client_does_include_with_value('client_id', '00010203040506')
        srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
        srv_msg.client_copy_option('server_id')
        srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
        srv_msg.client_requests_option(1)
        srv_msg.client_send_msg('REQUEST')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'ACK')
        srv_msg.response_check_content('yiaddr', '192.168.50.1')
        srv_msg.response_check_include_option(1)
        srv_msg.response_check_include_option(54)
        srv_msg.response_check_include_option(61)
        srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
        srv_msg.response_check_option_content(61, 'value', '00010203040506')


def _send_client_requests_in_rebind_state4(count):
    _send_client_requests4(count)

    # make sure that T1 time expires and client will be in RENEWING state.
    srv_msg.forge_sleep(5, 'seconds')

    for _ in range(count):
        misc.test_procedure()
        srv_msg.client_does_include_with_value('client_id', '00010203040506')
        srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
        srv_msg.client_copy_option('server_id')
        srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
        srv_msg.client_requests_option(1)
        srv_msg.client_send_msg('REQUEST')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'ACK')
        srv_msg.response_check_content('yiaddr', '192.168.50.1')
        srv_msg.response_check_include_option(1)
        srv_msg.response_check_include_option(54)
        srv_msg.response_check_include_option(61)
        srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
        srv_msg.response_check_option_content(61, 'value', '00010203040506')


def _wait_till_elapsed(start, seconds):
    print("Waiting for log rotation time to elapse...")
    while (datetime.now() - start).total_seconds() < seconds:
        pass


def _add_guarded_subnet_with_logging_off6(class_test=False):
    # Create guarded subnet with classs and reservation to check if it is not logged
    srv_control.config_srv_another_subnet_no_interface('2001:db8:20::/64', '2001:db8:20::5-2001:db8:20::50',
                                                       client_classes=['50'], id=5,
                                                       user_context={"legal-logging": False})
    srv_control.config_srv_prefix('2001:db8:30::', 0, 90, 94)
    srv_control.create_new_class('50')
    if class_test:
        srv_control.add_test_to_class(1, 'test', 'vendor[4491].option[1026].hex == 0xf6f5f4f3f205')
    reservations = [{"duid": "00:03:00:01:f6:f5:f4:f3:f2:05",
                     "client-classes": ["50"]}]
    world.dhcp_cfg.update({'reservations': reservations})
    world.dhcp_cfg['early-global-reservations-lookup'] = True
    world.dhcp_cfg['reservations-global'] = True


def _get_journal_logs(syslog):
    """Get journal logs for a given log file.

    :param syslog: syslog facility
    :type syslog: str
    """
    facility = int(syslog[-1]) + 16
    cmd = f'journalctl SYSLOG_FACILITY={facility} > /tmp/kea_syslog.log'
    fabric_sudo_command(cmd, ignore_errors=True)
    fabric_download_file('/tmp/kea_syslog.log', world.cfg["test_result_dir"], ignore_errors=True,
                         hide_all=world.f_cfg.forge_verbose == 0)


@pytest.mark.v6
@pytest.mark.legal_logging
@pytest.mark.parametrize('mode', ['global', 'subnet'])
def test_v6_legal_log_address_assigned_duid(mode):
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.log_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('preferred-lifetime', 400)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50', id=10)
    srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 94)
    if mode == 'subnet':
        _add_guarded_subnet_with_logging_off6()
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests(MESSAGE_COUNT)
    if mode == 'subnet':
        _send_client_requests(MESSAGE_COUNT, duid='00:03:00:01:f6:f5:f4:f3:f2:05')

    srv_msg.copy_remote(world.f_cfg.log_join('kea-legal*.txt'))
    file_contains_line_n_times(world.f_cfg.log_join('kea-legal*.txt'), MESSAGE_COUNT,
                               'Address: 2001:db8:1::5 has been assigned for 0 hrs 10 mins 0 secs '
                               'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 '
                               'and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')
    if mode == 'subnet':
        file_doesnt_contain_line(world.f_cfg.log_join('kea-legal*.txt'),
                                 'Address: 2001:db8:20::5 has been assigned for 0 hrs 10 mins 0 secs '
                                 'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:05 '
                                 'and hardware address: hwtype=1 f6:f5:f4:f3:f2:05 (from DUID)')
        srv_msg.check_leases({'address': '2001:db8:20::5', "duid": "00:03:00:01:f6:f5:f4:f3:f2:05"})


@pytest.mark.v6
@pytest.mark.legal_logging
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
@pytest.mark.parametrize('mode', ['global', 'subnet'])
def test_v6_legal_log_address_assigned_duid_db(backend, mode):
    srv_msg.remove_from_db_table('logs', backend)

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('preferred-lifetime', 400)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50', id=10)
    srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 94)
    if mode == 'subnet':
        _add_guarded_subnet_with_logging_off6()
    srv_control.add_database_hook(backend)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'type', backend)
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests(MESSAGE_COUNT)
    if mode == 'subnet':
        _send_client_requests(MESSAGE_COUNT, duid='00:03:00:01:f6:f5:f4:f3:f2:05')

    srv_msg.table_contains_line_n_times('logs', backend, MESSAGE_COUNT,
                                        'Address: 2001:db8:1::5 has been assigned for 0 hrs 10 mins 0 secs '
                                        'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 '
                                        'and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')
    if mode == 'subnet':
        srv_msg.table_contains_line_n_times('logs', backend, 0,
                                            'Address: 2001:db8:20::5 has been assigned for 0 hrs 10 mins 0 secs '
                                            'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:05 '
                                            'and hardware address: hwtype=1 f6:f5:f4:f3:f2:05 (from DUID)')
        srv_msg.check_leases({'address': '2001:db8:20::5',
                              "duid": "00:03:00:01:f6:f5:f4:f3:f2:05"})


@pytest.mark.v6
@pytest.mark.legal_logging
@pytest.mark.parametrize('mode', ['global', 'subnet'])
def test_v6_legal_log_address_renewed_duid(mode):
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.log_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('preferred-lifetime', 400)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50', id=10)
    srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 94)
    if mode == 'subnet':
        _add_guarded_subnet_with_logging_off6()
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests(MESSAGE_COUNT)

    _send_client_renews(MESSAGE_COUNT)

    if mode == 'subnet':
        _send_client_requests(MESSAGE_COUNT, duid='00:03:00:01:f6:f5:f4:f3:f2:05')
        _send_client_renews(MESSAGE_COUNT, duid='00:03:00:01:f6:f5:f4:f3:f2:05')

    srv_msg.copy_remote(world.f_cfg.log_join('kea-legal*.txt'))
    file_contains_line_n_times(world.f_cfg.log_join('kea-legal*.txt'), 2 * MESSAGE_COUNT,
                               'Address: 2001:db8:1::5 has been assigned for 0 hrs 10 mins 0 secs '
                               'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 '
                               'and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')

    if mode == 'subnet':
        file_doesnt_contain_line(world.f_cfg.log_join('kea-legal*.txt'),
                                 'Address: 2001:db8:20::5 has been assigned for 0 hrs 10 mins 0 secs '
                                 'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:05 '
                                 'and hardware address: hwtype=1 f6:f5:f4:f3:f2:05 (from DUID)')
        srv_msg.check_leases({'address': '2001:db8:20::5', "duid": "00:03:00:01:f6:f5:f4:f3:f2:05"})


@pytest.mark.v6
@pytest.mark.legal_logging
@pytest.mark.parametrize('mode', ['global', 'subnet'])
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_v6_legal_log_address_renewed_duid_db(backend, mode):
    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', backend)

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('preferred-lifetime', 400)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50', id=10)
    srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 94)
    if mode == 'subnet':
        _add_guarded_subnet_with_logging_off6()
    srv_control.add_database_hook(backend)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'type', backend)
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests(MESSAGE_COUNT)

    _send_client_renews(MESSAGE_COUNT)

    if mode == 'subnet':
        _send_client_requests(MESSAGE_COUNT, duid='00:03:00:01:f6:f5:f4:f3:f2:05')
        _send_client_renews(MESSAGE_COUNT, duid='00:03:00:01:f6:f5:f4:f3:f2:05')

    srv_msg.table_contains_line_n_times('logs', backend, 2 * MESSAGE_COUNT,
                                        'Address: 2001:db8:1::5 has been assigned for 0 hrs 10 mins 0 secs '
                                        'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 '
                                        'and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')
    if mode == 'subnet':
        srv_msg.table_contains_line_n_times('logs', backend, 0,
                                            'Address: 2001:db8:20::5 has been assigned for 0 hrs 10 mins 0 secs '
                                            'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:05 '
                                            'and hardware address: hwtype=1 f6:f5:f4:f3:f2:05 (from DUID)')
        srv_msg.check_leases({'address': '2001:db8:20::5',
                              "duid": "00:03:00:01:f6:f5:f4:f3:f2:05"})


@pytest.mark.v6
@pytest.mark.legal_logging
@pytest.mark.parametrize('mode', ['global', 'subnet'])
def test_v6_legal_log_address_rebind_duid(mode):
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.log_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('preferred-lifetime', 400)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50', id=10)
    srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 94)
    if mode == 'subnet':
        _add_guarded_subnet_with_logging_off6()
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests(MESSAGE_COUNT)

    _send_client_rebinds(MESSAGE_COUNT)

    if mode == 'subnet':
        _send_client_requests(MESSAGE_COUNT, duid='00:03:00:01:f6:f5:f4:f3:f2:05')
        _send_client_rebinds(MESSAGE_COUNT, duid='00:03:00:01:f6:f5:f4:f3:f2:05')

    srv_msg.copy_remote(world.f_cfg.log_join('kea-legal*.txt'))
    file_contains_line_n_times(world.f_cfg.log_join('kea-legal*.txt'), 2 * MESSAGE_COUNT,
                               'Address: 2001:db8:1::5 has been assigned for 0 hrs 10 mins 0 secs '
                               'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 '
                               'and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')
    if mode == 'subnet':
        file_doesnt_contain_line(world.f_cfg.log_join('kea-legal*.txt'),
                                 'Address: 2001:db8:20::5 has been assigned for 0 hrs 10 mins 0 secs '
                                 'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:05 '
                                 'and hardware address: hwtype=1 f6:f5:f4:f3:f2:05 (from DUID)')
        srv_msg.check_leases({'address': '2001:db8:20::5', "duid": "00:03:00:01:f6:f5:f4:f3:f2:05"})


@pytest.mark.v6
@pytest.mark.legal_logging
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
@pytest.mark.parametrize('mode', ['global', 'subnet'])
def test_v6_legal_log_address_rebind_duid_db(backend, mode):
    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', backend)

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('preferred-lifetime', 400)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50', id=10)
    srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 94)
    if mode == 'subnet':
        _add_guarded_subnet_with_logging_off6()
    srv_control.add_database_hook(backend)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'type', backend)
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests(MESSAGE_COUNT)

    _send_client_rebinds(MESSAGE_COUNT)

    if mode == 'subnet':
        _send_client_requests(MESSAGE_COUNT, duid='00:03:00:01:f6:f5:f4:f3:f2:05')
        _send_client_rebinds(MESSAGE_COUNT, duid='00:03:00:01:f6:f5:f4:f3:f2:05')

    srv_msg.table_contains_line_n_times('logs', backend, 2 * MESSAGE_COUNT,
                                        'Address: 2001:db8:1::5 has been assigned for 0 hrs 10 mins 0 secs '
                                        'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 '
                                        'and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')
    if mode == 'subnet':
        srv_msg.table_contains_line_n_times('logs', backend, 0,
                                            'Address: 2001:db8:20::5 has been assigned for 0 hrs 10 mins 0 secs '
                                            'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:05 '
                                            'and hardware address: hwtype=1 f6:f5:f4:f3:f2:05 (from DUID)')
        srv_msg.check_leases({'address': '2001:db8:20::5',
                              "duid": "00:03:00:01:f6:f5:f4:f3:f2:05"})


@pytest.mark.v6
@pytest.mark.legal_logging
def test_v6_legal_log_address_assigned_docsis_modem():
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.log_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('preferred-lifetime', 400)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50')
    srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 94)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_line({"mac-sources": ["docsis-modem"]})
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests_with_docsis(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.log_join('kea-legal*.txt'))
    file_contains_line_n_times(world.f_cfg.log_join('kea-legal*.txt'), MESSAGE_COUNT,
                               'Address: 2001:db8:1::5 has been assigned for 0 hrs 10 mins 0 secs '
                               'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 '
                               'and hardware address: hwtype=1 f6:f5:f4:f3:f2:01 (from DOCSIS MODEM)')


@pytest.mark.v6
@pytest.mark.legal_logging
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_v6_legal_log_address_assigned_docsis_modem_db(backend):
    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', backend)

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('preferred-lifetime', 400)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50')
    srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 94)
    srv_control.add_database_hook(backend)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'type', backend)
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'user', '$(DB_USER)')
    srv_control.add_line({"mac-sources": ["docsis-modem"]})
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests_with_docsis(MESSAGE_COUNT)

    srv_msg.table_contains_line_n_times('logs', backend, MESSAGE_COUNT,
                                        'Address: 2001:db8:1::5 has been assigned for 0 hrs 10 mins 0 secs '
                                        'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and '
                                        'hardware address: hwtype=1 f6:f5:f4:f3:f2:01 (from DOCSIS MODEM)')


@pytest.mark.v6
@pytest.mark.legal_logging
@pytest.mark.relay
def test_v6_legal_log_address_assigned_docsis_cmts():
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.log_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('preferred-lifetime', 400)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50')
    srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 94)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_line({"mac-sources": ["docsis-cmts"]})
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_relayed_client_requests_with_docsis(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.log_join('kea-legal*.txt'))
    file_contains_line_n_times(world.f_cfg.log_join('kea-legal*.txt'), MESSAGE_COUNT,
                               'Address: 2001:db8:1::5 has been assigned for 0 hrs 10 mins 0 secs '
                               'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:01 '
                               'and hardware address: hwtype=1 00:f5:f4:00:f2:01 (from DOCSIS CMTS)')


@pytest.mark.v6
@pytest.mark.legal_logging
@pytest.mark.relay
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_v6_legal_log_address_assigned_docsis_cmts_db(backend):
    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', backend)

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('preferred-lifetime', 400)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50')
    srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 94)
    srv_control.add_database_hook(backend)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'type', backend)
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'user', '$(DB_USER)')
    srv_control.add_line({"mac-sources": ["docsis-cmts"]})
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_relayed_client_requests_with_docsis(MESSAGE_COUNT)

    srv_msg.table_contains_line_n_times('logs', backend, MESSAGE_COUNT,
                                        'Address: 2001:db8:1::5 has been assigned for 0 hrs 10 mins 0 secs '
                                        'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:01 '
                                        'and hardware address: hwtype=1 00:f5:f4:00:f2:01 (from DOCSIS CMTS)')


@pytest.mark.v6
@pytest.mark.legal_logging
@pytest.mark.relay
def test_v6_legal_log_address_assigned_relay():
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.log_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('preferred-lifetime', 400)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50')
    srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 94)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_relayed_client_requests(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.log_join('kea-legal*.txt'))
    file_contains_line_n_times(world.f_cfg.log_join('kea-legal*.txt'), MESSAGE_COUNT,
                               'Address: 2001:db8:1::5 has been assigned for 0 hrs 10 mins 0 secs '
                               'to a device with DUID: 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01 '
                               'and hardware address: hwtype=1 f6:f5:f4:f3:f2:01 (from DUID) '
                               'connected via relay at address:')
    file_contains_line_n_times(world.f_cfg.log_join('kea-legal*.txt'), MESSAGE_COUNT,
                               'for client on link address: 2001:db8:1::1005, hop count: 4')


@pytest.mark.v6
@pytest.mark.legal_logging
@pytest.mark.relay
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_v6_legal_log_address_assigned_relay_db(backend):
    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', backend)

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('preferred-lifetime', 400)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50')
    srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 94)
    srv_control.add_database_hook(backend)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'type', backend)
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_relayed_client_requests(MESSAGE_COUNT)

    srv_msg.table_contains_line_n_times('logs', backend, MESSAGE_COUNT,
                                        'Address: 2001:db8:1::5 has been assigned for 0 hrs 10 mins 0 secs '
                                        'to a device with DUID: 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01 '
                                        'and hardware address: hwtype=1 f6:f5:f4:f3:f2:01 (from DUID) '
                                        'connected via relay at address:')
    srv_msg.table_contains_line_n_times('logs', backend, MESSAGE_COUNT,
                                        'for client on link address: 2001:db8:1::1005, hop count: 4')


@pytest.mark.v6
@pytest.mark.legal_logging
def test_v6_legal_log_with_flex_id_address_assigned():
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.log_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('preferred-lifetime', 400)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           0,
                                           'flex-id',
                                           '01:02:03:04:05:06')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '2001:db8:1::f')
    srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 94)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook("libdhcp_flex_id.so",
                                      'identifier-expression',
                                      'vendor[4491].option[1026].hex')
    srv_control.add_line({"host-reservation-identifiers": ["duid", "flex-id"]})
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests_for_flex_id(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.log_join('kea-legal*.txt'))
    file_contains_line_n_times(world.f_cfg.log_join('kea-legal*.txt'), MESSAGE_COUNT,
                               'Address: 2001:db8:1::f has been assigned for 0 hrs 10 mins 0 secs '
                               'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 '
                               'and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')


@pytest.mark.v6
@pytest.mark.legal_logging
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_v6_legal_log_with_flex_id_address_assigned_db(backend):
    srv_msg.remove_from_db_table('logs', backend)

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('preferred-lifetime', 400)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           0,
                                           'flex-id',
                                           '01:02:03:04:05:06')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '2001:db8:1::f')
    srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 94)
    srv_control.add_database_hook(backend)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'type', backend)
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'user', '$(DB_USER)')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook("libdhcp_flex_id.so",
                                      'identifier-expression',
                                      'vendor[4491].option[1026].hex')
    srv_control.add_line({"host-reservation-identifiers": ["duid", "flex-id"]})
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests_for_flex_id(MESSAGE_COUNT)

    srv_msg.table_contains_line_n_times('logs', backend, MESSAGE_COUNT,
                                        'Address: 2001:db8:1::f has been assigned for 0 hrs 10 mins 0 secs '
                                        'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 '
                                        'and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')


@pytest.mark.v6
@pytest.mark.legal_logging
def test_v6_legal_log_parser_format():
    """
    Test checks custom formatting of "legal_log" hook.
    'request-parser-format' and 'response-parser-format' parameters are configured with a set of expressions.
    SARR exchange is used to acquire leases.
    Log file is checked for proper content.
    """
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.log_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50')
    srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 94)
    srv_control.add_hooks('libdhcp_legal_log.so')
    request_format = "pkt.iface +" \
                     "addrtotext(pkt.src) +" \
                     "addrtotext(pkt.dst) +" \
                     "int32totext(pkt.len) +" \
                     "int32totext(pkt6.msgtype) +" \
                     "int32totext(pkt6.msgtype) +" \
                     "int32totext(pkt6.transid) +" \
                     "addrtotext(relay6[0].linkaddr) +" \
                     "0x0a"
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", "request-parser-format", request_format)
    response_format = "pkt.iface +" \
                      "addrtotext(pkt.src) +" \
                      "addrtotext(pkt.dst) +" \
                      "int32totext(pkt.len) +" \
                      "int32totext(pkt6.msgtype) +" \
                      "int32totext(pkt6.msgtype) +" \
                      "int32totext(pkt6.transid) +" \
                      "addrtotext(relay6[0].linkaddr)"
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", "response-parser-format", response_format)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.log_join('kea-legal*.txt'))
    request_line = f'{world.f_cfg.server_iface}' \
                   f'{world.f_cfg.cli_link_local}' \
                   f'ff02::1:2' \
                   f'80' \
                   f'3' \
                   f'3' \
                   f'{world.cfg["values"]["tr_id"]}' \
                   f''
    response_line = f'{world.f_cfg.server_iface}' \
                    f'{world.f_cfg.cli_link_local}' \
                    f'ff02::1:2' \
                    f'80' \
                    f'7' \
                    f'7' \
                    f'{world.cfg["values"]["tr_id"]}' \
                    f''

    file_contains_line_n_times(world.f_cfg.log_join('kea-legal*.txt'), MESSAGE_COUNT, request_line)
    file_contains_line_n_times(world.f_cfg.log_join('kea-legal*.txt'), MESSAGE_COUNT, response_line)


@pytest.mark.v6
@pytest.mark.legal_logging
def test_v6_legal_log_parser_format_via_relay():
    """
    Test checks custom formatting of "legal_log" hook.
    'request-parser-format' and 'response-parser-format' parameters are configured with a set of expressions.
    SARR exchange via relay is used to acquire leases.
    Log file is checked for proper content.
    """
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.log_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50')
    srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 94)
    srv_control.add_hooks('libdhcp_legal_log.so')
    request_format = "pkt.iface +" \
                     "addrtotext(pkt.src) +" \
                     "addrtotext(pkt.dst) +" \
                     "int32totext(pkt.len) +" \
                     "int32totext(pkt6.msgtype) +" \
                     "int32totext(pkt6.msgtype) +" \
                     "int32totext(pkt6.transid) +" \
                     "addrtotext(relay6[0].linkaddr) + " \
                     "addrtotext(relay6[0].peeraddr) + " \
                     "0x0a"
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", "request-parser-format", request_format)
    response_format = "pkt.iface +" \
                      "addrtotext(pkt.src) +" \
                      "addrtotext(pkt.dst) +" \
                      "int32totext(pkt.len) +" \
                      "int32totext(pkt6.msgtype) +" \
                      "int32totext(pkt6.msgtype) +" \
                      "int32totext(pkt6.transid) +" \
                      "addrtotext(relay6[0].linkaddr) + " \
                      "addrtotext(relay6[0].peeraddr)"
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", "response-parser-format", response_format)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_relayed_client_requests(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.log_join('kea-legal*.txt'))
    request_line = f'{world.f_cfg.server_iface}' \
                   f'{world.f_cfg.cli_link_local}' \
                   f'ff02::1:2' \
                   f'315' \
                   f'3' \
                   f'3' \
                   f'{world.cfg["values"]["tr_id"]}' \
                   f'2001:db8:1::1005' \
                   f'{world.f_cfg.cli_link_local}'
    response_line = f'{world.f_cfg.server_iface}' \
                    f'{world.f_cfg.cli_link_local}' \
                    f'ff02::1:2' \
                    f'309' \
                    f'7' \
                    f'7' \
                    f'{world.cfg["values"]["tr_id"]}' \
                    f'2001:db8:1::1005' \
                    f'{world.f_cfg.cli_link_local}'

    file_contains_line_n_times(world.f_cfg.log_join('kea-legal*.txt'), MESSAGE_COUNT, request_line)
    file_contains_line_n_times(world.f_cfg.log_join('kea-legal*.txt'), MESSAGE_COUNT, response_line)


@pytest.mark.v6
@pytest.mark.legal_logging
def test_v6_legal_log_parser_format_dual_ip():
    """
    Test checks custom formatting of "legal_log" hook with multiple ip addresses in one lease.
    'request-parser-format' and 'response-parser-format' parameters are configured with a set of expressions.
    SARR exchange is used to acquire leases.
    Log file is checked for proper content.
    """
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.log_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50')
    srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 94)
    srv_control.add_hooks('libdhcp_legal_log.so')
    request_format = "pkt.iface +" \
                     "ifelse(option[3].option[5].exists, addrtotext(substring(option[3].option[5].hex, 0, 16)),'none') +" \
                     "ifelse(option[25].option[26].exists, addrtotext(substring(option[25].option[26].hex, 9, 16)), 'none') +" \
                     "addrtotext(pkt.src) +" \
                     "addrtotext(pkt.dst) +" \
                     "int32totext(pkt.len) +" \
                     "int32totext(pkt6.msgtype) +" \
                     "int32totext(pkt6.msgtype) +" \
                     "int32totext(pkt6.transid) +" \
                     "addrtotext(relay6[0].linkaddr) +" \
                     "0x0a"
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", "request-parser-format", request_format)
    response_format = "pkt.iface +" \
                      "ifelse(option[3].option[5].exists, addrtotext(substring(option[3].option[5].hex, 0, 16)),'none') +" \
                      "ifelse(option[25].option[26].exists, addrtotext(substring(option[25].option[26].hex, 9, 16)), 'none') +" \
                      "addrtotext(pkt.src) +" \
                      "addrtotext(pkt.dst) +" \
                      "int32totext(pkt.len) +" \
                      "int32totext(pkt6.msgtype) +" \
                      "int32totext(pkt6.msgtype) +" \
                      "int32totext(pkt6.transid) +" \
                      "addrtotext(relay6[0].linkaddr)"
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", "response-parser-format", response_format)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests(MESSAGE_COUNT, ia_pd=True)

    srv_msg.copy_remote(world.f_cfg.log_join('kea-legal*.txt'))
    request_line_na = f'{world.f_cfg.server_iface}' \
                      f'2001:db8:1::5' \
                      f'none' \
                      f'{world.f_cfg.cli_link_local}' \
                      f'ff02::1:2' \
                      f'96' \
                      f'3' \
                      f'3' \
                      f'{world.cfg["values"]["tr_id"]}' \
                      f''
    response_line_na = f'{world.f_cfg.server_iface}' \
                       f'2001:db8:1::5' \
                       f'none' \
                       f'{world.f_cfg.cli_link_local}' \
                       f'ff02::1:2' \
                       f'125' \
                       f'7' \
                       f'7' \
                       f'{world.cfg["values"]["tr_id"]}' \
                       f''

    file_contains_line_n_times(world.f_cfg.log_join('kea-legal*.txt'), MESSAGE_COUNT, request_line_na)
    file_contains_line_n_times(world.f_cfg.log_join('kea-legal*.txt'), MESSAGE_COUNT, response_line_na)

    request_line_pd = f'{world.f_cfg.server_iface}' \
                      f'none' \
                      f'none' \
                      f'{world.f_cfg.cli_link_local}' \
                      f'ff02::1:2' \
                      f'96' \
                      f'3' \
                      f'3' \
                      f'{world.cfg["values"]["tr_id"]}' \
                      f''
    response_line_pd = f'{world.f_cfg.server_iface}' \
                       f'none' \
                       f'2001:db8:2::4:0:0' \
                       f'{world.f_cfg.cli_link_local}' \
                       f'ff02::1:2' \
                       f'125' \
                       f'7' \
                       f'7' \
                       f'{world.cfg["values"]["tr_id"]}' \
                       f''

    file_contains_line_n_times(world.f_cfg.log_join('kea-legal*.txt'), MESSAGE_COUNT, request_line_pd)
    file_contains_line_n_times(world.f_cfg.log_join('kea-legal*.txt'), MESSAGE_COUNT, response_line_pd)


@pytest.mark.v6
@pytest.mark.legal_logging
def test_v6_legal_log_dual_ip():
    """
    Test checks standard formatting of legal_log hook with multiple IP addresses in one lease.
    SARR exchange is used to acquire leases.
    Log file is checked for proper content.
    """
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.log_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('preferred-lifetime', 400)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50')
    srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 94)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests(MESSAGE_COUNT, ia_pd=True)

    srv_msg.copy_remote(world.f_cfg.log_join('kea-legal*.txt'))
    file_contains_line_n_times(world.f_cfg.log_join('kea-legal*.txt'), MESSAGE_COUNT,
                               'Address: 2001:db8:1::5 has been assigned for 0 hrs 10 mins 0 secs '
                               'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 '
                               'and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')
    file_contains_line_n_times(world.f_cfg.log_join('kea-legal*.txt'), MESSAGE_COUNT,
                               'Prefix: 2001:db8:2::4:0:0/94 has been assigned for 0 hrs 10 mins 0 '
                               'secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and '
                               'hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')


@pytest.mark.v4
@pytest.mark.legal_logging
def test_v4_legal_log_assigned_address():
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.log_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', 3)
    srv_control.set_time('rebind-timer', 50)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests4(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.log_join('kea-legal*.txt'))
    file_contains_line_n_times(world.f_cfg.log_join('kea-legal*.txt'), MESSAGE_COUNT,
                               'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs '
                               'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04, '
                               'client-id: 00:01:02:03:04:05:06')


@pytest.mark.v4
@pytest.mark.legal_logging
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_v4_legal_log_assigned_address_db(backend):
    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', backend)

    misc.test_setup()
    srv_control.set_time('renew-timer', 3)
    srv_control.set_time('rebind-timer', 50)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.add_database_hook(backend)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'type', backend)
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests4(MESSAGE_COUNT)

    srv_msg.table_contains_line_n_times('logs', backend, MESSAGE_COUNT,
                                        'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs '
                                        'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04, '
                                        'client-id: 00:01:02:03:04:05:06')


@pytest.mark.v4
@pytest.mark.legal_logging
def test_v4_legal_log_assigned_address_without_client_id():
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.log_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', 3)
    srv_control.set_time('rebind-timer', 50)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests4(MESSAGE_COUNT, client_id=False)

    srv_msg.copy_remote(world.f_cfg.log_join('kea-legal*.txt'))
    file_contains_line_n_times(world.f_cfg.log_join('kea-legal*.txt'), MESSAGE_COUNT,
                               'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs '
                               'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04')
    file_contains_line_n_times(world.f_cfg.log_join('kea-legal*.txt'), 0,
                               'client-id:')


@pytest.mark.v4
@pytest.mark.legal_logging
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_v4_legal_log_assigned_address_without_client_id_db(backend):
    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', backend)

    misc.test_setup()
    srv_control.set_time('renew-timer', 3)
    srv_control.set_time('rebind-timer', 50)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.add_database_hook(backend)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'type', backend)
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests4(MESSAGE_COUNT, client_id=False)

    srv_msg.table_contains_line_n_times('logs', backend, MESSAGE_COUNT,
                                        'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs '
                                        'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04')
    srv_msg.table_contains_line_n_times('logs', backend, 0, 'client-id:')


@pytest.mark.v4
@pytest.mark.legal_logging
@pytest.mark.relay
def test_v4_legal_log_assigned_address_via_relay():
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.log_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', 3)
    srv_control.set_time('rebind-timer', 50)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests_via_relay4(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.log_join('kea-legal*.txt'))
    file_contains_line_n_times(world.f_cfg.log_join('kea-legal*.txt'), MESSAGE_COUNT,
                               'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs '
                               'to a device with hardware address: hwtype=1 ff:01:02:03:ff:05, '
                               'client-id: 00:01:02:03:04:05:77 '
                               f'connected via relay at address: {world.f_cfg.giaddr4}')


@pytest.mark.v4
@pytest.mark.legal_logging
@pytest.mark.relay
def test_v4_legal_log_assigned_address_via_relay_one_address():
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.log_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', 3)
    srv_control.set_time('rebind-timer', 50)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.2-192.168.50.2')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests_via_relay4(MESSAGE_COUNT, '192.168.50.2')

    srv_msg.copy_remote(world.f_cfg.log_join('kea-legal*.txt'))
    file_contains_line_n_times(world.f_cfg.log_join('kea-legal*.txt'), MESSAGE_COUNT,
                               'Address: 192.168.50.2 has been assigned for 0 hrs 10 mins 0 secs '
                               'to a device with hardware address: hwtype=1 ff:01:02:03:ff:05, '
                               'client-id: 00:01:02:03:04:05:77 '
                               f'connected via relay at address: {world.f_cfg.giaddr4}')


@pytest.mark.v4
@pytest.mark.legal_logging
@pytest.mark.relay
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_v4_legal_log_assigned_address_via_relay_db(backend):
    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', backend)

    misc.test_setup()
    srv_control.set_time('renew-timer', 3)
    srv_control.set_time('rebind-timer', 50)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.add_database_hook(backend)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'type', backend)
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests_via_relay4(MESSAGE_COUNT)

    srv_msg.table_contains_line_n_times('logs', backend, MESSAGE_COUNT,
                                        'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs '
                                        'to a device with hardware address: hwtype=1 ff:01:02:03:ff:05, '
                                        'client-id: 00:01:02:03:04:05:77 '
                                        f'connected via relay at address: {world.f_cfg.giaddr4}')


@pytest.mark.v4
@pytest.mark.legal_logging
def test_v4_legal_log_renew_state():
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.log_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', 3)
    srv_control.set_time('rebind-timer', 50)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests_in_renew_state4(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.log_join('kea-legal*.txt'))
    file_contains_line_n_times(world.f_cfg.log_join('kea-legal*.txt'), 2 * MESSAGE_COUNT,
                               'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs '
                               'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04, '
                               'client-id: 00:01:02:03:04:05:06')


@pytest.mark.v4
@pytest.mark.legal_logging
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_v4_legal_log_renew_state_db(backend):
    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', backend)

    misc.test_setup()
    srv_control.set_time('renew-timer', 3)
    srv_control.set_time('rebind-timer', 50)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.add_database_hook(backend)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'type', backend)
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests_in_renew_state4(MESSAGE_COUNT)

    srv_msg.table_contains_line_n_times('logs', backend, 2 * MESSAGE_COUNT,
                                        'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs '
                                        'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04, '
                                        'client-id: 00:01:02:03:04:05:06')


@pytest.mark.v4
@pytest.mark.legal_logging
def test_v4_legal_log_rebind_state():
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.log_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', 3)
    srv_control.set_time('rebind-timer', 4)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests_in_rebind_state4(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.log_join('kea-legal*.txt'))
    file_contains_line_n_times(world.f_cfg.log_join('kea-legal*.txt'), 2 * MESSAGE_COUNT,
                               'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs '
                               'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04, '
                               'client-id: 00:01:02:03:04:05:06')


@pytest.mark.v4
@pytest.mark.legal_logging
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_v4_legal_log_rebind_state_db(backend):
    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', backend)

    misc.test_setup()
    srv_control.set_time('renew-timer', 3)
    srv_control.set_time('rebind-timer', 4)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.add_database_hook(backend)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'type', backend)
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests_in_rebind_state4(MESSAGE_COUNT)

    srv_msg.table_contains_line_n_times('logs', backend, 2 * MESSAGE_COUNT,
                                        'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs '
                                        'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04, '
                                        'client-id: 00:01:02:03:04:05:06')


# v4 disabled for time saving:
# @pytest.mark.v4
@pytest.mark.v6
@pytest.mark.legal_logging
def test_legal_log_rotation(dhcp_version):
    """
    Test to check if Kea makes new log file after specific time unit.
    :param dhcp_version: The DHCP version to use.
    :type dhcp_version: str
    """
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.log_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('valid-lifetime', 600)
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50')
        srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 94)

    srv_control.add_hooks('libdhcp_legal_log.so')
    # Configure log rotation
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'time-unit', 'second')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'count', 20 if dhcp_version == 'v4' else 15)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    # log server start time
    start = datetime.now()

    # Send 3 times 3 requests waiting for log rotation interval
    if dhcp_version == 'v4':
        _send_client_requests4(3)
        _wait_till_elapsed(start, 20)
        _send_client_requests4(3)
        _wait_till_elapsed(start, 40)
        _send_client_requests4(3)
    else:
        _send_client_requests(3)
        _wait_till_elapsed(start, 15)
        _send_client_requests(3)
        _wait_till_elapsed(start, 30)
        _send_client_requests(3)

    # Wait to be sure that logs are written to file
    srv_msg.forge_sleep(2, 'seconds')

    # make a list of produced log files
    log_files = fabric_sudo_command(f"cd {world.f_cfg.log_join('')} ; ls -1 kea-legal*.txt").splitlines()

    # Check if files have 640 permissions
    for name in log_files:
        verify_file_permissions(world.f_cfg.log_join(name))

    # copy log files to forge results folder
    for name in log_files:
        srv_msg.copy_remote(world.f_cfg.log_join(name), local_filename=name)

    # Check if there are 3 log files
    assert len(log_files) == 3

    if dhcp_version == 'v4':
        log_message = 'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs ' \
                      'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04, ' \
                      'client-id: 00:01:02:03:04:05:06'
    else:
        log_message = 'Address: 2001:db8:1::5 has been assigned for 0 hrs 10 mins 0 secs ' \
                      'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 ' \
                      'and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)'

    # Check contents of the log files
    for name in log_files:
        file_contains_line_n_times(world.f_cfg.log_join(name), 3, log_message)


# v4 disabled for time saving:
# @pytest.mark.v4
@pytest.mark.v6
@pytest.mark.legal_logging
def test_legal_log_basename(dhcp_version):
    """
    Test to check if Kea makes log file with custom filename.
    :param dhcp_version: The DHCP version to use.
    :type dhcp_version: str
    """
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.log_join('custom-log*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('valid-lifetime', 600)
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50')
        srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 94)

    srv_control.add_hooks('libdhcp_legal_log.so')
    # set custom name
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'base-name', 'custom-log')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Send 3 times 3 requests waiting for log rotation interval
    if dhcp_version == 'v4':
        _send_client_requests4(3)
    else:
        _send_client_requests(3)

    if dhcp_version == 'v4':
        log_message = 'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs ' \
                      'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04, ' \
                      'client-id: 00:01:02:03:04:05:06'
    else:
        log_message = 'Address: 2001:db8:1::5 has been assigned for 0 hrs 10 mins 0 secs ' \
                      'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 ' \
                      'and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)'

    # acquire date from server
    date = fabric_sudo_command('date +"%Y%m%d"')
    # Check contents of the log files
    file_contains_line_n_times(world.f_cfg.log_join(f'custom-log.{date}.txt'), 3, log_message)
    # Check if file has 640 permissions
    verify_file_permissions(world.f_cfg.log_join(f'custom-log.{date}.txt'))


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.legal_logging
def test_legal_log_path_configfile(dhcp_version):
    """
    Test to check if Kea makes log file in custom path.
    :param dhcp_version: The DHCP version to use.
    :type dhcp_version: str
    """
    misc.test_procedure()
    illegal_paths = [
        [world.f_cfg.log_join(''), True, 'LEGAL_LOG_STORE_OPENED Legal store opened'],
        ['/tmp/', False, 'An error occurred loading the library: invalid path specified:'],
        ['~/', False, 'An error occurred loading the library: invalid path specified:'],
        ['/var/', False, 'An error occurred loading the library: invalid path specified:'],
        ['/srv/', False, 'An error occurred loading the library: invalid path specified:'],
        ['/etc/kea/', False, 'An error occurred loading the library: invalid path specified:'],
    ]

    for path, should_succeed, message in illegal_paths:
        srv_control.clear_some_data('logs')
        srv_msg.remove_file_from_server(path + 'custom-log*.txt')
        misc.test_setup()
        srv_control.set_time('renew-timer', 100)
        srv_control.set_time('rebind-timer', 200)
        srv_control.set_time('valid-lifetime', 600)
        if dhcp_version == 'v4':
            srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
        else:
            srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50')
            srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 94)

        srv_control.add_hooks('libdhcp_legal_log.so')
        # set custom name
        srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'base-name', 'custom-log')
        srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'path', path)

        srv_control.build_and_send_config_files()
        srv_control.start_srv('DHCP', 'started', should_succeed=should_succeed)

        log_contains(message)


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.legal_logging
def test_legal_log_path_config_set(dhcp_version):
    """
    Test to check if Kea makes log file in custom path.
    :param dhcp_version: The DHCP version to use.
    :type dhcp_version: str
    """

    illegal_paths = [
        ['/tmp/', 1, 'One or more hook libraries failed to load'],
        ['~/', 1, 'One or more hook libraries failed to load'],
        ['/var/', 1, 'One or more hook libraries failed to load'],
        ['/srv/', 1, 'One or more hook libraries failed to load'],
        ['/etc/kea/', 1, 'One or more hook libraries failed to load'],
    ]

    misc.test_procedure()

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('valid-lifetime', 600)
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50')
        srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 94)

    srv_control.add_hooks('libdhcp_legal_log.so')
    # set custom name
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'base-name', 'custom-log')

    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Get current config
    cmd = {"command": "config-get", "arguments": {}}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')
    config_set = response['arguments']
    del config_set['hash']

    for path, exp_result, message in illegal_paths:
        srv_msg.remove_file_from_server(path + 'custom-log*.txt')
        config_set[f"Dhcp{dhcp_version[1]}"]['hooks-libraries'][0]['parameters']['path'] = path
        cmd = {"command": "config-set", "arguments": config_set}
        resp = srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=exp_result)
        assert message in resp['text']


# v4 disabled for time saving:
# @pytest.mark.v4
@pytest.mark.v6
@pytest.mark.legal_logging
def test_legal_log_rotate_actions(dhcp_version):
    """
    Test to check if Kea makes prerotate and postrotate actions.
    :param dhcp_version: The DHCP version to use.
    :type dhcp_version: str
    """
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.log_join('kea-legal*.txt'))
    srv_msg.remove_file_from_server(world.f_cfg.scripts_join('script*.sh'))
    srv_msg.remove_file_from_server(world.f_cfg.scripts_join('actions*.txt'))

    # Prepare action scripts executed by kea to log rotation filenames
    script_pre = f'#!/bin/bash \n' \
                 f'echo $1 >> {world.f_cfg.log_join("actions_pre.txt")}'
    script_post = f'#!/bin/bash \n' \
                  f'echo $1 >> {world.f_cfg.log_join("actions_post.txt")}'

    # transfer scripts to server and make them executable
    fabric_sudo_command(f"echo '{script_pre}' > {world.f_cfg.scripts_join('script_pre.sh')}")
    fabric_sudo_command(f"echo '{script_post}' > {world.f_cfg.scripts_join('script_post.sh')}")
    fabric_sudo_command(f"chmod +x {world.f_cfg.scripts_join('script*.sh')}")

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('valid-lifetime', 600)
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50')
        srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 94)

    srv_control.add_hooks('libdhcp_legal_log.so')
    # Configure log rotation
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'time-unit', 'second')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'count', 20 if dhcp_version == 'v4' else 15)

    # Configure log rotation actions
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'prerotate', world.f_cfg.scripts_join('script_pre.sh'))
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'postrotate', world.f_cfg.scripts_join('script_post.sh'))

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    # log server start time
    start = datetime.now()

    # Send 3 times 3 requests waiting for log rotation interval
    if dhcp_version == 'v4':
        _send_client_requests4(3)
        _wait_till_elapsed(start, 20)
        _send_client_requests4(3)
        _wait_till_elapsed(start, 40)
        _send_client_requests4(3)
    else:
        _send_client_requests(3)
        _wait_till_elapsed(start, 15)
        _send_client_requests(3)
        _wait_till_elapsed(start, 30)
        _send_client_requests(3)

    # Wait to be sure that logs are written to file
    srv_msg.forge_sleep(2, 'seconds')
    # make a list of produced log files
    log_files = fabric_sudo_command(f"cd {world.f_cfg.log_join('')} ; ls -1 kea-legal*.txt").splitlines()

    # copy log files to forge results folder
    for name in log_files:
        srv_msg.copy_remote(world.f_cfg.log_join(name), local_filename=name)
        verify_file_permissions(world.f_cfg.log_join(name))
    srv_msg.copy_remote(world.f_cfg.log_join("actions_pre.txt"), local_filename="actions_pre.txt")
    srv_msg.copy_remote(world.f_cfg.log_join("actions_post.txt"), local_filename="actions_post.txt")

    # Check if there are 3 log files
    assert len(log_files) == 3

    # Check contents of prerotate actions file. It should contain first and second log file name (third was not closed)
    file_contains_line_n_times(world.f_cfg.log_join('actions_pre.txt'), 1, world.f_cfg.log_join(log_files[0]))
    file_contains_line_n_times(world.f_cfg.log_join('actions_pre.txt'), 1, world.f_cfg.log_join(log_files[1]))

    # Check contents of postrotate actions file. It should contain second and third log file name
    # (first was open on server start, and not on rotation)
    file_contains_line_n_times(world.f_cfg.log_join('actions_post.txt'), 1, world.f_cfg.log_join(log_files[1]))
    file_contains_line_n_times(world.f_cfg.log_join('actions_post.txt'), 1, world.f_cfg.log_join(log_files[2]))


# v4 disabled for time saving:
# @pytest.mark.v4
@pytest.mark.v6
@pytest.mark.legal_logging
@pytest.mark.parametrize('facility', ['undefined', 'local0', 'local1', 'local2'])
def test_legal_log_syslog(dhcp_version, facility):
    """
    Test legal log using diferent syslog facilities.
    The test is parametrized to test with different syslog facilities.
    :param dhcp_version: The DHCP version to use.
    :type dhcp_version: str
    :param facility: The syslog facility to use.
    :type facility: str
    """
    misc.test_procedure()
    srv_control.clear_some_data('logs', force_syslog=True)

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('valid-lifetime', 600)
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50')
        srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 94)

    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'type', 'syslog')
    if facility != 'undefined':
        srv_control.add_parameter_to_hook("libdhcp_legal_log.so", 'facility', facility)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    if dhcp_version == 'v4':
        _send_client_requests4(3)
    else:
        _send_client_requests(3)

    if dhcp_version == 'v4':
        log_message = 'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs ' \
                      'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04, ' \
                      'client-id: 00:01:02:03:04:05:06'
    else:
        log_message = 'Address: 2001:db8:1::5 has been assigned for 0 hrs 10 mins 0 secs ' \
                      'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 ' \
                      'and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)'

    facility = 'syslog:' + facility if facility != 'undefined' else 'syslog:local0'
    wrong_facility = facility.replace(facility[-1], str(int(facility[-1])+1))
    log_contains_n_times(log_message, 3, facility)

    log_doesnt_contain(log_message, wrong_facility)

    # Forge does not archive journal logs by default, so we need to get them manually
    _get_journal_logs(facility)
