"""Kea6 User Check Hook Library - Logging"""

# pylint: disable=invalid-name,line-too-long

import glob
import pytest

from src import misc
from src import srv_control
from src import srv_msg


@pytest.mark.v6
@pytest.mark.user_check
@pytest.mark.IA_NA
@pytest.mark.logging
def test_user_check_hook_IA_NA_no_registry_logging():
    # Without a user registry and multiple subnets
    # Subnet selection will use subnet interface for subnet selection hint

    misc.test_setup()
    srv_msg.remove_file_from_server('/tmp/user_chk_registry.txt')
    srv_msg.remove_file_from_server('/tmp/user_chk_outcome.txt')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::5')
    srv_control.config_srv_another_subnet_no_interface('1000::/64', '1000::5-1000::5')
    srv_control.add_hooks('libdhcp_user_chk.so')
    srv_control.configure_loggers('kea-dhcp6.callouts', 'ERROR', 'None')
    srv_control.configure_loggers('kea-dhcp6.hooks', 'ERROR', 'None')
    srv_control.build_and_send_config_files()
    srv_control.start_srv_during_process('DHCP', 'configuration')

    # DHCP server is started.
    #
    # Test Procedure:
    # Client does include client-id.
    # Client does include IA_Address.
    # Client does include IA-NA.
    # Client sends SOLICIT message.
    #
    # Pass Criteria:
    # Server MUST respond with ADVERTISE message.
    # Response MUST include option 3.
    # Response option 3 MUST contain sub-option 5.
    # Response sub-option 5 from option 3 MUST contain address 3000::5.
    # File stored in kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp6.hooks
    # File stored in kea.log MUST contain line or phrase: ERROR \[kea-dhcp6.hooks
    # File stored in kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp6.callouts


@pytest.mark.v6
@pytest.mark.user_check
@pytest.mark.IA_NA
@pytest.mark.logging
def test_user_check_hook_IA_NA_with_registry_unknown_user_logging():
    # With a user registry and multiple subnets
    # an unknown user should get last subnet

    misc.test_setup()
    srv_msg.send_file_to_server(glob.glob("**/v6_registry_1.txt", recursive=True)[0],
                                '/tmp/user_chk_registry.txt')
    srv_msg.remove_file_from_server('/tmp/user_chk_outcome.txt')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::5')
    srv_control.config_srv_another_subnet_no_interface('1000::/64', '1000::5-1000::5')
    srv_control.add_hooks('libdhcp_user_chk.so')
    srv_control.configure_loggers('kea-dhcp6.callouts', 'DEBUG', 99)
    srv_control.configure_loggers('kea-dhcp6.hooks', 'INFO', 'None')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    # Send a query from an unregistered user
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '1000::5')
    # Check the outcome file for correct content
    srv_msg.copy_remote('/tmp/user_chk_outcome.txt')
    srv_msg.compare_file(glob.glob("**/v6_outcome_1.txt", recursive=True)[0])
    srv_msg.log_contains(r'INFO  \[kea-dhcp6.hooks')
    srv_msg.log_contains(r'DEBUG \[kea-dhcp6.callouts')


@pytest.mark.v6
@pytest.mark.user_check
@pytest.mark.IA_NA
@pytest.mark.logging
def test_user_check_hook_IA_NA_with_registry_unknown_user_logging_2():
    # With a user registry and multiple subnets
    # an unknown user should get last subnet

    misc.test_setup()
    srv_msg.send_file_to_server(glob.glob("**/v6_registry_1.txt", recursive=True)[0],
                                '/tmp/user_chk_registry.txt')
    srv_msg.remove_file_from_server('/tmp/user_chk_outcome.txt')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::5')
    srv_control.config_srv_another_subnet_no_interface('1000::/64', '1000::5-1000::5')
    srv_control.add_hooks('libdhcp_user_chk.so')
    # Server logging system is configured with logger type kea-dhcp4.callouts, severity DEBUG, severity level 99 and log file kea.log.
    # Server logging system is configured with logger type kea-dhcp4.hooks, severity INFO, severity level None and log file kea.log.
    srv_control.configure_loggers('kea-dhcp6.callouts', 'DEBUG', 99)
    srv_control.configure_loggers('kea-dhcp6.hooks', 'DEBUG', 99)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    # Send a query from an unregistered user
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '1000::5')
    # Check the outcome file for correct content
    srv_msg.copy_remote('/tmp/user_chk_outcome.txt')
    # File stored in kea.log MUST contain line or phrase: INFO  \[kea-dhcp6.hooks
    # File stored in kea.log MUST contain line or phrase: DEBUG \[kea-dhcp6.callouts
    srv_msg.compare_file(glob.glob("**/v6_outcome_1.txt", recursive=True)[0])

    srv_msg.forge_sleep(10, 'seconds')

    srv_control.start_srv('DHCP', 'stopped')
    misc.test_setup()
    srv_msg.remove_file_from_server('/tmp/user_chk_outcome.txt')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::5')
    srv_control.config_srv_another_subnet_no_interface('1000::/64', '1000::5-1000::5')
    srv_control.add_hooks('libdhcp_user_chk.so')
    srv_control.configure_loggers('kea-dhcp6.callouts', 'DEBUG', 99)
    srv_control.configure_loggers('kea-dhcp6.hooks', 'INFO', 'None')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    # Send a query from an unregistered user
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '1000::5')
    # Check the outcome file for correct content
    srv_msg.copy_remote('/tmp/user_chk_outcome.txt')
    # That test works, we don't need last step:
    # Client compares downloaded file from server with local file v6_outcome_1.txt.
    # srv_msg.compare_file(glob.glob("**/v6_outcome_1.txt", recursive=True)[0])


@pytest.mark.v6
@pytest.mark.user_check
@pytest.mark.vendor_options
def test_user_check_hook_vendor_options_all():

    # Install the requisite user registry file onto the server and then
    # Configure the server with two subnets.  The first subnet will be used
    # for registeted users, the second for unregistered users.
    misc.test_setup()
    srv_msg.send_file_to_server(glob.glob("**/v6_registry_1.txt", recursive=True)[0],
                                '/tmp/user_chk_registry.txt')
    srv_msg.remove_file_from_server('/tmp/user_chk_outcome.txt')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::20')
    srv_control.config_srv_another_subnet_no_interface('1000:1::/64', '1000:1::5-1000:1::5')
    srv_control.add_hooks('libdhcp_user_chk.so')
    srv_control.config_srv_opt_space('vendor-4491', 'tftp-servers', '7000::1')
    srv_control.config_srv_opt_space('vendor-4491', 'config-file', 'bootfile.from.server')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    #
    # Send a query from an unknown user
    #
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1, 32)
    srv_msg.add_vendor_suboption('Client', 1, 33)
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # We don't really care about the address value
    # Options should come from default user in registry
    srv_msg.response_check_include_option(17)
    srv_msg.response_check_option_content(17, 'sub-option', 32)
    # Response sub-option 32 from option 17 MUST contain tftp-servers 9000::1.
    srv_msg.response_check_option_content(17, 'sub-option', 33)
    srv_msg.response_check_suboption_content(33, 17, 'config-file', 'bootfile.from.default')

    #
    # Send a query from a registered user with no properties
    #
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:11:02:03:04:05:06')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1, 32)
    srv_msg.add_vendor_suboption('Client', 1, 33)
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # We don't really care about the address value
    # Options should come from server config
    srv_msg.response_check_include_option(17)
    srv_msg.response_check_option_content(17, 'sub-option', 32)
    # Response sub-option 32 from option 17 MUST contain tftp-servers 7000::1.
    srv_msg.response_check_option_content(17, 'sub-option', 33)
    srv_msg.response_check_suboption_content(33, 17, 'config-file', 'bootfile.from.server')

    #
    # Send a query from a registered user who supplies only bootfile
    #
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:22:02:03:04:05:06')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1, 32)
    srv_msg.add_vendor_suboption('Client', 1, 33)
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # We don't really care about the address value
    # bootfile should be from user, tftp server from server config
    srv_msg.response_check_include_option(17)
    srv_msg.response_check_option_content(17, 'sub-option', 32)
    # Response sub-option 32 from option 17 MUST contain tftp-servers 7000::1.
    srv_msg.response_check_option_content(17, 'sub-option', 33)
    srv_msg.response_check_suboption_content(33, 17, 'config-file', 'bootfile.from.user')

    #
    # Send a query from a registered user who supplies only tftp server
    #
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:33:02:03:04:05:06')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1, 32)
    srv_msg.add_vendor_suboption('Client', 1, 33)
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # We don't really care about the address value
    # bootfile should be from server config, tftp server from user
    srv_msg.response_check_include_option(17)
    srv_msg.response_check_option_content(17, 'sub-option', 32)
    # Response sub-option 32 from option 17 MUST contain tftp-servers 8000::1.
    srv_msg.response_check_option_content(17, 'sub-option', 33)
    srv_msg.response_check_suboption_content(33, 17, 'config-file', 'bootfile.from.server')

    misc.test_procedure()
    # Send a query from a registered user who supplies both tftp server and bootfile
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:44:02:03:04:05:06')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1, 32)
    srv_msg.add_vendor_suboption('Client', 1, 33)
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # We don't really care about the address value
    # tftp server and bootfile should be from user
    srv_msg.response_check_include_option(17)
    srv_msg.response_check_option_content(17, 'sub-option', 32)
    # Response sub-option 32 from option 17 MUST contain tftp-servers 8002::1.
    srv_msg.response_check_option_content(17, 'sub-option', 33)
    srv_msg.response_check_suboption_content(33, 17, 'config-file', 'bootfile.from.user-2')
