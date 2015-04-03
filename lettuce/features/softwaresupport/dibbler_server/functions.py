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


from softwaresupport.multi_server_functions import fabric_run_command, fabric_send_file, remove_local_file
from logging_facility import *
from lettuce.registry import world
from init_all import SERVER_INSTALL_DIR, SERVER_IFACE


def restart_srv():
    fabric_run_command("("+SERVER_INSTALL_DIR+"sbin/dibbler-server restart); sleep 1;")


def stop_srv(value = False):
    #pass
    fabric_run_command("("+SERVER_INSTALL_DIR+"sbin/dibbler-server stop); sleep 1;", value)


def prepare_cfg_default(step):
    world.cfg["conf"] = "# This is Forge generated config file.\n"
    

def add_defaults(rebinding_time = '1400', renewal_time = '10', preferred_lifetime = '1000',
                 lease_time = '2000', max_lease_time = '2000'):
    eth = SERVER_IFACE
    pointer_open = '{'
    pointer_close = '}'

    world.cfg["conf"] += '''
iface "{eth}" {pointer_open}
    '''.format(**locals())


def prepare_cfg_subnet(step, subnet, pool):
    get_common_logger().debug("Configure subnet...")
    if not "conf" in world.cfg:
        world.cfg["conf"] = ""
    if subnet == "default":
        subnet = "2001:db8:1::/64"
    if pool == "default":
        pool = "2001:db8:1::0-2001:db8:1::ffff"

    eth = SERVER_IFACE
    world.cfg["subnet"] = subnet
    add_defaults()  # add in future configuration of those functions
    pointer_open = '{'
    pointer_close = '}'
    world.cfg["conf"] += '''\
# subnet defintion
  class {pointer_open}
   T1 1800
   T2 2700
   prefered-lifetime 3600
   valid-lifetime 7200
   pool {pool}

    {pointer_close}
        '''.format(**locals())


#still not implemented
dibbler_options6 = {"client-id": 1,
                 "server-id": 2,
                 "IA_NA": 3,
                 "IN_TA": 4,
                 "IA_address": 5,
                 "preference": 7,
                 "relay-msg": 9,
                 "status-code": 13,
                 "rapid_commit": 14,
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
                 "information-refresh-time": 32
                    }


def prepare_cfg_add_option(step, option_name, option_value):
    if not "conf" in world.cfg:
        world.cfg["conf"] = ""

    world.dhcp["option_cnt"] = world.dhcp["option_cnt"] + 1


def prepare_cfg_add_custom_option(step, opt_name, opt_code, opt_type, opt_value):
    pass


def prepare_cfg_add_option_subnet(step, option_name, subnet, option_value):
    if not "conf" in world.cfg:
        world.cfg["conf"] = ""

    assert option_name in dibbler_options6, "Unsupported option name " + option_name
    option_code = dibbler_options6.get(option_name)


def cfg_write():
    cfg_file = open(world.cfg["cfg_file"], 'w')
    cfg_file.write(world.cfg["conf"])
    cfg_file.write('}')#add last } for closing file
    cfg_file.close()


def start_srv(a, b):
    """
    Start ISC-DHCPv6 with generated config.
    """
    cfg_write() 
    stop_srv()
    get_common_logger().debug("Starting Dibbler with generated config:")
    fabric_send_file(world.cfg["cfg_file"], '/etc/dibbler/server.conf')
    remove_local_file(world.cfg["cfg_file"])
    fabric_run_command ('('+SERVER_INSTALL_DIR+'sbin/dibbler-server start & ); sleep 4;')


def save_leases():
    assert False, "TODO!"


def save_logs():
    assert False, "TODO!"


def clear_all():
    assert False, "TODO!"
