"""Kea features"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_control
from features import misc
from features import srv_msg


@pytest.mark.v4
@pytest.mark.kea_only
def test_v4_echo_client_id(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.set_conf_parameter_global(step, 'echo-client-id', 'false')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040506')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '61')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040506')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '61')
