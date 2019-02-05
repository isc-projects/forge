"""Host Reservation DHCPv4 stored in PostgreSQL database."""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import misc
from features import srv_msg
from features import srv_control


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_pgsql_one_address_inside_pool(step):
    misc.test_setup(step)
    # outside of the pool
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.enable_db_backend_reservation(step, 'PostgreSQL')
    srv_control.new_db_backend_reservation(step, 'PostgreSQL', 'hw-address', 'ff:01:02:03:ff:04')
    srv_control.update_db_backend_reservation(step,
                                              'hostname',
                                              'reserved-hostname',
                                              'PostgreSQL',
                                              '1')
    srv_control.update_db_backend_reservation(step,
                                              'ipv4_address',
                                              '192.168.50.10',
                                              'PostgreSQL',
                                              '1')
    srv_control.update_db_backend_reservation(step, 'dhcp4_subnet_id', '1', 'PostgreSQL', '1')
    srv_control.upload_db_reservation(step, 'PostgreSQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
@pytest.mark.disabled
def test_v4_host_reservation_pgsql_client_id_one_address_inside_pool(step):
    misc.test_setup(step)
    # outside of the pool
    # TODO update names
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.enable_db_backend_reservation(step, 'PostgreSQL')
    srv_control.new_db_backend_reservation(step, 'PostgreSQL', 'client-id', '00010203040577')
    srv_control.add_line(step,
                         '"host-reservation-identifiers": [ "hw-address", "duid", "client-id" ]')
    srv_control.update_db_backend_reservation(step,
                                              'hostname',
                                              'reserved-hostname',
                                              'PostgreSQL',
                                              '1')
    srv_control.update_db_backend_reservation(step,
                                              'ipv4_address',
                                              '192.168.50.10',
                                              'PostgreSQL',
                                              '1')
    srv_control.update_db_backend_reservation(step, 'dhcp4_subnet_id', '1', 'PostgreSQL', '1')
    srv_control.upload_db_reservation(step, 'PostgreSQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040577')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040577')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_pgsql_one_address_inside_pool_option(step):
    misc.test_setup(step)
    # outside of the pool
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.enable_db_backend_reservation(step, 'PostgreSQL')
    srv_control.new_db_backend_reservation(step, 'PostgreSQL', 'hw-address', 'ff:01:02:03:ff:04')
    srv_control.update_db_backend_reservation(step, 'next_server', '11.1.1.1', 'PostgreSQL', '1')
    srv_control.update_db_backend_reservation(step,
                                              'server_hostname',
                                              'hostname-server.com',
                                              'PostgreSQL',
                                              '1')
    srv_control.update_db_backend_reservation(step,
                                              'boot_file_name',
                                              'file-name',
                                              'PostgreSQL',
                                              '1')
    srv_control.update_db_backend_reservation(step,
                                              'ipv4_address',
                                              '192.168.50.10',
                                              'PostgreSQL',
                                              '1')
    srv_control.update_db_backend_reservation(step, 'dhcp4_subnet_id', '1', 'PostgreSQL', '1')
    srv_control.option_db_record_reservation(step,
                                             '11',
                                             '10.0.0.1',
                                             'dhcp4',
                                             '1',
                                             '$(EMPTY)',
                                             '1',
                                             'subnet',
                                             'PostgreSQL',
                                             '1')
    srv_control.config_srv_opt(step, 'resource-location-servers', '199.199.199.1,150.150.150.1')
    srv_control.upload_db_reservation(step, 'PostgreSQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '11')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '11')
    srv_msg.response_check_option_content(step, 'Response', '11', None, 'value', '10.0.0.1')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_pgsql_one_address_outside_pool_dual_backend_1(step):
    misc.test_setup(step)
    # outside of the pool
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.30-192.168.50.50')
    srv_control.enable_db_backend_reservation(step, 'PostgreSQL')
    srv_control.new_db_backend_reservation(step, 'PostgreSQL', 'hw-address', 'ff:01:02:03:ff:04')
    srv_control.update_db_backend_reservation(step,
                                              'hostname',
                                              'reserved-hostname',
                                              'PostgreSQL',
                                              '1')
    srv_control.update_db_backend_reservation(step,
                                              'ipv4_address',
                                              '192.168.50.10',
                                              'PostgreSQL',
                                              '1')
    srv_control.update_db_backend_reservation(step, 'dhcp4_subnet_id', '1', 'PostgreSQL', '1')
    srv_control.upload_db_reservation(step, 'PostgreSQL')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.11',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:03')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:03')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.11')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.11')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:03')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.11')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_pgsql_one_address_outside_pool_dual_backend_2(step):
    misc.test_setup(step)
    # outside of the pool
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.30-192.168.50.50')
    srv_control.enable_db_backend_reservation(step, 'PostgreSQL')
    srv_control.new_db_backend_reservation(step, 'PostgreSQL', 'hw-address', 'ff:01:02:03:ff:04')
    srv_control.update_db_backend_reservation(step,
                                              'hostname',
                                              'reserved-hostname',
                                              'PostgreSQL',
                                              '1')
    srv_control.update_db_backend_reservation(step, 'next_server', '1.1.1.1', 'PostgreSQL', '1')
    srv_control.update_db_backend_reservation(step,
                                              'ipv4_address',
                                              '192.168.50.10',
                                              'PostgreSQL',
                                              '1')
    srv_control.update_db_backend_reservation(step, 'dhcp4_subnet_id', '1', 'PostgreSQL', '1')
    srv_control.upload_db_reservation(step, 'PostgreSQL')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.11',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:03')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:03')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.11')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.11')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:03')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.11')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_pgsql_one_address_inside_pool_different_mac(step):
    misc.test_setup(step)
    # request address from different mac that has been reserved
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.enable_db_backend_reservation(step, 'PostgreSQL')
    srv_control.new_db_backend_reservation(step, 'PostgreSQL', 'hw-address', 'ff:01:02:03:ff:04')

    srv_control.update_db_backend_reservation(step,
                                              'hostname',
                                              'reserved-hostname',
                                              'PostgreSQL',
                                              '1')
    srv_control.update_db_backend_reservation(step,
                                              'ipv4_address',
                                              '192.168.50.10',
                                              'PostgreSQL',
                                              '1')
    srv_control.update_db_backend_reservation(step, 'dhcp4_subnet_id', '1', 'PostgreSQL', '1')
    srv_control.upload_db_reservation(step, 'PostgreSQL')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', 'NOT ', 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'NAK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '0.0.0.0')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_one_address_empty_pool(step):
    misc.test_setup(step)
    # request address from different mac that has been reserved
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.10',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_pgsql_multiple_address_reservation_empty_pool(step):
    misc.test_setup(step)
    # request address from different mac that has been reserved
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.enable_db_backend_reservation(step, 'PostgreSQL')
    srv_control.new_db_backend_reservation(step, 'PostgreSQL', 'hw-address', 'ff:01:02:03:ff:04')
    srv_control.update_db_backend_reservation(step,
                                              'hostname',
                                              'reserved-hostname',
                                              'PostgreSQL',
                                              '1')
    srv_control.update_db_backend_reservation(step,
                                              'ipv4_address',
                                              '192.168.50.10',
                                              'PostgreSQL',
                                              '1')
    srv_control.update_db_backend_reservation(step, 'dhcp4_subnet_id', '1', 'PostgreSQL', '1')

    srv_control.new_db_backend_reservation(step, 'PostgreSQL', 'hw-address', 'ff:01:02:03:ff:03')
    srv_control.update_db_backend_reservation(step,
                                              'hostname',
                                              'reserved-hostname',
                                              'PostgreSQL',
                                              '2')
    srv_control.update_db_backend_reservation(step,
                                              'ipv4_address',
                                              '192.168.50.11',
                                              'PostgreSQL',
                                              '2')
    srv_control.update_db_backend_reservation(step, 'dhcp4_subnet_id', '1', 'PostgreSQL', '2')
    srv_control.upload_db_reservation(step, 'PostgreSQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_multiple_pgsql_address_reservation_empty_pool_2(step):
    misc.test_setup(step)
    # request address from different mac that has been reserved
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.12')
    srv_control.enable_db_backend_reservation(step, 'PostgreSQL')
    srv_control.new_db_backend_reservation(step, 'PostgreSQL', 'hw-address', 'ff:01:02:03:ff:04')
    srv_control.update_db_backend_reservation(step,
                                              'hostname',
                                              'reserved-hostname',
                                              'PostgreSQL',
                                              '1')
    srv_control.update_db_backend_reservation(step,
                                              'ipv4_address',
                                              '192.168.50.10',
                                              'PostgreSQL',
                                              '1')
    srv_control.update_db_backend_reservation(step, 'dhcp4_subnet_id', '1', 'PostgreSQL', '1')

    srv_control.new_db_backend_reservation(step, 'PostgreSQL', 'hw-address', 'ff:01:02:03:ff:03')
    srv_control.update_db_backend_reservation(step,
                                              'hostname',
                                              'reserved-hostname',
                                              'PostgreSQL',
                                              '2')
    srv_control.update_db_backend_reservation(step,
                                              'ipv4_address',
                                              '192.168.50.11',
                                              'PostgreSQL',
                                              '2')
    srv_control.update_db_backend_reservation(step, 'dhcp4_subnet_id', '1', 'PostgreSQL', '2')

    srv_control.new_db_backend_reservation(step, 'PostgreSQL', 'hw-address', 'ff:01:02:03:ff:02')
    srv_control.update_db_backend_reservation(step,
                                              'hostname',
                                              'reserved-hostname',
                                              'PostgreSQL',
                                              '3')
    srv_control.update_db_backend_reservation(step,
                                              'ipv4_address',
                                              '192.168.50.12',
                                              'PostgreSQL',
                                              '3')
    srv_control.update_db_backend_reservation(step, 'dhcp4_subnet_id', '1', 'PostgreSQL', '3')

    srv_control.upload_db_reservation(step, 'PostgreSQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:03')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:03')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:02')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:02')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)
