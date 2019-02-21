"""Kea DB config hook testing"""

import pytest
from features import srv_msg, srv_control, misc


def _setup_server_for_config_backend_cmds():
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.add_hooks('$(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_cb_cmds.so')
    srv_control.add_hooks('$(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_mysql_cb.so')
    srv_control.open_control_channel(
        'unix',
        '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel('$(SRV4_ADDR)',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.run_command(
        '"config-control":{"config-databases":[{"user":"$(DB_USER)",'
        '"password":"$(DB_PASSWD)","name":"$(DB_NAME)","type":"mysql"}]}')
    srv_control.run_command(',"server-tag": "abc"')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')


@pytest.mark.v4
@pytest.mark.config_backend
@pytest.mark.kea_only
def test_subnet_set_v4():
    dhcp_version = 'v4'
    _setup_server_for_config_backend_cmds()

    # send discover but no response should come back as there is no subnet defined yet
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')
    srv_msg.send_wait_for_message("MUST", False, "None")

    # define one subnet and now response for discover should be received
    cmd = {"command": "remote-subnet4-set",
           "arguments": {"remote": {"type": "mysql"},
                         "server-tags": ["abc"],
                         "subnets": [{
                             "subnet": "192.168.50.0/24",
                             "interface": "$(SERVER_IFACE)",
                             "pools": [{"pool": "192.168.50.1-192.168.50.100"}]}]}}
    response = srv_msg.send_request(dhcp_version, cmd)
    assert response["result"] == 0
    srv_control.start_srv('DHCP', 'restarted')

    # send discover and now offer should be received
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')


# TODO: Kea does not supported v6 yet
# @pytest.mark.v6
# @pytest.mark.config_backend
# @pytest.mark.kea_only
# def test_subnet_set_v6():
#     dhcp_version = 'v6'
#     _setup_server_for_config_backend_cmds()

#     # send discover but no response should come back as there is no subnet defined yet
#     misc.test_procedure()
#     srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
#     srv_msg.client_does_include('Client', None, 'client-id')
#     srv_msg.client_does_include('Client', None, 'IA-NA')
#     srv_msg.client_send_msg('SOLICIT')
#     msgs = srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
#     # check that status-code is NoAddrsAvail
#     srv_msg.response_check_include_option('Response', None, '3')
#     srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '13')
#     srv_msg.response_check_suboption_content('Response', '13', '3', None, 'statuscode', '2')

#     # define one subnet and now response for discover should be received
#     cmd = {"command": "remote-subnet6-set",
#            "arguments": {"remote": {"type": "mysql"},
#                          "server-tags": ["abc"],
#                          "subnets": [{
#                              "subnet": "2001:db8:1::/64",
#                              "interface":"$(SERVER_IFACE)",
#                              "pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}
#     response = srv_msg.send_request(dhcp_version, cmd)
#     assert response["result"] == 0
#     srv_control.start_srv('DHCP', 'restarted')

#     # send discover and now offer should be received
#     misc.test_procedure()
#     srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
#     srv_msg.client_does_include('Client', None, 'client-id')
#     srv_msg.client_does_include('Client', None, 'IA-NA')
#     srv_msg.client_send_msg('SOLICIT')
#     srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
#     # check that status-code is
#     srv_msg.response_check_include_option('Response', None, '3')
#     srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '13')
#     srv_msg.response_check_suboption_content('Response', '13', '3', None, 'statuscode', '')  # TODO


@pytest.mark.v4
@pytest.mark.config_backend
@pytest.mark.kea_only
@pytest.mark.parametrize("del_cmd", ['by-id', 'by-prefix'])
def test_subnet_set_and_del_and_set(del_cmd):
    dhcp_version = 'v4'
    _setup_server_for_config_backend_cmds()

    # send discover but no response should come back as there is no subnet defined yet
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')
    srv_msg.send_wait_for_message("MUST", False, "None")

    # define one subnet and now response for discover should be received
    cmd = {"command": "remote-subnet4-set",
           "arguments": {"remote": {"type": "mysql"},
                         "server-tags": ["abc"],
                         "subnets": [
                             {"subnet": "192.168.50.0/24",
                              "interface": "$(SERVER_IFACE)",
                              "pools": [{"pool": "192.168.50.100-192.168.50.100"}]}]}}
    response = srv_msg.send_request(dhcp_version, cmd)
    assert response["result"] == 0
    srv_control.start_srv('DHCP', 'restarted')

    # send discover and now offer should be received
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')

    # delete added subnet by id or prefix, now there should be no answer to discover
    if del_cmd == 'by-id':
        cmd = {"command": "remote-subnet4-del-by-id",
               "arguments": {"remote": {"type": "mysql"},
                             "server-tags": ["all"],
                             "subnets": [{"id": 1}]}}
    else:
        cmd = {"command": "remote-subnet4-del-by-prefix",
               "arguments": {"remote": {"type": "mysql"},
                             "server-tags": ["all"],
                             "subnets": [{"subnet": "192.168.50.0/24"}]}}

    response = srv_msg.send_request(dhcp_version, cmd)
    assert response["result"] == 0
    srv_control.start_srv('DHCP', 'restarted')

    # send discover and now offer should NOT be received
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')
    srv_msg.send_wait_for_message("MUST", False, "None")

    # define similar subnet and now response for discover should be received
    cmd = {"command": "remote-subnet4-set",
           "arguments": {"remote": {"type": "mysql"},
                         "server-tags": ["abc"],
                         "subnets": [
                             {"subnet": "192.168.50.0/24",
                              "interface": "$(SERVER_IFACE)",
                              "pools": [{"pool": "192.168.50.200-192.168.50.200"}]}]}}
    response = srv_msg.send_request(dhcp_version, cmd)
    assert response["result"] == 0
    srv_control.start_srv('DHCP', 'restarted')

    # send discover and now offer should be received
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')
    misc.pass_criteria()
    msgs = srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    # only 1 message received
    assert len(msgs) == 1
    # with address from tested server
    assert msgs[0].yiaddr == '192.168.50.200'


# TODO: server-tags are not supported by Kea yet
# @pytest.mark.v4
# @pytest.mark.config_backend
# @pytest.mark.kea_only
# def test_subnet_set_on_different_server_tag():
#     dhcp_version = 'v4'
#     _setup_server_for_config_backend_cmds()

#     # send discover but no response should come back as there is no subnet defined yet
#     misc.test_procedure()
#     srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
#     srv_msg.client_send_msg('DISCOVER')
#     srv_msg.send_wait_for_message("MUST", False, "None")

#     # define one subnet but on similar server-tag 'abc-wrong' instead of 'abc'
#     cmd = {"command": "remote-subnet4-set",
#            "arguments": {"remote": {"type": "mysql"},
#                          "server-tags": ["another-abc"],
#                          "subnets": [
#                              {"subnet": "192.168.50.0/24",
#                               "interface": "$(SERVER_IFACE)",
#                               "pools": [{"pool": "192.168.50.100-192.168.50.100"}]}]}}
#     response = srv_msg.send_request(dhcp_version, cmd)
#     assert response["result"] == 0
#     srv_control.start_srv('DHCP', 'restarted')

#     # send discover and now offer should NOT be received
#     misc.test_procedure()
#     srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
#     srv_msg.client_send_msg('DISCOVER')
#     misc.pass_criteria()
#     srv_msg.send_wait_for_message('MUST', None, 'None')


# TODO: server-tags are not supported by Kea yet
# @pytest.mark.v4
# @pytest.mark.config_backend
# @pytest.mark.kea_only
# def test_subnets_set_on_different_servers():
#     # There are 3 defined subnets on 3 different servers using different server-tag.
#     # Tested server
#     dhcp_version = 'v4'
#     _setup_server_for_config_backend_cmds()

#     # send discover but no response should come back as there is no subnet defined yet
#     misc.test_procedure()
#     srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
#     srv_msg.client_send_msg('DISCOVER')
#     srv_msg.send_wait_for_message("MUST", False, "None")

#     # add subnet 1 to server def (unknown server)
#     cmd = {"command": "remote-subnet4-set",
#            "arguments": {"remote": {"type": "mysql"},
#                          "server-tags": ["def"],
#                          "subnets": [{
#                              "subnet": "192.168.50.0/24",
#                              "interface": "$(SERVER_IFACE)",
#                              "pools": [{"pool": "192.168.50.1-192.168.50.100"}]}]}}
#     response = srv_msg.send_request(dhcp_version, cmd)
#     assert response["result"] == 0

#     # add subnet 1 to server abc (tested server)
#     cmd = {"command": "remote-subnet4-set",
#            "arguments": {"remote": {"type": "mysql"},
#                          "server-tags": ["abc"],
#                          "subnets": [{
#                              "subnet": "192.168.50.0/24",
#                              "interface": "$(SERVER_IFACE)",
#                              "pools": [{"pool": "192.168.51.1-192.168.51.100"}]}]}}
#     response = srv_msg.send_request(dhcp_version, cmd)
#     assert response["result"] == 0

#     # add subnet 3 to server xyz (unknown server)
#     cmd = {"command": "remote-subnet4-set",
#            "arguments": {"remote": {"type": "mysql"},
#                          "server-tags": ["xyz"],
#                          "subnets": [{
#                              "subnet": "192.168.52.0/24",
#                              "interface": "$(SERVER_IFACE)",
#                              "pools": [{"pool": "192.168.52.1-192.168.52.100"}]}]}}
#     response = srv_msg.send_request(dhcp_version, cmd)
#     assert response["result"] == 0

#     # restart tested server
#     srv_control.start_srv('DHCP', 'restarted')

#     # send discover and now offer should be received with address allocated
#     # by tested server
#     misc.test_procedure()
#     srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
#     srv_msg.client_send_msg('DISCOVER')
#     msgs = srv_msg.send_wait_for_message('MUST', None, 'OFFER')
#     # only 1 message received
#     assert len(msgs) == 1
#     # with address from tested server
#     assert msgs[0].yiaddr == '192.168.51.1'
