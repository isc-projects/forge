"""ISC_DHCP DHCPv4 Keywords"""

# pylint: disable=invalid-name,line-too-long

import pytest
import misc
import srv_control
import srv_msg

from softwaresupport.isc_dhcp6_server.functions import build_log_path, add_line_in_global


@pytest.mark.v4
@pytest.mark.dhcpd
def test_v4_dhcpd_keyword_dhcp_cache_threshold_billing_class():
    """new-v4.dhcpd.keyword.dhcp-cache-threshold.billing_class"""
    # # Verifies that cache-threshold logic takes billing class
    # # into account. In short, if the billing class associated with a
    # # lease changes it must be superseded, not resused.
    # #
    # # Setup:
    # # Client gets initial lease, with no billing class.
    # #
    # # Case 1:
    # # Client adds vendor-class-id when renewing with DORA before the
    # # threshold expires.
    # # - Server maps client to billing class and should NOT resuse the lease
    # #
    # # Case 2:
    # # Client uses same vendor-class-id and renews with DORA before the
    # # threshold expires.
    # # - Server should reuse the lease
    # #
    # # Case 3:
    # # Client uses same vendor-class-id and renews with RA before the
    # # threshold expires.
    # # - Server should reuse the lease
    # #
    # # Case 4:
    # # Client changes vendor-class-id when renewing with DORA before the
    # # threshold expires.
    # # - Server maps client to different billing class and should NOT
    # # resuse the lease
    # #
    misc.test_setup()
    add_line_in_global(' ping-check off;')
    add_line_in_global(' ddns-updates off;')
    add_line_in_global(' max-lease-time 50;')
    add_line_in_global(' default-lease-time 50;')
    add_line_in_global(' subnet 192.168.50.0 netmask 255.255.255.0 {')
    add_line_in_global('     authoritative;')
    add_line_in_global('     pool {')
    add_line_in_global('         range 192.168.50.100 192.168.50.101;')
    add_line_in_global('     }')
    add_line_in_global(' }')
    add_line_in_global(' dhcp-cache-threshold 20;')
    add_line_in_global(' class "vnd1001" {')
    add_line_in_global('    match if (option vendor-class-identifier = "vnd1001");')
    add_line_in_global('    lease limit 4;')
    add_line_in_global('}')
    add_line_in_global('class "vnd1003" {')
    add_line_in_global('    match if (option vendor-class-identifier = "vnd1003");')
    add_line_in_global('    lease limit 4;')
    add_line_in_global('}')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # ##################################################################
    # Setup: Get the initial lease, no billing class
    # ##################################################################
    misc.test_procedure()
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.100')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.100')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.100')
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', 50)
    srv_msg.wait_for_message_in_log('under 20% threshold', count=0, log_file=build_log_path())

    # ##################################################################
    # # Case 1:
    # # Client adds vendor-class-id when renewing with DORA before the
    # # threshold expires.
    # # - Server maps client to billing class and should NOT resuse the
    # # lease
    # ##################################################################
    misc.test_procedure()
    srv_msg.forge_sleep(1, 'seconds')
    srv_msg.client_does_include_with_value('vendor_class_id', 'vnd1001')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.100')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'vnd1001')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.100')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.100')
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', 50)
    srv_msg.wait_for_message_in_log('under 20% threshold', count=0, log_file=build_log_path())

    # ##################################################################
    # # Case 2:
    # # Client uses same vendor-class-id and renews with DORA before the
    # # threshold expires.
    # # - Server should reuse the lease
    # ##################################################################
    misc.test_procedure()
    srv_msg.forge_sleep(1, 'seconds')
    srv_msg.client_does_include_with_value('vendor_class_id', 'vnd1001')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.100')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'vnd1001')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.100')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.100')
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', 50, expect_include=False)
    srv_msg.wait_for_message_in_log('under 20% threshold', count=2, log_file=build_log_path())

    # ##################################################################
    # # Case 3:
    # # Client uses same vendor-class-id and renews with RA before the
    # # threshold expires.
    # # - Server should reuse the lease
    # ##################################################################
    misc.test_procedure()
    srv_msg.forge_sleep(1, 'seconds')
    srv_msg.client_does_include_with_value('vendor_class_id', 'vnd1001')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.100')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.100')
    srv_msg.response_check_include_option(51)
    # When forge supports comparison change this to less than 50
    srv_msg.response_check_option_content(51, 'value', 50, expect_include=False)
    srv_msg.wait_for_message_in_log('under 20% threshold', count=3, log_file=build_log_path())

    # ##################################################################
    # # Case 4:
    # # Client changes vendor-class-id when renewing with DORA before the
    # # threshold expires.
    # # - Server maps client to different billing class and should NOT
    # # resuse the lease
    # ##################################################################
    misc.test_procedure()
    srv_msg.forge_sleep(20, 'seconds')
    srv_msg.client_does_include_with_value('vendor_class_id', 'vnd1003')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.100')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'vnd1003')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.100')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.100')
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', 50)
    srv_msg.wait_for_message_in_log('under 20% threshold', count=3, log_file=build_log_path())

    # ##################################################################
    # # Case 5:
    # # Client uses same vendor-class-id and renews with RA before the
    # # threshold expires.
    # # - Server should reuse the lease
    # ##################################################################
    misc.test_procedure()
    srv_msg.forge_sleep(1, 'seconds')
    srv_msg.client_does_include_with_value('vendor_class_id', 'vnd1003')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.100')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.100')
    srv_msg.response_check_include_option(51)
    # When forge supports comparison change this to less than 50
    srv_msg.response_check_option_content(51, 'value', 50, expect_include=False)
    srv_msg.wait_for_message_in_log('under 20% threshold', count=4, log_file=build_log_path())

    # ##################################################################
    # # Case 6:
    # # Client omits vendor-class-id when renewing with DORA before the
    # # threshold expires.
    # # - Server removes billing class and should NOT resuse the lease
    # ##################################################################
    misc.test_procedure()
    srv_msg.forge_sleep(20, 'seconds')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.100')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.100')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.100')
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', 50)
    srv_msg.wait_for_message_in_log('under 20% threshold', count=4, log_file=build_log_path())
