# Copyright (C) 2014-2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Wlodzimierz Wencel

# pylint: disable=consider-using-f-string
# pylint: disable=consider-using-with
# pylint: disable=inconsistent-return-statements
# pylint: disable=line-too-long
# pylint: disable=no-else-return
# pylint: disable=possibly-unused-variable
# pylint: disable=unspecified-encoding
# pylint: disable=unused-argument
# pylint: disable=unused-import
# pylint: disable=broad-exception-caught

from src.softwaresupport.multi_server_functions import fabric_send_file, remove_local_file
from src.softwaresupport.multi_server_functions import copy_configuration_file, fabric_sudo_command, fabric_download_file

from src.forge_cfg import world

from src.softwaresupport.isc_dhcp6_server.functions import set_time, unset_time, stop_srv, convert_cfg_file
from src.softwaresupport.isc_dhcp6_server.functions import restart_srv, clear_all, save_leases, save_logs, start_srv
from src.softwaresupport.isc_dhcp6_server.functions import add_line_in_global, check_process_result, clear_leases
from src.softwaresupport.isc_dhcp6_server.functions import simple_file_layout, build_leases_path, build_log_path
from src.softwaresupport.isc_dhcp4_server.functions_ddns import build_ddns_config

# option names in isc-dhcp v4, list is that you can check which one is different then Kea names - Kea names are used
# in test scenarios.

isc_dhcp_options4 = [
    "subnet-mask",
    "time-offset",
    "routers",
    "time-servers",
    "ien116-name-servers",
    "domain-name-servers",
    "log-servers",
    "cookie-servers",
    "lpr-servers",
    "impress-servers",
    "resource-location-servers",
    "host-name",
    "boot-size",
    "merit-dump",
    "domain-name",
    "swap-server",
    "root-path",
    "extensions-path",
    "ip-forwarding",
    "non-local-source-routing",
    "policy-filter",
    "max-dgram-reassembly",
    "default-ip-ttl",
    "path-mtu-aging-timeout",
    "path-mtu-plateau-table",
    "interface-mtu",
    "all-subnets-local",
    "broadcast-address",
    "perform-mask-discovery",
    "mask-supplier",
    "router-discovery",
    "router-solicitation-address",
    "static-routes",
    "trailer-encapsulation",
    "arp-cache-timeout",
    "ieee802-3-encapsulation",
    "default-tcp-ttl",
    "tcp-keepalive-interval",
    "tcp-keepalive-garbage",
    "nis-domain",
    "nis-servers",
    "ntp-servers",
    "vendor-encapsulated-options",
    "netbios-name-servers",
    "netbios-dd-server",
    "netbios-node-type",
    "netbios-scope",
    "font-servers",
    "x-display-manager",
    "dhcp-requested-address",
    "dhcp-lease-time",
    "dhcp-option-overload",
    "dhcp-message-type",
    "dhcp-server-identifier",
    "dhcp-parameter-request-list",
    "dhcp-message",
    "dhcp-max-message-size",
    "dhcp-renewal-time",
    "dhcp-rebinding-time",
    "vendor-class-identifier",
    "dhcp-client-identifier",
    "nwip-domain",
    "nisplus-domain",
    "nisplus-servers",
    "tftp-server-name",
    "bootfile-name",
    "mobile-ip-home-agent",
    "smtp-server",
    "pop-server",
    "nntp-server",
    "www-server",
    "finger-server",
    "irc-server",
    "streettalk-server",
    "streettalk-directory",
    "assistance-server",
    "user-class",
    "slp-directory-agent",
    "slp-service-scope",
    "nds-servers",
    "nds-tree-name",
    "nds-context",
    "bcms-controller-names",
    "bcms-controller-address",
    "uap-servers",
    "netinfo-server-address",
    "netinfo-server-tag",
    "default-url",
    "subnet-selection",
    "domain-search",
    "vivso",
]

isc_dhcp_options4_different_name = {
    "name-servers": "ien116-name-servers",
    "boot-file-name": "bootfile-name",
    "nwip-domain-name": "nwip-domain"
}

# for vendor options, not checked with specs, that could need changes!
isc_dhcp_otheroptions = {
    "tftp-servers": 32,
    "config-file": 33,
    "syslog-servers": 34,
    "time-servers": 37,
    "time-offset": 38
}

isc_dhcp_otheroptions_value_type = {
    "tftp-servers": "array of ip-address",
    "config-file": "text",
    "syslog-servers": "array of ip-address",
    "time-servers": "array of ip-address",
    "time-offset": "integer 16"
}

# add " "
needs_changing_quote = [
    "host-name",
    "root-path",
    "extensions-path",
    "nis-domain",
    "nwip-domain"
]

needs_changing_comma = [
    "policy-filter",
    "static-routes"
]


def add_siaddr(addr, subnet_number):
    """
    Change siaddr value in a particular subnet.
    :param addr: string with ip address
    :param subnet_number: int with subnet id
    :return:
    """
    if subnet_number is None:
        if "simple_options" not in world.cfg:
            world.cfg["simple_options"] = ''
        world.cfg["simple_options"] += 'next-server {addr};'.format(**locals())
    else:
        subnet = int(subnet_number)
        world.subcfg[subnet][0] += 'next-server {addr};'.format(**locals())


def add_defaults():
    """
    Add default values in the config file
    """
    if "conf_time" not in world.cfg:
        world.cfg["conf_time"] = ""

    value = world.cfg["server_times"]["renew-timer"]
    if value is not None:
        world.cfg["conf_time"] += '''option dhcp-renewal-time {0};\n'''.format(value)

    value = world.cfg["server_times"]["rebind-timer"]
    if value is not None:
        world.cfg["conf_time"] += '''option dhcp-rebinding-time {0};\n'''.format(value)

    value = world.cfg["server_times"]["valid-lifetime"]
    if value is not None:
        world.cfg["conf_time"] += '''default-lease-time {0};\n'''.format(value)


def netmask(subnet):
    """
    Add netmask to configuration based on subnet
    :param subnet: string with subnet
    :return: string with replaced int value to netmask text
    """
    # this is ugly and easiest hack, just for standard values of netmasks
    # TODO: enable using all netmasks!
    tmp_subnet = subnet.split("/")
    if tmp_subnet[1] == '8':
        return tmp_subnet[0] + " netmask 255.0.0.0 "
    elif tmp_subnet[1] == '16':
        return tmp_subnet[0] + " netmask 255.255.0.0 "
    elif tmp_subnet[1] == '24':
        return tmp_subnet[0] + " netmask 255.255.255.0 "


def prepare_cfg_subnet(subnet, pool, iface=None):
    """
    Add first subnet of configuration with possible default values
    :param subnet: string with subnet
    :param pool: string with pool
    :param iface: not used
    """
    if "conf_subnet" not in world.cfg:
        world.cfg["conf_subnet"] = ""

    world.cfg["subnet"] = subnet
    pointer = '{'

    if subnet == "default":
        subnet = "192.168.0.0 netmask 255.255.255.0"

    if pool == "default":
        pool = "192.168.0.1 192.168.0.254"

    else:
        # switch from /XX for XXX.XXX.XXX.XXX
        subnet = netmask(subnet)
        # isc-dhcp uses whitespace to separate.
        pool = pool.replace('-', ' ')

    # world.cfg["conf_subnet"] += '''
    world.subcfg[world.dhcp["subnet_cnt"]][0] += '''
        subnet {subnet} {pointer}
            range {pool};
        '''.format(**locals())


def add_pool_to_subnet(pool, subnet):
    """
    Add pool to indicated subnet
    :param pool: string with pool
    :param subnet: int with subnet id
    """
    if pool == "default":
        pool = "192.168.0.1 192.168.0.254"
    else:
        pool = pool.replace('-', ' ')

    world.subcfg[subnet][0] += 'range {pool};'.format(**locals())


def config_srv_another_subnet(subnet, pool, eth):
    """
    Add first subnet of configuration with possible default values
    :param subnet: string with subnet
    :param pool: string with pool
    :param eth: not used
    """
    # it will pass ethernet interface but it will have no impact on config files
    world.subcfg.append(["", "", "", ""])
    world.dhcp["subnet_cnt"] += 1

    prepare_cfg_subnet(subnet, pool, eth)


def remove_comma(string):
    """
    because we in ISC-DHCP we separate ip addresses with whitespace and
    pairs of ip addresses with comma we need to remove every odd comma from configuration
    :param string: list of addresses
    """
    ##
    ##
    flag = False
    tmp = ""
    for each in string:
        if each == "," and not flag:
            flag = True
            tmp += " "
        elif each == "," and flag:
            tmp += each + " "
            flag = False
        else:
            tmp += each

    return tmp


def prepare_cfg_add_option(option_name, option_value, space='dhcp', always_send=None):
    """
    Add option to global part of configuration
    :param option_name: string with option name
    :param option_value: string with option value
    :param space: string on which option should be configured
    """
    if "conf_option" not in world.cfg:
        world.cfg["conf_option"] = ""

    if space == 'dhcp4':
        space = 'dhcp'
    # first check it in options that names are different then those used in kea
    option_proper_name = isc_dhcp_options4_different_name.get(option_name)
    # if there is no changes pass name directly to config file:
    if option_proper_name is None:
        option_proper_name = option_name

    # some functions needs " " in it, so lets add them
    # that's for all those functions which are configured
    # indifferent way then kea6 configuration, if you add
    # new such option, add it to needs_changing list.
    if option_proper_name in needs_changing_quote:
        tmp = option_value.split(",")
        option_value = ','.join('"' + item + '"' for item in tmp)

    if option_proper_name in needs_changing_comma:
        option_value = remove_comma(option_value)

    # for all common options
    if space == 'dhcp':
        world.cfg["conf_option"] += ''' option dhcp.{option_proper_name} {option_value};
                '''.format(**locals())

    # for vendor option, for now we support only one vendor in config file
    else:
        # check if we already have space in config
        if "conf_vendor" not in world.cfg:
            # if not add new
            # code width 2 length width 2 hash size 3
            world.cfg["conf_vendor"] = '''
                option space {space} code width 2 length width 2;
                '''.format(**locals())

        # if we have space configured check if we try to add new vendor
        elif "conf_vendor" in world.cfg and space not in world.cfg["conf_vendor"]:
            world.cfg["conf_vendor"] += '''
                option space {space} code width 2 length width 2;
                '''.format(**locals())

        value_type = isc_dhcp_otheroptions_value_type.get(option_name)
        world.cfg["conf_vendor"] += '''
            option {space}.{option_name} code {option_proper_name} = {value_type};
            option {space}.{option_name} {option_value};
            '''.format(**locals())


def prepare_cfg_add_custom_option(opt_name, opt_code, opt_type, opt_value, space):
    # implement this
    pass  # http://linux.die.net/man/5/dhcp-options


def prepare_cfg_add_option_subnet(option_name, subnet, option_value, space='dhcp', always_send=None):
    """
    Add option configuration in specific subnet
    :param option_name: string with option name
    :param subnet: int, subnet id
    :param option_value: string with option value
    :param space: string with space on which option have to be configured
    """
    if "conf_subnet" not in world.cfg:
        assert False, 'Configure subnet/pool first, then subnet options'

    option_proper_name = isc_dhcp_options4_different_name.get(option_name)
    # if there is no changes pass name directly to config file:
    if option_proper_name is None:
        option_proper_name = option_name

    subnet = int(subnet)
    if option_proper_name in needs_changing_quote:
        tmp = option_value.split(",")
        option_value = ','.join('"' + item + '"' for item in tmp)

    if option_proper_name in needs_changing_comma:
        option_value = option_value.replace(",", " ")

    if space == 'dhcp':
        world.subcfg[subnet][0] += 'option {space}.{option_proper_name} {option_value};'.format(**locals())

    # for vendor option, for now we support only one vendor in config file
    else:
        # check if we already have space in config
        value_type = isc_dhcp_otheroptions_value_type.get(option_name)
        if "conf_vendor" not in world.cfg:
            # if not add new
            # code width 2 length width 2 hash size 3
            world.cfg["conf_vendor"] = '''
                option space {space} code width 2 length width 2;
                option {space}.{option_name} code {option_proper_name} = {value_type};
                '''.format(**locals())

        # if we have space configured check if we try to add new vendor
        elif "conf_vendor" in world.cfg and space not in world.cfg["conf_vendor"]:
            world.cfg["conf_vendor"] += '''
                option {space}.{option_name} code {option_proper_name} = {value_type};
                option space {space} code width 2 length width 2;
                '''.format(**locals())

        world.subcfg[subnet][0] += '''
            option {space}.{option_name} {option_value};
            '''.format(**locals())


def prepare_cfg_prefix(prefix, length, delegated_length, subnet):
    assert False, "This function can be used only with DHCPv6"


def host_reservation(reservation_type, reserved_value, unique_host_value, un_used):
    """
    Create host reservation
    :param reservation_type: string, "address" is only accepted value
    :param reserved_value: string with reserved ip address
    :param unique_host_value: string with mac address for reservation
    :param un_used: not used
    """
    pointer_start = "{"
    pointer_end = "}"
    if "custom_lines" not in world.cfg:
        world.cfg["custom_lines"] = ""
    host_name = "anyhostname_"+str(len(world.cfg["custom_lines"]))

    if reservation_type == "address":
        world.cfg["custom_lines"] += '''host {host_name} {pointer_start} hardware ethernet {unique_host_value};
                                    fixed-address {reserved_value}; {pointer_end}'''.format(**locals())


def host_reservation_extension(reservation_number, subnet, reservation_type, reserved_value):
    assert False, "not used in isc-dhcp"
    # TODO implement this if needed


def cfg_write():
    """
    Combine all parts into single configuration file and save it
    """
    cfg_file = open(world.cfg["cfg_file"], 'w')
    cfg_file.write(world.cfg["conf_time"])
    cfg_file.write("authoritative;\n")

    if "log_facility" in world.cfg:
        cfg_file.write(world.cfg["log_facility"])

    if "custom_lines" in world.cfg:
        cfg_file.write(world.cfg["custom_lines"])

    if "conf_option" in world.cfg:
        cfg_file.write(world.cfg["conf_option"])

    if "conf_vendor" in world.cfg:
        cfg_file.write(world.cfg["conf_vendor"])

    if world.ddns_enable:
        build_ddns_config()
        cfg_file.write(world.ddns)
        # ddns we can add just to one subnet, for now
        world.subcfg[0][0] += 'ddns-rev-domainname "' + world.ddns_rev_domainname + '";'
        world.subcfg[0][0] += 'ddns-domainname "' + world.ddns_domainname + '";'

    for each_subnet in world.subcfg:
        if each_subnet[0] != "":
            cfg_file.write(each_subnet[0])
            cfg_file.write('}')  # add } for subnet block

    cfg_file.close()
    simple_file_layout()


def build_and_send_config_files(cfg, destination_address):
    """
    Build ISC-DHCP config file and send it to remote server
    :param cfg: not used
    :param destination_address: string with ip address
    """
    if "conf_option" not in world.cfg:
        world.cfg["conf_option"] = ""

    world.cfg['log_file'] = build_log_path()
    fabric_sudo_command('rm -f ' + world.cfg['log_file'], destination_host=destination_address)
    world.cfg["dhcp_log_file"] = world.cfg['log_file']

    log = "local7"
    if world.f_cfg.isc_dhcp_log_facility != "":
        log = world.f_cfg.isc_dhcp_log_facility

    world.cfg['log_facility'] = '''\nlog-facility {log};\n'''.format(**locals())

    add_defaults()
    cfg_write()
    convert_cfg_file(world.cfg["cfg_file"])
    fabric_send_file(world.cfg["cfg_file"] + '_processed', world.cfg["cfg_file"] + '_processed',
                     destination_host=destination_address)
    copy_configuration_file(world.cfg["cfg_file"] + '_processed')
    remove_local_file(world.cfg["cfg_file"])

    stop_srv(destination_address=destination_address)


def config_client_classification(subnet, option_value):
    assert False, "TODO!"
