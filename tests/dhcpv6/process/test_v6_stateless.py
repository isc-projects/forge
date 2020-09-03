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
    srv_msg.client_requests_option(27)
    srv_msg.client_requests_option(24)
    srv_msg.client_requests_option(7)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(27)
    srv_msg.response_check_option_content(27, 'addresses', '2001:db8::abc,3000::1,2000::1234')
    srv_msg.response_check_include_option(24)
    srv_msg.response_check_option_content(24, 'domains', 'domain1.example.com.,domain2.isc.org.')
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'prefval', 123)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)


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
    srv_msg.client_requests_option(27)
    srv_msg.client_requests_option(24)
    srv_msg.client_requests_option(7)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(27)
    srv_msg.response_check_option_content(27, 'addresses', '2001:db8::abc,3000::1,2000::1234')
    srv_msg.response_check_include_option(24)
    srv_msg.response_check_option_content(24, 'domains', 'domain1.example.com.,domain2.isc.org.')
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'prefval', 123)


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
    srv_msg.client_requests_option(27)
    srv_msg.client_requests_option(24)
    srv_msg.client_requests_option(7)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(27)
    srv_msg.response_check_option_content(27, 'addresses', '2001:db8::abc,3000::1,2000::1234')
    srv_msg.response_check_include_option(24)
    srv_msg.response_check_option_content(24, 'domains', 'domain1.example.com.,domain2.isc.org.')
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'prefval', 123)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)


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
    srv_msg.client_requests_option(27)
    srv_msg.client_requests_option(24)
    srv_msg.client_requests_option(7)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(27)
    srv_msg.response_check_option_content(27, 'addresses', '2001:db8::abc,3000::1,2000::1234')
    srv_msg.response_check_include_option(24)
    srv_msg.response_check_option_content(24, 'domains', 'domain1.example.com.,domain2.isc.org.')
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'prefval', 123)
