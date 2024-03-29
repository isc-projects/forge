# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea database config backend commands hook testing"""

import pytest
from src import srv_msg

from src.softwaresupport.cb_model import setup_server_for_config_backend_cmds

pytestmark = [pytest.mark.v4,
              pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.cb,
              pytest.mark.cb_cmds]


def _setup_server(backend):
    setup_server_for_config_backend_cmds(backend_type=backend, config_control={"config-fetch-wait-time": 1},
                                         force_reload=False)
    cmd = dict(command="remote-server4-set", arguments={"remote": {"type": backend},
                                                        "servers": [{"server-tag": "abc"}]})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)


def _get_server_config(reload_kea=False):
    if reload_kea:
        cmd = dict(command="config-backend-pull", arguments={})
        srv_msg.send_ctrl_cmd(cmd, exp_result=0)
    cmd = dict(command="config-get", arguments={})
    return srv_msg.send_ctrl_cmd(cmd, exp_result=0)


def _subnet_set(backend):
    cmd = dict(command="remote-subnet4-set",
               arguments={"remote": {"type": backend},
                          "server-tags": ["abc"],
                          "subnets": [{"subnet": "10.0.0.0/24",
                                       "id": 5,
                                       "interface": "$(SERVER_IFACE)",
                                       "shared-network-name": "",
                                       "pools": [{"pool": "10.0.0.1-10.0.0.100"}]}]})

    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 5, "subnet": "10.0.0.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}


def _set_network(backend, channel='http'):
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{"name": "floor13"}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"shared-networks": [{"name": "floor13"}]},
                        "result": 0, "text": "IPv4 shared network successfully set."}


@pytest.mark.v4
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_subnet_option(backend):
    _setup_server(backend)
    _subnet_set(backend)
    cmd = dict(command="remote-option4-subnet-set",
               arguments={"subnets": [{"id": 5}],
                          "options": [{"always-send": False,
                                       "code": 6,
                                       "csv-format": True,
                                       "data": "10.0.0.1",
                                       "name": "domain-name-servers",
                                       "never-send": True,
                                       "space": "dhcp4"}],
                          "remote": {"type": backend}})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    srv_msg.forge_sleep(3, "seconds")

    cfg = _get_server_config()
    assert cfg["arguments"]["Dhcp4"]["subnet4"][0]["option-data"] == cmd["arguments"]["options"]

    cmd = dict(command="remote-option4-subnet-del",
               arguments={"subnets": [{"id": 5}], "options": [{"code": 6, "space": "dhcp4"}],
                          "remote": {"type": backend}})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    srv_msg.forge_sleep(3, "seconds")

    cfg = _get_server_config()
    assert cfg["arguments"]["Dhcp4"]["subnet4"][0]["option-data"] == []


@pytest.mark.v4
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_multiple_subnet_option(backend):
    _setup_server(backend)
    _subnet_set(backend)

    cmd = dict(command="remote-subnet4-set",
               arguments={"remote": {"type": backend},
                          "server-tags": ["abc"],
                          "subnets": [{"subnet": "10.10.0.0/24",
                                       "id": 9,
                                       "interface": "$(SERVER_IFACE)",
                                       "shared-network-name": "",
                                       "pools": [{"pool": "10.10.0.1-10.10.0.100"}]}]})
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command="remote-option4-subnet-set",
               arguments={"subnets": [{"id": 5}],
                          "options": [{"always-send": False,
                                       "code": 6,
                                       "csv-format": True,
                                       "data": "10.0.0.1",
                                       "name": "domain-name-servers",
                                       "never-send": False,
                                       "space": "dhcp4"}],
                          "remote": {"type": backend}})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    cmd = dict(command="remote-option4-subnet-set",
               arguments={"subnets": [{"id": 9}],
                          "options": [{"always-send": False, "code": 6, "csv-format": True,
                                       "data": "10.0.0.2", "name": "domain-name-servers",
                                       "never-send": True, "space": "dhcp4"}], "remote": {"type": backend}})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    srv_msg.forge_sleep(3, "seconds")

    cfg = _get_server_config()

    subnets = cfg["arguments"]["Dhcp4"]["subnet4"]
    assert len(subnets) == 2
    if subnets[0]["id"] == 9:
        assert subnets[0]["option-data"] == cmd["arguments"]["options"]
    else:
        assert subnets[1]["option-data"] == cmd["arguments"]["options"]

    cmd = dict(command="remote-option4-subnet-del",
               arguments={"subnets": [{"id": 5}], "options": [{"code": 6, "space": "dhcp4"}],
                          "remote": {"type": backend}})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    srv_msg.forge_sleep(3, "seconds")

    cfg = _get_server_config(reload_kea=True)

    subnets = cfg["arguments"]["Dhcp4"]["subnet4"]
    assert len(subnets) == 2
    if subnets[0]["id"] == 5:
        assert subnets[0]["option-data"] == []
    else:
        assert subnets[1]["option-data"] == []


@pytest.mark.v4
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_subnet_in_network_option(backend):
    _setup_server(backend)
    _set_network(backend)
    cmd = dict(command="remote-subnet4-set",
               arguments={"remote": {"type": backend},
                          "server-tags": ["abc"],
                          "subnets": [{"subnet": "10.0.0.0/24",
                                       "id": 5,
                                       "interface": "$(SERVER_IFACE)",
                                       "shared-network-name": "floor13",
                                       "pools": [{"pool": "10.0.0.1-10.0.0.10"}]}]})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    cmd = dict(command="remote-option4-subnet-set",
               arguments={"subnets": [{"id": 5}],
                          "options": [{"always-send": False,
                                       "code": 6,
                                       "csv-format": True,
                                       "data": "10.0.0.1",
                                       "name": "domain-name-servers",
                                       "never-send": True,
                                       "space": "dhcp4"}],
                          "remote": {"type": backend}})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    srv_msg.forge_sleep(2, "seconds")

    cfg = _get_server_config()
    assert cfg["arguments"]["Dhcp4"]["shared-networks"][0]["subnet4"][0]["option-data"] == cmd["arguments"]["options"]


@pytest.mark.v4
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_option_on_all_levels(backend):
    _setup_server(backend)
    _set_network(backend)
    cmd = dict(command="remote-subnet4-set",
               arguments={"remote": {"type": backend},
                          "server-tags": ["abc"],
                          "subnets": [{"subnet": "10.0.0.0/24",
                                       "id": 5,
                                       "interface": "$(SERVER_IFACE)",
                                       "shared-network-name": "floor13",
                                       "pools": [{"pool": "10.0.0.1-10.0.0.10"}]}]})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    cmd_sub = dict(command="remote-option4-subnet-set",
                   arguments={"subnets": [{"id": 5}],
                              "options": [{"always-send": False,
                                           "code": 6,
                                           "csv-format": True,
                                           "name": "domain-name-servers",
                                           "never-send": True,
                                           "space": "dhcp4",
                                           "data": "10.0.0.1"}],
                              "remote": {"type": backend}})
    srv_msg.send_ctrl_cmd(cmd_sub, exp_result=0)

    cmd_pool = dict(command="remote-option4-pool-set",
                    arguments={"pools": [{"pool": "10.0.0.1-10.0.0.10"}],
                               "options": [{"always-send": False,
                                            "code": 6,
                                            "csv-format": True,
                                            "name": "domain-name-servers",
                                            "never-send": True,
                                            "space": "dhcp4",
                                            "data": "10.0.0.2"}],
                               "remote": {"type": backend}})
    srv_msg.send_ctrl_cmd(cmd_pool, exp_result=0)

    cmd_net = dict(command="remote-option4-network-set",
                   arguments={"shared-networks": [{"name": "floor13"}],
                              "options": [{"always-send": False,
                                           "code": 6,
                                           "csv-format": True,
                                           "name": "domain-name-servers",
                                           "never-send": True,
                                           "space": "dhcp4",
                                           "data": "10.0.0.3"}],
                              "remote": {"type": backend}})
    srv_msg.send_ctrl_cmd(cmd_net, exp_result=0)

    srv_msg.forge_sleep(2, "seconds")

    cfg = _get_server_config()
    assert cfg["arguments"]["Dhcp4"]["shared-networks"][0]["subnet4"][0]["option-data"] == \
        cmd_sub["arguments"]["options"]
    assert cfg["arguments"]["Dhcp4"]["shared-networks"][0]["subnet4"][0]["pools"][0]["option-data"] == \
        cmd_pool["arguments"]["options"]
    assert cfg["arguments"]["Dhcp4"]["shared-networks"][0]["option-data"] == cmd_net["arguments"]["options"]
    assert cfg["arguments"]["Dhcp4"]["option-data"] == []


@pytest.mark.v4
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_network_option(backend):
    _setup_server(backend)
    _set_network(backend)

    cmd = dict(command="remote-option4-network-set",
               arguments={"shared-networks": [{"name": "floor13"}],
                          "options": [{"always-send": False,
                                       "code": 6,
                                       "csv-format": True,
                                       "data": "10.0.0.1",
                                       "name": "domain-name-servers",
                                       "never-send": True,
                                       "space": "dhcp4"}],
                          "remote": {"type": backend}})

    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    srv_msg.forge_sleep(2, "seconds")
    cfg = _get_server_config()
    assert cfg["arguments"]["Dhcp4"]["shared-networks"][0]["option-data"] == cmd["arguments"]["options"]
    cmd = dict(command="remote-option4-network-del",
               arguments={"shared-networks": [{"name": "floor13"}],
                          "options": [{"code": 6, "space": "dhcp4"}],
                          "remote": {"type": backend}})

    srv_msg.send_ctrl_cmd(cmd, exp_result=0)
    srv_msg.forge_sleep(3, "seconds")
    cfg = _get_server_config()

    assert cfg["arguments"]["Dhcp4"]["shared-networks"][0]["option-data"] == []


@pytest.mark.v4
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_pool_option(backend):
    _setup_server(backend)
    _subnet_set(backend)
    cmd = dict(command="remote-option4-pool-set",
               arguments={"pools": [{"pool": "10.0.0.1-10.0.0.100"}],
                          "options": [{"always-send": False,
                                       "code": 6,
                                       "csv-format": True,
                                       "data": "10.0.0.1",
                                       "name": "domain-name-servers",
                                       "never-send": True,
                                       "space": "dhcp4"}],
                          "remote": {"type": backend}})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    srv_msg.forge_sleep(3, "seconds")

    cfg = _get_server_config()
    assert cfg["arguments"]["Dhcp4"]["subnet4"][0]["pools"][0]["option-data"] == cmd["arguments"]["options"]

    cmd = dict(command="remote-option4-pool-del",
               arguments={"pools": [{"pool": "10.0.0.1-10.0.0.100"}],
                          "options": [{"code": 6, "space": "dhcp4"}],
                          "remote": {"type": backend}})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    srv_msg.forge_sleep(4, "seconds")

    cfg = _get_server_config()
    assert cfg["arguments"]["Dhcp4"]["subnet4"][0]["pools"][0]["option-data"] == []
