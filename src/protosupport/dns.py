# Copyright (C) 2013-2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Wlodzimierz Wencel

# pylint: disable=consider-using-f-string
# pylint: disable=invalid-name
# pylint: disable=redefined-builtin
# pylint: disable=unused-argument
# pylint: disable=unused-variable

import time
import secrets
import logging
from locale import str

from scapy.all import sr
from scapy.layers import dns
from scapy.layers.inet import IP, UDP
from scapy.layers.dhcp6 import IPv6
from scapy.packet import Packet
from src.forge_cfg import world


log = logging.getLogger('forge')


dnstypes = {"ANY": 0,
            "ALL": 255,
            "A": 1,
            "NS": 2,
            "MD": 3,
            # "MD": 4,
            "CNAME": 5,
            "SOA": 6,
            "MB": 7,
            "MG": 8,
            "MR": 9,
            "NULL": 10,
            "WKS": 11,
            "PTR": 12,
            "HINFO": 13,
            "MINFO": 14,
            "MX": 15,
            "TXT": 16,
            "RP": 17,
            "AFSDB": 18,
            "AAAA": 28,
            "SRV": 33,
            "A6": 38,
            "DNAME": 39,
            "IXFR": 251,
            "AXFR": 252,
            "MAILB": 253,
            "MAILA": 254}

dnsclasses = {"IN": 1,
              "CS": 2,
              "CH": 3,
              "HS": 4,
              "ANY": 255}

op_codes = {"QUERY": 0,
            "IQUERY": 1,
            "STATUS": 2}

r_codes = {"OK": 0,
           "FORMAT-ERROR": 1,
           "SERVER-FAILURE": 2,
           "NAME-ERROR": 3,
           "NOT-IMPLEMENTED": 4,
           "REFUSED": 5}


def prepare_query(dns_addr=None, dns_port=None):
    world.climsg = []
    build_query()
    build_msg(dns_addr, dns_port)


def send_wait_for_query(choose_must, expect_include, iface=None):
    world.climsg[0].id = secrets.randbelow(65535)
    if iface is None:
        iface = world.cfg["dns_iface"]

    if world.f_cfg.show_packets_from in ['both', 'client']:
        world.climsg[0].show()

    timeout = world.cfg["wait_interval"] + world.dns_send_query_time_out

    log.info('sending DNS query, attempt %d/%d, timeout %.1f',
             world.dns_send_query_counter,
             world.f_cfg.dns_retry,
             timeout)

    ans, _ = sr(world.climsg,
                iface=iface,
                timeout=timeout,
                multi=True,
                verbose=99)

    world.dns_send_query_counter += 1
    world.dns_send_query_time_out += 0.5

    world.dns_qd = []
    world.dns_an = []
    world.dns_ns = []
    world.dns_ar = []

    world.srvmsg = []

    for x in ans:
        a, b = x
        world.srvmsg.append(b.getlayer(2))
        if world.f_cfg.show_packets_from in ['both', 'server'] and len(world.srvmsg) > 0:
            if isinstance(world.srvmsg[0], Packet):
                world.srvmsg[0].show()

    if expect_include:
        # if message was not received but expected, resend query with higher timeout
        if len(world.srvmsg) == 0 and world.dns_send_query_counter <= world.f_cfg.dns_retry:
            time.sleep(1)
            send_wait_for_query(choose_must, expect_include, iface=iface)
        else:
            assert len(world.srvmsg) != 0, "No response received."

    elif not expect_include:
        assert len(world.srvmsg) == 0, "Response received, not expected"

    msg = world.srvmsg[0]

    assert hasattr(msg, 'qd'), 'qd field not present in DNS response'
    if msg.qd is not None:
        for each in msg.qd:
            world.dns_qd.append(each.copy())

    assert hasattr(msg, 'an'), 'an field not present in DNS response'
    if msg.an is not None:
        for each in msg.an:
            world.dns_an.append(each.copy())

    assert hasattr(msg, 'ns'), 'ns field not present in DNS response'
    if msg.ns is not None:
        for each in msg.ns:
            world.dns_ns.append(each.copy())

    assert hasattr(msg, 'ar'), 'ar field not present in DNS response'
    if msg.ar is not None:
        for each in msg.ar:
            world.dns_ar.append(each.copy())


def build_query():
    # TODO all those should have ability to be set from test level
    world.dns_send_query_counter = 0  # let's put counter to zero for each new query
    world.dns_send_query_time_out = 0.5
    msg = dns.DNS(id=1,
                  qr=0,
                  opcode="QUERY",
                  aa=0,
                  tc=0,
                  rd=0,
                  ra=0,
                  z=0,
                  rcode="ok",
                  qdcount=1,
                  ancount=0,
                  nscount=0,
                  arcount=0)
    # if there will be need we could build here answers, authoritative_nameservers and additional_records.
    if hasattr(world, 'question_record'):
        msg.qd = world.question_record

    world.dns_query = msg


def dns_question_record(addr, my_qtype, my_qclass):
    assert my_qtype in dnstypes, "Unsupported question type " + my_qtype
    dnstype_code = dnstypes.get(my_qtype)

    assert my_qclass in dnsclasses, "Unsupported question type " + my_qclass
    dnsclass_code = dnsclasses.get(my_qclass)

    world.question_record = dns.DNSQR(qname=addr, qtype=dnstype_code, qclass=dnsclass_code)


def build_msg(dns_addr=None, dns_port=None):
    if dns_port is None:
        dns_port = world.cfg["dns_port"]

    if dns_addr is None:
        if world.proto == "v6":
            dns_addr = world.cfg["dns6_addr"]
        else:
            dns_addr = world.cfg["dns4_addr"]

    # this is now bit more complicated, normally we had v6 DNS traffic in v6 tests, for AD we need to have v4 traffic
    # in v6 tests. So instead checking world.proto we will check address itself
    if "." in dns_addr:
        msg = IP(dst=dns_addr)
    else:
        msg = IPv6(dst=dns_addr)

    msg /= UDP(sport=dns_port, dport=dns_port)
    world.climsg.append(msg/world.dns_query)


def check_dns_respond(expect, data_type, expected_data_value):
    if data_type == 'opcode':
        data_type = op_codes.get(data_type)
        received = world.srvmsg[0].opcode

    elif data_type == 'rcode':
        data_type = r_codes.get(data_type)
        received = world.srvmsg[0].rcode

    else:
        try:
            received = getattr(world.srvmsg[0], data_type.lower())
        except AttributeError:
            assert False, "There is no value named: {data_type}".format(**locals())

    if expected_data_value.isnumeric():
        expected_data_value = int(expected_data_value)

    flag = 0
    if expected_data_value == received:
        flag = 1  # if we found what we were looking for change flag to 1

    if expect and flag == 0:
        assert False, "Invalid {data_type} received {received} but expected: {expected_data_value}.".format(**locals())

    if not expect and flag == 1:
        assert False, "Invalid {data_type} received {received} that" \
                      " value has been excluded from correct values.".format(**locals())


def _resend_query(exp, name):
    time.sleep(3)
    send_wait_for_query('MUST', True)
    check_dns_option(exp, name)


def report_dns_option(flag, expect_include, name):
    if flag and not expect_include:
        if world.dns_send_query_counter <= world.f_cfg.dns_retry:
            _resend_query(False, name)
        else:
            assert False, 'In received DNS query part: "{name}" is NOT empty as we expected.'.format(**locals())

    elif not flag and expect_include:
        # this is where we had huge amount of failures on jenkins, let's bring here retries.
        if world.dns_send_query_counter <= world.f_cfg.dns_retry:
            _resend_query(True, name)
        else:
            assert False, 'In received DNS query part: "{name}" is empty.'.format(**locals())


def check_dns_option(expect_include, part_name):
    flag = 0
    if part_name == 'QUESTION':
        if len(world.dns_qd) > 0:
            flag = 1

    elif part_name == 'ANSWER':
        if len(world.dns_an) > 0:
            flag = 1

    elif part_name == 'AUTHORITATIVE_NAMESERVERS':
        if len(world.dns_ns) > 0:
            flag = 1

    elif part_name == 'ADDITIONAL_RECORDS':
        if len(world.dns_ar) > 0:
            flag = 1

    report_dns_option(flag, expect_include, part_name)


def parsing_received_parts(query_part_list, length, expect, value_name, value):
    outcome = ""
    for number in range(length):
        try:
            test = getattr(query_part_list[number], value_name.lower())
        except AttributeError:
            assert False, "There is no value named: {value_name}".format(**locals())

        if isinstance(test, int):
            test = str(test)

        if isinstance(test, bytes):
            test = test.decode('utf-8')

        if test == value:
            return 1, test
        outcome = outcome + test + ' '
    return 0, outcome


def dns_option_content(part_name, expect, value_name, value):
    if part_name == 'QUESTION':
        flag, outcome = parsing_received_parts(world.srvmsg[0].qd, world.srvmsg[0].qdcount, expect, value_name, value)

    elif part_name == 'ANSWER':
        flag, outcome = parsing_received_parts(world.srvmsg[0].an, world.srvmsg[0].ancount, expect, value_name, value)

    elif part_name == 'AUTHORITATIVE_NAMESERVERS':
        flag, outcome = parsing_received_parts(world.srvmsg[0].ns, world.srvmsg[0].nscount, expect, value_name, value)

    elif part_name == 'ADDITIONAL_RECORDS':
        flag, outcome = parsing_received_parts(world.srvmsg[0].ar, world.srvmsg[0].arcount, expect, value_name, value)
    else:
        assert False, f"No support implemented for: {part_name}"

    if not flag and expect:
        assert False, f'In received DNS query part: "{value_name}" there is/are values:' \
                      f' {outcome} expected was: {value}'
    elif flag and not expect:
        assert False, f'In received DNS query part: "{value_name}" there is value:' \
                      f' {outcome} which was forbidden to show up.'
