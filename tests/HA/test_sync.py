# Copyright (C) 2020-2023 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea HA syncing"""

# pylint: disable=invalid-name
# pylint: disable=line-too-long

import pytest

from src import misc
from src import srv_control
from src import srv_msg

from src.forge_cfg import world
from src.protosupport.multi_protocol_functions import wait_for_message_in_log, fabric_sudo_command
from src.softwaresupport.cb_model import setup_server_with_radius
from src.softwaresupport import radius

from .steps import generate_leases, load_hook_libraries, increase_mac, wait_until_ha_state
from .steps import HOT_STANDBY, LOAD_BALANCING, PASSIVE_BACKUP


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
@pytest.mark.parametrize('hook_order', ['alphabetical'])  # possible params:  'reverse'
def test_HA_hot_standby_multiple_leases_v6(hook_order: str):
    """
    Check that Kea HA can sync multiple IA_NA and IA_PD leases provided together
    in the same exchange.

    :param hook_order: the order in which hooks are loaded: either alphabetical
    or reverse alphabetical. This is to test all order combinations for each set
    of two hook libraries after problems were found on one order of loading HA
    with leasequery.
    """

    # HA SERVER 1
    misc.test_setup()
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
                                          "max-response-delay": 1500,
                                          "max-unacked-clients": 0,
                                          'sync-page-limit': 2,
                                          "this-server-name": "server1"})

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # HA SERVER 2
    misc.test_setup()
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)

    srv_control.config_srv_subnet('2001:db8:1::/64',
                                  '2001:db8:1::1-2001:db8:1::ffff',
                                  world.f_cfg.server2_iface)
    srv_control.config_srv_prefix('2001:db8:2::', 0, 48, 91)
    srv_control.config_srv_id('LLT', '00:01:00:02:52:7b:a8:f0:08:00:27:58:99:99')
    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address_2)

    load_hook_libraries('v6', hook_order)

    srv_control.update_ha_hook_parameter(HOT_STANDBY)
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 100,
                                          "max-response-delay": 1500,
                                          "max-unacked-clients": 0,
                                          'sync-page-limit': 2,
                                          "this-server-name": "server2"})
    world.dhcp_cfg['interfaces-config']['interfaces'] = [world.f_cfg.server2_iface]
    srv_control.build_and_send_config_files(dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    wait_until_ha_state('hot-standby')

    # Message exchanges
    misc.test_procedure()
    set_of_leases_1 = generate_leases(leases_count=4, iana=3, iapd=2)
    srv_msg.check_leases(set_of_leases_1)
    srv_msg.check_leases(set_of_leases_1, dest=world.f_cfg.mgmt_address_2)

    # Stop server 1 and wait for server 2 to enter partner-down state.
    srv_control.start_srv('DHCP', 'stopped')
    wait_until_ha_state('partner-down', dest=world.f_cfg.mgmt_address_2)

    # Check logs in server1.
    wait_for_message_in_log('HA_STATE_TRANSITION server1: server transitions from PARTNER-DOWN to '
                            'HOT-STANDBY state, partner state is READY')

    # Check logs in server2.
    wait_for_message_in_log(r'HA_LEASES_SYNC_LEASE_PAGE_RECEIVED server2: received [0-9][0-9]* leases '
                            'from server1', destination=world.f_cfg.mgmt_address_2)
    wait_for_message_in_log('HA_SYNC_SUCCESSFUL server2: lease database synchronization with '
                            'server1 completed successfully',
                            destination=world.f_cfg.mgmt_address_2)
    wait_for_message_in_log('HA_STATE_TRANSITION server2: server transitions from READY to '
                            'HOT-STANDBY state, partner state is HOT-STANDBY',
                            destination=world.f_cfg.mgmt_address_2)

    # More message exchanges
    set_of_leases_2 = generate_leases(leases_count=4, iana=3, iapd=2, mac="02:02:0c:03:0a:00")

    srv_control.start_srv('DHCP', 'started')
    wait_until_ha_state('hot-standby')

    srv_msg.check_leases(set_of_leases_1)
    srv_msg.check_leases(set_of_leases_2)

    # Check that bulk apply was used. 5 IPv6 leases == 3 IA_NA + 2 IA_PD in each response
    wait_for_message_in_log('Bulk apply of 5 IPv6 leases completed.', 4)


@pytest.mark.v4_bootp
@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.ha
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('hook_order', ['alphabetical'])  # possible params:  'reverse'
def test_HA_hot_standby_different_sync_page_limit(dhcp_version: str, backend: str, hook_order: str):
    """
    Check that Kea HA nodes can work if they have different sync-page-limit
    configuration entries.

    :param dhcp_version: v4 or v6, determined by pytest marks
    :param backend: the database backend to be used for leases
    :param hook_order: the order in which hooks are loaded: either alphabetical
    or reverse alphabetical. This is to test all order combinations for each set
    of two hook libraries after problems were found on one order of loading HA
    with leasequery.
    """

    # HA SERVER 1
    misc.test_setup()

    srv_control.define_temporary_lease_db_backend(backend)

    # we have to clear data on second system, before test forge does not know that we have multiple systems
    if dhcp_version == 'v6':
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ffff')
    elif dhcp_version in ['v4', 'v4_bootp']:
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.200')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.configure_loggers(f'kea-dhcp{world.proto[1]}.dhcpsrv', 'DEBUG', 99)
    srv_control.configure_loggers(f'kea-dhcp{world.proto[1]}.ha-hooks', 'DEBUG', 99)
    srv_control.configure_loggers('kea-ctrl-agent', 'DEBUG', 99, 'kea.log-CTRL')

    load_hook_libraries(dhcp_version, hook_order)

    srv_control.update_ha_hook_parameter(HOT_STANDBY)
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
                                      world.f_cfg.server2_iface)
    elif dhcp_version in ['v4', 'v4_bootp']:
        srv_control.config_srv_subnet('192.168.50.0/24',
                                      '192.168.50.1-192.168.50.200',
                                      world.f_cfg.server2_iface)

    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address_2)
    srv_control.configure_loggers(f'kea-dhcp{world.proto[1]}.dhcpsrv', 'DEBUG', 99)
    srv_control.configure_loggers(f'kea-dhcp{world.proto[1]}.ha-hooks', 'DEBUG', 99)
    srv_control.configure_loggers('kea-ctrl-agent', 'DEBUG', 99, 'kea.log-CTRL2')

    load_hook_libraries(dhcp_version, hook_order)

    srv_control.update_ha_hook_parameter(HOT_STANDBY)
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
    wait_until_ha_state('hot-standby', dhcp_version=dhcp_version)

    # Message exchanges
    set_of_leases_1 = generate_leases(leases_count=50, dhcp_version=dhcp_version)

    # turn off server2
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)
    # dump leases and logs of server2
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)
    # start clean server2
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)
    # let's wait for full synchronization of server2
    wait_until_ha_state('hot-standby', dhcp_version=dhcp_version)

    # Check logs in server1.
    wait_for_message_in_log('HA_STATE_TRANSITION server1: server transitions from PARTNER-DOWN to '
                            'HOT-STANDBY state, partner state is READY')

    # Check logs in server2.
    wait_for_message_in_log('HA_LEASES_SYNC_LEASE_PAGE_RECEIVED server2: received 15 leases from '
                            'server1', 3, destination=world.f_cfg.mgmt_address_2)
    wait_for_message_in_log('HA_SYNC_SUCCESSFUL server2: lease database synchronization with '
                            'server1 completed successfully',
                            destination=world.f_cfg.mgmt_address_2)
    wait_for_message_in_log('HA_STATE_TRANSITION server2: server transitions from READY to '
                            'HOT-STANDBY state, partner state is HOT-STANDBY',
                            destination=world.f_cfg.mgmt_address_2)

    # check if all leases are synced
    srv_msg.check_leases(set_of_leases_1, dest=world.f_cfg.mgmt_address_2, backend=backend)
    # stop server1
    srv_control.start_srv('DHCP', 'stopped')
    # dump leases and logs from server1
    srv_control.clear_some_data('all')
    # let's wait until secondary system switch status, we don't need elapsed time increased
    # due to server settings
    wait_until_ha_state('partner-down', dest=world.f_cfg.mgmt_address_2, dhcp_version=dhcp_version)

    # create leases in HA 2
    set_of_leases_2 = generate_leases(leases_count=50, dhcp_version=dhcp_version,
                                      mac="02:02:0c:03:0a:00")

    # start server1
    srv_control.start_srv('DHCP', 'started')
    # let's wait for full synchronization of server2
    wait_until_ha_state('hot-standby', dhcp_version=dhcp_version)

    # Check logs in server1.
    wait_for_message_in_log('HA_LEASES_SYNC_LEASE_PAGE_RECEIVED server1: received 10 leases from '
                            'server2', 10)

    # Check synced leases.
    srv_msg.check_leases(set_of_leases_1, backend=backend)
    srv_msg.check_leases(set_of_leases_2, backend=backend)


@pytest.mark.v4_bootp
@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.ha
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('hook_order', ['alphabetical'])  # possible params:  'reverse'
def test_HA_passive_backup_sync(dhcp_version: str, backend: str, hook_order: str):
    """
    Check that Kea can synchronize leases between HA nodes in passive-backup mode.

    :param dhcp_version: v4 or v6, determined by pytest marks
    :param backend: the database backend to be used for leases
    :param hook_order: the order in which hooks are loaded: either alphabetical
    or reverse alphabetical. This is to test all order combinations for each set
    of two hook libraries after problems were found on one order of loading HA
    with leasequery.
    """

    # HA SERVER 1
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)
    if dhcp_version == 'v6':
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ffff')
        srv_control.config_srv_prefix('2001:db8:2::', 0, 48, 91)
    elif dhcp_version in ['v4', 'v4_bootp']:
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.200')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()

    load_hook_libraries(dhcp_version, hook_order)

    srv_control.update_ha_hook_parameter(PASSIVE_BACKUP)
    srv_control.update_ha_hook_parameter({"this-server-name": "server1"})

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
    elif dhcp_version in ['v4', 'v4_bootp']:
        srv_control.config_srv_subnet('192.168.50.0/24',
                                      '192.168.50.1-192.168.50.200',
                                      world.f_cfg.server2_iface)

    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address_2)

    load_hook_libraries(dhcp_version, hook_order)

    srv_control.update_ha_hook_parameter(PASSIVE_BACKUP)
    srv_control.update_ha_hook_parameter({"this-server-name": "server2"})
    world.dhcp_cfg['interfaces-config']['interfaces'] = [world.f_cfg.server2_iface]
    srv_control.build_and_send_config_files(dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    # Wait for the passive-backup state.
    wait_until_ha_state('passive-backup', dhcp_version=dhcp_version)

    # Message exchanges
    leases_count = 4
    set_of_leases_1 = generate_leases(leases_count=leases_count, iana=3, iapd=2, dhcp_version=dhcp_version)

    # Wait for sync.
    if world.proto == 'v4':
        wait_for_message_in_log(r'\[ { "result": 0, "text": "IPv4 lease added\." } \]', leases_count)
    else:
        # 5 IPv6 leases == 3 IA_NA + 2 IA_PD in each response
        wait_for_message_in_log(r'\[ { "result": 0, "text": "Bulk apply of 5 IPv6 leases completed\." } \]', leases_count)

    # check synced leases
    srv_msg.check_leases(set_of_leases_1, backend=backend)
    srv_msg.check_leases(set_of_leases_1, backend=backend, dest=world.f_cfg.mgmt_address_2)


# disabled, we know it fails due to design of HA load-balancing nothing will change here
# @pytest.mark.v4_bootp
@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.disabled
@pytest.mark.ha
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('hook_order', ['alphabetical'])  # possible params:  'reverse'
def test_HA_load_balancing_sync(dhcp_version: str, backend: str, hook_order: str):
    """
    Check that Kea can synchronize leases between HA nodes in load-balancing mode.

    :param dhcp_version: v4 or v6, determined by pytest marks
    :param backend: the database backend to be used for leases
    :param hook_order: the order in which hooks are loaded: either alphabetical
    or reverse alphabetical. This is to test all order combinations for each set
    of two hook libraries after problems were found on one order of loading HA
    with leasequery.
    """

    # HA SERVER 1
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)
    if dhcp_version == "v6":
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::5')
        world.dhcp_cfg["subnet6"][0]["pools"][0].update({"client-class": "HA_server1"})
        world.dhcp_cfg["subnet6"][0]["pools"].append({"pool": "2001:db8:1::100-2001:db8:1::110",
                                                      "client-class": "HA_server2"})
    else:
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.5')
        world.dhcp_cfg["subnet4"][0]["pools"][0].update({"client-class": "HA_server1"})
        world.dhcp_cfg["subnet4"][0]["pools"].append({"pool": "192.168.50.20-192.168.50.30",
                                                      "client-class": "HA_server2"})
    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address)

    load_hook_libraries(dhcp_version, hook_order)

    srv_control.update_ha_hook_parameter(LOAD_BALANCING)
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 100,
                                          "max-response-delay": 1500,
                                          "max-unacked-clients": 0,
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
                                      '2001:db8:1::1-2001:db8:1::5',
                                      world.f_cfg.server2_iface)
        world.dhcp_cfg["subnet6"][0]["pools"][0].update({"client-class": "HA_server1"})
        world.dhcp_cfg["subnet6"][0]["pools"].append({"pool": "2001:db8:1::100-2001:db8:1::110",
                                                      "client-class": "HA_server2"})
    else:
        srv_control.config_srv_subnet('192.168.50.0/24',
                                      '192.168.50.1-192.168.50.5',
                                      world.f_cfg.server2_iface)
        world.dhcp_cfg["subnet4"][0]["pools"][0].update({"client-class": "HA_server1"})
        world.dhcp_cfg["subnet4"][0]["pools"].append({"pool": "192.168.50.20-192.168.50.30",
                                                      "client-class": "HA_server2"})

    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address_2)

    load_hook_libraries(dhcp_version, hook_order)

    srv_control.update_ha_hook_parameter(LOAD_BALANCING)
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 100,
                                          "max-response-delay": 1500,
                                          "max-unacked-clients": 0,
                                          "this-server-name": "server2"})
    world.dhcp_cfg['interfaces-config']['interfaces'] = [world.f_cfg.server2_iface]
    srv_control.build_and_send_config_files(dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    # Wait for the load-balancing states.
    wait_until_ha_state('load-balancing', dhcp_version=dhcp_version)
    wait_until_ha_state('load-balancing', dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)

    misc.test_procedure()

    # get 10 leases
    set_of_leases_1 = generate_leases(leases_count=10, iana=1, iapd=0, dhcp_version=dhcp_version)

    # check if there are indeed saved
    srv_msg.check_leases(set_of_leases_1, backend=backend)
    # check if those were propagated to other system
    srv_msg.check_leases(set_of_leases_1, dest=world.f_cfg.mgmt_address_2, backend=backend)
    # turn off server2
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)
    # dump leases and logs of server2
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)
    # start clean server2
    wait_until_ha_state('partner-down', dhcp_version=dhcp_version)
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)
    # let's wait for full synchronization of server2
    wait_until_ha_state('load-balancing', dhcp_version=dhcp_version)
    # check leases on server2
    srv_msg.check_leases(set_of_leases_1, dest=world.f_cfg.mgmt_address_2, backend=backend)

    # turn off server1
    srv_control.start_srv('DHCP', 'stopped')
    # dump leases and logs of server2
    srv_control.clear_some_data('all')
    # start clean server1
    wait_until_ha_state('partner-down', dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'started')
    # let's wait for full synchronization of server1
    wait_until_ha_state('load-balancing', dhcp_version=dhcp_version)
    # check leases on server1
    srv_msg.check_leases(set_of_leases_1, backend=backend)


@pytest.mark.v4_bootp
@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.disabled
@pytest.mark.ha
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('hook_order', ['alphabetical'])  # possible params:  'reverse'
def test_HA_load_balancing_both_scopes_for_primary(dhcp_version: str, backend: str, hook_order: str):
    """
    Check that a primary load-balancing HA node can take all the traffic when
    the secondary HA node is offline.

    :param dhcp_version: v4 or v6, determined by pytest marks
    :param backend: the database backend to be used for leases
    :param hook_order: the order in which hooks are loaded: either alphabetical
    or reverse alphabetical. This is to test all order combinations for each set
    of two hook libraries after problems were found on one order of loading HA
    with leasequery.
    """

    # HA SERVER 1
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)
    if dhcp_version == "v6":
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::20')
        world.dhcp_cfg["subnet6"][0]["pools"][0].update({"client-class": "HA_server1"})
        world.dhcp_cfg["subnet6"][0]["pools"].append({"pool": "2001:db8:1::100-2001:db8:1::120",
                                                      "client-class": "HA_server2"})
    else:
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.20')
        world.dhcp_cfg["subnet4"][0]["pools"][0].update({"client-class": "HA_server1"})
        world.dhcp_cfg["subnet4"][0]["pools"].append({"pool": "192.168.50.100-192.168.50.120",
                                                      "client-class": "HA_server2"})
    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address)

    load_hook_libraries(dhcp_version, hook_order)

    srv_control.update_ha_hook_parameter(LOAD_BALANCING)
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 100,
                                          "max-response-delay": 1500,
                                          "max-unacked-clients": 2,
                                          "this-server-name": "server1"})

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # HA SERVER 2
    # we don't need it, server1 wont detect server2 and will go straight to partner-down

    # Wait for the partner-down state.
    resp = wait_until_ha_state('partner-down', dhcp_version=dhcp_version)

    assert "server2" in resp["arguments"]["scopes"]
    assert "server1" in resp["arguments"]["scopes"]
    misc.test_procedure()
    # Get 40 leases split from server1 and server2.
    l_count = 40
    set_of_leases_1 = generate_leases(leases_count=l_count, iana=1, iapd=0, dhcp_version=dhcp_version)
    assert l_count == len(set_of_leases_1), "Server didn't give us all leases it had configured"
    srv_msg.check_leases(set_of_leases_1)


@pytest.mark.v4_bootp
@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.disabled
@pytest.mark.ha
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('hook_order', ['alphabetical'])  # possible params:  'reverse'
def test_HA_load_balancing_both_scopes_for_secondary(dhcp_version: str, backend: str, hook_order: str):
    """
    Check that a secondary load-balancing HA node can take all the traffic when
    the primary HA node is offline.

    :param dhcp_version: v4 or v6, determined by pytest marks
    :param backend: the database backend to be used for leases
    :param hook_order: the order in which hooks are loaded: either aplhabetical
    or reverse alphabetical. This is to test all order combinations for each set
    of two hook libraries after problems were found on one order of loading HA
    with leasequery.
    """

    # HA SERVER 1
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)
    if dhcp_version == "v6":
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::20')
        world.dhcp_cfg["subnet6"][0]["pools"][0].update({"client-class": "HA_server1"})
        world.dhcp_cfg["subnet6"][0]["pools"].append({"pool": "2001:db8:1::100-2001:db8:1::120",
                                                      "client-class": "HA_server2"})
    else:
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.20')
        world.dhcp_cfg["subnet4"][0]["pools"][0].update({"client-class": "HA_server1"})
        world.dhcp_cfg["subnet4"][0]["pools"].append({"pool": "192.168.50.100-192.168.50.120",
                                                      "client-class": "HA_server2"})
    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address)

    load_hook_libraries(dhcp_version, hook_order)

    srv_control.update_ha_hook_parameter(LOAD_BALANCING)
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 100,
                                          "max-response-delay": 1500,
                                          "max-unacked-clients": 0,
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
                                      '2001:db8:1::1-2001:db8:1::20',
                                      world.f_cfg.server2_iface)
        world.dhcp_cfg["subnet6"][0]["pools"][0].update({"client-class": "HA_server1"})
        world.dhcp_cfg["subnet6"][0]["pools"].append({"pool": "2001:db8:1::100-2001:db8:1::120",
                                                      "client-class": "HA_server2"})
    else:
        srv_control.config_srv_subnet('192.168.50.0/24',
                                      '192.168.50.1-192.168.50.20',
                                      world.f_cfg.server2_iface)
        world.dhcp_cfg["subnet4"][0]["pools"][0].update({"client-class": "HA_server1"})
        world.dhcp_cfg["subnet4"][0]["pools"].append({"pool": "192.168.50.100-192.168.50.120",
                                                      "client-class": "HA_server2"})

    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address_2)

    load_hook_libraries(dhcp_version, hook_order)

    srv_control.update_ha_hook_parameter(LOAD_BALANCING)
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 100,
                                          "max-response-delay": 1500,
                                          "max-unacked-clients": 0,
                                          "this-server-name": "server2"})  # this is now secondary!
    world.dhcp_cfg['interfaces-config']['interfaces'] = [world.f_cfg.server2_iface]
    srv_control.build_and_send_config_files(dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    # Wait for the load-balancing states.
    wait_until_ha_state('load-balancing', dhcp_version=dhcp_version)
    wait_until_ha_state('load-balancing', dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)

    # kill server1 and wait for secondary to go partner-down
    srv_control.start_srv('DHCP', 'stopped')
    resp = wait_until_ha_state('partner-down', dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)
    assert "server2" in resp["arguments"]["scopes"]
    assert "server1" in resp["arguments"]["scopes"]
    misc.test_procedure()
    # Get 40 leases split from server1 and server2.
    l_count = 40
    set_of_leases_1 = generate_leases(leases_count=l_count, iana=1, iapd=0, dhcp_version=dhcp_version)
    assert l_count == len(set_of_leases_1), f'Server gave us {len(set_of_leases_1)} leases, we wanted {l_count}'
    srv_msg.check_leases(set_of_leases_1, dest=world.f_cfg.mgmt_address_2)


def _add_ha_pools(address_space_size: int):
    """
    Add pools for the usual HA traffic coming from generate_leases().

    :param address_space_size: the number of addresses to fit in each pool
    """

    # Start with 10 to avoid RADIUS pools which are below 10.
    last_octet = 10 + address_space_size

    v = world.proto[1]
    if world.proto == 'v4':
        if f'subnet{v}' in world.dhcp_cfg:
            srv_control.merge_in_subnet(
                {'subnet': '192.168.50.0/24'},
                {'pools': [{'pool': f'192.168.50.11 - 192.168.50.{last_octet}'}]})
        elif 'shared-networks' in world.dhcp_cfg:
            srv_control.merge_in_network_subnet(
                {'name': 'net-1'},
                {'subnet': '192.168.50.0/24'},
                {'pools': [{'pool': f'192.168.50.11 - 192.168.50.{last_octet}'}]})
    elif world.proto == 'v6':
        if f'subnet{v}' in world.dhcp_cfg:
            srv_control.merge_in_subnet(
                {'subnet': '2001:db8:50::/64'},
                {'pools': [{'pool': f'2001:db8:50::11 - 2001:db8:50::{last_octet:02x}'}]})
        elif 'shared-networks' in world.dhcp_cfg:
            srv_control.merge_in_network_subnet(
                {'name': 'net-1'},
                {'subnet': '2001:db8:50::/64'},
                {'pools': [{'pool': f'2001:db8:50::11 - 2001:db8:50::{last_octet:02x}'}]})


@pytest.mark.v4
@pytest.mark.v4_bootp
@pytest.mark.v6
@pytest.mark.ha
@pytest.mark.radius
@pytest.mark.parametrize('backend', ['memfile'])  # other possible parameters: 'mysql', 'postgresql'
@pytest.mark.parametrize('ha_mode', ['hot-standby', 'load-balancing', 'passive-backup'])
@pytest.mark.parametrize('hook_order', ['alphabetical'])  # other possible parameters: 'reverse'
@pytest.mark.parametrize('config_type', ['multiple-subnets'])  # other possible parameters: 'network'
@pytest.mark.parametrize('radius_reservation_in_pool', ['radius-reservation-in-pool'])  # other possible parameters: 'radius-reservation-outside-pool'
def test_HA_and_RADIUS(dhcp_version: str,
                       backend: str,
                       ha_mode: str,
                       hook_order: str,
                       config_type: str,
                       radius_reservation_in_pool: str):
    """
    Check that HA and RADIUS can work together.

    :param dhcp_version: the DHCP version being tested
    :param backend: the lease database backend type
    :param ha_mode: the HA mode: HS, LB or PB
    :param hook_order: the order in which hooks are loaded: either alphabetical
        or reverse alphabetical. This is to test all order combinations for each
        set of two hook libraries after problems were found in one case where HA
        and leasequery were loaded in a certain order.
    :param config_type: different configurations used in testing
    :param radius_reservation_in_pool: whether there is an existing pool in Kea that contains the
                                       lease reserved by RADIUS for the first client in this test
    """

    # Constants
    leases_count = 50
    starting_mac = '01:02:0c:03:0a:00'
    starting_mac_2 = '02:02:0c:03:0a:00'

    # ---- HA server1 ----
    misc.test_setup()
    srv_control.configure_multi_threading(False)
    # Clear data.
    srv_control.clear_some_data('all')

    # Setup the RADIUS server.
    # Start with 10 to avoid RADIUS pools which are below 10.
    radius.add_usual_reservations()
    last_octet = 10
    for mac in [starting_mac, starting_mac_2]:
        for _ in range(leases_count):
            last_octet = last_octet + 1
            mac = increase_mac(mac)
            radius.add_reservation(mac, [
                f'Framed-IP-Address = "192.168.50.{last_octet}"',
                f'Framed-IPv6-Address = "2001:db8:50::{last_octet:02x}"',
            ])
    radius.init_and_start_radius()

    # Configure RADIUS in Kea. Server also starts here which is an
    # unfortunate side effect, but we'll restart after finishing
    # configuration below.
    configs = radius.configurations()
    setup_server_with_radius(**configs[config_type])

    # Configure the backend.
    srv_control.define_temporary_lease_db_backend(backend)

    # Start kea-ctrl-agent and configure the control socket in Kea.
    srv_control.agent_control_channel()
    srv_control.open_control_channel()

    # Load necessary hook libraries.
    load_hook_libraries(dhcp_version, hook_order)

    # Configure HA.
    if ha_mode == 'hot-standby':
        srv_control.update_ha_hook_parameter(HOT_STANDBY)
    elif ha_mode == 'load-balancing':
        srv_control.update_ha_hook_parameter(LOAD_BALANCING)
    elif ha_mode == 'passive-backup':
        srv_control.update_ha_hook_parameter(PASSIVE_BACKUP)
    srv_control.update_ha_hook_parameter({'heartbeat-delay': 1000,
                                          'max-ack-delay': 100,
                                          'max-response-delay': 1500,
                                          'max-unacked-clients': 0,
                                          'sync-page-limit': 10,
                                          'this-server-name': 'server1'})

    # Add a leading subnet to test subnet reselection in RADIUS.
    radius.add_leading_subnet()

    # Add pools for the usual HA traffic coming from generate_leases().
    # Two times the lease count - one for each starting MAC
    _add_ha_pools(2 * leases_count)

    # Start Kea.
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # ---- HA server2 ----
    misc.test_setup()

    # Clear data.
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)

    # Setup the RADIUS server.
    # Start with 10 to avoid RADIUS pools which are below 10.
    radius.add_usual_reservations()
    last_octet = 10
    for mac in [starting_mac, starting_mac_2]:
        for _ in range(leases_count):
            last_octet = last_octet + 1
            mac = increase_mac(mac)
            radius.add_reservation(mac, [
                f'Framed-IP-Address = "192.168.50.{last_octet}"',
                f'Framed-IPv6-Address = "2001:db8:50::{last_octet:02x}"',
            ])
    radius.init_and_start_radius(destination=world.f_cfg.mgmt_address_2)

    # Configure RADIUS in Kea. Server also starts here which is an
    # unfortunate side effect, but we'll restart after finishing
    # configuration below.
    configs = radius.configurations(interface=world.f_cfg.server2_iface)
    setup_server_with_radius(destination=world.f_cfg.mgmt_address_2,
                             interface=world.f_cfg.server2_iface,
                             **configs[config_type])

    # Configure the backend.
    srv_control.define_temporary_lease_db_backend(backend)

    # Start kea-ctrl-agent and configure the control socket in Kea.
    srv_control.agent_control_channel(host_address=world.f_cfg.mgmt_address_2)
    srv_control.open_control_channel()

    # Load necessary hook libraries.
    load_hook_libraries(dhcp_version, hook_order)

    # Configure HA.
    if ha_mode == 'hot-standby':
        srv_control.update_ha_hook_parameter(HOT_STANDBY)
    elif ha_mode == 'load-balancing':
        srv_control.update_ha_hook_parameter(LOAD_BALANCING)
    elif ha_mode == 'passive-backup':
        srv_control.update_ha_hook_parameter(PASSIVE_BACKUP)
    srv_control.update_ha_hook_parameter({'heartbeat-delay': 1000,
                                          'max-ack-delay': 100,
                                          'max-response-delay': 1500,
                                          'max-unacked-clients': 0,
                                          'sync-page-limit': 15,
                                          'this-server-name': 'server2'})
    world.dhcp_cfg['interfaces-config']['interfaces'] = [world.f_cfg.server2_iface]

    # Add a leading subnet to test subnet reselection in RADIUS.
    radius.add_leading_subnet()

    # Add pools for the usual HA traffic coming from generate_leases().
    # Two times the lease count - one for each starting MAC
    _add_ha_pools(2 * leases_count)

    # Start Kea.
    srv_control.build_and_send_config_files(dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    # Settle was the HA state should be for server2 in normal functioning mode.
    ha_mode_2 = ha_mode
    if ha_mode == 'passive-backup':
        ha_mode_2 = 'backup'

    # ---- Start testing. ----

    # Wait for both servers to reach functioning states.
    wait_until_ha_state(ha_mode, dhcp_version=dhcp_version)
    wait_until_ha_state(ha_mode_2, dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)

    # Exchange some messages and make sure leases are given.
    set_of_leases = generate_leases(dhcp_version=dhcp_version,
                                    iapd=0,
                                    leases_count=leases_count,
                                    mac=starting_mac)

    # Check that both servers have all the leases in the backends.
    srv_msg.check_leases(set_of_leases, backend=backend, dest=world.f_cfg.mgmt_address)
    srv_msg.check_leases(set_of_leases, backend=backend, dest=world.f_cfg.mgmt_address_2)

    # Restart server2.
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    # Wait for both servers to reach functioning states.
    wait_until_ha_state(ha_mode, dhcp_version=dhcp_version)
    wait_until_ha_state(ha_mode_2, dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)

    # Check that both servers have all the leases in the backends.
    srv_msg.check_leases(set_of_leases, backend=backend, dest=world.f_cfg.mgmt_address)
    srv_msg.check_leases(set_of_leases, backend=backend, dest=world.f_cfg.mgmt_address_2)

    if ha_mode in ['hot-standby', 'load-balancing']:
        # Stop server1.
        srv_control.start_srv('DHCP', 'stopped')

        # Wait until server2 switches status.
        wait_until_ha_state('partner-down',
                            dest=world.f_cfg.mgmt_address_2,
                            dhcp_version=dhcp_version)

    # Exchange some more messages and make sure leases are given.
    set_of_leases_2 = generate_leases(dhcp_version=dhcp_version,
                                      iapd=0,
                                      leases_count=leases_count,
                                      mac=starting_mac_2)

    if ha_mode in ['hot-standby', 'load-balancing']:
        # Start server1.
        srv_control.start_srv('DHCP', 'started')

        # Wait for both servers to reach functioning states.
        wait_until_ha_state(ha_mode, dhcp_version=dhcp_version)
        wait_until_ha_state(ha_mode_2, dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)

    # Exchange some messages and make sure leases are given with clients that
    # are configured in RADIUS.
    radius_leases = radius.send_and_receive(config_type, radius_reservation_in_pool, ha_mode)

    # Check that both servers have all the leases in the backends.
    for leases in [set_of_leases, set_of_leases_2, radius_leases]:
        for dest in [world.f_cfg.mgmt_address, world.f_cfg.mgmt_address_2]:
            srv_msg.check_leases(leases, backend=backend, dest=dest)


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.ha
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('hook_order', ['alphabetical'])  # possible params:  'reverse'
def test_HA_hot_standby_ha_sync_command(dhcp_version: str, backend: str, hook_order: str):
    """
    Check that the HA sync command works in hot-standby mode.
    Test runs two Kea servers in hot-standby mode. Than a set of leases is generated.
    It is removed from the second server. Second set of leases is generated and removed.
    ha-sync is run and the leases are checked on both servers.

    :param dhcp_version: v4 or v6, determined by pytest marks
    :param backend: the database backend to be used for leases
    :param hook_order: the order in which hooks are loaded: either alphabetical
    or reverse alphabetical. This is to test all order combinations for each set
    of two hook libraries after problems were found on one order of loading HA
    with leasequery.
    """

    # HA SERVER 1
    misc.test_setup()

    srv_control.define_temporary_lease_db_backend(backend)

    if dhcp_version == 'v6':
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ffff')
    elif dhcp_version in ['v4']:
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.200')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.configure_loggers(f'kea-dhcp{world.proto[1]}.dhcpsrv', 'DEBUG', 99)
    srv_control.configure_loggers(f'kea-dhcp{world.proto[1]}.ha-hooks', 'DEBUG', 99)
    srv_control.configure_loggers('kea-ctrl-agent', 'DEBUG', 99, 'kea.log-CTRL')

    load_hook_libraries(dhcp_version, hook_order)

    srv_control.update_ha_hook_parameter(HOT_STANDBY)
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
                                      world.f_cfg.server2_iface)
    elif dhcp_version in ['v4', 'v4_bootp']:
        srv_control.config_srv_subnet('192.168.50.0/24',
                                      '192.168.50.1-192.168.50.200',
                                      world.f_cfg.server2_iface)

    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address_2)
    srv_control.configure_loggers(f'kea-dhcp{world.proto[1]}.dhcpsrv', 'DEBUG', 99)
    srv_control.configure_loggers(f'kea-dhcp{world.proto[1]}.ha-hooks', 'DEBUG', 99)
    srv_control.configure_loggers('kea-ctrl-agent', 'DEBUG', 99, 'kea.log-CTRL2')

    load_hook_libraries(dhcp_version, hook_order)

    srv_control.update_ha_hook_parameter(HOT_STANDBY)
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
    wait_until_ha_state('hot-standby', dhcp_version=dhcp_version)

    # Message exchanges
    set_of_leases_1 = generate_leases(leases_count=20, dhcp_version=dhcp_version)

    # dump leases of server2

    if backend == 'memfile':
        srv_msg.send_ctrl_cmd({
            "command": f'lease{dhcp_version[1]}-wipe',
            "arguments": {
                "subnets": [1]
            }
        }, channel='http', address=world.f_cfg.mgmt_address_2, exp_result=0)
        srv_msg.send_ctrl_cmd({
            "command": "leases-reclaim",
            "arguments": {
                "remove": True,
            }
        }, channel='http', address=world.f_cfg.mgmt_address_2, exp_result=0)
        fabric_sudo_command(f'> {world.f_cfg.get_leases_path()}', world.f_cfg.mgmt_address_2)
    else:
        srv_control.clear_some_data('leases', dest=world.f_cfg.mgmt_address_2)

    # check if we deleted leases from second server
    srv_msg.check_leases(set_of_leases_1, backend=backend)
    srv_msg.check_leases(set_of_leases_1, dest=world.f_cfg.mgmt_address_2, backend=backend, should_succeed=False)
    srv_msg.send_ctrl_cmd({
            "command": f'lease{dhcp_version[1]}-get-all',
            "arguments": {
                "subnets": [1]
            }
        }, channel='http', address=world.f_cfg.mgmt_address_2, exp_result=3)

    # create new set of leases
    set_of_leases_2 = generate_leases(leases_count=20, dhcp_version=dhcp_version,
                                      mac="02:02:0c:03:0a:00")

    # Verify that second server has only second set of leases.
    srv_msg.check_leases(set_of_leases_1, dest=world.f_cfg.mgmt_address_2, backend=backend, should_succeed=False)
    srv_msg.check_leases(set_of_leases_2, backend=backend, dest=world.f_cfg.mgmt_address_2)

    # Send ha-sync command to server2
    response = srv_msg.send_ctrl_cmd({
        "command": "ha-sync",
        "arguments": {
            "server-name": "server1",
            "max-period": 60
        }
        }, channel='http', address=world.f_cfg.mgmt_address_2, exp_result=0)
    assert response == {
        'result': 0,
        'text': "Lease database synchronization complete."
    }

    # Check synced leases.
    srv_msg.check_leases(set_of_leases_1, dest=world.f_cfg.mgmt_address_2, backend=backend)
    srv_msg.check_leases(set_of_leases_2, backend=backend, dest=world.f_cfg.mgmt_address_2)
