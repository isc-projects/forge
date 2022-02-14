"""Kea database config backend commands hook testing"""

import pytest

import srv_msg

from cb_model import setup_server_for_config_backend_cmds
from forge_cfg import world


pytestmark = [pytest.mark.v4,
              pytest.mark.kea_only,
              pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.config_backend,
              pytest.mark.cb_cmds]


def _set_server_tag(backend, tag):
    cmd = dict(command="remote-server%s-set" % world.proto[-1], arguments={"remote": {"type": backend},
                                                                           "servers": [{"server-tag": tag}]})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)


def _setup_server(backend):
    setup_server_for_config_backend_cmds(backend_type=backend)
    _set_server_tag(backend, "abc")


def _send_cmd(cmd, backend="", tag=None, channel='http', exp_result=0):
    # remote and tag in cmd have priority over the ones in the parameters.
    if "remote" not in cmd["arguments"]:
        cmd["arguments"].update({"remote": {"type": backend}})
    if "server-tags" not in cmd["arguments"] and tag is not None:
        if not isinstance(tag, list):
            tag = [tag]
        cmd["arguments"].update({"server-tags": tag})

    return srv_msg.send_ctrl_cmd(cmd, channel=channel, exp_result=exp_result)


def test_availability():
    _setup_server('mysql')
    cmd = dict(command='list-commands')
    response = srv_msg.send_ctrl_cmd(cmd)

    for cmd in ["remote-class4-del",
                "remote-class4-get",
                "remote-class4-get-all",
                "remote-class4-set",
                "remote-global-parameter4-del",
                "remote-global-parameter4-get",
                "remote-global-parameter4-get-all",
                "remote-global-parameter4-set",
                "remote-network4-del",
                "remote-network4-get",
                "remote-network4-list",
                "remote-network4-set",
                "remote-option-def4-del",
                "remote-option-def4-get",
                "remote-option-def4-get-all",
                "remote-option-def4-set",
                "remote-option4-global-del",
                "remote-option4-global-get",
                "remote-option4-global-get-all",
                "remote-option4-global-set",
                "remote-option4-network-del",
                "remote-option4-network-set",
                "remote-option4-pool-del",
                "remote-option4-pool-set",
                "remote-option4-subnet-del",
                "remote-option4-subnet-set",
                "remote-server4-del",
                "remote-server4-get",
                "remote-server4-get-all",
                "remote-server4-set",
                "remote-subnet4-del-by-id",
                "remote-subnet4-del-by-prefix",
                "remote-subnet4-get-by-id",
                "remote-subnet4-get-by-prefix",
                "remote-subnet4-list",
                "remote-subnet4-set",
                "server-tag-get"]:
        assert cmd in response['arguments']


# subnet tests
@pytest.mark.parametrize('channel', ['socket', 'http'])
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_set_basic(channel, backend):
    _setup_server(backend)
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24",
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "id": 1,
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "192.168.50.1-192.168.50.100"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_set_empty_subnet(backend):
    _setup_server(backend)
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "shared-network-name": "",
                                                        "subnets": [{"subnet": "",
                                                                     "id": 1,
                                                                     "interface": "$(SERVER_IFACE)"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "subnet configuration failed: Invalid subnet syntax (prefix/len expected):" in response["text"]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_set_missing_subnet(backend):
    _setup_server(backend)
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "shared-network-name": "",
                                                        "subnets": [{"interface": "$(SERVER_IFACE)", "id": 1}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "subnet configuration failed: mandatory 'subnet' parameter " \
           "is missing for a subnet being configured" in response["text"]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_set_stateless(backend):
    _setup_server(backend)
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24",
                                                                     "id": 1,
                                                                     "shared-network-name": "",
                                                                     "interface": "$(SERVER_IFACE)"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_set_id(backend):
    _setup_server(backend)
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24", "id": 5,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "192.168.50.1-192.168.50.100"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 5, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_set_duplicated_id(backend):
    _setup_server(backend)
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24", "id": 5,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "192.168.50.1-192.168.50.100"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 5, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.51.0/24", "id": 5,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "192.168.51.1-192.168.51.100"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 5, "subnet": "192.168.51.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-list", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1,
                                      "subnets": [{"id": 5, "metadata": {"server-tags": ["abc"]},
                                                   "shared-network-name": None, "subnet": "192.168.51.0/24"}]},
                        "result": 0, "text": "1 IPv4 subnet(s) found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_set_duplicated_subnet(backend):
    _setup_server(backend)
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24", "id": 5,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "192.168.50.1-192.168.50.100"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 5, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24", "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "192.168.50.1-192.168.50.100"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-list", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    # Check that the subnet ID has changed.
    assert response == {"arguments": {"count": 1,
                                      "subnets": [{"id": 1, "metadata": {"server-tags": ["abc"]},
                                                   "shared-network-name": None, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "1 IPv4 subnet(s) found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_set_all_values(backend):
    _setup_server(backend)
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"4o6-interface": "eth9",
                                                                     "4o6-interface-id": "interf-id",
                                                                     "4o6-subnet": "2000::/64",
                                                                     "authoritative": False,
                                                                     "boot-file-name": "file-name",
                                                                     "shared-network-name": "",
                                                                     "id": 2, "interface": "$(SERVER_IFACE)",
                                                                     "match-client-id": False, "next-server": "0.0.0.0",
                                                                     "pools": [{"pool": "192.168.50.1-192.168.50.100",
                                                                                "option-data": [{"code": 6,
                                                                                                 "data": '192.0.2.2',
                                                                                                 "always-send": True,
                                                                                                 "csv-format": True}]}],
                                                                     "relay": {"ip-addresses": ["192.168.5.5"]},
                                                                     "reservation-mode": "all",
                                                                     "server-hostname": "name-xyz",
                                                                     "subnet": "192.168.50.0/24",
                                                                     "valid-lifetime": 1000,
                                                                     "rebind-timer": 500,
                                                                     "renew-timer": 200,
                                                                     "option-data": [{"code": 6,
                                                                                      "data": '192.0.2.1',
                                                                                      "always-send": True,
                                                                                      "csv-format": True}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 2, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_get_all_values(backend):
    _setup_server(backend)
    cmd = dict(command='remote-subnet4-set', arguments={
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
                        'code': 6,
                        'csv-format': True,
                        'data': '192.0.2.1'
                    }
                ],
                'pools': [
                    {
                        'option-data': [
                            {
                                'always-send': True,
                                'code': 6,
                                'csv-format': True,
                                'data': '192.0.2.2'
                            }
                        ],
                        'pool': '192.168.50.1-192.168.50.100'
                    }
                ],
                'rebind-timer': 500,
                'relay': {
                    'ip-addresses': [
                        '192.168.5.5'
                    ]
                },
                'renew-timer': 200,
                'require-client-classes': [
                    'XYZ'
                ],
                'reservation-mode': 'all',
                'server-hostname': 'name-xyz',
                'shared-network-name': '',
                'subnet': '192.168.50.0/24',
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
                    'subnet': '192.168.50.0/24'
                }
            ]
        },
        'result': 0,
        'text': 'IPv4 subnet successfully set.'
    }

    cmd = dict(command='remote-subnet4-get-by-prefix', arguments={
        'remote': {
            "type": backend
        },
        'subnets': [
            {
                'subnet': '192.168.50.0/24'
            }
        ]
    })
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {
        'arguments': {
            'count': 1,
            'subnets': [
                {
                    '4o6-interface': '',
                    '4o6-interface-id': '',
                    '4o6-subnet': '',
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
                            'code': 6,
                            'csv-format': True,
                            'data': '192.0.2.1',
                            'name': 'domain-name-servers',
                            'space': 'dhcp4'
                        }
                    ],
                    'pools': [
                        {
                            'option-data': [
                                {
                                    'always-send': True,
                                    'code': 6,
                                    'csv-format': True,
                                    'data': '192.0.2.2',
                                    'name': 'domain-name-servers',
                                    'space': 'dhcp4'
                                }
                            ],
                            'pool': '192.168.50.1-192.168.50.100'
                        }
                    ],
                    'rebind-timer': 500,
                    'relay': {
                        'ip-addresses': [
                            '192.168.5.5'
                        ]
                    },
                    'renew-timer': 200,
                    'require-client-classes': [
                        'XYZ'
                    ],
                    'reservations-global': False,
                    'reservations-in-subnet': True,
                    'reservations-out-of-pool': False,
                    'server-hostname': 'name-xyz',
                    'shared-network-name': None,
                    'subnet': '192.168.50.0/24',
                    'max-valid-lifetime': 1000,
                    'min-valid-lifetime': 1000,
                    'valid-lifetime': 1000
                }
            ]
        },
        'result': 0,
        'text': 'IPv4 subnet 192.168.50.0/24 found.'
    }


# reservation-mode is integer in db, so we need to check if it's converted correctly
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_set_reservation_mode_all_old(backend):
    _setup_server(backend)
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24",
                                                                     "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "reservation-mode": "all",
                                                                     "pools": [
                                                                         {"pool": "192.168.50.1-192.168.50.100"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-get-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"subnet": "192.168.50.0/24"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    subnet = response["arguments"]["subnets"][0]
    # since 1.9.1:
    assert "reservation-mode" not in subnet
    assert subnet["reservations-global"] is False
    assert subnet["reservations-in-subnet"] is True
    assert subnet["reservations-out-of-pool"] is False


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_set_reservation_mode_all(backend):
    _setup_server(backend)
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24",
                                                                     "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "reservations-global": False,
                                                                     "reservations-in-subnet": True,
                                                                     "reservations-out-of-pool": False,
                                                                     "pools": [
                                                                         {"pool": "192.168.50.1-192.168.50.100"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-get-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"subnet": "192.168.50.0/24"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    subnet = response["arguments"]["subnets"][0]
    # since 1.9.1:
    assert "reservation-mode" not in subnet
    assert subnet["reservations-global"] is False
    assert subnet["reservations-in-subnet"] is True
    assert subnet["reservations-out-of-pool"] is False


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_set_reservation_mode_global_old(backend):
    _setup_server(backend)
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24",
                                                                     "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "reservation-mode": "global",
                                                                     "pools": [
                                                                         {"pool": "192.168.50.1-192.168.50.100"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-get-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"subnet": "192.168.50.0/24"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    subnet = response["arguments"]["subnets"][0]
    # since 1.9.1:
    assert "reservation-mode" not in subnet
    assert subnet["reservations-global"] is True
    assert subnet["reservations-in-subnet"] is False


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_set_reservation_mode_global(backend):
    _setup_server(backend)
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24",
                                                                     "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "reservations-global": True,
                                                                     "reservations-in-subnet": False,
                                                                     "pools": [
                                                                         {"pool": "192.168.50.1-192.168.50.100"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-get-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"subnet": "192.168.50.0/24"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    subnet = response["arguments"]["subnets"][0]
    # since 1.9.1:
    assert "reservation-mode" not in subnet
    assert subnet["reservations-global"] is True
    assert subnet["reservations-in-subnet"] is False


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_set_reservation_mode_out_of_pool_old(backend):
    _setup_server(backend)
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24",
                                                                     "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "reservation-mode": "out-of-pool",
                                                                     "pools": [
                                                                         {"pool": "192.168.50.1-192.168.50.100"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-get-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"subnet": "192.168.50.0/24"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    subnet = response["arguments"]["subnets"][0]
    # since 1.9.1:
    assert "reservation-mode" not in subnet
    assert subnet["reservations-global"] is False
    assert subnet["reservations-in-subnet"] is True
    assert subnet["reservations-out-of-pool"] is True


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_set_reservation_mode_out_of_pool(backend):
    _setup_server(backend)
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24",
                                                                     "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "reservations-global": False,
                                                                     "reservations-in-subnet": True,
                                                                     "reservations-out-of-pool": True,
                                                                     "pools": [
                                                                         {"pool": "192.168.50.1-192.168.50.100"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-get-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"subnet": "192.168.50.0/24"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    subnet = response["arguments"]["subnets"][0]
    # since 1.9.1:
    assert "reservation-mode" not in subnet
    assert subnet["reservations-global"] is False
    assert subnet["reservations-in-subnet"] is True
    assert subnet["reservations-out-of-pool"] is True


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_set_reservation_mode_disabled_old(backend):
    _setup_server(backend)
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24",
                                                                     "id": 1,
                                                                     "shared-network-name": "",
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "reservation-mode": "disabled"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-get-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"subnet": "192.168.50.0/24"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    subnet = response["arguments"]["subnets"][0]
    # since 1.9.1:
    assert "reservation-mode" not in subnet
    assert subnet["reservations-global"] is False
    assert subnet["reservations-in-subnet"] is False


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_set_reservation_mode_disabled(backend):
    _setup_server(backend)
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24",
                                                                     "id": 1,
                                                                     "shared-network-name": "",
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "reservations-global": False,
                                                                     "reservations-in-subnet": False}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-get-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"subnet": "192.168.50.0/24"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    subnet = response["arguments"]["subnets"][0]
    # since 1.9.1:
    assert "reservation-mode" not in subnet
    assert subnet["reservations-global"] is False
    assert subnet["reservations-in-subnet"] is False


def _subnet_set(backend, server_tag=None):
    if server_tag is None:
        server_tag = ["abc"]
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": backend},
                                                        "server-tags": server_tag,
                                                        "subnets": [{"subnet": "192.168.50.0/24", "id": 5,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "192.168.50.1-192.168.50.100"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 5, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_del_by_id(backend):
    _setup_server(backend)
    _subnet_set(backend)

    cmd = dict(command="remote-subnet4-del-by-id", arguments={"remote": {"type": backend},
                                                              "subnets": [{"id": 5}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv4 subnet(s) deleted."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_del_by_id_incorrect_id(backend):
    _setup_server(backend)
    _subnet_set(backend)

    cmd = dict(command="remote-subnet4-del-by-id", arguments={"remote": {"type": backend},
                                                              "subnets": [{"id": 15}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 IPv4 subnet(s) deleted."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_del_id_negative_missing_subnet(backend):
    _setup_server(backend)
    _subnet_set(backend)

    cmd = dict(command="remote-subnet4-del-by-id", arguments={"remote": {"type": backend},
                                                              "subnets": [{"subnet": "192.168.50.0/24"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "missing 'id' parameter"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_del_by_prefix(backend):
    _setup_server(backend)
    _subnet_set(backend)

    cmd = dict(command="remote-subnet4-del-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"subnet": "192.168.50.0/24"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv4 subnet(s) deleted."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_del_by_prefix_non_existing_subnet(backend):
    _setup_server(backend)
    _subnet_set(backend)

    cmd = dict(command="remote-subnet4-del-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"subnet": "192.168.51.0/24"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 IPv4 subnet(s) deleted."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_del_by_prefix_missing_subnet_(backend):
    _setup_server(backend)
    _subnet_set(backend)
    cmd = dict(command="remote-subnet4-del-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"id": 2}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "missing 'subnet' parameter"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_get_by_id(backend):
    _setup_server(backend)
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"4o6-interface": "eth9",
                                                                     "shared-network-name": "",
                                                                     "4o6-interface-id": "interf-id",
                                                                     "require-client-classes": ["XYZ"],
                                                                     "4o6-subnet": "2000::/64",
                                                                     "authoritative": False,
                                                                     "boot-file-name": "file-name",
                                                                     "id": 2, "interface": "$(SERVER_IFACE)",
                                                                     "match-client-id": False, "next-server": "0.0.0.0",
                                                                     "pools": [{"pool": "192.168.50.1-192.168.50.100",
                                                                                "option-data": [{"code": 6,
                                                                                                 "data": '192.0.2.2',
                                                                                                 "always-send": True,
                                                                                                 "csv-format": True}]}],
                                                                     "relay": {"ip-addresses": ["192.168.5.5"]},
                                                                     "reservation-mode": "global",
                                                                     "server-hostname": "name-xyz",
                                                                     "subnet": "192.168.50.0/24",
                                                                     "valid-lifetime": 1000,
                                                                     "rebind-timer": 500,
                                                                     "renew-timer": 200,
                                                                     "option-data": [{"code": 6,
                                                                                      "data": '192.0.2.1',
                                                                                      "always-send": True,
                                                                                      "csv-format": True}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 2, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-get-by-id", arguments={"remote": {"type": backend},
                                                              "subnets": [{"id": 2}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1,
                                      "subnets": [{"4o6-interface": "eth9",
                                                   "metadata": {"server-tags": ["abc"]},
                                                   "shared-network-name": None,
                                                   "4o6-interface-id": "interf-id",
                                                   "require-client-classes": ["XYZ"],
                                                   "4o6-subnet": "2000::/64", "authoritative": False,
                                                   "boot-file-name": "file-name", "id": 2,
                                                   "interface": srv_msg.get_server_interface(),
                                                   "match-client-id": False, "next-server": "0.0.0.0",
                                                   "option-data": [{"always-send": True, "code": 6, "csv-format": True,
                                                                    "data": "192.0.2.1", "name": "domain-name-servers",
                                                                    "space": "dhcp4"}],
                                                   "pools": [{"option-data": [{"always-send": True, "code": 6,
                                                                               "csv-format": True, "data": "192.0.2.2",
                                                                               "name": "domain-name-servers",
                                                                               "space": "dhcp4"}],
                                                              "pool": "192.168.50.1-192.168.50.100"}],
                                                   "rebind-timer": 500,
                                                   "relay": {"ip-addresses": ["192.168.5.5"]}, "renew-timer": 200,
                                                   # "reservation-mode": "global",   # not anymore since 1.9.1
                                                   'reservations-global': True,      # new since 1.9.1
                                                   'reservations-in-subnet': False,  # new since 1.9.1
                                                   "server-hostname": "name-xyz",
                                                   "max-valid-lifetime": 1000,
                                                   "min-valid-lifetime": 1000,
                                                   "subnet": "192.168.50.0/24", "valid-lifetime": 1000}]},
                        "result": 0, "text": "IPv4 subnet 2 found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_get_by_id_incorrect_id(backend):
    _setup_server(backend)
    _subnet_set(backend)

    cmd = dict(command="remote-subnet4-get-by-id", arguments={"remote": {"type": backend},
                                                              "subnets": [{"id": 3}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "subnets": []},
                        "result": 3, "text": "IPv4 subnet 3 not found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_get_by_id_missing_id(backend):
    _setup_server(backend)
    _subnet_set(backend)

    cmd = dict(command="remote-subnet4-get-by-id", arguments={"remote": {"type": backend},
                                                              "subnets": [{"subnet": 3}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1,
                        "text": "missing 'id' parameter"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_get_by_prefix(backend):
    _setup_server(backend)
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"4o6-interface": "eth9",
                                                                     "shared-network-name": "",
                                                                     "4o6-interface-id": "interf-id",
                                                                     "4o6-subnet": "2000::/64",
                                                                     "id": 1,
                                                                     "authoritative": False,
                                                                     "boot-file-name": "file-name",
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "match-client-id": True, "next-server": "0.0.0.0",
                                                                     "pools": [{"pool": "192.168.50.1-192.168.50.100"}],
                                                                     "relay": {"ip-addresses": ["192.168.5.5"]},
                                                                     "reservation-mode": "all",
                                                                     "server-hostname": "name-xyz",
                                                                     "subnet": "192.168.50.0/24",
                                                                     "valid-lifetime": 1000}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-get-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"subnet": "192.168.50.0/24"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {
        "count": 1,
        "subnets": [{
            "4o6-interface": "eth9",
            "4o6-interface-id": "interf-id",
            "4o6-subnet": "2000::/64",
            "authoritative": False,
            "boot-file-name": "file-name",
            "metadata": {"server-tags": ["abc"]},
            "shared-network-name": None,
            "id": 1,
            "interface": srv_msg.get_server_interface(),
            "match-client-id": True,
            "next-server": "0.0.0.0",
            "option-data": [],
            "pools": [{
                "option-data": [],
                "pool": "192.168.50.1-192.168.50.100"}],
            "relay": {
                "ip-addresses": [
                    "192.168.5.5"]},
            # "reservation-mode": "all",  # not anymore since 1.9.1
            'reservations-global': False,       # new since 1.9.1
            'reservations-in-subnet': True,     # new since 1.9.1
            'reservations-out-of-pool': False,  # new since 1.9.1
            "server-hostname": "name-xyz",
            "max-valid-lifetime": 1000,
            "min-valid-lifetime": 1000,
            "subnet": "192.168.50.0/24",
            "valid-lifetime": 1000}]}, "result": 0, "text": "IPv4 subnet 192.168.50.0/24 found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_get_by_prefix_negative(backend):
    _setup_server(backend)
    _subnet_set(backend)

    cmd = dict(command="remote-subnet4-get-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"subnet": "10.0.0.2/12"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "subnets": []},
                        "result": 3, "text": "IPv4 subnet 10.0.0.2/12 not found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_get_by_prefix_incorrect_prefix(backend):
    _setup_server(backend)
    _subnet_set(backend)
    cmd = dict(command="remote-subnet4-get-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"subnet": "10.0.0/12"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1,
                        "text": "unable to parse invalid prefix 10.0.0/12"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_get_by_prefix_missing_prefix(backend):
    _setup_server(backend)
    _subnet_set(backend)

    cmd = dict(command="remote-subnet4-get-by-prefix", arguments={"remote": {"type": backend},
                                                                  "subnets": [{"id": "10.0.0/12"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1,
                        "text": "missing 'subnet' parameter"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet4_list(backend):
    _setup_server(backend)
    _subnet_set(backend)

    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.51.0/24", "id": 3,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "192.168.51.1-192.168.51.100"}]}]})
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.52.0/24", "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "192.168.52.1-192.168.52.100"}]}]})
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command="remote-subnet4-list", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 3, "subnets": [{"id": 1,
                                                               "metadata": {"server-tags": ["abc"]},
                                                               "shared-network-name": None,
                                                               "subnet": "192.168.52.0/24"},
                                                              {"id": 3,
                                                               "metadata": {"server-tags": ["abc"]},
                                                               "shared-network-name": None,
                                                               "subnet": "192.168.51.0/24"},
                                                              {"id": 5,
                                                               "metadata": {"server-tags": ["abc"]},
                                                               "shared-network-name": None,
                                                               "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "3 IPv4 subnet(s) found."}


# network tests
@pytest.mark.parametrize('channel', ['socket', 'http'])
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_network4_set_basic(channel, backend):
    _setup_server(backend)
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{"name": "floor13"}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"shared-networks": [{"name": "floor13"}]},
                        "result": 0, "text": "IPv4 shared network successfully set."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_network4_set_missing_name(backend):
    _setup_server(backend)
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "missing parameter 'name'" in response["text"]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_network4_set_empty_name(backend):
    _setup_server(backend)
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": ""}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "'name' parameter must not be empty"}


@pytest.mark.parametrize('channel', ['socket', 'http'])
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_network4_get_basic(channel, backend):
    _setup_server(backend)
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd, channel=channel)

    cmd = dict(command="remote-network4-get", arguments={"remote": {"type": backend},
                                                         "shared-networks": [{
                                                             "name": "net1"}]})

    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {"arguments": {"count": 1,
                                      "shared-networks": [{"interface": srv_msg.get_server_interface(), "name": "net1",
                                                           "metadata": {"server-tags": ["abc"]},
                                                           "option-data": [], "relay": {"ip-addresses": []}}]},
                        "result": 0, "text": "IPv4 shared network 'net1' found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_network4_get_all_values(backend):
    _setup_server(backend)
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "client-class": "abc",
                                                             "authoritative": False,
                                                             "rebind-timer": 200,
                                                             "renew-timer": 100,
                                                             "calculate-tee-times": True,
                                                             "require-client-classes": ["XYZ"],
                                                             "t1-percent": 0.5,
                                                             "t2-percent": 0.8,
                                                             "valid-lifetime": 300,
                                                             "reservation-mode": "global",
                                                             "match-client-id": True,
                                                             "user-context": {"some weird network": 55},
                                                             "interface": "$(SERVER_IFACE)",
                                                             "option-data": [{"code": 6,
                                                                              "data": '192.0.2.1',
                                                                              "always-send": True,
                                                                              "csv-format": True}]}]})
    srv_msg.send_ctrl_cmd(cmd)
    cmd = dict(command="remote-network4-get", arguments={"remote": {"type": backend},
                                                         "shared-networks": [{
                                                             "name": "net1"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1,
                                      "shared-networks": [{"authoritative": False, "client-class": "abc",
                                                           "rebind-timer": 200, "renew-timer": 100,
                                                           "valid-lifetime": 300,
                                                           "max-valid-lifetime": 300,
                                                           "min-valid-lifetime": 300,
                                                           # "reservation-mode": "global",   # not anymore since 1.9.1
                                                           'reservations-global': True,      # new since 1.9.1
                                                           'reservations-in-subnet': False,  # new since 1.9.1
                                                           "interface": srv_msg.get_server_interface(),
                                                           "metadata": {"server-tags": ["abc"]},
                                                           "require-client-classes": ["XYZ"],
                                                           "calculate-tee-times": True,
                                                           "t1-percent": 0.5,
                                                           "t2-percent": 0.8,
                                                           "match-client-id": True,
                                                           "name": "net1",
                                                           "option-data": [{"always-send": True, "code": 6,
                                                                            "csv-format": True, "data": "192.0.2.1",
                                                                            "name": "domain-name-servers",
                                                                            "space": "dhcp4"}],
                                                           "relay": {"ip-addresses": []},
                                                           "user-context": {"some weird network": 55}}]},
                        "result": 0, "text": "IPv4 shared network 'net1' found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_network4_set_t1_t2(backend):
    _setup_server(backend)
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "calculate-tee-times": True,
                                                             "t1-percent": 0.5,
                                                             "t2-percent": 10,
                                                             "interface": "$(SERVER_IFACE)"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "'t2-percent' parameter is not a real" in response["text"]

    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "calculate-tee-times": True,
                                                             "t1-percent": 10,
                                                             "t2-percent": 0.5,
                                                             "interface": "$(SERVER_IFACE)"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "'t1-percent' parameter is not a real" in response["text"]

    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": backend},
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
def test_remote_network4_list_basic(channel, backend):
    _setup_server(backend)
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd, channel=channel)

    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net2",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd, channel=channel)

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"count": 2, "shared-networks": [{"metadata": {"server-tags": ["abc"]},
                                                                       "name": "net1"},
                                                                      {"metadata": {"server-tags": ["abc"]},
                                                                       "name": "net2"}]},
                        "result": 0,
                        "text": "2 IPv4 shared network(s) found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_network4_list_no_networks(backend):
    _setup_server(backend)
    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0,
                                      "shared-networks": []},
                        "result": 3,
                        "text": "0 IPv4 shared network(s) found."}


@pytest.mark.parametrize('channel', ['socket', 'http'])
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_network4_del_basic(channel, backend):
    _setup_server(backend)
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd, channel=channel)

    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net2",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd, channel=channel)

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"count": 2,
                                      "shared-networks": [{"metadata": {"server-tags": ["abc"]}, "name": "net1"},
                                                          {"metadata": {"server-tags": ["abc"]}, "name": "net2"}]},
                        "result": 0,
                        "text": "2 IPv4 shared network(s) found."}

    cmd = dict(command="remote-network4-del", arguments={"remote": {"type": backend},
                                                         "shared-networks": [{"name": "net1"}]})

    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv4 shared network(s) deleted."}

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"count": 1,
                                      "shared-networks": [{"metadata": {"server-tags": ["abc"]}, "name": "net2"}]},
                        "result": 0, "text": "1 IPv4 shared network(s) found."}

    cmd = dict(command="remote-network4-del", arguments={"remote": {"type": backend},
                                                         "shared-networks": [{"name": "net2"}]})

    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv4 shared network(s) deleted."}

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel, exp_result=3)

    assert response == {"arguments": {"count": 0,
                                      "shared-networks": []},
                        "result": 3,
                        "text": "0 IPv4 shared network(s) found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_network4_del_subnet_keep(backend):
    _setup_server(backend)
    # add networks
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net2",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 2,
                                      "shared-networks": [{"metadata": {"server-tags": ["abc"]},
                                                           "name": "net1"},
                                                          {"metadata": {"server-tags": ["abc"]},
                                                           "name": "net2"}]},
                        "result": 0,
                        "text": "2 IPv4 shared network(s) found."}

    # add subnets to networks
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.8.0.0/24",
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "id": 1,
                                                                     "shared-network-name": "net1",
                                                                     "pools": [
                                                                         {"pool": "192.8.0.1-192.8.0.100"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "192.8.0.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.9.0.0/24",
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "id": 2,
                                                                     "shared-network-name": "net2",
                                                                     "pools": [
                                                                         {"pool": "192.9.0.1-192.9.0.100"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 2, "subnet": "192.9.0.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    # we want to have 2 subnets
    cmd = dict(command="remote-subnet4-list", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 2, "subnets": [{"id": 1, "subnet": "192.8.0.0/24",
                                                               "shared-network-name": "net1",
                                                               "metadata": {"server-tags": ["abc"]}},
                                                              {"id": 2, "subnet": "192.9.0.0/24",
                                                               "shared-network-name": "net2",
                                                               "metadata": {"server-tags": ["abc"]}}]},
                        "result": 0, "text": "2 IPv4 subnet(s) found."}

    cmd = dict(command="remote-network4-del", arguments={"remote": {"type": backend}, "subnets-action": "keep",
                                                         "shared-networks": [{"name": "net1"}]})

    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv4 shared network(s) deleted."}

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1,
                                      "shared-networks": [{"metadata": {"server-tags": ["abc"]}, "name": "net2"}]},
                        "result": 0, "text": "1 IPv4 shared network(s) found."}

    # after deleting network we still want to have 2 subnets
    cmd = dict(command="remote-subnet4-list", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 2,
                                      "subnets": [{"id": 1, "metadata": {"server-tags": ["abc"]},
                                                   "shared-network-name": None, "subnet": "192.8.0.0/24"},
                                                  {"id": 2, "metadata": {"server-tags": ["abc"]},
                                                   "shared-network-name": "net2", "subnet": "192.9.0.0/24"}]},
                        "result": 0, "text": "2 IPv4 subnet(s) found."}

    cmd = dict(command="remote-network4-del", arguments={"remote": {"type": backend}, "subnets-action": "keep",
                                                         "shared-networks": [{"name": "net2"}]})

    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv4 shared network(s) deleted."}

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0,
                                      "shared-networks": []},
                        "result": 3,
                        "text": "0 IPv4 shared network(s) found."}

    # after removing all networks we still want to have both subnets
    cmd = dict(command="remote-subnet4-list", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 2,
                                      "subnets": [{"id": 1, "metadata": {"server-tags": ["abc"]},
                                                   "shared-network-name": None, "subnet": "192.8.0.0/24"},
                                                  {"id": 2, "metadata": {"server-tags": ["abc"]},
                                                   "shared-network-name": None, "subnet": "192.9.0.0/24"}]},
                        "result": 0, "text": "2 IPv4 subnet(s) found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_network4_del_subnet_delete_simple(backend):
    _setup_server(backend)
    # for ticket #738
    cmd = dict(command='remote-network4-set', arguments={
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

    cmd = dict(command='remote-subnet4-set', arguments={
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
                        'pool': '192.8.0.1-192.8.0.100'
                    }
                ],
                'shared-network-name': 'net1',
                'subnet': '192.8.0.0/24'
            }
        ]
    })
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command='remote-network4-del', arguments={
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
def test_remote_network4_del_subnet_delete(backend):
    _setup_server(backend)
    # add networks
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net2",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 2,
                                      "shared-networks": [{"metadata": {"server-tags": ["abc"]},
                                                           "name": "net1"},
                                                          {"metadata": {"server-tags": ["abc"]},
                                                           "name": "net2"}]},
                        "result": 0,
                        "text": "2 IPv4 shared network(s) found."}

    # add subnets to networks
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.8.0.0/24",
                                                                     "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "net1",
                                                                     "pools": [
                                                                         {"pool": "192.8.0.1-192.8.0.100"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "192.8.0.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.9.0.0/24",
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "id": 2,
                                                                     "shared-network-name": "net2",
                                                                     "pools": [
                                                                         {"pool": "192.9.0.1-192.9.0.100"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 2, "subnet": "192.9.0.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    # we want to have 2 subnets
    cmd = dict(command="remote-subnet4-list", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 2, "subnets": [{"id": 1, "subnet": "192.8.0.0/24",
                                                               "shared-network-name": "net1",
                                                               "metadata": {"server-tags": ["abc"]}},
                                                              {"id": 2, "subnet": "192.9.0.0/24",
                                                               "shared-network-name": "net2",
                                                               "metadata": {"server-tags": ["abc"]}}]},
                        "result": 0, "text": "2 IPv4 subnet(s) found."}

    cmd = dict(command="remote-network4-del", arguments={"remote": {"type": backend}, "subnets-action": "delete",
                                                         "shared-networks": [{"name": "net1"}]})

    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv4 shared network(s) deleted."}

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1,
                                      "shared-networks": [{"metadata": {"server-tags": ["abc"]}, "name": "net2"}]},
                        "result": 0, "text": "1 IPv4 shared network(s) found."}

    # after deleting network we still want to have 2 subnets
    cmd = dict(command="remote-subnet4-list", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1,
                                      "subnets": [{"id": 2, "metadata": {"server-tags": ["abc"]},
                                                   "shared-network-name": "net2", "subnet": "192.9.0.0/24"}]},
                        "result": 0, "text": "1 IPv4 subnet(s) found."}

    cmd = dict(command="remote-network4-del", arguments={"remote": {"type": backend}, "subnets-action": "delete",
                                                         "shared-networks": [{"name": "net2"}]})

    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv4 shared network(s) deleted."}

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0,
                                      "shared-networks": []},
                        "result": 3,
                        "text": "0 IPv4 shared network(s) found."}

    # all subnets should be removed now
    cmd = dict(command="remote-subnet4-list", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "subnets": []},
                        "result": 3, "text": "0 IPv4 subnet(s) found."}


def _set_global_parameter(backend):
    cmd = dict(command="remote-global-parameter4-set", arguments={"remote": {"type": backend},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": {
                                                                      "boot-file-name": "/dev/null"}})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1, "parameters": {"boot-file-name": "/dev/null"}},
                        "result": 0,
                        "text": "1 DHCPv4 global parameter(s) successfully set."}


# global-parameter tests
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_parameter4_set_text(backend):
    _setup_server(backend)
    _set_global_parameter(backend)


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_parameter4_set_integer(backend):
    _setup_server(backend)
    cmd = dict(command="remote-global-parameter4-set", arguments={"remote": {"type": backend},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": {"valid-lifetime": 1000}})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1, "parameters": {"valid-lifetime": 1000}},
                        "result": 0,
                        "text": "1 DHCPv4 global parameter(s) successfully set."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_parameter4_set_incorrect_parameter(backend):
    _setup_server(backend)
    cmd = dict(command="remote-global-parameter4-set", arguments={"remote": {"type": backend},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": {"boot-fiabcsd": "/dev/null"}})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "unknown parameter 'boot-fiabcsd'"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_parameter4_del(backend):
    _setup_server(backend)
    _set_global_parameter(backend)

    cmd = dict(command="remote-global-parameter4-del", arguments={"remote": {"type": backend},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": ["boot-file-name"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1},
                        "result": 0, "text": "1 DHCPv4 global parameter(s) deleted."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_parameter4_del_not_existing_parameter(backend):
    _setup_server(backend)
    cmd = dict(command="remote-global-parameter4-del", arguments={"remote": {"type": backend},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": ["boot-file-name"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0},
                        "result": 3, "text": "0 DHCPv4 global parameter(s) deleted."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_parameter4_get(backend):
    _setup_server(backend)
    _set_global_parameter(backend)

    cmd = dict(command="remote-global-parameter4-get", arguments={"remote": {"type": backend},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": ["boot-file-name"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1,
                                      "parameters": {"boot-file-name": "/dev/null",
                                                     "metadata": {"server-tags": ["abc"]}}},
                        "result": 0, "text": "'boot-file-name' DHCPv4 global parameter found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_parameter4_get_all_one(backend):
    _setup_server(backend)
    _set_global_parameter(backend)

    cmd = dict(command="remote-global-parameter4-get-all", arguments={"remote": {"type": backend},
                                                                      "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1, "parameters": [{"boot-file-name": "/dev/null",
                                                                  "metadata": {"server-tags": ["abc"]}}]},
                        "result": 0, "text": "1 DHCPv4 global parameter(s) found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_parameter4_get_all_multiple(backend):
    _setup_server(backend)
    _set_global_parameter(backend)

    cmd = dict(command="remote-global-parameter4-set", arguments={"remote": {"type": backend},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": {"decline-probation-period": 15}})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1, "parameters": {"decline-probation-period": 15}}, "result": 0,
                        "text": "1 DHCPv4 global parameter(s) successfully set."}

    cmd = dict(command="remote-global-parameter4-get-all", arguments={"remote": {"type": backend},
                                                                      "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response["arguments"]["count"] == 2
    assert response["text"] == "2 DHCPv4 global parameter(s) found."
    assert {"boot-file-name": "/dev/null", "metadata": {"server-tags": ["abc"]}} in response["arguments"]["parameters"]
    assert {"decline-probation-period": 15, "metadata": {"server-tags": ["abc"]}} in response["arguments"]["parameters"]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_parameter4_get_all_zero(backend):
    _setup_server(backend)
    cmd = dict(command="remote-global-parameter4-get-all", arguments={"remote": {"type": backend},
                                                                      "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "parameters": []},
                        "result": 3, "text": "0 DHCPv4 global parameter(s) found."}


def _set_option_def(backend, channel='http'):
    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": backend},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 222,
                                                                "type": "uint32"}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"option-defs": [{"code": 222, "space": "dhcp4"}]},
                        "result": 0, "text": "DHCPv4 option definition successfully set."}


@pytest.mark.parametrize('channel', ['socket', 'http'])
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def4_set_basic(channel, backend):
    _setup_server(backend)
    _set_option_def(backend, channel=channel)


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def4_set_using_zero_as_code(backend):
    _setup_server(backend)
    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": backend},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 0,
                                                                "type": "uint32"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "invalid option code '0': reserved for PAD" in response["text"]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def4_set_using_standard_code(backend):
    _setup_server(backend)
    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": backend},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 24,
                                                                "type": "uint32"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "an option with code 24 already exists in space 'dhcp4'"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def4_set_missing_parameters(backend):
    _setup_server(backend)
    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": backend},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "code": 222,
                                                                "type": "uint32",
                                                                "array": False,
                                                                "record-types": "",
                                                                "space": "dhcp4",
                                                                "encapsulate": ""}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "missing parameter 'name'" in response["text"]

    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": backend},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "aa",
                                                                "type": "uint32",
                                                                "array": False,
                                                                "record-types": "",
                                                                "space": "dhcp4",
                                                                "encapsulate": ""}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "missing parameter 'code'" in response["text"]

    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": backend},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "aa",
                                                                "code": 234,
                                                                "array": False,
                                                                "record-types": "",
                                                                "space": "dhcp4",
                                                                "encapsulate": ""}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "missing parameter 'type'" in response["text"]


@pytest.mark.parametrize('channel', ['socket', 'http'])
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def4_get_basic(channel, backend):
    _setup_server(backend)
    _set_option_def(backend)

    cmd = dict(command="remote-option-def4-get", arguments={"remote": {"type": backend},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "code": 222}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {"arguments": {"count": 1, "option-defs": [{"array": False, "code": 222, "encapsulate": "",
                                                                   "name": "foo", "record-types": "", "space": "dhcp4",
                                                                   "metadata": {"server-tags": ["abc"]},
                                                                   "type": "uint32"}]},
                        "result": 0, "text": "DHCPv4 option definition 222 in 'dhcp4' found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def4_get_multiple_defs(backend):
    _setup_server(backend)
    _set_option_def(backend)

    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": backend},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 222,
                                                                "type": "uint32",
                                                                "space": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"option-defs": [{"code": 222, "space": "abc"}]},
                        "result": 0, "text": "DHCPv4 option definition successfully set."}

    cmd = dict(command="remote-option-def4-get", arguments={"remote": {"type": backend},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "code": 222,
                                                                "space": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1, "option-defs": [{"array": False, "code": 222, "encapsulate": "",
                                                                   "name": "foo", "record-types": "", "space": "abc",
                                                                   "metadata": {"server-tags": ["abc"]},
                                                                   "type": "uint32"}]},
                        "result": 0, "text": "DHCPv4 option definition 222 in 'abc' found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def4_get_missing_code(backend):
    _setup_server(backend)
    cmd = dict(command="remote-option-def4-get", arguments={"remote": {"type": backend},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "missing 'code' parameter"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def4_get_all_option_not_defined(backend):
    _setup_server(backend)
    cmd = dict(command="remote-option-def4-get-all", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "option-defs": []},
                        "result": 3, "text": "0 DHCPv4 option definition(s) found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def4_get_all_multiple_defs(backend):
    _setup_server(backend)
    _set_option_def(backend)

    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": backend},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 222,
                                                                "type": "uint32",
                                                                "space": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"option-defs": [{"code": 222, "space": "abc"}]},
                        "result": 0, "text": "DHCPv4 option definition successfully set."}

    cmd = dict(command="remote-option-def4-get-all", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 2, "option-defs": [{"array": False, "code": 222,
                                                                   "encapsulate": "", "name": "foo",
                                                                   "record-types": "", "space": "abc",
                                                                   "metadata": {"server-tags": ["abc"]},
                                                                   "type": "uint32"},
                                                                  {"array": False, "code": 222,
                                                                   "encapsulate": "", "name": "foo",
                                                                   "record-types": "", "space": "dhcp4",
                                                                   "metadata": {"server-tags": ["abc"]},
                                                                   "type": "uint32"}]},
                        "result": 0, "text": "2 DHCPv4 option definition(s) found."}


@pytest.mark.parametrize('channel', ['socket', 'http'])
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def4_get_all_basic(channel, backend):
    _setup_server(backend)
    _set_option_def(backend)

    cmd = dict(command="remote-option-def4-get-all", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {"arguments": {"count": 1, "option-defs": [{"array": False, "code": 222, "encapsulate": "",
                                                                   "metadata": {"server-tags": ["abc"]},
                                                                   "name": "foo", "record-types": "", "space": "dhcp4",
                                                                   "type": "uint32"}]},
                        "result": 0, "text": "1 DHCPv4 option definition(s) found."}


@pytest.mark.parametrize('channel', ['socket', 'http'])
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def4_del_basic(channel, backend):
    _setup_server(backend)
    _set_option_def(backend)

    cmd = dict(command="remote-option-def4-del", arguments={"remote": {"type": backend}, "server-tags": ["abc"],
                                                            "option-defs": [{"code": 222}]})

    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv4 option definition(s) deleted."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def4_del_different_space(backend):
    _setup_server(backend)
    _set_option_def(backend)

    cmd = dict(command="remote-option-def4-del", arguments={"remote": {"type": backend}, "server-tags": ["abc"],
                                                            "option-defs": [{"code": 222, "space": "abc"}]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 DHCPv4 option definition(s) deleted."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def4_del_incorrect_code(backend):
    _setup_server(backend)
    cmd = dict(command="remote-option-def4-del", arguments={"remote": {"type": backend}, "server-tags": ["abc"],
                                                            "option-defs": [{"name": 22}]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "missing 'code' parameter"}

    cmd = dict(command="remote-option-def4-del", arguments={"remote": {"type": backend}, "server-tags": ["abc"],
                                                            "option-defs": [{}]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "missing 'code' parameter"}

    cmd = dict(command="remote-option-def4-del", arguments={"remote": {"type": backend}, "server-tags": ["abc"],
                                                            "option-defs": [{"code": "abc"}]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "'code' parameter is not an integer"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def4_del_missing_option(backend):
    _setup_server(backend)
    cmd = dict(command="remote-option-def4-del", arguments={"remote": {"type": backend}, "server-tags": ["abc"],
                                                            "option-defs": [{"code": 212}]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 DHCPv4 option definition(s) deleted."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def4_del_multiple_options(backend):
    _setup_server(backend)
    _set_option_def(backend)

    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": backend},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 222,
                                                                "type": "uint32",
                                                                "space": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"option-defs": [{"code": 222, "space": "abc"}]},
                        "result": 0, "text": "DHCPv4 option definition successfully set."}

    cmd = dict(command="remote-option-def4-del", arguments={"remote": {"type": backend}, "server-tags": ["abc"],
                                                            "option-defs": [{"code": 222}]})

    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv4 option definition(s) deleted."}

    cmd = dict(command="remote-option-def4-get-all", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1, "option-defs": [{"array": False, "code": 222, "encapsulate": "",
                                                                   "metadata": {"server-tags": ["abc"]},
                                                                   "name": "foo", "record-types": "", "space": "abc",
                                                                   "type": "uint32"}]},
                        "result": 0, "text": "1 DHCPv4 option definition(s) found."}


def _set_global_option(backend):
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "code": 6,
                                                                   "data": "192.0.2.1, 192.0.2.2"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"result": 0, "text": "DHCPv4 option successfully set.",
                        "arguments": {"options": [{"code": 6, "space": "dhcp4"}]}}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option4_global_set_basic(backend):
    _setup_server(backend)
    _set_global_option(backend)


@pytest.mark.parametrize('channel', ['socket', 'http'])
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option4_global_set_missing_data(channel, backend):
    _setup_server(backend)
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "code": 6}]})
    srv_msg.send_ctrl_cmd(cmd, channel=channel)


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option4_global_set_name(backend):
    _setup_server(backend)
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "name": "host-name",
                                                                   "data": "isc.example.com"}]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"options": [{"code": 12, "space": "dhcp4"}]},
                        "result": 0, "text": "DHCPv4 option successfully set."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option4_global_set_incorrect_code_missing_name(backend):
    _setup_server(backend)
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "code": "aaa"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "'code' parameter is not an integer" in response["text"]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option4_global_set_incorrect_name_missing_code(backend):
    _setup_server(backend)
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "name": 123}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "'name' parameter is not a string" in response["text"]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option4_global_set_missing_code_and_name(backend):
    _setup_server(backend)
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "option data configuration requires one of " \
           "'code' or 'name' parameters to be specified" in response["text"]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option4_global_set_incorrect_code(backend):
    _setup_server(backend)
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": "aa",
                                                                            "name": "cc"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "'code' parameter is not an integer" in response["text"]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option4_global_set_incorrect_name(backend):
    _setup_server(backend)
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 12,
                                                                            "name": 12,
                                                                            "data": 'isc.example.com'}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "'name' parameter is not a string" in response["text"]


@pytest.mark.parametrize('channel', ['socket', 'http'])
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option4_global_get_basic(channel, backend):
    _setup_server(backend)
    _set_global_option(backend)

    cmd = dict(command="remote-option4-global-get", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {"arguments": {"count": 1, "options": [{"always-send": False, "code": 6, "csv-format": True,
                                                               "data": "192.0.2.1, 192.0.2.2",
                                                               "metadata": {"server-tags": ["abc"]},
                                                               "name": "domain-name-servers", "space": "dhcp4"}]},
                        "result": 0, "text": "DHCPv4 option 6 in 'dhcp4' found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option4_global_set_different_space(backend):
    _setup_server(backend)
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6,
                                                                            "data": '192.0.2.1, 192.0.2.2',
                                                                            "always-send": True,
                                                                            "csv-format": True,
                                                                            "space": "xyz"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "definition for the option 'xyz.' having code '6' does not exist" in response["text"]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option4_global_set_csv_false_incorrect(backend):
    _setup_server(backend)
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6,
                                                                            "data": '192.0.2.1',
                                                                            "always-send": True,
                                                                            "csv-format": False}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "option data is not a valid string of hexadecimal digits: 192.0.2.1" in response["text"]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option4_global_set_csv_false_correct(backend):
    _setup_server(backend)
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6,
                                                                            "data": "C0000201",  # 192.0.2.1
                                                                            "always-send": True,
                                                                            "csv-format": False}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"result": 0, "text": "DHCPv4 option successfully set.",
                        "arguments": {"options": [{"code": 6, "space": "dhcp4"}]}}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option4_global_set_csv_false_incorrect_hex(backend):
    _setup_server(backend)
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6,
                                                                            "data": "C0000201Z",
                                                                            "always-send": True,
                                                                            "csv-format": False}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "option data is not a valid string of hexadecimal digits: C0000201Z" in response["text"]


@pytest.mark.parametrize('channel', ['socket', 'http'])
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option4_global_del_basic(channel, backend):
    _setup_server(backend)
    _set_global_option(backend)

    cmd = dict(command="remote-option4-global-del", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv4 option(s) deleted."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option4_global_del_missing_code(backend):
    _setup_server(backend)
    cmd = dict(command="remote-option4-global-del", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"ab": 6}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "missing 'code' parameter"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option4_global_del_incorrect_code(backend):
    _setup_server(backend)
    cmd = dict(command="remote-option4-global-del", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": "6"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "'code' parameter is not an integer"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option4_global_del_missing_option(backend):
    _setup_server(backend)
    cmd = dict(command="remote-option4-global-del", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 DHCPv4 option(s) deleted."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option4_global_get_missing_code(backend):
    _setup_server(backend)
    cmd = dict(command="remote-option4-global-get", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"ab": 6}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "missing 'code' parameter"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option4_global_get_incorrect_code(backend):
    _setup_server(backend)
    cmd = dict(command="remote-option4-global-get", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": "6"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "'code' parameter is not an integer"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option4_global_get_missing_option(backend):
    _setup_server(backend)
    cmd = dict(command="remote-option4-global-get", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert response == {"arguments": {"count": 0, "options": []},
                        "result": 3, "text": "DHCPv4 option 6 in 'dhcp4' not found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option4_global_get_csv_false(backend):
    _setup_server(backend)
    cmd = dict(command="remote-option4-global-set",
               arguments={"remote": {"type": backend},
                          "server-tags": ["abc"],
                          "options": [{"code": 6,
                                       "data": "C0000301C0000302",
                                       "always-send": True,
                                       "csv-format": False}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"result": 0, "text": "DHCPv4 option successfully set.",
                        "arguments": {"options": [{"code": 6, "space": "dhcp4"}]}}

    cmd = dict(command="remote-option4-global-get",
               arguments={"remote": {"type": backend},
                          "server-tags": ["abc"],
                          "options": [{"code": 6}]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1, "options": [{"always-send": True, "code": 6, "csv-format": False,
                                                               "data": "C0000301C0000302",
                                                               "metadata": {"server-tags": ["abc"]},
                                                               "name": "domain-name-servers", "space": "dhcp4"}]},
                        "result": 0, "text": "DHCPv4 option 6 in 'dhcp4' found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_option4_global_get_all(backend):
    _setup_server(backend)
    _set_global_option(backend)

    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "code": 16,
                                                                   "data": "199.199.199.1"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"result": 0, "text": "DHCPv4 option successfully set.",
                        "arguments": {"options": [{"code": 16, "space": "dhcp4"}]}}

    cmd = dict(command="remote-option4-global-get-all", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 2,
                                      "options": [{"always-send": False, "code": 6, "csv-format": True,
                                                   "metadata": {"server-tags": ["abc"]},
                                                   "data": "192.0.2.1, 192.0.2.2", "name": "domain-name-servers",
                                                   "space": "dhcp4"},
                                                  {"always-send": False, "code": 16, "csv-format": True,
                                                   "metadata": {"server-tags": ["abc"]},
                                                   "data": "199.199.199.1", "name": "swap-server", "space": "dhcp4"}]},
                        "result": 0, "text": "2 DHCPv4 option(s) found."}

    cmd = dict(command="remote-option4-global-del", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6}]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv4 option(s) deleted."}

    cmd = dict(command="remote-option4-global-get-all", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1, "options": [{"always-send": False, "code": 16, "csv-format": True,
                                                               "data": "199.199.199.1", "name": "swap-server",
                                                               "metadata": {"server-tags": ["abc"]},
                                                               "space": "dhcp4"}]},
                        "result": 0, "text": "1 DHCPv4 option(s) found."}

    cmd = dict(command="remote-option4-global-del", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 16}]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv4 option(s) deleted."}

    cmd = dict(command="remote-option4-global-get-all", arguments={"remote": {"type": backend}, "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert response == {"arguments": {"count": 0, "options": []}, "result": 3, "text": "0 DHCPv4 option(s) found."}


def _set_class(backend, args=None, res=0, resp_text=None, tag='abc'):
    if args is None:
        args = {"client-classes": [{"name": "foo",
                                    "test": "member('KNOWN')"}]}
    if resp_text is None:
        resp_text = "DHCP%s client class successfully set." % world.proto
    resp_text = resp_text.replace("vX", world.proto)

    cmd = dict(command="remote-class%s-set" % world.proto[-1], arguments=args)
    response = _send_cmd(cmd, backend=backend, tag=tag, exp_result=res)

    if res == 1:
        assert response == {"result": 1, "text": resp_text}
    else:
        cls_name = args["client-classes"][0]["name"]
        assert response == {"result": 0, "text": resp_text, "arguments": {"client-classes": [{"name": cls_name}]}}


def _del_class(backend, args=None, res=0, resp_text=None, tag=None, count=1):
    if args is None:
        args = {"client-classes": [{"name": "foo"}]}
    if resp_text is None:
        resp_text = "1 DHCP%s client class(es) deleted." % world.proto
    resp_text = resp_text.replace("vX", world.proto)

    cmd = dict(command="remote-class%s-del" % world.proto[-1], arguments=args)
    response = _send_cmd(cmd, backend=backend, tag=tag, exp_result=res)
    if res == 1:
        assert response == {"result": res, "text": resp_text}
    else:
        assert response == {"result": res, "text": resp_text, "arguments": {"count": count}}


def _get_class(backend, args=None, args_rec=None, res=0, resp_text=None, tag=None):
    if args is None:
        args = {"client-classes": [{"name": "foo"}]}
    if resp_text is None:
        resp_text = "DHCP%s client class 'foo' found." % world.proto
    resp_text = resp_text.replace("vX", world.proto)
    if args_rec is None:
        args_rec = {
            "client-classes": [
                {"boot-file-name": "",
                 "metadata": {"server-tags": ["abc"]},
                 "name": "foo",
                 "next-server": "0.0.0.0",
                 "option-data": [],
                 "option-def": [],
                 "server-hostname": "", "test": "member('KNOWN')",
                 "valid-lifetime": 0}],
            "count": 1}
        if world.proto == 'v6':
            # in v6 we save a bit different data
            del args_rec["client-classes"][0]["next-server"]
            del args_rec["client-classes"][0]["boot-file-name"]
            del args_rec["client-classes"][0]["server-hostname"]
            del args_rec["client-classes"][0]["option-def"]
            args_rec["client-classes"][0].update({'preferred-lifetime': 0})

    cmd = dict(command="remote-class%s-get" % world.proto[-1], arguments=args)
    response = _send_cmd(cmd, backend=backend, tag=tag, exp_result=res)
    if res == 1:
        assert response == {"result": res, "text": resp_text}
    else:
        # resp_text
        assert response == {"result": res, "text": resp_text.replace("foo", args["client-classes"][0]["name"]),
                            "arguments": args_rec}


def _get_all_class(backend, args=None, args_rec=None, res=0, resp_text=None, tag=None):
    resp_text = resp_text.replace("vX", world.proto)
    cmd = dict(command="remote-class%s-get-all" % world.proto[-1], arguments=args)
    response = _send_cmd(cmd, backend=backend, tag=tag, exp_result=res)
    if res == 1:
        assert response == {"result": res, "text": resp_text}
    else:
        assert response == {"result": res, "text": resp_text, "arguments": args_rec}


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_class_set(dhcp_version, backend):  # pylint: disable=unused-argument
    _setup_server(backend)
    # I think there is too many test cases in this single test, but splitting them to separate test will result
    # in much longer testing time, and we should start saving time
    # let's start with default
    _set_class(backend)
    # just name
    _set_class(backend, {"client-classes": [{"name": "aaa"}]})
    # empty class should fail
    _set_class(backend, args={"client-classes": [{}]}, res=1, resp_text="missing parameter 'name' (<wire>:0:38)")
    # empty class list should fail
    _set_class(backend, args={"client-classes": []}, res=1,
               resp_text="'client-classes' list must include exactly one element")
    # multiple classes, also should fail
    _set_class(backend, args={"client-classes": [{"name": "aaa"}, {"name": "xyz"}]}, res=1,
               resp_text="'client-classes' list must include exactly one element")
    # the same class twice, should fail
    _set_class(backend, args={"client-classes": [{"name": "aaa"}, {"name": "aaa"}]}, res=1,
               resp_text="'client-classes' list must include exactly one element")
    # client-classes not list
    _set_class(backend, args={"client-classes": {"name": "aaa"}}, res=1,
               resp_text="'client-classes' parameter must be specified and must be a list")
    # client-classes missing
    _set_class(backend, args={}, res=1, resp_text="'client-classes' parameter must be specified and must be a list")
    # send without server tag
    _set_class(backend, args={"client-classes": [{"name": "something"}]}, res=1,
               resp_text="'server-tags' parameter is mandatory", tag=None)

    # option-def is only supported by v4
    # set class with custom option with code that is not defined
    arg = {"client-classes": [{"name": "my_weird_name",
                               "test": "member('KNOWN')",
                               "option-data": [{"name": "configfile123", "data": "1APC"}]}]}
    _set_class(backend, arg, res=1, resp_text="definition for the option 'dhcp%s.configfile123'"
                                              " does not exist (<wire>:0:107)" % world.proto[-1])
    # set class with custom option with name that is not defined, but it will be accepted as hex
    arg = {"client-classes": [{"name": "my_weird_name",
                               "test": "member('KNOWN')",
                               "option-data": [{"code": 222, "data": "123"}]}]}
    _set_class(backend, arg)
    # set class with custom option that is already defined in the database
    cmd = dict(command="remote-option-def%s-set" % world.proto[-1],
               arguments={"remote": {"type": backend},
                          "server-tags": ["abc"],
                          "option-defs": [{"name": "foo", "code": 222, "type": "uint32"}]})
    srv_msg.send_ctrl_cmd(cmd)
    # this will give us option 222/foo with uint32 value
    _set_class(backend, {"client-classes": [{"name": "my_weird_name", "option-data": [{"code": 222, "data": "123"}]}]})
    _set_class(backend, {"client-classes": [{"name": "my_weird_name_2",
                                             "option-data": [{"name": "foo", "data": "123"}]}]})
    # set class that is relaying on different already configured
    _set_class(backend, {"client-classes": [{"name": "next_pointless_class", "test": "member('aaa')"}]})
    # set class that is relaying on different not configured class
    _set_class(backend, {"client-classes": [{"name": "next_pointless_class_3", "test": "member('not_existing_name')"}]},
               res=1, resp_text="unmet dependency on client class: not_existing_name")


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.disabled
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_class_set_non_existing_params(dhcp_version, backend):  # pylint: disable=unused-argument
    _setup_server(backend)
    # add to many, not allowed parameters
    # it might and up disabled
    # bug, don't know what error should be here
    # https://gitlab.isc.org/isc-projects/kea/-/issues/290
    _set_class(backend, {"client-classes": [{"name": "aaa", "something": [{"more": 123}]}]}, res=1)


@pytest.mark.v4
@pytest.mark.v6
def remote_class_set_all_parameters(dhcp_version, backend):
    _setup_server(backend)
    # let's first set simple class
    _set_class(backend, {"client-classes": [{"name": "foo"}]})
    # and now we will overwrite this with another one, with all parameters
    send_arg = {"client-classes": [{"name": "foo",
                                    "only-if-required": True,
                                    "option-data": [{"code": 7, "data": "123", "always-send": True}],
                                    "test": "member('UNKNOWN')",
                                    "min-valid-lifetime": 100,
                                    "max-valid-lifetime": 1200,
                                    "max-preferred-lifetime": 900,
                                    "min-preferred-lifetime": 789,
                                    "valid-lifetime": 1000,
                                    "preferred-lifetime": 850}]}
    receive_arg = {"client-classes": [{"metadata": {"server-tags": ["abc"]},
                                       "name": "foo",
                                       "only-if-required": True,
                                       "option-data": [{"always-send": True, "code": 7, "csv-format": True,
                                                        "data": "123", "name": "preference", "space": "dhcp6"}],
                                       "test": "member('UNKNOWN')",
                                       "valid-lifetime": 1000,
                                       "min-valid-lifetime": 100,
                                       "max-valid-lifetime": 1200,
                                       "max-preferred-lifetime": 900,
                                       "min-preferred-lifetime": 789,
                                       "preferred-lifetime": 850}],
                   "count": 1}
    if dhcp_version == 'v4':
        send_arg = {"client-classes": [{"boot-file-name": "/var/something",
                                        "name": "foo",
                                        "only-if-required": True,
                                        "next-server": "10.11.12.13",
                                        "option-data": [{"code": 6, "data": "192.0.2.1, 192.0.2.2",
                                                         "always-send": True, "csv-format": True},
                                                        {"name": "foooption", "data": "22"}],
                                        "option-def": [{"array": False, "code": 222, "encapsulate": "",
                                                        "name": "foooption", "record-types": "", "space": "myspace",
                                                        "type": "uint32"}],
                                        "server-hostname": "abc.com",
                                        "min-valid-lifetime": 100,
                                        "max-valid-lifetime": 1200,
                                        "test": "member('UNKNOWN')",
                                        "valid-lifetime": 1000}]}
        receive_arg = {"client-classes": [{"boot-file-name": "/var/something",
                                           "metadata": {"server-tags": ["abc"]},
                                           "name": "foo",
                                           "only-if-required": True,
                                           "next-server": "10.11.12.13",
                                           "option-data": [{"always-send": True, "code": 6, "csv-format": True,
                                                            "data": "192.0.2.1, 192.0.2.2",
                                                            "name": "domain-name-servers", "space": "dhcp4"},
                                                           {"always-send": True, "code": 222, "csv-format": True,
                                                            "data": "22", "name": "foooption", "space": "myspace"}],
                                           "option-def": [{"array": False, "code": 222, "encapsulate": "",
                                                           "name": "foooption", "record-types": "",
                                                           "space": "myspace", "type": "uint32"}],
                                           "server-hostname": "abc.com",
                                           "min-valid-lifetime": 100,
                                           "max-valid-lifetime": 1200,
                                           "test": "member('UNKNOWN')",
                                           "valid-lifetime": 1000}],
                       "count": 1}
    _set_class(backend, send_arg)
    _get_class(backend=backend, args_rec=receive_arg)
    # and now again set simple class with the same name and check if this was overwritten correctly
    _set_class(backend)
    # get existing class
    _get_class(backend=backend)


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_class_del(dhcp_version, backend):  # pylint: disable=unused-argument
    _setup_server(backend)
    _set_class(backend)
    _set_class(backend, {"client-classes": [{"name": "bar"}]})
    # remove existing class
    _del_class(backend)
    # try to remove non existing class
    _del_class(backend, res=3, resp_text="0 DHCPvX client class(es) deleted.", count=0)
    # let's add once again class
    _set_class(backend)
    # empty class list
    _del_class(backend, {"client-classes": []}, res=1,
               resp_text="'client-classes' list must include exactly one element")
    # empty class in the list
    _del_class(backend, {"client-classes": [{}]}, res=1,
               resp_text="missing 'name' parameter")
    # try to remove multiple classes
    _del_class(backend, {"client-classes": [{"name": "foo"}, {"name": "bar"}]}, res=1,
               resp_text="'client-classes' list must include exactly one element")
    # try to remove one class twice
    _del_class(backend, {"client-classes": [{"name": "foo"}, {"name": "foo"}]}, res=1,
               resp_text="'client-classes' list must include exactly one element")
    # client-classes empty
    _del_class(backend, args={"client-classes": []}, res=1,
               resp_text="'client-classes' list must include exactly one element")
    # client-classes missing
    _del_class(backend, args={}, res=1, resp_text="'client-classes' parameter must be specified and must be a list")
    # try to remove existing class but with different server tag, should fail
    _del_class(backend, {"client-classes": [{"name": "foo"}]}, res=1, tag='abc',
               resp_text="'server-tags' parameter is forbidden")


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_class_get(dhcp_version, backend):  # pylint: disable=unused-argument
    _setup_server(backend)
    _set_class(backend)
    # get existing class
    _get_class(backend=backend)
    # delete existing class
    _del_class(backend)
    # get non existing class
    _get_class(backend=backend, res=3, resp_text="DHCPvX client class 'foo' not found.",
               args_rec={"client-classes": [], "count": 0})
    # empty class list
    _get_class(backend=backend, args={"client-classes": []}, res=1,
               resp_text="'client-classes' list must include exactly one element")
    # empty class in the list
    _get_class(backend=backend, args={"client-classes": [{}]}, res=1,
               resp_text="missing 'name' parameter")
    # try to get multiple classes
    _get_class(backend=backend, args={"client-classes": [{"name": "foo"}, {"name": "bar"}]}, res=1,
               resp_text="'client-classes' list must include exactly one element")
    # try to get the same classes twice
    _get_class(backend=backend, args={"client-classes": [{"name": "foo"}, {"name": "foo"}]}, res=1,
               resp_text="'client-classes' list must include exactly one element")
    # try to get exiting class with tag
    _get_class(backend=backend, args={"client-classes": [{"name": "foo"}]}, res=1, tag='abc',
               resp_text="'server-tags' parameter is forbidden")


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_class4_get_all(dhcp_version, backend):
    _setup_server(backend)
    # non existing tag
    _get_all_class(backend=backend, args={"server-tags": ["some-name-that-do-not-exist"]},
                   resp_text="0 DHCPvX client class(es) found.",
                   args_rec={"client-classes": [], "count": 0}, res=3)
    # check existing tag but no classes defined:
    _get_all_class(backend=backend, args={"server-tags": ["abc"]}, resp_text="0 DHCPvX client class(es) found.",
                   args_rec={"client-classes": [], "count": 0}, res=3)

    _set_server_tag(backend, "xyz")
    # set class, get just one
    _set_class(backend)
    args_rec = {"client-classes": [{"boot-file-name": "",
                                    "metadata": {"server-tags": ["abc"]},
                                    "name": "foo",
                                    "next-server": "0.0.0.0",
                                    "option-data": [],
                                    "option-def": [],
                                    "server-hostname": "",
                                    "test": "member('KNOWN')",
                                    "valid-lifetime": 0}],
                "count": 1}

    if dhcp_version == 'v6':
        args_rec = {"client-classes": [{"metadata": {"server-tags": ["abc"]},
                                        "name": "foo",
                                        "option-data": [],
                                        "preferred-lifetime": 0,
                                        "test": "member('KNOWN')",
                                        "valid-lifetime": 0}],
                    "count": 1}

    _get_all_class(backend=backend, args={"server-tags": ["abc"]}, resp_text="1 DHCPvX client class(es) found.",
                   args_rec=args_rec)

    # set another class, get two
    _set_class(backend, {"client-classes": [{"name": "bar"}]})  # this is without test parameter
    if dhcp_version == 'v6':
        args_rec["client-classes"].append({"metadata": {"server-tags": ["abc"]},
                                           "name": "bar",
                                           "option-data": [],
                                           "preferred-lifetime": 0,
                                           "valid-lifetime": 0})
        args_rec["count"] = 2
    else:
        args_rec["client-classes"].append({"boot-file-name": "",
                                           "metadata": {"server-tags": ["abc"]},
                                           "name": "bar",
                                           "next-server": "0.0.0.0",
                                           "option-data": [],
                                           "option-def": [],
                                           "server-hostname": "",
                                           "valid-lifetime": 0})
        args_rec["count"] = 2

    _get_all_class(backend=backend, args={"server-tags": ["abc"]}, resp_text="2 DHCPvX client class(es) found.",
                   args_rec=args_rec)

    # set 3rd class with different server tag
    _set_class(backend, {"client-classes": [{"name": "3rd-class", "test": "member('UNKNOWN')"}]}, tag="xyz")
    # get all for tag abs should be the same as above
    _get_all_class(backend=backend, args={"server-tags": ["abc"]}, resp_text="2 DHCPvX client class(es) found.",
                   args_rec=args_rec)

    # get all for tag xyz, should be just one
    args_rec_2 = {"client-classes": [{"boot-file-name": "",
                                      "metadata": {"server-tags": ["xyz"]},
                                      "name": "3rd-class",
                                      "next-server": "0.0.0.0",
                                      "option-data": [],
                                      "option-def": [],
                                      "server-hostname": "",
                                      "test": "member('UNKNOWN')",
                                      "valid-lifetime": 0}],
                  "count": 1}
    if dhcp_version == 'v6':
        args_rec_2 = {"client-classes": [{"metadata": {"server-tags": ["xyz"]},
                                          "name": "3rd-class",
                                          "option-data": [],
                                          "preferred-lifetime": 0,
                                          "test": "member('UNKNOWN')",
                                          "valid-lifetime": 0}],
                      "count": 1}

    _get_all_class(backend=backend, args={"server-tags": ["xyz"]}, resp_text="1 DHCPvX client class(es) found.",
                   args_rec=args_rec_2)
    # get abc, still should be just 2 classes
    _get_all_class(backend=backend, args={"server-tags": ["abc"]}, resp_text="2 DHCPvX client class(es) found.",
                   args_rec=args_rec)
    # set anther class with tag all, it should be in requests for abc and xyz
    _set_class(backend, {"client-classes": [{"name": "4th-class", "test": "member('UNKNOWN')"}]}, tag="all")

    if dhcp_version == 'v6':
        args_rec["client-classes"].append({"metadata": {"server-tags": ["all"]},
                                           "name": "4th-class",
                                           "option-data": [],
                                           "preferred-lifetime": 0,
                                           "test": "member('UNKNOWN')",
                                           "valid-lifetime": 0})
        args_rec["count"] = 3
        args_rec_2["client-classes"].append({"metadata": {"server-tags": ["all"]},
                                             "name": "4th-class",
                                             "option-data": [],
                                             "preferred-lifetime": 0,
                                             "test": "member('UNKNOWN')",
                                             "valid-lifetime": 0})
        args_rec_2["count"] = 2

    else:
        args_rec["client-classes"].append({"boot-file-name": "",
                                           "metadata": {"server-tags": ["all"]},
                                           "name": "4th-class",
                                           "next-server": "0.0.0.0",
                                           "option-data": [],
                                           "option-def": [],
                                           "server-hostname": "",
                                           "test": "member('UNKNOWN')",
                                           "valid-lifetime": 0})
        args_rec["count"] = 3
        args_rec_2["client-classes"].append({"boot-file-name": "",
                                             "metadata": {"server-tags": ["all"]},
                                             "name": "4th-class",
                                             "next-server": "0.0.0.0",
                                             "option-data": [],
                                             "option-def": [],
                                             "server-hostname": "",
                                             "test": "member('UNKNOWN')",
                                             "valid-lifetime": 0})
        args_rec_2["count"] = 2

    _get_all_class(backend=backend, args={"server-tags": ["abc", "all"]}, resp_text="3 DHCPvX client class(es) found.",
                   args_rec=args_rec)
    _get_all_class(backend=backend, args={"server-tags": ["xyz", "all"]}, resp_text="2 DHCPvX client class(es) found.",
                   args_rec=args_rec_2)

    # check tag just all
    args_rec_all = {"client-classes": [{"boot-file-name": "",
                                        "metadata": {"server-tags": ["all"]},
                                        "name": "4th-class",
                                        "next-server": "0.0.0.0",
                                        "option-data": [],
                                        "option-def": [],
                                        "server-hostname": "",
                                        "test": "member('UNKNOWN')",
                                        "valid-lifetime": 0}],
                    "count": 1}
    if dhcp_version == 'v6':
        args_rec_all = {"client-classes": [{"metadata": {"server-tags": ["all"]},
                                            "name": "4th-class",
                                            "option-data": [],
                                            "preferred-lifetime": 0,
                                            "test": "member('UNKNOWN')",
                                            "valid-lifetime": 0}],
                        "count": 1}

    _get_all_class(backend=backend, args={"server-tags": ["all"]}, resp_text="1 DHCPvX client class(es) found.",
                   args_rec=args_rec_all)

    _get_all_class(backend=backend, args={"server-tags": [""]}, resp_text="server-tag must not be empty", res=1)
    _get_all_class(backend=backend, args={"server-tags": []}, resp_text="'server-tags' list must not be empty", res=1)
    _get_all_class(backend=backend, args={}, resp_text="'server-tags' parameter is mandatory", res=1)
