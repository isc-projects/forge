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

from serversupport.multi_server_functions import fabric_run_command, fabric_send_file, remove_local_file, cpoy_configuration_file
from lettuce import world
from textwrap import dedent
import serversupport.kea6.functions
from logging_facility import get_common_logger
from init_all import SERVER_INSTALL_DIR

## functions to import:
## run_command, set_logger, prepare_config_file,cfg_write, parsing_bind_stdout
## set_time ?

def prepare_cfg_subnet(step, subnet, pool):

    # subnet defintion Kea4
    subnetcfg ='''\
    config add Dhcp4/subnet4
    config set Dhcp4/subnet4[0]/subnet "{subnet}"
    config set Dhcp4/subnet4[0]/pool [ "{pool}" ]
    config commit\n
    '''.format(**locals())
    
    world.cfg["conf"] += dedent(subnetcfg) 


kea_options4= { "subnet-mask": 1,
                 "routers": 3,
                 "name-servers": 5, # ipv4-address (array)
                 "domain-name-servers": 6, # ipv4-address (array)
                 "domain-name": 15, # fqdn (single)
                 "broadcast-address": 28, # ipv4-address (single)
                 "nis-domain": 40, # string (single)
                 "nis-servers": 41, # ipv4-address (array)
                 "ntp-servers": 42 # ipv4-address (array)
                 }

def prepare_cfg_add_custom_option(step, opt_name, opt_code, opt_type, opt_value, space):
    #implement this
    pass

def prepare_cfg_add_option_subnet(step, option_name, subnet, option_value):
    #implement this
    pass
def config_srv_another_subnet(step, subnet, pool, interface):
    #implement this
    pass
   
def prepare_cfg_add_option(step, option_name, option_value, space): # TODO: enable space configuration
    if (not "conf" in world.cfg):
        world.cfg["conf"] = ""

    assert option_name in kea_options4, "Unsupported option name " + option_name
    option_code = kea_options4.get(option_name)

    if not hasattr(world, 'kea'):
        world.kea = {}
    else:
        world.kea.clear()
    world.kea["option_cnt"] = 0
    
    option_cnt=world.kea["option_cnt"]
    options = '''\
    config add Dhcp4/option-data
    config set Dhcp4/option-data[{option_cnt}]/name "{option_name}"
    config set Dhcp4/option-data[{option_cnt}]/code {option_code}
    config set Dhcp4/option-data[{option_cnt}]/space "dhcp4"
    config set Dhcp4/option-data[{option_cnt}]/csv-format true
    config set Dhcp4/option-data[{option_cnt}]/data "{option_value}"
    config commit
    '''.format(**locals())
    world.cfg["conf"] +=  dedent(options)
    world.kea["option_cnt"] += 1

def prepare_cfg_kea4_for_kea4_start(filename):
    """
    config file for kea4 start
    """
    config = '''
        # This config file starts b10-dhcp4 server.
        config add Init/components b10-dhcp4
        config set Init/components/b10-dhcp4/kind dispensable
        config commit
        '''
    cfg_file = open(filename, "w")
    cfg_file.write(config)
    cfg_file.close()


def prepare_cfg_kea4_for_kea4_stop(filename):
    """
    config file for kea4 clear configuration and stopping
    """
    config = '''
        # This config file stops b10-dhcp4 server and removes its configuration.
        # Get rid of any subnets
        config set Dhcp4/subnet4 []
        # Get rid of any option format definitions
        config set Dhcp4/option-def []
        # Get rid of any option values
        config set Dhcp4/option-data []
        # Stop b10-dhcp4 server from starting again
        config remove Init/components b10-dhcp4
        config commit
        # And stop it
        Dhcp4 shutdown
        '''
    cfg_file = open(filename, "w")
    cfg_file.write(config)
    cfg_file.close()

def fabric_run_bindctl (opt):
    """
    Run bindctl with prepered config file
    """    
    if opt == "clean":
        get_common_logger().debug('------------ cleaning kea configuration')
        cfg_file = 'kea4-stop.cfg'
        prepare_cfg_kea4_for_kea4_stop(cfg_file)
        serversupport.kea6.functions.prepare_config_file(cfg_file)
        fabric_send_file(cfg_file + '_processed', cfg_file + '_processed')
    if opt == "start":
        get_common_logger().debug('------------ starting fresh kea')
        cfg_file = 'kea4-start.cfg'
        prepare_cfg_kea4_for_kea4_start(cfg_file)
        serversupport.kea6.functions.prepare_config_file(cfg_file)
        fabric_send_file(cfg_file + '_processed', cfg_file + '_processed')
    if opt == "conf":
        get_common_logger().debug('------------ kea configuration')
        cfg_file = world.cfg["cfg_file"]
        serversupport.kea6.functions.prepare_config_file(cfg_file)
        fabric_send_file(cfg_file + '_processed', cfg_file + '_processed')
        cpoy_configuration_file(cfg_file + '_processed')
    if opt == "restart":
        #implement this
        pass
    
    result = fabric_run_command('(echo "execute file '+cfg_file+'_processed" | ' + SERVER_INSTALL_DIR + 'bin/bindctl ); sleep 1')

def start_srv(start, process):
    serversupport.kea6.functions.cfg_write()
    get_common_logger().debug("------ Bind10, dhcp4 configuration procedure:")
    fabric_run_bindctl ('clean')#clean and stop
    fabric_run_bindctl ('start')#start
    fabric_run_bindctl ('conf')#conf


def restart_srv():
    pass
    # @todo: Implement this


def prepare_cfg_prefix(step, prefix, length, delegated_length, subnet):
    assert False, "This function can be used only with DHCPv6"