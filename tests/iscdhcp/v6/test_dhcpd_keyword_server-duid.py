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
@pytest.mark.server_duid
def test_v6_dhcpd_keyword_server_duid_ll(step):
    """new-v6.dhcpd.keyword.server-duid-ll"""
    # # Testing server-duid LL
    # #
    # # Message details 		Client		Server
    # # 						SOLICIT -->
    # # 		   						<--	ADVERTISE
    # # Pass Criteria:
    # #
    # # server DUID matches the configured LL value
    # #
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::2')
    srv_control.run_command(step, 'server-duid LL ethernet 00:16:6f:49:7d:9b;')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    # Response option 2 must contain duid 00:03:00:01:00:16:6f:49:7d:9b;
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.dhcpd
@pytest.mark.keyword
@pytest.mark.server_duid
def test_v6_dhcpd_keyword_server_duid_llt(step):
    """new-v6.dhcpd.keyword.server-duid-llt"""
    # # Testing server-duid LLT
    # #
    # # Message details 		Client		Server
    # # 						SOLICIT -->
    # # 		   						<--	ADVERTISE
    # # Pass Criteria:
    # #
    # # server DUID matches the configured LLT value
    # #
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::2')
    srv_control.run_command(step, 'server-duid LLT ethernet 9999 00:16:6f:49:7d:9b;')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    # Response option 2 must contain duid 00:01:00:01:27:0f:00:16:6f:49:7d:9b;
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.dhcpd
@pytest.mark.keyword
@pytest.mark.server_duid
def test_v6_dhcpd_keyword_server_duid_en(step):
    """new-v6.dhcpd.keyword.server-duid-en"""
    # # Testing server-duid EN
    # #
    # # Message details 		Client		Server
    # # 						SOLICIT -->
    # # 		   						<--	ADVERTISE
    # # Pass Criteria:
    # #
    # # server DUID matches the configured EN value
    # #
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::2')
    srv_control.run_command(step, 'server-duid EN 2495 "peter-pan";')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    # Response option 2 must contain duid 00022495peter-pan.
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')


