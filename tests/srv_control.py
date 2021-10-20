# Copyright (C) 2013-2020 Internet Systems Consortium.
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

import sys
import json
import logging
import importlib

from forge_cfg import world, step

import softwaresupport.bind9_server.functions as dns
from protosupport.multi_protocol_functions import test_define_value

log = logging.getLogger('forge')


class Dispatcher(object):
    def __init__(self, mod_name):
        self.mod_name = mod_name

    def __getattr__(self, attr_name):
        if any(('isc_dhcp' in s for s in world.f_cfg.software_under_test)):
            if world.f_cfg.proto == 'v4':
                server_name = 'isc_dhcp4_server'
            else:
                server_name = 'isc_dhcp6_server'
        else:
            if world.f_cfg.proto == 'v4':
                server_name = 'kea4_server'
            else:
                server_name = 'kea6_server'

        full_mod_name = "softwaresupport.%s.%s" % (server_name, self.mod_name)
        mod = importlib.import_module(full_mod_name)

        return getattr(mod, attr_name)


dhcp = Dispatcher('functions')
ddns = Dispatcher('functions_ddns')
mysql_reservation = Dispatcher('mysql_reservation')
pgsql_reservation = Dispatcher('pgsql_reservation')
cql_reservation = Dispatcher('cql_reservation')


##DHCP server configurations
@step(r'Server is configured with (\S+) subnet with (\S+) pool.')
def config_srv_subnet(subnet, pool, eth=None):
    """
    Adds server configuration with specified subnet and pool.
    subnet may define specific subnet or use the word "default"
    pool may define specific pool range or use the word "default"

    Setting subnet in that way, will cause to set in on interface you set in
    init_all.py as variable "SERVER_IFACE" leave it to None if you don want to set
    interface.
    """
    subnet, pool, eth = test_define_value(subnet, pool, eth)
    dhcp.prepare_cfg_subnet(subnet, pool, eth=eth)


@step(r'Server is configured on interface (\S+) and address (\S+) with (\S+) subnet with (\S+) pool.')
def config_srv_subnet_with_iface(interface, address, subnet, pool):
    """
    Adds server configuration with specified subnet and pool.
    subnet may define specific subnet or use the word "default"
    pool may define specific pool range or use the word "default"

    Setting subnet in that way, will cause to set in on interface you set in
    init_all.py as variable "SERVER_IFACE" leave it to None if you don want to set
    interface.
    """
    interface, address, subnet, pool = test_define_value(interface, address, subnet, pool)
    dhcp.prepare_cfg_subnet_specific_interface(interface, address, subnet, pool)


@step(r'Server is configured with another subnet on interface (\S+) with (\S+) subnet and (\S+) pool.')
def config_srv_another_subnet(interface, subnet, pool):
    """
    Add another subnet with specified subnet/pool/interface.
    """
    subnet, pool, interface = test_define_value(subnet, pool, interface)
    dhcp.config_srv_another_subnet(subnet, pool, interface)


@step(r'Server is configured with another subnet: (\S+) with (\S+) pool.')
def config_srv_another_subnet_no_interface(subnet, pool):
    """
    Add another subnet to config file without interface specified.
    """
    subnet, pool = test_define_value(subnet, pool)
    dhcp.config_srv_another_subnet(subnet, pool, None)


@step(r'Server is configured with (\S+) prefix in subnet (\d+) with (\d+) prefix length and (\d+) delegated prefix length.')
def config_srv_prefix(prefix, subnet, length, delegated_length):
    """
    Adds server configuration with specified prefix.
    """
    prefix, length, delegated_length, subnet = test_define_value(prefix, length, delegated_length, subnet)
    dhcp.prepare_cfg_prefix(prefix, length, delegated_length, subnet)


@step(r'Server-id configured with type (\S+) value (\S+).')
def config_srv_id(id_type, id_value):
    """
    Adds server configuration with specified prefix.
    """
    id_type, id_value = test_define_value(id_type, id_value)
    dhcp.config_srv_id(str(id_type), str(id_value))


@step(r'Next server value on subnet (\d+) is configured with address (\S+).')
def subnet_add_siaddr(subnet_number, addr):
    addr, subnet_number = test_define_value(addr, subnet_number)
    dhcp.add_siaddr(addr, subnet_number)


@step(r'Next server global value is configured with address (\S+).')
def global_add_siaddr(addr):
    addr = test_define_value(addr)[0]
    dhcp.add_siaddr(addr, None)


@step(r'Server is configured with (\S+) option with value (\S+).')
def config_srv_opt(option_name, option_value):
    """
    Add to configuration options like: preference, dns servers..
    This step causes to set in to main space!
    """
    option_name, option_value = test_define_value(option_name, option_value)
    dhcp.prepare_cfg_add_option(option_name, option_value, world.cfg["space"])


@step(r'On space (\S+) server is configured with (\S+) option with value (\S+).')
def config_srv_opt_space(space, option_name, option_value):
    """
    Add to configuration options like: preference, dns servers.. but you can specify
    to which space should that be included.
    """
    option_name, option_value, space = test_define_value(option_name, option_value, space)
    dhcp.prepare_cfg_add_option(option_name, option_value, space)


@step(r'Server is configured with custom option (\S+)/(\d+) with type (\S+) and value (\S+).')
def config_srv_custom_opt(opt_name, opt_code, opt_type, opt_value):
    """
    Prepare server configuration with the specified custom option.
    opt_name name of the option, e.g. foo
    opt_code code of the option, e.g. 100
    opt_type type of the option, e.g. uint8 (see bind10 guide for complete list)
    opt_value value of the option, e.g. 1
    """
    opt_name, opt_code, opt_type, opt_value = test_define_value(opt_name, opt_code, opt_type, opt_value)
    dhcp.prepare_cfg_add_custom_option(opt_name, opt_code, opt_type, opt_value, world.cfg["space"])


@step(r'On space (\S+) server is configured with a custom option (\S+)/(\d+) with type (\S+) and value (\S+).')
def config_srv_custom_opt_space(space, opt_name, opt_code, opt_type, opt_value):
    """
    Same step like "Server is configured with custom option.." but specify that option on different space then main.
    """
    opt_name, opt_code, opt_type, opt_value, space = test_define_value(opt_name, opt_code, opt_type, opt_value, space)
    dhcp.prepare_cfg_add_custom_option(opt_name, opt_code, opt_type, opt_value, space)


@step(r'Time (\S+) is configured with value (\S+).')
def set_time(which_time, value):
    """
    Change values of T1, T2, preffered lifetime and valid lifetime.
    """
    which_time, value = test_define_value(which_time, value)
    dhcp.set_time(which_time, value, None)


@step(r'Option (\S+) is configured with value (\S+).')
def set_time_option(which_time, value):
    """
    Change values of rapid-commit and other options that can be set on true or false.
    """
    which_time, value = test_define_value(which_time, value)
    dhcp.set_time(which_time, value)


@step(r'Add configuration parameter (\S+) with value (\S+) to global configuration.')
def set_conf_parameter_global(parameter_name, value):
    """
    Can be used on the end of configuration process, just before starting server.
    :param step:
    :param parameter_name:
    :param value:
    :return:
    """
    # parameter_name, value = test_define_value(parameter_name, value)
    dhcp.set_conf_parameter_global(parameter_name, value)


@step(r'Add configuration parameter (\S+) with value (\S+) to subnet (\d+) configuration.')
def set_conf_parameter_subnet(parameter_name, value, subnet_id):
    """
    Can be used on the end of configuration process, just before starting server.
    :param step:
    :param parameter_name:
    :param value:
    :return:
    """
    parameter_name, value, subnet_id = test_define_value(parameter_name, value, subnet_id)
    dhcp.set_conf_parameter_subnet(parameter_name, value, int(subnet_id))


@step(r'Add to config file line: (.+)')
def add_line(command):
    """
    The same step as 'Run configuration command: (.+)'
    """
    dhcp.add_line_in_global(command)


@step(r'To subnet (\d+) configuration section in the config file add line: (.+)')
def add_line_to_subnet(subnetid, command):
    test_define_value(command)
    dhcp.add_line_in_subnet(int(subnetid), command)


@step(r'Add hooks library located (\S+).')
def add_hooks(library_path):
    """
    Add hooks library to configuration. Only Kea.
    """
    full_library_path = world.f_cfg.hooks_join(library_path)
    dhcp.add_hooks(full_library_path)


@step(r'To hook no. (\d+) add parameter named (\S+) with value: (.+)')
def add_parameter_to_hook(hook_no, parameter_name, parameter_value):
    parameter_name, parameter_value = test_define_value(parameter_name, parameter_value)
    dhcp.add_parameter_to_hook(int(hook_no), parameter_name, parameter_value)


@step(r'Add High-Availability hook library located (\S+).')
def add_ha_hook(library_path):
    full_library_path = world.f_cfg.hooks_join(library_path)
    dhcp.ha_add_parameter_to_hook("lib", full_library_path)
    dhcp.add_hooks(full_library_path)


@step(r'To HA hook configuration add (\S+) with value: (.+)')
def add_parameter_to_ha_hook(parameter_name, parameter_value):
    parameter_name, parameter_value = test_define_value(parameter_name, parameter_value)
    dhcp.ha_add_parameter_to_hook(parameter_name, parameter_value)


def update_ha_hook_parameter(param):
    dhcp.update_ha_hook_parameter(param)


def build_database(dest=world.f_cfg.mgmt_address, db_name=world.f_cfg.db_name,
                   db_user=world.f_cfg.db_user, db_passwd=world.f_cfg.db_passwd,
                   init_db=True, disable=False):
    dest, db_name, db_user, db_passwd = test_define_value(dest, db_name, db_user, db_passwd)
    dhcp.db_setup(dest=dest, db_name=db_name, db_user=db_user, db_passwd=db_passwd, init_db=init_db, disable=disable)


@step(r'Use (\S+) as lease database backend.')
def define_temporary_lease_db_backend(lease_db_type):
    lease_db_type = test_define_value(lease_db_type)[0]
    world.f_cfg.db_type = lease_db_type


@step(r'Credentials for (\S+) database. User: (\S+); Passwd: (\S+); DB-name: (\S+); Host: (\S+);')
def define_temporary_lease_db_backend_credentials(db_type, tmp_db_user, tmp_db_passwd, tmp_db_name, tmp_db_host):
    # for now it's just support for leases.
    if world.f_cfg.tmp_db_type is None:
        assert False, "You should put 'Use (\S+) as lease database backend.' step first!"
    if db_type not in ["leases"]:  # , "reservation"]:
        assert False, "For this time we can use just 'leases'. 'reservation' is not available here."
    world.f_cfg.db_host = tmp_db_host
    world.f_cfg.db_name = tmp_db_name
    world.f_cfg.db_passwd = tmp_db_passwd
    world.f_cfg.db_user = tmp_db_user


# START Reservation backend section
@step(r'Use (\S+) reservation system.')
def enable_db_backend_reservation(db_type):
    # for now we are not implementing new configuration system for this one host reservation in databases
    if db_type == 'MySQL':
        mysql_reservation.enable_db_backend_reservation()
        mysql_reservation.clear_all_reservations()
    elif db_type == 'PostgreSQL':
        pgsql_reservation.enable_db_backend_reservation()
        pgsql_reservation.clear_all_reservations()
    elif db_type == 'Cassandra':
        cql_reservation.enable_db_backend_reservation()
        cql_reservation.clear_all_reservations()
    elif db_type == "memfile":
        pass
    else:
        assert False, "Database type not recognised."


@step(r'Create new (\S+) reservation identified by (\S+) (\S+).')
def new_db_backend_reservation(db_type, reservation_identifier, reservation_identifier_value):
    if db_type == 'MySQL':
        mysql_reservation.new_db_backend_reservation(reservation_identifier, reservation_identifier_value)
    elif db_type == 'PostgreSQL':
        pgsql_reservation.new_db_backend_reservation(reservation_identifier, reservation_identifier_value)
    elif db_type == 'Cassandra':
        cql_reservation.new_db_backend_reservation(reservation_identifier, reservation_identifier_value)
    else:
        assert False, "Database type not recognised."


@step(r'Add (\S+) (\S+) to (\S+) reservation record id (\d+).')
def update_db_backend_reservation(field_name, field_value, db_type, reservation_record_id):
    if db_type == 'MySQL':
        mysql_reservation.update_db_backend_reservation(field_name, field_value, int(reservation_record_id))
    elif db_type == 'PostgreSQL':
        pgsql_reservation.update_db_backend_reservation(field_name, field_value, int(reservation_record_id))
    elif db_type == 'Cassandra':
        cql_reservation.update_db_backend_reservation(field_name, field_value, int(reservation_record_id))
    else:
        assert False, "Database type not recognised."


@step(r'Add IPv6 prefix reservation (\S+) (\d+) with iaid (\S+) to (\S+) record id (\d+).')
def ipv6_prefix_db_backend_reservation(reserved_prefix, reserved_prefix_len,
                                       reserved_iaid, db_type, reservation_record_id):

    if db_type == 'MySQL':
        mysql_reservation.ipv6_prefix_db_backend_reservation(reserved_prefix, reserved_prefix_len, reserved_iaid,
                                                             int(reservation_record_id))
    elif db_type == 'PostgreSQL':
        pgsql_reservation.ipv6_prefix_db_backend_reservation(reserved_prefix, reserved_prefix_len, reserved_iaid,
                                                             int(reservation_record_id))
    elif db_type == 'Cassandra':
        cql_reservation.ipv6_prefix_db_backend_reservation(reserved_prefix, reserved_prefix_len, reserved_iaid,
                                                           int(reservation_record_id))
    else:
        assert False, "Database type not recognised."


@step(r'Add IPv6 address reservation (\S+) with iaid (\S+) to (\S+) record id (\d+).')
def ipv6_address_db_backend_reservation(reserved_address, reserved_iaid, db_type, reservation_record_id):
    if db_type == 'MySQL':
        mysql_reservation.ipv6_address_db_backend_reservation(reserved_address, reserved_iaid,
                                                              int(reservation_record_id))
    elif db_type == 'PostgreSQL':
        pgsql_reservation.ipv6_address_db_backend_reservation(reserved_address, reserved_iaid,
                                                              int(reservation_record_id))
    elif db_type == 'Cassandra':
        cql_reservation.ipv6_address_db_backend_reservation(reserved_address, reserved_iaid,
                                                            int(reservation_record_id))
    else:
        assert False, "Database type not recognised."


@step(r'Add option reservation code (\S+) value (\S+) space (\S+) persistent (\d+) client class (\S+) subnet id (\d+) and scope (\S+) to (\S+) record id (\d+).')
def option_db_record_reservation(reserved_option_code, reserved_option_value, reserved_option_space,
                                 reserved_option_persistent, reserved_option_client_class, reserved_subnet_id,
                                 reserved_option_scope, db_type, reservation_record_id):
    if db_type == 'MySQL':
        mysql_reservation.option_db_record_reservation(reserved_option_code, reserved_option_value,
                                                       reserved_option_space, reserved_option_persistent,
                                                       reserved_option_client_class, reserved_subnet_id,
                                                       reserved_option_scope, int(reservation_record_id))
    elif db_type == 'PostgreSQL':
        pgsql_reservation.option_db_record_reservation(reserved_option_code, reserved_option_value,
                                                       reserved_option_space, reserved_option_persistent,
                                                       reserved_option_client_class, reserved_subnet_id,
                                                       reserved_option_scope, int(reservation_record_id))
    elif db_type == 'Cassandra':
        cql_reservation.option_db_record_reservation(reserved_option_code, reserved_option_value,
                                                     reserved_option_space, reserved_option_persistent,
                                                     reserved_option_client_class, reserved_subnet_id,
                                                     reserved_option_scope, int(reservation_record_id))
    else:
        assert False, "Database type not recognised."


@step(r'Dump all the reservation entries from (\S+) database.')
def dump_db_reservation(db_type):
    if db_type == 'MySQL':
        mysql_reservation.clear_all_reservations()
    elif db_type == 'PostgreSQL':
        pgsql_reservation.clear_all_reservations()
    elif db_type == 'Cassandra':
        cql_reservation.clear_all_reservations()
    else:
        assert False, "Database type not recognised."


@step(r'Upload hosts reservation to (\S+) database.')
def upload_db_reservation(db_type, exp_failed=False):
    if db_type == 'MySQL':
        mysql_reservation.upload_db_reservation(exp_failed)
    elif db_type == 'PostgreSQL':
        pgsql_reservation.upload_db_reservation(exp_failed)
    elif db_type == 'Cassandra':
        cql_reservation.upload_db_reservation(exp_failed)
    else:
        assert False, "Database type not recognised."
# END Reservation backend section


@step(r'Reserve (\S+) (\S+) for host uniquely identified by (\S+) (\S+).')
def host_reservation(reservation_type, reserved_value, unique_host_value_type, unique_host_value):
    """
    Ability to configure simple host reservations.
    """
    reservation_type, reserved_value, unique_host_value_type, unique_host_value = test_define_value(reservation_type,
                                                                                                    reserved_value,
                                                                                                    unique_host_value_type,
                                                                                                    unique_host_value)
    dhcp.host_reservation(reservation_type, reserved_value, unique_host_value_type, unique_host_value, None)


##shared-subnet cfg
@step(r'Add subnet (\d+) to shared-subnet set (\d+).')
def shared_subnet(subnet_id, shared_subnet_id):
    """
    Configure shared subnets.
    """
    subnet_id, shared_subnet_id = test_define_value(subnet_id, shared_subnet_id)
    dhcp.add_to_shared_subnet(subnet_id, int(shared_subnet_id))


@step(r'Shared subnet (\d+) is configured with option line: (.+)')
def add_option_shared_subnet(shared_subnet_id, conf_line):
    shared_subnet_id, conf_line = test_define_value(shared_subnet_id, conf_line)
    dhcp.add_line_to_shared_subnet(shared_subnet_id, conf_line)


@step(r'Add configuration parameter (\S+) with value (\S+) to shared-subnet (\d+) configuration.')
def set_conf_parameter_shared_subnet(parameter_name, value, subnet_id):
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
@step(r'Reserve (\S+) (\S+) in subnet (\d+) for host uniquely identified by (\S+) (\S+).')
def host_reservation_in_subnet(reservation_type, reserved_value, subnet, unique_host_value_type, unique_host_value):
    """
    Ability to configure simple host reservations in subnet.
    """
    reservation_type, reserved_value, unique_host_value_type, unique_host_value = test_define_value(reservation_type,
                                                                                                    reserved_value,
                                                                                                    unique_host_value_type,
                                                                                                    unique_host_value)
    dhcp.host_reservation(reservation_type, reserved_value, unique_host_value_type, unique_host_value, int(subnet))


@step(r'For host reservation entry no. (\d+) in subnet (\d+) add (\S+) with value (\S+).')
def host_reservation_in_subnet_add_value(reservation_number, subnet, reservation_type, reserved_value):
    """
    Ability to configure simple host reservations in subnet.
    """
    reservation_type, reserved_value = test_define_value(reservation_type, reserved_value)
    dhcp.host_reservation_extension(int(reservation_number), int(subnet), reservation_type, reserved_value)


@step(r'Time (\S+) in subnet (\d+) is configured with value (\d+).')
def set_time_in_subnet(which_time, subnet, value):
    """
    Change values of T1, T2, preffered lifetime and valid lifetime.
    """
    which_time, subnet, value = test_define_value(which_time, subnet, value)
    dhcp.set_time(which_time, value, subnet)


@step(r'Server is configured with another pool (\S+) in subnet (\d+).')
def new_pool(pool, subnet):
    dhcp.add_pool_to_subnet(pool, int(subnet))


@step(r'Server is configured with (\S+) option in subnet (\d+) with value (\S+).')
def config_srv(option_name, subnet, option_value):
    """
    Prepare server configuration with the specified option.
    option_name name of the option, e.g. dns-servers (number may be used here)
    option_value value of the configuration
    """
    dhcp.prepare_cfg_add_option_subnet(option_name, subnet, option_value)


@step(r'On space (\S+) server is configured with (\S+) option in subnet (\d+) with value (\S+).')
def config_srv_on_space(space, option_name, subnet, option_value):
    """
    Prepare server configuration with the specified option.
    option_name name of the option, e.g. dns-servers (number may be used here)
    option_value value of the configuration
    """
    dhcp.prepare_cfg_add_option_subnet(option_name, subnet, option_value, space)


@step(r'Server is configured with client-classification option in subnet (\d+) with name (\S+).')
def config_client_classification(subnet, option_value):
    dhcp.config_client_classification(subnet, option_value)


@step(r'Server is configured with require-client-classification option in subnet (\d+) with name (\S+).')
def config_require_client_classification(subnet, option_value):
    dhcp.config_require_client_classification(subnet, option_value)


@step(r'Add class called (\S+).')
def create_new_class(class_name):
    dhcp.create_new_class(class_name)


@step(r'To class no (\d+) add parameter named: (\S+) with value: (.+)')
def add_test_to_class(class_number, parameter_name, parameter_value):
    if parameter_name == "test":
        parameter_name, parameter_value = test_define_value(parameter_name, parameter_value)
    dhcp.add_test_to_class(int(class_number), parameter_name, parameter_value)


@step(r'To class no (\d+) add option (\S+) with value (\S+).')
def add_option_to_defined_class(class_no, option, option_value):
    dhcp.add_option_to_defined_class(int(class_no), option, option_value)


@step(r'Server has control channel (\S+).')
def open_control_channel(socket_name=None):
    dhcp.open_control_channel_socket(socket_name)


@step(r'Server has control agent configured on HTTP connection with address (\S+):(\S+) and socket (\S+) path: (\S+).')
def agent_control_channel(host_address='$(MGMT_ADDRESS)', host_port=8000, socket_name='control_socket'):
    host_address, host_port = test_define_value(host_address, host_port)
    dhcp.agent_control_channel(host_address, host_port, socket_name)


##DNS server configuration
@step(r'DNS server is configured on (\S+) address (\S+) on port no. (\d+) and working directory (\S+).')
def dns_conf(ip_type, address, port, direct):
    ip_type, address, port, direct = test_define_value(ip_type, address, port, direct)
    dns.add_defaults(ip_type, address, port, direct)


@step(r'DNS server is configured with zone (\S+) with type: (\S+) file: (\S+) with dynamic update key: (\S+).')
def add_zone(zone, zone_type, file_nem, key):
    zone, zone_type, file_nem, key = test_define_value(zone, zone_type, file_nem, key)
    dns.add_zone(zone, zone_type, file_nem, key)


@step(r'Add DNS key named: (\S+) algorithm: (\S+) and value: (\S+).')
def dns_add_key(key_name, algorithm, key_value):
    key_name, algorithm, key_value = test_define_value(key_name, algorithm, key_value)
    dns.add_key(key_name, algorithm, key_value)


@step(r'Add DNS rndc-key on address (\S+) and port (\d+). Using algorithm: (\S+) with value: (\S+)')
def dns_rest(address, port, alg, value):
    address, port, alg, value = test_define_value(address, port, alg, value)
    dns.add_rndc(address, port, alg, value)


@step(r'Server logging system is configured with logger type (\S+), severity (\S+), severity level (\S+) and log file (\S+).')
def configure_loggers(log_type, severity, severity_level, logging_file=None):
    log_type, severity, severity_level = test_define_value(log_type, severity, severity_level)
    dhcp.add_logger(log_type, severity, severity_level, logging_file)


##servers management
@step(r'Create server configuration.')
def build_config_files(cfg=None):
    dhcp.build_config_files(cfg=cfg)


@step(r'Create and send server configuration.')
def build_and_send_config_files(cfg=None, dest=world.f_cfg.mgmt_address):
    dest = test_define_value(dest)[0]
    check_remote_address(dest)
    dhcp.build_and_send_config_files(cfg=cfg, destination_address=dest)


@step(r'(\S+) server is (started|stopped|restarted|reconfigured).')
def start_srv(name, type_of_action, config_set=None, dest=world.f_cfg.mgmt_address):
    """
    Decide which you want, start server of failed start (testing incorrect configuration)
    Also decide in which part should it failed.
    """
    dest = test_define_value(dest)[0]
    check_remote_address(dest)
    if name not in ["DHCP", "DNS"]:
        assert False, "I don't think there is support for something else than DNS or DHCP"
    if type_of_action == "started":
        if name == "DHCP":
            log.info('-----------------  KEA START %s -------------------------------------------------------', dest)
            dhcp.start_srv(True, None, destination_address=dest)
        elif name == "DNS":
            log.info('-----------------  BIND START %s -------------------------------------------------------', dest)
            if config_set is not None:
                use_dns_set_number(config_set)
            dns.start_srv(True, None, destination_address=dest)
    elif type_of_action == "stopped":
        if name == "DHCP":
            log.info('-----------------  KEA STOP %s  -------------------------------------------------------', dest)
            dhcp.stop_srv(destination_address=dest)
        elif name == "DNS":
            log.info('-----------------  BIND STOP %s  -------------------------------------------------------', dest)
            dns.stop_srv(destination_address=dest)
    elif type_of_action == "restarted":
        if name == "DHCP":
            log.info('-----------------  KEA RESTART %s  -------------------------------------------------------', dest)
            dhcp.restart_srv(destination_address=dest)
        elif name == "DNS":
            log.info('-----------------  BIND RESTART %s  -------------------------------------------------------', dest)
            dns.restart_srv(destination_address=dest)
    elif type_of_action == "reconfigured":
        if name == "DHCP":
            log.info('-----------------  KEA RECONFIG %s  -------------------------------------------------------', dest)
            dhcp.reconfigure_srv(destination_address=dest)
        elif name == "DNS":
            log.info('-----------------  BIND RECONFIG %s  -------------------------------------------------------', dest)
            dns.reconfigure_srv(destination_address=dest)
    else:
        assert False, "we don't support '%s' action." % str(type_of_action)


def check_remote_address(remote_address):
    """
    Add new remote server IP address as additional location, can be used for running dhcp server
    From all added locations all files on clean up will be downloaded to specific local location
    :param remote_address: IP address of remote vm
    :return: nothing
    """
    if remote_address not in world.f_cfg.multiple_tested_servers:
        world.f_cfg.multiple_tested_servers.append(remote_address)


@step(r'Remote (\S+) server is (started|stopped|restarted|reconfigured) on address (\S+).')
def remote_start_srv(name, type_of_action, destination_address):
    """
    Decide which you want, start server of failed start (testing incorrect configuration)
    Also decide in which part should it failed.
    """
    destination_address = test_define_value(destination_address)[0]
    check_remote_address(destination_address)
    if name not in ["DHCP", "DNS"]:
        assert False, "I don't think there is support for something else than DNS or DHCP"
    if type_of_action == "started":
        if name == "DHCP":
            dhcp.start_srv(True, None, destination_address)
        elif name == "DNS":
            dns.start_srv(True, None, destination_address)
    elif type_of_action == "stopped":
        if name == "DHCP":
            dhcp.stop_srv(destination_address=destination_address)
        elif name == "DNS":
            dns.stop_srv(destination_address=destination_address)
    elif type_of_action == "restarted":
        if name == "DHCP":
            dhcp.restart_srv(destination_address=destination_address)
        elif name == "DNS":
            dns.restart_srv(destination_address=destination_address)
    elif type_of_action == "reconfigured":
        if name == "DHCP":
            dhcp.reconfigure_srv(destination_address=destination_address)
        elif name == "DNS":
            dns.reconfigure_srv(destination_address=destination_address)
    else:
        assert False, "we don't support this action."


@step(r'(\S+) server failed to start. During (\S+) process.')
def start_srv_during_process(name, process):
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


@step(r'(\S+) server failed to start. During (\S+) process on remote destination (\S+).')
def start_srv_during_remote_process(name, process, destination_address):
    """
    Decide which you want, start server of failed start (testing incorrect configuration)
    Also decide in which part should it failed.
    """
    destination_address[0] = test_define_value(destination_address)
    check_remote_address(destination_address)
    if name == "DHCP":
        dhcp.start_srv(False, process, destination_address)
    elif name == "DNS":
        dns.start_srv(False, process, destination_address)
    else:
        assert False, "I don't think there is support for something else than DNS or DHCP"


@step(r'Add remote server with address: (\S+).')
def add_remote_server(remote_address):
    remote_address[0] = test_define_value(remote_address)
    check_remote_address(remote_address)


@step(r'Clear (\S+).')
def clear_some_data(data_type, service='dhcp', dest=world.f_cfg.mgmt_address,
                    software_install_path=world.f_cfg.software_install_path, db_user=world.f_cfg.db_user,
                    db_passwd=world.f_cfg.db_passwd, db_name=world.f_cfg.db_name):
    dest, db_name, db_user, db_passwd, install_path = test_define_value(dest, db_name, db_user,
                                                                        db_passwd, software_install_path)

    if service == 'dhcp':
        if data_type == "leases":
            dhcp.clear_leases(destination_address=dest, db_name=db_name, db_user=db_user, db_passwd=db_passwd)
        elif data_type == "logs":
            dhcp.clear_logs(destination_address=dest)
        elif data_type == "all":
            dhcp.clear_all(destination_address=dest, db_name=db_name, db_user=db_user, db_passwd=db_passwd)
    elif service.lower() == 'dns':
        # let's just dump all without logs
        dns.clear_all(remove_logs=False, destination_address=dest)

##DDNS server
@step(r'DDNS server has control channel (\S+).')
def ddns_open_control_channel(socket_name=None):
    ddns.ddns_open_control_channel_socket(socket_name)


@step(r'DDNS server is configured on (\S+) address and (\S+) port.')
def add_ddns_server(address, port):
    address, port = test_define_value(address, port)
    ddns.add_ddns_server(address, port)


@step(r'DDNS server is configured with (\S+) option set to (\S+).')
def add_ddns_server_options(option, value):
    option, value = test_define_value(option, value)
    ddns.add_ddns_server_options(option, value)


@step(r'Add forward DDNS with name (\S+) and key (\S+) on address (\S+) and port (\S+).')
def add_forward_ddns(name, key_name):
    if world.f_cfg.proto == 'v4':
        ip_address = world.f_cfg.dns4_addr
    else:
        ip_address = world.f_cfg.dns6_addr
    ddns.add_forward_ddns(name, key_name, ip_address, world.f_cfg.dns_port)


@step(r'Add reverse DDNS with name (\S+) and key (\S+) on address (\S+) and port (\S+).')
def add_reverse_ddns(name, key_name):
    if world.f_cfg.proto == 'v4':
        ip_address = world.f_cfg.dns4_addr
    else:
        ip_address = world.f_cfg.dns6_addr
    ddns.add_reverse_ddns(name, key_name, ip_address, world.f_cfg.dns_port)


@step(r'Add DDNS key named (\S+) based on (\S+) with secret value (\S+).')
def add_keys(name, algorithm, secret):
    ddns.add_keys(secret, name, algorithm)


@step(r'DDNS server is configured with GSS-TSIG.')
def ddns_add_gss_tsig():
    ddns.ddns_add_gss_tsig()


@step(r'Use DNS set no. (\d+).')
def use_dns_set_number(number):
    dns.use_config_set(int(number))


def print_cfg(service='DHCP'):
    if service.lower() == 'dhcp':
        print ("DHCP config:")
        print (json.dumps(world.dhcp_cfg, sort_keys=True, indent=2, separators=(',', ': ')))
    elif service.lower() == 'ddns':
        print ("DDNS config:")
        print (json.dumps(world.ddns_cfg, sort_keys=True, indent=2, separators=(',', ': ')))
