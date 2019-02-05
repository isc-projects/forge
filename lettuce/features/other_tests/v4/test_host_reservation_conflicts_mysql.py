"""Host Reservation DHCPv4"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_control
from features import misc
from features import srv_msg


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_conflicts_duplicate_reservations(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.10',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.12',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_conflicts_duplicate_reservations_different_subnets(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.50')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.10',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.12',
                                           '1',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.start_srv(step, 'DHCP', 'started')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_conflicts_mysql_reconfigure_server_with_reservation_of_used_address(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.2')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:11')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:11')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:55')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:55')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.3')

    srv_control.new_db_backend_reservation(step, 'MySQL', 'hw-address', 'ff:01:02:03:ff:77')
    srv_control.update_db_backend_reservation(step, 'hostname', 'reserved-hostname', 'MySQL', '1')
    srv_control.update_db_backend_reservation(step, 'ipv4_address', '192.168.50.2', 'MySQL', '1')
    srv_control.update_db_backend_reservation(step, 'dhcp4_subnet_id', '1', 'MySQL', '1')
    srv_control.upload_db_reservation(step, 'MySQL')

    # Reserve address 192.168.50.2 in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:77.
    srv_control.start_srv(step, 'DHCP', 'reconfigured')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:77')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', 'NOT ', 'yiaddr', '192.168.50.2')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_conflicts_mysql_reconfigure_server_with_reservation_of_used_address_2(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.2')

    srv_control.new_db_backend_reservation(step, 'MySQL', 'hw-address', 'ff:01:02:03:ff:11')
    srv_control.update_db_backend_reservation(step, 'hostname', 'reserved-hostname', 'MySQL', '1')
    srv_control.update_db_backend_reservation(step, 'ipv4_address', '192.168.50.2', 'MySQL', '1')
    srv_control.update_db_backend_reservation(step, 'dhcp4_subnet_id', '1', 'MySQL', '1')
    srv_control.upload_db_reservation(step, 'MySQL')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:11')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:11')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.2')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:55')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:55')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.3')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.2',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:77')

    srv_control.start_srv(step, 'DHCP', 'reconfigured')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:77')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', 'NOT ', 'yiaddr', '192.168.50.2')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_conflicts_reconfigure_server_with_reservation_of_used_address_3(step):
    misc.test_setup(step)
    # reconfigure different address for same MAC from outside of the pool
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.5-192.168.50.9')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.10',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
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
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.5-192.168.50.9')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.30',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')

    srv_control.start_srv(step, 'DHCP', 'reconfigured')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.30')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.30')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_conflicts_reconfigure_server_switched_mac_in_reservations_in_pool(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.5-192.168.50.30')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.10',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
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
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.5-192.168.50.30')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.10',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:01')

    srv_control.start_srv(step, 'DHCP', 'reconfigured')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', 'NOT ', 'yiaddr', '192.168.50.10')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_conflicts_reconfigure_server_switched_mac_in_reservations_out_of_pool(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.5-192.168.50.30')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.50',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
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
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.5-192.168.50.30')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.50',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:01')

    srv_control.start_srv(step, 'DHCP', 'reconfigured')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', 'NOT ', 'yiaddr', '192.168.50.50')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_conflicts_reconfigure_server_add_reservation_for_host_that_has_leases(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.5-192.168.50.5')
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
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.5')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.50',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')

    srv_control.start_srv(step, 'DHCP', 'reconfigured')

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
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.5')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_conflicts_renew_address_that_has_been_reserved_during_reconfiguration(step):

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '3')
    srv_control.set_time(step, 'rebind-timer', '50')
    srv_control.set_time(step, 'valid-lifetime', '500')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.5')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.5')

    srv_msg.forge_sleep(step, '5', 'seconds')

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '3')
    srv_control.set_time(step, 'rebind-timer', '50')
    srv_control.set_time(step, 'valid-lifetime', '500')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.5-192.168.50.10')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.5',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.start_srv(step, 'DHCP', 'reconfigured')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', 'NOT ', 'yiaddr', '192.168.50.5')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.5')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'NAK')

    srv_msg.forge_sleep(step, '6', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.5')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.5')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_conflicts_renew_address_using_different_mac_that_has_been_reserved_during_reconfiguration(step):

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '3')
    srv_control.set_time(step, 'rebind-timer', '50')
    srv_control.set_time(step, 'valid-lifetime', '500')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.5')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.5')

    srv_msg.forge_sleep(step, '5', 'seconds')

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '3')
    srv_control.set_time(step, 'rebind-timer', '50')
    srv_control.set_time(step, 'valid-lifetime', '500')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.5-192.168.50.10')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.5',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.start_srv(step, 'DHCP', 'reconfigured')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', 'NOT ', 'yiaddr', '192.168.50.5')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.5')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'NAK')

    srv_msg.forge_sleep(step, '6', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.5')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'NAK')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_conflicts_renew_address_which_reservation_changed_during_reconfigure(step):

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '3')
    srv_control.set_time(step, 'rebind-timer', '50')
    srv_control.set_time(step, 'valid-lifetime', '500')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.5',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:01')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.5')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.5')

    srv_msg.forge_sleep(step, '5', 'seconds')

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '3')
    srv_control.set_time(step, 'rebind-timer', '50')
    srv_control.set_time(step, 'valid-lifetime', '500')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.5-192.168.50.10')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.5',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.start_srv(step, 'DHCP', 'reconfigured')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', 'NOT ', 'yiaddr', '192.168.50.5')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.5')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'NAK')

    srv_msg.forge_sleep(step, '6', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.5')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.5')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_conflicts_renew_address_which_reservation_changed_during_reconfigure_2(step):

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '3')
    srv_control.set_time(step, 'rebind-timer', '50')
    srv_control.set_time(step, 'valid-lifetime', '500')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.5',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:01')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.5')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.5')

    srv_msg.forge_sleep(step, '5', 'seconds')

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '3')
    srv_control.set_time(step, 'rebind-timer', '50')
    srv_control.set_time(step, 'valid-lifetime', '500')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.5-192.168.50.60')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.50',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:01')
    srv_control.start_srv(step, 'DHCP', 'reconfigured')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.5')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'NAK')

    srv_msg.forge_sleep(step, '6', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.50')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_conflicts_rebind_address_which_reservation_changed_during_reconfigure(step):

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '3')
    srv_control.set_time(step, 'rebind-timer', '4')
    srv_control.set_time(step, 'valid-lifetime', '500')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.5',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:01')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.5')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.5')

    srv_msg.forge_sleep(step, '5', 'seconds')

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '3')
    srv_control.set_time(step, 'rebind-timer', '4')
    srv_control.set_time(step, 'valid-lifetime', '500')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.5-192.168.50.10')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.5',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.start_srv(step, 'DHCP', 'reconfigured')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', 'NOT ', 'yiaddr', '192.168.50.5')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.5')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'NAK')

    srv_msg.forge_sleep(step, '6', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.5')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.5')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_conflicts_rebind_address_which_reservation_changed_during_reconfigure_2(step):

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '3')
    srv_control.set_time(step, 'rebind-timer', '4')
    srv_control.set_time(step, 'valid-lifetime', '500')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.5',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:01')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.5')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.5')

    srv_msg.forge_sleep(step, '5', 'seconds')

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '3')
    srv_control.set_time(step, 'rebind-timer', '4')
    srv_control.set_time(step, 'valid-lifetime', '500')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.5-192.168.50.60')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.50',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:01')
    srv_control.start_srv(step, 'DHCP', 'reconfigured')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.5')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'NAK')

    srv_msg.forge_sleep(step, '6', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.50')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')
