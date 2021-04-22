"""DHCPv4 options part5"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_msg
import srv_control
import misc


@pytest.mark.v4
@pytest.mark.options
def test_v4_options_nisplus_domain_name():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('nisplus-domain-name', 'nisplus-domain.com')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(64)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(64)
    srv_msg.response_check_option_content(64, 'value', 'nisplus-domain.com')


@pytest.mark.v4
@pytest.mark.options
def test_v4_options_nisplus_servers():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('nisplus-servers', '199.1.1.1,200.1.1.2')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(65)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(65)
    srv_msg.response_check_option_content(65, 'value', '200.1.1.2')
    srv_msg.response_check_option_content(65, 'value', '199.1.1.1')


@pytest.mark.v4
@pytest.mark.options
def test_v4_options_mobile_ip_home_agent():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('mobile-ip-home-agent', '166.1.1.1,177.1.1.2')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(68)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(68)
    srv_msg.response_check_option_content(68, 'value', '166.1.1.1')
    srv_msg.response_check_option_content(68, 'value', '177.1.1.2')


@pytest.mark.v4
@pytest.mark.options
def test_v4_options_smtp_server():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('smtp-server', '199.1.1.1,200.1.1.2')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(69)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(69)
    srv_msg.response_check_option_content(69, 'value', '200.1.1.2')
    srv_msg.response_check_option_content(69, 'value', '199.1.1.1')


@pytest.mark.v4
@pytest.mark.options
def test_v4_options_pop_server():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('pop-server', '199.1.1.1,200.1.1.2')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(70)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(70)
    srv_msg.response_check_option_content(70, 'value', '200.1.1.2')
    srv_msg.response_check_option_content(70, 'value', '199.1.1.1')


@pytest.mark.v4
@pytest.mark.options
def test_v4_options_nntp_server():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('nntp-server', '199.1.1.1,200.1.1.2')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(71)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(71)
    srv_msg.response_check_option_content(71, 'value', '200.1.1.2')
    srv_msg.response_check_option_content(71, 'value', '199.1.1.1')


@pytest.mark.v4
@pytest.mark.options
def test_v4_options_www_server():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('www-server', '199.1.1.1,200.1.1.2')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(72)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(72)
    srv_msg.response_check_option_content(72, 'value', '200.1.1.2')
    srv_msg.response_check_option_content(72, 'value', '199.1.1.1')


@pytest.mark.v4
@pytest.mark.options
def test_v4_options_finger_server():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('finger-server', '199.1.1.1,200.1.1.2')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(73)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(73)
    srv_msg.response_check_option_content(73, 'value', '200.1.1.2')
    srv_msg.response_check_option_content(73, 'value', '199.1.1.1')


@pytest.mark.v4
@pytest.mark.options
def test_v4_options_irc_server():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('irc-server', '199.1.1.1,200.1.1.2')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(74)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(74)
    srv_msg.response_check_option_content(74, 'value', '200.1.1.2')
    srv_msg.response_check_option_content(74, 'value', '199.1.1.1')


@pytest.mark.v4
@pytest.mark.options
def test_v4_options_streettalk_server():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('streettalk-server', '199.1.1.1,200.1.1.2')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(75)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(75)
    srv_msg.response_check_option_content(75, 'value', '200.1.1.2')
    srv_msg.response_check_option_content(75, 'value', '199.1.1.1')


@pytest.mark.v4
@pytest.mark.options
def test_v4_options_streettalk_directory_assistance_server():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('streettalk-directory-assistance-server', '199.1.1.1,200.1.1.2')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(76)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(76)
    srv_msg.response_check_option_content(76, 'value', '200.1.1.2')
    srv_msg.response_check_option_content(76, 'value', '199.1.1.1')


@pytest.mark.v4
@pytest.mark.options
def test_v4_options_not_requested_options():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('routers', '100.100.100.10,50.50.50.5')
    srv_control.config_srv_opt('domain-name-servers', '199.199.199.1,100.100.100.1')
    # this should include fqdn option, 15
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(6, 'value', '100.100.100.1')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'value', '100.100.100.10')
    srv_msg.response_check_option_content(3, 'value', '50.50.50.5')

    # future tests:
    # vendor-class-identifier	60	binary	false
    # nwip-suboptions	63	binary	false
    # user_class	77	binary	false
    # authenticate	90	binary	false
    # domain-search	119	binary	false
    # vivco-suboptions	124	binary	false
    # vivso-suboptions	125	binary
