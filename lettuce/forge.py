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

from features.init_all import SOFTWARE_INSTALL_PATH, LOGLEVEL, PROTO, SOFTWARE_UNDER_TEST, DB_TYPE, SHOW_PACKETS_FROM, \
    SRV4_ADDR, REL4_ADDR, GIADDR4, IFACE, CLI_LINK_LOCAL, SERVER_IFACE, OUTPUT_WAIT_INTERVAL, \
    OUTPUT_WAIT_MAX_INTERVALS, PACKET_WAIT_INTERVAL, SRV_IPV6_ADDR_GLOBAL, SRV_IPV6_ADDR_LINK_LOCAL, HISTORY,\
    TCPDUMP, TCPDUMP_PATH, SAVE_CONFIG_FILE, AUTO_ARCHIVE, SLEEP_TIME_1, SLEEP_TIME_2, MGMT_ADDRESS, MGMT_USERNAME,\
    MGMT_PASSWORD, SAVE_LOGS, BIND_LOG_TYPE, BIND_LOG_LVL, BIND_MODULE, SAVE_LEASES, DNS_IFACE, DNS_ADDR, DNS_PORT, \
    DNS_SERVER_INSTALL_PATH, DNS_DATA_PATH, ISC_DHCP_LOG_FACILITY, ISC_DHCP_LOG_FILE, DB_NAME, DB_USER, DB_PASSWD,\
    DB_HOST, CIADDR

# Create Forge configuration class
SOFTWARE_INSTALL_DIR = SOFTWARE_INSTALL_PATH  # for backward compatibility of tests
LOGLEVEL = os.getenv('LOGLEVEL', LOGLEVEL)
PROTO = os.getenv('PROTO', PROTO)
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
MGMT_USERNAME = os.getenv('MGMT_USERNAME', MGMT_USERNAME)
MGMT_PASSWORD = os.getenv('MGMT_PASSWORD', MGMT_PASSWORD)
SAVE_LOGS = os.getenv('SAVE_LOGS', SAVE_LOGS)
BIND_LOG_TYPE = os.getenv('BIND_LOG_TYPE', BIND_LOG_TYPE)
BIND_LOG_LVL = os.getenv('BIND_LOG_LVL', BIND_LOG_LVL)
BIND_MODULE = os.getenv('BIND_MODULE', BIND_MODULE)
SAVE_LEASES = os.getenv('SAVE_LEASES', SAVE_LEASES)
DNS_IFACE = os.getenv('DNS_IFACE', DNS_IFACE)
DNS_ADDR = os.getenv('DNS_ADDR', DNS_ADDR)
DNS_PORT = os.getenv('DNS_PORT', DNS_PORT)
DNS_SERVER_INSTALL_PATH = os.getenv('DNS_SERVER_INSTALL_PATH', DNS_SERVER_INSTALL_PATH)
DNS_DATA_PATH = os.getenv('DNS_DATA_PATH', DNS_DATA_PATH)
ISC_DHCP_LOG_FACILITY = os.getenv('ISC_DHCP_LOG_FACILITY', ISC_DHCP_LOG_FACILITY)
ISC_DHCP_LOG_FILE = os.getenv('ISC_DHCP_LOG_FILE', ISC_DHCP_LOG_FILE)
DB_NAME = os.getenv('DB_NAME', DB_NAME)
DB_USER = os.getenv('DB_USER', DB_USER)
DB_PASSWD = os.getenv('DB_PASSWD', DB_PASSWD)
DB_HOST = os.getenv('DB_HOST', DB_HOST)


class ForgeConfiguration:
    def __init__(self):
        # default
        self.dns_used = "bind9_server",
        self.dhcp_used = "dibbler_server", "dibbler_client", "isc_dhcp4_server", "isc_dhcp6_server", \
                         "kea4_server", "kea4_server_bind", "kea6_server", "kea6_server_bind", "kea6_mini_server", \
                         "none_server"

        # no_server_management value can be set by -N option on startup to turn off remote server management
        self.no_server_management = False
        self.empty = ""
        self.white_space = " "
        self.none = None
        # FORGE
        self.mgmt_address = MGMT_ADDRESS
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

        # DHCP
        self.proto = PROTO
        self.software_under_test = SOFTWARE_UNDER_TEST
        self.software_install_path = SOFTWARE_INSTALL_PATH
        # TODO remove trailing / if there is some
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
        self.dns_addr = DNS_ADDR
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
        import fcntl, socket, struct, sys
        if sys.platform != "darwin":
            s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
            info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname))
            return ':'.join(['%02x' % ord(char) for char in info[18:24]])
        else:
            # TODO fix this for MAC OS, this is temporary quick fix just for my local system
            return "0a:00:27:00:00:00"

    def basic_validation(self):
        from sys import exit
        if self.proto not in ["v4", "v6"]:
            print "Configuration failure, protocol version not set properly." \
                  " Please use ./forge.py -T to validate configuration."
            exit(-1)
        if self.proto == "v4" and self.software_under_test[0] not in ["none_server"]:
            if "4" not in self.software_under_test[0]:
                print "Miss match of protocol version and DHCP server version"
                exit(-1)
        if self.proto == "v6" and self.software_under_test[0] not in ["none_server"]:
            if "6" not in self.software_under_test[0]:
                print "Miss match of protocol version and DHCP server version"
                exit(-1)
        if self.software_install_path == "":
            print "Configuration failure, software_install_path empty." \
                  " Please use ./forge.py -T to validate configuration."
            exit(-1)
        if self.mgmt_address == "":
            print "Configuration failure, mgmt_address empty. Please use ./forge.py -T to validate configuration."
            exit(-1)

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

    # def test_remote_location(self):
    #     """
    #     Check if Forge can connect to configured location
    #     :return:
    #     """
    #     from softwaresupport.multi_server_functions import fabric_run_command
    #     result = fabric_run_command("ls -la")
    #
    # def test_addresses(self):
    #     """
    #     Ping to all configured addresses
    #     :return:
    #     """
    #     # TODO develop this one
    #     pass
    #
    # def check_remote_path(self):
    #     """
    #     Check if somftware under test is indeed installed
    #     :return:
    #     """
    #     from softwaresupport.multi_server_functions import fabric_run_command
    #     if "kea" in self.software_under_test:
    #         result = fabric_run_command('(' + self.software_install_path + 'sbin/keactrl status')
    #     elif "isc_dhcp" in self.software_under_test:
    #         result = fabric_run_command('ls -la ' + self.software_install_path + 'sbin/dhcpd')
    #     else:
    #         result = True
    #
    # def test_priviledges(self):
    #     """
    #     Test priviledges on remote location
    #     :return:
    #     """
    #     # TODO develop this one
    #     from softwaresupport.multi_server_functions import fabric_sudo_command
    #     result = fabric_sudo_command("ls -la")
    #
    #     pass
    #
    # def test_database(self):
    #     """
    #     Test if non-memfile database is reachable
    #     :return:
    #     """
    #     # TODO develop this one
    #     if self.db_type == "memfile":
    #         print "Checking database ommitted: db_type is memfile"
    #         return 0
    #     else:
    #         print "!TODO"
    #         return 0


def option_parser():
    desc = '''
    Forge - Testing environment. For more information please run help.py to generate UserHelp.txt
    '''
    parser = optparse.OptionParser(description=desc, usage="%prog or type %prog -h (--help) for help")
    parser.add_option("-4", "--version4",
                      dest="version4",
                      action="store_true",
                      default=False,
                      help='Declare IP version 4 tests')

    parser.add_option("-6", "--version6",
                      dest="version6",
                      action="store_true",
                      default=False,
                      help="Declare IP version 6 tests")

    parser.add_option("-v", "--verbosity",
                      dest="verbosity",
                      type="int",
                      action="store",
                      default=4,
                      help="Level of the lettuce verbosity")

    parser.add_option("-l", "--list",
                      dest="list",
                      action="store_true",
                      default=False,
                      help='List all features (test sets) please choose also IP version')

    parser.add_option("-s", "--test_set",
                      dest="test_set",
                      action="store",
                      default=None,
                      help="Specific tests sets")

    parser.add_option("-n", "--name",
                      dest="name",
                      default=None,
                      help="Single scenario name, don't use that option with -s or -t")

    parser.add_option("-t", "--tags",
                      dest="tag",
                      action="append",
                      default=None,
                      help="Specific tests tags, multiple tags after ',' e.g. -t v6,basic." +
                      "If you wont specify any tags, Forge will perform all test for chosen IP version." +
                      "Also if you want to skip some tests use minus sing before that test tag (e.g. -kea).")

    parser.add_option("-x", "--with-xunit",
                      dest="enable_xunit",
                      action="store_true",
                      default=False,
                      help="Generate results file in xUnit format")

    parser.add_option("-p", "--explicit-path",
                      dest="explicit_path",
                      default=None,
                      help="Search path, relative to <forge>/lettuce/features for tests regardless of SUT or protocol")

    parser.add_option("-T", "--test-configuration",
                      dest="test_config",
                      action="store_true",
                      default=False,
                      help="Run basic tests on current configuration and exit.")

    parser.add_option("-N", "--no-server-actions",
                      dest="noserver",
                      action="store_true",
                      default=False,
                      help="Run test without remote server management.")

    (opts, args) = parser.parse_args()

    if opts.test_config:
        from features.init_all import ForgeConfiguration
        f_config = ForgeConfiguration()
        print f_config.__dict__
        f_config.test_addresses()
        f_config.test_remote_location()
        f_config.test_priviledges()
        f_config.test_database()
        sys.exit(-1)

    tag = ""
    if opts.tag is not None:
        tag = opts.tag[0].split(',')

    if not opts.version6 and not opts.version4:
        parser.print_help()
        parser.error("You must choose between -4 or -6.\n")

    if opts.version6 and opts.version4:
        parser.print_help()
        parser.error("options -4 and -6 are exclusive.\n")

    number = '6' if opts.version6 else '4'
    # Generate list of set tests and exit
    if opts.list:
        from help import UserHelp
        hlp = UserHelp()
        hlp.test(number, 0)
        sys.exit(-1)

    return number, opts.test_set, opts.name, opts.verbosity, tag, opts.enable_xunit, opts.explicit_path, opts.noserver


def test_path_select(number, test_set, name, explicit_path):
    # path for tests, all for specified IP version or only one set
    scenario = None
    from features.init_all import SOFTWARE_UNDER_TEST
    testType = ""
    for each in SOFTWARE_UNDER_TEST:
        if "client" in each:
            testType = "client"
        elif "server" in each:
            testType = "server"
        else:
            print "Are you sure that variable SOFTWARE_UNDER_TEST is correct?"
            sys.exit(-1)

    if explicit_path is not None:
        # Test search path will be <forge>/letttuce/features/<explicit_path/
        # without regard to SUT or protocol.  Can be used with -n to run
        # specific scenarios.
        base_path = os.getcwd() + "/features/" + explicit_path + "/"
        if name is not None:
            from help import find_scenario_in_path
            base_path, scenario = find_scenario_in_path(name, base_path)
            if base_path is None:
                print "Scenario named %s has been not found" % name
                sys.exit(-1)
    elif test_set is not None:
        path = "/features/dhcpv" + number + "/" + testType + "/" + test_set + "/"
        base_path = os.getcwd() + path
    elif name is not None:
        from help import find_scenario
        base_path, scenario = find_scenario(name, number)
        if base_path is None:
            print "Scenario named %s has been not found" % name
            sys.exit(-1)
    else:
        scenario = None
        path = "/features/dhcpv" + number + "/" + testType + "/"
        base_path = os.getcwd() + path

    return base_path, scenario


def check_config_file():
    try:
        importlib.import_module("features.init_all")
    except ImportError:
        print "\n Error: You need to create 'init_all.py' file with configuration! (example file: init_all.py_example)\n"
        # option_parser().print_help()
        sys.exit(-1)


def start_all(base_path, verbosity, scenario, tag, enable_xunit):

    from features.init_all import HISTORY
    if HISTORY:
        from help import TestHistory
        history = TestHistory()
        history.start()

    # lettuce starter, adding options
    try:
        from lettuce import Runner, world
    except ImportError:
        print "You have not Lettuce installed (or in path)."
        sys.exit(-1)

    runner = Runner(base_path,
                    verbosity=verbosity,
                    scenarios=scenario,
                    failfast=False,
                    tags=tag,
                    enable_xunit=enable_xunit)

    result = runner.run()  # start lettuce

    if HISTORY:
        history.information(result.scenarios_passed, result.scenarios_ran, tag, base_path)
        history.build_report()

    return result.scenarios_ran - result.scenarios_passed


if __name__ == '__main__':
    number, test_set, name, verbosity, tag, enable_xunit, explicit_path, server_management = option_parser()
    check_config_file()
    base_path, scenario = test_path_select(number, test_set, name, explicit_path)
    from lettuce import world

    world.f_cfg = ForgeConfiguration()
    if server_management:
        world.f_cfg.no_server_management = True
    failed = start_all(base_path, verbosity, scenario, tag, enable_xunit)
    if failed > 0:
        print "SCENARIOS FAILED: %d" % failed
        sys.exit(1)
    sys.exit(0)
