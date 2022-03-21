"""Kea6 Legal logging hook"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_control
import srv_msg
from forge_cfg import world


# number of messages that the client will send in each test
MESSAGE_COUNT = 3


def _send_client_requests(count, ia_pd=False):
    for _ in range(count):
        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
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
        srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
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


def _send_client_renews(count):
    for _ in range(count):
        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
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


def _send_client_rebinds(count):
    for _ in range(count):
        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
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


@pytest.mark.v6
@pytest.mark.legal_logging
def test_v6_legal_log_address_assigned_duid():
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

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

    _send_client_requests(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), MESSAGE_COUNT,
                                       'Address: 2001:db8:1::5 has been assigned for 0 hrs 10 mins 0 secs '
                                       'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 '
                                       'and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')


@pytest.mark.v6
@pytest.mark.legal_logging
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_v6_legal_log_address_assigned_duid_db(backend):
    srv_msg.remove_from_db_table('logs', backend)

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('preferred-lifetime', 400)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50')
    srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 94)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook(1, 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook(1, 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook(1, 'type', backend)
    srv_control.add_parameter_to_hook(1, 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests(MESSAGE_COUNT)

    srv_msg.table_contains_line_n_times('logs', backend, MESSAGE_COUNT,
                                        'Address: 2001:db8:1::5 has been assigned for 0 hrs 10 mins 0 secs '
                                        'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 '
                                        'and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')


@pytest.mark.v6
@pytest.mark.legal_logging
def test_v6_legal_log_address_renewed_duid():
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

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

    _send_client_requests(MESSAGE_COUNT)

    _send_client_renews(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), 2 * MESSAGE_COUNT,
                                       'Address: 2001:db8:1::5 has been assigned for 0 hrs 10 mins 0 secs '
                                       'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 '
                                       'and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')


@pytest.mark.v6
@pytest.mark.legal_logging
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_v6_legal_log_address_renewed_duid_db(backend):
    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', backend)

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('preferred-lifetime', 400)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50')
    srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 94)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook(1, 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook(1, 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook(1, 'type', backend)
    srv_control.add_parameter_to_hook(1, 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests(MESSAGE_COUNT)

    _send_client_renews(MESSAGE_COUNT)

    srv_msg.table_contains_line_n_times('logs', backend, 2 * MESSAGE_COUNT,
                                        'Address: 2001:db8:1::5 has been assigned for 0 hrs 10 mins 0 secs '
                                        'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 '
                                        'and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')


@pytest.mark.v6
@pytest.mark.legal_logging
def test_v6_legal_log_address_rebind_duid():
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

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

    _send_client_requests(MESSAGE_COUNT)

    _send_client_rebinds(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), 2 * MESSAGE_COUNT,
                                       'Address: 2001:db8:1::5 has been assigned for 0 hrs 10 mins 0 secs '
                                       'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 '
                                       'and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')


@pytest.mark.v6
@pytest.mark.legal_logging
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_v6_legal_log_address_rebind_duid_db(backend):
    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', backend)

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('preferred-lifetime', 400)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50')
    srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 94)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook(1, 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook(1, 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook(1, 'type', backend)
    srv_control.add_parameter_to_hook(1, 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests(MESSAGE_COUNT)

    _send_client_rebinds(MESSAGE_COUNT)

    srv_msg.table_contains_line_n_times('logs', backend, 2 * MESSAGE_COUNT,
                                        'Address: 2001:db8:1::5 has been assigned for 0 hrs 10 mins 0 secs '
                                        'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 '
                                        'and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')


@pytest.mark.v6
@pytest.mark.legal_logging
def test_v6_legal_log_address_assigned_docsis_modem():
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

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

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), MESSAGE_COUNT,
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
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook(1, 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook(1, 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook(1, 'type', backend)
    srv_control.add_parameter_to_hook(1, 'user', '$(DB_USER)')
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
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

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

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), MESSAGE_COUNT,
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
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook(1, 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook(1, 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook(1, 'type', backend)
    srv_control.add_parameter_to_hook(1, 'user', '$(DB_USER)')
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
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

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

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), MESSAGE_COUNT,
                                       'Address: 2001:db8:1::5 has been assigned for 0 hrs 10 mins 0 secs '
                                       'to a device with DUID: 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01 '
                                       'and hardware address: hwtype=1 f6:f5:f4:f3:f2:01 (from DUID) '
                                       'connected via relay at address:')
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), MESSAGE_COUNT,
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
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook(1, 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook(1, 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook(1, 'type', backend)
    srv_control.add_parameter_to_hook(1, 'user', '$(DB_USER)')
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
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

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
    srv_control.add_parameter_to_hook(2,
                                      'identifier-expression',
                                      'vendor[4491].option[1026].hex')
    srv_control.add_line({"host-reservation-identifiers": ["duid", "flex-id"]})
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests_for_flex_id(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), MESSAGE_COUNT,
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
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook(1, 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook(1, 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook(1, 'type', backend)
    srv_control.add_parameter_to_hook(1, 'user', '$(DB_USER)')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(2,
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
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

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
    srv_control.add_parameter_to_hook(1, "request-parser-format", request_format)
    response_format = "pkt.iface +" \
                      "addrtotext(pkt.src) +" \
                      "addrtotext(pkt.dst) +" \
                      "int32totext(pkt.len) +" \
                      "int32totext(pkt6.msgtype) +" \
                      "int32totext(pkt6.msgtype) +" \
                      "int32totext(pkt6.transid) +" \
                      "addrtotext(relay6[0].linkaddr)"
    srv_control.add_parameter_to_hook(1, "response-parser-format", response_format)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
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

    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), MESSAGE_COUNT, request_line)
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), MESSAGE_COUNT, response_line)


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
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

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
    srv_control.add_parameter_to_hook(1, "request-parser-format", request_format)
    response_format = "pkt.iface +" \
                      "addrtotext(pkt.src) +" \
                      "addrtotext(pkt.dst) +" \
                      "int32totext(pkt.len) +" \
                      "int32totext(pkt6.msgtype) +" \
                      "int32totext(pkt6.msgtype) +" \
                      "int32totext(pkt6.transid) +" \
                      "addrtotext(relay6[0].linkaddr) + " \
                      "addrtotext(relay6[0].peeraddr)"
    srv_control.add_parameter_to_hook(1, "response-parser-format", response_format)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_relayed_client_requests(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
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

    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), MESSAGE_COUNT, request_line)
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), MESSAGE_COUNT, response_line)


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
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

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
    srv_control.add_parameter_to_hook(1, "request-parser-format", request_format)
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
    srv_control.add_parameter_to_hook(1, "response-parser-format", response_format)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests(MESSAGE_COUNT, ia_pd=True)

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
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

    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), MESSAGE_COUNT, request_line_na)
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), MESSAGE_COUNT, response_line_na)

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

    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), MESSAGE_COUNT, request_line_pd)
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), MESSAGE_COUNT, response_line_pd)


@pytest.mark.v6
@pytest.mark.legal_logging
def test_v6_legal_log_dual_ip():
    """
    Test checks standart formatting of "legal_log" hook with multiple ip addresses in one lease.
    SARR exchange is used to acquire leases.
    Log file is checked for proper content.
    """
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

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

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), MESSAGE_COUNT,
                                       'Address: 2001:db8:1::5 has been assigned for 0 hrs 10 mins 0 secs '
                                       'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 '
                                       'and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), MESSAGE_COUNT,
                                       'Prefix: 2001:db8:2::4:0:0/94 has been assigned for 0 hrs 10 mins 0 '
                                       'secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and '
                                       'hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')


@pytest.mark.v4
@pytest.mark.legal_logging
def test_v4_legal_log_assigned_address():
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', 3)
    srv_control.set_time('rebind-timer', 50)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests4(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), MESSAGE_COUNT,
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
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook(1, 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook(1, 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook(1, 'type', backend)
    srv_control.add_parameter_to_hook(1, 'user', '$(DB_USER)')
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
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', 3)
    srv_control.set_time('rebind-timer', 50)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests4(MESSAGE_COUNT, client_id=False)

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), MESSAGE_COUNT,
                                       'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs '
                                       'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04')
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), 0,
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
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook(1, 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook(1, 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook(1, 'type', backend)
    srv_control.add_parameter_to_hook(1, 'user', '$(DB_USER)')
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
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', 3)
    srv_control.set_time('rebind-timer', 50)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests_via_relay4(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), MESSAGE_COUNT,
                                       'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs '
                                       'to a device with hardware address: hwtype=1 ff:01:02:03:ff:05, '
                                       'client-id: 00:01:02:03:04:05:77 '
                                       'connected via relay at address: $(GIADDR4)')


@pytest.mark.v4
@pytest.mark.legal_logging
@pytest.mark.relay
def test_v4_legal_log_assigned_address_via_relay_one_address():
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', 3)
    srv_control.set_time('rebind-timer', 50)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.2-192.168.50.2')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests_via_relay4(MESSAGE_COUNT, '192.168.50.2')

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), MESSAGE_COUNT,
                                       'Address: 192.168.50.2 has been assigned for 0 hrs 10 mins 0 secs '
                                       'to a device with hardware address: hwtype=1 ff:01:02:03:ff:05, '
                                       'client-id: 00:01:02:03:04:05:77 '
                                       'connected via relay at address: $(GIADDR4)')


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
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook(1, 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook(1, 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook(1, 'type', backend)
    srv_control.add_parameter_to_hook(1, 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests_via_relay4(MESSAGE_COUNT)

    srv_msg.table_contains_line_n_times('logs', backend, MESSAGE_COUNT,
                                        'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs '
                                        'to a device with hardware address: hwtype=1 ff:01:02:03:ff:05, '
                                        'client-id: 00:01:02:03:04:05:77 '
                                        'connected via relay at address: $(GIADDR4)')


@pytest.mark.v4
@pytest.mark.legal_logging
def test_v4_legal_log_renew_state():
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', 3)
    srv_control.set_time('rebind-timer', 50)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests_in_renew_state4(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), 2 * MESSAGE_COUNT,
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
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook(1, 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook(1, 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook(1, 'type', backend)
    srv_control.add_parameter_to_hook(1, 'user', '$(DB_USER)')
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
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', 3)
    srv_control.set_time('rebind-timer', 4)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests_in_rebind_state4(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), 2 * MESSAGE_COUNT,
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
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook(1, 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook(1, 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook(1, 'type', backend)
    srv_control.add_parameter_to_hook(1, 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests_in_rebind_state4(MESSAGE_COUNT)

    srv_msg.table_contains_line_n_times('logs', backend, 2 * MESSAGE_COUNT,
                                        'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs '
                                        'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04, '
                                        'client-id: 00:01:02:03:04:05:06')
