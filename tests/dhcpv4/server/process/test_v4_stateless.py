"""DHCPv4 Stateless clients"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_control
import srv_msg
import misc


@pytest.mark.v4
@pytest.mark.stateless
def test_v4_stateless_with_subnet_empty_pool():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '$(EMPTY)')
    srv_control.config_srv_opt('subnet-mask', '255.255.255.0')
    srv_control.config_srv_opt('time-offset', '50')
    srv_control.config_srv_opt('routers', '100.100.100.10,50.50.50.5')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_requests_option('2')
    srv_msg.client_requests_option('3')
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '0.0.0.0')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_option_content('Response', '2', None, 'value', '50')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'value', '100.100.100.10')
    srv_msg.response_check_option_content('Response', '3', None, 'value', '50.50.50.5')
