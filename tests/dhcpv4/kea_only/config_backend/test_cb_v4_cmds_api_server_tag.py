"""Kea database config backend commands hook testing"""

import pytest
import srv_msg
from cb_model import setup_server_for_config_backend_cmds

pytestmark = [pytest.mark.py_test,
              pytest.mark.v4,
              pytest.mark.kea_only,
              pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.config_backend,
              pytest.mark.cb_cmds]


@pytest.fixture(autouse=True)
def run_around_tests():
    # we still can use server configured with one server tag
    setup_server_for_config_backend_cmds(server_tag="abc")


def _set_server_tag(tag="abc"):
    cmd = dict(command="remote-server4-set", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": tag,
                                                                     "description": "some server"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    assert response == {"result": 0, "text": "DHCPv4 server successfully set.",
                        "arguments": {"servers": [{"server-tag": tag, "description": "some server"}]}}


def test_remote_server_tag_set():
    _set_server_tag()


def test_remote_server_tag_set_any():
    cmd = dict(command="remote-server4-set", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": "any"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "'any' is reserved and must not be used as a server-tag"}


@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_remote_server_tag_set_missing_tag(channel):
    cmd = dict(command="remote-server4-set", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"description": "some server"}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel, exp_result=1)

    assert response == {"result": 1, "text": "missing 'server-tag' parameter"}


def test_remote_server_tag_set_incorrect_tag():
    cmd = dict(command="remote-server4-set", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": 123}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "'server-tag' parameter is not a string"}


def test_remote_server_tag_set_empty_tag():
    cmd = dict(command="remote-server4-set", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": ""}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "server-tag must not be empty"}


def test_remote_server_tag_set_missing_description():
    cmd = dict(command="remote-server4-set", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": "someserver"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    assert response == {"arguments": {"servers": [{"description": "", "server-tag": "someserver"}]},
                        "result": 0, "text": "DHCPv4 server successfully set."}


def test_remote_server_tag_set_missing_servers():
    cmd = dict(command="remote-server4-set", arguments={"remote": {"type": "mysql"}})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "'servers' parameter must be specified and must be a list"}


def test_remote_server_tag_set_empty_servers():
    cmd = dict(command="remote-server4-set", arguments={"remote": {"type": "mysql"},
                                                        "servers": []})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "'servers' list must include exactly one element"}


def test_remote_server_tag_set_multiple_servers():
    cmd = dict(command="remote-server4-set", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": "someserver"},
                                                                    {"server-tag": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "'servers' list must include exactly one element"}


def test_remote_server_tag_get():
    _set_server_tag()
    cmd = dict(command="remote-server4-get", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    assert response == {"arguments": {"count": 1, "servers": [{"description": "some server", "server-tag": "abc"}]},
                        "result": 0, "text": "DHCPv4 server 'abc' found."}


def test_remote_server_tag_get_non_existing_tag():
    cmd = dict(command="remote-server4-get", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "servers": []},
                        "result": 3, "text": "DHCPv4 server 'abc' not found."}


def test_remote_server_tag_get_empty_tag():
    _set_server_tag()
    cmd = dict(command="remote-server4-get", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": ""}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "server-tag must not be empty"}


def test_remote_server_tag_get_missing_tag():
    _set_server_tag()
    cmd = dict(command="remote-server4-get", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "missing 'server-tag' parameter"}


def test_remote_server_tag_del():
    _set_server_tag()
    cmd = dict(command="remote-server4-del", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv4 server(s) deleted."}

    cmd = dict(command="remote-server4-get", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "servers": []},
                        "result": 3, "text": "DHCPv4 server 'abc' not found."}


def test_remote_server_tag_del_all():
    _set_server_tag()
    cmd = dict(command="remote-server4-del", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": "all"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1,
                        "text": "'all' is a name reserved for the server tag which associates the configuration "
                                "elements with all servers connecting to the database and may not be deleted"}

    # "all" can't be -get
    # cmd = dict(command="remote-server4-get", arguments={"remote": {"type": "mysql"},
    #                                                     "servers": [{"server-tag": "all"}]})
    #
    # srv_msg.send_ctrl_cmd(cmd)


def test_remote_server_tag_del_non_existing_tag():
    cmd = dict(command="remote-server4-del", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 DHCPv4 server(s) deleted."}


def test_remote_server_tag_del_empty_tag():
    _set_server_tag()
    cmd = dict(command="remote-server4-del", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": ""}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "server-tag must not be empty"}


def test_remote_server_tag_del_missing_tag():
    _set_server_tag()
    cmd = dict(command="remote-server4-del", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "missing 'server-tag' parameter"}


def test_remote_server_tag_get_all():
    _set_server_tag()
    _set_server_tag(tag="xyz")
    cmd = dict(command="remote-server4-get-all", arguments={"remote": {"type": "mysql"}})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    assert response == {"arguments": {"count": 2,
                                      "servers": [{"description": "some server", "server-tag": "abc"},
                                                  {"description": "some server", "server-tag": "xyz"}]},
                        "result": 0, "text": "2 DHCPv4 server(s) found."}


def test_remote_server_tag_get_all_no_tags():
    cmd = dict(command="remote-server4-get-all", arguments={"remote": {"type": "mysql"}})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "servers": []}, "result": 3, "text": "0 DHCPv4 server(s) found."}


def test_remote_server_tag_get_all_one_tags():
    _set_server_tag()

    cmd = dict(command="remote-server4-get-all", arguments={"remote": {"type": "mysql"}})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    assert response == {"arguments": {"count": 1,
                                      "servers": [{"description": "some server", "server-tag": "abc"}]},
                        "result": 0, "text": "1 DHCPv4 server(s) found."}


def _add_server_tag(server_tag=None):
    cmd = dict(command="remote-server4-set", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": server_tag}]})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)


def _subnet_set(server_tags, subnet_id, pool, exp_result=0, subnet="192.168.50.0/24", ):
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": server_tags,
                                                        "subnets": [{"subnet": subnet, "id": subnet_id,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": pool}]}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)

    assert response == {"arguments": {"subnets": [{"id": subnet_id, "subnet": subnet}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}


def _subnet_get(command, exp_result=0, subnet_parameter=None):
    cmd = dict(command=command, arguments={"remote": {"type": "mysql"}})
    if subnet_parameter:
        cmd["arguments"]["subnets"] = [subnet_parameter]

    return srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)


def _subnet_list(command, server_tags, exp_result=0):
    cmd = dict(command=command, arguments={"remote": {"type": "mysql"}, "server-tags": server_tags})

    return srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)


def _subnet_del(exp_result=0, subnet_parameter=None):
    return _subnet_get("remote-subnet4-del-by-id", exp_result=exp_result, subnet_parameter=subnet_parameter)


def _check_subnet_result(resp, server_tags, count=1, subnet_id=5, subnet="192.168.50.0/24"):
    assert resp["result"] == 0
    assert resp["arguments"]["count"] == count
    assert resp["arguments"]["subnets"][0]["metadata"] == {"server-tags": server_tags}
    assert resp["arguments"]["subnets"][0]["subnet"] == subnet
    assert resp["arguments"]["subnets"][0]["id"] == subnet_id


def test_remote_subnet4_server_tags_delete_server_tag_keep_data():
    _add_server_tag("abc")
    _add_server_tag("xyz")
    _subnet_set(server_tags=["abc"], subnet_id=5, pool="192.168.50.1-192.168.50.100")
    _subnet_set(server_tags=["xyz"], subnet_id=6, pool="192.168.53.1-192.168.53.10", subnet="192.168.53.0/24")

    resp = _subnet_get(command="remote-subnet4-get-by-id", subnet_parameter={"id": 5})
    _check_subnet_result(resp, server_tags=["abc"], subnet_id=5)

    resp = _subnet_get(command="remote-subnet4-get-by-id", subnet_parameter={"id": 6})
    _check_subnet_result(resp, server_tags=["xyz"], subnet_id=6, subnet="192.168.53.0/24")

    cmd = dict(command="remote-server4-del", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": "abc"}]})
    srv_msg.send_ctrl_cmd(cmd)

    resp = _subnet_get(command="remote-subnet4-get-by-id", subnet_parameter={"id": 5})
    _check_subnet_result(resp, server_tags=[], subnet_id=5, subnet="192.168.50.0/24")

    _add_server_tag("abc")
    resp = _subnet_get(command="remote-subnet4-get-by-id", subnet_parameter={"id": 5})
    _check_subnet_result(resp, server_tags=[], subnet_id=5, subnet="192.168.50.0/24")

    resp = _subnet_get(command="remote-subnet4-get-by-id", subnet_parameter={"id": 6})
    _check_subnet_result(resp, server_tags=["xyz"], subnet_id=6, subnet="192.168.53.0/24")


def test_remote_subnet4_get_server_tags():
    _add_server_tag("abc")
    _add_server_tag("xyz")
    _subnet_set(server_tags=["abc", "xyz"], subnet_id=5, pool="192.168.50.1-192.168.50.100")
    _subnet_set(server_tags=["xyz"], subnet_id=6, pool="192.168.53.1-192.168.53.10", subnet="192.168.53.0/24")
    _subnet_set(server_tags=["all"], subnet_id=7, pool="192.168.51.1-192.168.51.10", subnet="192.168.51.0/24")

    resp = _subnet_get(command="remote-subnet4-get-by-id", subnet_parameter={"id": 5})
    _check_subnet_result(resp, server_tags=["abc", "xyz"], subnet_id=5)

    resp = _subnet_get(command="remote-subnet4-get-by-id", subnet_parameter={"id": 6})
    _check_subnet_result(resp, server_tags=["xyz"], subnet_id=6, subnet="192.168.53.0/24")

    resp = _subnet_get(command="remote-subnet4-get-by-prefix",
                       subnet_parameter={"subnet": "192.168.53.0/24"})
    _check_subnet_result(resp, server_tags=["xyz"], subnet_id=6, subnet="192.168.53.0/24")

    resp = _subnet_get(command="remote-subnet4-get-by-prefix",
                       subnet_parameter={"subnet": "192.168.50.0/24"})
    _check_subnet_result(resp, server_tags=["abc", "xyz"], subnet_id=5)

    resp = _subnet_list(command="remote-subnet4-list", server_tags=["abc"])
    # not sure if this is how it suppose to work
    _check_subnet_result(resp, server_tags=["abc", "xyz"], count=2, subnet_id=5)

    resp = _subnet_list(command="remote-subnet4-list", server_tags=["xyz"])
    _check_subnet_result(resp, server_tags=["abc", "xyz"], count=3, subnet_id=5)
    assert resp["arguments"]["subnets"][1]["subnet"] == "192.168.53.0/24"
    assert resp["arguments"]["subnets"][1]["id"] == 6
    assert resp["arguments"]["subnets"][2]["subnet"] == "192.168.51.0/24"
    assert resp["arguments"]["subnets"][2]["id"] == 7


def test_remote_subnet4_get_server_tags_all_incorrect_setup():
    # Configure 2 subnet with the same id but different tags will result with just one subnet in configuration
    # the first one will be overwritten
    _add_server_tag("abc")
    _add_server_tag("xyz")
    _subnet_set(server_tags=["abc"], subnet_id=5, pool="192.168.50.1-192.168.50.100")
    _subnet_set(server_tags=["xyz"], subnet_id=5, pool="192.168.50.1-192.168.50.10")

    resp = _subnet_get(command="remote-subnet4-get-by-id", subnet_parameter={"id": 5})
    _check_subnet_result(resp, server_tags=["xyz"], subnet_id=5)


def test_remote_subnet4_del_server_tags():
    _add_server_tag("abc")
    _add_server_tag("xyz")
    _subnet_set(server_tags=["abc"], subnet_id=5, pool="192.168.50.1-192.168.50.100")
    _subnet_set(server_tags=["xyz"], subnet_id=6, pool="192.168.53.1-192.168.53.10", subnet="192.168.53.0/24")
    _subnet_set(server_tags=["all"], subnet_id=7, pool="192.168.51.1-192.168.51.10", subnet="192.168.51.0/24")

    resp = _subnet_get(command="remote-subnet4-get-by-id", subnet_parameter={"id": 5})
    _check_subnet_result(resp, server_tags=["abc"], subnet_id=5)

    resp = _subnet_get(command="remote-subnet4-get-by-id", subnet_parameter={"id": 6})
    _check_subnet_result(resp, server_tags=["xyz"], subnet_id=6, subnet="192.168.53.0/24")

    resp = _subnet_get(command="remote-subnet4-get-by-id", subnet_parameter={"id": 7})
    _check_subnet_result(resp, server_tags=["all"], subnet_id=7, subnet="192.168.51.0/24")

    # we should delete just one
    resp = _subnet_del(subnet_parameter={"id": 6})
    assert resp["arguments"]["count"] == 1
    assert resp["result"] == 0

    # since this one was just removed now we expect error
    resp = _subnet_del(subnet_parameter={"id": 6}, exp_result=3)
    assert resp["arguments"]["count"] == 0
    assert resp["result"] == 3

    # those two should still be configured
    resp = _subnet_get(command="remote-subnet4-get-by-id", subnet_parameter={"id": 5})
    _check_subnet_result(resp, server_tags=["abc"], subnet_id=5)

    resp = _subnet_get(command="remote-subnet4-get-by-id", subnet_parameter={"id": 7})
    _check_subnet_result(resp, server_tags=["all"], subnet_id=7, subnet="192.168.51.0/24")

    resp = _subnet_del(subnet_parameter={"id": 7})
    assert resp["arguments"]["count"] == 1
    assert resp["result"] == 0

    resp = _subnet_get(command="remote-subnet4-get-by-id", subnet_parameter={"id": 5})
    _check_subnet_result(resp, server_tags=["abc"], subnet_id=5)

    resp = _subnet_get(command="remote-subnet4-get-by-id", subnet_parameter={"id": 7}, exp_result=3)
    assert resp["arguments"]["count"] == 0
    assert resp["result"] == 3


def _network_set(server_tags, network_name="florX", exp_result=0):
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"}, "server-tags": server_tags,
                                                         "shared-networks": [{"name": network_name}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)

    assert response == {"arguments": {"shared-networks": [{"name": network_name}]},
                        "result": 0, "text": "IPv4 shared network successfully set."}


def _network_get(command, exp_result=0, network_parameter=None):
    cmd = dict(command=command, arguments={"remote": {"type": "mysql"}})
    if network_parameter:
        cmd["arguments"]["shared-networks"] = [network_parameter]

    return srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)


def _network_list(command, server_tags, exp_result=0):
    cmd = dict(command=command, arguments={"remote": {"type": "mysql"}, "server-tags": server_tags})

    return srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)


def _network_del(exp_result=0, network_parameter=None):
    return _network_get("remote-network4-del", exp_result=exp_result, network_parameter=network_parameter)


def _network_check_res(resp, server_tags, count=1, network_name="florX"):
    assert resp["result"] == 0
    assert resp["arguments"]["count"] == count
    assert resp["arguments"]["shared-networks"][0]["metadata"] == {"server-tags": server_tags}
    assert resp["arguments"]["shared-networks"][0]["name"] == network_name


def test_remote_network4_server_tags_remove_server_tag_keep_data():
    _add_server_tag("abc")
    _add_server_tag("xyz")
    _network_set(server_tags=["abc"])
    _network_set(server_tags=["xyz"], network_name="flor1")
    _network_set(server_tags=["all"], network_name="top_flor")

    resp = _network_get(command="remote-network4-get", network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=["abc"], network_name="florX")

    resp = _network_get(command="remote-network4-get", network_parameter={"name": "flor1"})
    _network_check_res(resp, server_tags=["xyz"], network_name="flor1")

    cmd = dict(command="remote-server4-del", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": "abc"}]})
    srv_msg.send_ctrl_cmd(cmd)

    # Tag removed but network should exist
    resp = _network_get(command="remote-network4-get", network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=[], network_name="florX")

    # add back the same tag, make sure that network is still unassigned
    _add_server_tag("abc")
    resp = _network_get(command="remote-network4-get", network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=[], network_name="florX")

    # rest should be intact
    resp = _network_get(command="remote-network4-get", network_parameter={"name": "flor1"})
    _network_check_res(resp, server_tags=["xyz"], network_name="flor1")


def test_remote_network4_get_server_tags():
    _add_server_tag("abc")
    _add_server_tag("xyz")
    _network_set(server_tags=["abc"])
    _network_set(server_tags=["xyz"], network_name="flor1")
    _network_set(server_tags=["all"], network_name="top_flor")

    resp = _network_get(command="remote-network4-get", network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=["abc"], network_name="florX")

    resp = _network_get(command="remote-network4-get", network_parameter={"name": "flor1"})
    _network_check_res(resp, server_tags=["xyz"], network_name="flor1")

    resp = _network_list(command="remote-network4-list", server_tags=["xyz"])
    _network_check_res(resp, server_tags=["xyz"], count=2, network_name="flor1")

    assert resp["arguments"]["shared-networks"][1]["metadata"] == {"server-tags": ["all"]}
    assert resp["arguments"]["shared-networks"][1]["name"] == "top_flor"


def test_remote_network4_get_server_tags_all_incorrect_setup():
    # Configure 2 networks with the same name but different tags will result with just one network in configuration
    # the first one will be overwritten
    _add_server_tag("abc")
    _add_server_tag("xyz")
    _network_set(server_tags=["abc"])
    _network_set(server_tags=["xyz"])

    resp = _network_get(command="remote-network4-get", network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=["xyz"], network_name="florX")


def test_remote_network4_del_server_tags():
    _add_server_tag("abc")
    _add_server_tag("xyz")
    _network_set(server_tags=["abc"])
    _network_set(server_tags=["xyz"], network_name="flor1")
    _network_set(server_tags=["all"], network_name="top_flor")

    resp = _network_get(command="remote-network4-get", network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=["abc"], network_name="florX")

    resp = _network_get(command="remote-network4-get", network_parameter={"name": "flor1"})
    _network_check_res(resp, server_tags=["xyz"], network_name="flor1")

    resp = _network_get(command="remote-network4-get", network_parameter={"name": "top_flor"})
    _network_check_res(resp, server_tags=["all"], network_name="top_flor")

    _network_del(network_parameter={"name": "flor1"})
    assert resp["arguments"]["count"] == 1
    assert resp["result"] == 0

    resp = _network_get(command="remote-network4-get", network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=["abc"], network_name="florX")

    # removed, so it should not be returned
    resp = _network_get(command="remote-network4-get", network_parameter={"name": "flor1"}, exp_result=3)
    assert resp["result"] == 3
    assert resp["arguments"]["count"] == 0

    resp = _network_get(command="remote-network4-get", network_parameter={"name": "top_flor"})
    _network_check_res(resp, server_tags=["all"], network_name="top_flor")

    resp = _network_del(network_parameter={"name": "top_flor"})
    assert resp["arguments"]["count"] == 1
    assert resp["result"] == 0

    resp = _network_get(command="remote-network4-get", network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=["abc"], network_name="florX")

    # removed, so it should not be returned
    resp = _network_get(command="remote-network4-get", network_parameter={"name": "top_flor"}, exp_result=3)
    assert resp["result"] == 3
    assert resp["arguments"]["count"] == 0


def _option_set(server_tags, exp_result=0, code=3, opt_data="1.1.1.1"):
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": server_tags,
                                                               "options": [{
                                                                   "code": code,
                                                                   "data": opt_data}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)

    assert response == {"result": 0, "text": "DHCPv4 option successfully set.",
                        "arguments": {"options": [{"code": code, "space": "dhcp4"}]}}


def _option_get(command, server_tags, exp_result=0, opt_code=None):
    cmd = dict(command=command, arguments={"remote": {"type": "mysql"},
                                           "server-tags": server_tags})

    if opt_code:
        cmd["arguments"]["options"] = [{"code": opt_code}]

    return srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)


def _option_del(server_tags, exp_result=0, opt_code=None):
    return _option_get("remote-option4-global-del", server_tags=server_tags, exp_result=exp_result, opt_code=opt_code)


def _check_option_result(resp, server_tags, count=1, opt_name=None, opt_data=None):
    assert resp["result"] == 0
    assert resp["arguments"]["count"] == count
    assert resp["arguments"]["options"][0]["metadata"] == {"server-tags": server_tags}
    assert resp["arguments"]["options"][0]["name"] == opt_name
    assert resp["arguments"]["options"][0]["data"] == opt_data


def test_remote_option4_get_server_tags_all():
    # simple test for one ticket https://gitlab.isc.org/isc-projects/kea/issues/737
    _add_server_tag("abc")
    _option_set(server_tags=["all"], opt_data='3.3.3.3')
    resp = _option_get(command="remote-option4-global-get-all", server_tags=["abc"], opt_code=3)
    _check_option_result(resp, count=1, server_tags=["all"], opt_name="routers", opt_data="3.3.3.3")


def test_remote_option_get_server_tags_get_non_existing_tag():
    # we will request option 3 from tag "abc" but it's was just configured for "all" which should be returned instead
    _add_server_tag("abc")
    _option_set(server_tags=["all"])

    resp = _option_get(command="remote-option4-global-get", server_tags=["abc"], opt_code=3)
    _check_option_result(resp, server_tags=["all"], opt_name="routers", opt_data="1.1.1.1")


def test_remote_option_remove_server_tag_and_data():
    _add_server_tag("abc")
    _option_set(server_tags=["abc"])

    resp = _option_get(command="remote-option4-global-get", server_tags=["abc"], opt_code=3)

    _check_option_result(resp, server_tags=["abc"], opt_name="routers", opt_data="1.1.1.1")

    cmd = dict(command="remote-server4-del", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": "abc"}]})
    srv_msg.send_ctrl_cmd(cmd)

    # after removing tag all options should be removed with it
    _option_get(command="remote-option4-global-get", server_tags=["abc"], opt_code=3, exp_result=3)


def test_remote_option4_get_server_tags():
    _add_server_tag("abc")
    _add_server_tag("xyz")
    _option_set(server_tags=["abc"])
    _option_set(server_tags=["xyz"], opt_data='2.2.2.2')
    _option_set(server_tags=["all"], opt_data='3.3.3.3')

    resp = _option_get(command="remote-option4-global-get", server_tags=["abc"], opt_code=3)
    _check_option_result(resp, server_tags=["abc"], opt_name="routers", opt_data="1.1.1.1")

    resp = _option_get(command="remote-option4-global-get", server_tags=["xyz"], opt_code=3)
    _check_option_result(resp, server_tags=["xyz"], opt_name="routers", opt_data="2.2.2.2")

    resp = _option_get(command="remote-option4-global-get", server_tags=["all"], opt_code=3)
    _check_option_result(resp, server_tags=["all"], opt_name="routers", opt_data="3.3.3.3")

    _option_set(server_tags=["abc"], code=4, opt_data='6.6.6.6')

    resp = _option_get(command="remote-option4-global-get-all", server_tags=["abc"], opt_code=3)
    _check_option_result(resp, count=2, server_tags=["abc"], opt_name="routers", opt_data="1.1.1.1")
    assert resp["arguments"]["options"][1]["metadata"] == {"server-tags": ["abc"]}
    assert resp["arguments"]["options"][1]["name"] == "time-servers"
    assert resp["arguments"]["options"][1]["data"] == "6.6.6.6"

    resp = _option_get(command="remote-option4-global-get-all", server_tags=["xyz"], opt_code=3)
    _check_option_result(resp, count=1, server_tags=["xyz"], opt_name="routers", opt_data="2.2.2.2")


def test_remote_option4_del_server_tags():
    _add_server_tag("abc")
    _add_server_tag("xyz")
    _option_set(server_tags=["abc"])
    _option_set(server_tags=["xyz"], opt_data='2.2.2.2')
    _option_set(server_tags=["all"], opt_data='3.3.3.3')

    resp = _option_get(command="remote-option4-global-get", server_tags=["abc"], opt_code=3)
    _check_option_result(resp, server_tags=["abc"], opt_name="routers", opt_data="1.1.1.1")

    resp = _option_get(command="remote-option4-global-get", server_tags=["xyz"], opt_code=3)
    _check_option_result(resp, server_tags=["xyz"], opt_name="routers", opt_data="2.2.2.2")

    resp = _option_get(command="remote-option4-global-get", server_tags=["all"], opt_code=3)
    _check_option_result(resp, server_tags=["all"], opt_name="routers", opt_data="3.3.3.3")

    resp = _option_del(server_tags=["xyz"], opt_code=3)
    assert resp["arguments"]["count"] == 1
    assert resp["text"] == "1 DHCPv4 option(s) deleted."
    assert resp["result"] == 0

    resp = _option_get(command="remote-option4-global-get", server_tags=["xyz"], opt_code=3)
    # it was removed but tag "all" should return option
    _check_option_result(resp, server_tags=["all"], opt_name="routers", opt_data="3.3.3.3")

    resp = _option_get(command="remote-option4-global-get", server_tags=["abc"], opt_code=3)
    _check_option_result(resp, server_tags=["abc"], opt_name="routers", opt_data="1.1.1.1")

    resp = _option_get(command="remote-option4-global-get", server_tags=["all"], opt_code=3)
    _check_option_result(resp, server_tags=["all"], opt_name="routers", opt_data="3.3.3.3")

    resp = _option_del(server_tags=["abc"], opt_code=3)
    assert resp["arguments"]["count"] == 1
    assert resp["text"] == "1 DHCPv4 option(s) deleted."
    assert resp["result"] == 0

    # this also should be tag all
    resp = _option_get(command="remote-option4-global-get", server_tags=["abc"], opt_code=3)
    _check_option_result(resp, server_tags=["all"], opt_name="routers", opt_data="3.3.3.3")

    # this should be from tag "all"
    resp = _option_get(command="remote-option4-global-get", server_tags=["xyz"], opt_code=3)
    _check_option_result(resp, server_tags=["all"], opt_name="routers", opt_data="3.3.3.3")

    resp = _option_get(command="remote-option4-global-get", server_tags=["all"], opt_code=3)
    _check_option_result(resp, server_tags=["all"], opt_name="routers", opt_data="3.3.3.3")

    resp = _option_get(command="remote-option4-global-del", server_tags=["all"], opt_code=3)
    assert resp["arguments"]["count"] == 1
    assert resp["text"] == "1 DHCPv4 option(s) deleted."
    assert resp["result"] == 0

    # now all commands should return error
    _option_get(command="remote-option4-global-get", server_tags=["xyz"], opt_code=3, exp_result=3)

    _option_get(command="remote-option4-global-get", server_tags=["abc"], opt_code=3, exp_result=3)

    resp = _option_get(command="remote-option4-global-get", server_tags=["all"], opt_code=3, exp_result=3)
    assert resp["arguments"]["count"] == 0
    assert resp["result"] == 3


def _optdef_set(server_tags, exp_result=0, opt_code=222, opt_name="foo", opt_type="uint32"):
    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": server_tags,
                                                            "option-defs": [{
                                                                "name": opt_name,
                                                                "code": opt_code,
                                                                "type": opt_type}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)

    assert response == {"arguments": {"option-defs": [{"code": opt_code, "space": "dhcp4"}]},
                        "result": 0, "text": "DHCPv4 option definition successfully set."}


def _optdef_get(command, server_tags, exp_result=0, option_def_parameter=None):
    cmd = dict(command=command, arguments={"remote": {"type": "mysql"},
                                           "server-tags": server_tags})
    if option_def_parameter:
        cmd["arguments"]["option-defs"] = [option_def_parameter]

    return srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)


def _optdef_del(server_tags, exp_result=0, option_def_parameter=None):
    return _optdef_get("remote-option-def4-del", server_tags, exp_result=exp_result,
                       option_def_parameter=option_def_parameter)


def _check_optdef_result(resp, server_tags, count=1, opt_type="uint32", opt_name="foo", opt_code=222):
    assert resp["result"] == 0
    assert resp["arguments"]["count"] == count
    assert resp["arguments"]["option-defs"][0]["metadata"] == {"server-tags": server_tags}
    assert resp["arguments"]["option-defs"][0]["name"] == opt_name
    assert resp["arguments"]["option-defs"][0]["code"] == opt_code
    assert resp["arguments"]["option-defs"][0]["type"] == opt_type


def test_remote_option_def_get_server_tags_tmp():
    # simple test for one ticket https://gitlab.isc.org/isc-projects/kea/issues/737
    _add_server_tag("abc")
    _optdef_set(server_tags=["all"])
    resp = _optdef_get(command="remote-option-def4-get-all", server_tags=["abc"])
    _check_optdef_result(resp, server_tags=["all"], count=1)


def test_remote_option_def_get_server_tags_get_non_existing_tag():
    _add_server_tag("abc")
    # let's make two definitions with the same name but different type and server tag, plus one different with
    # server tag "all"
    _optdef_set(server_tags=["all"])

    resp = _optdef_get(command="remote-option-def4-get", server_tags=["abc"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["all"])


def test_remote_option_def_remove_server_tag_and_data():
    _add_server_tag("abc")
    _optdef_set(server_tags=["abc"])

    resp = _optdef_get(command="remote-option-def4-get", server_tags=["abc"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["abc"])

    cmd = dict(command="remote-server4-del", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": "abc"}]})
    srv_msg.send_ctrl_cmd(cmd)

    # after removing tag all option definition should be removed with it
    _optdef_get(command="remote-option-def4-get", server_tags=["abc"], option_def_parameter={"code": 222},
                exp_result=3)


def test_remote_option_def_get_server_tags():
    _add_server_tag("abc")
    _add_server_tag("xyz")
    # let's make two definitions with the same name but different type and server tag, plus one different with
    # server tag "all"
    _optdef_set(server_tags=["abc"])
    _optdef_set(server_tags=["xyz"], opt_type="string")
    _optdef_set(server_tags=["all"], opt_code=233, opt_name="bar")

    resp = _optdef_get(command="remote-option-def4-get", server_tags=["abc"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["abc"])

    resp = _optdef_get(command="remote-option-def4-get", server_tags=["xyz"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["xyz"], opt_type="string")

    # this one should fail
    resp = _optdef_get(command="remote-option-def4-get", server_tags=["all"],
                       option_def_parameter={"code": 222}, exp_result=3)
    assert resp["arguments"]["count"] == 0
    assert resp["result"] == 3

    resp = _optdef_get(command="remote-option-def4-get", server_tags=["all"],
                       option_def_parameter={"code": 233})
    _check_optdef_result(resp, server_tags=["all"], opt_code=233, opt_name="bar")

    # let's check if -all will return list of two options for each tag and one option for "all"
    resp = _optdef_get(command="remote-option-def4-get-all", server_tags=["abc"])
    _check_optdef_result(resp, server_tags=["abc"], count=2)

    assert resp["arguments"]["option-defs"][1]["metadata"] == {"server-tags": ["all"]}
    assert resp["arguments"]["option-defs"][1]["name"] == "bar"
    assert resp["arguments"]["option-defs"][1]["code"] == 233

    resp = _optdef_get(command="remote-option-def4-get-all", server_tags=["xyz"])
    _check_optdef_result(resp, server_tags=["xyz"], count=2, opt_type="string")
    assert resp["arguments"]["option-defs"][1]["metadata"] == {"server-tags": ["all"]}
    assert resp["arguments"]["option-defs"][1]["name"] == "bar"
    assert resp["arguments"]["option-defs"][1]["code"] == 233

    resp = _optdef_get(command="remote-option-def4-get-all", server_tags=["all"])
    _check_optdef_result(resp, server_tags=["all"], opt_code=233, opt_name="bar")


def test_remote_option_def_del_server_tags():
    _add_server_tag("abc")
    _add_server_tag("xyz")
    # we should be able to configure the same option for each tag, different type is for distinguish returns
    # options from "all" should be overwritten by specific tags on kea configuration level, not in db!
    _optdef_set(server_tags=["abc"])
    _optdef_set(server_tags=["xyz"], opt_type="string")
    _optdef_set(server_tags=["all"], opt_type="uint8")

    resp = _optdef_get(command="remote-option-def4-get", server_tags=["abc"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["abc"], count=1)

    resp = _optdef_get(command="remote-option-def4-get", server_tags=["xyz"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["xyz"], opt_type="string", count=1)

    resp = _optdef_get(command="remote-option-def4-get", server_tags=["all"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["all"], opt_type="uint8")

    # let's remove one option and see if all other stays
    _optdef_del(["all"], option_def_parameter={"code": 222})

    resp = _optdef_get(command="remote-option-def4-get", server_tags=["abc"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["abc"])

    resp = _optdef_get(command="remote-option-def4-get", server_tags=["xyz"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["xyz"], opt_type="string")

    resp = _optdef_get(command="remote-option-def4-get", server_tags=["all"],
                       option_def_parameter={"code": 222}, exp_result=3)
    assert resp["arguments"]["count"] == 0
    assert resp["result"] == 3

    # same with -all command, we expect just one
    resp = _optdef_get(command="remote-option-def4-get-all", server_tags=["xyz"])
    _check_optdef_result(resp, server_tags=["xyz"], opt_type="string")

    resp = _optdef_get(command="remote-option-def4-get-all", server_tags=["xyz"])
    _check_optdef_result(resp, server_tags=["xyz"], opt_type="string")

    _optdef_del(["abc"], option_def_parameter={"code": 222})

    resp = _optdef_get(command="remote-option-def4-get", server_tags=["abc"],
                       option_def_parameter={"code": 222}, exp_result=3)
    assert resp["arguments"]["count"] == 0
    assert resp["result"] == 3

    resp = _optdef_get(command="remote-option-def4-get", server_tags=["xyz"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["xyz"], opt_type="string")
