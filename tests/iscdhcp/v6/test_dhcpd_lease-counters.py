"""ISC_DHCP DHCPv6 func"""

# pylint: disable=invalid-name,line-too-long

import pytest

from src import misc
from src import srv_control
from src import srv_msg

from src.protosupport.multi_protocol_functions import wait_for_message_in_log
from src.softwaresupport.isc_dhcp6_server.functions import build_log_path


@pytest.mark.v6
@pytest.mark.dhcpd
def test_v6_dhcpd_lease_counters():
    """new-v6.dhcpd.lease-counters"""
    # #
    # Checks that the count of total, active, and abandoned leases is
    # and abandoned-best-match are logged correctly when a declined
    # address is subsequently reclaimed:
    # #
    # Step 1: Client 1 gets an address then declines it
    # Step 2: Client 2 gets an address
    # Step 3: Client 1 solicits, but is denied
    #  - should see total 2, active 2, abandoned 1
    #  - should see best match message for DUID 1
    # Step 4: Client 1 requests denied address
    #  - server should reclaim and grant it
    # Step 5: Client 3 solicits but is denied
    #  - should see total 2, active 2, abandoned 0
    #  - should NOT see best match message for DUID 3
    # #
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::100-2001:db8:1::101')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # ###################################################
    # Step 1: Client 1 gets an address then declines it
    # ###################################################
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
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
    srv_msg.client_save_option_count(1, 'IA_NA')
    srv_msg.client_save_option_count(1, 'client-id')
    srv_msg.client_save_option_count(1, 'server-id')

    misc.test_procedure()
    # Client adds saved options in set no. 1. And DONT Erase.
    srv_msg.client_send_msg('DECLINE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    # ###################################################
    # Step 2: Client 2 gets an address
    # ###################################################
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_does_include('Client', 'client-id')
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

    # ###################################################
    # Step 3: Client 1 solicits, but is denied
    #  - should see total 2, active 2, abandoned 1
    #  - should see best match message for DUID 1
    # ###################################################
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)
    wait_for_message_in_log('shared network 2001:db8:1::/64: 2 total, 1 active,  1 abandoned',
                            count=1, log_file=build_log_path())
    wait_for_message_in_log('Best match for DUID 00:03:00:01:ff:ff:ff:ff:ff:01 is an abandoned address',
                            count=1, log_file=build_log_path())

    # ###################################################
    # Step 4: Client 1 reclaims denied address
    #  - server should reclaim and grant it
    # ###################################################
    misc.test_procedure()
    # Client adds saved options in set no. 1. and Erase.
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    # ###################################################
    # Step 5: Client 3 solicits but is denied
    #  - should see total 2, active 2, abandoned 0
    #  - should NOT see best match message for DUID 3
    # ###################################################
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:03')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)
    wait_for_message_in_log('shared network 2001:db8:1::/64: 2 total, 2 active,  0 abandoned',
                            count=1, log_file=build_log_path())
    wait_for_message_in_log('Best match for DUID 00:03:00:01:ff:ff:ff:ff:ff:03 is an abandoned address',
                            count=0, log_file=build_log_path())
