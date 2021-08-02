"""ISC_DHCP DHCPv6 Keywords"""


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
@pytest.mark.v6
@pytest.mark.dhcpd
@pytest.mark.keyword
@pytest.mark.log_threshold
def test_v6_dhcpd_keyword_log_threshold_none(step):
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
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::4')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # #
    # # Stage 1: Consume all leases
    # #

    # Grab first lease. Expect no threshold logs.
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    # save lease info for release
    srv_msg.client_save_option_count(step, '1', 'IA_NA')
    srv_msg.client_save_option_count(step, '1', 'client-id')
    srv_msg.client_save_option_count(step, '1', 'server-id')
    srv_msg.log_contains_line(step, 'DHCP', 'NOT ', 'Pool threshold')

    # Grab second lease. Expect no threshold logs.
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    # save lease info for release
    srv_msg.client_save_option_count(step, '2', 'IA_NA')
    srv_msg.client_save_option_count(step, '2', 'client-id')
    srv_msg.client_save_option_count(step, '2', 'server-id')
    srv_msg.log_contains_line(step, 'DHCP', 'NOT ', 'Pool threshold')

    # Grab third lease. Expect no threshold logs.
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:03')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    # save lease info for release
    srv_msg.client_save_option_count(step, '3', 'IA_NA')
    srv_msg.client_save_option_count(step, '3', 'client-id')
    srv_msg.client_save_option_count(step, '3', 'server-id')
    srv_msg.log_contains_line(step, 'DHCP', 'NOT ', 'Pool threshold')

    # Grab fourth lease. Expect no threshold logs.
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:04')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    # save lease info for release
    srv_msg.client_save_option_count(step, '4', 'IA_NA')
    srv_msg.client_save_option_count(step, '4', 'client-id')
    srv_msg.client_save_option_count(step, '4', 'server-id')
    srv_msg.log_contains_line(step, 'DHCP', 'NOT ', 'Pool threshold')

    # #
    # # Stage 2: Release leases until we cross low threshold.
    # #

    # Release the first lease, should not see low threshold log.
    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '1', None)
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'status-code', '0')
    srv_msg.log_contains_line(step, 'DHCP', 'NOT ', 'Pool threshold reset')

    # Release the second lease, should not see low threshold log.
    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '2', None)
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'status-code', '0')
    srv_msg.log_contains_line(step, 'DHCP', 'NOT ', 'Pool threshold reset')

    # Release third lease, should not see low threshold log.
    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '3', None)
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'status-code', '0')
    srv_msg.log_contains_line(step, 'DHCP', 'NOT ', 'Pool threshold reset')

    # Release fourth lease, should not see low threshold log.
    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '4', None)
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'status-code', '0')
    srv_msg.log_contains_line(step, 'DHCP', 'NOT ', 'Pool threshold reset')

    # #
    # # Stage 3: Grab a lease, should not see threshold reset log.
    # #

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.log_contains_line(step, 'DHCP', 'NOT ', 'Pool threshold reset')



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.dhcpd
@pytest.mark.keyword
@pytest.mark.log_threshold
def test_v6_dhcpd_keyword_log_threshold_high_gt_low(step):
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
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::4')
    srv_control.run_command(step, 'log-threshold-low 30;')
    srv_control.run_command(step, 'log-threshold-high 60;')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # #
    # # Stage 1: Consume leases until we exceed high threshold
    # #

    # Grab first lease. Expect no threshold logs.
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    # save lease info for release
    srv_msg.client_save_option_count(step, '1', 'IA_NA')
    srv_msg.client_save_option_count(step, '1', 'client-id')
    srv_msg.client_save_option_count(step, '1', 'server-id')
    srv_msg.log_contains_line(step, 'DHCP', 'NOT ', 'Pool threshold')

    # Grab second lease. Expect threshold high log.
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    # save lease info for release
    srv_msg.client_save_option_count(step, '2', 'IA_NA')
    srv_msg.client_save_option_count(step, '2', 'client-id')
    srv_msg.client_save_option_count(step, '2', 'server-id')
    srv_msg.log_includes_count(step, 'DHCP', '1', 'Pool threshold exceeded')

    # Grab third lease. Expect only 1 threshold high log.
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:03')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    # save lease info for release
    srv_msg.client_save_option_count(step, '3', 'IA_NA')
    srv_msg.client_save_option_count(step, '3', 'client-id')
    srv_msg.client_save_option_count(step, '3', 'server-id')
    srv_msg.log_includes_count(step, 'DHCP', '1', 'Pool threshold exceeded')

    # #
    # # Stage 2: Release leases until we cross low threshold.
    # #

    # Release the first lease, should not see low threshold log.
    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '1', None)
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'status-code', '0')
    srv_msg.log_contains_line(step, 'DHCP', 'NOT ', 'Pool threshold reset')

    # Release the second lease, should not see low threshold log.
    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '2', None)
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'status-code', '0')
    srv_msg.log_contains_line(step, 'DHCP', 'NOT ', 'Pool threshold reset')

    # Release third lease, should not see low threshold log.
    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '3', None)
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'status-code', '0')
    srv_msg.log_contains_line(step, 'DHCP', 'NOT ', 'Pool threshold reset')

    # #
    # # Stage 3: Grab a lease, should see threshold reset log.
    # #

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.log_includes_count(step, 'DHCP', '1', 'Pool threshold reset')



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.dhcpd
@pytest.mark.keyword
@pytest.mark.log_threshold
def test_v6_dhcpd_keyword_log_threshold_low_gt_high(step):
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
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::4')
    srv_control.run_command(step, 'log-threshold-low 65;')
    srv_control.run_command(step, 'log-threshold-high 60;')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # #
    # # Stage 1: Consume leases until we exceed high threshold
    # #

    # Grab first lease. Expect no threshold logs.
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    # save lease info for release
    srv_msg.client_save_option_count(step, '1', 'IA_NA')
    srv_msg.client_save_option_count(step, '1', 'client-id')
    srv_msg.client_save_option_count(step, '1', 'server-id')
    srv_msg.log_includes_count(step, 'DHCP', '0', 'Pool threshold exceeded')

    # Grab second lease. Expect threshold high log.
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    # save lease info for release
    srv_msg.client_save_option_count(step, '2', 'IA_NA')
    srv_msg.client_save_option_count(step, '2', 'client-id')
    srv_msg.client_save_option_count(step, '2', 'server-id')
    srv_msg.log_includes_count(step, 'DHCP', '1', 'Pool threshold exceeded')

    # Grab third lease. Expect another threshold high log.
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:03')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    # save lease info for release
    srv_msg.client_save_option_count(step, '3', 'IA_NA')
    srv_msg.client_save_option_count(step, '3', 'client-id')
    srv_msg.client_save_option_count(step, '3', 'server-id')
    srv_msg.log_includes_count(step, 'DHCP', '2', 'Pool threshold exceeded')

    # #
    # # Stage 2: Release leases until we cross low threshold.
    # #

    # Release the first lease, should not see low threshold log.
    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '1', None)
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'status-code', '0')
    srv_msg.log_contains_line(step, 'DHCP', 'NOT ', 'Pool threshold reset')

    # Release the second lease, should not see low threshold log.
    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '2', None)
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'status-code', '0')
    srv_msg.log_contains_line(step, 'DHCP', 'NOT ', 'Pool threshold reset')

    # Release third lease, should not see low threshold log.
    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '3', None)
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'status-code', '0')
    srv_msg.log_contains_line(step, 'DHCP', 'NOT ', 'Pool threshold reset')

    # #
    # # Stage 3: Grab a lease, should not see threshold reset log.
    # #

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    # make sure we added no new threshold logs
    srv_msg.log_includes_count(step, 'DHCP', '2', 'Pool threshold exceeded')
    srv_msg.log_includes_count(step, 'DHCP', '0', 'Pool threshold reset')



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.dhcpd
@pytest.mark.keyword
@pytest.mark.log_threshold
def test_v6_dhcpd_keyword_log_threshold_high_only(step):
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

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::4')
    srv_control.run_command(step, 'log-threshold-high 60;')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # #
    # # Stage 1: Consume leases until we exceed high threshold
    # #

    # Grab first lease. Expect no threshold logs.
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    # save lease info for release
    srv_msg.client_save_option_count(step, '1', 'IA_NA')
    srv_msg.client_save_option_count(step, '1', 'client-id')
    srv_msg.client_save_option_count(step, '1', 'server-id')
    srv_msg.log_includes_count(step, 'DHCP', '0', 'Pool threshold exceeded')

    # Grab second lease. Expect threshold high log.
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    # save lease info for release
    srv_msg.client_save_option_count(step, '2', 'IA_NA')
    srv_msg.client_save_option_count(step, '2', 'client-id')
    srv_msg.client_save_option_count(step, '2', 'server-id')
    srv_msg.log_includes_count(step, 'DHCP', '1', 'Pool threshold exceeded')

    # Grab third lease. Expect only 1 threshold high log.
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:03')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    # save lease info for release
    srv_msg.client_save_option_count(step, '3', 'IA_NA')
    srv_msg.client_save_option_count(step, '3', 'client-id')
    srv_msg.client_save_option_count(step, '3', 'server-id')
    srv_msg.log_includes_count(step, 'DHCP', '1', 'Pool threshold exceeded')

    # #
    # # Stage 2: Release leases until we cross low threshold.
    # #

    # Release the first lease, should not see low threshold log.
    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '1', None)
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'status-code', '0')
    srv_msg.log_includes_count(step, 'DHCP', '0', 'Pool threshold reset')

    # Release the second lease, should not see low threshold log.
    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '2', None)
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'status-code', '0')
    srv_msg.log_includes_count(step, 'DHCP', '0', 'Pool threshold reset')

    # Release third lease, should not see low threshold log.
    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '3', None)
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'status-code', '0')
    srv_msg.log_includes_count(step, 'DHCP', '0', 'Pool threshold reset')

    # #
    # # Stage 3: Grab a lease, should see threshold reset log.
    # #

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.log_includes_count(step, 'DHCP', '1', 'Pool threshold exceeded')
    srv_msg.log_includes_count(step, 'DHCP', '0', 'Pool threshold reset')



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.dhcpd
@pytest.mark.keyword
@pytest.mark.toms
def test_v6_dhcpd_keyword_log_threshold_low_only(step):
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
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::4')
    srv_control.run_command(step, 'log-threshold-low 30;')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # #
    # # Stage 1: Consume leases
    # #

    # Grab first lease. Expect no threshold logs.
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    # save lease info for release
    srv_msg.client_save_option_count(step, '1', 'IA_NA')
    srv_msg.client_save_option_count(step, '1', 'client-id')
    srv_msg.client_save_option_count(step, '1', 'server-id')
    srv_msg.log_includes_count(step, 'DHCP', '0', 'Pool threshold exceeded')

    # Grab second lease. Expect no threshold log.
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    # save lease info for release
    srv_msg.client_save_option_count(step, '2', 'IA_NA')
    srv_msg.client_save_option_count(step, '2', 'client-id')
    srv_msg.client_save_option_count(step, '2', 'server-id')
    srv_msg.log_includes_count(step, 'DHCP', '0', 'Pool threshold exceeded')

    # Grab third lease. Expect no threshold high log.
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:03')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    # save lease info for release
    srv_msg.client_save_option_count(step, '3', 'IA_NA')
    srv_msg.client_save_option_count(step, '3', 'client-id')
    srv_msg.client_save_option_count(step, '3', 'server-id')
    srv_msg.log_includes_count(step, 'DHCP', '0', 'Pool threshold exceeded')

    # Grab fourth lease. Expect no threshold logs.
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:04')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    # save lease info for release
    srv_msg.client_save_option_count(step, '4', 'IA_NA')
    srv_msg.client_save_option_count(step, '4', 'client-id')
    srv_msg.client_save_option_count(step, '4', 'server-id')
    srv_msg.log_includes_count(step, 'DHCP', '0', 'Pool threshold exceeded')

    # #
    # # Stage 2: Release leases until we cross low threshold.
    # #

    # Release the first lease, should not see low threshold log.
    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '1', None)
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'status-code', '0')
    srv_msg.log_includes_count(step, 'DHCP', '0', 'Pool threshold reset')

    # Release the second lease, should not see low threshold log.
    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '2', None)
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'status-code', '0')
    srv_msg.log_includes_count(step, 'DHCP', '0', 'Pool threshold reset')

    # Release third lease, should not see low threshold log.
    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '3', None)
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'status-code', '0')
    srv_msg.log_includes_count(step, 'DHCP', '0', 'Pool threshold reset')

    # Release fourth lease, should not see low threshold log.
    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '4', None)
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'status-code', '0')
    srv_msg.log_includes_count(step, 'DHCP', '0', 'Pool threshold reset')

    # #
    # # Stage 3: Grab a lease, should not see threshold reset log.
    # #

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.log_includes_count(step, 'DHCP', '0', 'Pool threshold exceeded')
    srv_msg.log_includes_count(step, 'DHCP', '0', 'Pool threshold reset')



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.dhcpd
@pytest.mark.keyword
@pytest.mark.log_threshold
def test_v6_dhcpd_keyword_log_threshold_too_large(step):
    """new-v6.dhcpd.keyword.log-threshold-too-large"""
    # #
    # # Checks that the server emits a log message stating that log-threshold
    # # is disabled for a shared-network when the total number of addresses in
    # # a given pond is too large to track.  For obvious reasons, we do not
    # # attempt to test that threshold logic is actually skipped.
    # #
    misc.test_setup(step)
    srv_control.run_command(step, ' shared-network net1 {')
    srv_control.run_command(step, ' subnet6 3000::/16 {')
    srv_control.run_command(step, '  range6 3000:1::0/63;')
    srv_control.run_command(step, '  range6 3000:D::0/66;')
    srv_control.run_command(step, '  range6 3000:E::0/66;')
    srv_control.run_command(step, ' }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.pass_criteria(step)
    srv_msg.log_includes_count(step,
                               'DHCP',
                               '1',
                               'Threshold logging disabled for shared subnet of ranges: 3000:1::/63, 3000:d::/66, 3000:e::/66')


