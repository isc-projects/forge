# Copyright (C) 2013-2023 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Wlodzimierz Wencel

# pylint: disable=consider-using-f-string
# pylint: disable=consider-using-with
# pylint: disable=line-too-long
# pylint: disable=protected-access
# pylint: disable=unspecified-encoding
# pylint: disable=unused-import

import os
import time
import logging
from shutil import rmtree
import subprocess
import importlib

from Crypto.Random.random import randint
from scapy.config import conf
from scapy.layers.dhcp6 import DUID_LLT

from . import dependencies
from .forge_cfg import world
from .softwaresupport.multi_server_functions import make_tarfile, archive_file_name, \
    fabric_run_command, start_tcpdump, stop_tcpdump, download_tcpdump_capture
from .softwaresupport import kea
from . import logging_facility
from .srv_control import start_srv

log = logging.getLogger('forge')

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
             "address_type": 1,  # dhcpv6 mac addr type, option 79
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
             "erpdomain": "",
             "user_class_data": "",
             "relay_id": None,
             "lq-query-type": 1,
             "lq-query-address": "0::0"}

srv_values_v6 = {"T1": 1000,
                 "T2": 2000,
                 "preferred-lifetime": 3000,
                 "valid-lifetime": 4000,
                 "prefix": "3000::",
                 "prefix-len": 64,
                 "timer": 10,
                 "dst_addr": ()}

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
             "htype": 1,
             "hlen": 6,
             "broadcastBit": False,
             "hops": 0,
             "secs": 0,
             "chaddr": None,
             "FQDN_flags": "",
             "FQDN_domain_name": ""}


# we should consider transfer most of functions to separate v4 and v6 files
# TODO: make separate files after branch merge

def _set_values():
    # this function is called after each message send.
    if world.f_cfg.proto == "v6":
        world.cfg["values"] = values_v6.copy()
        world.cfg["server_times"] = server_times_v6.copy()
        # reset values to 'default for scenario'
        world.cfg["values"]["cli_duid"] = world.cfg["cli_duid"]
        world.cfg["values"]["server_id"] = ""
        world.cfg["values"]["relay_id"] = ""
        world.cfg["values"]["ia_id"] = world.cfg["ia_id"]
        world.cfg["values"]["ia_pd"] = world.cfg["ia_pd"]
    else:
        world.cfg["values"] = values_v4.copy()
        world.cfg["server_times"] = server_times_v4.copy()


world.set_values = _set_values


def client_id(mac):
    world.cfg["cli_duid"] = DUID_LLT(timeval=int(time.time()), lladdr=mac)
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


def _v4_initialize():
    # Setup scapy for v4
    # conf.iface = IFACE
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


def _v6_initialize():
    world.dhcp_enable = True
    # RFC 3315 define two addresses:
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


def _dns_initialize():
    world.cfg["dns_iface"] = world.f_cfg.dns_iface
    world.cfg["dns4_addr"] = world.f_cfg.dns4_addr
    world.cfg["dns6_addr"] = world.f_cfg.dns6_addr
    world.cfg["dns_port"] = world.f_cfg.dns_port
    world.dns_enable = True


def _define_software(dhcp_version):
    # unfortunately we have to do this every single time
    world.cfg["dhcp_under_test"] = ""
    world.cfg["dns_under_test"] = ""
    for name in world.f_cfg.software_under_test:
        if name in world.f_cfg.dhcp_used:
            world.cfg["dhcp_under_test"] = name.replace('6', '4') if dhcp_version in ['v4', 'v4_bootp'] else name.replace('4', '6')
            # world.cfg["dns_under_test"] = ""
        elif name in world.f_cfg.dns_used:
            world.cfg["dns_under_test"] = name
            # world.cfg["dhcp_under_test"] = ""


def declare_all(dhcp_version=None):
    world.climsg = []  # Message(s) to be sent
    world.srvmsg = []  # Server's response(s)
    world.rlymsg = []  # Server's response(s) Relayed by Relay Agent
    world.tmpmsg = []  # container for temporary stored messages
    world.tcpmsg = []  # Server's response(s) via TCP
    world.cliopts = []  # Option(s) to be included in the next message sent
    world.relayopts = []  # option(s) to be included in Relay Forward message.
    world.rsoo = []  # List of relay-supplied-options
    world.savedmsg = {0: []}  # Saved option(s)
    world.define = []  # temporary define variables

    proto = dhcp_version if dhcp_version else world.f_cfg.proto
    # Most of the time, treat v4_bootp as v4. Use dhcp_version to differentiate between them.
    if proto == 'v4_bootp':
        proto = 'v4'
    world.proto = world.f_cfg.proto = proto
    world.oro = None
    world.vendor = []
    world.iaad = []
    world.iapd = []
    world.opts = []
    world.subopts = []
    world.message_fields = []
    world.subnet_add = True
    world.control_channel = None  # last received response from any communication channel
    world.cfg = {}

    _define_software(dhcp_version)

    world.f_cfg.multiple_tested_servers = [world.f_cfg.mgmt_address]
    # dictionary that will keep multiple configs for various servers
    # mainly for testing multiple kea servers in the single test,
    # multiple servers has to be configured exactly identical.
    # supported only for Kea servers

    world.configClass = None
    # list that will keep configuration class from which mysql/postgres/netconf
    # configuration script will be generated
    # in future it's designed to clear JSON configuration process as well

    world.configString = ""
    world.generated_config = None

    if 'isc_dhcp' in world.cfg['dhcp_under_test']:
        world.cfg['leases'] = '/tmp/dhcpd.leases'  # do not use different value
        world.cfg['dhcp_log_file'] = '/var/log/forge_dhcpd.log'  # do not use different value
    else:
        world.cfg['leases'] = os.path.join(world.f_cfg.software_install_path,
                                           f'var/lib/kea/kea-leases{world.proto[1]}.csv')

    world.cfg['kea_log_file'] = os.path.join(world.f_cfg.software_install_path + '/var/log/kea.log')
    world.cfg['kea_ca_log_file'] = os.path.join(world.f_cfg.software_install_path + '/var/log/kea-ctrl-agent.log')

    world.loops = {"active": False,
                   "save_leases_details": False}

    world.dns_enable = False
    world.dhcp_enable = False
    world.ddns_enable = False
    world.ctrl_enable = False
    world.fuzzing = False

    # clear tmp DB values to use default from configuration
    world.f_cfg.db_type = world.f_cfg.db_type_bk
    world.f_cfg.db_host = world.f_cfg.db_host_bk
    world.f_cfg.db_name = world.f_cfg.db_name_bk
    world.f_cfg.db_passwd = world.f_cfg.db_passwd_bk
    world.f_cfg.db_user = world.f_cfg.db_user_bk


# @before.all
def test_start():
    """
    Server starting before testing.
    Runs once per forge invocation.
    """
    # clear tests results
    if os.path.exists('tests_results'):
        rmtree('tests_results')
    os.makedirs('tests_results')
    if not os.path.exists('tests_results_archive') and world.f_cfg.auto_archive:
        os.makedirs('tests_results_archive')

    world.result = []

    # Print scapy version.
    dependencies.print_versions()

    # Initialize the common logger.
    logging_facility.logger_initialize(world.f_cfg.loglevel)

    # let's assume debian is always
    world.server_system = 'debian'
    # and now check if it's redhat or alpine
    result = fabric_run_command('ls -al /etc/redhat-release',
                                hide_all=True, ignore_errors=True)
    if result.succeeded:
        world.server_system = 'redhat'
        world.server_system_version = result.stdout
    else:
        result = fabric_run_command('ls -al /etc/alpine-release',
                                    hide_all=True, ignore_errors=True)
        if result.succeeded:
            world.server_system = 'alpine'
            world.server_system_version = result.stdout
    print('server running on %s based system' % world.server_system)

    # let's assume x86_64 is the default architecture
    world.server_architecture = 'x86_64'
    # chech what architecture system is returning
    result = fabric_run_command('arch',
                                hide_all=True, ignore_errors=True)
    if result.succeeded:
        world.server_architecture = result.stdout.rstrip()
        print(f'server running on {world.server_architecture} architecture')
    else:
        print('server running on UNKNOWN architecture, defaulting to x86_64')

    # stop any SUT running
    kea_under_test = False
    if not world.f_cfg.no_server_management:
        for sut_name in world.f_cfg.software_under_test:
            sut_module = importlib.import_module("src.softwaresupport.%s.functions" % sut_name)
            # True passed to stop_srv is to hide output in console.
            sut_module.stop_srv(destination_address=world.f_cfg.mgmt_address)

            if 'kea' in sut_name:
                kea_under_test = True

    if kea_under_test:
        # for now let's assume that both systems are the same
        kea.db_setup()
        if world.f_cfg.mgmt_address_2:
            kea.db_setup(dest=world.f_cfg.mgmt_address_2)


def _clear_remainings():
    if not world.f_cfg.no_server_management:
        for remote_server in world.f_cfg.multiple_tested_servers:
            for sut in world.f_cfg.software_under_test:
                functions = importlib.import_module("src.softwaresupport.%s.functions" % sut)
                # every software have something else to clear. Put in clear_all() whatever you need
                functions.clear_all(destination_address=remote_server)


# @before.each_scenario
def initialize(scenario):
    # try to automagically detect DHCP version based on fixture presence
    # or marker presence
    try:
        dhcp_version = scenario._request.getfixturevalue('dhcp_version')
    except BaseException:
        dhcp_version = None
        for v in ['v4', 'v6', 'v4_bootp']:
            if scenario.get_closest_marker(v):
                dhcp_version = v
                break

    # Declare all default values
    declare_all(dhcp_version)

    world.cfg["iface"] = world.f_cfg.iface
    # world.cfg["server_type"] = SOFTWARE_UNDER_TEST for now I'll leave it here,
    # now we use world.cfg["dhcp_under_test"] and world.cfg["dns_under_test"] (in function _define_software)
    # it is being filled with values in srv_control
    world.cfg["wait_interval"] = world.f_cfg.packet_wait_interval
    world.cfg['cfg_file'] = [f'kea-dhcp{world.proto[1]}.conf',
                             "kea-ddns.conf",
                             "kea-ctrl-agent.conf",
                             "kea-netconf.conf"]
    if "isc_dhcp" in world.cfg["dhcp_under_test"]:
        world.cfg["cfg_file"] = "server.cfg"
        world.subcfg = [["", "", "", "", "", "", ""]]

    world.cfg["cfg_file_2"] = "second_server.cfg"
    world.reservation_backend = ""
    test_result_dir = str(scenario.name).replace(".", "_").replace('[', '_').replace(']', '_').replace('/', '_')
    world.cfg["test_result_dir"] = os.path.join('tests_results', test_result_dir)
    world.cfg["subnet"] = ""
    world.cfg["server-id"] = ""
    world.cfg["csv-format"] = "true"
    world.cfg["tr_id"] = None
    world.name = scenario.name
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

    # dns cleanup
    world.dns_qd = []
    world.dns_an = []
    world.dns_ns = []
    world.dns_ar = []
    world.tcpmsg = []
    world.question_record = None
    world.dns_query = None

    if "dhcp_under_test" in world.cfg:
        # IPv6:
        if world.proto == "v6":
            _v6_initialize()
        # IPv4:
        if world.proto == "v4":
            _v4_initialize()

    if "dns_under_test" in world.cfg:
        _dns_initialize()

    world.set_values()
    world.cfg["values"]["tr_id"] = world.cfg["tr_id"]
    # to create separate files for each test we need:
    # create new directory for that test:
    if not os.path.exists(world.cfg["test_result_dir"]):
        os.makedirs(world.cfg["test_result_dir"])
    if not os.path.exists(world.cfg["test_result_dir"] + '/dns') and world.dns_enable:
        os.makedirs(world.cfg["test_result_dir"] + '/dns')

    if world.f_cfg.tcpdump:
        start_tcpdump(auto_start_dns=True)
    if world.f_cfg.tcpdump_on_remote_system:
        start_tcpdump(location=world.f_cfg.mgmt_address, file_name='remote.pcap')

    _clear_remainings()


# @after.each_scenario
def cleanup(scenario):
    """
    Global cleanup for each scenario. Implemented within tests by "Server is started."
    """
    info = str(scenario.name) + '\n' + str(scenario.failed)
    if 'outline' not in info:
        world.result.append(info)

    if world.f_cfg.tcpdump:
        stop_tcpdump()

    if not world.f_cfg.no_server_management:
        for remote_server in world.f_cfg.multiple_tested_servers:
            start_srv('DHCP', 'stopped', dest=remote_server)
            for sut in world.f_cfg.software_under_test:
                functions = importlib.import_module("src.softwaresupport.%s.functions" % sut)
                # try:
                if world.f_cfg.save_leases:
                    # save leases, if there is none leases in your software, just put "pass" in this function.
                    functions.save_leases(destination_address=remote_server)

                if world.f_cfg.save_logs:
                    functions.save_logs(destination_address=remote_server)

                if world.f_cfg.tcpdump_on_remote_system:
                    stop_tcpdump(location=remote_server)
                    # it's not bullet proof it won't download anything from second HA system
                    download_tcpdump_capture(location=remote_server, file_name='remote.pcap')


# @after.all
def say_goodbye():
    """
    Server stopping after whole work
    """
    if world.f_cfg.history:
        result = open('result', 'w')
        for item in world.result:
            result.write(str(item) + '\n')
        result.close()

    if not world.f_cfg.no_server_management:
        for remote_server in world.f_cfg.multiple_tested_servers:
            for sut in world.f_cfg.software_under_test:
                stop = importlib.import_module("src.softwaresupport.%s.functions" % sut)
                # True passed to stop_srv is to hide output in console.
                try:
                    stop.stop_srv(destination_address=remote_server)
                except BaseException:
                    pass

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
