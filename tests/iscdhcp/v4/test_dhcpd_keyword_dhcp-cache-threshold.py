# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""ISC_DHCP DHCPv4 Keywords"""

# pylint: disable=invalid-name

import pytest

from src import misc
from src import srv_control
from src import srv_msg

from src.protosupport.multi_protocol_functions import wait_for_message_in_log
from src.softwaresupport.isc_dhcp6_server.functions import build_log_path, add_line_in_global


@pytest.mark.v4
@pytest.mark.dhcpd
def test_v4_dhcpd_keyword_dhcp_cache_threshold_default_on_dora():
    """new-v4.dhcpd.keyword.dhcp-cache-threshold.default_on.dora"""
    # Verifies that by default the threshold is set to 25%, and
    # renewing via DORA works correctly.
    # #
    # Case 1:
    # Client gets initial lease
    # #
    # Case 2:
    # Client renews lease with DORA before threshold is reached
    # - Server should reuse the original lease.
    # #
    # Case 3:
    # Client renews lease with DORA after threshold is reached
    # - Server should extend the lease
    # #
    misc.test_setup()
    add_line_in_global(' ping-check off;')
    add_line_in_global(' ddns-updates off;')
    add_line_in_global(' max-lease-time 90;')
    add_line_in_global(' default-lease-time 90;')
    add_line_in_global(' subnet 192.168.50.0 netmask 255.255.255.0 {')
    add_line_in_global('     authoritative;')
    add_line_in_global('     pool {')
    add_line_in_global('         range 192.168.50.100 192.168.50.101;')
    add_line_in_global('     }')
    add_line_in_global(' }')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # ##################################################################
    # Case 1: Get the initial lease
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
    srv_msg.response_check_option_content(51, 'value', 90)
    wait_for_message_in_log('under 25% threshold', count=0, log_file=build_log_path())

    # ##################################################################
    # Case 2: Renew with DORA before threshold expires
    # ##################################################################
    misc.test_procedure()
    srv_msg.forge_sleep(1, 'seconds')
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
    # When forge supports comparison change this to less than 90
    srv_msg.response_check_option_content(51, 'value', 90, expect_include=False)
    wait_for_message_in_log('under 25% threshold', count=2, log_file=build_log_path())

    # ##################################################################
    # Case 3: Renew with DORA after threshold expires
    # ##################################################################
    misc.test_procedure()
    srv_msg.forge_sleep(25, 'seconds')
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
    srv_msg.response_check_option_content(51, 'value', 90)
    wait_for_message_in_log('under 25% threshold', count=2, log_file=build_log_path())


@pytest.mark.v4
@pytest.mark.dhcpd
def test_v4_dhcpd_keyword_dhcp_cache_threshold_default_ra():
    """new-v4.dhcpd.keyword.dhcp-cache-threshold.default.ra"""
    # Verifies that by default the threshold is set to 25% and.
    # client renewing using RAs works correctly.
    # #
    # Case 1:
    # Client gets initial lease
    # #
    # Case 2:
    # Client renews lease with RA before threshold is reached
    # - Server should reuse the original lease.
    # #
    # Case 3:
    # Client renews lease with RA after threshold is reached
    # - Server should extend the lease
    # #
    misc.test_setup()
    add_line_in_global(' ping-check off;')
    add_line_in_global(' ddns-updates off;')
    add_line_in_global(' max-lease-time 90;')
    add_line_in_global(' default-lease-time 90;')
    add_line_in_global(' subnet 192.168.50.0 netmask 255.255.255.0 {')
    add_line_in_global('     authoritative;')
    add_line_in_global('     pool {')
    add_line_in_global('         range 192.168.50.100 192.168.50.101;')
    add_line_in_global('     }')
    add_line_in_global(' }')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # ##################################################################
    # Case 1: Get the initial lease
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
    srv_msg.response_check_option_content(51, 'value', 90)
    wait_for_message_in_log('under 25% threshold', count=0, log_file=build_log_path())

    # ##################################################################
    # Case 2: Renew with RA before threshold expires
    # ##################################################################
    misc.test_procedure()
    srv_msg.forge_sleep(1, 'seconds')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.100')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.100')
    srv_msg.response_check_include_option(51)
    # When forge supports comparison change this to less than 90
    srv_msg.response_check_option_content(51, 'value', 90, expect_include=False)
    wait_for_message_in_log('under 25% threshold', count=1, log_file=build_log_path())

    # ##################################################################
    # Case 3: Renew with RA after threshold expires
    # ##################################################################
    misc.test_procedure()
    srv_msg.forge_sleep(25, 'seconds')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.100')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.100')
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', 90)
    wait_for_message_in_log('under 25% threshold', count=1, log_file=build_log_path())


@pytest.mark.v4
@pytest.mark.dhcpd
def test_v4_dhcpd_keyword_dhcp_cache_threshold_off():
    """new-v4.dhcpd.keyword.dhcp-cache-threshold.off"""
    # #
    # Case 1:
    # Client gets initial lease
    # #
    # Case 2:
    # Client renews lease with DORA before the default threshold has passed
    # - Server should extend the lease.
    # #
    # Case 3:
    # Client renews lease with DORA after the default threshold has passed
    # - Server should extend the lease
    # #
    misc.test_setup()
    add_line_in_global(' ping-check off;')
    add_line_in_global(' ddns-updates off;')
    add_line_in_global(' max-lease-time 90;')
    add_line_in_global(' default-lease-time 90;')
    add_line_in_global(' subnet 192.168.50.0 netmask 255.255.255.0 {')
    add_line_in_global('     authoritative;')
    add_line_in_global('     pool {')
    add_line_in_global('         range 192.168.50.100 192.168.50.101;')
    add_line_in_global('     }')
    add_line_in_global(' }')
    add_line_in_global(' dhcp-cache-threshold 0;')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # ##################################################################
    # Case 1: Get the initial lease
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
    srv_msg.response_check_option_content(51, 'value', 90)
    wait_for_message_in_log('under 25% threshold', count=0, log_file=build_log_path())

    # ##################################################################
    # Case 2: Renew with DORA before default threshold expires
    # ##################################################################
    misc.test_procedure()
    srv_msg.forge_sleep(1, 'seconds')
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
    srv_msg.response_check_option_content(51, 'value', 90)
    wait_for_message_in_log('under 25% threshold', count=0, log_file=build_log_path())

    # ##################################################################
    # Case 3: Renew with DORA after default threshold expires
    # ##################################################################
    misc.test_procedure()
    srv_msg.forge_sleep(25, 'seconds')
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
    srv_msg.response_check_option_content(51, 'value', 90)
    wait_for_message_in_log('under 25% threshold', count=0, log_file=build_log_path())


@pytest.mark.v4
@pytest.mark.dhcpd
def test_v4_dhcpd_keyword_dhcp_cache_threshold_config_on():
    """new-v4.dhcpd.keyword.dhcp-cache-threshold.config_on"""
    # Verifies that the threshold can set to a custom value and
    # that renewing works correctly.
    # #
    # Case 1:
    # Client gets initial lease
    # #
    # Case 2:
    # Client renews lease with DORA before threshold is reached
    # - Server should reuse the original lease.
    # #
    # Case 3:
    # Client renews lease with RA before threshold is reached
    # - Server should reuse the original lease.
    # #
    # Case 4:
    # Client renews lease with DORA after threshold is reached
    # - Server should extend the lease
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
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # ##################################################################
    # Case 1: Get the initial lease
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
    wait_for_message_in_log('under 20% threshold', count=0, log_file=build_log_path())

    # ##################################################################
    # Case 2: Renew with DORA before threshold expires
    # ##################################################################
    misc.test_procedure()
    srv_msg.forge_sleep(1, 'seconds')
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
    # When forge supports comparison change this to less than 50
    srv_msg.response_check_option_content(51, 'value', 50, expect_include=False)
    wait_for_message_in_log('under 20% threshold', count=2, log_file=build_log_path())

    # ##################################################################
    # Case 3: Renew with RA before threshold expires
    # ##################################################################
    misc.test_procedure()
    srv_msg.forge_sleep(1, 'seconds')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.100')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.100')
    srv_msg.response_check_include_option(51)
    # When forge supports comparison change this to less than 50
    srv_msg.response_check_option_content(51, 'value', 50, expect_include=False)
    wait_for_message_in_log('under 20% threshold', count=3, log_file=build_log_path())

    # ##################################################################
    # Case 3: Renew with DORA after threshold expires
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
    wait_for_message_in_log('under 20% threshold', count=3, log_file=build_log_path())
