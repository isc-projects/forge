# Copyright (C) 2012-2013 Internet Systems Consortium.
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

#
# This file contains a number of common steps that are general and may be used
# By a lot of feature files.
#

from lettuce import *
import os
import sys
import random
import scapy
from scapy.sendrecv import send,sendp,sniff
from scapy.all import *
from scapy.layers.dhcp6 import *

#IPv6,UDP,DHCP6

#change later for non global
IRID = random.randint(0, 256*256*256)
SRV_DUID = None


@step('Client requests option (\d+).')
def client_requests_option(step, opt_type):
    # TODO: check if ORO is not there yet
    if not hasattr(world, 'oro'):
        # There was no ORO at all, create new one
        world.oro = DHCP6OptOptReq()
        # Scapy creates ORO with 23, 24 options request. Let's get rid of them
        world.oro.reqopts = [] # don't request anything by default
    world.oro.reqopts.append(int(opt_type))

@step('Client sends (\w+) message( with (\w+) option)?')
def client_send_msg(step, msgname, opt_type, unknown):
    """
    Sends specified message with defined options.
    Parameters:
    msg ('<msg> message'): name of the message.
    num_opts: number of options to send.
    opt_type: option type
    """
    msg = None

    if (msgname == "SOLICIT"):
        msg = create_solicit(IRID)
    elif (msgname == "REQUEST"):
        msg = create_request(IRID)
    elif (msgname == "renew"):
        msg = create_renew()
    elif (msgname == "rebind"):
        msg = create_rebind()
    elif (msgname == "release"):
        msg = create_release()
    elif (msgname == "decline"):
        msg = create_decline()
    elif (msgname == "confirm"):
        msg = create_confirm()
    elif (msgname == "infrequest"):
        msg = create_infrequest()
    else:
        assert False, "Invalid message type: %s" % msgname
    

    if (world.oro is not None):
        msg = add_option(msg, world.oro)

#    if msg:
#        world.climsg.append(msg) 
    if msg:
        world.climsg = msg  
    print("IRID %d" %IRID)
    print("Message %s will be sent over %s interface." % (msgname, world.cfg["iface"]))

def add_option(msg, option):
    msg /= option
    return msg

@step('Server MUST (NOT )?respond with (\w+) message')
def send_wait_for_message(step, yes_or_no, message):
    """
    Block until the given message is (not) received.
    Parameter:
    new: (' new', optional): Only check the output printed since last time
                             this step was used for this process.
    process_name ('<name> stderr'): Name of the process to check the output of.
    message ('message <message>'): Output (part) to wait for.
    not_message ('not <message>'): Output (part) to wait for, and fail
    Fails if the message is not found after 10 seconds.
    """

    ans,unans = sr(world.climsg, iface=world.cfg["iface"], timeout=2, multi=True, verbose=1)
    print "ans:"
    ans.show()
    print "\nunans:"
    unans.show()
    world.srvmsg = []
    for x in ans:
        a,b = x
        world.srvmsg.append(b)
        
    print("Received traffic (answered/unanswered): %d/%d packet(s)." % (len(ans), len(unans)))

    if yes_or_no == None:
        assert len(world.srvmsg) != 0, "No response received."
    else:
        pass

# Returns option of specified type
def get_option(msg, opt_code):
    # We need to iterate over all options and see
    # if there's one we're looking for
    x = msg.getlayer(3) # 0th is IPv6, 1st is UDP, 2nd is DHCP6, 3rd is the first option
    while x:
        if x.optcode == int(opt_code):
            return x
        x = x.payload
    return None

@step('Response MUST (NOT )?include option (\d+).')
def response_check_include_option(step, yes_or_no, opt_code):

    assert len(world.srvmsg) != 0, "No response received."

    opt = get_option(world.srvmsg[0], opt_code)

    assert opt, "Expected option " + opt_code + " not present in the message."


# Returns text represenation of the option, interpreted as specified by data_type
def unknown_option_to_str(data_type, opt):
    if data_type=="uint8":
        assert len(opt.data) == 1, "Received option " + opt.optcode + " contains " + len(opt.data) + \
                                   " bytes, but expected exactly 1"
        return str(ord(opt.data[0:1]))
    else:
        assert False, "Parsing of option format " + data_type + " not implemented."

# Option 23 MUST contain addresses 2001:db8::1,2001:db8::2
@step('Response option (\d+) MUST (NOT )?contain (\S+) (\S+).')
def response_check_option_content(step, opt_code, expect, data_type, expected):

    opt_code = int(opt_code)

    assert len(world.srvmsg) != 0, "No response received."

    x = get_option(world.srvmsg[0], opt_code)

    assert x, "Expected option " + opt_code + " not present in the message."

    received = ""
    if opt_code == 7:
        received = str(x.prefval)
    elif opt_code == 21:
        received = ",".join(x.sipdomains)
    elif opt_code == 22:
        received = ",".join(x.sipservers)
    elif opt_code == 23:
        received = ",".join(x.dnsservers)
    elif opt_code == 24:
        received = ",".join(x.dnsdomains)
    elif opt_code == 27:
        received = ",".join(x.nisservers)
    elif opt_code == 28:
        received = ",".join(x.nispservers)
    elif opt_code == 29:
        received = x.nisdomain
    elif opt_code == 30:
        received = x.nispdomain
    elif opt_code == 31:
        received = ",".join(x.sntpservers)
    elif opt_code == 32:
        received = str(x.reftime)
    else:
        received = unknown_option_to_str(data_type, x)

    assert expected == received, "Invalid " + opt_code + " option received:" + received + \
                                 ", but expected " + expected

def receive_dhcp6_tcpdump(count = 1, timeout = 1):

    args = ["tcpdump", "-i", world.cfg["iface"], "-c", str(count), "-w", "test.pcap", "ip6"]
    print("Running tcpdump for %d seconds:" % timeout,)
    print(args)
    tcpdump = subprocess.Popen(args)
    time.sleep(timeout)
    tcpdump.terminate()

    ans = sniff(count=5, filter="ip6", offline="test.pcap", promisc=True, timeout=3)
    print("Received traffic: %d packet(s)." % len(ans))
    assert len(ans) != 0, "No response received."
    for x in ans:
        x.show()

def create_solicit(trid):
    x = IPv6(dst=All_DHCP_Relay_Agents_and_Servers)/UDP(sport=546, dport=547)/DHCP6_Solicit()
    x.trid = trid
    clientid = DHCP6OptClientId(duid = world.cfg["cli_duid"])
    ia = DHCP6OptIA_NA(iaid = 1)
    x /= clientid
    x /= ia

    return x

def create_request(trid):
    x = IPv6(dst=All_DHCP_Relay_Agents_and_Servers)/UDP(sport=546, dport=547)/DHCP6_Request()
    x.trid = trid
    clientid = DHCP6OptClientId(duid = world.cfg["cli_duid"])
    ia = DHCP6OptIA_NA(iaid = 1)
    x /= clientid
    x /= ia

    return x
