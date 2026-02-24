# Copyright (C) 2026 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""M20-M23, M30: RENEWING state compliance tests.

If CLIENT_RENEW_CMD is configured the tests trigger renewal immediately and
are NOT timing_sensitive.  If it is not configured the tests wait for T1 to
expire using a short lease and are marked timing_sensitive.
"""

import time, logging

import pytest

log = logging.getLogger(__name__)

from src.clientsupport.mock_server import DISCOVER, REQUEST
from src.clientsupport.packet_inspector import (
    filter_by_type,
    get_bootp_field,
    get_option,
    has_option,
    get_ip_dst,
)

pytestmark = [pytest.mark.v4, pytest.mark.client_compliance]

_TIMEOUT = 15
_SHORT_LEASE = 20   # seconds — used when waiting for T1 (timing_sensitive path)
_SHORT_T1 = 8
_SHORT_T2 = 15


def _wait_for_request_after_ack(pkts, after_index, timeout=_TIMEOUT):
    """Wait for a REQUEST that arrives after *after_index* in pkts."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        reqs = filter_by_type(pkts[after_index:], REQUEST)
        if reqs:
            return reqs[0]
        time.sleep(0.2)
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


def _do_initial_dora(mock_server, dhcp_client, world, lease_time=3600, t1=None, t2=None):
    """Complete DORA and return (leased_ip, server_ip, n_pkts_after_ack).

    Returns the number of packets in world.client_pkts after the ACK so
    callers can filter for subsequent REQUESTs.
    """
    if t1 is not None or t2 is not None:
        mock_server.set_lease_params(
            lease_time=lease_time,
            t1=t1 if t1 is not None else lease_time // 2,
            t2=t2 if t2 is not None else lease_time * 7 // 8,
        )

    iface = world.f_cfg.iface
    # Wait for the initial REQUEST (SELECTING state)
    deadline = time.time() + _TIMEOUT
    req = None
    while time.time() < deadline:
        reqs = filter_by_type(world.client_pkts, REQUEST)
        if reqs:
            req = reqs[0]
            break
        time.sleep(0.1)
    assert req is not None, 'No initial DHCPREQUEST received'

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

    leased_ip = get_option(req, 'requested_addr')
    server_ip = world.f_cfg.srv4_addr
    n_after = len(world.client_pkts)
    return leased_ip, server_ip, n_after


def _get_renewing_request(mock_server, dhcp_client, world, ctrl):
    """Trigger renewal and return the resulting REQUEST packet."""
    if ctrl.has_renew_cmd():
        # Immediate trigger — not timing_sensitive
        n_before = len(world.client_pkts)
        ctrl.renew()
        time.sleep(1)
        reqs = filter_by_type(world.client_pkts[n_before:], REQUEST)
        return reqs[0] if reqs else None
    else:
        # Fall back: wait for T1 with short lease
        pytest.importorskip('time')  # no-op; just to document the dependency
        
        # Wait for T1 + generous buffer for DAD. DAD takes ~4-5s before the lease
        # even starts, so we need to wait at least DAD_time + T1 + buffer.
        deadline = time.time() + _SHORT_T1 + 10
        while time.time() < deadline:
            # Look for a unicast REQUEST (RENEWING signature)
            for pkt in filter_by_type(world.client_pkts, REQUEST):
                if get_ip_dst(pkt) != '255.255.255.255':
                    return pkt
            time.sleep(0.5)
        return None


@pytest.mark.timing_sensitive
def _renewing_timing_sensitive():
    """Marker function — not called directly; used to detect timing path."""


def _maybe_mark_timing(ctrl):
    """Add timing_sensitive marker to the current test if renew cmd absent."""
    if not ctrl.has_renew_cmd():
        # The test was already collected; we can't add a marker at runtime,
        # but we document the dependency via a warning.
        import warnings
        warnings.warn(
            'CLIENT_RENEW_CMD not configured — RENEWING tests require T1 wait '
            '(run with --run-timing)',
            UserWarning,
        )


def test_renewing_request_fields(mock_server, dhcp_client):
    """M20-M23: RENEWING state DHCPREQUEST field requirements."""
    from src.forge_cfg import world

    ctrl = dhcp_client

    if not ctrl.has_renew_cmd():
        pytest.mark.timing_sensitive(test_renewing_request_fields)
        mock_server.set_lease_params(
            lease_time=_SHORT_LEASE, t1=_SHORT_T1, t2=_SHORT_T2
        )

    leased_ip, server_ip, n_after = _do_initial_dora(mock_server, dhcp_client, world)

    renew_req = _get_renewing_request(mock_server, dhcp_client, world, ctrl)
    assert renew_req is not None, \
        'No RENEWING REQUEST received (check CLIENT_RENEW_CMD or use --run-timing)'

    # M20: option 54 must NOT be present
    assert not has_option(renew_req, 'server_id'), \
        'M20: Option 54 (Server Identifier) must NOT be present in RENEWING REQUEST'

    # M21: option 50 must NOT be present
    assert not has_option(renew_req, 'requested_addr'), \
        'M21: Option 50 (Requested IP) must NOT be present in RENEWING REQUEST'

    # M22: ciaddr must be the leased address
    ciaddr = get_bootp_field(renew_req, 'ciaddr')
    assert ciaddr == leased_ip, \
        f'M22: ciaddr must be leased address {leased_ip!r}, got {ciaddr!r}'

    # M23: must be sent unicast (not broadcast)
    dst = get_ip_dst(renew_req)
    assert dst != '255.255.255.255', \
        'M23: RENEWING REQUEST must be unicast, not broadcast'


def test_unicast_uses_server_id_opt54(mock_server, dhcp_client):
    """M30: Unicast renewal REQUEST IP dst must equal opt54 from original ACK."""
    from src.forge_cfg import world

    ctrl = dhcp_client

    if not ctrl.has_renew_cmd():
        mock_server.set_lease_params(
            lease_time=_SHORT_LEASE, t1=_SHORT_T1, t2=_SHORT_T2
        )

    leased_ip, server_ip, n_after = _do_initial_dora(mock_server, dhcp_client, world)

    log.info(f'Leased IP: {leased_ip!r}')
    log.info(f'Server IP: {server_ip!r}')
    log.info('waiting for renewing request')
    renew_req = _get_renewing_request(mock_server, dhcp_client, world, ctrl)
    log.info('done waiting for renewing request')
    assert renew_req is not None, \
        'No RENEWING REQUEST received (check CLIENT_RENEW_CMD or use --run-timing)'

    log.info(f'Renewing request: {renew_req!r}')
    dst = get_ip_dst(renew_req)
    assert dst == server_ip, \
        (f'M30: RENEWING REQUEST IP dst {dst!r} must equal server_id from ACK '
         f'({server_ip!r})')
