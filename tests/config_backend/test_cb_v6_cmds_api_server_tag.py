# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
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


def _set_server_tag(backend, tag="abc"):
    cmd = dict(command="remote-server6-set", arguments={"remote": {"type": backend},
                                                        "servers": [{"server-tag": tag,
                                                                     "description": "some server"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"result": 0, "text": "DHCPv6 server successfully set.",
                        "arguments": {"servers": [{"server-tag": tag, "description": "some server"}]}}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_server_tag_set(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    _set_server_tag(backend)


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_server_tag_set_any(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    cmd = dict(command="remote-server6-set", arguments={"remote": {"type": backend},
                                                        "servers": [{"server-tag": "any"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "'any' is reserved and must not be used as a server-tag"}


@pytest.mark.parametrize('channel', ['socket', 'http'])
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_server_tag_set_missing_tag(channel, backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    cmd = dict(command="remote-server6-set", arguments={"remote": {"type": backend},
                                                        "servers": [{"description": "some server"}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel, exp_result=1)

    assert response == {"result": 1, "text": "missing 'server-tag' parameter"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_server_tag_set_incorrect_tag(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    cmd = dict(command="remote-server6-set", arguments={"remote": {"type": backend},
                                                        "servers": [{"server-tag": 123}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "'server-tag' parameter is not a string"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_server_tag_set_empty_tag(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    cmd = dict(command="remote-server6-set", arguments={"remote": {"type": backend},
                                                        "servers": [{"server-tag": ""}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "server-tag must not be empty"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_server_tag_set_missing_description(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    cmd = dict(command="remote-server6-set", arguments={"remote": {"type": backend},
                                                        "servers": [{"server-tag": "someserver"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"servers": [{"description": "", "server-tag": "someserver"}]},
                        "result": 0, "text": "DHCPv6 server successfully set."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_server_tag_set_missing_servers(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    cmd = dict(command="remote-server6-set", arguments={"remote": {"type": backend}})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "'servers' parameter must be specified and must be a list"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_server_tag_set_empty_servers(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    cmd = dict(command="remote-server6-set", arguments={"remote": {"type": backend},
                                                        "servers": []})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "'servers' list must include exactly one element"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_server_tag_set_multiple_servers(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    cmd = dict(command="remote-server6-set", arguments={"remote": {"type": backend},
                                                        "servers": [{"server-tag": "someserver"},
                                                                    {"server-tag": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "'servers' list must include exactly one element"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_server_tag_get(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    _set_server_tag(backend)
    cmd = dict(command="remote-server6-get", arguments={"remote": {"type": backend},
                                                        "servers": [{"server-tag": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1, "servers": [{"description": "some server", "server-tag": "abc"}]},
                        "result": 0, "text": "DHCPv6 server 'abc' found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_server_tag_get_non_existing_tag(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    cmd = dict(command="remote-server6-get", arguments={"remote": {"type": backend},
                                                        "servers": [{"server-tag": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "servers": []},
                        "result": 3, "text": "DHCPv6 server 'abc' not found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_server_tag_get_empty_tag(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    _set_server_tag(backend)
    cmd = dict(command="remote-server6-get", arguments={"remote": {"type": backend},
                                                        "servers": [{"server-tag": ""}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "server-tag must not be empty"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_server_tag_get_missing_tag(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    _set_server_tag(backend)
    cmd = dict(command="remote-server6-get", arguments={"remote": {"type": backend},
                                                        "servers": [{}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "missing 'server-tag' parameter"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_server_tag_del(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    _set_server_tag(backend)
    cmd = dict(command="remote-server6-del", arguments={"remote": {"type": backend},
                                                        "servers": [{"server-tag": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv6 server(s) deleted."}

    cmd = dict(command="remote-server6-get", arguments={"remote": {"type": backend},
                                                        "servers": [{"server-tag": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "servers": []},
                        "result": 3, "text": "DHCPv6 server 'abc' not found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_server_tag_del_all(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    _set_server_tag(backend)
    cmd = dict(command="remote-server6-del", arguments={"remote": {"type": backend},
                                                        "servers": [{"server-tag": "all"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1,
                        "text": "'all' is a name reserved for the server tag which associates the configuration "
                                "elements with all servers connecting to the database and may not be deleted"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_server_tag_del_non_existing_tag(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    cmd = dict(command="remote-server6-del", arguments={"remote": {"type": backend},
                                                        "servers": [{"server-tag": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 DHCPv6 server(s) deleted."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_server_tag_del_empty_tag(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    _set_server_tag(backend)
    cmd = dict(command="remote-server6-del", arguments={"remote": {"type": backend},
                                                        "servers": [{"server-tag": ""}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "server-tag must not be empty"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_server_tag_del_missing_tag(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    _set_server_tag(backend)
    cmd = dict(command="remote-server6-del", arguments={"remote": {"type": backend},
                                                        "servers": [{}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "missing 'server-tag' parameter"}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_server_tag_get_all(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    _set_server_tag(backend)
    _set_server_tag(backend, tag="xyz")
    cmd = dict(command="remote-server6-get-all", arguments={"remote": {"type": backend}})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 2,
                                      "servers": [{"description": "some server", "server-tag": "abc"},
                                                  {"description": "some server", "server-tag": "xyz"}]},
                        "result": 0, "text": "2 DHCPv6 server(s) found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_server_tag_get_all_no_tags(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    cmd = dict(command="remote-server6-get-all", arguments={"remote": {"type": backend}})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "servers": []}, "result": 3, "text": "0 DHCPv6 server(s) found."}


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_server_tag_get_all_one_tags(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    _set_server_tag(backend)

    cmd = dict(command="remote-server6-get-all", arguments={"remote": {"type": backend}})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1,
                                      "servers": [{"description": "some server", "server-tag": "abc"}]},
                        "result": 0, "text": "1 DHCPv6 server(s) found."}


def _add_server_tag(backend, server_tag=None):
    cmd = dict(command="remote-server6-set", arguments={"remote": {"type": backend},
                                                        "servers": [{"server-tag": server_tag}]})
    srv_msg.send_ctrl_cmd(cmd)


def _subnet_set(server_tags, subnet_id, pool, backend, exp_result=0, subnet="2001:db8:1::/64"):
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": backend},
                                                        "server-tags": server_tags,
                                                        "subnets": [{"subnet": subnet, "id": subnet_id,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": pool}]}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)

    assert response == {"arguments": {"subnets": [{"id": subnet_id, "subnet": subnet}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}


def _subnet_get(backend, command="remote-subnet6-get-by-id", exp_result=0, subnet_parameter=None):
    cmd = dict(command=command, arguments={"remote": {"type": backend}})
    if subnet_parameter:
        cmd["arguments"]["subnets"] = [subnet_parameter]

    return srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)


def _subnet_list(command, server_tags, backend, exp_result=0):
    cmd = dict(command=command, arguments={"remote": {"type": backend}, "server-tags": server_tags})

    return srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)


def _subnet_del(backend, exp_result=0, subnet_parameter=None):
    return _subnet_get(command="remote-subnet6-del-by-id", exp_result=exp_result, subnet_parameter=subnet_parameter,
                       backend=backend)


def _check_subnet_result(resp, server_tags, count=1, subnet_id=5, subnet="2001:db8:1::/64"):
    assert resp["result"] == 0
    assert resp["arguments"]["count"] == count
    assert resp["arguments"]["subnets"][0]["metadata"] == {"server-tags": server_tags}
    assert resp["arguments"]["subnets"][0]["subnet"] == subnet
    assert resp["arguments"]["subnets"][0]["id"] == subnet_id


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_server_tags_delete_server_tag_keep_data(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    _add_server_tag(backend, "abc")
    _add_server_tag(backend, "xyz")
    _subnet_set(server_tags=["abc"], subnet_id=5, pool="2001:db8:1::1-2001:db8:1::100", backend=backend)
    _subnet_set(server_tags=["xyz"], subnet_id=6, pool="2001:db8:3::1-2001:db8:3::10", subnet="2001:db8:3::/64",
                backend=backend)

    resp = _subnet_get(subnet_parameter={"id": 5}, backend=backend)
    _check_subnet_result(resp, server_tags=["abc"], subnet_id=5)

    resp = _subnet_get(subnet_parameter={"id": 6}, backend=backend)
    _check_subnet_result(resp, server_tags=["xyz"], subnet_id=6, subnet="2001:db8:3::/64")

    cmd = dict(command="remote-server6-del", arguments={"remote": {"type": backend},
                                                        "servers": [{"server-tag": "abc"}]})
    srv_msg.send_ctrl_cmd(cmd)

    resp = _subnet_get(subnet_parameter={"id": 5}, backend=backend)
    _check_subnet_result(resp, server_tags=[], subnet_id=5, subnet="2001:db8:1::/64")

    _add_server_tag(backend, "abc")
    resp = _subnet_get(subnet_parameter={"id": 5}, backend=backend)
    _check_subnet_result(resp, server_tags=[], subnet_id=5, subnet="2001:db8:1::/64")

    resp = _subnet_get(subnet_parameter={"id": 6}, backend=backend)
    _check_subnet_result(resp, server_tags=["xyz"], subnet_id=6, subnet="2001:db8:3::/64")


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_get_server_tags(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    _add_server_tag(backend, "abc")
    _add_server_tag(backend, "xyz")
    _subnet_set(server_tags=["abc", "xyz"], subnet_id=5, pool="2001:db8:1::1-2001:db8:1::100", backend=backend)
    _subnet_set(server_tags=["xyz"], subnet_id=6, pool="2001:db8:3::1-2001:db8:3::10",
                subnet="2001:db8:3::/64", backend=backend)
    _subnet_set(server_tags=["all"], subnet_id=7, pool="2001:db8:2::1-2001:db8:2::10",
                subnet="2001:db8:2::/64", backend=backend)

    resp = _subnet_get(subnet_parameter={"id": 5}, backend=backend)
    _check_subnet_result(resp, server_tags=["abc", "xyz"], subnet_id=5)

    resp = _subnet_get(subnet_parameter={"id": 6}, backend=backend)
    _check_subnet_result(resp, server_tags=["xyz"], subnet_id=6, subnet="2001:db8:3::/64")

    resp = _subnet_get(command="remote-subnet6-get-by-prefix",
                       subnet_parameter={"subnet": "2001:db8:3::/64"}, backend=backend)
    _check_subnet_result(resp, server_tags=["xyz"], subnet_id=6, subnet="2001:db8:3::/64")

    resp = _subnet_get(command="remote-subnet6-get-by-prefix",
                       subnet_parameter={"subnet": "2001:db8:1::/64"}, backend=backend)
    _check_subnet_result(resp, server_tags=["abc", "xyz"], subnet_id=5)

    resp = _subnet_list(command="remote-subnet6-list", server_tags=["abc"], backend=backend)
    # not sure if this is how it suppose to work
    _check_subnet_result(resp, server_tags=["abc", "xyz"], count=2, subnet_id=5)

    resp = _subnet_list(command="remote-subnet6-list", server_tags=["xyz"], backend=backend)
    _check_subnet_result(resp, server_tags=["abc", "xyz"], count=3, subnet_id=5)
    assert resp["arguments"]["subnets"][1]["subnet"] == "2001:db8:3::/64"
    assert resp["arguments"]["subnets"][1]["id"] == 6
    assert resp["arguments"]["subnets"][2]["subnet"] == "2001:db8:2::/64"
    assert resp["arguments"]["subnets"][2]["id"] == 7


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_get_server_tags_all_incorrect_setup(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    # Configure 2 subnet with the same id but different tags will result with just one subnet in configuration
    # the first one will be overwritten
    _add_server_tag(backend, "abc")
    _add_server_tag(backend, "xyz")
    _subnet_set(server_tags=["abc"], subnet_id=5, pool="2001:db8:1::1-2001:db8:1::100", backend=backend)
    _subnet_set(server_tags=["xyz"], subnet_id=5, pool="2001:db8:1::1-2001:db8:1::10", backend=backend)

    resp = _subnet_get(subnet_parameter={"id": 5}, backend=backend)
    _check_subnet_result(resp, server_tags=["xyz"], subnet_id=5)


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_subnet6_del_server_tags(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    _add_server_tag(backend, "abc")
    _add_server_tag(backend, "xyz")
    _subnet_set(server_tags=["abc"], subnet_id=5, pool="2001:db8:1::1-2001:db8:1::100", backend=backend)
    _subnet_set(server_tags=["xyz"], subnet_id=6, pool="2001:db8:3::1-2001:db8:3::10", subnet="2001:db8:3::/64",
                backend=backend)
    _subnet_set(server_tags=["all"], subnet_id=7, pool="2001:db8:2::1-2001:db8:2::10", subnet="2001:db8:2::/64",
                backend=backend)

    resp = _subnet_get(subnet_parameter={"id": 5}, backend=backend)
    _check_subnet_result(resp, server_tags=["abc"], subnet_id=5)

    resp = _subnet_get(subnet_parameter={"id": 6}, backend=backend)
    _check_subnet_result(resp, server_tags=["xyz"], subnet_id=6, subnet="2001:db8:3::/64")

    resp = _subnet_get(subnet_parameter={"id": 7}, backend=backend)
    _check_subnet_result(resp, server_tags=["all"], subnet_id=7, subnet="2001:db8:2::/64")

    # we should delete just one
    resp = _subnet_del(subnet_parameter={"id": 6}, backend=backend)
    assert resp["arguments"]["count"] == 1
    assert resp["result"] == 0

    # since this one was just removed now we expect error
    resp = _subnet_del(subnet_parameter={"id": 6}, exp_result=3, backend=backend)
    assert resp["arguments"]["count"] == 0
    assert resp["result"] == 3

    # those two should still be configured
    resp = _subnet_get(subnet_parameter={"id": 5}, backend=backend)
    _check_subnet_result(resp, server_tags=["abc"], subnet_id=5)

    resp = _subnet_get(subnet_parameter={"id": 7}, backend=backend)
    _check_subnet_result(resp, server_tags=["all"], subnet_id=7, subnet="2001:db8:2::/64")

    resp = _subnet_del(subnet_parameter={"id": 7}, backend=backend)
    assert resp["arguments"]["count"] == 1
    assert resp["result"] == 0

    resp = _subnet_get(subnet_parameter={"id": 5}, backend=backend)
    _check_subnet_result(resp, server_tags=["abc"], subnet_id=5)

    resp = _subnet_get(subnet_parameter={"id": 7}, exp_result=3, backend=backend)
    assert resp["arguments"]["count"] == 0
    assert resp["result"] == 3


def _network_set(server_tags, backend, network_name="florX", exp_result=0):
    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": backend}, "server-tags": server_tags,
                                                         "shared-networks": [{"name": network_name}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)

    assert response == {"arguments": {"shared-networks": [{"name": network_name}]},
                        "result": 0, "text": "IPv6 shared network successfully set."}


def _network_get(backend, command="remote-network6-get", exp_result=0, network_parameter=None):
    cmd = dict(command=command, arguments={"remote": {"type": backend}})
    if network_parameter:
        cmd["arguments"]["shared-networks"] = [network_parameter]

    return srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)


def _network_list(backend, server_tags, exp_result=0):
    cmd = dict(command="remote-network6-list", arguments={"remote": {"type": backend}, "server-tags": server_tags})

    return srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)


def _network_del(backend, exp_result=0, network_parameter=None):
    return _network_get(command="remote-network6-del", backend=backend, exp_result=exp_result,
                        network_parameter=network_parameter)


def _network_check_res(resp, server_tags, count=1, network_name="florX"):
    assert resp["result"] == 0
    assert resp["arguments"]["count"] == count
    assert resp["arguments"]["shared-networks"][0]["metadata"] == {"server-tags": server_tags}
    assert resp["arguments"]["shared-networks"][0]["name"] == network_name


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_network6_server_tags_remove_server_tag_keep_data(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    _add_server_tag(backend, "abc")
    _add_server_tag(backend, "xyz")
    _network_set(server_tags=["abc"], backend=backend)
    _network_set(server_tags=["xyz"], network_name="flor1", backend=backend)
    _network_set(server_tags=["all"], network_name="top_flor", backend=backend)

    resp = _network_get(backend=backend, network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=["abc"], network_name="florX")

    resp = _network_get(backend=backend, network_parameter={"name": "flor1"})
    _network_check_res(resp, server_tags=["xyz"], network_name="flor1")

    cmd = dict(command="remote-server6-del", arguments={"remote": {"type": backend},
                                                        "servers": [{"server-tag": "abc"}]})
    srv_msg.send_ctrl_cmd(cmd)

    # Tag removed but network should exist
    resp = _network_get(backend=backend, network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=[], network_name="florX")

    # add back the same tag, make sure that network is still unassigned
    _add_server_tag(backend, "abc")
    resp = _network_get(backend=backend, network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=[], network_name="florX")

    # rest should be intact
    resp = _network_get(backend=backend, network_parameter={"name": "flor1"})
    _network_check_res(resp, server_tags=["xyz"], network_name="flor1")


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_network6_get_server_tags(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    _add_server_tag(backend, "abc")
    _add_server_tag(backend, "xyz")
    _network_set(server_tags=["abc"], backend=backend)
    _network_set(server_tags=["xyz"], network_name="flor1", backend=backend)
    _network_set(server_tags=["all"], network_name="top_flor", backend=backend)

    resp = _network_get(backend=backend, network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=["abc"], network_name="florX")

    resp = _network_get(backend=backend, network_parameter={"name": "flor1"})
    _network_check_res(resp, server_tags=["xyz"], network_name="flor1")

    resp = _network_list(backend, server_tags=["xyz"])
    _network_check_res(resp, server_tags=["xyz"], count=2, network_name="flor1")

    assert resp["arguments"]["shared-networks"][1]["metadata"] == {"server-tags": ["all"]}
    assert resp["arguments"]["shared-networks"][1]["name"] == "top_flor"


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_network6_get_server_tags_all_incorrect_setup(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    # Configure 2 networks with the same name but different tags will result with just one network in configuration
    # the first one will be overwritten
    _add_server_tag(backend, "abc")
    _add_server_tag(backend, "xyz")
    _network_set(server_tags=["abc"], backend=backend)
    _network_set(server_tags=["xyz"], backend=backend)

    resp = _network_get(backend=backend, network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=["xyz"], network_name="florX")


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_network6_del_server_tags(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    _add_server_tag(backend, "abc")
    _add_server_tag(backend, "xyz")
    _network_set(server_tags=["abc"], backend=backend)
    _network_set(server_tags=["xyz"], network_name="flor1", backend=backend)
    _network_set(server_tags=["all"], network_name="top_flor", backend=backend)

    resp = _network_get(backend=backend, network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=["abc"], network_name="florX")

    resp = _network_get(backend=backend, network_parameter={"name": "flor1"})
    _network_check_res(resp, server_tags=["xyz"], network_name="flor1")

    resp = _network_get(backend=backend, network_parameter={"name": "top_flor"})
    _network_check_res(resp, server_tags=["all"], network_name="top_flor")

    _network_del(backend=backend, network_parameter={"name": "flor1"})
    assert resp["arguments"]["count"] == 1
    assert resp["result"] == 0

    resp = _network_get(backend=backend, network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=["abc"], network_name="florX")

    # removed, so it should not be returned
    resp = _network_get(backend=backend, network_parameter={"name": "flor1"}, exp_result=3)
    assert resp["result"] == 3
    assert resp["arguments"]["count"] == 0

    resp = _network_get(backend=backend, network_parameter={"name": "top_flor"})
    _network_check_res(resp, server_tags=["all"], network_name="top_flor")

    resp = _network_del(backend=backend, network_parameter={"name": "top_flor"})
    assert resp["arguments"]["count"] == 1
    assert resp["result"] == 0

    resp = _network_get(backend=backend, network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=["abc"], network_name="florX")

    # removed, so it should not be returned
    resp = _network_get(backend=backend, network_parameter={"name": "top_flor"}, exp_result=3)
    assert resp["result"] == 3
    assert resp["arguments"]["count"] == 0


def _option_set(backend, server_tags, exp_result=0, code=23, opt_data="2001::1"):
    cmd = dict(command="remote-option6-global-set", arguments={"remote": {"type": backend},
                                                               "server-tags": server_tags,
                                                               "options": [{
                                                                   "code": code,
                                                                   "data": opt_data}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)

    assert response == {"result": 0, "text": "DHCPv6 option successfully set.",
                        "arguments": {"options": [{"code": code, "space": "dhcp6"}]}}


def _option_get(backend, server_tags, command="remote-option6-global-get-all", exp_result=0, opt_code=None):
    cmd = dict(command=command, arguments={"remote": {"type": backend},
                                           "server-tags": server_tags})

    if opt_code:
        cmd["arguments"]["options"] = [{"code": opt_code}]

    return srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)


def _option_del(backend, server_tags, exp_result=0, opt_code=None):
    return _option_get(command="remote-option6-global-del", backend=backend, server_tags=server_tags,
                       exp_result=exp_result, opt_code=opt_code)


def _check_option_result(resp, server_tags, count=1, opt_name=None, opt_data=None):
    assert resp["result"] == 0
    assert resp["arguments"]["count"] == count
    assert resp["arguments"]["options"][0]["metadata"] == {"server-tags": server_tags}
    assert resp["arguments"]["options"][0]["name"] == opt_name
    assert resp["arguments"]["options"][0]["data"] == opt_data


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option6_get_server_tags_all(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    # simple test for one ticket https://gitlab.isc.org/isc-projects/kea/issues/737
    _add_server_tag(backend, "abc")
    _option_set(backend, server_tags=["all"], opt_data='2001::3')
    resp = _option_get(backend, server_tags=["abc"], opt_code=23)
    _check_option_result(resp, count=1, server_tags=["all"], opt_name="dns-servers", opt_data="2001::3")


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_get_server_tags_get_non_existing_tag(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    # we will request option 23 from tag "abc" but it's was just configured for "all" which should be returned instead
    _add_server_tag(backend, "abc")
    _option_set(backend, server_tags=["all"])

    resp = _option_get(backend, server_tags=["abc"], opt_code=23)
    _check_option_result(resp, server_tags=["all"], opt_name="dns-servers", opt_data="2001::1")


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_remove_server_tag_and_data(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    _add_server_tag(backend, "abc")
    _option_set(backend, server_tags=["abc"])

    resp = _option_get(backend, server_tags=["abc"], opt_code=23)

    _check_option_result(resp, server_tags=["abc"], opt_name="dns-servers", opt_data="2001::1")

    cmd = dict(command="remote-server6-del", arguments={"remote": {"type": backend},
                                                        "servers": [{"server-tag": "abc"}]})
    srv_msg.send_ctrl_cmd(cmd)

    # after removing tag all options should be removed with it
    _option_get(backend, server_tags=["abc"], opt_code=23, exp_result=3)


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option6_get_server_tags(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    _add_server_tag(backend, "abc")
    _add_server_tag(backend, "xyz")
    _option_set(backend, server_tags=["abc"])
    _option_set(backend, server_tags=["xyz"], opt_data='2001::2')
    _option_set(backend, server_tags=["all"], opt_data='2001::3')

    resp = _option_get(backend, server_tags=["abc"], opt_code=23)
    _check_option_result(resp, server_tags=["abc"], opt_name="dns-servers", opt_data="2001::1")

    resp = _option_get(backend, server_tags=["xyz"], opt_code=23)
    _check_option_result(resp, server_tags=["xyz"], opt_name="dns-servers", opt_data="2001::2")

    resp = _option_get(backend, server_tags=["all"], opt_code=23)
    _check_option_result(resp, server_tags=["all"], opt_name="dns-servers", opt_data="2001::3")

    _option_set(backend, server_tags=["abc"], code=28, opt_data='2001::6')

    resp = _option_get(backend, server_tags=["abc"], opt_code=23)
    _check_option_result(resp, count=2, server_tags=["abc"], opt_name="dns-servers", opt_data="2001::1")
    assert resp["arguments"]["options"][1]["metadata"] == {"server-tags": ["abc"]}
    assert resp["arguments"]["options"][1]["name"] == "nisp-servers"
    assert resp["arguments"]["options"][1]["data"] == "2001::6"

    resp = _option_get(backend, server_tags=["xyz"], opt_code=23)
    _check_option_result(resp, count=1, server_tags=["xyz"], opt_name="dns-servers", opt_data="2001::2")


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option6_del_server_tags(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    _add_server_tag(backend, "abc")
    _add_server_tag(backend, "xyz")
    _option_set(backend, server_tags=["abc"])
    _option_set(backend, server_tags=["xyz"], opt_data='2001::2')
    _option_set(backend, server_tags=["all"], opt_data='2001::3')

    resp = _option_get(backend, server_tags=["abc"], opt_code=23)
    _check_option_result(resp, server_tags=["abc"], opt_name="dns-servers", opt_data="2001::1")

    resp = _option_get(backend, server_tags=["xyz"], opt_code=23)
    _check_option_result(resp, server_tags=["xyz"], opt_name="dns-servers", opt_data="2001::2")

    resp = _option_get(backend, server_tags=["all"], opt_code=23)
    _check_option_result(resp, server_tags=["all"], opt_name="dns-servers", opt_data="2001::3")

    resp = _option_del(backend, server_tags=["xyz"], opt_code=23)
    assert resp["arguments"]["count"] == 1
    assert resp["text"] == "1 DHCPv6 option(s) deleted."
    assert resp["result"] == 0

    resp = _option_get(backend, server_tags=["xyz"], opt_code=23)
    # it was removed but tag "all" should return option
    _check_option_result(resp, server_tags=["all"], opt_name="dns-servers", opt_data="2001::3")

    resp = _option_get(backend, server_tags=["abc"], opt_code=23)
    _check_option_result(resp, server_tags=["abc"], opt_name="dns-servers", opt_data="2001::1")

    resp = _option_get(backend, server_tags=["all"], opt_code=23)
    _check_option_result(resp, server_tags=["all"], opt_name="dns-servers", opt_data="2001::3")

    resp = _option_del(backend, server_tags=["abc"], opt_code=23)
    assert resp["arguments"]["count"] == 1
    assert resp["text"] == "1 DHCPv6 option(s) deleted."
    assert resp["result"] == 0

    # this also should be tag all
    resp = _option_get(backend, server_tags=["abc"], opt_code=23)
    _check_option_result(resp, server_tags=["all"], opt_name="dns-servers", opt_data="2001::3")

    # this should be from tag "all"
    resp = _option_get(backend, server_tags=["xyz"], opt_code=23)
    _check_option_result(resp, server_tags=["all"], opt_name="dns-servers", opt_data="2001::3")

    resp = _option_get(backend, server_tags=["all"], opt_code=23)
    _check_option_result(resp, server_tags=["all"], opt_name="dns-servers", opt_data="2001::3")

    resp = _option_get(backend=backend, command="remote-option6-global-del", server_tags=["all"], opt_code=23)
    assert resp["arguments"]["count"] == 1
    assert resp["text"] == "1 DHCPv6 option(s) deleted."
    assert resp["result"] == 0

    # now all commands should return error
    _option_get(backend, server_tags=["xyz"], opt_code=23, exp_result=3)

    _option_get(backend, server_tags=["abc"], opt_code=23, exp_result=3)

    resp = _option_get(backend, server_tags=["all"], opt_code=23, exp_result=3)
    assert resp["arguments"]["count"] == 0
    assert resp["result"] == 3


def _optdef_set(backend, server_tags, exp_result=0, opt_code=222, opt_name="foo", opt_type="uint32"):
    cmd = dict(command="remote-option-def6-set", arguments={"remote": {"type": backend},
                                                            "server-tags": server_tags,
                                                            "option-defs": [{
                                                                "name": opt_name,
                                                                "code": opt_code,
                                                                "type": opt_type}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)

    assert response == {"arguments": {"option-defs": [{"code": opt_code, "space": "dhcp6"}]},
                        "result": 0, "text": "DHCPv6 option definition successfully set."}


def _optdef_get(backend, server_tags, command="remote-option-def6-get", exp_result=0, option_def_parameter=None):
    cmd = dict(command=command, arguments={"remote": {"type": backend},
                                           "server-tags": server_tags})
    if option_def_parameter:
        cmd["arguments"]["option-defs"] = [option_def_parameter]

    return srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)


def _optdef_del(backend, server_tags, exp_result=0, option_def_parameter=None):
    return _optdef_get(backend, server_tags, command="remote-option-def6-del", exp_result=exp_result,
                       option_def_parameter=option_def_parameter)


def _check_optdef_result(resp, server_tags, count=1, opt_type="uint32", opt_name="foo", opt_code=222):
    assert resp["result"] == 0
    assert resp["arguments"]["count"] == count
    assert resp["arguments"]["option-defs"][0]["metadata"] == {"server-tags": server_tags}
    assert resp["arguments"]["option-defs"][0]["name"] == opt_name
    assert resp["arguments"]["option-defs"][0]["code"] == opt_code
    assert resp["arguments"]["option-defs"][0]["type"] == opt_type


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def_get_server_tags_tmp(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    # simple test for one ticket https://gitlab.isc.org/isc-projects/kea/issues/737
    _add_server_tag(backend, "abc")
    _optdef_set(backend, server_tags=["all"])
    resp = _optdef_get(backend=backend, command="remote-option-def6-get-all", server_tags=["abc"])
    _check_optdef_result(resp, server_tags=["all"], count=1)


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def_get_server_tags_get_non_existing_tag(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    _add_server_tag(backend, "abc")
    # let's make two definitions with the same name but different type and server tag, plus one different with
    # server tag "all"
    _optdef_set(backend, server_tags=["all"])

    resp = _optdef_get(backend, server_tags=["abc"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["all"])


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def_remove_server_tag_and_data(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    _add_server_tag(backend, "abc")
    _optdef_set(backend, server_tags=["abc"])

    resp = _optdef_get(backend, server_tags=["abc"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["abc"])

    cmd = dict(command="remote-server6-del", arguments={"remote": {"type": backend},
                                                        "servers": [{"server-tag": "abc"}]})
    srv_msg.send_ctrl_cmd(cmd)

    # after removing tag all option definition should be removed with it
    _optdef_get(backend=backend, command="remote-option-def6-get", server_tags=["abc"],
                option_def_parameter={"code": 222}, exp_result=3)


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def_get_server_tags(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    _add_server_tag(backend, "abc")
    _add_server_tag(backend, "xyz")
    # let's make two definitions with the same name but different type and server tag, plus one different with
    # server tag "all"
    _optdef_set(backend, server_tags=["abc"])
    _optdef_set(backend, server_tags=["xyz"], opt_type="string")
    _optdef_set(backend, server_tags=["all"], opt_code=233, opt_name="bar")

    resp = _optdef_get(backend, server_tags=["abc"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["abc"])

    resp = _optdef_get(backend, server_tags=["xyz"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["xyz"], opt_type="string")

    # this one should fail
    resp = _optdef_get(backend, server_tags=["all"],
                       option_def_parameter={"code": 222}, exp_result=3)
    assert resp["arguments"]["count"] == 0
    assert resp["result"] == 3

    resp = _optdef_get(backend, server_tags=["all"],
                       option_def_parameter={"code": 233})
    _check_optdef_result(resp, server_tags=["all"], opt_code=233, opt_name="bar")

    # let's check if -all will return list of two options for each tag and one option for "all"
    resp = _optdef_get(backend=backend, command="remote-option-def6-get-all", server_tags=["abc"])
    _check_optdef_result(resp, server_tags=["abc"], count=2)

    assert resp["arguments"]["option-defs"][1]["metadata"] == {"server-tags": ["all"]}
    assert resp["arguments"]["option-defs"][1]["name"] == "bar"
    assert resp["arguments"]["option-defs"][1]["code"] == 233

    resp = _optdef_get(backend=backend, command="remote-option-def6-get-all", server_tags=["xyz"])
    _check_optdef_result(resp, server_tags=["xyz"], count=2, opt_type="string")
    assert resp["arguments"]["option-defs"][1]["metadata"] == {"server-tags": ["all"]}
    assert resp["arguments"]["option-defs"][1]["name"] == "bar"
    assert resp["arguments"]["option-defs"][1]["code"] == 233

    resp = _optdef_get(backend=backend, command="remote-option-def6-get-all", server_tags=["all"])
    _check_optdef_result(resp, server_tags=["all"], opt_code=233, opt_name="bar")


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_remote_option_def_del_server_tags(backend):
    setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    _add_server_tag(backend, "abc")
    _add_server_tag(backend, "xyz")
    # we should be able to configure the same option for each tag, different type is for distinguish returns
    # options from "all" should be overwritten by specific tags on kea configuration level, not in db!
    _optdef_set(backend, server_tags=["abc"])
    _optdef_set(backend, server_tags=["xyz"], opt_type="string")
    _optdef_set(backend, server_tags=["all"], opt_type="uint8")

    resp = _optdef_get(backend, server_tags=["abc"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["abc"], count=1)

    resp = _optdef_get(backend, server_tags=["xyz"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["xyz"], opt_type="string", count=1)

    resp = _optdef_get(backend, server_tags=["all"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["all"], opt_type="uint8")

    # let's remove one option and see if all other stays
    _optdef_del(backend, ["all"], option_def_parameter={"code": 222})

    resp = _optdef_get(backend, server_tags=["abc"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["abc"])

    resp = _optdef_get(backend, server_tags=["xyz"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["xyz"], opt_type="string")

    resp = _optdef_get(backend, server_tags=["all"],
                       option_def_parameter={"code": 222}, exp_result=3)
    assert resp["arguments"]["count"] == 0
    assert resp["result"] == 3

    # same with -all command, we expect just one
    resp = _optdef_get(backend=backend, command="remote-option-def6-get-all", server_tags=["xyz"])
    _check_optdef_result(resp, server_tags=["xyz"], opt_type="string")

    resp = _optdef_get(backend=backend, command="remote-option-def6-get-all", server_tags=["xyz"])
    _check_optdef_result(resp, server_tags=["xyz"], opt_type="string")

    _optdef_del(backend, ["abc"], option_def_parameter={"code": 222})

    resp = _optdef_get(backend, server_tags=["abc"],
                       option_def_parameter={"code": 222}, exp_result=3)
    assert resp["arguments"]["count"] == 0
    assert resp["result"] == 3

    resp = _optdef_get(backend, server_tags=["xyz"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["xyz"], opt_type="string")
