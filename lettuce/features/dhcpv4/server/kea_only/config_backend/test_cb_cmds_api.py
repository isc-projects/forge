"""Kea database config backend commands hook testing"""

import json
import pytest
import features.srv_msg as srv_msg
import features.srv_control as srv_control
import features.misc as misc

pytestmark = [pytest.mark.py_test,
              pytest.mark.v4,
              # pytest.mark.v6, TODO change it when feature is ready for v6
              pytest.mark.kea_only,
              pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.config_backend,
              pytest.mark.cb_cmds]

DHCP_VERSION = srv_msg.world.proto


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
        if DHCP_VERSION == 'v4':
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


def _check_kea():
    srv_control.start_srv('DHCP', 'restarted')
    srv_msg.send_through_socket_server_site(
        '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
        '{"command": "config-get", "arguments": {}}')


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
def test_remote_subnet4_set_id_duplicated_id(channel):
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
def test_remote_subnet4_set_id_duplicated_subnet(channel):
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

    assert response == {"arguments": {"subnets": [{"id": 5, "subnet": "192.168.51.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}
    #
    # cmd = dict(command="remote-subnet4-list", arguments={"remote": {"type": "mysql"},
    #                                                      "server-tags": ["abc"]})
    # response = _send_request(cmd, channel=channel)
    #
    # assert response == {"arguments": {
    #     "count": 1,
    #     "subnets": [
    #         {
    #             "id": 5,
    #             "subnet": "192.168.51.0/24"
    #         }
    #     ]
    # },
    #     "result": 0,
    #     "text": "1 IPv4 subnet(s) found."
    # }


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
                                                                     "pools": [{"pool": "192.168.50.1-192.168.50.100"}],
                                                                     "relay": {"ip-addresses": ["192.168.5.5"]},
                                                                     "reservation-mode": "all",
                                                                     "server-hostname": "name-xyz",
                                                                     "subnet": "192.168.50.0/24",
                                                                     "valid-lifetime": 1000}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"subnets": [{"id": 2, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}


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
                                                                     "pools": [{"pool": "192.168.50.1-192.168.50.100"}],
                                                                     "relay": {"ip-addresses": ["192.168.5.5"]},
                                                                     "reservation-mode": "all",
                                                                     "server-hostname": "name-xyz",
                                                                     "subnet": "192.168.50.0/24",
                                                                     "valid-lifetime": 1000}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"subnets": [{"id": 2, "subnet": "192.168.50.0/24"}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}

    cmd = dict(command="remote-subnet4-get-by-id", arguments={"remote": {"type": "mysql"},
                                                              "server-tags": ["abc"],
                                                              "subnets": [{"id": 2}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {
        "count": 1,
        "subnets": [{
            "4o6-interface": "eth9",
            "4o6-interface-id": "interf-id",
            "4o6-subnet": "2000::/64",
            "authoritative": False,
            "boot-file-name": "file-name",
            "id": 2,
            "interface": "$(SERVER_IFACE)",
            "match-client-id": False,
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
            "valid-lifetime": 1000}]}, "result": 0, "text": "IPv4 subnet 2 found."}


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
            "interface": "$(SERVER_IFACE)",
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
# "remote-network4-del",
# "remote-network4-get",
# "remote-network4-list",
# "remote-network4-set",


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

    assert response == {}


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_network4_set_empty_name(channel):
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "",
                                                             "subnet4": [{"subnet": "192.168.50.0/24",
                                                                          "interface": "$(SERVER_IFACE)"}]}]})
    response = _send_request(cmd, channel=channel)

    assert response == {}


# @pytest.mark.parametrize("channel", ['http', 'socket'])
# def test_remote_network4_set_basic(channel):
#     cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"},
#                                                          "server-tags": ["abc"],
#                                                          "shared-networks": [{
#                                                              "name": "floor13",
#                                                              "subnet4": [{"subnet": "192.168.50.0/24",
#                                                                           "interface": "$(SERVER_IFACE)"}]}]})
#     response = _send_request(cmd, channel=channel)
#
#     assert response == {}


# global-parameter tests

# "remote-global-parameter4-del",
# "remote-global-parameter4-get",
# "remote-global-parameter4-get-all",
# "remote-global-parameter4-set",

@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_parameter4_set_basic(channel):
    cmd = dict(command="remote-global-parameter4-set", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": [{
                                                                      "name": "boot-file-name",
                                                                      "value": "/dev/null"
                                                                  }]})
    response = _send_request(cmd, channel=channel)

    assert response == {"result": 0,
                        "text": "DHCPv4 global parameter successfully set."}


# "remote-option-def4-del",
# "remote-option-def4-get",
# "remote-option-def4-get-all",
# "remote-option-def4-set",


@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_option_def4_set_basic(channel):
    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 222,
                                                                "type": "uint32",
                                                                "array": False,
                                                                "record-types": "",
                                                                "space": "dhcp4",
                                                                "encapsulate": ""}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"arguments": {"option-defs": [{"code": 222, "space": "dhcp4"}]},
                        "result": 0, "text": "DHCPv4 option definition successfully set."}


# "remote-option4-global-del",
# "remote-option4-global-get",
# "remote-option4-global-get-all",
# "remote-option4-global-set",

@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_remote_global_option4_global_set_basic(channel):
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "code": 6,
                                                                   "space": "dhcp4",
                                                                   "data": "192.0.2.1, 192.0.2.2"}]})
    response = _send_request(cmd, channel=channel)

    assert response == {"result": 0, "text": "DHCPv4 option successfully set.",
                        "arguments": {"options": [{"code": 6, "space": "dhcp4"}]}}
