"""Kea6 Legal logging hook"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_control
import srv_msg
from forge_cfg import world


# number of messages that the client will send in each test
MESSAGE_COUNT = 3


def _send_client_requests(count):
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
        srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
        srv_msg.client_copy_option('server-id')
        srv_msg.client_copy_option('IA_NA')
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
        srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::1005')
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
        srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8::f')

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


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v6_legal_log_address_assigned_duid():
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('preferred-lifetime', 400)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::5-2001:db8::50')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 94)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), MESSAGE_COUNT,
                                       'Address: 2001:db8::5 has been assigned for 0 hrs 10 mins 0 secs '
                                       'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 '
                                       'and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.legal_logging
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_v6_legal_log_address_assigned_duid_db(backend):
    srv_msg.remove_from_db_table('logs', backend)

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('preferred-lifetime', 400)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::5-2001:db8::50')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 94)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook(1, 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook(1, 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook(1, 'type', backend)
    srv_control.add_parameter_to_hook(1, 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests(MESSAGE_COUNT)

    srv_msg.table_contains_line_n_times('logs', backend, MESSAGE_COUNT,
                                        'Address: 2001:db8::5 has been assigned for 0 hrs 10 mins 0 secs '
                                        'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 '
                                        'and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v6_legal_log_address_renewed_duid():
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('preferred-lifetime', 400)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::5-2001:db8::50')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 94)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests(MESSAGE_COUNT)

    _send_client_renews(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), 2 * MESSAGE_COUNT,
                                       'Address: 2001:db8::5 has been assigned for 0 hrs 10 mins 0 secs '
                                       'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 '
                                       'and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')


@pytest.mark.v6
@pytest.mark.kea_only
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
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::5-2001:db8::50')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 94)
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
                                        'Address: 2001:db8::5 has been assigned for 0 hrs 10 mins 0 secs '
                                        'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 '
                                        'and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v6_legal_log_address_rebind_duid():
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('preferred-lifetime', 400)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::5-2001:db8::50')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 94)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests(MESSAGE_COUNT)

    _send_client_rebinds(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), 2 * MESSAGE_COUNT,
                                       'Address: 2001:db8::5 has been assigned for 0 hrs 10 mins 0 secs '
                                       'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 '
                                       'and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')


@pytest.mark.v6
@pytest.mark.kea_only
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
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::5-2001:db8::50')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 94)
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
                                        'Address: 2001:db8::5 has been assigned for 0 hrs 10 mins 0 secs '
                                        'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 '
                                        'and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v6_legal_log_address_assigned_docsis_modem():
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('preferred-lifetime', 400)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::5-2001:db8::50')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 94)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_line({"mac-sources": ["docsis-modem"]})
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_client_requests_with_docsis(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), MESSAGE_COUNT,
                                       'Address: 2001:db8::5 has been assigned for 0 hrs 10 mins 0 secs '
                                       'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 '
                                       'and hardware address: hwtype=1 f6:f5:f4:f3:f2:01 (from DOCSIS MODEM)')


@pytest.mark.v6
@pytest.mark.kea_only
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
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::5-2001:db8::50')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 94)
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
                                        'Address: 2001:db8::5 has been assigned for 0 hrs 10 mins 0 secs '
                                        'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and '
                                        'hardware address: hwtype=1 f6:f5:f4:f3:f2:01 (from DOCSIS MODEM)')


@pytest.mark.v6
@pytest.mark.kea_only
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
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::5-2001:db8::50')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 94)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_line({"mac-sources": ["docsis-cmts"]})
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_relayed_client_requests_with_docsis(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), MESSAGE_COUNT,
                                       'Address: 2001:db8::5 has been assigned for 0 hrs 10 mins 0 secs '
                                       'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:01 '
                                       'and hardware address: hwtype=1 00:f5:f4:00:f2:01 (from DOCSIS CMTS)')


@pytest.mark.v6
@pytest.mark.kea_only
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
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::5-2001:db8::50')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 94)
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
                                        'Address: 2001:db8::5 has been assigned for 0 hrs 10 mins 0 secs '
                                        'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:01 '
                                        'and hardware address: hwtype=1 00:f5:f4:00:f2:01 (from DOCSIS CMTS)')


@pytest.mark.v6
@pytest.mark.kea_only
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
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::5-2001:db8::50')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 94)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_relayed_client_requests(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), MESSAGE_COUNT,
                                       'Address: 2001:db8::5 has been assigned for 0 hrs 10 mins 0 secs '
                                       'to a device with DUID: 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01 '
                                       'and hardware address: hwtype=1 f6:f5:f4:f3:f2:01 (from DUID) '
                                       'connected via relay at address:')
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), MESSAGE_COUNT,
                                       'for client on link address: 2001:db8::1005, hop count: 4')


@pytest.mark.v6
@pytest.mark.kea_only
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
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::5-2001:db8::50')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 94)
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook(1, 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook(1, 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook(1, 'type', backend)
    srv_control.add_parameter_to_hook(1, 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _send_relayed_client_requests(MESSAGE_COUNT)

    srv_msg.table_contains_line_n_times('logs', backend, MESSAGE_COUNT,
                                        'Address: 2001:db8::5 has been assigned for 0 hrs 10 mins 0 secs '
                                        'to a device with DUID: 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01 '
                                        'and hardware address: hwtype=1 f6:f5:f4:f3:f2:01 (from DUID) '
                                        'connected via relay at address:')
    srv_msg.table_contains_line_n_times('logs', backend, MESSAGE_COUNT,
                                        'for client on link address: 2001:db8::1005, hop count: 4')


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v6_legal_log_with_flex_id_address_assigned():
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('preferred-lifetime', 400)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::5-2001:db8::50')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           0,
                                           'flex-id',
                                           '01:02:03:04:05:06')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '2001:db8::f')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 94)
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
                                       'Address: 2001:db8::f has been assigned for 0 hrs 10 mins 0 secs '
                                       'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 '
                                       'and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.legal_logging
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_v6_legal_log_with_flex_id_address_assigned_db(backend):
    srv_msg.remove_from_db_table('logs', backend)

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('preferred-lifetime', 400)
    srv_control.set_time('valid-lifetime', 600)
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::5-2001:db8::50')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           0,
                                           'flex-id',
                                           '01:02:03:04:05:06')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '2001:db8::f')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 94)
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
                                        'Address: 2001:db8::f has been assigned for 0 hrs 10 mins 0 secs '
                                        'to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 '
                                        'and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')
