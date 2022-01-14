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

"""Kea API user context tests for v4"""

# pylint: disable=invalid-name,unused-argument
import pytest

import misc
import srv_msg
import srv_control
from forge_cfg import world
from protosupport.multi_protocol_functions import sort_container


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize("channel", ['socket', 'http'])
def test_hook_v4_lease_user_context(backend, channel):
    """
    Test adding and getting user-context by lease4 commands.
    :param backend: database backends as test parameter
    :param channel: communication channel as test parameter
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
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
                    "state": 0,
                    "subnet-id": 1,
                    "valid-lft": 4000}


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize("channel", ['socket', 'http'])
def test_hook_v4_lease_user_context_negative(channel):
    """
    Test invalid values send as user context by lease4-add and lease4-update
    :param channel: communication channel as test parameter
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
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
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_hook_v4_lease_extended_info(backend):
    """
    Test storing extended info of acquired lease and retrieving it by lease4-get
    :param backend: database backends as test parameter
    """
    misc.test_setup()
    world.dhcp_cfg['store-extended-info'] = True
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
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
                                 "state": 0,
                                 "subnet-id": 1,
                                 "user-context":
                                     {"ISC": {"relay-agent-info": "0x0106060106020603"}},
                                 "valid-lft": 4000}
