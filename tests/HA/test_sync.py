"""Kea HA syncing"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_control
import srv_msg

from forge_cfg import world
from HA.steps import generate_leases, load_hook_libraries, wait_until_ha_state
from HA.steps import HOT_STANDBY, LOAD_BALANCING, PASSIVE_BACKUP

# TODO add checking logs in all those tests


@pytest.fixture(autouse=True)
def kill_kea_on_second_system():
    # kill kea and clear data at the beginning and at the end
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)
    yield
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)


@pytest.mark.v6
@pytest.mark.HA
@pytest.mark.parametrize('hook_order', ['alphabetical', 'reverse'])
def test_v6_hooks_HA_page_size_sync_mulitple_NA(hook_order):
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
                                          "max-ack-delay": 0,
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
                                          "max-ack-delay": 0,
                                          "max-response-delay": 1500,
                                          "max-unacked-clients": 0,
                                          'sync-page-limit': 2,
                                          "this-server-name": "server2"})
    world.dhcp_cfg['interfaces-config']['interfaces'] = [world.f_cfg.server2_iface]
    srv_control.build_and_send_config_files(dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    wait_until_ha_state('hot-standby')
    misc.test_procedure()

    set_of_leases_1 = generate_leases(leases_count=5, iaid=3, iapd=2)
    srv_msg.check_leases(set_of_leases_1)
    srv_msg.check_leases(set_of_leases_1, dest=world.f_cfg.mgmt_address_2)
    # srv_msg.forge_sleep(2, 'seconds')

    # srv_msg.remote_log_includes_line(world.f_cfg.mgmt_address_2,
    #                                  '$(SOFTWARE_INSTALL_DIR)/var/log/kea.log-CA',
    #                                  None,
    #                                  'Bulk apply of 4 IPv6 leases completed.')
    srv_control.start_srv('DHCP', 'stopped')
    wait_until_ha_state('partner-down', dest=world.f_cfg.mgmt_address_2)

    set_of_leases_2 = generate_leases(leases_count=5, iaid=3, iapd=2, mac="02:02:0c:03:0a:00")

    srv_control.start_srv('DHCP', 'started')
    wait_until_ha_state('hot-standby')

    srv_msg.check_leases(set_of_leases_1)
    srv_msg.check_leases(set_of_leases_2)


@pytest.mark.v4_bootp
@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.HA
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('hook_order', ['alphabetical', 'reverse'])
def test_HA_hot_standby_different_page_size_sync(dhcp_version, backend, hook_order):
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)
    # we have to clear data on second system, before test forge does not know that we have multiple systems
    if dhcp_version == 'v6':
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ffff')
    elif dhcp_version in ['v4', 'v4_bootp']:
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.200')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.configure_loggers('kea-dhcp6.dhcpsrv', 'DEBUG', 99)
    srv_control.configure_loggers('kea-dhcp6.ha-hooks', 'DEBUG', 99)
    srv_control.configure_loggers('kea-ctrl-agent', 'DEBUG', 99, 'kea.log-CTRL')

    load_hook_libraries(dhcp_version, hook_order)

    srv_control.update_ha_hook_parameter(HOT_STANDBY)
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 0,
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
    srv_control.configure_loggers('kea-dhcp6.dhcpsrv', 'DEBUG', 99)
    srv_control.configure_loggers('kea-dhcp6.ha-hooks', 'DEBUG', 99)
    srv_control.configure_loggers('kea-ctrl-agent', 'DEBUG', 99, 'kea.log-CTRL2')

    load_hook_libraries(dhcp_version, hook_order)

    srv_control.update_ha_hook_parameter(HOT_STANDBY)
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 0,
                                          "max-response-delay": 1500,
                                          "max-unacked-clients": 0,
                                          "sync-page-limit": 15,
                                          "this-server-name": "server2"})
    world.dhcp_cfg['interfaces-config']['interfaces'] = [world.f_cfg.server2_iface]
    srv_control.build_and_send_config_files(dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    wait_until_ha_state('hot-standby', dhcp_version=dhcp_version)
    set_of_leases_1 = generate_leases(leases_count=50, iaid=1, iapd=1, dhcp_version=dhcp_version)

    # turn off server2
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)
    # dump leases and logs of server2
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)
    # start clean server2
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)
    # let's wait for full synchronization of server2
    wait_until_ha_state('hot-standby', sleep=2, dhcp_version=dhcp_version)

    # misc.pass_criteria()
    # if dhcp_version == 'v6':
    #     srv_msg.log_contains('DHCPSRV_MEMFILE_GET_PAGE6 obtaining at most 15 IPv6 leases starting')
    #     srv_msg.remote_log_includes_line(world.f_cfg.mgmt_address_2,
    #                                      '$(SOFTWARE_INSTALL_DIR)/var/log/kea.log',
    #                                      None,
    #                                      'HA_LEASES_SYNC_LEASE_PAGE_RECEIVED received 15 leases from server1')
    #     srv_msg.remote_log_includes_line(world.f_cfg.mgmt_address_2,
    #                                      '$(SOFTWARE_INSTALL_DIR)/var/log/kea.log',
    #                                      'NOT ',
    #                                      'DHCPSRV_MEMFILE_GET_PAGE6 obtaining at most 10 IPv6 leases starting from address 2001:')
    #     srv_msg.log_doesnt_contain('HA_LEASES_SYNC_LEASE_PAGE_RECEIVED received 10 leases from')
    #     srv_msg.remote_log_includes_line(world.f_cfg.mgmt_address_2,
    #                                      '$(SOFTWARE_INSTALL_DIR)/var/log/kea.log',
    #                                      None,
    #                                      'HA_SYNC_SUCCESSFUL lease database synchronization with server1 completed successfully')
    # else:
    #     srv_msg.log_contains('DHCPSRV_MEMFILE_GET_PAGE4 obtaining at most 15 IPv4 leases starting')
    #     srv_msg.remote_log_includes_line(world.f_cfg.mgmt_address_2,
    #                                      '$(SOFTWARE_INSTALL_DIR)/var/log/kea.log',
    #                                      None,
    #                                      'HA_LEASES_SYNC_LEASE_PAGE_RECEIVED received 15 leases from server1')
    #     srv_msg.remote_log_includes_line(world.f_cfg.mgmt_address_2,
    #                                      '$(SOFTWARE_INSTALL_DIR)/var/log/kea.log',
    #                                      'NOT ',
    #                                      'DHCPSRV_MEMFILE_GET_PAGE6 obtaining at most 10 IPv4 leases starting from address =')
    #     srv_msg.log_doesnt_contain('HA_LEASES_SYNC_LEASE_PAGE_RECEIVED received 10 leases from')
    #     srv_msg.remote_log_includes_line(world.f_cfg.mgmt_address_2,
    #                                      '$(SOFTWARE_INSTALL_DIR)/var/log/kea.log',
    #                                      None,
    #                                      'HA_SYNC_SUCCESSFUL lease database synchronization with server1 completed successfully')

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
    set_of_leases_2 = generate_leases(leases_count=50, iaid=1, iapd=1, dhcp_version=dhcp_version,
                                      mac="02:02:0c:03:0a:00")

    # start server1
    srv_control.start_srv('DHCP', 'started')
    # let's wait for full synchronization of server2
    wait_until_ha_state('hot-standby', sleep=2, dhcp_version=dhcp_version)

    # check synced leaases
    srv_msg.check_leases(set_of_leases_1, backend=backend)
    srv_msg.check_leases(set_of_leases_2, backend=backend)


@pytest.mark.v4_bootp
@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.HA
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('hook_order', ['alphabetical', 'reverse'])
def test_HA_passive_backup_sync(dhcp_version, backend, hook_order):
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)
    if dhcp_version == 'v6':
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ffff')
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

    wait_until_ha_state('passive-backup', dhcp_version=dhcp_version)
    set_of_leases_1 = generate_leases(leases_count=5, iaid=3, iapd=2, dhcp_version=dhcp_version)
    # we have no confirmation in syncing so just let's wait a bit
    srv_msg.forge_sleep(2, 'seconds')
    # check synced leases
    srv_msg.check_leases(set_of_leases_1, backend=backend)
    srv_msg.check_leases(set_of_leases_1, backend=backend, dest=world.f_cfg.mgmt_address_2)


# disabled, we know it fails due to design of HA load-balancing nothing will change here
@pytest.mark.v4_bootp
@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.disabled
@pytest.mark.HA
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('hook_order', ['alphabetical', 'reverse'])
def test_HA_load_balancing_sync(dhcp_version, backend, hook_order):
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
                                          "max-ack-delay": 0,
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
                                          "max-ack-delay": 0,
                                          "max-response-delay": 1500,
                                          "max-unacked-clients": 0,
                                          "this-server-name": "server2"})
    world.dhcp_cfg['interfaces-config']['interfaces'] = [world.f_cfg.server2_iface]
    srv_control.build_and_send_config_files(dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    wait_until_ha_state('load-balancing', dhcp_version=dhcp_version)
    wait_until_ha_state('load-balancing', dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)

    misc.test_procedure()
    # get 10 leases
    set_of_leases_1 = generate_leases(leases_count=10, iaid=1, iapd=0, dhcp_version=dhcp_version)

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
    wait_until_ha_state('load-balancing', sleep=2, dhcp_version=dhcp_version)
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
    wait_until_ha_state('load-balancing', sleep=2, dhcp_version=dhcp_version)
    # check leases on server1
    srv_msg.check_leases(set_of_leases_1, backend=backend)


@pytest.mark.v4_bootp
@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.disabled
@pytest.mark.HA
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('hook_order', ['alphabetical', 'reverse'])
def test_HA_load_balancing_both_scopes_for_primary(dhcp_version, backend, hook_order):
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

    resp = wait_until_ha_state('partner-down', dhcp_version=dhcp_version)
    # wait_until_ha_state('load-balancing', dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)
    assert "server2" in resp["arguments"]["scopes"]
    assert "server1" in resp["arguments"]["scopes"]
    misc.test_procedure()
    # get 10 leases some form server1 and some from server2
    l_count = 40
    set_of_leases_1 = generate_leases(leases_count=l_count, iaid=1, iapd=0, dhcp_version=dhcp_version)
    assert l_count == len(set_of_leases_1), "Server didn't give us all leases it had configured"
    srv_msg.check_leases(set_of_leases_1)


@pytest.mark.v4_bootp
@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.disabled
@pytest.mark.HA
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('hook_order', ['alphabetical', 'reverse'])
def test_HA_load_balancing_both_scopes_for_secondary(dhcp_version, backend, hook_order):
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
                                          "max-ack-delay": 0,
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
                                          "max-ack-delay": 0,
                                          "max-response-delay": 1500,
                                          "max-unacked-clients": 0,
                                          "this-server-name": "server2"})  # this is now secondary!
    world.dhcp_cfg['interfaces-config']['interfaces'] = [world.f_cfg.server2_iface]
    srv_control.build_and_send_config_files(dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    wait_until_ha_state('load-balancing', dhcp_version=dhcp_version)
    wait_until_ha_state('load-balancing', dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)

    # kill server1 and wait for secondary to go partner-down
    srv_control.start_srv('DHCP', 'stopped')
    resp = wait_until_ha_state('partner-down', dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2)
    assert "server2" in resp["arguments"]["scopes"]
    assert "server1" in resp["arguments"]["scopes"]
    misc.test_procedure()
    # get 10 leases some form server1 and some from server2
    l_count = 40
    set_of_leases_1 = generate_leases(leases_count=l_count, iaid=1, iapd=0, dhcp_version=dhcp_version)
    assert l_count == len(set_of_leases_1), "Server gave us %d leases, we wanted %d" % (len(set_of_leases_1), l_count)
    srv_msg.check_leases(set_of_leases_1, dest=world.f_cfg.mgmt_address_2)
