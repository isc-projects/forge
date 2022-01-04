"""Kea leases manipulation commands"""

# pylint: disable=invalid-name,line-too-long,unused-argument

import pytest

import srv_msg
import misc
import srv_control


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_hook_v6_lease_get_by_positive(backend):
    """
    Check various options of lease6-get-by-* commands
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::2')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:2::/64',
                                                       '2001:db8:2::5-2001:db8:2::6')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # check if there are no leases
    cmd = {"command": "lease6-get-all"}
    srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    # add a lease
    cmd = {"command": "lease6-add", "arguments": {"subnet-id": 1,
                                                  "ip-address": "2001:db8:1::1",
                                                  "duid": "00:03:00:01:66:55:44:33:22:11",
                                                  "iaid": 1234,
                                                  "hostname": "four.hostname.com"}}
    srv_msg.send_ctrl_cmd(cmd)

    # check for the lease by duid
    cmd = {"command": "lease6-get-by-duid",
           "arguments": {"duid": "00:03:00:01:66:55:44:33:22:11"}}
    resp = srv_msg.send_ctrl_cmd(cmd)

    del resp["arguments"]["leases"][0]["cltt"]  # this value is dynamic so we delete it
    assert resp["arguments"]["leases"][0] == {"duid": "00:03:00:01:66:55:44:33:22:11",
                                              "fqdn-fwd": False,
                                              "fqdn-rev": False,
                                              "hostname": "four.hostname.com",
                                              "iaid": 1234,
                                              "ip-address": "2001:db8:1::1",
                                              "preferred-lft": 4000,
                                              "state": 0,
                                              "subnet-id": 1,
                                              "type": "IA_NA",
                                              "valid-lft": 4000}

    # check for the lease by hostname
    cmd = {"command": "lease6-get-by-hostname",
           "arguments": {"hostname": "four.hostname.com"}}
    resp = srv_msg.send_ctrl_cmd(cmd)

    del resp["arguments"]["leases"][0]["cltt"]  # this value is dynamic so we delete it
    assert resp["arguments"]["leases"][0] == {"duid": "00:03:00:01:66:55:44:33:22:11",
                                              "fqdn-fwd": False,
                                              "fqdn-rev": False,
                                              "hostname": "four.hostname.com",
                                              "iaid": 1234,
                                              "ip-address": "2001:db8:1::1",
                                              "preferred-lft": 4000,
                                              "state": 0,
                                              "subnet-id": 1,
                                              "type": "IA_NA",
                                              "valid-lft": 4000}

    srv_msg.check_leases({"duid": "00:03:00:01:66:55:44:33:22:11",
                          "address": "2001:db8:1::1",
                          "iaid": 1234,
                          "hostname": "four.hostname.com"},
                         backend=backend)


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_hook_v6_lease_get_by_negative():
    """
    Check various options of incorrectly build
    lease6-get-by-hostname, lease6-get-by-duid, commands.
    """
    misc.test_setup()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Testing lease6-get-by-duid
    cmd = {"command": "lease6-get-by-duid"}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "Command arguments missing or a not a map."

    cmd = {"command": "lease6-get-by-duid",
           "arguments": {}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'duid' parameter not specified"

    cmd = {"command": "lease6-get-by-duid",
           "arguments": {"duid": ""}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "Empty DUIDs are not allowed"

    cmd = {"command": "lease6-get-by-duid",
           "arguments": {"duid": " "}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "two consecutive separators (' ') specified in a decoded string ' '"

    cmd = {"command": "lease6-get-by-duid",
           "arguments": {"duid": "xxx"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'xxx' is not a valid string of hexadecimal digits"

    cmd = {"command": "lease6-get-by-duid",
           "arguments": {"duid": 2}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'duid' parameter must be a string"

    cmd = {"command": "lease6-get-by-duid",
           "arguments": {"duid": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'duid' parameter must be a string"

    # Testing lease6-get-by-hostname
    cmd = {"command": "lease6-get-by-hostname"}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "Command arguments missing or a not a map."

    cmd = {"command": "lease6-get-by-hostname",
           "arguments": {}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'hostname' parameter not specified"

    cmd = {"command": "lease6-get-by-hostname",
           "arguments": {"hostname": ""}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'hostname' parameter is empty"

    cmd = {"command": "lease6-get-by-hostname",
           "arguments": {"hostname": 2}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'hostname' parameter must be a string"

    cmd = {"command": "lease6-get-by-hostname",
           "arguments": {"hostname": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'hostname' parameter must be a string"
