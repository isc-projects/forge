"""ISC_DHCP DHCPv6 func"""


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
@pytest.mark.func
@pytest.mark.lease_counters
def test_v6_dhcpd_lease_counters(step):
    """new-v6.dhcpd.lease-counters"""
    # #
    # # Checks that the count of total, active, and abandoned leases is
    # # and abandoned-best-match are logged correctly when a declined
    # # address is subsequently reclaimed:
    # #
    # # Step 1: Client 1 gets an address then declines it
    # # Step 2: Client 2 gets an address
    # # Step 3: Client 1 solicits, but is denied
    # #  - should see total 2, active 2, abandoned 1
    # #  - should see best match message for DUID 1
    # # Step 4: Client 1 requests denied address
    # #  - server should reclaim and grant it
    # # Step 5: Client 3 solicits but is denied
    # #  - should see total 2, active 2, abandoned 0
    # #  - should NOT see best match message for DUID 3
    # #
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::100-3000::101')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # ###################################################
    # # Step 1: Client 1 gets an address then declines it
    # ###################################################
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
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
    srv_msg.client_save_option_count(step, '1', 'IA_NA')
    srv_msg.client_save_option_count(step, '1', 'client-id')
    srv_msg.client_save_option_count(step, '1', 'server-id')

    misc.test_procedure(step)
    # Client adds saved options in set no. 1. And DONT Erase.
    srv_msg.client_send_msg(step, 'DECLINE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')

    # ###################################################
    # # Step 2: Client 2 gets an address
    # ###################################################
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
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

    # ###################################################
    # # Step 3: Client 1 solicits, but is denied
    # #  - should see total 2, active 2, abandoned 1
    # #  - should see best match message for DUID 1
    # ###################################################
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content(step, 'Response', '13', '3', None, 'statuscode', '2')
    srv_msg.log_includes_count(step,
                               'DHCP',
                               '1',
                               'shared network 3000::/64: 2 total, 1 active,  1 abandoned')
    srv_msg.log_includes_count(step,
                               'DHCP',
                               '1',
                               'Best match for DUID 00:03:00:01:ff:ff:ff:ff:ff:01 is an abandoned address')

    # ###################################################
    # # Step 4: Client 1 reclaims denied address
    # #  - server should reclaim and grant it
    # ###################################################
    misc.test_procedure(step)
    # Client adds saved options in set no. 1. and Erase.
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    # ###################################################
    # # Step 5: Client 3 solicits but is denied
    # #  - should see total 2, active 2, abandoned 0
    # #  - should NOT see best match message for DUID 3
    # ###################################################
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:03')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content(step, 'Response', '13', '3', None, 'statuscode', '2')
    srv_msg.log_includes_count(step,
                               'DHCP',
                               '1',
                               'shared network 3000::/64: 2 total, 2 active,  0 abandoned')
    srv_msg.log_includes_count(step,
                               'DHCP',
                               '0',
                               'Best match for DUID 00:03:00:01:ff:ff:ff:ff:ff:03 is an abandoned address')


