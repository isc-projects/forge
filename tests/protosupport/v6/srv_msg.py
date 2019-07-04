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

# Author: Wlodzimierz Wencel

#
# This file contains a number of common steps that are general and may be used
# By a lot of feature files.
#
import random
import sys
import logging
from cookielib import debug

from scapy.sendrecv import sr
from scapy.layers import dhcp6
from scapy.layers.inet6 import IPv6, UDP
from scapy.config import conf
from scapy.volatile import RandMAC
import scapy

from forge_cfg import world
from terrain import client_id, ia_id, ia_pd

log = logging.getLogger('forge')


# option codes for options and sub-options for dhcp v6
OPTIONS = {"client-id": 1,
           "server-id": 2,
           "IA_NA": 3,
           "IN_TA": 4,
           "IA_address": 5,
           "preference": 7,
           "relay-msg": 9,
           "unicast": 12,
           "status-code": 13,
           "rapid_commit": 14,
           "vendor-class": 16,
           "vendor-specific-info": 17,
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
           "information-refresh-time": 32,
           "bcmcs-server-dns": 33,
           "remote-id": 37,
           "subscriber-id": 38,
           "fqdn": 39,
           "client-arch-type": 61,
           "erp-local-domain-name": 65,
           "client-link-layer-addr": 79}

## ======================================================================
## ================ PREPARE MESSAGE OPTIONS BLOCK START =================


def client_requests_option(opt_type):
    """
    Add RequestOption to message.
    """
    if not hasattr(world, 'oro'):
        # There was no ORO at all, create new one
        world.oro = dhcp6.DHCP6OptOptReq()
        # Scapy creates ORO with 23, 24 options request. Let's get rid of them
        world.oro.reqopts = []  # don't request anything by default

    world.oro.reqopts.append(int(opt_type))


def client_send_msg(msgname, iface, addr):
    """
    Sends specified message with defined options.
    Parameters:
    msg ('<msg> message'): name of the message.
    """
    # iface and addr not used for v6 for now.

    # Remove previous message waiting to be sent, just in case this is a
    # REQUEST after we received ADVERTISE. We don't want to send SOLICIT
    # the second time.
    world.climsg = []

    if msgname == "SOLICIT":
        msg = build_msg(dhcp6.DHCP6_Solicit())

    elif msgname == "REQUEST":
        msg = build_msg(dhcp6.DHCP6_Request())

    elif msgname == "CONFIRM":
        msg = build_msg(dhcp6.DHCP6_Confirm())

    elif msgname == "RENEW":
        msg = build_msg(dhcp6.DHCP6_Renew())

    elif msgname == "REBIND":
        msg = build_msg(dhcp6.DHCP6_Rebind())

    elif msgname == "DECLINE":
        msg = build_msg(dhcp6.DHCP6_Decline())

    elif msgname == "RELEASE":
        msg = build_msg(dhcp6.DHCP6_Release())

    elif msgname == "INFOREQUEST":
        msg = build_msg(dhcp6.DHCP6_InfoRequest())

    else:
        assert False, "Invalid message type: %s" % msgname

    assert msg, "Message preparation failed"

    if msg:
        world.climsg.append(msg)

    log.debug("Message %s will be sent over %s interface." % (msgname, world.cfg["iface"]))


def client_sets_value(value_name, new_value):
    if value_name in world.cfg["values"]:
        if isinstance(world.cfg["values"][value_name], str):
            world.cfg["values"][value_name] = str(new_value)
        elif isinstance(world.cfg["values"][value_name], int):
            world.cfg["values"][value_name] = int(new_value)
        else:
            world.cfg["values"][value_name] = new_value
    else:
        assert value_name in world.cfg["values"], "Unknown value name : %s" % value_name


def unicast_addres(addr_type):
    """
    Turn off sending on All_DHCP_Relay_Agents_and_Servers, and use UNICAST address.
    """
    if addr_type:
        world.cfg["address_v6"] = world.f_cfg.srv_ipv6_addr_global
    else:
        world.cfg["address_v6"] = world.f_cfg.srv_ipv6_addr_link_local


def client_does_include(sender_type, opt_type, value):
    """
    Include options to message. This function refers to @step in lettuce
    """

    assert sender_type in ["Client", "RelayAgent", "Relay-Supplied-Option"], "Two sender type accepted: Client or" \
                                                                             " RelayAgent, your choice is: " \
                                                                             + sender_type
    world.sender_type = sender_type
    # value variable not used in v6
    # If you want to use options of received message to include it,
    # please use 'Client copies (\S+) option from received message.' step.
    if world.cfg["values"]["DUID"] is not None:
        world.cfg["values"]["cli_duid"] = convert_DUID(world.cfg["values"]["DUID"])

    if opt_type == "client-id":
        add_client_option(dhcp6.DHCP6OptClientId(duid=world.cfg["values"]["cli_duid"]))

    if opt_type == "wrong-client-id":
        #used for backwards compatibility
        add_client_option(dhcp6.DHCP6OptClientId(duid=dhcp6.DUID_LLT(timeval=int(time.time()), lladdr=RandMAC())))

    elif opt_type == "empty-client-id":
        add_client_option(dhcp6.DHCP6OptClientId())

    elif opt_type == "wrong-server-id":
        #used for backwards compatibility
        add_client_option(dhcp6.DHCP6OptServerId(duid=convert_DUID(world.cfg["values"]["server_id"])))

    elif opt_type == "server-id":
        add_client_option(dhcp6.DHCP6OptServerId(duid=convert_DUID(world.cfg["values"]["server_id"])))

    elif opt_type == "empty-server-id":
        add_client_option(dhcp6.DHCP6OptServerId())

    elif opt_type == "preference":
        add_client_option(dhcp6.DHCP6OptPref(prefval=world.cfg["values"]["prefval"]))

    elif opt_type == "rapid-commit":
        add_client_option(dhcp6.DHCP6OptRapidCommit())

    elif opt_type == "time":
        add_client_option(dhcp6.DHCP6OptElapsedTime(elapsedtime=world.cfg["values"]["elapsedtime"]))

    elif opt_type == "relay-msg":
        add_client_option(dhcp6.DHCP6OptRelayMsg(message=dhcp6.DHCP6_Solicit()))

    elif opt_type == "server-unicast":
        add_client_option(dhcp6.DHCP6OptServerUnicast(srvaddr=world.cfg["values"]["srvaddr"]))

    elif opt_type == "status-code":
        add_client_option(dhcp6.DHCP6OptStatusCode(statuscode=world.cfg["values"]["statuscode"],
                                                   statusmsg=world.cfg["values"]["statusmsg"]))

    elif opt_type == "interface-id":
        add_client_option(dhcp6.DHCP6OptIfaceId(ifaceid=world.cfg["values"]["ifaceid"]))

    elif opt_type == "reconfigure":
        add_client_option(dhcp6.DHCP6OptReconfMsg(msgtype=world.cfg["values"]["reconfigure_msg_type"]))

    elif opt_type == "reconfigure-accept":
        add_client_option(dhcp6.DHCP6OptReconfAccept())

    elif opt_type == "option-request":
        # later we can make it adjustable
        add_client_option(dhcp6.DHCP6OptOptReq(reqopts=world.cfg["values"]["reqopts"]))

    elif opt_type == "IA-PD":
        if len(world.iapd) > 0:
            add_client_option(dhcp6.DHCP6OptIA_PD(iaid=int(world.cfg["values"]["ia_pd"]),
                                                  T1=world.cfg["values"]["T1"],
                                                  T2=world.cfg["values"]["T2"],
                                                  iapdopt=world.iapd))
            world.iapd = []
        else:
            add_client_option(dhcp6.DHCP6OptIA_PD(iaid=int(world.cfg["values"]["ia_pd"]),
                                                  T1=world.cfg["values"]["T1"],
                                                  T2=world.cfg["values"]["T2"]))

    elif opt_type == "IA-NA":
        if len(world.iaad) > 0:
            add_client_option(dhcp6.DHCP6OptIA_NA(iaid=int(world.cfg["values"]["ia_id"]),
                                                  T1=world.cfg["values"]["T1"],
                                                  T2=world.cfg["values"]["T2"],
                                                  ianaopts=world.iaad))
            world.iaad = []
        else:
            add_client_option(dhcp6.DHCP6OptIA_NA(iaid=int(world.cfg["values"]["ia_id"]),
                                                  T1=world.cfg["values"]["T1"],
                                                  T2=world.cfg["values"]["T2"]))

    elif opt_type == "IA_Prefix":
        world.iapd.append(dhcp6.DHCP6OptIAPrefix(preflft=world.cfg["values"]["preflft"],
                                                 validlft=world.cfg["values"]["validlft"],
                                                 plen=world.cfg["values"]["plen"],
                                                 prefix=world.cfg["values"]["prefix"]))

    elif opt_type == "IA_Address":
        world.iaad.append(dhcp6.DHCP6OptIAAddress(addr=world.cfg["values"]["IA_Address"],
                                                  preflft=world.cfg["values"]["preflft"],
                                                  validlft=world.cfg["values"]["validlft"]))

    elif opt_type == "user-class":
        if world.cfg["values"]["user_class_data"] == "":
            add_client_option(dhcp6.DHCP6OptUserClass())
        else:
            add_client_option(dhcp6.DHCP6OptUserClass(userclassdata=dhcp6.USER_CLASS_DATA(data=str(world.cfg["values"]["user_class_data"]))))

    elif opt_type == "vendor-class":
        if world.cfg["values"]["vendor_class_data"] == "":
            add_client_option(dhcp6.DHCP6OptVendorClass(enterprisenum=world.cfg["values"]["enterprisenum"]))
        else:
            add_client_option(dhcp6.DHCP6OptVendorClass(enterprisenum=world.cfg["values"]["enterprisenum"],
                                                        vcdata=dhcp6.VENDOR_CLASS_DATA(
                                                            data=world.cfg["values"]["vendor_class_data"])))

    elif opt_type == "vendor-specific-info":
        # convert data for world.vendor with code == 1 (option request)
        # that is the only one option that needs converting.
        vendor_option_request_convert()

        # build VENDOR_CPECIDIC_OPTIONs depending on world.vendor:
        vso_tmp = []
        for each in world.vendor:
            vso_tmp.append(dhcp6.VENDOR_SPECIFIC_OPTION(optcode=each[0],
                                                        optdata=each[1]))
        add_client_option(dhcp6.DHCP6OptVendorSpecificInfo(enterprisenum=world.cfg["values"]["enterprisenum"],
                                                           vso=vso_tmp))
        # clear vendor list
        world.vendor = []

    elif opt_type == "fqdn":
        if world.cfg["values"]["FQDN_flags"] is None:
            assert False, "Please define FQDN flags first."

        converted_fqdn = world.cfg["values"]["FQDN_domain_name"]
        add_client_option(dhcp6.DHCP6OptClientFQDN(flags=str(world.cfg["values"]["FQDN_flags"]),
                                                   fqdn=converted_fqdn))

    elif opt_type == "client-link-layer-addr":
        add_client_option(dhcp6.DHCP6OptClientLinkLayerAddr(lltype=world.cfg["values"]["address_type"],
                                                            clladdr=world.cfg["values"]["link_local_mac_addr"]))

    elif opt_type == "remote-id":
        add_client_option(dhcp6.DHCP6OptRemoteID(enterprisenum=world.cfg["values"]["enterprisenum"],
                                                 remoteid=world.cfg["values"]["remote_id"].replace(':', '').decode('hex')))

    elif opt_type == "subscriber-id":
        add_client_option(dhcp6.DHCP6OptSubscriberID(subscriberid=world.cfg["values"]["subscriber_id"].
                                                     replace(':', '').decode('hex')))

    elif opt_type == "interface-id":
        add_client_option(dhcp6.DHCP6OptIfaceId(ifaceid=world.cfg["values"]["ifaceid"]))

    elif opt_type == "nii":
        add_client_option(dhcp6.DHCP6OptClientNetworkInterId(iitype=world.cfg["values"]["iitype"],
                                                             iimajor=world.cfg["values"]["iimajor"],
                                                             iiminor=world.cfg["values"]["iiminor"]))

    elif opt_type == "client-arch-type":
        add_client_option(dhcp6.DHCP6OptClientArchType(archtypes=world.cfg["values"]["archtypes"]))

    elif opt_type == "erp-local-domain-name":
        add_client_option(dhcp6.DHCP6OptERPDomain(erpdomain=[world.cfg["values"]["erpdomain"]]))

    elif opt_type == "rsoo":
        add_client_option(dhcp6.DHCP6OptRelaySuppliedOpt(relaysupplied=world.rsoo))

    else:
        assert "unsupported option: " + opt_type


def change_message_field(message_filed, value, value_type):
    convert_type = {"int": int,
                    "string": str,
                    "str": str,
                    "unicode": unicode}

    convert = convert_type[value_type]
    world.message_fields.append([str(message_filed), convert(value)])


def apply_message_fields_changes():
    for field_details in world.message_fields:

        try:
            setattr(world.climsg[0], field_details[0], field_details[1])
        except:
            assert False, "Message does not contain field: %s " % str(field_details[0])


def add_vendor_suboption(code, data):
    # if code == 1 we need check if we added code=1 before
    # if we do, we need append only data not whole suboption
    if code == 1 and len(world.vendor) > 0:
        for each in world.vendor:
            if each[0] == 1:
                each[1].append(int(data))

    # if world.vendor is empty and code == 1 add
    # code =1 and data as int (required to further conversion)
    elif code == 1:
        world.vendor.append([code, [int(data)]])

    # every other option just add
    else:
        world.vendor.append([code, str(data)])


def generate_new(opt):
    """
    Generate new client id with random MAC address.
    """
    if opt == 'client':
        client_id(RandMAC())
        ia_id()
    elif opt == 'Client_ID':
        client_id(RandMAC())
    elif opt == 'IA':
        ia_id()
    elif opt == 'IA_PD':
        ia_pd()

    else:
        assert False,  opt + " generation unsupported"

## ================ PREPARE MESSAGE OPTIONS BLOCK END ===================

## ============================================================
## ================ BUILD MESSAGE BLOCK START =================


def add_client_option(option):
    if world.sender_type == "Client":
        world.cliopts.append(option)
    elif world.sender_type == "RelayAgent":
        world.relayopts.append(option)
    elif world.sender_type == "Relay-Supplied-Option":
        world.rsoo.append(option)
    else:
        assert False, "Something went wrong with sender_type in add_client_option- you should never seen this error"


def add_option_to_msg(msg, option):
    # this is request_option option
    msg /= option
    return msg


def client_add_saved_option(erase, count="all"):
    """
    Add saved option to message, and erase.
    """
    if count == "all":
        for each_key in world.savedmsg.keys():
            for every_opt in world.savedmsg[each_key]:
                world.cliopts.append(every_opt)
            if erase:
                world.savedmsg = {}
    else:
        if not world.savedmsg.has_key(count):
            assert False, "There is no set no. {count} in saved opotions".format(**locals())

        for each in world.savedmsg[count]:
            world.cliopts.append(each)
        if erase:
            world.savedmsg[count] = []


def vendor_option_request_convert():
    data_tmp = ''
    for each in world.vendor:
        if each[0] == 1:
            for number in each[1]:
                data_tmp += '\00' + str(chr(number))
            each[1] = data_tmp
        else:
            each[1] = each[1].replace(':', '').decode('hex')


def convert_DUID_hwaddr(duid, threshold):
    tmp = duid[threshold:]
    hwaddr = ':'.join(tmp[i:i+2] for i in range(0, len(tmp), 2))
    return hwaddr


def convert_DUID(duid):
    """
    We can use two types of DUID:
        DUID_LLT link layer address + time (e.g. 00:01:00:01:52:7b:a8:f0:08:00:27:58:f1:e8 )
        DUID_LL link layer address (e.g. 00:03:00:01:ff:ff:ff:ff:ff:01 )

        third DUID based on vendor is not supported (also not planned to be ever supported)

        In case of using DUID_LLT:
            00:01:00:01:52:7b:a8:f0:08:00:27:58:f1:e8
            00:01 - duid type, it need to be 0001 for DUID_LLT
                  00:01 - hardware type, make it always 0001
                        52:7b:a8:f0 - converted time value
                                    08:00:27:58:f1:e8 - link layer address

        In case of using DUID_LL:
            00:03:00:01:ff:ff:ff:ff:ff:01
            00:03 - duid type, it need to be 0003 for DUID_LL
                  00:01 - hardware type, make it always 0001
                        ff:ff:ff:ff:ff:01 - link layer address

        You can use two forms for each DUID type, with ":" and without.
        For example
                00:01:00:01:52:7b:a8:f0:08:00:27:58:f1:e8
            it's same as:
                00010001527ba8f008002758f1e8
            and
                00:03:00:01:ff:ff:ff:ff:ff:01
            it's same as:
                00030001ffffffffff01

        Other configurations will cause to fail test.
    """
    duid = duid.replace(":", "")

    if duid[:8] == "00030001":
        return dhcp6.DUID_LL(lladdr=convert_DUID_hwaddr(duid, 8))
    elif duid[:8] == "00010001":
        return dhcp6.DUID_LLT(timeval=int(duid[8:16], 16), lladdr=convert_DUID_hwaddr(duid, 16))
    else:
        assert False, "DUID value is not valid! DUID: " + duid


def build_msg(msg):

    msg = IPv6(dst=world.cfg["address_v6"],
               src=world.cfg["cli_link_local"])/UDP(sport=world.cfg["source_port"],
                                                    dport=world.cfg["destination_port"])/msg

    # get back to multicast address.
    world.cfg["address_v6"] = "ff02::1:2"

    # transaction id
    if world.cfg["values"]["tr_id"] is None:
        msg.trid = random.randint(0, 256*256*256)
    else:
        msg.trid = int(world.cfg["values"]["tr_id"])
    world.cfg["values"]["tr_id"] = msg.trid

    # add option request if any
    try:
        if len(world.oro.reqopts) > 0:
            msg = add_option_to_msg(msg, world.oro)
    except:
        pass

    # add all rest options to message.
    world.cliopts = world.cliopts[::-1]
    while world.cliopts:
        msg /= world.cliopts.pop()
    # for each_option in world.cliopts:
    #     msg /= each_option
    #
    # world.cliopts = []
    return msg


def create_relay_forward(level=1):
    """
    Encapsulate message in relay-forward message.
    """
    assert level > 0
    # set flag for adding client option client-id which is added by default
    world.cfg["relay"] = True

    # we pretend to be relay-server so we need to listen on 547 port
    world.cfg["source_port"] = 547

    # get only DHCPv6 part of the message
    msg = world.climsg.pop().getlayer(2)

    # message encapsulation
    for lvl in range(level):
        # all three values: linkaddr, peeraddr and hopcount must be filled
        relay_msg = dhcp6.DHCP6_RelayForward(hopcount=lvl + 1,
                                              linkaddr=world.cfg["values"]["linkaddr"],
                                              peeraddr=world.cfg["values"]["peeraddr"])
        for each_option in world.relayopts:
            relay_msg /= each_option
        relay_msg /= dhcp6.DHCP6OptRelayMsg(message=msg)

        msg = relay_msg

    # build full message
    full_msg = IPv6(dst=world.cfg["address_v6"],
                     src=world.cfg["cli_link_local"])
    full_msg /= UDP(sport=world.cfg["source_port"],
                     dport=world.cfg["destination_port"])
    full_msg /= msg

    # in case if unicast used, get back to multicast address.
    world.cfg["address_v6"] = "ff02::1:2"

    world.climsg.append(full_msg)
    world.relayopts = []
    world.cfg["source_port"] = 546  # we should be able to change relay ports from test itself
    world.cfg["relay"] = False

## ================ BUILD MESSAGE BLOCK END ===================


## ===================================================================
## ================ SEND/RECEIVE MESSAGE BLOCK START =================


def send_wait_for_message(condition_type, presence, exp_message):
    """
    Block until the given message is (not) received.
    Parameter:
    new: (' new', optional): Only check the output printed since last time
                             this step was used for this process.
    process_name ('<name> stderr'): Name of the process to check the output of.
    message ('message <message>'): Output (part) to wait for.
    """
    world.cliopts = []  # clear options, always build new message, also possible make it in client_send_msg
    may_flag = False
    #debug.recv=[]
    if str(condition_type) in "MUST":
        pass
    elif str(condition_type) in "MAY":
        may_flag = True
    # we needs to get it operational
    # problem: break test with success. (for now we can break test only with fail)
    else:
        assert False, "Invalid expected behavior: %s." % str(condition_type)

    # Uncomment this to get debug.recv filled with all received messages
    conf.debug_match = True

    # checkIPsrc must be False so scapy can correctly match response to request
    conf.checkIPsrc = False
    apply_message_fields_changes()

    ans, unans = sr(world.climsg,
                    iface=world.cfg["iface"],
                    timeout=world.cfg["wait_interval"],
                    nofilter=1,
                    verbose=world.scapy_verbose)

    if world.f_cfg.show_packets_from in ['both', 'client']:
            world.climsg[0].show()

    expected_type_found = False
    received_names = ""
    world.srvmsg = []
    for x in ans:
        a, b = x
        world.srvmsg.append(b)

        if world.f_cfg.show_packets_from in ['both', 'server']:
            b.show()

        if not world.loops["active"]:
            log.info("Received packet type=%s" % get_msg_type(b))

        received_names = get_msg_type(b) + " " + received_names
        if get_msg_type(b) == exp_message:
            expected_type_found = True

    for x in unans:
        log.error(("Unanswered packet type=%s" % dhcp6.dhcp6_cls_by_type[x.msgtype]))

    if not world.loops["active"]:
        log.debug("Received traffic (answered/unanswered): %d/%d packet(s)." % (len(ans), len(unans)))

    if may_flag:
        if len(world.srvmsg) != 0:
            assert True, "Response received."
        if len(world.srvmsg) == 0:
            assert True, "Response not received."  # stop the test... ??
    elif presence:
        assert len(world.srvmsg) != 0, "No response received."
        assert expected_type_found, "Expected message " + exp_message + " not received (got " + received_names + ")"
    elif not presence:
        assert len(world.srvmsg) == 0, "Response received, not expected"

    return world.srvmsg


def get_last_response():
    assert len(world.srvmsg), "No response received."
    msg = world.srvmsg[len(world.srvmsg) - 1].copy()
    return msg

## ================ SEND/RECEIVE MESSAGE BLOCK END ===================


## =======================================================================
## ================ PARSING RECEIVED MESSAGE BLOCK START =================


def get_msg_type(msg):
    msg_types = {"ADVERTISE": dhcp6.DHCP6_Advertise,
                 "REQUEST": dhcp6.DHCP6_Request,
                 "REPLY": dhcp6.DHCP6_Reply,
                 "RELAYREPLY": dhcp6.DHCP6_RelayReply}

    # 0th is IPv6, 1st is UDP, 2nd should be DHCP6
    for msg_name in msg_types.keys():
        if type(msg.getlayer(2)) == msg_types[msg_name]:
            return msg_name

    return "UNKNOWN-TYPE"


def client_save_option(option_name, count=0):
    assert option_name in OPTIONS, "Unsupported option name " + option_name
    opt_code = OPTIONS.get(option_name)
    opt = get_option(get_last_response(), opt_code)

    assert opt, "Received message does not contain option " + option_name
    opt.payload = scapy.packet.NoPayload()

    if count not in world.savedmsg:
        world.savedmsg[count] = [opt]
    else:
        world.savedmsg[count].append(opt)


def client_copy_option(option_name):
    """
    Copy option from received message
    """
    assert world.srvmsg

    assert option_name in OPTIONS, "Unsupported option name " + option_name
    opt_code = OPTIONS.get(option_name)

    # find and copy option
    opt = get_option(world.srvmsg[0], opt_code)

    assert opt, "Received message does not contain option " + option_name

    # payload need to be 'None' otherwise we copy all options from one we are
    # looking for till the end of the message
    # it would be nice to remove 'status code' sub-option
    # before sending it back to server
    opt.payload = scapy.packet.NoPayload()
    add_client_option(opt)


def get_option(msg, opt_code):
    # We need to iterate over all options and see
    # if there's one we're looking for

    # message needs to be copied, otherwise we changing original message
    # what makes sometimes multiple copy impossible.
    tmp_msg = msg.copy()

    # clear all opts/subopts
    world.opts = []
    world.subopts = []
    tmp = None
    # TODO: get rid of x and tmp_msg
    if len(world.rlymsg) == 0:  # relay message is already cropped to exact layer
        x = tmp_msg.getlayer(3)  # 0th is IPv6, 1st is UDP, 2nd is DHCP6, 3rd is the first option
    else:
        x = tmp_msg

    # check all message, for expected option and all suboptions in IA_NA/IA_PD
    check_suboptions = ["ianaopts",
                        "iapdopt",
                        "vso",
                        "userclassdata",
                        "vcdata"
                        ]
    while x:
        if x.optcode == int(opt_code):
            tmp = x.copy()
            world.opts.append(x)

        for each in check_suboptions:
            if x.fields.get(each):
                tmp2 = x.copy()
                del tmp2.payload
                world.subopts.append([x.optcode, tmp2])

        # add Status Code to suboptions even if it is option in main message
        # TODO check if it is still needed!
        if x.optcode == 13:
            world.subopts.append([0, x])

        x = x.payload
    return tmp


def unknown_option_to_str(data_type, opt):
    if data_type == "uint8":
        assert len(opt.data) == 1, "Received option " + opt.optcode + " contains " + len(opt.data) + \
                                   " bytes, but expected exactly 1"
        return str(ord(opt.data[0:1]))
    else:
        assert False, "Parsing of option format " + str(data_type) + " not implemented."


def _get_opt_descr(opt_code):
    try:
        opt = dhcp6.dhcp6opts_by_code[int(opt_code)]
    except KeyError:
        opt = 'unknown'
    opt_descr = "%s[%s]" % (opt, opt_code)
    return opt_descr


def response_check_include_option(must_include, opt_code):
    """
    Checking presence of expected option.
    """
    assert len(world.srvmsg) != 0, "No response received."

    # if opt_code is actually a opt name then convert it to code
    if isinstance(opt_code, str) and not opt_code.isdigit():
        opt_code = OPTIONS[opt_code]

    opt = get_option(world.srvmsg[0], opt_code)

    opt_descr = _get_opt_descr(opt_code)

    if must_include:
        assert opt, "Expected option {opt_descr} not present in the message.".format(**locals())
    else:
        assert opt is None, "Unexpected option {opt_descr} found in the message.".format(**locals())

# Returns text representation of the option, interpreted as specified by data_type


def get_subopt_from_option(exp_opt_code, exp_subopt_code):
    result = []
    received = ''
    list_fields = ["ianaopts",
                   "iapdopt",
                   "vso",
                   "userclassdata",
                   "vcdata"]
    # firstly we go through all options that can include sub-options
    for opt_code, opt_data in world.subopts:
        # we need to be sure that option 13 is in 25 or 3
        # otherwise sub-option 13 from option 3 could be taken
        # as sub-option from option 25. And that's important!
        if opt_code != exp_opt_code:
            continue

        # now we need to find specific sub-option list:
        for list_field in list_fields:
            # if we found list - we need to check every option on that list
            subopts = opt_data.fields.get(list_field)
            if not subopts:
                continue

            for option_in_the_list in subopts:
                # if on selected list there is option we are looking for, return it!
                if option_in_the_list.optcode == exp_subopt_code:
                    result.append(option_in_the_list)
                    received = str(option_in_the_list.optcode)
    return result, received

def get_suboption(opt_code, subopt_code):
    # if opt_code is actually a opt name then convert it to code
    if isinstance(opt_code, str) and not opt_code.isdigit():
        opt_code = OPTIONS[opt_code]
    if isinstance(subopt_code, str) and not subopt_code.isdigit():
        subopt_code = OPTIONS[subopt_code]

    opt, _ = get_subopt_from_option(opt_code, subopt_code)
    return opt


def extract_duid(option):
    if option.type == 1:
        # DUID_LLT
        return "0001000" + str(option.hwtype) + str(hex(option.timeval))[2:] + str(option.lladdr).replace(":", "")
    elif option.type == 2:
        # DUID_EN
        return "0002" + str(option.enterprisenum) + str(option.id.decode())
    elif option.type == 3:
        # DUID_LL
        return "0003000" + str(option.hwtype) + str(option.lladdr).replace(":", "")


def response_check_include_suboption(opt_code, expect, expected_value):
    # if opt_code is actually a opt name then convert it to code
    if isinstance(opt_code, str) and not opt_code.isdigit():
        opt_code = OPTIONS[opt_code]
    if isinstance(expected_value, str) and not expected_value.isdigit():
        expected_value = OPTIONS[expected_value]

    x, receive_tmp = get_subopt_from_option(int(opt_code), int(expected_value))
    opt_descr = _get_opt_descr(opt_code)
    subopt_descr = _get_opt_descr(expected_value)
    if expect is None:
        assert len(x) > 0, "Expected sub-option {subopt_descr} not present in the option {opt_descr}".format(**locals())
    else:
        assert len(x) == 0, "NOT expected sub-option {subopt_descr} is present in the option {opt_descr}".format(**locals())
    return x, receive_tmp


values_equivalent = {7: "prefval", 13: "statuscode", 21: "sipdomains", 22: "sipservers", 23: "dnsservers",
                     24: "dnsdomains", 27: "nisservers", 28: "nispservers", 29: "nisdomain", 30: "nispdomain",
                     31: "sntpservers", 32: "reftime"}


def response_check_suboption_content(subopt_code, opt_code, expect, data_type, expected_value):
    # if opt_code is actually a opt name then convert it to code
    if isinstance(opt_code, str) and not opt_code.isdigit():
        opt_code = OPTIONS[opt_code]
    if isinstance(subopt_code, str) and not subopt_code.isdigit():
        subopt_code = OPTIONS[subopt_code]

    #first check if subotion exists and get suboption
    opt_code = int(opt_code)
    if opt_code == 17:
        data_type = "optdata"
    data_type = str(data_type)
    expected_value = str(expected_value)
    received = []
    opts, receive_tmp = response_check_include_suboption(opt_code, None, subopt_code)
    assert int(subopt_code) == int(receive_tmp), "You should never see this error, if so, please report that bug a"
    # that is duplicated code but lets leave it for now
    for opt in opts:
        tmp_field = opt.fields.get(data_type)
        if tmp_field is None:
            if opt_code not in [17]:
                data_type = values_equivalent.get(opt_code)
            tmp_field = opt.fields.get(data_type)
        if type(tmp_field) is list:
            received.append(",".join(tmp_field))
        else:
            received.append(str(tmp_field))

    opt_descr = _get_opt_descr(opt_code)

    if expect is None or expect is True:
        assert expected_value in received, ("Invalid {opt_descr} option, received {data_type}: ".format(**locals()) +
                                            ",".join(received) + ", but expected " + str(expected_value))
    else:
        assert expected_value not in received, ("Received value of {data_type}: ".format(**locals()) + ",".join(received) +
                                                " should not be equal to value from client - " + str(expected_value))


def convert_relayed_message(relayed_option):
    world.rlymsg.append(relayed_option)
    world.srvmsg.pop()
    world.srvmsg.append(relayed_option.message)


def response_check_option_content(opt_code, expect, data_type, expected_value):
    # if opt_code is actually a opt name then convert it to code
    if isinstance(opt_code, str) and not opt_code.isdigit():
        opt_code = OPTIONS[opt_code]
    opt_code = int(opt_code)
    data_type = str(data_type)
    expected_value = str(expected_value)
    initial_data_type = data_type
    # without any msg received, fail test
    assert len(world.srvmsg) != 0, "No response received."
    # get that one option, also fill world.opts (for multiple options same type, e.g. IA_NA)
    # and world.subopts for suboptions for e.g. IA Address or StatusCodes
    x = get_option(world.srvmsg[0], opt_code)
    received = []

    opt_descr = _get_opt_descr(opt_code)

    assert x, "Expected option {opt_descr} not present in the message.".format(**locals())
    # test all collected options,:
    # couple tweaks to make checking smoother

    if opt_code == 9:
        convert_relayed_message(x)
    else:
        if data_type == "iapd":
            data_type = "iaid"
        if data_type == "duid":
            expected_value = expected_value.replace(":", "")
            received.append(extract_duid(x.duid))
        else:
            for each in x:
                tmp_field = each.fields.get(data_type)
                if tmp_field is None:
                    data_type = values_equivalent.get(opt_code)
                    tmp_field = each.fields.get(data_type)
                if type(tmp_field) is list:
                    received.append(",".join(tmp_field))
                else:
                    received.append(str(tmp_field))

        # test if expected option/suboption/value is in all collected options/suboptions/values
        if received[0] == 'None':
            assert False, "Within option " + opt_descr + " there is no " + initial_data_type\
                          + " value. Probably that is test error"

        if expect is None or expect is True:
            assert expected_value in received, "Invalid " + opt_descr + " option, received "\
                                               + data_type + ": " + ",".join(received) + ", but expected " \
                                               + str(expected_value)
        else:
            assert expected_value not in received, "Received value of " + data_type + ": " + ",".join(received) +\
                                                   " should not be equal to value from client - " + str(expected_value)


def save_value_from_option(value_name, option_name):

    assert world.srvmsg
    get_option(world.srvmsg[0], option_name)
    if len(world.opts) == 0:
        temp = world.subopts[0][1].payload
        world.savedvalue = getattr(temp, value_name)
        world.subopts = []
    else:
        world.savedvalue = getattr(world.opts[0], value_name)
        world.opts = []
        world.subopts = []


def compare_values(value_name, option_name):

    assert world.srvmsg
    get_option(world.srvmsg[0], option_name)
    if len(world.opts) == 0:
        subopt = world.subopts[0][1].payload
        to_cmp = getattr(subopt, value_name)
        assert world.savedvalue == to_cmp, \
            "Compared values %s and %s do not match" % (world.savedvalue, to_cmp)
        world.subopts = []
    else:
        to_cmp = getattr(world.opts[0], value_name)
        assert world.savedvalue == to_cmp, \
            "Compared values %s and %s do not match" % (world.savedvalue, to_cmp)
        world.opts = []
        world.subopts = []

## ================ PARSING RECEIVED MESSAGE BLOCK END ===================


## =======================================================================
## ==================== TESTING IN LOOPS BLOCK START =====================

def loops_config_sld():
    world.loops["save_leases_details"] = True


def values_for_loops(value_name, file_flag, values):
    value_name = str(value_name)
    if value_name == "client-id":
        world.loops[value_name] = []
        for each in str(values).split(" "):
            world.cfg["values"]["DUID"] = each
            world.loops[value_name].append(convert_DUID())


def loops(message_type_1, message_type_2, repeat):
    import importlib
    testsetup = importlib.import_module("misc")
    repeat = int(repeat)
    testsetup.set_world()
    testsetup.test_procedure()

    if repeat < 1000:
        x_range = 10
    elif 1000 <= repeat < 10000:
        x_range = 250
    else:
        x_range = 1000

    world.loops["active"] = True
    world.scapy_verbose = 0

    if message_type_1 == "SOLICIT" and message_type_2 == "ADVERTISE":
        # short two message exchange without saving leases.
        for x in range(repeat):
            generate_new("client")
            client_does_include("Client", "client-id", None)
            client_does_include("Client", "IA-NA", None)
            client_send_msg(message_type_1, None, None)
            send_wait_for_message("MAY", True, message_type_2)

    elif message_type_1 == "SOLICIT" and message_type_2 == "REPLY":
        # first save server-id option
        client_does_include("Client", "client-id", None)
        client_does_include("Client", "IA-NA", None)
        client_send_msg(message_type_1, None, None)
        send_wait_for_message("MAY", True, "ADVERTISE")
        client_save_option("server-id")

        # long 4 message exchange with saving leases.
        for x in range(repeat):
            if x % x_range == 0:
                log.info("Message exchange no. %d", x)
            generate_new("client")
            client_does_include("Client", "client-id", None)
            client_does_include("Client", "IA-NA", None)
            client_send_msg(message_type_1, None, None)
            send_wait_for_message("MAY", True, "ADVERTISE")

            try:
                client_add_saved_option(False)
                client_copy_option("IA_NA")
            except AssertionError:
                pass
            client_does_include("Client", "client-id", None)
            client_send_msg("REQUEST", None, None)
            send_wait_for_message("MAY", True, message_type_2)

    elif message_type_1 == "REQUEST" and message_type_2 == "REPLY":
        # first save server-id option
        client_send_msg("SOLICIT", None, None)
        send_wait_for_message("MAY", True, "ADVERTISE")
        client_save_option("server-id")

        # long 4 message exchange with saving leases.
        for x in range(repeat):
            if x % x_range == 0:
                log.info("Message exchane no. %d", x)
            generate_new("client")
            client_add_saved_option(False)
            client_send_msg("REQUEST", None, None)
            send_wait_for_message("MAY", True, message_type_2)
            response_check_option_content(13, 3, "NOT", "statuscode", "2")

    elif message_type_1 == "RELEASE" and message_type_2 == "REPLY":
        # first save server-id option
        client_send_msg("SOLICIT", None, None)
        send_wait_for_message("MAY", True, "ADVERTISE")
        client_save_option("server-id")

        # long 4 message exchange with saving leases.
        for x in range(repeat):
            if x % x_range == 0:
                log.info("Message exchane no. %d", x)

            client_add_saved_option(False)
            client_send_msg("REQUEST", None, None)
            send_wait_for_message("MAY", True, message_type_2)

            client_add_saved_option(False)
            client_copy_option("IA_NA")
            client_send_msg("RELEASE", None, None)
            send_wait_for_message("MAY", True, message_type_2)
            #dhcpmsg.generate_new("client")

    elif message_type_1 == "RENEW" and message_type_2 == "REPLY":
        # first save server-id option
        client_send_msg("SOLICIT", None, None)
        send_wait_for_message("MAY", True, "ADVERTISE")
        client_save_option("server-id")

        # long 4 message exchange with saving leases.
        for x in range(repeat):
            if x % x_range == 0:
                log.info("Message exchane no. %d", x)

            client_add_saved_option(False)
            client_send_msg("REQUEST", None, None)
            send_wait_for_message("MAY", True, message_type_2)

            client_add_saved_option(False)
            client_copy_option("IA_NA")
            client_send_msg("RENEW", None, None)
            send_wait_for_message("MAY", True, message_type_2)

    else:
        pass
    for x in range(len(world.savedmsg)):
        world.savedmsg[x] = []


def save_info():
    pass
