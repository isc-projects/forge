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


from logging_facility import *
from lettuce.registry import world
from init_all import SERVER_INSTALL_DIR, SERVER_IFACE

from serversupport.multi_server_functions import fabric_run_command, fabric_send_file, remove_local_file, cpoy_configuration_file 

# it would be wise to remove redundant names,
# but I'll leave it that way for now.
isc_dhcp_options6 = {
#                  "client-id": 1,
#                  "server-id" : 2,
#                  "IA_NA" : 3,
#                  "IN_TA": 4,
#                  "IA_address" : 5,
                 "preference": "preference",
#                  "relay-msg": 9,
#                  "status-code": 13,
#                  "rapid_commit": 14,
#                  "interface-id": 18,
                 "sip-server-dns": "sip-servers-names",
                 "sip-server-addr": "sip-servers-addresses",
                 "dns-servers": "domain-name-servers",
                 "domain-search": "domain-search",
#                  "IA_PD": 25,
#                  "IA-Prefix": 26,
                 "nis-servers": "nis-servers",
                 "nisp-servers": "nisp-servers",
                 "nis-domain-name": "nis-domain-name",
                 "nisp-domain-name": "nisp-domain-name",
                 "sntp-servers": "sntp-servers",
                 "information-refresh-time": "info-refresh-time" 
                     }

needs_chenging = {
                  "sip-servers-names": True,
                  "domain-name-servers": True,
                  "domain-search": True,
                  "nis-domain-name": True,
                  "nisp-domain-name": True,
                  33: True #for 'config file', that will need more work:)
                  }

isc_dhcp_otheroptions = {"tftp-servers": 32,
                         "config-file": 33,
                         "syslog-servers": 34,
                         "time-servers": 37,
                         "time-offset": 38
                         }
isc_dhcp_otheroptions_value_type = {"tftp-servers": "array of ip6-address",
                         "config-file": "text",
                         "syslog-servers": "array of ip6-address",
                         "time-servers": "array of ip6-address",
                         "time-offset": "integer 16"
                         }

def switch_prefix6_lengths_to_pool(ip6_addr ,length, delegated_length):
    
    ip6_addr_splited = ip6_addr.split(":")
    if len(ip6_addr_splited) < 3 or len(ip6_addr_splited) > 9:
        raise "Error! Please enter correct IPv6 address!"
    error_flag = False
    for i in range(1, len(ip6_addr_splited) - 1):
        if not ip6_addr_splited[i]:
            if error_flag:
                raise "Error! Please enter correct IPv6 address!"
            error_flag = True
    
    for i in range (0, 6):
        if ip6_addr_splited[i]:
            continue
        else:
            ip6_addr_splited.append("")
    
    bin_addr = []
    for each in ip6_addr_splited:
        if not each:
            bin_addr.append('')
            continue
        bin_addr.append(bin(int(each,16)))
    
    str = ""
    for each in bin_addr:
        each = each.zfill(18)
        if "0b" in each:
            each = each.replace("0b","")
        else:
            each = each[2:]
        str += each
    lowest_prefix = str
    highest_prefix = lowest_prefix[0:length] + '1'*(delegated_length - length) + lowest_prefix[delegated_length:]
    
    ip6_addr_new = []
    for i in range (0,8):
        ip6_addr_new.append(highest_prefix[:16])
        highest_prefix = highest_prefix[16:]
    
    tmp = []
    for each in ip6_addr_new:
        b = hex(int(each,2))
        tmp.append(b[2:])
    
    prefix = []
    flag1 = False
    flag2 = False
    for i in range(0,8):
        if tmp[i] == "0" and not flag1 and not flag2:
            prefix.append("")
            flag1 = True
            continue
        elif tmp[i] == "0" and flag1 and not flag2:
            continue
        elif tmp[i] != "0" and flag1 and not flag2:
            prefix.append(tmp[i])
            flag2 = True
        else:
            prefix.append(tmp[i])
    
    final = ":".join(prefix)
    if final[-1]==":":
        final+=":"

    return final
def restart_srv():
    pass

def stop_srv():
    try:
        fabric_run_command("sudo killall dhcpd &>/dev/null")
    except:
        pass
    
def set_time(step, which_time, value):
    if which_time in world.cfg["server_times"]:
            world.cfg["server_times"][which_time] = value
    else:
        assert which_time in world.cfg["server_times"], "Unknown time name: %s" % which_time

def prepare_cfg_default(step):
    world.cfg["conf"] = "# Config file for ISC-DHCPv6 \n"
    
    #check this values!
def add_defaults():
    if (not "conf_time" in world.cfg):
        world.cfg["conf_time"] = ""
    t1 = world.cfg["server_times"]["renew-timer"]
    t2 = world.cfg["server_times"]["rebind-timer"]
    t3 = world.cfg["server_times"]["preferred-lifetime"]
    t4 = world.cfg["server_times"]["valid-lifetime"]
    world.cfg["conf_time"] = '''
    option dhcp-rebinding-time {t2};
    option dhcp-renewal-time {t1};
    preferred-lifetime {t3};
    default-lease-time {t4};
    '''.format(**locals())
    
def prepare_cfg_subnet(step, subnet, pool):
    get_common_logger().debug("Configure subnet...")
    if not "conf_subnet" in world.cfg:
        world.cfg["conf_subnet"] = ""

    world.cfg["subnet"] = subnet
    pointer = '{'
    
    if subnet == "default":
        subnet = "2001:db8:1::/64"
       
    if pool == "default":
        pool = "2001:db8:1::0 2001:db8:1::ffff"
    else:
        pool = pool.replace('-',' ')
        
    world.cfg["conf_subnet"] += '''\
        subnet6 {subnet} {pointer}
            range6 {pool};
        '''.format(**locals())

def prepare_cfg_add_option(step, option_name, option_value, space):
    if not "conf_option" in world.cfg:
        world.cfg["conf_option"] = ""

    # first check it in global options
    option_proper_name = isc_dhcp_options6.get(option_name)

    # is there is no such options check it in 'isc_dhcp_otheroptions'
    # it's mostly vendor options    
    if option_proper_name is None:
        option_proper_name = isc_dhcp_otheroptions.get(option_name)

    # if it's still None... assert error!
    elif option_proper_name is None:
        assert False, "Unsupported option name " + option_name

    # some functions needs " " in it, so lets add them
    # that's for all those functions which are configured 
    # indifferent way then kea6 configuration, if you add
    # new such option, add it to needs_chenging dict.
    if needs_chenging.get(option_proper_name):
        tmp = option_value.split(",")
        option_value = ','.join('"' + item + '"' for item in tmp)
    
    # for all common options
    if space == 'dhcp6':
        world.cfg["conf_option"] += ''' option dhcp6.{option_proper_name} {option_value};
                '''.format(**locals())

    # for vendor option, for now we support only one vendor in config file
    else:
        if not "conf_vendor" in world.cfg:
            world.cfg["conf_vendor"] = '''
                option space {space} code width 2 length width 2;
                '''.format(**locals())
                #code width 2 length width 2 hash size 3
        type = isc_dhcp_otheroptions_value_type.get(option_name)
        world.cfg["conf_vendor"] += '''
            option {space}.{option_name} code {option_proper_name} = {type};
            option {space}.{option_name} {option_value};
            '''.format(**locals())

def prepare_cfg_add_custom_option(step, opt_name, opt_code, opt_type, opt_value, space):
    #implement this
    pass

def prepare_cfg_add_option_subnet(step, option_name, subnet, option_value):
    if (not "conf_subnet" in world.cfg):
        assert False, 'Configure subnet/pool first, then subnet options'

    assert option_name in isc_dhcp_options6, "Unsupported option name " + option_name
    
    option_proper_name = isc_dhcp_options6.get(option_name)

    if needs_chenging.get(option_proper_name):
        tmp = option_value.split(",")
        option_value = ','.join('"' + item + '"' for item in tmp)
    
    world.cfg["conf_subnet"] += '''option dhcp6.{option_proper_name} {option_value};
         '''.format(**locals())

def prepare_cfg_prefix(step, prefix, length, delegated_length, subnet):
    
    highest = switch_prefix6_lengths_to_pool(str(prefix),int(length),int(delegated_length))
    
    world.cfg["conf_subnet"] += '''prefix6 {prefix} {highest} /{delegated_length};
         '''.format(**locals())

def cfg_write():
    cfg_file = open(world.cfg["cfg_file"], 'w')
    cfg_file.write(world.cfg["conf_time"])
    if "conf_option" in world.cfg:
        cfg_file.write(world.cfg["conf_option"])
    if "conf_vendor" in world.cfg:
        cfg_file.write(world.cfg["conf_vendor"])
    cfg_file.write(world.cfg["conf_subnet"])
    cfg_file.write('}')#add } for subnet block

    cfg_file.close()

def convert_cfg_file(cfg):
    tmpfile = cfg + "_processed"
    conf = open(cfg, "rt")
    process = open(tmpfile, "w")
    tab_flag = False
    # Copy input line by line, but skip empty and comment lines
    for line in conf:
        line = line.strip()
        if len(line) < 1:
            continue
        if (line[0] == "#"):
            continue
        if "}" in line:
            tab_flag = False
        if tab_flag:            
            process.write("\t"+line + "\n")
        if not tab_flag :
            process.write(line + "\n")
        if "{" in line:
            tab_flag = True

    conf.close()
    process.close

    remove_local_file(cfg)

def set_ethernet_interface():
    """
    To start ISC-DHCPv6 we need set some address from chosen pool on one ethernet interface 
    """
    tmp = world.cfg["subnet"].split('/')
    address = tmp[0] + "1/" + tmp[1]
    eth = SERVER_IFACE
    cmd = 'ip addr flush {eth}'.format(**locals())
    cmd1 = 'ip -6 addr add {address} dev {eth}'.format(**locals())
    
    get_common_logger().debug("Set up ethernet interface for ISC-DHCP server:")
    
#     fabric_cmd(cmd,0)
#     time.sleep(3)
#     fabric_cmd(cmd1,0)

def start_srv(start, process):
    """
    Start ISC-DHCPv6 with generated config.
    """
    if (not "conf_option" in world.cfg):
        world.cfg["conf_option"] = ""
    add_defaults()
    cfg_write() 
    get_common_logger().debug("Start ISC-DHCPv6 with generated config:")
    convert_cfg_file(world.cfg["cfg_file"])
    fabric_send_file(world.cfg["cfg_file"] + '_processed', world.cfg["cfg_file"] + '_processed')
    cpoy_configuration_file(world.cfg["cfg_file"] + '_processed')
    remove_local_file(world.cfg["cfg_file"])
    set_ethernet_interface()
    stop_srv()
    world.cfg["conf_subnet"] = ""
    fabric_run_command('echo y |rm /var/db/dhcpd6.leases')
    fabric_run_command('touch /var/db/dhcpd6.leases')
    fabric_run_command('( sudo '+SERVER_INSTALL_DIR+'sbin/dhcpd -6 -cf server.cfg_processed); sleep 3;')
    #uncomment this for less output, do this after full support for isc-dhcp
    #fabric_run_command('(rm nohup.out; nohup dhcpd -6 -cf server.cfg_processed); sleep 3;') 