# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Marcin Godzina

"""config-* commands tests"""

import json
import pytest

from src import srv_control
from src import srv_msg
from src import misc
from src.forge_cfg import world
from src.protosupport.multi_protocol_functions import sort_container
from src.protosupport.multi_protocol_functions import remove_file_from_server, copy_file_from_server


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.ca
@pytest.mark.controlchannel
def test_config_commands_usercontext(dhcp_version):
    """
    Test check if user-context is properly handled by config commands.
    """

    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Get current config
    cmd = {"command": "config-get", "arguments": {}}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')
    config_set = response['arguments']

    # Add user context to configuration
    config_set[f"Dhcp{dhcp_version[1]}"]['user-context'] = {
        "ISC": {
            "relay-info": [
                {
                    "hop": 0,
                    "link": "2001:db8:2::1000",
                    "options": "0x00120008706F727431323334",
                    "peer": "fe80::1"
                }
            ]
        },
        "version": [{"number": 1, "rev": 2}, {"id": 1, "no": 2}],
        "class": "!@#$%^&*(`)'_+=-?|\"\\\b\f\n\r\t",
        "tre,e": {"bra,nch1": {"treehouse": 1}, "bra,nch2": 2,
                  "bra,nch3": {"leaf1": 1,
                               "leaf2": ["vein1", "vein2"]}}
    }

    # Sort config for easier comparison
    config_set = sort_container(config_set)

    # Send modified config to server
    cmd = {"command": "config-set", "arguments": config_set}
    srv_msg.send_ctrl_cmd(cmd, 'http')

    # Get new config from server
    cmd = {"command": "config-get", "arguments": {}}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')
    config_get = response['arguments']
    config_get = sort_container(config_get)

    # Compare what we send and what Kea returned.
    assert config_set == config_get, "Send and received configurations are different"

    # Write config to file and download it
    remote_path = world.f_cfg.data_join('config-export.json')
    remove_file_from_server(remote_path)
    cmd = {"command": "config-write", "arguments": {"filename": remote_path}}
    srv_msg.send_ctrl_cmd(cmd, 'http')
    local_path = copy_file_from_server(remote_path, 'config-export.json')

    # Open downloaded file and sort it for easier comparison
    with open(local_path, 'r', encoding="utf-8") as config_file:
        config_write = json.load(config_file)
    config_write = sort_container(config_write)

    # Compare downloaded file with send config.
    assert config_set == config_write, "Send and downloaded file configurations are different"