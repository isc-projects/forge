# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Marcin Godzina

"""Kea Run Script Hook tests"""

# pylint: disable=line-too-long

import pytest

from src import misc
from src import srv_control
from src import srv_msg

from src.forge_cfg import world
from src.softwaresupport.multi_server_functions import fabric_sudo_command


def _send_client_request4():
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(61, 'value', '00010203040506')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(61, 'value', '00010203040506')


def _send_client_renew4():
    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(1)
    srv_msg.client_does_include_with_value('hostname', 'aa.four.example.com.')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')


@pytest.mark.v4
@pytest.mark.run_script
def test_run_script_leases4_committed():
    """
    Test checks if Run Script hook executes script and uses correct variables.
    First the script is prepared and send to Kea machine.
    Kea is started and script is triggered by desired action.
    Output file is checked for correct parameters and artifacts are copied to test results.
    """
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.data_join('script.sh'))
    srv_msg.remove_file_from_server(world.f_cfg.data_join('output.txt'))

    # Returned parameter names with expected value.
    # Values marked as "" will not be checked
    parameters = {
        "QUERY4_TYPE": "DHCPREQUEST",
        "QUERY4_TXID": "",
        "QUERY4_LOCAL_ADDR": "255.255.255.255",
        "QUERY4_LOCAL_PORT": "67",
        "QUERY4_REMOTE_ADDR": "0.0.0.0",
        "QUERY4_REMOTE_PORT": "68",
        "QUERY4_IFACE_INDEX": "",
        "QUERY4_IFACE_NAME": f"{world.f_cfg.server_iface}",
        "QUERY4_HOPS": "0",
        "QUERY4_SECS": "0",
        "QUERY4_FLAGS": "0",
        "QUERY4_CIADDR": "0.0.0.0",
        "QUERY4_SIADDR": "0.0.0.0",
        "QUERY4_YIADDR": "0.0.0.0",
        "QUERY4_GIADDR": "0.0.0.0",
        "QUERY4_RELAYED": "false",
        "QUERY4_HWADDR": "",
        "QUERY4_HWADDR_TYPE": "1",
        "QUERY4_LOCAL_HWADDR": "ff:ff:ff:ff:ff:ff",
        "QUERY4_LOCAL_HWADDR_TYPE": "1",
        "QUERY4_REMOTE_HWADDR": "",
        "QUERY4_REMOTE_HWADDR_TYPE": "1",
        "QUERY4_OPTION_82": "",
        "QUERY4_OPTION_82_SUB_OPTION_1": "",
        "QUERY4_OPTION_82_SUB_OPTION_2": "",
        "LEASES4_SIZE": "1",
        "DELETED_LEASES4_SIZE": "0"
    }

    # Prepare script to send to Kea
    script_content = f'#!/bin/bash \n' \
                     f'echo "parameter" $1 >> {world.f_cfg.data_join("output.txt")} \n'
    for name in parameters:
        script_content += f'echo "{name}" ${name} >> {world.f_cfg.data_join("output.txt")} \n'

    # transfer script to server and make it executable
    fabric_sudo_command(f"echo '{script_content}' > {world.f_cfg.data_join('script.sh')}")
    fabric_sudo_command(f"chmod +x {world.f_cfg.data_join('script.sh')}")

    # Configure hook
    srv_control.add_hooks('libdhcp_run_script.so')
    srv_control.add_parameter_to_hook(1, 'name', world.f_cfg.data_join('script.sh'))
    srv_control.add_parameter_to_hook(1, 'sync', False)

    # configure and start Kea
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Trigger script
    _send_client_request4()

    # Check contents of the output file ignoring values set as "".
    srv_msg.file_contains_line(world.f_cfg.data_join('output.txt'), None,
                               'parameter leases4_committed')
    for name, value in parameters.items():
        if value != "":
            srv_msg.file_contains_line(world.f_cfg.data_join('output.txt'), None,
                                       f'{name} {value}')

    # Copy output files to forge results folder
    srv_msg.copy_remote(world.f_cfg.data_join("script.sh"), local_filename="script.sh")
    srv_msg.copy_remote(world.f_cfg.data_join("output.txt"), local_filename="output.txt")


@pytest.mark.v4
@pytest.mark.run_script
def test_run_script_lease4_renew():
    """
    Test checks if Run Script hook executes script and uses correct variables.
    First the script is prepared and send to Kea machine.
    Kea is started and script is triggered by desired action.
    Output file is checked for correct parameters and artifacts are copied to test results.
    """
    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.data_join('script.sh'))
    srv_msg.remove_file_from_server(world.f_cfg.data_join('output.txt'))

    # Returned parameter names with expected value.
    # Values marked as "" will not be checked
    parameters = {
        "QUERY4_TYPE": "DHCPREQUEST",
        "QUERY4_TXID": "",
        "QUERY4_LOCAL_ADDR": "255.255.255.255",
        "QUERY4_LOCAL_PORT": "67",
        "QUERY4_REMOTE_ADDR": "0.0.0.0",
        "QUERY4_REMOTE_PORT": "68",
        "QUERY4_IFACE_INDEX": "",
        "QUERY4_IFACE_NAME": f"{world.f_cfg.server_iface}",
        "QUERY4_HOPS": "0",
        "QUERY4_SECS": "0",
        "QUERY4_FLAGS": "0",
        "QUERY4_CIADDR": "0.0.0.0",
        "QUERY4_SIADDR": "0.0.0.0",
        "QUERY4_YIADDR": "0.0.0.0",
        "QUERY4_GIADDR": "0.0.0.0",
        "QUERY4_RELAYED": "false",
        "QUERY4_HWADDR": "ff:01:02:03:ff:04",
        "QUERY4_HWADDR_TYPE": "1",
        "QUERY4_LOCAL_HWADDR": "ff:ff:ff:ff:ff:ff",
        "QUERY4_LOCAL_HWADDR_TYPE": "1",
        "QUERY4_REMOTE_HWADDR": "",
        "QUERY4_REMOTE_HWADDR_TYPE": "1",
        "QUERY4_OPTION_82": "",
        "QUERY4_OPTION_82_SUB_OPTION_1": "",
        "QUERY4_OPTION_82_SUB_OPTION_2": "",
        "SUBNET4_ID": "1",
        "SUBNET4_NAME": "192.168.50.0/24",
        "SUBNET4_PREFIX": "192.168.50.0",
        "SUBNET4_PREFIX_LEN": "24",
        "PKT4_CLIENT_ID": "00:01:02:03:04:05:06",
        "PKT4_HWADDR": "ff:01:02:03:ff:04",
        "PKT4_HWADDR_TYPE": "1",
        "LEASE4_ADDRESS": "192.168.50.1",
        "LEASE4_CLTT": "",
        "LEASE4_HOSTNAME": "aa.four.example.com.",
        "LEASE4_HWADDR": "ff:01:02:03:ff:04",
        "LEASE4_HWADDR_TYPE": "1",
        "LEASE4_STATE": "default",
        "LEASE4_SUBNET_ID": "1",
        "LEASE4_VALID_LIFETIME": "4000",
        "LEASE4_CLIENT_ID": "00:01:02:03:04:05:06"
    }

    # Prepare script to send to Kea
    script_content = f'#!/bin/bash \n' \
                     'if [[ $1 != "lease4_renew" ]]; then exit 0; fi \n' \
                     f'echo "parameter" $1 >> {world.f_cfg.data_join("output.txt")} \n'
    for name in parameters:
        script_content += f'echo "{name}" ${name} >> {world.f_cfg.data_join("output.txt")} \n'

    # transfer script to server and make it executable
    fabric_sudo_command(f"echo '{script_content}' > {world.f_cfg.data_join('script.sh')}")
    fabric_sudo_command(f"chmod +x {world.f_cfg.data_join('script.sh')}")

    # Configure hook
    srv_control.add_hooks('libdhcp_run_script.so')
    srv_control.add_parameter_to_hook(1, 'name', world.f_cfg.data_join('script.sh'))
    srv_control.add_parameter_to_hook(1, 'sync', False)

    # configure and start Kea
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Add a lease to trigger renew later
    cmd = {"command": "lease4-add",
           "arguments": {
               "client-id": "00:01:02:03:04:05:06",
               "hw-address": "ff:01:02:03:ff:04",
               "ip-address": "192.168.50.1",
               "hostname": "aa.four.example.com.",
               "subnet-id": 1,
               "valid-lft": 4000}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == "Lease for address 192.168.50.1, subnet-id 1 added."

    # Trigger script
    _send_client_renew4()

    # Check contents of the output file ignoring values set as "".
    srv_msg.file_contains_line(world.f_cfg.data_join('output.txt'), None,
                               'parameter lease4_renew')
    for name, value in parameters.items():
        if value != "":
            srv_msg.file_contains_line(world.f_cfg.data_join('output.txt'), None,
                                       f'{name} {value}')

    # Copy output files to forge results folder
    srv_msg.copy_remote(world.f_cfg.data_join("script.sh"), local_filename="script.sh")
    srv_msg.copy_remote(world.f_cfg.data_join("output.txt"), local_filename="output.txt")
