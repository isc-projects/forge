"""DHCPv6 Rapid commit"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_control
import srv_msg
import references
import misc


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.rapid
@pytest.mark.kea_only
def test_v6_rapid_commit_as_global_parameter():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.set_conf_parameter_global('rapid-commit', 'true')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv_during_process('DHCP', 'configuration')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.rapid
@pytest.mark.kea_only
def test_v6_rapid_commit_basic_one_subnet():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.set_conf_parameter_subnet('rapid-commit', 'true', '0')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'rapid-commit')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option('Response', None, '14')
    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.rapid
@pytest.mark.kea_only
def test_v6_rapid_commit_basic_one_subnet_rapid_not_included():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.set_conf_parameter_subnet('rapid-commit', 'true', '0')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option('Response', 'NOT ', '14')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option('Response', 'NOT ', '14')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.rapid
@pytest.mark.kea_only
def test_v6_rapid_commit_basic_two_subnets():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ff')
    srv_control.set_conf_parameter_subnet('rapid-commit', 'true', '0')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:2::/64',
                                                       '2001:db8:2::5-2001:db8:2::5')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option('Response', 'NOT ', '14')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::1')
    srv_msg.response_check_include_option('Response', 'NOT ', '14')
