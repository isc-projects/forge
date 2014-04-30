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

#
# This file contain management functions for BIND 10 
# 
#

from features.init_all import SERVER_INSTALL_DIR, SLEEP_TIME_1
from features.logging_facility import get_common_logger

from multi_server_functions import fabric_sudo_command 


def kill_bind10():
    """
    Kill any running bind10 instance
    """
    get_common_logger().debug("Killing all running Bind instances")
    return fabric_sudo_command('pkill b10-*; sleep ' + str(SLEEP_TIME_1))


def start_bind10():
    """
    Start Bind10 instance
    """
    get_common_logger().debug("Starting Bind instances")

    return fabric_sudo_command('(rm nohup.out; nohup ' + SERVER_INSTALL_DIR +
                               'sbin/bind10 &); sleep ' + str(SLEEP_TIME_1))