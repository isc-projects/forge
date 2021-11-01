"""Kea HA states"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_control
import srv_msg
from forge_cfg import world
from HA.steps import send_command, HOT_STANDBY, LOAD_BALANCING, wait_until_ha_state, send_heartbeat
# TODO add checking logs in all those tests


@pytest.fixture(autouse=True)
def kill_kea_on_second_system():
    # kill kea and clear data at the beginning and at the end
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)
    yield
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)


def _send_message(dhcp='v6', expect_answer=True):
    if dhcp == 'v6':
        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_does_include('Client', 'IA-NA')
        srv_msg.client_send_msg('SOLICIT')
        if expect_answer:
            srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
            srv_msg.response_check_include_option(1)
            srv_msg.response_check_include_option(2)
            srv_msg.response_check_include_option(3)
            srv_msg.response_check_option_content(3, 'sub-option', 5)
        else:
            srv_msg.send_dont_wait_for_message()
    else:
        misc.test_procedure()
        srv_msg.client_requests_option(1)
        srv_msg.client_send_msg('DISCOVER')
        if expect_answer:
            srv_msg.send_wait_for_message('MUST', 'OFFER')
        else:
            srv_msg.send_dont_wait_for_message()


@pytest.mark.v6
@pytest.mark.v4
@pytest.mark.HA
def test_HA_load_balancing_hold_state_always(dhcp_version):

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
    srv_control.update_ha_hook_parameter(LOAD_BALANCING)
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 100,
                                          "max-response-delay": 1100,
                                          "max-unacked-clients": 0,
                                          "this-server-name": "server1",
                                          "state-machine": {"states": [{"state": "waiting", "pause": "always"},
                                                                       {"state": "syncing", "pause": "always"},
                                                                       {"state": "ready", "pause": "always"},
                                                                       {"state": "load-balancing", "pause": "always"},
                                                                       {"state": "partner-down", "pause": "always"}]}})

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # HA SERVER 2
    misc.test_setup()

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
    srv_control.update_ha_hook_parameter(LOAD_BALANCING)
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 100,
                                          "max-response-delay": 1100,
                                          "max-unacked-clients": 0,
                                          "this-server-name": "server2",
                                          "state-machine": {"states": []}})
    world.dhcp_cfg['interfaces-config']['interfaces'] = [world.f_cfg.server2_iface]
    srv_control.build_and_send_config_files(dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    srv_msg.forge_sleep(3, 'seconds')

    _send_message(dhcp=dhcp_version, expect_answer=False)

    # make sure server 1 stay in waiting state
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "waiting"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "waiting"
    srv_msg.forge_sleep(3, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "waiting"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "waiting"

    # continue server1 from WAITING
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'
    wait_until_ha_state("syncing", dhcp_version=dhcp_version)
    srv_msg.forge_sleep(3, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "syncing"

    # continue server1 from SYNCING
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'
    wait_until_ha_state("ready", dhcp_version=dhcp_version)
    _send_message(dhcp=dhcp_version, expect_answer=False)
    srv_msg.forge_sleep(3, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "ready"
    _send_message(dhcp=dhcp_version, expect_answer=False)

    # continue server1 from READY
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'
    wait_until_ha_state("load-balancing", dhcp_version=dhcp_version)
    wait_until_ha_state("load-balancing", dest=world.f_cfg.mgmt_address_2, dhcp_version=dhcp_version)

    _send_message(dhcp=dhcp_version)

    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)
    srv_msg.forge_sleep(3, 'seconds')

    # server1 has to keep load-balancing
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "load-balancing"
    srv_msg.forge_sleep(3, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "load-balancing"

    # continue server1 from load-balancing
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'
    wait_until_ha_state("partner-down", dhcp_version=dhcp_version)

    _send_message(dhcp=dhcp_version)

    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    # keep partner-down state
    srv_msg.forge_sleep(3, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    srv_msg.forge_sleep(3, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"

    # continue server1 from partner-down
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'
    wait_until_ha_state("load-balancing", dhcp_version=dhcp_version)
    wait_until_ha_state("load-balancing", dest=world.f_cfg.mgmt_address_2, dhcp_version=dhcp_version)

    # stop server2
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)
    # server1 should stay in load-balancing
    srv_msg.forge_sleep(3, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "load-balancing"
    srv_msg.forge_sleep(3, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "load-balancing"

    # continue AGAIN from load-balancing
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'

    wait_until_ha_state("partner-down", dhcp_version=dhcp_version)
    srv_msg.forge_sleep(3, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"

    # start server2
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)
    srv_msg.forge_sleep(3, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    srv_msg.forge_sleep(3, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"

    # continue
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'
    wait_until_ha_state("load-balancing", dhcp_version=dhcp_version)
    wait_until_ha_state("load-balancing", dest=world.f_cfg.mgmt_address_2, dhcp_version=dhcp_version)


@pytest.mark.v6
@pytest.mark.v4
@pytest.mark.HA
def test_HA_load_balancing_hold_state_once(dhcp_version):

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
    srv_control.update_ha_hook_parameter(LOAD_BALANCING)
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 0,
                                          "max-response-delay": 1100,
                                          "max-unacked-clients": 0,
                                          "this-server-name": "server1",
                                          "state-machine": {"states": [{"state": "waiting", "pause": "once"},
                                                                       {"state": "syncing", "pause": "once"},
                                                                       {"state": "ready", "pause": "once"},
                                                                       {"state": "load-balancing", "pause": "once"},
                                                                       {"state": "partner-down", "pause": "once"}]}})

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
    srv_control.update_ha_hook_parameter(LOAD_BALANCING)
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 0,
                                          "max-response-delay": 1100,
                                          "max-unacked-clients": 0,
                                          "this-server-name": "server2",
                                          "state-machine": {"states": []}})
    world.dhcp_cfg['interfaces-config']['interfaces'] = [world.f_cfg.server2_iface]
    srv_control.build_and_send_config_files(dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)
    srv_msg.forge_sleep(3, 'seconds')

    # check that both servers keep waiting (server1 is paused, server2 is waiting for server1
    _send_message(dhcp=dhcp_version, expect_answer=False)
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "waiting"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "waiting"
    srv_msg.forge_sleep(3, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "waiting"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "waiting"

    # continue server1 from WAITING
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'
    srv_msg.forge_sleep(3, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "syncing"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "waiting"

    # continue server1 from SYNCING
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'

    # keep in ready
    srv_msg.forge_sleep(3, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "ready"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "ready"
    _send_message(dhcp=dhcp_version, expect_answer=False)
    srv_msg.forge_sleep(3, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "ready"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "ready"
    _send_message(dhcp=dhcp_version, expect_answer=False)

    # continue server1 from READY
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'
    wait_until_ha_state("load-balancing", dhcp_version=dhcp_version)
    wait_until_ha_state("load-balancing", dest=world.f_cfg.mgmt_address_2, dhcp_version=dhcp_version)

    _send_message(dhcp=dhcp_version)

    # stop server2, server1 should not move to partner-down
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)
    srv_msg.forge_sleep(3, 'seconds')

    # server1 has to keep load-balancing
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "load-balancing"
    srv_msg.forge_sleep(3, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "load-balancing"
    srv_msg.forge_sleep(3, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "load-balancing"

    # continue server1 from load-balancing
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'
    wait_until_ha_state("partner-down", dhcp_version=dhcp_version)
    srv_msg.forge_sleep(3, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"

    _send_message(dhcp=dhcp_version)

    # start second server, first should stay in partner-down
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    srv_msg.forge_sleep(3, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "ready"
    srv_msg.forge_sleep(3, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "ready"
    srv_msg.forge_sleep(3, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "ready"

    # continue from partner down
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'

    srv_msg.forge_sleep(3, 'seconds')
    wait_until_ha_state("load-balancing", dhcp_version=dhcp_version)
    wait_until_ha_state("load-balancing", dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)

    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)
    srv_msg.forge_sleep(3, 'seconds')

    # this time - no paused states!
    wait_until_ha_state("partner-down", dhcp_version=dhcp_version)
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine is not paused.'
    srv_msg.forge_sleep(3, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine is not paused.'
    srv_msg.forge_sleep(3, 'seconds')

    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    wait_until_ha_state("load-balancing", dhcp_version=dhcp_version)
    wait_until_ha_state("load-balancing", dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)

    _send_message(dhcp=dhcp_version)


@pytest.mark.v6
@pytest.mark.v4
@pytest.mark.HA
def test_HA_hot_standby_hold_state_once(dhcp_version):

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
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 10000,
                                          "max-response-delay": 1100,
                                          "max-unacked-clients": 0,
                                          "this-server-name": "server1",
                                          "state-machine": {"states": [{"state": "waiting", "pause": "once"},
                                                                       {"state": "syncing", "pause": "once"},
                                                                       {"state": "ready", "pause": "once"},
                                                                       {"state": "hot-standby", "pause": "once"},
                                                                       {"state": "partner-down", "pause": "once"}]}})

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
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 10000,
                                          "max-response-delay": 1100,
                                          "max-unacked-clients": 0,
                                          "this-server-name": "server2",
                                          "state-machine": {"states": []}})
    world.dhcp_cfg['interfaces-config']['interfaces'] = [world.f_cfg.server2_iface]
    srv_control.build_and_send_config_files(dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)
    srv_msg.forge_sleep(3, 'seconds')

    # keep both in waiting
    _send_message(dhcp=dhcp_version, expect_answer=False)
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "waiting"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "waiting"
    srv_msg.forge_sleep(3, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "waiting"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "waiting"

    # continue server1 from WAITING
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'

    wait_until_ha_state("syncing", dhcp_version=dhcp_version)
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "waiting"

    # continue server1 from SYNCING
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'

    wait_until_ha_state("ready", dhcp_version=dhcp_version)
    _send_message(dhcp=dhcp_version, expect_answer=False)

    srv_msg.forge_sleep(3, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "ready"
    _send_message(dhcp=dhcp_version, expect_answer=False)

    # continue server1 from READY
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'
    wait_until_ha_state("hot-standby", dhcp_version=dhcp_version)
    wait_until_ha_state("hot-standby", dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)

    _send_message(dhcp=dhcp_version)

    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)
    srv_msg.forge_sleep(3, 'seconds')

    # server1 has to keep hot-standby
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "hot-standby"
    srv_msg.forge_sleep(3, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "hot-standby"

    # continue server1 from hot-standby
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'
    wait_until_ha_state("partner-down", dhcp_version=dhcp_version)
    srv_msg.forge_sleep(3, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    _send_message(dhcp=dhcp_version)

    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)
    srv_msg.forge_sleep(3, 'seconds')
    # even if serrver is back online we should keep partner-down state
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    srv_msg.forge_sleep(3, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"

    # continue from partner-down
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'
    wait_until_ha_state("hot-standby", dhcp_version=dhcp_version)
    wait_until_ha_state("hot-standby", dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)

    # stop server 2
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)
    # this time - no paused states!
    wait_until_ha_state("partner-down", dhcp_version=dhcp_version)
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine is not paused.'
    srv_msg.forge_sleep(3, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine is not paused.'

    # start server2
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine is not paused.'
    wait_until_ha_state("hot-standby", dhcp_version=dhcp_version)
    wait_until_ha_state("hot-standby", dhcp_version=dhcp_version)

    _send_message(dhcp=dhcp_version)


@pytest.mark.v6
@pytest.mark.v4
@pytest.mark.HA
def test_HA_hot_standby_hold_state_always(dhcp_version):

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
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 0,
                                          "max-response-delay": 1100,
                                          "max-unacked-clients": 0,
                                          "this-server-name": "server1",
                                          "state-machine": {"states": [{"state": "waiting", "pause": "always"},
                                                                       {"state": "syncing", "pause": "always"},
                                                                       {"state": "ready", "pause": "always"},
                                                                       {"state": "hot-standby", "pause": "always"},
                                                                       {"state": "partner-down", "pause": "always"}]}})

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
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 0,
                                          "max-response-delay": 1100,
                                          "max-unacked-clients": 0,
                                          "this-server-name": "server2",
                                          "state-machine": {"states": []}})
    world.dhcp_cfg['interfaces-config']['interfaces'] = [world.f_cfg.server2_iface]
    srv_control.build_and_send_config_files(dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    srv_msg.forge_sleep(3, 'seconds')

    _send_message(dhcp=dhcp_version, expect_answer=False)

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "waiting"

    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "waiting"

    srv_msg.forge_sleep(3, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "waiting"

    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "waiting"

    # continue server1 from WAITING
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'

    srv_msg.forge_sleep(3, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "syncing"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "waiting"

    # continue server1 from SYNCING
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'

    srv_msg.forge_sleep(3, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "ready"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "ready"

    _send_message(dhcp=dhcp_version, expect_answer=False)

    srv_msg.forge_sleep(3, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "ready"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "ready"

    _send_message(dhcp=dhcp_version, expect_answer=False)

    # continue server1 from READY
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'

    srv_msg.forge_sleep(3, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "hot-standby"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "hot-standby"

    _send_message(dhcp=dhcp_version)

    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)

    srv_msg.forge_sleep(3, 'seconds')

    # server1 has to keep hot-standby
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "hot-standby"

    srv_msg.forge_sleep(3, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "hot-standby"

    srv_msg.forge_sleep(3, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "hot-standby"

    # continue server1 from hot-standby
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'
    srv_msg.forge_sleep(3, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    srv_msg.forge_sleep(3, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"

    _send_message(dhcp=dhcp_version)

    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    srv_msg.forge_sleep(3, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "ready"

    srv_msg.forge_sleep(3, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "ready"

    srv_msg.forge_sleep(3, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "ready"
    srv_msg.forge_sleep(3, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "ready"

    # continue server1 from partner-down
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'

    srv_msg.forge_sleep(3, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "hot-standby"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "hot-standby"

    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "hot-standby"

    srv_msg.forge_sleep(3, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "hot-standby"

    srv_msg.forge_sleep(3, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "hot-standby"

    # continue AGAIN from hot-standby
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'

    srv_msg.forge_sleep(3, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"

    srv_msg.forge_sleep(3, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    srv_msg.forge_sleep(3, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "ready"

    srv_msg.forge_sleep(3, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "ready"

    srv_msg.forge_sleep(3, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "ready"

    srv_msg.forge_sleep(3, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "ready"
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'

    srv_msg.forge_sleep(3, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "hot-standby"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "hot-standby"

    _send_message(dhcp=dhcp_version)
