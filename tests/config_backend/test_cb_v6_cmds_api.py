# Copyright (C) 2022-2024 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea database config backend commands hook testing"""

import pytest

from src import srv_msg

from src.softwaresupport.cb_model import setup_server_for_config_backend_cmds

pytestmark = [pytest.mark.v6,
              pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.cb,
              pytest.mark.cb_cmds]


def _set_server(backend):
    setup_server_for_config_backend_cmds(backend_type=backend)
    cmd = dict(command="remote-server6-set", arguments={"remote": {"type": backend},
                                                        "servers": [{"server-tag": "abc"}]})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)


def test_availability():
    _set_server('mysql')
    cmd = dict(command='list-commands')
    response = srv_msg.send_ctrl_cmd(cmd)

    for cmd in ["remote-global-parameter6-del",
                "remote-global-parameter6-get",
                "remote-global-parameter6-get-all",
                "remote-global-parameter6-set",
                "remote-network6-del",
                "remote-network6-get",
                "remote-network6-list",
                "remote-network6-set",
                "remote-option-def6-del",
                "remote-option-def6-get",
                "remote-option-def6-get-all",
                "remote-option-def6-set",
                "remote-option6-global-del",
                "remote-option6-global-get",
                "remote-option6-global-get-all",
                "remote-option6-global-set",
                "remote-subnet6-del-by-id",
                "remote-subnet6-del-by-prefix",
                "remote-subnet6-get-by-id",
                "remote-subnet6-get-by-prefix",
                "remote-subnet6-list",
                "remote-subnet6-set"]:
        assert cmd in response['arguments']


# subnet tests
@pytest.mark.parametrize('channel', ['socket', 'http'])
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_set_basic(channel, backend):
    _set_server(backend)
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64",
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "id": 1,
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "2001:db8:1::1-2001:db8:1::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_set_empty_subnet(backend):
    _set_server(backend)
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "shared-network-name": "",
                                                        "subnets": [{"subnet": "",
                                                                     "id": 1,
                                                                     "interface": "$(SERVER_IFACE)"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "subnet configuration failed: Invalid subnet syntax (prefix/len expected):" in response["text"]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_set_missing_subnet(backend):
    _set_server(backend)
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "shared-network-name": "",
                                                        "subnets": [{"interface": "$(SERVER_IFACE)", "id": 1}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "subnet configuration failed: mandatory 'subnet' parameter " \
           "is missing for a subnet being configured" in response["text"]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_set_stateless(backend):
    _set_server(backend)
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64",
                                                                     "id": 1,
                                                                     "shared-network-name": "",
                                                                     "interface": "$(SERVER_IFACE)"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_set_id(backend):
    _set_server(backend)
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64", "id": 5,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "2001:db8:1::1-2001:db8:1::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 5, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_set_duplicated_id(backend):
    _set_server(backend)
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64", "id": 5,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "2001:db8:1::1-2001:db8:1::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 5, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:2::/64", "id": 5,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "2001:db8:2::1-2001:db8:2::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 5, "subnet": "2001:db8:2::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    cmd = dict(command="remote-subnet6-list", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1,
                                      "subnets": [{"id": 5, "metadata": {"server-tags": ["abc"]},
                                                   "shared-network-name": None, "subnet": "2001:db8:2::/64"}]},
                        "result": 0, "text": "1 IPv6 subnet(s) found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_set_duplicated_subnet(backend):
    _set_server(backend)
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64", "id": 5,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "2001:db8:1::1-2001:db8:1::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 5, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64", "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "2001:db8:1::1-2001:db8:1::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    cmd = dict(command="remote-subnet6-list", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    # Check that the subnet ID has changed.
    assert response == {"arguments": {"count": 1,
                                      "subnets": [{"id": 1, "metadata": {"server-tags": ["abc"]},
                                                   "shared-network-name": None, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "1 IPv6 subnet(s) found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_set_all_values(backend):
    _set_server(backend)
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"shared-network-name": "",
                                                                     "evaluate-additional-classes": ["XYZ"],
                                                                     "id": 2, "interface": "$(SERVER_IFACE)",
                                                                     "pools": [{"pool": "2001:db8:1::1-2001:db8:1::10",
                                                                                "option-data": [{"code": 7,
                                                                                                 "data": "12",
                                                                                                 "always-send": True,
                                                                                                 "csv-format": True}]}],
                                                                     "pd-pools": [{
                                                                         "delegated-len": 91,
                                                                         "prefix": "2001:db8:2::",
                                                                         "prefix-len": 90}],
                                                                     "reservations-global": False,
                                                                     "reservations-in-subnet": True,
                                                                     "reservations-out-of-pool": False,
                                                                     "subnet": "2001:db8:1::/64",
                                                                     "valid-lifetime": 1000,
                                                                     "rebind-timer": 500,
                                                                     "renew-timer": 200,
                                                                     "option-data": [{"code": 7,
                                                                                      "data": "123",
                                                                                      "always-send": True,
                                                                                      "csv-format": True}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 2, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_get_all_values(backend):
    _set_server(backend)
    cmd = dict(command='remote-subnet6-set', arguments={
        'remote': {
            "type": backend
        },
        'server-tags': [
            'abc'
        ],
        'subnets': [
            {
                'id': 2,
                'interface': '$(SERVER_IFACE)',
                'option-data': [
                    {
                        'always-send': True,
                        'code': 7,
                        'csv-format': True,
                        'data': '123'
                    }
                ],
                'pd-pools': [
                    {
                        'delegated-len': 91,
                        'prefix': '2001:db8:2::',
                        'prefix-len': 90
                    }
                ],
                'pools': [
                    {
                        'option-data': [
                            {
                                'always-send': True,
                                'code': 7,
                                'csv-format': True,
                                'data': '12'
                            }
                        ],
                        'pool': '2001:db8:1::1-2001:db8:1::10'
                    }
                ],
                'rebind-timer': 500,
                'renew-timer': 200,
                'evaluate-additional-classes': ['XYZ'],
                'reservations-global': False,
                'reservations-in-subnet': True,
                'reservations-out-of-pool': False,
                'shared-network-name': '',
                'subnet': '2001:db8:1::/64',
                'valid-lifetime': 1000
            }
        ]
    })

    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {
        'arguments': {
            'subnets': [
                {
                    'id': 2,
                    'subnet': '2001:db8:1::/64'
                }
            ]
        },
        'result': 0,
        'text': 'IPv6 subnet successfully set.'
    }

    cmd = dict(command='remote-subnet6-get-by-prefix', arguments={
        'remote': {
            "type": backend
        },
        'subnets': [
            {
                'subnet': '2001:db8:1::/64'
            }
        ]
    })
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {
        'arguments': {
            'count': 1,
            'subnets': [
                {
                    'id': 2,
                    'interface': srv_msg.get_server_interface(),
                    'metadata': {
                        'server-tags': [
                            'abc'
                        ]
                    },
                    'option-data': [
                        {
                            'always-send': True,
                            'code': 7,
                            'csv-format': True,
                            'data': '123',
                            'name': 'preference',
                            'never-send': False,
                            'space': 'dhcp6'
                        }
                    ],
                    'pd-pools': [
                        {
                            'delegated-len': 91,
                            'option-data': [],
                            'prefix': '2001:db8:2::',
                            'prefix-len': 90
                        }
                    ],
                    'pools': [
                        {
                            'option-data': [
                                {
                                    'always-send': True,
                                    'code': 7,
                                    'csv-format': True,
                                    'data': '12',
                                    'name': 'preference',
                                    'never-send': False,
                                    'space': 'dhcp6'
                                }
                            ],
                            'pool': '2001:db8:1::1-2001:db8:1::10'
                        }
                    ],
                    'rebind-timer': 500,
                    'relay': {
                        'ip-addresses': []
                    },
                    'renew-timer': 200,
                    'evaluate-additional-classes': ['XYZ'],
                    'reservations-global': False,
                    'reservations-in-subnet': True,
                    'reservations-out-of-pool': False,
                    'shared-network-name': None,
                    'subnet': '2001:db8:1::/64',
                    "max-valid-lifetime": 1000,
                    "min-valid-lifetime": 1000,
                    'valid-lifetime': 1000
                }
            ]
        },
        'result': 0,
        'text': 'IPv6 subnet 2001:db8:1::/64 found.'
    }


# reservation-mode is integer in db, so we need to check if it's converted correctly
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_set_reservation_mode_all_old(backend):
    _set_server(backend)
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64",
                                                                     "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "reservations-global": False,
                                                                     "reservations-in-subnet": True,
                                                                     "reservations-out-of-pool": False,
                                                                     "pools": [
                                                                         {"pool": "2001:db8:1::1-2001:db8:1::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    cmd = dict(command="remote-subnet6-get-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"subnet": "2001:db8:1::/64"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    subnet = response["arguments"]["subnets"][0]
    # since 1.9.1:
    assert "reservation-mode" not in subnet
    assert subnet["reservations-global"] is False
    assert subnet["reservations-in-subnet"] is True
    assert subnet["reservations-out-of-pool"] is False


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_set_reservation_mode_all(backend):
    _set_server(backend)
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64", "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "reservations-global": False,
                                                                     "reservations-in-subnet": True,
                                                                     "reservations-out-of-pool": False,
                                                                     "pools": [
                                                                         {"pool": "2001:db8:1::1-2001:db8:1::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    cmd = dict(command="remote-subnet6-get-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"subnet": "2001:db8:1::/64"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    subnet = response["arguments"]["subnets"][0]
    # since 1.9.1:
    assert "reservation-mode" not in subnet
    assert subnet["reservations-global"] is False
    assert subnet["reservations-in-subnet"] is True
    assert subnet["reservations-out-of-pool"] is False


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_set_reservation_mode_global_old(backend):
    _set_server(backend)
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64",
                                                                     "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     'reservations-global': True,
                                                                     'reservations-in-subnet': False,
                                                                     "pools": [
                                                                         {"pool": "2001:db8:1::1-2001:db8:1::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    cmd = dict(command="remote-subnet6-get-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"subnet": "2001:db8:1::/64"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    subnet = response["arguments"]["subnets"][0]
    # since 1.9.1:
    assert "reservation-mode" not in subnet
    assert subnet["reservations-global"] is True
    assert subnet["reservations-in-subnet"] is False


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_set_reservation_mode_global(backend):
    _set_server(backend)
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64",
                                                                     "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "reservations-global": True,
                                                                     "reservations-in-subnet": False,
                                                                     "pools": [
                                                                         {"pool": "2001:db8:1::1-2001:db8:1::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    cmd = dict(command="remote-subnet6-get-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"subnet": "2001:db8:1::/64"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    subnet = response["arguments"]["subnets"][0]
    # since 1.9.1:
    assert "reservation-mode" not in subnet
    assert subnet["reservations-global"] is True
    assert subnet["reservations-in-subnet"] is False


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_set_reservation_mode_out_of_pool_old(backend):
    _set_server(backend)
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64", "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     'reservations-global': False,
                                                                     'reservations-in-subnet': True,
                                                                     'reservations-out-of-pool': True,

                                                                     "pools": [
                                                                         {"pool": "2001:db8:1::1-2001:db8:1::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    cmd = dict(command="remote-subnet6-get-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"subnet": "2001:db8:1::/64"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    subnet = response["arguments"]["subnets"][0]
    # since 1.9.1:
    assert "reservation-mode" not in subnet
    assert subnet["reservations-global"] is False
    assert subnet["reservations-in-subnet"] is True
    assert subnet["reservations-out-of-pool"] is True


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_set_reservation_mode_out_of_pool(backend):
    _set_server(backend)
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64",
                                                                     "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "reservations-global": False,
                                                                     "reservations-in-subnet": True,
                                                                     "reservations-out-of-pool": True,
                                                                     "pools": [
                                                                         {"pool": "2001:db8:1::1-2001:db8:1::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    cmd = dict(command="remote-subnet6-get-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"subnet": "2001:db8:1::/64"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    subnet = response["arguments"]["subnets"][0]
    # since 1.9.1:
    assert "reservation-mode" not in subnet
    assert subnet["reservations-global"] is False
    assert subnet["reservations-in-subnet"] is True
    assert subnet["reservations-out-of-pool"] is True


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_set_reservation_mode_disabled_old(backend):
    _set_server(backend)
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64",
                                                                     "id": 1,
                                                                     "shared-network-name": "",
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     'reservations-global': False,
                                                                     'reservations-in-subnet': False}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    cmd = dict(command="remote-subnet6-get-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"subnet": "2001:db8:1::/64"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    subnet = response["arguments"]["subnets"][0]
    # since 1.9.1:
    assert "reservation-mode" not in subnet
    assert subnet["reservations-global"] is False
    assert subnet["reservations-in-subnet"] is False


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_set_reservation_mode_disabled(backend):
    _set_server(backend)
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64",
                                                                     "id": 1,
                                                                     "shared-network-name": "",
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "reservations-global": False,
                                                                     "reservations-in-subnet": False}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    cmd = dict(command="remote-subnet6-get-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"subnet": "2001:db8:1::/64"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    subnet = response["arguments"]["subnets"][0]
    # since 1.9.1:
    assert "reservation-mode" not in subnet
    assert subnet["reservations-global"] is False
    assert subnet["reservations-in-subnet"] is False


def _subnet_set(backend):
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64", "id": 5,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "2001:db8:1::1-2001:db8:1::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 5, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_del_by_id(backend):
    _set_server(backend)
    _subnet_set(backend)

    cmd = dict(command="remote-subnet6-del-by-id", arguments={"remote": {"type": backend},
                                                              "subnets": [{"id": 5}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv6 subnet(s) deleted."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_del_by_id_incorrect_id(backend):
    _set_server(backend)
    _subnet_set(backend)

    cmd = dict(command="remote-subnet6-del-by-id", arguments={"remote": {"type": backend},
                                                              "subnets": [{"id": 15}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 IPv6 subnet(s) deleted."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_del_id_negative_missing_subnet(backend):
    _set_server(backend)
    _subnet_set(backend)

    cmd = dict(command="remote-subnet6-del-by-id", arguments={"remote": {"type": backend},
                                                              "subnets": [{"subnet": "2001:db8:1::/64"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "missing 'id' parameter"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_del_by_prefix(backend):
    _set_server(backend)
    _subnet_set(backend)

    cmd = dict(command="remote-subnet6-del-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"subnet": "2001:db8:1::/64"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv6 subnet(s) deleted."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_del_by_prefix_non_existing_subnet(backend):
    _set_server(backend)
    _subnet_set(backend)

    cmd = dict(command="remote-subnet6-del-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"subnet": "2001:db8:2::/64"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 IPv6 subnet(s) deleted."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_del_by_prefix_missing_subnet_(backend):
    _set_server(backend)
    _subnet_set(backend)
    cmd = dict(command="remote-subnet6-del-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"id": 2}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "missing 'subnet' parameter"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_get_by_id(backend):
    _set_server(backend)
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"shared-network-name": "",
                                                                     "id": 2, "interface": "$(SERVER_IFACE)",
                                                                     "pools": [{"pool": "2001:db8:1::1-2001:db8:1::10",
                                                                                "option-data": [{"code": 7,
                                                                                                 "data": "123",
                                                                                                 "always-send": True,
                                                                                                 "csv-format": True}]}],
                                                                     'reservations-global': True,
                                                                     'reservations-in-subnet': False,
                                                                     "subnet": "2001:db8:1::/64",
                                                                     "valid-lifetime": 1000,
                                                                     "rebind-timer": 500,
                                                                     "renew-timer": 200,
                                                                     "option-data": [{"code": 7,
                                                                                      "data": "12",
                                                                                      "always-send": True,
                                                                                      "csv-format": True}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 2, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    cmd = dict(command="remote-subnet6-get-by-id", arguments={"remote": {"type": backend},
                                                              "subnets": [{"id": 2}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1,
                                      "subnets": [{"metadata": {"server-tags": ["abc"]},
                                                   "shared-network-name": None,
                                                   "id": 2, "interface": srv_msg.get_server_interface(),
                                                   "option-data": [{"always-send": True, "code": 7, "csv-format": True,
                                                                    "data": "12", "name": "preference",
                                                                    "never-send": False,
                                                                    "space": "dhcp6"}],
                                                   "pools": [{"option-data": [{"always-send": True, "code": 7,
                                                                               "csv-format": True, "data": "123",
                                                                               "name": "preference",
                                                                               "never-send": False,
                                                                               "space": "dhcp6"}],
                                                              "pool": "2001:db8:1::1-2001:db8:1::10"}],
                                                   "rebind-timer": 500, "renew-timer": 200,
                                                   "max-valid-lifetime": 1000,
                                                   "min-valid-lifetime": 1000,
                                                   "reservations-global": True,
                                                   "reservations-in-subnet": False,
                                                   "pd-pools": [],
                                                   "relay": {"ip-addresses": []},
                                                   "subnet": "2001:db8:1::/64", "valid-lifetime": 1000}]},
                        "result": 0, "text": "IPv6 subnet 2 found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_get_by_id_incorrect_id(backend):
    _set_server(backend)
    _subnet_set(backend)

    cmd = dict(command="remote-subnet6-get-by-id", arguments={"remote": {"type": backend},
                                                              "subnets": [{"id": 3}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "subnets": []},
                        "result": 3, "text": "IPv6 subnet 3 not found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_get_by_id_missing_id(backend):
    _set_server(backend)
    _subnet_set(backend)

    cmd = dict(command="remote-subnet6-get-by-id", arguments={"remote": {"type": backend},
                                                              "subnets": [{"subnet": 3}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1,
                        "text": "missing 'id' parameter"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_get_by_prefix(backend):
    _set_server(backend)
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"shared-network-name": "",
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "pools": [
                                                                         {"pool": "2001:db8:1::1-2001:db8:1::10"}],
                                                                     "reservations-global": False,
                                                                     "reservations-in-subnet": True,
                                                                     "reservations-out-of-pool": False,
                                                                     "evaluate-additional-classes": ["XYZ"],
                                                                     "subnet": "2001:db8:1::/64", "id": 1,
                                                                     "valid-lifetime": 1000}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    cmd = dict(command="remote-subnet6-get-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"subnet": "2001:db8:1::/64"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {
        "count": 1,
        "subnets": [{
            "metadata": {"server-tags": ["abc"]},
            "evaluate-additional-classes": ["XYZ"],
            "shared-network-name": None,
            "id": 1,
            "interface": srv_msg.get_server_interface(),
            "option-data": [],
            "pools": [{
                "option-data": [],
                "pool": "2001:db8:1::1-2001:db8:1::10"}],
            "reservations-global": False,
            "reservations-in-subnet": True,
            "reservations-out-of-pool": False,
            "pd-pools": [],
            "relay": {"ip-addresses": []},
            "subnet": "2001:db8:1::/64",
            "max-valid-lifetime": 1000,
            "min-valid-lifetime": 1000,
            "valid-lifetime": 1000}]}, "result": 0, "text": "IPv6 subnet 2001:db8:1::/64 found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_get_by_prefix_negative(backend):
    _set_server(backend)
    _subnet_set(backend)

    cmd = dict(command="remote-subnet6-get-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"subnet": "2001:db8:2::/63"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "subnets": []},
                        "result": 3, "text": "IPv6 subnet 2001:db8:2::/63 not found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_get_by_prefix_incorrect_prefix(backend):
    _set_server(backend)
    _subnet_set(backend)
    cmd = dict(command="remote-subnet6-get-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"subnet": "::/64"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1,
                        "text": "unable to parse invalid IPv6 prefix ::/64"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_get_by_prefix_missing_prefix(backend):
    _set_server(backend)
    _subnet_set(backend)

    cmd = dict(command="remote-subnet6-get-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"id": "2001:db8:2::/63"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1,
                        "text": "missing 'subnet' parameter"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_list(backend):
    _set_server(backend)
    _subnet_set(backend)

    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:2::/64", "id": 3,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "2001:db8:2::1-2001:db8:2::10"}]}]})
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:3::/64", "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "2001:db8:3::1-2001:db8:3::10"}]}]})
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command="remote-subnet6-list", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 3, "subnets": [{"id": 1,
                                                               "metadata": {"server-tags": ["abc"]},
                                                               "shared-network-name": None,
                                                               "subnet": "2001:db8:3::/64"},
                                                              {"id": 3,
                                                               "metadata": {"server-tags": ["abc"]},
                                                               "shared-network-name": None,
                                                               "subnet": "2001:db8:2::/64"},
                                                              {"id": 5,
                                                               "metadata": {"server-tags": ["abc"]},
                                                               "shared-network-name": None,
                                                               "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "3 IPv6 subnet(s) found."}


# network tests
@pytest.mark.parametrize('channel', ['socket', 'http'])
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_network6_set_basic(channel, backend):
    _set_server(backend)
    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{"name": "floor13"}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"shared-networks": [{"name": "floor13"}]},
                        "result": 0, "text": "IPv6 shared network successfully set."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_network6_set_missing_name(backend):
    _set_server(backend)
    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "missing parameter 'name'" in response["text"]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_network6_set_empty_name(backend):
    _set_server(backend)
    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": ""}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "'name' parameter must not be empty"}


@pytest.mark.parametrize('channel', ['socket', 'http'])
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_network6_get_basic(channel, backend):
    _set_server(backend)
    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd, channel=channel)

    cmd = dict(command="remote-network6-get", arguments={"remote": {"type": backend},
                                                         "shared-networks": [{
                                                             "name": "net1"}]})

    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1,
                                      "shared-networks": [{"interface": srv_msg.get_server_interface(), "name": "net1",
                                                           "metadata": {"server-tags": ["abc"]},
                                                           "option-data": [], "relay": {"ip-addresses": []}}]},
                        "result": 0, "text": "IPv6 shared network 'net1' found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_network6_get_all_values(backend):
    _set_server(backend)
    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "client-classes": ["abc"],
                                                             "evaluate-additional-classes": ["XYZ"],
                                                             "rebind-timer": 200,
                                                             "renew-timer": 100,
                                                             "calculate-tee-times": True,
                                                             "t1-percent": 0.5,
                                                             "t2-percent": 0.8,
                                                             "rapid-commit": True,
                                                             "valid-lifetime": 300,
                                                             'reservations-global': True,
                                                             'reservations-in-subnet': False,
                                                             "user-context": {"some weird network": 55},
                                                             "interface": "$(SERVER_IFACE)",
                                                             "option-data": [{"code": 7,
                                                                              "data": "123",
                                                                              "always-send": True,
                                                                              "csv-format": True}]}]})
    srv_msg.send_ctrl_cmd(cmd)
    cmd = dict(command="remote-network6-get", arguments={"remote": {"type": backend},
                                                         "shared-networks": [{
                                                             "name": "net1"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1,
                                      "shared-networks": [{"client-classes": ["abc"],
                                                           "rebind-timer": 200, "renew-timer": 100,
                                                           "valid-lifetime": 300,
                                                           "max-valid-lifetime": 300,
                                                           "min-valid-lifetime": 300,
                                                           "reservations-global": True,
                                                           "reservations-in-subnet": False,
                                                           "interface": srv_msg.get_server_interface(),
                                                           "metadata": {"server-tags": ["abc"]},
                                                           "evaluate-additional-classes": ["XYZ"],
                                                           "calculate-tee-times": True,
                                                           "t1-percent": 0.5,
                                                           "t2-percent": 0.8,
                                                           "rapid-commit": True,
                                                           "name": "net1",
                                                           "option-data": [{"always-send": True, "code": 7,
                                                                            "csv-format": True, "data": "123",
                                                                            "name": "preference",
                                                                            "never-send": False,
                                                                            "space": "dhcp6"}],
                                                           "relay": {"ip-addresses": []},
                                                           "user-context": {"some weird network": 55}}]},
                        "result": 0, "text": "IPv6 shared network 'net1' found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_network6_set_t1_t2(backend):
    _set_server(backend)
    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "calculate-tee-times": True,
                                                             "t1-percent": 0.5,
                                                             "t2-percent": 10,
                                                             "interface": "$(SERVER_IFACE)"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "'t2-percent' parameter is not a real" in response["text"]

    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "calculate-tee-times": True,
                                                             "t1-percent": 10,
                                                             "t2-percent": 0.5,
                                                             "interface": "$(SERVER_IFACE)"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "'t1-percent' parameter is not a real" in response["text"]

    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "calculate-tee-times": True,
                                                             "t1-percent": 0.5,
                                                             "t2-percent": 0.1,
                                                             "interface": "$(SERVER_IFACE)"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "t1-percent:  0.5 is invalid, it must be less than t2-percent: 0.1" in response["text"]


@pytest.mark.parametrize('channel', ['socket', 'http'])
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_network6_list_basic(channel, backend):
    _set_server(backend)
    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd, channel=channel)

    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net2",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd, channel=channel)

    cmd = dict(command="remote-network6-list", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 2, "shared-networks": [{"metadata": {"server-tags": ["abc"]},
                                                                       "name": "net1"},
                                                                      {"metadata": {"server-tags": ["abc"]},
                                                                       "name": "net2"}]},
                        "result": 0,
                        "text": "2 IPv6 shared network(s) found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_network6_list_no_networks(backend):
    _set_server(backend)
    cmd = dict(command="remote-network6-list", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0,
                                      "shared-networks": []},
                        "result": 3,
                        "text": "0 IPv6 shared network(s) found."}


@pytest.mark.parametrize('channel', ['socket', 'http'])
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_network6_del_basic(channel, backend):
    _set_server(backend)
    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd, channel=channel)

    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net2",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd, channel=channel)

    cmd = dict(command="remote-network6-list", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"count": 2,
                                      "shared-networks": [{"metadata": {"server-tags": ["abc"]}, "name": "net1"},
                                                          {"metadata": {"server-tags": ["abc"]}, "name": "net2"}]},
                        "result": 0,
                        "text": "2 IPv6 shared network(s) found."}

    cmd = dict(command="remote-network6-del", arguments={"remote": {"type": backend},
                                                         "shared-networks": [{"name": "net1"}]})

    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv6 shared network(s) deleted."}

    cmd = dict(command="remote-network6-list", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"count": 1,
                                      "shared-networks": [{"metadata": {"server-tags": ["abc"]}, "name": "net2"}]},
                        "result": 0, "text": "1 IPv6 shared network(s) found."}

    cmd = dict(command="remote-network6-del", arguments={"remote": {"type": backend},
                                                         "shared-networks": [{"name": "net2"}]})

    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv6 shared network(s) deleted."}

    cmd = dict(command="remote-network6-list", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel, exp_result=3)

    assert response == {"arguments": {"count": 0,
                                      "shared-networks": []},
                        "result": 3,
                        "text": "0 IPv6 shared network(s) found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_network6_del_subnet_keep(backend):
    _set_server(backend)
    # add networks
    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net2",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command="remote-network6-list", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 2,
                                      "shared-networks": [{"metadata": {"server-tags": ["abc"]},
                                                           "name": "net1"},
                                                          {"metadata": {"server-tags": ["abc"]},
                                                           "name": "net2"}]},
                        "result": 0,
                        "text": "2 IPv6 shared network(s) found."}

    # add subnets to networks
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64", "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "net1",
                                                                     "pools": [{
                                                                         "pool": "2001:db8:1::1-2001:db8:1::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:2::/64", "id": 2,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "net2",
                                                                     "pools": [{
                                                                         "pool": "2001:db8:2::1-2001:db8:2::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 2, "subnet": "2001:db8:2::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    # we want to have 2 subnets
    cmd = dict(command="remote-subnet6-list", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 2, "subnets": [{"id": 1, "subnet": "2001:db8:1::/64",
                                                               "shared-network-name": "net1",
                                                               "metadata": {"server-tags": ["abc"]}},
                                                              {"id": 2, "subnet": "2001:db8:2::/64",
                                                               "shared-network-name": "net2",
                                                               "metadata": {"server-tags": ["abc"]}}]},
                        "result": 0, "text": "2 IPv6 subnet(s) found."}

    cmd = dict(command="remote-network6-del", arguments={"remote": {"type": backend}, "subnets-action": "keep",
                                                         "shared-networks": [{"name": "net1"}]})

    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv6 shared network(s) deleted."}

    cmd = dict(command="remote-network6-list", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1,
                                      "shared-networks": [{"metadata": {"server-tags": ["abc"]}, "name": "net2"}]},
                        "result": 0, "text": "1 IPv6 shared network(s) found."}

    # after deleting network we still want to have 2 subnets
    cmd = dict(command="remote-subnet6-list", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 2,
                                      "subnets": [{"id": 1, "metadata": {"server-tags": ["abc"]},
                                                   "shared-network-name": None, "subnet": "2001:db8:1::/64"},
                                                  {"id": 2, "metadata": {"server-tags": ["abc"]},
                                                   "shared-network-name": "net2", "subnet": "2001:db8:2::/64"}]},
                        "result": 0, "text": "2 IPv6 subnet(s) found."}

    cmd = dict(command="remote-network6-del", arguments={"remote": {"type": backend}, "subnets-action": "keep",
                                                         "shared-networks": [{"name": "net2"}]})

    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv6 shared network(s) deleted."}

    cmd = dict(command="remote-network6-list", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0,
                                      "shared-networks": []},
                        "result": 3,
                        "text": "0 IPv6 shared network(s) found."}

    # after removing all networks we still want to have both subnets
    cmd = dict(command="remote-subnet6-list", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 2,
                                      "subnets": [{"id": 1, "metadata": {"server-tags": ["abc"]},
                                                   "shared-network-name": None, "subnet": "2001:db8:1::/64"},
                                                  {"id": 2, "metadata": {"server-tags": ["abc"]},
                                                   "shared-network-name": None, "subnet": "2001:db8:2::/64"}]},
                        "result": 0, "text": "2 IPv6 subnet(s) found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_network6_del_subnet_delete_simple(backend):
    _set_server(backend)
    # the v6 counterpart of ticket #738
    cmd = dict(command='remote-network6-set', arguments={
        'remote': {
            "type": backend
        },
        'server-tags': [
            'abc'
        ],
        'shared-networks': [
            {
                'interface': '$(SERVER_IFACE)',
                'name': 'net1'
            }
        ]
    })
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command='remote-subnet6-set', arguments={
        'remote': {
            "type": backend
        },
        'server-tags': [
            'abc'
        ],
        'subnets': [
            {
                'id': 1,
                'interface': '$(SERVER_IFACE)',
                'pools': [
                    {
                        'pool': '2001:db8:1::0-2001:db8:1::100'
                    }
                ],
                'shared-network-name': 'net1',
                'subnet': '2001:db8:1::/64'
            }
        ]
    })
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command='remote-network6-del', arguments={
        'remote': {
            "type": backend
        },
        'shared-networks': [
            {
                'name': 'net1'
            }
        ],
        'subnets-action': 'delete'
    })
    srv_msg.send_ctrl_cmd(cmd)


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_network6_del_subnet_delete(backend):
    _set_server(backend)
    # add networks
    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net2",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command="remote-network6-list", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 2,
                                      "shared-networks": [{"metadata": {"server-tags": ["abc"]},
                                                           "name": "net1"},
                                                          {"metadata": {"server-tags": ["abc"]},
                                                           "name": "net2"}]},
                        "result": 0,
                        "text": "2 IPv6 shared network(s) found."}

    # add subnets to networks
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64", "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "net1",
                                                                     "pools": [{
                                                                         "pool": "2001:db8:1::1-2001:db8:1::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:2::/64", "id": 2,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "net2",
                                                                     "pools": [{
                                                                         "pool": "2001:db8:2::1-2001:db8:2::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 2, "subnet": "2001:db8:2::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    # we want to have 2 subnets
    cmd = dict(command="remote-subnet6-list", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 2, "subnets": [{"id": 1, "subnet": "2001:db8:1::/64",
                                                               "shared-network-name": "net1",
                                                               "metadata": {"server-tags": ["abc"]}},
                                                              {"id": 2, "subnet": "2001:db8:2::/64",
                                                               "shared-network-name": "net2",
                                                               "metadata": {"server-tags": ["abc"]}}]},
                        "result": 0, "text": "2 IPv6 subnet(s) found."}

    cmd = dict(command="remote-network6-del", arguments={"remote": {"type": backend}, "subnets-action": "delete",
                                                         "shared-networks": [{"name": "net1"}]})

    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv6 shared network(s) deleted."}

    cmd = dict(command="remote-network6-list", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1,
                                      "shared-networks": [{"metadata": {"server-tags": ["abc"]}, "name": "net2"}]},
                        "result": 0, "text": "1 IPv6 shared network(s) found."}

    # after deleting network we still want to have 2 subnets
    cmd = dict(command="remote-subnet6-list", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1,
                                      "subnets": [{"id": 2, "metadata": {"server-tags": ["abc"]},
                                                   "shared-network-name": "net2", "subnet": "2001:db8:2::/64"}]},
                        "result": 0, "text": "1 IPv6 subnet(s) found."}

    cmd = dict(command="remote-network6-del", arguments={"remote": {"type": backend}, "subnets-action": "delete",
                                                         "shared-networks": [{"name": "net2"}]})

    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv6 shared network(s) deleted."}

    cmd = dict(command="remote-network6-list", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0,
                                      "shared-networks": []},
                        "result": 3,
                        "text": "0 IPv6 shared network(s) found."}

    # all subnets should be removed now
    cmd = dict(command="remote-subnet6-list", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "subnets": []},
                        "result": 3, "text": "0 IPv6 subnet(s) found."}


def _set_global_parameter(backend):
    cmd = dict(command="remote-global-parameter6-set", arguments={"remote": {"type": backend},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": {
                                                                      "decline-probation-period": 123456}})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1, "parameters": {"decline-probation-period": 123456}},
                        "result": 0,
                        "text": "1 DHCPv6 global parameter(s) successfully set."}


# global-parameter tests
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_parameter6_set_text(backend):
    _set_server(backend)
    _set_global_parameter(backend)


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_parameter6_set_integer(backend):
    _set_server(backend)
    cmd = dict(command="remote-global-parameter6-set", arguments={"remote": {"type": backend},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": {"valid-lifetime": 1000}})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1, "parameters": {"valid-lifetime": 1000}},
                        "result": 0,
                        "text": "1 DHCPv6 global parameter(s) successfully set."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_parameter6_set_incorrect_parameter(backend):
    _set_server(backend)
    cmd = dict(command="remote-global-parameter6-set", arguments={"remote": {"type": backend},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": {"decline-aaa-period": 1234556}})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "unknown parameter 'decline-aaa-period'"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_parameter6_del(backend):
    _set_server(backend)
    _set_global_parameter(backend)

    cmd = dict(command="remote-global-parameter6-del", arguments={"remote": {"type": backend},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": ["decline-probation-period"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1},
                        "result": 0, "text": "1 DHCPv6 global parameter(s) deleted."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_parameter6_del_not_existing_parameter(backend):
    _set_server(backend)
    cmd = dict(command="remote-global-parameter6-del", arguments={"remote": {"type": backend},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": ["decline-probation-period"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0},
                        "result": 3, "text": "0 DHCPv6 global parameter(s) deleted."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_parameter6_get(backend):
    _set_server(backend)
    _set_global_parameter(backend)

    cmd = dict(command="remote-global-parameter6-get", arguments={"remote": {"type": backend},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": ["decline-probation-period"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1,
                                      "parameters": {"decline-probation-period": 123456,
                                                     "metadata": {"server-tags": ["abc"]}}},
                        "result": 0, "text": "'decline-probation-period' DHCPv6 global parameter found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_parameter6_get_all_one(backend):
    _set_server(backend)
    _set_global_parameter(backend)

    cmd = dict(command="remote-global-parameter6-get-all", arguments={"remote": {"type": backend},
                                                                      "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1, "parameters": [{"decline-probation-period": 123456,
                                                                  "metadata": {"server-tags": ["abc"]}}]},
                        "result": 0, "text": "1 DHCPv6 global parameter(s) found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_parameter6_get_all_multiple(backend):
    _set_server(backend)
    _set_global_parameter(backend)

    cmd = dict(command="remote-global-parameter6-set", arguments={"remote": {"type": backend},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": {"calculate-tee-times": True}})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1, "parameters": {"calculate-tee-times": True}},
                        "result": 0,
                        "text": "1 DHCPv6 global parameter(s) successfully set."}

    cmd = dict(command="remote-global-parameter6-get-all", arguments={"remote": {"type": backend},
                                                                      "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response["result"] == 0
    assert response["text"] == "2 DHCPv6 global parameter(s) found."
    assert response["arguments"]["count"] == 2
    assert {"calculate-tee-times": True, "metadata": {"server-tags": ["abc"]}} in response["arguments"]["parameters"]
    assert {"decline-probation-period": 123456,
            "metadata": {"server-tags": ["abc"]}} in response["arguments"]["parameters"]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_parameter6_get_all_zero(backend):
    _set_server(backend)
    cmd = dict(command="remote-global-parameter6-get-all", arguments={"remote": {"type": backend},
                                                                      "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "parameters": []},
                        "result": 3, "text": "0 DHCPv6 global parameter(s) found."}


def _set_option_def(backend, channel='http'):
    cmd = dict(command="remote-option-def6-set", arguments={"remote": {"type": backend},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 222,
                                                                "type": "uint32"}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"option-defs": [{"code": 222, "space": "dhcp6"}]},
                        "result": 0, "text": "DHCPv6 option definition successfully set."}


@pytest.mark.parametrize('channel', ['socket', 'http'])
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def6_set_basic(channel, backend):
    _set_server(backend)
    _set_option_def(backend, channel)


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def6_set_using_zero_as_code(backend):
    _set_server(backend)
    cmd = dict(command="remote-option-def6-set", arguments={"remote": {"type": backend},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 0,
                                                                "type": "uint32"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "invalid option code '0': reserved value" in response["text"]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def6_set_using_standard_code(backend):
    _set_server(backend)
    cmd = dict(command="remote-option-def6-set", arguments={"remote": {"type": backend},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 24,
                                                                "type": "uint32"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "an option with code 24 already exists in space 'dhcp6'"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def6_set_missing_parameters(backend):
    _set_server(backend)
    cmd = dict(command="remote-option-def6-set", arguments={"remote": {"type": backend},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "code": 222,
                                                                "type": "uint32",
                                                                "array": False,
                                                                "record-types": "",
                                                                "space": "dhcp6",
                                                                "encapsulate": ""}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "missing parameter 'name'" in response["text"]

    cmd = dict(command="remote-option-def6-set", arguments={"remote": {"type": backend},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "aa",
                                                                "type": "uint32",
                                                                "array": False,
                                                                "record-types": "",
                                                                "space": "dhcp6",
                                                                "encapsulate": ""}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "missing parameter 'code'" in response["text"]

    cmd = dict(command="remote-option-def6-set", arguments={"remote": {"type": backend},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "aa",
                                                                "code": 234,
                                                                "array": False,
                                                                "record-types": "",
                                                                "space": "dhcp6",
                                                                "encapsulate": ""}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "missing parameter 'type'" in response["text"]


@pytest.mark.parametrize('channel', ['socket', 'http'])
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def6_get_basic(channel, backend):
    _set_server(backend)
    _set_option_def(backend)

    cmd = dict(command="remote-option-def6-get", arguments={"remote": {"type": backend},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "code": 222}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {"arguments": {"count": 1, "option-defs": [{"array": False, "code": 222, "encapsulate": "",
                                                                   "name": "foo", "record-types": "", "space": "dhcp6",
                                                                   "metadata": {"server-tags": ["abc"]},
                                                                   "type": "uint32"}]},
                        "result": 0, "text": "DHCPv6 option definition 222 in 'dhcp6' found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def6_get_multiple_defs(backend):
    _set_server(backend)
    _set_option_def(backend)

    cmd = dict(command="remote-option-def6-set", arguments={"remote": {"type": backend},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 222,
                                                                "type": "uint32",
                                                                "space": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"option-defs": [{"code": 222, "space": "abc"}]},
                        "result": 0, "text": "DHCPv6 option definition successfully set."}

    cmd = dict(command="remote-option-def6-get", arguments={"remote": {"type": backend},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "code": 222,
                                                                "space": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1, "option-defs": [{"array": False, "code": 222, "encapsulate": "",
                                                                   "name": "foo", "record-types": "", "space": "abc",
                                                                   "metadata": {"server-tags": ["abc"]},
                                                                   "type": "uint32"}]},
                        "result": 0, "text": "DHCPv6 option definition 222 in 'abc' found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def6_get_missing_code(backend):
    _set_server(backend)
    cmd = dict(command="remote-option-def6-get", arguments={"remote": {"type": backend},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "missing 'code' parameter"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def6_get_all_option_not_defined(backend):
    _set_server(backend)
    cmd = dict(command="remote-option-def6-get-all", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "option-defs": []},
                        "result": 3, "text": "0 DHCPv6 option definition(s) found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def6_get_all_multiple_defs(backend):
    _set_server(backend)
    _set_option_def(backend)

    cmd = dict(command="remote-option-def6-set", arguments={"remote": {"type": backend},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 222,
                                                                "type": "uint32",
                                                                "space": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"option-defs": [{"code": 222, "space": "abc"}]},
                        "result": 0, "text": "DHCPv6 option definition successfully set."}

    cmd = dict(command="remote-option-def6-get-all", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 2, "option-defs": [{"array": False, "code": 222,
                                                                   "encapsulate": "", "name": "foo",
                                                                   "record-types": "", "space": "abc",
                                                                   "metadata": {"server-tags": ["abc"]},
                                                                   "type": "uint32"},
                                                                  {"array": False, "code": 222,
                                                                   "encapsulate": "", "name": "foo",
                                                                   "record-types": "", "space": "dhcp6",
                                                                   "metadata": {"server-tags": ["abc"]},
                                                                   "type": "uint32"}]},
                        "result": 0, "text": "2 DHCPv6 option definition(s) found."}


@pytest.mark.parametrize('channel', ['socket', 'http'])
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def6_get_all_basic(channel, backend):
    _set_server(backend)
    _set_option_def(backend)

    cmd = dict(command="remote-option-def6-get-all", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {"arguments": {"count": 1, "option-defs": [{"array": False, "code": 222, "encapsulate": "",
                                                                   "metadata": {"server-tags": ["abc"]},
                                                                   "name": "foo", "record-types": "", "space": "dhcp6",
                                                                   "type": "uint32"}]},
                        "result": 0, "text": "1 DHCPv6 option definition(s) found."}


@pytest.mark.parametrize('channel', ['socket', 'http'])
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def6_del_basic(channel, backend):
    _set_server(backend)
    _set_option_def(backend)

    cmd = dict(command="remote-option-def6-del", arguments={"remote": {"type": backend}, "server-tags": ["abc"],
                                                            "option-defs": [{"code": 222}]})

    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv6 option definition(s) deleted."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def6_del_different_space(backend):
    _set_server(backend)
    _set_option_def(backend)

    cmd = dict(command="remote-option-def6-del", arguments={"remote": {"type": backend}, "server-tags": ["abc"],
                                                            "option-defs": [{"code": 222, "space": "abc"}]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 DHCPv6 option definition(s) deleted."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def6_del_incorrect_code(backend):
    _set_server(backend)
    cmd = dict(command="remote-option-def6-del", arguments={"remote": {"type": backend},
                                                            "server-tags": ["abc"], "option-defs": [{"name": 22}]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "missing 'code' parameter"}

    cmd = dict(command="remote-option-def6-del", arguments={"remote": {"type": backend},
                                                            "server-tags": ["abc"], "option-defs": [{}]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "missing 'code' parameter"}

    cmd = dict(command="remote-option-def6-del", arguments={"remote": {"type": backend},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{"code": "abc"}]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "'code' parameter is not an integer"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def6_del_missing_option(backend):
    _set_server(backend)
    cmd = dict(command="remote-option-def6-del", arguments={"remote": {"type": backend},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{"code": 212}]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 DHCPv6 option definition(s) deleted."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def6_del_multiple_options(backend):
    _set_server(backend)
    _set_option_def(backend)

    cmd = dict(command="remote-option-def6-set", arguments={"remote": {"type": backend},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 222,
                                                                "type": "uint32",
                                                                "space": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"option-defs": [{"code": 222, "space": "abc"}]},
                        "result": 0, "text": "DHCPv6 option definition successfully set."}

    cmd = dict(command="remote-option-def6-del", arguments={"remote": {"type": backend},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{"code": 222}]})

    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv6 option definition(s) deleted."}

    cmd = dict(command="remote-option-def6-get-all", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1, "option-defs": [{"array": False, "code": 222, "encapsulate": "",
                                                                   "metadata": {"server-tags": ["abc"]},
                                                                   "name": "foo", "record-types": "", "space": "abc",
                                                                   "type": "uint32"}]},
                        "result": 0, "text": "1 DHCPv6 option definition(s) found."}


def _set_global_option(backend, channel='http'):
    cmd = dict(command="remote-option6-global-set", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "code": 7,
                                                                   "data": "123"}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"result": 0, "text": "DHCPv6 option successfully set.",
                        "arguments": {"options": [{"code": 7, "space": "dhcp6"}]}}


@pytest.mark.parametrize('channel', ['socket', 'http'])
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option6_global_set_basic(channel, backend):
    _set_server(backend)
    _set_global_option(backend, channel)


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option6_global_set_missing_data(backend):
    _set_server(backend)
    cmd = dict(command="remote-option6-global-set", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "code": 7}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "no option value specified" in response["text"]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option6_global_set_name(backend):
    _set_server(backend)
    cmd = dict(command="remote-option6-global-set", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "name": "sip-server-dns",
                                                                   "data": "isc.example.com"}]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"options": [{"code": 21, "space": "dhcp6"}]},
                        "result": 0, "text": "DHCPv6 option successfully set."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option6_global_set_incorrect_code_missing_name(backend):
    _set_server(backend)
    cmd = dict(command="remote-option6-global-set", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "code": "aaa"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "'code' parameter is not an integer" in response["text"]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option6_global_set_incorrect_name_missing_code(backend):
    _set_server(backend)
    cmd = dict(command="remote-option6-global-set", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "name": 123}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "'name' parameter is not a string" in response["text"]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option6_global_set_missing_code_and_name(backend):
    _set_server(backend)
    cmd = dict(command="remote-option6-global-set", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "option data configuration requires one of 'code' or 'name' parameters to be specified" in response["text"]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option6_global_set_incorrect_code(backend):
    _set_server(backend)
    cmd = dict(command="remote-option6-global-set", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": "aa",
                                                                            "name": "cc"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "'code' parameter is not an integer" in response["text"]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option6_global_set_incorrect_name(backend):
    _set_server(backend)
    cmd = dict(command="remote-option6-global-set", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 7,
                                                                            "name": 7,
                                                                            "data": "123"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "'name' parameter is not a string" in response["text"]


@pytest.mark.parametrize('channel', ['socket', 'http'])
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option6_global_get_basic(channel, backend):
    _set_server(backend)
    _set_global_option(backend)

    cmd = dict(command="remote-option6-global-get", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 7}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {"arguments": {"count": 1, "options": [{"always-send": False, "code": 7, "csv-format": True,
                                                               "data": "123",
                                                               "metadata": {"server-tags": ["abc"]},
                                                               "name": "preference",
                                                               "never-send": False, "space": "dhcp6"}]},
                        "result": 0, "text": "DHCPv6 option 7 in 'dhcp6' found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option6_global_set_different_space(backend):
    _set_server(backend)
    cmd = dict(command="remote-option6-global-set", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 7,
                                                                            "data": "123",
                                                                            "always-send": True,
                                                                            "csv-format": True,
                                                                            "space": "xyz"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "definition for the option 'xyz.' having code '7' does not exist" in response["text"]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option6_global_set_csv_false_incorrect(backend):
    _set_server(backend)
    cmd = dict(command="remote-option6-global-set", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 7,
                                                                            "data": "12Z3",
                                                                            "always-send": True,
                                                                            "csv-format": False}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "option data is not a valid string of hexadecimal digits: 12Z3" in response["text"]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option6_global_set_csv_false_correct(backend):
    _set_server(backend)
    cmd = dict(command="remote-option6-global-set", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 7,
                                                                            "data": "C0000201",  # 192.0.2.1
                                                                            "always-send": True,
                                                                            "csv-format": False}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"result": 0, "text": "DHCPv6 option successfully set.",
                        "arguments": {"options": [{"code": 7, "space": "dhcp6"}]}}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option6_global_set_csv_false_incorrect_hex(backend):
    _set_server(backend)
    cmd = dict(command="remote-option6-global-set", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 7,
                                                                            "data": "C0000201Z",
                                                                            "always-send": True,
                                                                            "csv-format": False}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "option data is not a valid string of hexadecimal digits: C0000201Z" in response["text"]


@pytest.mark.parametrize('channel', ['socket', 'http'])
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option6_global_del_basic(channel, backend):
    _set_server(backend)
    _set_global_option(backend)

    cmd = dict(command="remote-option6-global-del", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 7}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv6 option(s) deleted."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option6_global_del_missing_code(backend):
    _set_server(backend)
    cmd = dict(command="remote-option6-global-del", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"ab": 7}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "missing 'code' parameter"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option6_global_del_incorrect_code(backend):
    _set_server(backend)
    cmd = dict(command="remote-option6-global-del", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": "7"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "'code' parameter is not an integer"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option6_global_del_missing_option(backend):
    _set_server(backend)
    cmd = dict(command="remote-option6-global-del", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 7}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 DHCPv6 option(s) deleted."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option6_global_get_missing_code(backend):
    _set_server(backend)
    cmd = dict(command="remote-option6-global-get", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"ab": 6}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "missing 'code' parameter"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option6_global_get_incorrect_code(backend):
    _set_server(backend)
    cmd = dict(command="remote-option6-global-get", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": "7"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "'code' parameter is not an integer"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option6_global_get_missing_option(backend):
    _set_server(backend)
    cmd = dict(command="remote-option6-global-get", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert response == {"arguments": {"count": 0, "options": []},
                        "result": 3, "text": "DHCPv6 option 6 in 'dhcp6' not found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option6_global_get_csv_false(backend):
    _set_server(backend)
    cmd = dict(command="remote-option6-global-set",
               arguments={"remote": {"type": backend},
                          "server-tags": ["abc"],
                          "options": [{"code": 22,
                                       # in data: 1 IPv6 address encoded as 16 octets
                                       "data": "C0000301C00003020a0b0c0d0e0f0807",
                                       "always-send": True,
                                       "csv-format": False}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"result": 0, "text": "DHCPv6 option successfully set.",
                        "arguments": {"options": [{"code": 22, "space": "dhcp6"}]}}

    cmd = dict(command="remote-option6-global-get",
               arguments={"remote": {"type": backend},
                          "server-tags": ["abc"],
                          "options": [{"code": 22}]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1, "options": [{"always-send": True, "code": 22, "csv-format": False,
                                                               "data": "C0000301C00003020A0B0C0D0E0F0807",
                                                               "metadata": {"server-tags": ["abc"]},
                                                               "name": "sip-server-addr",
                                                               "never-send": False, "space": "dhcp6"}]},
                        "result": 0, "text": "DHCPv6 option 22 in 'dhcp6' found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option6_global_get_all(backend):
    _set_server(backend)
    _set_global_option(backend)

    cmd = dict(command="remote-option6-global-set", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "code": 22,
                                                                   "data": "2001:db8::2"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"result": 0, "text": "DHCPv6 option successfully set.",
                        "arguments": {"options": [{"code": 22, "space": "dhcp6"}]}}

    cmd = dict(command="remote-option6-global-get-all", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 2,
                                      "options": [{"always-send": False, "code": 7, "csv-format": True,
                                                   "metadata": {"server-tags": ["abc"]},
                                                   "data": "123", "name": "preference",
                                                   "never-send": False, "space": "dhcp6"},
                                                  {"always-send": False, "code": 22, "csv-format": True,
                                                   "metadata": {"server-tags": ["abc"]},
                                                   "data": "2001:db8::2", "name": "sip-server-addr",
                                                   "never-send": False, "space": "dhcp6"}]},
                        "result": 0, "text": "2 DHCPv6 option(s) found."}

    cmd = dict(command="remote-option6-global-del", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 7}]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv6 option(s) deleted."}

    cmd = dict(command="remote-option6-global-get-all", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1, "options": [{"always-send": False, "code": 22, "csv-format": True,
                                                               "data": "2001:db8::2", "name": "sip-server-addr",
                                                               "metadata": {"server-tags": ["abc"]},
                                                               "never-send": False, "space": "dhcp6"}]},
                        "result": 0, "text": "1 DHCPv6 option(s) found."}

    cmd = dict(command="remote-option6-global-del", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 22}]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv6 option(s) deleted."}

    cmd = dict(command="remote-option6-global-get-all", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert response == {"arguments": {"count": 0, "options": []}, "result": 3, "text": "0 DHCPv6 option(s) found."}
