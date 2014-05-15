from features.logging_facility import get_common_logger
from features.terrain import set_options, set_values
from lettuce.registry import world
from features.init_all import IFACE, CLI_MAC, CLI_LINK_LOCAL, SRV_IPV6_ADDR_LINK_LOCAL, SOFTWARE_UNDER_TEST
from scapy.layers.dhcp6 import *
import time
import importlib

SRV_IP6 = CLI_LINK_LOCAL
CLI_IP6 = SRV_IPV6_ADDR_LINK_LOCAL

clntFunc = importlib.import_module("softwaresupport.%s.functions"  % SOFTWARE_UNDER_TEST)

def client_msg_wrong_capture(step, wrongMsgType, correctMsgType):
    #step is used to check client answer for server's incorrect message
    # tell client_msg_capture step that msg is already sniffed and it
    # doesn't have to worry about it
    world.clntCfg["wasSniffed"] = True

    if wrongMsgType == "SOLICIT":
        wrongClientMsg = DHCP6_Solicit
    elif wrongMsgType == "REQUEST":
        wrongClientMsg = DHCP6_Request

    if correctMsgType == "SOLICIT":
        correctClientMsg = DHCP6_Solicit
    elif correctMsgType == "REQUEST":
        correctClientMsg = DHCP6_Request

    sniffedMsg = sniff(count=1, iface=IFACE, stop_filter=lambda x: x.haslayer(correctClientMsg))
    world.climsg.append(sniffedMsg[0])

    assert world.climsg[-1].haslayer(wrongClientMsg) == False, "%s message present in packet but " \
                                                               "not expected." % (wrongClientMsg)
    assert world.climsg[-1].haslayer(correctClientMsg) == True, "%s message is not present in packet but" \
                                                                "expected." % (correctClientMsg)

def client_msg_capture(step, msgType):
    # step sniffs message sent by client and stores it in list

    # prepare cliopts for new sniffed message
    world.cliopts = []
    #  sniffing client message on specified interface
    # TODO: support more types of messages;
    if msgType == "SOLICIT":
        clientMsg = DHCP6_Solicit
    elif msgType == "REQUEST":
        clientMsg = DHCP6_Request
    elif msgType == "RELEASE":
        clientMsg = DHCP6_Release
        clntFunc.release_command()

    # if step client_msg_wrong_capture was not executed, the message was not sniffed;
    # therefore the flag is still set to false and we need to sniff it :)
    if world.clntCfg["wasSniffed"] is False:
        sniffedMsg = sniff(count=1, iface=IFACE, stop_filter=lambda x: x.haslayer(clientMsg))
        world.climsg.append(sniffedMsg[-1])

    # world.time was set after sending generic server's msg to client;
    # this statement computes interval between receiving advertise
    # and sending request msg. note that preference option is not set to 255
    # if it is, then this statement is useless and will probably fail test
    # TODO: provide some flag in case of preference equal to 255
    if world.time is not None:
        world.time = time.time() - world.time

    assert world.climsg[-1].iaid is not 0, "iaid can not be a 0 number."
    assert len(world.climsg[world.clntCounter]) is not 0, "Got empty message... Exiting."

    # double check if we sniffed packet that we wanted
    assert world.climsg[-1].haslayer(clientMsg), "sniffed wrong message."

    # saving iaid value from first message received
    if world.iaid is None:
        if hasattr(world.climsg[-1], "iaid"):
            world.iaid = world.climsg[-1].iaid
        else:
            get_common_logger().error("No IAID attribute in message.")

    # fill world.cliopts with dhcpv6 options from sniffed message
    msg_traverse(world.climsg[-1])

    sniffedMsg = None

    # set this flag to false in case if it was set to true by client_msg_wrong_capture step;
    # it is mandatory for further sniffing client messages without need to execute other steps
    world.clntCfg["wasSniffed"] = False


def send_msg_to_client(step, response, msgType, newLink):
    # step sends created message to client

    world.clntCfg["response"] = response
    build_client_msg(msgType, newLink)

    send(world.srvmsg[-1], realtime=True)

    # set timestamp after sending msg
    if world.time is None:
        world.time = time.time()
    if not response:
        # if clntCounter is not increased, then we can fire packets with,
        # for example, the same trid;
        # useful when checking if client without preference 255 waits some
        # amount of time (collects advertises) and then sends request.
        world.clntCounter += 1


def add_option(step, msgType, optcode):
    # add options to server's generic message
    # TODO: support for many different options :)

    if msgType == "IA_PD":
        world.cfg["add_option"]["IA_PD"] = True
    elif msgType == "IA_Prefix":
        world.cfg["add_option"]["IA_Prefix"] = True
        world.srvopts.append(DHCP6OptIAPrefix(preflft=world.clntCfg["values"]["preferred-lifetime"],
                                              validlft=world.clntCfg["values"]["valid-lifetime"],
                                              plen=world.clntCfg["values"]["prefix-len"],
                                              prefix=world.clntCfg["values"]["prefix"]))
    elif msgType == "Status_Code":
        world.cfg["add_option"]["status_code"] = True
        world.srvopts = []
        world.srvopts.append(DHCP6OptStatusCode(statuscode=int(optcode)))
    elif msgType == "preference":
        world.cfg["add_option"]["preference"] = True
        world.pref = DHCP6OptPref(prefval=int(optcode))


def add_another_option(step, msgType):
    # add option that was already added - in case we want for example
    # two prefixes in ia_pd, this option is used
    # TODO: support for many different options :)

    if msgType == "IA_Prefix":
        world.srvopts.append(DHCP6OptIAPrefix(preflft=world.clntCfg["values"]["preferred-lifetime"],
                                              validlft=world.clntCfg["values"]["valid-lifetime"],
                                              plen=world.clntCfg["values"]["prefix-len"],
                                              prefix=world.clntCfg["values"]["prefix"]))


def build_client_msg(msgType, newLink):
    # step that creates server's message with additional options

    if msgType == "ADVERTISE":
        serverMsg = DHCP6_Advertise(msgtype=2)
    elif msgType == "REPLY":
        serverMsg = DHCP6_Reply(msgtype=7)

    msg = IPv6(src=SRV_IP6, dst=CLI_IP6)/UDP(dport=546, sport=547)/serverMsg

    # this needs some validation...
    try:
        msg.trid = world.climsg[world.clntCounter].trid
        msg /= DHCP6OptClientId(duid=world.climsg[world.clntCounter].duid, optlen=14)
    except IndexError:
        msg.trid = world.climsg[-1].trid
        msg /= DHCP6OptClientId(duid=world.climsg[-1].duid, optlen=14)

    srvDuid = DHCP6OptServerId(duid=DUID_LLT(hwtype=1, lladdr=CLI_MAC, type=1, timeval=434123369),
                            optlen=14, optcode=2)
    msg /= srvDuid
    # add_option ia_pd doesn't make sense for server's msg
    if world.cfg["add_option"]["IA_PD"]:
        msg /= DHCP6OptIA_PD(optcode=25, T2=world.clntCfg["values"]["T2"], T1=world.clntCfg["values"]["T1"],
                             iaid=world.climsg[-1].iaid)
    if world.cfg["add_option"]["IA_Prefix"]:
        msg /= DHCP6OptIA_PD(optcode=25, T2=world.clntCfg["values"]["T2"], T1=world.clntCfg["values"]["T1"],
                             iaid=world.climsg[-1].iaid,
                             iapdopt=[]
                            )
        for prefix in world.srvopts:
            msg.iapdopt.append(prefix)
    if world.cfg["add_option"]["status_code"]:
        msg /= DHCP6OptIA_PD(optcode=25, T2=world.clntCfg["values"]["T2"], T1=world.clntCfg["values"]["T1"],
                             iaid=world.climsg[-1].iaid, iapdopt=[])
        for status_code in world.srvopts:
            msg.iapdopt.append(status_code)
    if world.cfg["add_option"]["preference"]:
        if world.pref is not None:
            msg /= world.pref

    world.srvmsg.append(msg)


def srv_msg_clean(step):
    # flush server options list

    world.srvopts = []
    world.pref = None


# FIXME : probably wrong approach to measuring time interval for request message
def client_check_time_delay(step, timeval):
    # actually, computed value seems to match time delta values from wireshark.

    assert world.time >= float(timeval), "Client respond in shorter time than %.3f " \
                                         "second. Response time: %.3f" % (float(timeval), world.time)
    world.time = None


def client_cmp_values(step, value):
    # compare saved value with value from present message

    msg = world.climsg[-1]
    val = str(value).lower()
    cmp1 = getattr(msg, val)
    cmp2 = getattr(world, val)
    assert cmp1 == cmp2, "%s values are different: %d != %d.\n" % (val, cmp1, cmp2)


def msg_set_value(step, value_name, new_value):
    # set value different than value from values dictionary
    # it is for server's message of course

    if value_name in world.clntCfg["values"]:
        if isinstance(world.clntCfg["values"][value_name], str):
            world.clntCfg["values"][value_name] = str(new_value)
        elif isinstance(world.clntCfg["values"][value_name], int):
            world.clntCfg["values"][value_name] = int(new_value)
        else:
            world.clntCfg["values"][value_name] = new_value
    else:
        assert value_name in world.clntCfg["values"], "Unknown value name : %s" % value_name


def msg_traverse(msg):
    # this function breaks into pieces present client message;
    # cliopts will contain following lists for every layer:
    # optcode, layer; this will only parse options

    localMsg = msg.copy()
    localMsg = localMsg.getlayer(4)
    while localMsg:
        layer = localMsg.copy()
        layer.remove_payload()
        world.cliopts.append([layer.optcode, layer])
        localMsg = localMsg.payload


def client_msg_contains_opt(step, contain, opt):
    # this step checks by optcode whether present client message
    # contains option that we are looking for

    isFound = find_option(opt)
    if contain:
        assert isFound == True, "expected option " + str(opt) + " was not found in message."
    else:
        assert isFound == False, str(opt) + " should not be present in message."


def find_option(opt):
    # this function checks for option defined with optcode;
    # it could be implemented differently - by checking entries in world.cliopts

    # received msg from client must not be changed - make a copy of it
    tmp = world.climsg[world.clntCounter].copy()
    # 0 - ether, 1 - ipv6, 2 - udp, 3 - dhcpv6, 4 - opts
    tmp = tmp.getlayer(4)
    while tmp:
        if tmp.optcode == int(opt):
            return True
        tmp = tmp.payload
    return False


def client_msg_contains_subopt(step, opt_code, contain, subopt_code):
    # this step verifies whether in specific option exists specific suboption;

    for entry in world.cliopts:
        if int(opt_code) == entry[0]:
            if entry[0] == 25:
                if len(entry[1].iapdopt) > 0:
                    for subopt in entry[1].iapdopt:
                        world.subopts.append((entry[0],subopt.optcode, subopt))
    found = False
    for subopt in world.subopts:
        if subopt[1] == int(subopt_code):
            found = True
    if contain:
        assert found is True, "sub-option %d from %d option not found in " \
                              "message." % (int(subopt_code), int(opt_code))
    else:
        assert found is False, "sub-option %d from %d option found in message, " \
                               "but not expected" % (subopt_code, opt_code)


def client_opt_check_value(step, opt_code, expect, value_name, value):
    # this step compares proper value from message with value given in step;

    found = False
    for entry in world.cliopts:
        if entry[0] == int(opt_code):
            if hasattr(entry[1], value_name):
                if getattr(entry[1], value_name) == int(value):
                    found = True
    if expect:
        assert found is True, "%s has different value than expected." % str(value_name)
    else:
        assert found is False, "%s has %s value, but it shouldn't." % (str(value_name), str(value))


def client_subopt_check_value(step, subopt_code, opt_code, expect, value_name, value):
    # same as client_opt_check_value, but for suboption;

    found = False
    for entry in world.subopts:
        if entry[0] == int(opt_code) and entry[1] == int(subopt_code):
            if hasattr(entry[2], value_name):
                toCheck = getattr(entry[2], value_name)
                type_ = type(toCheck)
                if toCheck == type_(value):
                    found = True
    if expect:
        assert found is True, "%s value is different than expected." % (value_name)
    else:
        assert found is False, "found value which was not expected"


def client_msg_count_opt(step, contain, count, optcode):
    # step for checking count of option with certain opt-code in message;

    localCounter = 0
    for entry in world.cliopts:
        if entry[0] == int(optcode):
            localCounter += 1

    if contain:
        assert int(count) is localCounter, "count of option %d does not match with given value." % (int(optcode))
    else:
        assert int(count) is not localCounter, "count of option %d does match with given value," \
                                               " but it should not." % (int(optcode))


def client_msg_count_subopt(step, contain, count, subopt_code, opt_code):
    localCounter = 0
    for entry in world.subopts:
        if entry[0] == int(opt_code) and entry[1] == int(subopt_code):
            localCounter += 1

    if contain:
        assert localCounter is int(count), "count of suboption %d does not match with given value." % (int(subopt_code))
    else:
        assert int(count) is not localCounter, "count of suboption %d does match with given value," \
                                               " but it should not." % (int(subopt_code))


def client_check_field_presence(step, field, contain, optcode):
    # step for checking fields presence in option;

    found = False
    for entry in world.cliopts:
        if entry[0] == int(optcode):
            if hasattr(entry[1], field):
                found = True
    if contain:
        assert found is True, "message has wrong format - no %s field." % (str(field))
    else:
        assert found is False, "field %s was found in message but it was not expected." % (str(field))



