# Copyright (C) 2026 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""M28, M29, M35-M36: Lease timing and DHCPRELEASE compliance tests."""

import time, logging

import pytest

log = logging.getLogger('forge')
from src.clientsupport.mock_server import DISCOVER, REQUEST, RELEASE
from src.clientsupport.packet_inspector import (
    filter_by_type,
    get_bootp_field,
    get_option,
    has_option,
    get_ip_dst,
    get_ip_src,
)

pytestmark = [pytest.mark.v4, pytest.mark.client_compliance]

_TIMEOUT = 15
_BROADCAST = '255.255.255.255'


def _wait_for(pkts, msg_type, timeout=_TIMEOUT):
    deadline = time.time() + timeout
    while time.time() < deadline:
        matches = filter_by_type(pkts, msg_type)
        if matches:
            return matches[0]
        time.sleep(0.1)
    return None


def _arp_reachable(ip, iface, timeout=3):
    """Return True if *ip* replies to an ARP who-has on *iface*.

    Sends a unicast ARP request (sender IP 0.0.0.0, like a DAD probe) and
    returns True if any ARP reply is received within *timeout* seconds.
    """
    from scapy.all import ARP, Ether, srp
    log.info(f'Checking ARP reachability for {ip}')
    probe = Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(op='who-has', psrc='0.0.0.0', pdst=ip)
    answered, _ = srp(probe, iface=iface, timeout=timeout, verbose=False)
    log.info(f'Answered: {answered}')
    return len(answered) > 0


@pytest.mark.timing_sensitive
def test_expiry_stops_traffic(mock_server_short_lease, dhcp_client):
    """M29: After lease expiry the client must stop using the address.

    Uses a very short lease.  Before expiry the leased IP must reply to an
    ARP who-has probe.  After expiry the leased IP must not reply to ARP.
    """
    from src.forge_cfg import world

    iface = world.f_cfg.iface

    # The client may DECLINE and retry (DAD), so poll until it responds to ARP
    # or the timeout expires.  We use the most recently seen REQUEST's IP.
    leased_ip = None
    deadline = time.time() + _TIMEOUT
    log.info(f'Waiting for leased IP to become reachable via ARP within {_TIMEOUT}s')
    while time.time() < deadline:
        reqs = filter_by_type(world.client_pkts, REQUEST)
        if reqs:
            candidate = get_option(reqs[-1], 'requested_addr')
            log.debug(f'Arp candidate: {candidate}')
            if candidate and _arp_reachable(candidate, iface, timeout=1):
                log.info(f'IP address is reachable: {candidate}')
                leased_ip = candidate
                break
        time.sleep(0.5)

    assert leased_ip is not None, \
        f'M29: Client never became reachable via ARP within {_TIMEOUT}s'

    # Silence all renewals so the lease is not extended
    mock_server_short_lease.set_policy({REQUEST: 'silence'})

    log.info(f'Waiting to expire leased IP: {leased_ip}')
    # Wait for the short lease to expire (lease_time + margin)
    log.info(f'Waiting for {mock_server_short_lease.lease_time + 3}s to expire')
    time.sleep(mock_server_short_lease.lease_time + 3)
    
    log.info(f'Checking expired leased IP: {leased_ip}')
    # Post-expiry: client must have relinquished the address
    assert not _arp_reachable(leased_ip, iface), \
        f'M29: Client still replies to ARP at {leased_ip!r} after lease expiry'


def test_release_unicast_with_client_id(mock_server, dhcp_client):
    """M35-M36: DHCPRELEASE must be unicast and use the same client-id as DISCOVER.

    The client is made to send a DHCPRELEASE and the resulting
    packet is inspected.
    """
    from src.forge_cfg import world

    # Complete initial DORA
    req = _wait_for(world.client_pkts, REQUEST)
    assert req is not None, 'No DHCPREQUEST received'

    # Record client-id from DISCOVER (if present)
    discover = filter_by_type(world.client_pkts, DISCOVER)
    disc_client_id = get_option(discover[0], 'client_id') if discover else None

    # Trigger DHCPRELEASE via CLIENT_RELEASE_CMD (skips if not configured)
    n_before = len(world.client_pkts)
    time.sleep(10)
    log.info('Triggering DHCPRELEASE via CLIENT_RELEASE_CMD')
    dhcp_client.release()
    log.info('Waiting for DHCPRELEASE')
    time.sleep(5)
    log.info('Done waiting for DHCPRELEASE')

    releases = filter_by_type(world.client_pkts[n_before:], RELEASE)
    if not releases:
        pytest.fail(
            'CLIENT_RELEASE_CMD ran but client did not send DHCPRELEASE'
        )

    rel = releases[0]

    # M36: DHCPRELEASE must be unicast
    dst = get_ip_dst(rel)
    assert dst != _BROADCAST, \
        f'M36: DHCPRELEASE must be unicast, not broadcast (got dst={dst!r})'

    # M35: if client-id was used in DISCOVER, must use same in RELEASE
    if disc_client_id is not None:
        rel_client_id = get_option(rel, 'client_id')
        assert rel_client_id == disc_client_id, \
            (f'M35: RELEASE client_id {rel_client_id!r} must match '
             f'DISCOVER client_id {disc_client_id!r}')
