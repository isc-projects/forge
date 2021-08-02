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
@pytest.mark.dhcp_cache_threshold
def test_v4_dhcpd_keyword_dhcp_cache_threshold_billing_class(step):
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
    misc.test_setup(step)
    srv_control.run_command(step, ' ping-check off;')
    srv_control.run_command(step, ' ddns-updates off;')
    srv_control.run_command(step, ' max-lease-time 50;')
    srv_control.run_command(step, ' default-lease-time 50;')
    srv_control.run_command(step, ' subnet 178.16.1.0 netmask 255.255.255.0 {')
    srv_control.run_command(step, '     authoritative;')
    srv_control.run_command(step, '     pool {')
    srv_control.run_command(step, '         range 178.16.1.100 178.16.1.101;')
    srv_control.run_command(step, '     }')
    srv_control.run_command(step, ' }')
    srv_control.run_command(step, ' dhcp-cache-threshold 20;')
    srv_control.run_command(step, ' class "vnd1001" {')
    srv_control.run_command(step, '    match if (option vendor-class-identifier = "vnd1001");')
    srv_control.run_command(step, '    lease limit 4;')
    srv_control.run_command(step, '}')
    srv_control.run_command(step, 'class "vnd1003" {')
    srv_control.run_command(step, '    match if (option vendor-class-identifier = "vnd1003");')
    srv_control.run_command(step, '    lease limit 4;')
    srv_control.run_command(step, '}')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # ##################################################################
    # Setup: Get the initial lease, no billing class
    # ##################################################################
    misc.test_procedure(step)
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.100')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '178.16.1.100')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.100')
    srv_msg.response_check_include_option(step, 'Response', None, '51')
    srv_msg.response_check_option_content(step, 'Response', '51', None, 'value', '50')
    srv_msg.log_includes_count(step, 'DHCP', '0', 'under 20% threshold')

    # ##################################################################
    # # Case 1:
    # # Client adds vendor-class-id when renewing with DORA before the
    # # threshold expires.
    # # - Server maps client to billing class and should NOT resuse the
    # # lease
    # ##################################################################
    misc.test_procedure(step)
    srv_msg.forge_sleep(step, '1', 'seconds')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'vnd1001')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.100')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'vnd1001')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '178.16.1.100')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.100')
    srv_msg.response_check_include_option(step, 'Response', None, '51')
    srv_msg.response_check_option_content(step, 'Response', '51', None, 'value', '50')
    srv_msg.log_includes_count(step, 'DHCP', '0', 'under 20% threshold')

    # ##################################################################
    # # Case 2:
    # # Client uses same vendor-class-id and renews with DORA before the
    # # threshold expires.
    # # - Server should reuse the lease
    # ##################################################################
    misc.test_procedure(step)
    srv_msg.forge_sleep(step, '1', 'seconds')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'vnd1001')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.100')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'vnd1001')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '178.16.1.100')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.100')
    srv_msg.response_check_include_option(step, 'Response', None, '51')
    srv_msg.response_check_option_content(step, 'Response', '51', 'NOT ', 'value', '50')
    srv_msg.log_includes_count(step, 'DHCP', '2', 'under 20% threshold')

    # ##################################################################
    # # Case 3:
    # # Client uses same vendor-class-id and renews with RA before the
    # # threshold expires.
    # # - Server should reuse the lease
    # ##################################################################
    misc.test_procedure(step)
    srv_msg.forge_sleep(step, '1', 'seconds')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'vnd1001')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '178.16.1.100')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.100')
    srv_msg.response_check_include_option(step, 'Response', None, '51')
    # When forge supports comparison change this to less than 50
    srv_msg.response_check_option_content(step, 'Response', '51', 'NOT ', 'value', '50')
    srv_msg.log_includes_count(step, 'DHCP', '3', 'under 20% threshold')

    # ##################################################################
    # # Case 4:
    # # Client changes vendor-class-id when renewing with DORA before the
    # # threshold expires.
    # # - Server maps client to different billing class and should NOT
    # # resuse the lease
    # ##################################################################
    misc.test_procedure(step)
    srv_msg.forge_sleep(step, '20', 'seconds')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'vnd1003')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.100')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'vnd1003')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '178.16.1.100')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.100')
    srv_msg.response_check_include_option(step, 'Response', None, '51')
    srv_msg.response_check_option_content(step, 'Response', '51', None, 'value', '50')
    srv_msg.log_includes_count(step, 'DHCP', '3', 'under 20% threshold')

    # ##################################################################
    # # Case 5:
    # # Client uses same vendor-class-id and renews with RA before the
    # # threshold expires.
    # # - Server should reuse the lease
    # ##################################################################
    misc.test_procedure(step)
    srv_msg.forge_sleep(step, '1', 'seconds')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'vnd1003')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '178.16.1.100')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.100')
    srv_msg.response_check_include_option(step, 'Response', None, '51')
    # When forge supports comparison change this to less than 50
    srv_msg.response_check_option_content(step, 'Response', '51', 'NOT ', 'value', '50')
    srv_msg.log_includes_count(step, 'DHCP', '4', 'under 20% threshold')

    # ##################################################################
    # # Case 6:
    # # Client omits vendor-class-id when renewing with DORA before the
    # # threshold expires.
    # # - Server removes billing class and should NOT resuse the lease
    # ##################################################################
    misc.test_procedure(step)
    srv_msg.forge_sleep(step, '20', 'seconds')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.100')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '178.16.1.100')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.100')
    srv_msg.response_check_include_option(step, 'Response', None, '51')
    srv_msg.response_check_option_content(step, 'Response', '51', None, 'value', '50')
    srv_msg.log_includes_count(step, 'DHCP', '4', 'under 20% threshold')


