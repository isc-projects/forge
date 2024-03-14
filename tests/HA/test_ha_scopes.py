# Copyright (C) 2024 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea ha-scopes command"""

# pylint: disable=invalid-name
# pylint: disable=line-too-long

import pytest

from src import misc
from src import srv_control
from src import srv_msg

from src.forge_cfg import world
from .steps import load_hook_libraries, wait_until_ha_state
from .steps import HOT_STANDBY, LOAD_BALANCING, PASSIVE_BACKUP


@pytest.fixture(autouse=True)
def kill_kea_on_second_system():
    # kill kea and clear data at the beginning and at the end
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)
    yield
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)


@pytest.mark.v4_bootp
@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.ha
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('hook_order', ['alphabetical'])  # possible params:  'reverse'
@pytest.mark.parametrize('mode', ['load-balancing', 'hot-standby', 'passive-backup'])
def test_HA_ha_scopes(dhcp_version: str, backend: str, hook_order: str, mode: str):
    """
    Check that Kea recieves ha-scopes command and returns correct scopes.

    :param dhcp_version: v4 or v6, determined by pytest marks
    :param backend: the database backend to be used for leases
    :param hook_order: the order in which hooks are loaded: either alphabetical
    or reverse alphabetical. This is to test all order combinations for each set
    of two hook libraries after problems were found on one order of loading HA
    with leasequery.
    :param mode: the HA mode to be used in test.
    """
    config = {'load-balancing': LOAD_BALANCING, 'hot-standby': HOT_STANDBY, 'passive-backup': PASSIVE_BACKUP}

    # HA SERVER 1
    misc.test_setup()

    srv_control.define_temporary_lease_db_backend(backend)

    # we have to clear data on second system, before test forge does not know that we have multiple systems
    if dhcp_version == 'v6':
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ffff', id=1)
    elif dhcp_version in ['v4', 'v4_bootp']:
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.200', id=1)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.configure_loggers(f'kea-dhcp{world.proto[1]}.dhcpsrv', 'DEBUG', 99)
    srv_control.configure_loggers(f'kea-dhcp{world.proto[1]}.ha-hooks', 'DEBUG', 99)
    srv_control.configure_loggers('kea-ctrl-agent', 'DEBUG', 99, 'kea.log-CTRL')

    load_hook_libraries(dhcp_version, hook_order)

    srv_control.update_ha_hook_parameter(config[mode])
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 100,
                                          "max-response-delay": 1500,
                                          "max-unacked-clients": 0,
                                          "sync-page-limit": 10,
                                          "this-server-name": "server1"})

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # HA SERVER 2
    misc.test_setup()

    srv_control.define_temporary_lease_db_backend(backend)
    # we have to clear data on second system, before test forge does not know that we have multiple systems
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)

    if dhcp_version == 'v6':
        srv_control.config_srv_subnet('2001:db8:1::/64',
                                      '2001:db8:1::1-2001:db8:1::ffff',
                                      world.f_cfg.server2_iface, id=1)
    elif dhcp_version in ['v4', 'v4_bootp']:
        srv_control.config_srv_subnet('192.168.50.0/24',
                                      '192.168.50.1-192.168.50.200',
                                      world.f_cfg.server2_iface, id=1)

    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address_2)
    srv_control.configure_loggers(f'kea-dhcp{world.proto[1]}.dhcpsrv', 'DEBUG', 99)
    srv_control.configure_loggers(f'kea-dhcp{world.proto[1]}.ha-hooks', 'DEBUG', 99)
    srv_control.configure_loggers('kea-ctrl-agent', 'DEBUG', 99, 'kea.log-CTRL2')

    load_hook_libraries(dhcp_version, hook_order)

    srv_control.update_ha_hook_parameter(config[mode])
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 100,
                                          "max-response-delay": 1500,
                                          "max-unacked-clients": 0,
                                          "sync-page-limit": 15,
                                          "this-server-name": "server2"})
    world.dhcp_cfg['interfaces-config']['interfaces'] = [world.f_cfg.server2_iface]
    srv_control.build_and_send_config_files(dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    # Wait for the hot-standby state.
    wait_until_ha_state(mode, dhcp_version=dhcp_version)

    # Send ha-scopes command to the server1
    cmd = {"command": "ha-scopes", "arguments": {"scopes": ["server1", "server2"],
                                                 "server-name": "server1"}}
    srv_msg.send_ctrl_cmd(cmd, address=world.f_cfg.mgmt_address)

    # Check if server1 has received ha-scopes command
    cmd = {"command": "status-get", "arguments": {}}
    response = srv_msg.send_ctrl_cmd(cmd, address=world.f_cfg.mgmt_address)
    assert response['arguments']['high-availability'][0]['ha-servers']['local']['scopes'] == ["server1", "server2"]

    # Send ha-scopes command to the server2
    cmd = {"command": "ha-scopes", "arguments": {"scopes": ["server1", "server2"],
                                                 "server-name": "server1"}}
    srv_msg.send_ctrl_cmd(cmd, address=world.f_cfg.mgmt_address_2)

    # Check if server2 has received ha-scopes command
    cmd = {"command": "status-get", "arguments": {}}
    response = srv_msg.send_ctrl_cmd(cmd, address=world.f_cfg.mgmt_address_2)
    assert response['arguments']['high-availability'][0]['ha-servers']['local']['scopes'] == ["server1", "server2"]
