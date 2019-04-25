"""DHCPv4 options part3"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_control
import misc
import srv_msg


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_ip_forwarding():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('ip-forwarding', 'True')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('19')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '19')
    srv_msg.response_check_option_content('Response', '19', None, 'value', '1')
    srv_msg.response_check_option_content('Response', '19', 'NOT ', 'value', '0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_non_local_source_routing():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('non-local-source-routing', 'True')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('20')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '20')
    srv_msg.response_check_option_content('Response', '20', None, 'value', '1')
    srv_msg.response_check_option_content('Response', '20', 'NOT ', 'value', '0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_perform_mask_discovery():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('perform-mask-discovery', 'False')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('29')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '29')
    srv_msg.response_check_option_content('Response', '29', None, 'value', '0')
    srv_msg.response_check_option_content('Response', '29', 'NOT ', 'value', '1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_mask_supplier():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('mask-supplier', 'True')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('30')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '30')
    srv_msg.response_check_option_content('Response', '30', None, 'value', '1')
    srv_msg.response_check_option_content('Response', '30', 'NOT ', 'value', '0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_router_discovery():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('router-discovery', 'True')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('31')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '31')
    srv_msg.response_check_option_content('Response', '31', None, 'value', '1')
    srv_msg.response_check_option_content('Response', '31', 'NOT ', 'value', '0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_trailer_encapsulation():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('trailer-encapsulation', 'True')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('34')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '34')
    srv_msg.response_check_option_content('Response', '34', None, 'value', '1')
    srv_msg.response_check_option_content('Response', '34', 'NOT ', 'value', '0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_ieee802_3_encapsulation():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('ieee802-3-encapsulation', 'True')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('36')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '36')
    srv_msg.response_check_option_content('Response', '36', None, 'value', '\x01')
    srv_msg.response_check_option_content('Response', '36', 'NOT ', 'value', '\x00')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_tcp_keepalive_garbage():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('tcp-keepalive-garbage', 'True')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('39')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '39')
    srv_msg.response_check_option_content('Response', '39', None, 'value', '1')
    srv_msg.response_check_option_content('Response', '39', 'NOT ', 'value', '0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_user_custom_option():

    # This test it's kind of hack, to override scapy v4 restrictions.
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_custom_opt('foo', '176', 'uint8', '123')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('176')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    # Response MUST include option 176.
    # Response option 176 MUST contain value 123.


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_user_custom_option_code_0():
    # This test it's kind of hack, to override scapy v4 restrictions.
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_custom_opt('foo', '0', 'uint8', '123')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv_during_process('DHCP', 'configuration')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_user_custom_option_using_standard_code():
    # This test it's kind of hack, to override scapy v4 restrictions.
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_custom_opt('foo', '12', 'uint8', '123')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv_during_process('DHCP', 'configuration')
