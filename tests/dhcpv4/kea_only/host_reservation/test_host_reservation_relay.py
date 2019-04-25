"""Host Reservation DHCPv4"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_msg
import srv_control


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_circuit_id():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.10',
                                           '0',
                                           'circuit-id',
                                           '060106020603')
    # "host-reservation-identifiers": [ "hw-address", "duid", "circuit-id", "client-id" ]
    srv_control.add_line('"host-reservation-identifiers": [ "circuit-id" ]')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('relay_agent_Information', '16616263')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('relay_agent_Information', '16616263')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_circuit_id_negative():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.10',
                                           '0',
                                           'circuit-id',
                                           '060106020603')
    # "host-reservation-identifiers": [ "hw-address", "duid", "circuit-id", "client-id" ]
    srv_control.add_line('"host-reservation-identifiers": [ "hw-address", "duid", "client-id" ]')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('relay_agent_Information', '16616263')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', 'NOT ', 'yiaddr', '192.168.50.10')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_duid():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.host_reservation_in_subnet('address', '192.168.50.10', '0', 'duid', '04:33:44')
    # "host-reservation-identifiers": [ "hw-address", "duid", "circuit-id", "client-id" ]
    srv_control.add_line('"host-reservation-identifiers": [ "duid" ]')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:33:44')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:33:44')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_duid_negative():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.host_reservation_in_subnet('address', '192.168.50.10', '0', 'duid', '04:33:44')
    # "host-reservation-identifiers": [ "hw-address", "duid", "circuit-id", "client-id" ]
    srv_control.add_line('"host-reservation-identifiers": [ "hw-address", "circuit-id", "client-id" ]')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:33:44')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', 'NOT ', 'yiaddr', '192.168.50.10')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_hwaddr_negative():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.10',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:11')
    # "host-reservation-identifiers": [ "hw-address", "duid", "circuit-id", "client-id" ]
    srv_control.add_line('"host-reservation-identifiers": [ "circuit-id", "duid", "client-id" ]')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:11')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', 'NOT ', 'yiaddr', '192.168.50.10')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_client_id_negative():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.10',
                                           '0',
                                           'client-id',
                                           'ff:01:02:03:ff:11:22')
    # "host-reservation-identifiers": [ "hw-address", "duid", "circuit-id", "client-id" ]
    srv_control.add_line('"host-reservation-identifiers": [ "circuit-id", "duid", "hw-address" ]')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:33:44')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:11')
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:11:22')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', 'NOT ', 'yiaddr', '192.168.50.10')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_reserved_classes_1():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')

    srv_control.create_new_class('ipxe_efi_x64')
    srv_control.add_test_to_class('1', 'next-server', '192.0.2.254')
    srv_control.add_test_to_class('1', 'server-hostname', 'hal9000')
    srv_control.add_test_to_class('1', 'boot-file-name', '/dev/null')
    srv_control.add_option_to_defined_class('1', 'interface-mtu', '321')

    srv_control.add_line_to_subnet('0',
                                   ',"reservations": [{"hw-address": "aa:bb:cc:dd:ee:ff","ip-address": "192.168.50.10","client-classes": [ "ipxe_efi_x64" ]}]')
    srv_control.add_line('"host-reservation-identifiers": [ "hw-address" ]')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:55')
    srv_msg.client_requests_option('26')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', 'NOT ', '26')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'aa:bb:cc:dd:ee:ff')
    srv_msg.client_requests_option('26')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '26')
    srv_msg.response_check_option_content('Response', '26', None, 'value', '321')

    misc.test_procedure()
    srv_msg.client_requests_option('26')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'aa:bb:cc:dd:ee:ff')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option('Response', None, '26')
    srv_msg.response_check_option_content('Response', '26', None, 'value', '321')
    srv_msg.response_check_content('Response', None, 'siaddr', '192.0.2.254')
    srv_msg.response_check_content('Response', None, 'file', '/dev/null')
    srv_msg.response_check_content('Response', None, 'sname', 'hal9000')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_reserved_classes_2():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')

    srv_control.create_new_class('ipxe_efi_x64')
    srv_control.add_test_to_class('1', 'server-hostname', 'hal9000')
    srv_control.add_test_to_class('1', 'boot-file-name', '/dev/null')

    srv_control.create_new_class('class-abc')
    srv_control.add_test_to_class('2', 'next-server', '192.0.2.254')
    srv_control.add_option_to_defined_class('2', 'interface-mtu', '321')

    srv_control.add_line_to_subnet('0',
                                   ',"reservations": [{"hw-address": "aa:bb:cc:dd:ee:ff","ip-address": "192.168.50.10","client-classes": [ "ipxe_efi_x64", "class-abc" ]}]')
    srv_control.add_line('"host-reservation-identifiers": [ "hw-address" ]')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:55')
    srv_msg.client_requests_option('26')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', 'NOT ', '26')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'aa:bb:cc:dd:ee:ff')
    srv_msg.client_requests_option('26')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '26')
    srv_msg.response_check_option_content('Response', '26', None, 'value', '321')

    misc.test_procedure()
    srv_msg.client_requests_option('26')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'aa:bb:cc:dd:ee:ff')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option('Response', None, '26')
    srv_msg.response_check_option_content('Response', '26', None, 'value', '321')
    srv_msg.response_check_content('Response', None, 'siaddr', '192.0.2.254')
    srv_msg.response_check_content('Response', None, 'file', '/dev/null')
    srv_msg.response_check_content('Response', None, 'sname', 'hal9000')
