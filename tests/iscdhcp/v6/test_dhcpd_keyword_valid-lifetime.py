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
@pytest.mark.valid_lifetime
def test_v6_dhcpd_keyword_valid_lifetime_not_set(step):
    """new-v6.dhcpd.keyword.valid-lifetime-not-set"""
    # # Testing lease times offered when valid-lifetime
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
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::2')
    srv_control.unset_time(step, 'preferred-lifetime')
    srv_control.unset_time(step, 'valid-lifetime')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'validlft',
                                             '43200')
    srv_msg.response_check_suboption_content(step, 'Response', '5', '3', None, 'preflft', '27000')



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.dhcpd
@pytest.mark.keyword
@pytest.mark.valid_lifetime
def test_v6_dhcpd_keyword_valid_lifetime_set(step):
    """new-v6.dhcpd.keyword.valid-lifetime-set"""
    # # Testing lease times offered when valid-lifetime
    # # is specified.
    # #
    # # Message details 		Client		Server
    # # 						SOLICIT -->
    # # 		   						<--	ADVERTISE
    # # Pass Criteria:
    # #
    # # valid lifetime should be the configured value of 1000.
    # # preferred lifetime  should be 625.
    # #
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::2')
    srv_control.set_time(step, 'valid-lifetime', '1000')
    srv_control.unset_time(step, 'preferred-lifetime')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step, 'Response', '5', '3', None, 'validlft', '1000')
    srv_msg.response_check_suboption_content(step, 'Response', '5', '3', None, 'preflft', '625')


