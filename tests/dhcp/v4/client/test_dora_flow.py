# Copyright (C) 2026 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""M10-M16: XID handling and SELECTING state DHCPREQUEST compliance tests."""

import time

import pytest

from src.clientsupport.mock_server import DISCOVER, REQUEST
from src.clientsupport.packet_inspector import (
    filter_by_type,
    first_of_type,
    get_bootp_field,
    get_option,
    has_option,
    get_ip_dst,
)

pytestmark = [pytest.mark.v4, pytest.mark.client_compliance]

_BROADCAST = '255.255.255.255'
_TIMEOUT = 10


def _wait_for(pkts, msg_type, timeout=_TIMEOUT):
    deadline = time.time() + timeout
    while time.time() < deadline:
        matches = filter_by_type(pkts, msg_type)
        if matches:
            return matches[0]
        time.sleep(0.1)
    return None


def _wait_for_n(pkts, msg_type, n, timeout=_TIMEOUT):
    deadline = time.time() + timeout
    while time.time() < deadline:
        matches = filter_by_type(pkts, msg_type)
        if len(matches) >= n:
            return matches[:n]
        time.sleep(0.1)
    return filter_by_type(pkts, msg_type)


def test_xid_randomness(mock_server, dhcp_client):
    """M10: Client must choose xid to minimize collision — collect 10 DISCOVERs
    across multiple start/stop cycles and assert they are not all identical."""
    from src.forge_cfg import world
    from src.clientsupport.client_control import ClientController

    ctrl = dhcp_client
    xids = []

    # Collect first DISCOVER from this run
    pkt = _wait_for(world.client_pkts, DISCOVER)
    assert pkt is not None, 'No DHCPDISCOVER received'
    xids.append(get_bootp_field(pkt, 'xid'))

    # Restart the client several times to collect more XIDs
    for _ in range(9):
        world.client_pkts.clear()
        ctrl.stop()
        time.sleep(0.3)
        ctrl.flush()
        time.sleep(0.2)
        ctrl.start()
        pkt = _wait_for(world.client_pkts, DISCOVER)
        if pkt:
            xids.append(get_bootp_field(pkt, 'xid'))

    assert len(xids) >= 2, 'Could not collect enough DISCOVERs to test XID randomness'
    assert len(set(xids)) > 1, \
        f'M10: All {len(xids)} DISCOVER XIDs are identical ({xids[0]:#010x}) — not random'


def test_request_reuses_offer_xid(mock_server, dhcp_client):
    """M11: DHCPREQUEST in SELECTING state must use same xid as the DHCPOFFER."""
    from src.forge_cfg import world

    discover = _wait_for(world.client_pkts, DISCOVER)
    assert discover is not None, 'No DHCPDISCOVER received'

    request = _wait_for(world.client_pkts, REQUEST)
    assert request is not None, 'No DHCPREQUEST received after OFFER'

    disc_xid = get_bootp_field(discover, 'xid')
    req_xid = get_bootp_field(request, 'xid')
    assert req_xid == disc_xid, \
        f'M11: REQUEST xid {req_xid:#010x} != DISCOVER xid {disc_xid:#010x}'


def test_selecting_state_request_fields(mock_server, dhcp_client):
    """M12-M16: DHCPREQUEST in SELECTING state field requirements."""
    from src.forge_cfg import world

    discover = _wait_for(world.client_pkts, DISCOVER)
    assert discover is not None, 'No DHCPDISCOVER received'

    request = _wait_for(world.client_pkts, REQUEST)
    assert request is not None, 'No DHCPREQUEST received after OFFER'

    # M12: ciaddr must be zero in SELECTING state
    ciaddr = get_bootp_field(request, 'ciaddr')
    assert ciaddr in ('0.0.0.0', None, 0), \
        f'M12: ciaddr must be 0.0.0.0 in SELECTING state, got {ciaddr!r}'

    # M13: option 50 (requested IP) must be set to yiaddr from OFFER
    # The mock server's OFFER yiaddr is what the client should echo back
    req_ip = get_option(request, 'requested_addr')
    assert req_ip is not None, \
        'M13: Option 50 (Requested IP Address) must be present in SELECTING REQUEST'

    # M14: option 54 (server identifier) must be included
    assert has_option(request, 'server_id'), \
        'M14: Option 54 (Server Identifier) must be present in SELECTING REQUEST'

    # M15: secs must match the original DISCOVER secs
    disc_secs = get_bootp_field(discover, 'secs')
    req_secs = get_bootp_field(request, 'secs')
    assert req_secs == disc_secs, \
        f'M15: REQUEST secs {req_secs} must equal DISCOVER secs {disc_secs}'

    # M16: REQUEST must be broadcast
    dst = get_ip_dst(request)
    assert dst == _BROADCAST, \
        f'M16: SELECTING REQUEST must be broadcast to {_BROADCAST}, got {dst!r}'
