"""Kea6 User Check Hook Library"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_control
import srv_msg
import misc


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.user_check
def test_user_check_IA_NA_no_registry():
    # Without a user registry and multiple subnets
    # Subnet selection will use subnet interface for subnet selection hint

    misc.test_setup()
    srv_msg.remove_file_from_server('/tmp/user_chk_registry.txt')
    srv_msg.remove_file_from_server('/tmp/user_chk_outcome.txt')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.config_srv_another_subnet_no_interface('10.0.0.0/24', '10.0.0.5-10.0.0.5')
    srv_control.add_hooks('libdhcp_user_chk.so')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv_during_process('DHCP', 'configuration')

    # Test Procedure:
    # Client requests option 1.
    # Client sends DISCOVER message.
    #
    # Pass Criteria:
    # Server MUST respond with OFFER message.
    # Response MUST include option 1.
    # Response MUST contain yiaddr 192.168.50.5.
    # Response option 1 MUST contain value 255.255.255.0.
    #
    # Test Procedure:
    # Client copies server_id option from received message.
    # Client adds to the message requested_addr with value 192.168.50.5.
    # Client requests option 1.
    # Client sends REQUEST message.
    #
    # Pass Criteria:
    # Server MUST respond with ACK message.
    # Client download file from server stored in: /tmp/user_chk_outcome.txt.
    # Client download file from server stored in: /tmp/user_chk_registry.txt.


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.user_check
def test_user_check_IA_NA_with_registry_unknown_user():
    # With a user registry and multiple subnets
    # an unknown user should get last subnet

    misc.test_setup()
    srv_msg.send_file_to_server('tests/dhcpv4/kea_only/user_chk/registry_1.txt',
                                '/tmp/user_chk_registry.txt')
    srv_msg.remove_file_from_server('/tmp/user_chk_outcome.txt')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.config_srv_another_subnet_no_interface('10.0.0.0/24', '10.0.0.5-10.0.0.5')
    srv_control.add_hooks('libdhcp_user_chk.so')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_sets_value('Client', 'chaddr', '0c:0e:0a:01:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '10.0.0.5')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    # Check the outcome file for correct content
    srv_msg.copy_remote('/tmp/user_chk_outcome.txt')
    srv_msg.compare_file('tests/dhcpv4/kea_only/user_chk/outcome_1.txt')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.user_check
def test_user_check_IA_NA_with_registry_known_user():
    # With a user registry and multiple subnets
    # an known user should get first subnet

    misc.test_setup()
    srv_msg.send_file_to_server('tests/dhcpv4/kea_only/user_chk/registry_1.txt',
                                '/tmp/user_chk_registry.txt')
    srv_msg.remove_file_from_server('/tmp/user_chk_outcome.txt')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.config_srv_another_subnet_no_interface('10.0.0.0/24', '10.0.0.5-10.0.0.5')
    srv_control.add_hooks('libdhcp_user_chk.so')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_sets_value('Client', 'chaddr', '0c:0e:0a:01:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.5')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    # Check the outcome file for correct content
    srv_msg.copy_remote('/tmp/user_chk_outcome.txt')
    srv_msg.compare_file('tests/dhcpv4/kea_only/user_chk/outcome_2.txt')
