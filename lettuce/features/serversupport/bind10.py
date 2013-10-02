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

#
# This file contain management functions for BIND 10 
# 
#

from fabric.context_managers import settings, hide
from fabric.operations import run, sudo
from features.init_all import MGMT_USERNAME, MGMT_PASSWORD, SERVER_INSTALL_DIR
from features.logging_facility import get_common_logger


def kill_bind10(host):
    """
    Kill any running bind10 instance
    """
    get_common_logger().debug("Killing all running Bind instances")
    cmd = 'pkill b10-*; sleep 2'
    with settings(host_string = host, user = MGMT_USERNAME, password = MGMT_PASSWORD):
        with settings(warn_only = True):
            #with hide ('running', 'stdout'):
            sudo(cmd, pty = True)
            
def start_bind10(host):
    """
    Start Bind10 instance
    """
    get_common_logger().debug("Starting Bind instances")
    cmd = '(rm nohup.out; nohup ' + SERVER_INSTALL_DIR + 'sbin/bind10 &); sleep 2'
    with settings(host_string = host, user = MGMT_USERNAME, password = MGMT_PASSWORD):
        with settings(warn_only = True):
            #with hide ('running', 'stdout'):
            sudo(cmd, pty = True)
            