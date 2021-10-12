"""Kea Subnet manipulation commands"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_msg
import srv_control
import misc

from cb_model import setup_server_for_config_backend_cmds


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_list():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.config_srv_another_subnet_no_interface('1000::/32', '1000::5-1000::5')
    srv_control.config_srv_another_subnet_no_interface('3000::/100', '3000::5-3000::5')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-list","arguments":{}}')


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_get_by_id():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.config_srv_another_subnet_no_interface('1000::/32', '1000::5-1000::5')
    srv_control.config_srv_another_subnet_no_interface('3000::/100', '3000::5-3000::5')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-get","arguments":{"id":2}}')


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_get_by_subnet():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.config_srv_another_subnet_no_interface('1000::/32', '1000::5-1000::5')
    srv_control.config_srv_another_subnet_no_interface('3000::/100', '3000::5-3000::5')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-get","arguments":{"subnet":"3000::/100"}}')


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_add():
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.config_srv_opt('preference', '123')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-list","arguments":{}}', exp_result=3)
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-get","arguments":{"id": 234}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_add_with_options():
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.config_srv_opt('preference', '123')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)

    misc.test_procedure()
    srv_msg.client_requests_option(7)
    srv_msg.client_requests_option(24)
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 123)
    srv_msg.response_check_include_option(24)
    srv_msg.response_check_option_content(24, 'domains', 'domain1.example.com.,domain2.isc.org.')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-list","arguments":{}}', exp_result=3)
    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}],"option-data":[{"csv-format":true,"code":7,"data":"55","name":"preference","space":"dhcp6"}]}]}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-get","arguments":{"id": 234}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_requests_option(24)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 55)
    srv_msg.response_check_include_option(24)
    srv_msg.response_check_option_content(24, 'domains', 'domain1.example.com.,domain2.isc.org.')


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_add_conflict():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.config_srv_opt('preference', '123')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-list","arguments":{}}')
    response = srv_msg.send_ctrl_cmd_via_socket({"command": "subnet6-add",
                                                 "arguments": {"subnet6": [{"id": 1,
                                                                            "interface": "$(SERVER_IFACE)",
                                                                            "subnet": "2002:db8:1::/64",
                                                                            "pools": [{"pool": "2002:db8:1::10-2002:db8:1::20"}]}]}},
                                                exp_result=1)
    assert response['text'] == "ID of the new IPv6 subnet '1' is already in use"
    response = srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-get","arguments":{"id": 1}}')
    assert response['arguments']['subnet6'][0]['subnet'] == '2001:db8:1::/64'

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_del():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-list","arguments":{}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet6-del","arguments":{"id":1}}')
    # Using UNIX socket on server in path control_socket send {"command": "subnet6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-get","arguments":{"id": 1}}', exp_result=3)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_del_non_existing():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-list","arguments":{}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet6-del","arguments":{"id":2}}', exp_result=3)
    # Using UNIX socket on server in path control_socket send {"command": "subnet6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_del_global_options():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.config_srv_opt('preference', '123')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 123)

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-list","arguments":{}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet6-del","arguments":{"id":1}}')
    # Using UNIX socket on server in path control_socket send {"command": "subnet6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-get","arguments":{"id": 1}}', exp_result=3)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)

    misc.test_procedure()
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 123)


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_add_and_del():
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.config_srv_opt('preference', '123')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-list","arguments":{}}', exp_result=3)
    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-get","arguments":{"id": 234}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet6-del","arguments":{"id":234}}')
    # Using UNIX socket on server in path control_socket send {"command": "subnet6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}
    response = srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-get","arguments":{"id": 234}}', exp_result=3)
    assert response['text'] == 'No subnet with id 234 found'

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)


# Test that an user can increase a fully-allocated subnet through the use of
# subnet commands.
@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_hook_v6_subnet_grow_subnet_command(channel):
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "subnet6": [
                {
                    "id": 42,
                    "interface": "$(SERVER_IFACE)",
                    "pools": [
                        {
                            "pool": "2001:db8:1::1-2001:db8:1::1"
                        }
                    ],
                    "subnet": "2001:db8:1::/64"
                }
            ]
        },
        "command": "subnet6-add"
    }, channel=channel)
    assert response == {
        'arguments': {
            'subnets': [
                {
                    'id': 42,
                    'subnet': '2001:db8:1::/64'
                }
            ]
        },
        'result': 0,
        'text': 'IPv6 subnet added'
    }

    srv_msg.SARR('2001:db8:1::1')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "id": 42
        },
        "command": "subnet6-del"
    }, channel=channel)
    assert response == {
        'arguments': {
            'subnets': [
                {
                    'id': 42,
                    'subnet': '2001:db8:1::/64'
                }
            ]
        },
        'result': 0,
        'text': 'IPv6 subnet 2001:db8:1::/64 (id 42) deleted'
    }

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "subnet6": [
                {
                    "id": 42,
                    "interface": "$(SERVER_IFACE)",
                    "pools": [
                        {
                            "pool": "2001:db8:1::1-2001:db8:1::2"
                        }
                    ],
                    "subnet": "2001:db8:1::/64"
                }
            ]
        },
        "command": "subnet6-add"
    }, channel=channel)
    assert response == {
        'arguments': {
            'subnets': [
                {
                    'id': 42,
                    "subnet": "2001:db8:1::/64"
                }
            ]
        },
        'result': 0,
        'text': 'IPv6 subnet added'
    }

    srv_msg.SARR('2001:db8:1::1', exchange='renew-only')

    srv_msg.SARR('2001:db8:1::2', duid='00:03:00:01:f6:f5:f4:f3:f2:11')


# Test that an user can increase a fully-allocated subnet through the use of
# config backend commands.
@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_hook_v6_subnet_grow_cb_command(channel):
    misc.test_setup()
    if channel == 'http':
        srv_control.agent_control_channel()

    setup_server_for_config_backend_cmds(config_control={'config-fetch-wait-time': 1}, force_reload=False)

    srv_control.start_srv('DHCP', 'started')

    srv_msg.wait_for_message_in_log('DHCPSRV_CFGMGR_CONFIG6_MERGED Configuration backend data has been merged.', 2)

    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'remote': {
                'type': 'mysql'
            },
            'server-tags': ['all'],
            'subnets': [
                {
                    'id': 42,
                    'interface': '$(SERVER_IFACE)',
                    'pools': [
                        {
                            'pool': '2001:db8:1::1-2001:db8:1::1'
                        }
                    ],
                    'shared-network-name': None,
                    'subnet': '2001:db8:1::/64'
                }
            ]
        },
        'command': 'remote-subnet6-set'
    }, channel=channel)
    assert response == {
        'arguments': {
            'subnets': [
                {
                    'id': 42,
                    'subnet': '2001:db8:1::/64'
                }
            ]
        },
        'result': 0,
        'text': 'IPv6 subnet successfully set.'
    }

    srv_msg.wait_for_message_in_log('DHCPSRV_CFGMGR_CONFIG6_MERGED Configuration backend data has been merged.', 3)

    srv_msg.SARR('2001:db8:1::1')

    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'remote': {
                'type': 'mysql'
            },
            'subnets': [
                {
                    'id': 42
                }
            ]
        },
        'command': 'remote-subnet6-del-by-id'
    }, channel=channel)
    assert response == {
        'arguments': {
            'count': 1
        },
        'result': 0,
        'text': '1 IPv6 subnet(s) deleted.'
    }

    srv_msg.wait_for_message_in_log('DHCPSRV_CFGMGR_CONFIG6_MERGED Configuration backend data has been merged.', 4)

    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'remote': {
                'type': 'mysql'
            },
            'server-tags': ['all'],
            'subnets': [
                {
                    'id': 42,
                    'interface': '$(SERVER_IFACE)',
                    'pools': [
                        {
                            'pool': '2001:db8:1::1-2001:db8:1::2'
                        }
                    ],
                    'shared-network-name': None,
                    'subnet': '2001:db8:1::/64'
                }
            ]
        },
        'command': 'remote-subnet6-set'
    }, channel=channel)
    assert response == {
        'arguments': {
            'subnets': [
                {
                    'id': 42,
                    'subnet': '2001:db8:1::/64'
                }
            ]
        },
        'result': 0,
        'text': 'IPv6 subnet successfully set.'
    }

    srv_msg.wait_for_message_in_log('DHCPSRV_CFGMGR_CONFIG6_MERGED Configuration backend data has been merged.', 5)

    srv_msg.SARR('2001:db8:1::1', exchange='renew-only')

    srv_msg.SARR('2001:db8:1::2', duid='00:03:00:01:f6:f5:f4:f3:f2:11')
