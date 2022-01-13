"""ISC_DHCP DHCPv4 Keywords"""

# pylint: disable=invalid-name,line-too-long

import pytest
import misc
import srv_control
import srv_msg

from softwaresupport.isc_dhcp6_server.functions import build_log_path, add_line_in_global


@pytest.mark.v4
@pytest.mark.dhcpd
def test_v4_dhcpd_keyword_use_host_decl_names_on_ddns():
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
    misc.test_setup()
    add_line_in_global('ping-check off;')
    add_line_in_global('use-host-decl-names on;')
    add_line_in_global('ddns-update-style interim;')
    add_line_in_global('ddns-updates on;')
    add_line_in_global('update-static-leases on;')
    add_line_in_global('ddns-domainname "four.example.com";')

    add_line_in_global('zone four.example.com. {')
    add_line_in_global('    primary 127.0.0.1;')
    add_line_in_global('}')

    add_line_in_global('subnet 178.16.1.0 netmask 255.255.255.0 {')
    add_line_in_global('    pool {')
    add_line_in_global('        range 178.16.1.100 178.16.1.101;')
    add_line_in_global('    }')
    add_line_in_global('}')

    add_line_in_global('host one {')
    add_line_in_global('    option dhcp-client-identifier "1111";')
    add_line_in_global('    fixed-address 178.16.1.201;')
    add_line_in_global('}')

    add_line_in_global('host two {')
    add_line_in_global('    option dhcp-client-identifier "2222";')
    add_line_in_global('    option host-name "two_opt";')
    add_line_in_global('    fixed-address 178.16.1.202;')
    add_line_in_global('}')

    add_line_in_global('host three {')
    add_line_in_global('    option dhcp-client-identifier "3333";')
    add_line_in_global('    option host-name "three_opt";')
    add_line_in_global('    fixed-address 178.16.1.203;')
    add_line_in_global('}')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # #######################################################################
    # # Case 1:
    # # Get a lease for fixed host which has no host-name option
    # # Server should send the host declarartion name back in to the client
    # # as the hostname option and use it in forward DNS name.
    # #######################################################################
    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '31:31:31:31')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '178.16.1.201')
    srv_msg.response_check_include_option(12)
    srv_msg.response_check_option_content(12, 'value', 'one')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '178.16.1.201')
    srv_msg.client_does_include_with_value('client_id', '31:31:31:31')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '178.16.1.201')
    srv_msg.log_contains('DDNS_STATE_ADD_FW_NXDOMAIN 178.16.1.201 for one.four.example.com',
                         log_file=build_log_path())

    # #######################################################################
    # # Case 2:
    # # Get a lease for fixed host which has a host-name option
    # # Server should send the hostname option defined in the host
    # # declarartion back to the client, and and use it in forward DNS name.
    # #######################################################################
    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '32:32:32:32')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '178.16.1.202')
    srv_msg.response_check_include_option(12)
    srv_msg.response_check_option_content(12, 'value', 'two_opt')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '178.16.1.202')
    srv_msg.client_does_include_with_value('client_id', '32:32:32:32')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '178.16.1.202')
    srv_msg.log_contains('DDNS_STATE_ADD_FW_NXDOMAIN 178.16.1.202 for two_opt.four.example.com',
                         log_file=build_log_path())

    # #######################################################################
    # # Case 3:
    # # Get a lease for fixed host has a host-name option, client sends hostname.
    # # Server should send back the hostname option defined in the host
    # # declaration but should use the hostname provided by the client in the
    # # forward DNS name.
    # #######################################################################
    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '33:33:33:33')
    srv_msg.client_does_include_with_value('hostname', 'clnt_host')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '178.16.1.203')
    srv_msg.response_check_include_option(12)
    srv_msg.response_check_option_content(12, 'value', 'three_opt')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '33:33:33:33')
    srv_msg.client_does_include_with_value('hostname', 'clnt_host')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '178.16.1.203')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '178.16.1.203')
    srv_msg.log_contains('DDNS_STATE_ADD_FW_NXDOMAIN 178.16.1.203 for clnt_host.four.example.com',
                         log_file=build_log_path())

    # #######################################################################
    # # Case 4:
    # # Get a lease for a dynamic client.
    # # Server should NOT send back a hostname option and should not attempt
    # # a DNS update.
    # #######################################################################
    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '34:34:34:34')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '178.16.1.100')
    # Response MUST NOT include option 12.

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '34:34:34:34')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '178.16.1.100')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '178.16.1.100')
    srv_msg.log_doesnt_contain('DDNS_STATE_ADD_FW_NXDOMAIN 178.16.1.100', log_file=build_log_path())

    # #######################################################################
    # # Case 5:
    # # Get a lease for a dynamic client that sends hostname option.
    # # Server should NOT send back a hostname option and should not attempt
    # # a DNS update.
    # #######################################################################

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '34:34:34:34')
    srv_msg.client_does_include_with_value('hostname', 'clnt_host')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '178.16.1.100')
    srv_msg.response_check_include_option(12, expect_include=False)

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '34:34:34:34')
    srv_msg.client_does_include_with_value('hostname', 'clnt_host')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '178.16.1.100')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '178.16.1.100')
    srv_msg.log_contains('DDNS_STATE_ADD_FW_NXDOMAIN 178.16.1.100 for clnt_host.four.example.com',
                         log_file=build_log_path())
