# Copyright (C) 2012 Internet Systems Consortium.
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

from lettuce import *
import subprocess
import re

#import fabric.api

def prepare_cfg_dibbler(step, config_file):
    world.cfg["conf"] = "iface " + world.cfg["iface"] + "\n" + \
    "    class {\n" + \
    "        pool 2001:db8:1::/64\n" + \
    "    }\n" + \
    "}\n"

def prepare_cfg_isc_dhcp(step):
    # TODO: Implement me
    print("TODO: Config generation for ISC DHCP is not implemented yet.")

def prepare_cfg_kea6_default(step):
    world.cfg["conf"] = "# Default server config for Kea6 is just empty string\n"

def prepare_cfg_kea6_subnet(step, subnet, pool):
    if (not "conf" in world.cfg):
        world.cfg["conf"] = ""
    if (subnet == "default"):
        subnet = "2001:db8:1::/64"
    if (pool == "default"):
        pool = "2001:db8:1::0 - 2001:db8:1::ffff"
    world.cfg["conf"] = world.cfg["conf"] + \
    "# subnet defintion Kea 6\n" + \
    "config add Dhcp6/subnet6\n" + \
    "config set Dhcp6/subnet6[0]/subnet \"" + subnet + "\"\n" + \
    "config set Dhcp6/subnet6[0]/pool [ \"" + pool + "\" ]\n" +\
    "config commit\n"

kea_options6 = { "preference": 7,
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

def prepare_cfg_kea6_add_option(step, option_name, option_value):
    if (not "conf" in world.cfg):
        world.cfg["conf"] = ""

    assert option_name in kea_options6, "Unsupported option name " + option_name
    option_code = kea_options6.get(option_name)

    world.cfg["conf"] = world.cfg["conf"] + \
        "config add Dhcp6/option-data\n" + \
        "config set Dhcp6/option-data[0]/name \"" + option_name + "\"\n" + \
        "config set Dhcp6/option-data[0]/code " + str(option_code) + "\n" + \
        "config set Dhcp6/option-data[0]/space \"dhcp6\"\n" + \
        "config set Dhcp6/option-data[0]/csv-format true\n" + \
        "config set Dhcp6/option-data[0]/data \"" + option_value + "\"\n" + \
        "config commit\n"

def prepare_cfg_kea6_add_custom_option(step, opt_name, opt_code, opt_type, opt_value):
    if (not "conf" in world.cfg):
        world.cfg["conf"] = ""
    world.cfg["conf"] = world.cfg["conf"] + \
        "config add Dhcp6/option-def\n" + \
        "config set Dhcp6/option-def[0]/name \"" + opt_name + "\"\n" + \
        "config set Dhcp6/option-def[0]/code " + opt_code + "\n"  + \
        "config set Dhcp6/option-def[0]/type \"" + opt_type + "\"\n" + \
        "config set Dhcp6/option-def[0]/array false\n" + \
        "config set Dhcp6/option-def[0]/record-types \"\"\n" + \
        "config set Dhcp6/option-def[0]/space \"dhcp6\"\n" + \
        "config set Dhcp6/option-def[0]/encapsulate \"\"\n" + \
        "config commit\n\n" + \
        "config add Dhcp6/option-data\n" + \
        "config set Dhcp6/option-data[0]/name \"" + opt_name + "\"\n" + \
        "config set Dhcp6/option-data[0]/code " + opt_code + "\n" + \
        "config set Dhcp6/option-data[0]/space \"dhcp6\"\n" + \
        "config set Dhcp6/option-data[0]/csv-format true\n" + \
        "config set Dhcp6/option-data[0]/data \"" + opt_value + "\"\n" + \
        "config commit\n"

def prepare_cfg_kea4_add_custom_option(step, opt_name, opt_code, opt_type, opt_value):
    if (not "conf" in world.cfg):
        world.cfg["conf"] = ""
    world.cfg["conf"] = world.cfg["conf"] + \
        "config add Dhcp4/option-def\n" + \
        "config set Dhcp4/option-def[0]/name \"" + opt_name + "\"\n" + \
        "config set Dhcp4/option-def[0]/code " + opt_code + "\n"  + \
        "config set Dhcp4/option-def[0]/type \"" + opt_type + "\"\n" + \
        "config set Dhcp4/option-def[0]/array false\n" + \
        "config set Dhcp4/option-def[0]/record-types \"\"\n" + \
        "config set Dhcp4/option-def[0]/space \"dhcp4\"\n" + \
        "config set Dhcp4/option-def[0]/encapsulate \"\"\n" + \
        "config commit\n\n" + \
        "config add Dhcp4/option-data\n" + \
        "config set Dhcp4/option-data[0]/name \"" + opt_name + "\"\n" + \
        "config set Dhcp4/option-data[0]/code " + opt_code + "\n" + \
        "config set Dhcp4/option-data[0]/space \"dhcp4\"\n" + \
        "config set Dhcp4/option-data[0]/csv-format true\n" + \
        "config set Dhcp4/option-data[0]/data \"" + opt_value + "\"\n" + \
        "config commit\n"


def prepare_cfg_kea6_add_option_subnet(step, option_name, subnet, option_value):
    if (not "conf" in world.cfg):
        world.cfg["conf"] = ""

    assert option_name in kea_options6, "Unsupported option name " + option_name
    option_code = kea_options6.get(option_name)

    world.cfg["conf"] = world.cfg["conf"] + \
        "config add Dhcp6/subnet6[" + subnet + "]/option-data\n" + \
        "config set Dhcp6/subnet6[" + subnet + "]/option-data[0]/name \"" + option_name + "\"\n" + \
        "config set Dhcp6/subnet6[" + subnet + "]/option-data[0]/code " + str(option_code) + "\n" + \
        "config set Dhcp6/subnet6[" + subnet + "]/option-data[0]/space \"dhcp6\"\n" + \
        "config set Dhcp6/subnet6[" + subnet + "]/option-data[0]/csv-format true\n" + \
        "config set Dhcp6/subnet6[" + subnet + "]/option-data[0]/data \"" + option_value + "\"\n" + \
        "config commit\n"



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

def prepare_cfg_kea4_add_option(step, option_name, option_value):
    if (not "conf" in world.cfg):
        world.cfg["conf"] = ""

    assert option_name in kea_options4, "Unsupported option name " + option_name
    option_code = kea_options4.get(option_name)

    world.cfg["conf"] = world.cfg["conf"] + \
        "config add Dhcp4/option-data\n" + \
        "config set Dhcp4/option-data[0]/name \"" + option_name + "\"\n" + \
        "config set Dhcp4/option-data[0]/code " + str(option_code) + "\n" + \
        "config set Dhcp4/option-data[0]/space \"dhcp4\"\n" + \
        "config set Dhcp4/option-data[0]/csv-format true\n" + \
        "config set Dhcp4/option-data[0]/data \"" + option_value + "\"\n" + \
        "config commit\n"


def prepare_cfg_kea4_add_option_subnet(step, option_name, subnet, option_value):
    if (not "conf" in world.cfg):
        world.cfg["conf"] = ""

    assert option_name in kea_options4, "Unsupported option name " + option_name
    option_code = kea_options6.get(option_name)

    world.cfg["conf"] = world.cfg["conf"] + \
        "config add Dhcp4/subnet4[" + subnet + "]/option-data\n" + \
        "config set Dhcp4/subnet4[" + subnet + "]/option-data[0]/name \"" + option_name + "\"\n" + \
        "config set Dhcp4/subnet4[" + subnet + "]/option-data[0]/code " + str(option_code) + "\n" + \
        "config set Dhcp4/subnet4[" + subnet + "]/option-data[0]/space \"dhcp4\"\n" + \
        "config set Dhcp4/subnet4[" + subnet + "]/option-data[0]/csv-format true\n" + \
        "config set Dhcp4/subnet4[" + subnet + "]/option-data[0]/data \"" + option_value + "\"\n" + \
        "config commit\n"

def cfg_write(step):
    file = open(world.cfg["cfg_file"], 'w')
    file.write(world.cfg["conf"])
    file.close()

def start_srv_dibbler(step):
    args = [ 'dibbler-server', 'run' ]
    world.processes.add_process(step, "dhcpv6-server", args)
    # check output to know when startup has been completed
    (message, line) = world.processes.wait_for_stdout_str("dhcpv6-server",
                                                     ["Accepting connections.",
                                                      "Critical"])
    assert message == "Accepting connections.", "Got: " + str(line)

def start_srv_isc_dhcp(step, config_file):
    args = ['dhcpd' , '-d', '-cf', config_file ]

    world.processes.add_process(step, "dibbler-server", args)
    # check output to know when startup has been completed
    # TODO: Replace accepting connections.
    (message, line) = world.processes.wait_for_stderr_str(process_name,
                                                     ["Accepting connections.",
                                                      "exiting"])
    assert message == "Accepting connections.", "Got: " + str(line)


def prepare_cfg_kea4_subnet(step, subnet, pool):
    if (not "conf" in world.cfg):
        world.cfg["conf"] = ""
    if (subnet == "default"):
        subnet = "192.0.2.0/24"
    if (pool == "default"):
        pool = "192.0.2.1 - 192.0.2.10"
    world.cfg["conf"] = world.cfg["conf"] + \
    "# subnet defintion Kea4\n" + \
    "config add Dhcp4/subnet4\n" + \
    "config set Dhcp4/subnet4[0]/subnet \"" + subnet + "\"\n" + \
    "config set Dhcp4/subnet4[0]/pool [ \"" + pool + "\" ]\n" +\
    "config commit\n"


def start_srv_kea(step):

    print("Automatic start for Kea is not implemented yet. Please start Kea")
    print("manually and run the following config (also stored in %s):" % world.cfg["cfg_file"])
    print("------")
    f = open(world.cfg["cfg_file"], "r")
    print(f.read())
    f.close()
    print("------")
    raw_input("Press ENTER when ready")
          


#@step('have bind10 running(?: with configuration ([\S]+))?' +\
#      '(?: with cmdctl port (\d+))?' +\
#      '(?: as ([\S]+))?')
#def have_bind10_running(step, config_file, cmdctl_port, process_name):
#    """
#    Compound convenience step for running bind10, which consists of
#    start_bind10 and wait_for_auth.
#    Currently only supports the 'with configuration' option.
#    """
#    start_step = 'start bind10 with configuration ' + config_file
#    wait_step = 'wait for bind10 auth to start'
#    if cmdctl_port is not None:
#        start_step += ' with cmdctl port ' + str(cmdctl_port)
#   if process_name is not None:
#        start_step += ' as ' + process_name
#        wait_step = 'wait for bind10 auth of ' + process_name + ' to start'
#    step.given(start_step)
#    step.given(wait_step)

@step('Server is configured with (\S+) subnet with (\S+) pool.')
def config_srv_subnet(step, subnet, pool):
    """
    Adds server configuration with specified subnet and pool.
    subnet may define specific subnet or use the word "default"
    pool may define specific pool range or use the word "default"
    """
    if (world.cfg["server_type"] == "kea6"):
        prepare_cfg_kea6_subnet(step, subnet, pool)
    elif (world.cfg["server_type"] == "kea4"):
        prepare_cfg_kea4_subnet(step, subnet, pool)
    else:
        assert False, "Unsupported server type: %s" % world.cfg["server_type"]

@step('Server is configured with (\S+) option with value (\S+).')
def config_srv_opt(step, option_name, option_value):
    """
    Prepare server configuration with the specified option.
    option_name name of the option, e.g. dns-servers (number may be used here)
    option_value value of the configuration
    """
    if (world.cfg["server_type"] == "dibbler"):
        prepare_cfg_dibbler_add_option(step, option_name, option_value)
    elif (world.cfg["server_type"] == "isc-dhcp4"):
        prepare_cfg_isc_dhcp(step, config_file)
    elif (world.cfg["server_type"] == 'kea6'):
        prepare_cfg_kea6_add_option(step, option_name, option_value)
    elif (world.cfg["server_type"] == 'kea4'):
        prepare_cfg_kea4_add_option(step, option_name, option_value)
    else:
        assert False, "Unsupported server type: %s" % world.cfg["server_type"]

@step('Server is configured with custom option (\S+)/(\d+) with type (\S+) and value (\S+).')
def config_srv_custom_opt(step, opt_name, opt_code, opt_type, opt_value):
    """
    Prepare server configuration with the specified custom option.
    opt_name name of the option, e.g. foo
    opt_code code of the option, e.g. 100
    opt_type type of the option, e.g. uint8 (see bind10 guide for complete list)
    opt_value value of the option, e.g. 1
    """
    if (world.cfg["server_type"] == "dibbler"):
        prepare_cfg_dibbler_add_custom_option(step, opt_name, opt_code, opt_type, opt_value)
    elif (world.cfg["server_type"] == "isc-dhcp4"):
        prepare_cfg_isc6_add_custom_option(step, opt_name, opt_code, opt_type, opt_value)
    elif (world.cfg["server_type"] == 'kea6'):
        prepare_cfg_kea6_add_custom_option(step, opt_name, opt_code, opt_type, opt_value)
    elif (world.cfg["server_type"] == "kea4"):
        prepare_cfg_kea4_add_custom_option(step, opt_name, opt_code, opt_type, opt_value)
    else:
        assert False, "Unsupported server type: %s" % world.cfg["server_type"]


@step('Server is configured with (\S+) option in subnet (\d+) with value (\S+).')
def config_srv(step, option_name, subnet, option_value):
    """
    Prepare server configuration with the specified option.
    option_name name of the option, e.g. dns-servers (number may be used here)
    option_value value of the configuration
    """
    if (world.cfg["server_type"] == "dibbler"):
        prepare_cfg_dibbler_add_option_subnet(step, option_name, subnet, option_value)
    elif (world.cfg["server_type"] == "isc-dhcp4"):
        prepare_cfg_isc4_add_option_subnet(step, option_name, subnet, option_value)
    elif (world.cfg["server_type"] == "isc-dhcp6"):
        prepare_cfg_isc6_add_option_subnet(step, option_name, subnet, option_value)
    elif (world.cfg["server_type"] == 'kea4'):
        prepare_cfg_kea4_add_option_subnet(step, option_name, subnet, option_value)
    elif (world.cfg["server_type"] == 'kea6'):
        prepare_cfg_kea6_add_option_subnet(step, option_name, subnet, option_value)
    else:
        assert False, "Unsupported server type: %s" % world.cfg["server_type"]


@step('Server is started.')
def start_srv(step):

    # Write prepared config to a file
    cfg_write(step)

    if (world.cfg["server_type"] == "dibbler"):
        start_srv_dibbler(step)
    elif (world.cfg["server_type"] == "isc-dhcp"):
        start_srv_isc_dhcp(step)
    elif (world.cfg["server_type"] in ['kea4', 'kea6']):
        start_srv_kea(step)
    else:
        assert False, "Unsupported server type: %s" % world.cfg["server_type"]

@step('stop DHCPv6 server')
def stop_srv(step):
    world.processes.stop_process('dhcpv6-server')
