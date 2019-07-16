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
import re
import tty
import time
import json
import locale
import pprint
import termios
import shutil
import logging

#from _pyio import open  # TODO: why this way? WTF?
import requests

from forge_cfg import world
from softwaresupport.multi_server_functions import fabric_send_file, fabric_download_file,\
        fabric_remove_file_command, remove_local_file, fabric_sudo_command, generate_file_name,\
        save_local_file, fabric_run_command


log = logging.getLogger('forge')


def forge_sleep(duration, time_units):
    divide = 1.0
    if time_units == 'milliseconds' or time_units == 'millisecond':
        divide = 1000.0
    time.sleep(duration * 1.0 / divide)


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
    fabric_download_file(remote_path, world.cfg["test_result_dir"] + '/downloaded_file')


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

    outcome = open(world.cfg["test_result_dir"] + '/file_compare', 'w')

    # first remove all commented and blank lines of both files
    downloaded_stripped = strip_file(world.cfg["test_result_dir"] + '/downloaded_file')
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
        remove_local_file(world.cfg["test_result_dir"] + '/file_compare')

    assert error_flag, 'Downloaded file is NOT the same as local. Check %s/file_compare for details'\
                       % world.cfg["test_result_dir"]

    if len(downloaded_stripped) != len(local_stripped):
        assert len(downloaded_stripped) > len(local_stripped), 'Downloaded file is part of a local file.'
        assert len(downloaded_stripped) < len(local_stripped), 'Local file is a part of a downlaoded life.'


def file_includes_line(condition, line):
    """
    Check if downloaded file contain line.
    """
    downloaded_stripped = strip_file(world.cfg["test_result_dir"] + '/downloaded_file')
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
        # TODO: WTF?
        try:
            imported = getattr(__import__('init_all', fromlist=[variable_name]), variable_name)
        except:
            init_all = open("init_all.py", "a")  # TODO: this should be removed
            init_all.write("\n# USER VARIABLE:\n" + variable_name + " = " +
                           (variable_val if variable_val.isdigit() else '\"' + variable_val + '\"'))
            init_all.close()


def user_victory():
    if not os.path.exists(world.cfg["test_result_dir"]):
        os.makedirs(world.cfg["test_result_dir"])
    shutil.copy('../doc/.victory.jpg', world.cfg["test_result_dir"] + '/celebrate_success.jpg')


def log_contains(line, condition, log_file=None):
    if world.f_cfg.install_method == 'make':
        if log_file is None:
            log_file = 'kea.log'
        log_file = world.f_cfg.log_join(log_file)
        result = fabric_sudo_command('grep -c "%s" %s' % (line, log_file))
    else:
        if log_file is None:
            cmd = 'ts=`systemctl show -p ActiveEnterTimestamp isc-kea-dhcp%s-server.service | awk \'{{print $2 $3}}\'`;' % world.proto[1]
            cmd += ' journalctl -u isc-kea-dhcp%s-server.service --since $ts |' % world.proto[1]
            cmd += 'grep -c "%s"' % line
            result = fabric_sudo_command(cmd)
        else:
            log_file = world.f_cfg.log_join(log_file)
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
    else:
        assert False, "There is no possibility of configuration value named: {value_name}".format(**locals())


def execute_shell_cmd(path, arguments=''):
    result = fabric_sudo_command(path + ' ' + arguments, hide_all=False)

    file_name = path.split("/")[-1] + '_output'
    file_name = generate_file_name(1, file_name)

    # assert False, type(result.stdout)
    if not os.path.exists(world.cfg["test_result_dir"]):
        os.makedirs(world.cfg["test_result_dir"])

    myfile = open(world.cfg["test_result_dir"] + '/' + file_name, 'w')
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

    assert result.succeeded

    return result


def test_define_value(*args):
    """Substitute variable references in a string.

    Designed to use in test scenarios values from ini_all.py file. To makes them even more portable
    Bash like define variables: $(variable_name)
    You can use steps like:
        Client download file from server stored in: $(SERVER_SETUP_DIR)/other_dir/my_file
    or
        Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)/my_file

    $ sign is very important without it Forge wont find variable in init_all.

    You can use any variable form init_all in that way. Also you can add them using step:
    "Client defines new variable: (\S+) with value (\S+)." """
    tested_args = []
    for i in range(len(args)):
        try:
            tmp = str(args[i])
        except UnicodeEncodeError:
            tmp = unicode(args[i])
        tmp_loop = ""
        while True:
            imported = None
            front = None
            # if "$" in args[i]:
            if "$" in tmp:
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
                # TODO: WTF?
                #if imported is None:
                #    try:
                #        imported = getattr(__import__('init_all', fromlist=[tmp[2: index]]), tmp[2: index])
                #    except ImportError:
                #        assert False, "No variable in init_all.py or in world.define named: " + tmp[2: index]
                if front is None:
                    # tested_args.append(imported + tmp[index + 1:])
                    tmp_loop = str(imported) + tmp[index + 1:]
                else:
                    # tested_args.append(front + imported + tmp[index + 1:])
                    tmp_loop = front + str(imported) + tmp[index + 1:]
            else:
                # tested_args.append(args[i])
                tmp_loop = tmp
            if "$(" not in tmp_loop:
                tested_args.append(tmp_loop)
                break
            else:
                tmp = tmp_loop
    return tested_args


def substitute_vars(cfg):
    """Substitute variable references in any string occurance in dictionary.

    It goes through all fields, arrays etc in dictionary and in any string it substitutes vars.
    It works as test_define_value but it takes dict as argument that contains whole configuration
    fields instead of one big string."""
    for k, v in cfg.items():
        if isinstance(v, basestring):
            cfg[k] = test_define_value(v)[0]
        elif isinstance(v, dict):
            substitute_vars(v)
        elif isinstance(v, list):
            new_list = []
            for lv in v:
                if isinstance(lv, dict):
                    substitute_vars(lv)
                    new_list.append(lv)
                elif isinstance(lv, basestring):
                    new_list.append(test_define_value(lv)[0])
                else:
                    new_list.append(lv)
            cfg[k] = new_list


def _process_ctrl_response(response, exp_result):
    world.control_channel = response
    try:
        result = json.loads(response)
        log.info(json.dumps(result, sort_keys=True, indent=2, separators=(',', ': ')))
    except:
        log.exception('Problem with parsing json: %s', str(response))
        result = response

    if exp_result is not None:
        if isinstance(result, dict):
            res = result
        elif isinstance(result, list):
            res = result[0]
        else:
            raise Exception('unexpected type of result: %s' % str(type(result)))
        assert 'result' in res and res['result'] == exp_result
        if res['result'] == 1:
            assert len(res) == 2 and 'text' in res

    return result


def send_ctrl_cmd_via_socket(command, socket_name=None, destination_address=world.f_cfg.mgmt_address, exp_result=0, exp_failed=False):
    # if command is expected to fail it does not make sense to check response details
    if exp_failed:
        # expected result should be default (0) or None
        assert exp_result in [0, None]
        # force expected result to None so it is not checked
        exp_result = None

    log.info(pprint.pformat(command))
    if isinstance(command, dict):
        command = json.dumps(command)
    command_file = open(world.cfg["test_result_dir"] + '/command_file', 'w')
    try:
        command_file.write(command)
    except:
        command_file.close()
        command_file = open(world.cfg["test_result_dir"] + '/command_file', 'wb')  # TODO: why 'w' / 'wb'
        command_file.write(command)
    command_file.close()
    fabric_send_file(world.cfg["test_result_dir"] + '/command_file', 'command_file', destination_host=destination_address)

    if socket_name is not None:
        socket_path = world.f_cfg.run_join(socket_name)
    else:
        socket_path = world.f_cfg.run_join('control_socket')
    cmd = 'socat UNIX:' + socket_path + ' - <command_file'
    response = fabric_sudo_command(cmd, hide_all=True, destination_host=destination_address)
    if exp_failed:
        assert response.failed
    else:
        assert response.succeeded
    fabric_remove_file_command('command_file')

    result = _process_ctrl_response(response, exp_result)
    return result


def send_ctrl_cmd_via_http(command, address, port, exp_result=0):
    log.info(pprint.pformat(command))
    if isinstance(command, dict):
        command = json.dumps(command)
    response = requests.post("http://" + address + ":" + locale.str(port),
                             headers={"Content-Type": "application/json"},
                             data=command)
    response = response.text

    result = _process_ctrl_response(response, exp_result)
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
