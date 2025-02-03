#!/usr/bin/env python3

# Copyright (C) 2013-2024 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Wlodzimierz Wencel

# pylint: disable=access-member-before-definition
# pylint: disable=consider-using-f-string
# pylint: disable=c-extension-no-member
# pylint: disable=import-error
# pylint: disable=invalid-name
# pylint: disable=no-else-return
# pylint: disable=no-member
# pylint: disable=too-many-instance-attributes
# pylint: disable=unspecified-encoding
# pylint: disable=unused-argument

import os
import threading
import fcntl
import socket
import struct
# [B404:blacklist] Consider possible security implications associated with the subprocess module.
import subprocess  # nosec B404
import sys
import traceback
import netifaces

import init_all

# all settings and their default values, if value is None then it is required
SETTINGS = {
    'SOFTWARE_INSTALL_PATH': '/usr/local',
    'INSTALL_METHOD': 'make',
    'LOGLEVEL': 'info',
    'SOFTWARE_UNDER_TEST': ('kea4_server', 'bind9_server'),
    'SHOW_PACKETS_FROM': 'both',
    'SRV4_ADDR': None,
    'SRV4_ADDR_2': '',
    'REL4_ADDR': '0.0.0.0',
    'GIADDR4': None,
    'IFACE': None,
    'IFACE2': '',
    'CLI_LINK_LOCAL': '',
    'CLI_LINK_LOCAL2': '',
    'CLIENT_IPV6_ADDR_GLOBAL': '',
    'SERVER_IFACE': None,
    'SERVER_IFACE2': '',
    'SERVER2_IFACE': '',
    'SERVER3_IFACE': '',
    'OUTPUT_WAIT_INTERVAL': 1,
    'OUTPUT_WAIT_MAX_INTERVALS': 2,
    'PACKET_WAIT_INTERVAL': 1,
    'HA_PACKET_WAIT_INTERVAL_FACTOR': 4,
    'RADIUS_PACKET_WAIT_INTERVAL_FACTOR': 4,
    'SRV_IPV6_ADDR_GLOBAL': '3000::1000',
    'SRV_IPV6_ADDR_LINK_LOCAL': 'fe80::a00:27ff:fedf:63bc',
    'HISTORY': True,
    'TCPDUMP': True,
    'TCPDUMP_ON_REMOTE_SYSTEM': False,
    'TCPDUMP_PATH': '',
    'SAVE_CONFIG_FILE': True,
    'AUTO_ARCHIVE': False,
    'SLEEP_TIME_1': 1,
    'SLEEP_TIME_2': 2,
    'MGMT_ADDRESS': None,
    'MGMT_ADDRESS_2': '',
    'MGMT_ADDRESS_3': '',
    'MGMT_USERNAME': None,
    'MGMT_PASSWORD': None,
    'MGMT_PASSWORD_CMD': '',
    'SAVE_LOGS': True,
    'BIND_LOG_TYPE': 'INFO',
    'BIND_LOG_LVL': 0,
    'BIND_MODULE': '',
    'SAVE_LEASES': True,
    'DNS_IFACE': None,
    'DNS4_ADDR': None,
    'DNS6_ADDR': None,
    'WIN_DNS_ADDR': '',
    'DNS_PORT': 53,
    'DNS_SERVER_INSTALL_PATH': '/opt/bind/sbin',
    'DNS_DATA_PATH': '/opt/bind/data',
    'DB_TYPE': 'memfile',
    'DB_NAME': 'keadb',
    'DB_USER': 'keauser',
    'DB_PASSWD': 'keapass',
    'DB_HOST': '',
    'CIADDR': None,
    'FABRIC_PTY': False,
    'DNS_RETRY': 6,
    'DISABLE_DB_SETUP': False,
    'WIN_DNS_ADDR_2016': '',
    'WIN_DNS_ADDR_2019': '',
    'FORGE_VERBOSE': True
}


class ForgeConfiguration:
    def __init__(self):
        # default
        self.dns_used = ["bind9_server"]
        self.dhcp_used = ["kea4_server", "kea6_server", "none_server", "isc_dhcp4_server", "isc_dhcp6_server"]
        self.mgmt_address = None  # will be reconfigured, added to keep pycodestyle quiet
        self.mgmt_address_2 = None
        self.mgmt_address_3 = None

        self._determine_mgmt_password()

        self._load_settings()

        # no_server_management value can be set by -N option on startup to turn off remote server management
        self.no_server_management = False
        self.empty = ""
        self.white_space = " "
        self.none = None

        self.multiple_tested_servers = [self.mgmt_address]

        self.proto = 'v4'  # default value but it is overriden by each test in terrain.declare_all()

        # change this at the beginning of the test and we have
        # easy comparison between single and multi, or use as fixture
        self.multi_threading_enabled = True

        # value of --with-ca pytest option determines if control agent is used, by default CA is not used
        self.control_agent = ''

        if self.install_method == 'native':
            self.software_install_path = '/usr'

        # fields for restoring that can be overwritten by tests (TODO: WTF?)
        self.db_type_bk = self.db_type
        self.db_host_bk = self.db_host
        self.db_name_bk = self.db_name
        self.db_passwd_bk = self.db_passwd
        self.db_user_bk = self.db_user

        # backward compatibility
        self.gia4_addr = self.giaddr4
        self.software_install_dir = self.software_install_path
        self.isc_dhcp_log_file = "/var/log/dhcpd_forge.log"
        # add line:
        # local7.debug	/var/log/dhcpd_forge.log
        # to file /etc/rsyslog.conf and restart rsyslog
        self.isc_dhcp_log_facility = "local7"
        try:
            self.cli_mac = self.gethwaddr(self.iface)
        except BaseException:
            # Print an error message because the raised exception message
            # itself is too cryptic.
            print("ERROR: Could not get hardware address from interface '%s'." % self.iface)
            raise

        # get client link-local if empty
        if self.cli_link_local == '':
            addrs = netifaces.ifaddresses(self.iface)
            if netifaces.AF_INET6 not in addrs:
                raise Exception("ERROR: IPv6 is required on interface '%s'." % self.iface)
            addrs6 = addrs[netifaces.AF_INET6]
            for addr in addrs6:
                addr = addr['addr']
                if '%' in addr:
                    addr = addr.split('%')[0]
                if addr.startswith('fe80'):
                    self.cli_link_local = addr
                    break

        if self.cli_link_local2 == '' and self.iface2 != '':
            addrs = netifaces.ifaddresses(self.iface2)
            if netifaces.AF_INET6 not in addrs:
                raise Exception("ERROR: IPv6 is required on interface '%s'." % self.iface2)
            addrs6 = addrs[netifaces.AF_INET6]
            for addr in addrs6:
                addr = addr['addr']
                if '%' in addr:
                    addr = addr.split('%')[0]
                if addr.startswith('fe80'):
                    self.cli_link_local2 = addr
                    break
        # it could be simplified but let's keep it completely separate from cli_link_local
        # address detection
        if self.client_ipv6_addr_global == '':
            addrs = netifaces.ifaddresses(self.iface)
            if netifaces.AF_INET6 not in addrs:
                raise Exception("ERROR: IPv6 is required on interface '%s'." % self.iface)
            addrs6 = addrs[netifaces.AF_INET6]
            for addr in addrs6:
                addr = addr['addr']
                if 'fe80::' not in addr:
                    self.client_ipv6_addr_global = addr
                    break

        # used defined variables
        self.user_variables_temp = []

        # basic validation of configuration
        self.basic_validation()

    def _determine_mgmt_password(self):
        """_determine_mgmt_password Determine mgmt password.
        """
        if not hasattr(self, "mgmt_password_cmd") or self.mgmt_password_cmd is None or len(self.mgmt_password_cmd) == 0:
            return
        with subprocess.Popen(self.mgmt_password_cmd, shell=True, stdout=subprocess.PIPE) as pipe:
            output, _ = pipe.communicate()
            assert pipe.returncode == 0
            self.mgmt_password = output.decode('utf-8').strip()

    def _load_settings(self):
        """_load_settings Load settings from init_all.py.

        :raises Exception: if a mandatory parameter is missing
        """
        # Take configuration parameters from init_all.py.
        for key, default_value in SETTINGS.items():
            if hasattr(init_all, key):
                value = getattr(init_all, key)
            else:
                value = default_value
            value = os.getenv(key, value)
            print(f"setting {key.lower()} = {value}")  # TODO turn it into forge parameter like --debug
            setattr(self, key.lower(), value)

        # Check if mgmt_password can be determined from mgmt_password_cmd.
        self._determine_mgmt_password()

        # Complain about missing mandatory parameters.
        for key, default_value in SETTINGS.items():
            if hasattr(self, key):
                if getattr(self, key) is None:
                    raise Exception(f'{key} is mandatory in init_all.py. '
                                    'It should have a value and it should not be None.')

    def gethwaddr(self, ifname):
        """gethwaddr Get hardware address of interface.

        :param ifname: interface name
        :type ifname: str
        :return: hardware address
        :rtype: str
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', bytes(ifname, 'utf-8')[:15]))
        s.close()
        return ':'.join('%02x' % b for b in info[18:24])

    def basic_validation(self):
        """basic_validation Basic validation of configuration.
        """
        if self.software_install_path == "":
            print("Configuration failure, software_install_path is empty. "
                  "Please use ./src/forge_cfg.py -T to validate configuration.")
            sys.exit(-1)
        if self.mgmt_address == "":
            print("Configuration failure, mgmt_address is empty. "
                  "Please use ./src/forge_cfg.py -T to validate configuration.")
            sys.exit(-1)

    def set_env_val(self, env_name, env_val):
        """set_env_val Set environment variable.

        :param env_name: environment variable name
        :type env_name: str
        :param env_val: environment variable value
        :type env_val: str
        """
        os.putenv(env_name, env_val)

    def data_join(self, sub_path):
        """data_join Get path to var/lib/kea directory.

        :param sub_path: subpath to join
        :type sub_path: str
        :return: path to var/lib/kea directory
        :rtype: str
        """
        if self.install_method == 'make':
            return os.path.join(self.software_install_path, 'var/lib/kea', sub_path)
        else:
            return os.path.join('/var/lib/kea', sub_path)

    def log_join(self, sub_path):
        """log_join Get path to var/log directory.

        :param sub_path: subpath to join
        :type sub_path: str
        :return: path to var/log directory
        :rtype: str
        """
        if self.install_method == 'make':
            return os.path.join(self.software_install_path, 'var/log', sub_path)
        else:
            return os.path.join('/var/log/kea', sub_path)

    def etc_join(self, sub_path):
        """etc_join Get path to etc/kea directory.

        :param sub_path: subpath to join
        :type sub_path: str
        :return: path to etc/kea directory
        :rtype: str
        """
        if self.install_method == 'make':
            return os.path.join(self.software_install_path, 'etc/kea', sub_path)
        else:
            return os.path.join('/etc/kea', sub_path)

    def get_dhcp_conf_path(self):
        """get_dhcp_conf_path Get path to kea-dhcp{proto}.conf file.

        :return: path to kea-dhcp{proto}.conf file
        :rtype: str
        """
        if self.install_method == 'make':
            return os.path.join(self.software_install_path, f'etc/kea/kea-dhcp{world.proto[1]}.conf')
        else:
            return f'/etc/kea/kea-dhcp{world.proto[1]}.conf'

    def sbin_join(self, sub_path):
        """sbin_join Get path to sbin directory.

        :param sub_path: subpath to join
        :type sub_path: str
        :return: path to sbin directory
        :rtype: str
        """
        if self.install_method == 'make':
            return os.path.join(self.software_install_path, 'sbin', sub_path)
        else:
            return os.path.join('/usr/sbin', sub_path)

    def hooks_join(self, sub_path):
        """hooks_join Get path to lib/kea/hooks directory. Path differ between systems.

        :param sub_path: subpath to join
        :type sub_path: str
        :return: path to lib/kea/hooks directory
        :rtype: str
        """
        if self.install_method == 'make':
            return os.path.join(self.software_install_path, 'lib/kea/hooks', sub_path)
        else:
            if world.server_system == 'redhat':
                return os.path.join('/usr/lib64/kea/hooks', sub_path)
            if world.server_system == 'alpine':
                return os.path.join('/usr/lib/kea/hooks', sub_path)
            return os.path.join(f'/usr/lib/{world.server_architecture}-linux-gnu/kea/hooks', sub_path)

    def run_join(self, sub_path):
        """run_join Get path to run/kea directory.

        :param sub_path: subpath to join
        :type sub_path: str
        :return: path to run/kea directory
        :rtype: str
        """
        if self.install_method == 'make':
            return os.path.join(self.software_install_path, 'var/run/kea', sub_path)
        else:
            return os.path.join('/run/kea', sub_path)

    def get_share_path(self):
        """get_share_path Get path to share/kea directory.

        :return: path to share directory
        :rtype: str
        """
        if self.install_method == 'make':
            return os.path.join(self.software_install_path, 'share/kea')
        else:
            return '/usr/share/kea'

    @staticmethod
    def tmp_join(sub_path):
        """tmp_join Get path to temporary directory.

        :param sub_path: subpath to join
        :type sub_path: str
        :return: path to temporary directory
        :rtype: str
        """
        return os.path.join('/tmp', sub_path)

    def get_leases_path(self, proto=None):
        """get_leases_path Get path to leases file.

        :param proto: protocol version, defaults to None
        :type proto: str, optional
        :return: path to leases file
        :rtype: str
        """
        if not proto:
            proto = world.proto

        return self.data_join('kea-leases%s.csv' % proto[1])


def get_test_progress():
    """
    Returns a textual representation of the total test progress e.g. '#8/24'.
    Before running the first test, it's always just '#1'.
    :return: textual representation of the total test progress
    :rtype: str
    """
    result = f'#{world.current_test_index}'
    if world.test_count != 0:
        result += f'/{world.test_count}'
    return result


# global object that stores all needed data: configs, etc.
world = threading.local()
world.f_cfg = ForgeConfiguration()
world.current_test_index = 1
world.test_count = 0
world.get_test_progress = get_test_progress


def _conv_arg_to_txt(arg):
    """convert argument to string

    :param arg: argument to convert
    :type arg: any
    :return: string representation of argument
    :rtype: str
    """
    if isinstance(arg, str):
        return "'%s'" % arg
    else:
        return str(arg)


def step(pattern):
    """step replaces lettuce step decorator

    :param pattern: pattern to match
    :type pattern: str
    :return: wrapped function
    :rtype: function
    """
    def wrap(func):
        """wrap replaces lettuce wrap decorator

        :param func: function to wrap
        :type func: function
        :return: wrapped function
        :rtype: function
        """
        def wrapped_func(*args, **kwargs):
            """wrapped_func replaces lettuce wrapped_func

            :param args: arguments
            :type args: tuple
            :param kwargs: keyword arguments
            :type kwargs: dict
            :return: result of the wrapped function
            :rtype: any
            """
            txt = func.__name__ + '('
            txt_args = ", ".join([_conv_arg_to_txt(a) for a in args])
            txt_kwargs = ", ".join(['%s=%s' % (str(k), _conv_arg_to_txt(v)) for k, v in kwargs.items()])
            if txt_args:
                txt += txt_args
                if txt_kwargs:
                    txt += ', '
            if txt_kwargs:
                txt += txt_kwargs
            txt += ')\n'

            fout = os.path.join(world.cfg["test_result_dir"], 'test-steps.txt')
            with open(fout, 'a') as f:
                f.write(txt)

            try:
                return func(*args, **kwargs)
            except BaseException:
                txt = traceback.format_exc()
                with open(fout, 'a') as f:
                    f.write(txt)
                raise
        return wrapped_func
    return wrap
