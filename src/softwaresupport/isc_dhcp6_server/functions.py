# Copyright (C) 2014-2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Wlodzimierz Wencel

# pylint: disable=consider-using-f-string
# pylint: disable=consider-using-with
# pylint: disable=invalid-name
# pylint: disable=no-else-continue
# pylint: disable=possibly-unused-variable
# pylint: disable=redefined-outer-name
# pylint: disable=unspecified-encoding
# pylint: disable=unused-argument
# pylint: disable=unused-import
# pylint: disable=unused-variable
# pylint: disable=broad-exception-caught

import logging
import os
from src.forge_cfg import world

from src.softwaresupport.multi_server_functions import fabric_run_command, fabric_send_file, \
    remove_local_file, copy_configuration_file, fabric_sudo_command, fabric_download_file, \
    fabric_remove_file_command
from src.softwaresupport.isc_dhcp6_server.functions_ddns import build_ddns_config
from src.softwaresupport.multi_server_functions import check_local_path_for_downloaded_files
from src.protosupport.multi_protocol_functions import test_define_value

log = logging.getLogger('forge')


# it would be wise to remove redundant names,
# but I'll leave it that way for now.
isc_dhcp_options6 = {
    "preference": "preference",
    "rapid_commit": "rapid-commit",
    "interface-id": "interface-id",
    "sip-server-dns": "sip-servers-names",
    "sip-server-addr": "sip-servers-addresses",
    "dns-servers": "name-servers",
    "domain-search": "domain-search",
    "nis-servers": "nis-servers",
    "nisp-servers": "nisp-servers",
    "nis-domain-name": "nis-domain-name",
    "nisp-domain-name": "nisp-domain-name",
    "sntp-servers": "sntp-servers",
    "information-refresh-time": "info-refresh-time",
    "bcmcs-server-dns": "bcms-server-d",
    "bcmcs-server-addr": "bcms-server-a"
}

needs_changing = {
    "sip-servers-names": True,
    "domain-name-servers": True,
    "domain-search": True,
    "nis-domain-name": True,
    "nisp-domain-name": True,
    "new-posix-timezone": True,
    "new-tzdb-timezone": True,
    "bootfile-url": True,
    "bootfile-param": True,
    "bcms-server-d": True,
    33: True  # for 'config file', that will need more work:)
}

# mostly for vendor options
isc_dhcp_otheroptions = {
    "tftp-servers": 32,
    "config-file": 33,
    "syslog-servers": 34,
    "time-servers": 37,
    "time-offset": 38
}

isc_dhcp_otheroptions_value_type = {
    "tftp-servers": "array of ip6-address",
    "config-file": "text",
    "syslog-servers": "array of ip6-address",
    "time-servers": "array of ip6-address",
    "time-offset": "integer 16"
}


def switch_prefix6_lengths_to_pool(ip6_addr, length, delegated_length):
    """
    Calculate prefix pool from prefix length and prefix delegated length (different notation than in Kea)
    :param ip6_addr: subnet ip address
    :param length: int prefix length
    :param delegated_length: int prefix delegated length
    """

    ip6_addr_split = ip6_addr.split(":")
    if len(ip6_addr_split) < 3 or len(ip6_addr_split) > 9:
        assert False, "Error! Please enter correct IPv6 address!"
    error_flag = False
    for i in range(1, len(ip6_addr_split) - 1):
        if not ip6_addr_split[i]:
            if error_flag:
                assert False, "Error! Please enter correct IPv6 address!"
            error_flag = True

    for i in range(0, 6):
        if ip6_addr_split[i]:
            continue
        else:
            ip6_addr_split.append("")

    bin_addr = []
    for each in ip6_addr_split:
        if not each:
            bin_addr.append('')
            continue
        bin_addr.append(bin(int(each, 16)))

    tmp_str = ""
    for each in bin_addr:
        each = each.zfill(18)
        if "0b" in each:
            each = each.replace("0b", "")
        else:
            each = each[2:]
        tmp_str += each
    lowest_prefix = tmp_str
    highest_prefix = lowest_prefix[0:length] + '1' * (delegated_length - length) + lowest_prefix[delegated_length:]

    ip6_addr_new = []
    for i in range(0, 8):
        ip6_addr_new.append(highest_prefix[:16])
        highest_prefix = highest_prefix[16:]

    tmp = []
    for each in ip6_addr_new:
        b = hex(int(each, 2))
        tmp.append(b[2:])

    prefix = []
    flag1 = False
    flag2 = False
    for i in range(0, 8):
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
    if final[-1] == ":":
        final += ":"
    return final


def restart_srv(destination_address=world.f_cfg.mgmt_address):
    """
    Restart ISC-DHCP on remote system
    :param destination_address: string with ip address of remote system
    """
    stop_srv(destination_address=destination_address)
    fabric_sudo_command('(' + os.path.join(world.f_cfg.software_install_path, f'sbin/dhcpd -{world.proto[1]}')
                        + '-cf server.cfg_processed -lf '
                        + build_leases_path() + '); sleep ' + str(world.f_cfg.sleep_time_1) + ';',
                        destination_host=destination_address)


def set_time(which_time, value, subnet=None):
    """
    Change default value of configured time
    :param which_time: string with parameter name
    :param value: int with timer value
    :param subnet: int subnet id
    :return:
    """
    assert which_time in world.cfg["server_times"], "Unknown time name: %s" % which_time
    if subnet is None:
        world.cfg["server_times"][which_time] = value
    else:
        subnet = int(subnet)
        if which_time == "renew-timer":
            world.subcfg[subnet][0] += 'option dhcp-renewal-time {value};'.format(**locals())
        elif which_time == "rebind-timer":
            world.subcfg[subnet][0] += 'option dhcp-rebinding-time {value};'.format(**locals())
        elif which_time == "preferred-lifetime":
            world.subcfg[subnet][0] += 'preferred-lifetime {value};'.format(**locals())
        elif which_time == "valid-lifetime":
            world.subcfg[subnet][0] += 'default-lease-time {value};'.format(**locals())
        else:
            assert False, "If you see that message something went terribly wrong! Please report bug!"


def unset_time(which_time, subnet=None):
    """
    Remove single timer from configuration
    :param which_time: string with timer name e.g. "renew-timer"
    :param subnet: not used
    """
    if which_time in world.cfg["server_times"]:
        world.cfg["server_times"][which_time] = None
    else:
        assert which_time in world.cfg["server_times"], "Unknown time name: %s" % which_time


def add_defaults():
    """
    Add default parameters to configuration
    """
    if "conf_time" not in world.cfg:
        world.cfg["conf_time"] = ""

    value = world.cfg["server_times"]["renew-timer"]
    if value is not None:
        world.cfg["conf_time"] += '''option dhcp-renewal-time {0};\n'''.format(value)

    value = world.cfg["server_times"]["rebind-timer"]
    if value is not None:
        world.cfg["conf_time"] += '''option dhcp-rebinding-time {0};\n'''.format(value)

    value = world.cfg["server_times"]["preferred-lifetime"]
    if value is not None:
        world.cfg["conf_time"] += '''preferred-lifetime {0};\n'''.format(value)

    value = world.cfg["server_times"]["valid-lifetime"]
    if value is not None:
        world.cfg["conf_time"] += '''default-lease-time {0};\n'''.format(value)

    if world.cfg["server_times"]["rapid-commit"]:
        world.cfg["conf_time"] += '''
            option dhcp6.rapid-commit;
            '''


def add_pool_to_subnet(pool, subnet):
    """
    Add pool to indicated subnet
    :param pool: string with pool
    :param subnet: int with subnet id
    """
    if pool == "default":
        pool = "2001:db8:1::0 2001:db8:1::ffff"
    else:
        pool = pool.replace('-', ' ')

    world.subcfg[subnet][0] += f'range6 {pool};'


def prepare_cfg_subnet(subnet, pool, iface=None):
    """
    Add first subnet of configuration with possible default values
    :param subnet: string with subnet
    :param pool: string with pool
    :param iface: not used
    """
    # structure of world.subcfg is [["", "", "", "",""]] but we need only one argument in the list
    # every configuration added for subnets in ISC-DHCP is configured on the same level
    # so we use here: world.subcfg[0] = [all_options]
    if "conf_subnet" not in world.cfg:
        world.cfg["conf_subnet"] = ""

    # in case we will enable ip address changing on interface under test
    world.cfg["subnet"] = subnet

    if subnet == "default":
        subnet = "2001:db8:1::/64"

    if pool == "default":
        pool = "2001:db8:1::0 2001:db8:1::ffff"
    else:
        pool = pool.replace('-', ' ')

    tmp = None
    if len(world.subcfg[world.dhcp["subnet_cnt"]][0]) > 0:
        tmp = world.subcfg[world.dhcp["subnet_cnt"]][0]
        world.subcfg[world.dhcp["subnet_cnt"]][0] = ""

    # world.cfg["conf_subnet"] += '''
    world.subcfg[world.dhcp["subnet_cnt"]][0] += f'''
        subnet6 {subnet} {{
            range6 {pool};
        '''

    if tmp is not None:
        world.subcfg[world.dhcp["subnet_cnt"]][0] += tmp


def config_srv_another_subnet(subnet, pool, eth):
    """
    Create new subnet configuration and add there indicated subnet
    :param subnet: string with subnet
    :param pool: string with pool
    :param eth: not used in isc-dhcp
    """
    # it will pass ethernet interface but it will have no impact on config files
    world.subcfg.append(["", "", "", "", "", ""])
    world.dhcp["subnet_cnt"] += 1

    prepare_cfg_subnet(subnet, pool, eth)


def prepare_cfg_add_option(option_name, option_value, space, always_send=None):
    """
    Add option to global part of configuration
    :param option_name: string with option name
    :param option_value: string with option value
    :param space: string on which option should be configured
    """
    if "conf_option" not in world.cfg:
        world.cfg["conf_option"] = ""

    # first check it in global options
    option_proper_name = isc_dhcp_options6.get(option_name)

    # is there is no such options check it in 'isc_dhcp_otheroptions'
    # it's mostly vendor options
    if option_proper_name is None:
        option_proper_name = isc_dhcp_otheroptions.get(option_name)

    # if it's still None... pass option name from test without changing
    if option_proper_name is None:
        option_proper_name = option_name

    # some functions needs " " in it, so lets add them
    # that's for all those functions which are configured
    # indifferent way then kea6 configuration, if you add
    # new such option, add it to needs_changing dict.
    if needs_changing.get(option_proper_name):
        if option_proper_name in ["new-posix-timezone", "new-tzdb-timezone"]:
            option_value = '"' + option_value + '"'
        else:
            tmp = option_value.split(",")
            option_value = ','.join('"' + item + '"' for item in tmp)

    # for all common options
    if space == 'dhcp6':
        world.cfg["conf_option"] += f''' option dhcp6.{option_proper_name} {option_value};
                '''

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
            world.cfg["conf_vendor"] += f'''
                option space {space} code width 2 length width 2;
                '''

        value_type = isc_dhcp_otheroptions_value_type.get(option_name)
        world.cfg["conf_vendor"] += f'''
            option {space}.{option_name} code {option_proper_name} = {value_type};
            option {space}.{option_name} {option_value};
            '''


def prepare_cfg_prefix(prefix, length, delegated_length, subnet):
    """
    Add prefix configuration
    :param prefix: string with prefix
    :param length: int prefix length
    :param delegated_length: int prefix delegated length
    :param subnet: int subnet id in which prefix have to be configured
    :return:
    """
    subnet = int(subnet)

    highest = switch_prefix6_lengths_to_pool(str(prefix), int(length), int(delegated_length))

    # world.cfg["conf_subnet"] += '''prefix6 {prefix} {highest} /{delegated_length};
    world.subcfg[subnet][0] += f'prefix6 {prefix} {highest} /{delegated_length};'


def prepare_cfg_add_custom_option(opt_name, opt_code, opt_type, opt_value, space):
    # implement this
    pass  # http://linux.die.net/man/5/dhcp-options


def config_client_classification(subnet, option_value):
    assert False, "TODO!"


def prepare_cfg_add_option_subnet(option_name, subnet, option_value, space='dhcp6', always_send=None):
    """
    Add option configuration in specific subnet
    :param option_name: string with option name
    :param subnet: int, subnet id
    :param option_value: string with option value
    :param space: string with space on which option have to be configured
    """
    if "conf_subnet" not in world.cfg:
        assert False, 'Configure subnet/pool first, then subnet options'

    option_proper_name = isc_dhcp_options6.get(option_name)

    if option_proper_name is None:
        option_proper_name = isc_dhcp_otheroptions.get(option_name)

    elif option_proper_name is None:
        assert False, "Unsupported option name " + option_name

    subnet = int(subnet)
    if needs_changing.get(option_proper_name):
        tmp = option_value.split(",")
        option_value = ','.join('"' + item + '"' for item in tmp)

    if space == 'dhcp6':
        world.subcfg[subnet][0] += f'option {space}.{option_proper_name} {option_value};'

    # for vendor option, for now we support only one vendor in config file
    else:
        # check if we already have space in config
        value_type = isc_dhcp_otheroptions_value_type.get(option_name)
        if "conf_vendor" not in world.cfg:
            # if not add new
            # code width 2 length width 2 hash size 3
            world.cfg["conf_vendor"] = f'''
                option space {space} code width 2 length width 2;
                option {space}.{option_name} code {option_proper_name} = {value_type};
                '''

        # if we have space configured check if we try to add new vendor
        elif "conf_vendor" in world.cfg and space not in world.cfg["conf_vendor"]:
            world.cfg["conf_vendor"] += f'''
                option {space}.{option_name} code {option_proper_name} = {value_type};
                option space {space} code width 2 length width 2;
                '''

        world.subcfg[subnet][0] += f'option {space}.{option_name} {option_value};'


def host_reservation(reservation_type, reserved_value, unique_host_value, un_used):
    """
    Create host reservation
    :param reservation_type: string, "address" is only accepted value
    :param reserved_value: string with reserved ip address
    :param unique_host_value: string with mac address for reservation
    :param un_used: not used
    """
    if "custom_lines" not in world.cfg:
        world.cfg["custom_lines"] = ""
    host_name = "anyhostname_"+str(len(world.cfg["custom_lines"]))

    if reservation_type == "address":
        world.cfg["custom_lines"] += f'''host {host_name} {{ hardware ethernet {unique_host_value};
                                    fixed-address6 {reserved_value}; }}'''
    else:
        assert False, "Not supported"
        # TODO! implement this!


def host_reservation_extension(reservation_number, subnet, reservation_type, reserved_value):
    assert False, "not used in isc-dhcp"
    # TODO implement this if needed


def cfg_write():
    """
    Build config file from all previously added options, subnets and parameters.
    """
    cfg_file = open(world.cfg["cfg_file"], 'w')
    cfg_file.write(world.cfg["conf_time"])

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
        cfg_file.write(each_subnet[0])
        cfg_file.write('}')  # add } for subnet block

    cfg_file.close()
    simple_file_layout()


def convert_cfg_file(cfg):
    """
    Change layout of config file
    :param cfg: path to config file
    """
    tmpfile = cfg + "_processed"
    conf = open(cfg, "rt")
    process = open(tmpfile, "w")
    tab_flag = False
    # Copy input line by line, but skip empty and comment lines
    for line in conf:
        line = line.strip()
        if len(line) < 1:
            continue
        if line[0] == "#":
            continue
        if "}" in line:
            tab_flag = False
        if tab_flag:
            process.write("\t" + line + "\n")
        if not tab_flag:
            process.write(line + "\n")
        if "{" in line:
            tab_flag = True

    conf.close()
    process.close()
    remove_local_file(cfg)


def set_ethernet_interface():
    """
    To start ISC-DHCPv6 we need set some address from chosen pool on one ethernet interface
    """
    tmp = world.cfg["subnet"].split('/')
    address = tmp[0] + "1/" + tmp[1]
    eth = world.f_cfg.server_iface
    cmd = f'ip addr flush {eth}'
    cmd1 = f'ip -6 addr add {address} dev {eth}'


def build_leases_path():
    """
    :return: static value, path to leases file, do not change
    """
    return '/tmp/dhcpd.leases'


def build_log_path():
    """
    :return: static value, path to log file, do not change
    """
    # syslog/rsyslog typically will not write to log files unless
    # they are in /var/log without manual intervention.
    return '/var/log/forge_dhcpd.log'


def build_and_send_config_files(destination_address=world.f_cfg.mgmt_address, cfg=None):
    """
    Build and send ISC-DHCP configuration file to specific location
    :param destination_address: string with ip address of remote server running ISC-DHCP
    :param cfg: not used here
    """
    if "conf_option" not in world.cfg:
        world.cfg["conf_option"] = ""

    world.cfg['dhcp_log_file'] = build_log_path()

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


def check_process_result(succeed: bool, result: str):
    """
    Check result of starting ISC-DHCP
    :param succeed: True/False, True if we expect ISC-DHCP to start successfully
    :param result: logs from ISC-DHCP
    :return:
    """
    errors = ["exiting."]
    for each in errors:
        if succeed is True:
            if each in result:
                assert False, 'Server configuration/starting process failed!'
        else:
            if each not in result:
                assert False, 'Server configuration/starting process NOT failed!'


def add_line_in_global(command):
    """
    Add line to ISC-DHCP configuration file, will also perform replacing $() values
    :param command: string with line added to config file
    """
    command = test_define_value(command)[0]
    if "custom_lines" not in world.cfg:
        world.cfg["custom_lines"] = ''

    world.cfg["custom_lines"] += ('\n' + command + '\n')


def set_conf_parameter_global(parameter_name, value):
    """
    Add parameter in global configuration file of ISC-DHCP server
    :param parameter_name: string with parameter name
    :param value: sting with value of configured parameter
    :return:
    """
    if "custom_lines" not in world.cfg:
        world.cfg["custom_lines"] = ''
    if parameter_name == "rapid-commit":
        world.cfg["custom_lines"] += '\noption dhcp6.rapid-commit;\n'
    else:
        world.cfg["custom_lines"] += ('\n' + parameter_name + ' ' + value + ';\n')


def set_conf_parameter_subnet(parameter_name, value, subnet_id):
    """
    Add rapid commit option to specific subnet in server config file
    :param parameter_name: string with parameter name, here can only be rapid-commit
    :param value: True/False, True if we want to add this parameter
    :param subnet_id: id of subnet that should be configured
    """
    if parameter_name == "rapid-commit":
        if value == 'true':
            world.subcfg[subnet_id][0] += 'option dhcp6.rapid-commit;'
    else:
        pass
        # world.subcfg[subnet_id][0] += '{parameter_name} {value};'.format(**locals())


def start_srv(start: bool, destination_address: str = world.f_cfg.mgmt_address):
    """
    Start ISC-DHCP server on remote system
    :param start: binary value of expected result, True if server should successfully start
    :param process: None
    :param destination_address: string with ip address of remote system
    :return:
    """
    world.cfg['leases'] = build_leases_path()
    result = fabric_sudo_command('(' + os.path.join(world.f_cfg.software_install_path, f'sbin/dhcpd -{world.proto[1]}')
                                 + ' -cf server.cfg_processed'
                                 + ' -lf ' + build_leases_path()
                                 + '&); sleep ' + str(world.f_cfg.sleep_time_1) + ';',
                                 destination_host=destination_address)

    check_process_result(start, result)

    # clear configs in case we would like make couple configs in one test
    world.cfg["conf_time"] = ""
    world.cfg["log_facility"] = ""
    world.cfg["custom_lines"] = ""
    world.cfg["conf_option"] = ""
    world.cfg["conf_vendor"] = ""


def save_leases(destination_address=world.f_cfg.mgmt_address):
    """
    Download leases ISC-DHCP file from remote system
    :param destination_address: string with ip address
    """
    fabric_download_file(build_leases_path(),
                         check_local_path_for_downloaded_files(world.cfg["test_result_dir"],
                                                               'dhcpd.leases',
                                                               destination_address),
                         destination_host=destination_address)


def save_logs(destination_address=world.f_cfg.mgmt_address):
    """
    Download logs into tests_results
    :param destination_address: string with ip address of system running ISC-DHCP
    """
    if world.cfg["dhcp_log_file"] == "~/none_file":
        return

    try:
        # sometimes log file is not created, ignore it than.....
        fabric_download_file(build_log_path(),
                             check_local_path_for_downloaded_files(world.cfg["test_result_dir"],
                                                                   'forge_dhcpd.log',
                                                                   destination_address),
                             destination_host=destination_address)
    except BaseException:
        pass


def clear_leases(destination_address=world.f_cfg.mgmt_address,
                 software_install_path=world.f_cfg.software_install_path, db_user=world.f_cfg.db_user,
                 db_passwd=world.f_cfg.db_passwd, db_name=world.f_cfg.db_name):
    """
    Clear leases file on remote system
    :param destination_address: string with ip address
    :param software_install_path: not used, path is static
    :param db_user: not used
    :param db_passwd: not used
    :param db_name: not used
    """
    fabric_sudo_command(f'true > {build_leases_path()}', destination_host=destination_address)


def stop_srv(destination_address=world.f_cfg.mgmt_address, value=False):
    """
    Stop ISC-DHCP server
    :param destination_address: string with ip address
    :param value: not used in isc-dhcp
    """
    fabric_sudo_command("killall dhcpd &>/dev/null", ignore_errors=True, destination_host=destination_address)


def clear_logs(destination_address=world.f_cfg.mgmt_address):
    """
    Remove ISC-DHCP logs from remote system
    :param destination_address: string with ip address
    """
    fabric_sudo_command(f'rm -f {build_log_path()}', destination_host=destination_address)
    fabric_sudo_command(f'touch {build_log_path()}', destination_host=destination_address)
    try:
        fabric_sudo_command(f'chown syslog:syslog {build_log_path()}', destination_host=destination_address)
    except BaseException:
        fabric_sudo_command(f'chown root:root {build_log_path()}', destination_host=destination_address)
    fabric_sudo_command(f'chmod 644 {build_log_path()}', destination_host=destination_address)
    fabric_sudo_command('systemctl restart rsyslog', destination_host=destination_address)


def clear_all(destination_address=world.f_cfg.mgmt_address,
              software_install_path=world.f_cfg.software_install_path, db_user=world.f_cfg.db_user,
              db_passwd=world.f_cfg.db_passwd, db_name=world.f_cfg.db_name):
    """
    Clean leases and logs from remote system
    :param destination_address: ip address of the host on which isc-dhcp is running
    :param software_install_path: path to installed binaries
    :param db_user: not used in isc-dhcp
    :param db_passwd: not used in isc-dhcp
    :param db_name: not used in isc-dhcp
    """
    try:
        clear_logs(destination_address=destination_address)
        clear_leases(destination_address=destination_address, software_install_path=software_install_path,
                     db_user=db_user, db_passwd=db_passwd, db_name=db_name)
    except BaseException:
        pass


# ISC-DHCP specific functions
def simple_file_layout():
    """
    Format dhcp config file, add missing brackets
    """
    config = open(world.cfg["cfg_file"], 'r')
    new_config = ""

    for each in config:
        new_line = each.strip()
        new_config += new_line
    config.close()

    real_config = ""
    counter = 0
    space = "\t"
    flag = 0

    for each in new_config:
        if each == '"' and flag == 0:
            flag = 1
            real_config += each

        elif each == '"' and flag == 1:
            flag = 0
            real_config += each

        elif each == "{" and flag == 0:
            real_config += space * counter + each
            counter += 1
            real_config += "\n" + space * counter

        elif each == "}" and flag == 0:
            counter -= 1
            real_config += "\n" + space * counter + each + "\n" + space * counter

        elif each == ";" and flag == 0:
            real_config += each + "\n" + space * counter
        else:
            real_config += each

    config = open(world.cfg["cfg_file"], 'w')
    config.write(real_config)
    log.info(real_config)
    config.close()
