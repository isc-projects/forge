"""DHCPv6 Stateless clients"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_control
import misc
import srv_msg


@pytest.mark.v6
@pytest.mark.stateless
def test_v6_stateless_with_subnet_empty_pool():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '$(EMPTY)')
    srv_control.config_srv_opt('preference', '123')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv_opt('nis-servers', '2001:db8::abc,3000::1,2000::1234')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('27')
    srv_msg.client_requests_option('24')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '27')
    srv_msg.response_check_option_content('Response',
                                          '27',
                                          None,
                                          'addresses',
                                          '2001:db8::abc,3000::1,2000::1234')
    srv_msg.response_check_include_option('Response', None, '24')
    srv_msg.response_check_option_content('Response',
                                          '24',
                                          None,
                                          'domains',
                                          'domain1.example.com.,domain2.isc.org.')
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'prefval', '123')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content('Response', '13', '3', None, 'statuscode', '2')


@pytest.mark.v6
@pytest.mark.stateless
def test_v6_stateless_with_subnet_empty_pool_inforequest():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '$(EMPTY)')
    srv_control.config_srv_opt('preference', '123')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv_opt('nis-servers', '2001:db8::abc,3000::1,2000::1234')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('27')
    srv_msg.client_requests_option('24')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '27')
    srv_msg.response_check_option_content('Response',
                                          '27',
                                          None,
                                          'addresses',
                                          '2001:db8::abc,3000::1,2000::1234')
    srv_msg.response_check_include_option('Response', None, '24')
    srv_msg.response_check_option_content('Response',
                                          '24',
                                          None,
                                          'domains',
                                          'domain1.example.com.,domain2.isc.org.')
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'prefval', '123')


@pytest.mark.v6
@pytest.mark.stateless
def test_v6_stateless_without_subnet():

    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.config_srv_opt('preference', '123')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv_opt('nis-servers', '2001:db8::abc,3000::1,2000::1234')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('27')
    srv_msg.client_requests_option('24')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '27')
    srv_msg.response_check_option_content('Response',
                                          '27',
                                          None,
                                          'addresses',
                                          '2001:db8::abc,3000::1,2000::1234')
    srv_msg.response_check_include_option('Response', None, '24')
    srv_msg.response_check_option_content('Response',
                                          '24',
                                          None,
                                          'domains',
                                          'domain1.example.com.,domain2.isc.org.')
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'prefval', '123')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content('Response', '13', '3', None, 'statuscode', '2')


@pytest.mark.v6
@pytest.mark.stateless
def test_v6_stateless_without_subnet_inforequest():

    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.config_srv_opt('preference', '123')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv_opt('nis-servers', '2001:db8::abc,3000::1,2000::1234')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('27')
    srv_msg.client_requests_option('24')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '27')
    srv_msg.response_check_option_content('Response',
                                          '27',
                                          None,
                                          'addresses',
                                          '2001:db8::abc,3000::1,2000::1234')
    srv_msg.response_check_include_option('Response', None, '24')
    srv_msg.response_check_option_content('Response',
                                          '24',
                                          None,
                                          'domains',
                                          'domain1.example.com.,domain2.isc.org.')
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'prefval', '123')
