#Configuration file, please copy this to the init_all.py and fill it with your
#variables. init_all.py is added to gitignore.

# All configurations are separated to different sections:
# general - for general Forge configuration ;)
# ssh - for ssh connection between virtual machines
# kea - for kea configuration
# ISC-DHCP - for ISC-DHCP configurations

DNS = "bind9_server",
DHCP = "dibbler_server", "dibbler_client", "isc_dhcp4_server", "isc_dhcp6_server",\
       "kea4_server", "kea4_server_bind", "kea6_server", "kea6_server_bind"


# =============== GENERAL ===============
# This defines the logging level for the common logger used by this framework
# Possible values are CRITICAL, ERROR, WARNING, INFO and DEBUG and they are
# case insensitive.
LOGLEVEL = "info"

# This defines server type. Allowed values are:
# kea4, kea6, isc_dhcp4, isc_dhcp6, dibbler
# Not all of those are functional yet. This is essentailly
# name of the subdirectory in lettuce/features/serversupport
#SERVER_TYPE = "kea6"
SOFTWARE_UNDER_TEST = ("kea4_server", "kea6_server", "bind9_server"),

# This defines protocol family. Currently two are
# supported: v4 (which means DHCPv4) and v6 (which means DHCPv6)
PROTO = ""

# Parameters specific to DHCPv4 tests
SRV4_ADDR = "192.168.50.252"
REL4_ADDR = ""
GIADDR4 = "192.168.50.249"
CIADDR = "192.168.50.253"
# defines client MAC (used for DUID generation)
CLI_MAC = "00:01:02:03:04:05"
CLI_LINK_LOCAL="fe80::250:56ff:fe87:28b6"

SLEEP_TIME_1=2
SLEEP_TIME_2=2
# For all servers, choose ethernet interface on which server will be configured
SERVER_IFACE = "ens224"
# In order to make sure we start all tests with a 'clean' environment,
# We perform a number of initialization steps, like restoring configuration
# files, and removing generated data files.

# This approach may not scale; if so we should probably provide specific
# initialization steps for scenarios. But until that is shown to be a problem,
# It will keep the scenarios cleaner.

# This is a list of files that are freshly copied before each scenario
# The first element is the original, the second is the target that will be
# used by the tests that need them
copylist = [ ]

# This is a list of files that, if present, will be removed before each scenario
removelist = [ ]

# When waiting for output data of a running process, use OUTPUT_WAIT_INTERVAL
# as the interval in which to check again if it has not been found yet.
# If we have waited OUTPUT_WAIT_MAX_INTERVALS times, we will abort with an
# error (so as not to hang indefinitely). Values are counted in seconds.
OUTPUT_WAIT_INTERVAL = 3
OUTPUT_WAIT_MAX_INTERVALS = 5

# scope link server address for testing unicast messages
SRV_IPV6_ADDR_GLOBAL = "3000::"
SRV_IPV6_ADDR_LINK_LOCAL = "fe80::250:56ff:fe87:8c8"

# Defines name of the DUT-facing network interface
IFACE = "ens224"

# If you wont to build tests history in history.html set HISTORY on True if not, on False
# but for more detailed information about tests, use --with_xunit option when starting run_test.py
HISTORY = False

# Also you can save separate .pcap file of every test. In default it's disabled
# If you recieve error tcpdump: <file name>: Permission denied
# please use command as a root: aa-complain /usr/sbin/tcpdump
TCPDUMP = True

# If your tcpdump is installed in different location place that in TCPDUMP_INSTALL_DIR
# otherwise leave it blank
TCPDUMP_INSTALL_DIR = "/usr/sbin/"
TCPDUMP_PATH = TCPDUMP_INSTALL_DIR
# Also we can decide to keep main configuration file in tests_results.
SAVE_CONFIG_FILE = True
AUTO_ARCHIVE = False

# =============== SSH ===============

# This are required management information about device under test (the one that
# tested server will be running on) root privileges are required! So edit sudoers
# file, or use root account.
# ip address and port. ssh port default 22
MGMT_ADDRESS = "149.20.57.198"
MGMT_ADDRESS_2 = "149.20.57.203"
MGMT_ADDRESS_3 = ""
MGMT_USERNAME = "test"
MGMT_PASSWORD = "test&0"


# =============== Kea ===============
# Specifies path to the server installation directory on DUT. This must
# point to root directory of server installation and must end with /.
# The framework appends subdirectories to this path to run applications.
# For example, it appends "bin/" to obtain path to the bindctl.
SOFTWARE_INSTALL_DIR = "/home/test/jenkins_lab/var/area_A/"
SOFTWARE_INSTALL_PATH = SOFTWARE_INSTALL_DIR
# Copy logs file, different file for each test.
# WARRNING: this produce really big amount of data!
# Default - False
SAVE_BIND_LOGS = True

# Also we can decide which logging type choose, logging lvl,
# and BIND10 module type
# for more accurate information plz read BIND10 documentation: Chapter 21. Logging
BIND_LOG_TYPE = "DEBUG"
BIND_LOG_LVL = 99
BIND_MODULE = "*"

# =============== DIBBLER ================
DIBBLER_INSTALL_DIR = ""
SAVE_LEASES = True


#other
PACKET_WAIT_INTERVAL = 1
SAVE_LOGS = "True"
# ============ DNS ============
DNS_IFACE = "ens224"
DNS4_ADDR = "192.168.50.252"
DNS6_ADDR = "2001:db8:1::1000"
DNS_PORT = 53
DNS_SERVER_INSTALL_DIR = "/usr/sbin/"
DNS_SERVER_INSTALL_PATH = "/usr/sbin/"
FABRIC_PTY=False
DNS_DATA_DIR = "/home/test/dns/"
DNS_DATA_PATH = "/home/test/dns/"

ISC_DHCP_LOG_FACILITY = "local7"
ISC_DHCP_LOG_FILE = "/var/log/forge_dhcpd.log"

SHOW_PACKETS_FROM = ""


# Backend type: postgresql
DB_TYPE = ""

# Data base name:
DB_NAME = "kea"

# User name for databased named DB_NAME
DB_USER = "kea"

# Password for user DB_USER:
DB_PASSWD = "kea"

# Host address where is our data base, most likely it will be 'localhost'
DB_HOST = "localhost"

EMPTY=""
NONE=None
