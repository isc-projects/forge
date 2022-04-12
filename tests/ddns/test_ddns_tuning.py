# Copyright (C) 2013-2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Marcin Godzina

"""DDNS Tuning Hook basic tests"""

# pylint: disable=invalid-name,line-too-long

import pytest

from src import misc
from src import srv_msg
from src import srv_control


@pytest.mark.v4
@pytest.mark.ddns
def test_ddns_tuning_basic():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.add_hooks('libdhcp_ddns_tuning.so')
    srv_control.add_parameter_to_hook(1, "hostname-expr", "'host-'+hexstring(pkt4.mac,'-')")
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.DORA('192.168.50.1')
    cmd = {"command": "lease4-get-all"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')

    assert response['arguments']['leases'][0]['hostname'] == 'host-ff-01-02-03-ff-04'

