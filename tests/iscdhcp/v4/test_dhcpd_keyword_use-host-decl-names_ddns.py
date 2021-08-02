"""ISC_DHCP DHCPv4 Keywords"""


import sys
if 'features' not in sys.path:
    sys.path.append('features')

if 'pytest' in sys.argv[0]:
    import pytest
else:
    import lettuce as pytest

import misc
import srv_control
import srv_msg


@pytest.mark.py_test
@pytest.mark.v4
@pytest.mark.dhcpd
@pytest.mark.keyword
@pytest.mark.use_host_decl_names
@pytest.mark.ddns
def test_v4_dhcpd_keyword_use_host_decl_names_on_ddns(step):
    """new-v4.dhcpd.keyword.use-host-decl-names-on.ddns"""
    # # Tests use-host-decl-names enabled in conjunction with ddns updates
    # # The  test consists of a single server configuration and instance which
    # # is used to execute the following test cases:
    # #
    # # Case 1:
    # # Get a lease for fixed host which has no host-name option.
    # # Server should send the host declarartion name back in to the client
    # # as the hostname option and use it in forward DNS name.
    # #
    # # Case 2:
    # # Get a lease for fixed host which has a host-name option.
    # # Server should send the hostname option defined in the host
    # # declarartion back to the client, and and use it in forward DNS name.
    # #
    # # Case 3:
    # # Get a lease for fixed host has a host-name option, client sends hostname.
    # # Server should send back the hostname option defined in the host
    # # declaration but should use the hostname provided by the client in the
    # # forward DNS name.
    # #
    # # Case 4:
    # # Get a lease for a dynamic client.
    # # Server should NOT send back a hostname option and should not attempt
    # # a DNS update.
    # #
    # # Case 5:
    # # Get a lease for a dynamic client that sends hostname option.
    # # Server should NOT send back a hostname option and should not attempt
    # # a DNS update.
    # #
    # # NOTE: Currently Scapy does not support FQDN option for DHCPv4. Use of
    # # FQDN as the source for DDNS forward name cannot be tested via Forge
    # # at this time.
    # #
    misc.test_setup(step)
    srv_control.run_command(step, 'ping-check off;')
    srv_control.run_command(step, 'use-host-decl-names on;')
    srv_control.run_command(step, 'ddns-update-style interim;')
    srv_control.run_command(step, 'ddns-updates on;')
    srv_control.run_command(step, 'update-static-leases on;')
    srv_control.run_command(step, 'ddns-domainname "four.example.com";')

    srv_control.run_command(step, 'zone four.example.com. {')
    srv_control.run_command(step, '    primary 127.0.0.1;')
    srv_control.run_command(step, '}')

    srv_control.run_command(step, 'subnet 178.16.1.0 netmask 255.255.255.0 {')
    srv_control.run_command(step, '    pool {')
    srv_control.run_command(step, '        range 178.16.1.100 178.16.1.101;')
    srv_control.run_command(step, '    }')
    srv_control.run_command(step, '}')

    srv_control.run_command(step, 'host one {')
    srv_control.run_command(step, '    option dhcp-client-identifier "1111";')
    srv_control.run_command(step, '    fixed-address 178.16.1.201;')
    srv_control.run_command(step, '}')

    srv_control.run_command(step, 'host two {')
    srv_control.run_command(step, '    option dhcp-client-identifier "2222";')
    srv_control.run_command(step, '    option host-name "two_opt";')
    srv_control.run_command(step, '    fixed-address 178.16.1.202;')
    srv_control.run_command(step, '}')

    srv_control.run_command(step, 'host three {')
    srv_control.run_command(step, '    option dhcp-client-identifier "3333";')
    srv_control.run_command(step, '    option host-name "three_opt";')
    srv_control.run_command(step, '    fixed-address 178.16.1.203;')
    srv_control.run_command(step, '}')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # #######################################################################
    # # Case 1:
    # # Get a lease for fixed host which has no host-name option
    # # Server should send the host declarartion name back in to the client
    # # as the hostname option and use it in forward DNS name.
    # #######################################################################
    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', '31:31:31:31')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.201')
    srv_msg.response_check_include_option(step, 'Response', None, '12')
    srv_msg.response_check_option_content(step, 'Response', '12', None, 'value', 'one')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '178.16.1.201')
    srv_msg.client_does_include_with_value(step, 'client_id', '31:31:31:31')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.201')
    srv_msg.log_contains_line(step,
                              'DHCP',
                              None,
                              'DDNS_STATE_ADD_FW_NXDOMAIN 178.16.1.201 for one.four.example.com')

    # #######################################################################
    # # Case 2:
    # # Get a lease for fixed host which has a host-name option
    # # Server should send the hostname option defined in the host
    # # declarartion back to the client, and and use it in forward DNS name.
    # #######################################################################
    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', '32:32:32:32')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.202')
    srv_msg.response_check_include_option(step, 'Response', None, '12')
    srv_msg.response_check_option_content(step, 'Response', '12', None, 'value', 'two_opt')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '178.16.1.202')
    srv_msg.client_does_include_with_value(step, 'client_id', '32:32:32:32')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.202')
    srv_msg.log_contains_line(step,
                              'DHCP',
                              None,
                              'DDNS_STATE_ADD_FW_NXDOMAIN 178.16.1.202 for two_opt.four.example.com')

    # #######################################################################
    # # Case 3:
    # # Get a lease for fixed host has a host-name option, client sends hostname.
    # # Server should send back the hostname option defined in the host
    # # declaration but should use the hostname provided by the client in the
    # # forward DNS name.
    # #######################################################################
    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', '33:33:33:33')
    srv_msg.client_does_include_with_value(step, 'hostname', 'clnt_host')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.203')
    srv_msg.response_check_include_option(step, 'Response', None, '12')
    srv_msg.response_check_option_content(step, 'Response', '12', None, 'value', 'three_opt')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', '33:33:33:33')
    srv_msg.client_does_include_with_value(step, 'hostname', 'clnt_host')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '178.16.1.203')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.203')
    srv_msg.log_contains_line(step,
                              'DHCP',
                              None,
                              'DDNS_STATE_ADD_FW_NXDOMAIN 178.16.1.203 for clnt_host.four.example.com')

    # #######################################################################
    # # Case 4:
    # # Get a lease for a dynamic client.
    # # Server should NOT send back a hostname option and should not attempt
    # # a DNS update.
    # #######################################################################
    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', '34:34:34:34')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.100')
    # Response MUST NOT include option 12.

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', '34:34:34:34')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '178.16.1.100')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.100')
    srv_msg.log_contains_line(step, 'DHCP', 'NOT ', 'DDNS_STATE_ADD_FW_NXDOMAIN 178.16.1.100')

    # #######################################################################
    # # Case 5:
    # # Get a lease for a dynamic client that sends hostname option.
    # # Server should NOT send back a hostname option and should not attempt
    # # a DNS update.
    # #######################################################################
    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', '34:34:34:34')
    srv_msg.client_does_include_with_value(step, 'hostname', 'clnt_host')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.100')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '12')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', '34:34:34:34')
    srv_msg.client_does_include_with_value(step, 'hostname', 'clnt_host')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '178.16.1.100')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.100')
    srv_msg.log_contains_line(step,
                              'DHCP',
                              None,
                              'DDNS_STATE_ADD_FW_NXDOMAIN 178.16.1.100 for clnt_host.four.example.com')



