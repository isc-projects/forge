from features.logging_facility import get_common_logger
from features.terrain import set_options, set_values
from lettuce.registry import world
from features.init_all import IFACE, CLI_MAC, CLI_LINK_LOCAL, SRV_IPV6_ADDR_LINK_LOCAL, SOFTWARE_UNDER_TEST
from scapy.layers.dhcp6 import *
from scapy.sendrecv import debug
import time
import importlib
import random

SRV_IP6 = CLI_LINK_LOCAL
CLI_IP6 = SRV_IPV6_ADDR_LINK_LOCAL

clntFunc = importlib.import_module("softwaresupport.%s.functions"  % SOFTWARE_UNDER_TEST)


def client_msg_capture(step, msgType, tout_):
    # step sniffs message sent by client and stores it in list

    # prepare cliopts for new sniffed message
    # TODO: support more types of messages;
    if msgType == "SOLICIT":
        clientMsg = DHCP6_Solicit
    elif msgType == "REQUEST":
        clientMsg = DHCP6_Request
    elif msgType == "RENEW":
        clientMsg = DHCP6_Renew
    elif msgType == "REBIND":
        clientMsg = DHCP6_Rebind
    elif msgType == "RELEASE":
        clientMsg = DHCP6_Release
        clntFunc.release_command()

    if not tout_:
        sniffedMsg = sniff(iface=IFACE, timeout=10, stop_filter=lambda x: x.haslayer(clientMsg))
    else:
        sniffedMsg = sniff(iface=IFACE, stop_filter=lambda x: x.haslayer(clientMsg))
    world.climsg.append(sniffedMsg[-1])
    received = ""
    for msg in sniffedMsg:
        received += get_msg_type(msg) + " "

    # world.time was set after sending generic server's msg to client;
    # this statement computes interval between receiving advertise
    # and sending request msg. note that preference option is not set to 255
    # if it is, then this statement is useless and will probably fail test
    # TODO: provide some flag in case of preference equal to 255
    if world.time is not None:
        world.time = time.time() - world.time
        print world.time

    assert len(world.climsg[world.clntCounter]) is not 0, "Got empty message... Exiting."

    # double check if we sniffed packet that we wanted
    assert world.climsg[-1].haslayer(clientMsg), "Sniffed wrong message. " \
                                                 "Following messages were sniffed: %s." % (received)

    # fill world.cliopts with dhcpv6 options from sniffed message
    msg_traverse(world.climsg[-1])
    sniffedMsg = None


def server_build_msg(step, response, msgType):
    # step that creates server's message with additional options

    if msgType == "ADVERTISE":
        serverMsg = DHCP6_Advertise(msgtype=2)
    elif msgType == "REPLY":
        serverMsg = DHCP6_Reply(msgtype=7)

    msg = IPv6(src=SRV_IP6, dst=CLI_IP6)/UDP(dport=546, sport=547)/serverMsg

    # this needs some validation...
    if not world.clntCfg['set_wrong']['trid']:
        try:
            msg.trid = world.climsg[world.clntCounter].trid
        except IndexError:
            msg.trid = world.climsg[-1].trid
    else:
        msg.trid = random.randint(0, 256*256*256)

    if world.cfg["add_option"]["client_id"]:
        if not world.clntCfg['set_wrong']['client_id']:
            try:
                msg /= DHCP6OptClientId(duid=world.climsg[world.clntCounter].duid, optlen=14)
            except IndexError:
                msg /= DHCP6OptClientId(duid=world.climsg[-1].duid, optlen=14)
        else:
            msg /= DHCP6OptClientId(duid=DUID_LLT(hwtype=1, lladdr=CLI_MAC, type=1, 
                                    timeval=world.clntCfg['timeval']), optlen=14, optcode=1)

    if not world.cfg["add_option"]["server_id"]:
        if not world.clntCfg['set_wrong']['server_id']:
            msg /= DHCP6OptServerId(duid=DUID_LLT(hwtype=1, lladdr=CLI_MAC, type=1, 
                                    timeval=world.clntCfg['timeval']), optlen=14, optcode=2)
        else:
            # make it blank like wlodek does?
            msg /= DHCP6OptServerId(duid=DUID_LLT(hwtype=1, lladdr="00:01:02:03:04:05", type=1, 
                                    timeval=random.randint(0, 256*256*256)), optlen=14, optcode=2)
    
    for option in world.srvopts:
        msg /= option

    world.srvmsg.append(msg)
    if msgType == "REPLY":
        get_lease()
        send(msg)
        world.time = time.time()

    if not response:
        # if clntCounter is not increased, then we can fire packets with,
        # for example, the same trid;
        # useful when checking if client without preference 255 waits some
        # amount of time (collects advertises) and then sends request.
        world.clntCounter += 1

    set_values()
    set_options()


def server_set_wrong_val(step, value):
    if value == "trid":
        world.clntCfg['set_wrong']['trid'] = True
    elif value == "iaid":
        world.clntCfg['set_wrong']['iaid'] = True
    elif value == "client_id":
        world.clntCfg['set_wrong']['client_id'] = True
    elif value == "server_id":
        world.clntCfg['set_wrong']['server_id'] = True


def server_not_add(step, opt):
    if opt == "client_id":
        world.cfg["add_option"]["client_id"] = False
    elif opt == "server_id":
        world.cfg["add_option"]["server_id"] = True


def add_option(step, opt, optcode):
    # add options to server's generic message
    # TODO: support for many different options :)

    if opt == "IA_PD":
        if not world.clntCfg['set_wrong']['iaid']:
            if len(world.iaid) > world.clntCounter:
                if len(world.iaid[world.clntCounter]) > 1:
                    id_ = world.iaid[world.clntCounter].pop()
                else:
                    id_ = world.iaid[world.clntCounter][0]
            else:
                id_ = world.iaid[0][0]
        else:
            id_ = random.randint(0, 256*256*256)
        world.srvopts.append(DHCP6OptIA_PD(optcode=25, 
                                           T2=world.clntCfg["values"]["T2"],
                                           T1=world.clntCfg["values"]["T1"],
                                           iaid=id_,
                                           iapdopt=[]))

                                           
    elif opt == "IA_Prefix":
        world.srvopts[-1].iapdopt.append(
            DHCP6OptIAPrefix(preflft=world.clntCfg["values"]["preferred-lifetime"],
                             validlft=world.clntCfg["values"]["valid-lifetime"],
                             plen=world.clntCfg["values"]["prefix-len"],
                             prefix=world.clntCfg["values"]["prefix"]))

    elif opt == "Status_Code":
        world.srvopts[-1].iapdopt.append(DHCP6OptStatusCode(statuscode=int(optcode)))

    elif opt == "preference":
       world.srvopts.append(DHCP6OptPref(prefval=int(optcode)))

    elif opt == "rapid_commit":
        world.srvopts.append(DHCP6OptRapidCommit())

    elif opt == "option_request":
        world.srvopts.append(DHCP6OptOptReq())

    elif opt == "elapsed_time":
        world.srvopts.append(DHCP6OptElapsedTime())

    elif opt == "iface_id":
        world.srvopts.append(DHCP6OptIfaceId(ifaceid=world.cfg["values"]["ifaceid"]))

    elif opt == "reconfigure":
        world.srvopts.append(DHCP6OptReconfMsg())

    elif opt == "relay_message":
        world.srvopts.append(DHCP6OptRelayMsg())

    elif opt == "server_unicast":
        world.srvopts.append(DHCP6OptServerUnicast(srvaddr=SRV_IP6))


def client_send_receive(step, contain, msgType):
    # step sends created message to client and waits for client's answer
    found = False
    debug.recv = []
    conf.use_pcap = True
    templen = len(world.climsg)

    if msgType == "REQUEST":

        conf.debug_match = True
        ans, unans = sr(world.srvmsg, iface=IFACE, nofilter=1, timeout = 2, verbose = 99, clnt=1)
        # print ans
        for entry in ans:
            sent, received = entry
            # print sent.show(), received.show()
            world.climsg.append(received)
            get_common_logger().info("Received packet type = %s" % get_msg_type(received))
            msg_traverse(world.climsg[-1])
            if get_msg_type(received) == msgType:
                found = True
        # print unans
        for x in unans:
            get_common_logger().error(("Unmatched packet type = %s" % get_msg_type(x)))
        get_common_logger().debug("Received traffic (answered/unanswered): %d/%d packet(s)."
            % (len(ans), len(unans)))

    # set timestamp after sending msg
    if world.time is None:
        world.time = time.time()

    world.srvmsg = []

    if contain:
        assert len(world.climsg) > templen, " No response received."
        assert found is True, "message not found"
    else:
        assert found is False, "message found but not expected"


def srv_msg_clean(step):
    # flush server options list

    world.srvopts = []
    world.pref = None
    set_values()
    set_options()


def get_msg_type(msg):
    msg_types = { "SOLICIT": DHCP6_Solicit,
                  "REQUEST": DHCP6_Request,
                  "RENEW": DHCP6_Renew,
                  "REBIND": DHCP6_Rebind,
                  "RELEASE": DHCP6_Release
                }

    # 0th is IPv6, 1st is UDP, 2nd should be DHCP6
    if type(msg) == Ether:
        dhcp = msg.getlayer(3)
    else:
        dhcp = msg.getlayer(2)

    for msg_name in msg_types.keys():
        if type(dhcp) == msg_types[msg_name]:
            return msg_name

    return "UNKNOWN-TYPE"


# FIXME : probably wrong approach to measuring time interval for request message
def client_check_time_delay(step, timeval):
    # actually, computed value seems to match time delta values from wireshark.

    assert world.time >= float(timeval), "Client respond in shorter time than %.3f " \
                                         "second. Response time: %.3f" % (float(timeval), world.time)
    world.time = None


def client_cmp_values(step, value):
    # compare saved value with value from present message
    # currently, only one value can be checked.
    # clean container after comparing values.

    val = str(value).lower()
    assert world.saved[-1].sort() is world.saved[len(world.saved)-2].sort(), \
                                    "compared %s values are different." % (val)
    world.saved = []
    world.clntCfg['toSave'] = None


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

def save_value(step, value):
    world.clntCfg['toSave'] = value.lower()
    

def msg_traverse(msg):
    # this function breaks into pieces present client message;
    # cliopts will contain following lists for every layer:
    # optcode, layer; this will only parse options

    world.cliopts = []
    localMsg = msg.copy()
    temp = []
    tempIaid = []

    if type(localMsg) == Ether:
        localMsg = localMsg.getlayer(4)
    else:
        localMsg = localMsg.getlayer(3)

    while localMsg:
        layer = localMsg.copy()
        layer.remove_payload()
        if hasattr(layer, "iaid"):
            tempIaid.append(layer.iaid)
        # it is important to save every value, not just one;
        # client can request for multiple ia_pd's, so values
        # are stored in list
        if world.clntCfg['toSave'] is not None:
            if hasattr(layer, world.clntCfg['toSave']):
                saving = getattr(layer, world.clntCfg['toSave'])
                temp.append(saving)
        world.cliopts.append([layer.optcode, layer])
        localMsg = localMsg.payload
    world.saved.append(temp)
    world.iaid.append(tempIaid)


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
    if type(tmp) == Ether:
        tmp = tmp.getlayer(4)
    else:
        tmp = tmp.getlayer(3)
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
        assert int(count) is localCounter, "count of option %d does not match with" \
                                           " given value." % (int(optcode))
    else:
        assert int(count) is not localCounter, "count of option %d does match with " \
                                               "given value," \
                                               " but it should not." % (int(optcode))

def client_msg_count_subopt(step, contain, count, subopt_code, opt_code):
    localCounter = 0
    for entry in world.subopts:
        if entry[0] == int(opt_code) and entry[1] == int(subopt_code):
            localCounter += 1

    if contain:
        assert localCounter is int(count), "count of suboption %d does not match with" \
                                           " given value." % (int(subopt_code))
    else:
        assert int(count) is not localCounter, "count of suboption %d does match with" \
                                               " given value," \
                                               " but it should not." % (int(subopt_code))


def client_check_field_presence(step, contain, field, optcode):
    # step for checking fields presence in option;

    found = False
    for entry in world.cliopts:
        if entry[0] == int(optcode):
            if hasattr(entry[1], field):
                found = True
    if contain:
        assert found is True, "message has wrong format - no %s field." % (str(field))
    else:
        assert found is False, "field %s was found in message but it" \
                               " was not expected." % (str(field))


def get_lease():
    # make lease structure from scapy options
    # format is the same as lease from ParseISCString
    result = {}
    result['lease6'] = {}
    pdList = [iapd for iapd in world.srvopts if iapd.optcode == 25]
    for pd in pdList:
        pdDict = {}
        pdDict['renew'] ='''"''' + str(pd.T1) + '''"'''
        pdDict['rebind'] = '''"''' + str(pd.T2) + '''"'''
        prefixList = [prefix for prefix in pd.iapdopt if prefix.optcode == 26]
        for prefix in prefixList:
            prefixDict = {}
            prefixDict['preferred-life'] = '''"''' + str(prefix.preflft) + '''"'''
            prefixDict['max-life'] = '''"''' + str(prefix.validlft) + '''"'''
            pdDict['iaprefix ' + '''"''' + str(prefix.prefix) + '/' +
                   str(prefix.plen) + '''"'''] = dict(prefixDict)
            if SOFTWARE_UNDER_TEST == "isc_dhcp6_client":
                hexIaid = hex(pd.iaid)[2:]
                hexIaid = ':'.join(a+b for a,b in zip(hexIaid[::2], hexIaid[1::2]))
            else:
                hexIaid = pd.iaid

        result['lease6']['ia-pd ' + '''"''' + str(hexIaid) + '''"'''] = dict(pdDict)
    
    world.clntCfg['scapy_lease'] = result
