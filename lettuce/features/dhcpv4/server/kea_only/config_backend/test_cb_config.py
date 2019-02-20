"""Kea DB config hook testing"""

import sys
import pytest
import srv_msg
import misc
import srv_control


def _setup_server_for_config_backend_cmds(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '$(EMPTY)', '$(EMPTY)')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_cb_cmds.so')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_mysql_cb.so')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.run_command(step,
                            '"config-control":{"config-databases":[{"user":"$(DB_USER)",'
                            '"password":"$(DB_PASSWD)","name":"$(DB_NAME)","type":"mysql"}]}')
    srv_control.run_command(step, ',"server-tag": "abc"')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')


@pytest.mark.py_test
@pytest.mark.v4
@pytest.mark.config_backend
@pytest.mark.kea_only
def test_v4_config_backend_subnet_set(step):
    _setup_server_for_config_backend_cmds(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, "MUST", False, "None")

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"list-commands"}')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"remote-subnet4-set","arguments":{"remote":{"type":"mysql"},'
                                            '"server-tags":["abc"],'
                                            '"subnets":[{"subnet": "192.168.50.0/24","interface": "$(SERVER_IFACE)",'
                                            '"pools": [{"pool": "192.168.50.1-192.168.50.100"}]}]}}')

    srv_control.start_srv(step, 'DHCP', 'restarted')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "config-get", "arguments": {}}')
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')


@pytest.mark.v4
@pytest.mark.config_backend
@pytest.mark.kea_only
def test_v4_config_backend_subnet_set_and_del(step):
    _setup_server_for_config_backend_cmds(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, "MUST", False, "None")

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"list-commands"}')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "config-get", "arguments": {}}')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"remote-subnet4-set","arguments":{"remote":{"type":"mysql"},"server-tags":["abc-my-server"],"subnets":[{"subnet": "192.168.50.0/24","interface": "$(SERVER_IFACE)","pools": [{"pool": "192.168.50.100-192.168.50.100"}]}]}}')

    srv_control.start_srv(step, 'DHCP', 'restarted')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "config-get", "arguments": {}}')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"remote-subnet4-del-by-id", "arguments": {"subnets":[{"id":1}],"remote":{"type":"mysql"},"server-tags":["all"]}}}')

    srv_control.start_srv(step, 'DHCP', 'restarted')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, "MUST", False, "None")


@pytest.mark.py_test
@pytest.mark.v4
@pytest.mark.config_backend
@pytest.mark.kea_only
def test_v4_config_backend_subnet_set_2(step):
    _setup_server_for_config_backend_cmds(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, "MUST", False, "None")

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"list-commands"}')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"remote-subnet4-set","arguments":{"remote":{"type":"mysql"},"server-tags":["abc"],"subnets":[{"subnet": "192.168.50.0/24","interface": "$(SERVER_IFACE)","pools": [{"pool": "192.168.50.1-192.168.50.100"}]}]}}')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"remote-subnet4-set","arguments":{"remote":{"type":"mysql"},"server-tags":["def"],"subnets":[{"subnet": "192.168.51.0/24","interface": "$(SERVER_IFACE)","pools": [{"pool": "192.168.51.1-192.168.51.100"}]}]}}')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"remote-subnet4-set","arguments":{"remote":{"type":"mysql"},"server-tags":["xyz"],"subnets":[{"subnet": "192.168.52.0/24","interface": "$(SERVER_IFACE)","pools": [{"pool": "192.168.52.1-192.168.52.100"}]}]}}')

    srv_control.start_srv(step, 'DHCP', 'restarted')
    srv_msg.test_pause(step)
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "config-get", "arguments": {}}')
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
