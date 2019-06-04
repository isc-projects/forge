"""Kea database config backend commands hook testing"""

import pytest
import srv_msg
from cb_model import setup_server_for_config_backend_cmds

pytestmark = [pytest.mark.py_test,
              pytest.mark.v6,
              pytest.mark.kea_only,
              pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.config_backend,
              pytest.mark.cb_cmds]


@pytest.fixture(autouse=True)
def run_around_tests():
    # we still can use server configured with one server tag
    setup_server_for_config_backend_cmds()


def _subnet_set(server_tags, subnet_id, pool, subnet="2001:db8:1::/64"):
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": server_tags,
                                                        "subnets": [{"subnet": subnet, "id": subnet_id,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": pool}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": subnet_id, "subnet": subnet}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}


def _subnet_get(command, server_tags, subnet_parameter=None):
    cmd = dict(command=command, arguments={"remote": {"type": "mysql"},
                                           "server-tags": server_tags})
    if subnet_parameter:
        cmd["arguments"]["subnets"] = [subnet_parameter]

    return srv_msg.send_ctrl_cmd(cmd)


def _subnet_del(server_tags, subnet_parameter=None):
    return _subnet_get("remote-subnet6-del", server_tags, subnet_parameter)


def _check_subnet_result(resp, server_tags, count=1, subnet_id=5, subnet="2001:db8:1::/64"):
    assert resp["result"] == 0
    assert resp["arguments"]["count"] == count
    assert resp["arguments"]["subnets"][0]["metadata"] == {"server-tag": server_tags}
    assert resp["arguments"]["subnets"][0]["subnet"] == subnet
    assert resp["arguments"]["subnets"][0]["id"] == subnet_id


def test_remote_subnet6_get_server_tags():
    _subnet_set(server_tags=["abc"], subnet_id=5, pool="2001:db8:1::1-2001:db8:1::10")
    _subnet_set(server_tags=["xzy"], subnet_id=6, pool="2001:db8:1::15-2001:db8:1::20")
    _subnet_set(server_tags=["all"], subnet_id=7, pool="2001:db8:2::15-2001:db8:2::20", subnet="2001:db8:2::/64")

    resp = _subnet_get(command="remote-subnet6-get-by-id", server_tags=["abc"], subnet_parameter={"id": 5})
    _check_subnet_result(resp, server_tags=["abc"], subnet_id=5)

    resp = _subnet_get(command="remote-subnet6-get-by-id", server_tags=["xyz"], subnet_parameter={"id": 6})
    _check_subnet_result(resp, server_tags=["xyz"], subnet_id=6)

    resp = _subnet_get(command="remote-subnet6-get-by-prefix", server_tags=["xyz"],
                       subnet_parameter={"subnet": "2001:db8:1::/64"})
    _check_subnet_result(resp, server_tags=["xyz"], subnet_id=6)

    resp = _subnet_get(command="remote-subnet6-get-by-prefix", server_tags=["abc"],
                       subnet_parameter={"subnet": "2001:db8:1::/64"})
    _check_subnet_result(resp, server_tags=["abc"], subnet_id=5)

    resp = _subnet_get(command="remote-subnet6-list", server_tags=["abc"])
    # not sure if this is how it suppose to work
    _check_subnet_result(resp, server_tags=["abc"], count=2, subnet_id=5)
    assert resp["arguments"]["subnets"][1]["metadata"] == {"server-tag": "all"}
    # TODO not sure if that will be on the list
    assert resp["arguments"]["subnets"][1]["subnet"] == "2001:db8:2::/64"
    assert resp["arguments"]["subnets"][1]["id"] == 7

    resp = _subnet_get(command="remote-subnet6-list", server_tags=["xyz"])
    _check_subnet_result(resp, server_tags=["xyz"], count=2, subnet_id=6)
    assert resp["arguments"]["subnets"][1]["metadata"] == {"server-tag": "all"}
    # TODO not sure if that will be on the list
    assert resp["arguments"]["subnets"][1]["subnet"] == "2001:db8:2::/64"
    assert resp["arguments"]["subnets"][1]["id"] == 7


def test_remote_subnet6_get_server_tags_all_incorrect_setup():
    # Configure 2 subnets with the same id but different tags will result with just one subnet in configuration
    # the first one will be overwritten
    _subnet_set(server_tags=["abc"], subnet_id=5, pool="2001:db8:1::1-2001:db8:1::10")
    _subnet_set(server_tags=["xyz"], subnet_id=5, pool="2001:db8:1::15-2001:db8:1::20")

    resp = _subnet_get(command="remote-subnet6-get-by-id", server_tags=["abc"], subnet_parameter={"id": 5})
    assert resp["result"] == 3
    assert resp["arguments"]["count"] == 0

    resp = _subnet_get(command="remote-subnet6-get-by-id", server_tags=["xyz"], subnet_parameter={"id": 5})
    _check_subnet_result(resp, server_tags=["xyz"], subnet_id=5)


def test_remote_subnet6_del_server_tags():
    _subnet_set(server_tags=["abc"], subnet_id=5, pool="2001:db8:1::1-2001:db8:1::10")
    _subnet_set(server_tags=["xzy"], subnet_id=6, pool="2001:db8:1::15-2001:db8:1::20")
    _subnet_set(server_tags=["all"], subnet_id=7, pool="2001:db8:2::15-2001:db8:2::20", subnet="2001:db8:2::/64")

    resp = _subnet_get(command="remote-subnet6-get-by-id", server_tags=["abc"], subnet_parameter={"id": 5})
    _check_subnet_result(resp, server_tags=["abc"], subnet_id=5)

    resp = _subnet_get(command="remote-subnet6-get-by-id", server_tags=["xyz"], subnet_parameter={"id": 6})
    _check_subnet_result(resp, server_tags=["xyz"], subnet_id=6)

    resp = _subnet_get(command="remote-subnet6-get-by-id", server_tags=["all"], subnet_parameter={"id": 7})
    _check_subnet_result(resp, server_tags=["all"], subnet_id=7, subnet="2001:db8:2::/64")

    # we should delete just one
    resp = _subnet_del(server_tags=["xyz"], subnet_parameter={"id": 6})
    assert resp["arguments"]["count"] == 1
    assert resp["result"] == 0

    # since this one was just removed now we expect error
    resp = _subnet_del(server_tags=["xyz"], subnet_parameter={"id": 6})
    assert resp["arguments"]["count"] == 0
    assert resp["result"] == 3

    # those two should still be configured
    resp = _subnet_get(command="remote-subnet6-get-by-id", server_tags=["abc"], subnet_parameter={"id": 5})
    _check_subnet_result(resp, server_tags=["abc"], subnet_id=5)

    resp = _subnet_get(command="remote-subnet6-get-by-id", server_tags=["all"], subnet_parameter={"id": 7})
    _check_subnet_result(resp, server_tags=["all"], subnet_id=7, subnet="2001:db8:2::/64")

    resp = _subnet_del(server_tags=["all"], subnet_parameter={"id": 7})
    assert resp["arguments"]["count"] == 1
    assert resp["result"] == 0

    resp = _subnet_get(command="remote-subnet6-get-by-id", server_tags=["abc"], subnet_parameter={"id": 5})
    _check_subnet_result(resp, server_tags=["abc"], subnet_id=5)

    resp = _subnet_get(command="remote-subnet6-get-by-id", server_tags=["all"], subnet_parameter={"id": 7})
    assert resp["arguments"]["count"] == 0
    assert resp["result"] == 3


def _network_set(server_tags, network_name="florX"):
    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": "mysql"}, "server-tags": server_tags,
                                                         "shared-networks": [{"name": network_name}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"shared-networks": [{"name": network_name}]},
                        "result": 0, "text": "IPv6 shared network successfully set."}


def _network_get(command, server_tags, network_parameter=None):
    cmd = dict(command=command, arguments={"remote": {"type": "mysql"}, "server-tags": server_tags})
    if network_parameter:
        cmd["arguments"]["shared-networks"] = [network_parameter]

    return srv_msg.send_ctrl_cmd(cmd)


def _network_del(server_tags, network_parameter=None):
    return _network_get("remote-network6-del", server_tags, network_parameter)


def _network_check_res(resp, server_tags, count=1, network_name="florX"):
    assert resp["result"] == 0
    assert resp["arguments"]["count"] == count
    assert resp["arguments"]["shared-networks"][0]["metadata"] == {"server-tag": server_tags}
    assert resp["arguments"]["shared-networks"][0]["name"] == network_name


def test_remote_network6_get_server_tags():
    _network_set(server_tags=["abc"])
    _network_set(server_tags=["xzy"], network_name="flor1")
    _network_set(server_tags=["all"], network_name="top_flor")

    resp = _network_get(command="remote-network6-get", server_tags=["abc"], network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=["abc"], network_name="florX")

    resp = _network_get(command="remote-network6-get", server_tags=["xyz"], network_parameter={"name": "flor1"})
    _network_check_res(resp, server_tags=["xyz"], network_name="flor1")

    resp = _network_get(command="remote-network6-list", server_tags=["xyz"])
    _network_check_res(resp, server_tags=["xyz"], count=2)

    assert resp["arguments"]["shared-networks"][1]["metadata"] == {"server-tag": "all"}
    assert resp["arguments"]["shared-networks"][1]["name"] == "top_flor"


def test_remote_network6_get_server_tags_all_incorrect_setup():
    # Configure 2 networks with the same name but different tags will result with just one network in configuration
    # the first one will be overwritten
    _network_set(server_tags=["abc"])
    _network_set(server_tags=["xzy"])

    resp = _network_get(command="remote-network6-get", server_tags=["xyz"], network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=["xyz"], network_name="florX")

    resp = _network_get(command="remote-network6-get", server_tags=["abc"], network_parameter={"name": "florX"})
    assert resp["result"] == 3
    assert resp["arguments"]["count"] == 0


def test_remote_network6_del_server_tags():
    _network_set(server_tags=["abc"])
    _network_set(server_tags=["xzy"], network_name="flor1")
    _network_set(server_tags=["all"], network_name="top_flor")

    resp = _network_get(command="remote-network6-get", server_tags=["abc"], network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=["abc"], network_name="florX")

    resp = _network_get(command="remote-network6-get", server_tags=["xyz"], network_parameter={"name": "flor1"})
    _network_check_res(resp, server_tags=["xyz"], network_name="flor1")

    resp = _network_get(command="remote-network6-get", server_tags=["all"], network_parameter={"name": "top_flor"})
    _network_check_res(resp, server_tags=["all"], network_name="top_flor")

    _network_del(server_tags=["xyz"], network_parameter={"name": "flor1"})
    assert resp["arguments"]["count"] == 1
    assert resp["result"] == 0

    resp = _network_get(command="remote-network6-get", server_tags=["abc"], network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=["abc"], network_name="florX")

    # removed, so it should not be returned
    resp = _network_get(command="remote-network6-get", server_tags=["xyz"], network_parameter={"name": "flor1"})
    assert resp["result"] == 3
    assert resp["arguments"]["count"] == 0

    resp = _network_get(command="remote-network6-get", server_tags=["all"], network_parameter={"name": "top_flor"})
    _network_check_res(resp, server_tags=["all"], network_name="top_flor")

    _network_del(server_tags=["all"], network_parameter={"name": "top_flor"})
    assert resp["arguments"]["count"] == 1
    assert resp["result"] == 0

    resp = _network_get(command="remote-network6-get", server_tags=["abc"], network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=["abc"], network_name="florX")

    # removed, so it should not be returned
    resp = _network_get(command="remote-network6-get", server_tags=["all"], network_parameter={"name": "top_flor"})
    assert resp["result"] == 3
    assert resp["arguments"]["count"] == 0


def _option_set(server_tags, code=22, opt_data="2001::1"):
    cmd = dict(command="remote-option6-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": server_tags,
                                                               "options": [{
                                                                   "code": code,
                                                                   "data": opt_data}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"result": 0, "text": "DHCPv6 option successfully set.",
                        "arguments": {"options": [{"code": code, "space": "dhcp6"}]}}


def _option_get(command, server_tags, opt_code=None):
    cmd = dict(command=command, arguments={"remote": {"type": "mysql"},
                                           "server-tags": server_tags})

    if opt_code:
        cmd["arguments"]["options"] = [{"code": opt_code}]

    return srv_msg.send_ctrl_cmd(cmd)


def _option_del(server_tags, opt_code=None):
    return _option_get("remote-option6-global-del", server_tags, opt_code)


def _check_option_result(resp, server_tags, count=1, opt_name=None, opt_data=None):
    assert resp["result"] == 0
    assert resp["arguments"]["count"] == count
    assert resp["arguments"]["options"][0]["metadata"] == {"server-tag": server_tags}
    assert resp["arguments"]["options"][0]["name"] == opt_name
    assert resp["arguments"]["options"][0]["data"] == opt_data


def test_remote_option6_get_server_tags():
    _option_set(server_tags=["abc"])
    _option_set(server_tags=["xzy"], opt_data='2001::2')
    _option_set(server_tags=["all"], opt_data='2001::3')

    resp = _option_get(command="remote-option6-global-get", server_tags=["abc"], opt_code=22)
    _check_option_result(resp, server_tags=["abc"], opt_name="sip-server-addr", opt_data="2001::1")

    resp = _option_get(command="remote-option6-global-get", server_tags=["xyz"], opt_code=22)
    _check_option_result(resp, server_tags=["abc"], opt_name="sip-server-addr", opt_data="2001::2")

    resp = _option_get(command="remote-option6-global-get", server_tags=["all"], opt_code=22)
    _check_option_result(resp, server_tags=["abc"], opt_name="sip-server-addr", opt_data="2001::3")

    _option_set(server_tags=["abc"], code=23, opt_data='2001::6')

    resp = _option_get(command="remote-option6-global-get-all", server_tags=["abc"], opt_code=22)
    _check_option_result(resp, count=2, server_tags=["abc"], opt_name="sip-server-addr", opt_data="2001::1")
    assert resp["arguments"]["options"][1]["metadata"] == {"server-tag": ["abc"]}
    assert resp["arguments"]["options"][1]["name"] == "dns-servers"
    assert resp["arguments"]["options"][1]["data"] == "2001::6"

    resp = _option_get(command="remote-option6-global-get-all", server_tags=["xyz"], opt_code=22)
    _check_option_result(resp, count=2, server_tags=["abc"], opt_name="sip-server-addr", opt_data="2001::2")


def test_remote_option6_del_server_tags():
    _option_set(server_tags=["abc"])
    _option_set(server_tags=["xzy"], opt_data='2001::2')
    _option_set(server_tags=["all"], opt_data='2001::3')

    resp = _option_get(command="remote-option6-global-get", server_tags=["abc"], opt_code=22)
    _check_option_result(resp, server_tags=["abc"], opt_name="sip-server-addr", opt_data="2001::1")

    resp = _option_get(command="remote-option6-global-get", server_tags=["xyz"], opt_code=22)
    _check_option_result(resp, server_tags=["abc"], opt_name="sip-server-addr", opt_data="2001::2")

    resp = _option_get(command="remote-option6-global-get", server_tags=["all"], opt_code=22)
    _check_option_result(resp, server_tags=["abc"], opt_name="sip-server-addr", opt_data="2001::3")

    resp = _option_del(server_tags=["xyz"], opt_code=22)
    assert resp["arguments"]["count"] == 1
    assert resp["text"] == "1 DHCPv6 option(s) deleted."
    assert resp["result"] == 0

    resp = _option_get(command="remote-option6-global-get", server_tags=["abc"], opt_code=22)
    _check_option_result(resp, server_tags=["abc"], opt_name="sip-server-addr", opt_data="2001::1")

    resp = _option_get(command="remote-option6-global-get", server_tags=["all"], opt_code=22)
    _check_option_result(resp, server_tags=["abc"], opt_name="sip-server-addr", opt_data="2001::3")

    resp = _option_del(server_tags=["xyz"], opt_code=22)
    assert resp["arguments"]["count"] == 1
    assert resp["text"] == "1 DHCPv6 option(s) deleted."
    assert resp["result"] == 0

    resp = _option_get(command="remote-option6-global-get", server_tags=["abc"], opt_code=22)
    _check_option_result(resp, server_tags=["abc"], opt_name="sip-server-addr", opt_data="2001::1")

    # this should be missing
    resp = _option_get(command="remote-option6-global-get", server_tags=["xyz"], opt_code=22)
    assert resp["arguments"]["count"] == 0
    assert resp["result"] == 3

    resp = _option_get(command="remote-option6-global-get", server_tags=["all"], opt_code=22)
    _check_option_result(resp, server_tags=["abc"], opt_name="sip-server-addr", opt_data="2001::3")

    resp = _option_get(command="remote-option6-global-del", server_tags=["all"], opt_code=22)
    assert resp["arguments"]["count"] == 1
    assert resp["text"] == "1 DHCPv6 option(s) deleted."
    assert resp["result"] == 0

    resp = _option_get(command="remote-option6-global-get", server_tags=["abc"], opt_code=22)
    _check_option_result(resp, server_tags=["abc"], opt_name="sip-server-addr", opt_data="2001::1")

    # this should be missing
    resp = _option_get(command="remote-option6-global-get", server_tags=["all"], opt_code=22)
    assert resp["arguments"]["count"] == 0
    assert resp["result"] == 3


def _optdef_set(server_tags, opt_code=222, opt_name="foo", opt_type="uint32"):
    cmd = dict(command="remote-option-def6-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": server_tags,
                                                            "option-defs": [{
                                                                "name": opt_name,
                                                                "code": opt_code,
                                                                "type": opt_type}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"option-defs": [{"code": opt_code, "space": "dhcp6"}]},
                        "result": 0, "text": "DHCPv6 option definition successfully set."}


def _optdef_get(command, server_tags, option_def_parameter=None):
    cmd = dict(command=command, arguments={"remote": {"type": "mysql"},
                                           "server-tags": server_tags})
    if option_def_parameter:
        cmd["arguments"]["option-defs"] = [option_def_parameter]

    return srv_msg.send_ctrl_cmd(cmd)


def _optdef_del(server_tags, option_def_parameter=None):
    return _optdef_get("remote-option-def6-del", server_tags, option_def_parameter)


def _check_optdef_result(resp, server_tags, count=1, opt_type="uint32", opt_name="foo", opt_code=222):
    assert resp["result"] == 0
    assert resp["arguments"]["count"] == count
    assert resp["arguments"]["option-defs"][0]["metadata"] == {"server-tag": server_tags}
    assert resp["arguments"]["option-defs"][0]["name"] == opt_name
    assert resp["arguments"]["option-defs"][0]["code"] == opt_code
    assert resp["arguments"]["option-defs"][0]["type"] == opt_type


def test_remote_option_def_get_server_tags():
    # let's make two definitions with the same name but different type and server tag, plus one different with
    # server tag "all"
    _optdef_set(server_tags=["abc"])
    _optdef_set(server_tags=["xyz"], opt_type="string")
    _optdef_set(server_tags=["all"], opt_code=233, opt_name="bar")

    resp = _optdef_get(command="remote-option-def6-get", server_tags=["abc"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["abc"])

    resp = _optdef_get(command="remote-option-def6-get", server_tags=["xyz"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["xyz"], opt_type="string")

    # this one should fail
    resp = _optdef_get(command="remote-option-def6-get", server_tags=["all"],
                       option_def_parameter={"code": 222})
    assert resp["arguments"]["count"] == 0
    assert resp["result"] == 3

    resp = _optdef_get(command="remote-option-def6-get", server_tags=["all"],
                       option_def_parameter={"code": 233})
    _check_optdef_result(resp, server_tags=["all"], opt_code=233, opt_name="bar")

    # let's check if -all will return list of two options for each tag and one option for "all"
    resp = _optdef_get(command="remote-option-def6-get-all", server_tags=["abc"])
    _check_optdef_result(resp, server_tags=["abc"], count=2)
    assert resp["arguments"]["option-defs"][1]["metadata"] == {"server-tag": ["all"]}
    assert resp["arguments"]["option-defs"][1]["name"] == "bar"
    assert resp["arguments"]["option-defs"][1]["code"] == 233

    resp = _optdef_get(command="remote-option-def6-get-all", server_tags=["xyz"])
    _check_optdef_result(resp, server_tags=["xyz"], count=2)
    assert resp["arguments"]["option-defs"][1]["metadata"] == {"server-tag": ["all"]}
    assert resp["arguments"]["option-defs"][1]["name"] == "bar"
    assert resp["arguments"]["option-defs"][1]["code"] == 233

    resp = _optdef_get(command="remote-option-def6-get-all", server_tags=["all"])
    _check_optdef_result(resp, server_tags=["all"], opt_code=233, opt_name="bar")


def test_remote_option_def_del_server_tags():
    # we should be able to configure the same option for each tag, different type is for distinguish returns
    # options from "all" should be overwritten by specific tags on kea configuration level, not in db!
    _optdef_set(server_tags=["abc"])
    _optdef_set(server_tags=["xyz"], opt_type="string")
    _optdef_set(server_tags=["all"], opt_type="uint8")

    resp = _optdef_get(command="remote-option-def6-get", server_tags=["abc"],
                       option_def_parameter={"code": 222})
    # count = 2, we should get one from "abc" and one from "all"
    _check_optdef_result(resp, server_tags=["abc"], count=2)

    resp = _optdef_get(command="remote-option-def6-get", server_tags=["xyz"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["xyz"], opt_type="string", count=2)

    resp = _optdef_get(command="remote-option-def6-get", server_tags=["all"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["all"], opt_type="uint8")

    # let's remove one option and see if all other stays
    _optdef_del(["all"], option_def_parameter={"code": 222})

    resp = _optdef_get(command="remote-option-def6-get", server_tags=["abc"],
                       option_def_parameter={"code": 222})
    # now we expect just one option
    _check_optdef_result(resp, server_tags=["abc"])

    resp = _optdef_get(command="remote-option-def6-get", server_tags=["xyz"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["xyz"], opt_type="string")

    resp = _optdef_get(command="remote-option-def6-get", server_tags=["all"],
                       option_def_parameter={"code": 222})
    assert resp["arguments"]["count"] == 0
    assert resp["result"] == 3

    # same with -all command, we expect just one
    resp = _optdef_get(command="remote-option-def6-get-all", server_tags=["xyz"])
    _check_optdef_result(resp, server_tags=["xyz"])

    resp = _optdef_get(command="remote-option-def6-get-all", server_tags=["xyz"])
    _check_optdef_result(resp, server_tags=["xyz"])

    _optdef_del(["abc"], option_def_parameter={"code": 222})

    resp = _optdef_get(command="remote-option-def6-get", server_tags=["abc"],
                       option_def_parameter={"code": 222})
    assert resp["arguments"]["count"] == 0
    assert resp["result"] == 3

    resp = _optdef_get(command="remote-option-def6-get", server_tags=["xyz"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["xyz"], opt_type="string")
