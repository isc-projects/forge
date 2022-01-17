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

"""Kea backend migration tests"""

# pylint: disable=invalid-name,line-too-long,unused-argument
import time
import pytest

import misc
import srv_msg
import srv_control
from forge_cfg import world
from protosupport.multi_protocol_functions import lease_dump, execute_shell_cmd


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.parametrize('backend', ['mysql'])
def test_v4_lease_dump_single(backend):
    """
    Test to check validity of "kea-admin lease-dump" command with one lease.
    Test adds lease to Kea, confirms it and then dumps database to CSV file.
    Next CSV file is checked for header and added lease.
    CSV file is copied as new memfile, and server is restarted using this file.
    Last test checks if the first lease is restored from dump file as memfile.
    :param backend: 3 types of leases backend kea support
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # add lease with all possible values
    cmd = {"command": "lease4-add",
           "arguments": {"subnet-id": 1,
                         "ip-address": "192.168.50.5",
                         "hw-address": "1a:1b:1c:1d:1e:1f",
                         "fqdn-fwd": True,
                         "fqdn-rev": True,
                         "valid-lft": 7777,
                         "state": 1,
                         "expire": int(time.time()) + 7000,
                         "hostname": "my.host.some.name",
                         "client-id": "aa:bb:cc:dd:11:22",
                         "user-context": {"value": 1},
                         }}
    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == "Lease for address 192.168.50.5, subnet-id 1 added."

    # Check if the lease is added, and remember the cltt
    cmd = {"command": "lease4-get",
           "arguments": {"identifier-type": "client-id", "identifier": "aa:bb:cc:dd:11:22",
                         "subnet-id": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    resp = resp["arguments"]
    cltt = resp["cltt"]
    del resp["cltt"]  # this value is dynamic
    assert resp == {"client-id": "aa:bb:cc:dd:11:22",
                    "fqdn-fwd": True,
                    "fqdn-rev": True,
                    "hostname": "my.host.some.name",
                    "hw-address": "1a:1b:1c:1d:1e:1f",
                    "ip-address": "192.168.50.5",
                    "state": 1,
                    "subnet-id": 1,
                    'user-context': {'value': 1},
                    "valid-lft": 7777}

    # dump database to CSV file
    dump_file_path = lease_dump(backend)

    # Check CSV contents for header - column names
    srv_msg.file_contains_line(dump_file_path, None,
                               "address,hwaddr,client_id,valid_lifetime,expire,"
                               "subnet_id,fqdn_fwd,fqdn_rev,hostname,state,user_context")

    # Check CSV file for added lease
    srv_msg.file_contains_line(dump_file_path, None,
                               '192.168.50.5,1a:1b:1c:1d:1e:1f,aa:bb:cc:dd:11:22,7777,'
                               + str(cltt + 7777) +
                               ',1,1,1,my.host.some.name,1,{ "value": 1 }',
                               singlequotes=True)

    # delete assigned lease
    cmd = {"command": "lease4-del", "arguments": {"ip-address": "192.168.50.5"}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == "IPv4 lease deleted."

    # Check to see if lease4-get-all will return 0 leases
    cmd = {"command": "lease4-get-all",
           "arguments": {"subnets": [1]}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert resp["text"] == "0 IPv4 lease(s) found."

    # Copy database dump as new memfile
    execute_shell_cmd(f"cp -f '{dump_file_path}' '{world.f_cfg.get_leases_path()}'")

    # Restart server using database dump as memfile
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.define_temporary_lease_db_backend('memfile')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'restarted')

    # Check if the pre-dump lease from is present after restoring memfile from dump
    cmd = {"command": "lease4-get",
           "arguments": {"identifier-type": "client-id", "identifier": "aa:bb:cc:dd:11:22",
                         "subnet-id": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    resp = resp["arguments"]
    del resp["cltt"]  # this value is dynamic
    assert resp == {"client-id": "aa:bb:cc:dd:11:22",
                    "fqdn-fwd": True,
                    "fqdn-rev": True,
                    "hostname": "my.host.some.name",
                    "hw-address": "1a:1b:1c:1d:1e:1f",
                    "ip-address": "192.168.50.5",
                    "state": 1,
                    "subnet-id": 1,
                    'user-context': {'value': 1},
                    "valid-lft": 7777}


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.parametrize('backend', ['mysql'])
def test_v4_lease_dump_multiple(backend):
    """
    Test to check validity of "kea-admin lease-dump" command with few leases.
    Test adds leases to Kea, confirms it and then dumps database to CSV file.
    Next CSV file is checked for header and added leases.
    :param backend: 3 types of leases backend kea support
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
                             "ip-address": "192.168.50." + str(i + 1),
                             "hw-address": "1a:1b:1c:1d:1e:" + f'{i + 1:02}',
                             "fqdn-fwd": True,
                             "fqdn-rev": True,
                             "valid-lft": 7777,
                             "state": 1,
                             "expire": int(time.time()) + 7000,
                             "hostname": "my.host.some.name" + str(i + 1),
                             "client-id": "aa:bb:cc:dd:11:" + f'{i + 1:02}',
                             "user-context": {"value": 1},
                             }}
        srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    # Check if the leases are added, and remember the cltt
    cmd = {"command": "lease4-get-all",
           "arguments": {"subnets": [1]}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    cltt = []
    all_leases = resp["arguments"]["leases"]
    for lease in all_leases:
        lease_nbr = all_leases.index(lease)
        cltt.append(all_leases[lease_nbr]["cltt"])
        del all_leases[lease_nbr]["cltt"]  # this value is dynamic so we delete it
        assert all_leases[lease_nbr] == {"subnet-id": 1,
                                         "ip-address": "192.168.50." + str(lease_nbr + 1),
                                         "hw-address": "1a:1b:1c:1d:1e:" + f'{lease_nbr + 1:02}',
                                         "fqdn-fwd": True,
                                         "fqdn-rev": True,
                                         "valid-lft": 7777,
                                         "state": 1,
                                         "hostname": "my.host.some.name" + str(lease_nbr + 1),
                                         "client-id": "aa:bb:cc:dd:11:" + f'{lease_nbr + 1:02}',
                                         "user-context": {"value": 1},
                                         }

    # dump database to CSV file
    dump_file_path = lease_dump(backend)

    # Check CSV contents for header - column names
    srv_msg.file_contains_line(dump_file_path, None,
                               "address,hwaddr,client_id,valid_lifetime,expire,"
                               "subnet_id,fqdn_fwd,fqdn_rev,hostname,state,user_context")

    # Check CSV file for all added leases
    for i in range(5):
        line = '192.168.50.' + f'{i + 1}' + ',1a:1b:1c:1d:1e:' + f'{i + 1:02}' + \
               ',aa:bb:cc:dd:11:' + f'{i + 1:02}' + ',7777,' + f'{cltt[i] + 7777}' + \
               ',1,1,1,my.host.some.name' + f'{i + 1}' + ',1,{ "value": 1 }'
        srv_msg.file_contains_line(dump_file_path, None, line, singlequotes=True)
