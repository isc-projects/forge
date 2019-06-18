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
    setup_server_for_config_backend_cmds()


def _subnet_set(server_tags, subnet_id, pool, subnet="192.168.50.0/24"):
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": server_tags,
                                                        "subnets": [{"subnet": subnet, "id": subnet_id,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": pool}]}]})
    response = srv_msg.send_request('v4', cmd)

    assert response == {"arguments": {"subnets": [{"id": subnet_id, "subnet": subnet}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}


def _subnet_get(command, server_tags, subnet_parameter=None):
    cmd = dict(command=command, arguments={"remote": {"type": "mysql"},
                                           "server-tags": server_tags})
    if subnet_parameter:
        cmd["arguments"]["subnets"] = [subnet_parameter]

    return srv_msg.send_request('v4', cmd)


def _subnet_del(server_tags, subnet_parameter=None):
    return _subnet_get("remote-subnet4-del", server_tags, subnet_parameter)


def _check_subnet_result(resp, server_tags, count=1, subnet_id=5, subnet="192.168.50.0/24"):
    assert resp["result"] == 0
    assert resp["arguments"]["count"] == count
    assert resp["arguments"]["subnets"][0]["metadata"] == {"server-tag": server_tags}
    assert resp["arguments"]["subnets"][0]["subnet"] == subnet
    assert resp["arguments"]["subnets"][0]["id"] == subnet_id


def test_remote_subnet4_get_server_tags():
    _subnet_set(server_tags=["abc"], subnet_id=5, pool="192.168.50.1-192.168.50.100")
    _subnet_set(server_tags=["xzy"], subnet_id=6, pool="192.168.50.1-192.168.50.10")
    _subnet_set(server_tags=["all"], subnet_id=7, pool="192.168.51.1-192.168.51.10", subnet="192.168.51.0/24")

    resp = _subnet_get(command="remote-subnet4-get-by-id", server_tags=["abc"], subnet_parameter={"id": 5})
    _check_subnet_result(resp, server_tags=["abc"], subnet_id=5)

    resp = _subnet_get(command="remote-subnet4-get-by-id", server_tags=["xyz"], subnet_parameter={"id": 6})
    _check_subnet_result(resp, server_tags=["xyz"], subnet_id=6)

    resp = _subnet_get(command="remote-subnet4-get-by-prefix", server_tags=["xyz"],
                       subnet_parameter={"subnet": "192.168.50.0/24"})
    _check_subnet_result(resp, server_tags=["xyz"], subnet_id=6)

    resp = _subnet_get(command="remote-subnet4-get-by-prefix", server_tags=["abc"],
                       subnet_parameter={"subnet": "192.168.50.0/24"})
    _check_subnet_result(resp, server_tags=["abc"], subnet_id=5)

    resp = _subnet_get(command="remote-subnet4-list", server_tags=["abc"])
    # not sure if this is how it suppose to work
    _check_subnet_result(resp, server_tags=["abc"], count=2, subnet_id=5)
    assert resp["arguments"]["subnets"][1]["metadata"] == {"server-tag": "all"}
    # TODO not sure if that will be on the list
    assert resp["arguments"]["subnets"][1]["subnet"] == "192.168.51.0/24"
    assert resp["arguments"]["subnets"][1]["id"] == 7

    resp = _subnet_get(command="remote-subnet4-list", server_tags=["xyz"])
    _check_subnet_result(resp, server_tags=["xyz"], count=2, subnet_id=6)
    assert resp["arguments"]["subnets"][1]["metadata"] == {"server-tag": "all"}
    # TODO not sure if that will be on the list
    assert resp["arguments"]["subnets"][1]["subnet"] == "192.168.51.0/24"
    assert resp["arguments"]["subnets"][1]["id"] == 7


def test_remote_subnet4_get_server_tags_all_incorrect_setup():
    # Configure 2 subnet with the same id but different tags will result with just one subnet in configuration
    # the first one will be overwritten
    _subnet_set(server_tags=["abc"], subnet_id=5, pool="192.168.50.1-192.168.50.100")
    _subnet_set(server_tags=["xyz"], subnet_id=5, pool="192.168.50.1-192.168.50.10")

    resp = _subnet_get(command="remote-subnet4-get-by-id", server_tags=["abc"], subnet_parameter={"id": 5})
    assert resp["result"] == 3
    assert resp["arguments"]["count"] == 0

    resp = _subnet_get(command="remote-subnet4-get-by-id", server_tags=["xyz"], subnet_parameter={"id": 5})
    _check_subnet_result(resp, server_tags=["xyz"], subnet_id=5)


def test_remote_subnet4_del_server_tags():
    _subnet_set(server_tags=["abc"], subnet_id=5, pool="192.168.50.1-192.168.50.100")
    _subnet_set(server_tags=["xzy"], subnet_id=6, pool="192.168.50.1-192.168.50.10")
    _subnet_set(server_tags=["all"], subnet_id=7, pool="192.168.51.1-192.168.51.10", subnet="192.168.51.0/24")

    resp = _subnet_get(command="remote-subnet4-get-by-id", server_tags=["abc"], subnet_parameter={"id": 5})
    _check_subnet_result(resp, server_tags=["abc"], subnet_id=5)

    resp = _subnet_get(command="remote-subnet4-get-by-id", server_tags=["xyz"], subnet_parameter={"id": 6})
    _check_subnet_result(resp, server_tags=["xyz"], subnet_id=6)

    resp = _subnet_get(command="remote-subnet4-get-by-id", server_tags=["all"], subnet_parameter={"id": 7})
    _check_subnet_result(resp, server_tags=["all"], subnet_id=7, subnet="192.168.51.0/24")

    # we should delete just one
    resp = _subnet_del(server_tags=["xyz"], subnet_parameter={"id": 6})
    assert resp["arguments"]["count"] == 1
    assert resp["result"] == 0

    # since this one was just removed now we expect error
    resp = _subnet_del(server_tags=["xyz"], subnet_parameter={"id": 6})
    assert resp["arguments"]["count"] == 0
    assert resp["result"] == 3

    # those two should still be configured
    resp = _subnet_get(command="remote-subnet4-get-by-id", server_tags=["abc"], subnet_parameter={"id": 5})
    _check_subnet_result(resp, server_tags=["abc"], subnet_id=5)

    resp = _subnet_get(command="remote-subnet4-get-by-id", server_tags=["all"], subnet_parameter={"id": 7})
    _check_subnet_result(resp, server_tags=["all"], subnet_id=7, subnet="192.168.51.0/24")

    resp = _subnet_del(server_tags=["all"], subnet_parameter={"id": 7})
    assert resp["arguments"]["count"] == 1
    assert resp["result"] == 0

    resp = _subnet_get(command="remote-subnet4-get-by-id", server_tags=["abc"], subnet_parameter={"id": 5})
    _check_subnet_result(resp, server_tags=["abc"], subnet_id=5)

    resp = _subnet_get(command="remote-subnet4-get-by-id", server_tags=["all"], subnet_parameter={"id": 7})
    assert resp["arguments"]["count"] == 0
    assert resp["result"] == 3


def _network_set(server_tags, network_name="florX"):
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"}, "server-tags": server_tags,
                                                         "shared-networks": [{"name": network_name}]})
    response = srv_msg.send_request('v4', cmd)

    assert response == {"arguments": {"shared-networks": [{"name": network_name}]},
                        "result": 0, "text": "IPv4 shared network successfully set."}


def _network_get(command, server_tags, network_parameter=None):
    cmd = dict(command=command, arguments={"remote": {"type": "mysql"}, "server-tags": server_tags})
    if network_parameter:
        cmd["arguments"]["shared-networks"] = [network_parameter]

    return srv_msg.send_request('v4', cmd)


def _network_del(server_tags, network_parameter=None):
    return _network_get("remote-network4-del", server_tags, network_parameter)


def _network_check_res(resp, server_tags, count=1, network_name="florX"):
    assert resp["result"] == 0
    assert resp["arguments"]["count"] == count
    assert resp["arguments"]["shared-networks"][0]["metadata"] == {"server-tag": server_tags}
    assert resp["arguments"]["shared-networks"][0]["name"] == network_name


def test_remote_network4_get_server_tags():
    _network_set(server_tags=["abc"])
    _network_set(server_tags=["xzy"], network_name="flor1")
    _network_set(server_tags=["all"], network_name="top_flor")

    resp = _network_get(command="remote-network4-get", server_tags=["abc"], network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=["abc"], network_name="florX")

    resp = _network_get(command="remote-network4-get", server_tags=["xyz"], network_parameter={"name": "flor1"})
    _network_check_res(resp, server_tags=["xyz"], network_name="flor1")

    resp = _network_get(command="remote-network4-list", server_tags=["xyz"])
    _network_check_res(resp, server_tags=["xyz"], count=2)

    assert resp["arguments"]["shared-networks"][1]["metadata"] == {"server-tag": "all"}
    assert resp["arguments"]["shared-networks"][1]["name"] == "top_flor"


def test_remote_network4_get_server_tags_all_incorrect_setup():
    # Configure 2 networks with the same name but different tags will result with just one network in configuration
    # the first one will be overwritten
    _network_set(server_tags=["abc"])
    _network_set(server_tags=["xzy"])

    resp = _network_get(command="remote-network4-get", server_tags=["xyz"], network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=["xyz"], network_name="florX")

    resp = _network_get(command="remote-network4-get", server_tags=["abc"], network_parameter={"name": "florX"})
    assert resp["result"] == 3
    assert resp["arguments"]["count"] == 0


def test_remote_network4_del_server_tags():
    _network_set(server_tags=["abc"])
    _network_set(server_tags=["xzy"], network_name="flor1")
    _network_set(server_tags=["all"], network_name="top_flor")

    resp = _network_get(command="remote-network4-get", server_tags=["abc"], network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=["abc"], network_name="florX")

    resp = _network_get(command="remote-network4-get", server_tags=["xyz"], network_parameter={"name": "flor1"})
    _network_check_res(resp, server_tags=["xyz"], network_name="flor1")

    resp = _network_get(command="remote-network4-get", server_tags=["all"], network_parameter={"name": "top_flor"})
    _network_check_res(resp, server_tags=["all"], network_name="top_flor")

    _network_del(server_tags=["xyz"], network_parameter={"name": "flor1"})
    assert resp["arguments"]["count"] == 1
    assert resp["result"] == 0

    resp = _network_get(command="remote-network4-get", server_tags=["abc"], network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=["abc"], network_name="florX")

    # removed, so it should not be returned
    resp = _network_get(command="remote-network4-get", server_tags=["xyz"], network_parameter={"name": "flor1"})
    assert resp["result"] == 3
    assert resp["arguments"]["count"] == 0

    resp = _network_get(command="remote-network4-get", server_tags=["all"], network_parameter={"name": "top_flor"})
    _network_check_res(resp, server_tags=["all"], network_name="top_flor")

    _network_del(server_tags=["all"], network_parameter={"name": "top_flor"})
    assert resp["arguments"]["count"] == 1
    assert resp["result"] == 0

    resp = _network_get(command="remote-network4-get", server_tags=["abc"], network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=["abc"], network_name="florX")

    # removed, so it should not be returned
    resp = _network_get(command="remote-network4-get", server_tags=["all"], network_parameter={"name": "top_flor"})
    assert resp["result"] == 3
    assert resp["arguments"]["count"] == 0


def _option_set(server_tags, code=3, opt_data="1.1.1.1"):
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": server_tags,
                                                               "options": [{
                                                                   "code": code,
                                                                   "data": opt_data}]})
    response = srv_msg.send_request('v4', cmd)

    assert response == {"result": 0, "text": "DHCPv4 option successfully set.",
                        "arguments": {"options": [{"code": code, "space": "dhcp4"}]}}


def _option_get(command, server_tags, opt_code=None):
    cmd = dict(command=command, arguments={"remote": {"type": "mysql"},
                                           "server-tags": server_tags})

    if opt_code:
        cmd["arguments"]["options"] = [{"code": opt_code}]

    return srv_msg.send_request('v4', cmd)


def _option_del(server_tags, opt_code=None):
    return _option_get("remote-option4-global-del", server_tags, opt_code)


def _check_option_result(resp, server_tags, count=1, opt_name=None, opt_data=None):
    assert resp["result"] == 0
    assert resp["arguments"]["count"] == count
    assert resp["arguments"]["options"][0]["metadata"] == {"server-tag": server_tags}
    assert resp["arguments"]["options"][0]["name"] == opt_name
    assert resp["arguments"]["options"][0]["data"] == opt_data


def test_remote_option4_get_server_tags():
    _option_set(server_tags=["abc"])
    _option_set(server_tags=["xzy"], opt_data='2.2.2.2')
    _option_set(server_tags=["all"], opt_data='3.3.3.3')

    resp = _option_get(command="remote-option4-global-get", server_tags=["abc"], opt_code=3)
    _check_option_result(resp, server_tags=["abc"], opt_name="routers", opt_data="1.1.1.1")

    resp = _option_get(command="remote-option4-global-get", server_tags=["xyz"], opt_code=3)
    _check_option_result(resp, server_tags=["abc"], opt_name="routers", opt_data="2.2.2.2")

    resp = _option_get(command="remote-option4-global-get", server_tags=["all"], opt_code=3)
    _check_option_result(resp, server_tags=["abc"], opt_name="routers", opt_data="3.3.3.3")

    _option_set(server_tags=["abc"], code=4, opt_data='6.6.6.6')

    resp = _option_get(command="remote-option4-global-get-all", server_tags=["abc"], opt_code=3)
    _check_option_result(resp, count=2, server_tags=["abc"], opt_name="routers", opt_data="1.1.1.1")
    assert resp["arguments"]["options"][1]["metadata"] == {"server-tag": ["abc"]}
    assert resp["arguments"]["options"][1]["name"] == "time-servers"
    assert resp["arguments"]["options"][1]["data"] == "6.6.6.6"

    resp = _option_get(command="remote-option4-global-get-all", server_tags=["xyz"], opt_code=3)
    _check_option_result(resp, count=2, server_tags=["abc"], opt_name="routers", opt_data="2.2.2.2")


def test_remote_option4_del_server_tags():
    _option_set(server_tags=["abc"])
    _option_set(server_tags=["xzy"], opt_data='2.2.2.2')
    _option_set(server_tags=["all"], opt_data='3.3.3.3')

    resp = _option_get(command="remote-option4-global-get", server_tags=["abc"], opt_code=3)
    _check_option_result(resp, server_tags=["abc"], opt_name="routers", opt_data="1.1.1.1")

    resp = _option_get(command="remote-option4-global-get", server_tags=["xyz"], opt_code=3)
    _check_option_result(resp, server_tags=["abc"], opt_name="routers", opt_data="2.2.2.2")

    resp = _option_get(command="remote-option4-global-get", server_tags=["all"], opt_code=3)
    _check_option_result(resp, server_tags=["abc"], opt_name="routers", opt_data="3.3.3.3")

    resp = _option_del(server_tags=["xyz"], opt_code=3)
    assert resp["arguments"]["count"] == 1
    assert resp["text"] == "1 DHCPv4 option(s) deleted."
    assert resp["result"] == 0

    resp = _option_get(command="remote-option4-global-get", server_tags=["abc"], opt_code=3)
    _check_option_result(resp, server_tags=["abc"], opt_name="routers", opt_data="1.1.1.1")

    resp = _option_get(command="remote-option4-global-get", server_tags=["all"], opt_code=3)
    _check_option_result(resp, server_tags=["abc"], opt_name="routers", opt_data="3.3.3.3")

    resp = _option_del(server_tags=["xyz"], opt_code=3)
    assert resp["arguments"]["count"] == 1
    assert resp["text"] == "1 DHCPv4 option(s) deleted."
    assert resp["result"] == 0

    resp = _option_get(command="remote-option4-global-get", server_tags=["abc"], opt_code=3)
    _check_option_result(resp, server_tags=["abc"], opt_name="routers", opt_data="1.1.1.1")

    # this should be missing
    resp = _option_get(command="remote-option4-global-get", server_tags=["xyz"], opt_code=3)
    assert resp["arguments"]["count"] == 0
    assert resp["result"] == 3

    resp = _option_get(command="remote-option4-global-get", server_tags=["all"], opt_code=3)
    _check_option_result(resp, server_tags=["abc"], opt_name="routers", opt_data="3.3.3.3")

    resp = _option_get(command="remote-option4-global-del", server_tags=["all"], opt_code=3)
    assert resp["arguments"]["count"] == 1
    assert resp["text"] == "1 DHCPv4 option(s) deleted."
    assert resp["result"] == 0

    resp = _option_get(command="remote-option4-global-get", server_tags=["abc"], opt_code=3)
    _check_option_result(resp, server_tags=["abc"], opt_name="routers", opt_data="1.1.1.1")

    # this should be missing
    resp = _option_get(command="remote-option4-global-get", server_tags=["all"], opt_code=3)
    assert resp["arguments"]["count"] == 0
    assert resp["result"] == 3

# def test_remote_option_def_del_server_tags():
#     pass
