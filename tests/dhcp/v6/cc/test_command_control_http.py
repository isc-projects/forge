# Copyright (C) 2022-2026 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea Control Channel Agent - HTTP"""

# pylint: disable=line-too-long

import ipaddress
import pytest

from src import misc
from src import srv_msg
from src import srv_control
from src.forge_cfg import world
from src.softwaresupport.multi_server_functions import fabric_sudo_command


@pytest.mark.v6
@pytest.mark.controlchannel
def test_control_channel_http_dhcp_disable_timer():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::1')

    srv_msg.send_ctrl_cmd_via_http({"command": "dhcp-disable", "service": ["dhcp6"], "arguments": {"max-period": 5}},
                                   '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.forge_sleep(7, 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
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
def test_control_channel_http_dhcp_disable():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::1')

    srv_msg.send_ctrl_cmd_via_http({"command": "dhcp-disable", "service": ["dhcp6"]},
                                   '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()


@pytest.mark.v6
@pytest.mark.controlchannel
def test_control_channel_http_dhcp_disable_and_enable():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::1')

    srv_msg.send_ctrl_cmd_via_http({"command": "dhcp-disable", "service": ["dhcp6"]},
                                   '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.send_ctrl_cmd_via_http({"command": "dhcp-enable", "service": ["dhcp6"]},
                                   '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
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
def test_control_channel_http_config_set_basic():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_http({"command": "list-commands", "service": ["dhcp6"], "arguments": {}},
                                   '$(SRV4_ADDR)')
    srv_msg.send_ctrl_cmd_via_http({"command": "config-write", "service": ["dhcp6"], "arguments": {
                                   "filename": "config-modified-2017-03-15.json"}}, '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::1')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')

    # Server has control agent configured on HTTP connection with address $(SRV4_ADDR):8000 and socket unix path: control_socket.
    srv_control.build_config_files()
    srv_msg.send_ctrl_cmd_via_http({"command": "config-set", "service": ["dhcp6"], "arguments":  world.dhcp_cfg},
                                   '$(SRV4_ADDR)')

    srv_msg.forge_sleep('$(SLEEP_TIME_2)', 'seconds')
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
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
@pytest.mark.controlchannel
def test_control_channel_http_change_socket_during_reconfigure():
    # change address test needed also
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    result = srv_msg.send_ctrl_cmd_via_http({"command": "config-get", "service": ["dhcp6"], "arguments": {}},
                                            '$(SRV4_ADDR)')
    assert result[0]['result'] == 0

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::1')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.add_unix_socket(socket_name='control_socket2')
    srv_control.add_http_control_channel('$(SRV4_ADDR)', socket_name='control_socket2')

    # reconfigure dhcp6 (new subnet, new socket)
    srv_control.build_config_files()
    srv_msg.send_ctrl_cmd_via_http({"command": "config-set", "service": ["dhcp6"], "arguments":  world.dhcp_cfg},
                                   '$(SRV4_ADDR)')
    # reconfigure control-agent to switch to new dhcp4 socket
    if world.f_cfg.control_agent:
        srv_msg.send_ctrl_cmd_via_http({"command": "config-set", "arguments":  world.ca_cfg},
                                       '$(SRV4_ADDR)')
    srv_msg.forge_sleep('$(SLEEP_TIME_2)', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    result = srv_msg.send_ctrl_cmd_via_http({"command": "config-get", "service": ["dhcp6"], "arguments": {}},
                                            '$(SRV4_ADDR)')
    assert result[0]['result'] == 0


@pytest.mark.v6
@pytest.mark.controlchannel
def test_control_channel_http_after_restart_load_config_file():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::1')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.add_http_control_channel('$(SRV4_ADDR)')
    srv_control.build_config_files()

    srv_msg.send_ctrl_cmd_via_http({"command": "config-set", "service": ["dhcp6"], "arguments":  world.dhcp_cfg},
                                   '$(SRV4_ADDR)')

    srv_msg.forge_sleep('$(SLEEP_TIME_2)', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_control.start_srv('DHCP', 'restarted')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::1')


@pytest.mark.v6
@pytest.mark.controlchannel
def test_control_channel_http_get_config():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_http({"command": "config-get", "service": ["dhcp6"], "arguments": {}},
                                   '$(SRV4_ADDR)')


@pytest.mark.v6
@pytest.mark.controlchannel
def test_control_channel_http_test_config():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::1')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 96)
    srv_control.add_http_control_channel('$(SRV4_ADDR)')
    srv_control.config_srv_id('LLT', '00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8')
    srv_control.config_srv_opt('sip-server-addr', '2001:db8::1,2001:db8::2')
    srv_control.config_srv_opt('new-posix-timezone', 'EST5EDT4\\,M3.2.0/02:00\\,M11.1.0/02:00')
    srv_control.host_reservation_in_subnet('ip-address',
                                           '3000::1',
                                           0,
                                           'duid',
                                           '00:03:00:01:f6:f5:f4:f3:f2:01')

    srv_control.build_config_files()
    response = srv_msg.send_ctrl_cmd_via_http({"command": "config-test", "service": ["dhcp6"],
                                              "arguments":  world.dhcp_cfg}, '$(SRV4_ADDR)', exp_result=1)

    assert "specified reservation \'3000::1\' is not within the IPv6 subnet \'2001:db8:a::/64\'" in response[0]['text']
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::1')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 96)
    srv_control.add_http_control_channel('$(SRV4_ADDR)')
    srv_control.config_srv_id('LLT', '00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8')
    srv_control.config_srv_opt('sip-server-addr', '2001:db8::1,2001:db8::2')
    srv_control.config_srv_opt('new-posix-timezone', 'EST5EDT4\\,M3.2.0/02:00\\,M11.1.0/02:00')
    # WRONG ADDRESS RESERVATION
    srv_control.host_reservation_in_subnet('ip-address',
                                           '192.168.0.5',
                                           0,
                                           'duid',
                                           '00:03:00:01:f6:f5:f4:f3:f2:01')

    srv_control.build_config_files()
    response = srv_msg.send_ctrl_cmd_via_http({"command": "config-test", "service": ["dhcp6"], "arguments":  world.dhcp_cfg},
                                              '$(SRV4_ADDR)', exp_result=1)
    assert "invalid prefix '192.168.0.5' for new IPv6 reservation" in response[0]['text']

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::1')


@pytest.mark.v6
@pytest.mark.controlchannel
def test_control_channel_http_config_write():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # 1. check if configured subnet works and assigns addresses from 3000:
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::1')

    # 2. change configuration, subnet addresses pool is from 2001:db8:1:
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.add_http_control_channel('$(SRV4_ADDR)')

    srv_control.build_config_files()
    srv_msg.send_ctrl_cmd_via_socket({"command": "config-set", "service": ["dhcp6"], "arguments":  world.dhcp_cfg})

    srv_msg.forge_sleep('$(SLEEP_TIME_2)', 'seconds')

    # 3. check if configured subnet works and assigns addresses from 2001:db8:1:
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')

    # 4. restart the server, now it should revert to original configuration
    # and serve addressed from 3000: pool
    srv_control.start_srv('DHCP', 'restarted')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::1')


@pytest.mark.v6
@pytest.mark.controlchannel
def test_control_channel_http_reload_config():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::1')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()

    srv_msg.send_ctrl_cmd_via_http({"command": "config-reload", "service": ["dhcp6"], "arguments": {}},
                                   '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_control.start_srv('DHCP', 'restarted')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')


def _generate_ip_address_shift():
    """Function searches for IP addresses that can be used for additional sockets.

    :return: list of IP address shifts that can be used for additional sockets
    :rtype: list
    """
    ciaddr = ipaddress.IPv4Interface(f'{world.f_cfg.ciaddr}/24')
    srv4_addr = ipaddress.IPv4Interface(f'{world.f_cfg.srv4_addr}/24')
    # check if srv4_addr is bigger than ciaddr and 4 more addresses will fit in the same subnet
    if srv4_addr.ip > ciaddr.ip and (srv4_addr + 4).network.subnet_of(srv4_addr.network):
        return [1, 2, 3]
    # if not, check if srv4_addr is bigger than ciaddr + 4 and 4 more addresses will fit between them.
    if srv4_addr.ip > (ciaddr + 4).ip:
        return [-1, -2, -3]
    # if not, select addresses before ciaddr
    return [-5, -6, -7]


# Fixture to configure additional IP address for tests.
@pytest.fixture()
def _prepare_multiple_http_env():
    """Prepare environment for multiple http control channels.

    This fixture will add additional IP addresses to the server interface and remove them after the test
    """
    ip_address_shift = _generate_ip_address_shift()
    srv4_addr = ipaddress.ip_address(world.f_cfg.srv4_addr)
    # Assign additional IP addresses to server interface
    for ip_shift in ip_address_shift:
        new_ip = srv4_addr + ip_shift
        fabric_sudo_command(f'ip address replace {new_ip}/24 dev {world.f_cfg.server_iface}')
    yield
    for ip_shift in ip_address_shift:
        new_ip = srv4_addr + ip_shift
        fabric_sudo_command(f'ip address del {new_ip}/24 dev {world.f_cfg.server_iface}')


@pytest.mark.usefixtures('_prepare_multiple_http_env')
@pytest.mark.v6
@pytest.mark.controlchannel
def test_control_channel_multiple_http_basic():
    """Test multiple http control channels.

    This test will add additional IP addresses to the server interface and open http control channels on them.
    It will then send config-get command to all addresses and check if the response is the same.
    """
    if world.f_cfg.control_agent:
        pytest.skip('This test requires CA to be disabled. Making tests not viable because of CA deprecation.')

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.add_unix_socket()

    # Generate ip addresses for http sockets
    srv4_addr = ipaddress.ip_address(world.f_cfg.srv4_addr)
    srv_ip_addresses = [world.f_cfg.srv4_addr]
    ip_address_shift = _generate_ip_address_shift()
    for ip_shift in ip_address_shift:
        srv_ip_addresses.append(srv4_addr + ip_shift)

    # Add http sockets for all addresses
    for ip in srv_ip_addresses:
        srv_control.add_http_control_channel(ip, append=True)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    for ip in srv_ip_addresses:
        srv_msg.send_ctrl_cmd_via_http({"command": "config-get", "service": ["dhcp6"], "arguments": {}}, ip)


@pytest.mark.usefixtures('_prepare_multiple_http_env')
@pytest.mark.v6
@pytest.mark.controlchannel
def test_control_channel_multiple_http_one_address():
    """Test multiple http control channels.

    This test will add additional IP addresses to the server interface open http control channels on them.
    It will then send config-get command to all addresses and check if the response is correct.
    """
    if world.f_cfg.control_agent:
        pytest.skip('This test requires CA to be disabled. Making tests not viable because of CA deprecation.')

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.add_unix_socket()

    # Generate ip addresses for http sockets
    srv4_addr = ipaddress.ip_address(world.f_cfg.srv4_addr)
    srv_ip_addresses = [world.f_cfg.srv4_addr]
    ip_address_shift = _generate_ip_address_shift()
    for ip_shift in ip_address_shift:
        srv_ip_addresses.append(srv4_addr + ip_shift)

    # Add http sockets for one address
    srv_control.add_http_control_channel(srv_ip_addresses[0])

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Send config-get command to the first address
    srv_msg.send_ctrl_cmd_via_http({"command": "config-get", "service": ["dhcp6"], "arguments": {}}, srv_ip_addresses[0])

    # Send config-get command to the other addresses, it should fail
    for ip in srv_ip_addresses[1:]:
        srv_msg.send_ctrl_cmd_via_http({"command": "config-get", "service": ["dhcp6"], "arguments": {}}, ip, exp_failed=True)

    # Send config-get command to the first address again to make sure server still works
    srv_msg.send_ctrl_cmd_via_http({"command": "config-get", "service": ["dhcp6"], "arguments": {}}, srv_ip_addresses[0])


@pytest.mark.usefixtures('_prepare_multiple_http_env')
@pytest.mark.v6
@pytest.mark.controlchannel
def test_control_channel_http_127_0_0_1():
    """Test local http control channel.

    This test will add additional IP addresses to the server interface and add http control channel to 127.0.0.1.
    It will then send config-get command to all addresses and check if the response is correct.
    """
    if world.f_cfg.control_agent:
        pytest.skip('This test requires CA to be disabled. Making tests not viable because of CA deprecation.')

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.add_unix_socket()

    # Generate ip addresses for http sockets
    srv4_addr = ipaddress.ip_address(world.f_cfg.srv4_addr)
    srv_ip_addresses = [world.f_cfg.srv4_addr]
    ip_address_shift = _generate_ip_address_shift()
    for ip_shift in ip_address_shift:
        srv_ip_addresses.append(srv4_addr + ip_shift)

    # Add http sockets for one address
    srv_control.add_http_control_channel('127.0.0.1')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Send config-get command to all specified addresses, it should fail
    for ip in srv_ip_addresses:
        srv_msg.send_ctrl_cmd_via_http({"command": "config-get", "service": ["dhcp6"], "arguments": {}}, ip, exp_failed=True)

    # Send SARR to make sure server still works
    srv_msg.SARR('3000::1')

    # Send config-get command to 127.0.0.1 from within the server.
    http_command = '\'{"command": "config-get","service":["dhcp6"],"arguments": {} }\''
    cmd = f'curl -X POST -H "Content-Type: application/json" -d {http_command} -u "{world.f_cfg.auth_user}:{world.f_cfg.auth_passwd}" http://127.0.0.1:8000'
    result = fabric_sudo_command(cmd)
    assert '"result": 0' in result


@pytest.mark.usefixtures('_prepare_multiple_http_env')
@pytest.mark.v6
@pytest.mark.controlchannel
def test_control_channel_http_0_0_0_0():
    """Test local http control channel.

    This test will add additional IP addresses to the server interface and add http control channel to 0.0.0.0.
    It will then send config-get command to all addresses and check if the response is correct.
    """
    if world.f_cfg.control_agent:
        pytest.skip('This test requires CA to be disabled. Making tests not viable because of CA deprecation.')

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.add_unix_socket()

    # Generate ip addresses for http sockets
    srv4_addr = ipaddress.ip_address(world.f_cfg.srv4_addr)
    srv_ip_addresses = [world.f_cfg.srv4_addr]
    ip_address_shift = _generate_ip_address_shift()
    for ip_shift in ip_address_shift:
        srv_ip_addresses.append(srv4_addr + ip_shift)

    # Add http sockets for one address
    srv_control.add_http_control_channel('0.0.0.0')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Send config-get command to all specified addresses.
    for ip in srv_ip_addresses:
        srv_msg.send_ctrl_cmd_via_http({"command": "config-get", "service": ["dhcp6"], "arguments": {}}, ip)


@pytest.mark.usefixtures('_prepare_multiple_http_env')
@pytest.mark.v6
@pytest.mark.controlchannel
def test_control_channel_multiple_http_reload_config():
    """Test if sockets close properly after config reload.

    This test will add additional IP addresses to the server interface and open http control channels on them.
    It will then send config-reload command and check if the sockets are closed.
    """
    if world.f_cfg.control_agent:
        pytest.skip('This test requires CA to be disabled. Making tests not viable because of CA deprecation.')

    # Generate ip addresses for http sockets
    srv4_addr = ipaddress.ip_address(world.f_cfg.srv4_addr)
    srv_ip_addresses = [world.f_cfg.srv4_addr]
    ip_address_shift = _generate_ip_address_shift()
    for ip_shift in ip_address_shift:
        srv_ip_addresses.append(srv4_addr + ip_shift)

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.add_unix_socket()
    # Add http sockets for all addresses
    for ip in srv_ip_addresses:
        srv_control.add_http_control_channel(ip, append=True)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Send config-get command to all addresses
    for ip in srv_ip_addresses:
        srv_msg.send_ctrl_cmd_via_http({"command": "config-get", "service": ["dhcp6"], "arguments": {}}, ip)

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.add_unix_socket()
    # Configure only one address
    srv_control.add_http_control_channel(srv_ip_addresses[0])
    srv_control.build_and_send_config_files()

    srv_msg.send_ctrl_cmd_via_http({"command": "config-reload", "service": ["dhcp6"], "arguments": {}},
                                   '$(SRV4_ADDR)')

    # Send config-get command to the first address
    srv_msg.send_ctrl_cmd_via_http({"command": "config-get", "service": ["dhcp6"], "arguments": {}}, srv_ip_addresses[0])

    # Send config-get command to the other addresses, it should fail
    for ip in srv_ip_addresses[1:]:
        srv_msg.send_ctrl_cmd_via_http({"command": "config-get", "service": ["dhcp64"], "arguments": {}}, ip, exp_failed=True)

    # Send config-get command to the first address again to make sure server still works
    srv_msg.send_ctrl_cmd_via_http({"command": "config-get", "service": ["dhcp6"], "arguments": {}}, srv_ip_addresses[0])


@pytest.mark.usefixtures('_prepare_multiple_http_env')
@pytest.mark.v6
@pytest.mark.controlchannel
def test_control_channel_multiple_http_config_set():
    """Test if sockets close properly after config set.

    This test will add additional IP addresses to the server interface and open http control channels on them.
    It will then send config-set command and check if the sockets are closed.
    """
    if world.f_cfg.control_agent:
        pytest.skip('This test requires CA to be disabled. Making tests not viable because of CA deprecation.')

    # Generate ip addresses for http sockets
    srv4_addr = ipaddress.ip_address(world.f_cfg.srv4_addr)
    srv_ip_addresses = [world.f_cfg.srv4_addr]
    ip_address_shift = _generate_ip_address_shift()
    for ip_shift in ip_address_shift:
        srv_ip_addresses.append(srv4_addr + ip_shift)

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.add_unix_socket()
    # Add http sockets for all addresses
    for ip in srv_ip_addresses:
        srv_control.add_http_control_channel(ip, append=True)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Send config-get command to all addresses
    for ip in srv_ip_addresses:
        srv_msg.send_ctrl_cmd_via_http({"command": "config-get", "service": ["dhcp6"], "arguments": {}}, ip)

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.add_unix_socket()
    # Add http socket for the first address
    srv_control.add_http_control_channel(srv_ip_addresses[0])

    # Build config and send config-set command.
    srv_control.build_and_send_config_files()
    srv_msg.send_ctrl_cmd_via_http({"command": "config-set", "service": ["dhcp6"], "arguments":  world.dhcp_cfg},
                                   '$(SRV4_ADDR)')
    srv_msg.send_ctrl_cmd_via_http({"command": "list-commands", "service": ["dhcp6"], "arguments":  world.dhcp_cfg},
                                   '$(SRV4_ADDR)')

    # Wait for config to be applied
    srv_msg.forge_sleep('$(SLEEP_TIME_2)', 'seconds')

    # Send config-get command to the first address
    srv_msg.send_ctrl_cmd_via_http({"command": "config-get", "service": ["dhcp6"], "arguments": {}}, srv_ip_addresses[0])

    # Send config-get command to the other addresses, it should fail
    for ip in srv_ip_addresses[1:]:
        srv_msg.send_ctrl_cmd_via_http({"command": "config-get", "service": ["dhcp6"], "arguments": {}}, ip, exp_failed=True)

    # Send config-get command to the first address again to make sure server still works
    srv_msg.send_ctrl_cmd_via_http({"command": "config-get", "service": ["dhcp6"], "arguments": {}}, srv_ip_addresses[0])
