# Copyright (C) 2026 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Scapy-based scriptable mock DHCPv4 server for client compliance testing.

The mock server listens on UDP port 67 using Scapy's AsyncSniffer and sends
controlled responses via sendp().  Captured client packets are appended to
world.client_pkts for later inspection by test assertions.

Requires CAP_NET_RAW or root on the Forge machine.
"""

import logging
import socket
import struct
import threading
import time

from scapy.all import (
    AsyncSniffer,
    BOOTP,
    DHCP,
    Ether,
    IP,
    UDP,
    sendp,
    get_if_hwaddr,
)

from src.forge_cfg import world

log = logging.getLogger('forge')

# DHCP option 53 message-type values
DISCOVER = 1
OFFER = 2
REQUEST = 3
DECLINE = 4
ACK = 5
NAK = 6
RELEASE = 7
INFORM = 8


class MockDHCP4Server:
    """Scriptable mock DHCPv4 server that captures client packets.

    :param iface: local interface to sniff/send on (Forge-side)
    :param server_ip: IP address the mock server presents as its own
    :param pool_start: first IP to offer (incremented per unique chaddr)
    :param lease_time: default lease time in seconds
    :param t1: T1 renewal time in seconds (default: lease_time // 2)
    :param t2: T2 rebinding time in seconds (default: lease_time * 7 // 8)
    :param response_policy: dict mapping DHCP msg-type int ->
        'offer', 'ack', 'nak', or 'silence'.  Missing keys use defaults.
    """

    def __init__(self, iface, server_ip, pool_start='192.1.2.100',
                 lease_time=3600, t1=None, t2=None, response_policy=None):
        self.iface = iface
        self.server_ip = server_ip
        self.pool_start = pool_start
        self.lease_time = lease_time
        self.t1 = t1 if t1 is not None else lease_time // 2
        self.t2 = t2 if t2 is not None else lease_time * 7 // 8
        self.response_policy = response_policy or {}
        self._sniffer = None
        self._lock = threading.Lock()
        self._seen_pkts = {}  # (xid, msg_type) -> timestamp
        self._offered = {}   # chaddr -> offered IP
        self._pool_counter = self._ip_to_int(pool_start)
        self._server_mac = get_if_hwaddr(iface)
        self._captured_pkts = []  # Thread-safe list for captured packets

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def start(self):
        """Start the AsyncSniffer on port 67."""
        # Initialize world.client_pkts to point to our instance list
        world.client_pkts = self._captured_pkts
        self._sniffer = AsyncSniffer(
            iface=[self.iface, 'lo'],
            filter='arp or (udp and dst port 67)',
            prn=self._handle,
            store=False,
        )
        self._sniffer.start()
        # Give the sniffer a moment to open the socket
        time.sleep(0.2)
        log.info('MockDHCP4Server started on %s+lo (%s)', self.iface, self.server_ip)

    def stop(self):
        """Stop the AsyncSniffer."""
        if self._sniffer is not None:
            self._sniffer.stop()
            self._sniffer.join()
            self._sniffer = None
        log.info('MockDHCP4Server stopped')

    def set_policy(self, policy):
        """Update response policy mid-test.

        :param policy: dict mapping DHCP message-type integers to actions.
            Keys are integers (1=DISCOVER, 3=REQUEST, …).
            Values are 'offer', 'ack', 'nak', or 'silence'.

        Example: server.set_policy({REQUEST: 'silence'})
        """
        self.response_policy.update(policy)

    def set_lease_params(self, lease_time=None, t1=None, t2=None):
        """Change lease timing parameters mid-test."""
        if lease_time is not None:
            self.lease_time = lease_time
        if t1 is not None:
            self.t1 = t1
        if t2 is not None:
            self.t2 = t2

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _handle(self, pkt):
        """Classify an incoming packet and optionally reply."""
        if not (pkt.haslayer(BOOTP) and pkt.haslayer(DHCP)):
            return
        dhcp_opts = {opt[0]: opt[1] for opt in pkt[DHCP].options
                     if isinstance(opt, (list, tuple)) and len(opt) >= 2}
        msg_type = dhcp_opts.get('message-type')
        if msg_type is None:
            return

        now = time.time()
        with self._lock:
            key = (pkt[BOOTP].xid, msg_type)
            last_seen = self._seen_pkts.get(key, 0)
            if now - last_seen < 1.0:
                # Arrived on both interfaces within 1 second -> it's a loopback duplicate
                return
            self._seen_pkts[key] = now
            self._captured_pkts.append(pkt)

        log.debug('MockDHCP4Server received msg_type=%d from %s',
                  msg_type, pkt[BOOTP].chaddr.hex())

        action = self.response_policy.get(msg_type)

        if msg_type == DISCOVER:
            if action == 'silence':
                return
            self._send_offer(pkt, dhcp_opts)

        elif msg_type == REQUEST:
            if action == 'silence':
                return
            if action == 'nak':
                self._send_nak(pkt)
            else:
                self._send_ack(pkt, dhcp_opts)

        elif msg_type == INFORM:
            if action == 'silence':
                return
            self._send_inform_ack(pkt, dhcp_opts)

        # DECLINE, RELEASE — just record, no reply needed

    def _allocate_ip(self, chaddr):
        """Return (possibly cached) offered IP for this chaddr."""
        key = chaddr.hex() if isinstance(chaddr, bytes) else chaddr
        if key not in self._offered:
            self._offered[key] = self._int_to_ip(self._pool_counter)
            self._pool_counter += 1
        return self._offered[key]

    def _send_offer(self, req_pkt, dhcp_opts):
        offered_ip = self._allocate_ip(req_pkt[BOOTP].chaddr)
        pkt = self._build_response(
            req_pkt,
            msg_type=OFFER,
            yiaddr=offered_ip,
            extra_opts=[
                ('lease_time', self.lease_time),
                ('renewal_time', self.t1),
                ('rebinding_time', self.t2),
                ('server_id', self.server_ip),
            ],
        )
        sendp(pkt, iface=self.iface, verbose=False)
        log.debug('MockDHCP4Server sent OFFER %s', offered_ip)

    def _send_ack(self, req_pkt, dhcp_opts):
        # Use the requested IP if present, otherwise fall back to offered
        requested_ip = dhcp_opts.get('requested_addr')
        if not requested_ip:
            requested_ip = self._allocate_ip(req_pkt[BOOTP].chaddr)
        pkt = self._build_response(
            req_pkt,
            msg_type=ACK,
            yiaddr=requested_ip,
            extra_opts=[
                ('lease_time', self.lease_time),
                ('renewal_time', self.t1),
                ('rebinding_time', self.t2),
                ('server_id', self.server_ip),
            ],
        )
        sendp(pkt, iface=self.iface, verbose=False)
        log.debug('MockDHCP4Server sent ACK %s', requested_ip)

    def _send_nak(self, req_pkt):
        pkt = self._build_response(
            req_pkt,
            msg_type=NAK,
            yiaddr='0.0.0.0',
            extra_opts=[('server_id', self.server_ip)],
        )
        sendp(pkt, iface=self.iface, verbose=False)
        log.debug('MockDHCP4Server sent NAK')

    def _send_inform_ack(self, req_pkt, dhcp_opts):
        """ACK for DHCPINFORM — no lease time options per RFC 2131 §4.4.3."""
        pkt = self._build_response(
            req_pkt,
            msg_type=ACK,
            yiaddr='0.0.0.0',
            extra_opts=[
                ('server_id', self.server_ip),
                ('domain', 'test.example'),
            ],
        )
        sendp(pkt, iface=self.iface, verbose=False)
        log.debug('MockDHCP4Server sent INFORM-ACK')

    def _build_response(self, req_pkt, msg_type, yiaddr, extra_opts=None):
        """Build a DHCP response packet."""
        extra_opts = extra_opts or []
        dhcp_options = [('message-type', msg_type)] + extra_opts + [('end',)]

        # Determine destination: broadcast unless client has an IP
        ciaddr = req_pkt[BOOTP].ciaddr
        if ciaddr and ciaddr != '0.0.0.0':
            dst_ip = ciaddr
            dst_mac = req_pkt[Ether].src
        else:
            dst_ip = '255.255.255.255'
            dst_mac = 'ff:ff:ff:ff:ff:ff'

        pkt = (
            Ether(src=self._server_mac, dst=dst_mac) /
            IP(src=self.server_ip, dst=dst_ip) /
            UDP(sport=67, dport=68) /
            BOOTP(
                op=2,
                xid=req_pkt[BOOTP].xid,
                yiaddr=yiaddr,
                siaddr=self.server_ip,
                chaddr=req_pkt[BOOTP].chaddr,
                giaddr=req_pkt[BOOTP].giaddr,
            ) /
            DHCP(options=dhcp_options)
        )
        return pkt

    @staticmethod
    def _ip_to_int(ip):
        return struct.unpack('!I', struct.pack('4B', *map(int, ip.split('.'))))[0]

    @staticmethod
    def _int_to_ip(n):
        return '.'.join(str(b) for b in struct.pack('!I', n))
