"""Kea6 legal logging"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_msg
import misc
import srv_control
from forge_cfg import world


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_assigned_address():
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', '3')
    srv_control.set_time('rebind-timer', '50')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_include_option('Response', None, '61')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '61', None, 'value', '00010203040506')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_include_option('Response', None, '61')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '61', None, 'value', '00010203040506')

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line(world.f_cfg.data_join('kea-legal*.txt'),
                               None,
                               'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs')
    srv_msg.file_contains_line(world.f_cfg.data_join('kea-legal*.txt'),
                               None,
                               'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04, client-id: 00:01:02:03:04:05:06')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_assigned_address_pgsql():
    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', 'PostgreSQL')

    misc.test_setup()
    srv_control.set_time('renew-timer', '3')
    srv_control.set_time('rebind-timer', '50')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook('1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook('1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook('1', 'type', 'postgresql')
    srv_control.add_parameter_to_hook('1', 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_include_option('Response', None, '61')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '61', None, 'value', '00010203040506')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_include_option('Response', None, '61')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '61', None, 'value', '00010203040506')

    srv_msg.table_contains_line('logs',
                                'PostgreSQL',
                                None,
                                'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs')
    srv_msg.table_contains_line('logs',
                                'PostgreSQL',
                                None,
                                'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04, client-id: 00:01:02:03:04:05:06')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_assigned_address_mysql():
    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', 'MySQL')

    misc.test_setup()
    srv_control.set_time('renew-timer', '3')
    srv_control.set_time('rebind-timer', '50')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook('1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook('1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook('1', 'type', 'mysql')
    srv_control.add_parameter_to_hook('1', 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_include_option('Response', None, '61')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '61', None, 'value', '00010203040506')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_include_option('Response', None, '61')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '61', None, 'value', '00010203040506')

    srv_msg.table_contains_line('logs',
                                'MySQL',
                                None,
                                'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs')
    srv_msg.table_contains_line('logs',
                                'MySQL',
                                None,
                                'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04, client-id: 00:01:02:03:04:05:06')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_assigned_address_without_client_id():
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', '3')
    srv_control.set_time('rebind-timer', '50')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line(world.f_cfg.data_join('kea-legal*.txt'),
                               None,
                               'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs')
    srv_msg.file_contains_line(world.f_cfg.data_join('kea-legal*.txt'),
                               None,
                               'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04')
    srv_msg.file_contains_line(world.f_cfg.data_join('kea-legal*.txt'),
                               'NOT ',
                               'client-id:')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_assigned_address_without_client_id_pgsql():
    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', 'PostgreSQL')

    misc.test_setup()
    srv_control.set_time('renew-timer', '3')
    srv_control.set_time('rebind-timer', '50')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook('1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook('1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook('1', 'type', 'postgresql')
    srv_control.add_parameter_to_hook('1', 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    srv_msg.table_contains_line('logs',
                                'PostgreSQL',
                                None,
                                'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs')
    srv_msg.table_contains_line('logs',
                                'PostgreSQL',
                                None,
                                'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04')
    srv_msg.table_contains_line('logs', 'PostgreSQL', 'NOT ', 'client-id:')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_assigned_address_without_client_id_mysql():
    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', 'MySQL')

    misc.test_setup()
    srv_control.set_time('renew-timer', '3')
    srv_control.set_time('rebind-timer', '50')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook('1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook('1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook('1', 'type', 'mysql')
    srv_control.add_parameter_to_hook('1', 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    srv_msg.table_contains_line('logs',
                                'MySQL',
                                None,
                                'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs')
    srv_msg.table_contains_line('logs',
                                'MySQL',
                                None,
                                'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04')
    srv_msg.table_contains_line('logs', 'MySQL', 'NOT ', 'client-id:')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_assigned_address_via_relay_pgsql_1():
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', '3')
    srv_control.set_time('rebind-timer', '50')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.2-192.168.50.2')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '00010203040577')
    srv_msg.network_variable('source_port', '67')
    srv_msg.network_variable('source_address', '$(GIADDR4)')
    srv_msg.network_variable('destination_address', '$(SRV4_ADDR)')
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.2')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040577')
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.2')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.2')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))

    srv_msg.file_contains_line(world.f_cfg.data_join('kea-legal*.txt'),
                               None,
                               'Address: 192.168.50.2 has been assigned for 0 hrs 10 mins 0 secs to a device with hardware address: hwtype=1 00:00:00:00:00:00,')
    srv_msg.file_contains_line(world.f_cfg.data_join('kea-legal*.txt'),
                               None,
                               'client-id: 00:01:02:03:04:05:77 connected via relay at address: $(GIADDR4)')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_assigned_address_via_relay_pgsql_2():
    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', 'PostgreSQL')

    misc.test_setup()
    srv_control.set_time('renew-timer', '3')
    srv_control.set_time('rebind-timer', '50')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.2-192.168.50.2')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook('1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook('1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook('1', 'type', 'postgresql')
    srv_control.add_parameter_to_hook('1', 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '00010203040577')
    srv_msg.network_variable('source_port', '67')
    srv_msg.network_variable('source_address', '$(GIADDR4)')
    srv_msg.network_variable('destination_address', '$(SRV4_ADDR)')
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.2')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040577')
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.2')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.2')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    srv_msg.table_contains_line('logs',
                                'PostgreSQL',
                                None,
                                'Address: 192.168.50.2 has been assigned for 0 hrs 10 mins 0 secs to a device with hardware address: hwtype=1 00:00:00:00:00:00,')
    srv_msg.table_contains_line('logs',
                                'PostgreSQL',
                                None,
                                'client-id: 00:01:02:03:04:05:77 connected via relay at address: $(GIADDR4)')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_assigned_address_via_relay_mysql():
    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', 'MySQL')

    misc.test_setup()
    srv_control.set_time('renew-timer', '3')
    srv_control.set_time('rebind-timer', '50')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.2-192.168.50.2')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook('1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook('1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook('1', 'type', 'mysql')
    srv_control.add_parameter_to_hook('1', 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '00010203040577')
    srv_msg.network_variable('source_port', '67')
    srv_msg.network_variable('source_address', '$(GIADDR4)')
    srv_msg.network_variable('destination_address', '$(SRV4_ADDR)')
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.2')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040577')
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.2')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.2')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    srv_msg.table_contains_line('logs',
                                'MySQL',
                                None,
                                'Address: 192.168.50.2 has been assigned for 0 hrs 10 mins 0 secs to a device with hardware address: hwtype=1 00:00:00:00:00:00,')
    srv_msg.table_contains_line('logs',
                                'MySQL',
                                None,
                                'client-id: 00:01:02:03:04:05:77 connected via relay at address: $(GIADDR4)')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_renewed_address():
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', '3')
    srv_control.set_time('rebind-timer', '50')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.network_variable('source_port', '67')
    srv_msg.network_variable('source_address', '$(GIADDR4)')
    srv_msg.network_variable('destination_address', '$(SRV4_ADDR)')
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    # make sure that T1 time expires and client will be in RENEWING state.
    srv_msg.forge_sleep('3', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line(world.f_cfg.data_join('kea-legal*.txt'),
                               None,
                               'Address: 192.168.50.1 has been renewed for 0 hrs 10 mins 0 secs')
    srv_msg.file_contains_line(world.f_cfg.data_join('kea-legal*.txt'),
                               None,
                               'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04 connected via relay at address: $(GIADDR4)')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_renewed_address_pgsql():
    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', 'PostgreSQL')

    misc.test_setup()
    srv_control.set_time('renew-timer', '3')
    srv_control.set_time('rebind-timer', '50')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook('1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook('1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook('1', 'type', 'postgresql')
    srv_control.add_parameter_to_hook('1', 'user', '$(DB_USER)')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.network_variable('source_port', '67')
    srv_msg.network_variable('source_address', '$(GIADDR4)')
    srv_msg.network_variable('destination_address', '$(SRV4_ADDR)')
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    # make sure that T1 time expires and client will be in RENEWING state.
    srv_msg.forge_sleep('3', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    srv_msg.table_contains_line('logs',
                                'PostgreSQL',
                                None,
                                'ddress: 192.168.50.1 has been renewed for 0 hrs 10 mins 0 secs')
    srv_msg.table_contains_line('logs',
                                'PostgreSQL',
                                None,
                                'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04 connected via relay at address: $(GIADDR4)')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_renewed_address_mysql():
    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', 'MySQL')

    misc.test_setup()
    srv_control.set_time('renew-timer', '3')
    srv_control.set_time('rebind-timer', '50')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook('1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook('1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook('1', 'type', 'mysql')
    srv_control.add_parameter_to_hook('1', 'user', '$(DB_USER)')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.network_variable('source_port', '67')
    srv_msg.network_variable('source_address', '$(GIADDR4)')
    srv_msg.network_variable('destination_address', '$(SRV4_ADDR)')
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    # make sure that T1 time expires and client will be in RENEWING state.
    srv_msg.forge_sleep('3', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    srv_msg.table_contains_line('logs',
                                'MySQL',
                                None,
                                'ddress: 192.168.50.1 has been renewed for 0 hrs 10 mins 0 secs')
    srv_msg.table_contains_line('logs',
                                'MySQL',
                                None,
                                'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04 connected via relay at address: $(GIADDR4)')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_rebind_address():
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', '3')
    srv_control.set_time('rebind-timer', '4')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.network_variable('source_port', '67')
    srv_msg.network_variable('source_address', '$(GIADDR4)')
    srv_msg.network_variable('destination_address', '$(SRV4_ADDR)')
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    # make sure that T2 time expires and client will be in REBIND state.
    srv_msg.forge_sleep('5', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line(world.f_cfg.data_join('kea-legal*.txt'),
                               None,
                               'Address: 192.168.50.1 has been renewed for 0 hrs 10 mins 0 secs')
    srv_msg.file_contains_line(world.f_cfg.data_join('kea-legal*.txt'),
                               None,
                               'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04 connected via relay at address: $(GIADDR4)')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_rebind_address_mysql():
    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', 'MySQL')

    misc.test_setup()
    srv_control.set_time('renew-timer', '3')
    srv_control.set_time('rebind-timer', '4')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook('1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook('1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook('1', 'type', 'mysql')
    srv_control.add_parameter_to_hook('1', 'user', '$(DB_USER)')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.network_variable('source_port', '67')
    srv_msg.network_variable('source_address', '$(GIADDR4)')
    srv_msg.network_variable('destination_address', '$(SRV4_ADDR)')
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    # make sure that T2 time expires and client will be in REBIND state.
    srv_msg.forge_sleep('5', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    srv_msg.table_contains_line('logs',
                                'MySQL',
                                None,
                                'Address: 192.168.50.1 has been renewed for 0 hrs 10 mins 0 secs')
    srv_msg.table_contains_line('logs',
                                'MySQL',
                                None,
                                'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04 connected via relay at address: $(GIADDR4)')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_rebind_address_pgsql():
    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', 'PostgreSQL')

    misc.test_setup()
    srv_control.set_time('renew-timer', '3')
    srv_control.set_time('rebind-timer', '4')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook('1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook('1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook('1', 'type', 'postgresql')
    srv_control.add_parameter_to_hook('1', 'user', '$(DB_USER)')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.network_variable('source_port', '67')
    srv_msg.network_variable('source_address', '$(GIADDR4)')
    srv_msg.network_variable('destination_address', '$(SRV4_ADDR)')
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    # make sure that T2 time expires and client will be in REBIND state.
    srv_msg.forge_sleep('5', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    srv_msg.table_contains_line('logs',
                                'PostgreSQL',
                                None,
                                'Address: 192.168.50.1 has been renewed for 0 hrs 10 mins 0 secs')
    srv_msg.table_contains_line('logs',
                                'PostgreSQL',
                                None,
                                'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04 connected via relay at address: $(GIADDR4)')
