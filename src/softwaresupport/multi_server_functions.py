# Copyright (C) 2013-2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# pylint: disable=invalid-name,line-too-long

# Author: Wlodzimierz Wencel

import os
import logging
import tarfile
import warnings
import subprocess
from shutil import copy

from fabric.api import get, settings, put, sudo, run, hide
from fabric.exceptions import NetworkError
import fabric.state

from src.forge_cfg import world


log = logging.getLogger('forge')


def fabric_run_command(cmd, destination_host=world.f_cfg.mgmt_address,
                       user_loc=world.f_cfg.mgmt_username,
                       password_loc=world.f_cfg.mgmt_password, hide_all=False,
                       ignore_errors=False):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        with settings(host_string=destination_host, user=user_loc, password=password_loc, warn_only=ignore_errors):
            if ignore_errors:
                fabric.state.output.warnings = False
            if hide_all:
                with hide('running', 'stdout', 'stderr'):
                    result = run(cmd, pty=False)
            else:
                result = run(cmd, pty=False)
    fabric.state.output.warnings = True
    return result


def fabric_sudo_command(cmd, destination_host=world.f_cfg.mgmt_address,
                        user_loc=world.f_cfg.mgmt_username,
                        password_loc=world.f_cfg.mgmt_password, hide_all=False,
                        sudo_user=None, ignore_errors=False):
    # print("Executing command: %s" % cmd, "at %s" % destination_host)
    with settings(host_string=destination_host, user=user_loc, password=password_loc,
                  sudo_user=sudo_user, warn_only=ignore_errors):
        try:
            if ignore_errors:
                fabric.state.output.warnings = False
            if hide_all:
                with hide('running', 'stdout', 'stderr'):
                    result = sudo(cmd, pty=world.f_cfg.fabric_pty)
            else:
                result = sudo(cmd, pty=world.f_cfg.fabric_pty)
        except NetworkError:
            fabric.state.output.warnings = True
            assert False, "Network connection failed"
    fabric.state.output.warnings = True
    return result


def fabric_send_file(file_local, file_remote,
                     destination_host=world.f_cfg.mgmt_address,
                     user_loc=world.f_cfg.mgmt_username,
                     password_loc=world.f_cfg.mgmt_password,
                     mode=None):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore",category=DeprecationWarning)
        with settings(host_string=destination_host, user=user_loc, password=password_loc, warn_only=False):
            with hide('running', 'stdout', 'stderr'):
                result = put(file_local, file_remote, use_sudo=True, mode=mode)
    return result


def fabric_download_file(remote_path, local_path,
                         destination_host=world.f_cfg.mgmt_address,
                         user_loc=world.f_cfg.mgmt_username,
                         password_loc=world.f_cfg.mgmt_password, ignore_errors=False):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        with settings(host_string=destination_host, user=user_loc, password=password_loc, warn_only=ignore_errors):
            if ignore_errors:
                fabric.state.output.warnings = False
            result = get(remote_path, local_path)
            fabric.state.output.warnings = True
    return result


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir)


def fabric_remove_file_command(remote_path,
                               destination_host=world.f_cfg.mgmt_address,
                               user_loc=world.f_cfg.mgmt_username,
                               password_loc=world.f_cfg.mgmt_password,
                               hide_all=True):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        with settings(host_string=destination_host, user=user_loc, password=password_loc, warn_only=False):
            if hide_all:
                with hide('running', 'stdout', 'stderr'):
                    result = sudo("rm -f " + remote_path)
            else:
                result = sudo("rm -f " + remote_path)
    return result


def remove_local_file(file_local):
    try:
        os.remove(file_local)
    except OSError:
        print('File %s cannot be removed' % file_local)


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
        dest_path = check_local_path_for_downloaded_files(world.cfg["test_result_dir"], file_name, destination_host)
        dest_dir = os.path.dirname(dest_path)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        copy(local_file, dest_path)


# Open file, write content and at the end of the context delete the file.
class TemporaryFile(object):
    def __init__(self, file_name, content):
        self.file_name = file_name
        self.content = content

    def __enter__(self):
        mode = 'w'
        if isinstance(self.content, bytes):
            mode = 'wb'
        with open(self.file_name, mode) as f:
            f.write(self.content)

    def __exit__(self, exception_type, exception_value, traceback):
        os.unlink(self.file_name)


def send_content(local_path, remote_path, content, subdir):
    with TemporaryFile(local_path, content):
        fabric_send_file(local_path, remote_path)
        copy_configuration_file(local_path, os.path.join(subdir, local_path))


def start_tcpdump(file_name: str = "capture.pcap", iface: str = None, port_filter: str = None,
                  auto_start_dns: bool = False, destination: str = 'local'):
    """
    Start tcpdump process
    :param file_name: name of a pcap file
    :param iface: interface on which tcpdump will listen
    :param port_filter: port filter command
    :param auto_start_dns: detect if dns traffic is being send on different interface than dhcp, if so start another
    instance of tcpdump
    :param destination: local, or an ip address of vm on which tcpdump should be started
    """

    if iface is None:
        iface = world.cfg["iface"]
    if port_filter is None:
        port_filter = f'port {world.cfg["source_port"]} or port {world.cfg["destination_port"]} or port 53'

    cmd = f"sudo {os.path.join(world.f_cfg.tcpdump_path, 'tcpdump')}"
    cmd += f' -U -w {os.path.join(world.cfg["test_result_dir"], file_name)} -s 65535 -i {iface} {port_filter}'
    print(cmd)
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if world.dns_enable and world.f_cfg.dns_iface != iface and auto_start_dns:
        # if dns traffic goes through different interface start another tcpdump
        start_tcpdump(file_name='capture_dns.pcap', iface=world.f_cfg.dns_iface, port_filter='port 53',
                      auto_start_dns=False)


def stop_tcpdump(location='local'):
    """
    Kill all instances of tcpdump
    :param location:
    """
    args = ["sudo pkill tcpdump"]
    subprocess.call(args, shell=True)
