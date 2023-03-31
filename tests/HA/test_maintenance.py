# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea HA maintenance mode"""


import pytest

from src import misc
from src import srv_control
from src import srv_msg

from src.forge_cfg import world
from .steps import generate_leases, wait_until_ha_state, send_heartbeat, send_command
from .steps import HOT_STANDBY, LOAD_BALANCING


@pytest.fixture(autouse=True)
def kill_kea_on_second_system():
    # kill kea and clear data at the beginning and at the end
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)
    yield
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)


@pytest.mark.v6
@pytest.mark.ha
@pytest.mark.parametrize('backend', ['memfile'])
def test_hot_standby_maintenance(backend):
    """
    Check maintenance mode in hot standby setup, start of it, leases sync while in maintenance mode,
    correctness of going from maintenance mode to partner down and return to normal hot standby setup.

    Tests both scenarios when maintenance-start command is send to primary as well as to standby node.
    """
    # HA SERVER 1
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ffff')
    srv_control.config_srv_prefix('2001:db8:2::', 0, 48, 91)
    srv_control.config_srv_id('LLT', '00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(MGMT_ADDRESS)')
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_ha_hook('libdhcp_ha.so')

    srv_control.update_ha_hook_parameter(HOT_STANDBY)
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 100,
                                          "max-response-delay": 2500,
                                          "max-unacked-clients": 4,
                                          "this-server-name": "server1"})

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # HA SERVER 2
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)
    # we have to clear data on second system, before test forge does not know that we have multiple systems
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)

    srv_control.config_srv_subnet('2001:db8:1::/64',
                                  '2001:db8:1::1-2001:db8:1::ffff',
                                  world.f_cfg.server2_iface)
    srv_control.config_srv_prefix('2001:db8:2::', 0, 48, 91)
    srv_control.config_srv_id('LLT', '00:01:00:02:52:7b:a8:f0:08:00:27:58:99:99')

    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address_2)
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_ha_hook('libdhcp_ha.so')

    srv_control.update_ha_hook_parameter(HOT_STANDBY)
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 100,
                                          "max-response-delay": 2500,
                                          "max-unacked-clients": 4,
                                          "this-server-name": "server2"})

    world.dhcp_cfg['interfaces-config']['interfaces'] = [world.f_cfg.server2_iface]
    srv_control.build_and_send_config_files(dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    wait_until_ha_state('hot-standby')
    misc.test_procedure()

    # get 2 leases
    set_of_leases_1 = generate_leases(leases_count=2, mac="01:02:0c:03:0a:00",
                                      expected_server_id='00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8')

    # check if there are indeed saved
    srv_msg.check_leases(set_of_leases_1, backend=backend)
    # check if those were propagated to other system
    srv_msg.check_leases(set_of_leases_1, backend=backend, dest=world.f_cfg.mgmt_address_2)
    # check status of secondary system
    assert send_heartbeat(dest=world.f_cfg.mgmt_address_2)["arguments"]["state"] == "hot-standby"

    # start maintenance mode on server 1 (server 2 should go offline)
    send_command({"command": 'ha-maintenance-start'})

    wait_until_ha_state("partner-in-maintenance")
    wait_until_ha_state("in-maintenance", dest=world.f_cfg.mgmt_address_2)

    # assign lease in server 1
    set_of_leases_2 = generate_leases(leases_count=2, mac="02:02:0c:03:0a:00",
                                      expected_server_id='00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8')

    # check if there are indeed saved
    srv_msg.check_leases(set_of_leases_2, backend=backend)
    # check if those were propagated to other system, until server 1 goes to partner-down it will send updates
    srv_msg.check_leases(set_of_leases_2, backend=backend, dest=world.f_cfg.mgmt_address_2)

    # stop server 2
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)
    wait_until_ha_state("partner-down")

    # assign lease in server 1
    set_of_leases_3 = generate_leases(leases_count=2, mac="03:02:0c:03:0a:00",
                                      expected_server_id='00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8')

    # check if there are indeed saved
    srv_msg.check_leases(set_of_leases_3, backend=backend)

    # start server 2
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    # check state on both
    wait_until_ha_state('hot-standby')
    wait_until_ha_state('hot-standby', dest=world.f_cfg.mgmt_address_2)

    # check sync of lease
    srv_msg.check_leases(set_of_leases_3, backend=backend, dest=world.f_cfg.mgmt_address_2)

    # start maintenance mode on server 2 (server 1 should go offline)
    send_command({"command": 'ha-maintenance-start'}, dest=world.f_cfg.mgmt_address_2)

    wait_until_ha_state("partner-in-maintenance", dest=world.f_cfg.mgmt_address_2)
    wait_until_ha_state("in-maintenance")

    # those should be assigned by server 2
    set_of_leases_4 = generate_leases(leases_count=2, mac="04:02:0c:03:0a:00",
                                      expected_server_id='00:01:00:02:52:7b:a8:f0:08:00:27:58:99:99')

    srv_msg.check_leases(set_of_leases_4, backend=backend, dest=world.f_cfg.mgmt_address_2)
    srv_msg.check_leases(set_of_leases_4, backend=backend)

    # stop server 1
    srv_control.start_srv('DHCP', 'stopped')
    wait_until_ha_state("partner-down", dest=world.f_cfg.mgmt_address_2)

    # assign lease in server 2, check state
    set_of_leases_5 = generate_leases(leases_count=2, mac="05:02:0c:03:0a:00",
                                      expected_server_id='00:01:00:02:52:7b:a8:f0:08:00:27:58:99:99')
    srv_msg.check_leases(set_of_leases_5, backend=backend, dest=world.f_cfg.mgmt_address_2)

    # start server 1
    srv_control.start_srv('DHCP', 'started')
    # check state on both
    wait_until_ha_state('hot-standby')
    wait_until_ha_state('hot-standby', dest=world.f_cfg.mgmt_address_2)

    # check if sync worked
    srv_msg.check_leases(set_of_leases_5, backend=backend, dest=world.f_cfg.mgmt_address_2)

    # assign lease should be from server 1 :)
    set_of_leases_6 = generate_leases(leases_count=2, mac="06:02:0c:03:0a:00",
                                      expected_server_id='00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8')
    srv_msg.check_leases(set_of_leases_6, backend=backend)
    srv_msg.check_leases(set_of_leases_6, backend=backend, dest=world.f_cfg.mgmt_address_2)

    # check all leases server 1 and server 2

    all_leases = set_of_leases_6 + set_of_leases_5 + set_of_leases_4 + set_of_leases_3 \
        + set_of_leases_2 + set_of_leases_1

    leases_server_1 = send_command({"command": "lease6-get-all"})["arguments"]["leases"]
    leases_server_2 = send_command({"command": "lease6-get-all"},
                                   dest=world.f_cfg.mgmt_address_2)["arguments"]["leases"]

    all_leases = sorted(all_leases, key=lambda d: d['duid'])
    leases_server_1 = sorted(leases_server_1, key=lambda d: d['hw-address'])
    leases_server_2 = sorted(leases_server_2, key=lambda d: d['hw-address'])

    assert leases_server_2 == leases_server_1, \
        "lists of leases got via leases6-get-all command from both servers are not equal!"
    assert len(leases_server_1) == len(all_leases),\
        "number of leases generated via forge traffic differ from leases received via leases6-get-all command"

    # we already compared lists leases_server_1 and leases_server_2, so now just leases_server_1 and leases_all
    for lease_forge, lease_command in zip(all_leases, leases_server_1):
        assert lease_forge['address'] == lease_command['ip-address'],\
            "Incorrect address saved in one of the leases list"
        assert lease_forge['duid'] == lease_command['duid'],\
            "Incorrect duid saved in one of the leases list"


# Clients using those DUIDs will always be dropped by server1 and accepted by server2
# 00:03:00:01:02:03:0d:04:0b:01
# 00:03:00:01:05:06:10:07:0e:04
# 00:03:00:01:09:0a:14:0b:12:08
# 00:03:00:01:0a:0b:15:0c:13:09


@pytest.mark.v6
@pytest.mark.ha
@pytest.mark.parametrize('backend', ['memfile'])
def test_load_balancing_maintenance(backend):
    """
    Check maintenance mode in load balancing setup, start of it, leases sync while in maintenance mode,
    correctness of going from maintenance mode to partner down and return to normal load balancing setup.

    Tests both scenarios when maintenance-start command is send first to server1 and after returning
    to load balancing mode than to server2.
    """
    # HA SERVER 1
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)

    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::30')
    world.dhcp_cfg["subnet6"][0]["pools"][0].update({"client-class": "HA_server1"})
    world.dhcp_cfg["subnet6"][0]["pools"].append({"pool": "2001:db8:1::100-2001:db8:1::130",
                                                  "client-class": "HA_server2"})
    srv_control.config_srv_id('LLT', '00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8')
    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address)
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_ha_hook('libdhcp_ha.so')

    srv_control.update_ha_hook_parameter(LOAD_BALANCING)
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 100,
                                          "max-response-delay": 2500,
                                          "max-unacked-clients": 2,
                                          "this-server-name": "server1"})

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # HA SERVER 2
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)
    # we have to clear data on second system, before test forge does not know that we have multiple systems
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)

    srv_control.config_srv_subnet('2001:db8:1::/64',
                                  '2001:db8:1::1-2001:db8:1::30',
                                  world.f_cfg.server2_iface)
    world.dhcp_cfg["subnet6"][0]["pools"][0].update({"client-class": "HA_server1"})
    world.dhcp_cfg["subnet6"][0]["pools"].append({"pool": "2001:db8:1::100-2001:db8:1::130",
                                                  "client-class": "HA_server2"})
    srv_control.config_srv_id('LLT', '00:01:00:02:52:7b:a8:f0:08:00:27:58:99:99')
    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address_2)
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_ha_hook('libdhcp_ha.so')

    srv_control.update_ha_hook_parameter(LOAD_BALANCING)
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 100,
                                          "max-response-delay": 2500,
                                          "max-unacked-clients": 2,
                                          "this-server-name": "server2"})
    world.dhcp_cfg['interfaces-config']['interfaces'] = [world.f_cfg.server2_iface]
    srv_control.build_and_send_config_files(dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    wait_until_ha_state('load-balancing')
    wait_until_ha_state('load-balancing', dest=world.f_cfg.mgmt_address_2)

    misc.test_procedure()
    # get 10 leases some form server1 and some from server2
    set_of_leases_1 = generate_leases(leases_count=2)
    # check if there are indeed saved
    srv_msg.check_leases(set_of_leases_1, backend=backend)
    # check if those were propagated to other system
    srv_msg.check_leases(set_of_leases_1, dest=world.f_cfg.mgmt_address_2, backend=backend)

    # start maintenance on server 1 (server 2 goes offline)
    send_command({"command": 'ha-maintenance-start'})

    # wait for proper state and scopes
    resp = wait_until_ha_state("partner-in-maintenance")
    assert "server2" in resp["arguments"]["scopes"], "server2 scope is missing from server1"
    assert "server1" in resp["arguments"]["scopes"], "server1 scope is missing from server1"
    resp = wait_until_ha_state("in-maintenance", dest=world.f_cfg.mgmt_address_2)
    assert len(resp["arguments"]["scopes"]) == 0, "Server 2 should not have any pool scopes when in maintenance!"

    # assign lease in server 1 (use duids that should go to server 2)
    set_of_leases_2 = generate_leases(leases_count=1, mac="02:03:0d:04:0b:01",
                                      expected_server_id='00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8')

    set_of_leases_2 += generate_leases(leases_count=1, mac="05:06:10:07:0e:04",
                                       expected_server_id='00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8')

    # check if there are indeed saved
    srv_msg.check_leases(set_of_leases_2, backend=backend)
    # check if those were propagated to other system
    srv_msg.check_leases(set_of_leases_2, dest=world.f_cfg.mgmt_address_2, backend=backend)

    # stop server 2
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)
    wait_until_ha_state("partner-down")

    # assign lease in server 1 (use duids that should go to server 2)
    set_of_leases_3 = generate_leases(leases_count=1, mac="09:0a:14:0b:12:08",
                                      expected_server_id='00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8')
    set_of_leases_3 += generate_leases(leases_count=1, mac="0a:0b:15:0c:13:09",
                                       expected_server_id='00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8')

    # check if there are indeed saved
    srv_msg.check_leases(set_of_leases_2, backend=backend)
    # check if those were propagated to other system
    srv_msg.check_leases(set_of_leases_2, dest=world.f_cfg.mgmt_address_2, backend=backend)

    # start server 2
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)
    # check state on both
    resp = wait_until_ha_state('load-balancing')
    assert "server1" in resp["arguments"]["scopes"], "Server 1 should have just serve1 scope"
    resp = wait_until_ha_state('load-balancing', dest=world.f_cfg.mgmt_address_2)
    assert "server2" in resp["arguments"]["scopes"], "Server 2 should have just serve2 scope"
    # check if sync worked
    srv_msg.check_leases(set_of_leases_3, backend=backend)
    srv_msg.check_leases(set_of_leases_3, backend=backend, dest=world.f_cfg.mgmt_address_2)

    # start maintenance mode on server 2 (server 1 should go offline)
    send_command({"command": 'ha-maintenance-start'}, dest=world.f_cfg.mgmt_address_2)

    wait_until_ha_state("partner-in-maintenance", dest=world.f_cfg.mgmt_address_2)
    wait_until_ha_state("in-maintenance")

    # those should be assigned by server 2
    set_of_leases_4 = generate_leases(leases_count=10, mac="04:02:0c:03:0a:00",
                                      expected_server_id='00:01:00:02:52:7b:a8:f0:08:00:27:58:99:99')

    srv_msg.check_leases(set_of_leases_4, backend=backend, dest=world.f_cfg.mgmt_address_2)
    srv_msg.check_leases(set_of_leases_4, backend=backend)

    # stop server 1
    srv_control.start_srv('DHCP', 'stopped')
    wait_until_ha_state("partner-down", dest=world.f_cfg.mgmt_address_2)

    # those should be assigned by server 2
    set_of_leases_5 = generate_leases(leases_count=4, mac="07:02:0c:03:0a:00",
                                      expected_server_id='00:01:00:02:52:7b:a8:f0:08:00:27:58:99:99')

    srv_msg.check_leases(set_of_leases_5, backend=backend, dest=world.f_cfg.mgmt_address_2)

    # start server 1
    srv_control.start_srv('DHCP', 'started')
    # check state on both
    resp = wait_until_ha_state('load-balancing')
    assert "server1" in resp["arguments"]["scopes"], "Server 1 should have just serve1 scope"
    resp = wait_until_ha_state('load-balancing', dest=world.f_cfg.mgmt_address_2)
    assert "server2" in resp["arguments"]["scopes"], "Server 2 should have just serve2 scope"

    all_leases = set_of_leases_5 + set_of_leases_4 + set_of_leases_3 + set_of_leases_2 + set_of_leases_1

    leases_server_1 = send_command({"command": "lease6-get-all"})["arguments"]["leases"]
    leases_server_2 = send_command({"command": "lease6-get-all"},
                                   dest=world.f_cfg.mgmt_address_2)["arguments"]["leases"]

    all_leases = sorted(all_leases, key=lambda d: d['duid'])
    leases_server_1 = sorted(leases_server_1, key=lambda d: d['hw-address'])
    leases_server_2 = sorted(leases_server_2, key=lambda d: d['hw-address'])

    assert leases_server_2 == leases_server_1,\
        "lists of leases got via leases6-get-all command from both servers are not equal!"
    assert len(leases_server_1) == len(all_leases),\
        "number of leases generated via forge traffic differ from leases received via leases6-get-all command"

    # we already compared lists leases_server_1 and leases_server_2, so now just leases_server_1 and leases_all
    for lease_forge, lease_command in zip(all_leases, leases_server_1):
        assert lease_forge['address'] == lease_command['ip-address'],\
            "Incorrect address saved in one of the leases list"
        assert lease_forge['duid'] == lease_command['duid'],\
            "Incorrect duid saved in one of the leases list"
