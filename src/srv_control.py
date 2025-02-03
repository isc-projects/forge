# Copyright (C) 2013-2025 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Wlodzimierz Wencel

# pylint: disable=anomalous-backslash-in-string
# pylint: disable=consider-using-f-string
# pylint: disable=consider-using-in
# pylint: disable=line-too-long
# pylint: disable=logging-fstring-interpolation
# pylint: disable=superfluous-parens
# pylint: disable=unbalanced-tuple-unpacking
# pylint: disable=unused-variable
# pylint: disable=useless-object-inheritance

"""Functions used in manipulating or observing server behavior."""

import json
import logging
import importlib

from . import misc
from .forge_cfg import world, step

from .softwaresupport.bind9_server import functions as dns
from .protosupport.multi_protocol_functions import test_define_value

log = logging.getLogger('forge')


class Dispatcher(object):
    """Dispatcher."""

    def __init__(self, mod_name):
        """__init__.

        :param mod_name:
        :type mod_name:
        """
        self.mod_name = mod_name

    def __getattr__(self, attr_name):
        """__getattr__.

        :param attr_name:
        :type attr_name:
        """
        if any(('isc_dhcp' in s for s in world.f_cfg.software_under_test)):
            server_name = f'isc_dhcp{world.proto[1]}_server'
        else:
            server_name = f'kea{world.proto[1]}_server'

        full_mod_name = "src.softwaresupport.%s.%s" % (server_name, self.mod_name)
        mod = importlib.import_module(full_mod_name)

        return getattr(mod, attr_name)


dhcp = Dispatcher('functions')
ddns = Dispatcher('functions_ddns')
mysql_reservation = Dispatcher('mysql_reservation')
pgsql_reservation = Dispatcher('pgsql_reservation')


# DHCP server configurations
@step(r'Server is configured with (\S+) subnet with (\S+) pool.')
def config_srv_subnet(subnet, pool, iface=world.f_cfg.server_iface, **kwargs):
    """Add server configuration with specified subnet and pool.

    :param subnet: the value for "subnet". If None, then continue with configuring an
        already existing subnet element.
    :type subnet:
    :param pool: the value appended to "pools". If None, then leave "pools" alone.
    :type pool:
    :param iface: the interface to be configured on the subnet element (default: SERVER_IFACE)
    :type iface:
    :param kwargs:
    :type kwargs:
    """
    subnet, pool, iface = test_define_value(subnet, pool, iface)
    dhcp.prepare_cfg_subnet(subnet, pool, iface=iface, **kwargs)


@step(r'Server is configured on interface (\S+) and address (\S+) with (\S+) subnet with (\S+) pool.')
def config_srv_subnet_with_iface(interface, address, subnet, pool):
    """Add server configuration with specified subnet and pool.

    :param interface: the interface to be configured on the subnet element and at the global level
    :type interface:
    :param address: the address to be configured at the global level
    :type address:
    :param subnet: the value for "subnet". If None, then continue with configuring an
        already existing subnet element.
    :type subnet:
    :param pool: the value appended to "pools". If None, then leave "pools" alone.
    :type pool:
    """
    interface, address, subnet, pool = test_define_value(interface, address, subnet, pool)
    dhcp.prepare_cfg_subnet_specific_interface(interface, address, subnet, pool)


def merge_in_subnet(selector, modification, config=None):
    """Merge modification into the subnet identified by selector.

    :param selector: dictionary used to identify the subnet, all keys and values are checked
    :type selector:
    :param modification: dictionary with the additions or changes to be merged
    :type modification:
    :param config: the config that directly contains "subnet4" or "subnet6" (Default value = None)
    :type config:
    """
    if config is None:
        config = world.dhcp_cfg
    assert isinstance(selector, dict)
    assert isinstance(modification, dict)
    assert isinstance(config, dict)

    for subnet in config[f'subnet{world.proto[1]}']:
        for k, v in selector.items():
            if k in subnet and subnet[k] == v:
                misc.merge_containers(subnet, modification)


def merge_in_network_subnet(network_selector, subnet_selector, modification):
    """Merge modification into the subnet under network identified by selectors.

    :param network_selector: dictionary used to identify the shared network, all keys and values are checked
    :type network_selector:
    :param subnet_selector: dictionary used to identify the subnet, all keys and values are checked
    :type subnet_selector:
    :param modification: dictionary with the additions or changes to be merged
    :type modification:
    """
    assert isinstance(network_selector, dict)
    assert isinstance(subnet_selector, dict)
    assert isinstance(modification, dict)

    for shared_network in world.dhcp_cfg['shared-networks']:
        for k, v in network_selector.items():
            if k in shared_network and shared_network[k] == v:
                merge_in_subnet(subnet_selector, modification, shared_network)


def update_subnet_counter():
    """Update subnet counter.

    When subnets are configured via other functions than the ones in this
    module, the subnet counter is left behind. This function updates it so that
    the functions in this module e.g. config_srv_another_subnet() can be used
    correctly again.
    """
    subnet_key = f'subnet{world.proto[1]}'
    if subnet_key in world.dhcp_cfg:
        world.dhcp['subnet_cnt'] = len(world.dhcp_cfg[subnet_key])
    else:
        world.dhcp['subnet_cnt'] = 0


@step(r'Server is configured with another subnet on interface (\S+) with (\S+) subnet and (\S+) pool.')
def config_srv_another_subnet(iface, subnet, pool, **kwargs):
    """Add another subnet with specified subnet/pool/interface.

    :param iface:
    :type iface:
    :param subnet:
    :type subnet:
    :param pool:
    :type pool:
    :param kwargs:
    :type kwargs:
    """
    subnet, pool, iface = test_define_value(subnet, pool, iface)
    dhcp.config_srv_another_subnet(subnet, pool, iface, **kwargs)


@step(r'Server is configured with another subnet: (\S+) with (\S+) pool.')
def config_srv_another_subnet_no_interface(subnet, pool, **kwargs):
    """Add another subnet to config file without interface specified.

    :param subnet:
    :type subnet:
    :param pool:
    :type pool:
    :param kwargs:
    :type kwargs:
    """
    subnet, pool = test_define_value(subnet, pool)
    dhcp.config_srv_another_subnet(subnet, pool, **kwargs)


@step(r'Server is configured with (\S+) prefix in subnet (\d+) with (\d+) prefix length and (\d+) delegated prefix length.')
def config_srv_prefix(prefix, subnet, length, delegated_length, **kwargs):
    """Add server configuration with specified prefix.

    :param prefix:
    :type prefix:
    :param subnet:
    :type subnet:
    :param length:
    :type length:
    :param delegated_length:
    :type delegated_length:
    :param kwargs:
    :type kwargs:
    """
    prefix, length, delegated_length, subnet = test_define_value(prefix, length, delegated_length, subnet)
    dhcp.prepare_cfg_prefix(prefix, length, delegated_length, subnet, **kwargs)


def add_prefix_to_subnet(prefix, length, delegated_length, subnet):
    """Add prefix configuration to existing subnet.

    :param prefix:
    :type prefix:
    :param length:
    :type length:
    :param delegated_length:
    :type delegated_length:
    :param subnet:
    :type subnet:
    """
    prefix, length, delegated_length, subnet = test_define_value(prefix, length, delegated_length, subnet)
    dhcp.add_prefix_to_subnet(prefix, length, delegated_length, int(subnet))


@step(r'Server-id configured with type (\S+) value (\S+).')
def config_srv_id(id_type, id_value):
    """Add server configuration with specified prefix.

    :param id_type:
    :type id_type:
    :param id_value:
    :type id_value:
    """
    id_type, id_value = test_define_value(id_type, id_value)
    dhcp.config_srv_id(str(id_type), str(id_value))


@step(r'Next server value on subnet (\d+) is configured with address (\S+).')
def subnet_add_siaddr(subnet_number, addr):
    """subnet_add_siaddr.

    :param subnet_number:
    :type subnet_number:
    :param addr:
    :type addr:
    """
    addr, subnet_number = test_define_value(addr, subnet_number)
    dhcp.add_siaddr(addr, subnet_number)


@step(r'Next server global value is configured with address (\S+).')
def global_add_siaddr(addr):
    """global_add_siaddr.

    :param addr:
    :type addr:
    """
    addr = test_define_value(addr)[0]
    dhcp.add_siaddr(addr, None)


@step(r'Server is configured with (\S+) option with value (\S+).')
def config_srv_opt(option_name, option_value, **kwargs):
    """Add to configuration options like: preference, dns servers..

    This step causes to set in to main space!

    :param option_name:
    :type option_name:
    :param option_value:
    :type option_value:
    :param kwargs:
    :type kwargs:
    """
    option_name, option_value = test_define_value(option_name, option_value)
    dhcp.prepare_cfg_add_option(option_name, option_value, world.cfg["space"], **kwargs)


@step(r'On space (\S+) server is configured with (\S+) option with value (\S+).')
def config_srv_opt_space(space, option_name, option_value, **kwargs):
    """Add to configuration options like: preference, dns servers..

    You can specify to which space should that be included.

    :param space:
    :type space:
    :param option_name:
    :type option_name:
    :param option_value:
    :type option_value:
    :param kwargs:
    :type kwargs:
    """
    option_name, option_value, space = test_define_value(option_name, option_value, space)
    dhcp.prepare_cfg_add_option(option_name, option_value, space, **kwargs)


@step(r'Server is configured with custom option (\S+)/(\d+) with type (\S+) and value (\S+).')
def config_srv_custom_opt(opt_name, opt_code, opt_type, opt_value, **kwargs):
    """Prepare server configuration with the specified custom option.

    :param opt_name: name of the option, e.g. foo
    :type opt_name:
    :param opt_code: code of the option, e.g. 100
    :type opt_code:
    :param opt_type: type of the option, e.g. uint8 (see bind10 guide for complete list)
    :type opt_type:
    :param opt_value: value of the option, e.g. 1
    :type opt_value:
    :param kwargs:
    :type kwargs:
    """
    opt_name, opt_code, opt_type, opt_value = test_define_value(opt_name, opt_code, opt_type, opt_value)
    dhcp.prepare_cfg_add_custom_option(opt_name, opt_code, opt_type, opt_value, world.cfg["space"],
                                       **kwargs)


@step(r'On space (\S+) server is configured with a custom option (\S+)/(\d+) with type (\S+) and value (\S+).')
def config_srv_custom_opt_space(space, opt_name, opt_code, opt_type, opt_value, **kwargs):
    """Do the same as config_srv_custom_opt but specify that option on different space then main.

    :param space:
    :type space:
    :param opt_name:
    :type opt_name:
    :param opt_code:
    :type opt_code:
    :param opt_type:
    :type opt_type:
    :param opt_value:
    :type opt_value:
    :param kwargs:
    :type kwargs:
    """
    opt_name, opt_code, opt_type, opt_value, space = test_define_value(opt_name, opt_code, opt_type, opt_value, space)
    dhcp.prepare_cfg_add_custom_option(opt_name, opt_code, opt_type, opt_value, space, **kwargs)


@step(r'Time (\S+) is configured with value (\S+).')
def set_time(which_time, value):
    """Change values of T1, T2, preffered lifetime and valid lifetime.

    :param which_time:
    :type which_time:
    :param value:
    :type value:
    """
    which_time, value = test_define_value(which_time, value)
    dhcp.set_time(which_time, value, None)


@step(r'Option (\S+) is configured with value (\S+).')
def set_time_option(which_time, value):
    """Change values of rapid-commit and other options that can be set on true or false.

    :param which_time:
    :type which_time:
    :param value:
    :type value:
    """
    which_time, value = test_define_value(which_time, value)
    dhcp.set_time(which_time, value)


@step(r'Add configuration parameter (\S+) with value (\S+) to global configuration.')
def set_conf_parameter_global(parameter_name, value):
    """Can be used on the end of configuration process, just before starting server.

    :param value: return:
    :type value:
    :param parameter_name:
    :type parameter_name:
    """
    # parameter_name, value = test_define_value(parameter_name, value)
    dhcp.set_conf_parameter_global(parameter_name, value)


@step(r'Add configuration parameter (\S+) with value (\S+) to subnet (\d+) configuration.')
def set_conf_parameter_subnet(parameter_name, value, subnet_id):
    """Can be used on the end of configuration process, just before starting server.

    :param value: return:
    :type value:
    :param parameter_name:
    :type parameter_name:
    :param subnet_id:
    :type subnet_id:
    """
    parameter_name, value, subnet_id = test_define_value(parameter_name, value, subnet_id)
    dhcp.set_conf_parameter_subnet(parameter_name, value, int(subnet_id))


@step(r'Add to config file line: (.+)')
def add_line(command):
    """Do the same as step 'Run configuration command: (.+)'.

    :param command:
    :type command:
    """
    dhcp.add_line_in_global(command)


@step(r'To subnet (\d+) configuration section in the config file add line: (.+)')
def add_line_to_subnet(subnetid, command):
    """add_line_to_subnet.

    :param subnetid:
    :type subnetid:
    :param command:
    :type command:
    """
    test_define_value(command)
    dhcp.add_line_in_subnet(int(subnetid), command)


@step(r'Add hooks library located (\S+).')
def add_hooks(library_path):
    """Add hooks library to configuration. Only Kea.

    :param library_path:
    :type library_path:
    """
    full_library_path = world.f_cfg.hooks_join(library_path)
    dhcp.add_hooks(full_library_path)


def delete_hooks(hook_patterns):
    """Delete hooks.

    :param hook_patterns:
    :type hook_patterns:
    """
    dhcp.delete_hooks(hook_patterns)


@step(r'To hook no. (\d+) add parameter named (\S+) with value: (.+)')
def add_parameter_to_hook(hook_name, parameter_name, parameter_value=None):
    """Add parameter to hook.

    :param hook_name:
    :type hook_name:
    :param parameter_name:
    :type parameter_name:
    :param parameter_value: (Default value = None)
    :type parameter_value:
    """
    if not isinstance(parameter_name, dict):
        parameter_name, parameter_value = test_define_value(parameter_name, parameter_value)
    dhcp.add_parameter_to_hook(hook_name, parameter_name, parameter_value)


@step(r'Add High-Availability hook library located (\S+).')
def add_ha_hook(library_path):
    """Add HA hook.

    :param library_path:
    :type library_path:
    """
    full_library_path = world.f_cfg.hooks_join(library_path)
    dhcp.ha_add_parameter_to_hook("lib", full_library_path)
    dhcp.add_hooks(full_library_path)


@step(r'To HA hook configuration add (\S+) with value: (.+)')
def add_parameter_to_ha_hook(parameter_name, parameter_value, relationship=0):
    """Add parameter to HA hook.

    :param parameter_name:
    :type parameter_name:
    :param parameter_value:
    :type parameter_value:
    :param relationship: (Default value = 0)
    :type relationship:
    """
    parameter_name, parameter_value = test_define_value(parameter_name, parameter_value)
    dhcp.ha_add_parameter_to_hook(parameter_name, parameter_value, relationship)


def update_ha_hook_parameter(param, relationship=0):
    """Update HA hook parameter.

    :param param:
    :type param:
    :param relationship: (Default value = 0)
    :type relationship:
    """
    dhcp.update_ha_hook_parameter(param, relationship)


def build_database(dest=world.f_cfg.mgmt_address, db_name=world.f_cfg.db_name,
                   db_user=world.f_cfg.db_user, db_passwd=world.f_cfg.db_passwd,
                   init_db=True, disable=False):
    """Build database.

    :param dest: (Default value = world.f_cfg.mgmt_address)
    :type dest:
    :param db_name: (Default value = world.f_cfg.db_name)
    :type db_name:
    :param db_user: (Default value = world.f_cfg.db_user)
    :type db_user:
    :param db_passwd: (Default value = world.f_cfg.db_passwd)
    :type db_passwd:
    :param init_db: (Default value = True)
    :type init_db:
    :param disable: (Default value = False)
    :type disable:
    """
    dest, db_name, db_user, db_passwd = test_define_value(dest, db_name, db_user, db_passwd)
    dhcp.db_setup(dest=dest, db_name=db_name, db_user=db_user, db_passwd=db_passwd, init_db=init_db, disable=disable)


@step(r'Use (\S+) as lease database backend.')
def define_temporary_lease_db_backend(lease_db_type):
    """Define temporary lease database backend.

    :param lease_db_type:
    :type lease_db_type:
    """
    lease_db_type = test_define_value(lease_db_type)[0]
    world.f_cfg.db_type = lease_db_type
    dhcp.add_database_hook(lease_db_type)


@step(r'Credentials for (\S+) database. User: (\S+); Passwd: (\S+); DB-name: (\S+); Host: (\S+);')
def define_temporary_lease_db_backend_credentials(db_type, tmp_db_user, tmp_db_passwd, tmp_db_name, tmp_db_host):
    """Define temporary lease database backend credentials.

    :param db_type:
    :type db_type:
    :param tmp_db_user:
    :type tmp_db_user:
    :param tmp_db_passwd:
    :type tmp_db_passwd:
    :param tmp_db_name:
    :type tmp_db_name:
    :param tmp_db_host:
    :type tmp_db_host:
    """
    # for now it's just support for leases.
    assert world.f_cfg.tmp_db_type is not None, 'world.f_cfg.tmp_db_type is None'
    assert db_type in ["leases"], 'db_type not in ["leases"]'
    world.f_cfg.db_host = tmp_db_host
    world.f_cfg.db_name = tmp_db_name
    world.f_cfg.db_passwd = tmp_db_passwd
    world.f_cfg.db_user = tmp_db_user


def add_database_hook(db_type):
    """add_database_hook Check if database hook was added to configuration. If not it will add it.

    :param db_type: mysql, pgsql, postgres or memfile
    :type db_type: str
    """
    dhcp.add_database_hook(db_type)


# START Reservation backend section
@step(r'Use (\S+) reservation system.')
def enable_db_backend_reservation(db_type, clear=True):
    """Enable database backend reservation.

    :param db_type:
    :type db_type:
    :param clear: (Default value = True)
    :type clear:
    """
    # for now we are not implementing new configuration system for this one host reservation in databases
    if db_type.lower() == 'mysql':
        mysql_reservation.enable_db_backend_reservation()
        if clear:
            mysql_reservation.clear_all_reservations()
    elif db_type.lower() == 'postgresql':
        pgsql_reservation.enable_db_backend_reservation()
        if clear:
            pgsql_reservation.clear_all_reservations()
    elif db_type == "memfile":
        pass
    else:
        assert False, "Database type not recognised."
    # let's add hooks
    add_database_hook(db_type)


@step(r'Create new (\S+) reservation identified by (\S+) (\S+).')
def new_db_backend_reservation(db_type, reservation_identifier, reservation_identifier_value):
    """Add new database backend reservation.

    :param db_type:
    :type db_type:
    :param reservation_identifier:
    :type reservation_identifier:
    :param reservation_identifier_value:
    :type reservation_identifier_value:
    """
    if db_type.lower() == 'mysql':
        mysql_reservation.new_db_backend_reservation(reservation_identifier, reservation_identifier_value)
    elif db_type.lower() == 'postgresql':
        pgsql_reservation.new_db_backend_reservation(reservation_identifier, reservation_identifier_value)
    else:
        assert False, "Database type not recognised."


@step(r'Add (\S+) (\S+) to (\S+) reservation record id (\d+).')
def update_db_backend_reservation(field_name, field_value, db_type, reservation_record_id):
    """Update database backend reservation.

    :param field_name:
    :type field_name:
    :param field_value:
    :type field_value:
    :param db_type:
    :type db_type:
    :param reservation_record_id:
    :type reservation_record_id:
    """
    if db_type.lower() == 'mysql':
        mysql_reservation.update_db_backend_reservation(field_name, field_value, int(reservation_record_id))
    elif db_type.lower() == 'postgresql':
        pgsql_reservation.update_db_backend_reservation(field_name, field_value, int(reservation_record_id))
    else:
        assert False, "Database type not recognised."


@step(r'Add IPv6 prefix reservation (\S+) (\d+) with iaid (\S+) to (\S+) record id (\d+).')
def ipv6_prefix_db_backend_reservation(reserved_prefix, reserved_prefix_len,
                                       reserved_iaid, db_type, reservation_record_id):
    """ipv6_prefix_db_backend_reservation.

    :param reserved_prefix:
    :type reserved_prefix:
    :param reserved_prefix_len:
    :type reserved_prefix_len:
    :param reserved_iaid:
    :type reserved_iaid:
    :param db_type:
    :type db_type:
    :param reservation_record_id:
    :type reservation_record_id:
    """
    if db_type.lower() == 'mysql':
        mysql_reservation.ipv6_prefix_db_backend_reservation(reserved_prefix, reserved_prefix_len, reserved_iaid,
                                                             int(reservation_record_id))
    elif db_type.lower() == 'postgresql':
        pgsql_reservation.ipv6_prefix_db_backend_reservation(reserved_prefix, reserved_prefix_len, reserved_iaid,
                                                             int(reservation_record_id))
    else:
        assert False, "Database type not recognised."


@step(r'Add IPv6 address reservation (\S+) with iaid (\S+) to (\S+) record id (\d+).')
def ipv6_address_db_backend_reservation(reserved_address, reserved_iaid, db_type, reservation_record_id):
    """ipv6_address_db_backend_reservation.

    :param reserved_address:
    :type reserved_address:
    :param reserved_iaid:
    :type reserved_iaid:
    :param db_type:
    :type db_type:
    :param reservation_record_id:
    :type reservation_record_id:
    """
    if db_type.lower() == 'mysql':
        mysql_reservation.ipv6_address_db_backend_reservation(reserved_address, reserved_iaid,
                                                              int(reservation_record_id))
    elif db_type.lower() == 'postgresql':
        pgsql_reservation.ipv6_address_db_backend_reservation(reserved_address, reserved_iaid,
                                                              int(reservation_record_id))
    else:
        assert False, "Database type not recognised."


@step(r'Add option reservation code (\S+) value (\S+) space (\S+) persistent (\d+) client class (\S+) subnet id (\d+) and scope (\S+) to (\S+) record id (\d+).')
def option_db_record_reservation(reserved_option_code, reserved_option_value, reserved_option_space,
                                 reserved_option_persistent, reserved_option_client_class, reserved_subnet_id,
                                 reserved_option_scope, db_type, reservation_record_id):
    """option_db_record_reservation.

    :param reserved_option_code:
    :type reserved_option_code:
    :param reserved_option_value:
    :type reserved_option_value:
    :param reserved_option_space:
    :type reserved_option_space:
    :param reserved_option_persistent:
    :type reserved_option_persistent:
    :param reserved_option_client_class:
    :type reserved_option_client_class:
    :param reserved_subnet_id:
    :type reserved_subnet_id:
    :param reserved_option_scope:
    :type reserved_option_scope:
    :param db_type:
    :type db_type:
    :param reservation_record_id:
    :type reservation_record_id:
    """
    if db_type.lower() == 'mysql':
        mysql_reservation.option_db_record_reservation(reserved_option_code, reserved_option_value,
                                                       reserved_option_space, reserved_option_persistent,
                                                       reserved_option_client_class, reserved_subnet_id,
                                                       reserved_option_scope, int(reservation_record_id))
    elif db_type.lower() == 'postgresql':
        pgsql_reservation.option_db_record_reservation(reserved_option_code, reserved_option_value,
                                                       reserved_option_space, reserved_option_persistent,
                                                       reserved_option_client_class, reserved_subnet_id,
                                                       reserved_option_scope, int(reservation_record_id))
    else:
        assert False, "Database type not recognised."


@step(r'Dump all the reservation entries from (\S+) database.')
def dump_db_reservation(db_type):
    """Dump database reservation.

    :param db_type:
    :type db_type:
    """
    if db_type.lower() == 'mysql':
        mysql_reservation.clear_all_reservations()
    elif db_type.lower() == 'postgresql':
        pgsql_reservation.clear_all_reservations()
    else:
        assert False, "Database type not recognised."


@step(r'Upload hosts reservation to (\S+) database.')
def upload_db_reservation(db_type, exp_failed=False):
    """Upload database reservation.

    :param db_type:
    :type db_type:
    :param exp_failed: (Default value = False)
    :type exp_failed:
    """
    if db_type.lower() == 'mysql':
        mysql_reservation.upload_db_reservation(exp_failed)
    elif db_type.lower() == 'postgresql':
        pgsql_reservation.upload_db_reservation(exp_failed)
    else:
        assert False, "Database type not recognised."
# END Reservation backend section


@step(r'Reserve (\S+) (\S+) for host uniquely identified by (\S+) (\S+).')
def host_reservation(reservation_type, reserved_value, unique_host_value_type, unique_host_value):
    """Ability to configure simple host reservations.

    :param reservation_type:
    :type reservation_type:
    :param reserved_value:
    :type reserved_value:
    :param unique_host_value_type:
    :type unique_host_value_type:
    :param unique_host_value:
    :type unique_host_value:
    """
    reservation_type, reserved_value, unique_host_value_type, unique_host_value = test_define_value(reservation_type,
                                                                                                    reserved_value,
                                                                                                    unique_host_value_type,
                                                                                                    unique_host_value)
    dhcp.host_reservation(reservation_type, reserved_value, unique_host_value_type, unique_host_value, 'global')


# shared-subnet cfg
@step(r'Add subnet (\d+) to shared-subnet set (\d+).')
def shared_subnet(subnet_id, shared_subnet_id):
    """Configure shared subnets.

    :param subnet_id:
    :type subnet_id:
    :param shared_subnet_id:
    :type shared_subnet_id:
    """
    subnet_id, shared_subnet_id = test_define_value(subnet_id, shared_subnet_id)
    dhcp.add_to_shared_subnet(subnet_id, int(shared_subnet_id))


@step(r'Shared subnet (\d+) is configured with option line: (.+)')
def add_option_shared_subnet(shared_subnet_id, conf_line):
    """Add option shared subnet.

    :param shared_subnet_id:
    :type shared_subnet_id:
    :param conf_line:
    :type conf_line:
    """
    shared_subnet_id, conf_line = test_define_value(shared_subnet_id, conf_line)
    dhcp.add_line_to_shared_subnet(shared_subnet_id, conf_line)


@step(r'Add configuration parameter (\S+) with value (\S+) to shared-subnet (\d+) configuration.')
def set_conf_parameter_shared_subnet(parameter_name, value, subnet_id):
    """Can be used on the end of configuration process, just before starting server.

    :param parameter_name:
    :type parameter_name:
    :param value:
    :type value:
    :param subnet_id:
    :type subnet_id:
    """
    parameter_name, value, subnet_id = test_define_value(parameter_name, value, subnet_id)
    dhcp.set_conf_parameter_shared_subnet(parameter_name, value, int(subnet_id))


# subnet options
@step(r'Reserve (\S+) (\S+) in subnet (\d+) for host uniquely identified by (\S+) (\S+).')
def host_reservation_in_subnet(reservation_type, reserved_value, subnet, unique_host_value_type, unique_host_value):
    """Configure a subnet-level host reservation.

    :param reservation_type: the type of the reserved resource: "client-classes",
        "hostname", "ip-addresses", "option-data", "prefixes"
    :type reservation_type: the type of the reserved resource:
    :param reserved_value: the value of the reserved resource
    :type reserved_value:
    :param subnet: the ordinal number of the subnet under which the reservation will
        be made. Careful, this is not the subnet ID.
    :type subnet:
    :param unique_host_value_type: the type for the reservation's identifier:
        "circuit-id", "client-id", "duid", "flex-id", "hw-address"
    :type unique_host_value_type: the type for the reservation's identifier:
    :param unique_host_value: the value for the reservation's identifier
    :type unique_host_value:
    """
    reservation_type, reserved_value, unique_host_value_type, unique_host_value = test_define_value(reservation_type,
                                                                                                    reserved_value,
                                                                                                    unique_host_value_type,
                                                                                                    unique_host_value)
    dhcp.host_reservation(reservation_type, reserved_value, unique_host_value_type, unique_host_value, int(subnet))


@step(r'For host reservation entry no. (\d+) in subnet (\d+) add (\S+) with value (\S+).')
def host_reservation_in_subnet_add_value(reservation_number, subnet, reservation_type, reserved_value):
    """Ability to configure simple host reservations in subnet.

    :param reservation_number:
    :type reservation_number:
    :param subnet:
    :type subnet:
    :param reservation_type:
    :type reservation_type:
    :param reserved_value:
    :type reserved_value:
    """
    reservation_type, reserved_value = test_define_value(reservation_type, reserved_value)
    dhcp.host_reservation_extension(int(reservation_number), int(subnet), reservation_type, reserved_value)


@step(r'Time (\S+) in subnet (\d+) is configured with value (\d+).')
def set_time_in_subnet(which_time, subnet, value):
    """Change values of T1, T2, preffered lifetime and valid lifetime.

    :param which_time:
    :type which_time:
    :param subnet:
    :type subnet:
    :param value:
    :type value:
    """
    which_time, subnet, value = test_define_value(which_time, subnet, value)
    dhcp.set_time(which_time, value, subnet)


@step(r'Server is configured with another pool (\S+) in subnet (\d+).')
def new_pool(pool, subnet, pool_id=None):
    """Add new pool.

    :param pool:
    :type pool:
    :param subnet:
    :type subnet:
    :param pool_id: (Default value = None)
    :type pool_id:
    """
    dhcp.add_pool_to_subnet(pool, int(subnet), pool_id)


@step(r'Server is configured with (\S+) option in subnet (\d+) with value (\S+).')
def config_srv(option_name, subnet, option_value, **kwargs):
    """Prepare server configuration with the specified option.

    :param option_name: name of the option, e.g. dns-servers (number may be used here)
    :type option_name:
    :param subnet:
    :type subnet:
    :param option_value: value of the configuration
    :type option_value:
    :param kwargs:
    :type kwargs:
    """
    dhcp.prepare_cfg_add_option_subnet(option_name, subnet, option_value, **kwargs)


@step(r'On space (\S+) server is configured with (\S+) option in subnet (\d+) with value (\S+).')
def config_srv_on_space(space, option_name, subnet, option_value, **kwargs):
    """Prepare server configuration with the specified option.

    :param space:
    :type space:
    :param option_name: name of the option, e.g. dns-servers (number may be used here)
    :type option_name:
    :param subnet:
    :type subnet:
    :param option_value: value of the configuration
    :type option_value:
    :param kwargs:
    :type kwargs:
    """
    dhcp.prepare_cfg_add_option_subnet(option_name, subnet, option_value, space, **kwargs)


def option_in_shared_network(option_name: str, option_value: str, shared_network: int = 0, **kwargs):
    """Add option-data to shared network.

    :param option_name: string, option name
    :type option_name:
    :param option_value: string, option value
    :type option_value:
    :param shared_network: int, list index of network that should be updated
    :type shared_network:
    :param kwargs:
    :type kwargs:
    """
    dhcp.prepare_cfg_add_option_shared_network(option_name, option_value, shared_network=shared_network,
                                               **kwargs)


def add_option_to_pool(option_name: str, option_value: str, subnet: int = 0, pool: int = 0, **kwargs):
    """Add option data to a pool.

    :param option_name: string, option name
    :type option_name:
    :param option_value: string, option value
    :type option_value:
    :param subnet: int, index of subnet in the list of subnets
    :type subnet:
    :param pool: int, index of pool to be updated on the list of pools
    :type pool:
    :param kwargs:
    :type kwargs:
    """
    dhcp.prepare_cfg_add_option_pool(option_name, option_value, subnet=subnet, pool=pool, **kwargs)


@step(r'Server is configured with client-classification option in subnet (\d+) with name (\S+).')
def config_client_classification(subnet, option_value):
    """config_client_classification.

    :param subnet:
    :type subnet:
    :param option_value:
    :type option_value:
    """
    dhcp.config_client_classification(subnet, option_value)


@step(r'Server is configured with client-classification option in pool (\d+) with name (\S+).')
def config_pool_client_classification(subnet, pool, option_value):
    """config_pool_client_classification.

    :param subnet:
    :type subnet:
    :param pool:
    :type pool:
    :param option_value:
    :type option_value:
    """
    dhcp.config_pool_client_classification(subnet, pool, option_value)


@step(r'Server is configured with require-client-classification option in subnet (\d+) with name (\S+).')
def config_require_client_classification(subnet, option_value):
    """config_require_client_classification.

    :param subnet:
    :type subnet:
    :param option_value:
    :type option_value:
    """
    dhcp.config_require_client_classification(subnet, option_value)


@step(r'Add class called (\S+).')
def create_new_class(class_name):
    """Create new class.

    :param class_name:
    :type class_name:
    """
    dhcp.create_new_class(class_name)


@step(r'To class no (\d+) add parameter named: (\S+) with value: (.+)')
def add_test_to_class(class_number, parameter_name, parameter_value):
    """Add test to class.

    :param class_number:
    :type class_number:
    :param parameter_name:
    :type parameter_name:
    :param parameter_value:
    :type parameter_value:
    """
    if parameter_name == "test":
        parameter_name, parameter_value = test_define_value(parameter_name, parameter_value)
    dhcp.add_test_to_class(int(class_number), parameter_name, parameter_value)


@step(r'To class no (\d+) add option (\S+) with value (\S+).')
def add_option_to_defined_class(class_no, option, option_value):
    """Add option to defined class.

    :param class_no:
    :type class_no:
    :param option:
    :type option:
    :param option_value:
    :type option_value:
    """
    dhcp.add_option_to_defined_class(int(class_no), option, option_value)


@step(r'Server has control channel (\S+).')
def add_unix_socket(socket_name=None):
    """Add unix socket.

    :param socket_name: (Default value = None)
    :type socket_name:
    """
    dhcp.open_control_channel_socket(socket_name)


@step(r'Server has control agent configured on HTTP connection with address (\S+):(\S+) and socket (\S+) path: (\S+).')
def add_http_control_channel(host_address='$(MGMT_ADDRESS)', host_port=8000, socket_name='control_socket', auth=None):
    """Add HTTP control channel.

    :param host_address: (Default value = '$(MGMT_ADDRESS)')
    :type host_address:
    :param host_port: (Default value = 8000)
    :type host_port:
    :param socket_name: (Default value = 'control_socket')
    :type socket_name:
    :param auth: optional authorisation configuration
    :type auth: dict
    """
    host_address, host_port = test_define_value(host_address, host_port)
    dhcp.add_http_control_channel(host_address, host_port, socket_name, auth)


def disable_leases_affinity():
    """Disable lease affinity completely.

    This means lease will be removed from leases file immediately after client send release message
    By default Kea will keep those for brief period of time. Default behaviour changed on 2.3.2.
    """
    dhcp.disable_lease_affinity()


def configure_multi_threading(enable_mt: bool, pool: int = 0, queue: int = 0):
    """Configure multithreading settings directly, this will also disable automated check.

    :param enable_mt: bool, "enable-multi-threading" value
    :type enable_mt:
    :param pool: int, "thread-pool-size" value
    :type pool:
    :param queue: int, "packet-queue-size" value
    :type queue:
    """
    dhcp.configure_multi_threading(enable_mt, pool, queue)


def update_expired_leases_processing(param):
    """Update configuration map of "expired-leases-processing" with one or more parameters.

    Param checking is not required it will be done just before sending a config file.
    To set default config please use update_expired_leases_processing('default').
    To update configuration with param hold-reclaimed-time please use update_expired_leases_processing({"hold-reclaimed-time": <your value>}).

    :param param: str or dict
    :type param:
    """
    dhcp.update_expired_leases_processing(param)


# DNS server configuration
@step(r'DNS server is configured on (\S+) address (\S+) on port no. (\d+) and working directory (\S+).')
def dns_conf(ip_type, address, port, direct):
    """dns_conf.

    :param ip_type:
    :type ip_type:
    :param address:
    :type address:
    :param port:
    :type port:
    :param direct:
    :type direct:
    """
    ip_type, address, port, direct = test_define_value(ip_type, address, port, direct)
    dns.add_defaults(ip_type, address, port, direct)


@step(r'DNS server is configured with zone (\S+) with type: (\S+) file: (\S+) with dynamic update key: (\S+).')
def add_zone(zone, zone_type, file_nem, key):
    """Add zone.

    :param zone:
    :type zone:
    :param zone_type:
    :type zone_type:
    :param file_nem:
    :type file_nem:
    :param key:
    :type key:
    """
    zone, zone_type, file_nem, key = test_define_value(zone, zone_type, file_nem, key)
    dns.add_zone(zone, zone_type, file_nem, key)


@step(r'Add DNS key named: (\S+) algorithm: (\S+) and value: (\S+).')
def dns_add_key(key_name, algorithm, key_value):
    """Add DNS key.

    :param key_name:
    :type key_name:
    :param algorithm:
    :type algorithm:
    :param key_value:
    :type key_value:
    """
    key_name, algorithm, key_value = test_define_value(key_name, algorithm, key_value)
    dns.add_key(key_name, algorithm, key_value)


@step(r'Add DNS rndc-key on address (\S+) and port (\d+). Using algorithm: (\S+) with value: (\S+)')
def dns_rest(address, port, alg, value):
    """Add DNS rndc-key on address and port.

    :param address:
    :type address:
    :param port:
    :type port:
    :param alg:
    :type alg:
    :param value:
    :type value:
    """
    address, port, alg, value = test_define_value(address, port, alg, value)
    dns.add_rndc(address, port, alg, value)


@step(r'Server logging system is configured with logger type (\S+), severity (\S+), severity level (\S+) and log file (\S+).')
def configure_loggers(log_type, severity, severity_level, logging_file=None):
    """Configure loggers.

    :param log_type:
    :type log_type:
    :param severity:
    :type severity:
    :param severity_level:
    :type severity_level:
    :param logging_file: (Default value = None)
    :type logging_file:
    """
    log_type, severity, severity_level = test_define_value(log_type, severity, severity_level)
    dhcp.add_logger(log_type, severity, severity_level, logging_file)


# servers management
@step(r'Create server configuration.')
def build_config_files(cfg=None):
    """Build config files.

    :param cfg: (Default value = None)
    :type cfg:
    """
    dhcp.build_config_files(cfg=cfg)


@step(r'Create and send server configuration.')
def build_and_send_config_files(cfg=None, dest=world.f_cfg.mgmt_address):
    """Build and send configuration files.

    :param cfg: (Default value = None)
    :type cfg:
    :param dest: (Default value = world.f_cfg.mgmt_address)
    :type dest:
    """
    dest = test_define_value(dest)[0]
    check_remote_address(dest)
    dhcp.build_and_send_config_files(cfg=cfg, destination_address=dest)


def start_srv(name: str, action: str, config_set=None,
              dest: str = world.f_cfg.mgmt_address, should_succeed: bool = True):
    """Start, stop, restart or reconfigure server.

    :param name: DHCP' | 'DNS'
    :type name:
    :param action: started' | 'stopped' | 'restarted' | 'reconfigured'
    :type action:
    :param config_set: Dynamic configuration to be used. Currently used only as an integer to select
        a certain DNS configuration. (Default value = None)
    :type config_set:
    :param dest: management address of server
    :type dest:
    :param should_succeed: whether the action is supposed to succeed or fail (Default value = True)
    :type should_succeed: bool
    """
    dest = test_define_value(dest)[0]
    check_remote_address(dest)
    if name not in ["DHCP", "DNS", "CA"]:
        assert False, "I don't think there is support for something else than DNS,  DHCP or CA"
    log.info(f'---------------- {name} {action} {dest} ----------------')
    if action == "started":
        if name == "DHCP":
            dhcp.start_srv(should_succeed, destination_address=dest)
        elif name == "CA":
            dhcp.start_srv(should_succeed, destination_address=dest, process='ctrl_agent')
        elif name == "DNS":
            if config_set is not None:
                use_dns_set_number(config_set)
            dns.start_srv(should_succeed, destination_address=dest)
    elif action == "stopped":
        assert should_succeed, 'should_succeed == false not implemented for stop action'
        if name == "DHCP":
            dhcp.stop_srv(destination_address=dest)
        elif name == "DNS":
            dns.stop_srv(destination_address=dest)
    elif action == "restarted":
        assert should_succeed, 'should_succeed == false not implemented for restart action'
        if name == "DHCP":
            dhcp.restart_srv(destination_address=dest)
        elif name == "DNS":
            dns.restart_srv(destination_address=dest)
    elif action == "reconfigured":
        if name == "DHCP":
            dhcp.reconfigure_srv(should_succeed, destination_address=dest)
        elif name == "DNS":
            dns.reconfigure_srv(should_succeed, destination_address=dest)
    else:
        assert False, "we don't support '%s' action." % str(action)


def check_remote_address(remote_address):
    """Add new remote server IP address as additional location.

    Can be used for running dhcp server.
    From all added locations all files on clean up will be downloaded to specific local location

    :param remote_address: IP address of remote vm
    :type remote_address:
    """
    if remote_address not in world.f_cfg.multiple_tested_servers:
        world.f_cfg.multiple_tested_servers.append(remote_address)


@step(r'Add remote server with address: (\S+).')
def add_remote_server(remote_address):
    """Add remote server.

    :param remote_address:
    :type remote_address:
    """
    remote_address[0] = test_define_value(remote_address)
    check_remote_address(remote_address)


@step(r'Clear (\S+).')
def clear_some_data(data_type, service='dhcp', dest=world.f_cfg.mgmt_address,
                    software_install_path=world.f_cfg.software_install_path, db_user=world.f_cfg.db_user,
                    db_passwd=world.f_cfg.db_passwd, db_name=world.f_cfg.db_name):
    """Clear some data.

    :param data_type:
    :type data_type:
    :param service: (Default value = 'dhcp')
    :type service:
    :param dest: (Default value = world.f_cfg.mgmt_address)
    :type dest:
    :param software_install_path: (Default value = world.f_cfg.software_install_path)
    :type software_install_path:
    :param db_user: (Default value = world.f_cfg.db_user)
    :type db_user:
    :param db_passwd: (Default value = world.f_cfg.db_passwd)
    :type db_passwd:
    :param db_name: (Default value = world.f_cfg.db_name)
    :type db_name:
    """
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


# DDNS server
@step(r'DDNS server has control channel (\S+).')
def ddns_add_unix_socket(socket_name=None):
    """Add unix socket to DDNS server.

    :param socket_name: (Default value = None)
    :type socket_name:
    """
    ddns.ddns_open_control_channel_socket(socket_name)


@step(r'DDNS server is configured on (\S+) address and (\S+) port.')
def add_ddns_server(address, port):
    """Add DDNS server.

    :param address:
    :type address:
    :param port:
    :type port:
    """
    address, port = test_define_value(address, port)
    ddns.add_ddns_server(address, port)


@step(r'DDNS server is configured with (\S+) option set to (\S+).')
def add_ddns_server_behavioral_options(option, value):
    """Add option to DDNS server.

    :param option:
    :type option:
    :param value:
    :type value:
    """
    option, value = test_define_value(option, value)
    ddns.add_ddns_server_behavioral_options(option, value)


@step(r'DDNS server is configured with (\S+) option set to (\S+).')
def add_ddns_server_connectivity_options(option, value):
    """Add options to DDNS server.

    :param option:
    :type option:
    :param value:
    :type value:
    """
    option, value = test_define_value(option, value)
    ddns.add_ddns_server_connectivity_options(option, value)


@step(r'Add forward DDNS with name (\S+) and key (\S+) on address (\S+) and port (\S+).')
def add_forward_ddns(name, key_name, ip_address=None):
    """Add forward DDNS.

    :param name:
    :type name:
    :param key_name:
    :type key_name:
    :param ip_address: (Default value = None)
    :type ip_address:
    """
    if world.f_cfg.proto == 'v4' and ip_address is None:
        ip_address = world.f_cfg.dns4_addr
    elif world.f_cfg.proto == 'v6' and ip_address is None:
        ip_address = world.f_cfg.dns6_addr
    ddns.add_forward_ddns(name, key_name, ip_address, world.f_cfg.dns_port)


@step(r'Add reverse DDNS with name (\S+) and key (\S+) on address (\S+) and port (\S+).')
def add_reverse_ddns(name, key_name, ip_address=None):
    """Add reverse DDNS.

    :param name:
    :type name:
    :param key_name:
    :type key_name:
    :param ip_address: (Default value = None)
    :type ip_address:
    """
    if world.f_cfg.proto == 'v4' and ip_address is None:
        ip_address = world.f_cfg.dns4_addr
    elif world.f_cfg.proto == 'v6' and ip_address is None:
        ip_address = world.f_cfg.dns6_addr
    ddns.add_reverse_ddns(name, key_name, ip_address, world.f_cfg.dns_port)


@step(r'Add DDNS key named (\S+) based on (\S+) with secret value (\S+).')
def add_keys(name, algorithm, secret):
    """Add DDNS keys.

    :param name:
    :type name:
    :param algorithm:
    :type algorithm:
    :param secret:
    :type secret:
    """
    ddns.add_keys(secret, name, algorithm)


@step(r'DDNS server is configured with GSS-TSIG.')
def ddns_add_gss_tsig(addr, dns_system,
                      client_principal="DHCP/admin.example.com@EXAMPLE.COM",
                      client_tab="FILE:/tmp/dhcp.keytab",
                      fallback=False,
                      retry_interval=None,
                      rekey_interval=None,
                      server_id="server1",
                      server_principal="DNS/server.example.com@EXAMPLE.COM",
                      tkey_lifetime=3600):
    """Configure DDNS server with GSS-TSIG.

    :param addr:
    :type addr:
    :param dns_system:
    :type dns_system:
    :param client_principal: (Default value = "DHCP/admin.example.com@EXAMPLE.COM")
    :type client_principal:
    :param client_tab: (Default value = "FILE:/tmp/dhcp.keytab")
    :type client_tab:
    :param fallback: (Default value = False)
    :type fallback:
    :param retry_interval: (Default value = None)
    :type retry_interval:
    :param rekey_interval: (Default value = None)
    :type rekey_interval:
    :param server_id: (Default value = "server1")
    :type server_id:
    :param server_principal: (Default value = "DNS/server.example.com@EXAMPLE.COM")
    :type server_principal:
    :param tkey_lifetime: (Default value = 3600)
    :type tkey_lifetime:
    """
    ddns.ddns_add_gss_tsig(addr=addr, dns_system=dns_system, client_principal=client_principal, client_tab=client_tab,
                           fallback=fallback, retry_interval=retry_interval, rekey_interval=rekey_interval,
                           server_id=server_id, server_principal=server_principal, tkey_lifetime=tkey_lifetime)


@step(r'Use DNS set no. (\d+).')
def use_dns_set_number(number, override_dns_addr=None):
    """Use specific set of configs for bind 9, in future we can make this dynamic just like kea.

    :param number: int, number of set used
    :type number:
    :param override_dns_addr: string, for now it will be used only to switch between v4 and v6 in AD setup (Default value = None)
    :type override_dns_addr:
    """
    dns.use_config_set(int(number), override_dns=override_dns_addr)


def print_cfg(service='DHCP'):
    """Print configuration.

    :param service: (Default value = 'DHCP')
    :type service:
    """
    if service.lower() == 'dhcp':
        print("DHCP config:")
        print(json.dumps(world.dhcp_cfg, sort_keys=True, indent=2, separators=(',', ': ')))
    elif service.lower() == 'ddns':
        print("DDNS config:")
        print(json.dumps(world.ddns_cfg, sort_keys=True, indent=2, separators=(',', ': ')))
    elif service.lower() == 'ca':
        print("Control Agent config:")
        print(json.dumps(world.ca_cfg, sort_keys=True, indent=2, separators=(',', ': ')))


def generate_certificate():
    """Generate certificate.

    :return:
    :rtype:
    """
    return dhcp.generate_certificate()


def enable_https(trust_anchor, cert_file, key_file, cert_required):
    """Enable HTTPS.

    :param trust_anchor:
    :type trust_anchor:
    :param cert_file:
    :type cert_file:
    :param key_file:
    :type key_file:
    :param cert_required:
    :type cert_required:
    """
    dhcp.enable_https(trust_anchor, cert_file, key_file, cert_required)
