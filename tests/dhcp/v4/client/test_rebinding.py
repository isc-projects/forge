# Copyright (C) 2026 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""M24-M27: REBINDING state compliance tests.

If CLIENT_REBIND_CMD is configured the tests trigger rebinding immediately and
are NOT timing_sensitive.  If it is not configured the tests use a short lease,
silence renewal responses, and wait for T2 — making them timing_sensitive.
"""

import time
import warnings

import pytest

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
_SHORT_LEASE = 30
_SHORT_T1 = 8
_SHORT_T2 = 16
_BROADCAST = '255.255.255.255'


def _do_initial_dora(mock_server, world, lease_time=3600, t1=None, t2=None):
    mock_server.set_lease_params(
        lease_time=lease_time,
        t1=t1 if t1 is not None else lease_time // 2,
        t2=t2 if t2 is not None else lease_time * 7 // 8,
    )
    deadline = time.time() + _TIMEOUT
    req = None
    while time.time() < deadline:
        reqs = filter_by_type(world.client_pkts, REQUEST)
        if reqs:
            req = reqs[0]
            break
        time.sleep(0.1)
    assert req is not None, 'No initial DHCPREQUEST received'
    leased_ip = get_option(req, 'requested_addr')
    return leased_ip, len(world.client_pkts)


def _get_rebinding_request(mock_server, ctrl, world, n_after):
    """Trigger rebinding and return the resulting broadcast REQUEST."""
    if ctrl.has_rebind_cmd():
        n_before = len(world.client_pkts)
        ctrl.rebind()
        time.sleep(1)
        reqs = filter_by_type(world.client_pkts[n_before:], REQUEST)
        return reqs[0] if reqs else None
    else:
        # Silence renewal responses so client transitions to REBINDING at T2
        mock_server.set_policy({REQUEST: 'silence'})
        
        # Wait for T2 + generous buffer for DAD and renewal retries.
        # DAD takes ~4-5s before the lease even starts, so we need to wait
        # at least DAD_time + T2 + buffer. We poll so we can return early.
        deadline = time.time() + _SHORT_T2 + 10
        while time.time() < deadline:
            # Look for a broadcast REQUEST (REBINDING signature)
            for pkt in filter_by_type(world.client_pkts[n_after:], REQUEST):
                if get_ip_dst(pkt) == _BROADCAST:
                    return pkt
            time.sleep(0.5)
        return None


def test_rebinding_request_fields(mock_server, dhcp_client):
    """M24-M27: REBINDING state DHCPREQUEST field requirements."""
    from src.forge_cfg import world

    ctrl = dhcp_client

    if not ctrl.has_rebind_cmd():
        warnings.warn(
            'CLIENT_REBIND_CMD not configured — waiting for T2 expiry (timing_sensitive)',
            UserWarning,
        )
        leased_ip, n_after = _do_initial_dora(
            mock_server, world,
            lease_time=_SHORT_LEASE, t1=_SHORT_T1, t2=_SHORT_T2,
        )
    else:
        leased_ip, n_after = _do_initial_dora(mock_server, world)

    rebind_req = _get_rebinding_request(mock_server, ctrl, world, n_after)
    assert rebind_req is not None, \
        ('No REBINDING REQUEST received (check CLIENT_REBIND_CMD or use '
         '--run-timing with a short lease)')

    # M24: option 54 must NOT be present
    assert not has_option(rebind_req, 'server_id'), \
        'M24: Option 54 (Server Identifier) must NOT be present in REBINDING REQUEST'

    # M25: option 50 must NOT be present
    assert not has_option(rebind_req, 'requested_addr'), \
        'M25: Option 50 (Requested IP) must NOT be present in REBINDING REQUEST'

    # M26: ciaddr must be the leased address
    ciaddr = get_bootp_field(rebind_req, 'ciaddr')
    assert ciaddr == leased_ip, \
        f'M26: ciaddr must be leased address {leased_ip!r}, got {ciaddr!r}'

    # M27: must be broadcast
    dst = get_ip_dst(rebind_req)
    assert dst == _BROADCAST, \
        f'M27: REBINDING REQUEST must be broadcast to {_BROADCAST}, got {dst!r}'
