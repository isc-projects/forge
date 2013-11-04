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

from _pyio import open
from fabric.context_managers import settings
from fabric.operations import get
from lettuce.registry import world
from locale import str
import os
import sys

# Author: Wlodzimierz Wencel

def test_pause(step):
    """
    Pause the test for any reason. Press any key to continue. 
    """
    def getch():
        import tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
    getch()


def copy_file_from_server(step, remote_path):
    try:
        with settings(host_string = world.cfg["mgmt_addr"], user = world.cfg["mgmt_user"], password = world.cfg["mgmt_pass"]):
            get(remote_path, world.cfg["dir_name"]+'/downloaded_file')
    except:
        assert False, 'No remote file %s' %remote_path 

def compare_file(step, local_path):
    try:
        local = open (local_path, 'r')
    except:
        assert False, 'No local file %s' %local_path
        
    downloaded = open(world.cfg["dir_name"]+'/downloaded_file', 'r')
    outcome = open (world.cfg["dir_name"]+'/file_compare', 'w')
    
    downloaded_list = downloaded.readlines()
    local_list = local.readlines()
    line_number = 1
    error_flag = True
    for i, j in zip (downloaded_list, local_list):
        if i != j:
            outcome.write('Line number: '+str(line_number)+' \n\tDownloaded file line: "'+i.rstrip('\n')+ '" and local file line: "'+j.rstrip('\n')+'"\n')
            error_flag = False
        line_number += 1
    if error_flag:
        os.remove(world.cfg["dir_name"]+'/file_compare')
    assert error_flag, 'Downloaded file is NOT the same as local. ' 