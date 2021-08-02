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
@pytest.mark.default_lease_time
def test_v6_dhcpd_keyword_default_lease_time_not_set(step):
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
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::2')
    srv_control.unset_time(step, 'preferred-lifetime')
    srv_control.unset_time(step, 'valid-lifetime')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
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
@pytest.mark.default_lease_time
def test_v6_dhcpd_keyword_default_lease_time_set(step):
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
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::2')
    srv_control.unset_time(step, 'preferred-lifetime')
    srv_control.unset_time(step, 'valid-lifetime')
    srv_control.run_command(step, 'default-lease-time 1000;')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step, 'Response', '5', '3', None, 'validlft', '1000')
    srv_msg.response_check_suboption_content(step, 'Response', '5', '3', None, 'preflft', '625')


