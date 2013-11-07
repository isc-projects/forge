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

from _pyio import open
from fabric.context_managers import settings
from fabric.operations import get, put, run
from lettuce.registry import world
from locale import str
import os
import sys

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

def send_file_to_server(step, local_path, remote_path):
    with settings(host_string = world.cfg["mgmt_addr"], user = world.cfg["mgmt_user"], password = world.cfg["mgmt_pass"]):
        put(local_path, remote_path)

def remove_file_from_server(step, remote_path):
    cmd = "rm -f "+remote_path
    with settings(host_string = world.cfg["mgmt_addr"], user = world.cfg["mgmt_user"], password = world.cfg["mgmt_pass"]):
    #    with hide ('stdout','stderr'): #remove stdout if you want to see command stdout. good move to debug.
        run(cmd)

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

def compare_file(step, local_path):
    if not os.path.exists(local_path):
        assert False, 'No local file %s' %local_path
    
    outcome = open (world.cfg["dir_name"]+'/file_compare', 'w')
    
    # first remove all commented and blank lines of both files
    downloaded_stripped = strip_file(world.cfg["dir_name"]+'/downloaded_file')
    local_stripped = strip_file(local_path)

    line_number = 1
    error_flag = True
    for i, j in zip (downloaded_stripped, local_stripped):
        if i != j:
            outcome.write('Line number: '+str(line_number)+' \n\tDownloaded file line: "'+i.rstrip('\n')+ '" and local file line: "'+j.rstrip('\n')+'"\n')
            error_flag = False
        line_number += 1
    if error_flag:
        os.remove(world.cfg["dir_name"]+'/file_compare')
    assert error_flag, 'Downloaded file is NOT the same as local. Check %s/file_compare for details' %world.cfg["dir_name"] 
    
def file_includes_line(step, condition, line):
    downloaded_stripped = strip_file(world.cfg["dir_name"]+'/downloaded_file')
    if condition is not None:
        if line in downloaded_stripped:
            assert False, 'Downloaded file does contain line: "%s" But it should NOT.' %line
    else:
        if line not in downloaded_stripped:
            assert False, 'Downloaded file does NOT contain line: "%s"' %line

def beer(step):
    from shutil import copy
    copy('../doc/.beer.jpg',world.cfg["dir_name"]+'/beer_for_you.jpg')