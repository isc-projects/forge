# Copyright (C) 2024 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea database config backend commands hook testing"""

import pytest

from src import srv_msg

from src.softwaresupport.cb_model import setup_server_for_config_backend_cmds, get_config
from src.forge_cfg import world


pytestmark = [pytest.mark.v4,
              pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.cb,
              pytest.mark.cb_cmds]


def _set_server_tag(backend, tag):
    cmd = dict(command=f"remote-server{world.proto[1]}-set",
               arguments={"remote": {"type": backend},
                          "servers": [{"server-tag": tag}]})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)


def _setup_server(backend):
    setup_server_for_config_backend_cmds(backend_type=backend)
    _set_server_tag(backend, "abc")


def _reload():
    # request config reloading
    cmd = {"command": "config-backend-pull", "arguments": {}}
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {'result': 0, 'text': 'On demand configuration update successful.'}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_map_compatibility(backend):
    _setup_server(backend)
    cmd = dict(command="remote-global-parameter4-set",
               arguments={"remote": {"type": backend},
                          "server-tags": ["abc"],
                          "parameters": {
                              "compatibility.ignore-dhcp-server-identifier": True,
                              "compatibility.ignore-rai-link-selection": True,
                              "compatibility.lenient-option-parsing": True,
                              "compatibility.exclude-first-last-24": True,
               }})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments":
                        {
                            "count": 4,
                            "parameters":
                            {
                                "compatibility":
                                {
                                    "ignore-dhcp-server-identifier": True,
                                    "ignore-rai-link-selection": True,
                                    "lenient-option-parsing": True,
                                    "exclude-first-last-24": True,
                                }
                            }},
                        "result": 0,
                        "text": "4 DHCPv4 global parameter(s) successfully set."}

    _reload()
    config = get_config()
    assert config["Dhcp4"]["compatibility"]["ignore-dhcp-server-identifier"] is True
    assert config["Dhcp4"]["compatibility"]["ignore-rai-link-selection"] is True
    assert config["Dhcp4"]["compatibility"]["lenient-option-parsing"] is True
    assert config["Dhcp4"]["compatibility"]["exclude-first-last-24"] is True


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_map_compatibility_missing_parameter(backend):
    _setup_server(backend)
    cmd = dict(command="remote-global-parameter4-set",
               arguments={"remote": {"type": backend},
                          "server-tags": ["abc"],
                          "parameters": {
                              "compatibility.ignore-dhcp-server-identifier": True,
                              "compatibility.unknown-parameter": True
               }})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "unknown parameter 'compatibility.unknown-parameter'"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_map_control_socket(backend):
    _setup_server(backend)
    cmd = dict(command="remote-global-parameter4-set",
               arguments={"remote": {"type": backend},
                          "server-tags": ["abc"],
                          "parameters": {
                              "control-socket.socket-name": "/path/to/the/unix/socket-v4",
                              "control-socket.socket-type": "unix",
               }})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments":
                        {
                            "count": 2,
                            "parameters":
                            {
                                "control-socket":
                                {
                                    "socket-name": "/path/to/the/unix/socket-v4",
                                    "socket-type": "unix",
                                }
                            }},
                        "result": 0,
                        "text": "2 DHCPv4 global parameter(s) successfully set."}

    _reload()
    config = get_config()
    assert config["Dhcp4"]["control-socket"]["socket-name"] == "/path/to/the/unix/socket-v4"
    assert config["Dhcp4"]["control-socket"]["socket-type"] == "unix"


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_map_control_socket_missing_parameter(backend):
    _setup_server(backend)
    cmd = dict(command="remote-global-parameter4-set",
               arguments={"remote": {"type": backend},
                          "server-tags": ["abc"],
                          "parameters": {
                              "control-socket.socket-name": "/path/to/the/unix/socket-v4",
                              "control-socket.unknown-parameter": True,
               }})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "unknown parameter 'control-socket.unknown-parameter'"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_map_ddns(backend):
    _setup_server(backend)
    cmd = dict(command="remote-global-parameter4-set",
               arguments={"remote": {"type": backend},
                          "server-tags": ["abc"],
                          "parameters": {
                              "dhcp-ddns.enable-updates": True,
                              "dhcp-ddns.max-queue-size": 100,
                              "dhcp-ddns.ncr-format": "JSON",
                              "dhcp-ddns.ncr-protocol": "UDP",
                              "dhcp-ddns.sender-ip": "192.168.50.100",
                              "dhcp-ddns.sender-port": 530,
                              "dhcp-ddns.server-ip": "127.0.0.1",
                              "dhcp-ddns.server-port": 53,
               }})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments":
                        {
                            "count": 8,
                            "parameters":
                            {
                                "dhcp-ddns":
                                {
                                    "enable-updates": True,
                                    "max-queue-size": 100,
                                    "ncr-format": "JSON",
                                    "ncr-protocol": "UDP",
                                    "sender-ip": "192.168.50.100",
                                    "sender-port": 530,
                                    "server-ip": "127.0.0.1",
                                    "server-port": 53,
                                }
                            }},
                        "result": 0,
                        "text": "8 DHCPv4 global parameter(s) successfully set."}

    _reload()
    config = get_config()
    assert config["Dhcp4"]["dhcp-ddns"]["enable-updates"] is True
    assert config["Dhcp4"]["dhcp-ddns"]["max-queue-size"] == 100
    assert config["Dhcp4"]["dhcp-ddns"]["ncr-format"] == "JSON"
    assert config["Dhcp4"]["dhcp-ddns"]["ncr-protocol"] == "UDP"
    assert config["Dhcp4"]["dhcp-ddns"]["sender-ip"] == "192.168.50.100"
    assert config["Dhcp4"]["dhcp-ddns"]["sender-port"] == 530
    assert config["Dhcp4"]["dhcp-ddns"]["server-ip"] == "127.0.0.1"
    assert config["Dhcp4"]["dhcp-ddns"]["server-port"] == 53


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_map_ddns_missing_parameter(backend):
    _setup_server(backend)
    cmd = dict(command="remote-global-parameter4-set",
               arguments={"remote": {"type": backend},
                          "server-tags": ["abc"],
                          "parameters": {
                              "dhcp-ddns.enable-updates": True,
                              "dhcp-ddns.unknown-parameter": True,
               }})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "unknown parameter 'dhcp-ddns.unknown-parameter'"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_map_expired_leases_processing(backend):
    _setup_server(backend)
    cmd = dict(command="remote-global-parameter4-set",
               arguments={"remote": {"type": backend},
                          "server-tags": ["abc"],
                          "parameters": {
                              "expired-leases-processing.flush-reclaimed-timer-wait-time": 1000,
                              "expired-leases-processing.hold-reclaimed-time": 1000,
                              "expired-leases-processing.max-reclaim-leases": 1000,
                              "expired-leases-processing.max-reclaim-time": 1000,
                              "expired-leases-processing.reclaim-timer-wait-time": 1000,
                              "expired-leases-processing.unwarned-reclaim-cycles": 1000,
               }})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments":
                        {
                            "count": 6,
                            "parameters":
                            {
                                "expired-leases-processing":
                                {
                                    "flush-reclaimed-timer-wait-time": 1000,
                                    "hold-reclaimed-time": 1000,
                                    "max-reclaim-leases": 1000,
                                    "max-reclaim-time": 1000,
                                    "reclaim-timer-wait-time": 1000,
                                    "unwarned-reclaim-cycles": 1000,
                                }
                            }},
                        "result": 0,
                        "text": "6 DHCPv4 global parameter(s) successfully set."}
    _reload()
    config = get_config()
    assert config["Dhcp4"]["expired-leases-processing"]["flush-reclaimed-timer-wait-time"] == 1000
    assert config["Dhcp4"]["expired-leases-processing"]["hold-reclaimed-time"] == 1000
    assert config["Dhcp4"]["expired-leases-processing"]["max-reclaim-leases"] == 1000
    assert config["Dhcp4"]["expired-leases-processing"]["max-reclaim-time"] == 1000
    assert config["Dhcp4"]["expired-leases-processing"]["reclaim-timer-wait-time"] == 1000
    assert config["Dhcp4"]["expired-leases-processing"]["unwarned-reclaim-cycles"] == 1000


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_map_expired_leases_processing_missing_parameter(backend):
    _setup_server(backend)
    cmd = dict(command="remote-global-parameter4-set",
               arguments={"remote": {"type": "mysql"},
                          "server-tags": ["abc"],
                          "parameters": {
                              "expired-leases-processing.flush-reclaimed-timer-wait-time": 1000,
                              "expired-leases-processing.unknown-parameter": True,
               }})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "unknown parameter 'expired-leases-processing.unknown-parameter'"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_map_multi_threading(backend):
    _setup_server(backend)
    cmd = dict(command="remote-global-parameter4-set",
               arguments={"remote": {"type": backend},
                          "server-tags": ["abc"],
                          "parameters": {
                              "multi-threading.enable-multi-threading": True,
                              "multi-threading.thread-pool-size": 2,
                              "multi-threading.packet-queue-size": 4,
               }})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments":
                        {
                            "count": 3,
                            "parameters":
                            {
                                "multi-threading":
                                {
                                    "enable-multi-threading": True,
                                    "thread-pool-size": 2,
                                    "packet-queue-size": 4,
                                }
                            }},
                        "result": 0,
                        "text": "3 DHCPv4 global parameter(s) successfully set."}
    _reload()
    config = get_config()
    assert config["Dhcp4"]["multi-threading"]["enable-multi-threading"] is True
    assert config["Dhcp4"]["multi-threading"]["thread-pool-size"] == 2
    assert config["Dhcp4"]["multi-threading"]["packet-queue-size"] == 4


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_map_multi_threading_missing_parameter(backend):
    _setup_server(backend)
    cmd = dict(command="remote-global-parameter4-set",
               arguments={"remote": {"type": "mysql"},
                          "server-tags": ["abc"],
                          "parameters": {
                              "multi-threading.enable-multi-threading": True,
                              "multi-threading.unknown-parameter": True,
               }})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "unknown parameter 'multi-threading.unknown-parameter'"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_map_sanity_checks(backend):
    _setup_server(backend)
    cmd = dict(command="remote-global-parameter4-set",
               arguments={"remote": {"type": backend},
                          "server-tags": ["abc"],
                          "parameters": {
                              "sanity-checks.lease-checks": "fix-del",
                              "sanity-checks.extended-info-checks": "strict",
               }})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments":
                        {
                            "count": 2,
                            "parameters":
                            {
                                "sanity-checks":
                                {
                                    "lease-checks": "fix-del",
                                    "extended-info-checks": "strict",
                                }
                            }},
                        "result": 0,
                        "text": "2 DHCPv4 global parameter(s) successfully set."}
    _reload()
    config = get_config()
    assert config["Dhcp4"]["sanity-checks"]["lease-checks"] == "fix-del"
    assert config["Dhcp4"]["sanity-checks"]["extended-info-checks"] == "strict"


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_map_sanity_checks_missing_parameter(backend):
    _setup_server(backend)
    cmd = dict(command="remote-global-parameter4-set",
               arguments={"remote": {"type": backend},
                          "server-tags": ["abc"],
                          "parameters": {
                              "sanity-checks.lease-checks": "fix-del",
                              "sanity-checks.unknown-parameter": "strict",
               }})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "unknown parameter 'sanity-checks.unknown-parameter'"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_map_dhcp_queue_control(backend):
    _setup_server(backend)

    #  dhcp-queue-control is incompatible with multi-threading
    cmd = dict(command="remote-global-parameter4-set",
               arguments={"remote": {"type": backend},
                          "server-tags": ["abc"],
                          "parameters": {
                              "multi-threading.enable-multi-threading": False,
               }})
    srv_msg.send_ctrl_cmd(cmd)
    _reload()

    cmd = dict(command="remote-global-parameter4-set",
               arguments={"remote": {"type": backend},
                          "server-tags": ["abc"],
                          "parameters": {
                              "dhcp-queue-control.enable-queue": True,
                              "dhcp-queue-control.queue-type": "kea-ring4",
                              "dhcp-queue-control.capacity": 256,
               }})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments":
                        {
                            "count": 3,
                            "parameters":
                            {
                                "dhcp-queue-control":
                                {
                                    "enable-queue": True,
                                    "queue-type": "kea-ring4",
                                    "capacity": 256,
                                }
                            }},
                        "result": 0,
                        "text": "3 DHCPv4 global parameter(s) successfully set."}

    _reload()
    config = get_config()
    assert config["Dhcp4"]["dhcp-queue-control"]["enable-queue"] is True
    assert config["Dhcp4"]["dhcp-queue-control"]["queue-type"] == "kea-ring4"
    assert config["Dhcp4"]["dhcp-queue-control"]["capacity"] == 256


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_global_map_dhcp_queue_control_missing_parameter(backend):
    _setup_server(backend)
    cmd = dict(command="remote-global-parameter4-set",
               arguments={"remote": {"type": backend},
                          "server-tags": ["abc"],
                          "parameters": {
                              "dhcp-queue-control.enable-queue": True,
                              "dhcp-queue-control.unknown-parameter": "kea-ring4",
               }})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "unknown parameter 'dhcp-queue-control.unknown-parameter'"}
