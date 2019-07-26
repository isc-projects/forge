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
    setup_server_for_config_backend_cmds()
    cmd = dict(command="remote-server4-set", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": "abc"}]})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)


def test_availability():
    cmd = '{"command":"list-commands","arguments":{}}'
    response = srv_msg.send_ctrl_cmd_via_socket(cmd)

    for cmd in ["remote-global-parameter4-del",
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
                "remote-subnet4-del-by-id",
                "remote-subnet4-del-by-prefix",
                "remote-subnet4-get-by-id",
                "remote-subnet4-get-by-prefix",
                "remote-subnet4-list",
                "remote-subnet4-set"]:
        assert cmd in response['arguments']


# subnet tests
@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_remote_subnet4_set_basic(channel):
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
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


def test_remote_subnet4_set_empty_subnet():
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "shared-network-name": "",
                                                        "subnets": [{"subnet": "",
                                                                     "id": 1,
                                                                     "interface": "$(SERVER_IFACE)"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "subnet configuration failed: Invalid subnet syntax (prefix/len expected):" in response["text"]


def test_remote_subnet4_set_missing_subnet():
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "shared-network-name": "",
                                                        "subnets": [{"interface": "$(SERVER_IFACE)", "id": 1}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "subnet configuration failed: mandatory 'subnet' parameter is missing for a subnet being configured" in \
           response["text"]


def test_remote_subnet4_set_stateless():
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24",
                                                                     "shared-network-name": "",
                                                                     "interface": "$(SERVER_IFACE)", "id": 1}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}


def test_remote_subnet4_set_id():
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24", "id": 5,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "192.168.50.1-192.168.50.100"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 5, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}


def test_remote_subnet4_set_duplicated_id():
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24", "id": 5,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "192.168.50.1-192.168.50.100"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 5, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.51.0/24", "id": 5,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "192.168.51.1-192.168.51.100"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 5, "subnet": "192.168.51.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-list", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1,
                                      "subnets": [{"id": 5, "metadata": {"server-tags": ["abc"]},
                                                   "shared-network-name": None, "subnet": "192.168.51.0/24"}]},
                        "result": 0, "text": "1 IPv4 subnet(s) found."}


def test_remote_subnet4_set_duplicated_subnet():
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24", "id": 5,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "192.168.50.1-192.168.50.100"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 5, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24", "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "192.168.50.1-192.168.50.100"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}


def test_remote_subnet4_set_all_values():
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
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


# reservation-mode is integer in db, so we need to check if it's converted correctly
def test_remote_subnet4_set_reservation_mode_all():
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24",
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "id": 1,
                                                                     "reservation-mode": "disabled",
                                                                     "pools": [
                                                                         {"pool": "192.168.50.1-192.168.50.100"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-get-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "subnets": [{"subnet": "192.168.50.0/24"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response["arguments"]["subnets"][0]["reservation-mode"] == "disabled"


def test_remote_subnet4_set_reservation_mode_global():
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24",
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "id": 1,
                                                                     "reservation-mode": "global",
                                                                     "pools": [
                                                                         {"pool": "192.168.50.1-192.168.50.100"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-get-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "subnets": [{"subnet": "192.168.50.0/24"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response["arguments"]["subnets"][0]["reservation-mode"] == "global"


def test_remote_subnet4_set_reservation_mode_out_pool():
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24",
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "id": 1,
                                                                     "reservation-mode": "out-of-pool",
                                                                     "pools": [
                                                                         {"pool": "192.168.50.1-192.168.50.100"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-get-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "subnets": [{"subnet": "192.168.50.0/24"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response["arguments"]["subnets"][0]["reservation-mode"] == "out-of-pool"


def test_remote_subnet4_set_reservation_mode_disabled():
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24",
                                                                     "shared-network-name": "",
                                                                     "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "reservation-mode": "disabled"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-get-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "subnets": [{"subnet": "192.168.50.0/24"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response["arguments"]["subnets"][0]["reservation-mode"] == "disabled"


def _subnet_set(server_tag=None):
    if server_tag is None:
        server_tag = ["abc"]
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": server_tag,
                                                        "subnets": [{"subnet": "192.168.50.0/24", "id": 5,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "192.168.50.1-192.168.50.100"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 5, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}


def test_remote_subnet4_del_by_id():
    _subnet_set()

    cmd = dict(command="remote-subnet4-del-by-id", arguments={"remote": {"type": "mysql"},
                                                              "subnets": [{"id": 5}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv4 subnet(s) deleted."}


def test_remote_subnet4_del_by_id_incorrect_id():
    _subnet_set()

    cmd = dict(command="remote-subnet4-del-by-id", arguments={"remote": {"type": "mysql"},
                                                              "subnets": [{"id": 15}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 IPv4 subnet(s) deleted."}


def test_remote_subnet4_del_id_negative_missing_subnet():
    _subnet_set()

    cmd = dict(command="remote-subnet4-del-by-id", arguments={"remote": {"type": "mysql"},
                                                              "subnets": [{"subnet": "192.168.50.0/24"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "missing 'id' parameter"}


def test_remote_subnet4_del_by_prefix():
    _subnet_set()

    cmd = dict(command="remote-subnet4-del-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "subnets": [{"subnet": "192.168.50.0/24"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv4 subnet(s) deleted."}


def test_remote_subnet4_del_by_prefix_non_existing_subnet():
    _subnet_set()

    cmd = dict(command="remote-subnet4-del-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "subnets": [{"subnet": "192.168.51.0/24"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 IPv4 subnet(s) deleted."}


def test_remote_subnet4_del_by_prefix_missing_subnet_():
    _subnet_set()
    cmd = dict(command="remote-subnet4-del-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "subnets": [{"id": 2}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "missing 'subnet' parameter"}


def test_remote_subnet4_get_by_id():
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
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

    cmd = dict(command="remote-subnet4-get-by-id", arguments={"remote": {"type": "mysql"},
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
                                                   "interface": srv_msg.get_interface(),
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
                                                   "reservation-mode": "global", "server-hostname": "name-xyz",
                                                   "subnet": "192.168.50.0/24", "valid-lifetime": 1000}]},
                        "result": 0, "text": "IPv4 subnet 2 found."}


def test_remote_subnet4_get_by_id_incorrect_id():
    _subnet_set()

    cmd = dict(command="remote-subnet4-get-by-id", arguments={"remote": {"type": "mysql"},
                                                              "subnets": [{"id": 3}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "subnets": []},
                        "result": 3, "text": "IPv4 subnet 3 not found."}


def test_remote_subnet4_get_by_id_missing_id():
    _subnet_set()

    cmd = dict(command="remote-subnet4-get-by-id", arguments={"remote": {"type": "mysql"},
                                                              "subnets": [{"subnet": 3}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1,
                        "text": "missing 'id' parameter"}


def test_remote_subnet4_get_by_prefix():
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
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

    cmd = dict(command="remote-subnet4-get-by-prefix", arguments={"remote": {"type": "mysql"},
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
            "interface": srv_msg.get_interface(),
            "match-client-id": True,
            "next-server": "0.0.0.0",
            "option-data": [],
            "pools": [{
                "option-data": [],
                "pool": "192.168.50.1-192.168.50.100"}],
            "relay": {
                "ip-addresses": [
                    "192.168.5.5"]},
            "reservation-mode": "all",
            "server-hostname": "name-xyz",
            "subnet": "192.168.50.0/24",
            "valid-lifetime": 1000}]}, "result": 0, "text": "IPv4 subnet 192.168.50.0/24 found."}


def test_remote_subnet4_get_by_prefix_negative():
    _subnet_set()

    cmd = dict(command="remote-subnet4-get-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "subnets": [{"subnet": "10.0.0.2/12"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "subnets": []},
                        "result": 3, "text": "IPv4 subnet 10.0.0.2/12 not found."}


def test_remote_subnet4_get_by_prefix_incorrect_prefix():
    _subnet_set()
    cmd = dict(command="remote-subnet4-get-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "subnets": [{"subnet": "10.0.0/12"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1,
                        "text": "unable to parse invalid prefix 10.0.0/12"}


def test_remote_subnet4_get_by_prefix_missing_prefix():
    _subnet_set()

    cmd = dict(command="remote-subnet4-get-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "subnets": [{"id": "10.0.0/12"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1,
                        "text": "missing 'subnet' parameter"}


def test_remote_subnet4_list():
    _subnet_set()

    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.51.0/24", "id": 3,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "192.168.51.1-192.168.51.100"}]}]})
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.52.0/24", "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "192.168.52.1-192.168.52.100"}]}]})
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command="remote-subnet4-list", arguments={"remote": {"type": "mysql"},
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
def test_remote_network4_set_basic(channel):
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{"name": "floor13"}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"shared-networks": [{"name": "floor13"}]},
                        "result": 0, "text": "IPv4 shared network successfully set."}


def test_remote_network4_set_missing_name():
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "missing parameter 'name'" in response["text"]


def test_remote_network4_set_empty_name():
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": ""}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "'name' parameter must not be empty"}


@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_remote_network4_get_basic(channel):
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd, channel=channel)

    cmd = dict(command="remote-network4-get", arguments={"remote": {"type": "mysql"},
                                                         "shared-networks": [{
                                                             "name": "net1"}]})

    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {"arguments": {"count": 1,
                                      "shared-networks": [{"interface": srv_msg.get_interface(), "name": "net1",
                                                           "metadata": {"server-tags": ["abc"]},
                                                           "option-data": [], "relay": {"ip-addresses": []}}]},
                        "result": 0, "text": "IPv4 shared network 'net1' found."}


def test_remote_network4_get_all_values():
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
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
    cmd = dict(command="remote-network4-get", arguments={"remote": {"type": "mysql"},
                                                         "shared-networks": [{
                                                             "name": "net1"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1,
                                      "shared-networks": [{"authoritative": False, "client-class": "abc",
                                                           "rebind-timer": 200, "renew-timer": 100,
                                                           "valid-lifetime": 300, "reservation-mode": "global",
                                                           "interface": srv_msg.get_interface(),
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


def test_remote_network4_set_t1_t2():
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "calculate-tee-times": True,
                                                             "t1-percent": 0.5,
                                                             "t2-percent": 10,
                                                             "interface": "$(SERVER_IFACE)"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "'t2-percent' parameter is not a real" in response["text"]

    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "calculate-tee-times": True,
                                                             "t1-percent": 10,
                                                             "t2-percent": 0.5,
                                                             "interface": "$(SERVER_IFACE)"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "'t1-percent' parameter is not a real" in response["text"]

    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
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
def test_remote_network4_list_basic(channel):
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd, channel=channel)

    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net2",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd, channel=channel)

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"count": 2, "shared-networks": [{"metadata": {"server-tags": ["abc"]},
                                                                       "name": "net1"},
                                                                      {"metadata": {"server-tags": ["abc"]},
                                                                       "name": "net2"}]},
                        "result": 0,
                        "text": "2 IPv4 shared network(s) found."}


def test_remote_network4_list_no_networks():
    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0,
                                      "shared-networks": []},
                        "result": 3,
                        "text": "0 IPv4 shared network(s) found."}


@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_remote_network4_del_basic(channel):
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd, channel=channel)

    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net2",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd, channel=channel)

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"count": 2,
                                      "shared-networks": [{"metadata": {"server-tags": ["abc"]}, "name": "net1"},
                                                          {"metadata": {"server-tags": ["abc"]}, "name": "net2"}]},
                        "result": 0,
                        "text": "2 IPv4 shared network(s) found."}

    cmd = dict(command="remote-network4-del", arguments={"remote": {"type": "mysql"},
                                                         "shared-networks": [{"name": "net1"}]})

    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv4 shared network(s) deleted."}

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"count": 1,
                                      "shared-networks": [{"metadata": {"server-tags": ["abc"]}, "name": "net2"}]},
                        "result": 0, "text": "1 IPv4 shared network(s) found."}

    cmd = dict(command="remote-network4-del", arguments={"remote": {"type": "mysql"},
                                                         "shared-networks": [{"name": "net2"}]})

    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv4 shared network(s) deleted."}

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel, exp_result=3)

    assert response == {"arguments": {"count": 0,
                                      "shared-networks": []},
                        "result": 3,
                        "text": "0 IPv4 shared network(s) found."}


def test_remote_network4_del_subnet_keep():
    # add networks
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net2",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 2,
                                      "shared-networks": [{"metadata": {"server-tags": ["abc"]},
                                                           "name": "net1"},
                                                          {"metadata": {"server-tags": ["abc"]},
                                                           "name": "net2"}]},
                        "result": 0,
                        "text": "2 IPv4 shared network(s) found."}

    # add subnets to networks
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
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

    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
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
    cmd = dict(command="remote-subnet4-list", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 2, "subnets": [{"id": 1, "subnet": "192.8.0.0/24",
                                                               "shared-network-name": "net1",
                                                               "metadata": {"server-tags": ["abc"]}},
                                                              {"id": 2, "subnet": "192.9.0.0/24",
                                                               "shared-network-name": "net2",
                                                               "metadata": {"server-tags": ["abc"]}}]},
                        "result": 0, "text": "2 IPv4 subnet(s) found."}

    cmd = dict(command="remote-network4-del", arguments={"remote": {"type": "mysql"}, "subnets-action": "keep",
                                                         "shared-networks": [{"name": "net1"}]})

    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv4 shared network(s) deleted."}

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1,
                                      "shared-networks": [{"metadata": {"server-tags": ["abc"]}, "name": "net2"}]},
                        "result": 0, "text": "1 IPv4 shared network(s) found."}

    # after deleting network we still want to have 2 subnets
    cmd = dict(command="remote-subnet4-list", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 2,
                                      "subnets": [{"id": 1, "metadata": {"server-tags": ["abc"]},
                                                   "shared-network-name": None, "subnet": "192.8.0.0/24"},
                                                  {"id": 2, "metadata": {"server-tags": ["abc"]},
                                                   "shared-network-name": "net2", "subnet": "192.9.0.0/24"}]},
                        "result": 0, "text": "2 IPv4 subnet(s) found."}

    cmd = dict(command="remote-network4-del", arguments={"remote": {"type": "mysql"}, "subnets-action": "keep",
                                                         "shared-networks": [{"name": "net2"}]})

    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv4 shared network(s) deleted."}

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0,
                                      "shared-networks": []},
                        "result": 3,
                        "text": "0 IPv4 shared network(s) found."}

    # after removing all networks we still want to have both subnets
    cmd = dict(command="remote-subnet4-list", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 2,
                                      "subnets": [{"id": 1, "metadata": {"server-tags": ["abc"]},
                                                   "shared-network-name": None, "subnet": "192.8.0.0/24"},
                                                  {"id": 2, "metadata": {"server-tags": ["abc"]},
                                                   "shared-network-name": None, "subnet": "192.9.0.0/24"}]},
                        "result": 0, "text": "2 IPv4 subnet(s) found."}


def test_remote_network4_del_subnet_delete_simple():
    # for ticket #738
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.8.0.0/24",
                                                                     "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "net1",
                                                                     "pools": [
                                                                         {"pool": "192.8.0.1-192.8.0.100"}]}]})
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command="remote-network4-del", arguments={"remote": {"type": "mysql"}, "subnets-action": "delete",
                                                         "shared-networks": [{"name": "net1"}]})
    srv_msg.send_ctrl_cmd(cmd)


def test_remote_network4_del_subnet_delete():
    # add networks
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net2",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 2,
                                      "shared-networks": [{"metadata": {"server-tags": ["abc"]},
                                                           "name": "net1"},
                                                          {"metadata": {"server-tags": ["abc"]},
                                                           "name": "net2"}]},
                        "result": 0,
                        "text": "2 IPv4 shared network(s) found."}

    # add subnets to networks
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
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

    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
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
    cmd = dict(command="remote-subnet4-list", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 2, "subnets": [{"id": 1, "subnet": "192.8.0.0/24",
                                                               "shared-network-name": "net1",
                                                               "metadata": {"server-tags": ["abc"]}},
                                                              {"id": 2, "subnet": "192.9.0.0/24",
                                                               "shared-network-name": "net2",
                                                               "metadata": {"server-tags": ["abc"]}}]},
                        "result": 0, "text": "2 IPv4 subnet(s) found."}

    cmd = dict(command="remote-network4-del", arguments={"remote": {"type": "mysql"}, "subnets-action": "delete",
                                                         "shared-networks": [{"name": "net1"}]})

    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv4 shared network(s) deleted."}

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1,
                                      "shared-networks": [{"metadata": {"server-tags": ["abc"]}, "name": "net2"}]},
                        "result": 0, "text": "1 IPv4 shared network(s) found."}

    # after deleting network we still want to have 2 subnets
    cmd = dict(command="remote-subnet4-list", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1,
                                      "subnets": [{"id": 2, "metadata": {"server-tags": ["abc"]},
                                                   "shared-network-name": "net2", "subnet": "192.9.0.0/24"}]},
                        "result": 0, "text": "1 IPv4 subnet(s) found."}

    cmd = dict(command="remote-network4-del", arguments={"remote": {"type": "mysql"}, "subnets-action": "delete",
                                                         "shared-networks": [{"name": "net2"}]})

    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv4 shared network(s) deleted."}

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0,
                                      "shared-networks": []},
                        "result": 3,
                        "text": "0 IPv4 shared network(s) found."}

    # all subnets should be removed now
    cmd = dict(command="remote-subnet4-list", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "subnets": []},
                        "result": 3, "text": "0 IPv4 subnet(s) found."}


def _set_global_parameter():
    cmd = dict(command="remote-global-parameter4-set", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": {
                                                                      "boot-file-name": "/dev/null"}})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1, "parameters": {"boot-file-name": "/dev/null"}},
                        "result": 0,
                        "text": "1 DHCPv4 global parameter(s) successfully set."}


# global-parameter tests
def test_remote_global_parameter4_set_text():
    _set_global_parameter()


def test_remote_global_parameter4_set_integer():
    cmd = dict(command="remote-global-parameter4-set", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": {"valid-lifetime": 1000}})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1, "parameters": {"valid-lifetime": 1000}},
                        "result": 0,
                        "text": "1 DHCPv4 global parameter(s) successfully set."}


def test_remote_global_parameter4_set_incorrect_parameter():
    cmd = dict(command="remote-global-parameter4-set", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": {"boot-fiabcsd": "/dev/null"}})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "unknown parameter 'boot-fiabcsd'"}


def test_remote_global_parameter4_del():
    _set_global_parameter()

    cmd = dict(command="remote-global-parameter4-del", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": ["boot-file-name"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1},
                        "result": 0, "text": "1 DHCPv4 global parameter(s) deleted."}


def test_remote_global_parameter4_del_not_existing_parameter():
    cmd = dict(command="remote-global-parameter4-del", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": ["boot-file-name"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0},
                        "result": 3, "text": "0 DHCPv4 global parameter(s) deleted."}


def test_remote_global_parameter4_get():
    _set_global_parameter()

    cmd = dict(command="remote-global-parameter4-get", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": ["boot-file-name"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1,
                                      "parameters": {"boot-file-name": "/dev/null",
                                                     "metadata": {"server-tags": ["abc"]}}},
                        "result": 0, "text": "'boot-file-name' DHCPv4 global parameter found."}


def test_remote_global_parameter4_get_all_one():
    _set_global_parameter()

    cmd = dict(command="remote-global-parameter4-get-all", arguments={"remote": {"type": "mysql"},
                                                                      "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1, "parameters": [{"boot-file-name": "/dev/null",
                                                                  "metadata": {"server-tags": ["abc"]}}]},
                        "result": 0, "text": "1 DHCPv4 global parameter(s) found."}


def test_remote_global_parameter4_get_all_multiple():
    _set_global_parameter()

    cmd = dict(command="remote-global-parameter4-set", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": {"decline-probation-period": 15}})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1, "parameters": {"decline-probation-period": 15}}, "result": 0,
                        "text": "1 DHCPv4 global parameter(s) successfully set."}

    cmd = dict(command="remote-global-parameter4-get-all", arguments={"remote": {"type": "mysql"},
                                                                      "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 2, "parameters": [{"boot-file-name": "/dev/null",
                                                                  "metadata": {"server-tags": ["abc"]}},
                                                                 {"decline-probation-period": 15,
                                                                  "metadata": {"server-tags": ["abc"]}}]},
                        "result": 0, "text": "2 DHCPv4 global parameter(s) found."}


def test_remote_global_parameter4_get_all_zero():
    cmd = dict(command="remote-global-parameter4-get-all", arguments={"remote": {"type": "mysql"},
                                                                      "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "parameters": []},
                        "result": 3, "text": "0 DHCPv4 global parameter(s) found."}


def _set_option_def(channel='http'):
    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 222,
                                                                "type": "uint32"}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"option-defs": [{"code": 222, "space": "dhcp4"}]},
                        "result": 0, "text": "DHCPv4 option definition successfully set."}


@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_remote_option_def4_set_basic(channel):
    _set_option_def(channel=channel)


def test_remote_option_def4_set_using_zero_as_code():
    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 0,
                                                                "type": "uint32"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "invalid option code '0': reserved for PAD" in response["text"]


def test_remote_option_def4_set_using_standard_code():
    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 24,
                                                                "type": "uint32"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "an option with code 24 already exists in space 'dhcp4'"}


def test_remote_option_def4_set_missing_parameters():
    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
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

    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
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

    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
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
def test_remote_option_def4_get_basic(channel):
    _set_option_def()

    cmd = dict(command="remote-option-def4-get", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "code": 222}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {"arguments": {"count": 1, "option-defs": [{"array": False, "code": 222, "encapsulate": "",
                                                                   "name": "foo", "record-types": "", "space": "dhcp4",
                                                                   "metadata": {"server-tags": ["abc"]},
                                                                   "type": "uint32"}]},
                        "result": 0, "text": "DHCPv4 option definition 222 in 'dhcp4' found."}


def test_remote_option_def4_get_multiple_defs():
    _set_option_def()

    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 222,
                                                                "type": "uint32",
                                                                "space": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"option-defs": [{"code": 222, "space": "abc"}]},
                        "result": 0, "text": "DHCPv4 option definition successfully set."}

    cmd = dict(command="remote-option-def4-get", arguments={"remote": {"type": "mysql"},
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


def test_remote_option_def4_get_missing_code():
    cmd = dict(command="remote-option-def4-get", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "missing 'code' parameter"}


def test_remote_option_def4_get_all_option_not_defined():
    cmd = dict(command="remote-option-def4-get-all", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "option-defs": []},
                        "result": 3, "text": "0 DHCPv4 option definition(s) found."}


def test_remote_option_def4_get_all_multiple_defs():
    _set_option_def()

    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 222,
                                                                "type": "uint32",
                                                                "space": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"option-defs": [{"code": 222, "space": "abc"}]},
                        "result": 0, "text": "DHCPv4 option definition successfully set."}

    cmd = dict(command="remote-option-def4-get-all", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})

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
def test_remote_option_def4_get_all_basic(channel):
    _set_option_def()

    cmd = dict(command="remote-option-def4-get-all", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {"arguments": {"count": 1, "option-defs": [{"array": False, "code": 222, "encapsulate": "",
                                                                   "metadata": {"server-tags": ["abc"]},
                                                                   "name": "foo", "record-types": "", "space": "dhcp4",
                                                                   "type": "uint32"}]},
                        "result": 0, "text": "1 DHCPv4 option definition(s) found."}


@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_remote_option_def4_del_basic(channel):
    _set_option_def()

    cmd = dict(command="remote-option-def4-del", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"],
                                                            "option-defs": [{"code": 222}]})

    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv4 option definition(s) deleted."}


def test_remote_option_def4_del_different_space():
    _set_option_def()

    cmd = dict(command="remote-option-def4-del", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"],
                                                            "option-defs": [{"code": 222, "space": "abc"}]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 DHCPv4 option definition(s) deleted."}


def test_remote_option_def4_del_incorrect_code():
    cmd = dict(command="remote-option-def4-del", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"],
                                                            "option-defs": [{"name": 22}]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "missing 'code' parameter"}

    cmd = dict(command="remote-option-def4-del", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"],
                                                            "option-defs": [{}]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "missing 'code' parameter"}

    cmd = dict(command="remote-option-def4-del", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"],
                                                            "option-defs": [{"code": "abc"}]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "'code' parameter is not an integer"}


def test_remote_option_def4_del_missing_option():
    cmd = dict(command="remote-option-def4-del", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"],
                                                            "option-defs": [{"code": 212}]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 DHCPv4 option definition(s) deleted."}


def test_remote_option_def4_del_multiple_options():
    _set_option_def()

    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 222,
                                                                "type": "uint32",
                                                                "space": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"option-defs": [{"code": 222, "space": "abc"}]},
                        "result": 0, "text": "DHCPv4 option definition successfully set."}

    cmd = dict(command="remote-option-def4-del", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"],
                                                            "option-defs": [{"code": 222}]})

    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv4 option definition(s) deleted."}

    cmd = dict(command="remote-option-def4-get-all", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1, "option-defs": [{"array": False, "code": 222, "encapsulate": "",
                                                                   "metadata": {"server-tags": ["abc"]},
                                                                   "name": "foo", "record-types": "", "space": "abc",
                                                                   "type": "uint32"}]},
                        "result": 0, "text": "1 DHCPv4 option definition(s) found."}


def _set_global_option():
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "code": 6,
                                                                   "data": "192.0.2.1, 192.0.2.2"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"result": 0, "text": "DHCPv4 option successfully set.",
                        "arguments": {"options": [{"code": 6, "space": "dhcp4"}]}}


def test_remote_global_option4_global_set_basic():
    _set_global_option()


@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_remote_global_option4_global_set_missing_data(channel):
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "code": 6}]})
    srv_msg.send_ctrl_cmd(cmd, channel=channel, exp_result=1)


def test_remote_global_option4_global_set_name():
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "name": "host-name",
                                                                   "data": "isc.example.com"}]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"options": [{"code": 12, "space": "dhcp4"}]},
                        "result": 0, "text": "DHCPv4 option successfully set."}


def test_remote_global_option4_global_set_incorrect_code_missing_name():
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "code": "aaa"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "'code' parameter is not an integer" in response["text"]


def test_remote_global_option4_global_set_incorrect_name_missing_code():
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "name": 123}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "'name' parameter is not a string" in response["text"]


def test_remote_global_option4_global_set_missing_code_and_name():
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "option data configuration requires one of " \
           "'code' or 'name' parameters to be specified" in response["text"]


def test_remote_global_option4_global_set_incorrect_code():
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": "aa",
                                                                            "name": "cc"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "'code' parameter is not an integer" in response["text"]


def test_remote_global_option4_global_set_incorrect_name():
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 12,
                                                                            "name": 12,
                                                                            "data": 'isc.example.com'}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "'name' parameter is not a string" in response["text"]


@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_remote_global_option4_global_get_basic(channel):
    _set_global_option()

    cmd = dict(command="remote-option4-global-get", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {"arguments": {"count": 1, "options": [{"always-send": False, "code": 6, "csv-format": True,
                                                               "data": "192.0.2.1, 192.0.2.2",
                                                               "metadata": {"server-tags": ["abc"]},
                                                               "name": "domain-name-servers", "space": "dhcp4"}]},
                        "result": 0, "text": "DHCPv4 option 6 in 'dhcp4' found."}


def test_remote_global_option4_global_set_different_space():
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6,
                                                                            "data": '192.0.2.1, 192.0.2.2',
                                                                            "always-send": True,
                                                                            "csv-format": True,
                                                                            "space": "xyz"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "definition for the option 'xyz.' having code '6' does not exist" in response["text"]


def test_remote_global_option4_global_set_csv_false_incorrect():
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6,
                                                                            "data": '192.0.2.1',
                                                                            "always-send": True,
                                                                            "csv-format": False}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "option data is not a valid string of hexadecimal digits: 192.0.2.1" in response["text"]


def test_remote_global_option4_global_set_csv_false_correct():
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6,
                                                                            "data": "C0000201",  # 192.0.2.1
                                                                            "always-send": True,
                                                                            "csv-format": False}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"result": 0, "text": "DHCPv4 option successfully set.",
                        "arguments": {"options": [{"code": 6, "space": "dhcp4"}]}}


def test_remote_global_option4_global_set_csv_false_incorrect_hex():
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6,
                                                                            "data": "C0000201Z",
                                                                            "always-send": True,
                                                                            "csv-format": False}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "option data is not a valid string of hexadecimal digits: C0000201Z" in response["text"]


@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_remote_global_option4_global_del_basic(channel):
    _set_global_option()

    cmd = dict(command="remote-option4-global-del", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv4 option(s) deleted."}


def test_remote_global_option4_global_del_missing_code():
    cmd = dict(command="remote-option4-global-del", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"ab": 6}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "missing 'code' parameter"}


def test_remote_global_option4_global_del_incorrect_code():
    cmd = dict(command="remote-option4-global-del", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": "6"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "'code' parameter is not an integer"}


def test_remote_global_option4_global_del_missing_option():
    cmd = dict(command="remote-option4-global-del", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 DHCPv4 option(s) deleted."}


def test_remote_global_option4_global_get_missing_code():
    cmd = dict(command="remote-option4-global-get", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"ab": 6}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "missing 'code' parameter"}


def test_remote_global_option4_global_get_incorrect_code():
    cmd = dict(command="remote-option4-global-get", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": "6"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "'code' parameter is not an integer"}


def test_remote_global_option4_global_get_missing_option():
    cmd = dict(command="remote-option4-global-get", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert response == {"arguments": {"count": 0, "options": []},
                        "result": 3, "text": "DHCPv4 option 6 in 'dhcp4' not found."}


def test_remote_global_option4_global_get_csv_false():
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6,
                                                                            "data": "C0000301C0000302",
                                                                            "always-send": True,
                                                                            "csv-format": False}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"result": 0, "text": "DHCPv4 option successfully set.",
                        "arguments": {"options": [{"code": 6, "space": "dhcp4"}]}}

    cmd = dict(command="remote-option4-global-get", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6}]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1, "options": [{"always-send": True, "code": 6, "csv-format": False,
                                                               "data": "C0000301C0000302",
                                                               "metadata": {"server-tags": ["abc"]},
                                                               "name": "domain-name-servers", "space": "dhcp4"}]},
                        "result": 0, "text": "DHCPv4 option 6 in 'dhcp4' found."}


def test_remote_global_option4_global_get_all():
    _set_global_option()

    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "code": 16,
                                                                   "data": "199.199.199.1"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"result": 0, "text": "DHCPv4 option successfully set.",
                        "arguments": {"options": [{"code": 16, "space": "dhcp4"}]}}

    cmd = dict(command="remote-option4-global-get-all", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})

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

    cmd = dict(command="remote-option4-global-del", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6}]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv4 option(s) deleted."}

    cmd = dict(command="remote-option4-global-get-all", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1, "options": [{"always-send": False, "code": 16, "csv-format": True,
                                                               "data": "199.199.199.1", "name": "swap-server",
                                                               "metadata": {"server-tags": ["abc"]},
                                                               "space": "dhcp4"}]},
                        "result": 0, "text": "1 DHCPv4 option(s) found."}

    cmd = dict(command="remote-option4-global-del", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 16}]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv4 option(s) deleted."}

    cmd = dict(command="remote-option4-global-get-all", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert response == {"arguments": {"count": 0, "options": []}, "result": 3, "text": "0 DHCPv4 option(s) found."}
