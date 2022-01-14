# Copyright (C) 2013-2022 Internet Systems Consortium.
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

"""Kea API user context tests for v6"""

# pylint: disable=invalid-name,unused-argument
import pytest

import misc
import srv_msg
import srv_control
from forge_cfg import world


def _ordered(obj):
    """
    Helper function to sort JSON for ease of comparison.
    :param obj: json as dictionary
    :return: Sorted json dictionary
    """
    if isinstance(obj, dict):
        return sorted((k, _ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(_ordered(x) for x in obj)
    return obj


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize("channel", ['socket', 'http'])
def test_hook_v6_lease_user_context(backend, channel):
    """
    Test adding and getting user-context by lease6 commands.
    :param backend: database backends as test parameter
    :param channel: communication channel as test parameter
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
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
    assert _ordered(user_context) == _ordered(resp["user-context"])

    del resp["user-context"]  # We already checked it
    del resp["cltt"]  # this value is dynamic

    # check the rest of the response
    assert resp == {"duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                    "fqdn-fwd": False,
                    "fqdn-rev": False,
                    "hostname": "",
                    "iaid": 1234,
                    "ip-address": "2001:db8:1::1",
                    "preferred-lft": 4000,
                    "state": 0,
                    "subnet-id": 1,
                    "type": "IA_NA",
                    "valid-lft": 4000}


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize("channel", ['socket', 'http'])
def test_hook_v6_lease_user_context_negative(channel):
    """
    Test invalid values send as user context by lease6-add and lease4-update
    :param channel: communication channel as test parameter
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
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
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_hook_v6_lease_extended_info(backend):
    """
    Test storing extended info of acquired lease and retrieving it by lease6-get
    Communication with Kea is made by relayed messages to trigger storing relay info in user-context
    :param backend: database backends as test parameter
    """
    misc.test_setup()
    world.dhcp_cfg['store-extended-info'] = True
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
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
                                 "preferred-lft": 3000,
                                 "state": 0,
                                 "subnet-id": 1,
                                 "type": "IA_NA",
                                 "user-context": {
                                    "ISC": {
                                            "relays": [
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
