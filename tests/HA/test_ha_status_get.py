"""Kea HA syncing"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_control
import srv_msg

from forge_cfg import world
from HA.steps import generate_leases, load_hook_libraries, wait_until_ha_state, send_heartbeat
from HA.steps import HOT_STANDBY, LOAD_BALANCING, PASSIVE_BACKUP


@pytest.fixture(autouse=True)
def kill_kea_on_second_system():
    # kill kea and clear data at the beginning and at the end
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)
    yield
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)


@pytest.mark.v6
@pytest.mark.v4
@pytest.mark.HA
@pytest.mark.parametrize('channel', ['http'])
def test_HA_hot_standby_status_get(dhcp_version, channel):
    # HA SERVER 1
    misc.test_setup()
    if dhcp_version == 'v6':
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    else:
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address)

    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_ha_hook('libdhcp_ha.so')
    srv_control.update_ha_hook_parameter(HOT_STANDBY)
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 500,
                                          "max-ack-delay": 10000,
                                          "max-response-delay": 1100,
                                          "max-unacked-clients": 0,
                                          "this-server-name": "server1",
                                          "state-machine": {"states": []}})

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # HA SERVER 2
    misc.test_setup()
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)
    if dhcp_version == 'v6':
        srv_control.config_srv_subnet('2001:db8:1::/64',
                                      '2001:db8:1::1-2001:db8:1::1',
                                      world.f_cfg.server2_iface)
    else:
        srv_control.config_srv_subnet('192.168.50.0/24',
                                      '192.168.50.1-192.168.50.1',
                                      world.f_cfg.server2_iface)
    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address_2)

    srv_control.add_hooks('libdhcp_lease_cmds.so')

    srv_control.add_ha_hook('libdhcp_ha.so')
    srv_control.update_ha_hook_parameter(HOT_STANDBY)
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 500,
                                          "max-ack-delay": 10000,
                                          "max-response-delay": 1100,
                                          "max-unacked-clients": 0,
                                          "this-server-name": "server2",
                                          "state-machine": {"states": []}})
    world.dhcp_cfg['interfaces-config']['interfaces'] = [world.f_cfg.server2_iface]
    srv_control.build_and_send_config_files(dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    # wait for servers communication to settle
    for _ in range(10):
        srv_msg.forge_sleep(1, 'seconds')
        cmd = {"command": "status-get", "arguments": {}}
        response = srv_msg.send_ctrl_cmd(cmd, channel, address='$(MGMT_ADDRESS)')
        if not response['arguments']['high-availability'][0]['ha-servers']['remote']["communication-interrupted"] \
                and response['arguments']['high-availability'][0]['ha-servers']['local']['state'] == 'hot-standby'\
                and response['arguments']['high-availability'][0]['ha-servers']['remote']['last-state'] == 'hot-standby':
            break

    # wait_until_ha_state('hot-standby', sleep=2, dhcp_version=dhcp_version)

    # Get status from Server1 and test the response
    cmd = {"command": "status-get", "arguments": {}}
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel, address='$(MGMT_ADDRESS)')

    assert response['arguments']['high-availability'][0]['ha-mode'] == 'hot-standby'

    assert response['arguments']['high-availability'][0]['ha-servers']['local'] == \
           {"role": "primary", "scopes": ["server1"], "state": "hot-standby"}

    assert response['arguments']['high-availability'][0]['ha-servers']['remote']['age'] >= 0
    assert response['arguments']['high-availability'][0]['ha-servers']['remote']['analyzed-packets'] >= 0
    assert response['arguments']['high-availability'][0]['ha-servers']['remote']['communication-interrupted'] is False
    assert response['arguments']['high-availability'][0]['ha-servers']['remote']['connecting-clients'] >= 0
    assert response['arguments']['high-availability'][0]['ha-servers']['remote']['in-touch']
    assert response['arguments']['high-availability'][0]['ha-servers']['remote']['last-scopes'] == []
    assert response['arguments']['high-availability'][0]['ha-servers']['remote']['last-state'] == 'hot-standby'
    assert response['arguments']['high-availability'][0]['ha-servers']['remote']['role'] == 'standby'
    assert response['arguments']['high-availability'][0]['ha-servers']['remote']['unacked-clients'] >= 0
    assert response['arguments']['high-availability'][0]['ha-servers']['remote']['unacked-clients-left'] >= 0

    # Get status from Server2and test the response
    cmd = {"command": "status-get", "arguments": {}}
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel, address='$(MGMT_ADDRESS_2)')

    assert response['arguments']['high-availability'][0]['ha-mode'] == 'hot-standby'

    assert response['arguments']['high-availability'][0]['ha-servers']['local'] == \
           {"role": "standby", "scopes": [], "state": "hot-standby"}

    assert response['arguments']['high-availability'][0]['ha-servers']['remote']['age'] >= 0
    assert response['arguments']['high-availability'][0]['ha-servers']['remote']['analyzed-packets'] >= 0
    assert response['arguments']['high-availability'][0]['ha-servers']['remote']['communication-interrupted'] is False
    assert response['arguments']['high-availability'][0]['ha-servers']['remote']['connecting-clients'] >= 0
    assert response['arguments']['high-availability'][0]['ha-servers']['remote']['in-touch']
    assert response['arguments']['high-availability'][0]['ha-servers']['remote']['last-scopes'] == ["server1"]
    assert response['arguments']['high-availability'][0]['ha-servers']['remote']['last-state'] == 'hot-standby'
    assert response['arguments']['high-availability'][0]['ha-servers']['remote']['role'] == 'primary'
    assert response['arguments']['high-availability'][0]['ha-servers']['remote']['unacked-clients'] >= 0
    assert response['arguments']['high-availability'][0]['ha-servers']['remote']['unacked-clients-left'] >= 0
