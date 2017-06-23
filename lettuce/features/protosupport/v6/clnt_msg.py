# Copyright (C) 2014 Internet Systems Consortium.
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

# Author: Maciek Fijalkowski


from features.logging_facility import get_common_logger
from lettuce.registry import world
from scapy.layers.dhcp6 import *
from scapy.sendrecv import debug
import time
import importlib
import random

############################################################################
#TODO That import have to be switched to ForgeConfiguration class, world.f_cfg
# from features.init_all import IFACE, CLI_MAC, CLI_LINK_LOCAL, \
#                               SRV_IPV6_ADDR_LINK_LOCAL, SOFTWARE_UNDER_TEST

IFACE=""
CLI_MAC =""
CLI_LINK_LOCAL = ""
SRV_IPV6_ADDR_LINK_LOCAL = ""
SOFTWARE_UNDER_TEST = ""
############################################################################

SRV_IP6 = CLI_LINK_LOCAL
CLI_IP6 = SRV_IPV6_ADDR_LINK_LOCAL

#clntFunc = importlib.import_module("softwaresupport.%s.functions"  % SOFTWARE_UNDER_TEST)


def set_timer(step, timer_val):
    """
    @step("Set timer to (\S+).")

    This step sets a timer to a provided value. It can take values from
    world.clntCfg["values"] dictionary (T1, T2, preferred-lifetime,
    valid-lifetime) or be set to an implicit value, like 1234. By default,
    timer value is set to 10.
    """
    #if timer_val is T1, T2 or prev/valid
    if str(timer_val) in world.clntCfg["values"].keys():
        if isinstance(world.clntCfg["values"][str(timer_val)], int):
            world.clntCfg["values"]["timer"] = world.clntCfg["values"][str(timer_val)]
        else:
            assert False, "If you are passing a timer not as number, then it" \
                          " has to be an int in values dictionary."
    #else check if it was passed as number
    else:
        try:
            tmp = int(timer_val)
        except ValueError:
            assert False, "Wrong timer value was given. It was neither a " \
                          "number, nor a T1/T2/prev/valid. Aborting."
        world.clntCfg["values"]["timer"] = tmp


def client_msg_capture(step, msgType, tout_):
    """
    @step("Sniffing client (\S+) message from network( with timeout)?.")

    Step sniffs message(s) sent by client and stores it in list. It is an 
    important step and a lot of things take place here. We can sniff a
    message with or without a timeout. If, after reaching timeout, specific
    message was not sniffed, whole test fails. 
    Sniffed message is splitted onto particular options and stored in 
    variable. Time of receiving message is also saved.
    """

    if msgType == "SOLICIT":
        clientMsg = DHCP6_Solicit
    elif msgType == "REQUEST":
        clientMsg = DHCP6_Request
    elif msgType == "RENEW":
        clientMsg = DHCP6_Renew
        # RTranges is a set for measuring retransmission times of messages;
        # It was designed initially to support SOLICIT and REQUEST msgs;
        # In order to use it for RENEW/REBIND messages, we need to ignore
        # previous values and T1/T2 timers - therefore we are erasing 
        # RTranges two times;
        check_is_solicit_rt()
    elif msgType == "REBIND":
        clientMsg = DHCP6_Rebind
        check_is_solicit_rt()
    elif msgType == "RELEASE":
        clientMsg = DHCP6_Release
        clntFunc.release_command()

    if not tout_:
        sniffedMsg = sniff(iface=IFACE, timeout=world.clntCfg["values"]["timer"],
                           stop_filter=lambda x: x.haslayer(clientMsg))
    else:
        sniffedMsg = sniff(iface=IFACE, stop_filter=lambda x: x.haslayer(clientMsg))
    world.climsg.append(sniffedMsg[-1])
    received = ""
    for msg in sniffedMsg:
        received += get_msg_type(msg) + " "

    world.timestamps.append(time.time())
    if len(world.timestamps) >= 2:
        world.RTlist.append(world.timestamps[-1] - world.timestamps[-2])
        compute_rt_range()

    # world.time was set after sending generic server's msg to client;
    # this statement computes interval between receiving advertise
    # and sending request msg. note that preference option is not set to 255
    # if it is, then this statement is useless and will probably fail test
    # TODO: provide some flag in case of preference equal to 255
    if world.time is not None:
        world.time = time.time() - world.time

    assert len(world.climsg[world.clntCounter]) is not 0, "Got empty message..."\
                                                          "Exiting."

    # double check if we sniffed packet that we wanted
    assert world.climsg[-1].haslayer(clientMsg), "Sniffed wrong message. " \
                                                 "Following messages were " \
                                                 "sniffed: %s." % (received)

    # fill world.cliopts with dhcpv6 options from sniffed message
    msg_traverse(world.climsg[-1])
    sniffedMsg = None


def server_build_msg(step, response, msgType):
    """
    @step("Server sends (back )?(\S+) message.")

    Step is used for sending server's message to client. Mostly, it is
    used to send a REPLY message. If current message is ADVERTISE, the
    message is only build with this step and it would be sent with
    "Client MUST (NOT )?respond with (\S+) message." step.
    """

    if msgType == "ADVERTISE":
        serverMsg = DHCP6_Advertise(msgtype=2)
    elif msgType == "REPLY":
        serverMsg = DHCP6_Reply(msgtype=7)

    msg = IPv6(src=SRV_IP6, dst=CLI_IP6)/UDP(dport=546, sport=547)/serverMsg

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
                msg /= DHCP6OptClientId(duid=world.climsg[world.clntCounter].duid, 
                                        optlen=14)
            except IndexError:
                msg /= DHCP6OptClientId(duid=world.climsg[-1].duid, optlen=14)
        else:
            msg /= DHCP6OptClientId(duid=DUID_LLT(hwtype=1, lladdr=CLI_MAC, type=1, 
                                    timeval=world.clntCfg['timeval']),
                                    optlen=14, optcode=1)

    if not world.cfg["add_option"]["server_id"]:
        if not world.clntCfg['set_wrong']['server_id']:
            msg /= DHCP6OptServerId(duid=DUID_LLT(hwtype=1, lladdr=CLI_MAC, type=1, 
                                    timeval=world.clntCfg['timeval']),
                                    optlen=14, optcode=2)
        else:
            msg /= DHCP6OptServerId(duid=DUID_LLT(hwtype=1,
                                                  lladdr="00:01:02:03:04:05",
                                                  type=1, 
                                                  timeval=random.randint(0, 256*256*256)),
                                                  optlen=14,
                                                  optcode=2)
    
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

    world.set_values()
    #TODO after removing "set_options" from code v6 client testing should be rebuild
    #set_options()


def check_is_solicit_rt():
    """
    This is a helper function that provides retransmission time
    scopes for messages RENEW and REBIND. By default, retransmission
    times are computed for SOL_TIMEOUT and REQ_TIMEOUT (1s). This function
    provides those for REN_TIMEOUT and REB_TIMEOUT (10s).
    """
    if world.notSolicit < 2:
        world.RTranges = []
        world.RTranges.append([9.0, 11.0])
        world.notSolicit += 1


def server_set_wrong_val(step, value):
    """
    @step("Server sets wrong (\S+) value.")

    Step sets deliberately wrong value of given server's message
    component. It can be:
    - iaid,
    - client Id,
    - server Id,
    - transaction id.
    """

    if value == "trid":
        world.clntCfg['set_wrong']['trid'] = True
    elif value == "iaid":
        world.clntCfg['set_wrong']['iaid'] = True
    elif value == "client_id":
        world.clntCfg['set_wrong']['client_id'] = True
    elif value == "server_id":
        world.clntCfg['set_wrong']['server_id'] = True


def server_not_add(step, opt):
    """
    @step("Server does NOT add (\S+) option to message.")

    By default, to generic server message, options client id and server
    id are included. This step can provide not adding one of them, in
    order to check client's behaviour in that situation.
    """

    if opt == "client_id":
        world.cfg["add_option"]["client_id"] = False
    elif opt == "server_id":
        world.cfg["add_option"]["server_id"] = True


def add_option(step, opt, optcode):
    """
    @step("Server adds (\S+) (\d+ )?option to message.")

    Step adds an option to server's message. Options that can be added:
    -  IA_PD
    -  IA_Prefix
    -  Status_Code
    -  preference
    -  rapid_commit
    -  option_request
    -  elapsed_time
    -  iface_id
    -  reconfigure
    -  relay_message
    -  server_unicast
    """

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
            world.clntCfg['set_wrong']['iaid'] = False
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
    """
    @step("Client MUST (NOT )?respond with (\S+) message.")

    Step is responsible for sending previously prepared server's
    message and checking the response of a client. Scapy's sr()
    function is used here.
    """
    found = False
    debug.recv = []
    conf.use_pcap = True
    templen = len(world.climsg)

    if msgType == "REQUEST":

        conf.debug_match = True
        ans, unans = sr(world.srvmsg, iface=IFACE, nofilter=1, timeout = 2,
                        verbose = 99, clnt=1)
        # print ans
        for entry in ans:
            sent, received = entry
            # print sent.show(), received.show()
            world.climsg.append(received)
            world.timestamps.append(received.time)
            if len(world.timestamps) >= 2:
                world.RTlist.append(world.timestamps[-1] - world.timestamps[-2])
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
    
    #world.timestamps.append(time.time())
    world.srvmsg = []

    if contain:
        assert len(world.climsg) > templen, " No response received."
        assert found is True, "message not found"
    else:
        assert found is False, "message found but not expected"


def srv_msg_clean(step):
    """
    @step("Server builds new message.")

    Step prepares fresh instance of server's message. Previously saved
    values are removed and every other values are set to default.
    """

    world.srvopts = []
    world.pref = None
    world.set_values()
    #TODO after removing "set_options" from code v6 client testing should be rebuild
    #set_options()


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


def compute_rt_range():
    """
    RFC 3315, section 14:
    RT for each subsequent message transmission is based on the previous
    value of RT:
    RT = 2*RTprev + RAND*RTprev, RAND = <-0.1, 0.1>

    RTprev is stored by default in world.RTlist, so function can
    always count next RT based on a previous RT.
    """
    lowTime = world.RTlist[-1] * 2 + world.RTlist[-1] * (-0.1)
    highTime = world.RTlist[-1] * 2 + world.RTlist[-1] * 0.1
    world.RTranges.append([lowTime, highTime])


def client_rt_delay(step, timeval, dont_care):
    """
    @step("Message was (sent|retransmitted) after maximum (\S+) second(s)?.")

    Step for checking the time between last received message and the previous
    received message. This has nothing to do with retransmission times.
    This is used for example when we want to check that we have reached
    a maximum timeout for retransmission time.
    """
    assert world.RTlist[-1] <= float(timeval)


def client_time_interval(step):
    """
    @step("Retransmission time has required value.")

    Step is used for measuring message retransmission time and verifying
    it whether it fits in given time scope (which was previously computed).
    See retransmission_time_validation directory and tests in it.
    """
    
    rt = world.timestamps[-1] - world.timestamps[-2]
    assert rt >= world.RTranges[world.c][0], "Client respond in shorter time than" \
                                         " %.3f s. Response time: %.3f" % \
                                         (world.RTranges[world.c][0], rt)
    assert rt <= world.RTranges[world.c][1], "Client respond in longer time than" \
                                          " %.3f s. Response time: %.3f" % \
                                          (world.RTranges[world.c][1], rt)
    world.c += 1
    

def client_cmp_values(step, value):
    """
    @step("(\S+) value in client message is the same as saved one.")

    This step compares value from received client message with the value
    saved with "Save (\S+) value." step.
    """

    val = str(value).lower()
    # currently, only one value can be checked.
    assert world.saved[-1].sort() is world.saved[len(world.saved)-2].sort(), \
                                    "compared %s values are different." % (val)
    # clean container after comparing values.
    world.saved = []
    world.clntCfg['toSave'] = None


def msg_set_value(step, value_name, new_value):
    """
    @step("(\S+) value is set to (\S+).")

    Server sets value of one key from world.clntCfg["values"] 
    to different than its default value. It can be for example
    T1, T2, preferred-lifetime, valid-lifetime, prefix.
    """

    if new_value == '0xffffffff':
        new_value = 0xffffffff

    if str(value_name) in world.clntCfg["values"]:
        if isinstance(world.clntCfg["values"][str(value_name)], str):
            world.clntCfg["values"][str(value_name)] = str(new_value)
        elif isinstance(world.clntCfg["values"][str(value_name)], int):
            world.clntCfg["values"][str(value_name)] = int(new_value)
        else:
            world.clntCfg["values"][str(value_name)] = new_value
    else:
        assert str(value_name) in world.clntCfg["values"], "Unknown value " \
                                                           "name : %s" % str(value_name)


def save_value(step, value):
    """
    @step("Save (\S+) value.")

    Step saves value in variable for further comparison. One case of usage
    is checking the consistency of IAID value over message exchange.
    """
    world.clntCfg['toSave'] = value.lower()
    

def msg_traverse(msg):
    """
    This function breaks into pieces present client message;
    cliopts will contain following lists for every layer:
    optcode, layer; this will only parse options
    """

    world.clntCfg["values"]["dst_addr"] = ()
    world.cliopts = []
    localMsg = msg.copy()
    temp = []
    tempIaid = []

    if localMsg.haslayer(IPv6):
        dst_addr = localMsg.getlayer(IPv6).dst
        type_addr = "multicast" if dst_addr[0:2] == 'ff' else "unicast"
        world.clntCfg["values"]["dst_addr"] += (type_addr, dst_addr)

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


def client_dst_address_check(step, dst_type):
    """
    @step("Message was sent to (multicast|unicast) address.")

    Step checks whether message sent by dhcp client was sent to
    multicast or unicast address. If the destination address
    begins with 'ff', then it is interpreted as a multicast
    address. Otherwise, we assume that it is an unicast address.
    """
    assert str(dst_type) == world.clntCfg["values"]["dst_addr"][0], \
           "Destination address is %s and it's different than " \
           "expected." % world.clntCfg["values"]["dst_addr"][0]


def client_msg_contains_opt(step, contain, opt):
    """
    @step("Client message MUST (NOT )?contain option (\d+).")

    Step verifies the presence of particular option in received
    message from client. Options are checked by their option code.
    """

    isFound = find_option(opt)
    if contain:
        assert isFound == True, "expected option " + str(opt) + " was not found in message."
    else:
        assert isFound == False, str(opt) + " should not be present in message."


def find_option(opt):
    """
    This function checks for option defined with optcode;
    it could be implemented differently - by checking entries in world.cliopts
    """

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
    """
    @step("Client message MUST (NOT )?contain (\d+) options with opt-code (\d+).")

    Step verifies the presence of particular sub-option within option 
    in received message from client. Sub-options and options are checked 
    by their option code.
    """

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
    """
    @step("Client message option (\d+) MUST (NOT )?contain (\S+) (\S+).")

    Step checks the value of field within a specific option. It is compared
    with the value given in step. It might be used as following:
    Client message option 25 MUST NOT contain T1 2000.
    """

    found = False
    for entry in world.cliopts:
        if entry[0] == int(opt_code):
            if hasattr(entry[1], value_name):
                if getattr(entry[1], value_name) == int(value):
                    found = True
    if expect:
        assert found is True, "%s has different value than " \
                              "expected." % str(value_name)
    else:
        assert found is False, "%s has %s value, but it " \
                               "shouldn't." % (str(value_name), str(value))


def client_subopt_check_value(step, subopt_code, opt_code, expect, value_name, value):
    """
    This is the same as client_opt_check_value, but for suboption;
    """

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
    """
    @step("Client message MUST (NOT )?contain (\d+) options with opt-code (\d+).")

    Step checks whether client had included a expected number of particular
    option in message.
    """

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
    """
    @step("Client message MUST (NOT )?contain (\d+) sub-options with opt-code (\d+) within option (\d+).")

    Step checks whether client had included a expected number of particular
    sub-option within option in message.
    """
    localCounter = 0
    for entry in world.subopts:
        if entry[0] == int(opt_code) and entry[1] == int(subopt_code):
            localCounter += 1

    if contain:
        assert localCounter is int(count), "count of suboption %d does not match with" \
                                           " given value. got: %d, expected: %d." \
                                           % (int(subopt_code), localCounter, int(count))
    else:
        assert int(count) is not localCounter, "count of suboption %d does match with" \
                                               " given value," \
                                               " but it should not." % (int(subopt_code))


def client_check_field_presence(step, contain, field, optcode):
    """
    @step("Client message MUST (NOT )?contain (\S+) field in option (\d+).")

    Step checks if in specified option, specific field is present - like
    T1 field in option 25 (IA_PD).
    """

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
    """
    Function makes lease structure from scapy options.
    Format is the same as lease from ParseISCString.
    """

    result = {}
    result['lease6'] = {}
    pdList = [iapd for iapd in world.srvopts if iapd.optcode == 25]
    for pd in pdList:
        pdDict = {}
        pdDict['renew'] ="\"" + str(pd.T1) + "\""
        pdDict['rebind'] = "\"" + str(pd.T2) + "\""
        prefixList = [prefix for prefix in pd.iapdopt if prefix.optcode == 26]
        if len(prefixList) == 0:
            hexIaid = pd.iaid
        for prefix in prefixList:
            prefixDict = {}
            prefixDict['preferred-life'] = "\"" + str(prefix.preflft) + "\""
            prefixDict['max-life'] = "\"" + str(prefix.validlft) + "\""
            pdDict['iaprefix ' + "\"" + str(prefix.prefix) + '/' +
                   str(prefix.plen) + "\""] = dict(prefixDict)
            # dhclient stores iaid in hex value; if that's software that is 
            # currently tested, convert iaid to hexadecimal and add colons
            if "isc_dhcp6_client" in SOFTWARE_UNDER_TEST:
                hexIaid = hex(pd.iaid)[2:]
                hexIaid = ':'.join(a+b for a,b in zip(hexIaid[::2], hexIaid[1::2]))
            else:
                hexIaid = pd.iaid

        result['lease6']['ia-pd ' + "\"" + str(hexIaid) + "\""] = dict(pdDict)
    
    world.clntCfg['scapy_lease'] = result

