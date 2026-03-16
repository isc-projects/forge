# Copyright (C) 2026 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from src import srv_msg
from src import srv_control
from src import misc


@pytest.mark.controlchannel
def test_kea_4365_empty_control_sockets():
    """kea#4365"""
    misc.test_setup()
    srv_control.agent_control_channel()
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('CA', 'started')

    config = {'Control-agent': {'control-sockets': {'': {}}}}
    command = {'command': 'config-set', 'arguments': config}

    # Expect error.
    srv_msg.send_ctrl_cmd_via_http(command, exp_result=1)

    # Check that commands still work.
    srv_msg.send_ctrl_cmd_via_http({'command': 'config-get'}, exp_result=0)
