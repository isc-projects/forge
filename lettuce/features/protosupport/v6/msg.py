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
from features.serversupport.kea6.functions import kea_options6
from features.logging_facility import get_common_logger
from lettuce.registry import world
from scapy.layers.dhcp6 import *
from scapy.layers.inet import UDP
from scapy.layers.inet6 import IPv6
from scapy.sendrecv import sr



def client_requests_option(step, opt_type):
    """
    Add RequestOption to message.
    """
    if not hasattr(world, 'oro'):
        # There was no ORO at all, create new one
        world.oro = DHCP6OptOptReq()
        # Scapy creates ORO with 23, 24 options request. Let's get rid of them
        world.oro.reqopts = [] # don't request anything by default

    world.oro.reqopts.append(int(opt_type))

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
    
    if (msgname == "SOLICIT"):
        """
        RFC 3315 15.2 
        Servers MUST discard any Solicit messages that do not include a
        Client Identifier option or that do include a Server Identifier
        option.
        
        Also we can include IA options, Option Request, Rapid Commit and Reconfigure Accept.
        """
        msg = msg_add_defaults(DHCP6_Solicit())
        try:
            if (world.oro is not None):
                    msg = add_option_to_msg(msg, world.oro)
        except:
            pass
        
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
        try:
            if (world.oro is not None):
                    msg = add_option_to_msg(msg, world.oro)
        except:
            pass
        
    elif (msgname == "CONFIRM"):
        """
        RFC 3315 15.5 
        Servers MUST discard any received Confirm messages that do not
        include a Client Identifier option or that do include a Server
        Identifier option.
        """
        msg = msg_add_defaults(DHCP6_Confirm())
        try:
            if (world.oro is not None):
                    msg = add_option_to_msg(msg, world.oro)
        except:
            pass
        
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
        
    elif (msgname == "INFOREQUEST"):
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

    try:
        if world.oro is not None and len(world.cliopts):
            for opt in world.cliopts:
                msg = add_option_to_msg(msg, opt)
    except:
        pass
    
    if msg:
        world.climsg.append(msg)

    get_common_logger().debug("Message %s will be sent over %s interface." % (msgname, world.cfg["iface"]))

def unicast_addres(step):
    """
    Turn off sending on All_DHCP_Relay_Agents_and_Servers, and use UNICAST address. 
    """
    world.cfg["unicast"] = True

def add_option_to_msg(msg, option):
    msg /= option
    return msg

def add_client_option(option):
    world.cliopts.append(option)

def create_relay_forward(step, level):
    """
    Encapsulate message in relay-forward message.
    """
    #set flag for adding client option client-id which is added by default
    world.cfg["relay"] = True
    
    address = All_DHCP_Relay_Agents_and_Servers
    
    #get only DHCPv6 part of the message
    msg = world.climsg.pop().getlayer(2)
    from features.init_all import SRV_IPV6_ADDR
    level = int(level)

    #all three values: linkaddr, peeraddr and hopcount must be filled
    
    tmp = DHCP6_RelayForward(linkaddr="3000::ffff", peeraddr="::", hopcount = level)/DHCP6OptIfaceId(ifaceid = "15")
    #tmp = DHCP6_RelayForward(linkaddr="3000::ffff", peeraddr="::", hopcount = level)
    
    #add options (used only when checking "wrong option" test for relay-forward message. to add some options to relay-forward 
    #you need to put "Client does include opt_name." before "...using relay-agent encapsulated in 1 level." and after "Client sends SOLICIT message."
    tmp = client_option(tmp)
    
    #add RelayMsg option 
    tmp /= DHCP6OptRelayMsg()
    #message encapsulation 
    while True:
        level -= 1
        if not level: break;
        tmp /= DHCP6_RelayForward(linkaddr="3000::ffff", peeraddr="::", hopcount = level)/DHCP6OptIfaceId(ifaceid = "15")/DHCP6OptRelayMsg()

    #build full message
    relay_msg = IPv6(dst = address)/UDP(sport=546, dport=547)/tmp/msg
    
    world.climsg.append(relay_msg)
    
    world.cfg["relay"] = False

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

    #Uncomment this to get debug.recv filled with all received messages
    #conf.debug_match = True
    ans,unans = sr(world.climsg, iface = world.cfg["iface"], timeout=1, nofilter=1, verbose=99)
    
    expected_type_found = False
    received_names = ""
    world.srvmsg = []
    for x in ans:
        a,b = x
        world.srvmsg.append(b)
        get_common_logger().info("Received packet type = %s" % get_msg_type(b))
        received_names = get_msg_type(b) + " " + received_names
        if (get_msg_type(b) == exp_message):
            expected_type_found = True
            
    for x in unans:
        get_common_logger().error(("Unmatched packet type = %s" % get_msg_type(x)))

    get_common_logger().debug("Received traffic (answered/unanswered): %d/%d packet(s)." 
                              % (len(ans), len(unans)))
    
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
                  "REPLY": DHCP6_Reply,
                  "RELAYREPLY": DHCP6_RelayReply
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
    """
    Copy option from received message 
    """
    assert world.srvmsg

    assert option_name in kea_options6, "Unsupported option name " + option_name
    opt_code = kea_options6.get(option_name)
    opt = get_option(get_last_response(), opt_code)
    
    assert opt, "Received message does not contain option " + option_name

    #opt.payload = None

    add_client_option(opt)

def response_check_include_option(step, must_include, opt_code):
    """
    Checking presence of expected option.
    """
    assert len(world.srvmsg) != 0, "No response received."

    opt = get_option(world.srvmsg[0], opt_code)

    if must_include:
        assert opt, "Expected option " + opt_code + " not present in the message."
    else:
        assert opt == None, "Unexpected option " + opt_code + " found in the message."

def response_check_include_message(step, opt_code, expect, data_type, expected):
    """
    Checking included messages in relay-reply message.  
    still not operational :/
    """
    #UNDER CONSTRUCTION :)
    #UNDER CONSTRUCTION :)
#    assert len(world.srvmsg) != 0, "No response received."
    x = world.srvmsg[0].getlayer(2)
    print "msg:"
    x.show()
    
    msg_types = { "ADVERTISE": DHCP6_Advertise,
                  "REPLY": DHCP6_Reply,
    }
    
    
    while x:
        print "!"
        if x.optcode == 9:
            #if type(x.payload) == msg_types[msg_type]:
            x.show()
            print "\npayload type: ",type(x.payload)
            #z = DHCP6(x.payload.data)
            #z.show()
            print "hex payload: "
            z1 = hexdump(x.payload)
            print "str payload: \n", str(x.payload)
            print "payload:\n", x.payload
            print "hex payload.data: "
            z2 = hexdump(x.payload.data)
            print "str payload.data: \n", str(x.payload.data)
            print "payload.data:\n", x.payload.data
            
            
            print "\n\n", str(x.payload.data).decode("hex")
            y1 = str(z1)
            z1 = DHCP6(y1)
            z1.show()

            y2 = str(z2)
            z2 = DHCP6(y2)
            z2.show()
            
            #a.show()
            #print "\n\n", type(x.payload.data), "\n\n"
            #pay = x.payload
        x = x.payload
    
#      0th is IPv6, 1st is UDP, 2nd should be DHCP6
  
#     while x:
#         for msg_name in msg_types.keys():
#             if type(x) == msg_types[msg_name]:
#                 assert "Expected message " + msg_type + " present in the message."
#         x = x.payload
#          
#         x.show()

#     assert "Expected message " + msg_type + " not present in the message."
#     if must_include:
#         assert opt, "Expected message " + msg_type + " not present in the message."
#     else:
#         assert opt == None, "Unexpected message" + msg_type + " found in the message."    
    
# Returns text representation of the option, interpreted as specified by data_type
def unknown_option_to_str(data_type, opt):
    if data_type == "uint8":
        assert len(opt.data) == 1, "Received option " + opt.optcode + " contains " + len(opt.data) + \
                                   " bytes, but expected exactly 1"
        return str(ord(opt.data[0:1]))
    else:
        assert False, "Parsing of option format " + data_type + " not implemented."

def test_option_code(msg):
    print msg.statuscode

        
def response_check_option_content(step, opt_code, expect, data_type, expected):

    opt_code = int(opt_code)

    assert len(world.srvmsg) != 0, "No response received."

    x = get_option(world.srvmsg[0], opt_code)

    assert x, "Expected option " + str(opt_code) + " not present in the message."

    received = ""
    if opt_code == 3:
        #needs more work
        x.show()
        #received = str(x.ianaopts[0].optcode)
        #test_option_code(x.ianaopts[0])
    elif opt_code == 7:
        received = str(x.prefval)
    elif opt_code == 9:
        pass
        #received = str(x.optcode)
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

    assert expected == received, "Invalid " + str(opt_code) + " option received:" + received + \
                                 ", but expected " + str(expected)

def receive_dhcp6_tcpdump(count = 1, timeout = 1):

    args = ["tcpdump", "-i", world.cfg["iface"], "-c", str(count), "-w", "test.pcap", "ip6"]
    get_common_logger().debug("Running tcpdump for %d seconds:" % timeout)
    get_common_logger().debug(args)
    tcpdump = subprocess.Popen(args)
    time.sleep(timeout)
    tcpdump.terminate()

    ans = sniff(count=5, filter="ip6", offline="test.pcap", promisc=True, timeout=3)
    get_common_logger().debug("Received traffic: %d packet(s)." % len(ans))
    assert len(ans) != 0, "No response received."
    for x in ans:
        x.show()

def client_does_include(step, opt_type):
    """
    Include options to message. This function refers to @step in lettuce
    """
    #If you want to use parts of received message to include it, please use 'Client copies (\S+) option from received message.' step.
    if opt_type == "client-id":
        world.cfg["client_id"] = False
    elif opt_type == "wrong-client-id":
        world.cfg["wrong_client_id"] = True
    elif opt_type == "wrong-server-id":
        world.cfg["wrong_server_id"] = True
    elif opt_type == "preference":
        world.cfg["preference"] = True
    elif opt_type == "rapid-commit":
        world.cfg["rapid_commit"] = True
    elif opt_type == "time":
        world.cfg["time"] = True
    else:
        assert "unsupported option: " + opt_type
        
def new_client_id (step):
    """
    Generate new client id with random MAC address.
    """
    from features.terrain import client_id, ia_id
    client_id(RandMAC())
    ia_id()

def client_option (msg):
    """
    Add options (like server-id, rapid commit) to message. This function refers to building message
    """
    #server id with mistake
    if world.cfg["wrong_server_id"] == True:
        msg /= DHCP6OptServerId()
        world.cfg["wrong_server_id"] = False
        
    #client id
    if world.cfg["client_id"] == True and world.cfg["wrong_client_id"] == False:
        if world.cfg["relay"] == False:
            msg /= DHCP6OptClientId(duid = world.cfg["cli_duid"])
    elif world.cfg["client_id"] == True and world.cfg["wrong_client_id"] == True:
        msg /= DHCP6OptClientId()
        world.cfg["wrong_client_id"] = False
    elif world.cfg["client_id"] == False:
        world.cfg["client_id"] = True
        
    #preference option
    if world.cfg["preference"] == True:
        msg /= DHCP6OptPref()
        world.cfg["preference"] = False
        
    #rapid commit
    if world.cfg["rapid_commit"] == True:
        msg /= DHCP6OptRapidCommit()
        world.cfg["rapid_commit"] = False
    
    if world.cfg["time"] == True:
        msg /= DHCP6OptElapsedTime()
        world.cfg["time"] = False
    
    return msg


def msg_add_defaults(msg):
    
    if world.cfg["unicast"] == False:
        address = All_DHCP_Relay_Agents_and_Servers
    elif world.cfg["unicast"] == True:
        from features.init_all import SRV_IPV6_ADDR
        address = SRV_IPV6_ADDR
        world.cfg["unicast"] = False
    
    x = IPv6(dst = address)/UDP(sport=546, dport=547)/msg
    #transaction id
    x.trid = random.randint(0, 256*256*256)
    world.cfg["tr_id"] = x.trid
    #add all options to message. 
    x = client_option (x)
    
    if len(world.cliopts) > 0:
        if world.cliopts[0].optcode == 3:
            x /= DHCP6OptIA_NA(iaid = world.cfg["ia_id"], ianaopts = world.cliopts[0].ianaopts)
            world.cliopts = []
        else:
            x /= DHCP6OptIA_NA(iaid = world.cfg["ia_id"])
            return x
    else:
        x /= DHCP6OptIA_NA(iaid = world.cfg["ia_id"])
    return x

