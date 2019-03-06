"""DHCPv4 address request process"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_control
import misc
import srv_msg


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.request
def test_v4_request_renewing_success():

    misc.test_setup()
    srv_control.set_time('renew-timer', '2')
    srv_control.set_time('rebind-timer', '50')
    srv_control.set_time('valid-lifetime', '500')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    # make sure that T1 time expires and client will be in RENEWING state.
    srv_msg.forge_sleep('3', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.request
def test_v4_request_rebinding_success():

    misc.test_setup()
    srv_control.set_time('renew-timer', '2')
    srv_control.set_time('rebind-timer', '3')
    srv_control.set_time('valid-lifetime', '500')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    # make sure that T1 time expires and client will be in RENEWING state.
    srv_msg.forge_sleep('4', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.request
def test_v4_request_rebinding_fail():

    misc.test_setup()
    srv_control.set_time('renew-timer', '2')
    srv_control.set_time('rebind-timer', '3')
    srv_control.set_time('valid-lifetime', '4')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    # make sure that leases time expires
    srv_msg.forge_sleep('5', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'NAK')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')
