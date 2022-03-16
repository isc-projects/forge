"""Kea HA states"""

# pylint: disable=invalid-name,line-too-long,too-many-arguments

import pytest

import misc
import srv_control
import srv_msg
from forge_cfg import world
from HA.steps import send_command, HOT_STANDBY, LOAD_BALANCING, wait_until_ha_state, send_heartbeat
# TODO add checking logs in all those tests

WAIT_TIME = 3

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


def _get_status_HA(server1: bool, server2: bool, ha_mode: str, primary_state: str, secondary_state: str, primary_role: str,
                   secondary_role: str, primary_scopes: list, secondary_scopes: list,
                   comm_interrupt: bool, in_touch=True, channel='http'):
    """Check HA dependent status returned by 'status-get' command according to parameters.
    This function checks 2 servers in HA pair.

    :param server1: Should server1 be checked?
    :param server2: Should server2 be checked?
    :param ha_mode: HA mode that servers are in. ('load-balancing', 'hot-standby')
    :param primary_state: HA mode server1 is in. ('hot-standby', 'load-balancing', 'syncing', 'ready', 'waiting' etc.)
    :param secondary_state: HA mode server2 is in. ('hot-standby', 'load-balancing', 'syncing', 'ready', 'waiting' etc.)
    :param primary_role: HA role server1 is in. ('primary', 'secondary', 'standby' etc.)
    :param secondary_role: HA role server2 is in. ('primary', 'secondary', 'standby' etc.)
    :param primary_scopes: Server1 scopes
    :param secondary_scopes: Server2 scopes
    :param comm_interrupt: Is communication interrupted on any server.
    :param in_touch: Are servers in 'in touch' state.
    :param channel: Communication channel for 'status-get' command ('http', 'socket')
    :return:
    """
    if server1:
        # Get status from Server1 and test the response
        cmd = {"command": "status-get", "arguments": {}}
        response = srv_msg.send_ctrl_cmd(cmd, channel=channel, address='$(MGMT_ADDRESS)')

        assert response['arguments']['high-availability'][0]['ha-mode'] == ha_mode
        assert response['arguments']['high-availability'][0]['ha-servers']['local']['role'] == primary_role
        assert response['arguments']['high-availability'][0]['ha-servers']['local']['scopes'] == primary_scopes
        assert response['arguments']['high-availability'][0]['ha-servers']['local']['state'] == primary_state
        assert response['arguments']['high-availability'][0]['ha-servers']['remote']['age'] >= 0
        assert response['arguments']['high-availability'][0]['ha-servers']['remote']['analyzed-packets'] >= 0
        assert response['arguments']['high-availability'][0]['ha-servers']['remote']['communication-interrupted'] == comm_interrupt
        assert response['arguments']['high-availability'][0]['ha-servers']['remote']['connecting-clients'] >= 0
        assert response['arguments']['high-availability'][0]['ha-servers']['remote']['in-touch'] == in_touch
        assert response['arguments']['high-availability'][0]['ha-servers']['remote']['last-scopes'] == secondary_scopes
        assert response['arguments']['high-availability'][0]['ha-servers']['remote']['last-state'] == secondary_state
        assert response['arguments']['high-availability'][0]['ha-servers']['remote']['role'] == secondary_role
        assert response['arguments']['high-availability'][0]['ha-servers']['remote']['unacked-clients'] >= 0
        assert response['arguments']['high-availability'][0]['ha-servers']['remote']['unacked-clients-left'] >= 0
    if server2:
        # Get status from Server2 and test the response
        cmd = {"command": "status-get", "arguments": {}}
        response = srv_msg.send_ctrl_cmd(cmd, channel=channel, address='$(MGMT_ADDRESS_2)')

        assert response['arguments']['high-availability'][0]['ha-mode'] == ha_mode
        assert response['arguments']['high-availability'][0]['ha-servers']['local']['role'] == secondary_role
        assert response['arguments']['high-availability'][0]['ha-servers']['local']['scopes'] == secondary_scopes
        assert response['arguments']['high-availability'][0]['ha-servers']['local']['state'] == secondary_state
        assert response['arguments']['high-availability'][0]['ha-servers']['remote']['age'] >= 0
        assert response['arguments']['high-availability'][0]['ha-servers']['remote']['analyzed-packets'] >= 0
        assert response['arguments']['high-availability'][0]['ha-servers']['remote']['communication-interrupted'] == comm_interrupt
        assert response['arguments']['high-availability'][0]['ha-servers']['remote']['connecting-clients'] >= 0
        assert response['arguments']['high-availability'][0]['ha-servers']['remote']['in-touch'] == in_touch
        assert response['arguments']['high-availability'][0]['ha-servers']['remote']['last-scopes'] == primary_scopes
        assert response['arguments']['high-availability'][0]['ha-servers']['remote']['last-state'] == primary_state
        assert response['arguments']['high-availability'][0]['ha-servers']['remote']['role'] == primary_role
        assert response['arguments']['high-availability'][0]['ha-servers']['remote']['unacked-clients'] >= 0
        assert response['arguments']['high-availability'][0]['ha-servers']['remote']['unacked-clients-left'] >= 0


@pytest.mark.v6
@pytest.mark.v4
@pytest.mark.ha
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_HA_load_balancing_hold_state_always(dhcp_version, channel):

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

    _send_message(dhcp=dhcp_version, expect_answer=False)

    # make sure server 1 stay in waiting state
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "waiting"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "waiting"
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "waiting"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "waiting"

    # Check status-get output on both servers - WAITING
    _get_status_HA(True, True, ha_mode='load-balancing', primary_state='waiting', secondary_state='waiting',
                   primary_role='primary', secondary_role='secondary',
                   primary_scopes=[], secondary_scopes=[],
                   comm_interrupt=False, in_touch=True, channel=channel)

    # continue server1 from WAITING
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'
    wait_until_ha_state("syncing", dhcp_version=dhcp_version)
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "syncing"

    # Check status-get output on both servers - SYNCING/WAITING
    _get_status_HA(True, True, ha_mode='load-balancing', primary_state='syncing', secondary_state='waiting',
                   primary_role='primary', secondary_role='secondary',
                   primary_scopes=[], secondary_scopes=[],
                   comm_interrupt=False, in_touch=True, channel=channel)

    # continue server1 from SYNCING
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'
    wait_until_ha_state("ready", dhcp_version=dhcp_version)
    _send_message(dhcp=dhcp_version, expect_answer=False)
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "ready"
    _send_message(dhcp=dhcp_version, expect_answer=False)

    # Check status-get output on both servers - READY
    _get_status_HA(True, True, ha_mode='load-balancing', primary_state='ready', secondary_state='ready',
                   primary_role='primary', secondary_role='secondary',
                   primary_scopes=[], secondary_scopes=[],
                   comm_interrupt=False, in_touch=True, channel=channel)

    # continue server1 from READY
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'
    wait_until_ha_state("load-balancing", dhcp_version=dhcp_version)
    wait_until_ha_state("load-balancing", dest=world.f_cfg.mgmt_address_2, dhcp_version=dhcp_version)
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    _send_message(dhcp=dhcp_version)

    # Check status-get output on both servers - load-balancing
    _get_status_HA(True, True, ha_mode='load-balancing', primary_state='load-balancing', secondary_state='load-balancing',
                   primary_role='primary', secondary_role='secondary',
                   primary_scopes=['server1'], secondary_scopes=['server2'],
                   comm_interrupt=False, in_touch=True, channel=channel)

    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    # server1 has to keep load-balancing
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "load-balancing"
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "load-balancing"

    # Check status-get output on server1 - load-balancing
    _get_status_HA(True, False, ha_mode='load-balancing', primary_state='load-balancing', secondary_state='unavailable',
                   primary_role='primary', secondary_role='secondary',
                   primary_scopes=['server1'], secondary_scopes=['server2'],
                   comm_interrupt=True, in_touch=True, channel=channel)

    # continue server1 from load-balancing
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'
    wait_until_ha_state("partner-down", dhcp_version=dhcp_version)

    _send_message(dhcp=dhcp_version)

    # Check status-get output on server1 - load-balancing/partner-down
    _get_status_HA(True, False, ha_mode='load-balancing', primary_state='partner-down', secondary_state='unavailable',
                   primary_role='primary', secondary_role='secondary',
                   primary_scopes=["server1", "server2"], secondary_scopes=["server2"],
                   comm_interrupt=True, in_touch=True, channel=channel)

    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    # keep partner-down state
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"

    # continue server1 from partner-down
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'
    wait_until_ha_state("load-balancing", dhcp_version=dhcp_version)
    wait_until_ha_state("load-balancing", dest=world.f_cfg.mgmt_address_2, dhcp_version=dhcp_version)

    # stop server2
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)
    # server1 should stay in load-balancing
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "load-balancing"
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "load-balancing"

    # continue AGAIN from load-balancing
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'

    wait_until_ha_state("partner-down", dhcp_version=dhcp_version)
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"

    # start server2
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"

    # continue
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'
    wait_until_ha_state("load-balancing", dhcp_version=dhcp_version)
    wait_until_ha_state("load-balancing", dest=world.f_cfg.mgmt_address_2, dhcp_version=dhcp_version)


@pytest.mark.v6
@pytest.mark.v4
@pytest.mark.ha
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

    # check that both servers keep waiting (server1 is paused, server2 is waiting for server1
    _send_message(dhcp=dhcp_version, expect_answer=False)
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "waiting"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "waiting"
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "waiting"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "waiting"

    # continue server1 from WAITING
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "syncing"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "waiting"

    # continue server1 from SYNCING
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'

    # keep in ready
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "ready"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "ready"
    _send_message(dhcp=dhcp_version, expect_answer=False)
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
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
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    # server1 has to keep load-balancing
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "load-balancing"
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "load-balancing"
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "load-balancing"

    # continue server1 from load-balancing
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'
    wait_until_ha_state("partner-down", dhcp_version=dhcp_version)
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"

    _send_message(dhcp=dhcp_version)

    # start second server, first should stay in partner-down
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "ready"
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "ready"
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "ready"

    # continue from partner down
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'

    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
    wait_until_ha_state("load-balancing", dhcp_version=dhcp_version)
    wait_until_ha_state("load-balancing", dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)

    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    # this time - no paused states!
    wait_until_ha_state("partner-down", dhcp_version=dhcp_version)
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine is not paused.'
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine is not paused.'
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    wait_until_ha_state("load-balancing", dhcp_version=dhcp_version)
    wait_until_ha_state("load-balancing", dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)

    _send_message(dhcp=dhcp_version)


@pytest.mark.v6
@pytest.mark.v4
@pytest.mark.ha
@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_HA_hot_standby_hold_state_once(channel, dhcp_version):

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

    # keep both in waiting
    _send_message(dhcp=dhcp_version, expect_answer=False)
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "waiting"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "waiting"
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "waiting"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "waiting"

    # Check status-get output on both servers - WAITING
    _get_status_HA(True, True, ha_mode='hot-standby', primary_state='waiting', secondary_state='waiting',
                   primary_role='primary', secondary_role='standby',
                   primary_scopes=[], secondary_scopes=[],
                   comm_interrupt=False, in_touch=True, channel=channel)

    # continue server1 from WAITING
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'

    wait_until_ha_state("syncing", dhcp_version=dhcp_version)
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "waiting"

    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    # Check status-get output on both servers - syncing/waiting
    _get_status_HA(True, True, ha_mode='hot-standby', primary_state='syncing', secondary_state='waiting',
                   primary_role='primary', secondary_role='standby',
                   primary_scopes=[], secondary_scopes=[],
                   comm_interrupt=False, in_touch=True, channel=channel)

    # continue server1 from SYNCING
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'

    wait_until_ha_state("ready", dhcp_version=dhcp_version)
    _send_message(dhcp=dhcp_version, expect_answer=False)

    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "ready"
    _send_message(dhcp=dhcp_version, expect_answer=False)

    # Check status-get output on both servers - ready
    _get_status_HA(True, True, ha_mode='hot-standby', primary_state='ready', secondary_state='ready',
                   primary_role='primary', secondary_role='standby',
                   primary_scopes=[], secondary_scopes=[],
                   comm_interrupt=False, in_touch=True, channel=channel)

    # continue server1 from READY
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'
    wait_until_ha_state("hot-standby", dhcp_version=dhcp_version)
    wait_until_ha_state("hot-standby", dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)

    _send_message(dhcp=dhcp_version)

    # Check status-get output on both servers - hot-standby
    _get_status_HA(True, True, ha_mode='hot-standby', primary_state='hot-standby', secondary_state='hot-standby',
                   primary_role='primary', secondary_role='standby',
                   primary_scopes=['server1'], secondary_scopes=[],
                   comm_interrupt=False, in_touch=True, channel=channel)

    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    # server1 has to keep hot-standby
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "hot-standby"
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "hot-standby"

    # Check status-get output on server1 - hot-standby/unavailable
    _get_status_HA(True, False, ha_mode='hot-standby', primary_state='hot-standby', secondary_state='unavailable',
                   primary_role='primary', secondary_role='standby',
                   primary_scopes=['server1'], secondary_scopes=[],
                   comm_interrupt=True, in_touch=True, channel=channel)

    # continue server1 from hot-standby
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'
    wait_until_ha_state("partner-down", dhcp_version=dhcp_version)
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    _send_message(dhcp=dhcp_version)

    # Check status-get output on server1 - partner-down/unavailable
    _get_status_HA(True, False, ha_mode='hot-standby', primary_state='partner-down', secondary_state='unavailable',
                   primary_role='primary', secondary_role='standby',
                   primary_scopes=['server1'], secondary_scopes=[],
                   comm_interrupt=True, in_touch=True, channel=channel)

    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
    # even if server is back online we should keep partner-down state
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"

    # Check status-get output on both servers - partner-down/ready
    _get_status_HA(True, True, ha_mode='hot-standby', primary_state='partner-down', secondary_state='ready',
                   primary_role='primary', secondary_role='standby',
                   primary_scopes=['server1'], secondary_scopes=[],
                   comm_interrupt=False, in_touch=True, channel=channel)

    # continue from partner-down
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'
    wait_until_ha_state("hot-standby", dhcp_version=dhcp_version)
    wait_until_ha_state("hot-standby", dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    # Check status-get output on both servers - hot-standby
    _get_status_HA(True, True, ha_mode='hot-standby', primary_state='hot-standby', secondary_state='hot-standby',
                   primary_role='primary', secondary_role='standby',
                   primary_scopes=['server1'], secondary_scopes=[],
                   comm_interrupt=False, in_touch=True, channel=channel)

    # stop server 2
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)
    # this time - no paused states!
    wait_until_ha_state("partner-down", dhcp_version=dhcp_version)
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine is not paused.'
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
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
@pytest.mark.ha
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

    _send_message(dhcp=dhcp_version, expect_answer=False)

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "waiting"

    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "waiting"

    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "waiting"

    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "waiting"

    # continue server1 from WAITING
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'

    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "syncing"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "waiting"

    # continue server1 from SYNCING
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'

    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "ready"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "ready"

    _send_message(dhcp=dhcp_version, expect_answer=False)

    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "ready"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "ready"

    _send_message(dhcp=dhcp_version, expect_answer=False)

    # continue server1 from READY
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'

    srv_msg.forge_sleep(WAIT_TIME, 'seconds')
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "hot-standby"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "hot-standby"

    _send_message(dhcp=dhcp_version)

    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)

    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    # server1 has to keep hot-standby
    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "hot-standby"

    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "hot-standby"

    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "hot-standby"

    # continue server1 from hot-standby
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"

    _send_message(dhcp=dhcp_version)

    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "ready"

    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "ready"

    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "ready"
    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "ready"

    # continue server1 from partner-down
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'

    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "hot-standby"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "hot-standby"

    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "hot-standby"

    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "hot-standby"

    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "hot-standby"

    # continue AGAIN from hot-standby
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'

    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"

    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "ready"

    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "ready"

    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "ready"

    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "partner-down"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "ready"
    assert send_command(dhcp_version=dhcp_version, cmd={"command": "ha-continue"})["text"] == 'HA state machine continues.'

    srv_msg.forge_sleep(WAIT_TIME, 'seconds')

    assert send_heartbeat(dhcp_version=dhcp_version)["arguments"]["state"] == "hot-standby"
    assert send_heartbeat(dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "hot-standby"

    _send_message(dhcp=dhcp_version)
