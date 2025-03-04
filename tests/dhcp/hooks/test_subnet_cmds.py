# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea Subnet manipulation commands"""

# pylint: disable=line-too-long

import pytest

from src import srv_control
from src import srv_msg
from src import misc

from src.forge_cfg import world
from src.protosupport.multi_protocol_functions import wait_for_message_in_log
from src.softwaresupport.cb_model import setup_server_for_config_backend_cmds


def _config_get(exp_result: int = 0, exp_failed: bool = False) -> dict:
    """_config_get sent config-get command and return arguments part of the response

    :param exp_result: expected result from Kea (0,1,3), defaults to 0
    :type exp_result: int, optional
    :param exp_failed: does the test expect failure in sending the message, defaults to False
    :type exp_failed: bool, optional
    :return: arguments part of the response
    :rtype: dict
    """
    cmd = {"command": "config-get"}  # get config
    rsp = srv_msg.send_ctrl_cmd(cmd, exp_failed=exp_failed, exp_result=exp_result)
    if "arguments" in rsp:
        return rsp["arguments"]
    return rsp


def _save_and_reload(exp_result: int = 0, exp_failed: bool = False) -> tuple:
    """_save_and_reload Save Kea confing using config-write and reload it using config-reload

    :param exp_result: expected result from Kea (0,1,3), defaults to 0
    :type exp_result: int, optional
    :param exp_failed: does the test expect failure in sending the message, defaults to False
    :type exp_failed: bool, optional
    :return: return both responses from kea
    :rtype: tuple
    """
    cmd = {"command": "config-write", "arguments": {}}  # save config
    resp1 = srv_msg.send_ctrl_cmd(cmd, exp_failed=exp_failed, exp_result=exp_result)
    cmd = {"command": "config-reload", "arguments": {}}  # reload config
    resp2 = srv_msg.send_ctrl_cmd(cmd, exp_failed=exp_failed, exp_result=exp_result)
    return resp1, resp2


def _send_command(cmd: str, arguments: dict = None, exp_result: int = 0, exp_failed: bool = False) -> dict:
    """_send_command Send command to Kea server

    :param cmd: command to send
    :type cmd: str
    :param arguments: arguments if needed, defaults to None
    :type arguments: dict, optional
    :param exp_result: expected result from Kea (0,1,3), defaults to 0
    :type exp_result: int, optional
    :param exp_failed: does the test expect failure in sending the message, defaults to False
    :type exp_failed: bool, optional
    :return: arguments part of the response
    :rtype: dict
    """
    if arguments is None:
        arguments = {}
    cmd = {"command": cmd, "arguments": arguments}
    rsp = srv_msg.send_ctrl_cmd(cmd, exp_failed=exp_failed, exp_result=exp_result)
    if "arguments" in rsp:
        return rsp["arguments"]
    return rsp


def _check_hash_after_config_reload() -> None:
    """_check_hash_after_config_reload Sent config-get and save hash, than use _save_and_reload to save
    save config and restart Kea, than send config-get again and check if hash is the same
    """
    old_hash = _config_get()["hash"]
    _save_and_reload()
    srv_msg.forge_sleep(2)
    new_hash = _config_get()["hash"]
    assert (
        old_hash == new_hash
    ), "Config hash after reload should be the same as before reload"


def _discover(mac: str, addr: str = None) -> str:
    """_discover send DISCOVER message with mac and check if Kea response with OFFER, if address
    is not provided, test expect no response in return.

    :param mac: MAC address of the client
    :type mac: str
    :param addr: IP v4 address, defaults to None
    :type addr: str, optional
    :return: ip address Kea assigned to the client
    :rtype: str
    """
    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value("Client", "chaddr", mac)
    srv_msg.client_send_msg("DISCOVER")

    misc.pass_criteria()
    if addr:
        rsp = srv_msg.send_wait_for_message("MUST", "OFFER")[0]
        srv_msg.response_check_content("yiaddr", addr)
        srv_msg.response_check_content("chaddr", mac)
        srv_msg.response_check_include_option(1)
        srv_msg.response_check_option_content(1, "value", "255.255.255.0")
        return rsp.yiaddr
    srv_msg.send_dont_wait_for_message()
    return ""


def _request(mac: str, addr: str) -> None:
    """_request sent REQUEST message with mac and check if Kea response with ACK

    :param mac: MAC address of a client
    :type mac: str
    :param addr: IP v4 address expected to be assigned to the client
    :type addr: str
    """
    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', mac)
    srv_msg.client_does_include_with_value('requested_addr', addr)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content("chaddr", mac)
    srv_msg.response_check_content('yiaddr', addr)


def _solicit(duid, addr=None):
    """_solicit send Solicit message with specified DUID and address. Check response.
    If address is missing test will expect status code 2 in response.

    :param duid: DUID
    :type duid: str
    :param addr: ip v6 address, defaults to None
    :type addr: str, optional
    """
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    if addr:
        srv_msg.response_check_option_content(3, 'sub-option', 5)
        srv_msg.response_check_suboption_content(5, 3, 'addr', addr)
    else:
        srv_msg.response_check_option_content(3, 'sub-option', 13)
        srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)


def _request6(duid, addr):
    """_request6 send Request message with specified DUID and address. Check response.

    :param duid: DUID
    :type duid: str
    :param addr: ip v6 address
    :type addr: str
    """
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', addr)


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_list():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.config_srv_another_subnet_no_interface('10.0.0.0/24', '10.0.0.5-10.0.0.5')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet4-get","arguments":{"id": 234}}',
                                     exp_result=3)  # expect no such subnet i.e. 3


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_get_by_id():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.config_srv_another_subnet_no_interface('10.0.0.0/24', '10.0.0.5-10.0.0.5')
    srv_control.config_srv_another_subnet_no_interface('150.0.0.0/24', '150.0.0.5-150.0.0.5')
    srv_control.config_srv('streettalk-directory-assistance-server', 2, '199.1.1.1,200.1.1.2')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet4-get","arguments":{"id":3}}')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_get_by_subnet():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.config_srv_another_subnet_no_interface('10.0.0.0/24', '10.0.0.5-10.0.0.5')
    srv_control.config_srv('domain-name-servers', 1, '199.199.199.1,100.100.100.1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet4-get","arguments":{"subnet":"10.0.0.0/24"}}')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_add():
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.config_srv_opt('domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    # Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/etc/kea/control_socket send {"command":"subnet4-list","arguments":{}}
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet4-add","arguments":{"subnet4":[{"subnet":"192.168.50.0/24","interface":"$(SERVER_IFACE)","id":234,"pools":[{"pool":"192.168.50.1-192.168.50.1"}]}]}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet4-get","arguments":{"id": 234}}')
    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_add_with_options():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '$(EMPTY)')
    srv_control.config_srv_opt('domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(6, 'value', '100.100.100.1')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    # Using UNIX socket on server in path control_socket send {"command":"subnet4-list","arguments":{}}
    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet4-add","arguments": {"subnet4": [{"subnet": "192.168.51.0/24","interface": "$(SERVER_IFACE)","id": 234,"pools": [{"pool": "192.168.51.1-192.168.51.1"}],"option-data": [{"csv-format": true,"code": 6,"data": "19.19.19.1,10.10.10.1","name": "domain-name-servers","space": "dhcp4"}]}]}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet4-get","arguments":{"id": 234}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet4-del","arguments":{"id":1}}')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, 'value', '19.19.19.1')
    srv_msg.response_check_option_content(6, 'value', '10.10.10.1')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_add_conflict():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.config_srv_opt('domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    # Using UNIX socket on server in path control_socket send {"command":"subnet4-list","arguments":{}}
    srv_msg.send_ctrl_cmd_via_socket({"command": "subnet4-add",
                                      "arguments": {"subnet4": [{"subnet": "192.168.55.0/24",
                                                                 "interface": "$(SERVER_IFACE)",
                                                                 "id": 1,
                                                                 "pools": [{"pool": "192.168.55.1-192.168.55.1"}],
                                                                 "option-data": [{"csv-format": True,
                                                                                  "code": 6,
                                                                                  "data": "19.19.19.1,10.10.10.1",
                                                                                  "name": "domain-name-servers",
                                                                                  "space": "dhcp4"}]}]}},
                                     exp_result=1)
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet4-get","arguments":{"id": 1}}')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_del():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.config_srv_opt('domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet4-del","arguments":{"id":1}}')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_del_non_existing():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.config_srv_opt('domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet4-del","arguments":{"id":2}}',
                                     exp_result=3)  # it does not exists

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_del_global_options():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.config_srv_opt('domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet4-del","arguments":{"id":1}}')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    # That needs subnet with empty pool to work
    # Test Procedure:
    # Client requests option 6.
    # Client sets ciaddr value to $(CIADDR).
    # Client sends INFORM message.
    #
    # Pass Criteria:
    # Server MUST respond with ACK message.
    # Response MUST include option 6.
    # Response option 6 MUST contain value 199.199.199.1.
    # Response option 6 MUST contain value 100.100.100.1.


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_add_and_del():
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.config_srv_opt('domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet4-add","arguments":{"subnet4":[{"subnet":"192.168.50.0/24","interface":"$(SERVER_IFACE)","id":66,"pools":[{"pool":"192.168.50.1-192.168.50.1"}]}]}}')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet4-del","arguments":{"id":66}}')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()


# Test that an user can increase a fully-allocated subnet through the use of
# subnet commands.
@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_hook_v4_subnet_grow_subnet_command(channel):
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'subnet4': [
                {
                    'id': 42,
                    'interface': '$(SERVER_IFACE)',
                    'pools': [
                        {
                            'pool': '192.168.50.1-192.168.50.1'
                        }
                    ],
                    'subnet': '192.168.50.0/24'
                }
            ]
        },
        'command': 'subnet4-add'
    }, channel=channel)
    assert response == {
        'arguments': {
            'subnets': [
                {
                    'id': 42,
                    'subnet': '192.168.50.0/24'
                }
            ]
        },
        'result': 0,
        'text': 'IPv4 subnet added'
    }

    srv_msg.DORA('192.168.50.1')

    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'id': 42
        },
        'command': 'subnet4-del'
    }, channel=channel)
    assert response == {
        'arguments': {
            'subnets': [
                {
                    'id': 42,
                    'subnet': '192.168.50.0/24'
                }
            ]
        },
        'result': 0,
        'text': 'IPv4 subnet 192.168.50.0/24 (id 42) deleted'
    }

    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'subnet4': [
                {
                    'id': 42,
                    'interface': '$(SERVER_IFACE)',
                    'pools': [
                        {
                            'pool': '192.168.50.1-192.168.50.2'
                        }
                    ],
                    'subnet': '192.168.50.0/24'
                }
            ]
        },
        'command': 'subnet4-add'
    }, channel=channel)
    assert response == {
        'arguments': {
            'subnets': [
                {
                    'id': 42,
                    'subnet': '192.168.50.0/24'
                }
            ]
        },
        'result': 0,
        'text': 'IPv4 subnet added'
    }

    srv_msg.DORA('192.168.50.1', exchange='renew-only')

    srv_msg.DORA('192.168.50.2', chaddr='ff:01:02:03:ff:11')

    _check_hash_after_config_reload()


# Test that an user can increase a fully-allocated subnet through the use of
# config backend commands.
@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_hook_v4_subnet_grow_cb_command(channel):
    misc.test_setup()
    if channel == 'http':
        srv_control.agent_control_channel()

    setup_server_for_config_backend_cmds(config_control={'config-fetch-wait-time': 1}, force_reload=False)

    srv_control.start_srv('DHCP', 'started')

    wait_for_message_in_log('DHCPSRV_CFGMGR_CONFIG4_MERGED Configuration backend data has been merged.',
                            count=2, timeout=7)

    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'remote': {
                'type': 'mysql'
            },
            'server-tags': ['all'],
            'subnets': [
                {
                    'id': 42,
                    'interface': '$(SERVER_IFACE)',
                    'pools': [
                        {
                            'pool': '192.168.50.1-192.168.50.1'
                        }
                    ],
                    'shared-network-name': None,
                    'subnet': '192.168.50.0/24'
                }
            ]
        },
        'command': 'remote-subnet4-set'
    }, channel=channel)
    assert response == {
        'arguments': {
            'subnets': [
                {
                    'id': 42,
                    'subnet': '192.168.50.0/24'
                }
            ]
        },
        'result': 0,
        'text': 'IPv4 subnet successfully set.'
    }

    wait_for_message_in_log('DHCPSRV_CFGMGR_CONFIG4_MERGED Configuration backend data has been merged.', 3)

    srv_msg.DORA('192.168.50.1')

    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'remote': {
                'type': 'mysql'
            },
            'subnets': [
                {
                    'id': 42
                }
            ]
        },
        'command': 'remote-subnet4-del-by-id'
    }, channel=channel)
    assert response == {
        'arguments': {
            'count': 1
        },
        'result': 0,
        'text': '1 IPv4 subnet(s) deleted.'
    }

    wait_for_message_in_log('DHCPSRV_CFGMGR_CONFIG4_MERGED Configuration backend data has been merged.', 4)

    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'remote': {
                'type': 'mysql'
            },
            'server-tags': ['all'],
            'subnets': [
                {
                    'id': 42,
                    'interface': '$(SERVER_IFACE)',
                    'pools': [
                        {
                            'pool': '192.168.50.1-192.168.50.2'
                        }
                    ],
                    'shared-network-name': None,
                    'subnet': '192.168.50.0/24'
                }
            ]
        },
        'command': 'remote-subnet4-set'
    }, channel=channel)
    assert response == {
        'arguments': {
            'subnets': [
                {
                    'id': 42,
                    'subnet': '192.168.50.0/24'
                }
            ]
        },
        'result': 0,
        'text': 'IPv4 subnet successfully set.'
    }

    wait_for_message_in_log('DHCPSRV_CFGMGR_CONFIG4_MERGED Configuration backend data has been merged.', 5)

    srv_msg.DORA('192.168.50.1', exchange='renew-only')

    srv_msg.DORA('192.168.50.2', chaddr='ff:01:02:03:ff:11')

    _check_hash_after_config_reload()


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_hook_v4_subnet_delta_add(backend):
    """
    Test subnet4-delta-add command by adding a subnet and then modifying and adding options.
    Forge makes DORA exchanges to verify returned parameters.
    """
    misc.test_setup()
    srv_control.agent_control_channel()
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')

    if backend == 'memfile':
        srv_control.build_and_send_config_files()
        srv_control.start_srv('DHCP', 'started')
    else:
        setup_server_for_config_backend_cmds(backend_type=backend, **world.dhcp_cfg)

    # Add Subnet
    cmd = {
        "arguments":
            {"subnet4": [
                {"subnet": "192.168.50.0/24",
                 "interface": "$(SERVER_IFACE)",
                 "id": 234,
                 "valid-lifetime": 4000,
                 "max-valid-lifetime": 4000,
                 "min-valid-lifetime": 1000,
                 "pools": [
                     {
                         "pool": "192.168.50.1-192.168.50.10"
                     }
                 ]
                 }
            ]
            },
        "command": "subnet4-add"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')
    assert response == {
        "arguments": {
            "subnets": [
                {
                    "id": 234,
                    "subnet": "192.168.50.0/24"
                }
            ]
        },
        "result": 0,
        "text": "IPv4 subnet added"
    }

    # Verify that subnet is added correctly
    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(6, expect_include=False)
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', '4000')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option(6)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(6, expect_include=False)
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', '4000')

    # Add DNS address and modify valid lifetime
    cmd = {
        "arguments":
            {"subnet4": [
                {"subnet": "192.168.50.0/24",
                 "id": 234,
                 "valid-lifetime": 2000,
                 "option-data": [
                     {
                         "csv-format": True,
                         "code": 6,
                         "data": "21.21.21.1,20.20.20.1",
                         "name": "domain-name-servers",
                         "space": "dhcp4"}
                 ]
                 }
            ]
            },
        "command": "subnet4-delta-add"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')
    assert response == {
        "arguments": {
            "subnets": [
                {
                    "id": 234,
                    "subnet": "192.168.50.0/24"
                }
            ]
        },
        "result": 0,
        "text": "IPv4 subnet updated"
    }

    # Verify subnet was modified correctly
    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:05')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.2')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, 'value', '21.21.21.1')
    srv_msg.response_check_option_content(6, 'value', '20.20.20.1')
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', '2000')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.2')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:05')
    srv_msg.client_requests_option(6)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.2')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, 'value', '21.21.21.1')
    srv_msg.response_check_option_content(6, 'value', '20.20.20.1')
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', '2000')

    _check_hash_after_config_reload()


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_hook_v4_subnet_delta_add_negative(backend):
    """
    Test subnet4-delta-add command by adding a subnet and then using incorrect arguments.
    Forge makes DORA exchanges to verify returned parameters.
    """
    misc.test_setup()
    srv_control.agent_control_channel()
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')

    if backend == 'memfile':
        srv_control.build_and_send_config_files()
        srv_control.start_srv('DHCP', 'started')
    else:
        setup_server_for_config_backend_cmds(backend_type=backend, **world.dhcp_cfg)

    # Add Subnet
    cmd = {
        "arguments":
            {"subnet4": [
                {"subnet": "192.168.50.0/24",
                 "interface": "$(SERVER_IFACE)",
                 "id": 234,
                 "valid-lifetime": 4000,
                 "max-valid-lifetime": 4000,
                 "min-valid-lifetime": 1000,
                 "pools": [
                     {
                         "pool": "192.168.50.1-192.168.50.10"
                     }
                 ]
                 }
            ]
            },
        "command": "subnet4-add"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')
    assert response == {
        "arguments": {
            "subnets": [
                {
                    "id": 234,
                    "subnet": "192.168.50.0/24"
                }
            ]
        },
        "result": 0,
        "text": "IPv4 subnet added"
    }

    # Verify that subnet is added correctly
    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(6, expect_include=False)
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', '4000')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option(6)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(6, expect_include=False)
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', '4000')

    # Check invalid command arguments.
    cmd = {
        "arguments":
            {
            },
        "command": "subnet4-delta-add"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=1)
    assert response == {
        "result": 1,
        "text": "invalid number of arguments 0 for the 'subnet4-delta-add' command. Expecting 'subnet4' list"
    }

    cmd = {
        "arguments":
            {"subnet4": [
            ]
            },
        "command": "subnet4-delta-add"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=1)
    assert response == {
        "result": 1,
        "text": "invalid number of subnets specified for the 'subnet4-delta-add' command. Expected one subnet"
    }

    cmd = {
        "arguments":
            {"subnet4": [
                {"subnet": "192.168.50.0/24"
                 }
            ]
            },
        "command": "subnet4-delta-add"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=1)
    assert response == {
        "result": 1,
        "text": "must specify subnet id with 'subnet4-delta-add' command."
    }

    cmd = {
        "arguments":
            {"subnet4": [
                {"id": 234
                 }
            ]
            },
        "command": "subnet4-delta-add"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=1)
    assert response == {
        "result": 1,
        "text": "subnet configuration failed: mandatory 'subnet' parameter is missing for a subnet being configured (<wire>:0:31)"
    }

    cmd = {
        "arguments":
            {"subnet4": [
                {"subnet": "192.168.50.0/24",
                 "id": 234,
                 "valid-lifetime": True,
                 }
            ]
            },
        "command": "subnet4-delta-add"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=1)
    assert response == {
        "result": 1,
        "text": "'valid-lifetime' parameter is not an integer"
    }

    # Verify that subnet is not changed by incorrect commands
    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(6, expect_include=False)
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', '4000')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option(6)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(6, expect_include=False)
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', '4000')

    _check_hash_after_config_reload()


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_hook_v4_subnet_delta_del(backend):
    """
    Test subnet4-delta-del command by adding a subnet and then modifying and deleting options.
    Forge makes DORA exchanges to verify returned parameters.
    """
    misc.test_setup()
    srv_control.agent_control_channel()
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')

    if backend == 'memfile':
        srv_control.build_and_send_config_files()
        srv_control.start_srv('DHCP', 'started')
    else:
        world.dhcp_cfg["valid-lifetime"] = 4000
        setup_server_for_config_backend_cmds(backend_type=backend, **world.dhcp_cfg)

    # Add Subnet
    cmd = {
        "arguments":
            {"subnet4": [
                {"subnet": "192.168.50.0/24",
                 "interface": "$(SERVER_IFACE)",
                 "id": 234,
                 "valid-lifetime": 3000,
                 "max-valid-lifetime": 4000,
                 "min-valid-lifetime": 1000,
                 "pools": [
                     {
                         "pool": "192.168.50.1-192.168.50.10"
                     }
                 ],
                 "option-data": [
                     {
                         "csv-format": True,
                         "code": 6,
                         "data": "21.21.21.1,20.20.20.1",
                         "name": "domain-name-servers",
                         "space": "dhcp4"}
                 ]
                 }
            ]
            },
        "command": "subnet4-add"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')
    assert response == {
        "arguments": {
            "subnets": [
                {
                    "id": 234,
                    "subnet": "192.168.50.0/24"
                }
            ]
        },
        "result": 0,
        "text": "IPv4 subnet added"
    }

    # Verify that subnet is added correctly
    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, 'value', '21.21.21.1')
    srv_msg.response_check_option_content(6, 'value', '20.20.20.1')
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', '3000')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option(6)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, 'value', '21.21.21.1')
    srv_msg.response_check_option_content(6, 'value', '20.20.20.1')
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', '3000')

    # Remove DNS option and valid-lifetime
    cmd = {
        "arguments":
            {"subnet4": [
                {"subnet": "192.168.50.0/24",
                 "id": 234,
                 "valid-lifetime": 2000,
                 "option-data": [
                     {
                         "code": 6
                     }
                 ]
                 }
            ]
            },
        "command": "subnet4-delta-del"}

    response = srv_msg.send_ctrl_cmd(cmd, 'http')
    assert response == {
        "arguments": {
            "subnets": [
                {
                    "id": 234,
                    "subnet": "192.168.50.0/24"
                }
            ]
        },
        "result": 0,
        "text": "IPv4 subnet updated"
    }

    # Verify subnet was modified correctly
    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:05')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.2')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(6, expect_include=False)
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', '4000')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.2')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:05')
    srv_msg.client_requests_option(6)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.2')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(6, expect_include=False)
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', '4000')

    _check_hash_after_config_reload()
@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_hook_v4_subnet_delta_del_negative(backend):
    """
    Test subnet4-delta-del command by adding a subnet and then using incorrect arguments.
    Forge makes DORA exchanges to verify returned parameters.
    """
    misc.test_setup()
    srv_control.agent_control_channel()
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')

    if backend == 'memfile':
        srv_control.build_and_send_config_files()
        srv_control.start_srv('DHCP', 'started')
    else:
        world.dhcp_cfg["valid-lifetime"] = 4000
        setup_server_for_config_backend_cmds(backend_type=backend, **world.dhcp_cfg)

    # Add Subnet
    cmd = {
        "arguments":
            {"subnet4": [
                {"subnet": "192.168.50.0/24",
                 "interface": "$(SERVER_IFACE)",
                 "id": 234,
                 "valid-lifetime": 3000,
                 "max-valid-lifetime": 4000,
                 "min-valid-lifetime": 1000,
                 "pools": [
                     {
                         "pool": "192.168.50.1-192.168.50.10"
                     }
                 ],
                 "option-data": [
                     {
                         "csv-format": True,
                         "code": 6,
                         "data": "21.21.21.1,20.20.20.1",
                         "name": "domain-name-servers",
                         "space": "dhcp4"}
                 ]
                 }
            ]
            },
        "command": "subnet4-add"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')
    assert response == {
        "arguments": {
            "subnets": [
                {
                    "id": 234,
                    "subnet": "192.168.50.0/24"
                }
            ]
        },
        "result": 0,
        "text": "IPv4 subnet added"
    }

    # Verify that subnet is added correctly
    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, 'value', '21.21.21.1')
    srv_msg.response_check_option_content(6, 'value', '20.20.20.1')
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', '3000')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option(6)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, 'value', '21.21.21.1')
    srv_msg.response_check_option_content(6, 'value', '20.20.20.1')
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', '3000')

    # Check invalid command arguments.
    cmd = {
        "arguments":
            {},
        "command": "subnet4-delta-del"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=1)
    assert response == {
        "result": 1,
        "text": "invalid number of arguments 0 for the 'subnet4-delta-del' command. Expecting 'subnet4' list"
    }

    cmd = {
        "arguments":
            {"subnet4": []},
        "command": "subnet4-delta-del"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=1)
    assert response == {
        "result": 1,
        "text": "invalid number of subnets specified for the 'subnet4-delta-del' command. Expected one subnet"
    }

    cmd = {
        "arguments":
            {"subnet4": [
                {"subnet": "192.168.50.0/24"}
            ]},
        "command": "subnet4-delta-del"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=1)
    assert response == {
        "result": 1,
        "text": "must specify subnet id with 'subnet4-delta-del' command."
    }

    cmd = {
        "arguments":
            {"subnet4": [
                {"id": 234}
            ]},
        "command": "subnet4-delta-del"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=1)
    assert response == {
        "result": 1,
        "text": "subnet configuration failed: mandatory 'subnet' parameter is missing for a subnet being configured (<wire>:0:31)"
    }

    cmd = {
        "arguments":
            {"subnet4": [
                {"subnet": "192.168.50.0/24",
                 "id": 234,
                 "valid-lifetime": True}
            ]},
        "command": "subnet4-delta-del"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=1)
    assert response == {
        "result": 1,
        "text": "'valid-lifetime' parameter is not an integer"
    }

    # Verify that subnet is not changed by incorrect commands
    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, 'value', '21.21.21.1')
    srv_msg.response_check_option_content(6, 'value', '20.20.20.1')
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', '3000')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option(6)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, 'value', '21.21.21.1')
    srv_msg.response_check_option_content(6, 'value', '20.20.20.1')
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', '3000')

    _check_hash_after_config_reload()
@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_list():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.config_srv_another_subnet_no_interface('1000::/32', '1000::5-1000::5')
    srv_control.config_srv_another_subnet_no_interface('3000::/100', '3000::5-3000::5')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-list","arguments":{}}')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_get_by_id():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.config_srv_another_subnet_no_interface('1000::/32', '1000::5-1000::5')
    srv_control.config_srv_another_subnet_no_interface('3000::/100', '3000::5-3000::5')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-get","arguments":{"id":2}}')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_get_by_subnet():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.config_srv_another_subnet_no_interface('1000::/32', '1000::5-1000::5')
    srv_control.config_srv_another_subnet_no_interface('3000::/100', '3000::5-3000::5')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-get","arguments":{"subnet":"3000::/100"}}')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_add():
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.config_srv_opt('preference', '123')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-list","arguments":{}}', exp_result=3)
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-get","arguments":{"id": 234}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_add_with_options():
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.config_srv_opt('preference', '123')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)

    misc.test_procedure()
    srv_msg.client_requests_option(7)
    srv_msg.client_requests_option(24)
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 123)
    srv_msg.response_check_include_option(24)
    srv_msg.response_check_option_content(24, 'domains', 'domain1.example.com.,domain2.isc.org.')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-list","arguments":{}}', exp_result=3)
    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}],"option-data":[{"csv-format":true,"code":7,"data":"55","name":"preference","space":"dhcp6"}]}]}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-get","arguments":{"id": 234}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_requests_option(24)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 55)
    srv_msg.response_check_include_option(24)
    srv_msg.response_check_option_content(24, 'domains', 'domain1.example.com.,domain2.isc.org.')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_add_conflict():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.config_srv_opt('preference', '123')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-list","arguments":{}}')
    response = srv_msg.send_ctrl_cmd_via_socket({"command": "subnet6-add",
                                                 "arguments": {"subnet6": [{"id": 1,
                                                                            "interface": "$(SERVER_IFACE)",
                                                                            "subnet": "2002:db8:1::/64",
                                                                            "pools": [{"pool": "2002:db8:1::10-2002:db8:1::20"}]}]}},
                                                exp_result=1)
    assert response['text'] == "ID of the new IPv6 subnet '1' is already in use"
    response = srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-get","arguments":{"id": 1}}')
    assert response['arguments']['subnet6'][0]['subnet'] == '2001:db8:1::/64'

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_del():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-list","arguments":{}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet6-del","arguments":{"id":1}}')
    # Using UNIX socket on server in path control_socket send {"command": "subnet6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-get","arguments":{"id": 1}}', exp_result=3)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_del_non_existing():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-list","arguments":{}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet6-del","arguments":{"id":2}}', exp_result=3)
    # Using UNIX socket on server in path control_socket send {"command": "subnet6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_del_global_options():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.config_srv_opt('preference', '123')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 123)

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-list","arguments":{}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet6-del","arguments":{"id":1}}')
    # Using UNIX socket on server in path control_socket send {"command": "subnet6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-get","arguments":{"id": 1}}', exp_result=3)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)

    misc.test_procedure()
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 123)


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_add_and_del():
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.config_srv_opt('preference', '123')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-list","arguments":{}}', exp_result=3)
    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-get","arguments":{"id": 234}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet6-del","arguments":{"id":234}}')
    # Using UNIX socket on server in path control_socket send {"command": "subnet6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}
    response = srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-get","arguments":{"id": 234}}', exp_result=3)
    assert response['text'] == 'No subnet with id 234 found'

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)


# Test that an user can increase a fully-allocated subnet through the use of
# subnet commands.
@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_hook_v6_subnet_grow_subnet_command(channel):
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "subnet6": [
                {
                    "id": 42,
                    "interface": "$(SERVER_IFACE)",
                    "pools": [
                        {
                            "pool": "2001:db8:1::1-2001:db8:1::1"
                        }
                    ],
                    "subnet": "2001:db8:1::/64"
                }
            ]
        },
        "command": "subnet6-add"
    }, channel=channel)
    assert response == {
        'arguments': {
            'subnets': [
                {
                    'id': 42,
                    'subnet': '2001:db8:1::/64'
                }
            ]
        },
        'result': 0,
        'text': 'IPv6 subnet added'
    }

    srv_msg.SARR('2001:db8:1::1')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "id": 42
        },
        "command": "subnet6-del"
    }, channel=channel)
    assert response == {
        'arguments': {
            'subnets': [
                {
                    'id': 42,
                    'subnet': '2001:db8:1::/64'
                }
            ]
        },
        'result': 0,
        'text': 'IPv6 subnet 2001:db8:1::/64 (id 42) deleted'
    }

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "subnet6": [
                {
                    "id": 42,
                    "interface": "$(SERVER_IFACE)",
                    "pools": [
                        {
                            "pool": "2001:db8:1::1-2001:db8:1::2"
                        }
                    ],
                    "subnet": "2001:db8:1::/64"
                }
            ]
        },
        "command": "subnet6-add"
    }, channel=channel)
    assert response == {
        'arguments': {
            'subnets': [
                {
                    'id': 42,
                    "subnet": "2001:db8:1::/64"
                }
            ]
        },
        'result': 0,
        'text': 'IPv6 subnet added'
    }

    srv_msg.SARR('2001:db8:1::1', exchange='renew-only')

    srv_msg.SARR('2001:db8:1::2', duid='00:03:00:01:f6:f5:f4:f3:f2:11')


# Test that an user can increase a fully-allocated subnet through the use of
# config backend commands.
@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_hook_v6_subnet_grow_cb_command(channel):
    misc.test_setup()
    if channel == 'http':
        srv_control.agent_control_channel()

    setup_server_for_config_backend_cmds(config_control={'config-fetch-wait-time': 1}, force_reload=False)

    srv_control.start_srv('DHCP', 'started')

    wait_for_message_in_log('DHCPSRV_CFGMGR_CONFIG6_MERGED Configuration backend data has been merged.', 2)

    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'remote': {
                'type': 'mysql'
            },
            'server-tags': ['all'],
            'subnets': [
                {
                    'id': 42,
                    'interface': '$(SERVER_IFACE)',
                    'pools': [
                        {
                            'pool': '2001:db8:1::1-2001:db8:1::1'
                        }
                    ],
                    'shared-network-name': None,
                    'subnet': '2001:db8:1::/64'
                }
            ]
        },
        'command': 'remote-subnet6-set'
    }, channel=channel)
    assert response == {
        'arguments': {
            'subnets': [
                {
                    'id': 42,
                    'subnet': '2001:db8:1::/64'
                }
            ]
        },
        'result': 0,
        'text': 'IPv6 subnet successfully set.'
    }

    wait_for_message_in_log('DHCPSRV_CFGMGR_CONFIG6_MERGED Configuration backend data has been merged.', 3)

    srv_msg.SARR('2001:db8:1::1')

    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'remote': {
                'type': 'mysql'
            },
            'subnets': [
                {
                    'id': 42
                }
            ]
        },
        'command': 'remote-subnet6-del-by-id'
    }, channel=channel)
    assert response == {
        'arguments': {
            'count': 1
        },
        'result': 0,
        'text': '1 IPv6 subnet(s) deleted.'
    }

    wait_for_message_in_log('DHCPSRV_CFGMGR_CONFIG6_MERGED Configuration backend data has been merged.', 4)

    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'remote': {
                'type': 'mysql'
            },
            'server-tags': ['all'],
            'subnets': [
                {
                    'id': 42,
                    'interface': '$(SERVER_IFACE)',
                    'pools': [
                        {
                            'pool': '2001:db8:1::1-2001:db8:1::2'
                        }
                    ],
                    'shared-network-name': None,
                    'subnet': '2001:db8:1::/64'
                }
            ]
        },
        'command': 'remote-subnet6-set'
    }, channel=channel)
    assert response == {
        'arguments': {
            'subnets': [
                {
                    'id': 42,
                    'subnet': '2001:db8:1::/64'
                }
            ]
        },
        'result': 0,
        'text': 'IPv6 subnet successfully set.'
    }

    wait_for_message_in_log('DHCPSRV_CFGMGR_CONFIG6_MERGED Configuration backend data has been merged.', 5)

    srv_msg.SARR('2001:db8:1::1', exchange='renew-only')

    srv_msg.SARR('2001:db8:1::2', duid='00:03:00:01:f6:f5:f4:f3:f2:11')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_hook_v6_subnet_delta_add(backend):
    """
    Test subnet6-delta-add command by adding a subnet and then modifying and adding options.
    Forge makes SARR exchanges to verify returned parameters.
    """
    misc.test_setup()
    srv_control.agent_control_channel()
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')

    if backend == 'memfile':
        srv_control.build_and_send_config_files()
        srv_control.start_srv('DHCP', 'started')
    else:
        setup_server_for_config_backend_cmds(backend_type=backend, **world.dhcp_cfg)

    # Add Subnet
    cmd = {
        "arguments":
            {"subnet6": [
                {"subnet": "2001:db8:1::/64",
                 "interface": "$(SERVER_IFACE)",
                 "id": 234,
                 "valid-lifetime": 4000,
                 "max-valid-lifetime": 4000,
                 "min-valid-lifetime": 1000,
                 "pools": [
                     {
                         "pool": "2001:db8:1::1-2001:db8:1::10"
                     }
                 ]
                 }
            ]
            },
        "command": "subnet6-add"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')
    assert response == {
        "arguments": {
            "subnets": [
                {
                    "id": 234,
                    "subnet": "2001:db8:1::/64"
                }
            ]
        },
        "result": 0,
        "text": "IPv6 subnet added"
    }

    # Verify that subnet is added correctly
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.response_check_suboption_content(5, 3, 'validlft', 4000)
    srv_msg.response_check_include_option(23, expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(23, expect_include=False)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.response_check_suboption_content(5, 3, 'validlft', 4000)

    # Add DNS address and modify valid lifetime
    cmd = {
        "arguments":
            {"subnet6": [
                {"subnet": "2001:db8:1::/64",
                 "id": 234,
                 "valid-lifetime": 2000,
                 "option-data": [
                     {
                         "csv-format": True,
                         "code": 23,
                         "data": "2001:4860::1,2001:4860::2",
                         "name": "dns-servers",
                         "space": "dhcp6"}
                 ]
                 }
            ]
            },
        "command": "subnet6-delta-add"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')
    assert response == {
        "arguments": {
            "subnets": [
                {
                    "id": 234,
                    "subnet": "2001:db8:1::/64"
                }
            ]
        },
        "result": 0,
        "text": "IPv6 subnet updated"
    }

    # Verify subnet was modified correctly
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:05')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::2')
    srv_msg.response_check_suboption_content(5, 3, 'validlft', 2000)
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:4860::1,2001:4860::2')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:05')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::2')
    srv_msg.response_check_suboption_content(5, 3, 'validlft', 2000)
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:4860::1,2001:4860::2')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_hook_v6_subnet_delta_add_negative(backend):
    """
    Test subnet6-delta-add command by adding a subnet and then using incorrect arguments.
    Forge makes SARR exchanges to verify returned parameters.
    """
    misc.test_setup()
    srv_control.agent_control_channel()
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')

    if backend == 'memfile':
        srv_control.build_and_send_config_files()
        srv_control.start_srv('DHCP', 'started')
    else:
        setup_server_for_config_backend_cmds(backend_type=backend, **world.dhcp_cfg)

    # Add Subnet
    cmd = {
        "arguments":
            {"subnet6": [
                {"subnet": "2001:db8:1::/64",
                 "interface": "$(SERVER_IFACE)",
                 "id": 234,
                 "valid-lifetime": 4000,
                 "max-valid-lifetime": 4000,
                 "min-valid-lifetime": 1000,
                 "pools": [
                     {
                         "pool": "2001:db8:1::1-2001:db8:1::10"
                     }
                 ]
                 }
            ]
            },
        "command": "subnet6-add"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')
    assert response == {
        "arguments": {
            "subnets": [
                {
                    "id": 234,
                    "subnet": "2001:db8:1::/64"
                }
            ]
        },
        "result": 0,
        "text": "IPv6 subnet added"
    }

    # Verify that subnet is added correctly
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.response_check_suboption_content(5, 3, 'validlft', 4000)
    srv_msg.response_check_include_option(23, expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(23, expect_include=False)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.response_check_suboption_content(5, 3, 'validlft', 4000)

    # Check invalid command arguments.
    cmd = {
        "arguments":
            {
            },
        "command": "subnet6-delta-add"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=1)
    assert response == {
        "result": 1,
        "text": "invalid number of arguments 0 for the 'subnet6-delta-add' command. Expecting 'subnet6' list"
    }

    cmd = {
        "arguments":
            {"subnet6": [
            ]
            },
        "command": "subnet6-delta-add"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=1)
    assert response == {
        "result": 1,
        "text": "invalid number of subnets specified for the 'subnet6-delta-add' command. Expected one subnet"
    }

    cmd = {
        "arguments":
            {"subnet6": [
                {"subnet": "2001:db8:1::/64"}
            ]
            },
        "command": "subnet6-delta-add"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=1)
    assert response == {
        "result": 1,
        "text": "must specify subnet id with 'subnet6-delta-add' command."
    }

    cmd = {
        "arguments":
            {"subnet6": [
                {"id": 234}
            ]
            },
        "command": "subnet6-delta-add"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=1)
    assert response == {
        "result": 1,
        "text": "subnet configuration failed: mandatory 'subnet' parameter is missing for a subnet being configured (<wire>:0:31)"
    }

    cmd = {
        "arguments":
            {"subnet6": [
                {"subnet": "2001:db8:1::/64",
                 "id": 234,
                 "valid-lifetime": True}
            ]
            },
        "command": "subnet6-delta-add"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=1)
    assert response == {
        "result": 1,
        "text": "'valid-lifetime' parameter is not an integer"
    }

    # Verify that subnet is not changed by incorrect commands
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.response_check_suboption_content(5, 3, 'validlft', 4000)
    srv_msg.response_check_include_option(23, expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(23, expect_include=False)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.response_check_suboption_content(5, 3, 'validlft', 4000)


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_hook_v6_subnet_delta_del(backend):
    """
    Test subnet6-delta-del command by adding a subnet and then modifying and deleting options.
    Forge makes SARR exchanges to verify returned parameters.
    """
    misc.test_setup()
    srv_control.agent_control_channel()
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')

    if backend == 'memfile':
        srv_control.build_and_send_config_files()
        srv_control.start_srv('DHCP', 'started')
    else:
        world.dhcp_cfg["valid-lifetime"] = 4000
        setup_server_for_config_backend_cmds(backend_type=backend, **world.dhcp_cfg)

    # Add Subnet
    cmd = {
        "arguments":
            {"subnet6": [
                {"subnet": "2001:db8:1::/64",
                 "interface": "$(SERVER_IFACE)",
                 "id": 234,
                 "valid-lifetime": 2000,
                 "max-valid-lifetime": 4000,
                 "min-valid-lifetime": 1000,
                 "pools": [
                     {
                         "pool": "2001:db8:1::1-2001:db8:1::10"
                     }
                 ],
                 "option-data": [
                     {
                         "csv-format": True,
                         "code": 23,
                         "data": "2001:4860::1,2001:4860::2",
                         "name": "dns-servers",
                         "space": "dhcp6"}
                 ]
                 }
            ]
            },
        "command": "subnet6-add"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')
    assert response == {
        "arguments": {
            "subnets": [
                {
                    "id": 234,
                    "subnet": "2001:db8:1::/64"
                }
            ]
        },
        "result": 0,
        "text": "IPv6 subnet added"
    }

    # Verify that subnet is added correctly
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.response_check_suboption_content(5, 3, 'validlft', 2000)
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:4860::1,2001:4860::2')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.response_check_suboption_content(5, 3, 'validlft', 2000)
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:4860::1,2001:4860::2')

    # Add DNS address and modify valid lifetime
    cmd = {
        "arguments":
            {"subnet6": [
                {"subnet": "2001:db8:1::/64",
                 "id": 234,
                 "valid-lifetime": 2000,
                 "option-data": [
                     {
                         "code": 23
                     }
                 ]
                 }
            ]
            },
        "command": "subnet6-delta-del"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')
    assert response == {
        "arguments": {
            "subnets": [
                {
                    "id": 234,
                    "subnet": "2001:db8:1::/64"
                }
            ]
        },
        "result": 0,
        "text": "IPv6 subnet updated"
    }

    # Verify subnet was modified correctly
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:05')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::2')
    srv_msg.response_check_suboption_content(5, 3, 'validlft', 4000)
    srv_msg.response_check_include_option(23, expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:05')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::2')
    srv_msg.response_check_suboption_content(5, 3, 'validlft', 4000)
    srv_msg.response_check_include_option(23, expect_include=False)


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_hook_v6_subnet_delta_del_negative(backend):
    """
    Test subnet6-delta-del command by adding a subnet and then using incorrect arguments.
    Forge makes SARR exchanges to verify returned parameters.
    """
    misc.test_setup()
    srv_control.agent_control_channel()
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')

    if backend == 'memfile':
        srv_control.build_and_send_config_files()
        srv_control.start_srv('DHCP', 'started')
    else:
        world.dhcp_cfg["valid-lifetime"] = 4000
        setup_server_for_config_backend_cmds(backend_type=backend, **world.dhcp_cfg)

    # Add Subnet
    cmd = {
        "arguments":
            {"subnet6": [
                {"subnet": "2001:db8:1::/64",
                 "interface": "$(SERVER_IFACE)",
                 "id": 234,
                 "valid-lifetime": 2000,
                 "max-valid-lifetime": 4000,
                 "min-valid-lifetime": 1000,
                 "pools": [
                     {
                         "pool": "2001:db8:1::1-2001:db8:1::10"
                     }
                 ],
                 "option-data": [
                     {
                         "csv-format": True,
                         "code": 23,
                         "data": "2001:4860::1,2001:4860::2",
                         "name": "dns-servers",
                         "space": "dhcp6"}
                 ]
                 }
            ]
            },
        "command": "subnet6-add"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')
    assert response == {
        "arguments": {
            "subnets": [
                {
                    "id": 234,
                    "subnet": "2001:db8:1::/64"
                }
            ]
        },
        "result": 0,
        "text": "IPv6 subnet added"
    }

    # Verify that subnet is added correctly
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.response_check_suboption_content(5, 3, 'validlft', 2000)
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:4860::1,2001:4860::2')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.response_check_suboption_content(5, 3, 'validlft', 2000)
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:4860::1,2001:4860::2')

    # Check invalid command arguments.
    cmd = {
        "arguments":
            {},
        "command": "subnet6-delta-del"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=1)
    assert response == {
        "result": 1,
        "text": "invalid number of arguments 0 for the 'subnet6-delta-del' command. Expecting 'subnet6' list"
    }

    cmd = {
        "arguments":
            {"subnet6": []},
        "command": "subnet6-delta-del"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=1)
    assert response == {
        "result": 1,
        "text": "invalid number of subnets specified for the 'subnet6-delta-del' command. Expected one subnet"
    }

    cmd = {
        "arguments":
            {"subnet6": [
                {"subnet": "2001:db8:1::/64"}
            ]},
        "command": "subnet6-delta-del"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=1)
    assert response == {
        "result": 1,
        "text": "must specify subnet id with 'subnet6-delta-del' command."
    }

    cmd = {
        "arguments":
            {"subnet6": [
                {"id": 234}
            ]},
        "command": "subnet6-delta-del"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=1)
    assert response == {
        "result": 1,
        "text": "subnet configuration failed: mandatory 'subnet' parameter is missing for a subnet being configured (<wire>:0:31)"
    }

    cmd = {
        "arguments":
            {"subnet6": [
                {"subnet": "2001:db8:1::/64",
                 "id": 234,
                 "valid-lifetime": True}
            ]},
        "command": "subnet6-delta-del"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=1)
    assert response == {
        "result": 1,
        "text": "'valid-lifetime' parameter is not an integer"
    }

    # Verify that subnet is not changed by incorrect commands
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.response_check_suboption_content(5, 3, 'validlft', 2000)
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:4860::1,2001:4860::2')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.response_check_suboption_content(5, 3, 'validlft', 2000)
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:4860::1,2001:4860::2')


@pytest.mark.v4
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_get_backported():
    """test_hook_v4_subnet_get simple test for subnet4-get command, and list-commands
    Test backported from 2.7.7
    """
    misc.test_setup()
    srv_control.config_srv_subnet("192.168.50.0/24", "192.168.50.5-192.168.50.5")
    srv_control.config_srv_another_subnet_no_interface(
        "10.0.0.0/24", "10.0.0.5-10.0.0.5"
    )
    srv_control.config_srv(
        "streettalk-directory-assistance-server", 1, "199.1.1.1,200.1.1.2"
    )
    srv_control.open_control_channel()
    srv_control.add_hooks("libdhcp_subnet_cmds.so")
    srv_control.build_and_send_config_files()

    srv_control.start_srv("DHCP", "started")

    # those commands should fail - code 1
    _send_command("subnet4-get", {}, exp_result=1)
    _send_command("subnet4-get", {"something": []}, exp_result=1)
    # those should return nothing - code 3
    _send_command("subnet4-get", {"id": 234}, exp_result=3)
    _send_command("subnet4-get", {"subnet": "25.0.0.0/24"}, exp_result=3)

    # let's check if all commands are registered
    result = _send_command("list-commands")
    for cmd in [
        "subnet4-add",
        "subnet4-del",
        "subnet4-delta-add",
        "subnet4-delta-del",
        "subnet4-get",
        "subnet4-list",
        "subnet4-update",
        "subnet6-add",
        "subnet6-del",
        "subnet6-delta-add",
        "subnet6-delta-del",
        "subnet6-get",
        "subnet6-list",
        "subnet6-update",
    ]:
        assert cmd in result, f"Command {cmd} is not in the list of commands"

    # let's check subnet4-get, get same subnet via subnet and id
    resp1 = _send_command("subnet4-get", {"id": 1})
    resp2 = _send_command("subnet4-get", {"subnet": "192.168.50.0/24"})
    for resp in [resp1, resp2]:
        assert len(resp["subnet4"]) == 1, "There should be one subnet"
        assert resp["subnet4"][0]["subnet"] == "192.168.50.0/24", "invalid subnet returned"
        assert resp["subnet4"][0]["id"] == 1, "invalid id returned"
        assert len(resp["subnet4"][0]["option-data"]) == 0, "no options should be returned"

    resp1 = _send_command("subnet4-get", {"id": 2})
    resp2 = _send_command("subnet4-get", {"subnet": "10.0.0.0/24"})
    for resp in [resp1, resp2]:
        assert len(resp["subnet4"]) == 1, "There should be one subnet"
        assert resp["subnet4"][0]["subnet"] == "10.0.0.0/24", "invalid subnet returned"
        assert resp["subnet4"][0]["id"] == 2, "invalid id returned"
        assert len(resp["subnet4"][0]["option-data"]) == 1, "one option should be returned"
        assert resp["subnet4"][0]["option-data"][0]["code"] == 76, "invalid option code returned"


@pytest.mark.v4
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_add_backported():
    """test_hook_v4_subnet_cmds_add test for subnet4-add command, traffic, subnet4-get and config-get
    commands are used to check if subnet was added correctly. Kea is restarted during the test.
    Test backported from 2.7.7
    """
    misc.test_setup()
    srv_control.config_srv_subnet("$(EMPTY)", "$(EMPTY)")
    srv_control.config_srv_opt("domain-name-servers", "199.199.199.1,100.100.100.1")
    srv_control.open_control_channel()
    srv_control.add_hooks("libdhcp_subnet_cmds.so")
    srv_control.build_and_send_config_files()

    srv_control.start_srv("DHCP", "started")

    _discover("ff:01:02:03:ff:01")  # no response expected

    subnet = [
        {
            "subnet": "192.168.50.0/24",
            "interface": world.f_cfg.server_iface,
            "id": 234,
            "pools": [{"pool": "192.168.50.1-192.168.50.10"}],
        }
    ]
    _send_command("subnet4-add", {"subnet4": subnet})

    # let's retrive new subnet in 3 different ways, and check returend values
    resp1 = _send_command("subnet4-get", {"id": 234})
    resp2 = _send_command("subnet4-get", {"subnet": "192.168.50.0/24"})
    resp3 = _config_get()
    hash_1 = resp3["hash"]
    resp3 = resp3["Dhcp4"]
    for resp in [resp1, resp2, resp3]:
        assert len(resp["subnet4"]) == 1, "There should be one subnet"
        assert resp["subnet4"][0]["subnet"] == "192.168.50.0/24", "invalid subnet returned"
        assert resp["subnet4"][0]["id"] == 234, "invalid id returned"
        assert resp["subnet4"][0]["pools"][0]["pool"] == "192.168.50.1-192.168.50.10", "invalid pool returned"
        assert len(resp["subnet4"][0]["option-data"]) == 0, "zero options should be returned"

    _discover("ff:01:02:03:ff:01", "192.168.50.1")
    _request("ff:01:02:03:ff:01", "192.168.50.1")

    # save config and reload
    _save_and_reload()
    srv_msg.forge_sleep(2)

    # check if subnet is still configured
    _discover("ff:01:02:03:ff:02", "192.168.50.2")
    _request("ff:01:02:03:ff:02", "192.168.50.2")

    resp1 = _send_command("subnet4-get", {"id": 234})
    resp2 = _send_command("subnet4-get", {"subnet": "192.168.50.0/24"})
    resp3 = _config_get()
    hash_2 = resp3["hash"]
    resp3 = resp3["Dhcp4"]
    for resp in [resp1, resp2, resp3]:
        assert len(resp["subnet4"]) == 1, "There should be one subnet"
        assert resp["subnet4"][0]["subnet"] == "192.168.50.0/24", "invalid subnet returned"
        assert resp["subnet4"][0]["id"] == 234, "invalid id returned"
        assert resp["subnet4"][0]["pools"][0]["pool"] == "192.168.50.1-192.168.50.10", "invalid pool returned"
        assert len(resp["subnet4"][0]["option-data"]) == 0, "no option should be returned"

    # and check if config changed at all
    assert hash_1 == hash_2, "Config hash should be the same"


@pytest.mark.v4
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_del_backported():
    """test_hook_v4_subnet_cmds_del test for subnet4-del command for subnets configured globally,
    traffic, subnet4-get and config-get commands are used to check if subnet was added correctly.
    Kea is restarted during the test.
    Test backported from 2.7.7
    """
    misc.test_setup()
    srv_control.config_srv_subnet("192.168.51.0/24", "192.168.51.1-192.168.51.1")
    srv_control.config_srv_opt("domain-name-servers", "199.199.199.1,100.100.100.1")
    srv_control.open_control_channel()
    srv_control.add_hooks("libdhcp_subnet_cmds.so")
    srv_control.build_and_send_config_files()

    srv_control.start_srv("DHCP", "started")

    _discover("ff:01:02:03:ff:02", "192.168.51.1")

    # let's make sure subnet exists
    _send_command("subnet4-get", {"id": 1})
    _send_command("subnet4-get", {"subnet": "192.168.51.0/24"})

    # check some invalid subnet4-del command
    _send_command("subnet4-del", {}, exp_result=1)
    _send_command("subnet4-del", {"something": []}, exp_result=1)
    _send_command("subnet4-del", {"id": 234}, exp_result=3)

    # subnet4-del do not accept subnet parameter, only id
    _send_command("subnet4-del", {"subnet": "192.168.51.0/24"}, exp_result=1)

    # let's remove configured subnet
    resp1 = _send_command("subnet4-del", {"id": 1})
    assert resp1["subnets"][0]["id"] == 1, "incorrect subnet id returned"
    assert (
        resp1["subnets"][0]["subnet"] == "192.168.51.0/24"
    ), "incorrect subnet returned"

    # let's make sure subnet were indeed removed
    _send_command("subnet4-get", {"id": 1}, exp_result=3)
    _send_command("subnet4-get", {"subnet": "192.168.51.0/24"}, exp_result=3)
    cfg = _config_get()
    hash_1 = cfg["hash"]
    assert len(cfg["Dhcp4"]["subnet4"]) == 0, "There should be no subnets"

    _discover("ff:01:02:03:ff:03")  # expect no response

    # save configuration to the file and reload
    _save_and_reload()
    srv_msg.forge_sleep(2)

    # let's make sure subnet stay removed
    _send_command("subnet4-get", {"id": 1}, exp_result=3)
    _send_command("subnet4-get", {"subnet": "192.168.51.0/24"}, exp_result=3)
    cfg = _config_get()
    hash_2 = cfg["hash"]
    assert len(cfg["Dhcp4"]["subnet4"]) == 0, "There should be no subnets"

    assert hash_1 == hash_2, "Config hash should be the same"

    _discover("ff:01:02:03:ff:04")  # expect no response


@pytest.mark.v4
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_del_shared_network_backported():
    """test_hook_v4_subnet_cmds_del_shared_network test for subnet4-del command for subnets
    configured in shared-network, traffic, subnet4-get and config-get
    commands are used to check if subnet was added correctly.
    Kea is restarted during the test.
    Test backported from 2.7.7
    """
    misc.test_setup()
    srv_control.config_srv_subnet("192.168.51.0/24", "192.168.51.1-192.168.51.1")
    srv_control.config_srv_opt("domain-name-servers", "199.199.199.1,100.100.100.1")
    srv_control.shared_subnet("192.168.51.0/24", 0)
    srv_control.set_conf_parameter_shared_subnet("name", '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet("interface", world.f_cfg.server_iface, 0)
    srv_control.open_control_channel()
    srv_control.add_hooks("libdhcp_subnet_cmds.so")
    srv_control.build_and_send_config_files()

    srv_control.start_srv("DHCP", "started")

    _discover("ff:01:02:03:ff:03", "192.168.51.1")

    # let's make sure subnet exists
    _send_command("subnet4-get", {"id": 1})
    _send_command("subnet4-get", {"subnet": "192.168.51.0/24"})

    # check some invalid subnet4-del command
    _send_command("subnet4-del", {}, exp_result=1)
    _send_command("subnet4-del", {"something": []}, exp_result=1)

    # delete non existing subnet
    _send_command("subnet4-del", {"id": 234}, exp_result=3)

    # subnet4-del do not accept subnet parameter, only id
    _send_command("subnet4-del", {"subnet": "192.168.51.0/24"}, exp_result=1)

    # let's remove configured subnet
    resp1 = _send_command("subnet4-del", {"id": 1})
    assert resp1["subnets"][0]["id"] == 1, "incorrect subnet id returned"
    assert (
        resp1["subnets"][0]["subnet"] == "192.168.51.0/24"
    ), "incorrect subnet returned"

    # let's make sure subnet were indeed removed
    _send_command("subnet4-get", {"id": 1}, exp_result=3)
    _send_command("subnet4-get", {"subnet": "192.168.51.0/24"}, exp_result=3)
    cfg = _config_get()
    hash_1 = cfg["hash"]
    assert (
        len(cfg["Dhcp4"]["shared-networks"][0]["subnet4"]) == 0
    ), "There should be no subnets in the shared network"

    _discover("ff:01:02:03:ff:03")  # expect no response

    # save configuration to the file and reload
    _save_and_reload()
    srv_msg.forge_sleep(2)

    # let's make sure subnet stay removed
    _send_command("subnet4-get", {"id": 1}, exp_result=3)
    _send_command("subnet4-get", {"subnet": "192.168.51.0/24"}, exp_result=3)
    cfg = _config_get()
    hash_2 = cfg["hash"]
    assert (
        len(cfg["Dhcp4"]["shared-networks"][0]["subnet4"]) == 0
    ), "There should be no subnets"

    assert hash_1 == hash_2, "Config hash should be the same"

    _discover("ff:01:02:03:ff:03")  # expect no response


@pytest.mark.v4
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_add_with_options_backported():
    """test_hook_v4_subnet_cmds_add_with_options test for subnet4-add command for subnets
    with additional option inside. Traffic, subnet4-get and config-get
    commands are used to check if subnet was added correctly.
    Kea is restarted during the test.
    Test backported from 2.7.7
    """
    misc.test_setup()
    srv_control.config_srv_subnet("192.168.50.0/24", "$(EMPTY)")
    srv_control.config_srv_opt("domain-name-servers", "199.199.199.1,100.100.100.1")
    srv_control.open_control_channel()
    srv_control.add_hooks("libdhcp_subnet_cmds.so")
    srv_control.build_and_send_config_files()

    srv_control.start_srv("DHCP", "started")

    misc.test_procedure()
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value("Client", "ciaddr", "$(CIADDR)")
    srv_msg.client_send_msg("INFORM")

    misc.pass_criteria()
    srv_msg.send_wait_for_message("MUST", "ACK")
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, "value", "199.199.199.1")
    srv_msg.response_check_option_content(6, "value", "100.100.100.1")

    _discover("ff:01:02:03:ff:03")  # expect no response

    subnet = [
        {
            "subnet": "192.168.51.0/24",
            "interface": world.f_cfg.server_iface,
            "id": 10234,
            "pools": [{"pool": "192.168.51.1-192.168.51.2"}],
            "option-data": [
                {
                    "csv-format": True,
                    "code": 6,
                    "data": "19.19.19.1,10.10.10.1",
                    "name": "domain-name-servers",
                    "always-send": True,
                    "space": "dhcp4",
                }
            ],
        }
    ]
    _send_command("subnet4-add", {"subnet4": subnet})

    resp = _send_command("subnet4-get", {"id": 1})
    assert resp["subnet4"][0]["subnet"] == "192.168.50.0/24", "invalid subnet returned"
    resp = _send_command("subnet4-get", {"id": 10234})
    assert resp["subnet4"][0]["subnet"] == "192.168.51.0/24", "invalid subnet returned"
    assert resp["subnet4"][0]["id"] == 10234, "invalid id returned"
    assert len(resp["subnet4"][0]["option-data"]) == 1, "one option should be returned"
    assert resp["subnet4"][0]["option-data"][0]["code"] == 6, "invalid option id returned"
    assert resp["subnet4"][0]["option-data"][0]["data"] == "19.19.19.1,10.10.10.1", "invalid option value returned"

    _send_command("subnet4-del", {"id": 1})

    _discover("ff:01:02:03:ff:05", "192.168.51.1")
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, "value", "19.19.19.1")
    srv_msg.response_check_option_content(6, "value", "10.10.10.1")

    _request("ff:01:02:03:ff:05", "192.168.51.1")
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, "value", "19.19.19.1")
    srv_msg.response_check_option_content(6, "value", "10.10.10.1")

    _check_hash_after_config_reload()

    _discover("ff:01:02:03:ff:08", "192.168.51.2")
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, "value", "19.19.19.1")
    srv_msg.response_check_option_content(6, "value", "10.10.10.1")

    _request("ff:01:02:03:ff:08", "192.168.51.2")
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, "value", "19.19.19.1")
    srv_msg.response_check_option_content(6, "value", "10.10.10.1")


@pytest.mark.v4
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_add_conflict_backported():
    """test_hook_v4_subnet_cmds_add_conflict test for subnet4-add command in which we try to add
    subnet that is already configured. Traffic, subnet4-get and config-get commands are used to check
    if subnet was added correctly. Kea is restarted during the test.
    Test backported from 2.7.7
    """
    misc.test_setup()
    srv_control.config_srv_subnet("192.168.51.0/24", "192.168.51.1-192.168.51.3")
    srv_control.config_srv_opt("domain-name-servers", "199.199.199.1,100.100.100.1")
    srv_control.open_control_channel()
    srv_control.add_hooks("libdhcp_subnet_cmds.so")
    srv_control.build_and_send_config_files()

    srv_control.start_srv("DHCP", "started")

    _discover("ff:01:02:03:ff:05", "192.168.51.1")
    _request("ff:01:02:03:ff:05", "192.168.51.1")

    subnet = [
        {
            "subnet": "192.168.55.0/24",
            "interface": world.f_cfg.server_iface,
            "id": 1,
            "pools": [{"pool": "192.168.55.1-192.168.55.1"}],
            "option-data": [
                {
                    "csv-format": True,
                    "code": 6,
                    "data": "19.19.19.1,10.10.10.1",
                    "name": "domain-name-servers",
                    "space": "dhcp4",
                }
            ],
        }
    ]
    _send_command("subnet4-add", {"subnet4": [{"subnet": subnet}]}, exp_result=1)
    resp = _send_command("subnet4-get", {"id": 1})
    assert resp["subnet4"][0]["subnet"] == "192.168.51.0/24", "invalid subnet returned"

    _discover("ff:01:02:03:ff:06", "192.168.51.2")
    _request("ff:01:02:03:ff:06", "192.168.51.2")

    _check_hash_after_config_reload()

    _discover("ff:01:02:03:ff:07", "192.168.51.3")
    _request("ff:01:02:03:ff:07", "192.168.51.3")


@pytest.mark.v4
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_add_and_del_backported():
    """test_hook_v4_subnet_cmds_add_and_del test for subnet4-del commands that is used to removed
    subnets that were added using subnet4-add command. Traffic, subnet4-get and config-get
    commands are used to check if subnet was added correctly. Kea is restarted during the test.
    Test backported from 2.7.7
    """
    misc.test_setup()
    srv_control.config_srv_subnet("$(EMPTY)", "$(EMPTY)")
    srv_control.open_control_channel()
    srv_control.add_hooks("libdhcp_subnet_cmds.so")
    srv_control.build_and_send_config_files()

    srv_control.start_srv("DHCP", "started")

    _discover("ff:01:02:03:ff:07")  # expect no response

    subnet = [
        {
            "subnet": "192.168.55.0/24",
            "interface": world.f_cfg.server_iface,
            "id": 66,
            "pools": [{"pool": "192.168.55.1-192.168.55.1"}]
        }
    ]
    _send_command("subnet4-add", {"subnet4": subnet})
    resp = _send_command("subnet4-get", {"id": 66})
    assert resp["subnet4"][0]["subnet"] == "192.168.55.0/24", "invalid subnet returned"

    addr = _discover("ff:01:02:03:ff:09", "192.168.55.1")
    _request("ff:01:02:03:ff:09", addr)

    _send_command("subnet4-del", {"id": 66})

    _discover("ff:01:02:03:ff:10")  # expect no response

    _check_hash_after_config_reload()

    _send_command("subnet4-get", {"id": 66}, exp_result=3)
    _discover("ff:01:02:03:ff:10")  # expect no response


@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_del_backported():
    """test_hook_v6_subnet_cmds_del Check if it is possible to remove subnet using subnet6-del command.
    Traffic, subnet6-get commands and config-get commands are used to determine if subnet was removed correctly.
    Kea is restarted during the test to make sure that subnet is not present after restart.
    Test backported from 2.7.7
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::10')
    srv_control.open_control_channel()
    srv_control.add_hooks("libdhcp_subnet_cmds.so")
    srv_control.build_and_send_config_files()

    srv_control.start_srv("DHCP", "started")

    _solicit("00:03:00:01:66:55:44:33:22:11", "2001:db8:1::1")
    _request6("00:03:00:01:66:55:44:33:22:11", "2001:db8:1::1")

    # let's make sure subnet exists
    _send_command("subnet6-get", {"id": 1})
    _send_command("subnet6-get", {"subnet": "2001:db8:1::/64"})

    # check some invalid subnet6-del command
    _send_command("subnet6-del", {}, exp_result=1)
    _send_command("subnet6-del", {"something": []}, exp_result=1)
    _send_command("subnet6-del", {"id": 234}, exp_result=3)

    # subnet6-del do not accept subnet parameter, only id
    _send_command("subnet6-del", {"subnet": "2001:db8:1::/64"}, exp_result=1)

    # let's remove configured subnet
    resp1 = _send_command("subnet6-del", {"id": 1})
    assert resp1["subnets"][0]["id"] == 1, "incorrect subnet id returned"
    assert (
        resp1["subnets"][0]["subnet"] == "2001:db8:1::/64"
    ), "incorrect subnet returned"

    # let's make sure subnet were indeed removed
    _send_command("subnet6-get", {"id": 1}, exp_result=3)
    _send_command("subnet6-get", {"subnet": "2001:db8:1::/64"}, exp_result=3)
    cfg = _config_get()
    hash_1 = cfg["hash"]
    assert len(cfg["Dhcp6"]["subnet6"]) == 0, "There should be no subnets"

    _solicit("00:03:00:01:66:55:44:33:22:22")  # expect no response

    # save configuration to the file and reload
    _save_and_reload()
    srv_msg.forge_sleep(2)

    # let's make sure subnet stay removed
    _send_command("subnet6-get", {"id": 1}, exp_result=3)
    _send_command("subnet6-get", {"subnet": "2001:db8:1::/64"}, exp_result=3)
    cfg = _config_get()
    hash_2 = cfg["hash"]
    assert len(cfg["Dhcp6"]["subnet6"]) == 0, "There should be no subnets"

    assert hash_1 == hash_2, "Config hash should be the same"

    _solicit("00:03:00:01:66:55:44:33:22:22")  # expect no response


@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_del_shared_network_backported():
    """
    Test backported from 2.7.7
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::10')
    srv_control.shared_subnet('2001:db8:1::/64', 0)
    srv_control.set_conf_parameter_shared_subnet("name", '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet("interface", world.f_cfg.server_iface, 0)
    srv_control.open_control_channel()
    srv_control.add_hooks("libdhcp_subnet_cmds.so")
    srv_control.build_and_send_config_files()

    srv_control.start_srv("DHCP", "started")

    _solicit("00:03:00:01:66:55:44:33:22:11", "2001:db8:1::1")

    # let's make sure subnet exists
    _send_command("subnet6-get", {"id": 1})
    _send_command("subnet6-get", {"subnet": "2001:db8:1::/64"})

    # check some invalid subnet6-del command
    _send_command("subnet6-del", {}, exp_result=1)
    _send_command("subnet6-del", {"something": []}, exp_result=1)

    # delete non existing subnet
    _send_command("subnet6-del", {"id": 234}, exp_result=3)

    # subnet6-del do not accept subnet parameter, only id
    _send_command("subnet6-del", {"subnet": "2001:db8:1::/64"}, exp_result=1)

    # let's remove configured subnet
    resp1 = _send_command("subnet6-del", {"id": 1})
    assert resp1["subnets"][0]["id"] == 1, "incorrect subnet id returned"
    assert (
        resp1["subnets"][0]["subnet"] == "2001:db8:1::/64"
    ), "incorrect subnet returned"

    # let's make sure subnet were indeed removed
    _send_command("subnet6-get", {"id": 1}, exp_result=3)
    _send_command("subnet6-get", {"subnet": "2001:db8:1::/64"}, exp_result=3)
    cfg = _config_get()
    hash_1 = cfg["hash"]
    assert (
        len(cfg["Dhcp6"]["shared-networks"][0]["subnet6"]) == 0
    ), "There should be no subnets in the shared network"

    _solicit("00:03:00:01:66:55:44:33:22:22")  # expect no response

    # save configuration to the file and reload
    _save_and_reload()
    srv_msg.forge_sleep(2)

    # let's make sure subnet stay removed
    _send_command("subnet6-get", {"id": 1}, exp_result=3)
    _send_command("subnet6-get", {"subnet": "2001:db8:1::/64"}, exp_result=3)
    cfg = _config_get()
    hash_2 = cfg["hash"]
    assert (
        len(cfg["Dhcp6"]["shared-networks"][0]["subnet6"]) == 0
    ), "There should be no subnets"

    assert hash_1 == hash_2, "Config hash should be the same"

    _solicit("00:03:00:01:66:55:44:33:22:33")  # expect no response
