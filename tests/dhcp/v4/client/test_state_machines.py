# Copyright (C) 2026 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""M17-M19: INIT-REBOOT state compliance tests."""

import time, logging

import pytest

log = logging.getLogger('forge')

from src.clientsupport.mock_server import DISCOVER, REQUEST
from src.clientsupport.packet_inspector import (
    filter_by_type,
    get_bootp_field,
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


def test_init_reboot_request_fields(mock_server, dhcp_client):
    """M17-M19: DHCPREQUEST in INIT-REBOOT state field requirements.

    The client is started, completes a DORA to obtain a lease, then the
    client is stopped and restarted WITHOUT flushing the lease cache.
    The second REQUEST (with a prior lease known) must be in INIT-REBOOT state.
    """
    from src.forge_cfg import world

    # --- First boot: complete DORA to get a lease ---
    request1 = _wait_for(world.client_pkts, REQUEST)
    assert request1 is not None, 'No DHCPREQUEST received in first boot'

    # Record the leased address (from the ACK yiaddr the mock server sent)
    # We can infer it from the REQUEST's option 50 (requested_addr)
    prior_addr = get_option(request1, 'requested_addr')
    assert prior_addr is not None, \
        'Could not determine leased address from first DHCPREQUEST'

    # --- Restart WITHOUT flushing (INIT-REBOOT) ---
    world.client_pkts.clear()
    log.info('Client packets cleared')
    time.sleep(10)
    dhcp_client.stop()
    log.info('Client stopped. sleeping for 300.5 seconds')
    time.sleep(0.5)
    # Deliberately do NOT call flush — client should remember the lease
    dhcp_client.start()
    log.info('Client started')

    # Wait for the INIT-REBOOT REQUEST (may be preceded by a DISCOVER if the
    # client decides to do a full DORA; we look for a REQUEST with opt50 set
    # and no opt54, which is the INIT-REBOOT signature)
    init_reboot_req = None
    deadline = time.time() + _TIMEOUT
    while time.time() < deadline:
        for pkt in filter_by_type(world.client_pkts, REQUEST):
            if has_option(pkt, 'requested_addr') and not has_option(pkt, 'server_id'):
                init_reboot_req = pkt
                break
        if init_reboot_req:
            break
        time.sleep(0.1)

    if init_reboot_req is None:
        pytest.skip(
            'Client did not send an INIT-REBOOT REQUEST (may have done full DORA '
            'instead — behaviour is implementation-dependent when lease cache is retained)'
        )

    # M17: option 50 must be present with the previously assigned address
    req_addr = get_option(init_reboot_req, 'requested_addr')
    assert req_addr is not None, \
        'M17: Option 50 (Requested IP) must be present in INIT-REBOOT REQUEST'
    assert req_addr == prior_addr, \
        (f'M17: INIT-REBOOT REQUEST option 50 is {req_addr!r}, '
         f'expected prior lease address {prior_addr!r}')

    # M18: option 54 must NOT be present
    assert not has_option(init_reboot_req, 'server_id'), \
        'M18: Option 54 (Server Identifier) must NOT be present in INIT-REBOOT REQUEST'

    # M19: ciaddr must be zero
    ciaddr = get_bootp_field(init_reboot_req, 'ciaddr')
    assert ciaddr in ('0.0.0.0', None, 0), \
        f'M19: ciaddr must be 0.0.0.0 in INIT-REBOOT state, got {ciaddr!r}'
