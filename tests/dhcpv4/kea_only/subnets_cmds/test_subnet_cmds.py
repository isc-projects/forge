"""Kea Subnet manipulation commands"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_control
import srv_msg
import misc


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_list():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.config_srv_another_subnet_no_interface('10.0.0.0/24', '10.0.0.5-10.0.0.5')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet4-get","arguments":{"id": 234}}',
                                     exp_result=3)  # expect no such subnet i.e. 3


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_get_by_id():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.config_srv_another_subnet_no_interface('10.0.0.0/24', '10.0.0.5-10.0.0.5')
    srv_control.config_srv_another_subnet_no_interface('150.0.0.0/24', '150.0.0.5-150.0.0.5')
    srv_control.config_srv('streettalk-directory-assistance-server', '2', '199.1.1.1,200.1.1.2')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet4-get","arguments":{"id":3}}')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_get_by_subnet():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.config_srv_another_subnet_no_interface('10.0.0.0/24', '10.0.0.5-10.0.0.5')
    srv_control.config_srv('domain-name-servers', '1', '199.199.199.1,100.100.100.1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet4-get","arguments":{"subnet":"10.0.0.0/24"}}')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_add():
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.config_srv_opt('domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    # Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/etc/kea/control_socket send {"command":"subnet4-list","arguments":{}}
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet4-add","arguments":{"subnet4":[{"subnet":"192.168.50.0/24","interface":"$(SERVER_IFACE)","id":234,"pools":[{"pool":"192.168.50.1-192.168.50.1"}]}]}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet4-get","arguments":{"id": 234}}')
    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_add_with_options():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '$(EMPTY)')
    srv_control.config_srv_opt('domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('6')
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_include_option('Response', None, '6')
    srv_msg.response_check_option_content('Response', '6', None, 'value', '199.199.199.1')
    srv_msg.response_check_option_content('Response', '6', None, 'value', '100.100.100.1')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    # Using UNIX socket on server in path control_socket send {"command":"subnet4-list","arguments":{}}
    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet4-add","arguments": {"subnet4": [{"subnet": "192.168.51.0/24","interface": "$(SERVER_IFACE)","id": 234,"pools": [{"pool": "192.168.51.1-192.168.51.1"}],"option-data": [{"csv-format": true,"code": 6,"data": "19.19.19.1,10.10.10.1","name": "domain-name-servers","space": "dhcp4"}]}]}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet4-get","arguments":{"id": 234}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet4-del","arguments":{"id":1}}')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_requests_option('6')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option('Response', None, '6')
    srv_msg.response_check_option_content('Response', '6', None, 'value', '19.19.19.1')
    srv_msg.response_check_option_content('Response', '6', None, 'value', '10.10.10.1')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_add_conflict():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.config_srv_opt('domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_requests_option('6')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    # Using UNIX socket on server in path control_socket send {"command":"subnet4-list","arguments":{}}
    srv_msg.send_ctrl_cmd_via_socket({"command": "subnet4-add",
                                      "arguments": {"subnet4": [{"subnet": "192.168.55.0/24",
                                                                 "interface": "$(SERVER_IFACE)",
                                                                 "id": 1,
                                                                 "pools": [{"pool": "192.168.55.1-192.168.55.1"}],
                                                                 "option-data": [{"csv-format": True,
                                                                                  "code": 6,
                                                                                  "data": "19.19.19.1,10.10.10.1",
                                                                                  "name": "domain-name-servers",
                                                                                  "space": "dhcp4"}]}]}},
                                     exp_result=1)
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet4-get","arguments":{"id": 1}}')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_requests_option('6')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_del():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.config_srv_opt('domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_requests_option('6')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet4-del","arguments":{"id":1}}')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_del_non_existing():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.config_srv_opt('domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_requests_option('6')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet4-del","arguments":{"id":2}}',
                                     exp_result=3)  # it does not exists

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_requests_option('6')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_del_global_options():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.config_srv_opt('domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_requests_option('6')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet4-del","arguments":{"id":1}}')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    # That needs subnet with empty pool to work
    # Test Procedure:
    # Client requests option 6.
    # Client sets ciaddr value to $(CIADDR).
    # Client sends INFORM message.
    #
    # Pass Criteria:
    # Server MUST respond with ACK message.
    # Response MUST include option 6.
    # Response option 6 MUST contain value 199.199.199.1.
    # Response option 6 MUST contain value 100.100.100.1.


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_add_and_del():
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.config_srv_opt('domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet4-add","arguments":{"subnet4":[{"subnet":"192.168.50.0/24","interface":"$(SERVER_IFACE)","id":66,"pools":[{"pool":"192.168.50.1-192.168.50.1"}]}]}}')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_requests_option('6')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet4-del","arguments":{"id":66}}')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()
