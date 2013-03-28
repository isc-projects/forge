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

from cookielib import debug
from lettuce.decorators import step
from lettuce.registry import world
from scapy.config import conf
from scapy.layers.dhcp6 import *
from scapy.layers.inet import UDP
from scapy.layers.inet6 import IPv6
from scapy.sendrecv import sr


# @todo: this is a copy of the same list from serversupport.kea6.functions
# The following line doesn't seem to work as it gives the following error:
# ValueError: Attempted relative import in non-package
# from ...serversupport.kea6.functions import kea_options6
# For now, the kea_options6 is just duplicated here.
kea_options6 = { "client-id": 1,
                 "server-id" : 2,
                 "IA_NA" : 3,
                 "IA_address" : 5,
                 "preference": 7,
                 "sip-server-dns": 21,
                 "sip-server-addr": 22,
                 "dns-servers": 23,
                 "domain-search": 24,
                 "nis-servers": 27,
                 "nisp-servers": 28,
                 "nis-domain-name": 29,
                 "nisp-domain-name": 30,
                 "sntp-servers": 31,
                 "information-refresh-time": 32 }


    
def client_requests_option(step, opt_type):
    if not hasattr(world, 'oro'):
        # There was no ORO at all, create new one
        world.oro = DHCP6OptOptReq()
        # Scapy creates ORO with 23, 24 options request. Let's get rid of them
        world.oro.reqopts = [] # don't request anything by default

    world.oro.reqopts.append(int(opt_type))
    world.cfg["client_id"] = True
# @step('Client sends (\w+) message( with (\w+) option)?')
def client_send_msg(step, msgname, opt_type, unknown):
    """
    Sends specified message with defined options.
    Parameters:
    msg ('<msg> message'): name of the message.
    num_opts: number of options to send.
    opt_type: option type
    """

    # Remove previous message waiting to be sent, just in case this is a
    # REQUEST after we received ADVERTISE. We don't want to send SOLICIT
    # the second time.
    world.climsg = []
    world.cfg["client_id"] = True
    
    if (msgname == "SOLICIT"):
        """
        RFC 3315 15.2 
        Servers MUST discard any Solicit messages that do not include a
        Client Identifier option or that do include a Server Identifier
        option.
        """
        msg = msg_add_defaults(DHCP6_Solicit())
        if (world.oro is not None):
                msg = add_option_to_msg(msg, world.oro)
        
    elif (msgname == "REQUEST"):
        """
        RFC 3315 15.4 
        Servers MUST discard any received Request message that meet any of
        the following conditions:
           -  the message does not include a Server Identifier option.
           -  the contents of the Server Identifier option do not match the
              server's DUID.
           -  the message does not include a Client Identifier option.
        """
        msg = msg_add_defaults(DHCP6_Request())
        if (world.oro is not None):
                msg = add_option_to_msg(msg, world.oro)
        
    elif (msgname == "CONFIRM"):
        """
        RFC 3315 15.5 
        Servers MUST discard any received Confirm messages that do not
        include a Client Identifier option or that do include a Server
        Identifier option.
        """
        msg = msg_add_defaults(DHCP6_Confirm())
        
    elif (msgname == "RENEW"):
        """
        RFC 3315 15.6
        Servers MUST discard any received Renew message that meets any of the
        following conditions:
           -  the message does not include a Server Identifier option.
           -  the contents of the Server Identifier option does not match the
              server's identifier.
           -  the message does not include a Client Identifier option.
        """
        msg = msg_add_defaults(DHCP6_Renew())
        
    elif (msgname == "REBIND"):
        """
        RFC 3315 15.7
        Servers MUST discard any received Rebind messages that do not include
        a Client Identifier option or that do include a Server Identifier
        option.
        """
        msg = msg_add_defaults(DHCP6_Rebind())

    elif (msgname == "DECLINE"):
        """
        RFC 3315 15.8
        Servers MUST discard any received Decline message that meets any of
        the following conditions:
           -  the message does not include a Server Identifier option.
           -  the contents of the Server Identifier option does not match the
              server's identifier.
           -  the message does not include a Client Identifier option.
        """
        msg = msg_add_defaults(DHCP6_Decline())
                
    elif (msgname == "RELEASE"):
        """
        RFC 3315 15.9
        Servers MUST discard any received Release message that meets any of
        the following conditions:
           -  the message does not include a Server Identifier option.
           -  the contents of the Server Identifier option does not match the
              server's identifier.
           -  the message does not include a Client Identifier option.
        """
        msg = msg_add_defaults(DHCP6_Release())
        
    elif (msgname == "INFREQUEST"):
        """
        RFC 3315 15.12
        Servers MUST discard any received Information-request message that
        meets any of the following conditions:
           -  The message includes a Server Identifier option and the DUID in
              the option does not match the server's DUID.
           -  The message includes an IA option.
        """
        msg = msg_add_defaults(DHCP6_InfoRequest())
        
    else:
        assert False, "Invalid message type: %s" % msgname
    
    assert msg, "Message preparation failed"

    if world.oro is not None and len(world.cliopts):
        for opt in world.cliopts:
            msg = add_option_to_msg(msg, opt)

    if msg:
        world.climsg.append(msg)

    print("Message %s will be sent over %s interface." % (msgname, world.cfg["iface"]))

def client_doesnt_include(step, opt_type):
    """
    Remove client-id from message, maybe more if there will be need for that
    """

    print "...works"
    
    world.cfg["client_id"] = False
    assert "wtf?"

def add_option_to_msg(msg, option):
    msg /= option
    return msg

def add_client_option(option):
    world.cliopts.append(option)

def send_wait_for_message(step, presence, exp_message):
    """
    Block until the given message is (not) received.
    Parameter:
    new: (' new', optional): Only check the output printed since last time
                             this step was used for this process.
    process_name ('<name> stderr'): Name of the process to check the output of.
    message ('message <message>'): Output (part) to wait for.
    """
    world.cliopts = [] #clear options, always build new message, also possible make it in client_send_msg
    #debug.recv = []
    conf.use_pcap = True

    # Uncomment this to get debug.recv filled with all received messages
    #conf.debug_match = True
    ans,unans = sr(world.climsg, iface=world.cfg["iface"], timeout=1, nofilter=1, verbose=99)

    expected_type_found = False
    received_names = ""
    world.srvmsg = []
    for x in ans:
        a,b = x
        world.srvmsg.append(b)
        print("Debug: Received packet type = %s" % get_msg_type(b))
        received_names = get_msg_type(b) + " " + received_names
        if (get_msg_type(b) == exp_message):
            expected_type_found = True

    for x in unans:
        print("Unmatched packet type = %s" % get_msg_type(x))

    print("Received traffic (answered/unanswered): %d/%d packet(s)." % (len(ans), len(unans)))
    
    if presence:
        assert len(world.srvmsg) != 0, "No response received."
        assert expected_type_found, "Expected message " + exp_message + " not received (got " + received_names + ")"
    if not presence:
        assert len(world.srvmsg) == 0, "Response received, not expected"

def get_last_response():
    assert len(world.srvmsg), "No response received."

    return world.srvmsg[len(world.srvmsg) - 1]

def get_msg_type(msg):
    msg_types = { "SOLICIT": DHCP6_Solicit,
                  "ADVERTISE": DHCP6_Advertise,
                  "REQUEST": DHCP6_Request,
                  "REPLY": DHCP6_Reply
    }

    # 0th is IPv6, 1st is UDP, 2nd should be DHCP6
    dhcp = msg.getlayer(2)

    for msg_name in msg_types.keys():
        if type(dhcp) == msg_types[msg_name]:
            return msg_name

    return "UNKNOWN-TYPE"

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

def client_copy_option(step, option_name):

    assert world.srvmsg

    assert option_name in kea_options6, "Unsupported option name " + option_name
    opt_code = kea_options6.get(option_name)
    print opt_code
    opt = get_option(get_last_response(), opt_code)
    
    assert opt, "Received message does not contain option " + option_name

    opt.payload = None

    add_client_option(opt)

# @step('Response MUST (NOT )?include option (\d+).')
def response_check_include_option(step, must_include, opt_code):

    assert len(world.srvmsg) != 0, "No response received."

    opt = get_option(world.srvmsg[0], opt_code)

    if must_include:
        assert opt, "Expected option " + opt_code + " not present in the message."
    else:
        assert opt == None, "Unexpected option " + opt_code + " found in the message."

# Returns text represenation of the option, interpreted as specified by data_type
def unknown_option_to_str(data_type, opt):
    if data_type=="uint8":
        assert len(opt.data) == 1, "Received option " + opt.optcode + " contains " + len(opt.data) + \
                                   " bytes, but expected exactly 1"
        return str(ord(opt.data[0:1]))
    else:
        assert False, "Parsing of option format " + data_type + " not implemented."

# Option 23 MUST contain addresses 2001:db8::1,2001:db8::2
# @step('Response option (\d+) MUST (NOT )?contain (\S+) (\S+).')
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

def msg_add_defaults(msg):
    x = IPv6(dst=All_DHCP_Relay_Agents_and_Servers)/UDP(sport=546, dport=547)/msg
    x.trid = random.randint(0, 256*256*256)
    clientid = DHCP6OptClientId(duid = world.cfg["cli_duid"])
    if world.cfg["client_id"] == True:
        x /= clientid
    # rewrite whole creating message
    if len(world.cliopts)>0:
        if world.cliopts[0].optcode == 3:
            x /= DHCP6OptIA_NA(iaid = 1, ianaopts = world.cliopts[0].ianaopts)
            #x /= DHCP6OptIA_NA (world.cliopts[0].ianaopts)
            world.cliopts = []
        else:
            x /= DHCP6OptIA_NA(iaid = 1)
            return x
    else:
        x /= DHCP6OptIA_NA(iaid = 1)
    return x
