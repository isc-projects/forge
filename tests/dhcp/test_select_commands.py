# Copyright (C) 2024 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""DHCP *-test command tests"""

import pytest
from src import misc
from src import srv_msg
from src import srv_control

from src.forge_cfg import world


def _check_subnet4_select_test(arguments, exp_result, response, channel):
    cmd = {"command": "subnet4-select-test"}
    if arguments is not None:
        cmd["arguments"] = arguments
    cmd_response = srv_msg.send_ctrl_cmd(cmd, channel, exp_result=exp_result)
    assert cmd_response['text'] == response
    return True


def _check_subnet6_select_test(arguments, exp_result, response, channel):
    cmd = {"command": "subnet6-select-test"}
    if arguments is not None:
        cmd["arguments"] = arguments
    cmd_response = srv_msg.send_ctrl_cmd(cmd, channel, exp_result=exp_result)
    assert cmd_response['text'] == response
    return True


def _check_subnet4o6_select_test(arguments, exp_result, response, channel):
    cmd = {"command": "subnet4o6-select-test"}
    if arguments is not None:
        cmd["arguments"] = arguments
    cmd_response = srv_msg.send_ctrl_cmd(cmd, channel, exp_result=exp_result)
    assert cmd_response['text'] == response
    return True


@pytest.mark.v4
@pytest.mark.ca
@pytest.mark.controlchannel
@pytest.mark.parametrize('channel', ['socket'])
def test_subnet4_select_test_negative(channel):
    """ Tests if server responds correctly at malformed query.
    """
    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # define test cases in format [{arguments}, expected result, expected response]
    test_cases = [
        [None, 1, "empty arguments"],
        [{}, 3, "no subnet selected"],
        [[], 1, "arguments must be a map"],
        [{"foo": "bar"}, 1, "unknown entry 'foo'"],
        [{"interface": 1}, 1, "'interface' entry must be a string"],
        [{"interface": "foo"}, 1, "Error during command processing: interface foo doesn't exist and "
         "therefore it is impossible to find a suitable subnet for its IPv4 address"],
        [{"address": "2001:db8:1::1"}, 1, "bad 'address' entry: not IPv4"],
        [{"address": "foobar"}, 1,
         "bad 'address' entry: Failed to convert string to address 'foobar': Invalid argument"],
        [{"relay": 1}, 1, "'relay' entry must be a string"],
        [{"relay": "2001:db8:1::1"}, 1, "bad 'relay' entry: not IPv4"],
        [{"relay": "foobar"}, 1,
         "bad 'relay' entry: Failed to convert string to address 'foobar': Invalid argument"],
        [{"local": 1}, 1, "'local' entry must be a string"],
        [{"local": "2001:db8:1::1"}, 1, "bad 'local' entry: not IPv4"],
        [{"local": "foobar"}, 1,
         "bad 'local' entry: Failed to convert string to address 'foobar': Invalid argument"],
        [{"remote": 1}, 1, "'remote' entry must be a string"],
        [{"remote": "2001:db8:1::1"}, 1, "bad 'remote' entry: not IPv4"],
        [{"remote": "foobar"}, 1,
         "bad 'remote' entry: Failed to convert string to address 'foobar': Invalid argument"],
        [{"link": 1}, 1, "'link' entry must be a string"],
        [{"link": "2001:db8:1::1"}, 1, "bad 'link' entry: not IPv4"],
        [{"link": "foobar"}, 1,
         "bad 'link' entry: Failed to convert string to address 'foobar': Invalid argument"],
        [{"subnet": 1}, 1, "'subnet' entry must be a string"],
        [{"subnet": "2001:db8:1::1"}, 1, "bad 'subnet' entry: not IPv4"],
        [{"subnet": "foobar"}, 1,
         "bad 'subnet' entry: Failed to convert string to address 'foobar': Invalid argument"],
        [{"classes": 1}, 1, "'classes' entry must be a list"],
        [{"classes": "foo"}, 1, "'classes' entry must be a list"],
        [{"classes": [1]}, 1, "'classes' entry must be a list of strings"],
    ]

    for case in test_cases:
        _check_subnet4_select_test(case[0], case[1], case[2], channel)


@pytest.mark.v4
@pytest.mark.ca
@pytest.mark.controlchannel
@pytest.mark.parametrize('channel', ['socket'])
def test_subnet4_select_test(channel):
    """ Tests if server responds correctly for simple queries.
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10', id=1)
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24', '192.168.51.1-192.168.51.10', id=2)
    srv_control.config_client_classification(1, 'foobar')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # define test cases in format [{arguments}, expected result, expected response]
    test_cases = [
        [{"interface": "lo"}, 3, "no subnet selected"],
        [{"interface": world.f_cfg.server_iface}, 0, "selected subnet '192.168.50.0/24' id 1"],
        [{"address": "192.168.50.1"}, 0, "selected subnet '192.168.50.0/24' id 1"],
        [{"address": "192.168.51.1"}, 3, "no subnet selected"],
        [{"address": "192.168.51.1", "classes": ["foobar"]}, 0, "selected subnet '192.168.51.0/24' id 2"],
    ]

    for case in test_cases:
        _check_subnet4_select_test(case[0], case[1], case[2], channel)

    # Tests with shared network
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10', id=1)
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24', '192.168.51.1-192.168.51.10', id=2)
    srv_control.config_client_classification(1, 'foobar')
    srv_control.shared_subnet('192.168.50.0/24', 0)
    srv_control.shared_subnet('192.168.51.0/24', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"foo"', 0)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'restarted')

    # define test cases in format [{arguments}, expected result, expected response]
    test_cases = [
        [{"interface": world.f_cfg.server_iface}, 0,
         "selected shared network 'foo' starting with subnet '192.168.50.0/24' id 1"],
        [{"address": "192.168.51.1", "classes": ["foobar"]}, 0,
         "selected shared network 'foo' starting with subnet '192.168.51.0/24' id 2"],
    ]
    for case in test_cases:
        _check_subnet4_select_test(case[0], case[1], case[2], channel)


@pytest.mark.v4
@pytest.mark.ca
@pytest.mark.controlchannel
@pytest.mark.parametrize('channel', ['socket'])
def test_subnet4o6_select_test_negative(channel):
    """ Tests if server responds correctly at malformed query.
    """
    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # define test cases in format [{arguments}, expected result, expected response]
    test_cases = [
        [None, 1, "empty arguments"],
        [{}, 3, "no subnet selected"],
        [[], 1, "arguments must be a map"],
        [{"foo": "bar"}, 1, "unknown entry 'foo'"],
        [{"interface": 1}, 1, "'interface' entry must be a string"],
        [{"interface": "foo"}, 3, "no subnet selected"],
        [{"address": "2001:db8:1::1"}, 1, "bad 'address' entry: not IPv4"],
        [{"address": "foobar"}, 1,
         "bad 'address' entry: Failed to convert string to address 'foobar': Invalid argument"],
        [{"relay": 1}, 1, "'relay' entry must be a string"],
        [{"relay": "2001:db8:1::1"}, 1, "bad 'relay' entry: not IPv4"],
        [{"relay": "foobar"}, 1,
         "bad 'relay' entry: Failed to convert string to address 'foobar': Invalid argument"],
        [{"local": 1}, 1, "'local' entry must be a string"],
        [{"local": "192.168.1.200"}, 1, "bad 'local' entry: not IPv6"],
        [{"local": "foobar"}, 1,
         "bad 'local' entry: Failed to convert string to address 'foobar': Invalid argument"],
        [{"remote": 1}, 1, "'remote' entry must be a string"],
        [{"remote": "192.168.1.200"}, 1, "bad 'remote' entry: not IPv6"],
        [{"remote": "foobar"}, 1,
         "bad 'remote' entry: Failed to convert string to address 'foobar': Invalid argument"],
        [{"link": 1}, 1, "'link' entry must be a string"],
        [{"link": "192.168.1.200"}, 1, "bad 'link' entry: not IPv6"],
        [{"link": "foobar"}, 1,
         "bad 'link' entry: Failed to convert string to address 'foobar': Invalid argument"],
        [{"subnet": 1}, 1, "'subnet' entry must be a string"],
        [{"subnet": "2001:db8:1::1"}, 1, "bad 'subnet' entry: not IPv4"],
        [{"subnet": "foobar"}, 1,
         "bad 'subnet' entry: Failed to convert string to address 'foobar': Invalid argument"],
        [{"classes": 1}, 1, "'classes' entry must be a list"],
        [{"classes": "foo"}, 1, "'classes' entry must be a list"],
        [{"classes": [1]}, 1, "'classes' entry must be a list of strings"],
    ]

    for case in test_cases:
        _check_subnet4o6_select_test(case[0], case[1], case[2], channel)


@pytest.mark.v4
@pytest.mark.ca
@pytest.mark.controlchannel
@pytest.mark.parametrize('channel', ['socket'])
def test_subnet4o6_select_test(channel):
    """ Tests if server responds correctly for simple queries.
    """
    misc.test_setup()
    subnets_v4 = [
            {
                "id": 1,
                "4o6-subnet": "2001:db8:1::/64",
                "interface": world.f_cfg.server_iface,
                "4o6-interface": world.f_cfg.server_iface,
                "pools": [
                    {
                        "pool": "192.168.50.1-192.168.50.10"
                    }
                ],
                "subnet": "192.168.50.0/24"
            },
            {
                "id": 2,
                "interface": world.f_cfg.server_iface,
                "pools": [
                    {
                        "pool": "192.168.51.1-192.168.51.10"
                    }
                ],
                "subnet": "192.168.51.0/24"
            }
        ]
    world.dhcp_cfg.update({'subnet4': subnets_v4})
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # define test cases in format [{arguments}, expected result, expected response]
    test_cases = [
        [{"interface": "lo"}, 3, "no subnet selected"],
        [{"interface": world.f_cfg.server_iface}, 0, "selected subnet '192.168.50.0/24' id 1"],
        [{"remote": "2001:db8:2::2"}, 3, "no subnet selected"],
        [{"remote": "2001:db8:1::1"}, 0, "selected subnet '192.168.50.0/24' id 1"],
    ]

    for case in test_cases:
        _check_subnet4o6_select_test(case[0], case[1], case[2], channel)

    # Tests with shared network
    misc.test_setup()
    subnets_v4 = [
            {
                "id": 1,
                "4o6-subnet": "2001:db8:1::/64",
                "interface": world.f_cfg.server_iface,
                "4o6-interface": world.f_cfg.server_iface,
                "pools": [
                    {
                        "pool": "192.168.50.1-192.168.50.10"
                    }
                ],
                "subnet": "192.168.50.0/24"
            },
            {
                "id": 2,
                "4o6-subnet": "2001:db8:2::/64",
                "interface": world.f_cfg.server_iface,
                "4o6-interface": world.f_cfg.server_iface,
                "pools": [
                    {
                        "pool": "192.168.51.1-192.168.51.10"
                    }
                ],
                "subnet": "192.168.51.0/24"
            }
        ]
    world.dhcp_cfg.update({'subnet4': subnets_v4})
    srv_control.config_client_classification(1, 'foobar')
    srv_control.shared_subnet('192.168.50.0/24', 0)
    srv_control.shared_subnet('192.168.51.0/24', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"foo"', 0)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'restarted')

    # define test cases in format [{arguments}, expected result, expected response]
    test_cases = [
        [{"interface": world.f_cfg.server_iface}, 0,
         "selected shared network 'foo' starting with subnet '192.168.50.0/24' id 1"],
        [{"remote": "2001:db8:2::2", "classes": ["foobar"]}, 0,
         "selected shared network 'foo' starting with subnet '192.168.51.0/24' id 2"],
    ]
    for case in test_cases:
        _check_subnet4o6_select_test(case[0], case[1], case[2], channel)


@pytest.mark.v6
@pytest.mark.ca
@pytest.mark.controlchannel
@pytest.mark.parametrize('channel', ['socket'])
def test_subnet6_select_test_negative(channel):
    """ Tests if server responds correctly at malformed query for IPv6.
    """
    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # define test cases in format [{arguments}, expected result, expected response]
    test_cases = [
        [None, 1, "empty arguments"],
        [{}, 3, "no subnet selected"],
        [[], 1, "arguments must be a map"],
        [{"foo": "bar"}, 1, "unknown entry 'foo'"],
        [{"interface": 1}, 1, "'interface' entry must be a string"],
        [{"interface": "foo"}, 3, "no subnet selected"],
        [{"interface-id": 1}, 1, "'interface-id' entry must be a string"],
        [{"interface-id": ""}, 1, "'interface-id' must be not empty"],
        [{"interface-id": "foo"}, 1, "value of 'interface-id' was not recognized"],
        [{"remote": 1}, 1, "'remote' entry must be a string"],
        [{"remote": "192.168.1.1"}, 1, "bad 'remote' entry: not IPv6"],
        [{"remote": "foobar"}, 1,
         "bad 'remote' entry: Failed to convert string to address 'foobar': Invalid argument"],
        [{"link": 1}, 1, "'link' entry must be a string"],
        [{"link": "192.168.1.1"}, 1, "bad 'link' entry: not IPv6"],
        [{"link": "foobar"}, 1,
         "bad 'link' entry: Failed to convert string to address 'foobar': Invalid argument"],
        [{"classes": 1}, 1, "'classes' entry must be a list"],
        [{"classes": "foo"}, 1, "'classes' entry must be a list"],
        [{"classes": [1]}, 1, "'classes' entry must be a list of strings"],
    ]

    for case in test_cases:
        _check_subnet6_select_test(case[0], case[1], case[2], channel)


@pytest.mark.v6
@pytest.mark.ca
@pytest.mark.controlchannel
@pytest.mark.parametrize('channel', ['socket'])
def test_subnet6_select_test(channel):
    """ Tests if server responds correctly for simple queries.
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::100', id=1)
    srv_control.config_srv_another_subnet_no_interface('2001:db8:2::/64', '2001:db8:2::1-2001:db8:2::100', id=2)
    srv_control.config_client_classification(1, 'foobar')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # define test cases in format [{arguments}, expected result, expected response]
    test_cases = [
        [{"remote": "fe80::abcd"}, 3, "no subnet selected"],
        [{"remote": "2001:db8:1::1"}, 0, "selected subnet '2001:db8:1::/64' id 1"],
        [{"interface": "bar"}, 3, "no subnet selected"],
        [{"interface": world.f_cfg.server_iface}, 0, "selected subnet '2001:db8:1::/64' id 1"],
        [{"link": "2001:db8:2::2"}, 3, "no subnet selected"],
        [{"link": "2001:db8:1::1"}, 0, "selected subnet '2001:db8:1::/64' id 1"],
        [{"remote": "2001:db8:2::1", "classes": ["foobar"]}, 0,
         "selected subnet '2001:db8:2::/64' id 2"],
    ]

    for case in test_cases:
        _check_subnet6_select_test(case[0], case[1], case[2], channel)

    # Tests with shared network
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::100', id=1)
    srv_control.config_srv_another_subnet_no_interface('2001:db8:2::/64', '2001:db8:2::1-2001:db8:2::100', id=2)
    srv_control.config_client_classification(1, 'foobar')
    srv_control.shared_subnet('2001:db8:1::/64', 0)
    srv_control.shared_subnet('2001:db8:2::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"foo"', 0)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'restarted')

    # define test cases in format [{arguments}, expected result, expected response]
    test_cases = [
        [{"remote": "2001:db8:1::1"}, 0, "selected shared network 'foo' starting with subnet '2001:db8:1::/64' id 1"],
        [{"interface": world.f_cfg.server_iface}, 0,
         "selected shared network 'foo' starting with subnet '2001:db8:1::/64' id 1"],
        [{"remote": "2001:db8:2::1", "classes": ["foobar"]}, 0,
         "selected shared network 'foo' starting with subnet '2001:db8:2::/64' id 2"],
    ]
    for case in test_cases:
        _check_subnet6_select_test(case[0], case[1], case[2], channel)
