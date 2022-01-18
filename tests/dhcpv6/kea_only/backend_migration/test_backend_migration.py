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

"""Kea v6 backend migration tests"""

# pylint: disable=invalid-name,line-too-long,unused-argument
import pytest

import misc
import srv_msg
import srv_control
from forge_cfg import world
from protosupport.multi_protocol_functions import lease_dump, execute_shell_cmd


@pytest.mark.v6
@pytest.mark.parametrize('backend', ['mysql'])  # TODO add others when ready in kea
def test_v6_lease_dump_single(backend):
    """
    Test to check validity of "kea-admin lease-dump" command with one lease.
    Test adds lease to Kea, confirms it and then dumps database to CSV file.
    Next CSV file is checked for header and added lease.
    CSV file is copied as new memfile, and server is restarted using this file.
    Last test checks if the first lease is restored from dump file as memfile.
    :param backend: 3 types of leases backend kea support
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # adding lease by lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"subnet-id": 1,
                                                  "ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "iaid": 1234,
                                                  "hw-address": "1a:2b:3c:4d:5e:6f",
                                                  "preferred-lft": 7777,
                                                  "valid-lft": 11111,
                                                  "fqdn-fwd": True,
                                                  "fqdn-rev": True,
                                                  "hostname": "urania.example.org"}}
    srv_msg.send_ctrl_cmd(cmd)

    # checking if added lease is got by Control Agent
    cmd = {"command": "lease6-get",
           "arguments": {"ip-address": "2001:db8:1::1", "type": "IA_NA"}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    cltt = resp["arguments"]["cltt"]
    del resp["arguments"]["cltt"]  # this value is dynamic so we delete it
    assert resp["arguments"] == {"duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                 "fqdn-fwd": True,
                                 "fqdn-rev": True,
                                 "hostname": "urania.example.org",
                                 "hw-address": "1a:2b:3c:4d:5e:6f",
                                 "iaid": 1234,
                                 "ip-address": "2001:db8:1::1",
                                 "preferred-lft": 7777,
                                 "state": 0,
                                 "subnet-id": 1,
                                 "type": "IA_NA",
                                 "valid-lft": 11111}

    # dump database to CSV file
    dump_file_path = lease_dump(backend)

    # Check CSV contents for header - column names
    srv_msg.file_contains_line(dump_file_path, None,
                               "address,duid,valid_lifetime,expire,subnet_id,pref_lifetime,"
                               "lease_type,iaid,prefix_len,fqdn_fwd,fqdn_rev,hostname,hwaddr,"
                               "state,user_context,hwtype,hwaddr_source")

    # Check CSV file for added lease
    srv_msg.file_contains_line(dump_file_path, None,
                               '2001:db8:1::1,1a:1b:1c:1d:1e:1f:20:21:22:23:24,11111,'
                               + str(cltt + 11111) +
                               ',1,7777,0,1234,128,1,1,urania.example.org,1a:2b:3c:4d:5e:6f,0,,1,0',
                               singlequotes=True)

    # delete lease
    cmd = {"command": "lease6-del",
           "arguments": {"subnet-id": 1,
                         "identifier": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                         "identifier-type": "duid",
                         "iaid": 1234}}
    srv_msg.send_ctrl_cmd(cmd)

    # Check to see if lease6-get-all will return 0 leases
    cmd = {"command": "lease6-get-all",
           "arguments": {"subnets": [1]}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert resp["text"] == "0 IPv6 lease(s) found."

    # Copy database dump as new memfile
    execute_shell_cmd(f"cp -f '{dump_file_path}' '{world.f_cfg.get_leases_path()}'")

    # Restart server using database dump as memfile
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.define_temporary_lease_db_backend('memfile')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'restarted')

    # Check if the pre-dump lease is present after restoring memfile from dump
    cmd = {"command": "lease6-get",
           "arguments": {"ip-address": "2001:db8:1::1", "type": "IA_NA"}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    del resp["arguments"]["cltt"]  # this value is dynamic so we delete it
    assert resp["arguments"] == {"duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                 "fqdn-fwd": True,
                                 "fqdn-rev": True,
                                 "hostname": "urania.example.org",
                                 "hw-address": "1a:2b:3c:4d:5e:6f",
                                 "iaid": 1234,
                                 "ip-address": "2001:db8:1::1",
                                 "preferred-lft": 7777,
                                 "state": 0,
                                 "subnet-id": 1,
                                 "type": "IA_NA",
                                 "valid-lft": 11111}


@pytest.mark.v6
@pytest.mark.parametrize('backend', ['mysql'])  # TODO add others when ready in kea
def test_v6_lease_dump_multiple(backend):
    """
    Test to check validity of "kea-admin lease-dump" command with few leases.
    Test adds leases to Kea, confirms it and then dumps database to CSV file.
    Next CSV file is checked for header and added leases.
    :param backend: 3 types of leases backend kea support
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

    # add 5 leases
    for i in range(5):
        cmd = {"command": "lease6-add",
               "arguments": {"subnet-id": 1,
                             "ip-address": "2001:db8:1::" + f'{i + 1}',
                             "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:" + f'{i + 1:02}',
                             "iaid": 1230 + i,
                             "hw-address": "1a:2b:3c:4d:5e:6f:" + f'{i + 1:02}',
                             "preferred-lft": 7777,
                             "valid-lft": 11111,
                             "fqdn-fwd": True,
                             "fqdn-rev": True,
                             "hostname": "urania.example.org" + f'{i + 1}'}}
        srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    # Check if the leases are added to subnet 1, and remember the cltt
    cmd = {"command": "lease6-get-all",
           "arguments": {"subnets": [1]}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    cltt = []
    all_leases = resp["arguments"]["leases"]
    for lease in all_leases:
        lease_nbr = all_leases.index(lease)
        cltt.append(all_leases[lease_nbr]["cltt"])
        del all_leases[lease_nbr]["cltt"]  # this value is dynamic so we delete it
        assert all_leases[lease_nbr] == {"duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:"
                                                 + f'{lease_nbr + 1:02}',
                                         "fqdn-fwd": True,
                                         "fqdn-rev": True,
                                         "hostname": "urania.example.org" + f'{lease_nbr + 1}',
                                         "hw-address": "1a:2b:3c:4d:5e:6f:" + f'{lease_nbr + 1:02}',
                                         "iaid": 1230 + lease_nbr,
                                         "ip-address": "2001:db8:1::" + f'{lease_nbr + 1}',
                                         "preferred-lft": 7777,
                                         "state": 0,
                                         "subnet-id": 1,
                                         "type": "IA_NA",
                                         "valid-lft": 11111
                                         }

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
                                 "state": 0,
                                 "subnet-id": 2,
                                 "type": "IA_NA",
                                 "user-context": {
                                     "ISC": {
                                         "relays": [
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

    # dump database to CSV file
    dump_file_path = lease_dump(backend)

    # Check CSV contents for header - column names
    srv_msg.file_contains_line(dump_file_path, None,
                               "address,duid,valid_lifetime,expire,subnet_id,pref_lifetime,"
                               "lease_type,iaid,prefix_len,fqdn_fwd,fqdn_rev,hostname,hwaddr,"
                               "state,user_context,hwtype,hwaddr_source")

    # Check CSV file for all subnet 1 added leases
    for i in range(5):
        line = '2001:db8:1::' + f'{i + 1}' + ',1a:1b:1c:1d:1e:1f:20:21:22:23:' + f'{i + 1:02}' \
               + ',11111,' + f'{cltt[i] + 11111}' + ',1,7777,0,123' + f'{i}' \
               + ',128,1,1,urania.example.org' + f'{i + 1}' + ',1a:2b:3c:4d:5e:6f:' \
               + f'{i + 1:02}' + ',0,,1,0'
        srv_msg.file_contains_line(dump_file_path, None, line, singlequotes=True)

    # Check CSV file for subnet 2 acquired lease
    line = '2001:db8:2::1,00:03:00:01:f6:f5:f4:f3:f2:01,4000,' + f'{cltt2 + 4000}' + \
           ',2,3000,0,5678,128,0,0,,f6:f5:f4:f3:f2:01,0,{ "ISC": ' \
           '{ "relays": \\[ { "hop": 0&#x2c "link": "2001:db8:2::1000"&#x2c "options": ' \
           '"0x00120008706F727431323334"&#x2c "peer": "fe80::1" } \\] } },1,2'
    srv_msg.file_contains_line(dump_file_path, None, line, singlequotes=True)
