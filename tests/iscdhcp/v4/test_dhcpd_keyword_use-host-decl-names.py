"""ISC_DHCP DHCPv4 Keywords"""


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
@pytest.mark.v4
@pytest.mark.dhcpd
@pytest.mark.keyword
@pytest.mark.use_host_decl_names
def test_v4_dhcpd_keyword_use_host_decl_names_on(step):
    """new-v4.dhcpd.keyword.use-host-decl-names-on"""
    # # Tests use-host-decl-names enabled for both a BOOTP and DHCP.
    # #
    # # Message details 		Client		  Server
    # # 						BOOTP_REQUEST -->
    # # 		   						<--	BOOTP_REPLY
    # # 						DISCOVER -->
    # # 		   						<-- OFFER
    # #
    # # Pass Criteria: In both instances the server's response should contain
    # # the host-name option whose value is the name of the host declaration.
    # #
    misc.test_setup(step)
    srv_control.run_command(step, 'ping-check off;')
    srv_control.run_command(step, 'always-reply-rfc1048 on;')
    srv_control.run_command(step, 'subnet 178.16.1.0 netmask 255.255.255.0 {')
    srv_control.run_command(step, '     authoritative;')
    srv_control.run_command(step, '}')
    srv_control.run_command(step, 'group {')
    srv_control.run_command(step, '    use-host-decl-names on;')
    srv_control.run_command(step, '    host cartmen {')
    srv_control.run_command(step, '        hardware ethernet $(CLI_MAC);')
    srv_control.run_command(step, '        fixed-address 178.16.1.10;')
    srv_control.run_command(step, '    }')
    srv_control.run_command(step, '}')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # Do BOOTP_REQUEST, BOOTP_REPLY should have host-name = cartmen
    misc.test_procedure(step)
    srv_msg.client_send_msg(step, 'BOOTP_REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'BOOTP_REPLY')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.10')
    srv_msg.response_check_include_option(step, 'Response', None, '12')
    srv_msg.response_check_option_content(step, 'Response', '12', None, 'value', 'cartmen')

    # Do DISCOVER, OFFER should have host-name = cartmen
    misc.test_procedure(step)
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.10')
    srv_msg.response_check_include_option(step, 'Response', None, '12')
    srv_msg.response_check_option_content(step, 'Response', '12', None, 'value', 'cartmen')



@pytest.mark.py_test
@pytest.mark.v4
@pytest.mark.dhcpd
@pytest.mark.keyword
@pytest.mark.use_host_decl_names
def test_v4_dhcpd_keyword_use_host_decl_names_off(step):
    """new-v4.dhcpd.keyword.use-host-decl-names-off"""
    # # Tests use-host-decl-names enabled for both a BOOTP and DHCP.
    # #
    # # Message details 		Client		  Server
    # # 						BOOTP_REQUEST -->
    # # 		   						<--	BOOTP_REPLY
    # # 						DISCOVER -->
    # # 		   						<-- OFFER
    # #
    # # Pass Criteria: In both instances the server's response should NOT
    # # contain the host-name option.
    # #
    misc.test_setup(step)
    srv_control.run_command(step, 'ping-check off;')
    srv_control.run_command(step, 'always-reply-rfc1048 on;')
    srv_control.run_command(step, 'subnet 178.16.1.0 netmask 255.255.255.0 {')
    srv_control.run_command(step, '     authoritative;')
    srv_control.run_command(step, '}')
    srv_control.run_command(step, 'group {')
    srv_control.run_command(step, '    use-host-decl-names off;')
    srv_control.run_command(step, '    host cartmen {')
    srv_control.run_command(step, '        hardware ethernet $(CLI_MAC);')
    srv_control.run_command(step, '        fixed-address 178.16.1.10;')
    srv_control.run_command(step, '    }')
    srv_control.run_command(step, '}')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # Do BOOTP_REQUEST, BOOTP_REPLY should not contain host-name.
    misc.test_procedure(step)
    srv_msg.client_send_msg(step, 'BOOTP_REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'BOOTP_REPLY')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.10')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '12')

    # Do DISCCOVER, OFFER should not contain host-name.
    misc.test_procedure(step)
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.10')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '12')



@pytest.mark.py_test
@pytest.mark.v4
@pytest.mark.dhcpd
@pytest.mark.keyword
@pytest.mark.use_host_decl_names
def test_v4_dhcpd_keyword_use_host_decl_names_override(step):
    """new-v4.dhcpd.keyword.use-host-decl-names-override"""
    # # Tests use-host-decl-names enabled but overridden by host-name option
    # # defined within the host-declaration.
    # #
    # # Message details 		Client		  Server
    # # 						BOOTP_REQUEST -->
    # # 		   						<--	BOOTP_REPLY
    # # 						DISCOVER -->
    # # 		   						<-- OFFER
    # #
    # # Pass Criteria: In both instances the server's response should
    # # contain the host-name option whose value is that of the defined
    # # host-name option.
    # #
    misc.test_setup(step)
    srv_control.run_command(step, 'ping-check off;')
    srv_control.run_command(step, 'always-reply-rfc1048 on;')
    srv_control.run_command(step, 'subnet 178.16.1.0 netmask 255.255.255.0 {')
    srv_control.run_command(step, '     authoritative;')
    srv_control.run_command(step, '}')
    srv_control.run_command(step, 'group {')
    srv_control.run_command(step, '    use-host-decl-names on;')
    srv_control.run_command(step, '    host cartmen {')
    srv_control.run_command(step, '        hardware ethernet $(CLI_MAC);')
    srv_control.run_command(step, '        fixed-address 178.16.1.10;')
    srv_control.run_command(step, '        option host-name "notcartmen";')
    srv_control.run_command(step, '    }')
    srv_control.run_command(step, '}')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # Do BOOTP_REQUEST, BOOTP_REPLY should have host-name = notcartmen
    misc.test_procedure(step)
    srv_msg.client_send_msg(step, 'BOOTP_REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'BOOTP_REPLY')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.10')
    srv_msg.response_check_include_option(step, 'Response', None, '12')
    srv_msg.response_check_option_content(step, 'Response', '12', None, 'value', 'notcartmen')

    # Do DISCOVER, OFFER should have host-name = notcartmen
    misc.test_procedure(step)
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.10')
    srv_msg.response_check_include_option(step, 'Response', None, '12')
    srv_msg.response_check_option_content(step, 'Response', '12', None, 'value', 'notcartmen')


