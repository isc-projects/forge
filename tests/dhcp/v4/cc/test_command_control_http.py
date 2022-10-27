# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea Control Channel Agent - HTTP"""

# pylint: disable=line-too-long

import pytest

from src import misc
from src import srv_msg
from src import srv_control


@pytest.mark.v4
@pytest.mark.controlchannel
def test_control_channel_http_dhcp_disable_timer():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    srv_msg.send_ctrl_cmd_via_http('{"command": "dhcp-disable","service": ["dhcp4"], "arguments": {"max-period": 5}}',
                                   '$(SRV4_ADDR)')

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
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.controlchannel
def test_control_channel_http_dhcp_disable():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    srv_msg.send_ctrl_cmd_via_http('{"command": "dhcp-disable","service": ["dhcp4"]}',
                                   '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()


@pytest.mark.v4
@pytest.mark.controlchannel
def test_control_channel_http_dhcp_disable_and_enable():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    srv_msg.send_ctrl_cmd_via_http('{"command": "dhcp-disable","service": ["dhcp4"]}',
                                   '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.send_ctrl_cmd_via_http('{"command": "dhcp-enable","service": ["dhcp4"]}',
                                   '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.controlchannel
def test_control_channel_http_config_set_basic():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')

    srv_control.build_config_files()
    srv_msg.send_ctrl_cmd_via_http('{"command": "config-set", "service": ["dhcp4"], "arguments":  $(DHCP_CONFIG) }',
                                   '$(SRV4_ADDR)')
    srv_msg.send_ctrl_cmd_via_http('{"command": "list-commands", "service": ["dhcp4"],"arguments":  $(DHCP_CONFIG) }',
                                   '$(SRV4_ADDR)')

    srv_msg.forge_sleep('$(SLEEP_TIME_2)', 'seconds')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.controlchannel
def test_control_channel_http_change_socket_during_reconfigure():
    # change address test needed also
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    result = srv_msg.send_ctrl_cmd_via_http('{"command":"config-get", "service": ["dhcp4"], "arguments": {} }',
                                            '$(SRV4_ADDR)')
    assert result[0]['result'] == 0

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.open_control_channel(socket_name='control_socket2')
    srv_control.agent_control_channel('$(SRV4_ADDR)',
                                      socket_name='control_socket2')

    # reconfigure dhcp4 (new subnet, new socket)
    srv_control.build_config_files()
    srv_msg.send_ctrl_cmd_via_http('{"command": "config-set", "service": ["dhcp4"],"arguments":  $(DHCP_CONFIG) }',
                                   '$(SRV4_ADDR)')
    # reconfigure control-agent to switch to new dhcp4 socket
    srv_msg.send_ctrl_cmd_via_http('{"command": "config-set", "arguments":  $(AGENT_CONFIG) }',
                                   '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    result = srv_msg.send_ctrl_cmd_via_http('{"command":"config-get", "service": ["dhcp4"], "arguments": {} }',
                                            '$(SRV4_ADDR)')
    assert result[0]['result'] == 0


@pytest.mark.v4
@pytest.mark.controlchannel
def test_control_channel_http_after_restart_load_config_file():

    # initial configuration is taken from file
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    # now configuration is set over control-agent
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_config_files()

    srv_msg.send_ctrl_cmd_via_http('{"command": "config-set", "service": ["dhcp4"],"arguments":  $(DHCP_CONFIG) }',
                                   '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    # and now goes restart so configuration again is taken from files
    srv_control.start_srv('DHCP', 'restarted')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.controlchannel
def test_control_channel_http_get_config():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_http('{"command": "config-get","service":["dhcp4"],"arguments": {} }',
                                   '$(SRV4_ADDR)')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.disabled
def test_control_channel_http_test_config():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_ddns_server_options('qualifying-suffix', 'my.domain.com')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-name',
                                           0,
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '192.168.50.5')

    srv_control.build_config_files()
    response = srv_msg.send_ctrl_cmd_via_http('{"command": "config-test","service": ["dhcp4"],'
                                              ' "arguments":  $(DHCP_CONFIG) }', '$(SRV4_ADDR)', exp_result=1)

    assert "specified reservation '192.168.50.5' is not within the IPv4 subnet '192.168.51.0/24'" in response[0]['text']

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_ddns_server_options('qualifying-suffix', 'my.domain.com')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-name',
                                           0,
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '3000::1')

    srv_control.build_config_files()
    response = srv_msg.send_ctrl_cmd_via_http('{"command": "config-test","service": ["dhcp4"],'
                                              ' "arguments":  $(DHCP_CONFIG) }', '$(SRV4_ADDR)', exp_result=1)

    assert "address '3000::1' is not a valid IPv4 address" in response[0]['text']

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.controlchannel
def test_control_channel_http_config_write():
    # Start server with initial configuration.
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Write configuration to file.
    srv_msg.send_ctrl_cmd_via_http('{"command": "list-commands", "service": ["dhcp4"],"arguments": {} }',
                                   '$(SRV4_ADDR)')
    srv_msg.send_ctrl_cmd_via_http('{"command": "config-write", "service": ["dhcp4"],"arguments": {"filename": "/tmp/config-modified-2017-03-15.json"}}',  # TODO probably confing file location/name',
                                   '$(SRV4_ADDR)')

    # Send DISCOVER.
    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    # Receive OFFER.
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    # Generate new configuration.
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_config_files()

    # Set new configuration.
    srv_msg.send_ctrl_cmd_via_socket('{"command": "config-set", "service": ["dhcp4"],"arguments":  $(DHCP_CONFIG) }')

    # Send DISCOVER.
    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    # Receive OFFER.
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    # Restart server, it should configure itself with the old 192.168.50.0/24
    # subnet.
    srv_control.start_srv('DHCP', 'restarted')

    # Send DISCOVER.
    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    # Receive OFFER, it should contain a lease from the old configuration.
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.controlchannel
def test_control_channel_http_reload_config():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()

    srv_msg.send_ctrl_cmd_via_http('{"command":"config-reload","service":["dhcp4"],"arguments":{}}',
                                   '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    srv_control.start_srv('DHCP', 'restarted')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
