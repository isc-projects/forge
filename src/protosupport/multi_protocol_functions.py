# Copyright (C) 2013-2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Wlodzimierz Wencel

# pylint: disable=anomalous-backslash-in-string
# pylint: disable=consider-using-f-string
# pylint: disable=consider-using-in
# pylint: disable=consider-using-with
# pylint: disable=inconsistent-return-statements
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-timeout
# pylint: disable=no-else-break
# pylint: disable=no-else-continue
# pylint: disable=protected-access
# pylint: disable=too-many-branches
# pylint: disable=unbalanced-tuple-unpacking
# pylint: disable=undefined-variable
# pylint: disable=unexpected-keyword-arg
# pylint: disable=unidiomatic-typecheck
# pylint: disable=unspecified-encoding
# pylint: disable=unused-argument
# pylint: disable=unused-variable

import datetime
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
import socket
import logging
import codecs
import ipaddress
import copy
import requests

from src.forge_cfg import world
from src.softwaresupport.multi_server_functions import fabric_send_file, fabric_download_file,\
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


# ------------------------------- FILE TRANSFER ------------------------------ #


def copy_file_from_server(remote_path, local_filename='downloaded_file'):
    """
    Copy file from remote server via ssh. Address/login/password from init_all.py
    Path required.
    """
    fabric_download_file(remote_path, world.cfg["test_result_dir"] + f'/{local_filename}')


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


################################################################################


def sort_container(obj):
    """
    Helper function to sort JSON for ease of comparison.
    :param obj: json as dictionary or other list
    :return: Sorted json dictionary or other list
    """
    if isinstance(obj, dict):
        return json.loads(json.dumps(obj, sort_keys=True))
    if isinstance(obj, list):
        return sorted(sort_container(x) for x in obj)
    return obj


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
            getattr(__import__('init_all', fromlist=[variable_name]), variable_name)
        except ImportError:
            init_all = open("init_all.py", "a")  # TODO: this should be removed
            init_all.write("\n# USER VARIABLE:\n" + variable_name + " = " +
                           (variable_val if variable_val.isdigit() else '\"' + variable_val + '\"'))
            init_all.close()


def user_victory():
    if not os.path.exists(world.cfg["test_result_dir"]):
        os.makedirs(world.cfg["test_result_dir"])
    shutil.copy('../doc/.victory.jpg', world.cfg["test_result_dir"] + '/celebrate_success.jpg')


# ------------------------------ FILE INSPECTION ----------------------------- #


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
        assert len(downloaded_stripped) < len(local_stripped), 'Local file is part of a downloaded life.'


def get_line_count_in_file(line, file, destination=world.f_cfg.mgmt_address):
    """
    Retrieves the number of lines contained in a file.

    :param line: line (or part of file or glob pattern) being checked
    :param file: name of file being checked, or glob pattern potentially matching multiple files
    :param destination: address of server hosting the file
    """
    command = 'grep "$(cat <<EOF\n'
    command += f'{line}\n'
    command += 'EOF\n'
    command += f')" {file} | wc -l'
    result = fabric_sudo_command(command, destination_host=destination, ignore_errors=True)
    assert result.succeeded, f'Command in get_line_count_in_file failed:\n{command}'
    return int(result)


def get_line_count_in_log(line, log_file=None, destination=world.f_cfg.mgmt_address):
    """
    Retrieves the number of lines contained in a log file.

    :param line: line (or part of file or glob pattern) being checked
    :param log_file: name of the log file being checked. If None, default values
                     representing Kea logs are used.
    :param destination: address of server hosting the file
    """
    if world.f_cfg.install_method == 'make':
        if log_file is None:
            log_file = 'kea.log'
        log_file = world.f_cfg.log_join(log_file)
        result = get_line_count_in_file(line, log_file, destination)
    else:
        if log_file is None or log_file == 'kea.log_ddns':
            if log_file == 'kea.log_ddns':
                if world.server_system == 'redhat':
                    service_name = 'kea-dhcp-ddns'
                else:
                    service_name = 'isc-kea-dhcp-ddns-server'
            else:
                if world.server_system == 'redhat':
                    service_name = f'kea-dhcp{world.proto[1]}'
                else:
                    service_name = f'isc-kea-dhcp{world.proto[1]}-server'
            cmd = f'journalctl -u {service_name} |'  # get logs of kea service
            cmd += ' grep "$(cat <<EOF\n'
            cmd += f'{line}\n'
            cmd += 'EOF\n'
            cmd += ')" | wc -l'
            result = fabric_sudo_command(cmd, destination_host=destination, ignore_errors=True)
        else:
            log_file = world.f_cfg.log_join(log_file)
            result = get_line_count_in_file(line, log_file, destination)
    return int(result)


def file_contains_line(file, line, destination=world.f_cfg.mgmt_address):
    result = get_line_count_in_file(line, file, destination=destination)
    assert result > 0, f'Expected file "{file}" to contain line "{line}", but it does not.'


def file_contains_line_n_times(file, n, line, destination=world.f_cfg.mgmt_address):
    result = get_line_count_in_file(line, file, destination=destination)
    assert result == n, f'Expected file {file} to contain line "{line}" a number of {n} time{"" if n == 1 else "s"}. ' \
                        f'Found {result} time{"" if result == 1 else "s"}.'


def file_doesnt_contain_line(file, line, destination=world.f_cfg.mgmt_address):
    result = get_line_count_in_file(line, file, destination=destination)
    assert result == 0, f'Expected file "{file}" to not contain line "{line}".' \
                        f'Found {result} time{"" if result == 1 else "s"}.'


def lease_file_contains(line, destination=world.f_cfg.mgmt_address):
    file_contains_line(world.f_cfg.get_leases_path(), line, destination=destination)


def lease_file_doesnt_contain(line, destination=world.f_cfg.mgmt_address):
    file_doesnt_contain_line(world.f_cfg.get_leases_path(), line, destination=destination)


def log_contains(line, log_file=None, destination=world.f_cfg.mgmt_address):
    result = get_line_count_in_log(line, log_file, destination=destination)
    assert result > 0, f'Expected log file {log_file} to contain line "{line}", but it does not.'


def log_doesnt_contain(line, log_file=None, destination=world.f_cfg.mgmt_address):
    result = get_line_count_in_log(line, log_file, destination=destination)
    assert result == 0, f'Expected log file {log_file} to not contain line "{line}".' \
                        f'Found {result} time{"" if result == 1 else "s"}.'


def wait_for_message_in_log(line, count=1, timeout=4, log_file=None, destination=world.f_cfg.mgmt_address):
    """
    Wait until a line appears a certain number of times in a file.

    :param line: line (or part of file or glob pattern) being checked
    :param count: number of matching lines to wait for
    :param timeout: time to wait for in seconds
    :param file: name of file being checked, or glob pattern potentially matching multiple files.
                 Default: None i.e. default log file
    :param destination: address of server hosting the file
    """
    started_at = datetime.datetime.now()
    count = int(count)
    should_finish_by = started_at + datetime.timedelta(seconds=timeout)
    while True:
        # Get the number of line occurrences in the log.
        result = get_line_count_in_log(line, log_file, destination=destination)

        # If enough lines have been logged, we are done waiting.
        if count <= result:
            break

        # Assert that the timeout hasn't passed yet.
        assert datetime.datetime.now() < should_finish_by, \
            f'Timeout {timeout}s exceeded while waiting for {count} ' \
            f'line{"" if count == 1 else "s"} of "{line}" in log file {log_file}. ' \
            f'Instead got {result} lines.'

        # Sleep a bit to avoid busy waiting.
        forge_sleep(100, 'milliseconds')


################################################################################


def remove_from_db_table(table_name, db_type, db_name=world.f_cfg.db_name,
                         db_user=world.f_cfg.db_user, db_passwd=world.f_cfg.db_passwd):

    if db_type in ["mysql", "MySQL"]:
        # that is tmp solution - just clearing not saving.
        command = 'mysql -u {db_user} -p{db_passwd} -e "delete from {table_name}" {db_name}'.format(**locals())
        fabric_run_command(command)
    elif db_type in ["postgresql", "PostgreSQL"]:
        command = 'PGPASSWORD={db_passwd} psql -h localhost -U {db_user} -d {db_name} -c "delete from {table_name}"'.format(**locals())
        fabric_run_command(command)
    else:
        assert False, "db type {db_type} not recognized/not supported".format(**locals())


def db_table_record_count(table_name, db_type, line="", grep_cmd=None, db_name=world.f_cfg.db_name,
                          db_user=world.f_cfg.db_user, db_passwd=world.f_cfg.db_passwd,
                          destination=world.f_cfg.mgmt_address, lease=None):
    if db_type.lower() == "mysql":
        if lease is None:
            select = 'select *'
        elif table_name == 'lease6':
            select = "select"
            for attribute in lease:
                if attribute == "duid":
                    select += ", hex(%s)" % attribute
                else:
                    select += ", %s" % attribute
            select = select.replace(",", "", 1)  # delete first comma
        elif table_name == 'lease4':
            select = "select"
            for attribute in lease:
                if attribute in ["address", "hwaddr", "client_id"]:
                    select += ", hex(%s)" % attribute
                else:
                    select += ", %s" % attribute
            select = select.replace(",", "", 1)  # delete first comma
        else:
            select = 'select *'
        command = 'mysql -u {db_user} -p{db_passwd} -e "{select} from {table_name}"' \
                  ' {db_name} --silent > /tmp/db_out'.format(**locals())

    elif db_type.lower() in ["postgresql", "pgsql"]:
        if lease is None:
            select = 'select *'
        elif table_name == 'lease4':
            select = "select"
            for attribute in lease:
                if attribute == "address":
                    select += ", to_hex(%s)" % attribute
                elif attribute == "hwaddr":
                    select += ", encode(%s,'hex')" % attribute
                else:
                    select += ", %s" % attribute
            select = select.replace(",", "", 1)  # delete first comma
        else:
            select = 'select *'
        command = 'PGPASSWORD={db_passwd} psql -h localhost -U {db_user} -d {db_name} ' \
                  '-c "{select} from {table_name}" > /tmp/db_out'.format(**locals())

    else:
        assert False, "db type {db_type} not recognized/not supported".format(**locals())

    fabric_run_command(command, destination_host=destination)
    cmd = 'grep -c "{line}" /tmp/db_out'.format(**locals())
    if grep_cmd is not None:
        cmd = grep_cmd

    result = fabric_sudo_command(cmd, ignore_errors=True, destination_host=destination)
    return int(result)


def db_table_contains_line(table_name, db_type, line="", grep_cmd=None, expect=True, db_name=world.f_cfg.db_name,
                           db_user=world.f_cfg.db_user, db_passwd=world.f_cfg.db_passwd,
                           destination=world.f_cfg.mgmt_address, lease=None):
    result = db_table_record_count(table_name, db_type, line,
                                   grep_cmd, db_name, db_user, db_passwd,
                                   destination, lease)
    if expect:
        if result < 1:
            assert False, 'In database {0} table name "{1}" has {2} of: "{3}".'\
                .format(db_type, table_name, result, line)
    else:
        if result > 0:
            assert False, 'In database {0} table name "{1}" has {2} of: "{3}".' \
                          ' That is too much.'.format(db_type, table_name, result, line)


def db_table_contains_line_n_times(table_name, db_type, n, line="", grep_cmd=None, db_name=world.f_cfg.db_name,
                                   db_user=world.f_cfg.db_user, db_passwd=world.f_cfg.db_passwd,
                                   destination=world.f_cfg.mgmt_address):
    result = db_table_record_count(table_name, db_type, line,
                                   grep_cmd, db_name, db_user, db_passwd,
                                   destination)
    assert result == n, f'Expected {db_type} database table {table_name} to contain line "{line}" a number of {n} time{"" if n == 1 else "s"}. ' \
                        f'Found {result} time{"" if result == 1 else "s"}.'


def lease_dump(backend, db_name=world.f_cfg.db_name, db_user=world.f_cfg.db_user,
               db_passwd=world.f_cfg.db_passwd, destination_address=world.f_cfg.mgmt_address,
               out="/tmp/lease_dump.csv"):
    """
    Function dumps database to CSV file performing kea-admin lease-dump command on server.
    :param backend: Select database backend: mysql, pgsql
    :param db_name: specifies a database name to connect to
    :param db_user: specifies username when connecting to a database
    :param db_passwd: specifies a password for the database connection
    :param destination_address: specifies server address for management
    :param out: output file path
    :return: output file path on server
    """
    path = os.path.join(world.f_cfg.software_install_path, 'sbin/kea-admin')

    backend = 'pgsql' if backend == "postgresql" else backend

    remove_file_from_server(out)
    execute_shell_cmd(f"{path} lease-dump {backend} -u {db_user} -p {db_passwd} "
                      f"-n {db_name} -{world.f_cfg.proto[1]} -o {out}", dest=destination_address)
    return out


def lease_upload(backend, leases_file, db_name=world.f_cfg.db_name, db_user=world.f_cfg.db_user,
                 db_passwd=world.f_cfg.db_passwd, destination_address=world.f_cfg.mgmt_address):
    """
    Function uploads CSV file to database performing kea-admin lease-upload command on server.
    :param backend: Select database backend: mysql, pgsql
    :param leases_file: input file path
    :param db_name: specifies a database name to connect to
    :param db_user: specifies username when connecting to a database
    :param db_passwd: specifies a password for the database connection
    :param destination_address: specifies server address for management
    :return: shell operation result
    """
    path = os.path.join(world.f_cfg.software_install_path, 'sbin/kea-admin')

    backend = 'pgsql' if backend == "postgresql" else backend

    result = execute_shell_cmd(f"{path} lease-upload {backend} -u {db_user} -p {db_passwd} "
                               f"-n {db_name} -{world.f_cfg.proto[1]} -i {leases_file}",
                               dest=destination_address)
    return result


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


def execute_shell_cmd(path, save_results=True, dest=world.f_cfg.mgmt_address, exp_failed=False):
    result = fabric_sudo_command(path, hide_all=False, ignore_errors=True,
                                 destination_host=dest)

    if save_results:
        file_name = path.split("/")[-1] + '_output'
        file_name = generate_file_name(1, file_name)

        # assert False, type(result.stdout)
        if not os.path.exists(world.cfg["test_result_dir"]):
            os.makedirs(world.cfg["test_result_dir"])

        myfile = open(world.cfg["test_result_dir"] + '/' + file_name, 'w')
        myfile.write('Script: ' + path)
        if result.failed:
            myfile.write('\nStatus: FAILED\n')
        else:
            myfile.write('\nStatus: SUCCEED\n')

        myfile.write('\nScript stdout:\n' + result.stdout + '\n')
        myfile.close()

    if exp_failed:
        assert not result.succeeded
    else:
        assert result.succeeded

    return result


def test_define_value(*args):
    """Substitute variable references in a string.

    Designed to use in test scenarios values from init_all.py file. To makes them even more portable
    Bash like define variables: $(variable_name)
    You can use steps like:
        Client download file from server stored in: $(SERVER_SETUP_DIR)/other_dir/my_file
    or
        Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)/my_file

    $ sign is very important without it Forge wont find variable in init_all.

    You can use any variable form init_all in that way. Also you can add them using step:
    """
    tested_args = []
    for arg in args:
        if arg is None:
            tested_args.append(arg)
            continue
        try:
            tmp = str(arg)
        except UnicodeEncodeError:
            tmp = unicode(arg)
        tmp_loop = ""
        while True:
            imported = None
            front = None
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
                if front is None:
                    tmp_loop = str(imported) + tmp[index + 1:]
                else:
                    tmp_loop = front + str(imported) + tmp[index + 1:]
            else:
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
        if isinstance(v, str):
            cfg[k] = test_define_value(v)[0]
        elif isinstance(v, dict):
            substitute_vars(v)
        elif isinstance(v, list):
            new_list = []
            for lv in v:
                if isinstance(lv, dict):
                    substitute_vars(lv)
                    new_list.append(lv)
                elif isinstance(lv, str):
                    new_list.append(test_define_value(lv)[0])
                else:
                    new_list.append(lv)
            cfg[k] = new_list


def _process_ctrl_response(response, exp_result):
    world.control_channel = response
    try:
        result = json.loads(response)
        if world.f_cfg.forge_verbose:
            log.info(json.dumps(result, sort_keys=True, indent=2, separators=(',', ': ')))
    except BaseException:
        log.exception('Problem with parsing json:\n"%s"', str(response))
        result = response

    if exp_result is not None:
        if isinstance(result, dict):
            res = result
        elif isinstance(result, list):
            res = result[0]
        else:
            assert False, 'result is incorrectly formatted'
        assert 'result' in res and res['result'] == exp_result,\
            f'unexpected result: {res["result"]} we were expecting {exp_result}'
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
    if world.f_cfg.forge_verbose:
        log.info(pprint.pformat(command))
    if isinstance(command, dict):
        command = json.dumps(command)
    command_file = open(world.cfg["test_result_dir"] + '/command_file', 'w')
    try:
        command_file.write(command)
    except BaseException:
        command_file.close()
        command_file = open(world.cfg["test_result_dir"] + '/command_file', 'wb')  # TODO: why 'w' / 'wb'
        command_file.write(command)
    command_file.close()
    fabric_send_file(world.cfg["test_result_dir"] + '/command_file', 'command_file', destination_host=destination_address)

    if socket_name is not None:
        socket_path = world.f_cfg.run_join(socket_name)
    else:
        socket_path = world.f_cfg.run_join('control_socket')
    cmd = 'socat -t 5 UNIX:' + socket_path + ' - <command_file'

    attempts = 0
    while attempts < 3:
        response = fabric_sudo_command(cmd, hide_all=True, destination_host=destination_address, ignore_errors=exp_failed)
        if exp_failed:
            assert response.failed
        else:
            assert response.succeeded
        if str(response) != '':
            break
        attempts += 1

    fabric_remove_file_command('command_file')

    result = _process_ctrl_response(response, exp_result)
    return result


def send_ctrl_cmd_via_http(command, address, port, exp_result=0, exp_failed=False, https=False, verify=None, cert=None,
                           headers=None):
    """
    Send command to Control Agent using http or https
    :param command: dict, command
    :param address: string, IP address of Control Agent
    :param port: int, port number on which Control Agent is listening
    :param exp_result: int, value of result parameter send back by Control Agent
    :param exp_failed: boolean, set to True if we expect that message over http/https will be failed to deliver
    :param https: boolean, True if command should be send using https (default False)
    :param verify: boolean, verification of certificate
    :param cert: tuple, contain client cert and key
    :param headers: dict, dictionary that should be added to message headers
    return dict, json struct response from Control Agent
    """
    if exp_failed:
        # expected result should be default (0) or None
        assert exp_result in [0, None]
        # force expected result to None so it is not checked
        exp_result = None

    d_headers = {"Content-Type": "application/json"}
    if headers is not None:
        d_headers.update(headers)

    addr = "http://" + address + ":" + locale.str(port)
    addr = addr.replace('http', 'https') if https else addr

    if world.f_cfg.forge_verbose:
        log.info(pprint.pformat(command))
        log.info("send to address: %s", addr)

    if isinstance(command, dict):
        command = json.dumps(command)

    try:
        response = requests.post(addr, headers=d_headers, data=command, verify=verify, cert=cert)
    except requests.exceptions.ConnectionError:
        # this is weird, if post fail it should have 400 or 500 but it's not created instead
        response = None

    if exp_failed:
        if response is not None:
            assert False, "Connection successful, we expected failure"
    else:
        if response is None:
            assert False, "Connection failed, but we expected success"
        elif 200 <= response.status_code < 300:
            return _process_ctrl_response(response.text, exp_result)
        elif response.status_code in [401, 403]:
            return _process_ctrl_response(response._content, exp_result)


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


# ----------------------------- FILE MANIPULATION ---------------------------- #


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


################################################################################


def set_value(env_name, env_value):
    world.f_cfg.set_env_val(env_name, env_value)


def check_leases(leases_list, backend='memfile', destination=world.f_cfg.mgmt_address, should_succeed=True):
    if not isinstance(leases_list, list):
        leases_list = [leases_list]
    leases_list_copy = copy.deepcopy(leases_list)
    # TODO: make check_leases() work with the output of leaseX-get-all

    if backend == 'memfile':
        for lease in leases_list_copy:
            cmd = "cat %s " % world.f_cfg.get_leases_path()
            if "client_id" in lease:
                lease['client_id'] = ':'.join(lease['client_id'][i:i + 2] for i in range(0, 14, 2))
            for attribute in lease:
                cmd += "| grep %s " % lease[attribute]
            cmd += "| grep -c ^"

            result = fabric_sudo_command(cmd, ignore_errors=True, destination_host=destination)
            if should_succeed:
                assert result.succeeded, "Expected lease, but it does not exist: %s" % json.dumps(lease)
            else:
                assert result.failed, "Expected lease to not exist, but it does: %s" % json.dumps(lease)
            # TODO write check if there is more than one entry of the same type

    elif backend.lower() in ['mysql', 'postgresql', 'pgsql']:
        for lease in leases_list_copy:
            if world.f_cfg.proto == 'v4':
                table = 'lease4'
                cmd = "cat /tmp/db_out "
                if "hwaddr" in lease:
                    lease["hwaddr"] = lease["hwaddr"].replace(":", "")
                if "address" in lease:
                    lease["address"] = convert_address_to_hex(lease["address"])
                for attribute in lease:
                    cmd += "| grep -i %s " % lease[attribute]
                cmd += "| grep -c ^"
            elif world.f_cfg.proto == 'v6':
                table = 'lease6'
                cmd = "cat /tmp/db_out "
                if "duid" in lease:
                    lease["duid"] = lease["duid"].replace(":", "")
                for attribute in lease:
                    cmd += "| grep -i %s " % lease[attribute]
                cmd += "| grep -c ^"

            else:
                assert False, "There is something bad, you should never see this :)"
            db_table_contains_line(table, backend, grep_cmd=cmd,
                                   destination=destination, lease=lease,
                                   expect=should_succeed)


def convert_address_to_hex(address):
    '''Convert string address to hexadecimal representation.'''
    address = test_define_value(address)[0]
    if '.' in address:
        return '{:02X}{:02X}{:02X}{:02X}'.format(*map(int, address.split('.')))
    if ':' in address:
        # TODO: support for abbreviated two-colon format e.g. 2001:db8::1
        return codecs.decode(address.replace(':', ''), 'hex')
    raise Exception('%s is not a valid IPv4 or IPv6 address' % address)


def _increase_address_n(prefix):
    '''Increment an IPv[46]Network address.'''
    return prefix.network_address + \
        (1 << (prefix.network_address.max_prefixlen - int(prefix.prefixlen)))


def increase_address(address, prefix_length):
    '''
    Increment an IPv4 or IPv6 address belonging to a network with given prefix
    length.
    '''
    address, prefix_length = test_define_value(address, prefix_length)
    if '.' in address:
        network = ipaddress.IPv4Network(address + '/' + prefix_length)
        new_address = _increase_address_n(network)
        new_network = ipaddress.IPv4Network(
            new_address.compressed + '/' + prefix_length)
        return str(new_network.network_address)
    if ':' in address:
        network = ipaddress.IPv6Network(address + '/' + prefix_length)
        new_address = _increase_address_n(network)
        new_network = ipaddress.IPv6Network(
            new_address.compressed + '/' + prefix_length)
        return str(new_network.network_address)
    raise Exception('%s is not a valid IPv4 or IPv6 address' % address)


def get_address_of_local_vm(addr: str = None):
    """
    Get address of an interface that is facing other address in forge setup
    :param addr: ip address of remote system
    :return: string, local ip address
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((addr, 80))
    a = s.getsockname()[0]
    s.close()
    return a
