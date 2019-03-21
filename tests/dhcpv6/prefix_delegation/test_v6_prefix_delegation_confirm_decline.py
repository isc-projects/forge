"""DHCPv6 Prefix Delegation"""

# pylint: disable=invalid-name,line-too-long

import pytest

import references
import misc
import srv_control
import srv_msg


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_IA_and_PD_confirm():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::2-3000::2')
    srv_control.config_srv_prefix('2001:db8:1::', '0', '90', '96')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'IA-PD')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '25')
    srv_msg.response_check_option_content('Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content('Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '2001:db8:1::')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::2')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('CONFIRM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', 'NOT ', '25')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_IA_and_PD_decline():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::5')
    srv_control.config_srv_prefix('2001:db8:1::', '0', '90', '96')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'IA-PD')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '25')
    srv_msg.response_check_option_content('Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::5')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('DECLINE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', 'NOT ', '25')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '13')

    references.references_check('RFC')
