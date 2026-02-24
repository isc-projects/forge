# Copyright (C) 2026 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""M37-M39: Client identifier and Parameter Request List consistency tests."""

import time

import pytest

from src.clientsupport.mock_server import DISCOVER, REQUEST, RELEASE
from src.clientsupport.packet_inspector import (
    filter_by_type,
    get_option,
    has_option,
)

pytestmark = [pytest.mark.v4, pytest.mark.client_compliance]

_TIMEOUT = 10


def _wait_for(pkts, msg_type, timeout=_TIMEOUT):
    deadline = time.time() + timeout
    while time.time() < deadline:
        matches = filter_by_type(pkts, msg_type)
        if matches:
            return matches[0]
        time.sleep(0.1)
    return None


def test_client_id_prl_consistency(mock_server, dhcp_client):
    """M37, M39: client-id (opt 61) and PRL (opt 55) must be consistent.

    M37: If option 61 is used in any message, the same value must appear in
         all subsequent messages.
    M39: If option 55 (PRL) is present in DHCPDISCOVER, it must also be
         present in all subsequent DHCPREQUEST messages.

    M38 (client-id uniqueness within subnet) is not wire-testable and is
    skipped with a note.
    """
    from src.forge_cfg import world

    # Wait for initial DISCOVER
    discover = _wait_for(world.client_pkts, DISCOVER)
    assert discover is not None, 'No DHCPDISCOVER received'

    # Wait for SELECTING REQUEST
    request = _wait_for(world.client_pkts, REQUEST)
    assert request is not None, 'No DHCPREQUEST received'

    # Trigger RELEASE by stopping the client
    n_before = len(world.client_pkts)
    dhcp_client.stop()
    time.sleep(2)
    releases = filter_by_type(world.client_pkts[n_before:], RELEASE)

    # --- M37: client-id consistency ---
    disc_client_id = get_option(discover, 'client_id')
    req_client_id = get_option(request, 'client_id')

    if disc_client_id is not None:
        assert req_client_id == disc_client_id, \
            (f'M37: DISCOVER client_id {disc_client_id!r} != '
             f'REQUEST client_id {req_client_id!r}')
        if releases:
            rel_client_id = get_option(releases[0], 'client_id')
            assert rel_client_id == disc_client_id, \
                (f'M37: DISCOVER client_id {disc_client_id!r} != '
                 f'RELEASE client_id {rel_client_id!r}')

    # M38: not wire-testable (requires knowledge of all clients on subnet) — skipped.

    # --- M39: PRL consistency ---
    disc_prl = get_option(discover, 'param_req_list')
    req_prl = get_option(request, 'param_req_list')

    if disc_prl is not None:
        assert req_prl is not None, \
            'M39: PRL (option 55) present in DISCOVER but absent in REQUEST'
        # Compare as sets — order may differ
        assert set(disc_prl) == set(req_prl), \
            (f'M39: PRL in DISCOVER {sorted(disc_prl)} != '
             f'PRL in REQUEST {sorted(req_prl)}')
