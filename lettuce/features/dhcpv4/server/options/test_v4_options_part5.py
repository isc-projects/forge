"""DHCPv4 options part5"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import misc
from features import srv_msg
from features import srv_control


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_nisplus_domain_name(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'nisplus-domain-name', 'nisplus-domain.com')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '64')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '64')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '64',
                                          None,
                                          'value',
                                          'nisplus-domain.com')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_nisplus_servers(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'nisplus-servers', '199.1.1.1,200.1.1.2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '65')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '65')
    srv_msg.response_check_option_content(step, 'Response', '65', None, 'value', '200.1.1.2')
    srv_msg.response_check_option_content(step, 'Response', '65', None, 'value', '199.1.1.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_mobile_ip_home_agent(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'mobile-ip-home-agent', '166.1.1.1,177.1.1.2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '68')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '68')
    srv_msg.response_check_option_content(step, 'Response', '68', None, 'value', '166.1.1.1')
    srv_msg.response_check_option_content(step, 'Response', '68', None, 'value', '177.1.1.2')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_smtp_server(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'smtp-server', '199.1.1.1,200.1.1.2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '69')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '69')
    srv_msg.response_check_option_content(step, 'Response', '69', None, 'value', '200.1.1.2')
    srv_msg.response_check_option_content(step, 'Response', '69', None, 'value', '199.1.1.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_pop_server(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'pop-server', '199.1.1.1,200.1.1.2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '70')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '70')
    srv_msg.response_check_option_content(step, 'Response', '70', None, 'value', '200.1.1.2')
    srv_msg.response_check_option_content(step, 'Response', '70', None, 'value', '199.1.1.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_nntp_server(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'nntp-server', '199.1.1.1,200.1.1.2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '71')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '71')
    srv_msg.response_check_option_content(step, 'Response', '71', None, 'value', '200.1.1.2')
    srv_msg.response_check_option_content(step, 'Response', '71', None, 'value', '199.1.1.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_www_server(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'www-server', '199.1.1.1,200.1.1.2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '72')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '72')
    srv_msg.response_check_option_content(step, 'Response', '72', None, 'value', '200.1.1.2')
    srv_msg.response_check_option_content(step, 'Response', '72', None, 'value', '199.1.1.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_finger_server(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'finger-server', '199.1.1.1,200.1.1.2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '73')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '73')
    srv_msg.response_check_option_content(step, 'Response', '73', None, 'value', '200.1.1.2')
    srv_msg.response_check_option_content(step, 'Response', '73', None, 'value', '199.1.1.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_irc_server(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'irc-server', '199.1.1.1,200.1.1.2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '74')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '74')
    srv_msg.response_check_option_content(step, 'Response', '74', None, 'value', '200.1.1.2')
    srv_msg.response_check_option_content(step, 'Response', '74', None, 'value', '199.1.1.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_streettalk_server(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'streettalk-server', '199.1.1.1,200.1.1.2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '75')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '75')
    srv_msg.response_check_option_content(step, 'Response', '75', None, 'value', '200.1.1.2')
    srv_msg.response_check_option_content(step, 'Response', '75', None, 'value', '199.1.1.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_streettalk_directory_assistance_server(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step,
                               'streettalk-directory-assistance-server',
                               '199.1.1.1,200.1.1.2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '76')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '76')
    srv_msg.response_check_option_content(step, 'Response', '76', None, 'value', '200.1.1.2')
    srv_msg.response_check_option_content(step, 'Response', '76', None, 'value', '199.1.1.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_not_requested_options(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'routers', '100.100.100.10,50.50.50.5')
    srv_control.config_srv_opt(step, 'domain-name-servers', '199.199.199.1,100.100.100.1')
    # this should include fqdn option, 15
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '6')
    srv_msg.response_check_option_content(step, 'Response', '6', None, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(step, 'Response', '6', None, 'value', '100.100.100.1')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'value', '100.100.100.10')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'value', '50.50.50.5')

    # future tests:
    # vendor-class-identifier	60	binary	false
    # nwip-suboptions	63	binary	false
    # user-class	77	binary	false
    # authenticate	90	binary	false
    # domain-search	119	binary	false
    # vivco-suboptions	124	binary	false
    # vivso-suboptions	125	binary
