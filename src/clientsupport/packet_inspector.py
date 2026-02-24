# Copyright (C) 2026 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Helpers for inspecting captured DHCP client packets.

All functions operate on Scapy packet objects stored in world.client_pkts.
"""

from scapy.all import BOOTP, DHCP, IP, UDP


# ---------------------------------------------------------------------------
# Packet filtering helpers
# ---------------------------------------------------------------------------

def _dhcp_opts(pkt):
    """Return a dict of DHCP options from *pkt*."""
    if not pkt.haslayer(DHCP):
        return {}
    return {opt[0]: opt[1] for opt in pkt[DHCP].options
            if isinstance(opt, (list, tuple)) and len(opt) >= 2}


def get_msg_type(pkt):
    """Return the DHCP message-type integer from *pkt*, or None."""
    return _dhcp_opts(pkt).get('message-type')


def filter_by_type(pkts, msg_type):
    """Return packets from *pkts* whose DHCP message-type matches *msg_type*."""
    return [p for p in pkts if get_msg_type(p) == msg_type]


def first_of_type(pkts, msg_type):
    """Return the first packet of *msg_type* in *pkts*, or None."""
    matches = filter_by_type(pkts, msg_type)
    return matches[0] if matches else None


# ---------------------------------------------------------------------------
# Field / option accessors
# ---------------------------------------------------------------------------

def get_bootp_field(pkt, field):
    """Return a BOOTP field value from *pkt*.

    :param field: field name as used by Scapy, e.g. 'xid', 'ciaddr', 'chaddr'
    """
    if not pkt.haslayer(BOOTP):
        return None
    return getattr(pkt[BOOTP], field, None)


def get_option(pkt, opt_name):
    """Return the value of DHCP option *opt_name* from *pkt*, or None."""
    return _dhcp_opts(pkt).get(opt_name)


def has_option(pkt, opt_name):
    """Return True if *pkt* contains DHCP option *opt_name*."""
    opts = _dhcp_opts(pkt)
    return opt_name in opts


def get_ip_dst(pkt):
    """Return the IP destination address of *pkt*."""
    if pkt.haslayer(IP):
        return pkt[IP].dst
    return None


def get_ip_src(pkt):
    """Return the IP source address of *pkt*."""
    if pkt.haslayer(IP):
        return pkt[IP].src
    return None


# ---------------------------------------------------------------------------
# Assertion helpers
# ---------------------------------------------------------------------------

def check_client_pkt_field(pkt, field, expected, msg=None):
    """Assert that BOOTP *field* equals *expected*.

    :param pkt: Scapy packet
    :param field: BOOTP field name
    :param expected: expected value
    :param msg: optional assertion message prefix
    """
    actual = get_bootp_field(pkt, field)
    label = msg or f'BOOTP.{field}'
    assert actual == expected, f'{label}: expected {expected!r}, got {actual!r}'


def check_client_option(pkt, opt_name, expected=None, msg=None):
    """Assert that *pkt* contains DHCP option *opt_name*.

    If *expected* is provided, also assert the option value equals *expected*.
    """
    label = msg or f'DHCP option {opt_name!r}'
    assert has_option(pkt, opt_name), f'{label}: option not present in packet'
    if expected is not None:
        actual = get_option(pkt, opt_name)
        assert actual == expected, \
            f'{label}: expected {expected!r}, got {actual!r}'


def check_client_no_option(pkt, opt_name, msg=None):
    """Assert that *pkt* does NOT contain DHCP option *opt_name*."""
    label = msg or f'DHCP option {opt_name!r}'
    assert not has_option(pkt, opt_name), \
        f'{label}: option must not be present but was found'


def check_ip_dst(pkt, expected, msg=None):
    """Assert that the IP destination of *pkt* equals *expected*."""
    actual = get_ip_dst(pkt)
    label = msg or 'IP.dst'
    assert actual == expected, f'{label}: expected {expected!r}, got {actual!r}'


# ---------------------------------------------------------------------------
# Multi-packet helpers
# ---------------------------------------------------------------------------

def collect_xids(pkts, msg_type, count=10):
    """Return a list of xid values from the first *count* packets of *msg_type*."""
    return [get_bootp_field(p, 'xid')
            for p in filter_by_type(pkts, msg_type)[:count]]


def packet_timestamps(pkts, msg_type):
    """Return a list of (timestamp, packet) tuples for packets of *msg_type*.

    Uses Scapy's pkt.time attribute (float seconds since epoch).
    """
    return [(p.time, p) for p in filter_by_type(pkts, msg_type)]


def inter_packet_gaps(pkts, msg_type):
    """Return a list of inter-packet gap durations (seconds) for *msg_type*."""
    times = [p.time for p in filter_by_type(pkts, msg_type)]
    return [times[i + 1] - times[i] for i in range(len(times) - 1)]
