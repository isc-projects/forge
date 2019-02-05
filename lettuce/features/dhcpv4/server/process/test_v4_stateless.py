"""DHCPv4 Stateless clients"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import misc
from features import srv_msg
from features import srv_control


@pytest.mark.v4
@pytest.mark.stateless
def test_v4_stateless_with_subnet_empty_pool(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '$(EMPTY)')
    srv_control.config_srv_opt(step, 'subnet-mask', '255.255.255.0')
    srv_control.config_srv_opt(step, 'time-offset', '50')
    srv_control.config_srv_opt(step, 'routers', '100.100.100.10,50.50.50.5')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '2')
    srv_msg.client_requests_option(step, '3')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg(step, 'INFORM')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '0.0.0.0')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_option_content(step, 'Response', '2', None, 'value', '50')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'value', '100.100.100.10')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'value', '50.50.50.5')
