"""Kea config backend testing subnets."""

import pytest

from .cb_cmds import setup_server_for_config_backend_cmds
from .cb_cmds import send_discovery_with_no_answer
from .cb_cmds import get_address, set_subnet, del_subnet


pytestmark = [pytest.mark.kea_only,
              pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.config_backend]


# TODO: Kea does not supported v6 yet
# @pytest.mark.v6
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
@pytest.mark.parametrize("del_cmd", ['by-id', 'by-prefix'])
def test_subnet_set_and_del_and_set(del_cmd):
    setup_server_for_config_backend_cmds()

    # send discover but no response should come back as there is no subnet defined yet
    send_discovery_with_no_answer()

    # define one subnet and now response for discover should be received
    set_subnet(pool="192.168.50.100-192.168.50.100")

    # send discover and now offer should be received
    get_address(exp_yiaddr='192.168.50.100')

    # delete added subnet by id or prefix, now there should be no answer to discover
    del_subnet(del_cmd)

    # send discover and now offer should NOT be received
    send_discovery_with_no_answer()

    # define similar subnet and now response for discover should be received
    set_subnet(pool="192.168.50.200-192.168.50.200")

    # send discover and now offer should be received
    get_address(exp_yiaddr='192.168.50.200')


# TODO: server-tags are not supported by Kea yet
# @pytest.mark.v4
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
