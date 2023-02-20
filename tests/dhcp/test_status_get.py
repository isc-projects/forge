# Copyright (C) 2022-2023 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""DHCP status-get command tests"""

# pylint: disable=unused-argument

import pytest
from src import misc
from src import srv_msg
from src import srv_control
from src.forge_cfg import world
from src.softwaresupport.multi_server_functions import fabric_sudo_command


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.ca
@pytest.mark.controlchannel
@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_status_get_basic(channel, dhcp_version):
    """ Tests if server responds with expected arguments without checking their content.
    """
    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = {"command": "status-get", "arguments": {}}
    response = srv_msg.send_ctrl_cmd(cmd, channel)

    for cmd in ["pid",
                "reload",
                "uptime",
                "multi-threading-enabled"]:
        assert cmd in response['arguments']


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.ca
@pytest.mark.controlchannel
@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_status_get_reload(channel, dhcp_version):
    """ Tests if server changes last configuration reload timer after config reload.
    """
    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Sleep added to make sure at least one second passed from server start to check
    # difference between uptime and config reload. Kea counts in 1s intervals.
    srv_msg.forge_sleep(1, 'seconds')
    srv_control.start_srv('DHCP', 'reconfigured')
    cmd = {"command": "status-get", "arguments": {}}
    response = srv_msg.send_ctrl_cmd(cmd, channel)

    assert 0 <= response['arguments']['reload'] < response['arguments']['uptime']


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.ca
@pytest.mark.controlchannel
@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_status_get_restart(channel, dhcp_version):
    """ Tests if server reports new PID after restart.
    Test also checks if PID is the same as reported by OS
    """
    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    if world.proto == 'v4':
        pgrep = 'pgrep kea-dhcp4'
    else:
        pgrep = 'pgrep kea-dhcp6'

    os_reported_pid = fabric_sudo_command(pgrep, ignore_errors=True)
    cmd = {"command": "status-get", "arguments": {}}
    response = srv_msg.send_ctrl_cmd(cmd, channel)
    pid = response['arguments']['pid']
    assert pid == int(os_reported_pid)

    srv_control.start_srv('DHCP', 'restarted')
    os_reported_pid = fabric_sudo_command(pgrep, ignore_errors=True)
    cmd = {"command": "status-get", "arguments": {}}
    response = srv_msg.send_ctrl_cmd(cmd, channel)
    assert response['arguments']['pid'] == int(os_reported_pid)

    assert pid != response['arguments']['pid']


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.ca
@pytest.mark.controlchannel
@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_status_get_multi_threading_disabled(channel, dhcp_version):
    """ Tests if server with disabled multi-threading reports it properly.
    Test also checks if certain arguments are omitted in status when multi-threading is disabled.
    """
    misc.test_setup()
    srv_control.configure_multi_threading(False)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = {"command": "status-get", "arguments": {}}
    response = srv_msg.send_ctrl_cmd(cmd, channel)

    assert response['arguments']['multi-threading-enabled'] is False, "multi-threading-enabled is not set to False"
    for cmd in ["thread-pool-size",
                "packet-queue-size",
                "packet-queue-statistics"]:
        assert cmd not in response['arguments']


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.ca
@pytest.mark.controlchannel
def test_status_get_multi_threading_explicit_setting(dhcp_version):
    """ Tests if server with disabled multi-threading reports it properly.
    Test also checks if certain arguments are omitted in status when multi-threading is disabled.
    """
    misc.test_setup()
    srv_control.configure_multi_threading(True, 5, 50)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = {"command": "status-get", "arguments": {}}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')

    assert response['arguments']['multi-threading-enabled'] is True, "multi-threading-enabled is not set to True"
    assert response['arguments']['thread-pool-size'] == 5, "thread-pool-size is not set to 5"
    assert response['arguments']['packet-queue-size'] == 50, "packet-queue-size is not set to 50"


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.ca
@pytest.mark.controlchannel
def test_status_get_multi_threading_default_setting(dhcp_version):
    """ Tests if server with disabled multi-threading reports it properly.
    Test also checks if certain arguments are omitted in status when multi-threading is disabled.
    """
    misc.test_setup()
    world.f_cfg.multi_threading_enabled = False
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = {"command": "status-get", "arguments": {}}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')

    assert response['arguments']['multi-threading-enabled'] is True, "multi-threading-enabled is not set to True"


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.ca
@pytest.mark.controlchannel
@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_status_get_multi_threading_enabled(channel, dhcp_version):
    """ Tests if server with enabled multi-threading reports it properly.
    Test also checks if certain arguments are returned properly in status when multi-threading is enabled.
    """
    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    world.dhcp_cfg['multi-threading'] = {'enable-multi-threading': True, 'packet-queue-size': 21, 'thread-pool-size': 3}
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    cmd = {"command": "status-get", "arguments": {}}
    response = srv_msg.send_ctrl_cmd(cmd, channel)

    assert response['arguments']['multi-threading-enabled'] is True
    assert response['arguments']['thread-pool-size'] == 3
    assert response['arguments']['packet-queue-size'] == 21
    assert response['arguments']['packet-queue-statistics'] == [0.0, 0.0, 0.0]


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.ca
@pytest.mark.controlchannel
@pytest.mark.parametrize('channel', ['http'])
def test_status_get_multi_threading_queue(channel, dhcp_version):
    """ Tests if server with enabled multi-threading reports changes in packet-queue-statistics.
    """
    misc.test_setup()
    world.f_cfg.multi_threading_enabled = True
    if world.proto == 'v4':
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')

    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    if world.proto == 'v4':
        srv_msg.DORA('192.168.50.1')
    else:
        srv_msg.SARR('2001:db8:1::50')

    cmd = {"command": "status-get", "arguments": {}}
    response = srv_msg.send_ctrl_cmd(cmd, channel)

    assert response['arguments']['multi-threading-enabled'] is True
    for i in response['arguments']['packet-queue-statistics']:
        assert i > 0
