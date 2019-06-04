"""Kea Statistics"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_msg
import misc
import srv_control


@pytest.mark.disabled
def test_stats_4():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.send_ctrl_cmd_via_socket('{"command": "list-commands","arguments": {}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"statistic-get-all","arguments":{}}')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.send_ctrl_cmd_via_socket('{"command":"statistic-get-all","arguments":{}}')

    misc.test_procedure()
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'ciaddr', '0.0.0.0')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_send_msg('DECLINE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt4-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt4-discover-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt4-offer-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt4-request-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt4-ack-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt4-nak-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt4-release-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt4-decline-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt4-inform-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt4-unknown-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt4-sent"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt4-offer-sent"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt4-ack-sent"}}')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_sets_value('Client', 'ciaddr', '255.255.255.255')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'NAK')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt4-nak-sent"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt4-parse-failed"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt4-receive-drop"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "subnet[1].total-addresses"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "subnet[1].assigned-addresses"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-remove","arguments": {"name": "pkt4-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt4-received"}}')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'NAK')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt4-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-reset","arguments": {"name": "pkt4-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt4-received"}}')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'NAK')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt4-received"}}')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.1')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'reconfigured')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"statistic-get-all","arguments":{}}')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.1')
    srv_control.open_control_channel('control_socket2')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'reconfigured')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"statistic-get-all","arguments":{}}',
                                     socket_name='control_socket2')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"statistic-get-all","arguments":{}}')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'reconfigured')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"statistic-get-all","arguments":{}}')


@pytest.mark.disabled
def test_X():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_another_subnet_no_interface('3000:100::/64',
                                                       '3000:100::5-3000:100::ff')
    srv_control.config_srv_prefix('3000::', '0', '90', '92')
    srv_control.open_control_channel('control_socket2')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'reconfigured')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"statistic-get-all","arguments":{}}',
                                     socket_name='control_socket2')

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_prefix('3000::', '0', '90', '92')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'reconfigured')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"statistic-get-all","arguments":{}}')

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_prefix('3000::', '0', '90', '92')
    srv_control.open_control_channel('control_socket2')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'reconfigured')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"statistic-get-all","arguments":{}}',
                                     socket_name='control_socket2')

    srv_control.start_srv('DHCP', 'restarted')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"statistic-get-all","arguments":{}}',
                                     socket_name='control_socket2')
