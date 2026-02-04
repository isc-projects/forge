# Copyright (C) 2025 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea Control Channel - HTTP"""

# pylint: disable=line-too-long

import pytest

from src import misc
from src import srv_msg
from src import srv_control
from src.forge_cfg import world
from src.protosupport.multi_protocol_functions import log_contains
from src.softwaresupport.multi_server_functions import fabric_is_file, fabric_remove_file_command


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.parametrize('socket_protocol', ['http_v4', 'http_v6'])
def test_control_channel_http_headers_basic(dhcp_version, socket_protocol):
    """Test custom HTTP headers send by Kea server.

    :param dhcp_version: DHCP version
    :type dhcp_version: str
    :param socket_protocol: Socket protocol
    :type socket_protocol: str
    """
    misc.test_setup()
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')

    if socket_protocol == 'http_v4':
        server_address = '$(SRV4_ADDR)'
    else:
        server_address = '$(SRV_IPV6_ADDR_GLOBAL)'

    srv_control.add_unix_socket()
    srv_control.add_http_control_channel(server_address)

    headers_config = [
        {
            "user-context": {"comment": "HSTS header"},
            "name": "Strict-Transport-Security",
            "value": "max-age=31536000"
        }
    ]

    # Use diferent configuration file for Control agent or direct Kea testing.
    if world.f_cfg.control_agent:
        world.ca_cfg["Control-agent"]["http-headers"] = headers_config
    else:
        world.dhcp_cfg["control-sockets"][1]["http-headers"] = headers_config

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    headers = srv_msg.send_ctrl_cmd_via_http({"command": "config-get", "service": [f'dhcp{dhcp_version[1]}'], "arguments": {}},
                                             server_address, return_headers=True)
    assert headers['Strict-Transport-Security'] == 'max-age=31536000'


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.parametrize('socket_protocol', ['http_v4', 'http_v6'])
def test_control_channel_http_headers_multiple(dhcp_version, socket_protocol):
    """Test multiple custom HTTP headers send by Kea server.

    :param dhcp_version: DHCP version
    :type dhcp_version: str
    :param socket_protocol: Socket protocol
    :type socket_protocol: str
    """
    misc.test_setup()
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet(
            '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    else:
        srv_control.config_srv_subnet(
            '2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')

    if socket_protocol == 'http_v4':
        server_address = '$(SRV4_ADDR)'
    else:
        server_address = '$(SRV_IPV6_ADDR_GLOBAL)'
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel(server_address)

    long_string = '1234567890' * 5000

    headers_config = [
        {
            "user-context": {"comment": "HSTS header"},
            "name": "Strict-Transport-Security",
            "value": "max-age=31536000"
        },
        {
            "name": "FooBar",
            "value": "123456"
        },
        {
            "name": "LongCat",
            "value": long_string
        }
    ]

    # Use diferent configuration file for Control agent or direct Kea testing.
    if world.f_cfg.control_agent:
        world.ca_cfg["Control-agent"]["http-headers"] = headers_config
    else:
        world.dhcp_cfg["control-sockets"][1]["http-headers"] = headers_config

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    headers = srv_msg.send_ctrl_cmd_via_http({"command": "config-get", "service": [f'dhcp{dhcp_version[1]}'], "arguments": {}},
                                             server_address, return_headers=True)
    assert headers['Strict-Transport-Security'] == 'max-age=31536000'
    assert headers['FooBar'] == '123456'
    assert headers['LongCat'] == long_string


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.parametrize('socket_protocol', ['http_v4', 'http_v6'])
def test_control_channel_http_headers_too_long(dhcp_version, socket_protocol):
    """Test too long http header.
    Kea#4051 Kea is not fixed yet and error message is not decided yet.

    :param dhcp_version: DHCP version
    :type dhcp_version: str
    :param socket_protocol: Socket protocol
    :type socket_protocol: str
    """
    misc.test_setup()
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet(
            '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    else:
        srv_control.config_srv_subnet(
            '2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')

    if socket_protocol == 'http_v4':
        server_address = '$(SRV4_ADDR)'
    else:
        server_address = '$(SRV_IPV6_ADDR_GLOBAL)'
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel(server_address)

    headers_config = [
        {
            "name": "TooLongCat",
                    "value": '1234567890' * 10000
        }
    ]

    # Use diferent configuration file for Control agent or direct Kea testing.
    if world.f_cfg.control_agent:
        world.ca_cfg["Control-agent"]["http-headers"] = headers_config
    else:
        world.dhcp_cfg["control-sockets"][1]["http-headers"] = headers_config

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started', should_succeed=False)

    if world.f_cfg.install_method == 'make':
        log_contains("Some error message in logs", '/tmp/keactrl.log')  # TODO: add more specific error message
    else:
        if not world.f_cfg.control_agent:  # 'log_contains' does not support CA installed with packages
            log_contains("Some error message in logs")  # TODO: add more specific error message


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.parametrize('socket_protocol', ['http_v4', 'http_v6'])
def test_control_channel_http_headers_illegal(dhcp_version, socket_protocol):
    """Test illegal characters in HTTP headers.
    Kea#4052 Kea is not fixed yet and error message is not decided yet.

    :param dhcp_version: DHCP version
    :type dhcp_version: str
    :param socket_protocol: Socket protocol
    :type socket_protocol: str
    """
    test_cases = [{"header":
                   {
                       "name": "Spaces are bad",
                       "value": "max-age=31536000"
                   },
                   "error_message": "error"  # TODO: add more specific error message
                   },
                  {"header":
                   {
                       "name": "Colon:IsNotAllowed",
                       "value": "max-age=31536000"
                   },
                   "error_message": "error"  # TODO: add more specific error message
                   }
                  ]

    if socket_protocol == 'http_v4':
        server_address = '$(SRV4_ADDR)'
    else:
        server_address = '$(SRV_IPV6_ADDR_GLOBAL)'

    for test_case in test_cases:
        srv_control.clear_some_data('logs')
        misc.test_setup()
        if dhcp_version == 'v4':
            srv_control.config_srv_subnet(
                '192.168.50.0/24', '192.168.50.1-192.168.50.1')
        else:
            srv_control.config_srv_subnet(
                '2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
        srv_control.add_unix_socket()
        srv_control.add_http_control_channel(server_address)

        # Use diferent configuration file for Control agent or direct Kea testing.
        if world.f_cfg.control_agent:
            world.ca_cfg["Control-agent"]["http-headers"] = [test_case["header"]]
        else:
            world.dhcp_cfg["control-sockets"][1]["http-headers"] = [test_case["header"]]

        srv_control.build_and_send_config_files()
        srv_control.start_srv('DHCP', 'started', should_succeed=False)

        if world.f_cfg.install_method == 'make':
            log_contains(test_case["error_message"], '/tmp/keactrl.log')
        else:
            if not world.f_cfg.control_agent:  # 'log_contains' does not support CA installed with packages
                log_contains(test_case["error_message"])


def _remove_alpine_err_log(dhcp_version, host=world.f_cfg.mgmt_address):
    if fabric_is_file(f'/var/log/kea/kea-dhcp{dhcp_version[1]}.err', host):
        fabric_remove_file_command(
            f'/var/log/kea/kea-dhcp{dhcp_version[1]}.err', host, hide_all=world.f_cfg.forge_verbose == 0
        )


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.parametrize('socket_protocol', ['http_v4', 'http_v6'])
def test_control_channel_http_headers_negative(dhcp_version, socket_protocol):
    """Test wrong HTTP headers.

    :param dhcp_version: DHCP version
    :type dhcp_version: str
    :param socket_protocol: Socket protocol
    :type socket_protocol: str
    """
    test_cases = [{"header":
                   {
                       "name": "IntegersAreNotAllowed",
                       "value": 123456
                   },
                   "error_message": "syntax error, unexpected integer, expecting constant string"
                   },
                  {"header":
                   {
                       "name": "BooleanIsNotAllowed",
                       "value": True
                   },
                   "error_message": "syntax error, unexpected boolean, expecting constant string"
                   },
                  {"header":
                   {
                       "name": "NullIsNotAllowed",
                       "value": None
                   },
                   "error_message": "syntax error, unexpected null, expecting constant string"
                   }
                  ]

    if socket_protocol == 'http_v4':
        server_address = '$(SRV4_ADDR)'
    else:
        server_address = '$(SRV_IPV6_ADDR_GLOBAL)'

    for test_case in test_cases:
        srv_control.clear_some_data('logs')
        if world.server_system == 'alpine' and world.f_cfg.install_method == 'native':
            _remove_alpine_err_log(dhcp_version)
        misc.test_setup()
        if dhcp_version == 'v4':
            srv_control.config_srv_subnet(
                '192.168.50.0/24', '192.168.50.1-192.168.50.1')
        else:
            srv_control.config_srv_subnet(
                '2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
        srv_control.add_unix_socket()
        srv_control.add_http_control_channel(server_address)

        # Use diferent configuration file for Control agent or direct Kea testing.
        if world.f_cfg.control_agent:
            world.ca_cfg["Control-agent"]["http-headers"] = [test_case["header"]]
        else:
            world.dhcp_cfg["control-sockets"][1]["http-headers"] = [test_case["header"]]

        srv_control.build_and_send_config_files()
        srv_control.start_srv('DHCP', 'started', should_succeed=False)

        if world.f_cfg.install_method == 'make':
            log_contains(test_case["error_message"], '/tmp/keactrl.log')
        else:
            if not world.f_cfg.control_agent:  # 'log_contains' does not support CA installed with packages
                if world.server_system == 'alpine':
                    log_contains(test_case["error_message"], f'/var/log/kea/kea-dhcp{dhcp_version[1]}.err')
                else:
                    log_contains(test_case["error_message"])
