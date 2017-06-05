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

from fabric.api import get, settings, put, sudo, run, hide
from fabric.exceptions import NetworkError
from features.logging_facility import get_common_logger
from lettuce.registry import world
import os


def fabric_run_command(cmd, hide_all = False):
    with settings(host_string = world.f_cfg.mgmt_address,
                  user = world.f_cfg.mgmt_username,
                  password = world.f_cfg.mgmt_password,
                  warn_only = True):
        if hide_all:
            with hide('running', 'stdout', 'stderr'):
                result = run(cmd, pty = True)
        else:
            result = run(cmd, pty = True)
    return result


def fabric_sudo_command(cmd, hide_all = False):
    with settings(host_string = world.f_cfg.mgmt_address,
                  user = world.f_cfg.mgmt_username,
                  password = world.f_cfg.mgmt_password,
                  warn_only = True):
            if hide_all:
                with hide('running', 'stdout', 'stderr'):
                    try:
                        result = sudo(cmd, pty = True)
                    except NetworkError:
                        assert False, "Network connection failed"
            else:
                try:
                    result = sudo(cmd, pty = True)
                except NetworkError:
                    assert False, "Network connection failed"
    return result


def fabric_send_file(file_local, file_remote):
    with settings(host_string = world.f_cfg.mgmt_address,
                  user = world.f_cfg.mgmt_username,
                  password = world.f_cfg.mgmt_password,
                  warn_only = True):
        with hide('running', 'stdout', 'stderr'):
            result = put(file_local, file_remote)
    return result


def fabric_download_file(remote_path, local_path):
    with settings(host_string = world.f_cfg.mgmt_address,
                  user = world.f_cfg.mgmt_username,
                  password = world.f_cfg.mgmt_password,
                  warn_only = True):
        result = get(remote_path, local_path)
    return result


def make_tarfile(output_filename, source_dir):
    import tarfile
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir)


def fabric_remove_file_command(remote_path):
    with settings(host_string = world.f_cfg.mgmt_address,
                  user = world.f_cfg.mgmt_username,
                  password = world.f_cfg.mgmt_password,
                  warn_only = True):
        result = sudo("rm -f " + remote_path)
    return result


def remove_local_file(file_local):
    try:
        os.remove(file_local)
    except OSError:
        get_common_logger().error('File %s cannot be removed' % file_local)


def save_local_file(value, value_type="string", local_flie_name=None, local_location=None):
    local_location = world.cfg["dir_name"]
    if local_flie_name == None:
        local_flie_name = "saved_file"
        # TODO: make check here for existing files with the same name

    if value_type == "string":
        tmp = open(local_location + '/' + local_flie_name, 'w')
        tmp.write(str(value))
        tmp.close()
    elif value_type == "file":
        from shutil import copy
        copy(local_flie_name, local_location + '/' + local_flie_name)


def configuration_file_name(counter, file_name):
    if os.path.isfile(world.cfg["dir_name"] + '/' + file_name):
        if counter == 1:
            file_name += str(counter)
        else:
            file_name = file_name[:18] + str(counter)
        file_name = configuration_file_name(counter + 1, file_name)
    return file_name


def archive_file_name(counter, file_name):
    if os.path.isfile(file_name + '.tar.gz'):
        if counter == 1:
            file_name += '_' + str(counter)
        else:
            file_name = file_name[0:-2] + '_' + str(counter)
        file_name = archive_file_name(counter + 1, file_name)
    return file_name


def copy_configuration_file(local_file, file_name = 'configuration_file'):
    if world.f_cfg.save_config_file:
        file_name = configuration_file_name(1, file_name)
        from shutil import copy
        if not os.path.exists(world.cfg["dir_name"]):
            os.makedirs(world.cfg["dir_name"])
        copy(local_file, world.cfg["dir_name"] + '/' + file_name)


def simple_file_layout():
    ## Make simple config file (like ISC-DHCP style) correct!
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


def json_file_layout(input=None):
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