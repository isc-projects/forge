# Copyright (C) 2022 Internet Systems Consortium.
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

# Author: Marcin Godzina

"""Kea v4 backend migration tests"""

# pylint: disable=invalid-name,line-too-long,unused-argument
import time
import pytest

import misc
import srv_msg
import srv_control
from forge_cfg import world


@pytest.mark.v4
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_v4_lease_dump(backend):
    """
    Test to check validity of "kea-admin lease-dump" command.
    Test adds leases to Kea, confirms it and then dumps database to CSV file.
    Next CSV file is checked for header and added leases.
    Server is restarted using dumped CSV as new memfile.
    Last test checks if leases are restored from dump file as memfile.
    :param backend: 2 types of leases backend kea support (without memfile)
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # add 5 leases
    for i in range(5):
        cmd = {"command": "lease4-add",
               "arguments": {"subnet-id": 1,
                             "ip-address": f"192.168.50.{i+1}",
                             "hw-address": f"1a:1b:1c:1d:1e:{i+1:02}",
                             "fqdn-fwd": True,
                             "fqdn-rev": True,
                             "valid-lft": 7777,
                             "state": 1,
                             "expire": int(time.time()) + 7000,
                             "hostname": f"my.host.some.name{i+1}",
                             "client-id": f"aa:bb:cc:dd:11:{i+1:02}",
                             "user-context": {"value": 1},
                             }}
        srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    # Check if the leases are added, and remember the cltt
    cmd = {"command": "lease4-get-all",
           "arguments": {"subnets": [1]}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    cltt = []
    all_leases = resp["arguments"]["leases"]
    all_leases = sorted(all_leases, key=lambda d: d['hw-address'])

    print(all_leases)
    for lease in all_leases:
        lease_nbr = all_leases.index(lease)
        cltt.append(all_leases[lease_nbr]["cltt"])
        del all_leases[lease_nbr]["cltt"]  # this value is dynamic so we delete it
        assert all_leases[lease_nbr] == {"subnet-id": 1,
                                         "ip-address": f"192.168.50.{lease_nbr+1}",
                                         "hw-address": f"1a:1b:1c:1d:1e:{lease_nbr+1:02}",
                                         "fqdn-fwd": True,
                                         "fqdn-rev": True,
                                         "valid-lft": 7777,
                                         "state": 1,
                                         "hostname": f"my.host.some.name{lease_nbr+1}",
                                         "client-id": f"aa:bb:cc:dd:11:{lease_nbr+1:02}",
                                         "user-context": {"value": 1},
                                         }

    # dump database to CSV file to memfile path
    dump_file_path = srv_msg.lease_dump(backend, out=world.f_cfg.get_leases_path())

    # Check CSV contents for header - column names
    srv_msg.file_contains_line(dump_file_path, None,
                               "address,hwaddr,client_id,valid_lifetime,expire,"
                               "subnet_id,fqdn_fwd,fqdn_rev,hostname,state,user_context")

    # Check CSV file for all added leases
    for i in range(5):
        line = f'192.168.50.{i+1},1a:1b:1c:1d:1e:{i+1:02},aa:bb:cc:dd:11:{i+1:02},7777,' \
               f'{cltt[i]+7777},1,1,1,my.host.some.name{i+1},1,{{ "value": 1 }}'
        srv_msg.file_contains_line(dump_file_path, None, line, singlequotes=True)

    # delete assigned lease
    for i in range(5):
        cmd = {"command": "lease4-del", "arguments": {"ip-address": f"192.168.50.{i+1}"}}
        resp = srv_msg.send_ctrl_cmd(cmd)
        assert resp["text"] == "IPv4 lease deleted."

    # Check to see if lease4-get-all will return 0 leases
    cmd = {"command": "lease4-get-all",
           "arguments": {"subnets": [1]}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert resp["text"] == "0 IPv4 lease(s) found."

    # Restart server using database dump as memfile
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.define_temporary_lease_db_backend('memfile')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'restarted')

    # Check if the pre-dump leases are present after restoring memfile from dump
    cmd = {"command": "lease4-get-all",
           "arguments": {"subnets": [1]}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    all_leases = resp["arguments"]["leases"]
    all_leases = sorted(all_leases, key=lambda d: d['hw-address'])

    for lease in all_leases:
        lease_nbr = all_leases.index(lease)
        del all_leases[lease_nbr]["cltt"]  # this value is dynamic so we delete it
        assert all_leases[lease_nbr] == {"subnet-id": 1,
                                         "ip-address": f"192.168.50.{lease_nbr+1}",
                                         "hw-address": f"1a:1b:1c:1d:1e:{lease_nbr+1:02}",
                                         "fqdn-fwd": True,
                                         "fqdn-rev": True,
                                         "valid-lft": 7777,
                                         "state": 1,
                                         "hostname": f"my.host.some.name{lease_nbr+1}",
                                         "client-id": f"aa:bb:cc:dd:11:{lease_nbr+1:02}",
                                         "user-context": {"value": 1},
                                         }


@pytest.mark.v4
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_v4_lease_upload(backend):
    """
    Test to check validity of "kea-admin lease-upload" command.
    Test adds leases to Kea memfile.
    Kea is restarted with selected backend and tested to confirm 0 leases in the database.
    Next CSV file is uploaded using kae-admin lease-upload command..
    Last test checks if leases are restored from memfile to database.
    :param backend: 2 types of leases backend kea support (without memfile)
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.define_temporary_lease_db_backend('memfile')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # add 5 leases
    for i in range(5):
        cmd = {"command": "lease4-add",
               "arguments": {"subnet-id": 1,
                             "ip-address": f"192.168.50.{i+1}",
                             "hw-address": f"1a:1b:1c:1d:1e:{i+1:02}",
                             "fqdn-fwd": True,
                             "fqdn-rev": True,
                             "valid-lft": 7777,
                             "state": 1,
                             "expire": int(time.time()) + 7000,
                             "hostname": f"my.host.some.name{i+1}",
                             "client-id": f"aa:bb:cc:dd:11:{i+1:02}",
                             "user-context": {"value": 1},
                             }}
        srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    # Restart Kea with selected database
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'restarted')

    # Check to see if lease4-get-all will return 0 leases
    cmd = {"command": "lease4-get-all",
           "arguments": {"subnets": [1]}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert resp["text"] == "0 IPv4 lease(s) found."

    # Lease-upload from memfile
    srv_msg.lease_upload(backend, world.f_cfg.get_leases_path())

    # Check if the pre restart leases are present after uploading
    cmd = {"command": "lease4-get-all",
           "arguments": {"subnets": [1]}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    all_leases = resp["arguments"]["leases"]
    all_leases = sorted(all_leases, key=lambda d: d['hw-address'])

    for lease in all_leases:
        lease_nbr = all_leases.index(lease)
        del all_leases[lease_nbr]["cltt"]  # this value is dynamic so we delete it
        assert all_leases[lease_nbr] == {"subnet-id": 1,
                                         "ip-address": f"192.168.50.{lease_nbr+1}",
                                         "hw-address": f"1a:1b:1c:1d:1e:{lease_nbr+1:02}",
                                         "fqdn-fwd": True,
                                         "fqdn-rev": True,
                                         "valid-lft": 7777,
                                         "state": 1,
                                         "hostname": f"my.host.some.name{lease_nbr+1}",
                                         "client-id": f"aa:bb:cc:dd:11:{lease_nbr+1:02}",
                                         "user-context": {"value": 1},
                                         }
