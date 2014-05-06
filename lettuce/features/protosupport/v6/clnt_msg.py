from features.logging_facility import get_common_logger
from features.terrain import set_options, set_values
from lettuce.registry import world
from features.init_all import IFACE, CLI_MAC
from scapy.layers.dhcp6 import *


def client_msg_capture(step, msgType):
    if msgType == "SOLICIT":
        clientMsg = DHCP6_Solicit
    elif msgType == "REQUEST":
        clientMsg = DHCP6_Request

    sniffedMsg = sniff(count=1, iface=IFACE, stop_filter=lambda x: x.haslayer(clientMsg))
    assert sniffedMsg[-1].iaid is not 0, "iaid must not be a 0 number."
    world.climsg.append(sniffedMsg[-1])
    assert len(world.climsg[world.clntCounter]) is not 0, "different len: %d" %len(world.climsg[world.clntCounter])
    assert world.climsg[world.clntCounter].haslayer(clientMsg)
    # temporary code for checking iaid
    if clientMsg == DHCP6_Solicit:
        world.iaid = world.climsg[world.clntCounter].iaid
    if clientMsg == DHCP6_Request:
        assert world.iaid == sniffedMsg[0].iaid, "IA_IDs are different in clients messages."


def client_msg_contains_opt(step, contain, opt):
    isFound = find_option(opt)
    if contain:
        assert isFound == True, "expected option " + str(opt) + " was not found in message."
    else:
        assert isFound == False, str(opt) + " should not be present in message."


def find_option(opt):
    # received msg from client must not be changed - make a copy of it
    tmp = world.climsg[world.clntCounter].copy()
    # 0 - ether, 1 - ipv6, 2 - udp, 3 - dhcpv6, 4 - opts
    tmp = tmp.getlayer(4)
    while tmp:
        if tmp.optcode == int(opt):
            return True
        tmp = tmp.payload
    return False


def send_msg_to_client(step, msgType):
    if msgType == "ADVERTISE":
        serverMsg = DHCP6_Advertise(msgtype=2)
    elif msgType == "REPLY":
        serverMsg = DHCP6_Reply(msgtype=7)
    ipAddr = world.climsg[world.clntCounter].payload.src
    msg = IPv6(dst=ipAddr)/UDP(dport=546, sport=547)/serverMsg
    msg.trid = world.climsg[world.clntCounter].trid
    msg /= DHCP6OptClientId(duid=world.climsg[world.clntCounter].duid, optlen=14)
    srvDuid = DHCP6OptServerId(duid=DUID_LLT(hwtype=1, lladdr=CLI_MAC, type=1, timeval=434123369),
                            optlen=14, optcode=2)
    msg /= srvDuid/DHCP6OptIA_PD(optcode=25, T2=0, T1=0, iaid=world.climsg[world.clntCounter].iaid,
                                 iapdopt=[DHCP6OptIAPrefix(preflft=3000,validlft=2000,
                                 plen=64, prefix="3000::")])
    send(msg)
    world.clntCounter += 1





