# Copyright (C) 2026 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""M41: ARP probe sender IP compliance test."""

import time

import pytest

from scapy.all import ARP, AsyncSniffer

from src.clientsupport.mock_server import DISCOVER, REQUEST
from src.clientsupport.packet_inspector import (
    filter_by_type,
    get_option,
)

pytestmark = [pytest.mark.v4, pytest.mark.client_compliance]

_TIMEOUT = 15


def test_arp_probe_sender_ip_zero(mock_server, dhcp_client):
    """M41: When broadcasting ARP probe for offered address, sender IP must be 0.0.0.0.

    After the mock server sends an OFFER, the client should ARP-probe the
    offered address.  RFC 2131 §4.4.1 requires the sender protocol address
    in the ARP probe to be 0.0.0.0.
    """
    from src.forge_cfg import world

    iface = world.f_cfg.iface
    arp_probes = []

    def capture_arp(pkt):
        if pkt.haslayer(ARP) and pkt[ARP].op == 1:  # ARP request
            arp_probes.append(pkt)

    arp_sniffer = AsyncSniffer(
        iface=iface,
        filter='arp',
        prn=capture_arp,
        store=False,
    )
    arp_sniffer.start()

    try:
        # Wait for the client to complete DORA (REQUEST received)
        deadline = time.time() + _TIMEOUT
        request = None
        while time.time() < deadline:
            reqs = filter_by_type(world.client_pkts, REQUEST)
            if reqs:
                request = reqs[0]
                break
            time.sleep(0.1)

        # Give the client a moment to send ARP probes
        time.sleep(2)
    finally:
        arp_sniffer.stop()
        arp_sniffer.join()

    if not arp_probes:
        pytest.skip(
            'No ARP probes observed — client may not perform ARP probing (S03) '
            'or probes were not visible on this interface'
        )

    # Determine the offered IP
    offered_ip = None
    if request is not None:
        offered_ip = get_option(request, 'requested_addr')

    # Find ARP probes targeting the offered IP
    relevant_probes = arp_probes
    if offered_ip:
        relevant_probes = [p for p in arp_probes if p[ARP].pdst == offered_ip]

    if not relevant_probes:
        pytest.skip(
            f'No ARP probes for offered address {offered_ip!r} observed'
        )

    for probe in relevant_probes:
        sender_ip = probe[ARP].psrc
        assert sender_ip == '0.0.0.0', \
            (f'M41: ARP probe sender IP must be 0.0.0.0, '
             f'got {sender_ip!r} (target: {probe[ARP].pdst!r})')
