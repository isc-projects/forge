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
@pytest.mark.network_cmds
def test_hook_v4_network_cmds_list():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.1')
    srv_control.config_srv_another_subnet_no_interface('192.168.52.0/24',
                                                       '192.168.52.1-192.168.52.1')
    srv_control.config_srv_another_subnet_no_interface('192.168.53.0/24',
                                                       '192.168.53.1-192.168.53.1')
    # first shared subnet
    srv_control.shared_subnet('0', '0')
    srv_control.shared_subnet('1', '0')
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', '0')
    # second shared-subnet
    srv_control.shared_subnet('2', '1')
    srv_control.shared_subnet('3', '1')
    srv_control.set_conf_parameter_shared_subnet('name', '"name-xyz"', '1')
    srv_control.set_conf_parameter_shared_subnet('relay', '{"ip-address":"$(GIADDR4)"}', '1')

    srv_control.config_srv('time-servers', '0', '199.199.199.10')
    srv_control.config_srv('time-servers', '2', '199.199.199.100')
    srv_control.config_srv('time-servers', '3', '199.199.199.200')
    srv_control.add_hooks('libdhcp_subnet_cmds.so')

    srv_control.open_control_channel()
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-list","arguments":{}}')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v4_network_cmds_get_by_name():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.1')
    srv_control.config_srv_another_subnet_no_interface('192.168.52.0/24',
                                                       '192.168.52.1-192.168.52.1')
    srv_control.config_srv_another_subnet_no_interface('192.168.53.0/24',
                                                       '192.168.53.1-192.168.53.1')
    # first shared subnet
    srv_control.shared_subnet('0', '0')
    srv_control.shared_subnet('1', '0')
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', '0')
    # second shared-subnet
    srv_control.shared_subnet('2', '1')
    srv_control.shared_subnet('3', '1')
    srv_control.set_conf_parameter_shared_subnet('name', '"name-xyz"', '1')
    srv_control.set_conf_parameter_shared_subnet('relay', '{"ip-address":"$(GIADDR4)"}', '1')

    srv_control.config_srv('time-servers', '0', '199.199.199.10')
    srv_control.config_srv('time-servers', '2', '199.199.199.100')
    srv_control.config_srv('time-servers', '3', '199.199.199.200')
    srv_control.add_hooks('libdhcp_subnet_cmds.so')

    srv_control.open_control_channel()
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-get","arguments":{"name":"name-xyz"}}')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v4_network_cmds_add():
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

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-list","arguments":{}}', exp_result=3)
    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-add","arguments":{"shared-networks": [{"name": "name-xyz","rebind-timer": 100,"renew-timer": 100,"valid-lifetime": 400,"subnet4": [{"interface": "$(SERVER_IFACE)", "pools": [{"pool": "192.168.50.1/32"}],"rebind-timer": 2000,"renew-timer": 1000,"subnet": "192.168.50.0/24","valid-lifetime": 4000}]}]}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-get","arguments":{"name": "name-xyz"}}')

    srv_msg.forge_sleep('3', 'seconds')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_requests_option('6')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v4_network_cmds_add_conflict():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.1')
    srv_control.config_srv_another_subnet_no_interface('192.168.52.0/24',
                                                       '192.168.52.1-192.168.52.1')
    srv_control.config_srv_another_subnet_no_interface('192.168.53.0/24',
                                                       '192.168.53.1-192.168.53.1')
    # first shared subnet
    srv_control.shared_subnet('0', '0')
    srv_control.shared_subnet('1', '0')
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', '0')
    # second shared-subnet
    srv_control.shared_subnet('2', '1')
    srv_control.shared_subnet('3', '1')
    srv_control.set_conf_parameter_shared_subnet('name', '"name-xyz"', '1')
    srv_control.set_conf_parameter_shared_subnet('relay', '{"ip-address":"$(GIADDR4)"}', '1')

    srv_control.config_srv('time-servers', '0', '199.199.199.10')
    srv_control.config_srv('time-servers', '2', '199.199.199.100')
    srv_control.config_srv('time-servers', '3', '199.199.199.200')
    srv_control.add_hooks('libdhcp_subnet_cmds.so')

    srv_control.open_control_channel()
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-list","arguments":{}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-add","arguments":{"shared-networks": [{"match-client-id": true,"name": "name-xyz","option-data": [],"rebind-timer": 0,"relay": {"ip-address": "0.0.0.0"},"renew-timer": 0,"reservation-mode": "all","subnet4": [{"4o6-interface": "","4o6-interface-id": "","4o6-subnet": "","boot-file-name": "","id": 3,"match-client-id": true,"next-server": "0.0.0.0","option-data": [{"always-send": false,"code": 4,"csv-format": false,"data": "C7C7C764","name": "time-servers","space": "dhcp4"}],"pools": [{"option-data": [],"pool": "192.168.52.1/32"}],"rebind-timer": 2000,"relay": {"ip-address": "192.168.50.249"},"renew-timer": 1000,"reservation-mode": "all","server-hostname": "","subnet": "192.168.52.0/24","valid-lifetime": 4000},{"4o6-interface": "","4o6-interface-id": "","4o6-subnet": "","boot-file-name": "","id": 4,"match-client-id": true,"next-server": "0.0.0.0","option-data": [{"always-send": false,"code": 4,"csv-format": false,"data": "C7C7C7C8","name": "time-servers","space": "dhcp4"}],"pools": [{"option-data": [],"pool": "192.168.53.1/32"}],"rebind-timer": 2000,"relay": {"ip-address": "192.168.50.249"},"renew-timer": 1000,"reservation-mode": "all","server-hostname": "","subnet": "192.168.53.0/24","valid-lifetime": 4000}],"valid-lifetime": 0}]}}',
                                     exp_result=1)
    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-get","arguments":{"name": "name-xyz"}}')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v4_network_cmds_del():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.1')
    srv_control.shared_subnet('0', '0')
    srv_control.shared_subnet('1', '0')
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', '0')

    srv_control.config_srv('time-servers', '0', '199.199.199.10')
    srv_control.add_hooks('libdhcp_subnet_cmds.so')

    srv_control.open_control_channel()
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_requests_option('6')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-list","arguments":{}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-del","arguments":{"name":"name-abc","subnets-action": "delete"}}')

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
@pytest.mark.network_cmds
def test_hook_v4_network_cmds_del_keep_subnet():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.1')
    srv_control.shared_subnet('0', '0')
    srv_control.shared_subnet('1', '0')
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', '0')

    srv_control.config_srv('time-servers', '0', '199.199.199.10')
    srv_control.add_hooks('libdhcp_subnet_cmds.so')

    srv_control.open_control_channel()
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_requests_option('6')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-list","arguments":{}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-del","arguments":{"name":"name-abc","subnets-action": "keep"}}')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_requests_option('6')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-list","arguments":{}}', exp_result=3)


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v4_network_cmds_del_non_existing():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.1')
    srv_control.config_srv_another_subnet_no_interface('192.168.52.0/24',
                                                       '192.168.52.1-192.168.52.1')
    srv_control.config_srv_another_subnet_no_interface('192.168.53.0/24',
                                                       '192.168.53.1-192.168.53.1')
    # first shared subnet
    srv_control.shared_subnet('0', '0')
    srv_control.shared_subnet('1', '0')
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', '0')
    # second shared-subnet
    srv_control.shared_subnet('2', '1')
    srv_control.shared_subnet('3', '1')
    srv_control.set_conf_parameter_shared_subnet('name', '"name-xyz"', '1')
    srv_control.set_conf_parameter_shared_subnet('relay', '{"ip-address":"$(GIADDR4)"}', '1')

    srv_control.config_srv('time-servers', '0', '199.199.199.10')
    srv_control.config_srv('time-servers', '2', '199.199.199.100')
    srv_control.config_srv('time-servers', '3', '199.199.199.200')
    srv_control.add_hooks('libdhcp_subnet_cmds.so')

    srv_control.open_control_channel()
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-del","arguments":{"name":"name-xxyz,"subnets-action": "delete""}}',
                                     exp_result=1)
    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-list","arguments":{}}')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v4_network_cmds_del_global_options():
    misc.test_setup()
    srv_control.config_srv_opt('domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.config_srv_subnet('192.168.50.0/24', '$(EMPTY)')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.1')
    # first shared subnet
    srv_control.shared_subnet('1', '0')
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', '0')

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

    srv_msg.send_ctrl_cmd_via_socket('{"command": "network4-del","arguments":{"name":"name-abc","subnets-action": "delete"}}')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    # That needs subnet with empty pool to work
    misc.test_procedure()
    srv_msg.client_requests_option('6')
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_include_option('Response', None, '6')
    srv_msg.response_check_option_content('Response', '6', None, 'value', '199.199.199.1')
    srv_msg.response_check_option_content('Response', '6', None, 'value', '100.100.100.1')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v4_network_cmds_add_and_del():
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

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-add","arguments":{"shared-networks": [{"name": "name-xyz","rebind-timer": 100,"renew-timer": 100,"valid-lifetime": 400,"subnet4": [{"interface": "$(SERVER_IFACE)", "pools": [{"pool": "192.168.50.1/32"}],"rebind-timer": 2000,"renew-timer": 1000,"subnet": "192.168.50.0/24","valid-lifetime": 4000}]}]}}')

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

    srv_msg.send_ctrl_cmd_via_socket('{"command": "network4-del","arguments":{"name":"name-xyz","subnets-action": "delete"}}')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()
