"""ISC_DHCP DHCPv4 Keywords"""

# pylint: disable=invalid-name,line-too-long

import pytest
from src import misc
from src import srv_control
from src import srv_msg

from src.forge_cfg import world
from src.softwaresupport.isc_dhcp6_server.functions import add_line_in_global


@pytest.mark.v4
@pytest.mark.dhcpd
def test_v4_dhcpd_keyword_use_host_decl_names_on():
    """new-v4.dhcpd.keyword.use-host-decl-names-on"""
    # Tests use-host-decl-names enabled for both a BOOTP and DHCP.
    # #
    # Message details 		Client		  Server
    # 						BOOTP_REQUEST -->
    # 		   						<--	BOOTP_REPLY
    # 						DISCOVER -->
    # 		   						<-- OFFER
    # #
    # Pass Criteria: In both instances the server's response should contain
    # the host-name option whose value is the name of the host declaration.
    # #
    misc.test_setup()
    add_line_in_global('ping-check off;')
    add_line_in_global('always-reply-rfc1048 on;')
    add_line_in_global('subnet 192.168.50.0 netmask 255.255.255.0 {')
    add_line_in_global('     authoritative;')
    add_line_in_global('}')
    add_line_in_global('group {')
    add_line_in_global('    use-host-decl-names on;')
    add_line_in_global('    host cartmen {')
    add_line_in_global(f'        hardware ethernet {world.f_cfg.cli_mac};')
    add_line_in_global('        fixed-address 192.168.50.10;')
    add_line_in_global('    }')
    add_line_in_global('}')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Do BOOTP_REQUEST, BOOTP_REPLY should have host-name = cartmen
    # misc.test_procedure()
    # srv_msg.client_sets_value('Client', 'chaddr', f'{world.f_cfg.cli_mac}')
    # srv_msg.client_send_msg('BOOTP_REQUEST')
    #
    # misc.pass_criteria()
    # srv_msg.send_wait_for_message('MUST', 'BOOTP_REPLY')
    # srv_msg.response_check_content('yiaddr', '192.168.50.10')
    # srv_msg.response_check_include_option(12)
    # srv_msg.response_check_option_content(12, 'value', 'cartmen')
    srv_msg.BOOTP_REQUEST_and_BOOTP_REPLY("192.168.50.10")
    # Do DISCOVER, OFFER should have host-name = cartmen
    misc.test_procedure()
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(12)
    srv_msg.response_check_option_content(12, 'value', 'cartmen')


@pytest.mark.v4
@pytest.mark.dhcpd
def test_v4_dhcpd_keyword_use_host_decl_names_off():
    """new-v4.dhcpd.keyword.use-host-decl-names-off"""
    # Tests use-host-decl-names enabled for both a BOOTP and DHCP.
    # #
    # Message details 		Client		  Server
    # 						BOOTP_REQUEST -->
    # 		   						<--	BOOTP_REPLY
    # 						DISCOVER -->
    # 		   						<-- OFFER
    # #
    # Pass Criteria: In both instances the server's response should NOT
    # contain the host-name option.
    # #
    misc.test_setup()
    add_line_in_global('ping-check off;')
    add_line_in_global('always-reply-rfc1048 on;')
    add_line_in_global('subnet 192.168.50.0 netmask 255.255.255.0 {')
    add_line_in_global('     authoritative;')
    add_line_in_global('}')
    add_line_in_global('group {')
    add_line_in_global('    use-host-decl-names off;')
    add_line_in_global('    host cartmen {')
    add_line_in_global(f'        hardware ethernet {world.f_cfg.cli_mac};')
    add_line_in_global('        fixed-address 192.168.50.10;')
    add_line_in_global('    }')
    add_line_in_global('}')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Do BOOTP_REQUEST, BOOTP_REPLY should not contain host-name.
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', f'{world.f_cfg.cli_mac}')
    srv_msg.client_send_msg('BOOTP_REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'BOOTP_REPLY')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(12, expect_include=False)

    # Do DISCCOVER, OFFER should not contain host-name.
    misc.test_procedure()
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(12, expect_include=False)


@pytest.mark.v4
@pytest.mark.dhcpd
def test_v4_dhcpd_keyword_use_host_decl_names_override():
    """new-v4.dhcpd.keyword.use-host-decl-names-override"""
    # Tests use-host-decl-names enabled but overridden by host-name option
    # defined within the host-declaration.
    # #
    # Message details 		Client		  Server
    # 						BOOTP_REQUEST -->
    # 		   						<--	BOOTP_REPLY
    # 						DISCOVER -->
    # 		   						<-- OFFER
    # #
    # Pass Criteria: In both instances the server's response should
    # contain the host-name option whose value is that of the defined
    # host-name option.
    # #
    misc.test_setup()
    add_line_in_global('ping-check off;')
    add_line_in_global('always-reply-rfc1048 on;')
    add_line_in_global('subnet 192.168.50.0 netmask 255.255.255.0 {')
    add_line_in_global('     authoritative;')
    add_line_in_global('}')
    add_line_in_global('group {')
    add_line_in_global('    use-host-decl-names on;')
    add_line_in_global('    host cartmen {')
    add_line_in_global(f'        hardware ethernet {world.f_cfg.cli_mac};')
    add_line_in_global('        fixed-address 192.168.50.10;')
    add_line_in_global('        option host-name "notcartmen";')
    add_line_in_global('    }')
    add_line_in_global('}')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Do BOOTP_REQUEST, BOOTP_REPLY should have host-name = notcartmen
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', f'{world.f_cfg.cli_mac}')
    srv_msg.client_send_msg('BOOTP_REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'BOOTP_REPLY')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(12)
    srv_msg.response_check_option_content(12, 'value', 'notcartmen')

    # Do DISCOVER, OFFER should have host-name = notcartmen
    misc.test_procedure()
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(12)
    srv_msg.response_check_option_content(12, 'value', 'notcartmen')
