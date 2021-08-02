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
def test_v4_dhcpd_keyword_dhcp_cache_threshold_default_on_dora(step):
    """new-v4.dhcpd.keyword.dhcp-cache-threshold.default_on.dora"""
    # # Verifies that by default the threshold is set to 25%, and
    # # renewing via DORA works correctly.
    # #
    # # Case 1:
    # # Client gets initial lease
    # #
    # # Case 2:
    # # Client renews lease with DORA before threshold is reached
    # # - Server should reuse the original lease.
    # #
    # # Case 3:
    # # Client renews lease with DORA after threshold is reached
    # # - Server should extend the lease
    # #
    misc.test_setup(step)
    srv_control.run_command(step, ' ping-check off;')
    srv_control.run_command(step, ' ddns-updates off;')
    srv_control.run_command(step, ' max-lease-time 90;')
    srv_control.run_command(step, ' default-lease-time 90;')
    srv_control.run_command(step, ' subnet 178.16.1.0 netmask 255.255.255.0 {')
    srv_control.run_command(step, '     authoritative;')
    srv_control.run_command(step, '     pool {')
    srv_control.run_command(step, '         range 178.16.1.100 178.16.1.101;')
    srv_control.run_command(step, '     }')
    srv_control.run_command(step, ' }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # ##################################################################
    # Case 1: Get the initial lease
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
    srv_msg.response_check_option_content(step, 'Response', '51', None, 'value', '90')
    srv_msg.log_includes_count(step, 'DHCP', '0', 'under 25% threshold')

    # ##################################################################
    # Case 2: Renew with DORA before threshold expires
    # ##################################################################
    misc.test_procedure(step)
    srv_msg.forge_sleep(step, '1', 'seconds')
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
    # When forge supports comparison change this to less than 90
    srv_msg.response_check_option_content(step, 'Response', '51', 'NOT ', 'value', '90')
    srv_msg.log_includes_count(step, 'DHCP', '2', 'under 25% threshold')

    # ##################################################################
    # Case 3: Renew with DORA after threshold expires
    # ##################################################################
    misc.test_procedure(step)
    srv_msg.forge_sleep(step, '25', 'seconds')
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
    srv_msg.response_check_option_content(step, 'Response', '51', None, 'value', '90')
    srv_msg.log_includes_count(step, 'DHCP', '2', 'under 25% threshold')



@pytest.mark.py_test
@pytest.mark.v4
@pytest.mark.dhcpd
@pytest.mark.keyword
@pytest.mark.dhcp_cache_threshold
def test_v4_dhcpd_keyword_dhcp_cache_threshold_default_ra(step):
    """new-v4.dhcpd.keyword.dhcp-cache-threshold.default.ra"""
    # # Verifies that by default the threshold is set to 25% and.
    # # client renewing using RAs works correctly.
    # #
    # # Case 1:
    # # Client gets initial lease
    # #
    # # Case 2:
    # # Client renews lease with RA before threshold is reached
    # # - Server should reuse the original lease.
    # #
    # # Case 3:
    # # Client renews lease with RA after threshold is reached
    # # - Server should extend the lease
    # #
    misc.test_setup(step)
    srv_control.run_command(step, ' ping-check off;')
    srv_control.run_command(step, ' ddns-updates off;')
    srv_control.run_command(step, ' max-lease-time 90;')
    srv_control.run_command(step, ' default-lease-time 90;')
    srv_control.run_command(step, ' subnet 178.16.1.0 netmask 255.255.255.0 {')
    srv_control.run_command(step, '     authoritative;')
    srv_control.run_command(step, '     pool {')
    srv_control.run_command(step, '         range 178.16.1.100 178.16.1.101;')
    srv_control.run_command(step, '     }')
    srv_control.run_command(step, ' }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # ##################################################################
    # Case 1: Get the initial lease
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
    srv_msg.response_check_option_content(step, 'Response', '51', None, 'value', '90')
    srv_msg.log_includes_count(step, 'DHCP', '0', 'under 25% threshold')

    # ##################################################################
    # Case 2: Renew with RA before threshold expires
    # ##################################################################
    misc.test_procedure(step)
    srv_msg.forge_sleep(step, '1', 'seconds')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '178.16.1.100')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.100')
    srv_msg.response_check_include_option(step, 'Response', None, '51')
    # When forge supports comparison change this to less than 90
    srv_msg.response_check_option_content(step, 'Response', '51', 'NOT ', 'value', '90')
    srv_msg.log_includes_count(step, 'DHCP', '1', 'under 25% threshold')

    # ##################################################################
    # Case 3: Renew with RA after threshold expires
    # ##################################################################
    misc.test_procedure(step)
    srv_msg.forge_sleep(step, '25', 'seconds')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '178.16.1.100')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.100')
    srv_msg.response_check_include_option(step, 'Response', None, '51')
    srv_msg.response_check_option_content(step, 'Response', '51', None, 'value', '90')
    srv_msg.log_includes_count(step, 'DHCP', '1', 'under 25% threshold')



@pytest.mark.py_test
@pytest.mark.v4
@pytest.mark.dhcpd
@pytest.mark.keyword
@pytest.mark.dhcp_cache_threshold
def test_v4_dhcpd_keyword_dhcp_cache_threshold_off(step):
    """new-v4.dhcpd.keyword.dhcp-cache-threshold.off"""
    # #
    # # Case 1:
    # # Client gets initial lease
    # #
    # # Case 2:
    # # Client renews lease with DORA before the default threshold has passed
    # # - Server should extend the lease.
    # #
    # # Case 3:
    # # Client renews lease with DORA after the default threshold has passed
    # # - Server should extend the lease
    # #
    misc.test_setup(step)
    srv_control.run_command(step, ' ping-check off;')
    srv_control.run_command(step, ' ddns-updates off;')
    srv_control.run_command(step, ' max-lease-time 90;')
    srv_control.run_command(step, ' default-lease-time 90;')
    srv_control.run_command(step, ' subnet 178.16.1.0 netmask 255.255.255.0 {')
    srv_control.run_command(step, '     authoritative;')
    srv_control.run_command(step, '     pool {')
    srv_control.run_command(step, '         range 178.16.1.100 178.16.1.101;')
    srv_control.run_command(step, '     }')
    srv_control.run_command(step, ' }')
    srv_control.run_command(step, ' dhcp-cache-threshold 0;')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # ##################################################################
    # Case 1: Get the initial lease
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
    srv_msg.response_check_option_content(step, 'Response', '51', None, 'value', '90')
    srv_msg.log_includes_count(step, 'DHCP', '0', 'under 25% threshold')

    # ##################################################################
    # Case 2: Renew with DORA before default threshold expires
    # ##################################################################
    misc.test_procedure(step)
    srv_msg.forge_sleep(step, '1', 'seconds')
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
    srv_msg.response_check_option_content(step, 'Response', '51', None, 'value', '90')
    srv_msg.log_includes_count(step, 'DHCP', '0', 'under 25% threshold')

    # ##################################################################
    # Case 3: Renew with DORA after default threshold expires
    # ##################################################################
    misc.test_procedure(step)
    srv_msg.forge_sleep(step, '25', 'seconds')
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
    srv_msg.response_check_option_content(step, 'Response', '51', None, 'value', '90')
    srv_msg.log_includes_count(step, 'DHCP', '0', 'under 25% threshold')



@pytest.mark.py_test
@pytest.mark.v4
@pytest.mark.dhcpd
@pytest.mark.keyword
@pytest.mark.dhcp_cache_threshold
def test_v4_dhcpd_keyword_dhcp_cache_threshold_config_on(step):
    """new-v4.dhcpd.keyword.dhcp-cache-threshold.config_on"""
    # # Verifies that the threshold can set to a custom value and
    # # that renewing works correctly.
    # #
    # # Case 1:
    # # Client gets initial lease
    # #
    # # Case 2:
    # # Client renews lease with DORA before threshold is reached
    # # - Server should reuse the original lease.
    # #
    # # Case 3:
    # # Client renews lease with RA before threshold is reached
    # # - Server should reuse the original lease.
    # #
    # # Case 4:
    # # Client renews lease with DORA after threshold is reached
    # # - Server should extend the lease
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
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # ##################################################################
    # Case 1: Get the initial lease
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
    # Case 2: Renew with DORA before threshold expires
    # ##################################################################
    misc.test_procedure(step)
    srv_msg.forge_sleep(step, '1', 'seconds')
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
    # When forge supports comparison change this to less than 50
    srv_msg.response_check_option_content(step, 'Response', '51', 'NOT ', 'value', '50')
    srv_msg.log_includes_count(step, 'DHCP', '2', 'under 20% threshold')

    # ##################################################################
    # Case 3: Renew with RA before threshold expires
    # ##################################################################
    misc.test_procedure(step)
    srv_msg.forge_sleep(step, '1', 'seconds')
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
    # Case 3: Renew with DORA after threshold expires
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
    srv_msg.log_includes_count(step, 'DHCP', '3', 'under 20% threshold')



