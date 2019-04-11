#!/usr/bin/python

# Copyright (C) 2013-2018 Internet Systems Consortium.
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
#
# author: Wlodzimierz Wencel

import importlib
import optparse
import os
import sys
import threading
import fcntl
import socket
import struct
import sys


from init_all import SOFTWARE_INSTALL_PATH, LOGLEVEL, SOFTWARE_UNDER_TEST, DB_TYPE, SHOW_PACKETS_FROM, \
    SRV4_ADDR, REL4_ADDR, GIADDR4, IFACE, CLI_LINK_LOCAL, SERVER_IFACE, OUTPUT_WAIT_INTERVAL, \
    OUTPUT_WAIT_MAX_INTERVALS, PACKET_WAIT_INTERVAL, SRV_IPV6_ADDR_GLOBAL, SRV_IPV6_ADDR_LINK_LOCAL, HISTORY,\
    TCPDUMP, TCPDUMP_PATH, SAVE_CONFIG_FILE, AUTO_ARCHIVE, SLEEP_TIME_1, SLEEP_TIME_2, MGMT_ADDRESS, MGMT_USERNAME,\
    MGMT_PASSWORD, SAVE_LOGS, BIND_LOG_TYPE, BIND_LOG_LVL, BIND_MODULE, SAVE_LEASES, DNS_IFACE, DNS4_ADDR, DNS6_ADDR, DNS_PORT, \
    DNS_SERVER_INSTALL_PATH, DNS_DATA_PATH, ISC_DHCP_LOG_FACILITY, ISC_DHCP_LOG_FILE, DB_NAME, DB_USER, DB_PASSWD, \
    DB_HOST, CIADDR, MGMT_ADDRESS_2, MGMT_ADDRESS_3, FABRIC_PTY

# Create Forge configuration class
SOFTWARE_INSTALL_DIR = SOFTWARE_INSTALL_PATH  # for backward compatibility of tests
LOGLEVEL = os.getenv('LOGLEVEL', LOGLEVEL)
SOFTWARE_UNDER_TEST = os.getenv('SOFTWARE_UNDER_TEST', SOFTWARE_UNDER_TEST)
DB_TYPE = os.getenv('DB_TYPE', DB_TYPE)
SOFTWARE_INSTALL_PATH = os.getenv('SOFTWARE_INSTALL_DIR', SOFTWARE_INSTALL_PATH)
SHOW_PACKETS_FROM = os.getenv('SHOW_PACKETS_FROM', SHOW_PACKETS_FROM)
SRV4_ADDR = os.getenv('SRV4_ADDR', SRV4_ADDR)
REL4_ADDR = os.getenv('REL4_ADDR', REL4_ADDR)
GIADDR4 = os.getenv('GIADDR4', GIADDR4)
CIADDR = os.getenv('CIADDR', CIADDR)
IFACE = os.getenv('IFACE', IFACE)
CLI_LINK_LOCAL = os.getenv('CLI_LINK_LOCAL', CLI_LINK_LOCAL)
SERVER_IFACE = os.getenv('SERVER_IFACE', SERVER_IFACE)
OUTPUT_WAIT_INTERVAL = os.getenv('OUTPUT_WAIT_INTERVAL', OUTPUT_WAIT_INTERVAL)
OUTPUT_WAIT_MAX_INTERVALS = os.getenv('OUTPUT_WAIT_MAX_INTERVALS', OUTPUT_WAIT_MAX_INTERVALS)
PACKET_WAIT_INTERVAL = os.getenv('PACKET_WAIT_INTERVAL', PACKET_WAIT_INTERVAL)
SRV_IPV6_ADDR_GLOBAL = os.getenv('SRV_IPV6_ADDR_GLOBAL', SRV_IPV6_ADDR_GLOBAL)
SRV_IPV6_ADDR_LINK_LOCAL = os.getenv('SRV_IPV6_ADDR_LINK_LOCAL', SRV_IPV6_ADDR_LINK_LOCAL)
HISTORY = os.getenv('HISTORY', HISTORY)
TCPDUMP = os.getenv('TCPDUMP', TCPDUMP)
TCPDUMP_PATH = os.getenv('TCPDUMP_INSTALL_DIR', TCPDUMP_PATH)
SAVE_CONFIG_FILE = os.getenv('SAVE_CONFIG_FILE', SAVE_CONFIG_FILE)
AUTO_ARCHIVE = os.getenv('AUTO_ARCHIVE', AUTO_ARCHIVE)
SLEEP_TIME_1 = os.getenv('SLEEP_TIME_1', SLEEP_TIME_1)
SLEEP_TIME_2 = os.getenv('SLEEP_TIME_2', SLEEP_TIME_2)
MGMT_ADDRESS = os.getenv('MGMT_ADDRESS', MGMT_ADDRESS)
MGMT_ADDRESS_2 = os.getenv('MGMT_ADDRESS', MGMT_ADDRESS_2)
MGMT_ADDRESS_3 = os.getenv('MGMT_ADDRESS', MGMT_ADDRESS_3)
MGMT_USERNAME = os.getenv('MGMT_USERNAME', MGMT_USERNAME)
MGMT_PASSWORD = os.getenv('MGMT_PASSWORD', MGMT_PASSWORD)
SAVE_LOGS = os.getenv('SAVE_LOGS', SAVE_LOGS)
BIND_LOG_TYPE = os.getenv('BIND_LOG_TYPE', BIND_LOG_TYPE)
BIND_LOG_LVL = os.getenv('BIND_LOG_LVL', BIND_LOG_LVL)
BIND_MODULE = os.getenv('BIND_MODULE', BIND_MODULE)
SAVE_LEASES = os.getenv('SAVE_LEASES', SAVE_LEASES)
DNS_IFACE = os.getenv('DNS_IFACE', DNS_IFACE)
DNS4_ADDR = os.getenv('DNS4_ADDR', DNS4_ADDR)
DNS6_ADDR = os.getenv('DNS6_ADDR', DNS6_ADDR)
DNS_PORT = os.getenv('DNS_PORT', DNS_PORT)
DNS_SERVER_INSTALL_PATH = os.getenv('DNS_SERVER_INSTALL_PATH', DNS_SERVER_INSTALL_PATH)
DNS_DATA_PATH = os.getenv('DNS_DATA_PATH', DNS_DATA_PATH)
ISC_DHCP_LOG_FACILITY = os.getenv('ISC_DHCP_LOG_FACILITY', ISC_DHCP_LOG_FACILITY)
ISC_DHCP_LOG_FILE = os.getenv('ISC_DHCP_LOG_FILE', ISC_DHCP_LOG_FILE)
DB_NAME = os.getenv('DB_NAME', DB_NAME)
DB_USER = os.getenv('DB_USER', DB_USER)
DB_PASSWD = os.getenv('DB_PASSWD', DB_PASSWD)
DB_HOST = os.getenv('DB_HOST', DB_HOST)
FABRIC_PTY = os.getenv('FABRIC_PTY', FABRIC_PTY)


class ForgeConfiguration:
    def __init__(self):
        # default
        self.dns_used = ["bind9_server"]
        self.dhcp_used = ["dibbler_server", "dibbler_client", "isc_dhcp4_server", "isc_dhcp6_server",
                          "kea4_server", "kea4_server_bind", "kea6_server", "kea6_server_bind", "kea6_mini_server",
                          "none_server"]

        # no_server_management value can be set by -N option on startup to turn off remote server management
        self.no_server_management = False
        self.empty = ""
        self.white_space = " "
        self.none = None
        # FORGE
        self.mgmt_address = MGMT_ADDRESS
        self.mgmt_address_2 = MGMT_ADDRESS_2  # for additional vm, exact copy of main vm
        self.mgmt_address_3 = MGMT_ADDRESS_3  # for additional vm, exact copy of main vm
        self.mgmt_username = MGMT_USERNAME
        self.mgmt_password = MGMT_PASSWORD
        self.multiple_tested_servers = [self.mgmt_address]
        self.loglevel = LOGLEVEL
        self.history = HISTORY
        self.tcpdump = TCPDUMP
        self.tcpdump_path = TCPDUMP_PATH
        self.save_config_file = SAVE_CONFIG_FILE
        self.auto_archive = AUTO_ARCHIVE
        self.sleep_time_1 = SLEEP_TIME_1
        self.sleep_time_2 = SLEEP_TIME_2
        self.show_packets_from = SHOW_PACKETS_FROM
        self.save_leases = SAVE_LEASES
        self.save_logs = SAVE_LOGS
        self.packet_wait_interval = PACKET_WAIT_INTERVAL
        self.fabric_pty = FABRIC_PTY  # default is False
        # value_when_true if condition else value_when_false
        # DHCP
        self.proto = 'v4'  # default value but it is overriden by each test in terrain.declare_all()
        self.software_under_test = SOFTWARE_UNDER_TEST
        self.software_install_path = SOFTWARE_INSTALL_PATH
        self.software_install_dir = SOFTWARE_INSTALL_PATH  # that keeps backwards compatibility
        self.db_type = DB_TYPE
        self.db_host = DB_HOST
        self.db_name = DB_NAME
        self.db_passwd = DB_PASSWD
        self.db_user = DB_USER
        self.db_type_bk = DB_TYPE
        self.db_host_bk = DB_HOST
        self.db_name_bk = DB_NAME
        self.db_passwd_bk = DB_PASSWD
        self.db_user_bk = DB_USER
        self.srv4_addr = SRV4_ADDR
        self.rel4_addr = REL4_ADDR
        self.gia4_addr = GIADDR4
        self.giaddr4 = GIADDR4  # it's for backwards compatibility
        self.ciaddr = CIADDR
        self.iface = IFACE
        self.server_iface = SERVER_IFACE
        self.cli_mac = self.gethwaddr(self.iface)

        # DNS
        self.dns_iface = DNS_IFACE
        self.dns4_addr = DNS4_ADDR
        self.dns6_addr = DNS6_ADDR
        self.dns_port = DNS_PORT
        self.dns_data_path = DNS_DATA_PATH
        self.dns_server_install_path = DNS_SERVER_INSTALL_PATH

        # ISC-DHCP specific
        self.isc_dhcp_log_file = ISC_DHCP_LOG_FILE
        self.isc_dhcp_log_facility = ISC_DHCP_LOG_FACILITY

        # NETWORK
        self.srv_ipv6_addr_global = SRV_IPV6_ADDR_GLOBAL
        self.srv_ipv6_addr_link_local = SRV_IPV6_ADDR_LINK_LOCAL
        self.cli_link_local = CLI_LINK_LOCAL

        # used defined variables
        self.user_variables_temp = []

        # basic validation of configuration
        self.basic_validation()

    def gethwaddr(self, ifname):
        if sys.platform != "darwin":
            s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
            info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname))
            return ':'.join(['%02x' % ord(char) for char in info[18:24]])
        else:
            # TODO fix this for MAC OS, this is temporary quick fix just for my local system
            return "0a:00:27:00:00:00"

    def basic_validation(self):
        # TODO we need new basic validation or just dump it...
        # if self.proto == "v4" and self.software_under_test[0] not in ["none_server"]:
        #     if "4" not in self.software_under_test[0]:
        #         print "Miss match of protocol version and DHCP server version"
        #         sys.exit(-1)
        # if self.proto == "v6" and self.software_under_test[0] not in ["none_server"]:
        #     if "6" not in self.software_under_test[0]:
        #         print "Miss match of protocol version and DHCP server version"
        #         sys.exit(-1)
        if self.software_install_path == "":
            print "Configuration failure, software_install_path empty." \
                  " Please use ./forge.py -T to validate configuration."
            sys.exit(-1)
        if self.mgmt_address == "":
            print "Configuration failure, mgmt_address empty. Please use ./forge.py -T to validate configuration."
            sys.exit(-1)

    def set_env_val(self, env_name, env_val):
        """
        Set environmet variable.
        :param env_name:
        :param env_val:
        :return:
        """
        os.putenv(env_name, env_val)

    def set_temporaty_value(self, env_name, env_val):
        """
        Will set temporary value of existing variable for the purpose of one test,
        should be removed in section @after_each
        :return:
        """
        # TODO develop this one
        pass

    def remove_temporary_value(self, env_name):
        """
        Will remove all temporary changed values bringin back previously set values
        Have to be called in terrazin.py @after_each
        :return:
        """
        # TODO develop this one
        pass


# global object that stores all needed data: configs, etc.
world = threading.local()
world.f_cfg = ForgeConfiguration()


# stub that replaces lettuce step decorator
def step(pattern):
    def wrap(func):
        return func
    return wrap
