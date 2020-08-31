"""DHCPv4 options part3"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_control
import misc
import srv_msg


@pytest.mark.v4
@pytest.mark.options
def test_v4_options_ip_forwarding():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('ip-forwarding', True)
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(19)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(19)
    srv_msg.response_check_option_content(19, 'value', 1)
    srv_msg.response_check_option_content(19, 'value', 0, expect_include=False)


@pytest.mark.v4
@pytest.mark.options
def test_v4_options_non_local_source_routing():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('non-local-source-routing', True)
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(20)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(20)
    srv_msg.response_check_option_content(20, 'value', 1)
    srv_msg.response_check_option_content(20, 'value', 0, expect_include=False)


@pytest.mark.v4
@pytest.mark.options
def test_v4_options_perform_mask_discovery():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('perform-mask-discovery', False)
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(29)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(29)
    srv_msg.response_check_option_content(29, 'value', 0)
    srv_msg.response_check_option_content(29, 'value', 1, expect_include=False)


@pytest.mark.v4
@pytest.mark.options
def test_v4_options_mask_supplier():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('mask-supplier', True)
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(30)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(30)
    srv_msg.response_check_option_content(30, 'value', 1)
    srv_msg.response_check_option_content(30, 'value', 0, expect_include=False)


@pytest.mark.v4
@pytest.mark.options
def test_v4_options_router_discovery():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('router-discovery', True)
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(31)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(31)
    srv_msg.response_check_option_content(31, 'value', 1)
    srv_msg.response_check_option_content(31, 'value', 0, expect_include=False)


@pytest.mark.v4
@pytest.mark.options
def test_v4_options_trailer_encapsulation():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('trailer-encapsulation', True)
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(34)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(34)
    srv_msg.response_check_option_content(34, 'value', 1)
    srv_msg.response_check_option_content(34, 'value', 0, expect_include=False)


@pytest.mark.v4
@pytest.mark.options
def test_v4_options_ieee802_3_encapsulation():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('ieee802-3-encapsulation', True)
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(36)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(36)
    srv_msg.response_check_option_content(36, 'value', 1)
    srv_msg.response_check_option_content(36, 'value', 0, expect_include=False)


@pytest.mark.v4
@pytest.mark.options
def test_v4_options_tcp_keepalive_garbage():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('tcp-keepalive-garbage', True)
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(39)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(39)
    srv_msg.response_check_option_content(39, 'value', 1)
    srv_msg.response_check_option_content(39, 'value', 0, expect_include=False)


@pytest.mark.v4
@pytest.mark.options
def test_v4_options_user_custom_option():

    # This test it's kind of hack, to override scapy v4 restrictions.
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_custom_opt('foo', '176', 'uint8', 123)
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('176')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    # Response MUST include option 176.
    # Response option 176 MUST contain value 123.


@pytest.mark.v4
@pytest.mark.options
def test_v4_options_user_custom_option_code_0():
    # This test it's kind of hack, to override scapy v4 restrictions.
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_custom_opt('foo', 0, 'uint8', 123)
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv_during_process('DHCP', 'configuration')


@pytest.mark.v4
@pytest.mark.options
def test_v4_options_user_custom_option_using_standard_code():
    # This test it's kind of hack, to override scapy v4 restrictions.
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_custom_opt('foo', 12, 'uint8', 123)
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv_during_process('DHCP', 'configuration')
