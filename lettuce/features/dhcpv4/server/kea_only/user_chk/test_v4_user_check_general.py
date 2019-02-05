"""Kea6 User Check Hook Library"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import misc
from features import srv_control
from features import srv_msg


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.user_check
def test_user_check_IA_NA_no_registry(step):
    # Without a user registry and multiple subnets
    # Subnet selection will use subnet interface for subnet selection hint

    misc.test_setup(step)
    srv_msg.remove_file_from_server(step, '/tmp/user_chk_registry.txt')
    srv_msg.remove_file_from_server(step, '/tmp/user_chk_outcome.txt')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.config_srv_another_subnet_no_interface(step, '10.0.0.0/24', '10.0.0.5-10.0.0.5')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_user_chk.so')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

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
def test_user_check_IA_NA_with_registry_unknown_user(step):
    # With a user registry and multiple subnets
    # an unknown user should get last subnet

    misc.test_setup(step)
    srv_msg.send_file_to_server(step,
                                'features/dhcpv4/server/kea_only/user_chk/registry_1.txt',
                                '/tmp/user_chk_registry.txt')
    srv_msg.remove_file_from_server(step, '/tmp/user_chk_outcome.txt')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.config_srv_another_subnet_no_interface(step, '10.0.0.0/24', '10.0.0.5-10.0.0.5')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_user_chk.so')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '0c:0e:0a:01:ff:01')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '10.0.0.5')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    # Check the outcome file for correct content
    srv_msg.copy_remote(step, '/tmp/user_chk_outcome.txt')
    srv_msg.compare_file(step, 'features/dhcpv4/server/kea_only/user_chk/outcome_1.txt')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.kea_only
@pytest.mark.user_check
def test_user_check_IA_NA_with_registry_known_user(step):
    # With a user registry and multiple subnets
    # an known user should get first subnet

    misc.test_setup(step)
    srv_msg.send_file_to_server(step,
                                'features/dhcpv4/server/kea_only/user_chk/registry_1.txt',
                                '/tmp/user_chk_registry.txt')
    srv_msg.remove_file_from_server(step, '/tmp/user_chk_outcome.txt')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.config_srv_another_subnet_no_interface(step, '10.0.0.0/24', '10.0.0.5-10.0.0.5')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_user_chk.so')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '0c:0e:0a:01:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.5')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    # Check the outcome file for correct content
    srv_msg.copy_remote(step, '/tmp/user_chk_outcome.txt')
    srv_msg.compare_file(step, 'features/dhcpv4/server/kea_only/user_chk/outcome_2.txt')
