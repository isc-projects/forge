# Copyright (C) 2026 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""S01-S14: DHCP client SHOULD requirement compliance tests.

SHOULD failures emit warnings via warnings.warn() — they do NOT cause test
failures.  All warnings are visible in the pytest summary via:
    filterwarnings = always::UserWarning  (in pytest.ini)
"""

import time
import warnings

import pytest

from scapy.all import ARP, AsyncSniffer

from src.clientsupport.mock_server import DISCOVER, REQUEST, DECLINE, INFORM
from src.clientsupport.packet_inspector import (
    filter_by_type,
    first_of_type,
    get_bootp_field,
    get_option,
    get_ip_dst,
    has_option,
    inter_packet_gaps,
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


# ---------------------------------------------------------------------------
# S01: Initial random delay
# ---------------------------------------------------------------------------

@pytest.mark.timing_sensitive
def test_initial_delay(mock_server, dhcp_client):
    """S01: Client SHOULD wait 1-10 seconds before sending first DHCPDISCOVER."""
    from src.forge_cfg import world

    # Record time just before the client was started (dhcp_client fixture
    # calls start() after flush; we approximate with time.time() here)
    start_time = time.time()
    discover = _wait_for(world.client_pkts, DISCOVER, timeout=20)
    if discover is None:
        warnings.warn('[SHOULD S01] No DHCPDISCOVER received — cannot measure initial delay',
                      UserWarning)
        return

    delay = discover.time - start_time
    if not (1.0 <= delay <= 10.0):
        warnings.warn(
            f'[SHOULD S01] Initial DISCOVER delay is {delay:.2f}s; '
            f'RFC 2131 §4.4.1 recommends 1-10 seconds',
            UserWarning,
        )


# ---------------------------------------------------------------------------
# S02: Maximum DHCP Message Size option
# ---------------------------------------------------------------------------

def test_max_msg_size_option(mock_server, dhcp_client):
    """S02: Client SHOULD include option 57 (Maximum DHCP Message Size)."""
    from src.forge_cfg import world

    discover = _wait_for(world.client_pkts, DISCOVER)
    if discover is None:
        warnings.warn('[SHOULD S02] No DHCPDISCOVER received', UserWarning)
        return

    if not has_option(discover, 'max_dhcp_size'):
        warnings.warn(
            '[SHOULD S02] Option 57 (Maximum DHCP Message Size) not present in DISCOVER; '
            'RFC 2131 §3.5 recommends including it',
            UserWarning,
        )


# ---------------------------------------------------------------------------
# S03: ARP check before accepting offered address
# ---------------------------------------------------------------------------

def test_arp_check_before_accept(mock_server, dhcp_client):
    """S03: Client SHOULD perform ARP check on offered address before accepting."""
    from src.forge_cfg import world

    iface = world.f_cfg.iface
    arp_probes = []

    def capture_arp(pkt):
        if pkt.haslayer(ARP) and pkt[ARP].op == 1:
            arp_probes.append(pkt)

    arp_sniffer = AsyncSniffer(iface=iface, filter='arp', prn=capture_arp, store=False)
    arp_sniffer.start()

    try:
        request = _wait_for(world.client_pkts, REQUEST)
        time.sleep(1)
    finally:
        arp_sniffer.stop()
        arp_sniffer.join()

    if not arp_probes:
        warnings.warn(
            '[SHOULD S03] No ARP probe observed before DHCPREQUEST; '
            'RFC 2131 §4.4.1 recommends probing the offered address',
            UserWarning,
        )


# ---------------------------------------------------------------------------
# S04: Gratuitous ARP after ACK
# ---------------------------------------------------------------------------

def test_gratuitous_arp_after_ack(mock_server, dhcp_client):
    """S04: After DHCPACK, client SHOULD broadcast ARP announcement."""
    from src.forge_cfg import world

    iface = world.f_cfg.iface
    garp_seen = []

    def capture_garp(pkt):
        if pkt.haslayer(ARP) and pkt[ARP].op == 2:  # ARP reply
            if pkt[ARP].psrc == pkt[ARP].pdst:      # gratuitous
                garp_seen.append(pkt)

    # Wait for REQUEST first (ACK follows shortly)
    request = _wait_for(world.client_pkts, REQUEST)

    arp_sniffer = AsyncSniffer(iface=iface, filter='arp', prn=capture_garp, store=False)
    arp_sniffer.start()
    try:
        time.sleep(3)
    finally:
        arp_sniffer.stop()
        arp_sniffer.join()

    if not garp_seen:
        warnings.warn(
            '[SHOULD S04] No gratuitous ARP observed after DHCPACK; '
            'RFC 2131 §4.4.1 recommends broadcasting an ARP announcement',
            UserWarning,
        )


# ---------------------------------------------------------------------------
# S05: Delay after DHCPDECLINE before restarting
# ---------------------------------------------------------------------------

@pytest.mark.timing_sensitive
def test_decline_restart_delay(mock_server, dhcp_client):
    """S05: Client SHOULD wait at least 10 seconds after DHCPDECLINE before restarting."""
    from src.forge_cfg import world
    from scapy.all import Ether, sendp

    iface = world.f_cfg.iface

    discover = _wait_for(world.client_pkts, DISCOVER)
    if discover is None:
        warnings.warn('[SHOULD S05] No DHCPDISCOVER received', UserWarning)
        return

    offered_ip = mock_server._allocate_ip(get_bootp_field(discover, 'chaddr'))

    # Inject ARP conflict to trigger DECLINE
    conflict_mac = 'de:ad:be:ef:00:02'
    from scapy.all import ARP
    arp_conflict = (
        Ether(src=conflict_mac, dst='ff:ff:ff:ff:ff:ff') /
        ARP(op=2, hwsrc=conflict_mac, psrc=offered_ip,
            hwdst='ff:ff:ff:ff:ff:ff', pdst=offered_ip)
    )
    sendp(arp_conflict, iface=iface, verbose=False)

    decline = _wait_for(world.client_pkts, DECLINE, timeout=10)
    if decline is None:
        warnings.warn('[SHOULD S05] No DHCPDECLINE observed — cannot measure restart delay',
                      UserWarning)
        return

    decline_time = decline.time
    n_before = len(world.client_pkts)

    # Wait for the next DISCOVER
    next_discover = None
    deadline = time.time() + 30
    while time.time() < deadline:
        new_discovers = filter_by_type(world.client_pkts[n_before:], DISCOVER)
        if new_discovers:
            next_discover = new_discovers[0]
            break
        time.sleep(0.2)

    if next_discover is None:
        warnings.warn('[SHOULD S05] No DHCPDISCOVER after DECLINE — cannot measure restart delay',
                      UserWarning)
        return

    restart_delay = next_discover.time - decline_time
    if restart_delay < 10.0:
        warnings.warn(
            f'[SHOULD S05] Client restarted {restart_delay:.1f}s after DECLINE; '
            f'RFC 2131 §3.1 recommends waiting at least 10 seconds',
            UserWarning,
        )


# ---------------------------------------------------------------------------
# S06-S07: Broadcast flag behaviour
# ---------------------------------------------------------------------------

def test_broadcast_flag_behavior(mock_server, dhcp_client):
    """S06-S07: Observe and optionally validate the broadcast flag in DISCOVER."""
    from src.forge_cfg import world

    discover = _wait_for(world.client_pkts, DISCOVER)
    if discover is None:
        warnings.warn('[SHOULD S06/S07] No DHCPDISCOVER received', UserWarning)
        return

    flags = get_bootp_field(discover, 'flags')
    broadcast_bit_set = bool(flags & 0x8000)
    observed = 'set' if broadcast_bit_set else 'clear'

    # Always log the observed value
    hint_raw = getattr(world.f_cfg, 'client_broadcasts_flag', '')
    hint = hint_raw.lower().strip() if hint_raw else ''

    if hint == 'true':
        if not broadcast_bit_set:
            warnings.warn(
                f'[SHOULD S06] Broadcast flag is {observed} but CLIENT_BROADCASTS_FLAG=true; '
                f'RFC 2131 §4.1: client that cannot receive unicast SHOULD set broadcast flag',
                UserWarning,
            )
    elif hint == 'false':
        if broadcast_bit_set:
            warnings.warn(
                f'[SHOULD S07] Broadcast flag is {observed} but CLIENT_BROADCASTS_FLAG=false; '
                f'RFC 2131 §4.1: client that can receive unicast SHOULD clear broadcast flag',
                UserWarning,
            )
    else:
        # No hint — just log
        warnings.warn(
            f'[SHOULD S06/S07] DISCOVER broadcast flag is {observed} '
            f'(flags=0x{int(flags):04x}). Set CLIENT_BROADCASTS_FLAG to "true" or "false" '
            f'in init_all.py to enable comparison.',
            UserWarning,
        )


# ---------------------------------------------------------------------------
# S08-S09: Initial retransmission timing
# ---------------------------------------------------------------------------

@pytest.mark.timing_sensitive
def test_retransmission_timing(mock_server, dhcp_client):
    """S08-S09: First retransmission delay ~4s; subsequent delays should double."""
    from src.forge_cfg import world

    # Silence responses so we can observe retransmissions
    mock_server.set_policy({DISCOVER: 'silence'})

    # Collect at least 4 DISCOVERs
    deadline = time.time() + 4 + 8 + 16 + 20
    while time.time() < deadline:
        if len(filter_by_type(world.client_pkts, DISCOVER)) >= 4:
            break
        time.sleep(0.5)

    gaps = inter_packet_gaps(world.client_pkts, DISCOVER)
    if len(gaps) < 1:
        warnings.warn('[SHOULD S08] Not enough DISCOVERs to measure retransmission timing',
                      UserWarning)
        return

    # S08: first gap should be ~4s (±1s)
    first_gap = gaps[0]
    if not (3.0 <= first_gap <= 5.0):
        warnings.warn(
            f'[SHOULD S08] First retransmission gap is {first_gap:.1f}s; '
            f'RFC 2131 §4.1 recommends 4s ± 1s random jitter',
            UserWarning,
        )

    # S09: subsequent gaps should approximately double (up to 64s)
    for i in range(1, len(gaps)):
        prev = gaps[i - 1]
        curr = gaps[i]
        expected = min(prev * 2, 64)
        lo = expected * 0.5
        hi = expected * 1.5
        if not (lo <= curr <= hi):
            warnings.warn(
                f'[SHOULD S09] Retransmission gap {i + 1} is {curr:.1f}s; '
                f'expected ~{expected:.0f}s (doubling from {prev:.1f}s)',
                UserWarning,
            )


# ---------------------------------------------------------------------------
# S10-S11: Renewal/rebinding retry timing
# ---------------------------------------------------------------------------

@pytest.mark.timing_sensitive
def test_renew_rebind_retry_timing(mock_server, dhcp_client):
    """S10-S11: In RENEWING/REBINDING, retry interval should be half remaining
    time to T2/expiry (minimum 60 seconds).

    Uses a long lease (≥ 240s, T2 ≥ 180s) to make the 60s minimum exercisable.
    """
    from src.forge_cfg import world

    lease_time = 300
    t1 = 120
    t2 = 240
    mock_server.set_lease_params(lease_time=lease_time, t1=t1, t2=t2)

    ctrl = dhcp_client

    # Complete initial DORA
    request = _wait_for(world.client_pkts, REQUEST)
    if request is None:
        warnings.warn('[SHOULD S10/S11] No initial REQUEST received', UserWarning)
        return

    # Trigger renewal
    if ctrl.has_renew_cmd():
        n_before = len(world.client_pkts)
        ctrl.renew()
    else:
        # Wait for T1
        time.sleep(t1 + 2)
        n_before = len(world.client_pkts)

    # Silence renewal responses so client retransmits
    mock_server.set_policy({REQUEST: 'silence'})

    # Collect at least 2 renewal REQUESTs
    deadline = time.time() + 180
    while time.time() < deadline:
        renew_reqs = filter_by_type(world.client_pkts[n_before:], REQUEST)
        if len(renew_reqs) >= 2:
            break
        time.sleep(1)

    renew_reqs = filter_by_type(world.client_pkts[n_before:], REQUEST)
    if len(renew_reqs) < 2:
        warnings.warn(
            '[SHOULD S10] Not enough renewal REQUESTs to measure retry interval',
            UserWarning,
        )
        return

    gap = renew_reqs[1].time - renew_reqs[0].time
    # Expected: half remaining time to T2, minimum 60s
    # With T2=240s and T1=120s, remaining time to T2 at T1 is ~120s → expected ~60s
    if gap < 60:
        warnings.warn(
            f'[SHOULD S10] RENEWING retry interval is {gap:.1f}s; '
            f'RFC 2131 §4.4.5 recommends half remaining time to T2 (minimum 60s)',
            UserWarning,
        )


# ---------------------------------------------------------------------------
# S12: New address notification after expiry
# ---------------------------------------------------------------------------

def test_expiry_new_address_notification(mock_server, dhcp_client):
    """S12: After expiry + new ACK with different address, client SHOULD NOT
    continue using the old address."""
    from src.forge_cfg import world

    # Use a very short lease
    mock_server.set_lease_params(lease_time=12, t1=5, t2=9)

    request = _wait_for(world.client_pkts, REQUEST)
    if request is None:
        warnings.warn('[SHOULD S12] No initial REQUEST received', UserWarning)
        return

    old_ip = get_option(request, 'requested_addr')

    # Silence responses to let lease expire, then offer a new address
    mock_server.set_policy({REQUEST: 'silence'})
    time.sleep(14)  # past expiry

    # Change the pool so the next OFFER gives a different IP
    mock_server._pool_counter += 10
    mock_server.set_policy({REQUEST: 'ack'})

    # Wait for new REQUEST
    n_before = len(world.client_pkts)
    deadline = time.time() + 15
    new_req = None
    while time.time() < deadline:
        new_reqs = filter_by_type(world.client_pkts[n_before:], REQUEST)
        if new_reqs:
            new_req = new_reqs[0]
            break
        time.sleep(0.2)

    if new_req is None:
        warnings.warn('[SHOULD S12] Client did not restart after lease expiry', UserWarning)
        return

    new_ip = get_option(new_req, 'requested_addr')
    if new_ip == old_ip:
        warnings.warn(
            f'[SHOULD S12] Client is still requesting old address {old_ip!r} '
            f'after lease expiry; RFC 2131 §4.4.5 recommends not reusing it',
            UserWarning,
        )


# ---------------------------------------------------------------------------
# S13: Reacquire on boot
# ---------------------------------------------------------------------------

def test_reacquire_on_boot(mock_server, dhcp_client):
    """S13: Client SHOULD use DHCP to reacquire/verify address at system boot."""
    from src.forge_cfg import world

    # The dhcp_client fixture already started the client fresh.
    # We simply verify the first packet is a DISCOVER or INIT-REBOOT REQUEST.
    deadline = time.time() + _TIMEOUT
    first_pkt = None
    while time.time() < deadline:
        if world.client_pkts:
            first_pkt = world.client_pkts[0]
            break
        time.sleep(0.1)

    if first_pkt is None:
        warnings.warn(
            '[SHOULD S13] No DHCP packets observed after client start; '
            'RFC 2131 §3.7 recommends reacquiring address on boot',
            UserWarning,
        )
        return

    from src.clientsupport.mock_server import DISCOVER, REQUEST
    from src.clientsupport.packet_inspector import get_msg_type
    msg_type = get_msg_type(first_pkt)
    if msg_type not in (DISCOVER, REQUEST):
        warnings.warn(
            f'[SHOULD S13] First packet after boot is message-type {msg_type}, '
            f'expected DISCOVER (1) or REQUEST (3); '
            f'RFC 2131 §3.7 recommends using DHCP on boot',
            UserWarning,
        )


# ---------------------------------------------------------------------------
# S14: DHCPINFORM should not request lease time parameters
# ---------------------------------------------------------------------------

def test_inform_no_lease_time_params(mock_server, dhcp_client):
    """S14: Client SHOULD NOT request lease time parameters in DHCPINFORM."""
    from src.forge_cfg import world

    ctrl = dhcp_client

    # Trigger DHCPINFORM — skips if CLIENT_INFORM_CMD is not configured
    ctrl.inform()
    time.sleep(2)

    informs = filter_by_type(world.client_pkts, INFORM)
    if not informs:
        warnings.warn('[SHOULD S14] No DHCPINFORM observed after CLIENT_INFORM_CMD',
                      UserWarning)
        return

    inform_pkt = informs[0]

    # Check for lease time options: 51 (lease_time), 58 (renewal_time), 59 (rebinding_time)
    lease_opts = {
        'lease_time': 51,
        'renewal_time': 58,
        'rebinding_time': 59,
    }
    for opt_name in lease_opts:
        if has_option(inform_pkt, opt_name):
            warnings.warn(
                f'[SHOULD S14] DHCPINFORM contains option {opt_name!r}; '
                f'RFC 2131 §4.4.3 recommends not requesting lease time parameters',
                UserWarning,
            )
