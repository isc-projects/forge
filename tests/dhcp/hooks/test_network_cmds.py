# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea Subnet manipulation commands"""

# pylint: disable=line-too-long

import pytest

from src import srv_control
from src import srv_msg
from src import misc


@pytest.mark.v4
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
    srv_control.config_srv('time-servers', 0, '199.199.199.10')
    srv_control.config_srv('time-servers', 2, '199.199.199.100')
    srv_control.config_srv('time-servers', 3, '199.199.199.200')

    # first shared subnet
    srv_control.shared_subnet('192.168.50.0/24', 0)
    srv_control.shared_subnet('192.168.51.0/24', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)
    # second shared-subnet
    srv_control.shared_subnet('192.168.52.0/24', 1)
    srv_control.shared_subnet('192.168.53.0/24', 1)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-xyz"', 1)
    srv_control.set_conf_parameter_shared_subnet('relay', '{"ip-addresses": ["$(GIADDR4)"]}', 1)

    srv_control.add_hooks('libdhcp_subnet_cmds.so')

    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-list","arguments":{}}')


@pytest.mark.v4
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
    srv_control.config_srv('time-servers', 0, '199.199.199.10')
    srv_control.config_srv('time-servers', 2, '199.199.199.100')
    srv_control.config_srv('time-servers', 3, '199.199.199.200')
    srv_control.add_hooks('libdhcp_subnet_cmds.so')

    # first shared subnet
    srv_control.shared_subnet('192.168.50.0/24', 0)
    srv_control.shared_subnet('192.168.51.0/24', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)
    # second shared-subnet
    srv_control.shared_subnet('192.168.52.0/24', 1)
    srv_control.shared_subnet('192.168.53.0/24', 1)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-xyz"', 1)
    srv_control.set_conf_parameter_shared_subnet('relay', '{"ip-addresses": ["$(GIADDR4)"]}', 1)

    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-get","arguments":{"name":"name-xyz"}}')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v4_network_cmds_add():
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.config_srv_opt('domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-list","arguments":{}}', exp_result=3)
    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-add","arguments":{"shared-networks": [{"name": "name-xyz","rebind-timer": 100,"renew-timer": 100,"valid-lifetime": 400,"subnet4": [{"interface": "$(SERVER_IFACE)", "pools": [{"pool": "192.168.50.1/32"}],"rebind-timer": 2000,"renew-timer": 1000,"subnet": "192.168.50.0/24","valid-lifetime": 4000, "id": 1}]}]}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-get","arguments":{"name": "name-xyz"}}')

    srv_msg.forge_sleep(3, 'seconds')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')


@pytest.mark.v4
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
    srv_control.config_srv('time-servers', 0, '199.199.199.10')
    srv_control.config_srv('time-servers', 2, '199.199.199.100')
    srv_control.config_srv('time-servers', 3, '199.199.199.200')
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    # first shared subnet
    srv_control.shared_subnet('192.168.50.0/24', 0)
    srv_control.shared_subnet('192.168.51.0/24', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)
    # second shared-subnet
    srv_control.shared_subnet('192.168.52.0/24', 1)
    srv_control.shared_subnet('192.168.53.0/24', 1)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-xyz"', 1)
    srv_control.set_conf_parameter_shared_subnet('relay', '{"ip-addresses": ["$(GIADDR4)"]}', 1)

    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-list","arguments":{}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-add","arguments":{"shared-networks": [{"match-client-id": true,"name": "name-xyz","option-data": [],"rebind-timer": 0,"relay": {"ip-addresses": ["0.0.0.0"]},"renew-timer": 0,"reservation-mode": "all","subnet4": [{"4o6-interface": "","4o6-interface-id": "","4o6-subnet": "","boot-file-name": "","id": 3,"match-client-id": true,"next-server": "0.0.0.0","option-data": [{"always-send": false,"code": 4,"csv-format": false,"data": "C7C7C764","name": "time-servers","space": "dhcp4"}],"pools": [{"option-data": [],"pool": "192.168.52.1/32"}],"rebind-timer": 2000,"relay": {"ip-addresses": ["192.168.50.249"]},"renew-timer": 1000,"reservation-mode": "all","server-hostname": "","subnet": "192.168.52.0/24","valid-lifetime": 4000},{"4o6-interface": "","4o6-interface-id": "","4o6-subnet": "","boot-file-name": "","id": 4,"match-client-id": true,"next-server": "0.0.0.0","option-data": [{"always-send": false,"code": 4,"csv-format": false,"data": "C7C7C7C8","name": "time-servers","space": "dhcp4"}],"pools": [{"option-data": [],"pool": "192.168.53.1/32"}],"rebind-timer": 2000,"relay": {"ip-addresses": ["192.168.50.249"]},"renew-timer": 1000,"reservation-mode": "all","server-hostname": "","subnet": "192.168.53.0/24","valid-lifetime": 4000}],"valid-lifetime": 0}]}}',
                                     exp_result=1)
    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-get","arguments":{"name": "name-xyz"}}')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v4_network_cmds_del():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.1')
    srv_control.config_srv('time-servers', 0, '199.199.199.10')

    srv_control.shared_subnet('192.168.50.0/24', 0)
    srv_control.shared_subnet('192.168.51.0/24', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    srv_control.add_hooks('libdhcp_subnet_cmds.so')

    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-list","arguments":{}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-del","arguments":{"name":"name-abc","subnets-action": "delete"}}')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v4_network_cmds_del_keep_subnet():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.1')
    srv_control.config_srv('time-servers', 0, '199.199.199.10')
    srv_control.shared_subnet('192.168.50.0/24', 0)
    srv_control.shared_subnet('192.168.51.0/24', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    srv_control.add_hooks('libdhcp_subnet_cmds.so')

    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-list","arguments":{}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-del","arguments":{"name":"name-abc","subnets-action": "keep"}}')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-list","arguments":{}}', exp_result=3)


@pytest.mark.v4
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
    srv_control.config_srv('time-servers', 0, '199.199.199.10')
    srv_control.config_srv('time-servers', 2, '199.199.199.100')
    srv_control.config_srv('time-servers', 3, '199.199.199.200')
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    # first shared subnet
    srv_control.shared_subnet('192.168.50.0/24', 0)
    srv_control.shared_subnet('192.168.51.0/24', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)
    # second shared-subnet
    srv_control.shared_subnet('192.168.52.0/24', 1)
    srv_control.shared_subnet('192.168.53.0/24', 1)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-xyz"', 1)
    srv_control.set_conf_parameter_shared_subnet('relay', '{"ip-addresses": ["$(GIADDR4)"]}', 1)

    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-del","arguments":{"name":"name-xxyz,"subnets-action": "delete""}}',
                                     exp_result=1)
    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-list","arguments":{}}')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v4_network_cmds_del_global_options():
    misc.test_setup()
    srv_control.config_srv_opt('domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.config_srv_subnet('192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.config_srv_another_subnet_no_interface('192.168.50.0/24', '$(EMPTY)')

    # first shared subnet
    srv_control.shared_subnet('192.168.51.0/24', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "network4-del","arguments":{"name":"name-abc","subnets-action": "delete"}}')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    # That needs subnet with empty pool to work
    misc.test_procedure()
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(6, 'value', '100.100.100.1')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v4_network_cmds_add_and_del():
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.config_srv_opt('domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network4-add","arguments":{"shared-networks": [{"name": "name-xyz","rebind-timer": 100,"renew-timer": 100,"valid-lifetime": 400,"subnet4": [{"interface": "$(SERVER_IFACE)", "pools": [{"pool": "192.168.50.1/32"}],"rebind-timer": 2000,"renew-timer": 1000,"subnet": "192.168.50.0/24", "id": 1,"valid-lifetime": 4000}]}]}}')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "network4-del","arguments":{"name":"name-xyz","subnets-action": "delete"}}')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v6_network_cmds_list():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:e::/64',
                                                       '2001:db8:e::1-2001:db8:e::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:f::/64',
                                                       '2001:db8:f::1-2001:db8:f::1')
    srv_control.config_srv('dns-servers', 1, '2001:db8::1,2001:db8::2')
    # first shared subnet
    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.shared_subnet('2001:db8:b::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface-id', '"interface-abc"', 0)
    # second shared-subnet
    srv_control.shared_subnet('2001:db8:c::/64', 1)
    srv_control.shared_subnet('2001:db8:d::/64', 1)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-xyz"', 1)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 1)
    srv_control.shared_subnet('2001:db8:e::/64', 2)
    srv_control.shared_subnet('2001:db8:f::/64', 2)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-something"', 2)
    srv_control.set_conf_parameter_shared_subnet('relay', '{"ip-addresses":["2001:db8::1234"]}', 2)
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-list","arguments":{}}')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v6_network_cmds_get_by_name():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:e::/64',
                                                       '2001:db8:e::1-2001:db8:e::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:f::/64',
                                                       '2001:db8:f::1-2001:db8:f::1')
    srv_control.config_srv('dns-servers', 1, '2001:db8::1,2001:db8::2')
    # first shared subnet
    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.shared_subnet('2001:db8:b::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface-id', '"interface-abc"', 0)
    # second shared-subnet
    srv_control.shared_subnet('2001:db8:c::/64', 1)
    srv_control.shared_subnet('2001:db8:d::/64', 1)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-xyz"', 1)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 1)
    srv_control.shared_subnet('2001:db8:e::/64', 2)
    srv_control.shared_subnet('2001:db8:f::/64', 2)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-something"', 2)
    srv_control.set_conf_parameter_shared_subnet('relay', '{"ip-addresses":["2001:db8::1234"]}', 2)
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-get","arguments":{"name":"name-xyz"}}')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v6_network_cmds_add_on_interface():
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.config_srv_opt('preference', '123')
    # Server is configured with domain-search option with value domain1.example.com,domain2.isc.org.
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

    srv_msg.send_ctrl_cmd_via_socket('{"command": "network6-add","arguments": {"shared-networks": [{"name": "name-abc","preferred-lifetime": 3000,"rebind-timer": 2000,"renew-timer": 1000,"valid-lifetime": 4000,"subnet6":[{"subnet":"2001:db8:a::/64","id":1,"interface": "$(SERVER_IFACE)","pools":[{"pool":"2001:db8:a::1-2001:db8:a::1"}]}]}]}}')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-get","arguments":{"name": "name-abc"}}')
    srv_msg.forge_sleep(5, 'seconds')
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:22')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v6_network_cmds_add_on_interface_id():
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

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-add","arguments":{"shared-networks":[{"name": "name-abc","interface-id": "interface-abc","preferred-lifetime": 3000,"rebind-timer": 2000,"renew-timer": 1000,"valid-lifetime": 4000,"subnet6":[{"id":1,"pools": [{"pool": "2001:db8:1::1-2001:db8:1::10"}],"preferred-lifetime": 3000,"rebind-timer": 2000,"renew-timer": 1000,"reservation-mode": "all","subnet": "2001:db8:1::/64","valid-lifetime": 4000}]}]}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-get","arguments":{"name": "name-abc"}}')
    srv_msg.forge_sleep(5, 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v6_network_cmds_add_on_relay_addr():
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

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-add","arguments":{"shared-networks":[{"name": "name-abc", "relay":{"ip-addresses":["2001:db8::abcd"]},"preferred-lifetime": 3000,"rebind-timer": 2000,"renew-timer": 1000,"valid-lifetime": 4000,"subnet6":[{"id":1,"pools": [{"pool": "2001:db8:1::1-2001:db8:1::10"}],"preferred-lifetime": 3000,"rebind-timer": 2000,"renew-timer": 1000,"reservation-mode": "all","subnet": "2001:db8:1::/64", "valid-lifetime": 4000}]}]}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-get","arguments":{"name": "name-abc"}}')
    srv_msg.forge_sleep(5, 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v6_network_cmds_add_conflict():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    # first shared subnet
    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.shared_subnet('2001:db8:b::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-xyz"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-list","arguments":{}}')
    response = srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-add","arguments":{"shared-networks": [{"interface": "$(SERVER_IFACE)","name": "name-xyz","option-data": [],"preferred-lifetime": 0,"rapid-commit": false,"rebind-timer": 0,"relay": {"ip-addresses": ["::"]},"renew-timer": 0,"reservation-mode": "all","subnet6": [{"id": 3,"interface": "$(SERVER_IFACE)","option-data": [],"pd-pools": [],"pools": [{"option-data": [],"pool": "2001:db8:c::1/128"}],"preferred-lifetime": 3000,"rapid-commit": false,"rebind-timer": 2000,"relay": {"ip-addresses": ["::"]},"renew-timer": 1000,"reservation-mode": "all","subnet": "2001:db8:c::/64","valid-lifetime": 4000},{"id": 4,"interface": "$(SERVER_IFACE)","option-data": [],"pd-pools": [],"pools": [{"option-data": [],"pool": "2001:db8:d::1/128"}],"preferred-lifetime": 3000,"rapid-commit": false,"rebind-timer": 2000,"relay": {"ip-addresses": ["::"]},"renew-timer": 1000,"reservation-mode": "all","subnet": "2001:db8:d::/64","valid-lifetime": 4000}],"valid-lifetime": 0}]}}',
                                                exp_result=1)
    assert response['text'] == "duplicate network 'name-xyz' found in the configuration"

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

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_save_option('server-id')
    srv_msg.client_add_saved_option()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:22')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:22')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_add_saved_option()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:44:44')
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
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v6_network_cmds_del():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:e::/64',
                                                       '2001:db8:e::1-2001:db8:e::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:f::/64',
                                                       '2001:db8:f::1-2001:db8:f::1')
    srv_control.config_srv('dns-servers', 1, '2001:db8::1,2001:db8::2')
    # first shared subnet
    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.shared_subnet('2001:db8:b::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface-id', '"interface-abc"', 0)
    # second shared-subnet
    srv_control.shared_subnet('2001:db8:c::/64', 1)
    srv_control.shared_subnet('2001:db8:d::/64', 1)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-xyz"', 1)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 1)
    srv_control.shared_subnet('2001:db8:e::/64', 2)
    srv_control.shared_subnet('2001:db8:f::/64', 2)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-something"', 2)
    srv_control.set_conf_parameter_shared_subnet('relay', '{"ip-addresses": ["2001:db8::1234"]}', 2)
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-list","arguments":{}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "network6-del","arguments":{"name":"name-xyz","subnets-action": "delete"}}')
    # Using UNIX socket on server in path control_socket send {"command": "network6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}
    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-list","arguments":{}}')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v6_network_cmds_del_2():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    # first shared subnet
    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)
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

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-list","arguments":{}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "network6-del","arguments":{"name":"name-abc","subnets-action": "delete"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-list","arguments":{}}', exp_result=3)

    srv_msg.forge_sleep(5, 'seconds')
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
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v6_network_cmds_del_non_existing():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:e::/64',
                                                       '2001:db8:e::1-2001:db8:e::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:f::/64',
                                                       '2001:db8:f::1-2001:db8:f::1')
    srv_control.config_srv('dns-servers', 1, '2001:db8::1,2001:db8::2')
    # first shared subnet
    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.shared_subnet('2001:db8:b::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface-id', '"interface-abc"', 0)
    # second shared-subnet
    srv_control.shared_subnet('2001:db8:c::/64', 1)
    srv_control.shared_subnet('2001:db8:d::/64', 1)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-xyz"', 1)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 1)
    srv_control.shared_subnet('2001:db8:e::/64', 2)
    srv_control.shared_subnet('2001:db8:f::/64', 2)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-something"', 2)
    srv_control.set_conf_parameter_shared_subnet('relay', '{"ip-addresses": ["2001:db8::1234"]}', 2)
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-list","arguments":{}}')
    response = srv_msg.send_ctrl_cmd_via_socket('{"command": "network6-del","arguments":{"name":"name-xyzc"}}', exp_result=3)
    assert response['text'] == "no shared network with name 'name-xyzc' found"
    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-list","arguments":{}}')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v6_network_cmds_add_and_del():
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

    srv_msg.send_ctrl_cmd_via_socket('{"command": "network6-add","arguments": {"shared-networks": [{"name": "name-abc","preferred-lifetime": 3000,"rebind-timer": 2000,"renew-timer": 1000,"valid-lifetime": 4000,"subnet6":[{"subnet":"2001:db8:a::/64", "id": 1,"interface": "$(SERVER_IFACE)","pools":[{"pool":"2001:db8:a::1-2001:db8:a::1"}]}]}]}}')

    srv_msg.forge_sleep(5, 'seconds')
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
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:a::1')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "network6-del","arguments":{"name":"name-abc","subnets-action": "delete"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-list","arguments":{}}', exp_result=3)

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
