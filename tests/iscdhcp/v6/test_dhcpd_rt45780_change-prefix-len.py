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
@pytest.mark.rt45870
def test_dhcpd_rt45780_change_prefix_len_exact(step):
    """new-dhcpd.rt45780.change-prefix-len.exact"""

    misc.test_setup(step)
    srv_control.run_command(step, 'prefix-length-mode exact;')
    srv_control.run_command(step, 'ddns-updates off;')
    srv_control.run_command(step, 'authoritative;')
    srv_control.run_command(step, 'subnet6 3000::/16 {')
    srv_control.run_command(step, ' pool6 {')
    srv_control.run_command(step, '  prefix6 3000:db8:0:100:: 3000:db8:0:100:: /64;')
    srv_control.run_command(step, '  prefix6 3000:db8:0:200:: 3000:db8:0:200:: /60;')
    srv_control.run_command(step, ' }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # Verify SOLICIT of /60 gets us a /60 prefix
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '60')
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
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '60')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:200::')

    # Verify SOLICIT of /64 gets us a /64 prefix
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '64')
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
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '64')
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

    # Verify REQUEST for 3000:db8:0:100::/64
    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'plen', '64')
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
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '64')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')

    # Verify RELEASE for 3000:db8:0:100::/64
    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'plen', '64')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '3000:db8:0:100::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'statuscode', '0')


    # Verify SOLICIT of /60 gets us a /60 prefix AFTER we released /64
    # when mode is not "ignore"
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '60')
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
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '60')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:200::')

    # #############################################################################


@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.ticket
@pytest.mark.rt45870
def test_dhcpd_rt45780_change_prefix_len_ignore(step):
    """new-dhcpd.rt45780.change-prefix-len.ignore"""

    misc.test_setup(step)
    srv_control.run_command(step, 'prefix-length-mode ignore;')
    srv_control.run_command(step, 'ddns-updates off;')
    srv_control.run_command(step, 'authoritative;')
    srv_control.run_command(step, 'subnet6 3000::/16 {')
    srv_control.run_command(step, ' pool6 {')
    srv_control.run_command(step, '  prefix6 3000:db8:0:100:: 3000:db8:0:100:: /64;')
    srv_control.run_command(step, '  prefix6 3000:db8:0:200:: 3000:db8:0:200:: /60;')
    srv_control.run_command(step, ' }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # Verify SOLICIT of /60 gets us a /64 prefix as the hint
    # is ignored, giving us first available
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '60')
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
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '64')
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

    # Verify REQUEST for 3000:db8:0:100::/64
    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'plen', '64')
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
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '64')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')

    # Verify RELEASE for 3000:db8:0:100::/64
    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'plen', '64')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '3000:db8:0:100::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'statuscode', '0')

    # Verify SOLICIT of /60 gets us our previous /64 prefix
    # when mode is "ignore"
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '60')
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
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '64')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')


