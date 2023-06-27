# Copyright (C) 2022 Internet Systems Consortium.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Marcin Godzina

"""Kea backend migration tests"""
import time
import pytest

from src import misc
from src import srv_msg
from src import srv_control

from src.forge_cfg import world
from src.protosupport.multi_protocol_functions import file_contains_line
from src.softwaresupport.multi_server_functions import fabric_sudo_command


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

    # parameters for added leases
    valid_lifetime = 7777
    expire = int(time.time()) + valid_lifetime

    # add 5 leases
    for i in range(5):
        cmd = {"command": "lease4-add",
               "arguments": {"subnet-id": 1,
                             "ip-address": f"192.168.50.{i+1}",
                             "hw-address": f"1a:1b:1c:1d:1e:{i+1:02}",
                             "fqdn-fwd": True,
                             "fqdn-rev": True,
                             "valid-lft": valid_lifetime,
                             "state": 1,
                             "expire": expire,
                             "hostname": f"my.host.some.name{i+1}",
                             "client-id": f"aa:bb:cc:dd:11:{i+1:02}",
                             "user-context": {"value": 1},
                             }}
        srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    # Check if the leases are added, and remember the cltt
    cmd = {"command": "lease4-get-all",
           "arguments": {"subnets": [1]}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    all_leases = resp["arguments"]["leases"]
    all_leases = sorted(all_leases, key=lambda d: d['hw-address'])

    for lease_nbr, lease in enumerate(all_leases):
        assert lease == {"subnet-id": 1,
                         "cltt": expire - valid_lifetime,
                         "ip-address": f"192.168.50.{lease_nbr + 1}",
                         "hw-address": f"1a:1b:1c:1d:1e:{lease_nbr + 1:02}",
                         "fqdn-fwd": True,
                         "fqdn-rev": True,
                         "valid-lft": valid_lifetime,
                         # "pool-id": 0, if id is 0 it's no longer returned
                         "state": 1,
                         "hostname": f"my.host.some.name{lease_nbr + 1}",
                         "client-id": f"aa:bb:cc:dd:11:{lease_nbr + 1:02}",
                         "user-context": {"value": 1},
                         }
        # Check if lease is in database
        srv_msg.check_leases({"address": f"192.168.50.{lease_nbr+1}"}, backend=backend)

    # dump database to CSV file to memfile path
    dump_file_path = srv_msg.lease_dump(backend, out=world.f_cfg.get_leases_path())
    fabric_sudo_command(f'chmod 666 {dump_file_path}')

    # Check CSV contents for header - column names
    file_contains_line(dump_file_path,
                       "address,hwaddr,client_id,valid_lifetime,expire,subnet_id,"
                       "fqdn_fwd,fqdn_rev,hostname,state,user_context")

    # Check CSV file for all added leases
    for i in range(5):
        line = f'192.168.50.{i+1},1a:1b:1c:1d:1e:{i+1:02},aa:bb:cc:dd:11:{i+1:02},{valid_lifetime},' \
               f'{expire},1,1,1,my.host.some.name{i+1},1,{{ "value": 1 }}'
        file_contains_line(dump_file_path, line)

    # delete assigned lease
    for i in range(5):
        cmd = {"command": "lease4-del", "arguments": {"ip-address": f"192.168.50.{i+1}"}}
        resp = srv_msg.send_ctrl_cmd(cmd)
        assert resp["text"] == "IPv4 lease deleted."
        # Check if lease is absent in database
        srv_msg.check_leases({"address": f"192.168.50.{i+1}"}, backend=backend, should_succeed=False)

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

    for lease_nbr, lease in enumerate(all_leases):
        assert lease == {"subnet-id": 1,
                         "cltt": expire - valid_lifetime,
                         "ip-address": f"192.168.50.{lease_nbr + 1}",
                         "hw-address": f"1a:1b:1c:1d:1e:{lease_nbr + 1:02}",
                         "fqdn-fwd": True,
                         "fqdn-rev": True,
                         "valid-lft": valid_lifetime,
                         # "pool-id": 0, if id is 0 it's no longer returned
                         "state": 1,
                         "hostname": f"my.host.some.name{lease_nbr + 1}",
                         "client-id": f"aa:bb:cc:dd:11:{lease_nbr + 1:02}",
                         "user-context": {"value": 1},
                         }
        # Check if lease is in database
        srv_msg.check_leases({"address": f"192.168.50.{lease_nbr + 1}"}, backend='memfile')


@pytest.mark.v4
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_v4_lease_upload(backend):
    """
    Test to check validity of "kea-admin lease-upload" command.
    Test adds leases to Kea memfile.
    Kea is restarted with selected backend and tested to confirm 0 leases in the database.
    Next CSV file is uploaded using kea-admin lease-upload command..
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

    # parameters for added leases
    valid_lifetime = 7777
    expire = int(time.time()) + valid_lifetime

    # add 5 leases
    for i in range(5):
        cmd = {"command": "lease4-add",
               "arguments": {"subnet-id": 1,
                             "ip-address": f"192.168.50.{i+1}",
                             "hw-address": f"1a:1b:1c:1d:1e:{i+1:02}",
                             "fqdn-fwd": True,
                             "fqdn-rev": True,
                             "valid-lft": valid_lifetime,
                             "state": 1,
                             "expire": expire,
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

    for lease_nbr, lease in enumerate(all_leases):
        assert lease == {"subnet-id": 1,
                         "cltt": expire - valid_lifetime,
                         "ip-address": f"192.168.50.{lease_nbr + 1}",
                         "hw-address": f"1a:1b:1c:1d:1e:{lease_nbr + 1:02}",
                         "fqdn-fwd": True,
                         "fqdn-rev": True,
                         "valid-lft": valid_lifetime,
                         # "pool-id": 0, if id is 0 it's no longer returned
                         "state": 1,
                         "hostname": f"my.host.some.name{lease_nbr + 1}",
                         "client-id": f"aa:bb:cc:dd:11:{lease_nbr + 1:02}",
                         "user-context": {"value": 1},
                         }
        # Check if lease is in database
        srv_msg.check_leases({"address": f"192.168.50.{lease_nbr+1}"}, backend=backend)


@pytest.mark.v4
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_v4_lease_upload_duplicate(backend):
    """
    Test to check validity of "kea-admin lease-upload" command.
    Test adds leases to Kea memfile, deletes them and adds again to make duplicate entries
    im memfile (journal like).
    Kea is restarted with selected backend and tested to confirm 0 leases in the database.
    Next CSV file is uploaded using kea-admin lease-upload command.
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

    # parameters for added leases
    valid_lifetime = 7777
    expire = int(time.time()) + valid_lifetime

    # add 5 leases
    for i in range(5):
        cmd = {"command": "lease4-add",
               "arguments": {"subnet-id": 1,
                             "ip-address": f"192.168.50.{i+1}",
                             "hw-address": f"1a:1b:1c:1d:1e:{i+1:02}",
                             "fqdn-fwd": True,
                             "fqdn-rev": True,
                             "valid-lft": valid_lifetime,
                             "state": 1,
                             "expire": expire,
                             "hostname": f"my.host.some.name{i+1}",
                             "client-id": f"aa:bb:cc:dd:11:{i+1:02}",
                             "user-context": {"value": 1},
                             }}
        srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    # delete 5 leases
    for i in range(5):
        cmd = {"command": "lease4-del",
               "arguments": {"ip-address": f"192.168.50.{i+1}"}}
        srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    # add the same 5 leases again to make duplicates in memfile
    for i in range(5):
        cmd = {"command": "lease4-add",
               "arguments": {"subnet-id": 1,
                             "ip-address": f"192.168.50.{i + 1}",
                             "hw-address": f"1a:1b:1c:1d:1e:{i + 1:02}",
                             "fqdn-fwd": True,
                             "fqdn-rev": True,
                             "valid-lft": valid_lifetime,
                             # "pool-id": 0, if id is 0 it's no longer returned
                             "state": 1,
                             "expire": expire,
                             "hostname": f"my.host.some.name{i + 1}",
                             "client-id": f"aa:bb:cc:dd:11:{i + 1:02}",
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

    for lease_nbr, lease in enumerate(all_leases):
        assert lease == {"subnet-id": 1,
                         "cltt": expire - valid_lifetime,
                         "ip-address": f"192.168.50.{lease_nbr + 1}",
                         "hw-address": f"1a:1b:1c:1d:1e:{lease_nbr + 1:02}",
                         "fqdn-fwd": True,
                         "fqdn-rev": True,
                         "valid-lft": valid_lifetime,
                         # "pool-id": 0, if id is 0 it's no longer returned
                         "state": 1,
                         "hostname": f"my.host.some.name{lease_nbr + 1}",
                         "client-id": f"aa:bb:cc:dd:11:{lease_nbr + 1:02}",
                         "user-context": {"value": 1},
                         }
        # Check if lease is in database
        srv_msg.check_leases({"address": f"192.168.50.{lease_nbr+1}"}, backend=backend)


@pytest.mark.v6
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_v6_lease_dump(backend):
    """
    Test to check validity of "kea-admin lease-dump" command.
    Test adds leases to Kea, confirms it and then dumps database to CSV file.
    Next CSV file is checked for header and added leases.
    Server is restarted using dumped CSV as new memfile.
    Last test checks if leases are restored from dump file as memfile.
    :param backend: 2 types of leases backend kea support (without memfile)
    """
    misc.test_setup()
    world.dhcp_cfg['store-extended-info'] = True
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::5')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:2::/64',
                                                       '2001:db8:2::1-2001:db8:2::1')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # parameters for added leases
    valid_lifetime = 7777
    expire = int(time.time()) + valid_lifetime

    # add 5 leases
    for i in range(5):
        cmd = {"command": "lease6-add",
               "arguments": {"subnet-id": 1,
                             "ip-address": f"2001:db8:1::{i+1}",
                             "duid": f"1a:1b:1c:1d:1e:1f:20:21:22:23:{i+1:02}",
                             "iaid": 1230 + i,
                             "hw-address": f"1a:2b:3c:4d:5e:6f:{i+1:02}",
                             "preferred-lft": 7777,
                             "valid-lft": valid_lifetime,
                             "expire": expire,
                             "fqdn-fwd": True,
                             "fqdn-rev": True,
                             "hostname": f"urania.example.org{i+1}"}}
        srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    # Check if the leases are added to subnet 1, and remember the cltt
    cmd = {"command": "lease6-get-all",
           "arguments": {"subnets": [1]}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    all_leases = resp["arguments"]["leases"]
    all_leases = sorted(all_leases, key=lambda d: d['duid'])

    for lease_nbr, lease in enumerate(all_leases):
        assert lease == {"duid": f"1a:1b:1c:1d:1e:1f:20:21:22:23:{lease_nbr + 1:02}",
                         "cltt": expire - valid_lifetime,
                         "fqdn-fwd": True,
                         "fqdn-rev": True,
                         "hostname": f"urania.example.org{lease_nbr + 1}",
                         "hw-address": f"1a:2b:3c:4d:5e:6f:{lease_nbr + 1:02}",
                         "iaid": 1230 + lease_nbr,
                         "ip-address": f"2001:db8:1::{lease_nbr + 1}",
                         "preferred-lft": 7777,
                         # "pool-id": 0, if id is 0 it's no longer returned
                         "state": 0,
                         "subnet-id": 1,
                         "type": "IA_NA",
                         "valid-lft": valid_lifetime
                         }
        # Check if lease is in database
        srv_msg.check_leases({"address": f"2001:db8:1::{lease_nbr+1}"}, backend=backend)

    # Get lease for subnet 2 with user-context relay info

    # Prepare Solicit message
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value('Client', 'ia_id', 5678)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    # Encapsulate the solicit in a relay forward message.
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8:2::1000')
    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'port1234')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    # Send message and expect a relay reply.
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')

    # Prepare Request message using options from Advertise
    misc.test_procedure()
    # Checking response for Relayed option and setting sender_type to 'Client' is required
    # to copy options to correct place in Request message
    # TODO Modify client_copy_option to copy options into relayed messages w\o world.sender_type.
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    world.sender_type = "Client"
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    # Encapsulate the Request in a relay forward message.
    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'port1234')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8:2::1000')
    srv_msg.client_sets_value('RelayAgent', 'peeraddr', 'fe80::1')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    # Send message and expect a relay reply.
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')

    # get the lease with lease6-get
    cmd = {"command": "lease6-get",
           "arguments": {"subnet-id": 2,
                         "ip-address": "2001:db8:2::1",
                         "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
                         "iaid": 1234}}

    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == "IPv6 lease found."
    cltt2 = resp["arguments"]["cltt"]
    del resp["arguments"]["cltt"]  # this value is dynamic
    # check the response for user-context added by Kea server.
    assert resp["arguments"] == {"duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
                                 "fqdn-fwd": False,
                                 "fqdn-rev": False,
                                 "hostname": "",
                                 "hw-address": "f6:f5:f4:f3:f2:01",
                                 "iaid": 5678,
                                 "ip-address": "2001:db8:2::1",
                                 "preferred-lft": 3000,
                                 # "pool-id": 0, if id is 0 it's no longer returned
                                 "state": 0,
                                 "subnet-id": 2,
                                 "type": "IA_NA",
                                 "user-context": {
                                     "ISC": {
                                         "relay-info": [
                                             {
                                                 "hop": 0,
                                                 "link": "2001:db8:2::1000",
                                                 "options": "0x00120008706F727431323334",
                                                 "peer": "fe80::1"
                                             }
                                         ]
                                     }
                                 },
                                 "valid-lft": 4000}
    # Check if lease is in database
    srv_msg.check_leases({"address": "2001:db8:2::1"}, backend=backend)

    # dump database to CSV file to memfile path
    dump_file_path = srv_msg.lease_dump(backend, out=world.f_cfg.get_leases_path())
    fabric_sudo_command(f'chmod 666 {dump_file_path}')

    # Check CSV contents for header - column names
    file_contains_line(dump_file_path,
                       "address,duid,valid_lifetime,expire,subnet_id,pref_lifetime,"
                       "lease_type,iaid,prefix_len,fqdn_fwd,fqdn_rev,hostname,hwaddr,"
                       "state,user_context,hwtype,hwaddr_source")

    # Check CSV file for all subnet 1 added leases
    for i in range(5):
        line = f'2001:db8:1::{i+1},1a:1b:1c:1d:1e:1f:20:21:22:23:{i+1:02},{valid_lifetime},{expire},' \
               f'1,7777,0,123{i},128,1,1,urania.example.org{i+1},1a:2b:3c:4d:5e:6f:{i+1:02},0,,1,0'
        file_contains_line(dump_file_path, line)

    # Check CSV file for subnet 2 acquired lease
    line = f'2001:db8:2::1,00:03:00:01:f6:f5:f4:f3:f2:01,4000,{cltt2+4000}' \
           f',2,3000,0,5678,128,0,0,,f6:f5:f4:f3:f2:01,0,{{ "ISC": ' \
           f'{{ "relay-info": \\[ {{ "hop": 0&#x2c "link": "2001:db8:2::1000"&#x2c "options": ' \
           f'"0x00120008706F727431323334"&#x2c "peer": "fe80::1" }} \\] }} }},1,2'
    file_contains_line(dump_file_path, line)

    # delete subnet 1 leases
    for i in range(5):
        cmd = {"command": "lease6-del",
               "arguments": {"subnet-id": 1,
                             "identifier": f"1a:1b:1c:1d:1e:1f:20:21:22:23:{i+1:02}",
                             "identifier-type": "duid",
                             "iaid": 1230 + i}}
        srv_msg.send_ctrl_cmd(cmd)

    # delete subnet 2 lease
    cmd = {"command": "lease6-del",
           "arguments": {"subnet-id": 2,
                         "ip-address": "2001:db8:2::1",
                         "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
                         "iaid": 5678}}
    srv_msg.send_ctrl_cmd(cmd)

    # Check to see if lease6-get-all will return 0 leases
    cmd = {"command": "lease6-get-all"}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert resp["text"] == "0 IPv6 lease(s) found."

    # Restart server using database dump as memfile
    misc.test_setup()
    world.dhcp_cfg['store-extended-info'] = True
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::5')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:2::/64',
                                                       '2001:db8:2::1-2001:db8:2::1')
    srv_control.define_temporary_lease_db_backend('memfile')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'restarted')

    # checking subnet 1 leases with lease6-get
    cmd = {"command": "lease6-get-all",
           "arguments": {"subnets": [1]}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    all_leases = resp["arguments"]["leases"]
    all_leases = sorted(all_leases, key=lambda d: d['duid'])

    for lease_nbr, lease in enumerate(all_leases):
        assert lease == {"duid": f"1a:1b:1c:1d:1e:1f:20:21:22:23:{lease_nbr + 1:02}",
                         "cltt": expire - valid_lifetime,
                         "fqdn-fwd": True,
                         "fqdn-rev": True,
                         "hostname": f"urania.example.org{lease_nbr + 1}",
                         "hw-address": f"1a:2b:3c:4d:5e:6f:{lease_nbr + 1:02}",
                         "iaid": 1230 + lease_nbr,
                         "ip-address": f"2001:db8:1::{lease_nbr + 1}",
                         "preferred-lft": 7777,
                         # "pool-id": 0, if id is 0 it's no longer returned
                         "state": 0,
                         "subnet-id": 1,
                         "type": "IA_NA",
                         "valid-lft": valid_lifetime
                         }
        # Check if lease is in database
        srv_msg.check_leases({"address": f"2001:db8:1::{lease_nbr+1}"}, backend='memfile')

    # check subnet 2 lease with lease6-get
    cmd = {"command": "lease6-get",
           "arguments": {"subnet-id": 2,
                         "ip-address": "2001:db8:2::1",
                         "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
                         "iaid": 5678}}
    resp = srv_msg.send_ctrl_cmd(cmd)

    assert resp["text"] == "IPv6 lease found."
    # check the response for user-context added by Kea server.
    assert resp["arguments"] == {"duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
                                 "cltt": cltt2,
                                 "fqdn-fwd": False,
                                 "fqdn-rev": False,
                                 "hostname": "",
                                 "hw-address": "f6:f5:f4:f3:f2:01",
                                 "iaid": 5678,
                                 "ip-address": "2001:db8:2::1",
                                 # "pool-id": 0, if id is 0 it's no longer returned
                                 "preferred-lft": 3000,
                                 "state": 0,
                                 "subnet-id": 2,
                                 "type": "IA_NA",
                                 "user-context": {
                                     "ISC": {
                                         "relay-info": [
                                             {
                                                 "hop": 0,
                                                 "link": "2001:db8:2::1000",
                                                 "options": "0x00120008706F727431323334",
                                                 "peer": "fe80::1"
                                             }
                                         ]
                                     }
                                 },
                                 "valid-lft": 4000}
    # Check if lease is in database
    srv_msg.check_leases({"address": "2001:db8:2::1"}, backend='memfile')


@pytest.mark.v6
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_v6_lease_upload(backend):
    """
    Test to check validity of "kea-admin lease-upload" command.
    Test adds leases to Kea memfile.
    Kea is restarted with selected backend and tested to confirm 0 leases in the database
    Next CSV file is uploaded using kea-admin lease-upload command.
    Last test checks if leases are restored from memfile to database.
    :param backend: 2 types of leases backend kea support (without memfile)
    """
    misc.test_setup()
    world.dhcp_cfg['store-extended-info'] = True
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::5')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:2::/64',
                                                       '2001:db8:2::1-2001:db8:2::1')
    srv_control.define_temporary_lease_db_backend('memfile')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # parameters for added leases
    valid_lifetime = 7777
    expire = int(time.time()) + valid_lifetime

    # add 5 leases
    for i in range(5):
        cmd = {"command": "lease6-add",
               "arguments": {"subnet-id": 1,
                             "ip-address": f"2001:db8:1::{i+1}",
                             "duid": f"1a:1b:1c:1d:1e:1f:20:21:22:23:{i+1:02}",
                             "iaid": 1230 + i,
                             "hw-address": f"1a:2b:3c:4d:5e:6f:{i+1:02}",
                             "preferred-lft": 7777,
                             "valid-lft": valid_lifetime,
                             "expire": expire,
                             "fqdn-fwd": True,
                             "fqdn-rev": True,
                             "hostname": f"urania.example.org{i+1}"}}
        srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    # Get lease for subnet 2 with user-context relay info
    # Prepare Solicit message
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value('Client', 'ia_id', 5678)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    # Encapsulate the solicit in a relay forward message.
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8:2::1000')
    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'port1234')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    # Send message and expect a relay reply.
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')

    # Prepare Request message using options from Advertise
    misc.test_procedure()
    # Checking response for Relayed option and setting sender_type to 'Client' is required
    # to copy options to correct place in Request message
    # TODO Modify client_copy_option to copy options into relayed messages w\o world.sender_type.
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    world.sender_type = "Client"
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    # Encapsulate the Request in a relay forward message.
    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'port1234')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8:2::1000')
    srv_msg.client_sets_value('RelayAgent', 'peeraddr', 'fe80::1')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    # Send message and expect a relay reply.
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')

    # Restart Kea with selected database
    misc.test_setup()
    world.dhcp_cfg['store-extended-info'] = True
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::5')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:2::/64',
                                                       '2001:db8:2::1-2001:db8:2::1')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'restarted')

    # Check to see if lease6-get-all will return 0 leases
    cmd = {"command": "lease6-get-all"}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert resp["text"] == "0 IPv6 lease(s) found."

    # Lease-upload from memfile
    srv_msg.lease_upload(backend, world.f_cfg.get_leases_path())

    # Check if the leases are restored to subnet 1
    cmd = {"command": "lease6-get-all",
           "arguments": {"subnets": [1]}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    all_leases = resp["arguments"]["leases"]
    all_leases = sorted(all_leases, key=lambda d: d['duid'])

    for lease_nbr, lease in enumerate(all_leases):
        assert lease == {"duid": f"1a:1b:1c:1d:1e:1f:20:21:22:23:{lease_nbr + 1:02}",
                         "cltt": expire - valid_lifetime,
                         "fqdn-fwd": True,
                         "fqdn-rev": True,
                         "hostname": f"urania.example.org{lease_nbr + 1}",
                         "hw-address": f"1a:2b:3c:4d:5e:6f:{lease_nbr + 1:02}",
                         "iaid": 1230 + lease_nbr,
                         "ip-address": f"2001:db8:1::{lease_nbr + 1}",
                         # "pool-id": 0, if id is 0 it's no longer returned
                         "preferred-lft": 7777,
                         "state": 0,
                         "subnet-id": 1,
                         "type": "IA_NA",
                         "valid-lft": valid_lifetime
                         }
        # Check if lease is in database
        srv_msg.check_leases({"address": f"2001:db8:1::{lease_nbr+1}"}, backend=backend)

    # get the second lease with lease6-get
    cmd = {"command": "lease6-get",
           "arguments": {"subnet-id": 2,
                         "ip-address": "2001:db8:2::1",
                         "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
                         "iaid": 1234}}

    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == "IPv6 lease found."
    del resp["arguments"]["cltt"]  # this value is dynamic
    # check the response for user-context added by Kea server.
    assert resp["arguments"] == {"duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
                                 "fqdn-fwd": False,
                                 "fqdn-rev": False,
                                 "hostname": "",
                                 "hw-address": "f6:f5:f4:f3:f2:01",
                                 "iaid": 5678,
                                 "ip-address": "2001:db8:2::1",
                                 # "pool-id": 0, if id is 0 it's no longer returned
                                 "preferred-lft": 3000,
                                 "state": 0,
                                 "subnet-id": 2,
                                 "type": "IA_NA",
                                 "user-context": {
                                     "ISC": {
                                         "relay-info": [
                                             {
                                                 "hop": 0,
                                                 "link": "2001:db8:2::1000",
                                                 "options": "0x00120008706F727431323334",
                                                 "peer": "fe80::1"
                                             }
                                         ]
                                     }
                                 },
                                 "valid-lft": 4000}
    # Check if lease is in database
    srv_msg.check_leases({"address": "2001:db8:2::1"}, backend=backend)


@pytest.mark.v6
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_v6_lease_upload_duplicate(backend):
    """
    Test to check validity of "kea-admin lease-upload" command.
    Test adds leases to Kea memfile, deletes them and adds again to make duplicate entries
    im memfile (journal like).
    Kea is restarted with selected backend and tested to confirm 0 leases in the database.
    Next CSV file is uploaded using kea-admin lease-upload command.
    Last test checks if leases are restored from memfile to database.
    :param backend: 2 types of leases backend kea support (without memfile)
    """
    misc.test_setup()
    world.dhcp_cfg['store-extended-info'] = True
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::5')
    srv_control.define_temporary_lease_db_backend('memfile')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # parameters for added leases
    valid_lifetime = 7777
    expire = int(time.time()) + valid_lifetime

    # add 5 leases
    for i in range(5):
        cmd = {"command": "lease6-add",
               "arguments": {"subnet-id": 1,
                             "ip-address": f"2001:db8:1::{i+1}",
                             "duid": f"1a:1b:1c:1d:1e:1f:20:21:22:23:{i+1:02}",
                             "iaid": 1230 + i,
                             "hw-address": f"1a:2b:3c:4d:5e:6f:{i+1:02}",
                             "preferred-lft": 7777,
                             "valid-lft": valid_lifetime,
                             "expire": expire,
                             "fqdn-fwd": True,
                             "fqdn-rev": True,
                             "hostname": f"urania.example.org{i+1}"}}
        srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    # delete 5 leases
    for i in range(5):
        cmd = {"command": "lease6-del",
               "arguments": {"subnet-id": 1,
                             "identifier": f"1a:1b:1c:1d:1e:1f:20:21:22:23:{i+1:02}",
                             "identifier-type": "duid",
                             "iaid": 1230 + i}}
        srv_msg.send_ctrl_cmd(cmd)

    # add the same 5 leases again to make duplicates in memfile
    for i in range(5):
        cmd = {"command": "lease6-add",
               "arguments": {"subnet-id": 1,
                             "ip-address": f"2001:db8:1::{i+1}",
                             "duid": f"1a:1b:1c:1d:1e:1f:20:21:22:23:{i+1:02}",
                             "iaid": 1230 + i,
                             "hw-address": f"1a:2b:3c:4d:5e:6f:{i+1:02}",
                             "preferred-lft": 7777,
                             "valid-lft": valid_lifetime,
                             "expire": expire,
                             "fqdn-fwd": True,
                             "fqdn-rev": True,
                             "hostname": f"urania.example.org{i+1}"}}
        srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    # Restart Kea with selected database
    misc.test_setup()
    world.dhcp_cfg['store-extended-info'] = True
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::5')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'restarted')

    # Check to see if lease6-get-all will return 0 leases
    cmd = {"command": "lease6-get-all",
           "arguments": {"subnets": [1]}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert resp["text"] == "0 IPv6 lease(s) found."

    # Lease-upload from memfile
    srv_msg.lease_upload(backend, world.f_cfg.get_leases_path())

    # Check if the pre restart leases are present after uploading
    cmd = {"command": "lease6-get-all",
           "arguments": {"subnets": [1]}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    all_leases = resp["arguments"]["leases"]
    all_leases = sorted(all_leases, key=lambda d: d['duid'])

    for lease_nbr, lease in enumerate(all_leases):
        assert lease == {"duid": f"1a:1b:1c:1d:1e:1f:20:21:22:23:{lease_nbr + 1:02}",
                         "cltt": expire - valid_lifetime,
                         "fqdn-fwd": True,
                         "fqdn-rev": True,
                         "hostname": f"urania.example.org{lease_nbr + 1}",
                         "hw-address": f"1a:2b:3c:4d:5e:6f:{lease_nbr + 1:02}",
                         "iaid": 1230 + lease_nbr,
                         "ip-address": f"2001:db8:1::{lease_nbr + 1}",
                         # "pool-id": 0, if id is 0 it's no longer returned
                         "preferred-lft": 7777,
                         "state": 0,
                         "subnet-id": 1,
                         "type": "IA_NA",
                         "valid-lft": valid_lifetime
                         }
        # Check if lease is in database
        srv_msg.check_leases({"address": f"2001:db8:1::{lease_nbr+1}"}, backend=backend)
