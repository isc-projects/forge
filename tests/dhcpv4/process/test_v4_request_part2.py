"""DHCPv4 address request process"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_msg
import srv_control
import misc


@pytest.mark.v4
@pytest.mark.request
def test_v4_request_initreboot_success():
    # check if for REQUEST from client in INIT-REBOOT client state
    # the server will respond with ACK confirming its previous address

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.request
def test_v4_request_initreboot_fail():
    # check if for REQUEST with wrong address from client in INIT-REBOOT client state
    # the server will respond with NAK

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    # at first send correct address to be confirmed by server
    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    # the server should confirm it with ACK
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    # now send another REQUEST but this time with wrong address
    misc.test_procedure()
    srv_msg.client_does_include_with_value('requested_addr', '185.0.50.0')
    srv_msg.client_send_msg('REQUEST')

    #  the server should discard it with NAK
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'NAK')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')


@pytest.mark.v4
@pytest.mark.request
@pytest.mark.disabled
def test_v4_request_initreboot_no_requested_address():
    # do not allocate any address, just go straight without including requested address;
    # the server should respond with NAK

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_send_msg('REQUEST')

    #  the server should discard it with NAK
    # bug: #1608, closed as designed
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'NAK')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')


@pytest.mark.v4
@pytest.mark.request
def test_v4_request_initreboot_no_lease():
    # do not allocate any address, just go straight with including some requested address;
    # the server should respond with NAK

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    # if the server does not have any lease for this address then it should remain silent
    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()
