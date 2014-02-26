from lettuce import world
from logging_facility import *
from scapy.all import get_if_raw_hwaddr, Ether, srp 
from scapy.config import conf
from scapy.fields import Field
from scapy.layers.dhcp import BOOTP, DHCP, DHCPOptions
from scapy.layers.inet import IP, UDP
from scapy.sendrecv import send, sendp, sniff
from random import randint
import protosupport.v6.msg

def client_requests_option(step, opt_type):
    if not hasattr(world, 'prl'):
        world.prl = "" # don't request anything by default
    world.prl += chr(int(opt_type)) # put a single byte there

def client_send_msg(step, msgname, iface, addr):
    """
    Sends specified message with defined options.
    Parameters:
    msg ('<msg> message'): name of the message.
    num_opts: number of options to send.
    opt_type: option type
    """
    # set different ethernet interface then default one.
    if iface != None:
        world.cfg["iface"] = iface
        world.cfg["srv4_addr"] = addr
        
    world.climsg = []
    options = world.cliopts

    if hasattr(world, 'prl') and len(world.prl) > 0:
        options += [("param_req_list", str(world.prl))]
#     else:
#         assert False, "No PRL defined"

    options += ["end"] # end option

    # What about messages: "force_renew","lease_query",
    # "lease_unassigned","lease_unknown","lease_active",
    # messages from server: offer, ack, nak

    if (msgname == "DISCOVER"):
        # msg code: 1
        msg = build_msg([("message-type","discover")] + options)
        
    elif (msgname == "REQUEST"):
        # msg code: 3
        msg = build_msg([("message-type","request")] + options)
        
    elif (msgname == "DECLINE"):
        # msg code: 4
        msg = build_msg([("message-type","decline")] + options)
        
    elif (msgname == "RELEASE"):
        # msg code: 7
        msg = build_msg([("message-type","release")] + options)
        
    elif (msgname == "INFORM"):
        # msg code: 8
        msg = build_msg([("message-type","inform")] + options)

    else:
        assert False, "Invalid message type: %s" % msgname

    assert msg, "Failed to create " + msgname

    if msg:
        world.climsg.append(msg)

    get_common_logger().debug("Message %s will be sent over %s interface." % (msgname, world.cfg["iface"]))

def client_sets_value(step, value_name, new_value):
    if value_name in world.cfg["values"]:
        if isinstance(world.cfg["values"][value_name], str):
            world.cfg["values"][value_name] = str(new_value)
        elif isinstance(world.cfg["values"][value_name], int):
            world.cfg["values"][value_name] = int(new_value)
        else:
            world.cfg["values"][value_name] = new_value
    else:
        assert value_name in world.cfg["values"], "Unknown value name : %s" % value_name

def client_does_include(step, opt_type, value):
    if opt_type == 'client_id':
        world.cliopts += [(opt_type, convert_MAC(value))]
#     elif opt_type =='vendor_class_id':
#         world.cliopts += [(opt_type, str(value), "my-other-class")]
    else:
#         if isinstance(value, str):
#             world.cliopts += [(opt_type, str(value))]
#         elif isinstance(value, int):
#             world.cliopts += [(opt_type, int(value))]
#         else:
#             assert False, "wtf"
        world.cliopts += [(opt_type, str(value))]

def response_check_content(step, expect, data_type, expected):
    
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
        received = world.srvmsg[0].chaddr #decode!!
    elif data_type == 'sname':
        received = world.srvmsg[0].sname.replace('\x00', '')
    elif data_type == 'file':
        received = world.srvmsg[0].file.replace('\x00', '')
        
    else:
        assert False, "Value %s is not supported" % data_type
    
    # because we are using function to parse full option not just value
    # I did little hack, added 'value:' as option code, and changed assertion message
    outcome, received = test_option(0, ['value:', received], expected)

    if expect == None:
        assert outcome, "Invalid received {received}"\
                                " but expected: {expected}.".format(**locals())
    else:
        assert not outcome, "Invalid received {received}"\
                                 " that value has been excluded from correct values.".format(**locals())
    return received
                             
def client_copy_option(step, opt_name):
    from serversupport.kea4.functions import kea_options4
    opt_code = kea_options4.get(opt_name)
    
    assert opt_name in kea_options4, "Unsupported option name " + opt_name
    
    received = get_option(world.srvmsg[0], opt_code)
    world.cliopts.append(received)
    
def convert_MAC(mac):
    # convert MAC address to hex representation
    return mac.replace(':', '').decode('hex')

def build_msg(opts):

    conf.checkIPaddr = False
    fam,hw = get_if_raw_hwaddr(str(world.cfg["iface"]))
    tmp_hw = None

    # we need to choose if we want to use chaddr, or client id. 
    # also we can include both: client_id and chaddr
    if world.cfg["values"]["chaddr"] == None:
        tmp_hw = hw
    elif world.cfg["values"]["chaddr"] == "empty":
        tmp_hw = convert_MAC("00:00:00:00:00:00")
    else:
        tmp_hw = convert_MAC(world.cfg["values"]["chaddr"])
    
    msg = Ether(dst = "ff:ff:ff:ff:ff:ff", src = hw)/IP(src = world.cfg["values"]["source_IP"], dst = world.cfg["values"]["dstination_IP"])
    msg /= UDP(sport = 68, dport = 67)/BOOTP(chaddr = tmp_hw, giaddr = world.cfg["values"]["giaddr"])
    msg /= DHCP(options = opts)
    msg.xid = randint(0, 256*256*256)
    msg.siaddr = world.cfg["values"]["siaddr"]
    msg.ciaddr = world.cfg["values"]["ciaddr"]
    msg.yiaddr = world.cfg["values"]["yiaddr"]

    return msg

def get_msg_type(msg):
    
    msg_types = {1:"DISCOVER",
                 2:"OFFER",
                 3:"REQUEST",
                 4:"DECLINE",
                 5:"ACK",
                 6:"NAK",
                 7:"RELEASE",
                 8:"INFORM"
                 }
    # option 53 it's message type
    opt = get_option(msg, 53)
    
    # opt[1] it's value of message-type option
    for msg_code in msg_types.keys():
        if opt[1] == msg_code:
            return msg_types[msg_code]
        
    return "UNKNOWN-TYPE"
def send_wait_for_message(step, type, presence, exp_message):
    """
    Block until the given message is (not) received.
    """
    # We need to use srp() here (send and receive on layer 2)
    ans,unans = srp(world.climsg, iface = world.cfg["iface"], timeout = world.cfg["PACKET_WAIT_INTERVAL"], multi = True, verbose = 99)
    #world.climsg[0].show()
    expected_type_found = False
    
    received_names = ""
    world.cliopts = []
    world.srvmsg = []
    for x in ans:
        a,b = x
        world.srvmsg.append(b)
        b.show()
        received_names = get_msg_type(b) + " " + received_names
        if (get_msg_type(b) == exp_message):
            expected_type_found = True
            
    get_common_logger().debug("Received traffic (answered/unanswered): %d/%d packet(s)."
                              % (len(ans), len(unans)))
    if exp_message != "None":
        for x in unans:
            get_common_logger().error(("Unmatched packet type = %s" % get_msg_type(x)))
            
        if presence:
            assert len(world.srvmsg) != 0, "No response received."
            assert expected_type_found, "Expected message " + exp_message + " not received (got " + received_names + ")"
        elif not presence:
            assert len(world.srvmsg) == 0, "Response received, not expected"
        assert presence == bool(world.srvmsg), "No response received."
    else:
        pass
        # make assertion for receiving message that not suppose to come!

# Returns option of specified type
def get_option(msg, opt_code):
    # We need to iterate over all options and see
    # if there's one we're looking for
    world.opts = []
    opt_name = DHCPOptions[int(opt_code)]
    
    # dhcpv4 implementation in Scapy is a mess. The options array contains mix of 
    # strings, IPField, ByteEnumField and who knows what else. In each case the
    # values are accessed differenty
    if (isinstance(opt_name, Field)):
        opt_name = opt_name.name

    x = msg.getlayer(4) # 0th is Ethernet, 1 is IPv4, 2 is UDP, 3 is BOOTP, 4 is DHCP options
    for opt in x.options:
        if opt[0] == opt_name:
            world.opts.append(opt)
            return opt
    return None

def ByteToHex (byteStr):
    return ''.join([ "%02X " % ord(x) for x in byteStr]).replace(" ","")

def test_option(opt_code, received, expected):
    tmp = ""
    decode_opts = [61]

    if opt_code in decode_opts:
        received = received[0], ByteToHex(received[1])

    for each in received:
        tmp += str(each) + ' '
        if str(each) == expected:
            return True, each
    return False, tmp

def response_check_include_option(step, expected, opt_code):
    assert len(world.srvmsg) != 0, "No response received."
    opt = get_option(world.srvmsg[0], opt_code)
    if expected:
        assert opt, "Expected option " + opt_code + " not present in the message."
    else:
        assert opt == None, "Expected option " + opt_code + " present in the message. But not expected!"

def response_check_option_content(step, subopt_code, opt_code, expect, data_type, expected):
    # expect == None when we want that content and NOT when we dont want! that's messy correct that!
    assert len(world.srvmsg) != 0, "No response received."
    
    opt_code = int(opt_code)
    received = get_option(world.srvmsg[0], opt_code)
    outcome, received = test_option(opt_code, received ,expected)

    if expect == None:
        assert outcome, "Invalid {opt_code} option received: {received}"\
                                    " but expected {expected}".format(**locals())
    else:
        assert not outcome, "Invalid {opt_code} option received: {received}"\
                                 " that value has been excluded from correct values".format(**locals())
