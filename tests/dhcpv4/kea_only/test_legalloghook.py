"""Kea6 legal logging"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_msg
import misc
import srv_control
from forge_cfg import world


# number of messages that the client will send in each test
MESSAGE_COUNT = 3


def _send_client_requests(count, client_id=True):
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


def _send_client_requests_via_relay(count):
    for _ in range(count):
        misc.test_procedure()
        srv_msg.client_does_include_with_value('client_id', '00010203040577')
        srv_msg.network_variable('source_port', 67)
        srv_msg.network_variable('source_address', '$(GIADDR4)')
        srv_msg.network_variable('destination_address', '$(SRV4_ADDR)')
        srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
        srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
        srv_msg.client_sets_value('Client', 'hops', 1)
        srv_msg.client_requests_option(1)
        srv_msg.client_send_msg('DISCOVER')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'OFFER')
        srv_msg.response_check_include_option(1)
        srv_msg.response_check_content('yiaddr', '192.168.50.1')
        srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
        srv_msg.client_does_include_with_value('client_id', '00010203040577')
        srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
        srv_msg.client_sets_value('Client', 'hops', 1)
        srv_msg.client_copy_option('server_id')
        srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
        srv_msg.client_requests_option(1)
        srv_msg.client_send_msg('REQUEST')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'ACK')
        srv_msg.response_check_content('yiaddr', '192.168.50.1')
        srv_msg.response_check_include_option(1)
        srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


def _send_client_requests_in_renew_state(count):
    _send_client_requests(count)

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


def _send_client_requests_in_rebind_state(count):
    _send_client_requests(count)

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


@pytest.mark.v4
@pytest.mark.kea_only
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

    _send_client_requests(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), MESSAGE_COUNT,
                                       'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs '
                                       'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04, '
                                       'client-id: 00:01:02:03:04:05:06')


@pytest.mark.v4
@pytest.mark.kea_only
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

    _send_client_requests(MESSAGE_COUNT)

    srv_msg.table_contains_line_n_times('logs', backend, MESSAGE_COUNT,
                                        'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs '
                                        'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04, '
                                        'client-id: 00:01:02:03:04:05:06')


@pytest.mark.v4
@pytest.mark.kea_only
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

    _send_client_requests(MESSAGE_COUNT, client_id=False)

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), MESSAGE_COUNT,
                                       'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs '
                                       'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04')
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), 0,
                                       'client-id:')


@pytest.mark.v4
@pytest.mark.kea_only
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

    _send_client_requests(MESSAGE_COUNT, client_id=False)

    srv_msg.table_contains_line_n_times('logs', backend, MESSAGE_COUNT,
                                        'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs '
                                        'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04')
    srv_msg.table_contains_line_n_times('logs', backend, 0, 'client-id:')


@pytest.mark.v4
@pytest.mark.kea_only
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

    _send_client_requests_via_relay(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), MESSAGE_COUNT,
                                       'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs '
                                       'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04, '
                                       'client-id: 00:01:02:03:04:05:06 '
                                       'connected via relay at address: $(GIADDR4)')


@pytest.mark.v4
@pytest.mark.kea_only
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

    _send_client_requests_via_relay(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), MESSAGE_COUNT,
                                       'Address: 192.168.50.2 has been assigned for 0 hrs 10 mins 0 secs '
                                       'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04, '
                                       'client-id: 00:01:02:03:04:05:06 '
                                       'connected via relay at address: $(GIADDR4)')


@pytest.mark.v4
@pytest.mark.kea_only
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

    _send_client_requests_via_relay(MESSAGE_COUNT)

    srv_msg.table_contains_line_n_times('logs', backend, MESSAGE_COUNT,
                                        'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs '
                                        'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04, '
                                        'client-id: 00:01:02:03:04:05:06 '
                                        'connected via relay at address: $(GIADDR4)')


@pytest.mark.v4
@pytest.mark.kea_only
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

    _send_client_requests_in_renew_state(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), 2 * MESSAGE_COUNT,
                                       'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs '
                                       'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04, '
                                       'client-id: 00:01:02:03:04:05:06')


@pytest.mark.v4
@pytest.mark.kea_only
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

    _send_client_requests_in_renew_state(MESSAGE_COUNT)

    srv_msg.table_contains_line_n_times('logs', backend, 2 * MESSAGE_COUNT,
                                        'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs '
                                        'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04, '
                                        'client-id: 00:01:02:03:04:05:06')


@pytest.mark.v4
@pytest.mark.kea_only
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

    _send_client_requests_in_rebind_state(MESSAGE_COUNT)

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line_n_times(world.f_cfg.data_join('kea-legal*.txt'), 2 * MESSAGE_COUNT,
                                       'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs '
                                       'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04, '
                                       'client-id: 00:01:02:03:04:05:06')


@pytest.mark.v4
@pytest.mark.kea_only
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

    _send_client_requests_in_rebind_state(MESSAGE_COUNT)

    srv_msg.table_contains_line_n_times('logs', backend, 2 * MESSAGE_COUNT,
                                        'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs '
                                        'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04, '
                                        'client-id: 00:01:02:03:04:05:06')
