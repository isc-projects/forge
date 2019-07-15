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
import cgitb

import init_all

# all settings and their default values, if value is None then it is required
SETTINGS = {
    'SOFTWARE_INSTALL_PATH': '/usr/local',
    'INSTALL_METHOD': 'make',
    'LOGLEVEL': 'info',
    'SOFTWARE_UNDER_TEST': ('kea4_server', 'bind9_server'),
    'SHOW_PACKETS_FROM': 'both',
    'SRV4_ADDR': None,
    'REL4_ADDR': "0.0.0.0",
    'GIADDR4': None,
    'IFACE': None,
    'CLI_LINK_LOCAL': None,
    'SERVER_IFACE': None,
    'OUTPUT_WAIT_INTERVAL': 1,
    'OUTPUT_WAIT_MAX_INTERVALS': 2,
    'PACKET_WAIT_INTERVAL': 1,
    'SRV_IPV6_ADDR_GLOBAL': '3000::1000',
    'SRV_IPV6_ADDR_LINK_LOCAL': 'fe80::a00:27ff:fedf:63bc',
    'HISTORY': True,
    'TCPDUMP': True,
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
    'SAVE_LOGS': True,
    'BIND_LOG_TYPE': 'INFO',
    'BIND_LOG_LVL': 0,
    'BIND_MODULE': '',
    'SAVE_LEASES': True,
    'DNS_IFACE': None,
    'DNS4_ADDR': None,
    'DNS6_ADDR': None,
    'DNS_PORT': 53,
    'DNS_SERVER_INSTALL_PATH': '/opt/bind/sbin',
    'DNS_DATA_PATH': '/opt/bind/data',
    'ISC_DHCP_LOG_FACILITY': 'local7',
    'ISC_DHCP_LOG_FILE': '/var/log/forge_dhcpd.log',
    'DB_TYPE': 'memfile',
    'DB_NAME': 'keadb',
    'DB_USER': 'keauser',
    'DB_PASSWD': 'keapass',
    'DB_HOST': '',
    'CIADDR': None,
    'FABRIC_PTY': False,
    'DISABLE_DB_SETUP': False,
}


class ForgeConfiguration:
    def __init__(self):
        # default
        self.dns_used = ["bind9_server"]
        self.dhcp_used = ["dibbler_server", "dibbler_client", "isc_dhcp4_server", "isc_dhcp6_server",
                          "kea4_server", "kea4_server_bind", "kea6_server", "kea6_server_bind", "kea6_mini_server",
                          "none_server"]

        self._load_settings()

        # no_server_management value can be set by -N option on startup to turn off remote server management
        self.no_server_management = False
        self.empty = ""
        self.white_space = " "
        self.none = None

        self.multiple_tested_servers = [self.mgmt_address]

        self.proto = 'v4'  # default value but it is overriden by each test in terrain.declare_all()

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

        self.cli_mac = self.gethwaddr(self.iface)

        # used defined variables
        self.user_variables_temp = []

        # basic validation of configuration
        self.basic_validation()

    def _load_settings(self):
        for key, default_value in SETTINGS.items():
            if hasattr(init_all, key):
                value = getattr(init_all, key)
            else:
                if default_value is None:
                    raise Exception('Cannot find %s in init_all.py' % key)
                value = default_value
            value = os.getenv(key, value)
            setattr(self, key.lower(), value)

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

    def data_join(self, sub_path):
        if self.install_method == 'make':
            return os.path.join(self.software_install_path, 'var/lib/kea', sub_path)
        else:
            return os.path.join('/var/lib/kea', sub_path)

    def log_join(self, sub_path):
        if self.install_method == 'make':
            return os.path.join(self.software_install_path, 'var/log', sub_path)
        else:
            return os.path.join('/var/log/kea', sub_path)

    def etc_join(self, sub_path):
        if self.install_method == 'make':
            return os.path.join(self.software_install_path, 'etc/kea', sub_path)
        else:
            return os.path.join('/etc/kea', sub_path)

    def get_dhcp_conf_path(self):
        if self.install_method == 'make':
            return os.path.join(self.software_install_path, 'etc/kea/kea.conf')
        else:
            return '/etc/kea/kea-dhcp%s.conf' % world.proto[1]

    def sbin_join(self, sub_path):
        if self.install_method == 'make':
            return os.path.join(self.software_install_path, 'sbin', sub_path)
        else:
            return os.path.join('/usr/sbin', sub_path)

    def hooks_join(self, sub_path):
        if self.install_method == 'make':
            return os.path.join(self.software_install_path, 'lib/kea/hooks', sub_path)
        else:
            return os.path.join('/usr/lib/x86_64-linux-gnu/kea/hooks', sub_path)

    def run_join(self, sub_path):
        if self.install_method == 'make':
            return os.path.join(self.software_install_path, 'var/run/kea', sub_path)
        else:
            return os.path.join('/run/kea', sub_path)

    def tmp_join(self, sub_path):
        return os.path.join('/tmp', sub_path)

    def get_leases_path(self, proto=None):
        if not proto:
            proto = world.proto

        return self.data_join('kea-leases%s.csv' % proto[1])




# global object that stores all needed data: configs, etc.
world = threading.local()
world.f_cfg = ForgeConfiguration()


def _conv_arg_to_txt(arg):
    if isinstance(arg, basestring):
        return "'%s'" % arg
    else:
        return str(arg)

# stub that replaces lettuce step decorator
def step(pattern):
    def wrap(func):
        def wrapped_func(*args, **kwargs):
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
            except:
                txt = cgitb.text(sys.exc_info())
                with open(fout, 'a') as f:
                    f.write(txt)
                raise
        return wrapped_func
    return wrap
