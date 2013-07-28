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


from fabric.api import run, settings, put, hide
from logging_facility import *
from lettuce.registry import world
from init_all import SERVER_INSTALL_DIR, SERVER_IFACE
import os


def restart_srv():
    try:
        fabric_cmd ("(dibbler-server restart); sleep 1;", 1)
    except:
        pass

def stop_srv():
    try:
        fabric_cmd ("(dibbler-server stop); sleep 1;", 1)
    except:
        pass

def prepare_cfg_default(step):
    world.cfg["conf"] = "# This is Forge generated config file.\n"
    
    #check this values!
def add_defaults(rebinding_time = '1400', renewal_time = '10', preferred_lifetime = '1000', lease_time = '2000', max_lease_time = '2000'):
    eth = SERVER_IFACE
    pointer_open = '{'
    pointer_close = '}'
    
#option dhcp-rebinding-time {rebinding_time};
#option dhcp-renewal-time {renewal_time};
#preferred-lifetime {preferred_lifetime};
#default-lease-time {lease_time};
#max-lease-time {max_lease_time};
#log-level 4
#log-mode short
#preference 0
    world.cfg["conf"] += '''
iface "{eth}" {pointer_open}
    '''.format(**locals())
    
def prepare_cfg_subnet(step, subnet, pool):
    get_common_logger().debug("Configure subnet...")
    if (not "conf" in world.cfg):
        world.cfg["conf"] = ""
    if (subnet == "default"):
        subnet = "2001:db8:1::/64"
       
    if (pool == "default"):
        pool = "2001:db8:1::0-2001:db8:1::ffff"
        
    world.cfg["subnet"] = subnet
    add_defaults() #add in future configuration of those functions
    pointer_open = '{'
    pointer_close = '}'
    world.cfg["conf"] += '''\
# subnet defintion
  class {pointer_open}
   pool {pool}
  {pointer_close}
        '''.format(**locals())
        
    
#still not implemented
dibbler_options6 = { 
                    }

def prepare_cfg_add_option(step, option_name, option_value):
    if (not "conf" in world.cfg):
        world.cfg["conf"] = ""

    assert option_name in isc_dhcp_options6, "Unsupported option name " + option_name
    option_code = isc_dhcp_options6.get(option_name)

#     world.cfg["conf"] += '''config add Dhcp6/option-data
#         config set Dhcp6/option-data[0]/name "{option_name}"
#         config set Dhcp6/option-data[0]/code {option_code}
#         config set Dhcp6/option-data[0]/space "dhcp6"
#         config set Dhcp6/option-data[0]/csv-format true
#         config set Dhcp6/option-data[0]/data "{option_value}"
#         config commit
#         '''.format(**locals())

    world.kea["option_cnt"] = world.kea["option_cnt"] + 1
    
def prepare_cfg_add_custom_option(step, opt_name, opt_code, opt_type, opt_value):
    if (not "conf" in world.cfg):
        world.cfg["conf"] = ""
#     world.cfg["conf"] += '''config add Dhcp6/option-def
#         config set Dhcp6/option-def[0]/name "{opt_name}"
#         config set Dhcp6/option-def[0]/code {opt_code}
#         config set Dhcp6/option-def[0]/type "{opt_type}"
#         config set Dhcp6/option-def[0]/array false
#         config set Dhcp6/option-def[0]/record-types ""
#         config set Dhcp6/option-def[0]/space "dhcp6"
#         config set Dhcp6/option-def[0]/encapsulate ""
#         config add Dhcp6/option-data
#         config set Dhcp6/option-data[0]/name "{opt_name}"
#         config set Dhcp6/option-data[0]/code {opt_code}
#         config set Dhcp6/option-data[0]/space "dhcp6"
#         config set Dhcp6/option-data[0]/csv-format true
#         config set Dhcp6/option-data[0]/data "{opt_value}"
#         config commit
#         '''.format(**locals())

def prepare_cfg_add_option_subnet(step, option_name, subnet, option_value):
    if (not "conf" in world.cfg):
        world.cfg["conf"] = ""

    assert option_name in dibbler_options6, "Unsupported option name " + option_name
    option_code = dibbler_options6.get(option_name)
    
#     world.cfg["conf"] += '''
#         config add Dhcp6/subnet6[{subnet}]/option-data
#         config set Dhcp6/subnet6[{subnet}]/option-data[0]/name "{option_name}"
#         config set Dhcp6/subnet6[{subnet}]/option-data[0]/code {option_code}
#         config set Dhcp6/subnet6[{subnet}]/option-data[0]/space "dhcp6"
#         config set Dhcp6/subnet6[{subnet}]/option-data[0]/csv-format true
#         config set Dhcp6/subnet6[{subnet}]/option-data[0]/data "{option_value}"
#         config commit
#         '''.format(**locals())

def cfg_write():
    cfg_file = open(world.cfg["cfg_file"], 'w')
    cfg_file.write(world.cfg["conf"])
    cfg_file.write('}')#add last } for closing file
    cfg_file.close()

def send_file (file_local):
    """
    Send file to remote virtual machine
    """
    file_remote = '/etc/dibbler/server.conf'
    with settings(host_string = world.cfg["mgmt_addr"],
                  user = world.cfg["mgmt_user"],
                  password = world.cfg["mgmt_pass"]):
        with hide('running', 'stdout'):
            put(file_local, file_remote)
    try:
        os.remove(file_local)
    except OSError:
        get_common_logger().error('File %s cannot be removed' % file_local)


def fabric_cmd (cmd, hide_opt):
    with settings(host_string = world.cfg["mgmt_addr"], user = world.cfg["mgmt_user"], password = world.cfg["mgmt_pass"]):
        if hide_opt:
            with hide('running', 'stdout', 'stderr', 'output','warnings'):
                run(cmd, pty = True)
        else:
            run(cmd, pty = True)

def start_srv():
    """
    Start ISC-DHCPv6 with generated config.
    """
    cfg_write() 
    stop_srv()
    #set_ethernet_interface()
    get_common_logger().debug("Starting Dibbler with generated config:")
    send_file (world.cfg["cfg_file"])
    fabric_cmd ('(rm nohup.out; nohup dibbler-server run & ); sleep 2;', 0)

