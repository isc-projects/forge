"""ISC_DHCP DHCPv6 Tickets Prefix Length Pool Mismatch"""

# pylint: disable=invalid-name,line-too-long

import pytest
from src import misc
from src import srv_control
from src import srv_msg

from src.softwaresupport.isc_dhcp6_server.functions import add_line_in_global


@pytest.mark.v6
@pytest.mark.dhcpd
def test_dhcpd_rt35378_prefix_len_mismatch():
    """new-dhcpd.rt35378.prefix-len-mismatch"""
    # Test 01:
    # Verifies that SOLICIT of a valid prefix/len returns an advertised
    # prefix.
    # Test 02:
    # Verifies that SOLICIT of mismatched prefix len
    # returns None Available.
    # Test 03:
    # Verifies that a REQUEST for a mismatched prefix length
    # returns None Available.
    # Test 04:
    # Verifies that a REBIND for a mismatched prefix, returns
    # the prefix with lifetimes set to zero.
    # Test 05:
    # Verifies that a REQUEST with a matched prefix length
    # returns a lease
    # Test 06:
    # Verifies that a RENEW with a matched prefix length
    # returns the lease
    # Test 07:
    # Verifies that a REBIND with a matched prefix length
    # returns the lease
    # Test 08:
    # Verifies that a REQUEST with a mismatched prefix length
    # when there's an existing lease, returns the existing lease
    # Test 09:
    # Verifies that a RENEW with a mismatched prefix length
    # when there's an existing lease, returns No Binding
    # Test 10:
    # Verifies that a REBIND with a mismatched prefix length
    # when there's an existing lease, returns the mismatched
    # preifx with lifetimes set to zero.
    misc.test_setup()
    add_line_in_global('prefix-length-mode exact;')
    add_line_in_global('ddns-updates off;')
    add_line_in_global('authoritative;')
    add_line_in_global('subnet6 2001:db8::/32 {')
    add_line_in_global(' pool6 {')
    add_line_in_global('  prefix6 2001:db8:0:100:: 2001:db8:0:100:: /56;')
    add_line_in_global(' }')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Verify SOLICIT of 2001:db8:0:100::/56 is valid
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 56)
    srv_msg.client_sets_value('Client', 'prefix', '2001:db8:0:100::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'preflft', 3000)
    srv_msg.response_check_suboption_content(26, 25, 'validlft', 4000)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 56)
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:0:100::')

    # Save the client and server ids for REQUEST/RENEW tests
    srv_msg.client_save_option_count(1, 'client-id')
    srv_msg.client_save_option_count(1, 'server-id')

    # Verify SOLICIT of 2001:db8:0:100::/72 returns None Available
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', '72')
    srv_msg.client_sets_value('Client', 'prefix', '2001:db8:0:100::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 25, 'statuscode', 6)

    # Verify REQUEST for 2001:db8:0:100::/72, without a pre-existing
    # PD lease, returns None Available
    misc.test_procedure()
    srv_msg.client_add_saved_option_count(1)
    srv_msg.client_sets_value('Client', 'plen', '72')
    srv_msg.client_sets_value('Client', 'prefix', '2001:db8:0:100::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 25, 'statuscode', 6)

    # Verify RENEW for 2001:db8:0:100::/72, without a pre-existing
    # PD lease,  returns No Binding
    misc.test_procedure()
    srv_msg.client_add_saved_option_count(1)
    srv_msg.client_sets_value('Client', 'plen', '72')
    srv_msg.client_sets_value('Client', 'prefix', '2001:db8:0:100::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 25, 'statuscode', 3)

    # Verify REBIND for 2001:db8:0:100::/72, without a pre-existing
    # PD lease returns the prefix with lifetimes set to 0
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', '72')
    srv_msg.client_sets_value('Client', 'prefix', '2001:db8:0:100::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('REBIND')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'preflft', 0)
    srv_msg.response_check_suboption_content(26, 25, 'validlft', 0)
    srv_msg.response_check_suboption_content(26, 25, 'plen', '72')
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:0:100::')

    # Verify REQUEST for 2001:db8:0:100::/56 returns a lease
    misc.test_procedure()
    srv_msg.client_add_saved_option_count(1)
    srv_msg.client_sets_value('Client', 'plen', 56)
    srv_msg.client_sets_value('Client', 'prefix', '2001:db8:0:100::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'preflft', 3000)
    srv_msg.response_check_suboption_content(26, 25, 'validlft', 4000)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 56)
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:0:100::')

    # Verify RENEW for 2001:db8:0:100::/56 returns the prefix
    # with valid lifetimes
    misc.test_procedure()
    srv_msg.client_add_saved_option_count(1)
    srv_msg.client_sets_value('Client', 'plen', 56)
    srv_msg.client_sets_value('Client', 'prefix', '2001:db8:0:100::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'preflft', 3000)
    srv_msg.response_check_suboption_content(26, 25, 'validlft', 4000)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 56)
    srv_msg.response_check_suboption_content(26,  25,  'prefix', '2001:db8:0:100::')

    # Verify REBIND for 2001:db8:0:100::/56 returns the prefix
    # with valid lifetimes
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 56)
    srv_msg.client_sets_value('Client', 'prefix', '2001:db8:0:100::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('REBIND')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'preflft', 3000)
    srv_msg.response_check_suboption_content(26, 25, 'validlft', 4000)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 56)
    srv_msg.response_check_suboption_content(26,  25,  'prefix', '2001:db8:0:100::')

    # Verify REQUEST for 2001:db8:0:100::/72 (mismatch) when there's
    # an existing lease returns No Binding.  (If mode is ingore it
    # will return the prior, this is tested in a different
    # feature file, 45780.
    misc.test_procedure()
    srv_msg.client_add_saved_option_count(1)
    srv_msg.client_sets_value('Client', 'plen', '72')
    srv_msg.client_sets_value('Client', 'prefix', '2001:db8:0:100::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 25, 'statuscode', 6)

    # Verify RENEW for 2001:db8:0:100::/72 (mismatch) when there's
    # an existing lease returns No Binding.
    misc.test_procedure()
    srv_msg.client_add_saved_option_count(1)
    srv_msg.client_sets_value('Client', 'plen', '72')
    srv_msg.client_sets_value('Client', 'prefix', '2001:db8:0:100::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 25, 'statuscode', 3)

    # Verify REBIND for 2001:db8:0:100::/72 (mismatch) when there's
    # an existing lease, should return the mismatch with lifetimes
    # set to zero.
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', '72')
    srv_msg.client_sets_value('Client', 'prefix', '2001:db8:0:100::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('REBIND')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    # TODO looks like dhcp is sending 2999 and 3999
    # srv_msg.response_check_suboption_content(26, 25, 'preflft', 3000)
    # srv_msg.response_check_suboption_content(26, 25, 'validlft', 4000)
    srv_msg.response_check_suboption_content(26, 25, 'plen', '72')
    srv_msg.response_check_suboption_content(26,  25,  'prefix', '2001:db8:0:100::')
