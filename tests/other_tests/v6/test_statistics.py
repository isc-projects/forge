"""Kea Statistics"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_msg
import srv_control
import misc


@pytest.mark.disabled
def test_stats_6():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_prefix('3001::', '0', '90', '92')
    srv_control.open_control_channel()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    # message wont contain client-id option
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.loops('SOLICIT', 'ADVERTISE', '50')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "list-commands","arguments": {}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"statistic-get-all","arguments":{}}')

    srv_msg.loops('SOLICIT', 'ADVERTISE', '50')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"statistic-get-all","arguments":{}}')

    srv_msg.loops('SOLICIT', 'ADVERTISE', '50')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('CONFIRM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-receive-drop"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-parse-failed"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-solicit-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-confirm-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-advertise-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-reply-received"}}')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-renew-received"}}')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REBIND')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-rebind-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-release-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-decline-received"}}')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-infrequest-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-unknown-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-sent"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-advertise-sent"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-reply-sent"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "subnet[1].total-nas"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "subnet[1].assigned-nas"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "subnet[1].total-pds"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "subnet[1].assigned-pds"}}')

    srv_msg.loops('REQUEST', 'REPLY', '50')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'IA-PD')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-advertise-sent"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-reply-sent"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "subnet[1].total-nas"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "subnet[1].assigned-nas"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "subnet[1].total-pds"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "subnet[1].assigned-pds"}}')

    srv_msg.loops('REQUEST', 'REPLY', '50')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get-all","arguments":{}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "subnet[1].total-nas"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "subnet[1].assigned-nas"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-reset","arguments": {"name": "pkt6-request-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}')

    srv_msg.loops('SOLICIT', 'ADVERTISE', '50')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}')

    srv_msg.loops('REQUEST', 'REPLY', '50')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-remove","arguments": {"name": "pkt6-request-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}')

    srv_msg.loops('SOLICIT', 'ADVERTISE', '50')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}')

    srv_msg.loops('REQUEST', 'REPLY', '50')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    misc.test_procedure()
    srv_msg.client_save_option('IA_NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('DECLINE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-decline-received"}}')

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_another_subnet_no_interface('3000:100::/64',
                                                       '3000:100::5-3000:100::ff')
    srv_control.config_srv_prefix('2001:db8:1::', '0', '90', '92')
    srv_control.open_control_channel('control_socket2')
    srv_control.start_srv('DHCP', 'reconfigured')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"statistic-get-all","arguments":{}}',
                                     socket_name='control_socket2')

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_prefix('2001:db8:1::', '0', '90', '92')
    srv_control.start_srv('DHCP', 'reconfigured')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"statistic-get-all","arguments":{}}')

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_prefix('2001:db8:1::', '0', '90', '92')
    srv_control.open_control_channel('control_socket2')
    srv_control.start_srv('DHCP', 'reconfigured')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"statistic-get-all","arguments":{}}',
                                     socket_name='control_socket2')

    srv_control.start_srv('DHCP', 'restarted')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"statistic-get-all","arguments":{}}',
                                     socket_name='control_socket2')
