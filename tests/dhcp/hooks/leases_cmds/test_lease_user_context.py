# Copyright (C) 2022 Internet Systems Consortium.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Marcin Godzina

"""Kea API user context tests for v4"""

# pylint: disable=invalid-name
# pylint: disable=unused-argument

import pytest

from src import misc
from src import srv_msg
from src import srv_control
from src.forge_cfg import world
from src.protosupport.multi_protocol_functions import sort_container


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize("channel", ['http'])
def test_v4_lease_user_context(backend, channel):
    """
    Test adding and getting user-context by lease4 commands.
    :param backend: database backends as test parameter
    :param channel: communication channel as test parameter
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # prepare user-context JSON
    user_context = {"version": [{"number": 1, "rev": 2}, {"id": 1, "no": 2}],
                    "class": "!@#$%^&*(`)'_+=-?|\"\\\b\f\n\r\t",
                    "tre,e": {"bra,nch1": {"treehouse": 1}, "bra,nch2": 2,
                              "bra,nch3": {"leaf1": 1,
                                           "leaf2": ["vein1", "vein2"]}}}
    # add lease with user-context
    cmd = {"command": "lease4-add",
           "arguments": {"hw-address": "ff:01:02:03:ff:04", "ip-address": "192.168.50.5",
                         "user-context": user_context}}
    resp = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert resp["text"] == "Lease for address 192.168.50.5, subnet-id 1 added."

    # get the lease with lease4-get
    cmd = {"command": "lease4-get",
           "arguments": {"identifier-type": "hw-address", "identifier": "ff:01:02:03:ff:04",
                         "subnet-id": 1}}

    resp = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert resp["text"] == "IPv4 lease found."

    resp = resp["arguments"]  # drop unnecessary info for comparison

    # compare sorted JSON prepared on start with sorted returned one
    assert sort_container(user_context) == sort_container(resp["user-context"])

    del resp["user-context"]  # We already checked it
    del resp["cltt"]  # this value is dynamic

    # check the rest of the response
    assert resp == {"fqdn-fwd": False,
                    "fqdn-rev": False,
                    "hostname": "",
                    "hw-address": "ff:01:02:03:ff:04",
                    "ip-address": "192.168.50.5",
                    # "pool-id": 0, if id is 0 it's no longer returned
                    "state": 0,
                    "subnet-id": 1,
                    "valid-lft": 4000}


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize("channel", ['http'])
def test_v4_lease_user_context_negative(channel):
    """
    Test invalid values send as user context by lease4-add and lease4-update
    :param channel: communication channel as test parameter
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # add lease with invalid user-context
    cmd = {"command": "lease4-add",
           "arguments": {"hw-address": "ff:01:02:03:ff:04", "ip-address": "192.168.50.5",
                         "user-context": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd, channel=channel, exp_result=1)
    assert resp["text"] == "Invalid user context '1' is not a JSON map."

    # add lease with invalid user-context
    cmd = {"command": "lease4-add",
           "arguments": {"hw-address": "ff:01:02:03:ff:04", "ip-address": "192.168.50.5",
                         "user-context": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, channel=channel, exp_result=1)
    assert resp["text"] == "Invalid user context 'true' is not a JSON map."

    # add lease with invalid user-context
    cmd = {"command": "lease4-add",
           "arguments": {"hw-address": "ff:01:02:03:ff:04", "ip-address": "192.168.50.5",
                         "user-context": "test"}}
    resp = srv_msg.send_ctrl_cmd(cmd, channel=channel, exp_result=1)
    assert resp["text"] == "Invalid user context '\"test\"' is not a JSON map."


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_v4_lease_extended_info(backend):
    """
    Test storing extended info of acquired lease and retrieving it by lease4-get
    :param backend: database backends as test parameter
    """
    misc.test_setup()
    world.dhcp_cfg['store-extended-info'] = True
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('relay_agent_information', '0106060106020603')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')

    # get the lease with lease4-get
    cmd = {"command": "lease4-get",
           "arguments": {"identifier-type": "hw-address", "identifier": "ff:01:02:03:ff:04",
                         "subnet-id": 1}}

    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == "IPv4 lease found."

    del resp["arguments"]["cltt"]  # this value is dynamic

    # check the response
    assert resp["arguments"] == {"fqdn-fwd": False,
                                 "fqdn-rev": False,
                                 "hostname": "",
                                 "hw-address": "ff:01:02:03:ff:04",
                                 "ip-address": "192.168.50.1",
                                 # "pool-id": 0, if id is 0 it's no longer returned
                                 "state": 0,
                                 "subnet-id": 1,
                                 "user-context": {
                                   "ISC": {
                                     "relay-agent-info": {
                                       "sub-options": "0x0106060106020603"
                                     }
                                   }
                                 },
                                 "valid-lft": 4000}


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize("channel", ['http'])
def test_v6_lease_user_context(backend, channel):
    """
    Test adding and getting user-context by lease6 commands.
    :param backend: database backends as test parameter
    :param channel: communication channel as test parameter
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # prepare user-context JSON
    user_context = {"version": [{"number": 1, "rev": 2}, {"id": 1, "no": 2}],
                    "class": "!@#$%^&*(`)'_+=-?|\"\\\b\f\n\r\t",
                    "tre,e": {"bra,nch1": {"treehouse": 1}, "bra,nch2": 2,
                              "bra,nch3": {"leaf1": 1,
                                           "leaf2": ["vein1", "vein2"]}}}
    # add lease with user-context
    cmd = {"command": "lease6-add",
           "arguments": {"subnet-id": 1,
                         "ip-address": "2001:db8:1::1",
                         "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                         "iaid": 1234,
                         "user-context": user_context}}
    resp = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert resp["text"] == "Lease for address 2001:db8:1::1, subnet-id 1 added."

    # get the lease with lease6-get
    cmd = {"command": "lease6-get",
           "arguments": {"subnet-id": 1,
                         "ip-address": "2001:db8:1::1",
                         "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                         "iaid": 1234}}

    resp = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert resp["text"] == "IPv6 lease found."

    resp = resp["arguments"]  # drop unnecessary info for comparison

    # compare sorted JSON prepared on start with sorted returned one
    assert sort_container(user_context) == sort_container(resp["user-context"])

    del resp["user-context"]  # We already checked it
    del resp["cltt"]  # this value is dynamic

    # check the rest of the response
    assert resp == {"duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                    "fqdn-fwd": False,
                    "fqdn-rev": False,
                    "hostname": "",
                    "iaid": 1234,
                    "ip-address": "2001:db8:1::1",
                    # "pool-id": 0, if id is 0 it's no longer returned
                    "preferred-lft": 4000,
                    "state": 0,
                    "subnet-id": 1,
                    "type": "IA_NA",
                    "valid-lft": 4000}


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize("channel", ['http'])
def test_v6_lease_user_context_negative(channel):
    """
    Test invalid values send as user context by lease6-add and lease4-update
    :param channel: communication channel as test parameter
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # add lease with invalid user-context
    cmd = {"command": "lease6-add",
           "arguments": {"subnet-id": 1,
                         "ip-address": "2001:db8:1::1",
                         "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                         "iaid": 1234,
                         "user-context": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd, channel=channel, exp_result=1)
    assert resp["text"] == "Invalid user context '1' is not a JSON map."

    # add lease with invalid user-context
    cmd = {"command": "lease6-add",
           "arguments": {"subnet-id": 1,
                         "ip-address": "2001:db8:1::1",
                         "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                         "iaid": 1234,
                         "user-context": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, channel=channel, exp_result=1)
    assert resp["text"] == "Invalid user context 'true' is not a JSON map."

    # add lease with invalid user-context
    cmd = {"command": "lease6-add",
           "arguments": {"subnet-id": 1,
                         "ip-address": "2001:db8:1::1",
                         "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                         "iaid": 1234,
                         "user-context": "test"}}
    resp = srv_msg.send_ctrl_cmd(cmd, channel=channel, exp_result=1)
    assert resp["text"] == "Invalid user context '\"test\"' is not a JSON map."


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_v6_lease_extended_info(backend):
    """
    Test storing extended info of acquired lease and retrieving it by lease6-get
    Communication with Kea is made by relayed messages to trigger storing relay info in user-context
    :param backend: database backends as test parameter
    """
    misc.test_setup()
    world.dhcp_cfg['store-extended-info'] = True
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # Prepare Solicit message
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value('Client', 'ia_id', 1234)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    # Encapsulate the solicit in a relay forward message.
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8:1::1000')
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
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8:1::1000')
    srv_msg.client_sets_value('RelayAgent', 'peeraddr', 'fe80::1')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    # Send message and expect a relay reply.
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')

    # get the lease with lease6-get
    cmd = {"command": "lease6-get",
           "arguments": {"subnet-id": 1,
                         "ip-address": "2001:db8:1::1",
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
                                 "iaid": 1234,
                                 "ip-address": "2001:db8:1::1",
                                 # "pool-id": 0, if id is 0 it's no longer returned
                                 "preferred-lft": 3000,
                                 "state": 0,
                                 "subnet-id": 1,
                                 "type": "IA_NA",
                                 "user-context": {
                                    "ISC": {
                                        "relay-info": [
                                                        {
                                                         "hop": 0,
                                                         "link": "2001:db8:1::1000",
                                                         "options": "0x00120008706F727431323334",
                                                         "peer": "fe80::1"
                                                        }
                                                      ]
                                            }
                                 },
                                 "valid-lft": 4000}
