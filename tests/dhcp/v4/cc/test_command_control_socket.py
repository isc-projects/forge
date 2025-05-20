# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea Control Channel - socket"""

import pytest

from src import misc
from src import srv_msg
from src import srv_control
from src.forge_cfg import world

from src.softwaresupport.multi_server_functions import verify_file_permissions
from src.protosupport.multi_protocol_functions import log_contains


@pytest.mark.v4
@pytest.mark.controlchannel
def test_control_channel_socket_dhcp_disable_timer():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.add_unix_socket()
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.5')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "dhcp-disable", "arguments": {"max-period": 5}}')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.forge_sleep(7, 'seconds')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.5')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.controlchannel
def test_control_channel_socket_dhcp_disable():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.add_unix_socket()
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.5')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "dhcp-disable" }')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()


@pytest.mark.v4
@pytest.mark.controlchannel
def test_control_channel_socket_dhcp_disable_and_enable():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.add_unix_socket()
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.5')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "dhcp-disable" }')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.send_ctrl_cmd_via_socket('{"command": "dhcp-enable" }')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.5')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.controlchannel
def test_control_channel_socket_config_get_basic():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.add_unix_socket()
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.5')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.add_unix_socket()

    srv_control.build_config_files()
    srv_msg.send_ctrl_cmd_via_socket('{"command": "config-get","arguments":  $(DHCP_CONFIG) }')


@pytest.mark.v4
@pytest.mark.controlchannel
def test_control_channel_socket_config_set_basic():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.add_unix_socket()
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.5')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.add_unix_socket()

    srv_control.build_config_files()
    srv_msg.send_ctrl_cmd_via_socket('{"command": "config-set","arguments":  $(DHCP_CONFIG) }')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.50')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.controlchannel
def test_control_channel_socket_path():
    """Test that the control socket path is valid.
    """
    illegal_paths = [
        ['', True, 'COMMAND_ACCEPTOR_START Starting to accept connections via unix domain socket bound to'],
        ['/tmp/', False, '\'socket-name\' is invalid: invalid path specified:'],
        ['~/', False, '\'socket-name\' is invalid: invalid path specified:'],
        ['/var/', False, '\'socket-name\' is invalid: invalid path specified:'],
        ['/srv/', False, '\'socket-name\' is invalid: invalid path specified:'],
        ['/etc/kea/', False, '\'socket-name\' is invalid: invalid path specified:'],
    ]

    for path, should_succeed, exp_text in illegal_paths:
        srv_control.clear_some_data('logs')
        misc.test_setup()
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
        srv_control.add_unix_socket(path + 'control_socket')
        srv_control.build_and_send_config_files()

        srv_control.start_srv('DHCP', 'started', should_succeed=should_succeed)

        if should_succeed:
            if path == '':
                path = world.f_cfg.run_join('')
            verify_file_permissions(path + 'control_socket', '750')
            verify_file_permissions(path, '750')

        misc.test_procedure()
        log_contains(exp_text)


@pytest.mark.v4
@pytest.mark.controlchannel
def test_control_channel_socket_change_socket_during_reconfigure():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.add_unix_socket()
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    for socket in world.dhcp_cfg["Dhcp4"]["control-sockets"]:
        if socket["socket-type"] == "unix":
            verify_file_permissions(socket["socket-name"], '750')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.5')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.add_unix_socket('control_socket2')

    srv_control.build_config_files()
    srv_msg.send_ctrl_cmd_via_socket({"command": "config-set","arguments": world.dhcp_cfg})

    for socket in world.dhcp_cfg["Dhcp4"]["control-sockets"]:
        if socket["socket-type"] == "unix":
            verify_file_permissions(world.f_cfg.run_join(socket["socket-name"]), '750')

    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.50')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "list-commands","arguments": {}}',
                                     socket_name='control_socket2')


@pytest.mark.v4
@pytest.mark.controlchannel
def test_control_channel_socket_after_restart_load_config_file():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.add_unix_socket()
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    for socket in world.dhcp_cfg["Dhcp4"]["control-sockets"]:
        if socket["socket-type"] == "unix":
            verify_file_permissions(socket["socket-name"], '750')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.5')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.add_unix_socket()
    srv_control.build_config_files()

    srv_msg.send_ctrl_cmd_via_socket('{"command": "config-set","arguments":  $(DHCP_CONFIG) }')

    misc.test_procedure()
    for socket in world.dhcp_cfg["Dhcp4"]["control-sockets"]:
        if socket["socket-type"] == "unix":
            verify_file_permissions(socket["socket-name"], '750')

    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.50')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    srv_control.start_srv('DHCP', 'restarted')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.5')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
