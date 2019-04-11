# Copyright (C) 2013-2017 Internet Systems Consortium.
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND INTERNET SYSTEMS CONSORTIUM
# DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# INTERNET SYSTEMS CONSORTIUM BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
# FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
# WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# Author: Wlodzimierz Wencel

import sys
from locale import str
import random

from scapy.all import sr
from scapy.layers import dns
from scapy.layers.inet import IP, UDP
from scapy.layers.dhcp6 import IPv6

from forge_cfg import world


dnstypes = {"ANY": 0,
            "ALL": 255,
            "A": 1,
            "NS": 2,
            "MD": 3,
            #"MD": 4,
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


def prepare_query():
    world.climsg = []
    build_query()
    build_msg()


def send_wait_for_query(choose_must, presence):
    if world.f_cfg.show_packets_from in ['both', 'client']:
            world.climsg[0].show()

    ans, unans = sr(world.climsg,
                    iface=world.cfg["dns_iface"],
                    timeout=world.cfg["wait_interval"],
                    multi=True,
                    verbose=99)

    world.dns_qd = []
    world.dns_an = []
    world.dns_ns = []
    world.dns_ar = []

    world.srvmsg = []
    world.climsg = []

    for x in ans:
        a, b = x
        world.srvmsg.append(b.getlayer(2))

        if world.f_cfg.show_packets_from in ['both', 'server']:
            try:  # that is temp solution until we have good respond system checking!
                world.srvmsg[0].show()
            except:
                pass

    if presence:
        assert len(world.srvmsg) != 0, "No response received."
        # TODO testing should be more sophisticated, it's not working for dns queries
        # TODO make assertion for getting message that we didn't expected

    elif not presence:
        assert len(world.srvmsg) == 0, "Response received, not expected"

    if world.srvmsg[0].qd is not None:
        for each in world.srvmsg[0].qd:
            world.dns_qd.append(each.copy())

    if world.srvmsg[0].an is not None:
        for each in world.srvmsg[0].an:
            world.dns_an.append(each.copy())

    if world.srvmsg[0].ns is not None:
        for each in world.srvmsg[0].ns:
            world.dns_ns.append(each.copy())

    if world.srvmsg[0].ar is not None:
        for each in world.srvmsg[0].ar:
            world.dns_ar.append(each.copy())


def build_query():
    # TODO all those should have ability to be set from test level
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


def build_msg():
    if world.proto == "v6":
        msg = IPv6(dst=world.cfg["dns6_addr"])/UDP(sport=world.cfg["dns_port"], dport=world.cfg["dns_port"])
    else:
        msg = IP(dst=world.cfg["dns4_addr"])/UDP(sport=world.cfg["dns_port"], dport=world.cfg["dns_port"])
    msg.trid = random.randint(0, 256*256*256)
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

    if expect is None and flag == 0:
        assert False, "Invalid {data_type} received {received} but expected: {expected_data_value}.".format(**locals())

    if expect is not None and flag == 1:
        assert False, "Invalid {data_type} received {received} that" \
                      " value has been excluded from correct values.".format(**locals())


def report_dns_option(flag, expect_empty, name):
    if flag and expect_empty is None:
        assert False, 'In received DNS query part: "{name}" is NOT empty as we expected.'.format(**locals())

    elif not flag and expect_empty is not None:
        assert False, 'In received DNS query part: "{name}" is empty.'.format(**locals())


def check_dns_option(expect_empty, part_name):
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

    report_dns_option(flag, expect_empty, part_name)


def parsing_received_parts(query_part_list, length, expect, value_name, value):
    outcome = ""
    for number in range(length):
        try:
            test = getattr(query_part_list[number], value_name.lower())
        except AttributeError:
            assert False, "There is no value named: {value_name}".format(**locals())

        if isinstance(test, int):
            test = str(test)

        if test == value:
            return 1, test
        outcome = outcome + test + ' '
    else:
        return 0, outcome


def dns_option_content(part_name, expect, value_name, value):
    flag = 0
    if part_name == 'QUESTION':
        flag, outcome = parsing_received_parts(world.srvmsg[0].qd, world.srvmsg[0].qdcount, expect, value_name, value)

    elif part_name == 'ANSWER':
        flag, outcome = parsing_received_parts(world.srvmsg[0].an, world.srvmsg[0].ancount, expect, value_name, value)

    elif part_name == 'AUTHORITATIVE_NAMESERVERS':
        flag, outcome = parsing_received_parts(world.srvmsg[0].ns, world.srvmsg[0].nscount, expect, value_name, value)

    elif part_name == 'ADDITIONAL_RECORDS':
        flag, outcome = parsing_received_parts(world.srvmsg[0].ar, world.srvmsg[0].arcount, expect, value_name, value)

    if not flag and expect is None:
        assert False, 'In received DNS query part: "{value_name}" there is/are values:' \
                      ' {outcome} expected was: {value}'.format(**locals())
    elif flag and expect is not None:
        assert False, 'In received DNS query part: "{value_name}" there is value:' \
                      ' {outcome} which was forbidden to show up.'.format(**locals())
