"""ISC_DHCP DHCPv6 Tickets Prefix Length Pool Mismatch"""

# pylint: disable=invalid-name,line-too-long

import pytest
import misc
import srv_control
import srv_msg

from softwaresupport.isc_dhcp6_server.functions import add_line_in_global


@pytest.mark.v6
@pytest.mark.dhcpd
def test_dhcpd_rt45780_change_prefix_len_exact():
    """new-dhcpd.rt45780.change-prefix-len.exact"""

    misc.test_setup()
    add_line_in_global('prefix-length-mode exact;')
    add_line_in_global('ddns-updates off;')
    add_line_in_global('authoritative;')
    add_line_in_global('subnet6 2001:db8::/32 {')
    add_line_in_global(' pool6 {')
    add_line_in_global('  prefix6 2001:db8:0:100:: 2001:db8:0:100:: /64;')
    add_line_in_global('  prefix6 2001:db8:0:200:: 2001:db8:0:200:: /60;')
    add_line_in_global(' }')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Verify SOLICIT of /60 gets us a /60 prefix
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 60)
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'preflft', 3000)
    srv_msg.response_check_suboption_content(26, 25, 'validlft', 4000)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 60)
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:0:200::')

    # Verify SOLICIT of /64 gets us a /64 prefix
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 64)
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'preflft', 3000)
    srv_msg.response_check_suboption_content(26, 25, 'validlft', 4000)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 64)
    srv_msg.response_check_suboption_content(26,  25,  'prefix', '2001:db8:0:100::')

    # Save the client and server ids for REQUEST/RENEW tests
    srv_msg.client_save_option_count(1, 'client-id')
    srv_msg.client_save_option_count(1, 'server-id')

    # Verify REQUEST for 2001:db8:0:100::/64
    misc.test_procedure()
    srv_msg.client_add_saved_option_count(1)
    srv_msg.client_sets_value('Client', 'plen', 64)
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
    srv_msg.response_check_suboption_content(26, 25, 'plen', 64)
    srv_msg.response_check_suboption_content(26,  25,  'prefix', '2001:db8:0:100::')

    # Verify RELEASE for 2001:db8:0:100::/64
    misc.test_procedure()
    srv_msg.client_add_saved_option_count(1)
    srv_msg.client_sets_value('Client', 'plen', 64)
    srv_msg.client_sets_value('Client', 'prefix', '2001:db8:0:100::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'statuscode', 0)

    # Verify SOLICIT of /60 gets us a /60 prefix AFTER we released /64
    # when mode is not "ignore"
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 60)
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'preflft', 3000)
    srv_msg.response_check_suboption_content(26, 25, 'validlft', 4000)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 60)
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:0:200::')

    # #############################################################################


@pytest.mark.v6
@pytest.mark.dhcpd
def test_dhcpd_rt45780_change_prefix_len_ignore():
    """new-dhcpd.rt45780.change-prefix-len.ignore"""

    misc.test_setup()
    add_line_in_global('prefix-length-mode ignore;')
    add_line_in_global('ddns-updates off;')
    add_line_in_global('authoritative;')
    add_line_in_global('subnet6 2001:db8::/32 {')
    add_line_in_global(' pool6 {')
    add_line_in_global('  prefix6 2001:db8:0:100:: 2001:db8:0:100:: /64;')
    add_line_in_global('  prefix6 2001:db8:0:200:: 2001:db8:0:200:: /60;')
    add_line_in_global(' }')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Verify SOLICIT of /60 gets us a /64 prefix as the hint
    # is ignored, giving us first available
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 60)
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'preflft', 3000)
    srv_msg.response_check_suboption_content(26, 25, 'validlft', 4000)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 64)
    srv_msg.response_check_suboption_content(26,  25,  'prefix', '2001:db8:0:100::')

    # Save the client and server ids for REQUEST/RENEW tests
    srv_msg.client_save_option_count(1, 'client-id')
    srv_msg.client_save_option_count(1, 'server-id')

    # Verify REQUEST for 2001:db8:0:100::/64
    misc.test_procedure()
    srv_msg.client_add_saved_option_count(1)
    srv_msg.client_sets_value('Client', 'plen', 64)
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
    srv_msg.response_check_suboption_content(26, 25, 'plen', 64)
    srv_msg.response_check_suboption_content(26,  25,  'prefix', '2001:db8:0:100::')

    # Verify RELEASE for 2001:db8:0:100::/64
    misc.test_procedure()
    srv_msg.client_add_saved_option_count(1)
    srv_msg.client_sets_value('Client', 'plen', 64)
    srv_msg.client_sets_value('Client', 'prefix', '2001:db8:0:100::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'statuscode', 0)

    # Verify SOLICIT of /60 gets us our previous /64 prefix
    # when mode is "ignore"
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 60)
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'preflft', 3000)
    srv_msg.response_check_suboption_content(26, 25, 'validlft', 4000)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 64)
    srv_msg.response_check_suboption_content(26,  25,  'prefix', '2001:db8:0:100::')
