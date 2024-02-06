# Copyright (C) 2023 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea4 Ping Check hook"""

import os
import pytest

from src import misc
from src import srv_msg
from src import srv_control

from src.forge_cfg import world
from src.protosupport.multi_protocol_functions import log_contains, log_doesnt_contain


# Set of IP addresses to be used in testing. Number corresponds to the shift in last field from CIADDR.
IPADDRESSES = [
    -1,  # Empty IP address before CIADDR - can be modified
    0,  # CIADDR
    1,  # Empty IP address after CIADDR - can be modified
    2,  # IP address after CIADDR that will be added do forge interface to respond to PING - can be modified
    3  # Empty IP address after CIADDR - can be modified
]


# Fixture to configure additional IP address for tests.
@pytest.fixture()
def prepare_pingcheck_env():
    ciaddr = world.f_cfg.ciaddr
    # Assign responding IP address to forge interface
    new_ip = ".".join(ciaddr.split(".")[0:-1] + [str(int(ciaddr.split(".")[-1]) + IPADDRESSES[3])])
    command = os.system(f'ip address replace {new_ip}/24 dev {world.f_cfg.iface}')
    assert command == 0
    yield
    command = os.system(f'ip address del {new_ip}/24 dev {world.f_cfg.iface}')
    assert command == 0


@pytest.mark.usefixtures('prepare_pingcheck_env')
@pytest.mark.v4
@pytest.mark.hook
def test_v4_ping_check_basic():
    """
    This test configures a pool with two IP addresses that will respond to PING and uses Discover
    and full DORA exchanges to test proper response.
    CIADDR and IPADDRESSES[3] addresses will respond to ping.
    """
    misc.test_setup()
    # Create subnet CIADDR and new ips.
    ciaddr = world.f_cfg.ciaddr
    subnet = '.'.join(ciaddr.split('.')[0:-1]+['0/24'])
    srv_control.config_srv_subnet(subnet, None)
    # Generate IP addresses from IPADDRESSES table.
    ip_addresses = []
    for i in IPADDRESSES:
        ip_addresses.append(".".join(ciaddr.split(".")[0:-1] + [str(int(ciaddr.split(".")[-1]) + i)]))
    # Create pools from ip addresses
    for ip_address in ip_addresses:
        srv_control.new_pool(f'{ip_address}/32', 0)

    # Increase timeout of DORA messages to account for ping check.
    world.cfg['wait_interval'] += 1

    srv_control.add_hooks('libdhcp_ping_check.so')
    srv_control.add_parameter_to_hook(1, "enable-ping-check", True)
    srv_control.add_parameter_to_hook(1, "min-ping-requests", 1)
    srv_control.add_parameter_to_hook(1, "reply-timeout", 100)
    srv_control.add_parameter_to_hook(1, "ping-cltt-secs", 60)
    srv_control.add_parameter_to_hook(1, "ping-channel-threads", 0)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

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
def test_v4_ping_check_requests():
    """
    Test that checks configuration of number of ping requests.
    """
    misc.test_setup()
    # Create subnet and pool
    ciaddr = world.f_cfg.ciaddr
    subnet = '.'.join(ciaddr.split('.')[0:-1]+['0/24'])
    ip_address = ".".join(ciaddr.split(".")[0:-1]+[str(int(ciaddr.split(".")[-1])+IPADDRESSES[2])])
    srv_control.config_srv_subnet(subnet, f'{ip_address}/32')

    # Increase timeout of DORA messages to account for ping check.
    world.cfg['wait_interval'] += 1

    # Number of PING requests to try
    requests = 5
    srv_control.add_hooks('libdhcp_ping_check.so')
    srv_control.add_parameter_to_hook(1, "enable-ping-check", True)
    srv_control.add_parameter_to_hook(1, "min-ping-requests", requests)
    srv_control.add_parameter_to_hook(1, "reply-timeout", 100)
    srv_control.add_parameter_to_hook(1, "ping-cltt-secs", 60)
    srv_control.add_parameter_to_hook(1, "ping-channel-threads", 0)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Send DORA for new client.
    srv_msg.DORA(ip_address, chaddr='ff:01:02:03:ff:04',)

    # Verify that proper number of PINGs was sent.
    for r in range(requests):
        log_contains(f'PING_CHECK_CHANNEL_ECHO_REQUEST_SENT to address {ip_address}, id 1, sequence {r+1}')
    log_doesnt_contain(f'PING_CHECK_CHANNEL_ECHO_REQUEST_SENT to address {ip_address}, id 1, sequence {requests+1}')


@pytest.mark.v4
@pytest.mark.hook
def test_v4_ping_check_timeout():
    """
    Test that checks configuration of ping timeout.
    """
    misc.test_setup()
    # Create subnet and pool
    ciaddr = world.f_cfg.ciaddr
    subnet = '.'.join(ciaddr.split('.')[0:-1]+['0/24'])
    ip_address = ".".join(ciaddr.split(".")[0:-1]+[str(int(ciaddr.split(".")[-1])+IPADDRESSES[2])])
    srv_control.config_srv_subnet(subnet, f'{ip_address}/32')

    # Timeout for ping-check
    timeout = 2000
    srv_control.add_hooks('libdhcp_ping_check.so')
    srv_control.add_parameter_to_hook(1, "enable-ping-check", True)
    srv_control.add_parameter_to_hook(1, "min-ping-requests", 1)
    srv_control.add_parameter_to_hook(1, "reply-timeout", timeout)
    srv_control.add_parameter_to_hook(1, "ping-cltt-secs", 60)
    srv_control.add_parameter_to_hook(1, "ping-channel-threads", 0)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Send DISCOVER for new client.
    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    # Decrease timeout of DISCOVER message so we will not wait for Offer.
    world.cfg['wait_interval'] = 0.1
    srv_msg.send_dont_wait_for_message()

    # Verify that ping was send and Kea is waiting for response.
    log_contains(f'PING_CHECK_CHANNEL_ECHO_REQUEST_SENT to address {ip_address}, id 1, sequence 1')
    log_doesnt_contain(f'PING_CHECK_MGR_REPLY_TIMEOUT_EXPIRED for {ip_address}, ECHO REQUEST 1 of 1, '
                       f'reply-timeout {timeout}')
    log_doesnt_contain(f'PING_CHECK_MGR_LEASE_FREE_TO_USE address {ip_address} is free to use')

    # Wait for reply timeout.
    srv_msg.forge_sleep(timeout+1000, 'milliseconds')

    # Verify that Kea timed out waiting for response.
    log_contains(f'PING_CHECK_MGR_REPLY_TIMEOUT_EXPIRED for {ip_address}, ECHO REQUEST 1 of 1, '
                 f'reply-timeout {timeout}')
    log_contains(f'PING_CHECK_MGR_LEASE_FREE_TO_USE address {ip_address} is free to use')


@pytest.mark.v4
@pytest.mark.hook
def test_v4_ping_check_cltt():
    """
    Test that checks configuration of ping cltt.
    """
    misc.test_setup()
    probation_period = 2
    srv_control.set_conf_parameter_global('decline-probation-period', probation_period)
    # Create subnet and pool
    ciaddr = world.f_cfg.ciaddr
    subnet = '.'.join(ciaddr.split('.')[0:-1] + ['0/24'])
    ip_address = ".".join(ciaddr.split(".")[0:-1] + [str(int(ciaddr.split(".")[-1])+IPADDRESSES[2])])
    srv_control.config_srv_subnet(subnet, f'{ip_address}/32')

    # Increase timeout of DORA messages to account for ping check.
    world.cfg['wait_interval'] += 1

    # Timeout for ping-check
    ping_cltt = 2
    srv_control.add_hooks('libdhcp_ping_check.so')
    srv_control.add_parameter_to_hook(1, "enable-ping-check", True)
    srv_control.add_parameter_to_hook(1, "min-ping-requests", 1)
    srv_control.add_parameter_to_hook(1, "reply-timeout", 100)
    srv_control.add_parameter_to_hook(1, "ping-cltt-secs", ping_cltt)
    srv_control.add_parameter_to_hook(1, "ping-channel-threads", 0)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Send DORA for new client.
    srv_msg.DORA(ip_address, chaddr='ff:01:02:03:ff:04')

    # Verify that only one PING was send.
    log_contains(f'PING_CHECK_CHANNEL_ECHO_REQUEST_SENT to address {ip_address}, id 1, sequence 1')
    log_doesnt_contain(f'PING_CHECK_CHANNEL_ECHO_REQUEST_SENT to address {ip_address}, id 1, sequence 2')

    # Send discover before ping-cltt elapses.
    srv_msg.DO(ip_address, chaddr='ff:01:02:03:ff:04')

    # Verify that no new PINGs were sent.
    log_doesnt_contain(f'PING_CHECK_CHANNEL_ECHO_REQUEST_SENT to address {ip_address}, id 1, sequence 2')

    # Wait for ping-cltt to elapse
    srv_msg.forge_sleep(ping_cltt, 'seconds')

    # Send discover after ping-cltt elapsed.
    srv_msg.DO(ip_address, chaddr='ff:01:02:03:ff:04')

    # Verify that new PINGs was sent.
    log_contains(f'PING_CHECK_CHANNEL_ECHO_REQUEST_SENT to address {ip_address}, id 1, sequence 2')
