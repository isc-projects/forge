"""Kea6 User Check Hook Library"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_msg
import srv_control
import misc


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.user_check
@pytest.mark.vendor_options
def test_user_check_hook_vendor_options_all():

    # Install the requisite user registry file onto the server and then
    # Configure the server with two subnets.  The first subnet will be used
    # for registeted users, the second for unregistered users.
    misc.test_setup()
    srv_msg.send_file_to_server('tests/dhcpv6/kea_only/user_chk/registry_1.txt',
                                '/tmp/user_chk_registry.txt')
    srv_msg.remove_file_from_server('/tmp/user_chk_outcome.txt')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::20')
    srv_control.config_srv_another_subnet_no_interface('1000:1::/64', '1000:1::5-1000:1::5')
    srv_control.add_hooks('libdhcp_user_chk.so')
    srv_control.config_srv_opt_space('vendor-4491', 'tftp-servers', '7000::1')
    srv_control.config_srv_opt_space('vendor-4491', 'config-file', 'bootfile.from.server')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    #
    # Send a query from an unknown user
    #
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption('Client', '1', '32')
    srv_msg.add_vendor_suboption('Client', '1', '33')
    srv_msg.client_does_include('Client', None, 'vendor-specific-info')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    # We don't really care about the address value
    # Options should come from default user in registry
    srv_msg.response_check_include_option('Response', None, '17')
    srv_msg.response_check_option_content('Response', '17', None, 'sub-option', '32')
    # Response sub-option 32 from option 17 MUST contain tftp-servers 9000::1.
    srv_msg.response_check_option_content('Response', '17', None, 'sub-option', '33')
    srv_msg.response_check_suboption_content('Response',
                                             '33',
                                             '17',
                                             None,
                                             'config-file',
                                             'bootfile.from.default')

    #
    # Send a query from a registered user with no properties
    #
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:11:02:03:04:05:06')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption('Client', '1', '32')
    srv_msg.add_vendor_suboption('Client', '1', '33')
    srv_msg.client_does_include('Client', None, 'vendor-specific-info')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    # We don't really care about the address value
    # Options should come from server config
    srv_msg.response_check_include_option('Response', None, '17')
    srv_msg.response_check_option_content('Response', '17', None, 'sub-option', '32')
    # Response sub-option 32 from option 17 MUST contain tftp-servers 7000::1.
    srv_msg.response_check_option_content('Response', '17', None, 'sub-option', '33')
    srv_msg.response_check_suboption_content('Response',
                                             '33',
                                             '17',
                                             None,
                                             'config-file',
                                             'bootfile.from.server')

    #
    # Send a query from a registered user who supplies only bootfile
    #
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:22:02:03:04:05:06')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption('Client', '1', '32')
    srv_msg.add_vendor_suboption('Client', '1', '33')
    srv_msg.client_does_include('Client', None, 'vendor-specific-info')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    # We don't really care about the address value
    # bootfile should be from user, tftp server from server config
    srv_msg.response_check_include_option('Response', None, '17')
    srv_msg.response_check_option_content('Response', '17', None, 'sub-option', '32')
    # Response sub-option 32 from option 17 MUST contain tftp-servers 7000::1.
    srv_msg.response_check_option_content('Response', '17', None, 'sub-option', '33')
    srv_msg.response_check_suboption_content('Response',
                                             '33',
                                             '17',
                                             None,
                                             'config-file',
                                             'bootfile.from.user')

    #
    # Send a query from a registered user who supplies only tftp server
    #
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:33:02:03:04:05:06')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption('Client', '1', '32')
    srv_msg.add_vendor_suboption('Client', '1', '33')
    srv_msg.client_does_include('Client', None, 'vendor-specific-info')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    # We don't really care about the address value
    # bootfile should be from server config, tftp server from user
    srv_msg.response_check_include_option('Response', None, '17')
    srv_msg.response_check_option_content('Response', '17', None, 'sub-option', '32')
    # Response sub-option 32 from option 17 MUST contain tftp-servers 8000::1.
    srv_msg.response_check_option_content('Response', '17', None, 'sub-option', '33')
    srv_msg.response_check_suboption_content('Response',
                                             '33',
                                             '17',
                                             None,
                                             'config-file',
                                             'bootfile.from.server')

    misc.test_procedure()
    # Send a query from a registered user who supplies both tftp server and bootfile
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:44:02:03:04:05:06')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption('Client', '1', '32')
    srv_msg.add_vendor_suboption('Client', '1', '33')
    srv_msg.client_does_include('Client', None, 'vendor-specific-info')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    # We don't really care about the address value
    # tftp server and bootfile should be from user
    srv_msg.response_check_include_option('Response', None, '17')
    srv_msg.response_check_option_content('Response', '17', None, 'sub-option', '32')
    # Response sub-option 32 from option 17 MUST contain tftp-servers 8002::1.
    srv_msg.response_check_option_content('Response', '17', None, 'sub-option', '33')
    srv_msg.response_check_suboption_content('Response',
                                             '33',
                                             '17',
                                             None,
                                             'config-file',
                                             'bootfile.from.user-2')
