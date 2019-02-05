"""Kea6 legal logging"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_msg
from features import srv_control
from features import misc


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_assigned_address(step):
    misc.test_procedure(step)
    srv_msg.remove_file_from_server(step, '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt')

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '3')
    srv_control.set_time(step, 'rebind-timer', '50')
    srv_control.set_time(step, 'valid-lifetime', '600')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040506')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_include_option(step, 'Response', None, '61')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '00010203040506')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040506')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_include_option(step, 'Response', None, '61')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '00010203040506')

    srv_msg.copy_remote(step, '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt',
                               None,
                               'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt',
                               None,
                               'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04, client-id: 00:01:02:03:04:05:06')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_assigned_address_pgsql(step):
    misc.test_procedure(step)
    srv_msg.remove_from_db_table(step, 'logs', 'PostgreSQL')

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '3')
    srv_control.set_time(step, 'rebind-timer', '50')
    srv_control.set_time(step, 'valid-lifetime', '600')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook(step, '1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook(step, '1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook(step, '1', 'type', 'postgresql')
    srv_control.add_parameter_to_hook(step, '1', 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040506')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_include_option(step, 'Response', None, '61')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '00010203040506')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040506')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_include_option(step, 'Response', None, '61')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '00010203040506')

    srv_msg.table_contains_line(step,
                                'logs',
                                'PostgreSQL',
                                None,
                                'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs')
    srv_msg.table_contains_line(step,
                                'logs',
                                'PostgreSQL',
                                None,
                                'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04, client-id: 00:01:02:03:04:05:06')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_assigned_address_mysql(step):
    misc.test_procedure(step)
    srv_msg.remove_from_db_table(step, 'logs', 'MySQL')

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '3')
    srv_control.set_time(step, 'rebind-timer', '50')
    srv_control.set_time(step, 'valid-lifetime', '600')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook(step, '1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook(step, '1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook(step, '1', 'type', 'mysql')
    srv_control.add_parameter_to_hook(step, '1', 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040506')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_include_option(step, 'Response', None, '61')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '00010203040506')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040506')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_include_option(step, 'Response', None, '61')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '00010203040506')

    srv_msg.table_contains_line(step,
                                'logs',
                                'MySQL',
                                None,
                                'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs')
    srv_msg.table_contains_line(step,
                                'logs',
                                'MySQL',
                                None,
                                'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04, client-id: 00:01:02:03:04:05:06')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_assigned_address_without_client_id(step):
    misc.test_procedure(step)
    srv_msg.remove_file_from_server(step, '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt')

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '3')
    srv_control.set_time(step, 'rebind-timer', '50')
    srv_control.set_time(step, 'valid-lifetime', '600')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    srv_msg.copy_remote(step, '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt',
                               None,
                               'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt',
                               None,
                               'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt',
                               'NOT ',
                               'client-id:')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_assigned_address_without_client_id_pgsql(step):
    misc.test_procedure(step)
    srv_msg.remove_from_db_table(step, 'logs', 'PostgreSQL')

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '3')
    srv_control.set_time(step, 'rebind-timer', '50')
    srv_control.set_time(step, 'valid-lifetime', '600')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook(step, '1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook(step, '1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook(step, '1', 'type', 'postgresql')
    srv_control.add_parameter_to_hook(step, '1', 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    srv_msg.table_contains_line(step,
                                'logs',
                                'PostgreSQL',
                                None,
                                'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs')
    srv_msg.table_contains_line(step,
                                'logs',
                                'PostgreSQL',
                                None,
                                'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04')
    srv_msg.table_contains_line(step, 'logs', 'PostgreSQL', 'NOT ', 'client-id:')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_assigned_address_without_client_id_mysql(step):
    misc.test_procedure(step)
    srv_msg.remove_from_db_table(step, 'logs', 'MySQL')

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '3')
    srv_control.set_time(step, 'rebind-timer', '50')
    srv_control.set_time(step, 'valid-lifetime', '600')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook(step, '1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook(step, '1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook(step, '1', 'type', 'mysql')
    srv_control.add_parameter_to_hook(step, '1', 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    srv_msg.table_contains_line(step,
                                'logs',
                                'MySQL',
                                None,
                                'Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs')
    srv_msg.table_contains_line(step,
                                'logs',
                                'MySQL',
                                None,
                                'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04')
    srv_msg.table_contains_line(step, 'logs', 'MySQL', 'NOT ', 'client-id:')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_assigned_address_via_relay_pgsql_1(step):
    misc.test_procedure(step)
    srv_msg.remove_file_from_server(step, '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt')

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '3')
    srv_control.set_time(step, 'rebind-timer', '50')
    srv_control.set_time(step, 'valid-lifetime', '600')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.2-192.168.50.2')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040577')
    srv_msg.network_variable(step, 'source_port', '67')
    srv_msg.network_variable(step, 'source_address', '$(GIADDR4)')
    srv_msg.network_variable(step, 'destination_address', '$(SRV4_ADDR)')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.2')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040577')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.2')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.2')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    srv_msg.copy_remote(step, '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt',
                               None,
                               'Address: 192.168.50.2 has been assigned for 0 hrs 10 mins 0 secs to a device with hardware address: hwtype=1 00:00:00:00:00:00,')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt',
                               None,
                               'client-id: 00:01:02:03:04:05:77 connected via relay at address: $(GIADDR4)')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_assigned_address_via_relay_pgsql_2(step):
    misc.test_procedure(step)
    srv_msg.remove_from_db_table(step, 'logs', 'PostgreSQL')

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '3')
    srv_control.set_time(step, 'rebind-timer', '50')
    srv_control.set_time(step, 'valid-lifetime', '600')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.2-192.168.50.2')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook(step, '1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook(step, '1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook(step, '1', 'type', 'postgresql')
    srv_control.add_parameter_to_hook(step, '1', 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040577')
    srv_msg.network_variable(step, 'source_port', '67')
    srv_msg.network_variable(step, 'source_address', '$(GIADDR4)')
    srv_msg.network_variable(step, 'destination_address', '$(SRV4_ADDR)')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.2')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040577')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.2')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.2')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    srv_msg.table_contains_line(step,
                                'logs',
                                'PostgreSQL',
                                None,
                                'Address: 192.168.50.2 has been assigned for 0 hrs 10 mins 0 secs to a device with hardware address: hwtype=1 00:00:00:00:00:00,')
    srv_msg.table_contains_line(step,
                                'logs',
                                'PostgreSQL',
                                None,
                                'client-id: 00:01:02:03:04:05:77 connected via relay at address: $(GIADDR4)')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_assigned_address_via_relay_mysql(step):
    misc.test_procedure(step)
    srv_msg.remove_from_db_table(step, 'logs', 'MySQL')

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '3')
    srv_control.set_time(step, 'rebind-timer', '50')
    srv_control.set_time(step, 'valid-lifetime', '600')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.2-192.168.50.2')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook(step, '1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook(step, '1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook(step, '1', 'type', 'mysql')
    srv_control.add_parameter_to_hook(step, '1', 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040577')
    srv_msg.network_variable(step, 'source_port', '67')
    srv_msg.network_variable(step, 'source_address', '$(GIADDR4)')
    srv_msg.network_variable(step, 'destination_address', '$(SRV4_ADDR)')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.2')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040577')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.2')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.2')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    srv_msg.table_contains_line(step,
                                'logs',
                                'MySQL',
                                None,
                                'Address: 192.168.50.2 has been assigned for 0 hrs 10 mins 0 secs to a device with hardware address: hwtype=1 00:00:00:00:00:00,')
    srv_msg.table_contains_line(step,
                                'logs',
                                'MySQL',
                                None,
                                'client-id: 00:01:02:03:04:05:77 connected via relay at address: $(GIADDR4)')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_renewed_address(step):
    misc.test_procedure(step)
    srv_msg.remove_file_from_server(step, '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt')

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '3')
    srv_control.set_time(step, 'rebind-timer', '50')
    srv_control.set_time(step, 'valid-lifetime', '600')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.network_variable(step, 'source_port', '67')
    srv_msg.network_variable(step, 'source_address', '$(GIADDR4)')
    srv_msg.network_variable(step, 'destination_address', '$(SRV4_ADDR)')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '$(SRV4_ADDR)')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '$(SRV4_ADDR)')

    # make sure that T1 time expires and client will be in RENEWING state.
    srv_msg.forge_sleep(step, '3', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '$(SRV4_ADDR)')

    srv_msg.copy_remote(step, '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt',
                               None,
                               'Address: 192.168.50.1 has been renewed for 0 hrs 10 mins 0 secs')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt',
                               None,
                               'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04 connected via relay at address: $(GIADDR4)')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_renewed_address_pgsql(step):
    misc.test_procedure(step)
    srv_msg.remove_from_db_table(step, 'logs', 'PostgreSQL')

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '3')
    srv_control.set_time(step, 'rebind-timer', '50')
    srv_control.set_time(step, 'valid-lifetime', '600')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook(step, '1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook(step, '1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook(step, '1', 'type', 'postgresql')
    srv_control.add_parameter_to_hook(step, '1', 'user', '$(DB_USER)')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.network_variable(step, 'source_port', '67')
    srv_msg.network_variable(step, 'source_address', '$(GIADDR4)')
    srv_msg.network_variable(step, 'destination_address', '$(SRV4_ADDR)')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '$(SRV4_ADDR)')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '$(SRV4_ADDR)')

    # make sure that T1 time expires and client will be in RENEWING state.
    srv_msg.forge_sleep(step, '3', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '$(SRV4_ADDR)')

    srv_msg.table_contains_line(step,
                                'logs',
                                'PostgreSQL',
                                None,
                                'ddress: 192.168.50.1 has been renewed for 0 hrs 10 mins 0 secs')
    srv_msg.table_contains_line(step,
                                'logs',
                                'PostgreSQL',
                                None,
                                'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04 connected via relay at address: $(GIADDR4)')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_renewed_address_mysql(step):
    misc.test_procedure(step)
    srv_msg.remove_from_db_table(step, 'logs', 'MySQL')

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '3')
    srv_control.set_time(step, 'rebind-timer', '50')
    srv_control.set_time(step, 'valid-lifetime', '600')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook(step, '1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook(step, '1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook(step, '1', 'type', 'mysql')
    srv_control.add_parameter_to_hook(step, '1', 'user', '$(DB_USER)')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.network_variable(step, 'source_port', '67')
    srv_msg.network_variable(step, 'source_address', '$(GIADDR4)')
    srv_msg.network_variable(step, 'destination_address', '$(SRV4_ADDR)')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '$(SRV4_ADDR)')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '$(SRV4_ADDR)')

    # make sure that T1 time expires and client will be in RENEWING state.
    srv_msg.forge_sleep(step, '3', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '$(SRV4_ADDR)')

    srv_msg.table_contains_line(step,
                                'logs',
                                'MySQL',
                                None,
                                'ddress: 192.168.50.1 has been renewed for 0 hrs 10 mins 0 secs')
    srv_msg.table_contains_line(step,
                                'logs',
                                'MySQL',
                                None,
                                'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04 connected via relay at address: $(GIADDR4)')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_rebind_address(step):
    misc.test_procedure(step)
    srv_msg.remove_file_from_server(step, '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt')

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '3')
    srv_control.set_time(step, 'rebind-timer', '4')
    srv_control.set_time(step, 'valid-lifetime', '600')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.network_variable(step, 'source_port', '67')
    srv_msg.network_variable(step, 'source_address', '$(GIADDR4)')
    srv_msg.network_variable(step, 'destination_address', '$(SRV4_ADDR)')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '$(SRV4_ADDR)')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '$(SRV4_ADDR)')

    # make sure that T2 time expires and client will be in REBIND state.
    srv_msg.forge_sleep(step, '5', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '$(SRV4_ADDR)')

    srv_msg.copy_remote(step, '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt',
                               None,
                               'Address: 192.168.50.1 has been renewed for 0 hrs 10 mins 0 secs')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt',
                               None,
                               'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04 connected via relay at address: $(GIADDR4)')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_rebind_address_mysql(step):
    misc.test_procedure(step)
    srv_msg.remove_from_db_table(step, 'logs', 'MySQL')

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '3')
    srv_control.set_time(step, 'rebind-timer', '4')
    srv_control.set_time(step, 'valid-lifetime', '600')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook(step, '1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook(step, '1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook(step, '1', 'type', 'mysql')
    srv_control.add_parameter_to_hook(step, '1', 'user', '$(DB_USER)')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.network_variable(step, 'source_port', '67')
    srv_msg.network_variable(step, 'source_address', '$(GIADDR4)')
    srv_msg.network_variable(step, 'destination_address', '$(SRV4_ADDR)')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '$(SRV4_ADDR)')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '$(SRV4_ADDR)')

    # make sure that T2 time expires and client will be in REBIND state.
    srv_msg.forge_sleep(step, '5', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '$(SRV4_ADDR)')

    srv_msg.table_contains_line(step,
                                'logs',
                                'MySQL',
                                None,
                                'Address: 192.168.50.1 has been renewed for 0 hrs 10 mins 0 secs')
    srv_msg.table_contains_line(step,
                                'logs',
                                'MySQL',
                                None,
                                'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04 connected via relay at address: $(GIADDR4)')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v4_legal_log_rebind_address_pgsql(step):
    misc.test_procedure(step)
    srv_msg.remove_from_db_table(step, 'logs', 'PostgreSQL')

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '3')
    srv_control.set_time(step, 'rebind-timer', '4')
    srv_control.set_time(step, 'valid-lifetime', '600')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook(step, '1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook(step, '1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook(step, '1', 'type', 'postgresql')
    srv_control.add_parameter_to_hook(step, '1', 'user', '$(DB_USER)')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.network_variable(step, 'source_port', '67')
    srv_msg.network_variable(step, 'source_address', '$(GIADDR4)')
    srv_msg.network_variable(step, 'destination_address', '$(SRV4_ADDR)')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '$(SRV4_ADDR)')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '$(SRV4_ADDR)')

    # make sure that T2 time expires and client will be in REBIND state.
    srv_msg.forge_sleep(step, '5', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '$(SRV4_ADDR)')

    srv_msg.table_contains_line(step,
                                'logs',
                                'PostgreSQL',
                                None,
                                'Address: 192.168.50.1 has been renewed for 0 hrs 10 mins 0 secs')
    srv_msg.table_contains_line(step,
                                'logs',
                                'PostgreSQL',
                                None,
                                'to a device with hardware address: hwtype=1 ff:01:02:03:ff:04 connected via relay at address: $(GIADDR4)')
