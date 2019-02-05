"""Host Reservation DHCPv4"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import misc
from features import srv_msg
from features import srv_control


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_one_address_inside_pool_hw_address(step):
    misc.test_setup(step)
    # outside of the pool
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.10',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
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
def test_v4_host_reservation_one_address_inside_pool_client_id(step):
    misc.test_setup(step)
    # outside of the pool
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.10',
                                           '0',
                                           'client-id',
                                           'ff:01:02:03:ff:04:11:22')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
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
def test_v4_host_reservation_one_address_outside_pool(step):
    misc.test_setup(step)
    # outside of the pool
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.30-192.168.50.50')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.10',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
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


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_one_address_inside_pool_different_mac(step):
    misc.test_setup(step)
    # request address from different mac that has been reserved
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.50')
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
def test_v4_host_reservation_multiple_address_reservation_empty_pool(step):
    misc.test_setup(step)
    # request address from different mac that has been reserved
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.10',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.11',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:03')
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
def test_v4_host_reservation_multiple_address_reservation_empty_pool_2(step):
    misc.test_setup(step)
    # request address from different mac that has been reserved
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.12')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.10',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.11',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:03')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.12',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:02')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

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
