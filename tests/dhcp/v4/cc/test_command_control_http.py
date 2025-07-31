# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
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


@pytest.mark.v4
@pytest.mark.controlchannel
def test_control_channel_http_dhcp_disable_timer():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel('$(SRV4_ADDR)')
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
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel('$(SRV4_ADDR)')
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
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel('$(SRV4_ADDR)')
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
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel('$(SRV4_ADDR)')
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
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel('$(SRV4_ADDR)')

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
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel('$(SRV4_ADDR)')
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
    srv_control.add_unix_socket(socket_name='control_socket2')
    srv_control.add_http_control_channel('$(SRV4_ADDR)', socket_name='control_socket2')

    # reconfigure dhcp4 (new subnet, new socket)
    srv_control.build_config_files()
    srv_msg.send_ctrl_cmd_via_http('{"command": "config-set", "service": ["dhcp4"],"arguments":  $(DHCP_CONFIG) }',
                                   '$(SRV4_ADDR)')
    # reconfigure control-agent to switch to new dhcp4 socket
    if world.f_cfg.control_agent:
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
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel('$(SRV4_ADDR)')
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
    srv_control.add_http_control_channel('$(SRV4_ADDR)')
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
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel('$(SRV4_ADDR)')
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
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel('$(SRV4_ADDR)')
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
    srv_control.add_ddns_server_connectivity_options('enable-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-send-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-qualifying-suffix', 'my.domain.com')
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
    srv_control.add_ddns_server_connectivity_options('enable-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-send-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-qualifying-suffix', 'my.domain.com')
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
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_http('{"command": "list-commands", "service": ["dhcp4"],"arguments": {} }',
                                   '$(SRV4_ADDR)')
    srv_msg.send_ctrl_cmd_via_http('{"command": "config-write", "service": ["dhcp4"],"arguments": {"filename": "config-modified-2017-03-15.json"}}', '$(SRV4_ADDR)')

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
    srv_control.add_http_control_channel('$(SRV4_ADDR)')
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
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel('$(SRV4_ADDR)')
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
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel('$(SRV4_ADDR)')
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


def _generate_ip_address_shift():
    """Function searches for IP addresses that can be used for additional sockets.

    :return: list of IP address shifts that can be used for additional sockets
    :rtype: list
    """
    ciaddr = ipaddress.IPv4Interface(f'{world.f_cfg.ciaddr}/24')
    srv4_addr = ipaddress.IPv4Interface(f'{world.f_cfg.srv4_addr}/24')
    # chceck if srv4_addr is bigger than ciaddr and 4 more addresses will fit in the same subnet
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
    # Assign additional IP addressess to server interface
    for ip_shift in ip_address_shift:
        new_ip = srv4_addr + ip_shift
        fabric_sudo_command(f'ip address replace {new_ip}/24 dev {world.f_cfg.server_iface}')
    yield
    for ip_shift in ip_address_shift:
        new_ip = srv4_addr + ip_shift
        fabric_sudo_command(f'ip address del {new_ip}/24 dev {world.f_cfg.server_iface}')


@pytest.mark.usefixtures('_prepare_multiple_http_env')
@pytest.mark.v4
@pytest.mark.controlchannel
def test_control_channel_multiple_http_get_config():
    """Test multiple http control channels.

    This test will add additional IP addresses to the server interface and add http control channels for them.
    It will then send config-get command to all addresses and check if the response is the same.
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
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
        srv_msg.send_ctrl_cmd_via_http('{"command": "config-get","service":["dhcp4"],"arguments": {} }', ip)
