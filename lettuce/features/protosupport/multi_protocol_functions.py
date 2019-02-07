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
import sys
import os
from time import sleep
import json
import locale
import re
import tty
import termios
from shutil import copy
import logging

from _pyio import open
import requests

from forge import world
from features.softwaresupport.multi_server_functions import fabric_send_file, fabric_download_file,\
        fabric_remove_file_command, remove_local_file, fabric_sudo_command, generate_file_name,\
        save_local_file, fabric_run_command


log = logging.getLogger('forge')


def forge_sleep(time, time_units):
    divide = 1.0
    if time_units == 'milliseconds' or time_units == 'millisecond':
        divide = 1000.0
    sleep(time * 1.0 / divide)


def test_pause():
    """
    Pause the test for any reason. Press any key to continue.
    """
    def getch():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
    getch()


def copy_file_from_server(remote_path):
    """
    Copy file from remote server via ssh. Address/login/password from init_all.py
    Path required.
    """
    fabric_download_file(remote_path, world.cfg["dir_name"] + '/downloaded_file')


def send_file_to_server(local_path, remote_path):
    """
    Send file to remote server via ssh. Address/login/password from init_all
    Two paths required.
    Local - relative to lettuce directory
    Remote - absolute
    """
    fabric_send_file(local_path, remote_path)


def remove_file_from_server(remote_path):
    """
    Remove file from remote server.
    """
    fabric_remove_file_command(remote_path)


def strip_file(file_path):
    tmp_list = []
    tmp = open(file_path, 'r')
    for line in tmp:
        line = line.strip()
        if len(line) < 1:
            continue
        elif line[0] == '#':
            continue
        else:
            tmp_list.append(line.strip())
    tmp.close()
    return tmp_list


def compare_file(local_path):
    """
    Compare two files, downloaded and local
    """
    if not os.path.exists(local_path):
        assert False, 'No local file %s' % local_path

    outcome = open(world.cfg["dir_name"] + '/file_compare', 'w')

    # first remove all commented and blank lines of both files
    downloaded_stripped = strip_file(world.cfg["dir_name"] + '/downloaded_file')
    local_stripped = strip_file(local_path)

    line_number = 1
    error_flag = True
    for i, j in zip(downloaded_stripped, local_stripped):
        if i != j:
            outcome.write('Line number: ' + locale.str(line_number) + ' \n\tDownloaded file line: "' +
                          i.rstrip('\n') + '" and local file line: "' + j.rstrip('\n') + '"\n')
            error_flag = False
        line_number += 1
    if error_flag:
        remove_local_file(world.cfg["dir_name"] + '/file_compare')

    assert error_flag, 'Downloaded file is NOT the same as local. Check %s/file_compare for details'\
                       % world.cfg["dir_name"]

    if len(downloaded_stripped) != len(local_stripped):
        assert len(downloaded_stripped) > len(local_stripped), 'Downloaded file is part of a local file.'
        assert len(downloaded_stripped) < len(local_stripped), 'Local file is a part of a downlaoded life.'


def file_includes_line(condition, line):
    """
    Check if downloaded file contain line.
    """
    downloaded_stripped = strip_file(world.cfg["dir_name"] + '/downloaded_file')
    if condition is not None:
        if line in downloaded_stripped:
            assert False, 'Downloaded file does contain line: "%s" But it should NOT.' % line
    else:
        if line not in downloaded_stripped:
            assert False, 'Downloaded file does NOT contain line: "%s"' % line


def add_variable(variable_name, variable_val, val_type):
    """
    Define variable and add it to temporary list or to init_all.py file.
    """
    assert not bool(re.compile('[^A-Z^0-9^_] + ').search(variable_name)),\
        "Variable name contain invalid characters (Allowed are only capital letters, numbers and sign '_')."

    if not val_type:
        # temporary
        if variable_name not in world.define:
            tmp = variable_val if variable_val.isdigit() else variable_val
            world.define.append([variable_name, tmp])
        else:
            world.define[variable_name] = variable_val
    elif val_type:
        # permanent
        # TO: for same name change value
        try:
            imported = getattr(__import__('init_all', fromlist=[variable_name]), variable_name)
        except:
            init_all = open("features/init_all.py", "a")
            init_all.write("\n# USER VARIABLE:\n" + variable_name + " = " +
                           (variable_val if variable_val.isdigit() else '\"' + variable_val + '\"'))
            init_all.close()


def user_victory():
    if not os.path.exists(world.cfg["dir_name"]):
        os.makedirs(world.cfg["dir_name"])
    copy('../doc/.victory.jpg', world.cfg["dir_name"] + '/celebrate_success.jpg')


def log_contains(server_type, condition, line):
    if server_type == "DHCP":
        log_file = world.cfg["dhcp_log_file"]
    elif server_type == "DNS":
        log_file = world.cfg["dns_log_file"]
    else:
        assert False, "No such name as: {server_type}".format(**locals())

    result = fabric_sudo_command('grep -c "%s" %s' % (line, log_file))

    if condition is not None:
        if result.succeeded:
            assert False, 'Log contains line: "%s" But it should NOT.' % line
    else:
        if result.failed:
            assert False, 'Log does NOT contain line: "%s"' % line


def regular_file_contain(file_name, condition, line, destination=None):

    if destination is None:
        result = fabric_sudo_command('grep -c "%s" %s' % (line, file_name))
    else:
        result = fabric_sudo_command('grep -c "%s" %s' % (line, file_name), destination_host=destination)

    if condition is not None:
        if result.succeeded:
            assert False, 'File {0} contains line/phrase: {1} But it should NOT.'.format(file_name, line)
    else:
        if result.failed:
            assert False, 'File {0} does NOT contain line/phrase: {1} .'.format(file_name, line)


def remove_from_db_table(table_name, db_type, db_name=world.f_cfg.db_name,
                         db_user=world.f_cfg.db_user, db_passwd=world.f_cfg.db_passwd):

    if db_type in ["mysql", "MySQL"]:
        # that is tmp solution - just clearing not saving.
        command = 'mysql -u {db_user} -p{db_passwd} -e "delete from {table_name}" {db_name}'.format(**locals())
        fabric_run_command(command)
    elif db_type in ["postgresql", "PostgreSQL"]:
        command = 'psql -U {db_user} -d {db_name} -c "delete from {table_name}"'.format(**locals())
        fabric_run_command(command)
    elif db_type == "cql":
        # TODO: hardcoded passwords for now in cassandra, extend it in some time :)
        command = 'for table_name in dhcp_option_scope host_reservations lease4 lease6 logs;' \
                  ' do cqlsh --keyspace=keatest --user=keatest --password=keatest -e "TRUNCATE $table_name;"' \
                  ' ; done'.format(**locals())
        fabric_run_command(command)
    else:
        assert False, "db type {db_type} not recognized/not supported".format(**locals())


def db_table_contain(table_name, db_type, condition, line, db_name=world.f_cfg.db_name,
                     db_user=world.f_cfg.db_user, db_passwd=world.f_cfg.db_passwd):

    if db_type in ["mysql", "MySQL"]:
        command = 'mysql -u {db_user} -p{db_passwd} -e "select * from {table_name}"' \
                  ' {db_name} --silent --raw > /tmp/mysql_out'.format(**locals())
        fabric_run_command(command)
        result = fabric_sudo_command('grep -c "{line}" /tmp/mysql_out'.format(**locals()))

    elif db_type in ["postgresql", "PostgreSQL"]:
        command = 'psql -U {db_user} -d {db_name} -c "select * from {table_name}" > /tmp/pgsql_out'.format(**locals())
        fabric_run_command(command)
        result = fabric_sudo_command('grep -c "{line}" /tmp/pgsql_out'.format(**locals()))

    elif world.f_cfg.db_type == "cql":
        result = -1
        # command = 'for table_name in dhcp_option_scope host_reservations lease4 lease6;' \
        #           ' do cqlsh --keyspace=keatest --user=keatest --password=keatest -e "TRUNCATE $table_name;"' \
        #           ' ; done'.format(**locals())
        # fabric_run_command(command)
    else:
        assert False, "db type {db_type} not recognized/not supported".format(**locals())

    if condition is not None:
        if int(result) > 0:
            assert False, 'In database {0} table name "{1}" has {2} of: "{3}".' \
                          ' That is to much.'.format(db_type, table_name, result, line)
    else:
        if int(result) < 1:
            assert False, 'In database {0} table name "{1}" has {2} of: "{3}".'.format(db_type,
                                                                                       table_name, result, line)


def log_contains_count(server_type, count, line):
    if server_type == "DHCP":
        log_file = world.cfg["dhcp_log_file"]
    elif server_type == "DNS":
        log_file = world.cfg["dns_log_file"]
    else:
        assert False, "No such name as: {server_type}".format(**locals())

    result = fabric_sudo_command('grep -c "%s" %s' % (line, log_file))

    if count != result:
        assert False, 'Log has {0} of expected {1} of line: "{2}".'.format(result, count, line)


def change_network_variables(value_name, value):
    if value_name == "source_port":
        world.cfg["source_port"] = int(value)
    elif value_name == "destination_port":
        world.cfg["destination_port"] = int(value)
    elif value_name == "client_link_local_address":
        world.cfg["cli_link_local"] = value
    elif value_name == "source_address":
        world.cfg["source_IP"] = value
        # world.cfg["address_v6"] = value
    elif value_name == "destination_address":
        world.cfg["destination_IP"] = value
    elif value_name == "dns_iface":
        world.cfg["dns_iface"] = value
    elif value_name == "dns_address":
        world.cfg["dns_addr"] = value
    elif value_name == "dns_port":
        world.cfg["dns_port"] = int(value)
    else:
        assert False, "There is no possibility of configuration value named: {value_name}".format(**locals())


def execute_shell_script(path, arguments):
    result = fabric_sudo_command(path + ' ' + arguments, hide_all=False)

    file_name = path.split("/")[-1] + '_output'
    file_name = generate_file_name(1, file_name)

    # assert False, type(result.stdout)
    if not os.path.exists(world.cfg["dir_name"]):
        os.makedirs(world.cfg["dir_name"])

    myfile = open(world.cfg["dir_name"] + '/' + file_name, 'w')
    myfile.write(unicode('Script: ' + path))
    if arguments == '':
        arguments = "no arguments used!"
    myfile.write(unicode('\nwith arguments: ' + arguments + '\n'))
    if result.failed:
        myfile.write(unicode('\nStatus: FAILED\n'))
    else:
        myfile.write(unicode('\nStatus: SUCCEED\n'))

    myfile.write(unicode('\nScript stdout:\n' + result.stdout))
    myfile.close()
    forge_sleep(3, "seconds")


def execute_shell_command(command):
    fabric_sudo_command(command, hide_all=False)


def connect_socket(command):
    fabric_sudo_command(command, hide_all=False)


def send_through_socket_server_site(socket_path, command, destination_address=world.f_cfg.mgmt_address):
    if type(command) is unicode:
        command = command.encode('ascii', 'ignore')
    command_file = open(world.cfg["dir_name"] + '/command_file', 'w')
    try:
        command_file.write(command)
    except:
        command_file.close()
        command_file = open(world.cfg["dir_name"] + '/command_file', 'wb')  # TODO: why 'w' / 'wb'
        command_file.write(command)
    command_file.close()
    fabric_send_file(world.cfg["dir_name"] + '/command_file', 'command_file', destination_host=destination_address)
    world.control_channel = fabric_sudo_command('socat UNIX:' + socket_path + ' - <command_file', hide_all=True,
                                                destination_host=destination_address)
    fabric_remove_file_command('command_file')
    try:
        result = json.loads(world.control_channel)
        log.info(json.dumps(result, sort_keys=True, indent=2, separators=(',', ': ')))
        world.cmd_resp = result
    except:
        log.exception('Problem with parsing json: ', str(world.control_channel))
        world.cmd_resp = world.control_channel
    return world.cmd_resp


def send_through_http(host_address, host_port, command):
    world.control_channel = requests.post("http://" + host_address + ":" + locale.str(host_port),
                                          headers={"Content-Type": "application/json"}, data=command).text

    result = json.loads(world.control_channel)
    log.info(json.dumps(result, sort_keys=True, indent=2, separators=(',', ': ')))
    return result


def assert_result(condition, result, value):
    if result == 1 and condition is None:
        # it's ok :)
        pass
    elif result == 1 and condition is not None:
        # we received something we didn't want
        assert False, "Received message contain: " + value + "; which was not anticipated."
    elif result == 0 and condition is None:
        assert False, "Received message does not contain: " + value
    elif result == 0 and condition is not None:
        pass


def parse_json_file(condition, parameter_name, parameter_value):
    world.control_channel_parsed = [None, None, None]
    save_local_file(json.dumps(json.loads(world.control_channel), sort_keys=True, indent=2,
                               separators=(',', ': ')), local_file_name=generate_file_name(1, "command_result"))

    # here there is messed situation, when JSON respond comes via HTTP it's a list, when via socket, it's dict.
    loaded_json = json.loads(world.control_channel)
    if type(loaded_json) is list:
        loaded_json = loaded_json[0]

    try:
        world.control_channel_parsed[0] = "".join(json.dumps(loaded_json["arguments"]))
    except KeyError:
        world.control_channel_parsed[0] = "arguments not found in received message"
    try:
        world.control_channel_parsed[1] = "".join(json.dumps(loaded_json["result"]))
    except KeyError:
        world.control_channel_parsed[1] = "result not found in received message"
    try:
        world.control_channel_parsed[2] = "".join(json.dumps(loaded_json["text"]))
    except KeyError:
        world.control_channel_parsed[2] = "text not found in received message"

    if parameter_name == "arguments":
        if parameter_value in world.control_channel_parsed[0]:
            assert_result(condition, 1, parameter_value)
        else:
            assert_result(condition, 0, parameter_value)
    elif parameter_name == "result":
        if parameter_value == world.control_channel_parsed[1]:

            assert_result(condition, 1, parameter_value)
        else:
            assert_result(condition, 0, parameter_value)
    elif parameter_name == "text":
        if parameter_value in world.control_channel_parsed[2]:
            assert_result(condition, 1, parameter_value)
        else:
            assert_result(condition, 0, parameter_value)
    else:
        pass


def parse_socket_received_data():
    pass


def set_value(env_name, env_value):
    world.f_cfg.set_env_val(env_name, env_value)


def temp_set_value(env_name, env_value):
    world.f_cfg.set_temporaty_value(env_name, env_value)
