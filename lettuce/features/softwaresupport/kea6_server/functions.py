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


from softwaresupport.multi_server_functions import fabric_run_command, fabric_send_file,\
    remove_local_file, copy_configuration_file, fabric_sudo_command, json_file_layout,\
    fabric_download_file, fabric_remove_file_command, locate_entry

from functions_ddns import add_forward_ddns, add_reverse_ddns, add_keys, build_ddns_config

from logging_facility import *
from lettuce.registry import world
from init_all import SOFTWARE_INSTALL_DIR, SAVE_LOGS, BIND_LOG_TYPE, BIND_LOG_LVL,\
    BIND_MODULE, SERVER_IFACE, SLEEP_TIME_2, SLEEP_TIME_1, SOFTWARE_UNDER_TEST, \
    SOFTWARE_INSTALL_DIR, DB_TYPE, DB_NAME, DB_USER, DB_PASSWD, DB_HOST
kea_options6 = {
    "client-id": 1,
    "server-id": 2,
    "IA_NA": 3,
    "IN_TA": 4,
    "IA_address": 5,
    "preference": 7,
    "relay-msg": 9,
    "status-code": 13,
    "rapid_commit": 14,
    "interface-id": 18,
    "sip-server-dns": 21,
    "sip-server-addr": 22,
    "dns-servers": 23,
    "domain-search": 24,
    "IA_PD": 25,
    "IA-Prefix": 26,
    "nis-servers": 27,
    "nisp-servers": 28,
    "nis-domain-name": 29,
    "nisp-domain-name": 30,
    "sntp-servers": 31,
    "information-refresh-time": 32
}
# kea_otheoptions was originally designed for vendor options
# because codes sometime overlap with basic options
kea_otheroptions = {
    "tftp-servers": 32,
    "config-file": 33,
    "syslog-servers": 34,
    "device-id": 36,
    "time-servers": 37,
    "time-offset": 38
}


def set_time(step, which_time, value, subnet = None):
    assert which_time in world.cfg["server_times"], "Unknown time name: %s" % which_time

    if subnet is None:
            world.cfg["server_times"][which_time] = value

    else:
        subnet = int(subnet)
        if len(world.subcfg[subnet][3]) > 2:
            world.subcfg[subnet][3] += ', '
        world.subcfg[subnet][3] += '"{which_time}": {value}'.format(**locals())

## =============================================================
## ================ PREPARE CONFIG BLOCK START =================
#  world.subcfg - is prepare for multi-subnet configuration
#  it's concatenated lists:
#  world.subcfg[0] - default subnet
#  each another subnet is append to world.subcfg


def add_interface(eth):
    if len(world.cfg["interfaces"]) > 3:
        world.cfg["interfaces"] += ','
    world.cfg["interfaces"] += '"{eth}"'.format(**locals())


def add_defaults():
    t1 = world.cfg["server_times"]["renew-timer"]
    t2 = world.cfg["server_times"]["rebind-timer"]
    t3 = world.cfg["server_times"]["preferred-lifetime"]
    t4 = world.cfg["server_times"]["valid-lifetime"]
    eth = SERVER_IFACE
    pointer_start = "{"
    pointer_end = "}"

    world.cfg["main"] = '''
        {pointer_start} "Dhcp6" :

        {pointer_start}
        "renew-timer": {t1},
        "rebind-timer": {t2},
        "preferred-lifetime": {t3},
        "valid-lifetime": {t4},
        '''.format(**locals())

    if eth is not None and not eth in world.cfg["interfaces"]:
        add_interface(eth)


def prepare_cfg_subnet(step, subnet, pool, eth = None):
    # world.subcfg[0] = [main, prefixes, options, single options, pools, host reservation]
    if subnet == "default":
        subnet = "2001:db8:1::/64"
    if pool == "default":
        pool = "2001:db8:1::1 - 2001:db8:1::ffff"
    if eth is None:
        eth = SERVER_IFACE

    if not "interfaces" in world.cfg:
        world.cfg["interfaces"] = ''

    pointer_start = "{"
    pointer_end = "}"

    world.subcfg[world.dhcp["subnet_cnt"]][0] += '''{pointer_start} "subnet": "{subnet}"
         '''.format(**locals())
    world.subcfg[world.dhcp["subnet_cnt"]][0] += ', "interface": "{eth}" '.format(**locals())
    if pool is not "":
        world.subcfg[world.dhcp["subnet_cnt"]][4] += '{pointer_start}"pool": "{pool}" {pointer_end}'.format(**locals())

    if not eth in world.cfg["interfaces"]:
        add_interface(eth)


def add_pool_to_subnet(step, pool, subnet):
    pointer_start = "{"
    pointer_end = "}"

    world.subcfg[subnet][4] += ',{pointer_start}"pool": "{pool}"{pointer_end}'.format(**locals())
    pass


def config_srv_another_subnet(step, subnet, pool, eth):
    world.subcfg.append(["", "", "", "", "", ""])
    world.dhcp["subnet_cnt"] += 1

    prepare_cfg_subnet(step, subnet, pool, eth)


def config_client_classification(step, subnet, option_value):
    subnet = int(subnet)
    if len(world.subcfg[subnet][3]) > 2:
        world.subcfg[subnet][3] += ', '
    world.subcfg[subnet][3] += '"client-class": "{option_value}"\n'.format(**locals())


def prepare_cfg_prefix(step, prefix, length, delegated_length, subnet):
    subnet = int(subnet)
    pointer_start = "{"
    pointer_end = "}"
    world.subcfg[subnet][1] += """
        "pd-pools": [
        {pointer_start}"delegated-len": {delegated_length},
        "prefix": "{prefix}",
        "prefix-len": {length} {pointer_end}]""".format(**locals())


def prepare_cfg_add_option(step, option_name, option_value, space,
                           option_code = None, option_type = 'default', where = 'options'):
    if not where in world.cfg:
        world.cfg[where] = '"option-data": ['
    else:
        world.cfg[where] += ","

    # check if we are configuring default option or user option via function "prepare_cfg_add_custom_option"
    if option_type == 'default':
        option_code = kea_options6.get(option_name)
        if option_code is None:
            option_code = kea_otheroptions.get(option_name)

    pointer_start = "{"
    pointer_end = "}"

    assert option_code is not None, "Unsupported option name for other Kea6 options: " + option_name

    world.cfg[where] += '''
            {pointer_start}"csv-format": true, "code": {option_code}, "data": "{option_value}",
            "name": "{option_name}", "space": "{space}"{pointer_end}'''.format(**locals())


def prepare_cfg_add_custom_option(step, opt_name, opt_code, opt_type, opt_value, space):
    pointer_start = "{"
    pointer_end = "}"

    if not "option_def" in world.cfg:
        world.cfg["option_def"] = '"option-def": ['
    else:
        world.cfg["option_def"] += ","

    # make definition of the new option
    world.cfg["option_def"] += '''
            {pointer_start}"code": {opt_code}, "name": "{opt_name}", "space": "{space}",
            "encapsulate": "", "record-types": "", "array": false, "type": "{opt_type}"{pointer_end}'''\
        .format(**locals())

    # add defined option
    prepare_cfg_add_option(step, opt_name, opt_value, space, opt_code, 'user')


def prepare_cfg_add_option_subnet(step, option_name, subnet, option_value):
    # check if we are configuring default option or user option via function "prepare_cfg_add_custom_option"
    space = world.cfg["space"]
    subnet = int(subnet)
    option_code = kea_options6.get(option_name)
    if option_code is None:
        option_code = kea_otheroptions.get(option_name)

    pointer_start = "{"
    pointer_end = "}"

    assert option_code is not None, "Unsupported option name for other Kea6 options: " + option_name
    if len(world.subcfg[subnet][2]) > 10:
        world.subcfg[subnet][2] += ','

    world.subcfg[subnet][2] += '''
            {pointer_start}"csv-format": true, "code": {option_code}, "data": "{option_value}",
            "name": "{option_name}", "space": "{space}"{pointer_end}'''.format(**locals())


def run_command(step, command):
    if not "custom_lines" in world.cfg:
        world.cfg["custom_lines"] = ''

    world.cfg["custom_lines"] += ('\n'+command+'\n')


def set_logger():
    pass
    assert False, "For now option unavailable!"


def host_reservation(reservation_type, reserved_value, unique_host_value, subnet):
    if len(world.subcfg[subnet][5]) > 20:
        world.subcfg[subnet][5] += ','

    if len(unique_host_value.replace(':', '')) == 12:
        unique_host_value_type = "hw-address"
    elif len(unique_host_value.replace(':', '')) > 12:
        unique_host_value_type = "duid"
    world.subcfg[subnet][5] += "{"
    if reservation_type == "address":
        world.subcfg[subnet][5] += '"{unique_host_value_type}":"{unique_host_value}",' \
                                   '"ip-addresses":["{reserved_value}"]'.format(**locals())
    elif reservation_type == "prefix":
        world.subcfg[subnet][5] += '"{unique_host_value_type}":"{unique_host_value}",' \
                                   '"prefixes":["{reserved_value}"]'.format(**locals())
    elif reservation_type == "hostname":
        world.subcfg[subnet][5] += '"{unique_host_value_type}":"{unique_host_value}",' \
                                   '"hostname":"{reserved_value}"'.format(**locals())
    world.subcfg[subnet][5] += "}"


def host_reservation_extension(reservation_number, subnet, reservation_type, reserved_value):
    pointer = locate_entry(world.subcfg[subnet][5], '}', reservation_number)

    if reservation_type == "address":
        tmp = world.subcfg[subnet][5][:pointer] + ',"ip-addresses":["{reserved_value}"]'.format(**locals())
        tmp += world.subcfg[subnet][5][pointer:]
    elif reservation_type == "prefix":
        tmp = world.subcfg[subnet][5][:pointer] + ',"prefixes":["{reserved_value}"]'.format(**locals())
        tmp += world.subcfg[subnet][5][pointer:]
    elif reservation_type == "hostname":
        tmp = world.subcfg[subnet][5][:pointer] + ',"hostname":"{reserved_value}"'.format(**locals())
        tmp += world.subcfg[subnet][5][pointer:]
    else:
        assert False, "Not supported"
        #TODO implement this if we needs it.
    world.subcfg[subnet][5] = tmp


def check_kea_status():
    v6 = 0
    v4 = 0
    result = fabric_sudo_command(SOFTWARE_INSTALL_DIR + "sbin/keactrl status")
    # not very sophisticated but easiest fastest way ;)
    if "DHCPv4 server: inactive" in result:
        v4 = 0
    elif "DHCPv4 server: active" in result:
        v4 = 1
    if "DHCPv6 server: inactive" in result:
        v6 = 0
    elif "DHCPv6 server: active" in result:
        v6 = 1
    return v6, v4


def set_kea_ctrl_config():
    path = SOFTWARE_INSTALL_DIR[:-1]

    kea6 = 'no'
    kea4 = 'no'
    ddns = 'no'
    if "kea6" in world.cfg["dhcp_under_test"]:
        kea6 = 'yes'
    elif "kea4" in world.cfg["dhcp_under_test"]:
        kea4 = 'yes'
    if world.ddns_enable:
        ddns = 'yes'

    world.cfg["keactrl"] = '''kea_config_file={path}/etc/kea/kea.conf
    dhcp4_srv={path}/sbin/kea-dhcp4
    dhcp6_srv={path}/sbin/kea-dhcp6
    dhcp_ddns_srv={path}/sbin/kea-dhcp-ddns
    dhcp4={kea4}
    dhcp6={kea6}
    dhcp_ddns={ddns}
    kea_verbose=no
    '''.format(**locals())


def add_simple_opt(passed_option):
    if not "simple_options" in world.cfg:
        world.cfg["simple_options"] = ''
    else:
        world.cfg["simple_options"] += ","

    world.cfg["simple_options"] += passed_option


def add_option_to_main(option, value):
    pass
    # if value in ["True", "true", "TRUE", "False", "FALSE", "false"]:
    #     world.cfg["main"] += ',"{option}":{value}'.format(**locals())
    # else:
    #     world.cfg["main"] += ',"{option}":"{value}"'.format(**locals())


def config_db_backend():
    if DB_TYPE == "" or DB_TYPE == "memfile":
        add_simple_opt('"lease-database":{"type": "memfile"}')

    else:
        pointer_start = '{'
        pointer_end = '}'
        db_type = DB_TYPE
        db_name = DB_NAME
        db_user = DB_USER
        db_passwd = DB_PASSWD

        if DB_HOST == "" or DB_HOST == "localhost":
            db_host = ""
        else:
            db_host = DB_HOST

        add_simple_opt('''"lease-database":{pointer_start}"type": "{db_type}",
                       "name":"{db_name}", "host":"{db_host}", "user":"{db_user}",
                       "password":"{db_passwd}"{pointer_end}'''.format(**locals()))
        if world.reservation_backend in {"mysql", "postgresql"}:
            add_simple_opt('''"hosts-database":{pointer_start}"type": "{db_type}",
                           "name":"{db_name}", "host":"{db_host}", "user":"{db_user}",
                           "password":"{db_passwd}"{pointer_end}'''.format(**locals()))


def add_hooks(library_path):
    if not "hooks" in world.cfg:
        world.cfg["hooks"] = ''
    else:
        # if hooks are already created it means we have at least one library there
        # so we need just comma
        world.cfg["hooks"] += ','

    world.cfg["hooks"] += '{"library": "' + library_path + '"}'


def add_logger(log_type, severity, severity_level, logging_file):
    if not "logger" in world.cfg:
        world.cfg["logger"] = ''
    else:
        if len(world.cfg["logger"]) > 20:
            world.cfg["logger"] += ','
    logging_file_path = SOFTWARE_INSTALL_DIR + 'var/kea/' + logging_file
    if severity_level != "None":
        world.cfg["logger"] += '{"name": "' + log_type + '","output_options": [{"output": "' + logging_file_path + '",' \
                               '"destination": "file"}],"debuglevel": ' + severity_level + ',"severity": ' \
                               '"' + severity + '"}'
    else:
        world.cfg["logger"] += '{"name": "' + log_type + '","output_options": [{"output": "' + logging_file_path + '",' \
                               '"destination": "file"}],"severity": ' \
                               '"' + severity + '"}'


def open_control_channel(socket_type, socket_name):
    world.cfg["socket"] = '"control-socket": {"socket-type": "' +\
                          socket_type + '","socket-name": "' + socket_name + '"}'


def cfg_write():
    config_db_backend()
    for number in range(0, len(world.subcfg)):
        if len(world.subcfg[number][2]) > 10:
            world.subcfg[number][2] = '"option-data": [' + world.subcfg[number][2] + "]"
        if len(world.subcfg[number][4]) > 10:
            world.subcfg[number][4] = '"pools": [' + world.subcfg[number][4] + "]"
        if len(world.subcfg[number][5]) > 10:
            world.subcfg[number][5] = '"reservations":[' + world.subcfg[number][5] + "]"
    cfg_file = open(world.cfg["cfg_file"], 'w')
    ## add timers
    cfg_file.write(world.cfg["main"])
    ## add interfaces
    cfg_file.write('"interfaces-config": { "interfaces": [ ' + world.cfg["interfaces"] + ' ] },')
    ## add header for subnets
    if "kea6" in world.cfg["dhcp_under_test"]:
        cfg_file.write('"subnet6":[')
    elif "kea4" in world.cfg["dhcp_under_test"]:
        cfg_file.write('"subnet4":[')

    ## add subnets
    counter = 0
    for each_subnet in world.subcfg:
        tmp = each_subnet[0]
        counter += 1
        for each_subnet_config_part in each_subnet[1:]:
            if len(each_subnet_config_part) > 0:
                tmp += ',' + each_subnet_config_part
            #tmp += str(each_subnet[-1])
        cfg_file.write(tmp + '}')
        if counter != len(world.subcfg) and len(world.subcfg) > 1:
            cfg_file.write(",")
    cfg_file.write(']')

    if "options" in world.cfg:
        cfg_file.write(',' + world.cfg["options"])
        cfg_file.write("]")
        del world.cfg["options"]

    if "option_def" in world.cfg:
        cfg_file.write(',' + world.cfg["option_def"])
        cfg_file.write("]")
        del world.cfg["option_def"]

    if "hooks" in world.cfg:
        cfg_file.write(',"hooks-libraries": [' + world.cfg["hooks"] + ']')
        del world.cfg["hooks"]

    if "simple_options" in world.cfg:
        cfg_file.write(',' + world.cfg["simple_options"])
        del world.cfg["simple_options"]

    if world.ddns_enable:
        cfg_file.write(',' + world.ddns_add + '}')

    if "custom_lines" in world.cfg:
        cfg_file.write(',' + world.cfg["custom_lines"])
        #cfg_file.write("]")
        del world.cfg["custom_lines"]

    if "socket" in world.cfg:
        cfg_file.write(',' + world.cfg["socket"])
        del world.cfg["socket"]

    cfg_file.write('}')

    if world.ddns_enable:
        build_ddns_config()
        cfg_file.write(world.ddns)
        #cfg_file.write("}")

    logging_file = SOFTWARE_INSTALL_DIR + 'var/kea/kea.log'

    log_type = ''
    if "kea6" in world.cfg["dhcp_under_test"]:
        log_type = 'kea-dhcp6'
    elif "kea4" in world.cfg["dhcp_under_test"]:
        log_type = 'kea-dhcp4'

    cfg_file.write(',"Logging": {"loggers": [')
    if not "logger" in world.cfg:
        cfg_file.write('{"name": "' + log_type + '","output_options": [{"output": "' + logging_file + '",'
                       '"destination": "file"}')
        cfg_file.write('],"debuglevel": 99,"severity": "DEBUG"}')
        if world.ddns_enable:
            cfg_file.write(',{"name": "kea-dhcp-ddns","output_options": [{"output": "' + logging_file + '_ddns",'
                           '"destination": "file"}')
            cfg_file.write('],"debuglevel": 99,"severity": "DEBUG"}')
    else:
        cfg_file.write(world.cfg["logger"])

    cfg_file.write(']}')
    cfg_file.write('}')  # end of the config file
    cfg_file.close()
    # kea ctrl script config file
    cfg_file = open(world.cfg["cfg_file_2"], 'w')
    cfg_file.write(world.cfg["keactrl"])
    cfg_file.close()
    json_file_layout()
    world.subcfg = [["", "", "", "", "", ""]]


def check_kea_process_result(succeed, result, process):
    errors = ["Failed to apply configuration", "Failed to initialize server",
              "Service failed", "failed to initialize Kea server", "failed to initialize Kea"]

    if succeed:
        if any(error_message in result for error_message in errors):
            assert False, 'Server operation: ' + process + ' failed! '
    if not succeed:
        if not any(error_message in result for error_message in errors):
            assert False, 'Server operation: ' + process + ' NOT failed!'


## =============================================================
## ================ PREPARE CONFIG BLOCK END  ==================

## =============================================================
## ================ REMOTE SERVER BLOCK START ==================


def build_and_send_config_files():
    world.cfg['leases'] = SOFTWARE_INSTALL_DIR + 'var/kea/kea-leases6.csv'
    add_defaults()
    set_kea_ctrl_config()
    cfg_write()
    fabric_send_file(world.cfg["cfg_file"], SOFTWARE_INSTALL_DIR + "etc/kea/kea.conf")
    fabric_send_file(world.cfg["cfg_file_2"], SOFTWARE_INSTALL_DIR + "etc/kea/keactrl.conf")
    copy_configuration_file(world.cfg["cfg_file"])
    copy_configuration_file(world.cfg["cfg_file_2"], "kea_ctrl_config")
    remove_local_file(world.cfg["cfg_file"])
    remove_local_file(world.cfg["cfg_file_2"])


def start_srv(start, process):
    """
    Start kea with generated config
    """
    build_and_send_config_files()
    v6, v4 = check_kea_status()

    if process is None:
        process = "starting"

    if not v6:
        result = fabric_sudo_command('(' + SOFTWARE_INSTALL_DIR + 'sbin/keactrl start '
                                     + ' & ); sleep ' + str(SLEEP_TIME_1))
        check_kea_process_result(start, result, process)
    else:
        result = fabric_sudo_command('(' + SOFTWARE_INSTALL_DIR + 'sbin/keactrl stop '
                                     + ' & ); sleep ' + str(SLEEP_TIME_1))
        check_kea_process_result(start, result, process)
        result = fabric_sudo_command('(' + SOFTWARE_INSTALL_DIR + 'sbin/keactrl start '
                                     + ' & ); sleep ' + str(SLEEP_TIME_1))
        check_kea_process_result(start, result, process)


def reconfigure_srv():
    build_and_send_config_files()
    result = fabric_sudo_command('(' + SOFTWARE_INSTALL_DIR + 'sbin/keactrl reload '
                                 + ' & ); sleep ' + str(SLEEP_TIME_1))
    check_kea_process_result(True, result, 'reconfigure')


def stop_srv(value = False):
    fabric_sudo_command('(' + SOFTWARE_INSTALL_DIR + 'sbin/keactrl stop ' + ' & ); sleep ' + str(SLEEP_TIME_1), value)


def restart_srv():
    fabric_sudo_command('(' + SOFTWARE_INSTALL_DIR + 'sbin/keactrl stop ' + ' & ); sleep ' + str(SLEEP_TIME_1))
    fabric_sudo_command('(' + SOFTWARE_INSTALL_DIR + 'sbin/keactrl start ' + ' & ); sleep ' + str(SLEEP_TIME_1))

## =============================================================
## ================ REMOTE SERVER BLOCK END ====================


def clear_leases():
    db_name = DB_NAME
    db_user = DB_USER
    db_passwd = DB_PASSWD

    if DB_TYPE == "mysql":
        # that is tmp solution - just clearing not saving.
        #command = '''mysql -u {db_user} -p{db_passwd} -Nse 'show tables' {db_name} | while read table; do mysql -u {db_user} -p{db_passwd} -e "truncate table $table" {db_name}; done'''.format(**locals())
        command = 'for table_name in dhcp4_options dhcp6_options ipv6_reservations hosts lease4 lease6; do mysql -u {db_user} -p{db_passwd} -e "delete from $table_name" {db_name}; done'.format(**locals())
        fabric_run_command(command)
    elif DB_TYPE == "postgresql":
        pointer_start = '{'
        pointer_end = '}'
        #command = """psql -U {db_user} -d {db_name} -c "\\\\dtvs" -t  | awk '{pointer_start}print $3{pointer_end}' | while read table; do if [ ! -z "$table" -a "$table" != " " ]; then psql -U {db_user} -d {db_name} -c "truncate $table"; fi done""".format(**locals())
        command = 'for table_name in dhcp4_options dhcp6_options ipv6_reservations hosts lease4 lease6; do psql -U {db_user} -d {db_name} -c "delete from $table_name" ; done'.format(**locals())
        fabric_run_command(command)
    else:
        fabric_remove_file_command(world.cfg['leases'])


def save_leases():
    db_name = DB_NAME
    db_user = DB_USER
    db_passwd = DB_PASSWD

    if DB_TYPE == "mysql":
        # that is tmp solution - just clearing not saving.
        #command = '''mysql -u {db_user} -p{db_passwd} -Nse 'show tables' {db_name} | while read table; do mysql -u {db_user} -p{db_passwd} -e "truncate table $table" {db_name}; done'''.format(**locals())
        command = 'for table_name in dhcp4_options dhcp6_options ipv6_reservations hosts lease4 lease6; do mysql -u {db_user} -p{db_passwd} -e "delete from $table_name" {db_name}; done'.format(**locals())
        fabric_run_command(command)
    elif DB_TYPE == "postgresql":
        pointer_start = '{'
        pointer_end = '}'
        #command = """psql -U {db_user} -d {db_name} -c "\\\\dtvs" -t  | awk '{pointer_start}print $3{pointer_end}' | while read table; do if [ ! -z "$table" -a "$table" != " " ]; then psql -U {db_user} -d {db_name} -c "truncate $table"; fi done""".format(**locals())
        command = 'for table_name in dhcp4_options dhcp6_options ipv6_reservations hosts lease4 lease6; do psql -U {db_user} -d {db_name} -c "delete from $table_name" ; done'.format(**locals())
        fabric_run_command(command)
    else:
        fabric_download_file(world.cfg['leases'], world.cfg["dir_name"] + '/kea_leases.csv')


def save_logs():
    fabric_download_file(SOFTWARE_INSTALL_DIR + 'var/kea/kea.log*', world.cfg["dir_name"] + '/.')


def clear_all():
    fabric_remove_file_command(SOFTWARE_INSTALL_DIR + 'var/kea/kea.log*')

    db_name = DB_NAME
    db_user = DB_USER
    db_passwd = DB_PASSWD
    if DB_TYPE in ["memfile", ""]:
        fabric_remove_file_command(world.cfg['leases'])
    elif DB_TYPE == "mysql":
        #command = '''mysql -u {db_user} -p{db_passwd} -Nse 'show tables' {db_name} | while read table; do mysql -u {db_user} -p{db_passwd} -e "truncate table $table" {db_name}; done'''.format(**locals())
        command = 'for table_name in dhcp4_options dhcp6_options ipv6_reservations hosts lease4 lease6; do mysql -u {db_user} -p{db_passwd} -e "delete from $table_name" {db_name}; done'.format(**locals())
        fabric_run_command(command)
    elif DB_TYPE == "postgresql":
        pointer_start = '{'
        pointer_end = '}'
        command = 'for table_name in dhcp4_options dhcp6_options ipv6_reservations hosts lease4 lease6; do psql -U {db_user} -d {db_name} -c "delete from $table_name" ; done'.format(**locals())
        fabric_run_command(command)
