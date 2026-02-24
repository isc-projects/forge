# Copyright (C) 2026 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""M42-M43: DHCPINFORM compliance tests."""

import time

import pytest

from scapy.all import UDP

from src.clientsupport.mock_server import INFORM
from src.clientsupport.packet_inspector import (
    filter_by_type,
    get_option,
    has_option,
)

pytestmark = [pytest.mark.v4, pytest.mark.client_compliance]

_TIMEOUT = 10


def test_inform_port_and_no_opt50(mock_server, dhcp_client):
    """M42-M43: DHCPINFORM must be directed to UDP port 67 and must not
    include option 50 (Requested IP Address).
    """
    from src.forge_cfg import world

    ctrl = dhcp_client

    # Trigger DHCPINFORM — skips if CLIENT_INFORM_CMD is not configured
    ctrl.inform()
    time.sleep(2)

    informs = filter_by_type(world.client_pkts, INFORM)
    assert informs, \
        'M42: No DHCPINFORM packet received after triggering CLIENT_INFORM_CMD'

    inform_pkt = informs[0]

    # M42: must be directed to UDP port 67
    assert inform_pkt.haslayer(UDP), 'DHCPINFORM packet has no UDP layer'
    dport = inform_pkt[UDP].dport
    assert dport == 67, \
        f'M42: DHCPINFORM must be sent to UDP port 67, got port {dport}'

    # M43: must NOT include option 50 (Requested IP Address)
    assert not has_option(inform_pkt, 'requested_addr'), \
        'M43: DHCPINFORM must NOT include option 50 (Requested IP Address)'
