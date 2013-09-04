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
from features.logging_facility import get_common_logger

from features.terrain import set_options
from lettuce.registry import world
from scapy.layers.dhcp6 import *
from scapy.layers.inet import UDP
from scapy.layers.inet6 import IPv6
from scapy.sendrecv import sr

options6 = {     "client-id": 1,
                 "server-id" : 2,
                 "IA_NA" : 3,
                 "IN_TA": 4,
                 "IA_address" : 5,
                 "preference": 7,
                 "relay-msg": 9,
                 "status-code": 13,
                 "rapid_commit": 14,
                 "interface-id": 18,
                 "sip-server-dns": 21,
                 "sip-server-addr": 22,
                 "dns-servers": 23,
                 "domain-search": 24,
                 "IA_PD": 25,
                 "IA-Prefix": 26,
                 "nis-servers": 27,
                 "nisp-servers": 28,
                 "nis-domain-name": 29,
                 "nisp-domain-name": 30,
                 "sntp-servers": 31,
                 "information-refresh-time": 32 }

def test_pause(step):
    """
    Pause the test for any reason. Press any key to continue. 
    """
    def getch():
        import tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
    getch()
    
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
        msg = build_msg(DHCP6_Solicit())
        
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
        msg = build_msg(DHCP6_Request())

        
    elif (msgname == "CONFIRM"):
        """
        RFC 3315 15.5 
        Servers MUST discard any received Confirm messages that do not
        include a Client Identifier option or that do include a Server
        Identifier option.
        """
        msg = build_msg(DHCP6_Confirm())
        
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
        msg = build_msg(DHCP6_Renew())
        
    elif (msgname == "REBIND"):
        """
        RFC 3315 15.7
        Servers MUST discard any received Rebind messages that do not include
        a Client Identifier option or that do include a Server Identifier
        option.
        """
        msg = build_msg(DHCP6_Rebind())

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
        msg = build_msg(DHCP6_Decline())
                
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
        msg = build_msg(DHCP6_Release())
        
    elif (msgname == "INFOREQUEST"):
        """
        RFC 3315 15.12
        Servers MUST discard any received Information-request message that
        meets any of the following conditions:
           -  The message includes a Server Identifier option and the DUID in
              the option does not match the server's DUID.
           -  The message includes an IA option.
        """
        world.cfg["add_option"]["IA_NA"] = False #by default, IA restricted
        world.cfg["add_option"]["IA_TA"] = False
        msg = build_msg(DHCP6_InfoRequest())
        
    else:
        assert False, "Invalid message type: %s" % msgname
    
    assert msg, "Message preparation failed"

   
    if msg:
        world.climsg.append(msg)

    get_common_logger().debug("Message %s will be sent over %s interface." % (msgname, world.cfg["iface"]))

def unicast_addres(step):
    """
    Turn off sending on All_DHCP_Relay_Agents_and_Servers, and use UNICAST address. 
    """
    world.cfg["unicast"] = True

def add_option_to_msg(msg, option):#this is request_option option
    msg /= option
    return msg

def test_content(value_name):
    #this is only beta version of value testing
    if value_name in "address":
        opt = get_option(world.srvmsg[0], 3)
        if str(opt.ianaopts[0].addr[-1]) in [":","0"]:
            assert False, "Invalid assigned address: %s" % opt.ianaopts[0].addr
    else:
        assert False, "testing %s not implemented" % value_name

def client_add_saved_option(step, erase):
    """
    Add saved option to message, and erase.
    """
    if len(world.savedmsg) < 1: assert "No saved option!"
    for each in world.savedmsg:
        world.cliopts.append(each)
    if erase:
        world.savedmsg = []

def add_client_option(option):
    world.cliopts.append(option)

def client_save_option(step, option_name):
    assert option_name in options6, "Unsupported option name " + option_name
    opt_code = options6.get(option_name)
    opt = get_option(get_last_response(), opt_code)
    
    assert opt, "Received message does not contain option " + option_name
    opt.payload = None
    world.savedmsg.append(opt)

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
    
    tmp = DHCP6_RelayForward(linkaddr = "3000::ffff", peeraddr = "2000::1", hopcount = level)/DHCP6OptIfaceId(ifaceid = "15")
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
        tmp /= DHCP6_RelayForward(linkaddr = "3000::ffff", peeraddr = "2000::1", hopcount = level)/DHCP6OptIfaceId(ifaceid = "15")/DHCP6OptRelayMsg()

    #build full message
    relay_msg = IPv6(dst = address)/UDP(sport = 546, dport = 547)/tmp/msg
    
    world.climsg.append(relay_msg)
    
    world.cfg["relay"] = False

def send_wait_for_message(step, type, presence, exp_message):
    """
    Block until the given message is (not) received.
    Parameter:
    new: (' new', optional): Only check the output printed since last time
                             this step was used for this process.
    process_name ('<name> stderr'): Name of the process to check the output of.
    message ('message <message>'): Output (part) to wait for.
    """
    world.cliopts = [] #clear options, always build new message, also possible make it in client_send_msg
    may_flag = False
    #debug.recv = []
    conf.use_pcap = True
    if str(type) in "MUST":
        pass
    elif str(type) in "MAY":
        may_flag = True
    else:
        assert False, "Invalid expected behavior: %s." %str(type)
    #Uncomment this to get debug.recv filled with all received messages
    #conf.debug_match = True
    ans,unans = sr(world.climsg, iface = world.cfg["iface"], timeout = 1, nofilter = 1, verbose = 99)
    
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
    if may_flag:
        if len(world.srvmsg) != 0:
            assert True, "Response received."
        if len(world.srvmsg) == 0:
            assert True, "Response not received." #stop the test... ??
    elif presence:
        assert len(world.srvmsg) != 0, "No response received."
        assert expected_type_found, "Expected message " + exp_message + " not received (got " + received_names + ")"
    elif not presence:
        assert len(world.srvmsg) == 0, "Response received, not expected"

def get_last_response():
    assert len(world.srvmsg), "No response received."
    msg = world.srvmsg[len(world.srvmsg) - 1].copy()
    return msg 

def get_msg_type(msg):
    msg_types = { 
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
    
    # message needs to be copied, otherwise we changing original message what makes sometimes multiple copy impossible. 
    tmp_msg = msg.copy()
    
    world.opts = []
    world.subopts = []
    tmp = None
    x = tmp_msg.getlayer(3) # 0th is IPv6, 1st is UDP, 2nd is DHCP6, 3rd is the first option
    while x:
        if x.optcode == int(opt_code):
            tmp = x
            world.opts.append(x)

        if x.optcode == 3: # add IA Address and Status Code as separate option
            for each in x.ianaopts:
                world.subopts.append(each)
        if x.optcode == 25: # add IA PrefixDelegation and Status Code as separate option
            for each in x.iapdopt:
                world.subopts.append(each)
        x = x.payload
    return tmp

def client_copy_option(step, option_name):
    """
    Copy option from received message 
    """
    assert world.srvmsg

    assert option_name in options6, "Unsupported option name " + option_name
    opt_code = options6.get(option_name)
    opt = get_option(world.srvmsg[0], opt_code)
    
    assert opt, "Received message does not contain option " + option_name
    opt.payload = None
    #opt.show()
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

#===============================================================================
# #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# 
# def many_byte_xor(buf, key):
#     buf = bytearray(buf)
#     key = bytearray(key)
#     key_len = len(key)
#     for i, bufbyte in enumerate(buf):
#         buf[i] = bufbyte ^ key[i % key_len]
#     return str(buf)
# 
# def process_packets(infile):
#     pkts = rdpcap(infile)
#     cooked=[]
#     for p in pkts:
#         # You may have to adjust the payload depth here:
#         # i.e. p.payload.payload.payload
#         pkt_payload = str(p.payload.payload)
#         pkt_offset = str(p.payload.payload)[:3]
#         if pkt_payload and pkt_offset:
#             pmod=p
#             # You may have to adjust the payload depth here:
#             p.payload.payload=many_byte_xor(pkt_payload, pkt_offset)
#             cooked.append(pmod)
# 
#     
#     pkt = cooked[0]
#     print pkt.payload.payload
#     strpayload = str(pkt.payload.payload)
#     fd=open('/tmp/file', 'w')
#     fd.write(strpayload)
#     fd.close()
#     print os.system('file /tmp/file')
#     print "WYNIK: ", cooked
#     wrpcap("p.pcap", cooked)
# 
# 
# def response_check_include_message(step, opt_code, expect, data_type, expected):
#     """
#     Checking included messages in relay-reply message.  
#     still not operational :/
#     """
#     #UNDER CONSTRUCTION :)
#     #UNDER CONSTRUCTION :)
# #    assert len(world.srvmsg) != 0, "No response received."
#     x = world.srvmsg[0].getlayer(2)
#     print "msg:"
#     x.show()
#    
# #     while x:
# #         print "!"
# #         if x.optcode == 9:
# #             #if type(x.payload) == msg_types[msg_type]:
# #             
# #             z2 = hexdump(x.payload.data)
# #             wrpcap("p.pcap", x)
# #             process_packets("p.pcap")
# #         x = x.payload
#     
# #      0th is IPv6, 1st is UDP, 2nd should be DHCP6
#   
# #     while x:
# #         for msg_name in msg_types.keys():
# #             if type(x) == msg_types[msg_name]:
# #                 assert "Expected message " + msg_type + " present in the message."
# #         x = x.payload
# #          
# #         x.show()
# 
# #     assert "Expected message " + msg_type + " not present in the message."
# #     if must_include:
# #         assert opt, "Expected message " + msg_type + " not present in the message."
# #     else:
# #         assert opt == None, "Unexpected message" + msg_type + " found in the message."    
#===============================================================================
    
    
    
# Returns text representation of the option, interpreted as specified by data_type
def unknown_option_to_str(data_type, opt):
    if data_type == "uint8":
        assert len(opt.data) == 1, "Received option " + opt.optcode + " contains " + len(opt.data) + \
                                   " bytes, but expected exactly 1"
        return str(ord(opt.data[0:1]))
    else:
        assert False, "Parsing of option format " + data_type + " not implemented."

def response_check_option_content(step, opt_code, expect, data_type, expected):
    opt_code = int(opt_code)
    x = None
    assert len(world.srvmsg) != 0, "No response received."
    
    if opt_code == 13: # that's little messy but option 13 is unique, Forge checks it inside option 3 and 25.
        x = get_option(world.srvmsg[0], 3) 
        if x == None:
            x = get_option(world.srvmsg[0], 25)
    else:
        x = get_option(world.srvmsg[0], opt_code)
    
    assert x, "Expected option " + str(opt_code) + " not present in the message."

    received = ""
    for each in world.opts:
        if opt_code == 3:
            try:
                if each.ianaopts[0].optcode == 13:
                    received += str(each.ianaopts[0].optcode)
                elif each.ianaopts[0].optcode == 5:
                    received += each.ianaopts[0].addr + ' '
            except:
                pass
        elif opt_code == 7:
            received = str(each.prefval)
        elif opt_code == 9:
            pass
            #received = str(x.optcode)
        elif opt_code == 13:
            
            try:
                received += str(each.ianaopts[0].statuscode) + ' '
            except:
                pass
            try:
                each.iapdopt[0].show()
                received += str(each.iapdopt[0].statuscode) + ' '
            except:
                pass
        elif opt_code == 21:
            received = ",".join(each.sipdomains)
        elif opt_code == 22:
            received = ",".join(each.sipservers)
        elif opt_code == 23:
            received = ",".join(each.dnsservers)
        elif opt_code == 24:
            received = ",".join(each.dnsdomains)
        elif opt_code == 25:
            for every in each.iapdopt:
                #every.show()
                try:
                    if every.optcode == 13:
                        received += ' ' + str(every.statuscode)
                    elif every.optcode == 26:
                        received += every.prefix + ' '
                except:
                    pass

        elif opt_code == 27:
            received = ",".join(each.nisservers)
        elif opt_code == 28:
            received = ",".join(each.nispservers)
        elif opt_code == 29:
            received = each.nisdomain
        elif opt_code == 30:
            received = each.nispdomain
        elif opt_code == 31:
            received = ",".join(each.sntpservers)
        elif opt_code == 32:
            received = str(each.reftime)
        else:
            received = unknown_option_to_str(data_type, each)
    

    assert expected in received, "Invalid " + str(opt_code) + " option received: " + received + \
                                 ", but expected " + str(expected)

def receive_dhcp6_tcpdump(count = 1, timeout = 1):

    args = ["tcpdump", "-i", world.cfg["iface"], "-c", str(count), "-w", "test.pcap", "ip6"]
    get_common_logger().debug("Running tcpdump for %d seconds:" % timeout)
    get_common_logger().debug(args)
    tcpdump = subprocess.Popen(args)
    time.sleep(timeout)
    tcpdump.terminate()

    ans = sniff(count = 5, filter = "ip6", offline = "test.pcap", promisc = True, timeout = 3)
    get_common_logger().debug("Received traffic: %d packet(s)." % len(ans))
    assert len(ans) != 0, "No response received."
#     for x in ans:
#         x.show()

def client_does_include(step, opt_type):
    """
    Include options to message. This function refers to @step in lettuce
    """
    #If you want to use options of received message to include it, please use 'Client copies (\S+) option from received message.' step.
    if opt_type == "client-id":
        world.cfg["add_option"]["client_id"] = False
    elif opt_type == "wrong-client-id":
        world.cfg["add_option"]["wrong_client_id"] = True
    elif opt_type == "wrong-server-id":
        world.cfg["add_option"]["wrong_server_id"] = True
    elif opt_type == "preference":
        world.cfg["add_option"]["preference"] = True
    elif opt_type == "rapid-commit":
        world.cfg["add_option"]["rapid_commit"] = True
    elif opt_type == "time":
        world.cfg["add_option"]["time"] = True
    elif opt_type == "relay-msg":
        world.cfg["add_option"]["relay_msg"] = True
    elif opt_type == "server-unicast":
        world.cfg["add_option"]["server_uni"] = True
    elif opt_type == "status-code":
        world.cfg["add_option"]["status_code"] = True
    elif opt_type == "interface-id":
        world.cfg["add_option"]["interface_id"] = True
    elif opt_type == "reconfigure":
        world.cfg["add_option"]["reconfig"] = True
    elif opt_type == "reconfigure-accept":
        world.cfg["add_option"]["reconfig_accept"] = True
    elif opt_type == "option-request":
        world.cfg["add_option"]["option_request"] = True
    elif opt_type == "IA-PD":
        world.cfg["add_option"]["IA_PD"] = True
    elif opt_type == "IA-NA":
        world.cfg["add_option"]["IA_NA"] = False
        
    else:
        assert "unsupported option: " + opt_type

def generate_new (step, opt):
    """
    Generate new client id with random MAC address.
    """
    if opt == 'client':
        from features.terrain import client_id, ia_id
        client_id(RandMAC())
        ia_id()
    elif opt == 'IA':
        from features.terrain import ia_id
        ia_id()
    elif opt == 'IA_PD':
        from features.terrain import ia_pd
        ia_pd()

    else:
        assert False,  opt + " generation unsupported" 

def client_option (msg):
    """
    Add options (like server-id, rapid commit) to message. This function refers to building message
    """
    #server id with mistake, if you want to add correct server id, plz use 'client copies server id...'
    if world.cfg["add_option"]["wrong_server_id"] == True:
        msg /= DHCP6OptServerId(duid = DUID_LLT(timeval = int(time.time()), lladdr = RandMAC() ))
        
    #client id
    if world.cfg["add_option"]["client_id"] == True and world.cfg["add_option"]["wrong_client_id"] == False:
        if world.cfg["relay"] == False:
            msg /= DHCP6OptClientId(duid = world.cfg["cli_duid"])
    elif world.cfg["add_option"]["client_id"] == True and world.cfg["add_option"]["wrong_client_id"] == True:
        msg /= DHCP6OptClientId()#it needs to stay blank!
        
    elif world.cfg["add_option"]["client_id"] == False:
        #world.cfg["add_option"]["client_id"] = True
        pass
    
    if world.cfg["add_option"]["IA_NA"] == True and world.cfg["relay"] == False:
        if world.oro is not None and len(world.cliopts):
            for opt in world.cliopts:
                if opt.optcode == 3:
                    break #if there is no IA_NA/TA in world.cliopts, break.. 
            else:
                msg /= DHCP6OptIA_NA(iaid = world.cfg["ia_id"]) # if not, add IA_NA
        else:
            msg /= DHCP6OptIA_NA(iaid = world.cfg["ia_id"]) # if not, add IA_NA   

    if world.cfg["add_option"]["preference"] == True:
        msg /= DHCP6OptPref()
        
    if world.cfg["add_option"]["rapid_commit"] == True:
        msg /= DHCP6OptRapidCommit()
    
    if world.cfg["add_option"]["time"] == True:
        msg /= DHCP6OptElapsedTime()

    if world.cfg["add_option"]["server_uni"] == True:
        msg /= DHCP6OptServerUnicast()

    if world.cfg["add_option"]["status_code"] == True:
        msg /= DHCP6OptStatusCode()

    if world.cfg["add_option"]["interface_id"] == True:
        msg /= DHCP6OptIfaceId(ifaceid = "15")

    if world.cfg["add_option"]["reconfig"] == True:
        msg /= DHCP6OptReconfMsg()

    if world.cfg["add_option"]["reconfig_accept"] == True:
        msg /= DHCP6OptReconfAccept()

    if world.cfg["add_option"]["IA_PD"] == True:
        msg /= DHCP6OptIA_PD(iaid = world.cfg["ia_pd"])

    if world.cfg["add_option"]["option_request"] == True:
        msg /= DHCP6OptOptReq() #this adds 23 and 24 opt by default, we can leave it that way in this point.
        
    if world.cfg["add_option"]["relay_msg"] == True:
        msg /= DHCP6OptRelayMsg()/DHCP6_Solicit()
    
    set_options()
    return msg
 
def build_msg(msg):
    
    if world.cfg["unicast"] == False:
        address = All_DHCP_Relay_Agents_and_Servers
    elif world.cfg["unicast"] == True:
        from features.init_all import SRV_IPV6_ADDR
        address = SRV_IPV6_ADDR
        world.cfg["unicast"] = False
    
    msg = IPv6(dst = address)/UDP(sport=546, dport=547)/msg
    #transaction id
    msg.trid = random.randint(0, 256*256*256)
    world.cfg["tr_id"] = msg.trid
    
    #add option request if any
    try:
        if (len(world.oro.reqopts) > 0):
                msg = add_option_to_msg(msg, world.oro)
    except:
        pass
    
    #add other options if any
    try:
        if world.oro is not None and len(world.cliopts):
            for opt in world.cliopts:
                msg = add_option_to_msg(msg, opt)
    except:
        pass
    
    #add all rest options to message. 
    msg = client_option (msg)
    
    return msg

