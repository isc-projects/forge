"""ISC_DHCP DHCPv6 Keywords"""

# pylint: disable=invalid-name,line-too-long

import pytest
from src import misc
from src import srv_control
from src import srv_msg

from src.softwaresupport.isc_dhcp6_server.functions import build_log_path, add_line_in_global


@pytest.mark.v6
@pytest.mark.dhcpd
def test_v6_dhcpd_keyword_log_threshold_none():
    """new-v6.dhcpd.keyword.log-threshold-none"""
    # #
    # # Testing: That log messages for crossing the high and
    # # low thresholds do not appear if log-threshold values
    # # are not set.
    # #
    # # Stage 1: Consume all leases from the pool and verify that the
    # # high threshold message is not logged
    # #
    # # Stage 2: Release all leases
    # #
    # # Stage 3: request a lease, and verify that the low threshold log message
    # # does not appear.
    # #
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::4')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # #
    # # Stage 1: Consume all leases
    # #

    # Grab first lease. Expect no threshold logs.
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # save lease info for release
    srv_msg.client_save_option_count(1, 'IA_NA')
    srv_msg.client_save_option_count(1, 'client-id')
    srv_msg.client_save_option_count(1, 'server-id')
    srv_msg.log_doesnt_contain('Pool threshold', log_file=build_log_path())

    # Grab second lease. Expect no threshold logs.
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # save lease info for release
    srv_msg.client_save_option_count(2, 'IA_NA')
    srv_msg.client_save_option_count(2, 'client-id')
    srv_msg.client_save_option_count(2, 'server-id')
    srv_msg.log_doesnt_contain('Pool threshold', log_file=build_log_path())

    # Grab third lease. Expect no threshold logs.
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:03')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # save lease info for release
    srv_msg.client_save_option_count(3, 'IA_NA')
    srv_msg.client_save_option_count(3, 'client-id')
    srv_msg.client_save_option_count(3, 'server-id')
    srv_msg.log_doesnt_contain('Pool threshold', log_file=build_log_path())

    # Grab fourth lease. Expect no threshold logs.
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:04')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # save lease info for release
    srv_msg.client_save_option_count(4, 'IA_NA')
    srv_msg.client_save_option_count(4, 'client-id')
    srv_msg.client_save_option_count(4, 'server-id')
    srv_msg.log_doesnt_contain('Pool threshold', log_file=build_log_path())

    # #
    # # Stage 2: Release leases until we cross low threshold.
    # #

    # Release the first lease, should not see low threshold log.
    misc.test_procedure()
    srv_msg.client_add_saved_option_count(1, erase=True)
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'status-code', 0)
    srv_msg.log_doesnt_contain('Pool threshold reset', log_file=build_log_path())

    # Release the second lease, should not see low threshold log.
    misc.test_procedure()
    srv_msg.client_add_saved_option_count(2, None)
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'status-code', 0)
    srv_msg.log_doesnt_contain('Pool threshold reset', log_file=build_log_path())

    # Release third lease, should not see low threshold log.
    misc.test_procedure()
    srv_msg.client_add_saved_option_count(3, None)
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'status-code', 0)
    srv_msg.log_doesnt_contain('Pool threshold reset', log_file=build_log_path())

    # Release fourth lease, should not see low threshold log.
    misc.test_procedure()
    srv_msg.client_add_saved_option_count(4, None)
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'status-code', 0)
    srv_msg.log_doesnt_contain('Pool threshold reset', log_file=build_log_path())

    # #
    # # Stage 3: Grab a lease, should not see threshold reset log.
    # #

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.log_doesnt_contain('Pool threshold reset', log_file=build_log_path())


@pytest.mark.v6
@pytest.mark.dhcpd
def test_v6_dhcpd_keyword_log_threshold_high_gt_low():
    """new-v6.dhcpd.keyword.log-threshold-high-gt-low"""
    # #
    # # Testing: That log messages for crossing the high and low
    # # thresholds are output at the correct times when both
    # # high and low are set, and high threshold is larger than low
    # # threshold.
    # #
    # # Stage 1: consume enough leases from the pool to verify the
    # # that the high threshold message is logged
    # #
    # # Stage 2: release enough leases to fall under the low threshold.
    # #
    # # Stage 3: request a lease, and verify the low threshold log
    # # message appears. (thresholds are testing only during allocation
    # # not release... asinine but true).
    # #
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::4')
    add_line_in_global('log-threshold-low 30;')
    add_line_in_global('log-threshold-high 60;')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # #
    # # Stage 1: Consume leases until we exceed high threshold
    # #

    # Grab first lease. Expect no threshold logs.
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # save lease info for release
    srv_msg.client_save_option_count(1, 'IA_NA')
    srv_msg.client_save_option_count(1, 'client-id')
    srv_msg.client_save_option_count(1, 'server-id')
    srv_msg.log_doesnt_contain('Pool threshold', log_file=build_log_path())

    # Grab second lease. Expect threshold high log.
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # save lease info for release
    srv_msg.client_save_option_count(2, 'IA_NA')
    srv_msg.client_save_option_count(2, 'client-id')
    srv_msg.client_save_option_count(2, 'server-id')
    srv_msg.wait_for_message_in_log('Pool threshold exceeded', count=1, log_file=build_log_path())

    # Grab third lease. Expect only 1 threshold high log.
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:03')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # save lease info for release
    srv_msg.client_save_option_count(3, 'IA_NA')
    srv_msg.client_save_option_count(3, 'client-id')
    srv_msg.client_save_option_count(3, 'server-id')
    srv_msg.wait_for_message_in_log('Pool threshold exceeded', count=1, log_file=build_log_path())

    # #
    # # Stage 2: Release leases until we cross low threshold.
    # #

    # Release the first lease, should not see low threshold log.
    misc.test_procedure()
    srv_msg.client_add_saved_option_count(1, erase=True)
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'status-code', 0)
    srv_msg.log_doesnt_contain('Pool threshold reset', log_file=build_log_path())

    # Release the second lease, should not see low threshold log.
    misc.test_procedure()
    srv_msg.client_add_saved_option_count(2, None)
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'status-code', 0)
    srv_msg.log_doesnt_contain('Pool threshold reset', log_file=build_log_path())

    # Release third lease, should not see low threshold log.
    misc.test_procedure()
    srv_msg.client_add_saved_option_count(3, None)
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'status-code', 0)
    srv_msg.log_doesnt_contain('Pool threshold reset', log_file=build_log_path())

    # #
    # # Stage 3: Grab a lease, should see threshold reset log.
    # #

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.wait_for_message_in_log('Pool threshold reset', count=1, log_file=build_log_path())


@pytest.mark.v6
@pytest.mark.dhcpd
def test_v6_dhcpd_keyword_log_threshold_low_gt_high():
    """new-v6.dhcpd.keyword.log-threshold-low-gt-high"""
    # #
    # # Testing: When low threshold is greater than high threshold
    # # the high threshold log should be output on each grant once exceeded.
    # # and low threshold crossing never logs.
    # #
    # # Stage 1: consume enough leases from the pool to verify
    # # that the high threshold message is logged. Verify the high
    # # threshold message repeats.
    # #
    # # Stage 2: release all the leases
    # #
    # # Stage 3: request a lease, and verify that no new threshold logs
    # # are output.
    # #
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::4')
    add_line_in_global('log-threshold-low 65;')
    add_line_in_global('log-threshold-high 60;')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # #
    # # Stage 1: Consume leases until we exceed high threshold
    # #

    # Grab first lease. Expect no threshold logs.
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # save lease info for release
    srv_msg.client_save_option_count(1, 'IA_NA')
    srv_msg.client_save_option_count(1, 'client-id')
    srv_msg.client_save_option_count(1, 'server-id')
    srv_msg.wait_for_message_in_log('Pool threshold exceeded', count=0, log_file=build_log_path())

    # Grab second lease. Expect threshold high log.
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # save lease info for release
    srv_msg.client_save_option_count(2, 'IA_NA')
    srv_msg.client_save_option_count(2, 'client-id')
    srv_msg.client_save_option_count(2, 'server-id')
    srv_msg.wait_for_message_in_log('Pool threshold exceeded', count=1, log_file=build_log_path())

    # Grab third lease. Expect another threshold high log.
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:03')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # save lease info for release
    srv_msg.client_save_option_count(3, 'IA_NA')
    srv_msg.client_save_option_count(3, 'client-id')
    srv_msg.client_save_option_count(3, 'server-id')
    srv_msg.wait_for_message_in_log('Pool threshold exceeded', count=2, log_file=build_log_path())

    # #
    # # Stage 2: Release leases until we cross low threshold.
    # #

    # Release the first lease, should not see low threshold log.
    misc.test_procedure()
    srv_msg.client_add_saved_option_count(1, erase=True)
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'status-code', 0)
    srv_msg.log_doesnt_contain('Pool threshold reset', log_file=build_log_path())

    # Release the second lease, should not see low threshold log.
    misc.test_procedure()
    srv_msg.client_add_saved_option_count(2, None)
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'status-code', 0)
    srv_msg.log_doesnt_contain('Pool threshold reset', log_file=build_log_path())

    # Release third lease, should not see low threshold log.
    misc.test_procedure()
    srv_msg.client_add_saved_option_count(3, None)
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'status-code', 0)
    srv_msg.log_doesnt_contain('Pool threshold reset', log_file=build_log_path())

    # #
    # # Stage 3: Grab a lease, should not see threshold reset log.
    # #

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # make sure we added no new threshold logs
    srv_msg.wait_for_message_in_log('Pool threshold exceeded', count=2, log_file=build_log_path())
    srv_msg.wait_for_message_in_log('Pool threshold reset', count=0, log_file=build_log_path())


@pytest.mark.v6
@pytest.mark.dhcpd
def test_v6_dhcpd_keyword_log_threshold_high_only():
    """new-v6.dhcpd.keyword.log-threshold-high-only"""
    # #
    # # Testing: When only the high threshold is specified
    # # than the threshold exceeded log only occurs once each
    # # time it is exceeded.  In other words, once exceeded it
    # # does not repeat with each grant.  Since low threshold
    # # defaults to 0, that log should never appear.
    # #
    # # Stage 1: consume enough leases from the pool to verify the
    # # that the high threshold message is logged. Verify the high
    # # threshold message does not repeat.
    # #
    # # Stage 2: release all the leases
    # #
    # # Stage 3: request a lease, and verify that no new threshold logs
    # # are output.
    # #

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::4')
    add_line_in_global('log-threshold-high 60;')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # #
    # # Stage 1: Consume leases until we exceed high threshold
    # #

    # Grab first lease. Expect no threshold logs.
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # save lease info for release
    srv_msg.client_save_option_count(1, 'IA_NA')
    srv_msg.client_save_option_count(1, 'client-id')
    srv_msg.client_save_option_count(1, 'server-id')
    srv_msg.wait_for_message_in_log('Pool threshold exceeded', count=0, log_file=build_log_path())

    # Grab second lease. Expect threshold high log.
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # save lease info for release
    srv_msg.client_save_option_count(2, 'IA_NA')
    srv_msg.client_save_option_count(2, 'client-id')
    srv_msg.client_save_option_count(2, 'server-id')
    srv_msg.wait_for_message_in_log('Pool threshold exceeded', count=1, log_file=build_log_path())

    # Grab third lease. Expect only 1 threshold high log.
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:03')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # save lease info for release
    srv_msg.client_save_option_count(3, 'IA_NA')
    srv_msg.client_save_option_count(3, 'client-id')
    srv_msg.client_save_option_count(3, 'server-id')
    srv_msg.wait_for_message_in_log('Pool threshold exceeded', count=1, log_file=build_log_path())

    # #
    # # Stage 2: Release leases until we cross low threshold.
    # #

    # Release the first lease, should not see low threshold log.
    misc.test_procedure()
    srv_msg.client_add_saved_option_count(1, erase=True)
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'status-code', 0)
    srv_msg.wait_for_message_in_log('Pool threshold reset', count=0, log_file=build_log_path())

    # Release the second lease, should not see low threshold log.
    misc.test_procedure()
    srv_msg.client_add_saved_option_count(2, None)
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'status-code', 0)
    srv_msg.wait_for_message_in_log('Pool threshold reset', count=0, log_file=build_log_path())

    # Release third lease, should not see low threshold log.
    misc.test_procedure()
    srv_msg.client_add_saved_option_count(3, None)
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'status-code', 0)
    srv_msg.wait_for_message_in_log('Pool threshold reset', count=0, log_file=build_log_path())

    # #
    # # Stage 3: Grab a lease, should see threshold reset log.
    # #

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.wait_for_message_in_log('Pool threshold exceeded', count=1, log_file=build_log_path())
    srv_msg.wait_for_message_in_log('Pool threshold reset', count=0, log_file=build_log_path())


@pytest.mark.v6
@pytest.mark.dhcpd
def test_v6_dhcpd_keyword_log_threshold_low_only():
    """new-v6.dhcpd.keyword.log-threshold-low-only"""
    # #
    # # Testing: That log messages for crossing the high and
    # # low thresholds do not appear if only log-threshold-low
    # # value is set.
    # #
    # # Stage 1: Consume all leases from the pool and verify that the
    # # high threshold message is not logged
    # #
    # # Stage 2: Release all leases
    # #
    # # Stage 3: request a lease, and verify that the low threshold log does not
    # # message appear.
    # #
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::4')
    add_line_in_global('log-threshold-low 30;')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # #
    # # Stage 1: Consume leases
    # #

    # Grab first lease. Expect no threshold logs.
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # save lease info for release
    srv_msg.client_save_option_count(1, 'IA_NA')
    srv_msg.client_save_option_count(1, 'client-id')
    srv_msg.client_save_option_count(1, 'server-id')
    srv_msg.wait_for_message_in_log('Pool threshold exceeded', count=0, log_file=build_log_path())

    # Grab second lease. Expect no threshold log.
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # save lease info for release
    srv_msg.client_save_option_count(2, 'IA_NA')
    srv_msg.client_save_option_count(2, 'client-id')
    srv_msg.client_save_option_count(2, 'server-id')
    srv_msg.wait_for_message_in_log('Pool threshold exceeded', count=0, log_file=build_log_path())

    # Grab third lease. Expect no threshold high log.
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:03')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # save lease info for release
    srv_msg.client_save_option_count(3, 'IA_NA')
    srv_msg.client_save_option_count(3, 'client-id')
    srv_msg.client_save_option_count(3, 'server-id')
    srv_msg.wait_for_message_in_log('Pool threshold exceeded', count=0, log_file=build_log_path())

    # Grab fourth lease. Expect no threshold logs.
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:04')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # save lease info for release
    srv_msg.client_save_option_count(4, 'IA_NA')
    srv_msg.client_save_option_count(4, 'client-id')
    srv_msg.client_save_option_count(4, 'server-id')
    srv_msg.wait_for_message_in_log('Pool threshold exceeded', count=0, log_file=build_log_path())

    # #
    # # Stage 2: Release leases until we cross low threshold.
    # #

    # Release the first lease, should not see low threshold log.
    misc.test_procedure()
    srv_msg.client_add_saved_option_count(1, erase=True)
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'status-code', 0)
    srv_msg.wait_for_message_in_log('Pool threshold reset', count=0, log_file=build_log_path())

    # Release the second lease, should not see low threshold log.
    misc.test_procedure()
    srv_msg.client_add_saved_option_count(2, None)
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'status-code', 0)
    srv_msg.wait_for_message_in_log('Pool threshold reset', count=0, log_file=build_log_path())

    # Release third lease, should not see low threshold log.
    misc.test_procedure()
    srv_msg.client_add_saved_option_count(3, None)
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'status-code', 0)
    srv_msg.wait_for_message_in_log('Pool threshold reset', count=0, log_file=build_log_path())

    # Release fourth lease, should not see low threshold log.
    misc.test_procedure()
    srv_msg.client_add_saved_option_count(4, None)
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'status-code', 0)
    srv_msg.wait_for_message_in_log('Pool threshold reset', count=0, log_file=build_log_path())

    # #
    # # Stage 3: Grab a lease, should not see threshold reset log.
    # #

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.wait_for_message_in_log('Pool threshold exceeded', count=0, log_file=build_log_path())
    srv_msg.wait_for_message_in_log('Pool threshold reset', count=0, log_file=build_log_path())


@pytest.mark.v6
@pytest.mark.dhcpd
def test_v6_dhcpd_keyword_log_threshold_too_large():
    """new-v6.dhcpd.keyword.log-threshold-too-large"""
    # #
    # # Checks that the server emits a log message stating that log-threshold
    # # is disabled for a shared-network when the total number of addresses in
    # # a given pond is too large to track.  For obvious reasons, we do not
    # # attempt to test that threshold logic is actually skipped.
    # #
    misc.test_setup()
    add_line_in_global(' shared-network net1 {')
    add_line_in_global(' subnet6 2001:db8::/32 {')
    add_line_in_global('  range6 2001:db8:1::0/66;')
    add_line_in_global('  range6 2001:db8:2::0/66;')
    add_line_in_global(' }')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.pass_criteria()
    srv_msg.wait_for_message_in_log('Threshold logging disabled for shared subnet of ranges: 2001:db8:1::0/66, 2001:db8:2::0/66',
                                    count=1, log_file=build_log_path())
