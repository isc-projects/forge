"""DHCPv6 Stateless clients"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import misc
from features import srv_msg
from features import srv_control


@pytest.mark.v6
@pytest.mark.stateless
def test_v6_stateless_with_subnet_empty_pool(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '$(EMPTY)')
    srv_control.config_srv_opt(step, 'preference', '123')
    srv_control.config_srv_opt(step, 'domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv_opt(step, 'nis-servers', '2001:db8::abc,3000::1,2000::1234')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '27')
    srv_msg.client_requests_option(step, '24')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '27')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '27',
                                          None,
                                          'addresses',
                                          '2001:db8::abc,3000::1,2000::1234')
    srv_msg.response_check_include_option(step, 'Response', None, '24')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '24',
                                          None,
                                          'domains',
                                          'domain1.example.com,domain2.isc.org')
    srv_msg.response_check_include_option(step, 'Response', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', None, 'prefval', '123')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content(step, 'Response', '13', '3', None, 'statuscode', '2')


@pytest.mark.v6
@pytest.mark.stateless
def test_v6_stateless_with_subnet_empty_pool_inforequest(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '$(EMPTY)')
    srv_control.config_srv_opt(step, 'preference', '123')
    srv_control.config_srv_opt(step, 'domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv_opt(step, 'nis-servers', '2001:db8::abc,3000::1,2000::1234')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '27')
    srv_msg.client_requests_option(step, '24')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'INFOREQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '27')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '27',
                                          None,
                                          'addresses',
                                          '2001:db8::abc,3000::1,2000::1234')
    srv_msg.response_check_include_option(step, 'Response', None, '24')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '24',
                                          None,
                                          'domains',
                                          'domain1.example.com,domain2.isc.org')
    srv_msg.response_check_include_option(step, 'Response', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', None, 'prefval', '123')


@pytest.mark.v6
@pytest.mark.stateless
def test_v6_stateless_without_subnet(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '$(EMPTY)', '$(EMPTY)')
    srv_control.config_srv_opt(step, 'preference', '123')
    srv_control.config_srv_opt(step, 'domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv_opt(step, 'nis-servers', '2001:db8::abc,3000::1,2000::1234')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '27')
    srv_msg.client_requests_option(step, '24')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '27')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '27',
                                          None,
                                          'addresses',
                                          '2001:db8::abc,3000::1,2000::1234')
    srv_msg.response_check_include_option(step, 'Response', None, '24')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '24',
                                          None,
                                          'domains',
                                          'domain1.example.com,domain2.isc.org')
    srv_msg.response_check_include_option(step, 'Response', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', None, 'prefval', '123')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content(step, 'Response', '13', '3', None, 'statuscode', '2')


@pytest.mark.v6
@pytest.mark.stateless
def test_v6_stateless_without_subnet_inforequest(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '$(EMPTY)', '$(EMPTY)')
    srv_control.config_srv_opt(step, 'preference', '123')
    srv_control.config_srv_opt(step, 'domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv_opt(step, 'nis-servers', '2001:db8::abc,3000::1,2000::1234')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '27')
    srv_msg.client_requests_option(step, '24')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'INFOREQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '27')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '27',
                                          None,
                                          'addresses',
                                          '2001:db8::abc,3000::1,2000::1234')
    srv_msg.response_check_include_option(step, 'Response', None, '24')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '24',
                                          None,
                                          'domains',
                                          'domain1.example.com,domain2.isc.org')
    srv_msg.response_check_include_option(step, 'Response', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', None, 'prefval', '123')
