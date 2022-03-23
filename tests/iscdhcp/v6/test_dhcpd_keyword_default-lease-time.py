"""ISC_DHCP DHCPv6 Keywords"""

# pylint: disable=invalid-name,line-too-long

import pytest
from src import misc
from src import srv_control
from src import srv_msg

from src.softwaresupport.isc_dhcp6_server.functions import unset_time, add_line_in_global


@pytest.mark.v6
@pytest.mark.dhcpd
def test_v6_dhcpd_keyword_default_lease_time_not_set():
    """new-v6.dhcpd.keyword.default-lease-time-not-set"""
    # #
    # # Testing lease times offered when default-lease-time
    # # is NOT specified.
    # #
    # # Message details 		Client		Server
    # # 						SOLICIT -->
    # # 		   						<--	ADVERTISE
    # # Pass Criteria:
    # #
    # # valid lifetime offered should be default of 43200.
    # # preferred lifetime should be 27000 (62.5% of valid lifetime)
    # #
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::2')
    unset_time('preferred-lifetime')
    unset_time('valid-lifetime')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'validlft', 43200)
    srv_msg.response_check_suboption_content(5, 3, 'preflft', 27000)


@pytest.mark.v6
@pytest.mark.dhcpd
def test_v6_dhcpd_keyword_default_lease_time_set():
    """new-v6.dhcpd.keyword.default-lease-time-set"""
    # #
    # # Testing lease times offered when default-lease-time
    # # is specified.
    # #
    # # Message details 		Client		Server
    # # 						SOLICIT -->
    # # 		   						<--	ADVERTISE
    # # Pass Criteria:
    # #
    # # valid lifetime offered should match default-lease-time
    # # preferred lifetime should be 62.5% of valid lifetime
    # #
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::2')
    unset_time('preferred-lifetime')
    unset_time('valid-lifetime')
    add_line_in_global('default-lease-time 1000;')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'validlft', 1000)
    srv_msg.response_check_suboption_content(5, 3, 'preflft', 625)
