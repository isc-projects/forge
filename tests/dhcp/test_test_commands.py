# Copyright (C) 2024 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""DHCP *-test command tests"""


import pytest
from src import misc
from src import srv_msg
from src import srv_control
from src.forge_cfg import world
from src.softwaresupport.multi_server_functions import fabric_sudo_command


@pytest.mark.v4
@pytest.mark.ca
@pytest.mark.controlchannel
@pytest.mark.parametrize('channel', ['socket'])
def test_subnet4_select_test_negative(channel, dhcp_version):
    """ Tests if server responds with expected arguments without checking their content.
    """
    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = {"command": "subnet4-select-test"}
    response = srv_msg.send_ctrl_cmd(cmd, channel, exp_result = 1)

    assert response['text'] == 'empty arguments'


    cmd = {"command": "subnet4-select-test", "arguments": {}}
    response = srv_msg.send_ctrl_cmd(cmd, channel, exp_result = 3)

    assert response['text'] == 'no subnet selected'