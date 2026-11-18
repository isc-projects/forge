# Copyright (C) 2026 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea HA basic authentication"""

# pylint: disable=invalid-name
# pylint: disable=line-too-long

import copy
import os
import pytest

from src import misc
from src import srv_control
from src import srv_msg

from src.forge_cfg import world
from .steps import wait_until_ha_state, send_heartbeat, generate_leases
from .steps import HOT_STANDBY, LOAD_BALANCING, PASSIVE_BACKUP


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
@pytest.mark.parametrize('backend', ['memfile'])
@pytest.mark.parametrize('mode', ['load-balancing', 'hot-standby', 'passive-backup'])
@pytest.mark.parametrize('auth_location', ['config', 'file'])
def test_HA_basic_authentication(dhcp_version: str, backend: str, mode: str, auth_location: str):
    """Check that Kea can authenticate with basic authentication with user and password in Kea config file or separate files.
    Used configure parameters is basic-auth-user and basic-auth-password or basic-auth-user-file and basic-auth-password-file.
    :param dhcp_version: v4 or v6, determined by pytest marks
    :param backend: the database backend to be used for leases
    :param mode: the HA mode to be used in test.
    :param auth_location: the location of the authentication file or in Kea configuration.
    """
    config = {'load-balancing': LOAD_BALANCING, 'hot-standby': HOT_STANDBY, 'passive-backup': PASSIVE_BACKUP}

    # HA SERVER 1
    misc.test_setup()

    srv_control.define_lease_db_backend(backend)

    # we have to clear data on second system, before test forge does not know that we have multiple systems
    if dhcp_version == 'v6':
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ffff', id=1)
    elif dhcp_version in ['v4', 'v4_bootp']:
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.200', id=1)
    # srv_control.add_unix_socket()
    # srv_control.add_http_control_channel()
    srv_control.configure_loggers(f'kea-dhcp{world.proto[1]}.dhcpsrv', 'DEBUG', 99)
    srv_control.configure_loggers(f'kea-dhcp{world.proto[1]}.ha-hooks', 'DEBUG', 99)

    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_hooks('libdhcp_ha.so')
    if dhcp_version == 'v4_bootp':
        srv_control.add_hooks('libdhcp_bootp.so')

    srv_control.update_ha_hook_parameter(copy.deepcopy(config[mode]))  # copy to avoid modifying the original dictionary
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 100,
                                          "max-response-delay": 1500,
                                          "max-unacked-clients": 0,
                                          "sync-page-limit": 10,
                                          "this-server-name": "server1"})
    if auth_location == 'config':
        srv_control.add_parameter_to_ha_hook("peers", {"basic-auth-user": "superAdmin_HA",
                                                       "basic-auth-password": "difficultPassword_HA"},
                                             relationship=0)
    elif auth_location == 'file':
        user_file = os.path.join(world.f_cfg.get_share_path(), "kea-creds", "superAdmin_HA")
        password_file = os.path.join(world.f_cfg.get_share_path(), "kea-creds", "superAdmin_HA_password")
        srv_control.create_user_and_password_file("superAdmin_HA", "difficultPassword_HA")
        srv_control.add_parameter_to_ha_hook("peers", {"basic-auth-user-file": user_file,
                                                       "basic-auth-password-file": password_file},
                                             relationship=0)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # HA SERVER 2
    misc.test_setup()

    srv_control.define_lease_db_backend(backend)
    # we have to clear data on second system, before test forge does not know that we have multiple systems
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)

    if dhcp_version == 'v6':
        srv_control.config_srv_subnet('2001:db8:1::/64',
                                      '2001:db8:1::1-2001:db8:1::ffff',
                                      world.f_cfg.server2_iface, id=1)
    else:
        srv_control.config_srv_subnet('192.168.50.0/24',
                                      '192.168.50.1-192.168.50.200',
                                      world.f_cfg.server2_iface, id=1)

    # srv_control.add_unix_socket()
    # srv_control.add_http_control_channel(world.f_cfg.mgmt_address_2)
    srv_control.configure_loggers(f'kea-dhcp{world.proto[1]}.dhcpsrv', 'DEBUG', 99)
    srv_control.configure_loggers(f'kea-dhcp{world.proto[1]}.ha-hooks', 'DEBUG', 99)

    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_hooks('libdhcp_ha.so')
    if dhcp_version == 'v4_bootp':
        srv_control.add_hooks('libdhcp_bootp.so')

    srv_control.update_ha_hook_parameter(copy.deepcopy(config[mode]))  # copy to avoid modifying the original dictionary
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 100,
                                          "max-response-delay": 1500,
                                          "max-unacked-clients": 0,
                                          "sync-page-limit": 15,
                                          "this-server-name": "server2"})
    if auth_location == 'config':
        srv_control.add_parameter_to_ha_hook("peers", {"basic-auth-user": "superAdmin_HA",
                                                       "basic-auth-password": "difficultPassword_HA"},
                                             relationship=0)
    elif auth_location == 'file':
        user_file = os.path.join(world.f_cfg.get_share_path(), "kea-creds", "superAdmin_HA")
        password_file = os.path.join(world.f_cfg.get_share_path(), "kea-creds", "superAdmin_HA_password")
        srv_control.create_user_and_password_file("superAdmin_HA", "difficultPassword_HA", dest=world.f_cfg.mgmt_address_2)
        srv_control.add_parameter_to_ha_hook("peers", {"basic-auth-user-file": user_file,
                                                       "basic-auth-password-file": password_file},
                                             relationship=0)

    world.dhcp_cfg['interfaces-config']['interfaces'] = [world.f_cfg.server2_iface]
    srv_control.build_and_send_config_files(dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    # wait for established configuration, this will show that communication between servers is established and working.
    # and access using correct authentication credentials is working.
    wait_until_ha_state(mode, dest=world.f_cfg.mgmt_address, dhcp_version=dhcp_version,
                        port=8003, auth="superAdmin_HA:difficultPassword_HA")
    ha_mode_2 = mode
    if mode == 'passive-backup':
        ha_mode_2 = 'backup'
    wait_until_ha_state(ha_mode_2, dest=world.f_cfg.mgmt_address_2, dhcp_version=dhcp_version,
                        port=8003, auth="superAdmin_HA:difficultPassword_HA")

    # now let's get some leases and if those are synced to both systems
    # in this case we will check that syncing leases with credentials is working.
    set_of_leases_1 = generate_leases(leases_count=5, dhcp_version=dhcp_version)
    srv_msg.check_leases(set_of_leases_1, dest=world.f_cfg.mgmt_address, backend=backend)
    srv_msg.check_leases(set_of_leases_1, dest=world.f_cfg.mgmt_address_2, backend=backend)

    # let's send heartbeats to both servers with missing or incorrect credentials
    send_heartbeat(dest=world.f_cfg.mgmt_address, port=8003, exp_result=401, auth="a:b")
    send_heartbeat(dest=world.f_cfg.mgmt_address_2, port=8003, exp_result=401, auth="c:d")

    send_heartbeat(dest=world.f_cfg.mgmt_address, port=8003, exp_result=401)
    send_heartbeat(dest=world.f_cfg.mgmt_address_2, port=8003, exp_result=401)

    # and now send correct credentials to both servers to not finish the test with an error.
    send_heartbeat(dest=world.f_cfg.mgmt_address, port=8003, auth="superAdmin_HA:difficultPassword_HA")
    send_heartbeat(dest=world.f_cfg.mgmt_address_2, port=8003, auth="superAdmin_HA:difficultPassword_HA")
