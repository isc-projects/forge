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

from fabric.api import get, settings, put, sudo, run, hide
from features.init_all import MGMT_ADDRESS, MGMT_USERNAME, MGMT_PASSWORD, SAVE_CONFIG_FILE
from features.logging_facility import get_common_logger
from lettuce.registry import world
import os

#from features.serversupport.multi_server_functions import fabric_run_command, fabric_sudo_command,\
# fabric_send_file,fabric_download_file,fabric_remove_file_command,remove_local_file

def fabric_run_command(cmd):
    with settings(host_string = MGMT_ADDRESS, user = MGMT_USERNAME, password = MGMT_PASSWORD, warn_only = True):
        result = run(cmd, pty = True)
    return result

def fabric_sudo_command(cmd):
    with settings(host_string = MGMT_ADDRESS, user = MGMT_USERNAME, password = MGMT_PASSWORD, warn_only = True):
        result = sudo(cmd, pty = True)
    return result
        
def fabric_send_file(file_local, file_remote):
    with settings(host_string = MGMT_ADDRESS, user = MGMT_USERNAME, password = MGMT_PASSWORD, warn_only = True):
        with hide('running', 'stdout'):
            result = put(file_local, file_remote)
    return result

def fabric_download_file(remote_path, local_path):
    with settings(host_string = MGMT_ADDRESS, user = MGMT_USERNAME, password = MGMT_PASSWORD, warn_only = True):
#         try:
        result = get(remote_path, local_path)
#         except:
#             assert False, 'No remote file %s' %remote_path
    return result

def make_tarfile(output_filename, source_dir):
    import tarfile
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir)

def fabric_remove_file_command(remote_path):
    with settings(host_string = MGMT_ADDRESS, user = MGMT_USERNAME, password = MGMT_PASSWORD, warn_only = True):
        result = run("rm -f "+remote_path)
    return result

def remove_local_file(file_local):
    try:
        os.remove(file_local)
    except OSError:
        get_common_logger().error('File %s cannot be removed' % file_local)

def configuration_file_name(counter, file_name):
    if os.path.isfile(world.cfg["dir_name"] +'/'+ file_name):
        if counter == 1:
            file_name += str(counter)
        else:
            file_name = file_name[:18] + str(counter)
        file_name = configuration_file_name(counter + 1, file_name)

    return file_name

def cpoy_configuration_file(local_file, file_name = 'configuration_file'):
    if SAVE_CONFIG_FILE:
        file_name = configuration_file_name(1, file_name)
        from shutil import copy
        if not os.path.exists(world.cfg["dir_name"]):
            os.makedirs(world.cfg["dir_name"])
        copy(local_file, world.cfg["dir_name"]+'/'+file_name)
    