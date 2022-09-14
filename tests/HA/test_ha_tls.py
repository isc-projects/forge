# Copyright (C) 2022 Internet Systems Consortium.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Marcin Godzina

"""Kea HA TLS connection tests"""

import pytest

from src import misc
from src import srv_control
from src import srv_msg

from src.forge_cfg import world
from src.softwaresupport.multi_server_functions import fabric_send_file
from .steps import get_status_HA, wait_until_ha_state

HA_CONFIG = {
    "mode": "hot-standby",
    "peers": [{
        "auto-failover": True,
        "name": "server1",
        "role": "primary",
        "url": f"https://{world.f_cfg.mgmt_address}:8000/"
    }, {
        "auto-failover": True,
        "name": "server2",
        "role": "standby",
        "url": f"https://{world.f_cfg.mgmt_address_2}:8000/"
    }],
    "state-machine": {
        "states": []
    }
}


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
def test_ha_tls_with_ca(dhcp_version, backend):
    """
    Basic test of TLS functionality in HA Setup with Control Agent.
    Test generates certificate for both HA peers and their Control Agent.
    We check for hot-standby HA status after server start and then try top get a lease
    and check both databases for it.
    If status is acquired and lease is propagated to both backends
    we can assume TLS connection is working.
    """
    # HA SERVER 1
    # Create certificates.
    certificate = srv_control.generate_certificate()
    ca_cert = certificate.download('ca_cert')
    server_cert = certificate.download('server_cert')
    server_key = certificate.download('server_key')
    server2_cert = certificate.download('server2_cert')
    server2_key = certificate.download('server2_key')

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
    # Configure Control Agent to use TLS.
    world.ca_cfg["Control-agent"]["trust-anchor"] = certificate.ca_cert
    world.ca_cfg["Control-agent"]["cert-file"] = certificate.server_cert
    world.ca_cfg["Control-agent"]["key-file"] = certificate.server_key
    world.ca_cfg["Control-agent"]["cert-required"] = False

    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_ha_hook('libdhcp_ha.so')

    # Configure HA hook to use TLS.
    srv_control.update_ha_hook_parameter(HA_CONFIG)
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 100,
                                          "max-response-delay": 1500,
                                          "max-unacked-clients": 4,
                                          "this-server-name": "server1",
                                          "trust-anchor": certificate.ca_cert,
                                          "cert-file": certificate.server_cert,
                                          "key-file": certificate.server_key
                                          })

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # HA SERVER 2
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)

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
    # Configure Control Agent to use TLS.
    world.ca_cfg["Control-agent"]["trust-anchor"] = certificate.ca_cert
    world.ca_cfg["Control-agent"]["cert-file"] = certificate.server2_cert
    world.ca_cfg["Control-agent"]["key-file"] = certificate.server2_key
    world.ca_cfg["Control-agent"]["cert-required"] = False

    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_ha_hook('libdhcp_ha.so')

    # Configure HA hook to use TLS.
    srv_control.update_ha_hook_parameter(HA_CONFIG)
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 100,
                                          "max-response-delay": 1500,
                                          "max-unacked-clients": 4,
                                          "this-server-name": "server2",
                                          "trust-anchor": certificate.ca_cert,
                                          "cert-file": certificate.server2_cert,
                                          "key-file": certificate.server2_key
                                          })

    world.dhcp_cfg['interfaces-config']['interfaces'] = [world.f_cfg.server2_iface]
    srv_control.build_and_send_config_files(dest=world.f_cfg.mgmt_address_2)

    # Send certificates to second server
    fabric_send_file(ca_cert, certificate.ca_cert, destination_host=world.f_cfg.mgmt_address_2)
    fabric_send_file(server_cert, certificate.server_cert, destination_host=world.f_cfg.mgmt_address_2)
    fabric_send_file(server_key, certificate.server_key, destination_host=world.f_cfg.mgmt_address_2)
    fabric_send_file(server2_cert, certificate.server2_cert, destination_host=world.f_cfg.mgmt_address_2)
    fabric_send_file(server2_key, certificate.server2_key, destination_host=world.f_cfg.mgmt_address_2)

    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    # Wait for HA pair to communicate
    wait_until_ha_state('hot-standby', dhcp_version=dhcp_version, channel='https', verify=ca_cert)
    wait_until_ha_state('hot-standby', dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2, channel='https',
                        verify=ca_cert)

    # Check if desired status is met.
    get_status_HA(True, True, ha_mode='hot-standby', primary_state='hot-standby', secondary_state='hot-standby',
                  primary_role='primary', secondary_role='standby',
                  primary_scopes=['server1'], secondary_scopes=[],
                  comm_interrupt=False, in_touch=True, channel='https', verify=ca_cert)

    # Acquire a lese and check it in both backends.
    if dhcp_version == 'v6':
        srv_msg.SARR(address='2001:db8:1::1', duid='00:03:00:01:66:55:44:33:22:11')
        srv_msg.check_leases({'address': '2001:db8:1::1', 'duid': '00:03:00:01:66:55:44:33:22:11'}, backend=backend)
        srv_msg.check_leases({'address': '2001:db8:1::1', 'duid': '00:03:00:01:66:55:44:33:22:11'}, backend=backend,
                             dest=world.f_cfg.mgmt_address_2)
    else:
        srv_msg.DORA('192.168.50.1')
        srv_msg.check_leases({'address': '192.168.50.1'}, backend=backend)
        srv_msg.check_leases({'address': '192.168.50.1'}, backend=backend, dest=world.f_cfg.mgmt_address_2)


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.ha
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_ha_tls(dhcp_version, backend):
    """
    Basic test of TLS functionality in HA Setup.
    Test generates certificate for both HA peers.
    We check for hot-standby HA status after server start and then try top get a lease
    and check both databases for it.
    If status is acquired and lease is propagated to both backends
    we can assume TLS connection is working.
    """
    # HA SERVER 1
    # Create certificates.
    certificate = srv_control.generate_certificate()
    ca_cert = certificate.download('ca_cert')
    server_cert = certificate.download('server_cert')
    server_key = certificate.download('server_key')
    server2_cert = certificate.download('server2_cert')
    server2_key = certificate.download('server2_key')

    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)
    if dhcp_version == 'v6':
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ffff')
        srv_control.config_srv_prefix('2001:db8:2::', 0, 48, 91)
        srv_control.config_srv_id('LLT', '00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8')
    else:
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.200')

    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_ha_hook('libdhcp_ha.so')

    # Configure HA hook to use TLS.
    srv_control.update_ha_hook_parameter(HA_CONFIG)
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 2000,
                                          "max-ack-delay": 1000,
                                          "max-response-delay": 4000,
                                          "max-unacked-clients": 4,
                                          "this-server-name": "server1",
                                          "trust-anchor": certificate.ca_cert,
                                          "cert-file": certificate.server_cert,
                                          "key-file": certificate.server_key,
                                          "require-client-certs": False,
                                          "multi-threading": {
                                              "enable-multi-threading": True,
                                              "http-dedicated-listener": True,
                                              "http-listener-threads": 2,
                                              "http-client-threads": 1
                                              }
                                          })

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # HA SERVER 2
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)

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

    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_ha_hook('libdhcp_ha.so')

    # Configure HA hook to use TLS.
    srv_control.update_ha_hook_parameter(HA_CONFIG)
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 2000,
                                          "max-ack-delay": 1000,
                                          "max-response-delay": 4000,
                                          "max-unacked-clients": 4,
                                          "this-server-name": "server2",
                                          "trust-anchor": certificate.ca_cert,
                                          "cert-file": certificate.server2_cert,
                                          "key-file": certificate.server2_key,
                                          "require-client-certs": False,
                                          "multi-threading": {
                                              "enable-multi-threading": True,
                                              "http-dedicated-listener": True,
                                              "http-listener-threads": 2,
                                              "http-client-threads": 1
                                          }
                                          })

    world.dhcp_cfg['interfaces-config']['interfaces'] = [world.f_cfg.server2_iface]
    srv_control.build_and_send_config_files(dest=world.f_cfg.mgmt_address_2)

    # Send certificates to second server
    fabric_send_file(ca_cert, certificate.ca_cert, destination_host=world.f_cfg.mgmt_address_2)
    fabric_send_file(server_cert, certificate.server_cert, destination_host=world.f_cfg.mgmt_address_2)
    fabric_send_file(server_key, certificate.server_key, destination_host=world.f_cfg.mgmt_address_2)
    fabric_send_file(server2_cert, certificate.server2_cert, destination_host=world.f_cfg.mgmt_address_2)
    fabric_send_file(server2_key, certificate.server2_key, destination_host=world.f_cfg.mgmt_address_2)

    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    # Wait for HA pair to communicate
    wait_until_ha_state('hot-standby', dhcp_version=dhcp_version, channel='https', verify=ca_cert)
    wait_until_ha_state('hot-standby', dhcp_version=dhcp_version, dest=world.f_cfg.mgmt_address_2, channel='https',
                        verify=ca_cert)

    # let's allow to one more exchange between servers
    srv_msg.forge_sleep(3)

    # Check if desired status is met.
    get_status_HA(True, True, ha_mode='hot-standby', primary_state='hot-standby', secondary_state='hot-standby',
                  primary_role='primary', secondary_role='standby',
                  primary_scopes=['server1'], secondary_scopes=[],
                  comm_interrupt=False, in_touch=True, channel='https', verify=ca_cert)

    # Acquire a lese and check it in both backends.
    if dhcp_version == 'v6':
        srv_msg.SARR(address='2001:db8:1::1', duid='00:03:00:01:66:55:44:33:22:11')
        srv_msg.check_leases({'address': '2001:db8:1::1', 'duid': '00:03:00:01:66:55:44:33:22:11'}, backend=backend)
        srv_msg.check_leases({'address': '2001:db8:1::1', 'duid': '00:03:00:01:66:55:44:33:22:11'}, backend=backend,
                             dest=world.f_cfg.mgmt_address_2)
    else:
        srv_msg.DORA('192.168.50.1')
        srv_msg.check_leases({'address': '192.168.50.1'}, backend=backend)
        srv_msg.check_leases({'address': '192.168.50.1'}, backend=backend, dest=world.f_cfg.mgmt_address_2)
