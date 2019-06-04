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

import os
import sys
import logging
import warnings
from shutil import copy

from fabric.api import get, settings, put, sudo, run, hide
from fabric.exceptions import NetworkError

from forge_cfg import world


log = logging.getLogger('forge')


def fabric_run_command(cmd, destination_host=world.f_cfg.mgmt_address,
                       user_loc=world.f_cfg.mgmt_username,
                       password_loc=world.f_cfg.mgmt_password, hide_all=False):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore",category=DeprecationWarning)
        with settings(host_string=destination_host, user=user_loc, password=password_loc, warn_only=True):
            if hide_all:
                with hide('running', 'stdout', 'stderr'):
                    result = run(cmd, pty=False)
            else:
                result = run(cmd, pty=False)
    return result


def fabric_sudo_command(cmd, destination_host=world.f_cfg.mgmt_address,
                        user_loc=world.f_cfg.mgmt_username,
                        password_loc=world.f_cfg.mgmt_password, hide_all=False,
                        sudo_user=None):
    with settings(host_string=destination_host, user=user_loc, password=password_loc,
                  sudo_user=sudo_user, warn_only=True):
        if hide_all:
            with hide('running', 'stdout', 'stderr'):
                try:
                    result = sudo(cmd, pty=world.f_cfg.fabric_pty)
                except NetworkError:
                    assert False, "Network connection failed"
        else:
            try:
                result = sudo(cmd, pty=world.f_cfg.fabric_pty)
            except NetworkError:
                assert False, "Network connection failed"
    return result


def fabric_send_file(file_local, file_remote,
                     destination_host=world.f_cfg.mgmt_address,
                     user_loc=world.f_cfg.mgmt_username,
                     password_loc=world.f_cfg.mgmt_password):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore",category=DeprecationWarning)
        with settings(host_string=destination_host, user=user_loc, password=password_loc, warn_only=False):
            with hide('running', 'stdout', 'stderr'):
                result = put(file_local, file_remote, use_sudo=True)
    return result


def fabric_download_file(remote_path, local_path,
                         destination_host=world.f_cfg.mgmt_address,
                         user_loc=world.f_cfg.mgmt_username,
                         password_loc=world.f_cfg.mgmt_password, warn_only=False):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore",category=DeprecationWarning)
        with settings(host_string=destination_host, user=user_loc, password=password_loc, warn_only=warn_only):
            result = get(remote_path, local_path)
    return result


def make_tarfile(output_filename, source_dir):
    import tarfile
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir)


def fabric_remove_file_command(remote_path,
                               destination_host=world.f_cfg.mgmt_address,
                               user_loc=world.f_cfg.mgmt_username,
                               password_loc=world.f_cfg.mgmt_password):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore",category=DeprecationWarning)
        with settings(host_string=destination_host, user=user_loc, password=password_loc, warn_only=False):
            result = sudo("rm -f " + remote_path)
    return result


def remove_local_file(file_local):
    try:
        os.remove(file_local)
    except OSError:
        get_common_logger().error('File %s cannot be removed' % file_local)


def save_local_file(value, value_type="string", local_file_name=None, local_location=None):
    local_location = world.cfg["test_result_dir"]
    if local_file_name is None:
        local_file_name = "saved_file"
        # TODO: make check here for existing files with the same name

    if value_type == "string":
        tmp = open(os.path.join(local_location, local_file_name), 'w')
        tmp.write(str(value))
        tmp.close()
    elif value_type == "file":
        copy(local_file_name, os.path.join(local_location, local_file_name))


def generate_file_name(counter, file_name):
    if os.path.isfile(os.path.join(world.cfg["test_result_dir"], file_name)):
        if counter == 1:
            file_name += str(counter)
        else:
            file_name = file_name[:18] + str(counter)
        file_name = generate_file_name(counter + 1, file_name)
    return file_name


def archive_file_name(counter, file_name):
    if os.path.isfile(file_name + '.tar.gz'):
        if counter == 1:
            file_name += '_' + str(counter)
        else:
            file_name = file_name[0:-2] + '_' + str(counter)
        file_name = archive_file_name(counter + 1, file_name)
    return file_name


def check_local_path_for_downloaded_files(local_file_path, local_file_name, remote_address):
    """
    Function will calculate if downloaded file should be saved in main directory or in specific location in case it
    will be downloaded from remote location that is not default one
    :param local_file_path: default path
    :param local_file_name: default file name
    :param remote_address: address of remote server
    :return: changed path if remote server is not default one
    """
    if remote_address != world.f_cfg.mgmt_address:
        if not os.path.exists(os.path.join(local_file_path, remote_address)):
            os.makedirs(os.path.join(local_file_path, remote_address))
        return os.path.join(local_file_path, remote_address, local_file_name)
    return os.path.join(local_file_path, local_file_name)


def copy_configuration_file(local_file, file_name='configuration_file', destination_host=world.f_cfg.mgmt_address):
    if world.f_cfg.save_config_file:
        file_name = generate_file_name(1, file_name)
        if not os.path.exists(world.cfg["test_result_dir"]):
            os.makedirs(world.cfg["test_result_dir"])
        copy(local_file, check_local_path_for_downloaded_files(world.cfg["test_result_dir"], file_name, destination_host))


def simple_file_layout():
    # Make simple config file (like ISC-DHCP style) correct!
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
    config.close()


def locate_entry(where_we_looking, what_we_looking, n):
    start = where_we_looking.find(what_we_looking)
    while start >= 0 and n > 1:
        start = where_we_looking.find(what_we_looking, start+len(what_we_looking))
        n -= 1
    return start


def json_file_layout(userinput=None):
    # make json file more readable!
    config = open(world.cfg["cfg_file"], 'r')
    new_config = ""

    for each in config:
        new_line = each.strip()
        new_line = new_line.replace(" ", "")
        new_config += new_line
    config.close()

    real_config = ""
    counter = 0
    space = "  "
    flag = 0

    for each in new_config:
        if each == '"' and flag == 0:
            flag = 1
            real_config += each

        elif each == '"' and flag == 1:
            flag = 0
            real_config += each

        elif each == "{" and flag == 0:
            real_config += "\n" + space * counter + each
            counter += 2
            real_config += "\n" + space * counter

        elif each == "}" and flag == 0:
            counter -= 2
            real_config += "\n" + space * counter + each + "\n" + space * counter

        elif each == "," and flag == 0:
            real_config += each + "\n" + space * counter
        else:
            real_config += each

    config = open(world.cfg["cfg_file"], 'w')
    config.write(real_config)
    config.close()
