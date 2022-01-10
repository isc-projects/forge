"""Kea add valid tests"""

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


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_hook_v4_user_context_add(backend):
    """
    Test adding and getting user-context by lease4 commands.
    @param backend: database backends as test parameter
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
    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == "Lease for address 192.168.50.5, subnet-id 1 added."

    # get the lease with lease4-get
    cmd = {"command": "lease4-get",
           "arguments": {"identifier-type": "hw-address", "identifier": "ff:01:02:03:ff:04",
                         "subnet-id": 1}}

    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == "IPv4 lease found."

    resp = resp["arguments"]  # drop unnecessary info for comparison

    # compare sorted JSON prepared on start with sorted returned one
    assert ordered(user_context) == ordered(resp["user-context"])

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
