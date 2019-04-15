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
import logging
from random import randint

from scapy.all import get_if_raw_hwaddr, Ether, srp
from scapy.config import conf
from scapy.fields import Field
from scapy.layers.dhcp import BOOTP, DHCP, DHCPOptions
from scapy.packet import Raw
from scapy.layers.inet import IP, UDP
from scapy.packet import fuzz
from scapy.sendrecv import send, sendp, sniff

from forge_cfg import world
from protosupport.v6.srv_msg import client_add_saved_option, change_message_field, apply_message_fields_changes


log = logging.getLogger('forge')


def client_requests_option(opt_type):
    if not hasattr(world, 'prl'):
        world.prl = ""  # don't request anything by default
    world.prl += chr(int(opt_type))  # put a single byte there


def client_send_msg(msgname, iface, addr):
    """
    Sends specified message with defined options.
    Parameters:
    msg ('<msg> message'): name of the message.
    num_opts: number of options to send.
    opt_type: option type
    """
    # set different ethernet interface then default one.
    if iface is not None:
        world.cfg["iface"] = iface
        world.cfg["srv4_addr"] = addr

    world.climsg = []
    options = world.cliopts

    if hasattr(world, 'prl') and len(world.prl) > 0:
        if conf.version == '2.2.0-dev':
            options += [("param_req_list", str(world.prl))]
        else:
            options += [("param_req_list", [ord(o) for o in world.prl])]
#     else:
#         assert False, "No PRL defined"

    # What about messages: "force_renew","lease_query",
    # "lease_unassigned","lease_unknown","lease_active",
    # messages from server: offer, ack, nak

    if msgname == "DISCOVER":
        # msg code: 1
        # world.cfg["values"]["broadcastBit"] = True
        msg = build_msg([("message-type", "discover")] + options)

    elif msgname == "REQUEST":
        # msg code: 3
        msg = build_msg([("message-type", "request")] + options)

    elif msgname == "DECLINE":
        # msg code: 4
        msg = build_msg([("message-type", "decline")] + options)

    elif msgname == "RELEASE":
        # msg code: 7
        msg = build_msg([("message-type", "release")] + options)

    elif msgname == "INFORM":
        # msg code: 8
        msg = build_msg([("message-type", "inform")] + options)

    elif msgname == "BOOTP_REQUEST":
        msg = build_msg(options)

    else:
        assert False, "Invalid message type: %s" % msgname

    assert msg, "Failed to create " + msgname

    if msg:
        world.climsg.append(msg)

    log.debug("Message %s will be sent over %s interface." % (msgname, world.cfg["iface"]))


def client_sets_value(value_name, new_value):
    if value_name in world.cfg["values"]:
        if isinstance(world.cfg["values"][value_name], str):
            world.cfg["values"][value_name] = str(new_value)
        elif isinstance(world.cfg["values"][value_name], int):
            world.cfg["values"][value_name] = int(new_value)
        else:
            world.cfg["values"][value_name] = new_value
    else:
        assert value_name in world.cfg["values"], "Unknown value name : %s" % value_name


def convert_flags_fqdn():
    flag_filed = 0
    if 'N' in world.cfg["values"]["FQDN_flags"]:
        flag_filed += 8
    if 'E' in world.cfg["values"]["FQDN_flags"]:
        flag_filed += 4
    if 'O' in world.cfg["values"]["FQDN_flags"]:
        flag_filed += 2
    if 'S' in world.cfg["values"]["FQDN_flags"]:
        flag_filed += 1
    return flag_filed


options_formatted_by_forge = ["vendor_specific",  # code 43
                              "pxe_client_machine_identifier",  # code 82
                              "relay_agent_information"  # code 97
                              ]


def client_does_include(sender_type, opt_type, value):
    if opt_type == 'client_id':
        # code - 61
        world.cliopts += [(opt_type, convert_MAC(value))]
#     elif opt_type =='vendor_class_id':
#         world.cliopts += [(opt_type, str(value), "my-other-class")]
    elif opt_type == 'fqdn':
        # code - 81
        flags = chr(int(convert_flags_fqdn()))
        # flags, RCODE1, RCODE2, domain name
        # RCODE1 and RCODE2 are deprecated but we need to add them.
        if 'E' not in world.cfg["values"]["FQDN_flags"]:
            fqdn = (flags + '\x00\x00' + world.cfg["values"]["FQDN_domain_name"])
        else:
            domain = "".join(map(lambda z: chr(len(z))+z, world.cfg["values"]["FQDN_domain_name"].split('.')))
            fqdn = (flags + '\x00\x00' + domain)
        world.cliopts += [('client_FQDN', fqdn)]
    elif opt_type == 'pxe_client_architecture':
        # code - 93
        world.cliopts += [(opt_type, '\00' + chr(int(value)))]
    elif opt_type == 'pxe_client_network_interface':
        # code - 94
        world.cliopts += [(opt_type, chr(int(value[0])) + chr(int(value[1])) + chr(int(value[2])))]
    elif opt_type in options_formatted_by_forge:
        world.cliopts += [(opt_type, "".join(map(lambda z: chr(int(z, 16)), list(value))))]
    elif opt_type in ["vendor_specific_information", "vendor_class"]:
        world.cliopts += [(opt_type, value.decode("hex"))]
    else:
        try:
            world.cliopts += [(opt_type, str(value))]
        except UnicodeEncodeError:
            world.cliopts += [(opt_type, unicode(value))]


def response_check_content(expect, data_type, expected):

    if data_type == 'yiaddr':
        received = world.srvmsg[0].yiaddr
    elif data_type == 'ciaddr':
        received = world.srvmsg[0].ciaddr
    elif data_type == 'siaddr':
        received = world.srvmsg[0].siaddr
    elif data_type == 'giaddr':
        received = world.srvmsg[0].giaddr
    elif data_type == 'src_address':
        received = world.srvmsg[0].src
    elif data_type == 'chaddr':
        pass
        # TODO: implement this!
        received = world.srvmsg[0].chaddr  # decode!!
    elif data_type == 'sname':
        received = world.srvmsg[0].sname.replace('\x00', '')
    elif data_type == 'file':
        received = world.srvmsg[0].file.replace('\x00', '')

    else:
        assert False, "Value %s is not supported" % data_type

    # because we are using function to parse full option not just value
    # I did little hack, added 'value:' as option code, and changed assertion message
    outcome, received = test_option(0, ['value:', received], expected)

    if expect is None:
        assert outcome, "Invalid {data_type} received {received}" \
                        " but expected: {expected}.".format(**locals())
    else:
        assert not outcome, "Invalid {data_type} received {received}" \
                            " that value has been excluded from correct values.".format(**locals())
    return received


def client_save_option(opt_name, count=0):
    opt_code = world.kea_options4.get(opt_name)

    assert opt_name in world.kea_options4, "Unsupported option name " + opt_name

    if count not in world.savedmsg:
        world.savedmsg[count] = [get_option(world.srvmsg[0], opt_code)]
    else:
        world.savedmsg[count].append(get_option(world.srvmsg[0], opt_code))


def client_copy_option(opt_name):
    opt_code = world.kea_options4.get(opt_name)

    assert opt_name in world.kea_options4, "Unsupported option name " + opt_name

    received = get_option(world.srvmsg[0], opt_code)
    world.cliopts.append(received)


def convert_MAC(mac):
    # convert MAC address to hex representation
    return mac.replace(':', '').decode('hex')


def start_fuzzing():  # time_period, time_units):
    world.fuzzing = True


def build_msg(opts):
    conf.checkIPaddr = False
    msg_flag = 0
    import sys
    if sys.platform != "darwin":
        fam, hw = get_if_raw_hwaddr(str(world.cfg["iface"]))
    else:
        # TODO fix this for MAC OS, this is temporary quick fix just for my local system
        hw = convert_MAC("0a:00:27:00:00:00")
    tmp_hw = None

    # we need to choose if we want to use chaddr, or client id.
    # also we can include both: client_id and chaddr
    if world.cfg["values"]["chaddr"] is None or world.cfg["values"]["chaddr"] == "default":
        tmp_hw = hw
    elif world.cfg["values"]["chaddr"] == "empty":
        tmp_hw = convert_MAC("00:00:00:00:00:00")
    else:
        tmp_hw = convert_MAC(world.cfg["values"]["chaddr"])

    if world.cfg["values"]["broadcastBit"]:
        # value for setting 1000 0000 0000 0000 in bootp message in field 'flags' for broadcast msg.
        msg_flag = 32768
    else:
        msg_flag = 0

    msg = Ether(dst="ff:ff:ff:ff:ff:ff",
                src=hw)
    msg /= IP(src=world.cfg["source_IP"],
              dst=world.cfg["destination_IP"],)
    msg /= UDP(sport=world.cfg["source_port"], dport=world.cfg["destination_port"])
    msg /= BOOTP(chaddr=tmp_hw,
                 giaddr=world.cfg["values"]["giaddr"],
                 flags=msg_flag,
                 hops=world.cfg["values"]["hops"])

    # BOOTP requests can be optionless
    if len(opts) > 0:
        opts += ["end"]  # end option
        msg /= DHCP(options=opts)

    #transaction id
    if world.cfg["values"]["tr_id"] is None:
        msg.xid = randint(0, 256*256*256)
    else:
        msg.xid = int(world.cfg["values"]["tr_id"])
    world.cfg["values"]["tr_id"] = msg.xid

    msg.siaddr = world.cfg["values"]["siaddr"]
    msg.ciaddr = world.cfg["values"]["ciaddr"]
    msg.yiaddr = world.cfg["values"]["yiaddr"]
    msg.htype = world.cfg["values"]["htype"]
    return msg


def get_msg_type(msg):

    msg_types = {1: "DISCOVER",
                 2: "OFFER",
                 3: "REQUEST",
                 4: "DECLINE",
                 5: "ACK",
                 6: "NAK",
                 7: "RELEASE",
                 8: "INFORM"
                 }
    # option 53 it's message type
    opt = get_option(msg, 53)

    # BOOTP_REPLYs have no message type
    if opt is None:
        return "BOOTP_REPLY"

    # opt[1] it's value of message-type option
    for msg_code in msg_types.keys():
        if opt[1] == msg_code:
            return msg_types[msg_code]

    return "UNKNOWN-TYPE"


def send_wait_for_message(msgtype, presence, exp_message):
    """
    Block until the given message is (not) received.
    """
    # We need to use srp() here (send and receive on layer 2)

    apply_message_fields_changes()
    ans, unans = srp(world.climsg,
                     iface=world.cfg["iface"],
                     timeout=world.cfg["wait_interval"],
                     multi=True,
                     verbose=99)

    if world.f_cfg.show_packets_from in ['both', 'client']:
        world.climsg[0].show()
        print('\n')

    expected_type_found = False

    received_names = ""
    world.cliopts = []
    world.srvmsg = []
    for x in ans:
        a, b = x
        world.srvmsg.append(b)
        if world.f_cfg.show_packets_from in ['both', 'server']:
            b.show()
            print('\n')

        received_names = get_msg_type(b) + " " + received_names
        if get_msg_type(b) == exp_message:
            expected_type_found = True

    log.debug("Received traffic (answered/unanswered): %d/%d packet(s)."
                              % (len(ans), len(unans)))
    if exp_message != "None":
        for x in unans:
            log.error(("Unanswered packet type = %s" % get_msg_type(x)))

        if presence:
            assert len(world.srvmsg) != 0, "No response received."
            assert expected_type_found, "Expected message " + exp_message + " not received (got " + received_names + ")"
        elif not presence:
            assert len(world.srvmsg) == 0, "Response received, not expected"
        assert presence == bool(world.srvmsg), "No response received."
    else:
        assert len(world.srvmsg) == 0, "Response message " + received_names + "received but none message expected."
        # TODO: make assertion for receiving message that not suppose to come!

    return world.srvmsg


def get_option(msg, opt_code):
    # Returns option of specified type
    # We need to iterate over all options and see
    # if there's one we're looking for
    world.opts = []
    opt_name = DHCPOptions[int(opt_code)]
    # dhcpv4 implementation in Scapy is a mess. The options array contains mix of
    # strings, IPField, ByteEnumField and who knows what else. In each case the
    # values are accessed differently
    if isinstance(opt_name, Field):
        opt_name = opt_name.name

    x = msg.getlayer(4)  # 0th is Ethernet, 1 is IPv4, 2 is UDP, 3 is BOOTP, 4 is DHCP options
    # BOOTP messages may be optionless, so check first
    if x is not None:
        for opt in x.options:
            if opt[0] is opt_name:
                world.opts.append(opt)
                return opt
    return None


def ByteToHex(byteStr):
    return ''.join(["%02X " % ord(x) for x in byteStr]).replace(" ", "")


def test_option(opt_code, received, expected):
    tmp = ""

    decode_opts_byte_to_hex = [61, 76]

    if opt_code in decode_opts_byte_to_hex or expected[:4] == "HEX:":
        received = received[0], ByteToHex(received[1])

    decode_opts_hex_to_int = [76]
    if opt_code in decode_opts_hex_to_int:
        received = received[0], int(str(received[1]), 16)

    if expected[:4] == "HEX:":
        expected = expected[4:]

    for each in received:
        tmp += str(each) + ' '
        if str(each) == expected:
            return True, each
    return False, tmp


def _get_opt_descr(opt_code):
    opt = DHCPOptions[int(opt_code)]
    if isinstance(opt, str):
        opt_descr = "%s[%s]" % (opt, opt_code)
    else:
        opt_descr = "%s[%s]" % (opt.name, opt_code)
    return opt_descr


def response_check_include_option(expected, opt_code):
    assert len(world.srvmsg) != 0, "No response received."
    opt = get_option(world.srvmsg[0], opt_code)

    opt_descr = _get_opt_descr(opt_code)

    if expected:
        assert opt, "Expected option {opt_descr} not present in the message.".format(**locals())
    else:
        assert opt is None, "Expected option {opt_descr} present in the message. But not expected!".format(**locals())


def response_check_option_content(opt_code, expect, data_type, expected):
    # expect == None when we want that content and NOT when we dont want! that's messy correct that!
    assert len(world.srvmsg) != 0, "No response received."

    opt_code = int(opt_code)
    received = get_option(world.srvmsg[0], opt_code)

    # FQDN is being parsed different way because of scapy imperfections
    if opt_code == 81:
        tmp = received[0]
        if data_type == 'flags':
            received = tmp, int(ByteToHex(received[1][0]), 16)
        elif data_type == 'fqdn':
            received = tmp, received[1][3:]
        else:
            assert False, "In option 81 you can look only for: 'fqdn' or 'flags'."

        # assert False, bytes(received[1][0])

    outcome, received = test_option(opt_code, received, expected)

    opt_descr = _get_opt_descr(opt_code)

    if expect is None:
        assert outcome, "Invalid {opt_descr} option received: {received} but expected {expected}".format(**locals())
    else:
        assert not outcome, "Invalid {opt_descr} option received: {received}" \
                            " that value has been excluded from correct values".format(**locals())
