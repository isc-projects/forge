"""DHCPv4 options part3"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_control
from features import srv_msg
from features import misc


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_ip_forwarding(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'ip-forwarding', 'True')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '19')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '19')
    srv_msg.response_check_option_content(step, 'Response', '19', None, 'value', '1')
    srv_msg.response_check_option_content(step, 'Response', '19', 'NOT ', 'value', '0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_non_local_source_routing(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'non-local-source-routing', 'True')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '20')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '20')
    srv_msg.response_check_option_content(step, 'Response', '20', None, 'value', '1')
    srv_msg.response_check_option_content(step, 'Response', '20', 'NOT ', 'value', '0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_perform_mask_discovery(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'perform-mask-discovery', 'False')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '29')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '29')
    srv_msg.response_check_option_content(step, 'Response', '29', None, 'value', '0')
    srv_msg.response_check_option_content(step, 'Response', '29', 'NOT ', 'value', '1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_mask_supplier(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'mask-supplier', 'True')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '30')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '30')
    srv_msg.response_check_option_content(step, 'Response', '30', None, 'value', '1')
    srv_msg.response_check_option_content(step, 'Response', '30', 'NOT ', 'value', '0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_router_discovery(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'router-discovery', 'True')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '31')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '31')
    srv_msg.response_check_option_content(step, 'Response', '31', None, 'value', '1')
    srv_msg.response_check_option_content(step, 'Response', '31', 'NOT ', 'value', '0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_trailer_encapsulation(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'trailer-encapsulation', 'True')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '34')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '34')
    srv_msg.response_check_option_content(step, 'Response', '34', None, 'value', '1')
    srv_msg.response_check_option_content(step, 'Response', '34', 'NOT ', 'value', '0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_ieee802_3_encapsulation(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'ieee802-3-encapsulation', 'True')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '36')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '36')
    srv_msg.response_check_option_content(step, 'Response', '36', None, 'value', '1')
    srv_msg.response_check_option_content(step, 'Response', '36', 'NOT ', 'value', '0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_tcp_keepalive_garbage(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'tcp-keepalive-garbage', 'True')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '39')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '39')
    srv_msg.response_check_option_content(step, 'Response', '39', None, 'value', '1')
    srv_msg.response_check_option_content(step, 'Response', '39', 'NOT ', 'value', '0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
def test_v4_options_user_custom_option(step):

    # This test it's kind of hack, to override scapy v4 restrictions.
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_custom_opt(step, 'foo', '176', 'uint8', '123')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '176')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    # Response MUST include option 176.
    # Response option 176 MUST contain value 123.
