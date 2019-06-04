"""Kea6 User Check Hook Library"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_control
import misc
import srv_msg


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.user_check
@pytest.mark.IA_NA
def test_user_check_hook_IA_NA_no_registry():
    # Without a user registry and multiple subnets
    # Subnet selection will use subnet interface for subnet selection hint

    misc.test_setup()
    srv_msg.remove_file_from_server('/tmp/user_chk_registry.txt')
    srv_msg.remove_file_from_server('/tmp/user_chk_outcome.txt')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::5')
    srv_control.config_srv_another_subnet_no_interface('1000::/64', '1000::5-1000::5')
    srv_control.add_hooks('libdhcp_user_chk.so')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv_during_process('DHCP', 'configuration')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.user_check
@pytest.mark.IA_NA
def test_user_check_hook_IA_NA_with_registry_unknown_user():
    # With a user registry and multiple subnets
    # an unknown user should get last subnet

    misc.test_setup()
    srv_msg.send_file_to_server('tests/dhcpv6/kea_only/user_chk/registry_1.txt',
                                '/tmp/user_chk_registry.txt')
    srv_msg.remove_file_from_server('/tmp/user_chk_outcome.txt')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::5')
    srv_control.config_srv_another_subnet_no_interface('1000::/64', '1000::5-1000::5')
    srv_control.add_hooks('libdhcp_user_chk.so')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    # Send a query from an unregistered user
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '1000::5')
    # Check the outcome file for correct content
    srv_msg.copy_remote('/tmp/user_chk_outcome.txt')
    srv_msg.compare_file('tests/dhcpv6/kea_only/user_chk/outcome_1.txt')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.user_check
@pytest.mark.IA_NA
def test_user_check_hook_IA_NA_with_registry_known_user():
    # With a user registry and multiple subnets
    # an known user should get first subnet

    misc.test_setup()
    srv_msg.send_file_to_server('tests/dhcpv6/kea_only/user_chk/registry_1.txt',
                                '/tmp/user_chk_registry.txt')
    srv_msg.remove_file_from_server('/tmp/user_chk_outcome.txt')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::5')
    srv_control.config_srv_another_subnet_no_interface('1000::/64', '1000::5-1000::5')
    srv_control.add_hooks('libdhcp_user_chk.so')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    # Send a query from a registered user
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:11:02:03:04:05:06')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::5')
    # Check the outcome file for correct content
    srv_msg.copy_remote('/tmp/user_chk_outcome.txt')
    srv_msg.compare_file('tests/dhcpv6/kea_only/user_chk/outcome_2.txt')
