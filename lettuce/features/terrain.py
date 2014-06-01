# Copyright (C) 2013 Internet Systems Consortium.
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
from init_all import LOGLEVEL, MGMT_ADDRESS, SOFTWARE_UNDER_TEST, CLI_MAC, IFACE, \
    REL4_ADDR, SRV4_ADDR, PROTO, HISTORY, GIADDR4, TCPDUMP, TCPDUMP_INSTALL_DIR, \
    SAVE_BIND_LOGS, AUTO_ARCHIVE, SAVE_LEASES, PACKET_WAIT_INTERVAL,CLI_LINK_LOCAL
from lettuce import world, before, after
from logging_facility import *
from scapy.all import sniff
from scapy.config import conf
from scapy.layers.dhcp6 import DUID_LLT
from softwaresupport.bind10 import kill_bind10, start_bind10
from time import sleep
from softwaresupport.multi_server_functions import fabric_download_file, make_tarfile, archive_file_name, fabric_remove_file_command

import importlib
import os
import subprocess
import sys
import time

add_option_v6 = {'client_id': True,
                 'preference': False,
                 'time': False,
                 'relay_msg': False,
                 'server_uni': False,
                 'status_code': False,
                 'rapid_commit': False,
                 'interface_id': False,
                 'reconfig': False,
                 'option_request': False,
                 'reconfig_accept': False,
                 'server_id': False,
                 'wrong_client_id': False,
                 'wrong_server_id': False,
                 'IA_NA': True,
                 'IA_TA': False,
                 'IA_PD': False,
                 'IA_Prefix': False,
                 'IA_Address': False,
                 'vendor_class': False,
                 'vendor_specific_info': False
                 }

values_v6 = {"T1": 0,  # IA_NA IA_PD
             "T2": 0,  # IA_NA IA_PD
             "address": "::",
             "prefix": "::",
             "plen": 0,  # prefix; plz remember, to add prefix and prefix length!
             "preflft": 0,  # IA_Address IA_Prefix
             "validlft": 0,  # IA_Address IA_Prefix
             "enterprisenum": 0,  # vendor
             "linkaddr": "3000::ffff",  # relay
             "peeraddr": "2000::1",  # relay
             "ifaceid": "15",  # relay
             "DUID": None
             }

srv_values_v6 = {"T1": 1000,
                 "T2": 2000,
                 "preferred-lifetime": 3000,
                 "valid-lifetime": 4000,
                 "prefix": "3000::",
                 "prefix-len" : 64
                }

clnt_set_wrong = {"trid": False,
                  "iaid": False,
                  "client_id": False,
                  "server_id": False
                 }

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
                   "valid-lifetime": 4000,
                   }

values_v4 = {"source_IP": "0.0.0.0",
             "dstination_IP": "255.255.255.255",
             "ciaddr": "0.0.0.0",
             "yiaddr": "0.0.0.0",
             "siaddr": "0.0.0.0",
             "giaddr": GIADDR4,
             "chaddr": None
             }

add_option_v4 = {"vendor_class_id": False,
                 "client_id": True
                 }

# we should consider transfer most of functions to separate v4 and v6 files
# TODO: make separate files after branch merge

def set_values():
    if PROTO == "v6":
        world.cfg["values"] = values_v6.copy()
        world.cfg["server_times"] = server_times_v6.copy()
        world.clntCfg["values"] = srv_values_v6.copy()
        world.clntCfg["set_wrong"] = clnt_set_wrong.copy()
    else:
        world.cfg["values"] = values_v4.copy()
        world.cfg["server_times"] = server_times_v4.copy()


def set_options():
    if PROTO == "v6":
        world.cfg["add_option"] = add_option_v6.copy()
    else:
        world.cfg["add_option"] = add_option_v4.copy()



def add_result_to_raport(info):
    world.result.append(info)


def client_id(mac):
    world.cfg["cli_duid"] = DUID_LLT(timeval=int(time.time()), lladdr=mac)


def ia_id():
    world.cfg["ia_id"] = randint(1, 99999)


def ia_pd():
    world.cfg["ia_pd"] = randint(1, 99999)


def multiprotocol_initialize():
    pass


def v4_initialize():
    # Setup scapy for v4
    #conf.iface = IFACE
    conf.checkIPaddr = False  # DHCPv4 is sent from 0.0.0.0, so response matching may confuse scapy
    world.cfg["srv4_addr"] = SRV4_ADDR
    world.cfg["rel4_addr"] = REL4_ADDR
    world.cfg["giaddr4"] = GIADDR4
    world.cfg["space"] = "dhcp4"
    world.cfg["PACKET_WAIT_INTERVAL"] = PACKET_WAIT_INTERVAL


def v6_initialize():
    # RFC 3315 define two addresess:
    # All_DHCP_Relay_Agents_and_Servers = ff02::1:2
    # All DHCP_Servers ff05::1:3 that is deprecated. 
    world.cfg["address_v6"] = "ff02::1:2"
    world.cfg["cli_link_local"] = CLI_LINK_LOCAL
    world.cfg["unicast"] = False
    world.cfg["relay"] = False
    world.cfg["space"] = "dhcp6"

    # Setup scapy for v6
    conf.iface6 = IFACE
    conf.use_pcap = True


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
    if not os.path.exists('tests_results_archive') and AUTO_ARCHIVE:
        os.makedirs('tests_results_archive')

    world.result = []

    # Initialize the common logger. The instance of this logger can
    # be instantiated by get_common_logger()
    logger_initialize(LOGLEVEL)

    if "server" in SOFTWARE_UNDER_TEST:
        if SOFTWARE_UNDER_TEST in ['kea4_server', 'kea6_server']:
            get_common_logger().debug("Starting Bind:")

            try:
                # Make sure there is noo garbage instance of bind10 running.
                kill_bind10()
                start_bind10()
                get_common_logger().debug("Bind10 successfully started")
            except:
                get_common_logger().error("Bind10 start failed\n\nSomething go wrong with connection\n\
                                            Please make sure it's configured properly\nIP destination \
                                            address: %s\nLocal Mac address: %s\nNetwork interface: %s"
                                          % (MGMT_ADDRESS, CLI_MAC, IFACE))
                sys.exit()
        elif SOFTWARE_UNDER_TEST in ["isc_dhcp6_server", "dibbler_server"]:
            # TODO: import only one function
            stop = importlib.import_module("softwaresupport.%s.functions" % SOFTWARE_UNDER_TEST)
            stop.stop_srv()  # shouldn't we start the server here?

        else:
            get_common_logger().error("Server " + SOFTWARE_UNDER_TEST + " not implemented yet")
    elif "client" in SOFTWARE_UNDER_TEST:
        idx = SOFTWARE_UNDER_TEST.find("_client")
        get_common_logger().debug("cleaning " + SOFTWARE_UNDER_TEST[:idx] + "...")
        clnt = importlib.import_module("softwaresupport.%s.functions" % SOFTWARE_UNDER_TEST)
        clnt.stop_clnt()


        #If relay is used routing needs to be reconfigured on DUT


#     try:
#         if REL4_ADDR and (SOFTWARE_UNDER_TEST  == 'kea4'):
#             assert False, "we don't support ip v4 yet"
# #             with settings(host_string = MGMT_ADDRESS, user = MGMT_USERNAME, password = MGMT_PASSWORD):
# #                 run("route add -host %s gw %s" % (GIADDR4, REL4_ADDR))
#     except:
#         pass # most likely REL4_ADDR caused this exception -> we do not use relay

@before.each_scenario
def initialize(scenario):
    world.climsg = []  # Message(s) to be sent
    world.cliopts = []  # Option(s) to be included in the next message sent
    world.srvmsg = []  # Server's response(s)
    world.savedmsg = []  # Saved option(s)
    world.define = []  # temporary define variables

    world.proto = PROTO
    world.oro = None
    world.vendor = []
    world.opts = []
    world.subopts = []

    world.cfg = {}
    world.cfg["iface"] = IFACE
    world.cfg["server_type"] = SOFTWARE_UNDER_TEST

    world.cfg["cfg_file"] = "server.cfg"
    world.cfg["conf"] = ""  # Just empty config for now

    dir_name = str(scenario.name).replace(".", "_")
    world.cfg["dir_name"] = 'tests_results/' + dir_name

    world.cfg["subnet"] = ""

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
    world.saved = []
    world.iaid = []
    world.clntCfg['timeval'] = int(time.time())
    world.clntCfg['toSave'] = None

    # Setup DUID for DHCPv6 (and also for DHCPv4, see RFC4361)
    if not hasattr(world.cfg, "cli_duid"):
        client_id(CLI_MAC)

    if not hasattr(world.cfg, "ia_id"):
        ia_id()

    if not hasattr(world.cfg, "ia_pd"):
        ia_pd()

    # set couple things depending on used IP version:
    # IPv6:
    if world.proto == "v6":
        v6_initialize()
        
    # IPv4:
    if world.proto == "v4":
        v4_initialize()

    set_values()
    set_options()

    if TCPDUMP:
        # to create separate files for each test we need:
        # create new directory for that test:

        if not os.path.exists(world.cfg["dir_name"]):
            os.makedirs(world.cfg["dir_name"])
        # create new file for capture
        if not os.path.exists(world.cfg["dir_name"] + '/capture.pcap'):
            tmp = open(world.cfg["dir_name"] + '/capture.pcap', 'w+')
            tmp.close()
        # also IP version for tcpdump
        type = 'ip'

        if PROTO == "v6":
            type = type + '6'
        cmd = TCPDUMP_INSTALL_DIR + 'tcpdump'
        args = [cmd, "-U", "-w", world.cfg["dir_name"] + "/capture.pcap",
                "-s", str(65535), "-i", world.cfg["iface"], type]
        get_common_logger().debug("Running tcpdump: ")
        get_common_logger().debug(args)
        # TODO: hide stdout, log it in debug mode
        subprocess.Popen(args)


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
    initialize(None)  # we need to initialize all


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
    add_result_to_raport(info)


@after.each_step
def cleanup_option(step):
    #set_options ()
    pass


@after.each_scenario
def cleanup(scenario):
    """
    Global cleanup for each scenario. Implemented within tests by "Server is started."
    """
    info = str(scenario.name) + '\n' + str(scenario.failed)
    if 'outline' not in info:
        add_result_to_raport(info)

    if TCPDUMP:
        args = ["killall tcpdump"]
        subprocess.call(args, shell=True)
        # TODO: log output in debug mode

    # copy log file from remote server:
    if 'server' in SOFTWARE_UNDER_TEST:
        if SAVE_BIND_LOGS:
            fabric_download_file('log_file', world.cfg["dir_name"] + '/log_file')

        if SAVE_LEASES:
            if SOFTWARE_UNDER_TEST not in ['kea', 'kea4_server', 'kea6_server']:
                fabric_download_file(world.cfg['leases'], world.cfg["dir_name"] + '/dhcpd6.leases')
            elif SOFTWARE_UNDER_TEST in ['kea','kea4_server', 'kea6_server']:
                fabric_download_file(world.cfg['leases'], world.cfg["dir_name"] + '/kea_leases.csv')
            else:
                pass
        if SOFTWARE_UNDER_TEST in ['kea','kea4_server', 'kea6_server']:
            fabric_remove_file_command(world.cfg['leases'])
    elif "client" in SOFTWARE_UNDER_TEST:
        idx = SOFTWARE_UNDER_TEST.find("_client")
        get_common_logger().debug("cleaning " + SOFTWARE_UNDER_TEST[:idx] + "...")
        clnt = importlib.import_module("softwaresupport.%s.functions" % SOFTWARE_UNDER_TEST)
        clnt.kill_clnt()

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
    if HISTORY:
        result = open('result', 'w')
        for item in world.result:
            result.write(str(item) + '\n')
        result.close()
    if "server" in SOFTWARE_UNDER_TEST:
        if SOFTWARE_UNDER_TEST in ['kea4_server', 'kea6_server']:
            #TODO: import only one function!
            clean_config = importlib.import_module("softwaresupport.%s.functions" % SOFTWARE_UNDER_TEST)
            clean_config.run_bindctl(True, 'clean')
            kill_bind10()
        #         try:
        #             if REL4_ADDR and (SOFTWARE_UNDER_TEST  == 'kea4'):
        #                 with settings(host_string = MGMT_ADDRESS, user = MGMT_USERNAME, password = MGMT_PASSWORD):
        #                     run("route del -host %s" % (GIADDR4))
        #         except NameError:
        #             pass # most likely REL4_ADDR caused this exception -> we do not use relay
        elif SOFTWARE_UNDER_TEST in ['isc_dhcp6_server', 'dibbler_server']:
            stop = importlib.import_module("softwaresupport.%s.functions" % SOFTWARE_UNDER_TEST)
            stop.stop_srv()
    elif "client" in SOFTWARE_UNDER_TEST:
        idx = SOFTWARE_UNDER_TEST.find("_client")
        get_common_logger().debug("cleaning " + SOFTWARE_UNDER_TEST[:idx] + "...")
        clnt = importlib.import_module("softwaresupport.%s.functions" % SOFTWARE_UNDER_TEST)
        clnt.stop_clnt()

    if AUTO_ARCHIVE:
        archive_name = PROTO + '_' + SOFTWARE_UNDER_TEST + '_' + time.strftime("%Y-%m-%d-%H:%M")
        archive_name = archive_file_name(1, 'tests_results_archive/' + archive_name)
        make_tarfile(archive_name + '.tar.gz', 'tests_results')

    get_common_logger().info("Goodbye.")
