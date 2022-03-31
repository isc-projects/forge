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
    setup_server_for_config_backend_cmds(backend_type=backend,
                                         config_control={"config-fetch-wait-time": 1}, force_reload=False)
    cmd = dict(command="remote-server6-set", arguments={"remote": {"type": backend},
                                                        "servers": [{"server-tag": "abc"}]})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)


def _get_server_config(reload_kea=False):
    if reload_kea:
        cmd = dict(command="config-backend-pull", arguments={})
        srv_msg.send_ctrl_cmd(cmd, exp_result=0)
    cmd = dict(command="config-get", arguments={})
    return srv_msg.send_ctrl_cmd(cmd, exp_result=0)


def _subnet_set(backend):
    cmd = dict(command="remote-subnet6-set",
               arguments={"remote": {"type": backend},
                          "server-tags": ["abc"],
                          "subnets": [{"subnet": "2001:db8:1::/64",
                                       "id": 5,
                                       "interface": "$(SERVER_IFACE)",
                                       "shared-network-name": "",
                                       "pools": [{"pool": "2001:db8:1::1-2001:db8:1::10"}]}]})

    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 5, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}


def _set_network(backend, channel='http'):
    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": backend},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{"name": "floor13"}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"shared-networks": [{"name": "floor13"}]},
                        "result": 0, "text": "IPv6 shared network successfully set."}


def _set_global_parameter(backend):
    cmd = dict(command="remote-global-parameter6-set", arguments={"remote": {"type": backend},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": {"decline-probation-period": 123456}})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1, "parameters": {"decline-probation-period": 123456}},
                        "result": 0,
                        "text": "1 DHCPv6 global parameter(s) successfully set."}


def _set_global_option(backend, channel='http'):
    cmd = dict(command="remote-option6-global-set", arguments={"remote": {"type": backend},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "code": 7,
                                                                   "data": "123"}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"result": 0, "text": "DHCPv6 option successfully set.",
                        "arguments": {"options": [{"code": 7, "space": "dhcp6"}]}}


@pytest.mark.v6
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_subnet_option(backend):
    _set_server(backend)
    _subnet_set(backend)
    cmd = dict(command="remote-option6-subnet-set",
               arguments={"subnets": [{"id": 5}],
                          "options": [{"always-send": False,
                                       "code": 23,
                                       "csv-format": True,
                                       "data": "2001:db8:1::1",
                                       "name": "dns-servers",
                                       "space": "dhcp6"}],
                          "remote": {"type": backend}})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    srv_msg.forge_sleep(3, "seconds")

    cfg = _get_server_config()
    assert cfg["arguments"]["Dhcp6"]["subnet6"][0]["option-data"] == cmd["arguments"]["options"]

    cmd = dict(command="remote-option6-subnet-del",
               arguments={"subnets": [{"id": 5}], "options": [{"code": 23, "space": "dhcp6"}],
                          "remote": {"type": backend}})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    srv_msg.forge_sleep(3, "seconds")

    cfg = _get_server_config()
    assert cfg["arguments"]["Dhcp6"]["subnet6"][0]["option-data"] == []


@pytest.mark.v6
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_subnet_in_network_option(backend):
    _set_server(backend)
    _set_network(backend)
    cmd = dict(command="remote-subnet6-set",
               arguments={"remote": {"type": backend},
                          "server-tags": ["abc"],
                          "subnets": [{"subnet": "2001:db8:1::/64",
                                       "id": 5,
                                       "interface": "$(SERVER_IFACE)",
                                       "shared-network-name": "floor13",
                                       "pools": [{"pool": "2001:db8:1::1-2001:db8:1::10"}]}]})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    cmd = dict(command="remote-option6-subnet-set",
               arguments={"subnets": [{"id": 5}],
                          "options": [{"always-send": False,
                                       "code": 23,
                                       "csv-format": True,
                                       "data": "2001:db8:1::1",
                                       "name": "dns-servers",
                                       "space": "dhcp6"}],
                          "remote": {"type": backend}})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    srv_msg.forge_sleep(2, "seconds")

    cfg = _get_server_config()
    assert cfg["arguments"]["Dhcp6"]["shared-networks"][0]["subnet6"][0]["option-data"] == cmd["arguments"]["options"]


@pytest.mark.v6
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_option_on_all_levels(backend):
    _set_server(backend)
    _set_network(backend)
    cmd = dict(command="remote-subnet6-set",
               arguments={"remote": {"type": backend},
                          "server-tags": ["abc"],
                          "subnets": [{"subnet": "2001:db8:1::/64",
                                       "id": 5,
                                       "interface": "$(SERVER_IFACE)",
                                       "shared-network-name": "floor13",
                                       "pools": [{"pool": "2001:db8:1::1-2001:db8:1::10"}],
                                       "pd-pools": [{"delegated-len": 91,
                                                     "prefix": "2001:db8:2::",
                                                     "prefix-len": 90}]}]})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    cmd_sub = dict(command="remote-option6-subnet-set",
                   arguments={"subnets": [{"id": 5}],
                              "options": [{"always-send": False,
                                           "code": 23,
                                           "csv-format": True,
                                           "name": "dns-servers",
                                           "space": "dhcp6",
                                           "data": "2001:db8:1::1"}],
                              "remote": {"type": backend}})
    srv_msg.send_ctrl_cmd(cmd_sub, exp_result=0)

    cmd_pool = dict(command="remote-option6-pool-set",
                    arguments={"pools": [{"pool": "2001:db8:1::1-2001:db8:1::10"}],
                               "options": [{"always-send": False,
                                            "code": 23,
                                            "csv-format": True,
                                            "name": "dns-servers",
                                            "space": "dhcp6",
                                            "data": "2001:db8:1::2"}],
                               "remote": {"type": backend}})
    srv_msg.send_ctrl_cmd(cmd_pool, exp_result=0)

    cmd_net = dict(command="remote-option6-network-set",
                   arguments={"shared-networks": [{"name": "floor13"}],
                              "options": [{"always-send": False,
                                           "code": 23,
                                           "csv-format": True,
                                           "name": "dns-servers",
                                           "space": "dhcp6",
                                           "data": "2001:db8:1::3"}],
                              "remote": {"type": backend}})
    srv_msg.send_ctrl_cmd(cmd_net, exp_result=0)

    cmd_pd = dict(command="remote-option6-pd-pool-set",
                  arguments={"pd-pools": [{"prefix": "2001:db8:2::", "prefix-len": 90}],
                             "options": [{"always-send": False,
                                          "code": 23,
                                          "csv-format": True,
                                          "name": "dns-servers",
                                          "space": "dhcp6",
                                          "data": "2001:db8:1::3"}],
                             "remote": {"type": backend}})
    srv_msg.send_ctrl_cmd(cmd_pd, exp_result=0)

    srv_msg.forge_sleep(2, "seconds")

    cfg = _get_server_config()
    assert cfg["arguments"]["Dhcp6"]["shared-networks"][0]["subnet6"][0]["option-data"] == \
        cmd_sub["arguments"]["options"]
    assert cfg["arguments"]["Dhcp6"]["shared-networks"][0]["subnet6"][0]["pd-pools"][0]["option-data"] == \
        cmd_pd["arguments"]["options"]
    assert cfg["arguments"]["Dhcp6"]["shared-networks"][0]["subnet6"][0]["pools"][0]["option-data"] == \
        cmd_pool["arguments"]["options"]
    assert cfg["arguments"]["Dhcp6"]["shared-networks"][0]["option-data"] == cmd_net["arguments"]["options"]
    assert cfg["arguments"]["Dhcp6"]["option-data"] == []


@pytest.mark.v6
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_network_option(backend):
    _set_server(backend)
    _set_network(backend)

    cmd = dict(command="remote-option6-network-set",
               arguments={"shared-networks": [{"name": "floor13"}],
                          "options": [{"always-send": False,
                                       "code": 23,
                                       "csv-format": True,
                                       "data": "2001:db8:1::1",
                                       "name": "dns-servers",
                                       "space": "dhcp6"}],
                          "remote": {"type": backend}})

    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    srv_msg.forge_sleep(2, "seconds")
    cfg = _get_server_config()
    assert cfg["arguments"]["Dhcp6"]["shared-networks"][0]["option-data"] == cmd["arguments"]["options"]
    cmd = dict(command="remote-option6-network-del",
               arguments={"shared-networks": [{"name": "floor13"}],
                          "options": [{"code": 23, "space": "dhcp6"}],
                          "remote": {"type": backend}})

    srv_msg.send_ctrl_cmd(cmd, exp_result=0)
    srv_msg.forge_sleep(3, "seconds")
    cfg = _get_server_config()

    assert cfg["arguments"]["Dhcp6"]["shared-networks"][0]["option-data"] == []


@pytest.mark.v6
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_pool_option(backend):
    _set_server(backend)
    _subnet_set(backend)
    cmd = dict(command="remote-option6-pool-set",
               arguments={"pools": [{"pool": "2001:db8:1::1-2001:db8:1::10"}],
                          "options": [{"always-send": False,
                                       "code": 23,
                                       "csv-format": True,
                                       "data": "2001:db8:1::1",
                                       "name": "dns-servers",
                                       "space": "dhcp6"}],
                          "remote": {"type": backend}})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    srv_msg.forge_sleep(3, "seconds")

    cfg = _get_server_config()
    assert cfg["arguments"]["Dhcp6"]["subnet6"][0]["pools"][0]["option-data"] == cmd["arguments"]["options"]

    cmd = dict(command="remote-option6-pool-del",
               arguments={"pools": [{"pool": "2001:db8:1::1-2001:db8:1::10"}],
                          "options": [{"code": 23, "space": "dhcp6"}],
                          "remote": {"type": backend}})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    srv_msg.forge_sleep(4, "seconds")

    cfg = _get_server_config()
    assert cfg["arguments"]["Dhcp6"]["subnet6"][0]["pools"][0]["option-data"] == []


@pytest.mark.v6
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_pd_pool_option(backend):
    _set_server(backend)
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": backend},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64", "id": 5,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pd-pools": [{
                                                                         "delegated-len": 91,
                                                                         "prefix": "2001:db8:2::",
                                                                         "prefix-len": 90}]}]})
    srv_msg.send_ctrl_cmd(cmd)

    srv_msg.forge_sleep(2, "seconds")

    cmd = dict(command="remote-option6-pd-pool-set", arguments={
        "pd-pools": [{"prefix": "2001:db8:2::", "prefix-len": 90}],
        "options": [{"always-send": False,
                     "code": 23,
                     "csv-format": True,
                     "data": "2001:db8:1::1",
                     "name": "dns-servers",
                     "space": "dhcp6"}],
        "remote": {"type": backend}})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    srv_msg.forge_sleep(3, "seconds")

    cfg = _get_server_config()

    assert cfg["arguments"]["Dhcp6"]["subnet6"][0]["pd-pools"][0]["option-data"] == cmd["arguments"]["options"]

    cmd = dict(command="remote-option6-pd-pool-del", arguments={
        "pd-pools": [{"prefix": "2001:db8:2::", "prefix-len": 90}],
        "options": [{"code": 23, "space": "dhcp6"}],
        "remote": {"type": backend}})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    srv_msg.forge_sleep(3, "seconds")

    cfg = _get_server_config()
    assert cfg["arguments"]["Dhcp6"]["subnet6"][0]["pd-pools"][0]["option-data"] == []
