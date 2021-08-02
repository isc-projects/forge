"""ISC_DHCP DHCPv6 Tickets Prefix Length Pool Mismatch"""


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
@pytest.mark.dhcp6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.ticket
@pytest.mark.rt35378
def test_dhcpd_rt35378_prefix_len_mismatch(step):
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
    misc.test_setup(step)
    srv_control.run_command(step, 'prefix-length-mode exact;')
    srv_control.run_command(step, 'ddns-updates off;')
    srv_control.run_command(step, 'authoritative;')
    srv_control.run_command(step, 'subnet6 3000::/16 {')
    srv_control.run_command(step, ' pool6 {')
    srv_control.run_command(step, '  prefix6 3000:db8:0:100:: 3000:db8:0:100:: /56;')
    srv_control.run_command(step, ' }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # Verify SOLICIT of 3000:db8:0:100::/56 is valid
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '56')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '3000:db8:0:100::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'preflft',
                                             '3000')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'validlft',
                                             '4000')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '56')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')

    # Save the client and server ids for REQUEST/RENEW tests
    srv_msg.client_save_option_count(step, '1', 'client-id')
    srv_msg.client_save_option_count(step, '1', 'server-id')

    # Verify SOLICIT of 3000:db8:0:100::/72 returns None Available
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '72')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '3000:db8:0:100::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '13',
                                             '25',
                                             None,
                                             'statuscode',
                                             '6')

    # Verify REQUEST for 3000:db8:0:100::/72, without a pre-existing
    # PD lease, returns None Available
    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'plen', '72')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '3000:db8:0:100::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '13',
                                             '25',
                                             None,
                                             'statuscode',
                                             '6')

    # Verify RENEW for 3000:db8:0:100::/72, without a pre-existing
    # PD lease,  returns No Binding
    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'plen', '72')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '3000:db8:0:100::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'RENEW')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '13',
                                             '25',
                                             None,
                                             'statuscode',
                                             '3')

    # Verify REBIND for 3000:db8:0:100::/72, without a pre-existing
    # PD lease returns the prefix with lifetimes set to 0
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '72')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '3000:db8:0:100::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'REBIND')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'preflft', '0')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'validlft', '0')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '72')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')

    # Verify REQUEST for 3000:db8:0:100::/56 returns a lease
    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'plen', '56')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '3000:db8:0:100::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'preflft',
                                             '3000')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'validlft',
                                             '4000')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '56')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')

    # Verify RENEW for 3000:db8:0:100::/56 returns the prefix
    # with valid lifetimes
    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'plen', '56')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '3000:db8:0:100::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'RENEW')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'preflft',
                                             '3000')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'validlft',
                                             '4000')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '56')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')

    # Verify REBIND for 3000:db8:0:100::/56 returns the prefix
    # with valid lifetimes
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '56')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '3000:db8:0:100::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'REBIND')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'preflft',
                                             '3000')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'validlft',
                                             '4000')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '56')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')

    # Verify REQUEST for 3000:db8:0:100::/72 (mismatch) when there's
    # an existing lease returns No Binding.  (If mode is ingore it
    # will return the prior, this is tested in a different
    # feature file, 45780.
    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'plen', '72')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '3000:db8:0:100::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '13',
                                             '25',
                                             None,
                                             'statuscode',
                                             '6')

    # Verify RENEW for 3000:db8:0:100::/72 (mismatch) when there's
    # an existing lease returns No Binding.
    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'plen', '72')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '3000:db8:0:100::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'RENEW')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '13',
                                             '25',
                                             None,
                                             'statuscode',
                                             '3')

    # Verify REBIND for 3000:db8:0:100::/72 (mismatch) when there's
    # an existing lease, should return the mismatch with lifetimes
    # set to zero.
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '72')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '3000:db8:0:100::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'REBIND')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'preflft',
                                             '3000')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'validlft',
                                             '4000')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '72')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')


