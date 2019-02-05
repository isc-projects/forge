"""Kea6 User Check Hook Library - Logging"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_control
from features import srv_msg
from features import misc


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.user_check
@pytest.mark.IA_NA
@pytest.mark.logging
def test_user_check_hook_IA_NA_no_registry_logging(step):
    # Without a user registry and multiple subnets
    # Subnet selection will use subnet interface for subnet selection hint

    misc.test_setup(step)
    srv_msg.remove_file_from_server(step, '/tmp/user_chk_registry.txt')
    srv_msg.remove_file_from_server(step, '/tmp/user_chk_outcome.txt')
    srv_control.config_srv_subnet(step, '3000::/64', '3000::5-3000::5')
    srv_control.config_srv_another_subnet_no_interface(step, '1000::/64', '1000::5-1000::5')
    srv_control.configure_loggers(step, 'kea-dhcp6.callouts', 'ERROR', 'None', 'kea.log')
    srv_control.configure_loggers(step, 'kea-dhcp6.hooks', 'ERROR', 'None', 'kea.log')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_user_chk.so')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

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
    # File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp6.hooks
    # File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST contain line or phrase: ERROR \[kea-dhcp6.hooks
    # File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp6.callouts


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.user_check
@pytest.mark.IA_NA
@pytest.mark.logging
def test_user_check_hook_IA_NA_with_registry_unknown_user_logging(step):
    # With a user registry and multiple subnets
    # an unknown user should get last subnet

    misc.test_setup(step)
    srv_msg.send_file_to_server(step,
                                'features/dhcpv6/server/kea_only/user_chk/registry_1.txt',
                                '/tmp/user_chk_registry.txt')
    srv_msg.remove_file_from_server(step, '/tmp/user_chk_outcome.txt')
    srv_control.config_srv_subnet(step, '3000::/64', '3000::5-3000::5')
    srv_control.config_srv_another_subnet_no_interface(step, '1000::/64', '1000::5-1000::5')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_user_chk.so')
    srv_control.configure_loggers(step, 'kea-dhcp6.callouts', 'DEBUG', '99', 'kea.log')
    srv_control.configure_loggers(step, 'kea-dhcp6.hooks', 'INFO', 'None', 'kea.log')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    # Send a query from an unregistered user
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '1000::5')
    # Check the outcome file for correct content
    srv_msg.copy_remote(step, '/tmp/user_chk_outcome.txt')
    srv_msg.compare_file(step, 'features/dhcpv6/server/kea_only/user_chk/outcome_1.txt')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'INFO  \[kea-dhcp6.hooks')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'DEBUG \[kea-dhcp6.callouts')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.user_check
@pytest.mark.IA_NA
@pytest.mark.logging
def test_user_check_hook_IA_NA_with_registry_unknown_user_logging_2(step):
    # With a user registry and multiple subnets
    # an unknown user should get last subnet

    misc.test_setup(step)
    srv_msg.send_file_to_server(step,
                                'features/dhcpv6/server/kea_only/user_chk/registry_1.txt',
                                '/tmp/user_chk_registry.txt')
    srv_msg.remove_file_from_server(step, '/tmp/user_chk_outcome.txt')
    srv_control.config_srv_subnet(step, '3000::/64', '3000::5-3000::5')
    srv_control.config_srv_another_subnet_no_interface(step, '1000::/64', '1000::5-1000::5')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_user_chk.so')
    srv_control.configure_loggers(step, 'kea-dhcp6.callouts', 'DEBUG', '99', 'kea.log')
    srv_control.configure_loggers(step, 'kea-dhcp6.hooks', 'DEBUG', '99', 'kea.log')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    # DHCP server failed to start. During configuration process.
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    # Send a query from an unregistered user
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '1000::5')
    # Check the outcome file for correct content
    srv_msg.copy_remote(step, '/tmp/user_chk_outcome.txt')
    srv_msg.compare_file(step, 'features/dhcpv6/server/kea_only/user_chk/outcome_1.txt')

    srv_msg.forge_sleep(step, '10', 'seconds')

    srv_control.start_srv(step, 'DHCP', 'stopped')
    misc.test_setup(step)
    srv_msg.remove_file_from_server(step, '/tmp/user_chk_outcome.txt')
    srv_control.config_srv_subnet(step, '3000::/64', '3000::5-3000::5')
    srv_control.config_srv_another_subnet_no_interface(step, '1000::/64', '1000::5-1000::5')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_user_chk.so')
    srv_control.configure_loggers(step, 'kea-dhcp6.callouts', 'DEBUG', '99', 'kea.log')
    srv_control.configure_loggers(step, 'kea-dhcp6.hooks', 'INFO', 'None', 'kea.log')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    # Send a query from an unregistered user
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '1000::5')
    # Check the outcome file for correct content
    srv_msg.copy_remote(step, '/tmp/user_chk_outcome.txt')
    # That test works, we don't need last step:
    # Client compares downloaded file from server with local file stored in: features/dhcpv6/server/kea_only/user_chk/outcome_1.txt. # pylint: disable=line-too-long
