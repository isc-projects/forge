# Copyright (C) 2024-2025 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea4 Ping Check hook HA tests"""

import os
import ipaddress
import pytest

from src import misc
from src import srv_msg
from src import srv_control

from src.forge_cfg import world
from src.protosupport.multi_protocol_functions import log_contains, log_doesnt_contain
from .steps import get_status_HA, wait_until_ha_state, send_increased_elapsed_time


def generate_ip_address_shift():
    """Function searches for IP addresses that can be used for ping check.
    """
    # shift_list
    # 1 Empty IP address before CIADDR
    # 2 New CIADDR
    # 3 Empty IP address after CIADDR
    # 4 IP address after CIADDR that will be added do forge interface to respond to PING
    # 5 Empty IP address after CIADDR

    ciaddr = ipaddress.IPv4Interface(f'{world.f_cfg.ciaddr}/24')
    srv4_addr = ipaddress.IPv4Interface(f'{world.f_cfg.srv4_addr}/24')
    # chceck if srv4_addr is bigger than ciaddr by 10 to fit new ip
    if srv4_addr.ip > ciaddr.ip+10:
        return [1, 2, 3, 4, 5]
    # if not, check if srv4_addr is bigger than ciaddr and if ciaddr - 10 is in the same subnet
    if srv4_addr.ip > ciaddr.ip:
        if (ciaddr - 10).network.subnet_of(ciaddr.network):
            return [-5, -4, -3, -2, -1]
        return [11, 12, 13, 14, 15]
    if srv4_addr.ip < ciaddr.ip-10:
        return [-5, -4, -3, -2, -1]
    if (ciaddr + 10).network.subnet_of(ciaddr.network):
        return [1, 2, 3, 4, 5]
    return [-15, -14, -13, -12, -11]


# Fixture to configure additional IP address for tests.
@pytest.fixture()
def prepare_pingcheck_env():
    ip_address_shift = generate_ip_address_shift()
    ciaddr = ipaddress.ip_address(world.f_cfg.ciaddr)
    # Assign responding IP address to forge interface
    new_ip = ciaddr + ip_address_shift[3]
    command = os.system(f'ip address replace {new_ip}/24 dev {world.f_cfg.iface}')
    # Assing new address to forge to use instead of ciaddr
    new_ciaddr_ip = ciaddr + ip_address_shift[1]
    command = os.system(f'ip address replace {new_ciaddr_ip}/24 dev {world.f_cfg.iface}')
    assert command == 0
    yield
    command = os.system(f'ip address del {new_ip}/24 dev {world.f_cfg.iface}')
    command = os.system(f'ip address del {new_ciaddr_ip}/24 dev {world.f_cfg.iface}')
    assert command == 0


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


@pytest.mark.usefixtures('prepare_pingcheck_env')
@pytest.mark.v4
@pytest.mark.ha
@pytest.mark.parametrize('ha_state', ['standby', 'partnerdown'])
def test_v4_ping_check_basic_ha(ha_state):
    """
    This test configures a pool with two IP addresses that will respond to PING and uses Discover
    and full DORA exchanges to test proper response.
    CIADDR and IPADDRESSES[3] addresses will respond to ping.
    'partnerdown' parameter tests if feature works with primary server down.
    """
    misc.test_setup()
    # Create subnet CIADDR and new ips.
    ciaddr = ipaddress.IPv4Interface(f'{world.f_cfg.ciaddr}/24')
    srv_control.config_srv_subnet(ciaddr.network, None)
    # Generate IP addresses from ip_addresses table.
    ip_address_shift = generate_ip_address_shift()
    ip_addresses = []
    for i in ip_address_shift:
        ip_addresses.append(ciaddr.ip + i)
    # Create pools from ip addresses
    for ip_address in ip_addresses:
        srv_control.new_pool(f'{ip_address}/32', 0)

    # Increase timeout of DORA messages to account for ping check.
    world.cfg['wait_interval'] += 1

    srv_control.add_unix_socket()
    srv_control.add_http_control_channel('$(MGMT_ADDRESS)')
    srv_control.add_hooks('libdhcp_ping_check.so')
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "enable-ping-check", True)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "min-ping-requests", 1)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "reply-timeout", 100)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "ping-cltt-secs", 60)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "ping-channel-threads", 0)
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_hooks('libdhcp_ha.so')
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
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)
    srv_control.config_srv_subnet(ciaddr.network, None, world.f_cfg.server2_iface)
    for ip_address in ip_addresses:
        srv_control.new_pool(f'{ip_address}/32', 0)

    world.cfg['wait_interval'] += 1
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel(world.f_cfg.mgmt_address_2)
    srv_control.add_hooks('libdhcp_ping_check.so')
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "enable-ping-check", True)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "min-ping-requests", 1)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "reply-timeout", 100)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "ping-cltt-secs", 60)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "ping-channel-threads", 0)
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_hooks('libdhcp_ha.so')
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
    wait_until_ha_state('hot-standby', dhcp_version='v4', channel='http')
    wait_until_ha_state('hot-standby', dhcp_version='v4', dest=world.f_cfg.mgmt_address_2, channel='http')

    # Check if desired status is met.
    get_status_HA(True, True, ha_mode='hot-standby', primary_state='hot-standby', secondary_state='hot-standby',
                  primary_role='primary', secondary_role='standby',
                  primary_scopes=['server1'], secondary_scopes=[],
                  comm_interrupt=False, in_touch=True, channel='http')

    if ha_state == 'partnerdown':
        # Shutdown primary server and wait for 'partner-down' status
        srv_control.start_srv('DHCP', 'stopped')
        srv_msg.forge_sleep(2, 'seconds')
        send_increased_elapsed_time(5, dhcp_version='v4')
        wait_until_ha_state('partner-down', dhcp_version='v4', dest=world.f_cfg.mgmt_address_2, channel='http')
        srv_msg.forge_sleep(2, 'seconds')

    # Send DORA for new client. (IPADDRESSES[0])
    srv_msg.DORA(ip_addresses[0], chaddr='ff:01:02:03:ff:04')

    # Send DISCOVER - next IP in line is used. (IPADDRESSES[1] = CIADDR)
    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:05')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER', expect_response=False)

    # Send DORA for new client. (IPADDRESSES[2])
    srv_msg.DORA(ip_addresses[2], chaddr='ff:01:02:03:ff:05')

    # Send DISCOVER - next IP in line is used. (IPADDRESSES[3])
    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:06')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER', expect_response=False)

    # Send DORA for new client. (IPADDRESSES[4])
    srv_msg.DORA(ip_addresses[4], chaddr='ff:01:02:03:ff:06')


@pytest.mark.v4
@pytest.mark.hook
@pytest.mark.ha
@pytest.mark.parametrize('ha_state', ['standby', 'partnerdown'])
def test_v4_ping_check_requests_ha(ha_state):
    """
    Test that checks configuration of number of ping requests.
    'partnerdown' parametr tests if feature works with primary server down.
    """
    # Create subnet and pool
    ciaddr = ipaddress.IPv4Interface(f'{world.f_cfg.ciaddr}/24')
    ip_address_shift = generate_ip_address_shift()
    ip_address = ciaddr + ip_address_shift[2]

    # Number of PING requests to try
    requests = 5

    # HA SERVER 1
    misc.test_setup()
    srv_control.config_srv_subnet(ciaddr.network, ip_address)
    # Increase timeout of DORA messages to account for ping check.
    world.cfg['wait_interval'] += 1

    srv_control.add_unix_socket()
    srv_control.add_http_control_channel('$(MGMT_ADDRESS)')
    srv_control.add_hooks('libdhcp_ping_check.so')
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "enable-ping-check", True)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "min-ping-requests", requests)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "reply-timeout", 100)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "ping-cltt-secs", 60)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "ping-channel-threads", 0)
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_hooks('libdhcp_ha.so')
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
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)
    srv_control.config_srv_subnet(ciaddr.network, ip_address, world.f_cfg.server2_iface)

    world.cfg['wait_interval'] += 1
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel(world.f_cfg.mgmt_address_2)
    srv_control.add_hooks('libdhcp_ping_check.so')
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "enable-ping-check", True)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "min-ping-requests", requests)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "reply-timeout", 100)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "ping-cltt-secs", 60)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "ping-channel-threads", 0)
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_hooks('libdhcp_ha.so')
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
    wait_until_ha_state('hot-standby', dhcp_version='v4', channel='http')
    wait_until_ha_state('hot-standby', dhcp_version='v4', dest=world.f_cfg.mgmt_address_2, channel='http')

    # Check if desired status is met.
    get_status_HA(True, True, ha_mode='hot-standby', primary_state='hot-standby', secondary_state='hot-standby',
                  primary_role='primary', secondary_role='standby',
                  primary_scopes=['server1'], secondary_scopes=[],
                  comm_interrupt=False, in_touch=True, channel='http')

    if ha_state == 'partnerdown':
        # Shutdown primary server and wait for 'partner-down' status
        srv_control.start_srv('DHCP', 'stopped')
        srv_msg.forge_sleep(2, 'seconds')
        send_increased_elapsed_time(5, dhcp_version='v4')
        wait_until_ha_state('partner-down', dhcp_version='v4', dest=world.f_cfg.mgmt_address_2, channel='http')
        srv_msg.forge_sleep(2, 'seconds')

    # Send DORA for new client.
    srv_msg.DORA(ip_address.ip, chaddr='ff:01:02:03:ff:04')

    # Verify that proper number of PINGs was sent.
    log_server = world.f_cfg.mgmt_address_2 if ha_state == 'partnerdown' else world.f_cfg.mgmt_address
    for r in range(requests):
        log_contains(f'PING_CHECK_CHANNEL_ECHO_REQUEST_SENT to address {ip_address.ip}, id 1, sequence {r+1}',
                     destination=log_server)
    log_doesnt_contain(f'PING_CHECK_CHANNEL_ECHO_REQUEST_SENT to address {ip_address.ip}, id 1, sequence {requests+1}',
                       destination=log_server)


@pytest.mark.v4
@pytest.mark.ha
@pytest.mark.parametrize('ha_state', ['standby', 'partnerdown'])
def test_v4_ping_check_timeout_ha(ha_state):
    """
    Test that checks configuration of ping timeout.
    'partnerdown' parametr tests if feature works with primary server down.
    """
    # Timeout for ping-check
    timeout = 2000
    # Create subnet and pool
    ciaddr = ipaddress.IPv4Interface(f'{world.f_cfg.ciaddr}/24')
    ip_address_shift = generate_ip_address_shift()
    ip_address = ciaddr + ip_address_shift[2]

    # HA SERVER 1
    misc.test_setup()
    srv_control.config_srv_subnet(ciaddr.network, ip_address)
    # Increase timeout of DORA messages to account for ping check.
    world.cfg['wait_interval'] += 1

    srv_control.add_unix_socket()
    srv_control.add_http_control_channel('$(MGMT_ADDRESS)')
    srv_control.add_hooks('libdhcp_ping_check.so')
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "enable-ping-check", True)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "min-ping-requests", 1)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "reply-timeout", timeout)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "ping-cltt-secs", 60)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "ping-channel-threads", 0)
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_hooks('libdhcp_ha.so')
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
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)
    srv_control.config_srv_subnet(ciaddr.network, ip_address, world.f_cfg.server2_iface)

    world.cfg['wait_interval'] += 1
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel(world.f_cfg.mgmt_address_2)
    srv_control.add_hooks('libdhcp_ping_check.so')
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "enable-ping-check", True)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "min-ping-requests", 1)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "reply-timeout", timeout)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "ping-cltt-secs", 60)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "ping-channel-threads", 0)
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_hooks('libdhcp_ha.so')
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
    wait_until_ha_state('hot-standby', dhcp_version='v4', channel='http')
    wait_until_ha_state('hot-standby', dhcp_version='v4', dest=world.f_cfg.mgmt_address_2, channel='http')

    # Check if desired status is met.
    get_status_HA(True, True, ha_mode='hot-standby', primary_state='hot-standby', secondary_state='hot-standby',
                  primary_role='primary', secondary_role='standby',
                  primary_scopes=['server1'], secondary_scopes=[],
                  comm_interrupt=False, in_touch=True, channel='http')

    if ha_state == 'partnerdown':
        # Shutdown primary server and wait for 'partner-down' status
        srv_control.start_srv('DHCP', 'stopped')
        srv_msg.forge_sleep(2, 'seconds')
        send_increased_elapsed_time(5, dhcp_version='v4')
        wait_until_ha_state('partner-down', dhcp_version='v4', dest=world.f_cfg.mgmt_address_2, channel='http')
        srv_msg.forge_sleep(2, 'seconds')

    # Send DISCOVER for new client.
    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    # Decrease timeout of DISCOVER message so we will not wait for Offer.
    world.cfg['wait_interval'] = 0.1
    srv_msg.send_dont_wait_for_message()

    log_server = world.f_cfg.mgmt_address_2 if ha_state == 'partnerdown' else world.f_cfg.mgmt_address
    # Verify that ping was send and Kea is waiting for response.
    log_contains(
        f'PING_CHECK_CHANNEL_ECHO_REQUEST_SENT to address {ip_address.ip}, id 1, sequence 1', destination=log_server)
    log_doesnt_contain(f'PING_CHECK_MGR_REPLY_TIMEOUT_EXPIRED for {ip_address.ip}, ECHO REQUEST 1 of 1, '
                       f'reply-timeout {timeout}', destination=log_server)
    log_doesnt_contain(f'PING_CHECK_MGR_LEASE_FREE_TO_USE address {ip_address.ip} is free to use',
                       destination=log_server)

    # Wait for reply timeout.
    srv_msg.forge_sleep(timeout+1000, 'milliseconds')

    # Verify that Kea timed out waiting for response.
    log_contains(f'PING_CHECK_MGR_REPLY_TIMEOUT_EXPIRED for {ip_address.ip}, ECHO REQUEST 1 of 1, '
                 f'reply-timeout {timeout}', destination=log_server)
    log_contains(f'PING_CHECK_MGR_LEASE_FREE_TO_USE address {ip_address.ip} is free to use', destination=log_server)


@pytest.mark.v4
@pytest.mark.ha
@pytest.mark.parametrize('ha_state', ['standby', 'partnerdown', 'interrupted'])
def test_v4_ping_check_cltt_ha(ha_state):
    """
    Test that checks configuration of ping cltt.
    'partnerdown' parameter tests if feature works with primary server down before DHCP traffic starts.
    'interrupted' parameter tests if cltt is honored by second server if first shuts down after making ping-check.
    """
    probation_period = 2
    # Timeout for ping-check
    ping_cltt = 2 if ha_state != 'interrupted' else 10
    # Create subnet and pool
    ciaddr = ipaddress.IPv4Interface(f'{world.f_cfg.ciaddr}/24')
    ip_address_shift = generate_ip_address_shift()
    ip_address = ciaddr + ip_address_shift[2]

    # HA SERVER 1
    misc.test_setup()
    srv_control.config_srv_subnet(ciaddr.network, ip_address)
    # Increase timeout of DORA messages to account for ping check.
    world.cfg['wait_interval'] += 1
    srv_control.set_conf_parameter_global('decline-probation-period', probation_period)
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel('$(MGMT_ADDRESS)')
    srv_control.add_hooks('libdhcp_ping_check.so')
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "enable-ping-check", True)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "min-ping-requests", 1)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "reply-timeout", 100)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "ping-cltt-secs", ping_cltt)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "ping-channel-threads", 0)
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_hooks('libdhcp_ha.so')
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
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)
    srv_control.config_srv_subnet(ciaddr.network, ip_address, world.f_cfg.server2_iface)

    world.cfg['wait_interval'] += 1
    srv_control.set_conf_parameter_global('decline-probation-period', probation_period)
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel(world.f_cfg.mgmt_address_2)
    srv_control.add_hooks('libdhcp_ping_check.so')
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "enable-ping-check", True)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "min-ping-requests", 1)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "reply-timeout", 100)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "ping-cltt-secs", ping_cltt)
    srv_control.add_parameter_to_hook("libdhcp_ping_check.so", "ping-channel-threads", 0)
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_hooks('libdhcp_ha.so')
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
    wait_until_ha_state('hot-standby', dhcp_version='v4', channel='http')
    wait_until_ha_state('hot-standby', dhcp_version='v4', dest=world.f_cfg.mgmt_address_2, channel='http')

    # Check if desired status is met.
    get_status_HA(True, True, ha_mode='hot-standby', primary_state='hot-standby', secondary_state='hot-standby',
                  primary_role='primary', secondary_role='standby',
                  primary_scopes=['server1'], secondary_scopes=[],
                  comm_interrupt=False, in_touch=True, channel='http')

    if ha_state == 'partnerdown':
        # Shutdown primary server and wait for 'partner-down' status
        srv_control.start_srv('DHCP', 'stopped')
        srv_msg.forge_sleep(2, 'seconds')
        send_increased_elapsed_time(5, dhcp_version='v4')
        wait_until_ha_state('partner-down', dhcp_version='v4', dest=world.f_cfg.mgmt_address_2, channel='http')
        srv_msg.forge_sleep(2, 'seconds')

    # Send DORA for new client.
    srv_msg.DORA(ip_address.ip, chaddr='ff:01:02:03:ff:04')

    log_server = world.f_cfg.mgmt_address_2 if ha_state == 'partnerdown' else world.f_cfg.mgmt_address
    # Verify that only one PING was send.
    log_contains(
        f'PING_CHECK_CHANNEL_ECHO_REQUEST_SENT to address {ip_address.ip}, id 1, sequence 1', destination=log_server)
    log_doesnt_contain(
        f'PING_CHECK_CHANNEL_ECHO_REQUEST_SENT to address {ip_address.ip}, id 1, sequence 2', destination=log_server)

    if ha_state == 'interrupted':
        # Shutdown primary server and wait for 'partner-down' status
        srv_control.start_srv('DHCP', 'stopped')
        srv_msg.forge_sleep(2, 'seconds')
        send_increased_elapsed_time(5, dhcp_version='v4')
        wait_until_ha_state('partner-down', dhcp_version='v4', dest=world.f_cfg.mgmt_address_2, channel='http')
        srv_msg.forge_sleep(2, 'seconds')
        log_server = world.f_cfg.mgmt_address_2

    # Send discover before ping-cltt elapses.
    srv_msg.DO(ip_address.ip, chaddr='ff:01:02:03:ff:04')

    # Verify that no new PINGs were sent.
    log_doesnt_contain(
        f'PING_CHECK_CHANNEL_ECHO_REQUEST_SENT to address {ip_address.ip}, id 1, sequence 2', destination=log_server)

    # Wait for ping-cltt to elapse
    srv_msg.forge_sleep(ping_cltt, 'seconds')

    # Send discover after ping-cltt elapsed.
    srv_msg.DO(ip_address.ip, chaddr='ff:01:02:03:ff:04')

    # Verify that new PINGs was sent.
    log_contains(
        f'PING_CHECK_CHANNEL_ECHO_REQUEST_SENT to address {ip_address.ip}, id 1, sequence 2', destination=log_server)
