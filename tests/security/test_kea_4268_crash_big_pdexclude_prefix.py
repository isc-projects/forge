# Copyright (C) 2026 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from src import srv_msg
from src import srv_control
from src import misc

from src.forge_cfg import world


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.parametrize('channel', ['http', 'unix', 'plain-config'])
def test_kea_4268_crash_big_pdexclude_prefix(channel):
    """Issue description in kea#4268, fix in kea#4295"""
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::10 - 2001:db8::20')
    srv_control.add_http_control_channel()
    srv_control.add_unix_socket()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    world.dhcp_cfg['Dhcp6']['option-data'].append(
        {
            'option-data': [{'code': 67, 'data': '::/ce'}],
        }
    )

    # Using commands makes this test fail on the SARR step until kea#4389 is fixed.
    # So let's have this plain-config parametrization that tests that the config is rejected.
    # TODO: when kea#4389 is merged, remove the plain-config parametrization.
    if channel == 'plain-config':
        world.dhcp_cfg = world.dhcp_cfg['Dhcp6']  # Otherwise, Dhcp6 ends up duplicated.
        srv_control.start_srv('DHCP', 'stopped')
        srv_control.build_and_send_config_files()
        srv_control.start_srv('DHCP', 'started', should_succeed=False)
        return

    command = {'command': 'config-set', 'arguments': world.dhcp_cfg}

    # Expect error.
    if channel == 'http':
        srv_msg.send_ctrl_cmd_via_http(command, exp_result=1)
    elif channel == 'unix':
        srv_msg.send_ctrl_cmd_via_socket(command, exp_result=1)
    else:
        pytest.fail(f'unknown channel {channel}')

    # But commands should still work.
    command = {'command': 'config-get'}
    if channel == 'http':
        srv_msg.send_ctrl_cmd_via_http(command, exp_result=0)
    elif channel == 'unix':
        srv_msg.send_ctrl_cmd_via_socket(command, exp_result=0)
    else:
        pytest.fail(f'unknown channel {channel}')

    # And DHCP should still function.
    srv_msg.SARR('2001:db8::10')
