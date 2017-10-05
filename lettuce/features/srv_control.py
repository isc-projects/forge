# Copyright (C) 2013-2017 Internet Systems Consortium.
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
from terrain import declare_all
import importlib

DHCP = world.f_cfg.dhcp_used
DNS = world.f_cfg.dns_used
declare_all()

for each_server_name in SOFTWARE_UNDER_TEST:
    if each_server_name in DHCP:
        dhcp = importlib.import_module("softwaresupport.%s.functions" % each_server_name)
        world.cfg["dhcp_under_test"] = each_server_name
        ddns_enable = True
        mysql_reservation_enable = True
        pgsql_reservation_enable = True
        try:
            ddns = importlib.import_module("softwaresupport.%s.functions_ddns" % each_server_name)
        except ImportError:
            ddns_enable = False
        try:
            mysql_reservation = importlib.import_module("softwaresupport.%s.mysql_reservation" % each_server_name)
        except ImportError:
            mysql_reservation_enable = False
        try:
            pgsql_reservation = importlib.import_module("softwaresupport.%s.pgsql_reservation" % each_server_name)
        except ImportError:
            pgsql_reservation_enable = False
    elif each_server_name in DNS:
        try:
            dns = importlib.import_module("softwaresupport.%s.functions" % each_server_name)
            world.cfg["dns_under_test"] = each_server_name
        except ImportError:
            dns_enable = False


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
        Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)my_file

    $ sign is very important without it Forge wont find variable in init_all.

    There is no slash ("/") between $(SOFTWARE_INSTALL_DIR) and my_file because variable $(SOFTWARE_INSTALL_DIR)
    should end with slash.

    You can use any variable form init_all in that way. Also you can add them using step:
    "Client defines new variable: (\S+) with value (\S+)."

    """
    tested_args = []
    for i in range(len(args)):
        imported = None
        front = None
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
                imported = getattr(world.f_cfg, tmp[2: index].lower())
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


##DHCP server configurations
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
    subnet, pool = test_define_value(subnet, pool)
    dhcp.prepare_cfg_subnet(step, subnet, pool)


@step('Server is configured with another subnet on interface (\S+) with (\S+) subnet and (\S+) pool.')
def config_srv_another_subnet(step, interface, subnet, pool):
    """
    Add another subnet with specified subnet/pool/interface.
    """
    subnet, pool, interface = test_define_value(subnet, pool, interface)
    dhcp.config_srv_another_subnet(step, subnet, pool, interface)


@step('Server is configured with another subnet: (\S+) with (\S+) pool.')
def config_srv_another_subnet_no_interface(step, subnet, pool):
    """
    Add another subnet to config file without interface specified.
    """
    subnet, pool = test_define_value(subnet, pool)
    dhcp.config_srv_another_subnet(step, subnet, pool, None)


@step('Server is configured with (\S+) prefix in subnet (\d+) with (\d+) prefix length and (\d+) delegated prefix length.')
def config_srv_prefix(step, prefix, subnet, length, delegated_length):
    """
    Adds server configuration with specified prefix.
    """
    prefix, length, delegated_length, subnet = test_define_value(prefix, length, delegated_length, subnet)
    dhcp.prepare_cfg_prefix(step, prefix, length, delegated_length, subnet)


@step('Server-id configured with type (\S+) value (\S+).')
def config_srv_id(step, id_type, id_value):
    """
    Adds server configuration with specified prefix.
    """
    id_type, id_value = test_define_value(id_type, id_value)
    dhcp.config_srv_id(str(id_type), str(id_value))


@step('Next server value on subnet (\d+) is configured with address (\S+).')
def subnet_add_siaddr(step, subnet_number, addr):
    addr, subnet_number = test_define_value(addr, subnet_number)
    dhcp.add_siaddr(step, addr, subnet_number)


@step('Next server global value is configured with address (\S+).')
def global_add_siaddr(step, addr):
    addr = test_define_value(addr)[0]
    dhcp.add_siaddr(step, addr, None)


@step('Server is configured with (\S+) option with value (\S+).')
def config_srv_opt(step, option_name, option_value):
    """
    Add to configuration options like: preference, dns servers..
    This step causes to set in to main space!
    """
    option_name, option_value = test_define_value(option_name, option_value)
    dhcp.prepare_cfg_add_option(step, option_name, option_value, world.cfg["space"])


@step('On space (\S+) server is configured with (\S+) option with value (\S+).')
def config_srv_opt_space(step, space, option_name, option_value):
    """
    Add to configuration options like: preference, dns servers.. but you can specify
    to which space should that be included.
    """
    option_name, option_value, space = test_define_value(option_name, option_value, space)
    dhcp.prepare_cfg_add_option(step, option_name, option_value, space)


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
    dhcp.prepare_cfg_add_custom_option(step, opt_name, opt_code, opt_type, opt_value, world.cfg["space"])


@step('On space (\S+) server is configured with a custom option (\S+)/(\d+) with type (\S+) and value (\S+).')
def config_srv_custom_opt_space(step, space, opt_name, opt_code, opt_type, opt_value):
    """
    Same step like "Server is configured with custom option.." but specify that option on different space then main.
    """
    opt_name, opt_code, opt_type, opt_value, space = test_define_value(opt_name, opt_code, opt_type, opt_value, space)
    dhcp.prepare_cfg_add_custom_option(step, opt_name, opt_code, opt_type, opt_value, space)


@step('Time (\S+) is configured with value (\S+).')
def set_time(step, which_time, value):
    """
    Change values of T1, T2, preffered lifetime and valid lifetime.
    """
    which_time, value = test_define_value(which_time, value)
    dhcp.set_time(step, which_time, value, None)


@step('Time (\S+) is not configured.')
def unset_time(step, which_time):
    """
    Remove default values of T1, T2, preferred lifetime and valid lifetime.
    """
    which_time = test_define_value(which_time)[0]
    dhcp.unset_time(step, which_time)


@step('Option (\S+) is configured with value (\S+).')
def set_time_option(step, which_time, value):
    """
    Change values of rapid-commit and other options that can be set on true or false.
    """
    which_time, value = test_define_value(which_time, value)
    dhcp.set_time(step, which_time, value)


@step('Add configuration parameter (\S+) with value (\S+) to global configuration.')
def set_conf_parameter_global(step, parameter_name, value):
    """
    Can be used on the end of configuration process, just before starting server.
    :param step:
    :param parameter_name:
    :param value:
    :return:
    """
    parameter_name, value = test_define_value(parameter_name, value)
    dhcp.set_conf_parameter_global(parameter_name, value)


@step('Add configuration parameter (\S+) with value (\S+) to subnet (\d+) configuration.')
def set_conf_parameter_subnet(step, parameter_name, value, subnet_id):
    """
    Can be used on the end of configuration process, just before starting server.
    :param step:
    :param parameter_name:
    :param value:
    :return:
    """
    parameter_name, value, subnet_id = test_define_value(parameter_name, value, subnet_id)
    dhcp.set_conf_parameter_subnet(parameter_name, value, int(subnet_id))


@step('Run configuration command: (.+)')
def run_command(step, command):
    """
    Add single line to configuration, there is no validation within this step.
    Be aware what you are putting this and in what moment. If you use that
    I recommend set variable "SAVE_CONFIG_FILES" to True.

    Includes everything after "command: " to the end of the line.
    """
    command = test_define_value(command)[0]
    dhcp.add_line_in_global(command)


@step('Add to config file line: (.+)')
def add_line(step, command):
    """
    The same step as 'Run configuration command: (.+)'
    """
    dhcp.add_line_in_global(command)


@step('To global section of the config add file line: (.+)')
def add_line2(step, command):
    """
    The same step as 'Run configuration command: (.+)'
    """
    dhcp.add_line_in_global(command)


@step('To subnet (\d+) configuration section in the config file add line: (.+)')
def add_line_to_subnet(step, subnetid, command):
    """
    The same step as 'Run configuration command: (.+)'
    """
    dhcp.add_line_in_subnet(int(subnetid), command)


@step('Add hooks library located (\S+).')
def add_hooks(step, library_path):
    """
    Add hooks library to configuration. Only Kea.
    """
    library_path = test_define_value(library_path)[0]
    dhcp.add_hooks(library_path)


# MySQL
@step('Use (\S+) reservation system.')
def enable_db_backend_reservation(step, db_type):
    if db_type == 'MySQL':
        mysql_reservation.enable_db_backend_reservation()
        mysql_reservation.clear_all_reservations()
    elif db_type == 'PostgreSQL':
        pgsql_reservation.enable_db_backend_reservation()
        pgsql_reservation.clear_all_reservations()
    else:
        assert False, "Database type not recognised."


@step('Create new (\S+) reservation identified by (\S+) (\S+).')
def new_db_backend_reservation(step, db_type, reservation_identifier, reservation_identifier_value):
    if db_type == 'MySQL':
        mysql_reservation.new_db_backend_reservation(reservation_identifier, reservation_identifier_value)
    elif db_type == 'PostgreSQL':
        pgsql_reservation.new_db_backend_reservation(reservation_identifier, reservation_identifier_value)
    else:
        assert False, "Database type not recognised."



@step('Add (\S+) (\S+) to (\S+) reservation record id (\d+).')
def update_db_backend_reservation(step, field_name, field_value, db_type, reservation_record_id):
    if db_type == 'MySQL':
        mysql_reservation.update_db_backend_reservation(field_name, field_value, int(reservation_record_id))
    elif db_type == 'PostgreSQL':
        pgsql_reservation.update_db_backend_reservation(field_name, field_value, int(reservation_record_id))
    else:
        assert False, "Database type not recognised."


@step('Add IPv6 prefix reservation (\S+) (\d+) with iaid (\S+) to (\S+) record id (\d+).')
def ipv6_prefix_db_backend_reservation(step, reserved_prefix, reserved_prefix_len, reserved_iaid, db_type, reservation_record_id):

    if db_type == 'MySQL':
        mysql_reservation.ipv6_prefix_db_backend_reservation(reserved_prefix, reserved_prefix_len, reserved_iaid,
                                                         int(reservation_record_id))
    elif db_type == 'PostgreSQL':
        pgsql_reservation.ipv6_prefix_db_backend_reservation(reserved_prefix, reserved_prefix_len, reserved_iaid,
                                                         int(reservation_record_id))
    else:
        assert False, "Database type not recognised."


@step('Add IPv6 address reservation (\S+) with iaid (\S+) to (\S+) record id (\d+).')
def ipv6_address_db_backend_reservation(step, reserved_address, reserved_iaid, db_type, reservation_record_id):
    if db_type == 'MySQL':
        mysql_reservation.ipv6_address_db_backend_reservation(reserved_address, reserved_iaid, int(reservation_record_id))
    elif db_type == 'PostgreSQL':
        pgsql_reservation.ipv6_address_db_backend_reservation(reserved_address, reserved_iaid, int(reservation_record_id))
    else:
        assert False, "Database type not recognised."


@step('Add option reservation code (\S+) value (\S+) space (\S+) persistent (\d+) client class (\S+) subnet id (\d+) and scope (\S+) to (\S+) record id (\d+).')
def option_db_record_reservation(step, reserved_option_code, reserved_option_value, reserved_option_space,
                                 reserved_option_persistent, reserved_option_client_class, reserved_subnet_id,
                                 reserved_option_scope, db_type, reservation_record_id):
    if db_type == 'MySQL':
        mysql_reservation.option_db_record_reservation(reserved_option_code, reserved_option_value,
                                                       reserved_option_space, reserved_option_persistent,
                                                       reserved_option_client_class, reserved_subnet_id,
                                                       reserved_option_scope, int(reservation_record_id))
    elif db_type == 'PostgreSQL':
        pgsql_reservation.option_db_record_reservation(reserved_option_code, reserved_option_value,
                                                                         reserved_option_space,
                                                                         reserved_option_persistent,
                                                                         reserved_option_client_class,
                                                                         reserved_subnet_id,
                                                                         reserved_option_scope,
                                                                         int(reservation_record_id))
    else:
        assert False, "Database type not recognised."

@step('Dump all the reservation entries from (\S+) database.')
def upload_db_reservation(step, db_type):
    if db_type == 'MySQL':
        mysql_reservation.clear_all_reservations()
    elif db_type == 'PostgreSQL':
        pgsql_reservation.clear_all_reservations()
    else:
        assert False, "Database type not recognised."


@step('Upload hosts reservation to (\S+) database.')
def upload_db_reservation(step, db_type):
    if db_type == 'MySQL':
        mysql_reservation.upload_db_reservation()
    elif db_type == 'PostgreSQL':
        pgsql_reservation.upload_db_reservation()
    else:
        assert False, "Database type not recognised."
##endMySQL


@step('Reserve (\S+) (\S+) for host uniquely identified by (\S+) (\S+).')
def host_reservation(step, reservation_type, reserved_value, unique_host_value_type, unique_host_value):
    """
    Ability to configure simple host reservations.
    """
    reservation_type, reserved_value, unique_host_value_type, unique_host_value = test_define_value(reservation_type,
                                                                                                    reserved_value,
                                                                                                    unique_host_value_type,
                                                                                                    unique_host_value)
    dhcp.host_reservation(reservation_type, reserved_value, unique_host_value_type, unique_host_value, None)

##shared-subnet cfg
@step('Add subnet (\d+) to shared-subnet set (\d+).')
def shared_subnet(step, subnet_id, shared_subnet_id):
    """
    Configure shared subnets.
    """
    subnet_id, shared_subnet_id = test_define_value(subnet_id, shared_subnet_id)
    dhcp.add_to_shared_subnet(int(subnet_id), int(shared_subnet_id))


@step('Shared subnet (\d+) is configured with option line: (.+)')
def add_option_shared_subnet(step, shared_subnet_id, conf_line):
    shared_subnet_id, conf_line = test_define_value(shared_subnet_id, conf_line)
    dhcp.add_line_to_shared_subnet(shared_subnet_id, conf_line)


@step('Add configuration parameter (\S+) with value (\S+) to shared-subnet (\d+) configuration.')
def set_conf_parameter_shared_subnet(step, parameter_name, value, subnet_id):
    """
    Can be used on the end of configuration process, just before starting server.
    :param step:
    :param parameter_name:
    :param value:
    :return:
    """
    parameter_name, value, subnet_id = test_define_value(parameter_name, value, subnet_id)
    dhcp.set_conf_parameter_shared_subnet(parameter_name, value, int(subnet_id))


##subnet options
@step('Reserve (\S+) (\S+) in subnet (\d+) for host uniquely identified by (\S+) (\S+).')
def host_reservation(step, reservation_type, reserved_value, subnet, unique_host_value_type, unique_host_value):
    """
    Ability to configure simple host reservations in subnet.
    """
    reservation_type, reserved_value, unique_host_value_type, unique_host_value = test_define_value(reservation_type,
                                                                                                    reserved_value,
                                                                                                    unique_host_value_type,
                                                                                                    unique_host_value)
    dhcp.host_reservation(reservation_type, reserved_value, unique_host_value_type, unique_host_value, int(subnet))


@step('For host reservation entry no. (\d+) in subnet (\d+) add (\S+) with value (\S+).')
def host_reservation(step, reservation_number, subnet, reservation_type, reserved_value):
    """
    Ability to configure simple host reservations in subnet.
    """
    reservation_type, reserved_value = test_define_value(reservation_type, reserved_value)
    dhcp.host_reservation_extension(int(reservation_number), int(subnet), reservation_type, reserved_value)


@step('Time (\S+) in subnet (\d+) is configured with value (\d+).')
def set_time(step, which_time, subnet, value):
    """
    Change values of T1, T2, preffered lifetime and valid lifetime.
    """
    which_time, subnet, value = test_define_value(which_time, subnet, value)
    dhcp.set_time(step, which_time, value, subnet)


@step('Server is configured with another pool (\S+) in subnet (\d+).')
def new_pool(step, pool, subnet):
    dhcp.add_pool_to_subnet(step, pool, int(subnet))


@step('Server is configured with (\S+) option in subnet (\d+) with value (\S+).')
def config_srv(step, option_name, subnet, option_value):
    """
    Prepare server configuration with the specified option.
    option_name name of the option, e.g. dns-servers (number may be used here)
    option_value value of the configuration
    """
    dhcp.prepare_cfg_add_option_subnet(step, option_name, subnet, option_value)


@step('On space (\S+) server is configured with (\S+) option in subnet (\d+) with value (\S+).')
def config_srv(step, space, option_name, subnet, option_value):
    """
    Prepare server configuration with the specified option.
    option_name name of the option, e.g. dns-servers (number may be used here)
    option_value value of the configuration
    """
    dhcp.prepare_cfg_add_option_subnet(step, option_name, subnet, option_value, space)


@step('Server is configured with client-classification option in subnet (\d+) with name (\S+).')
def config_client_classification(step, subnet, option_value):
    """
    """
    dhcp.config_client_classification(step, subnet, option_value)


@step('Server has control channel on (\S+) socket with name (\S+).')
def open_control_channel(step, socket_type, socket_name):
    """
    """
    socket_type, socket_name = test_define_value(socket_type, socket_name)
    dhcp.open_control_channel_socket(socket_type, socket_name)

@step('Server has control agent configured on HTTP connection with address (\S+):(\S+) and socket (\S+) path: (\S+).')
def agent_control_channel(step, host_address, host_port, socket_type, socket_name):
    """
    """
    host_address, host_port, socket_type, socket_name = test_define_value(host_address, host_port, socket_type, socket_name)
    dhcp.agent_control_channel(host_address, host_port, socket_type, socket_name)


##DNS server configuration
@step('DNS server is configured on (\S+) address (\S+) on port no. (\d+) and working directory (\S+).')
def dns_conf(step, ip_type, address, port, direct):
    ip_type, address, port, direct = test_define_value(ip_type, address, port, direct)
    dns.add_defaults(ip_type, address, port, direct)


@step('DNS server is configured with zone (\S+) with type: (\S+) file: (\S+) with dynamic update key: (\S+).')
def add_zone(step, zone, zone_type, file_nem, key):
    zone, zone_type, file_nem, key = test_define_value(zone, zone_type, file_nem, key)
    dns.add_zone(zone, zone_type, file_nem, key)


@step('Add DNS key named: (\S+) algorithm: (\S+) and value: (\S+).')
def dns_add_key(step, key_name, algorithm, key_value):
    key_name, algorithm, key_value = test_define_value(key_name, algorithm, key_value)
    dns.add_key(key_name, algorithm, key_value)


@step('Add DNS rndc-key on address (\S+) and port (\d+). Using algorithm: (\S+) with value: (\S+)')
def dns_rest(step, address, port, alg, value):
    address, port, alg, value = test_define_value(address, port, alg, value)
    dns.add_rndc(address, port, alg, value)


@step('Server logging system is configured with logger type (\S+), severity (\S+), severity level (\S+) and log file (\S+).')
def configure_loggers(step, log_type, severity, severity_level, logging_file):
    log_type, severity, severity_level, logging_file = test_define_value(log_type, severity,
                                                                         severity_level, logging_file)
    dhcp.add_logger(log_type, severity, severity_level, logging_file)


##servers management
@step('Send server configuration using (\S+) and (\S+).')
def build_and_send_config_files(step, connection_type, configuration_type):
    """
    Step used to choosing configuration type and channel to send it.
    :param step:
    :param connection_type:
    :param configuration_type:
    """
    connection_type, configuration_type = test_define_value(connection_type, configuration_type)
    dhcp.build_and_send_config_files(connection_type, configuration_type)


@step('Generate server configuration file.')
def generate_config_files(step):
    dhcp.build_and_send_config_files(connection_type=None, configuration_type="config-file")


@step('(\S+) server is started.')
def start_srv(step, name):
    """
    Decide which you want, start server of failed start (testing incorrect configuration)
    Also decide in which part should it failed.
    """
    if name == "DHCP":
        dhcp.start_srv(True, None)
    elif name == "DNS":
        dns.start_srv(True, None)
    else:
        assert False, "I don't think there is support for something else than DNS or DHCP"


@step('(\S+) server failed to start. During (\S+) process.')
def start_srv(step, name, process):
    """
    Decide which you want, start server of failed start (testing incorrect configuration)
    Also decide in which part should it failed.
    """
    if name == "DHCP":
        dhcp.start_srv(False, process)
    elif name == "DNS":
        dns.start_srv(False, process)
    else:
        assert False, "I don't think there is support for something else than DNS or DHCP"


@step('Restart (\S+) server.')
def restart_srv(step, name):
    """
    Restart DHCP/DNS server without reconfiguration.
    """
    if name == "DHCP":
        dhcp.restart_srv()
    elif name == "DNS":
        dns.restart_srv()
    else:
        assert False, "I don't think there is support for something else than DNS or DHCP"


@step('Reconfigure (\S+) server.')
def restart_srv(step, name):
    """
    Reconfigure DHCP/DNS server.
    """
    if name == "DHCP":
        dhcp.reconfigure_srv()
    elif name == "DNS":
        dns.reconfigure_srv()
    else:
        assert False, "I don't think there is support for something else than DNS or DHCP"


@step('(\S+) server is stopped.')
def stop_srv(step, name):
    """
    For test that demands turning off server in the middle
    """
    if name == "DHCP":
        dhcp.stop_srv()
    elif name == "DNS":
        dns.stop_srv()
    else:
        assert False, "I don't think there is support for something else than DNS or DHCP"


@step('Clear leases.')
def clear_leases(step):
    dhcp.clear_leases()


##DDNS server
@step('DDNS server is configured on (\S+) address and (\S+) port.')
def add_ddns_server(step, address, port):
    ddns_block()
    address, port = test_define_value(address, port)
    ddns.add_ddns_server(address, port)


@step('DDNS server is configured with (\S+) option set to (\S+).')
def add_ddns_server_options(step, option, value):
    ddns_block()
    option, value = test_define_value(option, value)
    ddns.add_ddns_server_options(option, value)


@step('Add forward DDNS with name (\S+) and key (\S+) on address (\S+) and port (\S+).')
def add_forward_ddns(step, name, key_name, ipaddress, port):
    ddns_block()
    ddns.add_forward_ddns(name, key_name, ipaddress, port)


@step('Add reverse DDNS with name (\S+) and key (\S+) on address (\S+) and port (\S+).')
def add_reverse_ddns(step, name, key_name, ipaddress, port):
    ddns_block()
    ddns.add_reverse_ddns(name, key_name, ipaddress, port)


@step('Add DDNS key named (\S+) based on (\S+) with secret value (\S+).')
def add_keys(step, name, algorithm, secret):
    ddns_block()
    ddns.add_keys(secret, name, algorithm)


@step('Use DNS set no. (\d+).')
def log_includes_count(step, number):
    """
    Check if Log includes line.
    Be aware that tested line is every thing after "line: " until end of the line.
    """
    dns.use_config_set(int(number))
