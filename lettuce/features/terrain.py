# Copyright (C) 2013-2017 Internet Systems Consortium.
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

from Crypto.Random.random import randint

#from init_all import ForgeConfiguration
from lettuce import world, before, after
from logging_facility import *
from scapy.config import conf
from scapy.layers.dhcp6 import DUID_LLT
from softwaresupport.bind10 import kill_bind10, start_bind10
from softwaresupport.multi_server_functions import fabric_download_file, make_tarfile, archive_file_name,\
    fabric_remove_file_command, fabric_run_command

import importlib
import os
import subprocess
import sys
import time


values_v6 = {"T1": 0,  # IA_NA IA_PD
             "T2": 0,  # IA_NA IA_PD
             "address": "::",
             "IA_Address": "::",
             "prefix": "::",
             "plen": 0,  # prefix; plz remember, to add prefix and prefix length!
             "preflft": 0,  # IA_Address IA_Prefix
             "validlft": 0,  # IA_Address IA_Prefix
             "enterprisenum": 0,  # vendor
             "vendor_class_data": "",
             "linkaddr": world.f_cfg.srv_ipv6_addr_global,  # relay
             "peeraddr": world.f_cfg.cli_link_local,  # relay
             "ifaceid": "15",  # relay
             "DUID": None,
             "FQDN_flags": "",
             "FQDN_domain_name": "",
             "address_type": 1,
             "link_local_mac_addr": world.f_cfg.cli_mac,
             "remote_id": "",
             "subscriber_id": "",
             "ia_id": 0,
             "ia_pd": 0,
             "prefval": 1,
             "elapsedtime": 1,
             "srvaddr": "::",
             "statuscode": 0,
             "statusmsg": "",
             "reconfigure_msg_type": 5,
             "reqopts": 7,
             "paaaddr": "::",
             "iitype": 0,
             "iimajor": 0,
             "iiminor": 0,
             "archtypes": 1,
             "user_class_data": ""}

srv_values_v6 = {"T1": 1000,
                 "T2": 2000,
                 "preferred-lifetime": 3000,
                 "valid-lifetime": 4000,
                 "prefix": "3000::",
                 "prefix-len": 64,
                 "timer": 10,
                 "dst_addr": ()}

clnt_set_wrong = {"trid": False,
                  "iaid": False,
                  "client_id": False,
                  "server_id": False}

values_dns = {"qname": "",
              "qtype": "",
              "qclass": ""}

# times values, plz do not change this.
# there is a test step to do this
server_times_v6 = {"renew-timer": 1000,
                   "rebind-timer": 2000,
                   "preferred-lifetime": 3000,
                   "valid-lifetime": 4000,
                   "rapid-commit": False  # yes that little odd, but let us keep it that way,
                   # rapid-commit it's only option that is used
                   # only in server configuration
                   }

server_times_v4 = {"renew-timer": 1000,
                   "rebind-timer": 2000,
                   "valid-lifetime": 4000}

values_v4 = {"ciaddr": "0.0.0.0",
             "yiaddr": "0.0.0.0",
             "siaddr": "0.0.0.0",
             "giaddr": "0.0.0.0",
             "broadcastBit": False,
             "hops": 0,
             "chaddr": None,
             "FQDN_flags": "",
             "FQDN_domain_name": ""}


# we should consider transfer most of functions to separate v4 and v6 files
# TODO: make separate files after branch merge

@world.absorb
def set_values():
    # this function is called after each message send.
    if world.f_cfg.proto == "v6":
        world.cfg["values"] = values_v6.copy()
        world.cfg["server_times"] = server_times_v6.copy()
        world.clntCfg["values"] = srv_values_v6.copy()
        world.clntCfg["set_wrong"] = clnt_set_wrong.copy()
        # reset values to 'default for scenario'
        world.cfg["values"]["cli_duid"] = world.cfg["cli_duid"]
        world.cfg["values"]["server_id"] = ""
        world.cfg["values"]["ia_id"] = world.cfg["ia_id"]
        world.cfg["values"]["ia_pd"] = world.cfg["ia_pd"]
    else:
        world.cfg["values"] = values_v4.copy()
        world.cfg["server_times"] = server_times_v4.copy()


def add_result_to_report(info):
    world.result.append(info)


def client_id(mac):
    world.cfg["cli_duid"] = DUID_LLT(timeval = int(time.time()), lladdr = mac)
    if "values" in world.cfg:
        world.cfg["values"]["cli_duid"] = world.cfg["cli_duid"]


def ia_id():
    world.cfg["ia_id"] = randint(1, 99999)
    if "values" in world.cfg:
        world.cfg["values"]["ia_id"] = world.cfg["ia_id"]


def ia_pd():
    world.cfg["ia_pd"] = randint(1, 99999)
    if "values" in world.cfg:
        world.cfg["values"]["ia_pd"] = world.cfg["ia_pd"]


def multiprotocol_initialize():
    pass


def v4_initialize():
    # Setup scapy for v4
    #conf.iface = IFACE
    conf.checkIPaddr = False  # DHCPv4 is sent from 0.0.0.0, so response matching may confuse scapy
    world.cfg["srv4_addr"] = world.f_cfg.srv4_addr
    world.cfg["rel4_addr"] = world.f_cfg.rel4_addr
    world.cfg["giaddr4"] = world.f_cfg.giaddr4
    world.cfg["space"] = "dhcp4"

    world.cfg["source_port"] = 68
    world.cfg["destination_port"] = 67
    world.cfg["source_IP"] = "0.0.0.0"
    world.cfg["destination_IP"] = "255.255.255.255"
    world.dhcp_enable = True


def v6_initialize():
    world.dhcp_enable = True
    # RFC 3315 define two addresess:
    # All_DHCP_Relay_Agents_and_Servers = ff02::1:2
    # All DHCP_Servers ff05::1:3.
    world.cfg["address_v6"] = "ff02::1:2"
    world.cfg["cli_link_local"] = world.f_cfg.cli_link_local
    world.cfg["unicast"] = False
    world.cfg["relay"] = False
    world.cfg["space"] = "dhcp6"

    world.cfg["source_port"] = 546
    world.cfg["destination_port"] = 547

    # Setup scapy for v6
    conf.iface6 = world.f_cfg.iface
    conf.use_pcap = True

    # those values should be initialized once each test
    # if you are willing to change it use 'client set value' steps
    client_id(world.f_cfg.cli_mac)
    ia_id()
    ia_pd()


def dns_initialize():
    world.cfg["dns_iface"] = world.f_cfg.dns_iface
    world.cfg["dns_addr"] = world.f_cfg.dns_addr
    world.cfg["dns_port"] = world.f_cfg.dns_port
    world.dns_enable = True


def define_software():
    # unfortunately we have to do this every single time
    world.cfg["dhcp_under_test"] = ""
    world.cfg["dns_under_test"] = ""
    for each_name in world.f_cfg.software_under_test:
        if each_name in world.f_cfg.dhcp_used:
            world.cfg["dhcp_under_test"] = each_name
            #world.cfg["dns_under_test"] = ""
        elif each_name in world.f_cfg.dns_used:
            world.cfg["dns_under_test"] = each_name
            #world.cfg["dhcp_under_test"] = ""


def declare_all():
    world.climsg = []  # Message(s) to be sent
    world.srvmsg = []  # Server's response(s)
    world.rlymsg = []  # Server's response(s) Relayed by Relay Agent
    world.tmpmsg = []  # container for temporary stored messages
    world.cliopts = []  # Option(s) to be included in the next message sent
    world.relayopts = []  # option(s) to be included in Relay Forward message.
    world.savedmsg = {0: []}  # Saved option(s)
    world.define = []  # temporary define variables

    world.proto = world.f_cfg.proto
    world.oro = None
    world.vendor = []
    world.iaad = []
    world.iapd = []
    world.opts = []
    world.subopts = []
    world.message_fields = []
    world.subnet_add = True
    world.cfg = {}
    world.configString = ""
    world.cfg['leases'] = "~/none_file"
    world.cfg["dhcp_log_file"] = "~/none_file"

    world.loops = {"active": False,
                   "save_leases_details": False}
    world.scapy_verbose = 99

    world.dns_enable = False
    world.dhcp_enable = False
    world.ddns_enable = False
    world.ctrl_enable = False
    world.fuzzing = False


@before.all
def test_start():
    """
    Server starting before testing
    """
    # clear tests results
    from shutil import rmtree

    if os.path.exists('tests_results'):
        rmtree('tests_results')
    os.makedirs('tests_results')
    if not os.path.exists('tests_results_archive') and world.f_cfg.auto_archive:
        os.makedirs('tests_results_archive')

    world.result = []

    # Initialize the common logger. The instance of this logger can
    # be instantiated by get_common_logger()
    logger_initialize(world.f_cfg.loglevel)

    for each in world.f_cfg.software_under_test:
        if "server" in each:
            if each in ['kea4_server_bind', 'kea6_server_bind']:
                get_common_logger().debug("Starting Bind:")
                kill_bind10()
                try:
                    # Make sure there is noo garbage instance of bind10 running.
                    start_bind10()
                except:
                    get_common_logger().error("Bind10 start failed\n\nSomething go wrong with connection\n\
                                                Please make sure it's configured properly\nIP destination \
                                                address: %s\nLocal Mac address: %s\nNetwork interface: %s"
                                              % (world.f_cfg.mgmt_address, world.f_cfg.cli_mac, world.f_cfg.iface))
                    sys.exit(-1)
                get_common_logger().debug("Bind10 successfully started")

        elif "client" in each:
            clnt = importlib.import_module("softwaresupport.%s.functions" % each)
            clnt.stop_clnt()

        else:
            stop = importlib.import_module("softwaresupport.%s.functions" % each)
            # True passed to stop_srv is to hide output in console.
            stop.stop_srv(True)
            #  that is pointless, we should use same name for stop_srv and stop_clnt functions,
            #  and erase that last elif.


@before.each_scenario
def initialize(scenario):

    # Declare all default values
    declare_all()
    define_software()

    world.cfg["iface"] = world.f_cfg.iface
    # world.cfg["server_type"] = SOFTWARE_UNDER_TEST for now I'll leave it here,
    # now we use world.cfg["dhcp_under_test"] and world.cfg["dns_under_test"] (in function define_software)
    # it is being filled with values in srv_control and clnt_control
    world.cfg["wait_interval"] = world.f_cfg.packet_wait_interval
    world.cfg["cfg_file"] = "server.cfg"
    world.cfg["cfg_file_2"] = "second_server.cfg"
    world.cfg["conf"] = ""  # Just empty config for now
    world.subcfg = [["", "", "", "", "", "", ""]]  # additional config structure
    world.shared_subcfg = []
    world.shared_subnets = []
    world.shared_subnets_tmp = []
    world.hooks = []
    world.classification = []
    world.reservation_backend = ""
    dir_name = str(scenario.name).replace(".", "_")
    world.cfg["dir_name"] = 'tests_results/' + dir_name
    world.cfg["subnet"] = ""
    world.cfg["server-id"] = ""
    world.cfg["csv-format"] = "true"
    world.cfg["tr_id"] = None
    world.name = scenario.name
    world.clntCounter = 0
    world.srvCounter = 0
    world.clntCfg = {}
    world.srvopts = []
    world.pref = None
    world.time = None
    # append single timestamp to list
    world.timestamps = []
    # response times list
    world.RTlist = []
    # time ranges that response time must fit in
    world.RTranges = []
    world.RTranges.append([0.9, 1.1])
    world.c = 0
    world.notSolicit = 0
    world.saved = []
    world.iaid = []
    world.clntCfg['timeval'] = int(time.time())
    world.clntCfg['toSave'] = None
    world.clntCfg['insist'] = False
    world.clntCfg['lease_file'] = ""
    if "dhcp_under_test" in world.cfg:
        # IPv6:
        if world.proto == "v6":
            v6_initialize()
        # IPv4:
        if world.proto == "v4":
            v4_initialize()

    if "dns_under_test" in world.cfg:
        dns_initialize()

    world.set_values()
    world.cfg["values"]["tr_id"] = world.cfg["tr_id"]
    # to create separate files for each test we need:
    # create new directory for that test:
    if not os.path.exists(world.cfg["dir_name"]):
        os.makedirs(world.cfg["dir_name"])
    if not os.path.exists(world.cfg["dir_name"] + '/dns') and world.dns_enable:
        os.makedirs(world.cfg["dir_name"] + '/dns')

    if world.f_cfg.tcpdump:
        cmd = world.f_cfg.tcpdump_path + 'tcpdump'
        args = [cmd, "-U", "-w", world.cfg["dir_name"] + "/capture.pcap",
                "-s", str(65535), "-i", world.cfg["iface"]]

        subprocess.Popen(args)
        # potential probelms with two instances of tcpdump running
        # TODO make sure it works properly!
        if world.dhcp_enable and world.dns_enable:
            if world.cfg["dns_iface"] != world.cfg["iface"]:
                cmd2 = world.f_cfg.tcpdump_path + 'tcpdump'
                args2 = [cmd2, "-U", "-w", world.cfg["dir_name"] + "/capture_dns.pcap",
                         "-s", str(65535), "-i", world.cfg["dns_iface"]]

                subprocess.Popen(args2)


@before.outline
def outline_before(scenario, number, step, failed):
    """
    For Outline Scenarios,
        scenario - name
        number - number of scenario
        step - which 'example' from test
        failed - reason of failure
    For more info please read UserHelp - Outline Scenarios
    """
    initialize(scenario)  # we need to initialize all


@after.outline
def outline_result(scenario, number, step, failed):
    """
    For Outline Scenarios,
        scenario - name
        number - number of scenario
        step - which 'example' from test
        failed - reason of failure
    For more info please read UserHelp - Outline Scenarios
    """
    if len(failed) == 0:
        result = 'False'
    else:
        result = 'True'
    info = str(scenario.name) + str(step) + '\n' + result
    add_result_to_report(info)


@after.each_step
def cleanup_option(step):
    pass


@after.each_scenario
def cleanup(scenario):
    """
    Global cleanup for each scenario. Implemented within tests by "Server is started."
    """
    info = str(scenario.name) + '\n' + str(scenario.failed)
    if 'outline' not in info:
        add_result_to_report(info)

    if world.f_cfg.tcpdump:
        time.sleep(1)
        args = ["killall tcpdump"]
        subprocess.call(args, shell = True)
        # TODO: log output in debug mode

    for each in world.f_cfg.software_under_test:
        functions = importlib.import_module("softwaresupport.%s.functions" % each)
        if world.f_cfg.save_leases:
            # save leases, if there is none leases in your software, just put "pass" in this function.
            functions.save_leases()

        if world.f_cfg.save_logs:
            functions.save_logs()

        # every software have something else to clear. Put in clear_all() whatever you need
        functions.clear_all()

        if '_client' in each:
            functions.kill_clnt()


@after.all
def say_goodbye(total):
    """
    Server stopping after whole work
    """
    world.clntCounter = 0
    world.srvCounter = 0
    get_common_logger().info("%d of %d scenarios passed." % (
        total.scenarios_passed,
        total.scenarios_ran
    ))
    if world.f_cfg.history:
        result = open('result', 'w')
        for item in world.result:
            result.write(str(item) + '\n')
        result.close()

    for each in world.f_cfg.software_under_test:
        if each in ['kea4_server_bind', 'kea6_server_bind']:
            clean_config = importlib.import_module("softwaresupport.%s.functions" % each)
            clean_config.run_bindctl(True, 'clean')
            kill_bind10()

        elif "client" in each:
            kill_msg = "kill the " + each[:each.find("_client")]
            get_common_logger().debug(kill_msg)
            clnt = importlib.import_module("softwaresupport.%s.functions" % each)
            clnt.stop_clnt()

        else:
            stop = importlib.import_module("softwaresupport.%s.functions" % each)
            # True passed to stop_srv is to hide output in console.
            stop.stop_srv(True)

    if world.f_cfg.auto_archive:
        name = ""
        if world.cfg["dhcp_under_test"] != "":
            name += world.cfg["dhcp_under_test"]
        if world.cfg["dns_under_test"] != "":
            if name != "":
                name += "_"
            name += world.cfg["dhcp_under_test"]

        archive_name = world.f_cfg.proto + '_' + name + '_' + time.strftime("%Y-%m-%d-%H:%M")
        archive_name = archive_file_name(1, 'tests_results_archive/' + archive_name)
        make_tarfile(archive_name + '.tar.gz', 'tests_results')

    get_common_logger().info("Goodbye.")
