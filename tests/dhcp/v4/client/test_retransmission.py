# Copyright (C) 2026 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""M40: Retransmission exponential backoff compliance test."""

import time

import pytest

from src.clientsupport.mock_server import DISCOVER
from src.clientsupport.packet_inspector import (
    filter_by_type,
    inter_packet_gaps,
)

pytestmark = [pytest.mark.v4, pytest.mark.client_compliance, pytest.mark.timing_sensitive]

# RFC 2131 §4.1 retransmission schedule: 4, 8, 16, 32, 64 seconds (±1s jitter)
# We allow ±50% tolerance to account for implementation variation.
_EXPECTED_GAPS = [4, 8, 16, 32, 64]
_TOLERANCE = 0.5   # 50%
_COLLECT_TIMEOUT = 4 + 8 + 16 + 32 + 64 + 30  # enough for 5 retransmissions


def test_exponential_backoff(mock_server, dhcp_client):
    """M40: Client must use randomized exponential backoff retransmission.

    The mock server stays silent (no OFFER sent).  We collect DISCOVER
    retransmissions and verify the inter-packet gaps approximately follow
    the RFC 2131 schedule: 4, 8, 16, 32, 64 seconds (±50% jitter tolerance).
    """
    from src.forge_cfg import world

    # Silence all responses
    mock_server.set_policy({DISCOVER: 'silence'})

    # Collect at least 4 DISCOVERs (3 gaps to verify)
    min_discovers = 4
    deadline = time.time() + _COLLECT_TIMEOUT
    while time.time() < deadline:
        if len(filter_by_type(world.client_pkts, DISCOVER)) >= min_discovers:
            break
        time.sleep(1)

    discovers = filter_by_type(world.client_pkts, DISCOVER)
    assert len(discovers) >= 2, \
        f'M40: Need at least 2 DISCOVERs to measure gaps, got {len(discovers)}'

    gaps = inter_packet_gaps(world.client_pkts, DISCOVER)
    assert len(gaps) >= 1, 'M40: No inter-DISCOVER gaps measured'

    for i, (gap, expected) in enumerate(zip(gaps, _EXPECTED_GAPS)):
        lo = expected * (1 - _TOLERANCE)
        hi = expected * (1 + _TOLERANCE)
        assert lo <= gap <= hi, \
            (f'M40: Gap {i + 1} is {gap:.1f}s, expected {expected}s '
             f'(±{int(_TOLERANCE * 100)}%); range [{lo:.1f}, {hi:.1f}]')
