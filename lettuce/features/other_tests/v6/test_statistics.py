"""Kea Statistics"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import misc
from features import srv_msg
from features import srv_control


@pytest.mark.disabled
def test_stats_6(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_prefix(step, '3001::', '0', '90', '92')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    # message wont contain client-id option
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    srv_msg.loops(step, 'SOLICIT', 'ADVERTISE', '50')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "list-commands","arguments": {}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"statistic-get-all","arguments":{}}')

    srv_msg.loops(step, 'SOLICIT', 'ADVERTISE', '50')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"statistic-get-all","arguments":{}}')

    srv_msg.loops(step, 'SOLICIT', 'ADVERTISE', '50')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'CONFIRM')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "pkt6-received"}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "pkt6-receive-drop"}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "pkt6-parse-failed"}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "pkt6-solicit-received"}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "pkt6-confirm-received"}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "pkt6-advertise-received"}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "pkt6-reply-received"}}')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'RENEW')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "pkt6-renew-received"}}')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REBIND')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "pkt6-rebind-received"}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "pkt6-release-received"}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "pkt6-decline-received"}}')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'INFOREQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "pkt6-infrequest-received"}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "pkt6-unknown-received"}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "pkt6-sent"}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "pkt6-advertise-sent"}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "pkt6-reply-sent"}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "subnet[1].total-nas"}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "subnet[1].assigned-nas"}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "subnet[1].total-pds"}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "subnet[1].assigned-pds"}}')

    srv_msg.loops(step, 'REQUEST', 'REPLY', '50')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_PD')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_PD')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'RENEW')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "pkt6-advertise-sent"}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "pkt6-reply-sent"}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "subnet[1].total-nas"}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "subnet[1].assigned-nas"}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "subnet[1].total-pds"}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "subnet[1].assigned-pds"}}')

    srv_msg.loops(step, 'REQUEST', 'REPLY', '50')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get-all","arguments":{}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "subnet[1].total-nas"}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "subnet[1].assigned-nas"}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-reset","arguments": {"name": "pkt6-request-received"}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}')

    srv_msg.loops(step, 'SOLICIT', 'ADVERTISE', '50')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}')

    srv_msg.loops(step, 'REQUEST', 'REPLY', '50')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-remove","arguments": {"name": "pkt6-request-received"}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}')

    srv_msg.loops(step, 'SOLICIT', 'ADVERTISE', '50')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}')

    srv_msg.loops(step, 'REQUEST', 'REPLY', '50')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'IA_NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'DECLINE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "statistic-get","arguments": {"name": "pkt6-decline-received"}}')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '3000:100::/64',
                                                       '3000:100::5-3000:100::ff')
    srv_control.config_srv_prefix(step, '2001:db8:1::', '0', '90', '92')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket2')
    srv_control.start_srv(step, 'DHCP', 'reconfigured')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket2',
                                            '{"command":"statistic-get-all","arguments":{}}')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_prefix(step, '2001:db8:1::', '0', '90', '92')
    srv_control.start_srv(step, 'DHCP', 'reconfigured')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"statistic-get-all","arguments":{}}')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_prefix(step, '2001:db8:1::', '0', '90', '92')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket2')
    srv_control.start_srv(step, 'DHCP', 'reconfigured')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket2',
                                            '{"command":"statistic-get-all","arguments":{}}')

    srv_control.start_srv(step, 'DHCP', 'restarted')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket2',
                                            '{"command":"statistic-get-all","arguments":{}}')
