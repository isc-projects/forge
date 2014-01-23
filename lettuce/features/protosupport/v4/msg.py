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

def client_send_msg(step, msgname):
    """
    Sends specified message with defined options.
    Parameters:
    msg ('<msg> message'): name of the message.
    num_opts: number of options to send.
    opt_type: option type
    """
    world.climsg = []
    options = []

    if hasattr(world, 'prl'):
        options += [("param_req_list", str(world.prl))]
    else:
        assert False, "No PRL defined"

    options += ["end"] # end option

    # What about messages: "force_renew","lease_query",
    # "lease_unassigned","lease_unknown","lease_active",
    # messages from server: offer, ack, nak

    if (msgname == "DISCOVER"):
        # msg code: 1
        msg = build_msg([("message-type","discover")]+options)
        
    elif (msgname == "REQUEST"):
        # msg code: 3
        msg = build_msg([("message-type","request")]+options)
        
    elif (msgname == "DECLINE"):
        # msg code: 4
        msg = build_msg([("message-type","decline")]+options)
        
    elif (msgname == "RELEASE"):
        # msg code: 7
        msg = build_msg([("message-type","release")]+options)
        
    elif (msgname == "INFORM"):
        # msg code: 8
        msg = build_msg([("message-type","inform")]+options)

    else:
        assert False, "Invalid message type: %s" % msgname

    assert msg, "Failed to create " + msgname

    if msg:
        world.climsg.append(msg)

    get_common_logger().debug("Message %s will be sent over %s interface." % (msgname, world.cfg["iface"]))
    

def build_msg(opts):

    conf.checkIPaddr = False
    fam,hw = get_if_raw_hwaddr(conf.iface)


    msg = Ether(dst = "ff:ff:ff:ff:ff:ff")/IP(dst = world.cfg["srv4_addr"])
    msg /= UDP(sport = 68, dport = 67)/BOOTP(chaddr = hw, giaddr = world.cfg["giaddr4"])
    msg /= DHCP(options = opts)
    msg.xid = randint(0, 256*256*256)
    
    return msg

def send_wait_for_message(step, type, presence, exp_message):
    """
    Block until the given message is (not) received.
    """
    # We need to use srp() here (send and receive on layer 2)
    ans,unans = srp(world.climsg, iface = world.cfg["iface"], timeout = 1, multi = True, verbose = 1)

    world.srvmsg = []
    for x in ans:
        a,b = x
        world.srvmsg.append(b)
        #b.show()
    get_common_logger().debug("Received traffic (answered/unanswered): %d/%d packet(s)."
                              % (len(ans), len(unans)))

    assert presence == bool(world.srvmsg), "No response received."

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

def test_option(received, expected):
    tmp = ""
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
    outcome, received = test_option(received ,expected)

    if expect == None:
        assert outcome, "Invalid {opt_code} option received: {received}"\
                                    " but expected {expected}".format(**locals())
    else:
        assert not outcome, "Invalid {opt_code} option received: {received}"\
                                 " that value has been excluded from correct values".format(**locals())