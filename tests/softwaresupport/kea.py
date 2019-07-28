# Copyright (C) 2013-2019 Internet Systems Consortium.
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

import os
import sys
import json
import logging

from forge_cfg import world
from protosupport.multi_protocol_functions import add_variable
from softwaresupport.multi_server_functions import fabric_run_command, fabric_send_file, remove_local_file
from softwaresupport.multi_server_functions import copy_configuration_file, fabric_sudo_command, fabric_download_file
from softwaresupport.multi_server_functions import locate_entry, fabric_remove_file_command, json_file_layout
from softwaresupport.multi_server_functions import check_local_path_for_downloaded_files

from kea6_server.functions_ddns import build_ddns_config

log = logging.getLogger('forge')


# kea_otheroptions was originally designed for vendor options
# because codes sometime overlap with basic options
kea_otheroptions = {
    "tftp-servers": 32,
    "config-file": 33,
    "syslog-servers": 34,
    "device-id": 36,
    "time-servers": 37,
    "time-offset": 38
}


def add_defaults4():
    eth = world.f_cfg.server_iface
    t1 = world.cfg["server_times"]["renew-timer"]
    t2 = world.cfg["server_times"]["rebind-timer"]
    t3 = world.cfg["server_times"]["valid-lifetime"]

    pointer_start = "{"
    pointer_end = "}"

    world.cfg["main"] = '{"Dhcp4" :{'
    if t1 != "":
        world.cfg["main"] += '"renew-timer": {t1},'.format(**locals())
    if t2 != "":
        world.cfg["main"] += '"rebind-timer": {t2},'.format(**locals())
    if t3 != "":
        world.cfg["main"] += '"valid-lifetime": {t3},'.format(**locals())

    if "global_parameters" in world.cfg:
        world.cfg["main"] += world.cfg["global_parameters"]

    if eth is not None and eth not in world.cfg["interfaces"]:
        add_interface(eth)

    # world.cfg["conf"] += dedent(subnetcfg)
    # world.dhcp["subnet_cnt"] += 1


def add_defaults6():
    t1 = world.cfg["server_times"]["renew-timer"]
    t2 = world.cfg["server_times"]["rebind-timer"]
    t3 = world.cfg["server_times"]["preferred-lifetime"]
    t4 = world.cfg["server_times"]["valid-lifetime"]
    eth = world.f_cfg.server_iface
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
    if "global_parameters" in world.cfg:
        world.cfg["main"] += world.cfg["global_parameters"]

    if eth is not None and eth not in world.cfg["interfaces"]:
        add_interface(eth)


def _set_kea_ctrl_config():
    if world.f_cfg.software_install_path.endswith('/'):
        path = world.f_cfg.software_install_path[:-1]
    else:
        path = world.f_cfg.software_install_path

    kea6 = 'no'
    kea4 = 'no'
    ddns = 'no'
    ctrl_agent = 'no'
    if "kea6" in world.cfg["dhcp_under_test"]:
        kea6 = 'yes'
    elif "kea4" in world.cfg["dhcp_under_test"]:
        kea4 = 'yes'
    if world.ddns_enable:
        ddns = 'yes'
    if world.ctrl_enable:
        ctrl_agent = 'yes'
    world.cfg["keactrl"] = '''kea_config_file={path}/etc/kea/kea.conf
    dhcp4_srv={path}/sbin/kea-dhcp4
    dhcp6_srv={path}/sbin/kea-dhcp6
    dhcp_ddns_srv={path}/sbin/kea-dhcp-ddns
    ctrl_agent_srv={path}/sbin/kea-ctrl-agent
    netconf_srv={path}/sbin/kea-netconf
    kea_dhcp4_config_file={path}/etc/kea/kea.conf
    kea_dhcp6_config_file={path}/etc/kea/kea.conf
    kea_dhcp_ddns_config_file={path}/etc/kea/kea.conf
    kea_ctrl_agent_config_file={path}/etc/kea/kea.conf
    kea_netconf_config_file={path}/etc/kea/kea.conf
    dhcp4={kea4}
    dhcp6={kea6}
    dhcp_ddns={ddns}
    kea_verbose=no
    netconf=no
    ctrl_agent={ctrl_agent}
    '''.format(**locals())


def _add_simple_opt(passed_option):
    if "simple_options" not in world.cfg:
        world.cfg["simple_options"] = ''
    else:
        world.cfg["simple_options"] += ","
    world.cfg["simple_options"] += passed_option


def _config_add_reservation_database():
    db_type = world.reservation_backend
    db_name = world.f_cfg.db_name
    db_user = world.f_cfg.db_user
    db_passwd = world.f_cfg.db_passwd
    pointer_start = '{'
    pointer_end = '}'
    if world.f_cfg.db_host == "" or world.f_cfg.db_host == "localhost":
        db_host = ""

    if world.reservation_backend in ["mysql", "postgresql"]:
        _add_simple_opt('''"hosts-database":{pointer_start}"type": "{db_type}",
                       "name":"{db_name}", "host":"{db_host}", "user":"{db_user}",
                       "password":"{db_passwd}"{pointer_end}'''.format(**locals()))

    # TODO remove hardcoded values for cassandra
    if world.reservation_backend in ["cql"]:
        _add_simple_opt('''"hosts-database":{pointer_start}"type": "{db_type}",
                       "keyspace":"keatest", "host":"", "user":"keatest",
                       "password":"keatest"{pointer_end}'''.format(**locals()))


def _config_db_backend():
    if world.f_cfg.db_type == "" or world.f_cfg.db_type == "memfile":
        _add_simple_opt('"lease-database":{"type": "memfile"}')
        # _add_simple_opt('"lease-database":{"type": "memfile", "lfc-interval": 10}')
    else:
        pointer_start = '{'
        pointer_end = '}'
        db_type = world.f_cfg.db_type
        db_name = world.f_cfg.db_name
        db_user = world.f_cfg.db_user
        db_passwd = world.f_cfg.db_passwd
        if world.f_cfg.db_host == "" or world.f_cfg.db_host == "localhost":
            db_host = ""
        else:
            db_host = world.f_cfg.db_host
        if db_type in ["mysql", "postgresql"]:
            _add_simple_opt('''"lease-database":{pointer_start}"type": "{db_type}",
                            "name":"{db_name}", "host":"{db_host}", "user":"{db_user}",
                            "password":"{db_passwd}"{pointer_end}'''.format(**locals()))
        # TODO remove hardcoded values for cassandra
        elif db_type in ["cql"]:
            _add_simple_opt('''"lease-database":{pointer_start}"type": "{db_type}",
                            "keyspace":"keatest", "host":"", "user":"keatest",
                            "password":"keatest"{pointer_end}'''.format(**locals()))
    _config_add_reservation_database()


def _cfg_write():
    _config_db_backend()
    checker = 0
    for number in range(len(world.subcfg)):
        if len(world.subcfg[number][2]) > 10:
            world.subcfg[number][2] = '"option-data": [' + world.subcfg[number][2] + "]"
        if len(world.subcfg[number][4]) > 10:
            world.subcfg[number][4] = '"pools": [' + world.subcfg[number][4] + "]"
        if len(world.subcfg[number][5]) > 10:
            world.subcfg[number][5] = '"reservations":[' + world.subcfg[number][5] + "]"
    cfg_file = open(world.cfg["cfg_file"], 'w')
    # add timers
    cfg_file.write(world.cfg["main"])
    if len(world.cfg["server-id"]) > 5:
        cfg_file.write(world.cfg["server-id"])
    # add class definitions
    if len(world.classification) > 0:
        if len(world.classification[0][0]) > 0:
            cfg_file.write('"client-classes": [')
            counter = 0
            for each_class in world.classification:
                if counter > 0:
                    cfg_file.write(',')
                cfg_file.write('{')  # open class
                cfg_file.write('"name":"' + each_class[0] + '"')
                if len(each_class[1]) > 0:
                    cfg_file.write("," + each_class[1])
                if len(each_class[2]) > 0:
                    cfg_file.write(',"option-data": [' + each_class[2] + "]")
                cfg_file.write('}')  # close each class
                counter += 1
            cfg_file.write("],")  # close classes
    # add interfaces
    cfg_file.write('"interfaces-config": { "interfaces": [ ' + world.cfg["interfaces"] + ' ] },')
    # add header for subnets
    if world.subnet_add:
        if "kea6" in world.cfg["dhcp_under_test"]:
            cfg_file.write('"subnet6":[')
        elif "kea4" in world.cfg["dhcp_under_test"]:
            cfg_file.write('"subnet4":[')
        # add subnets
        counter = 0
        comma = 0
        for each_subnet in world.subcfg:
            if counter in world.shared_subnets_tmp:
                # subnets that suppose to go to shared-networks should be omitted here
                checker = 1
                counter += 1
                continue
            if counter > 0 and comma == 1:
                cfg_file.write(",")
            tmp = each_subnet[0]
            # we need to be able to add interface-id to config but we want to keep backward compatibility.
            if "interface" not in tmp or "interface-id" not in tmp:
                eth = world.f_cfg.server_iface
                tmp += ', "interface": "{eth}" '.format(**locals())
            counter += 1
            comma = 1
            for each_subnet_config_part in each_subnet[1:]:
                checker = 1
                if len(each_subnet_config_part) > 0:
                    tmp += ',' + each_subnet_config_part
            cfg_file.write(tmp + '}')
        cfg_file.write(']')
        # that is ugly hack but kea confing generation is awaiting rebuild anyway
        if "options" in world.cfg:
            cfg_file.write(',' + world.cfg["options"])
            cfg_file.write("]")
            del world.cfg["options"]

    if "options" in world.cfg:
        cfg_file.write(world.cfg["options"])
        checker = 1
        cfg_file.write("]")
        del world.cfg["options"]

    if "option_def" in world.cfg:
        cfg_file.write(',' + world.cfg["option_def"])
        cfg_file.write("]")
        del world.cfg["option_def"]

    if len(world.hooks) > 0 or len(world.kea_ha[0]) > 0:
        if checker == 1:
            cfg_file.write(',')
        cfg_file.write('"hooks-libraries": [')
        test_length_1 = len(world.hooks)
        counter_1 = 1
        for each_hook in world.hooks:
            cfg_file.write('{"library": "' + each_hook[0] + '"')
            if len(each_hook[1]) > 0:
                cfg_file.write(',"parameters": {')
                test_length_2 = len(each_hook[1])
                counter_2 = 1
                for every_parameter in each_hook[1]:
                    cfg_file.write('"' + every_parameter[0] + '":')
                    if every_parameter[1] in ["true", "false"]:  # TODO add if value is numeric
                        cfg_file.write(every_parameter[1])
                    else:
                        cfg_file.write('"' + every_parameter[1] + '"')
                    if counter_2 < test_length_2:
                        cfg_file.write(',')
                    counter_2 += 1
                cfg_file.write('}')  # closing parameters
            if counter_1 < test_length_1:
                cfg_file.write('},')
            counter_1 += 1
        cfg_file.write('}')  # closing libs
        if len(world.kea_ha[0]) > 0:
            if len(world.hooks) > 0:
                cfg_file.write(',')
            cfg_file.write('{"library": "' + world.kea_ha[0][0] + '","parameters":{"high-availability":[{')
            # add single parameters to main map
            for each_param in world.kea_ha[1]:
                cfg_file.write('"'+each_param[0]+'":'+each_param[1]+",")
            # add peers
            cfg_file.write('"peers": [')
            for each_ha_peer in world.kea_ha[2]:
                cfg_file.write(each_ha_peer)
                if world.kea_ha[2].index(each_ha_peer) != len(world.kea_ha[2]) - 1:
                    cfg_file.write(",")
            cfg_file.write(']')
            if len(world.kea_ha[3]) > 0:
                cfg_file.write(',"state-machine":{"states":[')
                for each_state in world.kea_ha[3]:
                    cfg_file.write(each_state)
                    if world.kea_ha[3].index(each_state) != len(world.kea_ha[3]) - 1:
                        cfg_file.write(",")
                cfg_file.write(']}')
            cfg_file.write('}]}}')

        cfg_file.write(']')  # closing hooks

    if "simple_options" in world.cfg:
        cfg_file.write(',' + world.cfg["simple_options"])
        del world.cfg["simple_options"]

    if world.ddns_enable:
        cfg_file.write(',"dhcp-ddns":' + json.dumps(world.ddns_add))

    if "custom_lines" in world.cfg:
        cfg_file.write(',' + world.cfg["custom_lines"])
        # cfg_file.write("]")
        del world.cfg["custom_lines"]

    if "socket" in world.cfg:
        cfg_file.write(',' + world.cfg["socket"])
        del world.cfg["socket"]

    if len(world.shared_subnets) > 0:
        shared_counter = 0
        last_option = ""
        cfg_file.write(' ,"shared-networks":[')
        for each_shared_subnet in world.shared_subnets:
            counter = 0
            comma = 0
            if shared_counter > 0:
                cfg_file.write(',')
            cfg_file.write('{')

            for each_option in world.shared_subcfg[shared_counter]:
                cfg_file.write(each_option)
                last_option = each_option

            if last_option[:-1] != ",":
                cfg_file.write(",")

            if "kea6" in world.cfg["dhcp_under_test"]:
                cfg_file.write('"subnet6":[')

            elif "kea4" in world.cfg["dhcp_under_test"]:
                cfg_file.write('"subnet4":[')

            for each_subnet in world.subcfg:
                if counter in each_shared_subnet:
                    if counter > 0 and comma == 1:
                        cfg_file.write(",")
                    tmp = each_subnet[0]
                    # we need to be able to add interface-id to config but we want to keep backward compatibility.
                    # if "interface" not in tmp or "interface-id" not in tmp:
                    #     eth = world.f_cfg.server_iface
                    #     tmp += ', "interface": "{eth}" '.format(**locals())
                    counter += 1
                    comma = 1

                    for each_subnet_config_part in each_subnet[1:]:
                        if len(each_subnet_config_part) > 0:
                            tmp += ',' + each_subnet_config_part
                        # tmp += str(each_subnet[-1])
                    cfg_file.write(tmp + '}')
                else:
                    counter += 1
            # shared_counter += 1
            cfg_file.write(']')
            shared_counter += 1
            cfg_file.write('}')  # end of map of each shared network
        cfg_file.write(']')  # end of shared networks list

    cfg_file.write('}')  # end of DHCP part (should be moved if something else will be added after shared-networks

    if world.ddns_enable:
        build_ddns_config()
        cfg_file.write(world.ddns)

    if "agent" in world.cfg:
        cfg_file.write(',' + world.cfg["agent"])
        del world.cfg["agent"]

    if world.f_cfg.install_method == 'make':
        logging_file = world.f_cfg.log_join('kea.log')
    else:
        logging_file = 'stdout'

    log_type = ''
    if "kea6" in world.cfg["dhcp_under_test"]:
        log_type = 'kea-dhcp6'
    elif "kea4" in world.cfg["dhcp_under_test"]:
        log_type = 'kea-dhcp4'

    cfg_file.write(',"Logging": {"loggers": [')
    if "logger" not in world.cfg:
        cfg_file.write('{"name": "' + log_type + '","output_options": [{"output": "' + logging_file + '"}')
        cfg_file.write('],"debuglevel": 99,"severity": "DEBUG"}')
        if world.ddns_enable:
            cfg_file.write(',{"name": "kea-dhcp-ddns","output_options": [{"output": "' + logging_file + '_ddns"}')
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
    world.subcfg = [["", "", "", "", "", "", ""]]
    config = open(world.cfg["cfg_file"], 'r')
    world.configString = config.read().replace('\n', '').replace(' ', '')
    config.close()
    add_variable("SERVER_CONFIG", world.configString, False)  # TODO: is it needed?
    json_file_layout()


def _write_cfg2(cfg):
    # log.info('provisioned cfg:\n%s', cfg)
    with open(world.cfg["cfg_file"], 'w') as cfg_file:
        json.dump(cfg, cfg_file, sort_keys=True, indent=4, separators=(',', ': '))

    cfg_file = open(world.cfg["cfg_file_2"], 'w')
    cfg_file.write(world.cfg["keactrl"])
    cfg_file.close()


def build_and_send_config_files(connection_type, configuration_type="config-file",
                                destination_address=world.f_cfg.mgmt_address, cfg=None):
    """
    Generate final config file, save it to test result directory
    and send it to remote system unless testing step will define differently.
    :param connection_type: for now two values expected: SSH and None for stating if files should be send
    :param configuration_type: for now supported just config-file, generate file and save to results dir
    :param destination_address: address of remote system to which conf file will be send,
    default it's world.f_cfg.mgmt_address
    """

    #import pudb; pudb.set_trace()

    if world.proto == 'v4':
        add_defaults4()
    else:
        add_defaults6()

    _set_kea_ctrl_config()

    if cfg is None:
        _cfg_write()
    else:
        _write_cfg2(cfg)

    if connection_type == "SSH":
        if world.f_cfg.install_method == 'make':
            fabric_send_file(world.cfg["cfg_file_2"],
                             world.f_cfg.etc_join("keactrl.conf"),
                             destination_host=destination_address)
            kea_conf_file = "kea.conf"
        else:
            fabric_send_file(world.cfg["cfg_file"],
                             world.f_cfg.etc_join('kea-ctrl-agent.conf'),
                             destination_host=destination_address)
            kea_conf_file = "kea-dhcp%s.conf" % world.proto[1]
        fabric_send_file(world.cfg["cfg_file"],
                         world.f_cfg.etc_join(kea_conf_file),
                         destination_host=destination_address)

    copy_configuration_file(world.cfg["cfg_file"], destination_host=destination_address)
    copy_configuration_file(world.cfg["cfg_file_2"], "kea_ctrl_config", destination_host=destination_address)
    remove_local_file(world.cfg["cfg_file"])
    remove_local_file(world.cfg["cfg_file_2"])


def clear_logs(destination_address=world.f_cfg.mgmt_address):
    fabric_remove_file_command(world.f_cfg.log_join('kea.log*'),
                               destination_host=destination_address)


def _clear_db_config(db_name=world.f_cfg.db_name, db_user=world.f_cfg.db_user, db_passwd=world.f_cfg.db_passwd,
                    destination_address=world.f_cfg.mgmt_address):

    tables = ['dhcp4_audit_revision',
              'dhcp4_audit',
              'dhcp4_global_parameter',
              'dhcp4_global_parameter_server',
              'dhcp4_option_def',
              'dhcp4_option_def_server',
              'dhcp4_options',
              'dhcp4_options_server',
              'dhcp4_pool',
              'dhcp4_shared_network',
              'dhcp4_shared_network_server',
              'dhcp4_subnet',
              'dhcp4_subnet_server',
              'dhcp6_audit_revision',
              'dhcp6_audit',
              'dhcp6_global_parameter',
              'dhcp6_global_parameter_server',
              'dhcp6_option_def',
              'dhcp6_option_def_server',
              'dhcp6_options',
              'dhcp6_options_server',
              'dhcp6_pd_pool',
              'dhcp6_pool',
              'dhcp6_shared_network',
              'dhcp6_shared_network_server',
              'dhcp6_subnet',
              'dhcp6_subnet_server']
    tables = ' '.join(tables)

    command = 'for table_name in {tables}; do mysql -u {db_user} -p{db_passwd} -e '
    command += '"SET foreign_key_checks = 0; truncate $table_name" {db_name}; done'
    command = command.format(**locals())
    fabric_run_command(command, destination_host=destination_address, hide_all=True)

    tables = ['dhcp6_server', 'dhcp4_server']
    tables = ' '.join(tables)
    command = 'for table_name in {tables}; do mysql -u {db_user} -p{db_passwd} -e '
    command += '"SET foreign_key_checks = 0; DELETE FROM $table_name WHERE tag != \'all\'" {db_name}; done'
    command = command.format(**locals())
    fabric_run_command(command, destination_host=destination_address, hide_all=True)


def clear_leases(db_name=world.f_cfg.db_name, db_user=world.f_cfg.db_user, db_passwd=world.f_cfg.db_passwd,
                 destination_address=world.f_cfg.mgmt_address):

    if world.f_cfg.db_type == "mysql":
        # that is tmp solution - just clearing not saving.
        command = 'for table_name in dhcp4_options dhcp6_options ipv6_reservations hosts lease4 lease6 logs; ' \
                  'do mysql -u {db_user} -p{db_passwd} -e' \
                  ' "SET foreign_key_checks = 0; delete from $table_name" {db_name}; done'.format(**locals())
        fabric_run_command(command, destination_host=destination_address)
    elif world.f_cfg.db_type == "postgresql":
        command = 'for table_name in dhcp4_options dhcp6_options ipv6_reservations hosts lease4 lease6 logs;' \
                  ' do psql -U {db_user} -d {db_name} -c "delete from $table_name" ; done'.format(**locals())
        fabric_run_command(command, destination_host=destination_address)
    elif world.f_cfg.db_type == "cql":
        # TODO: hardcoded passwords for now in cassandra, extend it in some time :)
        command = 'for table_name in dhcp_option_scope host_reservations lease4 lease6 logs;' \
                  ' do cqlsh --keyspace=keatest --user=keatest --password=keatest -e "TRUNCATE $table_name;"' \
                  ' ; done'.format(**locals())
        fabric_run_command(command, destination_host=destination_address)
    elif world.f_cfg.db_type in ["memfile", ""]:
        fabric_remove_file_command(world.f_cfg.get_leases_path(), destination_host=destination_address)
    else:
        raise Exception('Unsupported db type %s' % world.f_cfg.db_type)


def clear_all(tmp_db_type=None, destination_address=world.f_cfg.mgmt_address):
    clear_logs(destination_address)
    clear_leases(destination_address=world.f_cfg.mgmt_address)
    _clear_db_config(destination_address=world.f_cfg.mgmt_address)


def _check_kea_status(destination_address=world.f_cfg.mgmt_address):
    v4 = False
    v6 = False
    result = fabric_sudo_command(os.path.join(world.f_cfg.software_install_path, "sbin/keactrl") + " status",
                                 destination_host=destination_address)
    # not very sophisticated but easiest fastest way ;)
    if "DHCPv4 server: inactive" in result:
        v4 = False
    elif "DHCPv4 server: active" in result:
        v4 = True
    if "DHCPv6 server: inactive" in result:
        v6 = False
    elif "DHCPv6 server: active" in result:
        v6 = True
    return v4, v6


def _restart_kea_with_systemctl(destination_address):
    cmd_tpl = 'systemctl restart {service} &&'
    cmd_tpl += ' ts=`systemctl show -p ActiveEnterTimestamp {service}.service | awk \'{{print $2 $3}}\'`;'
    cmd_tpl += ' SECONDS=0; while (( SECONDS < 4 )); do'
    cmd_tpl += ' journalctl -u {service}.service --since $ts |'
    cmd_tpl += ' grep "server version .* started" 2>/dev/null;'
    cmd_tpl += ' if [ $? -eq 0 ]; then break; fi done'

    cmd = cmd_tpl.format(service='isc-kea-dhcp%s-server' % world.proto[1])
    fabric_sudo_command(cmd, destination_host=destination_address)

    if world.ctrl_enable:
        cmd = cmd_tpl.format(service='isc-kea-ctrl-agent')
        fabric_sudo_command(cmd, destination_host=destination_address)


def start_srv(start, process, destination_address=world.f_cfg.mgmt_address):
    """
    Start kea with generated config
    """
    if world.f_cfg.install_method == 'make':
        v4_running, v6_running = _check_kea_status(destination_address)

        if process is None:
            process = "starting"
        # check process - if None add some.

        if v4_running and world.proto == 'v4' or v6_running and world.proto == 'v6':
            result = _stop_kea_with_keactrl(destination_address)  # TODO: check result

        result = _start_kea_with_keactrl(destination_address)
        _check_kea_process_result(start, result, process)
    else:
        _restart_kea_with_systemctl(destination_address)


def stop_srv(value=False, destination_address=world.f_cfg.mgmt_address):
    if world.f_cfg.install_method == 'make':
        result = _stop_kea_with_keactrl(destination_address)  # TODO: check result
    else:
        if hasattr(world, 'proto'):
            cmd = 'systemctl stop isc-kea-dhcp%s-server' % world.proto[1]
            fabric_sudo_command(cmd, destination_host=destination_address)
        else:
            for v in [4, 6]:
                cmd = 'systemctl stop isc-kea-dhcp%s-server' % v
                fabric_sudo_command(cmd, destination_host=destination_address)
        cmd = 'systemctl stop isc-kea-ctrl-agent'
        fabric_sudo_command(cmd, destination_host=destination_address)


def _check_kea_process_result(succeed, result, process):
    errors = ["Failed to apply configuration", "Failed to initialize server",
              "Service failed", "failed to initialize Kea"]

    if succeed:
        if any(error_message in result for error_message in errors):
            assert False, 'Server operation: ' + process + ' failed! '
    if not succeed:
        if not any(error_message in result for error_message in errors):
            assert False, 'Server operation: ' + process + ' NOT failed!'


def _start_kea_with_keactrl(destination_host):
    # Start kea services and check if they started ok.
    # - nohup to shield kea services from getting SIGHUP from SSH
    # - in a loop check if there is 'server version .* started' expression in the logs;
    #   repeat the loop only for 4 seconds
    # - sync to disk any logs traced by keactrl or kea services
    # - display these logs to screen using cat so forge can catch errors in the logs
    start_cmd = 'nohup ' + os.path.join(world.f_cfg.software_install_path, 'sbin/keactrl')
    start_cmd += " start  < /dev/null > /tmp/keactrl.log 2>&1; SECONDS=0; while (( SECONDS < 4 ));"
    start_cmd += " do tail /usr/local/var/kea/kea.log 2>/dev/null | grep 'server version .* started' 2>/dev/null;"
    start_cmd += " if [ $? -eq 0 ]; then break; fi done;"
    start_cmd += " sync; cat /tmp/keactrl.log"
    return fabric_sudo_command(start_cmd, destination_host=destination_host)


def _stop_kea_with_keactrl(destination_host):
    stop_cmd = os.path.join(world.f_cfg.software_install_path, 'sbin/keactrl') + ' stop'
    return fabric_sudo_command(stop_cmd, destination_host=destination_host)


def _reload_kea_with_keactrl(destination_host):
    stop_cmd = os.path.join(world.f_cfg.software_install_path, 'sbin/keactrl') + ' reload'
    return fabric_sudo_command(stop_cmd, destination_host=destination_host)


def reconfigure_srv(destination_address=world.f_cfg.mgmt_address):
    result = _reload_kea_with_keactrl(destination_address)
    _check_kea_process_result(True, result, 'reconfigure')


def restart_srv(destination_address=world.f_cfg.mgmt_address):
    if world.f_cfg.install_method == 'make':
        result = _stop_kea_with_keactrl(destination_address)  # TODO: check result
        result = _start_kea_with_keactrl(destination_address)
    else:
        _restart_kea_with_systemctl(destination_address)


def agent_control_channel(host_address, host_port, socket_name='control_socket'):
    world.ctrl_enable = True
    world.cfg["agent"] = '"Control-agent":{"http-host": "' + host_address
    world.cfg["agent"] += '","http-port":' + host_port
    world.cfg["agent"] += ',"control-sockets":{"dhcp%s":{' % world.proto[1]
    world.cfg["agent"] += '"socket-type": "unix","socket-name": "' + world.f_cfg.run_join(socket_name)
    world.cfg["agent"] += '"}}}'


def save_leases(tmp_db_type=None, destination_address=world.f_cfg.mgmt_address):
    if world.f_cfg.db_type in ["mysql", "postgresql", "cql"]:
        # TODO
        pass
    else:
        fabric_download_file(world.f_cfg.get_leases_path(),
                             check_local_path_for_downloaded_files(world.cfg["test_result_dir"],
                                                                   'leases.csv',
                                                                   destination_address),
                             destination_host=destination_address, warn_only=True)


def save_logs(destination_address=world.f_cfg.mgmt_address):
    fabric_download_file(world.f_cfg.log_join('kea.log*'),
                         check_local_path_for_downloaded_files(world.cfg["test_result_dir"],
                                                               '.',
                                                               destination_address),
                         destination_host=destination_address, warn_only=True)


def ha_add_parameter_to_hook(parameter_name, parameter_value):
    if parameter_name == "lib":
        world.kea_ha[0].append(parameter_value)
    elif parameter_name == "machine-state":
        world.kea_ha[3] += ([parameter_value])
    elif parameter_name == "peers":
        world.kea_ha[2] += ([parameter_value])
    else:
        world.kea_ha[1] += ([[parameter_name, parameter_value]])


def add_hooks(library_path):
    world.hooks.append([library_path, []])


def add_parameter_to_hook(hook_no, parameter_name, parameter_value):
    try:
        world.hooks[hook_no-1][1].append([parameter_name, parameter_value])
    except():
        assert False, "There is no hook with such number, add hook first."


def add_logger(log_type, severity, severity_level, logging_file=None):
    if "logger" not in world.cfg:
        world.cfg["logger"] = ''
    else:
        if len(world.cfg["logger"]) > 20:
            world.cfg["logger"] += ','

    if world.f_cfg.install_method == 'make':
        if logging_file is None:
            logging_file = 'kea.log'
        logging_file_path = world.f_cfg.log_join(logging_file)
    else:
        if logging_file is None:
            logging_file_path = 'stdout'
        else:
            logging_file_path = world.f_cfg.log_join(logging_file)

    if severity_level != "None":
        world.cfg["logger"] += '{"name": "' + log_type + '","output_options": [{"output": "' + logging_file_path + '"' \
                               '}],"debuglevel": ' + severity_level + ',"severity": ' \
                               '"' + severity + '"}'
    else:
        world.cfg["logger"] += '{"name": "' + log_type + '","output_options": [{"output": "' + logging_file_path + '"' \
                               '}],"severity": ' \
                               '"' + severity + '"}'


def open_control_channel_socket(socket_name=None):
    if socket_name is not None:
        socket_path = world.f_cfg.run_join(socket_name)
    else:
        socket_path = world.f_cfg.run_join('control_socket')
    world.cfg["socket"] = '"control-socket": {"socket-type": "unix","socket-name": "' + socket_path + '"}'


def add_test_to_class(class_number, parameter_name, parameter_value):
    if len(world.classification[class_number-1][1]) > 5:
        world.classification[class_number-1][1] += ','
    if parameter_value[0] in ["[", "{"] or parameter_value in ["true", "false"]:
        world.classification[class_number-1][1] += '"{parameter_name}" : {parameter_value}'.format(**locals())
    else:
        world.classification[class_number-1][1] += '"{parameter_name}" : "{parameter_value}"'.format(**locals())


def create_new_class(class_name):
    world.classification.append([class_name, "", ""])  # class name, class test (now empty), list of class options


def set_logger():
    pass
    assert False, "For now option unavailable!"


def set_time(which_time, value, subnet=None):
    assert which_time in world.cfg["server_times"], "Unknown time name: %s" % which_time

    if subnet is None:
            world.cfg["server_times"][which_time] = value
    else:
        subnet = int(subnet)
        if len(world.subcfg[subnet][3]) > 2:
            world.subcfg[subnet][3] += ', '
        world.subcfg[subnet][3] += '"{which_time}": {value}'.format(**locals())


def add_line_in_global(command):
    if "custom_lines" not in world.cfg:
        world.cfg["custom_lines"] = ''

    world.cfg["custom_lines"] += ('\n'+command+'\n')


def prepare_cfg_subnet(subnet, pool, eth=None):
    # world.subcfg[0] = [subnet, client class/simple options, options, pools, host reservation]
    if world.proto == 'v4':
        if subnet == "default":
            subnet = "192.168.0.0/24"
        if pool == "default":
            pool = "192.168.0.1 - 192.168.0.254"
    else:
        if subnet == "default":
            subnet = "2001:db8:1::/64"
        if pool == "default":
            pool = "2001:db8:1::1 - 2001:db8:1::ffff"
    if eth is None:
        eth = world.f_cfg.server_iface

    if "interfaces" not in world.cfg:
        world.cfg["interfaces"] = ''

    pointer_start = "{"
    pointer_end = "}"

    if subnet is not "":
        world.subcfg[world.dhcp["subnet_cnt"]][0] += '''{pointer_start} "subnet": "{subnet}"'''.format(**locals())
    else:
        world.subnet_add = False
    if pool is not "":
        world.subcfg[world.dhcp["subnet_cnt"]][4] += '{pointer_start}"pool": "{pool}" {pointer_end}'.format(**locals())

    if eth not in world.cfg["interfaces"]:
        add_interface(eth)


def config_srv_another_subnet(subnet, pool, eth):
    world.subcfg.append(["", "", "", "", "", "", ""])
    world.dhcp["subnet_cnt"] += 1

    prepare_cfg_subnet(subnet, pool, eth)


def prepare_cfg_add_custom_option(opt_name, opt_code, opt_type, opt_value, space):
    pointer_start = "{"
    pointer_end = "}"

    if "option_def" not in world.cfg:
        world.cfg["option_def"] = '"option-def": ['
    else:
        world.cfg["option_def"] += ","

    # make definition of the new option
    world.cfg["option_def"] += '''
            {pointer_start}"code": {opt_code}, "name": "{opt_name}", "space": "{space}",
            "encapsulate": "", "record-types": "", "array": false, "type": "{opt_type}"{pointer_end}'''\
        .format(**locals())

    # add defined option
    prepare_cfg_add_option(opt_name, opt_value, space, opt_code, 'user')


def add_interface(eth):
    if len(world.cfg["interfaces"]) > 3:
        world.cfg["interfaces"] += ','
    world.cfg["interfaces"] += '"{eth}"'.format(**locals())


def add_pool_to_subnet(pool, subnet):
    pointer_start = "{"
    pointer_end = "}"

    world.subcfg[subnet][4] += ',{pointer_start}"pool": "{pool}"{pointer_end}'.format(**locals())
    pass


def set_conf_parameter_global(parameter_name, value):
    if "global_parameters" not in world.cfg:
        world.cfg["global_parameters"] = ''

    world.cfg["global_parameters"] += '"{parameter_name}": {value},'.format(**locals())


def set_conf_parameter_subnet(parameter_name, value, subnet_id):
    world.subcfg[subnet_id][0] += ',"{parameter_name}": {value}'.format(**locals())


def add_line_in_subnet(subnetid, command):
    if len(world.subcfg[subnetid][0][-1:]) == ",":
        world.subcfg[subnetid][0] += ","
        world.subcfg[subnetid][0] += command
    else:
        world.subcfg[subnetid][0] += command


def add_line_to_shared_subnet(subnet_id, cfg_line):
    if len(world.shared_subcfg[subnet_id][0]) > 1:
        world.shared_subcfg[subnet_id][0] += ","
    world.shared_subcfg[subnet_id][0] += cfg_line


def add_to_shared_subnet(subnet_id, shared_subnet_id):
    if len(world.shared_subnets) <= shared_subnet_id:
        world.shared_subnets.append([])
        world.shared_subcfg.append([""])
    world.shared_subnets[shared_subnet_id].append(subnet_id)
    world.shared_subnets_tmp.append(subnet_id)


def set_conf_parameter_shared_subnet(parameter_name, value, subnet_id):
    if len(world.shared_subcfg[subnet_id][0]) > 1:
        world.shared_subcfg[subnet_id][0] += ','
    world.shared_subcfg[subnet_id][0] += '"{parameter_name}": {value}'.format(**locals())


def prepare_cfg_subnet_specific_interface(interface, address, subnet, pool):
    if subnet == "default":
        subnet = "2001:db8:1::/64"
    if pool == "default":
        pool = "2001:db8:1::1 - 2001:db8:1::ffff"

    eth = world.f_cfg.server_iface

    if "interfaces" not in world.cfg:
        world.cfg["interfaces"] = ''

    pointer_start = "{"
    pointer_end = "}"

    if subnet is not "":
        world.subcfg[world.dhcp["subnet_cnt"]][0] += '''{pointer_start} "subnet": "{subnet}"'''.format(**locals())
    else:
        world.subnet_add = False
    if pool is not "":
        world.subcfg[world.dhcp["subnet_cnt"]][4] += '{pointer_start}"pool": "{pool}" {pointer_end}'.format(**locals())

    if len(world.cfg["interfaces"]) > 3:
        world.cfg["interfaces"] += ','
    world.cfg["interfaces"] += '"{interface}/{address}"'.format(**locals())


def _check_empty_value(val):
    return ("false", "") if val == "<empty>" else ("true", val)


def prepare_cfg_add_option(option_name, option_value, space,
                           option_code=None, opt_type='default', where='options'):
    if where not in world.cfg:
        world.cfg[where] = '"option-data": ['
    else:
        world.cfg[where] += ","

    # check if we are configuring default option or user option via function "prepare_cfg_add_custom_option"
    if opt_type == 'default':
        if world.proto == 'v4':
            option_code = world.kea_options4.get(option_name)
        else:
            option_code = world.kea_options6.get(option_name)
            if option_code is None:
                option_code = kea_otheroptions.get(option_name)

    pointer_start = "{"
    pointer_end = "}"

    if world.proto == 'v4':
        csv_format, option_value = _check_empty_value(option_value)
    else:
        csv_format = 'true'

    assert option_code is not None, "Unsupported option name for other options: " + option_name

    world.cfg[where] += '''
            \t{pointer_start}"csv-format": {csv_format}, "code": {option_code}, "data": "{option_value}",
            \t"name": "{option_name}", "space": "{space}"{pointer_end}'''.format(**locals())


def prepare_cfg_add_option_subnet(option_name, subnet, option_value):
    # check if we are configuring default option or user option via function "prepare_cfg_add_custom_option"
    space = world.cfg["space"]
    subnet = int(subnet)
    if world.proto == 'v4':
        option_code = world.kea_options4.get(option_name)
    else:
        option_code = world.kea_options6.get(option_name)
        if option_code is None:
            option_code = kea_otheroptions.get(option_name)

    pointer_start = "{"
    pointer_end = "}"

    assert option_code is not None, "Unsupported option name for other options: " + option_name
    if len(world.subcfg[subnet][2]) > 10:
        world.subcfg[subnet][2] += ','

    world.subcfg[subnet][2] += '''
            \t{pointer_start}"csv-format": true, "code": {option_code}, "data": "{option_value}",
            \t"name": "{option_name}", "space": "{space}"{pointer_end}'''.format(**locals())


def prepare_cfg_add_option_shared_subnet(option_name, shared_subnet, option_value):
    # check if we are configuring default option or user option via function "prepare_cfg_add_custom_option"
    space = world.cfg["space"]
    shared_subnet = int(shared_subnet)
    if world.proto == 'v4':
        option_code = world.kea_options4.get(option_name)
    else:
        option_code = world.kea_options6.get(option_name)
        if option_code is None:
            option_code = kea_otheroptions.get(option_name)

    pointer_start = "{"
    pointer_end = "}"

    assert option_code is not None, "Unsupported option name for other Kea4 options: " + option_name
    if len(world.shared_subcfg[shared_subnet][0]) > 10:
        world.shared_subcfg[shared_subnet][0] += ','

    world.shared_subcfg[shared_subnet][0] += '''
            {pointer_start}"csv-format": true, "code": {option_code}, "data": "{option_value}",
            "name": "{option_name}", "space": "{space}"{pointer_end}'''.format(**locals())
