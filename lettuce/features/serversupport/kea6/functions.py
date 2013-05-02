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


from fabric.api import sudo, run, settings, put, hide
from logging_facility import *
from lettuce.registry import world
from init_all import SERVER_INSTALL_DIR
import os


def restart_srv():
    fabric_run_bindctl ('restart')

def stop_srv():
    # @todo: implement this
    pass

def prepare_cfg_default(step):
    world.cfg["conf"] = "# Default server config for Kea6 is just empty string\n"
    
def prepare_cfg_subnet(step, subnet, pool):
    get_common_logger().debug("Configure subnet...")
    if (not "conf" in world.cfg):
        world.cfg["conf"] = ""
    if (subnet == "default"):
        subnet = "2001:db8:1::/64"
    if (pool == "default"):
        pool = "2001:db8:1::0 - 2001:db8:1::ffff"
    world.cfg["conf"] = '''\
        # subnet defintion Kea 6
        config add Dhcp6/subnet6
        config set Dhcp6/subnet6[0]/subnet "{subnet}"
        config set Dhcp6/subnet6[0]/pool [ "{pool}" ]
        config commit
        '''.format(**locals())
        
    
  
kea_options6 = { "blank": 0, 
                 "client-id": 1,
                 "server-id" : 2,
                 "IA_NA" : 3,
                 "IA_address" : 5,
                 "preference": 7,
                 "status-code": 13,
                 "sip-server-dns": 21,
                 "sip-server-addr": 22,
                 "dns-servers": 23,
                 "domain-search": 24,
                 "nis-servers": 27,
                 "nisp-servers": 28,
                 "nis-domain-name": 29,
                 "nisp-domain-name": 30,
                 "sntp-servers": 31,
                 "information-refresh-time": 32 }

def prepare_cfg_add_option(step, option_name, option_value):
    if (not "conf" in world.cfg):
        world.cfg["conf"] = ""

    assert option_name in kea_options6, "Unsupported option name " + option_name
    option_code = kea_options6.get(option_name)

    world.cfg["conf"] += '''config add Dhcp6/option-data
        config set Dhcp6/option-data[0]/name "{option_name}"
        config set Dhcp6/option-data[0]/code {option_code}
        config set Dhcp6/option-data[0]/space "dhcp6"
        config set Dhcp6/option-data[0]/csv-format true
        config set Dhcp6/option-data[0]/data "{option_value}"
        config commit
        '''.format(**locals())

    world.kea["option_cnt"] = world.kea["option_cnt"] + 1
    
def prepare_cfg_add_custom_option(step, opt_name, opt_code, opt_type, opt_value):
    if (not "conf" in world.cfg):
        world.cfg["conf"] = ""
    world.cfg["conf"] += '''config add Dhcp6/option-def
        config set Dhcp6/option-def[0]/name "{opt_name}"
        config set Dhcp6/option-def[0]/code {opt_code}
        config set Dhcp6/option-def[0]/type "{opt_type}"
        config set Dhcp6/option-def[0]/array false
        config set Dhcp6/option-def[0]/record-types ""
        config set Dhcp6/option-def[0]/space "dhcp6"
        config set Dhcp6/option-def[0]/encapsulate ""
        config add Dhcp6/option-data
        config set Dhcp6/option-data[0]/name "{opt_name}"
        config set Dhcp6/option-data[0]/code {opt_code}
        config set Dhcp6/option-data[0]/space "dhcp6"
        config set Dhcp6/option-data[0]/csv-format true
        config set Dhcp6/option-data[0]/data "{opt_value}"
        config commit
        '''.format(**locals())

def prepare_cfg_add_option_subnet(step, option_name, subnet, option_value):
    if (not "conf" in world.cfg):
        world.cfg["conf"] = ""

    assert option_name in kea_options6, "Unsupported option name " + option_name
    option_code = kea_options6.get(option_name)
    
    world.cfg["conf"] += '''
        config add Dhcp6/subnet6[{subnet}]/option-data
        config set Dhcp6/subnet6[{subnet}]/option-data[0]/name "{option_name}"
        config set Dhcp6/subnet6[{subnet}]/option-data[0]/code {option_code}
        config set Dhcp6/subnet6[{subnet}]/option-data[0]/space "dhcp6"
        config set Dhcp6/subnet6[{subnet}]/option-data[0]/csv-format true
        config set Dhcp6/subnet6[{subnet}]/option-data[0]/data "{option_value}"
        config commit
        '''.format(**locals())

def prepare_cfg_kea6_for_kea6_start():
    """
    config file for kea6 start
    """
    config = '''
        # This config file starts b10-dhcp6 server.
        config add Init/components b10-dhcp6
        config set Init/components/b10-dhcp6/kind dispensable
        config commit
        '''
    cfg_file = open("kea6-start.cfg", "w")
    cfg_file.write(config)
    cfg_file.close()


def prepare_cfg_kea6_for_kea6_stop():
    """
    config file for kea6 clear configuration and stopping
    """
    config = '''
        # This config file stops b10-dhcp6 server and removes its configuration.
        # Get rid of any subnets
        config set Dhcp6/subnet6 []
        # Get rid of any option format definitions
        config set Dhcp6/option-def []
        # Get rid of any option values
        config set Dhcp6/option-data []
        # Stop b10-dhcp6 server from starting again
        config remove Init/components b10-dhcp6
        config commit
        # And stop it
        Dhcp6 shutdown
        '''
    cfg_file = open("kea6-stop.cfg", "w")
    cfg_file.write(config)
    cfg_file.close()

def cfg_write():
    cfg_file = open(world.cfg["cfg_file"], 'w')
    cfg_file.write(world.cfg["conf"])
    cfg_file.close()
 
def pepere_config_file(cfg):
    """
    Prepare config file from generated world.cfg["cfg_file"] or START/STOP
    """
    tmpfile = cfg + "_processed"
    conf = open(cfg, "rt")
    process = open(tmpfile, "w")
    # Copy input line by line, but skip empty and comment lines
    for line in conf:
        line = line.strip()
        if len(line)<2:
            continue
        if (line[0] == "#"):
            continue
        process.write(line+"\n")
    conf.close()
    process.close()
    try:
        os.remove(cfg)
    except OSError:
        get_common_logger().error('File %s cannot be removed' % cfg)
        

def fabric_send_file (file_local):
    """
    Send file to remote virtual machine
    """
    file_remote = file_local
    with settings(host_string=world.cfg["mgmt_addr"],
                  user=world.cfg["mgmt_user"],
                  password=world.cfg["mgmt_pass"]):
        with hide('running', 'stdout'):
            put(file_local, file_remote)
    try:
        os.remove(file_local)
    except OSError:
        get_common_logger().error('File %s cannot be removed' % file_local)
        
def fabric_run_bindctl (opt):
    """
    Run bindctl with prepered config file
    """    
    if opt == "clean":
        get_common_logger().debug('------------ cleaning kea configuration')
        prepare_cfg_kea6_for_kea6_stop()
        cfg_file = 'kea6-stop.cfg'
        pepere_config_file(cfg_file)
        fabric_send_file (cfg_file+"_processed")
    if opt == "start":
        get_common_logger().debug('------------ starting fresh kea')
        prepare_cfg_kea6_for_kea6_start()
        cfg_file = 'kea6-start.cfg'
        pepere_config_file(cfg_file)
        fabric_send_file (cfg_file+"_processed")
    if opt == "conf":
        get_common_logger().debug('------------ kea configuration')
        cfg_file = world.cfg["cfg_file"]
        pepere_config_file(cfg_file)
        fabric_send_file (cfg_file+"_processed")
    if opt == "restart":
        #implement this
        pass
    cmd='(echo "execute file '+cfg_file+'_processed" | ' + SERVER_INSTALL_DIR + 'bin/bindctl ); sleep 1'
    with settings(host_string=world.cfg["mgmt_addr"],
                  user=world.cfg["mgmt_user"],
                  password=world.cfg["mgmt_pass"]):
        run(cmd)

def start_srv():
    """
    Start kea with generated config
    """
    cfg_write() 
    get_common_logger().debug("------ Bind10, dhcp6 configuration procedure:")
    fabric_run_bindctl ('clean')#clean and stop
    fabric_run_bindctl ('start')#start
    fabric_run_bindctl ('conf')#conf
#     
