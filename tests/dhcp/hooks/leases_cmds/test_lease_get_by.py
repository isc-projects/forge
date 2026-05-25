# Copyright (C) 2022-2023 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea lease get by client-id/hostname/hw-address/state"""

import secrets
import string

import pytest

from src import misc
from src import srv_msg
from src import srv_control
from src.forge_cfg import world


def _send_cmd(cmd, extra_param=None, exp_result=0):
    cmd = {'command': cmd, 'arguments': {}}
    if isinstance(extra_param, dict):
        cmd["arguments"].update(extra_param)
    return srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result, channel='socket')


def _get_address(mac, address, cli_id=None, fqdn=None):
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', mac)
    if cli_id is not None:
        srv_msg.client_does_include_with_value('client_id', cli_id)
    if fqdn is not None:
        srv_msg.client_sets_value('Client', 'FQDN_domain_name', fqdn)
        srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
        srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', address)

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    if cli_id is not None:
        srv_msg.client_does_include_with_value('client_id', cli_id)
    srv_msg.client_does_include_with_value('requested_addr', address)
    if fqdn is not None:
        srv_msg.client_sets_value('Client', 'FQDN_domain_name', fqdn)
        srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
        srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', address)


def _del_cltt(leases):
    for lease in leases:
        del lease["cltt"]


# lease4-get-by-client-id, lease4-get-by-hostname, lease4-get-by-hw-address, lease4-get-by-state
@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_control_channel_lease4_get_by_positive(backend):
    """
    Check various options of lease4-get-by-* commands.

    :param backend: lease backend type
    :type backend: str
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.6')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.10-192.168.51.11')
    srv_control.define_lease_db_backend(backend)

    world.dhcp_cfg.update({"ddns-send-updates": False})
    world.dhcp_cfg["subnet4"][1].update({"ddns-send-updates": False})
    world.dhcp_cfg["subnet4"][0].update({"ddns-send-updates": True,
                                         "ddns-generated-prefix": "four",
                                         "ddns-qualifying-suffix": "example.com"})

    srv_control.shared_subnet('192.168.50.0/24', 0)
    srv_control.shared_subnet('192.168.51.0/24', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_unix_socket()

    srv_control.add_ddns_server('127.0.0.1', 53001)
    srv_control.add_ddns_server_connectivity_options('enable-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-send-updates', True)
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _get_address("08:08:08:08:08:08", "192.168.50.5", cli_id="00010203040506", fqdn="four.hostname.com.")
    _get_address("09:09:09:09:09:09", "192.168.50.6", cli_id="00010203040507")
    _get_address("10:10:10:10:10:10", "192.168.51.10")
    _get_address("11:11:11:11:11:11", "192.168.51.11", fqdn="xyz.com.")

    # let's get 08:08:08:08:08:08 for in a different ways
    lease_1 = {"fqdn-fwd": True,
               "fqdn-rev": True,
               "client-id": "00:01:02:03:04:05:06",
               "hostname": "four.hostname.com.",
               "hw-address": "08:08:08:08:08:08",
               "ip-address": "192.168.50.5",
               # "pool-id": 0, if id is 0 it's no longer returned
               "state": 0,
               "subnet-id": 1,
               "valid-lft": 4000}
    by_id = _send_cmd("lease4-get-by-client-id", extra_param={"client-id": "00010203040506"})
    del by_id["arguments"]["leases"][0]["cltt"]
    assert by_id["arguments"]["leases"][0] == lease_1

    by_host = _send_cmd("lease4-get-by-hostname", extra_param={"hostname": "four.hostname.com."})
    del by_host["arguments"]["leases"][0]["cltt"]
    assert by_host["arguments"]["leases"][0] == lease_1

    by_hw = _send_cmd("lease4-get-by-hw-address", extra_param={"hw-address": "08:08:08:08:08:08"})
    del by_hw["arguments"]["leases"][0]["cltt"]
    assert by_hw["arguments"]["leases"][0] == lease_1

    # let's get 09:09:09:09:09:09 for in a different ways
    lease_2 = {"fqdn-fwd": False,
               "fqdn-rev": False,
               "client-id": "00:01:02:03:04:05:07",
               "hw-address": "09:09:09:09:09:09",
               "ip-address": "192.168.50.6",
               "hostname": "",
               # "pool-id": 0, if id is 0 it's no longer returned
               "state": 0,
               "subnet-id": 1,
               "valid-lft": 4000}
    by_id = _send_cmd("lease4-get-by-client-id", extra_param={"client-id": "00010203040507"})
    del by_id["arguments"]["leases"][0]["cltt"]
    assert by_id["arguments"]["leases"][0] == lease_2

    by_hw = _send_cmd("lease4-get-by-hw-address", extra_param={"hw-address": "09:09:09:09:09:09"})
    del by_hw["arguments"]["leases"][0]["cltt"]
    assert by_hw["arguments"]["leases"][0] == lease_2

    # let's get 11:11:11:11:11:11 for in a different ways
    # THOSE TWO ARE FAILING
    lease_3 = {"fqdn-fwd": False,
               "fqdn-rev": False,
               # "client-id": "", #TODO I think it should be added kea#1391
               "hostname": "xyz.com.",
               "hw-address": "11:11:11:11:11:11",
               "ip-address": "192.168.51.11",
               # "pool-id": 0, if id is 0 it's no longer returned
               "state": 0,
               "subnet-id": 2,
               "valid-lft": 4000}
    by_host = _send_cmd("lease4-get-by-hostname", extra_param={"hostname": "xyz.com."})
    del by_host["arguments"]["leases"][0]["cltt"]
    assert by_host["arguments"]["leases"][0] == lease_3

    by_hw = _send_cmd("lease4-get-by-hw-address", extra_param={"hw-address": "11:11:11:11:11:11"})
    del by_hw["arguments"]["leases"][0]["cltt"]
    assert by_hw["arguments"]["leases"][0] == lease_3

    by_hw = _send_cmd("lease4-get-by-hw-address", extra_param={"hw-address": "11:11:11:11:11:11"})
    del by_hw["arguments"]["leases"][0]["cltt"]
    assert by_hw["arguments"]["leases"][0] == lease_3

    lease_4 = {"fqdn-fwd": False,
               "fqdn-rev": False,
               # "client-id": "", #TODO I think it should be added kea#1391
               "hw-address": "10:10:10:10:10:10",
               "ip-address": "192.168.51.10",
               "hostname": "",
               # "pool-id": 0, if id is 0 it's no longer returned
               "state": 0,
               "subnet-id": 2,
               "valid-lft": 4000}
    by_hw = _send_cmd("lease4-get-by-hw-address", extra_param={"hw-address": "10:10:10:10:10:10"})
    del by_hw["arguments"]["leases"][0]["cltt"]
    assert by_hw["arguments"]["leases"][0] == lease_4

    assigned_leases = sorted([lease_1, lease_2, lease_3, lease_4], key=lambda x: x["hw-address"])
    by_assigned = _send_cmd("lease4-get-by-state", extra_param={"state": 0}, exp_result=0)
    _del_cltt(by_assigned["arguments"]["leases"])
    by_assigned = sorted(by_assigned["arguments"]["leases"], key=lambda x: x["hw-address"])
    assert by_assigned == assigned_leases
    # state in string form
    by_assigned = _send_cmd("lease4-get-by-state", extra_param={"state": "assigned"}, exp_result=0)
    _del_cltt(by_assigned["arguments"]["leases"])
    by_assigned = sorted(by_assigned["arguments"]["leases"], key=lambda x: x["hw-address"])
    assert by_assigned == assigned_leases

    by_assigned_subnet = _send_cmd("lease4-get-by-state", extra_param={"state": 0, "subnet-id": 1}, exp_result=0)
    _del_cltt(by_assigned_subnet["arguments"]["leases"])
    by_assigned_subnet = sorted(by_assigned_subnet["arguments"]["leases"], key=lambda x: x["hw-address"])
    assert by_assigned_subnet == [lease_1, lease_2]

    # subnet id 0 == all subnets
    by_assigned_subnet = _send_cmd("lease4-get-by-state",
                                   extra_param={"state": "assigned", "subnet-id": 0}, exp_result=0)
    _del_cltt(by_assigned_subnet["arguments"]["leases"])
    by_assigned_subnet = sorted(by_assigned_subnet["arguments"]["leases"], key=lambda x: x["hw-address"])
    assert by_assigned_subnet == assigned_leases

    # Decline lease 1 and check if it's in declined state
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', lease_1["hw-address"])
    srv_msg.client_does_include_with_value('client_id', lease_1["client-id"])
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'ciaddr', '0.0.0.0')
    srv_msg.client_does_include_with_value('requested_addr', lease_1["ip-address"])
    srv_msg.client_send_msg('DECLINE')
    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()
    by_declined = _send_cmd("lease4-get-by-state", extra_param={"state": 1}, exp_result=0)
    _del_cltt(by_declined["arguments"]["leases"])
    assert by_declined["arguments"]["leases"][0] == {
                   'fqdn-fwd': False,
                   'fqdn-rev': False,
                   'hostname': '',
                   'hw-address': '',
                   'ip-address': '192.168.50.5',
                   'state': 1,
                   'subnet-id': 1,
                   'valid-lft': 86400}  # "decline-probation-period"

    _send_cmd("lease4-get-by-hw-address", extra_param={"hw-address": "11:11:12:12:13:13"}, exp_result=3)
    _send_cmd("lease4-get-by-hostname", extra_param={"hostname": "abc.com."}, exp_result=3)
    _send_cmd("lease4-get-by-client-id", extra_param={"client-id": "111111111111"}, exp_result=3)
    _send_cmd("lease4-get-by-state", extra_param={"state": 2}, exp_result=3)
    _send_cmd("lease4-get-by-state", extra_param={"state": "released", "subnet-id": 1}, exp_result=3)

    _send_cmd("lease4-get-by-hw-address", exp_result=1)
    _send_cmd("lease4-get-by-hostname", exp_result=1)
    _send_cmd("lease4-get-by-client-id", exp_result=1)


# lease4-get-by-client-id, lease4-get-by-hostname, lease4-get-by-hw-address, lease4-get-by-state
@pytest.mark.v4
@pytest.mark.controlchannel
def test_control_channel_lease4_get_by_negative():
    """
    Check various options of incorrectly build
    lease4-get-by-client-id, lease4-get-by-hostname, lease4-get-by-hw-address, commands.
    """
    misc.test_setup()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Testing lease4-get-by-client-id
    cmd = {"command": "lease4-get-by-client-id"}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "Command arguments missing or a not a map."

    cmd = {"command": "lease4-get-by-client-id",
           "arguments": {}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'client-id' parameter not specified"

    # Per RFC2132, section 9.14, client ID has a minimum length of 2.
    cmd = {"command": "lease4-get-by-client-id",
           "arguments": {"client-id": ""}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "identifier is too short (0), at least 2 is required"

    cmd = {"command": "lease4-get-by-client-id",
           "arguments": {"client-id": "00"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "identifier is too short (1), at least 2 is required"

    cmd = {"command": "lease4-get-by-client-id",
           "arguments": {"client-id": "0011"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert resp["text"] == "0 IPv4 lease(s) found."

    # RFCs do not enforce an upper length for client ID, but the
    # byte used to specify the option size byte can only go up to 255.

    # 255 should work.
    cmd = {
        "command": "lease4-get-by-client-id",
        "arguments": {
            "client-id": ''.join(secrets.choice(string.hexdigits) for _ in range(510)).lower()
        }
    }
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert resp["text"] == "0 IPv4 lease(s) found."

    # 256 should result in error.
    cmd = {
        "command": "lease4-get-by-client-id",
        "arguments": {
            "client-id": ''.join(secrets.choice(string.hexdigits) for _ in range(512)).lower()
        }
    }
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "identifier is too large (256), at most 255 is required"

    cmd = {"command": "lease4-get-by-client-id",
           "arguments": {"client-id": " "}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "two consecutive separators (' ') specified in a decoded string ' '"

    cmd = {"command": "lease4-get-by-client-id",
           "arguments": {"client-id": "xx"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'xx' is not a valid string of hexadecimal digits"

    cmd = {"command": "lease4-get-by-client-id",
           "arguments": {"client-id": 0}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'client-id' parameter must be a string"

    # Testing lease4-get-by-hostname
    cmd = {"command": "lease4-get-by-hostname"}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "Command arguments missing or a not a map."

    cmd = {"command": "lease4-get-by-hostname",
           "arguments": {}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'hostname' parameter not specified"

    cmd = {"command": "lease4-get-by-hostname",
           "arguments": {"hostname": ""}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'hostname' parameter is empty"

    cmd = {"command": "lease4-get-by-hostname",
           "arguments": {"hostname": ""}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'hostname' parameter is empty"

    cmd = {"command": "lease4-get-by-hostname",
           "arguments": {"hostname": 0}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'hostname' parameter must be a string"

    # Testing lease4-get-by-hw-address
    cmd = {"command": "lease4-get-by-hw-address"}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "Command arguments missing or a not a map."

    cmd = {"command": "lease4-get-by-hw-address",
           "arguments": {}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'hw-address' parameter not specified"

    cmd = {"command": "lease4-get-by-hw-address",
           "arguments": {"hw-address": " "}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "' ' is not a valid hexadecimal digit in decoded string ' '"

    cmd = {"command": "lease4-get-by-hw-address",
           "arguments": {"hw-address": "aaaaaaaaaaaaaaaaaaaaaaa"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid format of the decoded string 'aaaaaaaaaaaaaaaaaaaaaaa'"

    cmd = {"command": "lease4-get-by-hw-address",
           "arguments": {"hw-address": 0}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'hw-address' parameter must be a string"

    cmd = {"command": "lease4-get-by-state"}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "Command arguments missing or a not a map."

    cmd = {"command": "lease4-get-by-state",
           "arguments": {"state": {}}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'state' parameter must be a number or a string"

    resp = _send_cmd("lease4-get-by-state", extra_param={"state": "not_a_state"}, exp_result=1)
    assert resp["text"] == "'state' parameter value (not_a_state) is not recognized"
    # Inconsistent, ideally should also return 1
    resp = _send_cmd("lease4-get-by-state", extra_param={"state": 9}, exp_result=3)
    assert resp["text"] == "0 IPv4 lease(s) found with state 9."


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_v6_lease_get_by_positive(backend):
    """
    Check various options of lease6-get-by-* commands.

    :param backend: lease backend type
    :type backend: str
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::2')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:2::/64',
                                                       '2001:db8:2::5-2001:db8:2::6')
    srv_control.define_lease_db_backend(backend)
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # check if there are no leases
    cmd = {"command": "lease6-get-all"}
    srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    # add a leases
    cmd = {"command": "lease6-bulk-apply", "arguments": {
        "leases": [
            {"subnet-id": 1,
             "ip-address": "2001:db8:1::1",
             "duid": "00:03:00:01:66:55:44:33:22:11",
             "iaid": 1234,
             "hostname": "four.hostname.com",
             "hw-address": "08:08:08:08:08:08"},
            {"subnet-id": 2,
             "ip-address": "2001:db8:2::5",
             "duid": "00:04:00:01:66:55:44:33:22:11",
             "iaid": 1234,
             "hostname": "five.hostname.com",
             "hw-address": "09:09:09:09:09:09"},
        ]}}
    srv_msg.send_ctrl_cmd(cmd)

    lease1_params = {"duid": "00:03:00:01:66:55:44:33:22:11",
                     "fqdn-fwd": False,
                     "fqdn-rev": False,
                     "hostname": "four.hostname.com",
                     "iaid": 1234,
                     "ip-address": "2001:db8:1::1",
                     "hw-address": "08:08:08:08:08:08",
                     # "pool-id": 0, if id is 0 it's no longer returned
                     "preferred-lft": 4000,
                     "state": 0,
                     "subnet-id": 1,
                     "type": "IA_NA",
                     "valid-lft": 4000}
    lease2_params = {"duid": "00:04:00:01:66:55:44:33:22:11",
                     "fqdn-fwd": False,
                     "fqdn-rev": False,
                     "hostname": "five.hostname.com",
                     "iaid": 1234,
                     "ip-address": "2001:db8:2::5",
                     "hw-address": "09:09:09:09:09:09",
                     # "pool-id": 0, if id is 0 it's no longer returned
                     "preferred-lft": 4000,
                     "state": 0,
                     "subnet-id": 2,
                     "type": "IA_NA",
                     "valid-lft": 4000}
    leases_params = [lease1_params, lease2_params]

    # check for the lease by duid
    cmd = {"command": "lease6-get-by-duid",
           "arguments": {"duid": "00:03:00:01:66:55:44:33:22:11"}}
    resp = srv_msg.send_ctrl_cmd(cmd)

    del resp["arguments"]["leases"][0]["cltt"]  # this value is dynamic so we delete it
    assert resp["arguments"]["leases"][0] == lease1_params

    # check for the lease by hostname
    cmd = {"command": "lease6-get-by-hostname",
           "arguments": {"hostname": "four.hostname.com"}}
    resp = srv_msg.send_ctrl_cmd(cmd)

    del resp["arguments"]["leases"][0]["cltt"]  # this value is dynamic so we delete it
    assert resp["arguments"]["leases"][0] == lease1_params

    # check for the lease by hw-address
    cmd = {"command": "lease6-get-by-hw-address",
           "arguments": {"hw-address": "08:08:08:08:08:08"}}
    resp = srv_msg.send_ctrl_cmd(cmd)

    del resp["arguments"]["leases"][0]["cltt"]  # this value is dynamic so we delete it
    assert resp["arguments"]["leases"][0] == lease1_params

    # check for the lease by state
    cmd = {"command": "lease6-get-by-state",
           "arguments": {"state": 0}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    _del_cltt(resp["arguments"]["leases"])
    assert resp["arguments"]["leases"] == leases_params

    cmd = {"command": "lease6-get-by-state",
           "arguments": {"state": 0, "subnet-id": 2}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    _del_cltt(resp["arguments"]["leases"])
    assert resp["arguments"]["leases"] == [lease2_params]

    cmd = {"command": "lease6-get-by-state",
           "arguments": {"state": "assigned", "subnet-id": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    _del_cltt(resp["arguments"]["leases"])
    assert resp["arguments"]["leases"] == [lease1_params]

    _send_cmd("lease6-get-by-state", extra_param={"state": 2}, exp_result=3)
    _send_cmd("lease4-get-by-state", extra_param={"state": "released", "subnet-id": 1}, exp_result=3)

    srv_msg.check_leases([{"duid": "00:03:00:01:66:55:44:33:22:11",
                           "address": "2001:db8:1::1",
                           "iaid": 1234,
                           "hostname": "four.hostname.com",
                           "hw-address": "08:08:08:08:08:08"},
                          {"duid": "00:04:00:01:66:55:44:33:22:11",
                           "address": "2001:db8:2::5",
                           "iaid": 1234,
                           "hostname": "five.hostname.com",
                           "hw-address": "09:09:09:09:09:09"},
                          ],
                         backend=backend)


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_v6_lease_get_by_negative():
    """
    Check various options of incorrectly build
    lease6-get-by-hostname, lease6-get-by-duid, commands.
    """
    misc.test_setup()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
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

    # Per RFC 8415, section 11.1, DUID should have at least one byte of value.
    # The first two bytes representing type are mandatory, so that's a total
    # minimum of 3 bytes.
    cmd = {"command": "lease6-get-by-duid",
           "arguments": {"duid": ""}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "identifier is too short (0), at least 3 is required"

    cmd = {"command": "lease6-get-by-duid",
           "arguments": {"duid": "00"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "identifier is too short (1), at least 3 is required"

    cmd = {"command": "lease6-get-by-duid",
           "arguments": {"duid": "0011"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "identifier is too short (2), at least 3 is required"

    cmd = {"command": "lease6-get-by-duid",
           "arguments": {"duid": "001122"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert resp["text"] == "0 IPv6 lease(s) found."

    # The maximum DUID size specified in RFC 8415, section 11.1 is 130:
    # 2 fixed octets for the type + 128 maximum octets for the value.

    # 130 should work.
    cmd = {
        "command": "lease6-get-by-duid",
        "arguments": {
            "duid": ''.join(secrets.choice(string.hexdigits) for _ in range(260)).lower()
        }
    }
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert resp["text"] == "0 IPv6 lease(s) found."

    # 131 should result in error.
    cmd = {
        "command": "lease6-get-by-duid",
        "arguments": {
            "duid": ''.join(secrets.choice(string.hexdigits) for _ in range(262)).lower()
        }
    }
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "identifier is too large (131), at most 130 is required"

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

    # Testing lease6-get-by-hw-address
    cmd = {"command": "lease6-get-by-hw-address"}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "Command arguments missing or a not a map."

    cmd = {"command": "lease6-get-by-hw-address",
           "arguments": {}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'hw-address' parameter not specified"

    cmd = {"command": "lease6-get-by-hw-address",
           "arguments": {"hw-address": ""}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'hw-address' parameter must not be empty"

    cmd = {"command": "lease6-get-by-hw-address",
           "arguments": {"hw-address": "0011"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid format of the decoded string '0011'"

    cmd = {
        "command": "lease6-get-by-hw-address",
        "arguments": {
            "hw-address": ''.join(secrets.choice(string.hexdigits) + secrets.choice(string.hexdigits) +
                                  ":" for _ in range(260)).lower()[:-1]
        }
    }
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "address vector size exceeds MAX_HWADDR_LEN"

    cmd = {"command": "lease6-get-by-hw-address",
           "arguments": {"hw-address": " "}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "' ' is not a valid hexadecimal digit in decoded string ' '"

    cmd = {"command": "lease6-get-by-hw-address",
           "arguments": {"hw-address": "xxx"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid format of the decoded string 'xxx'"

    cmd = {"command": "lease6-get-by-hw-address",
           "arguments": {"hw-address": 2}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'hw-address' parameter must be a string"

    cmd = {"command": "lease6-get-by-hw-address",
           "arguments": {"hw-address": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'hw-address' parameter must be a string"

    cmd = {"command": "lease6-get-by-state",
           "arguments": {"state": {}}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'state' parameter must be a number or a string"

    resp = _send_cmd("lease6-get-by-state", extra_param={"state": "not_a_state"}, exp_result=1)
    assert resp["text"] == "'state' parameter value (not_a_state) is not recognized"
    # Inconsistent, ideally should also return 1
    resp = _send_cmd("lease6-get-by-state", extra_param={"state": 9}, exp_result=3)
    assert resp["text"] == "0 IPv6 lease(s) found with state 9."
