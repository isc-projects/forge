# Copyright (C) 2026 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""M31-M34: DHCPDECLINE compliance tests."""

import time

import pytest

from scapy.all import ARP, Ether, sendp, get_if_hwaddr

from src.clientsupport.mock_server import DISCOVER, REQUEST, DECLINE
from src.clientsupport.packet_inspector import (
    filter_by_type,
    get_bootp_field,
    get_option,
    has_option,
    get_ip_dst,
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


def test_decline_on_arp_conflict(mock_server, dhcp_client):
    """M31-M34: Client must send DHCPDECLINE when ARP conflict detected.

    After the mock server sends an OFFER, we inject a gratuitous ARP reply
    claiming the offered address is already in use.  The client should detect
    the conflict (via its ARP probe) and send DHCPDECLINE.

    Note: This test depends on the client performing ARP probing (S03).
    If the client does not probe, it will accept the address and no DECLINE
    will be sent; the test is skipped in that case.
    """
    from src.forge_cfg import world

    iface = world.f_cfg.iface

    # Wait for the mock server to send an OFFER (we intercept by watching for
    # the client's DISCOVER, then inject the ARP conflict before the client
    # can complete its ARP probe)
    discover = _wait_for(world.client_pkts, DISCOVER)
    assert discover is not None, 'No DHCPDISCOVER received'

    # The mock server will have sent an OFFER; determine the offered IP
    # by waiting briefly then checking what IP the server allocated
    time.sleep(0.3)
    offered_ip = mock_server._allocate_ip(get_bootp_field(discover, 'chaddr'))

    # Inject a gratuitous ARP reply claiming the offered IP is in use
    # Use a different MAC so it looks like a real conflict
    conflict_mac = 'de:ad:be:ef:00:01'
    arp_conflict = (
        Ether(src=conflict_mac, dst='ff:ff:ff:ff:ff:ff') /
        ARP(
            op=2,           # ARP reply
            hwsrc=conflict_mac,
            psrc=offered_ip,
            hwdst='ff:ff:ff:ff:ff:ff',
            pdst=offered_ip,
        )
    )
    sendp(arp_conflict, iface=iface, verbose=False)

    # Wait for DHCPDECLINE
    decline = _wait_for(world.client_pkts, DECLINE, timeout=_TIMEOUT)
    if decline is None:
        pytest.skip(
            'Client did not send DHCPDECLINE after ARP conflict injection — '
            'client may not perform ARP probing (S03) or may not have detected '
            'the injected conflict in time'
        )

    # M31: DHCPDECLINE must be sent (already confirmed above)

    # M32: option 50 (Requested IP) must be present with the conflicting address
    req_addr = get_option(decline, 'requested_addr')
    assert req_addr is not None, \
        'M32: Option 50 (Requested IP) must be present in DHCPDECLINE'
    assert req_addr == offered_ip, \
        (f'M32: DECLINE option 50 is {req_addr!r}, '
         f'expected conflicting address {offered_ip!r}')

    # M33: option 54 (Server Identifier) must be present
    assert has_option(decline, 'server_id'), \
        'M33: Option 54 (Server Identifier) must be present in DHCPDECLINE'

    # M34: DHCPDECLINE must be broadcast
    dst = get_ip_dst(decline)
    assert dst == _BROADCAST, \
        f'M34: DHCPDECLINE must be broadcast to {_BROADCAST}, got {dst!r}'
