from features.logging_facility import get_common_logger
from features.terrain import set_options, set_values
from lettuce.registry import world
from features.init_all import IFACE
from scapy.layers.dhcp6 import *


def client_msg_capture(step, msgType):
    if msgType == "SOLICIT":
        clientMsg = DHCP6_Solicit
    elif msgType == "REQUEST":
        clientMsg = DHCP6_Request
    temp = sniff(count=1, iface=IFACE, stop_filter=lambda x: x.haslayer(clientMsg))
    world.climsg.append(temp[-1])
    assert len(world.climsg[world.clntCounter]) is not 0, "different len: %d" %len(world.climsg[world.clntCounter])
    assert world.climsg[world.clntCounter].haslayer(clientMsg)


def send_msg_to_client(step, msgType):
    if msgType == "ADVERTISE":
        serverMsg = DHCP6_Advertise(msgtype=2)
    elif msgType == "REPLY":
        serverMsg = DHCP6_Reply(msgtype=7)
    msg = IPv6(src='fe80::a00:27ff:fec5:3fea', dst='fe80::a00:27ff:fead:66d3')/UDP(dport=546, sport=547)/\
          serverMsg
    msg.trid = world.climsg[world.clntCounter].trid
    msg /= DHCP6OptClientId(duid=world.climsg[world.clntCounter].duid, optlen=14)
    srvDuid = DHCP6OptServerId(duid=DUID_LLT(hwtype=1, lladdr='08:00:27:c5:3f:ea', type=1, timeval=434123369),
                            optlen=14, optcode=2)
    # world.srvmsg.append(srvDuid)
    msg /= srvDuid/DHCP6OptIA_PD(optcode=25, T2=0, T1=0, iaid=world.climsg[world.clntCounter].iaid,
                                 iapdopt=[DHCP6OptIAPrefix(preflft=1000,validlft=2000,
                                 plen=64, prefix="3000::")])
    send(msg)
    world.clntCounter += 1





