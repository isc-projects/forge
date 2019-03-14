"""Kea database config backend commands hook testing"""

import json
import pytest

import srv_msg
import srv_control
import misc

pytestmark = [pytest.mark.py_test,
              pytest.mark.v4,
              # pytest.mark.v6, TODO change it when feature is ready for v6
              pytest.mark.kea_only,
              pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.config_backend,
              pytest.mark.cb_cmds]


def _setup_server_for_cb_cmds():
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.config_client_classification('0', 'Client_Class_1')
    srv_control.open_control_channel('unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel('$(SRV4_ADDR)',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.add_hooks('$(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_cb_cmds.so')
    srv_control.add_hooks('$(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_mysql_cb.so')
    srv_control.run_command('"config-control":{"config-databases":[{"user":"$(DB_USER)",'
                            '"password":"$(DB_PASSWD)","name":"$(DB_NAME)","type":"mysql"}]}')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')


def _send_request(cmd, channel='http'):
    if channel == 'http':
        if srv_msg.get_proto_version() == 'v4':
            cmd["service"] = ['dhcp4']
        else:
            cmd["service"] = ['dhcp6']
    cmd_str = json.dumps(cmd)

    if channel == 'http':
        response = srv_msg.send_through_http(
            '$(SRV4_ADDR)',
            '8000',
            cmd_str)
        response = response[0]
    elif channel == 'socket':
        response = srv_msg.send_through_socket_server_site(
            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
            cmd_str)
    else:
        raise ValueError('unsupported channel type: %s' % str(channel))
    return response


@pytest.fixture(autouse=True)
def run_around_tests():
    misc.test_setup()
    _setup_server_for_cb_cmds()


def test_availability():
    cmd = dict(command='list-commands')
    response = _send_request(cmd)

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
@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_subnet4_set_basic(channel):
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24",
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "pools": [
                                                                         {"pool": "192.168.50.1-192.168.50.100"}]}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}


def test_remote_subnet4_set_empty_subnet(channel='http'):
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "",
                                                                     "interface": "$(SERVER_IFACE)"}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"result": 1,
                        "text": "subnet configuration failed: Invalid subnet syntax"
                                " (prefix/len expected): (<wire>:0:122)"}


def test_remote_subnet4_set_missing_subnet(channel='http'):
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"interface": "$(SERVER_IFACE)"}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"result": 1,
                        "text": "subnet configuration failed: mandatory 'subnet' parameter"
                                " is missing for a subnet being configured (<wire>:0:88)"}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_subnet4_set_stateless(channel):
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24",
                                                                     "interface": "$(SERVER_IFACE)"}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_subnet4_set_id(channel):
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24", "id": 5,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "pools": [
                                                                         {"pool": "192.168.50.1-192.168.50.100"}]}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"subnets": [{"id": 5, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_subnet4_set_duplicated_id(channel):
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24", "id": 5,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "pools": [
                                                                         {"pool": "192.168.50.1-192.168.50.100"}]}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"subnets": [{"id": 5, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.51.0/24", "id": 5,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "pools": [
                                                                         {"pool": "192.168.51.1-192.168.51.100"}]}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"subnets": [{"id": 5, "subnet": "192.168.51.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-list", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 1, "subnets": [{"id": 5, "subnet": "192.168.51.0/24"}]},
                        "result": 0, "text": "1 IPv4 subnet(s) found."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_subnet4_set_duplicated_subnet(channel):
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24", "id": 5,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "pools": [
                                                                         {"pool": "192.168.50.1-192.168.50.100"}]}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"subnets": [{"id": 5, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24", "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "pools": [
                                                                         {"pool": "192.168.50.1-192.168.50.100"}]}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_subnet4_set_all_values(channel):
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"4o6-interface": "eth9",
                                                                     "4o6-interface-id": "interf-id",
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
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"subnets": [{"id": 2, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}


# reservation-mode is integer in db, so we need to check if it's converted correctly
@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_subnet4_set_reservation_mode_all(channel):
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24",
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "reservation-mode": "disabled",
                                                                     "pools": [
                                                                         {"pool": "192.168.50.1-192.168.50.100"}]}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-get-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "subnets": [{"subnet": "192.168.50.0/24"}]})
    response = _send_request(cmd, channel=channel)

    assert response["arguments"]["subnets"][0]["reservation-mode"] == "disabled"


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_subnet4_set_reservation_mode_global(channel):
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24",
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "reservation-mode": "global",
                                                                     "pools": [
                                                                         {"pool": "192.168.50.1-192.168.50.100"}]}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-get-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "subnets": [{"subnet": "192.168.50.0/24"}]})
    response = _send_request(cmd, channel=channel)

    assert response["arguments"]["subnets"][0]["reservation-mode"] == "global"


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_subnet4_set_reservation_mode_out_pool(channel):
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24",
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "reservation-mode": "out-of-pool",
                                                                     "pools": [
                                                                         {"pool": "192.168.50.1-192.168.50.100"}]}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-get-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "subnets": [{"subnet": "192.168.50.0/24"}]})
    response = _send_request(cmd, channel=channel)

    assert response["arguments"]["subnets"][0]["reservation-mode"] == "out-of-pool"


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_subnet4_set_reservation_mode_disabled(channel):
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24",
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "reservation-mode": "disabled"}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-get-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "subnets": [{"subnet": "192.168.50.0/24"}]})
    response = _send_request(cmd, channel=channel)

    assert response["arguments"]["subnets"][0]["reservation-mode"] == "disabled"


def _subnet_set(channel):
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.50.0/24", "id": 5,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "pools": [
                                                                         {"pool": "192.168.50.1-192.168.50.100"}]}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"subnets": [{"id": 5, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_subnet4_del_by_id(channel):
    _subnet_set(channel)

    cmd = dict(command="remote-subnet4-del-by-id", arguments={"remote": {"type": "mysql"},
                                                              "server-tags": ["abc"],
                                                              "subnets": [{"id": 5}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv4 subnet(s) deleted."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_subnet4_del_by_id_incorrect_id(channel):
    _subnet_set(channel)

    cmd = dict(command="remote-subnet4-del-by-id", arguments={"remote": {"type": "mysql"},
                                                              "server-tags": ["abc"],
                                                              "subnets": [{"id": 15}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 IPv4 subnet(s) deleted."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_subnet4_del_id_negative_missing_subnet(channel):
    _subnet_set(channel)

    cmd = dict(command="remote-subnet4-del-by-id", arguments={"remote": {"type": "mysql"},
                                                              "server-tags": ["abc"],
                                                              "subnets": [{"subnet": "192.168.50.0/24"}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"result": 1, "text": "missing 'id' parameter"}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_subnet4_del_by_prefix(channel):
    _subnet_set(channel)

    cmd = dict(command="remote-subnet4-del-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "subnets": [{"subnet": "192.168.50.0/24"}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv4 subnet(s) deleted."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_subnet4_del_by_prefix_non_existing_subnet(channel):
    _subnet_set(channel)

    cmd = dict(command="remote-subnet4-del-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "subnets": [{"subnet": "192.168.51.0/24"}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 IPv4 subnet(s) deleted."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_subnet4_del_by_prefix_missing_subnet_(channel):
    _subnet_set(channel)
    cmd = dict(command="remote-subnet4-del-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "subnets": [{"id": 2}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"result": 1, "text": "missing 'subnet' parameter"}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_subnet4_get_by_id(channel):
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"4o6-interface": "eth9",
                                                                     "4o6-interface-id": "interf-id",
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
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"subnets": [{"id": 2, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-get-by-id", arguments={"remote": {"type": "mysql"},
                                                              "server-tags": ["abc"],
                                                              "subnets": [{"id": 2}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 1,
                                      "subnets": [{"4o6-interface": "eth9",
                                                   "4o6-interface-id": "interf-id",
                                                   "4o6-subnet": "2000::/64", "authoritative": False,
                                                   "boot-file-name": "file-name", "id": 2, "interface": "enp0s9",
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


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_subnet4_get_by_id_incorrect_id(channel):
    _subnet_set(channel)

    cmd = dict(command="remote-subnet4-get-by-id", arguments={"remote": {"type": "mysql"},
                                                              "server-tags": ["abc"],
                                                              "subnets": [{"id": 3}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 0, "subnets": []},
                        "result": 3, "text": "IPv4 subnet 3 not found."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_subnet4_get_by_id_missing_id(channel):
    _subnet_set(channel)

    cmd = dict(command="remote-subnet4-get-by-id", arguments={"remote": {"type": "mysql"},
                                                              "server-tags": ["abc"],
                                                              "subnets": [{"subnet": 3}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"result": 1,
                        "text": "missing 'id' parameter"}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_subnet4_get_by_prefix(channel):
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"4o6-interface": "eth9",
                                                                     "4o6-interface-id": "interf-id",
                                                                     "4o6-subnet": "2000::/64",
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
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-get-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "subnets": [{"subnet": "192.168.50.0/24"}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {
        "count": 1,
        "subnets": [{
            "4o6-interface": "eth9",
            "4o6-interface-id": "interf-id",
            "4o6-subnet": "2000::/64",
            "authoritative": False,
            "boot-file-name": "file-name",
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
            "valid-lifetime": 1000}]}, "result": 0, "text": "IPv4 subnet '192.168.50.0/24' found."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_subnet4_get_by_prefix_negative(channel):
    _subnet_set(channel)

    cmd = dict(command="remote-subnet4-get-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "subnets": [{"subnet": "10.0.0.2/12"}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 0, "subnets": []},
                        "result": 3, "text": "IPv4 subnet '10.0.0.2/12' not found."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_subnet4_get_by_prefix_incorrect_prefix(channel):
    _subnet_set(channel)
    cmd = dict(command="remote-subnet4-get-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "subnets": [{"subnet": "10.0.0/12"}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"result": 1,
                        "text": "unable to parse invalid prefix 10.0.0/12"}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_subnet4_get_by_prefix_missing_prefix(channel):
    _subnet_set(channel)

    cmd = dict(command="remote-subnet4-get-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "subnets": [{"id": "10.0.0/12"}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"result": 1,
                        "text": "missing 'subnet' parameter"}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_subnet4_list(channel):
    _subnet_set(channel)

    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.51.0/24", "id": 3,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "pools": [
                                                                         {"pool": "192.168.51.1-192.168.51.100"}]}]})
    _send_request(cmd, channel=channel)

    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "192.168.52.0/24", "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "pools": [
                                                                         {"pool": "192.168.52.1-192.168.52.100"}]}]})
    _send_request(cmd, channel=channel)

    cmd = dict(command="remote-subnet4-list", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 3, "subnets": [{"id": 1, "subnet": "192.168.52.0/24"},
                                                              {"id": 3, "subnet": "192.168.51.0/24"},
                                                              {"id": 5, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "3 IPv4 subnet(s) found."}


# network tests
@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_network4_set_basic(channel):
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "floor13",
                                                             "subnet4": [{"subnet": "192.168.50.0/24",
                                                                          "interface": "$(SERVER_IFACE)"}]}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"shared-networks": [{"name": "floor13"}]},
                        "result": 0, "text": "IPv4 shared network successfully set."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_network4_set_missing_name(channel):
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "subnet4": [{"subnet": "192.168.50.0/24",
                                                                          "interface": "$(SERVER_IFACE)"}]}]})
    response = _send_request(cmd, channel=channel)
    if channel == 'socket':
        assert response == {"result": 1, "text": "missing parameter 'name' (<wire>:0:123)"}
    else:
        assert response == {"result": 1, "text": "missing parameter 'name' (<wire>:0:96)"}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_network4_set_empty_name(channel):
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "",
                                                             "subnet4": [{"subnet": "192.168.50.0/24",
                                                                          "interface": "$(SERVER_IFACE)"}]}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"result": 1, "text": "'name' parameter must not be empty"}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_network4_get_basic(channel):
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "interface": "$(SERVER_IFACE)",
                                                             "subnet4": [{"subnet": "192.8.0.0/24",
                                                                          "interface": "$(SERVER_IFACE)",
                                                                          "pools": [{
                                                                              "pool": "192.8.0.1-192.8.0.1"}]}]}]})
    _send_request(cmd, channel=channel)

    cmd = dict(command="remote-network4-get", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1"}]})

    response = _send_request(cmd, channel=channel)
    assert response == {"arguments": {"count": 1,
                                      "shared-networks": [{"interface": srv_msg.get_interface(), "name": "net1",
                                                           "option-data": [], "relay": {"ip-addresses": []},
                                                           "subnet4": [{"4o6-interface": "", "4o6-interface-id": "",
                                                                        "4o6-subnet": "", "id": 1, "option-data": [],
                                                                        "pools": [{"option-data": [],
                                                                                   "pool": "192.8.0.1/32"}],
                                                                        "relay": {"ip-addresses": []},
                                                                        "interface": srv_msg.get_interface(),
                                                                        "subnet": "192.8.0.0/24"}]}]},
                        "result": 0, "text": "IPv4 shared network 'net1' found."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_network4_get_all_values(channel):
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "client-class": "abc",
                                                             "rebind-timer": 200,
                                                             "renew-timer": 100,
                                                             "calculate-tee-times": True,
                                                             "t1-percent": 0.5,
                                                             "t2-percent": 0.8,
                                                             "valid-lifetime": 300,
                                                             "reservation-mode": "global",
                                                             "user-context": "some weird network",
                                                             "interface": "$(SERVER_IFACE)",
                                                             "subnet4": [{"subnet": "192.8.0.0/24",
                                                                          "interface": "$(SERVER_IFACE)",
                                                                          "pools": [{
                                                                              "pool": "192.8.0.1-192.8.0.1"}],
                                                                          "option-data": [{"code": 6,
                                                                                           "data": '192.0.2.2',
                                                                                           "always-send": True,
                                                                                           "csv-format": True}]}],
                                                             "option-data": [{"code": 6,
                                                                              "data": '192.0.2.1',
                                                                              "always-send": True,
                                                                              "csv-format": True}]}]})
    _send_request(cmd, channel=channel)

    cmd = dict(command="remote-network4-get", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1"}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 1,
                                      "shared-networks": [{"authoritative": False, "client-class": "abc",
                                                           "rebind-timer": 200, "renew-timer": 100,
                                                           "valid-lifetime": 300, "reservation-mode": "global",
                                                           "interface": srv_msg.get_interface(),
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
                                                           "subnet4": [{"subnet": "192.8.0.0/24",
                                                                        "interface": srv_msg.get_interface(),
                                                                        "option-data": [
                                                                            {"always-send": True, "code": 6,
                                                                             "csv-format": True, "data": "192.0.2.2",
                                                                             "name": "domain-name-servers",
                                                                             "space": "dhcp4"}],
                                                                        "pools": [{"pool": "192.8.0.1/32",
                                                                                   "option-data": []}]}],
                                                           "user-context": "some weird network"}]},
                        "result": 0, "text": "IPv4 shared network 'net1' found."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_network4_set_t1_t2(channel):
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "calculate-tee-times": True,
                                                             "t1-percent": 0.5,
                                                             "t2-percent": 10,
                                                             "interface": "$(SERVER_IFACE)",
                                                             "subnet4": [{"subnet": "192.8.0.0/24",
                                                                          "interface": "$(SERVER_IFACE)"}]}]})
    response = _send_request(cmd, channel=channel)
    if channel == 'http':
        assert response == {"result": 1, "text": "invalid type specified for parameter 't2-percent' (<wire>:0:266)"}
    else:
        assert response == {"result": 1, "text": "invalid type specified for parameter 't2-percent' (<wire>:0:137)"}

    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "calculate-tee-times": True,
                                                             "t1-percent": 10,
                                                             "t2-percent": 0.5,
                                                             "interface": "$(SERVER_IFACE)",
                                                             "subnet4": [{"subnet": "192.8.0.0/24",
                                                                          "interface": "$(SERVER_IFACE)"}]}]})
    response = _send_request(cmd, channel=channel)
    if channel == 'http':
        assert response == {"result": 1, "text": "invalid type specified for parameter 't1-percent' (<wire>:0:247)"}
    else:
        assert response == {"result": 1, "text": "invalid type specified for parameter 't1-percent' (<wire>:0:236)"}

    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "calculate-tee-times": True,
                                                             "t1-percent": 0.5,
                                                             "t2-percent": 0.1,
                                                             "interface": "$(SERVER_IFACE)",
                                                             "subnet4": [{"subnet": "192.8.0.0/24",
                                                                          "interface": "$(SERVER_IFACE)"}]}]})
    response = _send_request(cmd, channel=channel)
    assert False, "bug reported"  # https://gitlab.isc.org/isc-projects/kea/issues/535
    if channel == 'http':
        assert response == {"result": 1, "text": "invalid type specified for parameter 't1-percent' (<wire>:0:247)"}
    else:
        assert response == {"result": 1, "text": "invalid type specified for parameter 't1-percent' (<wire>:0:236)"}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_network4_list_basic(channel):
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "interface": "$(SERVER_IFACE)",
                                                             "subnet4": [{"subnet": "192.8.0.0/24",
                                                                          "interface": "$(SERVER_IFACE)",
                                                                          "pools": [{
                                                                              "pool": "192.8.0.1-192.8.0.1"}]}]}]})
    _send_request(cmd, channel=channel)

    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net2",
                                                             "interface": "$(SERVER_IFACE)",
                                                             "subnet4": [{"subnet": "192.9.0.0/24",
                                                                          "interface": "$(SERVER_IFACE)",
                                                                          "pools": [{
                                                                              "pool": "192.9.0.1-192.9.0.1"}]}]}]})
    _send_request(cmd, channel=channel)

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 2,
                                      "shared-networks": ["net1", "net2"]},
                        "result": 0,
                        "text": "2 IPv4 shared network(s) found."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_network4_list_no_networks(channel):
    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 0,
                                      "shared-networks": []},
                        "result": 3,
                        "text": "0 IPv4 shared network(s) found."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_network4_del_basic(channel):
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "interface": "$(SERVER_IFACE)",
                                                             "subnet4": [{"subnet": "192.8.0.0/24",
                                                                          "interface": "$(SERVER_IFACE)",
                                                                          "pools": [{
                                                                              "pool": "192.8.0.1-192.8.0.1"}]}]}]})
    _send_request(cmd, channel=channel)

    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net2",
                                                             "interface": "$(SERVER_IFACE)",
                                                             "subnet4": [{"subnet": "192.9.0.0/24",
                                                                          "interface": "$(SERVER_IFACE)",
                                                                          "pools": [{
                                                                              "pool": "192.9.0.1-192.9.0.1"}]}]}]})
    _send_request(cmd, channel=channel)

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 2,
                                      "shared-networks": ["net1", "net2"]},
                        "result": 0,
                        "text": "2 IPv4 shared network(s) found."}

    cmd = dict(command="remote-network4-del", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{"name": "net1"}]})

    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv4 shared network(s) deleted."}

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 1,
                                      "shared-networks": ["net2"]},
                        "result": 0,
                        "text": "1 IPv4 shared network(s) found."}

    cmd = dict(command="remote-network4-del", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{"name": "net2"}]})

    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv4 shared network(s) deleted."}

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 0,
                                      "shared-networks": []},
                        "result": 3,
                        "text": "0 IPv4 shared network(s) found."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_network4_del_subnet_keep(channel):
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "interface": "$(SERVER_IFACE)",
                                                             "subnet4": [{"subnet": "192.8.0.0/24",
                                                                          "interface": "$(SERVER_IFACE)",
                                                                          "pools": [{
                                                                              "pool": "192.8.0.1-192.8.0.1"}]}]}]})
    _send_request(cmd, channel=channel)

    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net2",
                                                             "interface": "$(SERVER_IFACE)",
                                                             "subnet4": [{"subnet": "192.9.0.0/24",
                                                                          "interface": "$(SERVER_IFACE)",
                                                                          "pools": [{
                                                                              "pool": "192.9.0.1-192.9.0.1"}]}]}]})
    _send_request(cmd, channel=channel)

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 2,
                                      "shared-networks": ["net1", "net2"]},
                        "result": 0,
                        "text": "2 IPv4 shared network(s) found."}

    cmd = dict(command="remote-subnet4-list", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"]})
    response = _send_request(cmd, channel=channel)

    # we want to have 2 subnets
    assert response == {"arguments": {"count": 2, "subnets": [{"id": 1, "subnet": "192.8.0.0/24"},
                                                              {"id": 2, "subnet": "192.9.0.0/24"}]},
                        "result": 0, "text": "2 IPv4 subnet(s) found."}

    cmd = dict(command="remote-network4-del", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"], "subnets-action": "keep",
                                                         "shared-networks": [{"name": "net1"}]})

    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv4 shared network(s) deleted."}

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 1,
                                      "shared-networks": ["net2"]},
                        "result": 0,
                        "text": "1 IPv4 shared network(s) found."}

    # after deleting network we still want to have 2 subnets
    cmd = dict(command="remote-subnet4-list", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 2, "subnets": [{"id": 1, "subnet": "192.8.0.0/24"},
                                                              {"id": 2, "subnet": "192.9.0.0/24"}]},
                        "result": 0, "text": "2 IPv4 subnet(s) found."}

    cmd = dict(command="remote-network4-del", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"], "subnets-action": "keep",
                                                         "shared-networks": [{"name": "net2"}]})

    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv4 shared network(s) deleted."}

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 0,
                                      "shared-networks": []},
                        "result": 3,
                        "text": "0 IPv4 shared network(s) found."}

    # after removing all networks we still want to have both subnets
    cmd = dict(command="remote-subnet4-list", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 2, "subnets": [{"id": 1, "subnet": "192.8.0.0/24"},
                                                              {"id": 2, "subnet": "192.9.0.0/24"}]},
                        "result": 0, "text": "2 IPv4 subnet(s) found."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_network4_del_subnet_delete(channel):
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "interface": "$(SERVER_IFACE)",
                                                             "subnet4": [{"subnet": "192.8.0.0/24",
                                                                          "interface": "$(SERVER_IFACE)",
                                                                          "pools": [{
                                                                              "pool": "192.8.0.1-192.8.0.1"}]}]}]})
    _send_request(cmd, channel=channel)

    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net2",
                                                             "interface": "$(SERVER_IFACE)",
                                                             "subnet4": [{"subnet": "192.9.0.0/24",
                                                                          "interface": "$(SERVER_IFACE)",
                                                                          "pools": [{
                                                                              "pool": "192.9.0.1-192.9.0.1"}]}]}]})
    _send_request(cmd, channel=channel)

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 2,
                                      "shared-networks": ["net1", "net2"]},
                        "result": 0,
                        "text": "2 IPv4 shared network(s) found."}
    # we want to find two configured subnets
    cmd = dict(command="remote-subnet4-list", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 2, "subnets": [{"id": 1, "subnet": "192.8.0.0/24"},
                                                              {"id": 2, "subnet": "192.9.0.0/24"}]},
                        "result": 0, "text": "2 IPv4 subnet(s) found."}

    cmd = dict(command="remote-network4-del", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"], "subnets-action": "delete",
                                                         "shared-networks": [{"name": "net1"}]})

    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv4 shared network(s) deleted."}

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 1,
                                      "shared-networks": ["net2"]},
                        "result": 0,
                        "text": "1 IPv4 shared network(s) found."}

    cmd = dict(command="remote-subnet4-list", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"]})
    response = _send_request(cmd, channel=channel)

    # after removing network with subnet we want to find just one subnet left
    assert response == {"arguments": {"count": 1, "subnets": [{"id": 2, "subnet": "192.9.0.0/24"}]},
                        "result": 0, "text": "1 IPv4 subnet(s) found."}

    cmd = dict(command="remote-network4-del", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"], "subnets-action": "delete",
                                                         "shared-networks": [{"name": "net2"}]})

    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv4 shared network(s) deleted."}

    cmd = dict(command="remote-network4-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 0,
                                      "shared-networks": []},
                        "result": 3,
                        "text": "0 IPv4 shared network(s) found."}

    # all subnets should be removed now
    cmd = dict(command="remote-subnet4-list", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 0, "subnets": []},
                        "result": 3, "text": "0 IPv4 subnet(s) found."}


def _set_global_parameter(channel):
    cmd = dict(command="remote-global-parameter4-set", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": [{
                                                                      "name": "boot-file-name",
                                                                      "value": "/dev/null"}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"result": 0,
                        "text": "DHCPv4 global parameter successfully set."}


# global-parameter tests
@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_parameter4_set_text(channel):
    _set_global_parameter(channel)
    assert False, "I will fail this tests because response is incomplete compared to design"


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_parameter4_set_integer(channel):
    cmd = dict(command="remote-global-parameter4-set", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": [{
                                                                      "name": "valid-lifetime",
                                                                      "value": 1000}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"result": 0,
                        "text": "DHCPv4 global parameter successfully set."}
    assert False, "I will fail this tests because response is incomplete compared to design"


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_parameter4_set_incorrect_parameter(channel):
    cmd = dict(command="remote-global-parameter4-set", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": [{
                                                                      "name": "boot-fiabcsd",
                                                                      "value": "/dev/null"}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"result": 1, "text": "unknown parameter 'boot-fiabcsd'"}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_parameter4_del(channel):
    _set_global_parameter(channel)

    cmd = dict(command="remote-global-parameter4-del", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": [{
                                                                      "name": "boot-file-name"}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 1},
                        "result": 0, "text": "1 DHCPv4 global parameter(s) deleted."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_parameter4_del_not_existing_parameter(channel):
    cmd = dict(command="remote-global-parameter4-del", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": [{
                                                                      "name": "boot-file-name"}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 0},
                        "result": 3, "text": "0 DHCPv4 global parameter(s) deleted."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_parameter4_get(channel):
    _set_global_parameter(channel)

    cmd = dict(command="remote-global-parameter4-get", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": [{
                                                                      "name": "boot-file-name"}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 1, "parameters": [{"name": "boot-file-name", "value": "/dev/null"}]},
                        "result": 0, "text": "'boot-file-name' DHCPv4 global parameter found."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_parameter4_get_all_one(channel):
    _set_global_parameter(channel)

    cmd = dict(command="remote-global-parameter4-get-all", arguments={"remote": {"type": "mysql"},
                                                                      "server-tags": ["abc"]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 1, "parameters": [{"name": "boot-file-name", "value": "/dev/null"}]},
                        "result": 0, "text": "1 DHCPv4 global parameter(s) found."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_parameter4_get_all_multiple(channel):
    _set_global_parameter(channel)

    cmd = dict(command="remote-global-parameter4-set", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": [{
                                                                      "name": "decline-probation-period",
                                                                      "value": 15}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"result": 0,
                        "text": "DHCPv4 global parameter successfully set."}

    cmd = dict(command="remote-global-parameter4-get-all", arguments={"remote": {"type": "mysql"},
                                                                      "server-tags": ["abc"]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 2, "parameters": [{"name": "boot-file-name", "value": "/dev/null"},
                                                                 {"name": "decline-probation-period", "value": 15}]},
                        "result": 0, "text": "2 DHCPv4 global parameter(s) found."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_parameter4_get_all_zero(channel):
    cmd = dict(command="remote-global-parameter4-get-all", arguments={"remote": {"type": "mysql"},
                                                                      "server-tags": ["abc"]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 0, "parameters": []},
                        "result": 3, "text": "0 DHCPv4 global parameter(s) found."}


def _set_option_def(channel):
    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 222,
                                                                "type": "uint32"}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"option-defs": [{"code": 222, "space": "dhcp4"}]},
                        "result": 0, "text": "DHCPv4 option definition successfully set."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_option_def4_set_basic(channel):
    _set_option_def(channel)


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_option_def4_set_using_zero_as_code(channel):
    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 0,
                                                                "type": "uint32"}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"option-defs": [{"code": 0, "space": "dhcp4"}]},
                        "result": 0, "text": "DHCPv4 option definition successfully set."}
    assert False, "bug reported"  # bug #500


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_option_def4_set_using_standard_code(channel):
    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 1,
                                                                "type": "uint32"}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"option-defs": [{"code": 1, "space": "dhcp4"}]},
                        "result": 0, "text": "DHCPv4 option definition successfully set."}

    cmd = dict(command="config-reload")

    response = _send_request(cmd, channel=channel)
    assert response["result"] == 1
    assert "Config reload failed" in response["text"]
    # but I think this is but so I will fail test itself
    assert False, "bug"  # bug #500


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_option_def4_set_missing_parameters(channel):
    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "code": 222,
                                                                "type": "uint32",
                                                                "array": False,
                                                                "record-types": "",
                                                                "space": "dhcp4",
                                                                "encapsulate": ""}]})
    response = _send_request(cmd, channel=channel)

    if channel == 'socket':
        assert response == {"result": 1, "text": "missing parameter 'name' (<wire>:0:93)"}
    else:
        assert response == {"result": 1, "text": "missing parameter 'name' (<wire>:0:35)"}

    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "aa",
                                                                "type": "uint32",
                                                                "array": False,
                                                                "record-types": "",
                                                                "space": "dhcp4",
                                                                "encapsulate": ""}]})
    response = _send_request(cmd, channel=channel)

    if channel == 'socket':
        assert response == {"result": 1, "text": "missing parameter 'code' (<wire>:0:93)"}
    else:
        assert response == {"result": 1, "text": "missing parameter 'code' (<wire>:0:35)"}

    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "aa",
                                                                "code": 234,
                                                                "array": False,
                                                                "record-types": "",
                                                                "space": "dhcp4",
                                                                "encapsulate": ""}]})
    response = _send_request(cmd, channel=channel)

    if channel == 'socket':
        assert response == {"result": 1, "text": "missing parameter 'type' (<wire>:0:93)"}
    else:
        assert response == {"result": 1, "text": "missing parameter 'type' (<wire>:0:35)"}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_option_def4_get_basic(channel):
    _set_option_def(channel)

    cmd = dict(command="remote-option-def4-get", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "code": 222}]})
    response = _send_request(cmd, channel=channel)
    assert response == {"arguments": {"count": 1, "option-defs": [{"array": False, "code": 222, "encapsulate": "",
                                                                   "name": "foo", "record-types": "", "space": "dhcp4",
                                                                   "type": "uint32"}]},
                        "result": 0, "text": "DHCPv4 option definition 222 in 'dhcp4' found."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_option_def4_get_multiple_defs(channel):
    _set_option_def(channel)

    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 222,
                                                                "type": "uint32",
                                                                "space": "abc"}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"option-defs": [{"code": 222, "space": "abc"}]},
                        "result": 0, "text": "DHCPv4 option definition successfully set."}

    cmd = dict(command="remote-option-def4-get", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "code": 222,
                                                                "space": "abc"}]})
    response = _send_request(cmd, channel=channel)
    assert response == {"arguments": {"count": 1, "option-defs": [{"array": False, "code": 222, "encapsulate": "",
                                                                   "name": "foo", "record-types": "", "space": "abc",
                                                                   "type": "uint32"}]},
                        "result": 0, "text": "DHCPv4 option definition 222 in 'abc' found."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_option_def4_get_missing_code(channel):
    cmd = dict(command="remote-option-def4-get", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo"}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"result": 1, "text": "missing 'code' parameter"}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_option_def4_get_all_option_not_defined(channel):
    cmd = dict(command="remote-option-def4-get-all", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 0, "option-defs": []},
                        "result": 3, "text": "0 DHCPv4 option definition(s) found."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_option_def4_get_all_multiple_defs(channel):
    _set_option_def(channel)

    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 222,
                                                                "type": "uint32",
                                                                "space": "abc"}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"option-defs": [{"code": 222, "space": "abc"}]},
                        "result": 0, "text": "DHCPv4 option definition successfully set."}

    cmd = dict(command="remote-option-def4-get-all", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})

    response = _send_request(cmd, channel=channel)
    assert response == {"arguments": {"count": 2, "option-defs": [{"array": False, "code": 222,
                                                                   "encapsulate": "", "name": "foo",
                                                                   "record-types": "", "space": "abc",
                                                                   "type": "uint32"},
                                                                  {"array": False, "code": 222,
                                                                   "encapsulate": "", "name": "foo",
                                                                   "record-types": "", "space": "dhcp4",
                                                                   "type": "uint32"}]},
                        "result": 0, "text": "2 DHCPv4 option definition(s) found."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_option_def4_get_all_basic(channel):
    _set_option_def(channel)

    cmd = dict(command="remote-option-def4-get-all", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})

    response = _send_request(cmd, channel=channel)
    assert response == {"arguments": {"count": 1, "option-defs": [{"array": False, "code": 222, "encapsulate": "",
                                                                   "name": "foo", "record-types": "", "space": "dhcp4",
                                                                   "type": "uint32"}]},
                        "result": 0, "text": "1 DHCPv4 option definition(s) found."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_option_def4_del_basic(channel):
    _set_option_def(channel)

    cmd = dict(command="remote-option-def4-del", arguments={"remote": {"type": "mysql"},
                                                            "option-defs": [{"code": 222}]})

    response = _send_request(cmd, channel=channel)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv4 option definition(s) deleted."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_option_def4_del_different_space(channel):
    _set_option_def(channel)

    cmd = dict(command="remote-option-def4-del", arguments={"remote": {"type": "mysql"},
                                                            "option-defs": [{"code": 222, "space": "abc"}]})

    response = _send_request(cmd, channel=channel)
    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 DHCPv4 option definition(s) deleted."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_option_def4_del_incorrect_code(channel):
    cmd = dict(command="remote-option-def4-del", arguments={"remote": {"type": "mysql"}, "option-defs": [{"name": 22}]})

    response = _send_request(cmd, channel=channel)
    assert response == {"result": 1, "text": "missing 'code' parameter"}

    cmd = dict(command="remote-option-def4-del", arguments={"remote": {"type": "mysql"}, "option-defs": [{}]})

    response = _send_request(cmd, channel=channel)
    assert response == {"result": 1, "text": "missing 'code' parameter"}

    cmd = dict(command="remote-option-def4-del", arguments={"remote": {"type": "mysql"},
                                                            "option-defs": [{"code": "abc"}]})

    response = _send_request(cmd, channel=channel)
    assert response == {"result": 1, "text": "'code' parameter is not an integer"}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_option_def4_del_missing_option(channel):
    cmd = dict(command="remote-option-def4-del", arguments={"remote": {"type": "mysql"},
                                                            "option-defs": [{"code": 212}]})

    response = _send_request(cmd, channel=channel)
    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 DHCPv4 option definition(s) deleted."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_option_def4_del_multiple_options(channel):
    _set_option_def(channel)

    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 222,
                                                                "type": "uint32",
                                                                "space": "abc"}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"option-defs": [{"code": 222, "space": "abc"}]},
                        "result": 0, "text": "DHCPv4 option definition successfully set."}

    cmd = dict(command="remote-option-def4-del", arguments={"remote": {"type": "mysql"},
                                                            "option-defs": [{"code": 222}]})

    response = _send_request(cmd, channel=channel)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv4 option definition(s) deleted."}

    cmd = dict(command="remote-option-def4-get-all", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})

    response = _send_request(cmd, channel=channel)
    assert response == {"arguments": {"count": 1, "option-defs": [{"array": False, "code": 222, "encapsulate": "",
                                                                   "name": "foo", "record-types": "", "space": "abc",
                                                                   "type": "uint32"}]},
                        "result": 0, "text": "1 DHCPv4 option definition(s) found."}


def _set_global_option(channel):
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "code": 6,
                                                                   "data": "192.0.2.1, 192.0.2.2"}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"result": 0, "text": "DHCPv4 option successfully set.",
                        "arguments": {"options": [{"code": 6, "space": "dhcp4"}]}}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_option4_global_set_basic(channel):
    _set_global_option(channel)


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_option4_global_set_missing_data(channel):
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "code": 6}]})
    response = _send_request(cmd, channel=channel)
    # bug #501
    assert response == {"result": 3, "text": "Missing data parameter"}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_option4_global_set_name(channel):
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "name": "host-name",
                                                                   "data": "isc.example.com"}]})
    response = _send_request(cmd, channel=channel)
    assert response == {"arguments": {"options": [{"code": 12, "space": "dhcp4"}]},
                        "result": 0, "text": "DHCPv4 option successfully set."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_option4_global_set_incorrect_code_missing_name(channel):
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "code": "aaa"}]})
    response = _send_request(cmd, channel=channel)

    if channel == "http":
        assert response == {"result": 1,
                            "text": "option data configuration requires one of "
                                    "'code' or 'name' parameters to be specified (<wire>:0:31)"}
    else:
        assert response == {"result": 1,
                            "text": "option data configuration requires one of "
                                    "'code' or 'name' parameters to be specified (<wire>:0:121)"}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_option4_global_set_incorrect_name_missing_code(channel):
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "name": 123}]})
    response = _send_request(cmd, channel=channel)

    if channel == "http":
        assert response == {"result": 1,
                            "text": "option data configuration requires one of "
                                    "'code' or 'name' parameters to be specified (<wire>:0:31)"}
    else:
        assert response == {"result": 1,
                            "text": "option data configuration requires one of "
                                    "'code' or 'name' parameters to be specified (<wire>:0:121)"}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_option4_global_set_missing_code_and_name(channel):
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{}]})
    response = _send_request(cmd, channel=channel)

    if channel == "http":
        assert response == {"result": 1,
                            "text": "option data configuration requires one of "
                                    "'code' or 'name' parameters to be specified (<wire>:0:31)"}
    else:
        assert response == {"result": 1,
                            "text": "option data configuration requires one of "
                                    "'code' or 'name' parameters to be specified (<wire>:0:121)"}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_option4_global_set_incorrect_code(channel):
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": "aa",
                                                                            "name": "cc"}]})
    response = _send_request(cmd, channel=channel)

    if channel == "http":
        assert response == {"result": 1,
                            "text": "definition for the option 'dhcp4.cc' having code '0' does not exist (<wire>:0:54)"}
    else:
        assert response == {"result": 1,
                            "text": "definition for the option 'dhcp4.cc' "
                                    "having code '0' does not exist (<wire>:0:143)"}
    assert False, "looks like incorrect message"
    # bug/not implemented feature


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_option4_global_set_incorrect_name(channel):
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 12,
                                                                            "name": 12,
                                                                            "data": 'isc.example.com'}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"bug, shouldn't be accepted?"}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_option4_global_get_basic(channel):
    _set_global_option(channel)

    cmd = dict(command="remote-option4-global-get", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6}]})
    response = _send_request(cmd, channel=channel)
    assert response == {"arguments": {"count": 1, "options": [{"always-send": False, "code": 6, "csv-format": True,
                                                               "data": "192.0.2.1, 192.0.2.2",
                                                               "name": "domain-name-servers", "space": "dhcp4"}]},
                        "result": 0, "text": "DHCPv4 option 6 in 'dhcp4' found."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_option4_global_set_different_space(channel):
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6,
                                                                            "data": '192.0.2.1, 192.0.2.2',
                                                                            "always-send": True,
                                                                            "csv-format": True,
                                                                            "space": "xyz"}]})
    response = _send_request(cmd, channel=channel)

    if channel == 'http':
        assert response == {"result": 1,
                            "text": "definition for the option 'xyz.' having code '6' does not exist (<wire>:0:31)"}
    else:
        assert response == {"result": 1, "text": "definition for the option 'xyz.'"
                                                 " having code '6' does not exist (<wire>:0:121)"}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_option4_global_set_csv_false_incorrect(channel):
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6,
                                                                            "data": '192.0.2.1',
                                                                            "always-send": True,
                                                                            "csv-format": False}]})
    response = _send_request(cmd, channel=channel)

    if channel == 'http':
        assert response == {"result": 1, "text": "option data is not a valid "
                                                 "string of hexadecimal digits: 192.0.2.1 (<wire>:0:93)"}
    else:
        assert response == {"result": 1, "text": "option data is not a valid "
                                                 "string of hexadecimal digits: 192.0.2.1 (<wire>:0:182)"}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_option4_global_set_csv_false_correct(channel):
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6,
                                                                            "data": "C0000201",  # 199.0.2.1
                                                                            "always-send": True,
                                                                            "csv-format": False}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"result": 0, "text": "DHCPv4 option successfully set.",
                        "arguments": {"options": [{"code": 6, "space": "dhcp4"}]}}

    # TODO after merging kea feature don't forget to run this code
    # misc.test_procedure()
    # srv_msg.client_requests_option('6')
    # srv_msg.client_send_msg('DISCOVER')
    #
    # misc.pass_criteria()
    # srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    # srv_msg.response_check_include_option('Response', None, '6')
    # srv_msg.response_check_option_content('Response', '6', None, 'value', '199.0.2.1')


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_option4_global_set_csv_false_incorrect_hex(channel):
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6,
                                                                            "data": "C0000201Z",
                                                                            "always-send": True,
                                                                            "csv-format": False}]})
    response = _send_request(cmd, channel=channel)

    assert response["result"] == 1
    assert "option data is not a valid string of hexadecimal digits: C0000201Z" in response["text"]


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_option4_global_del_basic(channel):
    _set_global_option(channel)

    cmd = dict(command="remote-option4-global-del", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6}]})
    response = _send_request(cmd, channel=channel)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv4 option(s) deleted."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_option4_global_del_missing_code(channel):
    cmd = dict(command="remote-option4-global-del", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"ab": 6}]})
    response = _send_request(cmd, channel=channel)
    assert response == {"result": 1, "text": "missing 'code' parameter"}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_option4_global_del_incorrect_code(channel):
    cmd = dict(command="remote-option4-global-del", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": "6"}]})
    response = _send_request(cmd, channel=channel)
    assert response == {"result": 1, "text": "'code' parameter is not an integer"}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_option4_global_del_missing_option(channel):
    cmd = dict(command="remote-option4-global-del", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6}]})
    response = _send_request(cmd, channel=channel)
    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 DHCPv4 option(s) deleted."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_option4_global_get_missing_code(channel):
    cmd = dict(command="remote-option4-global-get", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"ab": 6}]})
    response = _send_request(cmd, channel=channel)
    assert response == {"result": 1, "text": "missing 'code' parameter"}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_option4_global_get_incorrect_code(channel):
    cmd = dict(command="remote-option4-global-get", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": "6"}]})
    response = _send_request(cmd, channel=channel)
    assert response == {"result": 1, "text": "'code' parameter is not an integer"}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_option4_global_get_missing_option(channel):
    cmd = dict(command="remote-option4-global-get", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6}]})
    response = _send_request(cmd, channel=channel)
    assert response == {"arguments": {"count": 0, "options": []},
                        "result": 3, "text": "DHCPv4 option 6 in 'dhcp4' not found."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_option4_global_get_csv_false(channel):
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6,
                                                                            "data": "31 39 32 2e 31 30 2e 30 2e 31",
                                                                            "always-send": True,
                                                                            "csv-format": False}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"result": 0, "text": "DHCPv4 option successfully set.",
                        "arguments": {"options": [{"code": 6, "space": "dhcp4"}]}}

    cmd = dict(command="remote-option4-global-get", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6}]})
    response = _send_request(cmd, channel=channel)
    assert response == {"arguments": {"count": 1, "options": [{"always-send": False, "code": 6, "csv-format": True,
                                                               "data": "31 39 32 2e 31 30 2e 30 2e 31",
                                                               "name": "domain-name-servers", "space": "dhcp4"}]},
                        "result": 0, "text": "DHCPv4 option 6 in 'dhcp4' found."}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_option4_global_get_all(channel):
    _set_global_option(channel)

    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "code": 16,
                                                                   "data": "199.199.199.1"}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"result": 0, "text": "DHCPv4 option successfully set.",
                        "arguments": {"options": [{"code": 16, "space": "dhcp4"}]}}

    cmd = dict(command="remote-option4-global-get-all", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})

    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"count": 2,
                                      "options": [{"always-send": False, "code": 6, "csv-format": True,
                                                   "data": "192.0.2.1, 192.0.2.2", "name": "domain-name-servers",
                                                   "space": "dhcp4"},
                                                  {"always-send": False, "code": 16, "csv-format": True,
                                                   "data": "199.199.199.1", "name": "swap-server", "space": "dhcp4"}]},
                        "result": 0, "text": "2 DHCPv4 option(s) found."}

    cmd = dict(command="remote-option4-global-del", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6}]})
    response = _send_request(cmd, channel=channel)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv4 option(s) deleted."}

    cmd = dict(command="remote-option4-global-get-all", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})

    response = _send_request(cmd, channel=channel)
    assert response == {"arguments": {"count": 1, "options": [{"always-send": False, "code": 16, "csv-format": True,
                                                               "data": "199.199.199.1", "name": "swap-server",
                                                               "space": "dhcp4"}]},
                        "result": 0, "text": "1 DHCPv4 option(s) found."}

    cmd = dict(command="remote-option4-global-del", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 16}]})
    response = _send_request(cmd, channel=channel)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv4 option(s) deleted."}

    cmd = dict(command="remote-option4-global-get-all", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})

    response = _send_request(cmd, channel=channel)
    assert response == {"arguments": {"count": 0, "options": []}, "result": 3, "text": "0 DHCPv4 option(s) found."}
