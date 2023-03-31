# Copyright (C) 2022-2023 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea HA fail detection"""

# pylint: disable=invalid-name
# pylint: disable=line-too-long

import pytest

from src import misc
from src import srv_control
from src import srv_msg

from src.forge_cfg import world
from src.protosupport.multi_protocol_functions import wait_for_message_in_log
from src.softwaresupport import kea

from .steps import generate_leases, wait_until_ha_state, send_increased_elapsed_time, send_heartbeat
from .steps import HOT_STANDBY, LOAD_BALANCING


@pytest.fixture(autouse=True)
def kill_kea_on_second_system():
    # kill kea and clear data at the beginning and at the end
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)
    yield
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.ha
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_HA_hot_standby_fail_detected(dhcp_version, backend):
    # HA SERVER 1
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)
    if dhcp_version == 'v6':
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ffff')
        srv_control.config_srv_prefix('2001:db8:2::', 0, 48, 91)
        srv_control.config_srv_id('LLT', '00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8')
    else:
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.200')
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

    if dhcp_version == 'v6':
        srv_control.config_srv_subnet('2001:db8:1::/64',
                                      '2001:db8:1::1-2001:db8:1::ffff',
                                      world.f_cfg.server2_iface)
        srv_control.config_srv_prefix('2001:db8:2::', 0, 48, 91)
        srv_control.config_srv_id('LLT', '00:01:00:02:52:7b:a8:f0:08:00:27:58:99:99')
    else:
        srv_control.config_srv_subnet('192.168.50.0/24',
                                      '192.168.50.1-192.168.50.200',
                                      world.f_cfg.server2_iface)
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

    wait_until_ha_state('hot-standby', dhcp_version=dhcp_version)
    misc.test_procedure()

    # Get 4 leases.
    leases_count = 4
    set_of_leases_1 = generate_leases(leases_count=leases_count, iana=2, iapd=2, dhcp_version=dhcp_version)
    # check if there are indeed saved
    srv_msg.check_leases(set_of_leases_1, backend=backend)
    # check if those were propagated to other system
    srv_msg.check_leases(set_of_leases_1, backend=backend, dest=world.f_cfg.mgmt_address_2)
    # check status of secondary system
    assert send_heartbeat(dest=world.f_cfg.mgmt_address_2, dhcp_version=dhcp_version)["arguments"]["state"] == "hot-standby"
    # stop primary system
    srv_control.start_srv('DHCP', 'stopped')
    srv_msg.forge_sleep(2, 'seconds')
    # check status of secondary system, it should not be changed
    assert send_heartbeat(dest=world.f_cfg.mgmt_address_2, dhcp_version=dhcp_version)["arguments"]["state"] == "hot-standby"
    # send traffic with increased elapsed time (system is set to change after 5 clients)
    send_increased_elapsed_time(5, dhcp_version=dhcp_version)
    # let's wait until secondary system switch status
    wait_until_ha_state('partner-down', dest=world.f_cfg.mgmt_address_2, dhcp_version=dhcp_version)
    # check leases in secondary system
    set_of_leases_2 = generate_leases(leases_count=leases_count, iana=2, iapd=2, dhcp_version=dhcp_version,
                                      mac="02:02:0c:03:0a:00")
    # start primary
    srv_control.start_srv('DHCP', 'started')
    # wait until it's synced
    wait_until_ha_state('hot-standby', dhcp_version=dhcp_version)

    # Wait for sync.
    if world.proto == 'v4':
        wait_for_message_in_log(r'\[ { "result": 0, "text": "IPv4 lease added\." } \]', leases_count)
    else:
        # 4 IPv6 leases == 2 IA_NA + 2 IA_PD in each response
        wait_for_message_in_log(r'\[ { "result": 0, "text": "Bulk apply of 4 IPv6 leases completed\." } \]', leases_count)

    # check if primary has all assigned addresses
    srv_msg.check_leases(set_of_leases_1, backend=backend)
    srv_msg.check_leases(set_of_leases_2, backend=backend)


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.ha
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_HA_hot_standby_shared_networks_fail_detected(dhcp_version, backend):
    # in shared networks let's add small pools to insure that during test addresses from both pools will be assigned
    # HA SERVER 1
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.3')
        srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                           '192.168.51.6-192.168.51.16')
        srv_control.shared_subnet('192.168.50.0/24', 0)
        srv_control.shared_subnet('192.168.51.0/24', 0)
    else:
        srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::4')
        srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                           '2001:db8:b::11-2001:db8:b::16')
        srv_control.config_srv_prefix('2001:db8:2::', 0, 48, 91)
        srv_control.shared_subnet('2001:db8:a::/64', 0)
        srv_control.shared_subnet('2001:db8:b::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)
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

    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.50.0/24',
                                      '192.168.50.1-192.168.50.3',
                                      world.f_cfg.server2_iface)
        srv_control.config_srv_another_subnet(world.f_cfg.server2_iface,
                                              '192.168.51.0/24',
                                              '192.168.51.6-192.168.51.16')
        srv_control.shared_subnet('192.168.50.0/24', 0)
        srv_control.shared_subnet('192.168.51.0/24', 0)
    else:
        srv_control.config_srv_subnet('2001:db8:a::/64',
                                      '2001:db8:a::1-2001:db8:a::4',
                                      world.f_cfg.server2_iface)
        srv_control.config_srv_another_subnet(world.f_cfg.server2_iface,
                                              '2001:db8:b::/64',
                                              '2001:db8:b::11-2001:db8:b::16')
        srv_control.config_srv_prefix('2001:db8:2::', 0, 48, 91)
        srv_control.shared_subnet('2001:db8:a::/64', 0)
        srv_control.shared_subnet('2001:db8:b::/64', 0)

    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER2_IFACE)"', 0)
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

    wait_until_ha_state('hot-standby', dhcp_version=dhcp_version)
    misc.test_procedure()

    # get 4 leases
    leases_count = 4
    set_of_leases_1 = generate_leases(leases_count=leases_count, dhcp_version=dhcp_version)
    # check if there are indeed saved
    srv_msg.check_leases(set_of_leases_1, backend=backend)
    # check if those were propagated to other system
    srv_msg.check_leases(set_of_leases_1, backend=backend, dest=world.f_cfg.mgmt_address_2)
    # check status of secondary system
    assert send_heartbeat(dest=world.f_cfg.mgmt_address_2, dhcp_version=dhcp_version)["arguments"]["state"] == "hot-standby"
    # stop primary system
    srv_control.start_srv('DHCP', 'stopped')
    srv_msg.forge_sleep(2, 'seconds')
    # check status of secondary system, it should not be changed
    assert send_heartbeat(dest=world.f_cfg.mgmt_address_2, dhcp_version=dhcp_version)["arguments"]["state"] == "hot-standby"
    # send traffic with increased elapsed time (system is set to change after 5 clients)
    send_increased_elapsed_time(5, dhcp_version=dhcp_version)
    # let's wait until secondary system switch status
    wait_until_ha_state('partner-down', dest=world.f_cfg.mgmt_address_2, dhcp_version=dhcp_version)
    # check leases in secondary system
    set_of_leases_2 = generate_leases(leases_count=leases_count, dhcp_version=dhcp_version,
                                      mac="02:02:0c:03:0a:00")
    # start primary
    srv_control.start_srv('DHCP', 'started')
    # wait until it's synced
    wait_until_ha_state('hot-standby', dhcp_version=dhcp_version)

    # Wait for sync.
    if world.proto == 'v4':
        wait_for_message_in_log(r'\[ { "result": 0, "text": "IPv4 lease added\." } \]', leases_count)
    else:
        # 2 IPv6 leases == 1 IA_NA + 1 IA_PD in each response, enabled by default in generate_leases().
        wait_for_message_in_log(r'\[ { "result": 0, "text": "Bulk apply of 2 IPv6 leases completed\." } \]', leases_count)

    # check if primary has all assigned addresses
    srv_msg.check_leases(set_of_leases_1, backend=backend)
    srv_msg.check_leases(set_of_leases_2, backend=backend)


# will always go to secondary
# 02:03:0d:04:0b:01  03:04:0e:05:0c:02 04:05:0f:06:0d:03 05:06:10:07:0e:04
# 00:03:00:01:02:03:0d:04:0b:01 00:03:00:01:05:06:10:07:0e:04
# 00:03:00:01:09:0a:14:0b:12:08 00:03:00:01:0a:0b:15:0c:13:09
@pytest.mark.v6
@pytest.mark.v4
@pytest.mark.ha
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_HA_load_balancing_fail_detected_in_secondary(dhcp_version, backend):
    # TODO maybe we should run this tests just with one backend
    # HA SERVER 1
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)
    if dhcp_version == "v6":
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::30')
        world.dhcp_cfg["subnet6"][0]["pools"][0].update({"client-class": "HA_server1"})
        world.dhcp_cfg["subnet6"][0]["pools"].append({"pool": "2001:db8:1::100-2001:db8:1::130",
                                                      "client-class": "HA_server2"})
    else:
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.30')
        world.dhcp_cfg["subnet4"][0]["pools"][0].update({"client-class": "HA_server1"})
        world.dhcp_cfg["subnet4"][0]["pools"].append({"pool": "192.168.50.100-192.168.50.130",
                                                      "client-class": "HA_server2"})
    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address)
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_ha_hook('libdhcp_ha.so')

    srv_control.update_ha_hook_parameter(LOAD_BALANCING)
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 100,
                                          "max-response-delay": 4000,
                                          "max-unacked-clients": 2,
                                          "this-server-name": "server1"})

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # HA SERVER 2
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)
    # we have to clear data on second system, before test forge does not know that we have multiple systems
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)

    if dhcp_version == "v6":
        srv_control.config_srv_subnet('2001:db8:1::/64',
                                      '2001:db8:1::1-2001:db8:1::30',
                                      world.f_cfg.server2_iface)
        world.dhcp_cfg["subnet6"][0]["pools"][0].update({"client-class": "HA_server1"})
        world.dhcp_cfg["subnet6"][0]["pools"].append({"pool": "2001:db8:1::100-2001:db8:1::130",
                                                      "client-class": "HA_server2"})
    else:
        srv_control.config_srv_subnet('192.168.50.0/24',
                                      '192.168.50.1-192.168.50.30',
                                      world.f_cfg.server2_iface)
        world.dhcp_cfg["subnet4"][0]["pools"][0].update({"client-class": "HA_server1"})
        world.dhcp_cfg["subnet4"][0]["pools"].append({"pool": "192.168.50.100-192.168.50.130",
                                                      "client-class": "HA_server2"})
    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address_2)
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_ha_hook('libdhcp_ha.so')

    srv_control.update_ha_hook_parameter(LOAD_BALANCING)
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 100,
                                          "max-response-delay": 4000,
                                          "max-unacked-clients": 2,
                                          "this-server-name": "server2"})
    world.dhcp_cfg['interfaces-config']['interfaces'] = [world.f_cfg.server2_iface]
    srv_control.build_and_send_config_files(dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    wait_until_ha_state('load-balancing', dhcp_version=dhcp_version)
    wait_until_ha_state('load-balancing', dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)

    misc.test_procedure()
    # Get 10 leases split from server1 and server2.
    set_of_leases_1 = generate_leases(leases_count=10, iana=1, iapd=0, dhcp_version=dhcp_version)
    # check if there are indeed saved
    srv_msg.check_leases(set_of_leases_1, backend=backend)
    # check if those were propagated to other system
    srv_msg.check_leases(set_of_leases_1, dest=world.f_cfg.mgmt_address_2, backend=backend)

    # stop server2
    kea.insert_message_in_server_logs('Just about to stop server2.')
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)
    kea.insert_message_in_server_logs('server2 is now stopped.')

    # The primary node is expected to not enter partner-down untill all these DISCOVERs or SOLICITs
    # were sent. It's a sensitive timing issue, because after each message, forge waits to make sure
    # there is no answer, and that takes time.
    if dhcp_version == 'v4':
        send_increased_elapsed_time(4, dhcp_version=dhcp_version, mac=["02:03:0d:04:0b:01",
                                                                       "03:04:0e:05:0c:02",
                                                                       "04:05:0f:06:0d:03",
                                                                       "05:06:10:07:0e:04"])
    else:
        send_increased_elapsed_time(4, dhcp_version=dhcp_version, duid=["00:03:00:01:01:03:0d:04:0b:01",
                                                                        "00:03:00:01:05:06:10:07:0e:04",
                                                                        "00:03:00:01:09:0a:14:0b:12:08",
                                                                        "00:03:00:01:0a:0b:15:0c:13:09"])
    # server should be in partner down
    resp = wait_until_ha_state('partner-down', dhcp_version=dhcp_version)
    assert "server2" in resp["arguments"]["scopes"]
    assert "server1" in resp["arguments"]["scopes"]

    set_of_leases_2 = generate_leases(leases_count=30, iana=1, iapd=0, dhcp_version=dhcp_version,
                                      mac="03:02:0c:03:0a:00")
    srv_msg.check_leases(set_of_leases_2, backend=backend)

    # clear data on server2 and start it
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    # wait for both of them will be in synced and ready to work
    wait_until_ha_state('load-balancing', dhcp_version=dhcp_version)
    wait_until_ha_state('load-balancing', dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)

    # check if server 2 has all leases
    srv_msg.check_leases(set_of_leases_1, dest=world.f_cfg.mgmt_address_2, backend=backend)
    srv_msg.check_leases(set_of_leases_2, dest=world.f_cfg.mgmt_address_2, backend=backend)


# will always go to primary
# 01:14:e5:cf:c4:e2 01:13:d9:bb:b9:d2 01:12:c5:ae:b0:c7 01:0e:9b:7f:92:8b
# 00:03:00:01:01:13:c7:96:d6:b4 00:03:00:01:01:14:d4:aa:e1:c0 00:03:00:01:01:15:d9:b8:e8:c9
# 00:03:00:01:01:16:ea:ca:eb:dc
@pytest.mark.v6
@pytest.mark.v4
@pytest.mark.ha
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_HA_load_balancing_fail_detected_in_primary(dhcp_version, backend):
    # TODO maybe we should run this tests just with one backend
    # HA SERVER 1
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)
    if dhcp_version == "v6":
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::30')
        world.dhcp_cfg["subnet6"][0]["pools"][0].update({"client-class": "HA_server1"})
        world.dhcp_cfg["subnet6"][0]["pools"].append({"pool": "2001:db8:1::100-2001:db8:1::130",
                                                      "client-class": "HA_server2"})
    else:
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.30')
        world.dhcp_cfg["subnet4"][0]["pools"][0].update({"client-class": "HA_server1"})
        world.dhcp_cfg["subnet4"][0]["pools"].append({"pool": "192.168.50.100-192.168.50.130",
                                                      "client-class": "HA_server2"})
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

    if dhcp_version == "v6":
        srv_control.config_srv_subnet('2001:db8:1::/64',
                                      '2001:db8:1::1-2001:db8:1::30',
                                      world.f_cfg.server2_iface)
        world.dhcp_cfg["subnet6"][0]["pools"][0].update({"client-class": "HA_server1"})
        world.dhcp_cfg["subnet6"][0]["pools"].append({"pool": "2001:db8:1::100-2001:db8:1::130",
                                                      "client-class": "HA_server2"})
    else:
        srv_control.config_srv_subnet('192.168.50.0/24',
                                      '192.168.50.1-192.168.50.30',
                                      world.f_cfg.server2_iface)
        world.dhcp_cfg["subnet4"][0]["pools"][0].update({"client-class": "HA_server1"})
        world.dhcp_cfg["subnet4"][0]["pools"].append({"pool": "192.168.50.100-192.168.50.130",
                                                      "client-class": "HA_server2"})
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

    wait_until_ha_state('load-balancing', dhcp_version=dhcp_version)
    wait_until_ha_state('load-balancing', dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)

    misc.test_procedure()
    # Get 10 leases split from server1 and server2.
    set_of_leases_1 = generate_leases(leases_count=10, iana=1, iapd=0, dhcp_version=dhcp_version)
    # check if there are indeed saved
    srv_msg.check_leases(set_of_leases_1, backend=backend)
    # check if those were propagated to other system
    srv_msg.check_leases(set_of_leases_1, dest=world.f_cfg.mgmt_address_2, backend=backend)

    # stop server1
    srv_control.start_srv('DHCP', 'stopped')
    if dhcp_version == 'v4':
        send_increased_elapsed_time(4, dhcp_version=dhcp_version, mac=["01:14:e5:cf:c4:e2",
                                                                       "01:13:d9:bb:b9:d2",
                                                                       "01:12:c5:ae:b0:c7",
                                                                       "01:0e:9b:7f:92:8b"])
    else:
        send_increased_elapsed_time(4, dhcp_version=dhcp_version, duid=["00:03:00:01:01:13:c7:96:d6:b4",
                                                                        "00:03:00:01:01:14:d4:aa:e1:c0",
                                                                        "00:03:00:01:01:15:d9:b8:e8:c9",
                                                                        "00:03:00:01:01:16:ea:ca:eb:dc"])
    # server2 should be in partner down
    resp = wait_until_ha_state('partner-down', dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)
    assert "server2" in resp["arguments"]["scopes"]
    assert "server1" in resp["arguments"]["scopes"]

    set_of_leases_2 = generate_leases(leases_count=10, iana=1, iapd=0, dhcp_version=dhcp_version,
                                      mac="03:02:0c:03:0a:00")
    srv_msg.check_leases(set_of_leases_2, backend=backend, dest=world.f_cfg.mgmt_address_2)

    # start server1
    srv_control.start_srv('DHCP', 'started')

    # wait for both of them will be in synced and ready to work
    wait_until_ha_state('load-balancing', dhcp_version=dhcp_version)
    wait_until_ha_state('load-balancing', dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)

    # check if server1 has all leases
    srv_msg.check_leases(set_of_leases_1, backend=backend)
    srv_msg.check_leases(set_of_leases_2, backend=backend)
