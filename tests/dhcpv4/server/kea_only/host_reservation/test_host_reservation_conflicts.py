"""Host Reservation DHCPv4"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_control
import srv_msg


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_conflicts_duplicate_reservations():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.10',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.12',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv_during_process('DHCP', 'configuration')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_conflicts_duplicate_reservations_different_subnets():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.50')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.10',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.12',
                                           '1',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_conflicts_reconfigure_server_with_reservation_of_used_address():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.2')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:11')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:11')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:55')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:55')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.3')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.2',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:77')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'reconfigured')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:77')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', 'NOT ', 'yiaddr', '192.168.50.2')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_conflicts_reconfigure_server_with_reservation_of_used_address_2():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.2')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.2',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:11')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:11')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:11')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.2')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:55')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:55')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.3')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.2',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:77')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'reconfigured')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:77')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', 'NOT ', 'yiaddr', '192.168.50.2')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_conflicts_reconfigure_server_with_reservation_of_used_address_3():
    misc.test_setup()
    # reconfigure different address for same MAC from outside of the pool
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.9')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.10',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.9')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.30',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'reconfigured')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.30')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.30')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_conflicts_reconfigure_server_switched_mac_in_reservations_in_pool():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.30')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.10',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.30')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.10',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:01')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'reconfigured')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', 'NOT ', 'yiaddr', '192.168.50.10')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_conflicts_reconfigure_server_switched_mac_in_reservations_out_of_pool():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.30')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.50',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.30')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.50',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:01')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'reconfigured')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', 'NOT ', 'yiaddr', '192.168.50.50')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_conflicts_reconfigure_server_add_reservation_for_host_that_has_leases():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.5')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.50',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'reconfigured')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.5')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
@pytest.mark.disabled
def test_v4_host_reservation_conflicts_renew_address_that_has_been_reserved_during_reconfiguration():

    misc.test_setup()
    srv_control.set_time('renew-timer', '3')
    srv_control.set_time('rebind-timer', '50')
    srv_control.set_time('valid-lifetime', '500')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.5')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.5')

    srv_msg.forge_sleep('5', 'seconds')

    misc.test_setup()
    srv_control.set_time('renew-timer', '3')
    srv_control.set_time('rebind-timer', '50')
    srv_control.set_time('valid-lifetime', '500')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.10')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.5',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'reconfigured')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', 'NOT ', 'yiaddr', '192.168.50.5')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.5')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'NAK')

    srv_msg.forge_sleep('6', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.5')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.5')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.5')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_conflicts_renew_address_using_different_mac_that_has_been_reserved_during_reconfiguration():

    misc.test_setup()
    srv_control.set_time('renew-timer', '3')
    srv_control.set_time('rebind-timer', '50')
    srv_control.set_time('valid-lifetime', '500')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.5')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.5')

    srv_msg.forge_sleep('5', 'seconds')

    misc.test_setup()
    srv_control.set_time('renew-timer', '3')
    srv_control.set_time('rebind-timer', '50')
    srv_control.set_time('valid-lifetime', '500')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.10')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.5',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'reconfigured')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', 'NOT ', 'yiaddr', '192.168.50.5')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.5')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'NAK')

    srv_msg.forge_sleep('6', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.5')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'NAK')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
@pytest.mark.disabled
def test_v4_host_reservation_conflicts_renew_address_which_reservation_changed_during_reconfigure():

    misc.test_setup()
    srv_control.set_time('renew-timer', '3')
    srv_control.set_time('rebind-timer', '50')
    srv_control.set_time('valid-lifetime', '500')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.5',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:01')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.5')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.5')

    srv_msg.forge_sleep('5', 'seconds')

    misc.test_setup()
    srv_control.set_time('renew-timer', '3')
    srv_control.set_time('rebind-timer', '50')
    srv_control.set_time('valid-lifetime', '500')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.10')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.5',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'reconfigured')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', 'NOT ', 'yiaddr', '192.168.50.5')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.5')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'NAK')

    srv_msg.forge_sleep('6', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.5')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.5')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.5')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_conflicts_renew_address_which_reservation_changed_during_reconfigure_2():

    misc.test_setup()
    srv_control.set_time('renew-timer', '3')
    srv_control.set_time('rebind-timer', '50')
    srv_control.set_time('valid-lifetime', '500')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.5',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:01')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.5')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.5')

    srv_msg.forge_sleep('5', 'seconds')

    misc.test_setup()
    srv_control.set_time('renew-timer', '3')
    srv_control.set_time('rebind-timer', '50')
    srv_control.set_time('valid-lifetime', '500')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.60')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.50',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:01')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'reconfigured')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.5')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'NAK')

    srv_msg.forge_sleep('6', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.50')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
@pytest.mark.disabled
def test_v4_host_reservation_conflicts_rebind_address_which_reservation_changed_during_reconfigure():

    misc.test_setup()
    srv_control.set_time('renew-timer', '3')
    srv_control.set_time('rebind-timer', '4')
    srv_control.set_time('valid-lifetime', '500')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.5',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:01')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.5')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.5')

    srv_msg.forge_sleep('5', 'seconds')

    misc.test_setup()
    srv_control.set_time('renew-timer', '3')
    srv_control.set_time('rebind-timer', '4')
    srv_control.set_time('valid-lifetime', '500')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.10')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.5',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'reconfigured')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', 'NOT ', 'yiaddr', '192.168.50.5')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.5')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'NAK')

    srv_msg.forge_sleep('6', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.5')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.5')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.5')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_conflicts_rebind_address_which_reservation_changed_during_reconfigure_2():

    misc.test_setup()
    srv_control.set_time('renew-timer', '3')
    srv_control.set_time('rebind-timer', '4')
    srv_control.set_time('valid-lifetime', '500')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.5',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:01')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.5')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.5')

    srv_msg.forge_sleep('5', 'seconds')

    misc.test_setup()
    srv_control.set_time('renew-timer', '3')
    srv_control.set_time('rebind-timer', '4')
    srv_control.set_time('valid-lifetime', '500')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.60')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.50',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:01')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'reconfigured')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.5')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'NAK')

    srv_msg.forge_sleep('6', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.50')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')
