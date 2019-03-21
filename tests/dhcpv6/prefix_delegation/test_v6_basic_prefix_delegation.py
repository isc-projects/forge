"""DHCPv6 Prefix Delegation"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_control
import misc
import references
import srv_msg


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_onlyPD_advertise():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.config_srv_prefix('2001:db8:1::', '0', '90', '96')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'IA-PD')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '25')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_IA_and_PD():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::2-3000::2')
    srv_control.config_srv_prefix('2001:db8:1::', '0', '90', '91')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-PD')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::2')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_without_server_configuration():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'IA-PD')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option('Response', None, '25')
    srv_msg.response_check_option_content('Response', '25', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content('Response', '13', '25', None, 'statuscode', '6')

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::3-3000::3')
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
    srv_msg.response_check_suboption_content('Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '2001:db8:1::')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::3')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_exclude_prefix():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/48', '2001:db8:a::1-2001:db8:a::1')
    srv_control.add_line_to_subnet('0',
                                   ',"pd-pools":[{"prefix": "2001:db8:1::","prefix-len": 90,"delegated-len": 90,"excluded-prefix": "2001:db8:1::20:0:0","excluded-prefix-len": 91}]')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'IA-PD')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_requests_option('67')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option('Response', None, '25')
    srv_msg.response_check_option_content('Response', '25', None, 'sub-option', '26')
    # Response option 26 MUST contain sub-option 67.
    # Test works, but forge lacks support for extracting sub-options of sub-options
    references.references_check('RFC')
