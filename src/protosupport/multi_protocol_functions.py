# Copyright (C) 2013-2025 Internet Systems Consortium, Inc. ("ISC")
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

"""Functions that can be used for testing all protocols."""

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
from src.softwaresupport.multi_server_functions import fabric_send_file, fabric_download_file, \
        fabric_remove_file_command, remove_local_file, fabric_sudo_command, generate_file_name, \
        save_local_file, fabric_run_command


log = logging.getLogger('forge')


def forge_sleep(duration, time_units):
    """forge_sleep.

    :param duration:
    :type duration:
    :param time_units:
    :type time_units:
    """
    divide = 1.0
    if time_units == 'milliseconds' or time_units == 'millisecond':
        divide = 1000.0
    time.sleep(duration * 1.0 / divide)


def test_pause():
    """Pause the test for any reason. Press any key to continue."""
    def getch():
        """Getch.

        :return:
        :rtype:
        """
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
    getch()


# ------------------------------- FILE TRANSFER ------------------------------ #


def copy_file_from_server(remote_path, local_filename='downloaded_file', dest=world.f_cfg.mgmt_address):
    """Copy file from remote server via ssh. Address/login/password from init_all.py.

    :param remote_path:
    :type remote_path: str
    :param local_filename: (Default value = 'downloaded_file')
    :type local_filename:
    :param dest: Default value = world.f_cfg.mgmt_address)
    :type dest:
    :return:
    :rtype:
    """
    fabric_download_file(remote_path, world.cfg["test_result_dir"] + f'/{local_filename}', destination_host=dest)
    return world.cfg["test_result_dir"] + f'/{local_filename}'


def send_file_to_server(local_path, remote_path):
    """Send file to remote server via ssh. Address/login/password from init_all.py.

    :param local_path: relative to lettuce directory
    :type local_path:
    :param remote_path: absolute
    :type remote_path:
    """
    fabric_send_file(local_path, remote_path)


def remove_file_from_server(remote_path, dest=world.f_cfg.mgmt_address):
    """Remove file from remote server.

    :param remote_path:
    :type remote_path:
    :param dest: (Default value = world.f_cfg.mgmt_address)
    :type dest:
    """
    fabric_remove_file_command(remote_path, destination_host=dest)


################################################################################


def sort_container(obj):
    """Sort JSON for ease of comparison.

    :param obj: json as dictionary or other list
    :type obj:
    :return: Sorted json dictionary or other list
    :rtype:
    """
    if isinstance(obj, dict):
        return json.loads(json.dumps(obj, sort_keys=True))
    if isinstance(obj, list):
        return sorted(sort_container(x) for x in obj)
    return obj


def add_variable(variable_name, variable_val, val_type):
    """Define variable and add it to temporary list or to init_all.py file.

    :param variable_name:
    :type variable_name:
    :param variable_val:
    :type variable_val:
    :param val_type:
    :type val_type:
    """
    assert not bool(re.compile('[^A-Z^0-9^_] + ').search(variable_name)), \
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
    """user_victory."""
    if not os.path.exists(world.cfg["test_result_dir"]):
        os.makedirs(world.cfg["test_result_dir"])
    shutil.copy('../doc/.victory.jpg', world.cfg["test_result_dir"] + '/celebrate_success.jpg')


# ------------------------------ FILE INSPECTION ----------------------------- #


def compare_file(local_path):
    """Compare two files: downloaded and local.

    :param local_path:
    :type local_path:
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
    """Retrieve the number of lines contained in a file.

    :param line: line (or part of file or glob pattern) being checked
    :type line:
    :param file: name of file being checked, or glob pattern potentially matching multiple files
    :type file:
    :param destination: address of server hosting the file (Default value = world.f_cfg.mgmt_address)
    :type destination:
    :return:
    :rtype:
    """
    command = 'grep "$(cat <<EOF\n'
    command += f'{line}\n'
    command += 'EOF\n'
    command += f')" {file} | wc -l'
    result = fabric_sudo_command(command, destination_host=destination, ignore_errors=True)
    assert result.succeeded, f'Command in get_line_count_in_file failed:\n{command}'
    get_line_count_in_file.file = file
    return int(result)


def get_line_count_in_log(line, log_file=None, destination=world.f_cfg.mgmt_address):
    """Retrieve the number of lines contained in a log file.

    :param line: line (or part of file or glob pattern) being checked
    :type line:
    :param log_file: name of the log file being checked. If None, default values
    :type log_file:
                     representing Kea logs are used.
    :param destination: address of server hosting the file (Default value = world.f_cfg.mgmt_address)
    :type destination:
    :return:
    :rtype:
    """
    if world.f_cfg.install_method == 'make':
        if log_file is None:
            log_file = 'kea.log'
        log_file = world.f_cfg.log_join(log_file)
        result = get_line_count_in_file(line, log_file, destination)
    else:
        if log_file is None or log_file == 'kea-dhcp-ddns.log':
            if log_file == 'kea-dhcp-ddns.log':
                if world.server_system in ['redhat', 'alpine']:
                    service_name = 'kea-dhcp-ddns'
                else:
                    service_name = 'isc-kea-dhcp-ddns-server'
            else:
                if world.server_system in ['redhat', 'alpine']:
                    service_name = f'kea-dhcp{world.proto[1]}'
                else:
                    service_name = f'isc-kea-dhcp{world.proto[1]}-server'
            if world.server_system == 'alpine':
                log_file = world.f_cfg.log_join(f'{service_name}.log')
                cmd = f'cat {log_file} |'
            else:
                log_file = "journalctl"
                cmd = f'journalctl -u {service_name} |'  # get logs of kea service
            cmd += ' grep "$(cat <<EOF\n'
            cmd += f'{line}\n'
            cmd += 'EOF\n'
            cmd += ')" | wc -l'
            result = fabric_sudo_command(cmd, destination_host=destination, ignore_errors=True)
        else:
            log_file = world.f_cfg.log_join(log_file)
            result = get_line_count_in_file(line, log_file, destination)
    get_line_count_in_log.file = log_file
    return int(result)


def file_contains_line(file, line, destination=world.f_cfg.mgmt_address):
    """file_contains_line.

    :param file:
    :type file:
    :param line:
    :type line:
    :param destination: Default value = world.f_cfg.mgmt_address)
    :type destination:
    """
    result = get_line_count_in_file(line, file, destination=destination)
    assert result > 0, f'Expected file "{get_line_count_in_file.file}" to contain line "{line}", but it does not.'


def file_contains_line_n_times(file, n, line, destination=world.f_cfg.mgmt_address):
    """file_contains_line_n_times.

    :param file:
    :type file:
    :param n:
    :type n:
    :param line:
    :type line:
    :param destination: (Default value = world.f_cfg.mgmt_address)
    :type destination:
    """
    result = get_line_count_in_file(line, file, destination=destination)
    assert result == n, f'Expected file {get_line_count_in_file.file} to contain line "{line}" a number of {n} time{"" if n == 1 else "s"}. ' \
                        f'Found {result} time{"" if result == 1 else "s"}.'


def file_doesnt_contain_line(file, line, destination=world.f_cfg.mgmt_address):
    """file_doesnt_contain_line.

    :param file:
    :type file:
    :param line:
    :type line:
    :param destination: Default value = world.f_cfg.mgmt_address)
    :type destination:
    """
    result = get_line_count_in_file(line, file, destination=destination)
    assert result == 0, f'Expected file "{get_line_count_in_file.file}" to not contain line "{line}".' \
                        f'Found {result} time{"" if result == 1 else "s"}.'


def lease_file_contains(line, destination=world.f_cfg.mgmt_address):
    """lease_file_contains.

    :param line:
    :type line:
    :param destination: (Default value = world.f_cfg.mgmt_address)
    :type destination:
    """
    file_contains_line(world.f_cfg.get_leases_path(), line, destination=destination)


def lease_file_doesnt_contain(line, destination=world.f_cfg.mgmt_address):
    """lease_file_doesnt_contain.

    :param line:
    :type line:
    :param destination: (Default value = world.f_cfg.mgmt_address)
    :type destination:
    """
    file_doesnt_contain_line(world.f_cfg.get_leases_path(), line, destination=destination)


def log_contains(line, log_file=None, destination=world.f_cfg.mgmt_address):
    """log_contains.

    :param line:
    :type line:
    :param log_file: (Default value = None)
    :type log_file:
    :param destination: Default value = world.f_cfg.mgmt_address)
    :type destination:
    """
    result = get_line_count_in_log(line, log_file, destination=destination)
    assert result > 0, f'Expected log file {get_line_count_in_log.file} to contain line "{line}", but it does not.'


def log_contains_n_times(line, n, log_file=None, destination=world.f_cfg.mgmt_address):
    """log_contains_n_times.

    :param line:
    :type line:
    :param n:
    :type n:
    :param log_file: Default value = None)
    :type log_file:
    :param destination: Default value = world.f_cfg.mgmt_address)
    :type destination:
    """
    result = get_line_count_in_log(line, log_file, destination=destination)
    assert result == n, f'Expected log file {get_line_count_in_log.file} to contain line "{line}" a number of {n} time{"" if n == 1 else "s"}. ' \
                        f'Found {result} time{"" if result == 1 else "s"}.'


def log_doesnt_contain(line, log_file=None, destination=world.f_cfg.mgmt_address):
    """log_doesnt_contain.

    :param line:
    :type line:
    :param log_file: (Default value = None)
    :type log_file:
    :param destination: Default value = world.f_cfg.mgmt_address)
    :type destination:
    """
    result = get_line_count_in_log(line, log_file, destination=destination)
    assert result == 0, f'Expected log file {get_line_count_in_log.file} to not contain line "{line}".' \
                        f'Found {result} time{"" if result == 1 else "s"}.'


def wait_for_message_in_log(line, count=1, timeout=4, log_file=None, destination=world.f_cfg.mgmt_address):
    """Wait until a line appears a certain number of times in a file.

    :param line: line (or part of file or glob pattern) being checked
    :type line:
    :param count: number of matching lines to wait for (Default value = 1)
    :type count:
    :param timeout: time to wait for in seconds (Default value = 4)
    :type timeout:
    :param log_file: name of file being checked, or glob pattern potentially matching multiple files.
        Default is None i.e. default log file.
    :type log_file:
    :param destination: address of server hosting the file (Default value = world.f_cfg.mgmt_address)
    :type destination:
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
                         db_user=world.f_cfg.db_user, db_passwd=world.f_cfg.db_passwd, destination=world.f_cfg.mgmt_address):
    """remove_from_db_table.

    :param table_name:
    :type table_name:
    :param db_type:
    :type db_type:
    :param db_name: Default value = world.f_cfg.db_name)
    :type db_name:
    :param db_user: Default value = world.f_cfg.db_user)
    :type db_user:
    :param db_passwd: Default value = world.f_cfg.db_passwd)
    :type db_passwd:
    :param destination: Default value = world.f_cfg.mgmt_address)
    :type destination:
    """
    if db_type in ["mysql", "MySQL"]:
        # that is tmp solution - just clearing not saving.
        command = 'mysql -u {db_user} -p{db_passwd} -e "delete from {table_name}" {db_name}'.format(**locals())
        fabric_run_command(command, destination_host=destination)
    elif db_type in ["postgresql", "PostgreSQL"]:
        command = 'PGPASSWORD={db_passwd} psql -h localhost -U {db_user} -d {db_name} -c "delete from {table_name}"'.format(**locals())
        fabric_run_command(command, destination_host=destination)
    else:
        assert False, "db type {db_type} not recognized/not supported".format(**locals())


def db_table_record_count(table_name, db_type, line="", grep_cmd=None, db_name=world.f_cfg.db_name,
                          db_user=world.f_cfg.db_user, db_passwd=world.f_cfg.db_passwd,
                          destination=world.f_cfg.mgmt_address, lease=None):
    """db_table_record_count.

    :param table_name:
    :type table_name:
    :param db_type:
    :type db_type:
    :param line: Default value = "")
    :type line:
    :param grep_cmd: Default value = None)
    :type grep_cmd:
    :param db_name: Default value = world.f_cfg.db_name)
    :type db_name:
    :param db_user: Default value = world.f_cfg.db_user)
    :type db_user:
    :param db_passwd: Default value = world.f_cfg.db_passwd)
    :type db_passwd:
    :param destination: Default value = world.f_cfg.mgmt_address)
    :type destination:
    :param lease: Default value = None)
    :type lease:
    :return:
    :rtype:
    """
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
    """db_table_contains_line.

    :param table_name:
    :type table_name:
    :param db_type:
    :type db_type:
    :param line: Default value = "")
    :type line:
    :param grep_cmd: Default value = None)
    :type grep_cmd:
    :param expect: Default value = True)
    :type expect:
    :param db_name: Default value = world.f_cfg.db_name)
    :type db_name:
    :param db_user: Default value = world.f_cfg.db_user)
    :type db_user:
    :param db_passwd: Default value = world.f_cfg.db_passwd)
    :type db_passwd:
    :param destination: Default value = world.f_cfg.mgmt_address)
    :type destination:
    :param lease: Default value = None)
    :type lease:
    """
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
    """db_table_contains_line_n_times.

    :param table_name:
    :type table_name:
    :param db_type:
    :type db_type:
    :param n:
    :type n:
    :param line: (Default value = "")
    :type line:
    :param grep_cmd: Default value = None)
    :type grep_cmd:
    :param db_name: Default value = world.f_cfg.db_name)
    :type db_name:
    :param db_user: Default value = world.f_cfg.db_user)
    :type db_user:
    :param db_passwd: Default value = world.f_cfg.db_passwd)
    :type db_passwd:
    :param destination: Default value = world.f_cfg.mgmt_address)
    :type destination:
    """
    result = db_table_record_count(table_name, db_type, line,
                                   grep_cmd, db_name, db_user, db_passwd,
                                   destination)
    assert result == n, f'Expected {db_type} database table {table_name} to contain line "{line}" a number of {n} time{"" if n == 1 else "s"}. ' \
                        f'Found {result} time{"" if result == 1 else "s"}.'


def lease_dump(backend, db_name=world.f_cfg.db_name, db_user=world.f_cfg.db_user,
               db_passwd=world.f_cfg.db_passwd, destination_address=world.f_cfg.mgmt_address,
               out="/tmp/lease_dump.csv"):
    """Dump database to CSV file performing kea-admin lease-dump command on server.

    :param backend: Select database backend: mysql, pgsql
    :type backend: Select database backend:
    :param db_name: specifies a database name to connect to (Default value = world.f_cfg.db_name)
    :type db_name:
    :param db_user: specifies username when connecting to a database (Default value = world.f_cfg.db_user)
    :type db_user:
    :param db_passwd: specifies a password for the database connection (Default value = world.f_cfg.db_passwd)
    :type db_passwd:
    :param destination_address: specifies server address for management (Default value = world.f_cfg.mgmt_address)
    :type destination_address:
    :param out: output file path (Default value = "/tmp/lease_dump.csv")
    :type out:
    :return: output file path on server
    :rtype:
    """
    path = os.path.join(world.f_cfg.software_install_path, 'sbin/kea-admin')

    backend = 'pgsql' if backend == "postgresql" else backend

    remove_file_from_server(out, dest=destination_address)
    execute_shell_cmd(f"{path} lease-dump {backend} -u {db_user} -p {db_passwd} "
                      f"-n {db_name} -{world.f_cfg.proto[1]} -o {out}", dest=destination_address)
    return out


def lease_upload(backend, leases_file, db_name=world.f_cfg.db_name, db_user=world.f_cfg.db_user,
                 db_passwd=world.f_cfg.db_passwd, destination_address=world.f_cfg.mgmt_address):
    """Upload CSV file to database performing kea-admin lease-upload command on server.

    :param backend: Select database backend: mysql, pgsql
    :type backend: Select database backend:
    :param leases_file: input file path
    :type leases_file:
    :param db_name: specifies a database name to connect to (Default value = world.f_cfg.db_name)
    :type db_name:
    :param db_user: specifies username when connecting to a database (Default value = world.f_cfg.db_user)
    :type db_user:
    :param db_passwd: specifies a password for the database connection (Default value = world.f_cfg.db_passwd)
    :type db_passwd:
    :param destination_address: specifies server address for management (Default value = world.f_cfg.mgmt_address)
    :type destination_address:
    :return: shell operation result
    :rtype:
    """
    path = os.path.join(world.f_cfg.software_install_path, 'sbin/kea-admin')

    backend = 'pgsql' if backend == "postgresql" else backend

    result = execute_shell_cmd(f"{path} lease-upload {backend} -u {db_user} -p {db_passwd} "
                               f"-n {db_name} -{world.f_cfg.proto[1]} -i {leases_file}",
                               dest=destination_address)
    return result


def change_network_variables(value_name, value):
    """Change network variables.

    :param value_name:
    :type value_name:
    :param value:
    :type value:
    """
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
    """Execute shell command.

    :param path:
    :type path:
    :param save_results: (Default value = True)
    :type save_results:
    :param dest: Default value = world.f_cfg.mgmt_address)
    :type dest:
    :param exp_failed: Default value = False)
    :type exp_failed:
    :return:
    :rtype:
    """
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
        assert result.failed
    else:
        assert result.succeeded

    return result


def test_define_value(*args):
    """Substitute variable references in a string.

    Designed to use in test scenarios values from init_all.py file. To makes them even more portable
    Bash like define variables: $(variable_name)
    You can use steps like:
    - Client download file from server stored in: $(SERVER_SETUP_DIR)/other_dir/my_file
    or
    - Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)/my_file
    $ sign is very important without it Forge wont find variable in init_all.
    You can use any variable form init_all in that way.

    :param args:
    :type args:
    :return:
    :rtype:
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
    fields instead of one big string.

    :param cfg:
    :type cfg:
    """
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
    """Process control response.

    :param response:
    :type response:
    :param exp_result:
    :type exp_result:
    :return:
    :rtype:
    """
    world.control_channel = response
    try:
        result = json.loads(response)
        if world.f_cfg.forge_verbose:
            log.info(json.dumps(result, sort_keys=True, indent=2, separators=(',', ': ')))
    except BaseException:  # pylint: disable=broad-exception-caught
        log.exception('Problem with parsing json:\n"%s"', str(response))
        result = response

    if exp_result is not None:
        if isinstance(result, dict):
            res = result
        elif isinstance(result, list):
            res = result[0]
        else:
            assert False, 'result is incorrectly formatted'
        assert 'result' in res and res['result'] == exp_result, \
            f'unexpected result: {res["result"]} we were expecting {exp_result}'
        if res['result'] == 1:
            assert len(res) == 2 and 'text' in res

    return result


def send_ctrl_cmd_via_socket(command, socket_name=None, destination_address=world.f_cfg.mgmt_address, exp_result=0, exp_failed=False):
    """Send control command via socket.

    :param command:
    :type command:
    :param socket_name: (Default value = None)
    :type socket_name:
    :param destination_address: Default value = world.f_cfg.mgmt_address)
    :type destination_address:
    :param exp_result: Default value = 0)
    :type exp_result:
    :param exp_failed: Default value = False)
    :type exp_failed:
    :return:
    :rtype:
    """
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
    with open(world.cfg["test_result_dir"] + '/command_file', 'w') as command_file:
        command_file.write(command)
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
    """Send command to Control Agent using http or https.

    :param command: dict, command
    :type command:
    :param address: string, IP address of Control Agent
    :type address:
    :param port: int, port number on which Control Agent is listening
    :type port:
    :param exp_result: int, value of result parameter send back by Control Agent (Default value = 0)
    :type exp_result:
    :param exp_failed: boolean, set to True if we expect that message over http/https will be failed to deliver (Default value = False)
    :type exp_failed:
    :param https: boolean, True if command should be send using https (default False)
    :type https:
    :param verify: boolean, verification of certificate (Default value = None)
    :type verify:
    :param cert: tuple, contain client cert and key (Default value = None)
    :type cert:
    :param headers: dict, dictionary that should be added to message headers
    :type headers:
    :return: json struct response from Control Agent (Default value = None)
    :rtype: dict
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
        response = requests.post(addr, headers=d_headers, data=command, verify=verify, cert=cert, timeout=300)
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
    """Assert result.

    :param condition:
    :type condition:
    :param result:
    :type result:
    :param value:
    :type value:
    """
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
    """Parse JSON file.

    :param condition:
    :type condition:
    :param parameter_name:
    :type parameter_name:
    :param parameter_value:
    :type parameter_value:
    """
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
    """Strip file.

    :param file_path:
    :type file_path:
    :return:
    :rtype:
    """
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
    """Set value.

    :param env_name:
    :type env_name:
    :param env_value:
    :type env_value:
    """
    world.f_cfg.set_env_val(env_name, env_value)


def check_leases(leases_list, backend='memfile', destination=world.f_cfg.mgmt_address, should_succeed=True):
    """Check leases.

    :param leases_list:
    :type leases_list:
    :param backend: (Default value = 'memfile')
    :type backend:
    :param destination: Default value = world.f_cfg.mgmt_address)
    :type destination:
    :param should_succeed: Default value = True)
    :type should_succeed:
    """
    if not isinstance(leases_list, list):
        leases_list = [leases_list]
    leases_list_copy = copy.deepcopy(leases_list)
    # TODO: make check_leases() work with the output of leaseX-get-all
    lease_file = world.f_cfg.get_leases_path()
    # if we are checking database, first lest dump leases as memfile and proceed with different path
    if backend.lower() in ['mysql', 'postgresql', 'pgsql']:
        lease_dump(backend, destination_address=destination)
        lease_file = '/tmp/lease_dump.csv'

    for lease in leases_list_copy:
        if 'server_id' in lease:
            del lease['server_id']
        cmd = f"cat {lease_file} "
        if "client_id" in lease:
            lease['client_id'] = ':'.join(lease['client_id'][i:i + 2] for i in range(0, len(lease['client_id']), 2))
        for attribute in lease:
            cmd += f"| grep {lease[attribute]} "
        cmd += "| grep -c ^"

        result = fabric_sudo_command(cmd, ignore_errors=True, destination_host=destination)
        if should_succeed:
            assert result.succeeded, "Expected lease, but it does not exist: %s" % json.dumps(lease)
        else:
            assert result.failed, "Expected lease to not exist, but it does: %s" % json.dumps(lease)
        # TODO write check if there is more than one entry of the same type


def print_leases(backend='memfile', db_name=world.f_cfg.db_name, db_user=world.f_cfg.db_user,
                 db_passwd=world.f_cfg.db_passwd, destination_address=world.f_cfg.mgmt_address):
    """print_leases Print leases to standard out.

    Not very useful in automated tests, but can speed up debugging and writing new tests.

    :param backend: type of lease backend, defaults to 'memfile'
    :type backend: str, optional
    :param db_name: database name, defaults to world.f_cfg.db_name
    :type db_name: str, optional
    :param db_user: database user name, defaults to world.f_cfg.db_user
    :type db_user: srt, optional
    :param db_passwd: database user password, defaults to world.f_cfg.db_passwd
    :type db_passwd: str, optional
    :param destination_address: destination of a node on which action will be executed, defaults to world.f_cfg.mgmt_address
    :type destination_address: str, optional
    """
    if backend.lower() in ['mysql', 'postgresql', 'pgsql']:
        lease_dump(backend, destination_address=destination_address)
        fabric_sudo_command('cat /tmp/lease_dump.csv', ignore_errors=True, destination_host=destination_address)
    else:
        fabric_sudo_command(f'cat {world.f_cfg.get_leases_path()}', ignore_errors=True, destination_host=destination_address)


def convert_address_to_hex(address):
    """Convert string address to hexadecimal representation.

    :param address:
    :type address:
    :return:
    :rtype:
    """
    address = test_define_value(address)[0]
    if '.' in address:
        return '{:02X}{:02X}{:02X}{:02X}'.format(*map(int, address.split('.')))
    if ':' in address:
        # TODO: support for abbreviated two-colon format e.g. 2001:db8::1
        return codecs.decode(address.replace(':', ''), 'hex')
    raise Exception('%s is not a valid IPv4 or IPv6 address' % address)  # pylint: disable=broad-exception-raised


def _increase_address_n(prefix):
    """Increment an IPv[46]Network address.

    :param prefix:
    :type prefix:
    :return:
    :rtype:
    """
    return prefix.network_address + \
        (1 << (prefix.network_address.max_prefixlen - int(prefix.prefixlen)))


def increase_address(address, prefix_length):
    """Increment an IPv4 or IPv6 address belonging to a network with given prefix length.

    :param address:
    :type address:
    :param prefix_length:
    :type prefix_length:
    :return:
    :rtype:
    """
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
    raise Exception('%s is not a valid IPv4 or IPv6 address' % address)  # pylint: disable=broad-exception-raised


def get_address_of_local_vm(addr: str = None):
    """Get address of an interface that is facing other address in forge setup.

    :param addr: ip address of remote system
    :type addr:
    :return: local ip address
    :rtype: str
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((addr, 80))
    a = s.getsockname()[0]
    s.close()
    return a


def create_db_dump(database: str, db_name: str = world.f_cfg.db_name,
                   db_user: str = world.f_cfg.db_user, db_password: str = world.f_cfg.db_passwd,
                   destination_address=world.f_cfg.mgmt_address, file_name=None):
    """Create database dump.

    :param database:
    :type database: str:
    :param db_name: (Default value = world.f_cfg.db_name)
    :type db_name: str:
    :param db_user: (Default value = world.f_cfg.db_user)
    :type db_user: str:
    :param db_password: (Default value = world.f_cfg.db_passwd)
    :type db_password: str:
    :param destination_address: Default value = world.f_cfg.mgmt_address)
    :type destination_address:
    :param file_name: Default value = None)
    :type file_name:
    """
    if file_name is None:
        file_name = f"/tmp/{database}_dump.sql"

    remove_file_from_server(file_name, dest=destination_address)

    if database == 'mysql':
        # create dump of database with events and procedures
        execute_shell_cmd(f"mysqldump --events --routines -u {db_user} -p'{db_password}' {db_name} > {file_name}",
                          est=destination_address)
        # replace interface and user used on setup that was used to generate dump to value later changed to interface
        # it's needed otherwise kea would not start on differently configured setup
        execute_shell_cmd(f"sed -i 's/$(SERVER_IFACE)/!serverinterface!/g' {file_name}",
                          dest=destination_address)
        execute_shell_cmd(f"sed -i 's/$(DB_USER)/!db_user!/g' {file_name}",
                          dest=destination_address)
    else:
        cmd = f'sudo -S -u postgres pg_dump {db_name} > {file_name}'
        fabric_run_command(cmd, ignore_errors=False, destination_host=destination_address)
        execute_shell_cmd(f"sed -i 's/$(DB_USER)/!db_user!/g' {file_name}", dest=destination_address)
        execute_shell_cmd(f"sed -i 's/$(SERVER_IFACE)/!serverinterface!/g' {file_name}",
                          dest=destination_address)


def restore_db_from_dump(database: str, db_name: str = None,
                         db_user: str = None,
                         db_password: str = world.f_cfg.db_passwd,
                         destination_address=world.f_cfg.mgmt_address, file_name=None):
    """Restore database from dump.

    :param database: str:
    :type database: str:
    :param db_name: str: (Default value = None)
    :type db_name: str:
    :param db_user: str: (Default value = None)
    :type db_user: str:
    :param db_password: str: (Default value = world.f_cfg.db_passwd)
    :type db_password: str:
    :param destination_address: Default value = world.f_cfg.mgmt_address)
    :type destination_address:
    :param file_name: Default value = None)
    :type file_name:
    """
    for i in [db_name, db_user, db_password, file_name]:
        assert i, "Missing required parameter"

    execute_shell_cmd(f"sed -i 's/!serverinterface!/$(SERVER_IFACE)/g' {file_name}")
    execute_shell_cmd(f"sed -i 's/!db_user!/{db_user}/g' {file_name}")
    if world.server_system == 'redhat' and database == 'mysql':
        execute_shell_cmd(f"sed -i 's/CHARSET=utf8mb4/CHARSET=latin1/g' {file_name}")

    if database == 'mysql':
        # this solves the problem: "Variable 'sql_mode' can't be set to the value of 'NO_AUTO_CREATE_USER'"
        execute_shell_cmd(f"sed -i 's/NO_AUTO_CREATE_USER,//g' {file_name}")
        cmd = f"mysql -u root -e 'GRANT SUPER ON *.* TO {db_user}@localhost;'"
        fabric_sudo_command(cmd, destination_host=destination_address)
        # recreate db content in new db
        execute_shell_cmd(f'mysql -u {db_user} -p{db_password} {db_name} < {file_name}')
    else:
        cmd = f'sudo -S -u postgres psql {db_name} < {file_name}'
        fabric_run_command(cmd, ignore_errors=False, destination_host=destination_address)
