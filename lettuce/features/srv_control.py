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

from lettuce import world, step
from init_all import SOFTWARE_UNDER_TEST
import importlib
dhcpfun = importlib.import_module("softwaresupport.%s.functions" % SOFTWARE_UNDER_TEST)

ddns_enable = True
try:
    ddns = importlib.import_module("softwaresupport.%s.functions_ddns" % SOFTWARE_UNDER_TEST)
except ImportError:
    ddns_enable = False


def ddns_block():
    if not ddns_enable:
        assert False, "Forge couldn't import DDNS support."


def test_define_value(*args):
    """
    Designed to use in test scenarios values from ini_all.py file. To makes them even more portable
    Bash like define variables: $(variable_name)
    You can use steps like:
        Client download file from server stored in: $(SERVER_SETUP_DIR)other_dir/my_file
    or
        Client removes file from server located in: $(SERVER_INSTALL_DIR)my_file

    $ sign is very important without it Forge wont find variable in init_all.

    There is no slash ("/") between $(SERVER_INSTALL_DIR) and my_file because variable $(SERVER_INSTALL_DIR)
    should end with slash.

    You can use any variable form init_all in that way. Also you can add them using step:
    "Client defines new variable: (\S+) with value (\S+)."

    """
    imported = None
    front = None
    tested_args = []

    for i in range(len(args)):
        tmp = str(args[i])
        if "$" in args[i]:
            index = tmp.find('$')
            front = tmp[:index]
            tmp = tmp[index:]

        if tmp[:2] == "$(":
            index = tmp.find(')')
            assert index > 2, "Defined variable not complete. Missing ')'. "

            for each in world.define:
                if str(each[0]) == tmp[2: index]:
                    imported = int(each[1]) if each[1].isdigit() else str(each[1])
            if imported is None:
                try:
                    imported = getattr(__import__('init_all', fromlist = [tmp[2: index]]), tmp[2: index])
                except ImportError:
                    assert False, "No variable in init_all.py or in world.define named: " + tmp[2: index]
            if front is None:
                tested_args.append(imported + tmp[index + 1:])
            else:
                tested_args.append(front + imported + tmp[index + 1:])
        else:
            tested_args.append(args[i])
    return tested_args


##server configurations
@step('Server is configured with (\S+) subnet with (\S+) pool.')
def config_srv_subnet(step, subnet, pool):
    """
    Adds server configuration with specified subnet and pool.
    subnet may define specific subnet or use the word "default"
    pool may define specific pool range or use the word "default"

    Setting subnet in that way, will cause to set in on interface you set in
    init_all.py as variable "SERVER_IFACE" leave it to None if you don want to set
    interface.
    """
    subnet, pool = test_define_value( subnet, pool)
    dhcpfun.prepare_cfg_subnet(step, subnet, pool)


@step('On interface (\S+) server is configured with another subnet: (\S+) with (\S+) pool.')
def config_srv_another_subnet(step, interface, subnet, pool):
    """
    Add another subnet with specified subnet/pool/interface.
    """
    if SOFTWARE_UNDER_TEST in ['dibbler_server', 'isc_dhcp4_server', 'isc_dhcp6_server']:
        assert False, "Test temporary available only for Kea servers."
    subnet, pool, interface = test_define_value( subnet, pool, interface)
    dhcpfun.config_srv_another_subnet(step, subnet, pool, interface)


@step('Server is configured with another subnet: (\S+) with (\S+) pool.')
def config_srv_another_subnet_no_interface(step, subnet, pool):
    """
    Add another subnet to config file without interface specified.
    """
    if SOFTWARE_UNDER_TEST in ['dibbler_server', 'isc_dhcp4_server', 'isc_dhcp6_server']:
        assert False, "Test temporary available only for Kea servers."
    subnet, pool = test_define_value( subnet, pool)
    dhcpfun.config_srv_another_subnet(step, subnet, pool, None)


@step('Server is configured with (\S+) prefix in subnet (\d+) with (\d+) prefix length and (\d+) delegated prefix length.')
def config_srv_prefix(step, prefix, subnet, length, delegated_length ):
    """
    Adds server configuration with specified prefix.
    """
    prefix, length, delegated_length, subnet = test_define_value(prefix, length, delegated_length, subnet)
    dhcpfun.prepare_cfg_prefix(step, prefix, length, delegated_length, subnet)


@step('Next server value on subnet (\d+) is configured with address (\S+).')
def subnet_add_siaddr(step, subnet_number, addr):
    addr, subnet_number = test_define_value(addr, subnet_number)
    dhcpfun.add_siaddr(step, addr, subnet_number)


@step('Next server global value is configured with address (\S+).')
def global_add_siaddr(step, addr):
    #TODO: implement this
    #addr, subnet_number = test_define_value(addr, "pass")
    dhcpfun.add_siaddr(step, addr, None)


@step('Server is configured with (\S+) option with value (\S+).')
def config_srv_opt(step, option_name, option_value):
    """
    Add to configuration options like: preference, dns servers..
    This step causes to set in to main space!
    """
    option_name, option_value = test_define_value( option_name, option_value)
    dhcpfun.prepare_cfg_add_option(step, option_name, option_value, world.cfg["space"])


@step('On space (\S+) server is configured with (\S+) option with value (\S+).')
def config_srv_opt_space(step, space, option_name, option_value):
    """
    Add to configuration options like: preference, dns servers.. but you can specify
    to which space should that be included.
    """
    option_name, option_value, space = test_define_value(option_name, option_value, space)
    dhcpfun.prepare_cfg_add_option(step, option_name, option_value, space)


@step('Server is configured with custom option (\S+)/(\d+) with type (\S+) and value (\S+).')
def config_srv_custom_opt(step, opt_name, opt_code, opt_type, opt_value):
    """
    Prepare server configuration with the specified custom option.
    opt_name name of the option, e.g. foo
    opt_code code of the option, e.g. 100
    opt_type type of the option, e.g. uint8 (see bind10 guide for complete list)
    opt_value value of the option, e.g. 1
    """
    opt_name, opt_code, opt_type, opt_value = test_define_value(opt_name, opt_code, opt_type, opt_value)
    dhcpfun.prepare_cfg_add_custom_option(step, opt_name, opt_code, opt_type, opt_value, world.cfg["space"])


@step('On space (\S+) server is configured with a custom option (\S+)/(\d+) with type (\S+) and value (\S+).')
def config_srv_custom_opt_space(step, space, opt_name, opt_code, opt_type, opt_value):
    """
    Same step like "Server is configured with custom option.." but specify that option on different space then main.
    """
    opt_name, opt_code, opt_type, opt_value, space = test_define_value(opt_name, opt_code, opt_type, opt_value, space)
    dhcpfun.prepare_cfg_add_custom_option(step, opt_name, opt_code, opt_type, opt_value, space)


@step('Time (\S+) is configured with value (\d+).')
def set_time(step, which_time, value):
    """
    Change values of T1, T2, preffered lifetime and valid lifetime.
    """
    which_time, value = test_define_value(which_time, value)
    dhcpfun.set_time(step, which_time, value)

@step('Time (\S+) is not configured.')
def unset_time(step, which_time):
    """
    Remove default values of T1, T2, preferred lifetime and valid lifetime.
    """
    which_time = test_define_value(which_time)[0]
    dhcpfun.unset_time(step, which_time)

@step('Option (\S+) is configured with value (\S+).')
def set_time_option(step, which_time, value):
    """
    Change values of rapid-commit and other options that can be set on true or false.
    """
    which_time, value = test_define_value(which_time, value)
    dhcpfun.set_time(step, which_time, value)


@step('Run configuration command: (.+)')
def run_command(step, command):
    """
    Add single line to configuration, there is no validation within this step.
    Be aware what you are putting this and in what moment. If you use that
    I recommend set variable "SAVE_CONFIG_FILES" to True.

    Includes everything after "command: " to the end of the line.
    """
    command = test_define_value(command)[0]
    dhcpfun.run_command(step, command)


##subnet options
@step('Server is configured with (\S+) option in subnet (\d+) with value (\S+).')
def config_srv(step, option_name, subnet, option_value):
    """
    Prepare server configuration with the specified option.
    option_name name of the option, e.g. dns-servers (number may be used here)
    option_value value of the configuration
    """
    dhcpfun.prepare_cfg_add_option_subnet(step, option_name, subnet, option_value)


@step('Server is configured with client-classification option in subnet (\d+) with name (\S+).')
def config_client_classification(step, subnet, option_value):
    """
    """
    dhcpfun.config_client_classification(step, subnet, option_value)


##server management
@step('(Server is started.)|(Server failed to start. During (\S+) process.)')
def start_srv(step, started, failed, process):
    """
    Decide which you want, start server of failed start (testing incorrect configuration)
    Also decide in which part should it failed.
    """
    # pass True for 'Server is started' and False for 'Server failed to start.'
    start = True if started is not None else False
    dhcpfun.start_srv(start, process)


@step('Restart server.')
def restart_srv(step):
    """
    Restart DHCPv6 without changing server configuration
    """
    dhcpfun.restart_srv()


@step('Server is stopped.')
def stop_srv(step):
    """
    For test that demands turning off server in the middle
    """
    dhcpfun.stop_srv()

##DDNS server
@step('DDNS server is configured on address (\S+) and port (\S+).')
def add_ddns_server(step, address, port):
    ddns_block()
    ddns.add_ddns_server(address, port)


@step('Add forward DDNS with name (\S+), key (\S+) on address (\S+) and port (\S+).')
def add_forward_ddns(step, name, key_name, ipaddress, port):
    ddns_block()
    ddns.add_forward_ddns(name, key_name, ipaddress, port)


@step('Add reverse DDNS with name (\S+) on address (\S+) and port (\S+).')
def add_reverse_ddns(step, name, ipaddress, port):
    ddns_block()
    ddns.add_reverse_ddns(name, ipaddress, port)


@step('Add DDNS key named (\S+) based on (\S+) with secret value (\S+).')
def add_keys(step, name, algorithm, secret):
    ddns_block()
    ddns.add_keys(secret, name, algorithm)

@step('Log MUST (NOT )?contain line: (.+)')
def log_includes_line(step, condition, line):
    """
    Check if Log includes line.
    Be aware that tested line is every thing after "line: " until end of the line.
    """
    line = test_define_value(line)[0]
    dhcpfun.log_contains(step, condition, line)
