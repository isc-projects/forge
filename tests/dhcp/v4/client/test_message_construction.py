# Copyright (C) 2026 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""M01-M08: DHCP client message construction compliance tests."""

import time

import pytest

from scapy.all import BOOTP, DHCP

from src.clientsupport.mock_server import DISCOVER
from src.clientsupport.packet_inspector import (
    filter_by_type,
    first_of_type,
    get_bootp_field,
    get_option,
    has_option,
)

pytestmark = [pytest.mark.v4, pytest.mark.client_compliance]

# Magic cookie value defined in RFC 2131
DHCP_MAGIC_COOKIE = b'\x63\x82\x53\x63'


def _wait_for_discover(pkts, timeout=5):
    """Poll world.client_pkts until a DISCOVER arrives or timeout."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        matches = filter_by_type(pkts, DISCOVER)
        if matches:
            return matches[0]
        time.sleep(0.1)
    return None


@pytest.mark.usefixtures('mock_server_and_client')
def test_magic_cookie_and_msg_type(mock_server_and_client):
    """M01-M03: option 53 present, magic cookie correct, END option present."""
    from src.forge_cfg import world
    srv, _ = mock_server_and_client
    pkt = _wait_for_discover(world.client_pkts)
    assert pkt is not None, 'No DHCPDISCOVER received from client'

    # M01: option 53 must be present
    assert has_option(pkt, 'message-type'), \
        'M01: DHCP option 53 (message-type) not present in DISCOVER'

    # M02: magic cookie
    raw_bootp = bytes(pkt[BOOTP])
    # The magic cookie occupies bytes 236-240 of the BOOTP payload
    cookie = raw_bootp[236:240]
    assert cookie == DHCP_MAGIC_COOKIE, \
        f'M02: Magic cookie {cookie.hex()} != expected 63825363'

    # M03: END option (255) must be the last option
    opts = pkt[DHCP].options
    assert opts[-1] == 'end', \
        f'M03: Last DHCP option must be END (255), got {opts[-1]!r}'


@pytest.mark.usefixtures('mock_server_and_client')
def test_flags_reserved_bits_zero(mock_server_and_client):
    """M04: Reserved bits in the flags field must be zero."""
    from src.forge_cfg import world
    srv, _ = mock_server_and_client
    pkt = _wait_for_discover(world.client_pkts)
    assert pkt is not None, 'No DHCPDISCOVER received from client'

    flags = get_bootp_field(pkt, 'flags')
    reserved = flags & 0x7FFF
    assert reserved == 0, \
        f'M04: Reserved bits in flags must be 0, got flags=0x{flags:04x}'


@pytest.mark.usefixtures('mock_server_and_client')
def test_chaddr_populated(mock_server_and_client):
    """M05: Client must include its hardware address in chaddr."""
    from src.forge_cfg import world
    srv, _ = mock_server_and_client
    pkt = _wait_for_discover(world.client_pkts)
    assert pkt is not None, 'No DHCPDISCOVER received from client'

    chaddr = get_bootp_field(pkt, 'chaddr')
    # chaddr is 16 bytes; first 6 should be non-zero for Ethernet
    assert chaddr[:6] != b'\x00' * 6, \
        'M05: chaddr must contain the client hardware address (all zeros found)'


@pytest.mark.usefixtures('mock_server_and_client')
def test_op_bootrequest(mock_server_and_client):
    """M06: op field must be BOOTREQUEST (1) in all client messages."""
    from src.forge_cfg import world
    srv, _ = mock_server_and_client
    pkt = _wait_for_discover(world.client_pkts)
    assert pkt is not None, 'No DHCPDISCOVER received from client'

    op = get_bootp_field(pkt, 'op')
    assert op == 1, f'M06: BOOTP op must be 1 (BOOTREQUEST), got {op}'


@pytest.mark.usefixtures('mock_server_and_client')
def test_hops_zero(mock_server_and_client):
    """M07: hops must be set to 0 by the client."""
    from src.forge_cfg import world
    srv, _ = mock_server_and_client
    pkt = _wait_for_discover(world.client_pkts)
    assert pkt is not None, 'No DHCPDISCOVER received from client'

    hops = get_bootp_field(pkt, 'hops')
    assert hops == 0, f'M07: hops must be 0, got {hops}'


def test_option_overload_handling(mock_server, dhcp_client):
    """M08: Client must correctly process option overload in server responses.

    The mock server sends an OFFER with option 52 (file/sname overload) where
    the server-id is placed in the sname field.  The client must parse the
    overloaded sname and send a REQUEST using the correct server-id.
    """
    from src.forge_cfg import world
    from scapy.all import Ether, IP, UDP, BOOTP, DHCP, sendp, get_if_hwaddr
    from src.clientsupport.mock_server import OFFER, REQUEST, ACK

    # Override the mock server's DISCOVER handler to send an overloaded OFFER
    server_ip = world.f_cfg.srv4_addr
    iface = world.f_cfg.iface
    server_mac = get_if_hwaddr(iface)
    # Capture the list object now — world is thread-local and won't be accessible
    # from the sniffer's background thread.
    client_pkts = world.client_pkts

    def overloaded_offer_handler(pkt):
        from src.clientsupport.packet_inspector import get_msg_type
        msg_type = get_msg_type(pkt)
        if msg_type is None:
            return
        client_pkts.append(pkt)
        if msg_type == DISCOVER:
            # Build OFFER with option 52=2 (sname field contains options)
            # Place server-id in sname as raw bytes (option 54 + len + IP)
            import socket
            import struct
            sid_bytes = socket.inet_aton(server_ip)
            # option 54 (server identifier), length 4, then IP
            sname_opts = bytes([54, 4]) + sid_bytes + bytes([255])
            sname_padded = sname_opts.ljust(64, b'\x00')

            offered_ip = '192.168.50.50'
            reply = (
                Ether(src=server_mac, dst='ff:ff:ff:ff:ff:ff') /
                IP(src=server_ip, dst='255.255.255.255') /
                UDP(sport=67, dport=68) /
                BOOTP(
                    op=2,
                    xid=pkt[BOOTP].xid,
                    yiaddr=offered_ip,
                    siaddr=server_ip,
                    chaddr=pkt[BOOTP].chaddr,
                    sname=sname_padded,
                ) /
                DHCP(options=[
                    ('message-type', OFFER),
                    ('lease_time', 3600),
                    ('dhcp-option-overload', 2),  # 2 = sname field contains options
                    'end',
                ])
            )
            sendp(reply, iface=iface, verbose=False)

    mock_server.stop()
    from scapy.all import AsyncSniffer
    sniffer = AsyncSniffer(
        iface=[iface, 'lo'],
        filter='udp and port 67',
        prn=overloaded_offer_handler,
        store=False,
    )
    sniffer.start()
    import time
    time.sleep(0.2)

    try:
        dhcp_client.stop()
        time.sleep(1)
        dhcp_client.flush()
        time.sleep(0.3)
        dhcp_client.start()
        # Wait for REQUEST
        deadline = time.time() + 10
        req_pkt = None
        while time.time() < deadline:
            reqs = filter_by_type(client_pkts, REQUEST)
            if reqs:
                req_pkt = reqs[0]
                break
            time.sleep(0.2)
    finally:
        if getattr(sniffer, 'running', False):
            try:
                sniffer.stop()
                sniffer.join()
            except Exception:  # noqa: BLE001
                pass

    assert req_pkt is not None, \
        'M08: Client did not send DHCPREQUEST after receiving overloaded OFFER'

    # The client must have parsed the server-id from the sname field
    sid = get_option(req_pkt, 'server_id')
    assert sid == server_ip, \
        (f'M08: Client REQUEST server_id {sid!r} does not match the server-id '
         f'embedded in the overloaded sname field ({server_ip!r})')
