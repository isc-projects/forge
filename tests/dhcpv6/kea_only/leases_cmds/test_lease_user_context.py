"""Kea API user context tests for v4"""

# pylint: disable=invalid-name,unused-argument
import pytest

import misc
import srv_msg
import srv_control


def ordered(obj):
    """
    Helper function to sort JSON for ease of comparison.
    :param obj: json as dictionary
    :return: Sorted json dictionary
    """
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
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
    assert ordered(user_context) == ordered(resp["user-context"])

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
