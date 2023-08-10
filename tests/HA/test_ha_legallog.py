# Copyright (C) 2022 Internet Systems Consortium.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Marcin Godzina

"""Kea HA Legal Log tests"""

import pytest

from src import misc
from src import srv_control
from src import srv_msg

from src.forge_cfg import world
from src.protosupport.multi_protocol_functions import file_contains_line
from .steps import get_status_HA, wait_until_ha_state

HA_CONFIG = {
    "mode": "hot-standby",
    "peers": [{
        "auto-failover": True,
        "name": "server1",
        "role": "primary",
        "url": f"http://{world.f_cfg.mgmt_address}:8000/"
    }, {
        "auto-failover": True,
        "name": "server2",
        "role": "standby",
        "url": f"http://{world.f_cfg.mgmt_address_2}:8000/"
    }],
    "state-machine": {
        "states": []
    }
}


def _save_log_files():
    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'), local_filename='server1_kea-legal.txt',
                        dest=world.f_cfg.mgmt_address)
    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'), local_filename='server2_kea-legal.txt',
                        dest=world.f_cfg.mgmt_address_2)


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.ha
@pytest.mark.legal_logging
@pytest.mark.parametrize('backend', ['file', 'mysql', 'postgresql'])
def test_ha_legallog(dhcp_version, backend):
    """
    Test if both HA servers log proper messages in Legal Log.
    """
    # HA SERVER 1
    misc.test_setup()
    if backend == 'file':
        srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'), dest=world.f_cfg.mgmt_address)
    else:
        srv_msg.remove_from_db_table('logs', backend, destination=world.f_cfg.mgmt_address)
    if dhcp_version == 'v6':
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::100')
        srv_control.config_srv_prefix('2001:db8:2::', 0, 48, 91)
        srv_control.config_srv_id('LLT', '00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8')
    else:
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.200')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(MGMT_ADDRESS)')

    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_ha_hook('libdhcp_ha.so')
    srv_control.add_hooks('libdhcp_legal_log.so')
    if backend != 'file':
        srv_control.add_parameter_to_hook(3, 'name', '$(DB_NAME)')
        srv_control.add_parameter_to_hook(3, 'password', '$(DB_PASSWD)')
        srv_control.add_parameter_to_hook(3, 'type', backend)
        srv_control.add_parameter_to_hook(3, 'user', '$(DB_USER)')

    # Configure HA hook to use TLS.
    srv_control.update_ha_hook_parameter(HA_CONFIG)
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 100,
                                          "max-response-delay": 1500,
                                          "max-unacked-clients": 4,
                                          "this-server-name": "server1",
                                          })

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # HA SERVER 2
    misc.test_setup()
    if backend == 'file':
        srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'), dest=world.f_cfg.mgmt_address_2)
    else:
        srv_msg.remove_from_db_table('logs', backend, destination=world.f_cfg.mgmt_address_2)
    if dhcp_version == 'v6':
        srv_control.config_srv_subnet('2001:db8:1::/64',
                                      '2001:db8:1::1-2001:db8:1::100',
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
    srv_control.add_hooks('libdhcp_legal_log.so')
    if backend != 'file':
        srv_control.add_parameter_to_hook(3, 'name', '$(DB_NAME)')
        srv_control.add_parameter_to_hook(3, 'password', '$(DB_PASSWD)')
        srv_control.add_parameter_to_hook(3, 'type', backend)
        srv_control.add_parameter_to_hook(3, 'user', '$(DB_USER)')

    srv_control.update_ha_hook_parameter(HA_CONFIG)
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 100,
                                          "max-response-delay": 1500,
                                          "max-unacked-clients": 4,
                                          "this-server-name": "server2",
                                          })

    world.dhcp_cfg['interfaces-config']['interfaces'] = [world.f_cfg.server2_iface]
    srv_control.build_and_send_config_files(dest=world.f_cfg.mgmt_address_2)

    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    # Wait for HA pair to communicate
    wait_until_ha_state('hot-standby', dhcp_version=dhcp_version, channel='http')
    wait_until_ha_state('hot-standby', dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2, channel='http')

    # Check if desired status is met.
    get_status_HA(True, True, ha_mode='hot-standby', primary_state='hot-standby', secondary_state='hot-standby',
                  primary_role='primary', secondary_role='standby',
                  primary_scopes=['server1'], secondary_scopes=[],
                  comm_interrupt=False, in_touch=True, channel='http')

    # Acquire a lese and check it in both backends.
    if dhcp_version == 'v6':
        srv_msg.SARR(address='2001:db8:1::1', duid='00:03:00:01:66:55:44:33:22:11')
        srv_msg.check_leases(srv_msg.get_all_leases())
        srv_msg.check_leases(srv_msg.get_all_leases(),
                             dest=world.f_cfg.mgmt_address_2)
        message1 = 'Address: 2001:db8:1::1 has been assigned for 1 hrs 6 mins 40 secs to a device with ' \
                   'DUID: 00:03:00:01:66:55:44:33:22:11 and hardware address: ' \
                   'hwtype=1 66:55:44:33:22:11 (from DUID)'
        message2 = 'HA partner updated information on the lease of address: 2001:db8:1::1 to a device with ' \
                   'DUID: 00:03:00:01:66:55:44:33:22:11 and hardware address: ' \
                   'hardware address: hwtype=1 66:55:44:33:22:11 (from DUID) for 1 hrs 6 mins 40 secs'
        if backend == 'file':
            _save_log_files()
            file_contains_line(world.f_cfg.data_join('kea-legal*.txt'),
                               message1, destination=world.f_cfg.mgmt_address)
            file_contains_line(world.f_cfg.data_join('kea-legal*.txt'),
                               message2, destination=world.f_cfg.mgmt_address_2)
        else:
            srv_msg.table_contains_line_n_times('logs', backend, 1,
                                                message1, destination=world.f_cfg.mgmt_address)
            srv_msg.table_contains_line_n_times('logs', backend, 1,
                                                message2, destination=world.f_cfg.mgmt_address)

    else:
        srv_msg.DORA('192.168.50.1')
        srv_msg.check_leases(srv_msg.get_all_leases())
        srv_msg.check_leases(srv_msg.get_all_leases(), dest=world.f_cfg.mgmt_address_2)
        message1 = 'Address: 192.168.50.1 has been assigned for 1 hrs 6 mins 40 secs to a device with hardware ' \
                   'address: hwtype=1 ff:01:02:03:ff:04'
        message2 = 'HA partner updated information on the lease of address: 192.168.50.1 to a device with ' \
                   'hardware address: ff:01:02:03:ff:04 for 1 hrs 6 mins 40 secs'
        if backend == 'file':
            _save_log_files()
            file_contains_line(world.f_cfg.data_join('kea-legal*.txt'),
                               message1, destination=world.f_cfg.mgmt_address)
            file_contains_line(world.f_cfg.data_join('kea-legal*.txt'),
                               message2, destination=world.f_cfg.mgmt_address_2)
        else:
            srv_msg.table_contains_line_n_times('logs', backend, 1,
                                                message1, destination=world.f_cfg.mgmt_address)
            srv_msg.table_contains_line_n_times('logs', backend, 1,
                                                message2, destination=world.f_cfg.mgmt_address)
