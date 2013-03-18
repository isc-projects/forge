from lettuce import world
from scapy.arch.linux import get_if_raw_hwaddr
from scapy.config import conf
from scapy.layers.dhcp import BOOTP, DHCP
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether

def client_requests_option(step, opt_type):
    if not hasattr(world, 'prl'):
        world.prl = "" # don't request anything by default
    world.prl += chr(int(opt_type)) # put a single byte there

def client_send_msg(step, msgname, opt_type, unknown):
    """
    Sends specified message with defined options.
    Parameters:
    msg ('<msg> message'): name of the message.
    num_opts: number of options to send.
    opt_type: option type
    """
    
    options = []

    if hasattr(world, 'prl'):
        options += [("param_req_list", str(world.prl))]
    else:
        assert False, "No PRL defined"

    options += ["end"] # end option

    if (msgname == "DISCOVER"):
        msg = create_discover(options)
#    elif (msgname == "OFFER"):
#        msg = create_offer()
#    elif (msgname == "REQUEST"):
#        msg = create_request()
#    elif (msgname == "ACK"):
#        msg = create_ack()
#    elif (msgname == "NAK"):
#        msg = create_nak()
#    elif (msgname == "DHCPINFORM"):
#        msg = create_inform()
#    elif (msgname == "DHCPRELEASE"):
#        msg = create_release()
    else:
        assert False, "Invalid message type: %s" % msgname

    assert msg, "Failed to create " + msgname

    if msg:
        world.climsg.append(msg)

    print("Message %s will be sent over %s interface." % (msgname, world.cfg["iface"]))
    

def create_discover(options):

    opts = [("message-type","discover")]
    if options:
        opts += options
    else:
        assert False

    conf.checkIPaddr = False
    fam,hw = get_if_raw_hwaddr(conf.iface)

    discover = Ether(dst="ff:ff:ff:ff:ff:ff")/IP(src=world.cfg["rel4_addr"],dst=world.cfg["srv4_addr"])
    discover /= UDP(sport=68,dport=67)/BOOTP(chaddr=hw, giaddr="192.0.2.1")
    dhcp = DHCP(options=opts)
    discover /= dhcp
    return discover
