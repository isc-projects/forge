# Copyright (C) 2025 Internet Systems Consortium, Inc. ("ISC")
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
from src.forge_cfg import world
from src.protosupport.multi_protocol_functions import log_contains


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
    world.dhcp_cfg["control-sockets"][1]["http-headers"] = [
                    {
                        "user-context": {"comment": "HSTS header"},
                        "name": "Strict-Transport-Security",
                        "value": "max-age=31536000"
                    }
                ]
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

    world.dhcp_cfg["control-sockets"][1]["http-headers"] = [
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
    world.dhcp_cfg["control-sockets"][1]["http-headers"] = [
                {
                    "name": "TooLongCat",
                    "value": '1234567890' * 10000
                }
            ]
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started', should_succeed=False)
    log_contains("Some error message in logs", '/tmp/keactrl.log')  # TODO: add more specific error message


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

        world.dhcp_cfg["control-sockets"][1]["http-headers"] = [test_case["header"]]
        srv_control.build_and_send_config_files()

        srv_control.start_srv('DHCP', 'started', should_succeed=False)
        log_contains(test_case["error_message"], '/tmp/keactrl.log')


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
        misc.test_setup()
        if dhcp_version == 'v4':
            srv_control.config_srv_subnet(
                '192.168.50.0/24', '192.168.50.1-192.168.50.1')
        else:
            srv_control.config_srv_subnet(
                '2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
        srv_control.add_unix_socket()
        srv_control.add_http_control_channel(server_address)

        world.dhcp_cfg["control-sockets"][1]["http-headers"] = [test_case["header"]]
        srv_control.build_and_send_config_files()

        srv_control.start_srv('DHCP', 'started', should_succeed=False)
        log_contains(test_case["error_message"], '/tmp/keactrl.log')
