# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea leases manipulation commands"""

# pylint: disable=line-too-long

import os
import time
import pytest

from src import misc
from src import srv_msg
from src import srv_control
from src.softwaresupport.multi_server_functions import fabric_sudo_command, verify_file_permissions
from src.protosupport.multi_protocol_functions import file_contains_line, sort_container
from src.forge_cfg import world


def _get_lease(addr='192.168.50.1', mac="ff:01:02:03:ff:04"):
    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', mac)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', addr)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', addr)
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', mac)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', addr)
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize("channel", ['socket', 'http'])
def test_lease_cmds_list(channel):
    """
    Check if with loaded hook, lease commands are available
    @param channel: we accept socket or http
    """
    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')
    cmd = {"command": "list-commands", "arguments": {}}
    resp = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    for cmd in ["lease4-add",
                "lease4-del",
                "lease4-get",
                "lease4-get-all",
                "lease4-get-by-client-id",
                "lease4-get-by-hostname",
                "lease4-get-by-hw-address",
                "lease4-resend-ddns",
                "lease4-get-page",
                "lease4-update",
                "lease4-wipe",
                "lease4-write",
                "lease6-add",
                "lease6-bulk-apply",
                "lease6-del",
                "lease6-get",
                "lease6-get-all",
                "lease6-get-by-duid",
                "lease6-get-by-hostname",
                "lease6-get-page",
                "lease6-resend-ddns",
                "lease6-update",
                "lease6-wipe",
                "lease6-write",
                "leases-reclaim"]:
        assert cmd in resp["arguments"]


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_v4_lease_cmds_update(backend):
    """
    Check if lease4-update works correctly on existing lease
    @param backend: 3 types of leases backend kea support
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface('10.0.0.0/24', '10.0.0.5-10.0.0.5')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # get new lease
    _get_lease()

    # check if it's there
    cmd = {"command": "lease4-get",
           "arguments": {"ip-address": "192.168.50.1"}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == "IPv4 lease found."
    resp = resp["arguments"]
    del resp["cltt"]  # this value is dynamic

    assert resp == {"fqdn-fwd": False,
                    "fqdn-rev": False,
                    "hostname": "",
                    "hw-address": "ff:01:02:03:ff:04",
                    "ip-address": "192.168.50.1",
                    # "pool-id": 0, if id is 0 it's no longer returned
                    "state": 0,
                    "subnet-id": 1,
                    "valid-lft": 4000}

    # update existing lease
    cmd = {"command": "lease4-update",
           "arguments": {"ip-address": "192.168.50.1",
                         "hostname": "newhostname.example.org",
                         "hw-address": "1a:1b:1c:1d:1e:1f",
                         "subnet-id": 1,
                         "valid-lft": 7000}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == "IPv4 lease updated."

    # check if it's really updated
    cmd = {"command": "lease4-get",
           "arguments": {"ip-address": "192.168.50.1"}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == "IPv4 lease found."
    resp = resp["arguments"]
    del resp["cltt"]  # this value is dynamic

    assert resp == {"fqdn-fwd": False,
                    "fqdn-rev": False,
                    "hostname": "newhostname.example.org",
                    "hw-address": "1a:1b:1c:1d:1e:1f",
                    "ip-address": "192.168.50.1",
                    # "pool-id": 0, if id is 0 it's no longer returned
                    "state": 0,
                    "subnet-id": 1,
                    "valid-lft": 7000}

    # check old mac address, it's should be missing
    cmd = {"command": "lease4-get",
           "arguments": {"identifier-type": "hw-address", "identifier": "ff:01:02:03:ff:04", "subnet-id": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert resp["text"] == "Lease not found."

    # make sure that updated lease is indeed saved in database/lease file
    srv_msg.check_leases({"hwaddr": "1a:1b:1c:1d:1e:1f", "address": "192.168.50.1", "valid_lifetime": 7000},
                         backend=backend)


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_v4_lease_cmds_get():
    """
    Basic test to check lease4-get command by hw address and ip address
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface('10.0.0.0/24', '10.0.0.5-10.0.0.5')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # assign new lease
    _get_lease()

    # get lease using ip address
    cmd = {"command": "lease4-get",
           "arguments": {"ip-address": "192.168.50.1"}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == "IPv4 lease found."
    resp = resp["arguments"]
    save_cltt = resp["cltt"]
    del resp["cltt"]  # this value is dynamic

    # check content of lease4-get
    assert resp == {"fqdn-fwd": False,
                    "fqdn-rev": False,
                    "hostname": "",
                    "hw-address": "ff:01:02:03:ff:04",
                    "ip-address": "192.168.50.1",
                    # "pool-id": 0, if id is 0 it's no longer returned
                    "state": 0,
                    "subnet-id": 1,
                    "valid-lft": 4000}

    # check lease using mac address
    cmd = {"command": "lease4-get",
           "arguments": {"identifier-type": "hw-address", "identifier": "ff:01:02:03:ff:04", "subnet-id": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == "IPv4 lease found."
    resp = resp["arguments"]

    assert resp == {"cltt": save_cltt,
                    "fqdn-fwd": False,
                    "fqdn-rev": False,
                    "hostname": "",
                    "hw-address": "ff:01:02:03:ff:04",
                    "ip-address": "192.168.50.1",
                    # "pool-id": 0, if id is 0 it's no longer returned
                    "state": 0,
                    "subnet-id": 1,
                    "valid-lft": 4000}

    # try nonexistent lease using ip address to confirm Lease not found
    cmd = {"command": "lease4-get",
           "arguments": {"ip-address": "192.168.50.2"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert resp["text"] == "Lease not found."

    # try nonexistent lease using mac address to confirm Lease not found
    cmd = {"command": "lease4-get",
           "arguments": {"identifier-type": "hw-address", "identifier": "ff:01:02:03:ff:05", "subnet-id": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert resp["text"] == "Lease not found."


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_v4_lease_cmds_add(backend):
    """
    Add leases using lease4-add to different subnets, check with lease4-get and check content of database/lease file
    @param backend: 3 types of leases backend kea support
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.config_srv_another_subnet_no_interface('192.168.150.0/24', '192.168.150.5-192.168.150.5')
    srv_control.set_time('valid-lifetime', 1111)  # global
    srv_control.set_time_in_subnet('valid-lifetime', 1, 2222)  # subnet 192.168.150.0
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # let's check first if lease is missing
    cmd = {"command": "lease4-get",
           "arguments": {"identifier-type": "hw-address", "identifier": "ff:01:02:03:ff:04", "subnet-id": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert resp["text"] == "Lease not found."

    # add new to subnet 1 with non default valid lifetime
    cmd = {"command": "lease4-add",
           "arguments": {"hw-address": "ff:01:02:03:ff:04", "ip-address": "192.168.50.5", "valid-lft": 999}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == "Lease for address 192.168.50.5, subnet-id 1 added."

    # check if we can add it again
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=4)
    assert resp["text"] == "IPv4 lease already exists."

    # re-check with command
    cmd = {"command": "lease4-get",
           "arguments": {"identifier-type": "hw-address", "identifier": "ff:01:02:03:ff:04", "subnet-id": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == "IPv4 lease found."
    resp = resp["arguments"]
    del resp["cltt"]  # this value is dynamic
    assert resp == {"fqdn-fwd": False,
                    "fqdn-rev": False,
                    "hostname": "",
                    "hw-address": "ff:01:02:03:ff:04",
                    "ip-address": "192.168.50.5",
                    # "pool-id": 0, if id is 0 it's no longer returned
                    "state": 0,
                    "subnet-id": 1,
                    "valid-lft": 999}

    # this new lease will be for second subnet with address out of pool,
    # and used the same mac address
    # valid lifetime should be the one configured on subnet level = 2222
    cmd = {"command": "lease4-add",
           "arguments": {"hw-address": "ff:01:02:03:ff:04", "ip-address": "192.168.150.50"}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == "Lease for address 192.168.150.50, subnet-id 2 added."

    # check if it's really added
    cmd = {"command": "lease4-get",
           "arguments": {"identifier-type": "hw-address", "identifier": "ff:01:02:03:ff:04", "subnet-id": 2}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == "IPv4 lease found."
    resp = resp["arguments"]
    del resp["cltt"]  # this value is dynamic
    assert resp == {"fqdn-fwd": False,
                    "fqdn-rev": False,
                    "hostname": "",
                    "hw-address": "ff:01:02:03:ff:04",
                    "ip-address": "192.168.150.50",
                    # "pool-id": 0, if id is 0 it's no longer returned
                    "state": 0,
                    "subnet-id": 2,
                    "valid-lft": 2222}

    # let's check that first lease is still in place
    cmd = {"command": "lease4-get",
           "arguments": {"identifier-type": "hw-address", "identifier": "ff:01:02:03:ff:04", "subnet-id": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == "IPv4 lease found."
    resp = resp["arguments"]
    del resp["cltt"]  # this value is dynamic
    assert resp == {"fqdn-fwd": False,
                    "fqdn-rev": False,
                    "hostname": "",
                    "hw-address": "ff:01:02:03:ff:04",
                    "ip-address": "192.168.50.5",
                    # "pool-id": 0, if id is 0 it's no longer returned
                    "state": 0,
                    "subnet-id": 1,
                    "valid-lft": 999}

    # check 3rd lease to subnet 1, this time without leases lifetime set, should have global value = 1111
    cmd = {"command": "lease4-add",
           "arguments": {"hw-address": "ff:01:02:03:04:05", "ip-address": "192.168.50.150"}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == "Lease for address 192.168.50.150, subnet-id 1 added."

    # check if it's really added
    cmd = {"command": "lease4-get",
           "arguments": {"identifier-type": "hw-address", "identifier": "ff:01:02:03:04:05", "subnet-id": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == "IPv4 lease found."
    resp = resp["arguments"]
    del resp["cltt"]  # this value is dynamic
    assert resp == {"fqdn-fwd": False,
                    "fqdn-rev": False,
                    "hostname": "",
                    "hw-address": "ff:01:02:03:04:05",
                    "ip-address": "192.168.50.150",
                    # "pool-id": 0, if id is 0 it's no longer returned
                    "state": 0,
                    "subnet-id": 1,
                    "valid-lft": 1111}

    # and now check database/lease file directly
    leases_lst = [{"hwaddr": "ff:01:02:03:ff:04", "address": "192.168.50.5", "valid_lifetime": 999},
                  {"hwaddr": "ff:01:02:03:ff:04", "address": "192.168.150.50", "valid_lifetime": 2222},
                  {"hwaddr": "ff:01:02:03:04:05", "address": "192.168.50.150", "valid_lifetime": 1111}]
    srv_msg.check_leases(leases_lst, backend=backend)


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_v4_lease_cmds_add_with_additional_values(backend):
    """
    Check lease4-add with all values possible to set in lease. Checks if lease is reported as added
    and if it's in database/lease file
    @param backend: 3 types of leases backend kea support
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # make sure that leases file is empty
    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.5')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    cmd = {"command": "lease4-get",
           "arguments": {"identifier-type": "hw-address", "identifier": "1a:1b:1c:1d:1e:1f", "subnet-id": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert resp["text"] == "Lease not found."

    # add lease with all possible values and check
    cmd = {"command": "lease4-add",
           "arguments": {"subnet-id": 1,
                         "ip-address": "192.168.50.5",
                         "hw-address": "1a:1b:1c:1d:1e:1f",
                         "fqdn-fwd": True,
                         "fqdn-rev": True,
                         "valid-lft": 7777,
                         # "pool-id": 0, if id is 0 it's no longer returned
                         "state": 1,
                         "expire": int(time.time()) + 7000,
                         "hostname": "my.host.some.name",
                         "client-id": "aa:bb:cc:dd:11:22"}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == "Lease for address 192.168.50.5, subnet-id 1 added."

    cmd = {"command": "lease4-get",
           "arguments": {"identifier-type": "client-id", "identifier": "aa:bb:cc:dd:11:22", "subnet-id": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    resp = resp["arguments"]
    del resp["cltt"]  # this value is dynamic

    assert resp == {"fqdn-fwd": True,
                    "fqdn-rev": True,
                    "client-id": "aa:bb:cc:dd:11:22",
                    "hostname": "my.host.some.name",
                    "hw-address": "1a:1b:1c:1d:1e:1f",
                    "ip-address": "192.168.50.5",
                    # "pool-id": 0, if id is 0 it's no longer returned
                    "state": 1,
                    "subnet-id": 1,
                    "valid-lft": 7777}
    srv_msg.check_leases({"hwaddr": "1a:1b:1c:1d:1e:1f", "address": "192.168.50.5", "valid_lifetime": 7777},
                         backend=backend)


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_v4_lease_cmds_del(backend):
    """
    Check if we can delete lease using lease4-del command
    @param backend: 3 types of leases backend kea support
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # assign new lease
    _get_lease()

    # this exchange should fail, kea is configured with just one address
    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', 'aa:bb:cc:dd:ee:11')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    # delete assigned lease
    cmd = {"command": "lease4-del", "arguments": {"ip-address": "192.168.50.1"}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == "IPv4 lease deleted."

    # let's try to get deleted lease, it should fail
    cmd = {"command": "lease4-get", "arguments": {"ip-address": "192.168.50.1"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert resp["text"] == "Lease not found."

    # another one lease
    _get_lease(mac="ff:01:02:03:ff:05")

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', 'aa:bb:cc:dd:ee:11')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    # get new lease
    cmd = {"command": "lease4-get", "arguments": {"ip-address": "192.168.50.1"}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == "IPv4 lease found."
    assert resp["arguments"]["hw-address"] == "ff:01:02:03:ff:05"
    assert resp["arguments"]["ip-address"] == "192.168.50.1"

    # and remove this using mac address as identifier
    cmd = {"command": "lease4-del", "arguments": {"identifier": "ff:01:02:03:ff:05",
                                                  "identifier-type": "hw-address",
                                                  "subnet-id": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == "IPv4 lease deleted."

    # check if it's deleted
    cmd = {"command": "lease4-get", "arguments": {"ip-address": "192.168.50.1"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert resp["text"] == "Lease not found."

    # if Kea can assign 3rd lease for 3rd client - database/lease file is indeed empty
    _get_lease(mac="ff:01:02:03:ff:06")


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile'])
def test_v4_lease_cmds_wipe(backend):
    """
    Check lease4-wipe command while multiple leases saved
    @param backend: 1 type of leases backend kea support; wipeLeases4 is not implemented in MySQL and PostgreSQL
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.2')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # assign two leases
    _get_lease()
    _get_lease(addr="192.168.50.2", mac="ff:01:02:03:ff:05")

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', 'aa:bb:cc:dd:ee:11')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    # get two leases
    cmd = {"command": "lease4-get", "arguments": {"ip-address": "192.168.50.1"}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == "IPv4 lease found."
    assert resp["arguments"]["hw-address"] == "ff:01:02:03:ff:04"
    assert resp["arguments"]["ip-address"] == "192.168.50.1"

    cmd = {"command": "lease4-get", "arguments": {"ip-address": "192.168.50.2"}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == "IPv4 lease found."
    assert resp["arguments"]["hw-address"] == "ff:01:02:03:ff:05"
    assert resp["arguments"]["ip-address"] == "192.168.50.2"

    # wipe those assigned leases
    cmd = {"command": "lease4-wipe", "arguments": {"subnet-id": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == "Deleted 2 IPv4 lease(s) from subnet(s) 1 WARNING: lease4-wipe is deprecated!"

    # we shouldn't get leases back after wipe.
    cmd = {"command": "lease4-get", "arguments": {"ip-address": "192.168.50.1"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert resp["text"] == "Lease not found."

    cmd = {"command": "lease4-get", "arguments": {"ip-address": "192.168.50.2"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert resp["text"] == "Lease not found."

    # if we can again assign new leases for new clients - database/leases file was empty
    _get_lease(mac="ff:01:02:03:ff:11")
    _get_lease(addr="192.168.50.2", mac="ff:01:02:03:ff:15")


# negative tests
@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_v4_lease_cmds_lease_add_negative():
    """
    Check various options of incorrectly build lease4-add command
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    cmd = {"command": "lease4-add"}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "no parameters specified for the command"

    cmd = {"command": "lease4-add",
           "arguments": {}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "missing parameter 'ip-address'" in resp["text"]

    cmd = {"command": "lease4-add",
           "arguments": {"subnet-id": 44,
                         "ip-address": "192.168.50.5",
                         "hw-address": "1a:1b:1c:1d:1e:1f"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=4)
    assert resp["text"] == "Invalid subnet-id: No IPv4 subnet with subnet-id=44 currently configured."

    cmd = {"command": "lease4-add",
           "arguments": {"subnet-id": 1,
                         "ip-address": "192.0.0.5",
                         "hw-address": "1a:1b:1c:1d:1e:1f"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=4)
    assert resp["text"] == "The address 192.0.0.5 does not belong to subnet 192.168.50.0/24, subnet-id=1"

    cmd = {"command": "lease4-add",
           "arguments": {"subnet-id": 1,
                         "ip-address": "192.168.50.5"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "missing parameter 'hw-address'" in resp["text"]

    cmd = {"command": "lease4-add",
           "arguments": {"subnet-id": 1,
                         "ip-address": "192.168.50.300",
                         "hw-address": "1a:1b:1c:1d:1e:1f"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "Failed to convert '192.168.50.300' to address: Failed to convert string to address '192.168.50.300': Invalid argument" in resp["text"]

    cmd = {"command": "lease4-add",
           "arguments": {"subnet-id": 1,
                         "ip-address": "192.168.50.5",
                         "valid-lft": "invalid-data-type",
                         "hw-address": "1a:1b:1c:1d:1e:1f"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "invalid type specified for parameter 'valid-lft'" in resp["text"]

    cmd = {"command": "lease4-add",
           "arguments": {"subnet-id": 1,
                         "ip-address": "192.168.50.5",
                         "valid-lft": 888,
                         "expire": -1,
                         "hw-address": "1a:1b:1c:1d:1e:1f"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "expiration time must be positive for address 192.168.50.5"

    cmd = {"command": "lease4-add",
           "arguments": {"subnet-id": 1,
                         "ip-address": "192.168.50.5",
                         "valid-lft": 888,
                         "client-id": 1234,
                         "hw-address": "1a:1b:1c:1d:1e:1f"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "invalid type specified for parameter 'client-id'" in resp["text"]

    cmd = {"command": "lease4-add",
           "arguments": {"subnet-id": 1,
                         "ip-address": "192.168.50.5",
                         "valid-lft": 888,
                         "state": 8,
                         "hw-address": "1a:1b:1c:1d:1e:1f"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "Invalid state value: 8, supported values are: 0 (default), 1 (declined) and 2 (expired-reclaimed)"


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_v4_lease_cmds_lease_get_negative():
    """
    Check various options of incorrectly build lease4-get command
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    cmd = {"command": "lease4-get"}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "Parameters missing or are not a map."

    cmd = {"command": "lease4-get",
           "arguments": {}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "Mandatory 'subnet-id' parameter missing."

    cmd = {"command": "lease4-get",
           "arguments": {"ip-address": ""}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "Failed to convert string to address '': Invalid argument"

    cmd = {"command": "lease4-get",
           "arguments": {"identifier": "ff:01:02:03:ff:05",
                         "identifier-type": "hw-address",
                         "subnet-id": 10}}
    srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    cmd = {"command": "lease4-get",
           "arguments": {"identifier": "ff:01:02:03:ff:05",
                         "identifier-type": "duid",
                         "subnet-id": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "Query by duid is not allowed in v4."

    cmd = {"command": "lease4-get",
           "arguments": {"identifier": "ff:01:02:03:ff:05",
                         "identifier-type": "something",
                         "subnet-id": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "Incorrect identifier type: something, the only supported values are: address, hw-address, client-id"
    # TODO: test fails, kea#2260

    cmd = {"command": "lease4-get",
           "arguments": {"identifier": "ff:01:02:03:ff:05",
                         "subnet-id": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "No 'ip-address' provided and 'identifier-type' is either missing or not a string."

    cmd = {"command": "lease4-get",
           "arguments": {"identifier-type": "hw-address",
                         "subnet-id": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "No 'ip-address' provided and 'identifier' is either missing or not a string."

    cmd = {"command": "lease4-get",
           "arguments": {"identifier": 123,
                         "identifier-type": "hw-address",
                         "subnet-id": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "No 'ip-address' provided and 'identifier' is either missing or not a string."


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('file', ['overwrite', 'new'])
def test_v4_lease_cmds_write(file):
    """
    Check if lease4-write makes correct memfile.
    @param file: Select if memfile should be overwritten, or made as new file.
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # prepare user-context JSON
    user_context = {
        "ISC": {
            "relay-info": [
                {
                    "hop": 0,
                    "link": "2001:db8:2::1000",
                    "options": "0x00120008706F727431323334",
                    "peer": "fe80::1"
                }
            ]
        },
        "version": [{"number": 1, "rev": 2}, {"id": 1, "no": 2}],
        "class": "!@#$%^&*(`)'_+=-?|\"\\\b\f\n\r\t",
        "tre,e": {"bra,nch1": {"treehouse": 1}, "bra,nch2": 2,
                  "bra,nch3": {"leaf1": 1,
                               "leaf2": ["vein1", "vein2"]}}
    }

    # make sure that leases file is empty
    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.5')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    cmd = {"command": "lease4-get",
           "arguments": {"identifier-type": "hw-address", "identifier": "1a:1b:1c:1d:1e:1f", "subnet-id": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert resp["text"] == "Lease not found."

    # add lease with all possible values and check
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
                         "user-context": user_context}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == "Lease for address 192.168.50.5, subnet-id 1 added."

    if file == 'overwrite':
        # Empty the memfile
        fabric_sudo_command(f'echo "Empty_File" > {world.f_cfg.get_leases_path()}')
        # Verify that memfile has no leases
        srv_msg.check_leases({"hwaddr": "1a:1b:1c:1d:1e:1f", "address": "192.168.50.5", "valid_lifetime": 7777},
                             backend='memfile', should_succeed=False)
        write_path = world.f_cfg.get_leases_path()
    else:  # file == new
        # Verify that lease is in memfile
        srv_msg.check_leases({"hwaddr": "1a:1b:1c:1d:1e:1f", "address": "192.168.50.5", "valid_lifetime": 7777},
                             backend='memfile')
        write_path = world.f_cfg.data_join('new-leases.csv')

    # Verify that lease is in memory
    cmd = {"command": "lease4-get",
           "arguments": {"identifier-type": "client-id", "identifier": "aa:bb:cc:dd:11:22", "subnet-id": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    resp = resp["arguments"]
    del resp["cltt"]  # this value is dynamic

    # compare sorted JSON prepared on start with sorted returned one
    assert sort_container(user_context) == sort_container(resp["user-context"])
    del resp["user-context"]  # already checked

    assert resp == {"fqdn-fwd": True,
                    "fqdn-rev": True,
                    "client-id": "aa:bb:cc:dd:11:22",
                    "hostname": "my.host.some.name",
                    "hw-address": "1a:1b:1c:1d:1e:1f",
                    "ip-address": "192.168.50.5",
                    # "pool-id": 0, if id is 0 it's no longer returned
                    "state": 1,
                    "subnet-id": 1,
                    "valid-lft": 7777}

    # Execute lease4-write
    cmd = {"command": "lease4-write",
           "arguments": {"filename": write_path}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == f'IPv4 lease database into \'{write_path}\'.'

    # Check if lease file is restored
    srv_msg.check_leases({"hwaddr": "1a:1b:1c:1d:1e:1f", "address": "192.168.50.5", "valid_lifetime": 7777},
                         backend='memfile')

    if file == 'overwrite':
        # Check if backup file is created
        cmd = {"command": "status-get", "arguments": {}}
        response = srv_msg.send_ctrl_cmd(cmd)
        pid = response['arguments']['pid']
        file_contains_line(f'{write_path}.bak{pid}', 'Empty_File')
    elif file == 'new':
        # Verify that new file contains lease
        file_contains_line(write_path, '192.168.50.5,1a:1b:1c:1d:1e:1f,aa:bb:cc:dd:11:22,7777')
        fabric_sudo_command(f'cp {write_path} {world.f_cfg.get_leases_path()}')

    srv_control.start_srv('DHCP', 'restarted')

    # Verify that lease is in memory
    cmd = {"command": "lease4-get",
           "arguments": {"identifier-type": "client-id", "identifier": "aa:bb:cc:dd:11:22", "subnet-id": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    resp = resp["arguments"]  # drop unnecessary info for comparison

    # compare sorted JSON prepared on start with sorted returned one
    assert sort_container(user_context) == sort_container(resp["user-context"])


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_v4_lease_cmds_write_no_persist():
    """
    Check if lease4-write makes correct memfile with persist: false.
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    world.dhcp_cfg.update({"lease-database": {"type": "memfile", "persist": False}})
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # make sure that leases file is empty
    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.5')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    cmd = {"command": "lease4-get",
           "arguments": {"identifier-type": "hw-address", "identifier": "1a:1b:1c:1d:1e:1f", "subnet-id": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert resp["text"] == "Lease not found."

    # prepare user-context JSON
    user_context = {
        "ISC": {
            "relay-info": [
                {
                    "hop": 0,
                    "link": "2001:db8:2::1000",
                    "options": "0x00120008706F727431323334",
                    "peer": "fe80::1"
                }
            ]
        },
        "version": [{"number": 1, "rev": 2}, {"id": 1, "no": 2}],
        "class": "!@#$%^&*(`)'_+=-?|\"\\\b\f\n\r\t",
        "tre,e": {"bra,nch1": {"treehouse": 1}, "bra,nch2": 2,
                  "bra,nch3": {"leaf1": 1,
                               "leaf2": ["vein1", "vein2"]}}
    }

    # add lease with all possible values and check
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
                         "user-context": user_context}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == "Lease for address 192.168.50.5, subnet-id 1 added."

    # Verify that lease is in memory
    cmd = {"command": "lease4-get",
           "arguments": {"identifier-type": "client-id", "identifier": "aa:bb:cc:dd:11:22", "subnet-id": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    resp = resp["arguments"]

    # Check if lease file is still empty
    srv_msg.check_leases({"hwaddr": "1a:1b:1c:1d:1e:1f", "address": "192.168.50.5", "valid_lifetime": 7777},
                         backend='memfile', should_succeed=False)

    # Execute lease4-write
    cmd = {"command": "lease4-write",
           "arguments": {"filename": world.f_cfg.get_leases_path()}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == f'IPv4 lease database into \'{world.f_cfg.get_leases_path()}\'.'

    # Check if lease file is restored
    srv_msg.check_leases({"hwaddr": "1a:1b:1c:1d:1e:1f", "address": "192.168.50.5", "valid_lifetime": 7777},
                         backend='memfile')

    # Restart with "persist": True
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'restarted')

    # checking if added lease is present after restart
    cmd = {"command": "lease4-get",
           "arguments": {"identifier-type": "client-id", "identifier": "aa:bb:cc:dd:11:22", "subnet-id": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    resp = resp["arguments"]  # drop unnecessary info for comparison

    # compare sorted JSON prepared on start with sorted returned one
    assert sort_container(user_context) == sort_container(resp["user-context"])


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_v6_lease_cmds_add_valid(backend):
    """
    Add lease using lease6-add, check with Solicit and check content of database/lease file
    @param backend: 3 types of leases backend kea support
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.config_srv_opt('preference', '123')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # checking if leases are available
    srv_msg.SA(address='2001:db8:1::1', duid='00:03:00:01:66:55:44:33:22:11')

    # adding lease by lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"subnet-id": 1,
                                                  "ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "iaid": 1234}}
    srv_msg.send_ctrl_cmd(cmd)

    # checking if leases are not available -
    # lease6-add should occupy the one and only lease from subnet
    srv_msg.SA(duid='00:03:00:01:66:55:44:33:22:11')

    # checking if lease exists in database
    srv_msg.check_leases({"duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                          "address": "2001:db8:1::1",
                          "valid_lifetime": 4000,
                          "iaid": 1234},
                         backend=backend)


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_v6_lease_cmds_add_expired_with_options(backend):
    """
    Add expired lease using lease6-add with additional options,
    check with Solicit and check content of database/lease file
    @param backend: 3 types of leases backend kea support
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.config_srv_opt('preference', '123')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # checking if leases are available
    srv_msg.SA(address='2001:db8:1::1', duid='00:03:00:01:66:55:44:33:22:11')

    # adding expired lease by lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"subnet-id": 1,
                                                  "ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "iaid": 1234,
                                                  "hw-address": "1a:2b:3c:4d:5e:6f",
                                                  "preferred-lft": 500,
                                                  "valid-lft": 11111,
                                                  "expire": 123456789,
                                                  "fqdn-fwd": True,
                                                  "fqdn-rev": True,
                                                  "hostname": "urania.example.org"}}
    srv_msg.send_ctrl_cmd(cmd)

    # checking if leases are available - should be one
    srv_msg.SA(address='2001:db8:1::1', duid='00:03:00:01:66:55:44:33:22:11')

    # checking if expired lease exists in database
    srv_msg.check_leases({"duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                          "address": "2001:db8:1::1",
                          "iaid": 1234,
                          "hostname": "urania.example.org"},
                         backend=backend)


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_v6_lease_cmds_add_valid_with_options(backend):
    """
    Add valid lease using lease6-add with additional options,
    check with Solicit and check content of database/lease file
    @param backend: 3 types of leases backend kea support
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.config_srv_opt('preference', '123')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # checking if leases are available
    srv_msg.SA(address='2001:db8:1::1', duid='00:03:00:01:66:55:44:33:22:11')

    # adding expired lease by lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"subnet-id": 1,
                                                  "ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "iaid": 1234,
                                                  "hw-address": "1a:2b:3c:4d:5e:6f",
                                                  "preferred-lft": 500,
                                                  "valid-lft": 11111,
                                                  "fqdn-fwd": True,
                                                  "fqdn-rev": True,
                                                  "hostname": "urania.example.org"}}
    srv_msg.send_ctrl_cmd(cmd)

    # checking if leases are available - should be none
    srv_msg.SA(duid='00:03:00:01:66:55:44:33:22:11')

    # checking if added lease is got by Control Agent
    cmd = {"command": "lease6-get",
           "arguments": {"ip-address": "2001:db8:1::1", "type": "IA_NA"}}
    srv_msg.send_ctrl_cmd(cmd)

    # checking if added lease exists in database
    srv_msg.check_leases({"duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                          "address": "2001:db8:1::1",
                          "iaid": 1234,
                          "hostname": "urania.example.org"},
                         backend=backend)


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_v6_lease_cmds_add_notvalid():
    """
    Add not valid lease using lease6-add
    testing nonexistent subnet and ip outside of subnet
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.config_srv_opt('preference', '123')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # checking wrong subnet id
    cmd = {"command": "lease6-add",
           "arguments": {"subnet-id": 11,
                         "ip-address": "2001:db8:1::1",
                         "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                         "iaid": 1234}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=4)
    assert resp["text"] == "Invalid subnet-id: No IPv6 subnet with " \
                           "subnet-id=11 currently configured."

    # checking ip outside of subnet
    cmd = {"command": "lease6-add",
           "arguments": {"subnet-id": 1,
                         "ip-address": "2001:db8:2::1",
                         "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                         "iaid": 1234}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=4)
    assert resp["text"] == "The address 2001:db8:2::1 does not belong " \
                           "to subnet 2001:db8:1::/64, subnet-id=1"

    # try adding the same lease
    cmd = {"command": "lease6-add",
           "arguments": {"subnet-id": 1,
                         "ip-address": "2001:db8:1::1",
                         "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                         "iaid": 1234}}
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=4)
    assert resp["text"] == "IPv6 lease already exists."


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_v6_lease_cmds_del_using_address(backend):
    """
    Get lease by SARR, delete it with lease6-del using ip address and check if it is available again
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # Get lease
    srv_msg.SARR(address='2001:db8:1::1', duid='00:03:00:01:66:55:44:33:22:11')

    # be sure none are left
    srv_msg.SA(duid='00:03:00:01:66:55:44:33:55:66')

    # checking lease exists in database
    srv_msg.check_leases({"duid": "00:03:00:01:66:55:44:33:22:11",
                          "address": "2001:db8:1::1"},
                         backend=backend)

    # delete lease
    cmd = {"command": "lease6-del",
           "arguments": {"ip-address": "2001:db8:1::1"}}
    srv_msg.send_ctrl_cmd(cmd)

    # check if leases are available
    srv_msg.SA(address='2001:db8:1::1', duid='00:03:00:01:66:55:44:33:55:66')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_v6_lease_cmds_del_using_duid(backend):
    """
    Get lease by SARR, delete it with lease6-del using duid and check if it is available again
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # Get lease
    srv_msg.SARR(address='2001:db8:1::1', duid='00:03:00:01:66:55:44:33:22:11', iaid=1234)

    # be sure none are left
    srv_msg.SA(duid='00:03:00:01:66:55:44:33:55:66')

    # checking lease exists in database
    srv_msg.check_leases({"duid": "00:03:00:01:66:55:44:33:22:11",
                          "address": "2001:db8:1::1"},
                         backend=backend)

    # delete lease
    cmd = {"command": "lease6-del",
           "arguments": {"subnet-id": 1,
                         "identifier": "00:03:00:01:66:55:44:33:22:11",
                         "identifier-type": "duid",
                         "iaid": 1234}}
    srv_msg.send_ctrl_cmd(cmd)

    # check if leases are available
    srv_msg.SA(address='2001:db8:1::1', duid='00:03:00:01:66:55:44:33:55:66')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_v6_lease_cmds_get_using_address(backend):
    """
    Get lease by SARR, check if returned correctly by lease6-get using ip address
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # Get lease
    srv_msg.SARR(address='2001:db8:1::1', duid='00:03:00:01:66:55:44:33:22:11', iaid=1234)

    # be sure none are left
    srv_msg.SA(duid='00:03:00:01:66:55:44:33:55:66')

    # checking lease exists in database
    srv_msg.check_leases({"duid": "00:03:00:01:66:55:44:33:22:11",
                          "address": "2001:db8:1::1"},
                         backend=backend)

    # check if lease6-get returns proper lease
    cmd = {"command": "lease6-get",
           "arguments": {"ip-address": "2001:db8:1::1"}}
    resp = srv_msg.send_ctrl_cmd(cmd)

    del resp["arguments"]["cltt"]  # this value is dynamic so we delete it
    assert resp["arguments"] == {"duid": "00:03:00:01:66:55:44:33:22:11",
                                 "fqdn-fwd": False,
                                 "fqdn-rev": False,
                                 "hostname": "",
                                 "hw-address": "66:55:44:33:22:11",
                                 "iaid": 1234,
                                 "ip-address": "2001:db8:1::1",
                                 # "pool-id": 0, if id is 0 it's no longer returned
                                 "preferred-lft": 3000,
                                 "state": 0,
                                 "subnet-id": 1,
                                 "type": "IA_NA",
                                 "valid-lft": 4000}


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_v6_lease_cmds_get_using_duid(backend):
    """
    Get lease by SARR, check if returned correctly by lease6-get using duid
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # Get lease
    srv_msg.SARR(address='2001:db8:1::1', duid='00:03:00:01:66:55:44:33:22:11', iaid=1234)

    # be sure none are left
    srv_msg.SA(duid='00:03:00:01:66:55:44:33:55:66')

    # checking lease exists in database
    srv_msg.check_leases({"duid": "00:03:00:01:66:55:44:33:22:11",
                          "address": "2001:db8:1::1"},
                         backend=backend)

    # check if lease6-get returns proper lease
    cmd = {"command": "lease6-get",
           "arguments": {"subnet-id": 1,
                         "identifier": "00:03:00:01:66:55:44:33:22:11",
                         "identifier-type": "duid",
                         "iaid": 1234}}
    resp = srv_msg.send_ctrl_cmd(cmd)

    del resp["arguments"]["cltt"]  # this value is dynamic so we delete it
    assert resp["arguments"] == {"duid": "00:03:00:01:66:55:44:33:22:11",
                                 "fqdn-fwd": False,
                                 "fqdn-rev": False,
                                 "hostname": "",
                                 "hw-address": "66:55:44:33:22:11",
                                 "iaid": 1234,
                                 "ip-address": "2001:db8:1::1",
                                 # "pool-id": 0, if id is 0 it's no longer returned
                                 "preferred-lft": 3000,
                                 "state": 0,
                                 "subnet-id": 1,
                                 "type": "IA_NA",
                                 "valid-lft": 4000}


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_v6_lease_cmds_wipe():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::2')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    # Client sets ia_id value to 666.
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:11:22:33:44:55:66')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:11:22:33:44:55:66')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:11:11:11:11:11:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)

    srv_msg.send_ctrl_cmd_via_socket('{"command":"lease6-wipe", "arguments": {"subnet-id":1}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:11:11:11:11:11:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:11:22:33:44:55:66')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:11:22:33:44:55:66')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:11:11:11:11:11:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_v6_lease_cmds_update(backend):
    """
    Get lease by SARR, check if returned correctly by lease6-get,
    update it with lease6-update and check again
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::2')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # Get lease
    srv_msg.SARR(address='2001:db8:1::1', duid='00:03:00:01:66:55:44:33:22:11', iaid=1234)

    # check if lease6-get returns proper acquired lease
    cmd = {"command": "lease6-get",
           "arguments": {"subnet-id": 1,
                         "identifier": "00:03:00:01:66:55:44:33:22:11",
                         "identifier-type": "duid",
                         "iaid": 1234}}
    resp = srv_msg.send_ctrl_cmd(cmd)

    del resp["arguments"]["cltt"]  # this value is dynamic so we delete it
    assert resp["arguments"] == {"duid": "00:03:00:01:66:55:44:33:22:11",
                                 "fqdn-fwd": False,
                                 "fqdn-rev": False,
                                 "hostname": "",
                                 "hw-address": "66:55:44:33:22:11",
                                 "iaid": 1234,
                                 "ip-address": "2001:db8:1::1",
                                 "preferred-lft": 3000,
                                 "state": 0,
                                 "subnet-id": 1,
                                 # "pool-id": 0, if id is 0 it's no longer returned
                                 "type": "IA_NA",
                                 "valid-lft": 4000}

    # check if lease6-get returns 0 leases of the planed update
    cmd = {"command": "lease6-get",
           "arguments": {"subnet-id": 1,
                         "identifier": "01:02:03:04:05:06:07:08",
                         "identifier-type": "duid",
                         "iaid": 2345}}
    srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    # update lease
    cmd = {"command": "lease6-update",
           "arguments": {"subnet-id": 1,
                         "ip-address": "2001:db8:1::1",
                         "duid": "01:02:03:04:05:06:07:08",
                         "iaid": 2345,
                         "hw-address": "1a:1b:1c:1d:1e:1f",
                         "preferred-lft": 500,
                         "valid-lft": 1000,
                         "hostname": "urania.example.org"}}
    srv_msg.send_ctrl_cmd(cmd)

    # check if lease6-get returns updated lease
    cmd = {"command": "lease6-get",
           "arguments": {"ip-address": "2001:db8:1::1"}}
    resp = srv_msg.send_ctrl_cmd(cmd)

    del resp["arguments"]["cltt"]  # this value is dynamic so we delete it
    assert resp["arguments"] == {"duid": "01:02:03:04:05:06:07:08",
                                 "fqdn-fwd": False,
                                 "fqdn-rev": False,
                                 "hostname": "urania.example.org",
                                 "hw-address": "1a:1b:1c:1d:1e:1f",
                                 "iaid": 2345,
                                 "ip-address": "2001:db8:1::1",
                                 "preferred-lft": 500,
                                 "state": 0,
                                 # "pool-id": 0, if id is 0 it's no longer returned
                                 "subnet-id": 1,
                                 "type": "IA_NA",
                                 "valid-lft": 1000}


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_v6_lease_cmds_add_negative():
    """
    Negative tests sending invalid or missing arguments to lease6-add
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # sending empty lease6-add command
    cmd = {"command": "lease6-add"}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "no parameters specified for the command"

    # sending no arguments in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "missing parameter 'ip-address' (<wire>:0:16)"

    # ip-address
    # sending wrong ip-address format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "xxx"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "Failed to convert 'xxx' to address: Failed to convert string " \
                           "to address 'xxx': Invalid argument(<wire>:0:31)"

    # sending wrong ip-address format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'ip-address' (<wire>:0:31)"

    # sending wrong ip-address format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'ip-address' (<wire>:0:31)"

    # duid
    # sending not enough arguments in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "missing parameter 'duid' (<wire>:0:16)"

    # sending wrong duid format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1", "duid": "xxx"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'xxx' is not a valid string of hexadecimal digits"

    # sending wrong duid format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1", "duid": " "}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "two consecutive separators (' ') specified in a decoded string ' '"

    # sending wrong duid format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1", "duid": 2}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'duid' (<wire>:0:25)"

    # sending wrong duid format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1", "duid": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'duid' (<wire>:0:25)"

    # subnet-id
    # sending ip out of subnet to lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:2::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=4)
    assert resp["text"] == "subnet-id not specified and failed to find a subnet for " \
                           "address 2001:db8:2::1"

    # sending not enough arguments in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "missing parameter 'iaid' (<wire>:0:16)"

    # sending wrong subnet-id format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": 12345678901}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "out of range value (12345678901) specified for " \
                           "parameter 'subnet-id' (<wire>:0:105)"

    # sending wrong subnet-id format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'subnet-id' (<wire>:0:105)"

    # sending wrong subnet-id format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": "xxx"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'subnet-id' (<wire>:0:105)"

    # sending wrong subnet-id format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": " "}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'subnet-id' (<wire>:0:105)"

    # sending non-existent subnet-id to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": 2}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=4)
    assert resp["text"] == "Invalid subnet-id: No IPv6 subnet with " \
                           "subnet-id=2 currently configured."

    # iaid
    # sending not enough arguments in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "missing parameter 'iaid' (<wire>:0:16)"

    # sending wrong iaid format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": 1,
                                                  "iaid": 12345678901}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "out of range value (12345678901) specified " \
                           "for parameter 'iaid' (<wire>:0:69)"

    # sending wrong iaid format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": 1,
                                                  "iaid": "1"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'iaid' (<wire>:0:69)"

    # sending wrong iaid format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": 1,
                                                  "iaid": "xxx"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'iaid' (<wire>:0:69)"

    # sending wrong iaid format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": 1,
                                                  "iaid": " "}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'iaid' (<wire>:0:69)"

    # sending wrong iaid format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": 1,
                                                  "iaid": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'iaid' (<wire>:0:69)"


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_v6_lease_cmds_add_options_negative():
    """
    Negative tests sending invalid or missing arguments to lease6-add
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # hw-address
    # sending wrong hw-address format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": 1,
                                                  "iaid": 1234,
                                                  "hw-address": " "}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "' ' is not a valid hexadecimal digit in decoded string ' '"

    # sending wrong hw-address format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": 1,
                                                  "iaid": 1234,
                                                  "hw-address": "1234"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid format of the decoded string '1234'"

    # sending wrong hw-address format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": 1,
                                                  "iaid": 1234,
                                                  "hw-address": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'hw-address' (<wire>:0:75)"

    # sending wrong hw-address format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": 1,
                                                  "iaid": 1234,
                                                  "hw-address": 2}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'hw-address' (<wire>:0:75)"

    # preferred-lft
    # sending wrong preferred-lft format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": 1,
                                                  "iaid": 1234,
                                                  "preferred-lft": "2000"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'preferred-lft' (<wire>:0:123)"

    # sending wrong preferred-lft format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": 1,
                                                  "iaid": 1234,
                                                  "preferred-lft": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'preferred-lft' (<wire>:0:123)"

    # sending wrong preferred-lft format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": 1,
                                                  "iaid": 1234,
                                                  "preferred-lft": 12345678901}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "out of range value (12345678901) specified for " \
                           "parameter 'preferred-lft' (<wire>:0:123)"

    # valid-lft
    # sending wrong valid-lft format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": 1,
                                                  "iaid": 1234,
                                                  "valid-lft": "2000"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'valid-lft' (<wire>:0:135)"

    # sending wrong valid-lft format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": 1,
                                                  "iaid": 1234,
                                                  "valid-lft": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'valid-lft' (<wire>:0:135)"

    # sending wrong valid-lft format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": 1,
                                                  "iaid": 1234,
                                                  "valid-lft": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'valid-lft' (<wire>:0:135)"

    # sending wrong valid-lft format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": 1,
                                                  "iaid": 1234,
                                                  "valid-lft": 12345678901}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "out of range value (12345678901) specified for " \
                           "parameter 'valid-lft' (<wire>:0:135)"

    # fqdn-fwd
    # sending wrong fqdn-fwd format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": 1,
                                                  "iaid": 1234,
                                                  "fqdn-fwd": "2000"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'fqdn-fwd' (<wire>:0:73)"

    # sending wrong fqdn-fwd format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": 1,
                                                  "iaid": 1234,
                                                  "fqdn-fwd": 0}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'fqdn-fwd' (<wire>:0:73)"

    # sending not enough arguments in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": 1,
                                                  "iaid": 1234,
                                                  "fqdn-fwd": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "No hostname specified and either forward or " \
                           "reverse fqdn was set to true."

    # fqdn-rev
    # sending wrong fqdn-rev format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": 1,
                                                  "iaid": 1234,
                                                  "fqdn-rev": "2000"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'fqdn-rev' (<wire>:0:73)"

    # sending wrong fqdn-rev format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": 1,
                                                  "iaid": 1234,
                                                  "fqdn-rev": 0}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'fqdn-rev' (<wire>:0:73)"

    # sending not enough arguments in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": 1,
                                                  "iaid": 1234,
                                                  "fqdn-rev": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "No hostname specified and either forward or " \
                           "reverse fqdn was set to true."

    # hostname
    # sending wrong hostname format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": 1,
                                                  "iaid": 1234,
                                                  "hostname": 2}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'hostname' (<wire>:0:73)"

    # sending wrong hostname format to in lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "subnet-id": 1,
                                                  "iaid": 1234,
                                                  "hostname": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'hostname' (<wire>:0:73)"


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_v6_lease_cmds_del_negative():
    """
    Negative tests sending invalid or missing arguments to lease6-del
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # sending not enough arguments to lease6-del command
    cmd = {"command": "lease6-del"}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "Parameters missing or are not a map."

    # sending not enough arguments to lease6-del command
    cmd = {"command": "lease6-del", "arguments": {}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "Mandatory 'subnet-id' parameter missing."

    # ip-address
    # sending wrong ip-address to lease6-del command
    cmd = {"command": "lease6-del", "arguments": {"ip-address": ""}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "Failed to convert string to address '': Invalid argument"

    # sending wrong ip-address to lease6-del command
    cmd = {"command": "lease6-del", "arguments": {"ip-address": " "}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "Failed to convert string to address ' ': Invalid argument"

    # sending wrong ip-address to lease6-del command
    cmd = {"command": "lease6-del", "arguments": {"ip-address": 2}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'ip-address' is not a string."

    # sending wrong ip-address to lease6-del command
    cmd = {"command": "lease6-del", "arguments": {"ip-address": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'ip-address' is not a string."

    # subnet-id
    # sending not enough arguments to lease6-del command
    cmd = {"command": "lease6-del", "arguments": {"subnet-id": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "No 'ip-address' provided and 'identifier-type' is either " \
                           "missing or not a string."

    # sending wrong subnet-id to lease6-del command
    cmd = {"command": "lease6-del", "arguments": {"subnet-id": ""}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'subnet-id' parameter is not integer."

    # sending wrong subnet-id to lease6-del command
    cmd = {"command": "lease6-del", "arguments": {"subnet-id": " "}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'subnet-id' parameter is not integer."

    # sending wrong subnet-id to lease6-del command
    cmd = {"command": "lease6-del", "arguments": {"subnet-id": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'subnet-id' parameter is not integer."

    # identifier-type
    # sending not enough arguments to lease6-del command
    cmd = {"command": "lease6-del", "arguments": {"subnet-id": 1, "identifier-type": "duid"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "No 'ip-address' provided and 'identifier' is " \
                           "either missing or not a string."

    # sending wrong identifier-type to lease6-del command
    cmd = {"command": "lease6-del", "arguments": {"subnet-id": 1, "identifier-type": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "No 'ip-address' provided and 'identifier-type' is " \
                           "either missing or not a string."

    # sending wrong identifier-type to lease6-del command
    cmd = {"command": "lease6-del", "arguments": {"subnet-id": 1, "identifier-type": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "No 'ip-address' provided and 'identifier-type' is " \
                           "either missing or not a string."

    # sending wrong identifier-type to lease6-del command
    cmd = {"command": "lease6-del", "arguments": {"subnet-id": 1, "identifier-type": "xxx",
                                                  "identifier": "00:03:00:01:66:55:44:33:22:11"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "Incorrect identifier type: xxx, the only supported values " \
                           "are: address, hw-address, duid"

    # duid
    # sending wrong duid identifier to lease6-del command
    cmd = {"command": "lease6-del", "arguments": {"subnet-id": 1, "identifier-type": "duid",
                                                  "identifier": ""}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "identifier is too short (0), at least 3 is required"

    # sending wrong duid identifier to lease6-del command
    cmd = {"command": "lease6-del", "arguments": {"subnet-id": 1, "identifier-type": "duid",
                                                  "identifier": " "}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "two consecutive separators (' ') specified in a decoded string ' '"

    # sending wrong duid identifier to lease6-del command
    cmd = {"command": "lease6-del", "arguments": {"subnet-id": 1, "identifier-type": "duid",
                                                  "identifier": "xxx"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'xxx' is not a valid string of hexadecimal digits"

    # sending wrong duid identifier to lease6-del command
    cmd = {"command": "lease6-del", "arguments": {"subnet-id": 1, "identifier-type": "duid",
                                                  "identifier": 2}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "No 'ip-address' provided and 'identifier' is either " \
                           "missing or not a string."

    # iaid
    # sending wrong iaid identifier to lease6-del command
    cmd = {"command": "lease6-del", "arguments": {"subnet-id": 1, "identifier-type": "duid",
                                                  "identifier": "00:03:00:01:66:55:44:33:22:11",
                                                  "iaid": ""}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "intValue() called on non-integer Element in (<wire>:0:25)"

    # sending wrong iaid identifier to lease6-del command
    cmd = {"command": "lease6-del", "arguments": {"subnet-id": 1, "identifier-type": "duid",
                                                  "identifier": "00:03:00:01:66:55:44:33:22:11",
                                                  "iaid": " "}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "intValue() called on non-integer Element in (<wire>:0:25)"

    # sending wrong iaid identifier to lease6-del command
    cmd = {"command": "lease6-del", "arguments": {"subnet-id": 1, "identifier-type": "duid",
                                                  "identifier": "00:03:00:01:66:55:44:33:22:11",
                                                  "iaid": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "intValue() called on non-integer Element in (<wire>:0:25)"

    # address
    # sending wrong address identifier to lease6-del command
    cmd = {"command": "lease6-del", "arguments": {"subnet-id": 1, "identifier-type": "address",
                                                  "identifier": 2}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "No 'ip-address' provided and 'identifier' is either " \
                           "missing or not a string."


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_v6_lease_cmds_get_negative():
    """
    Negative tests sending invalid or missing arguments to lease6-get
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # sending not enough arguments to lease6-get command
    cmd = {"command": "lease6-get"}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "Parameters missing or are not a map."

    # sending not enough arguments to lease6-get command
    cmd = {"command": "lease6-get", "arguments": {}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "Mandatory 'subnet-id' parameter missing."

    # ip-address
    # sending wrong ip-address to lease6-get command
    cmd = {"command": "lease6-get", "arguments": {"ip-address": ""}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "Failed to convert string to address '': Invalid argument"

    # sending wrong ip-address to lease6-get command
    cmd = {"command": "lease6-get", "arguments": {"ip-address": " "}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "Failed to convert string to address ' ': Invalid argument"

    # sending wrong ip-address to lease6-get command
    cmd = {"command": "lease6-get", "arguments": {"ip-address": 2}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'ip-address' is not a string."

    # sending wrong ip-address to lease6-get command
    cmd = {"command": "lease6-get", "arguments": {"ip-address": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'ip-address' is not a string."

    # subnet-id
    # sending not enough arguments to lease6-get command
    cmd = {"command": "lease6-get", "arguments": {"subnet-id": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "No 'ip-address' provided and 'identifier-type' is either " \
                           "missing or not a string."

    # sending wrong subnet-id to lease6-get command
    cmd = {"command": "lease6-get", "arguments": {"subnet-id": ""}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'subnet-id' parameter is not integer."

    # sending wrong subnet-id to lease6-get command
    cmd = {"command": "lease6-get", "arguments": {"subnet-id": " "}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'subnet-id' parameter is not integer."

    # sending wrong subnet-id to lease6-get command
    cmd = {"command": "lease6-get", "arguments": {"subnet-id": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'subnet-id' parameter is not integer."

    # identifier-type
    # sending not enough arguments to lease6-get command
    cmd = {"command": "lease6-get", "arguments": {"subnet-id": 1, "identifier-type": "duid"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "No 'ip-address' provided and 'identifier' is " \
                           "either missing or not a string."

    # sending wrong identifier-type to lease6-get command
    cmd = {"command": "lease6-get", "arguments": {"subnet-id": 1, "identifier-type": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "No 'ip-address' provided and 'identifier-type' is " \
                           "either missing or not a string."

    # sending wrong identifier-type to lease6-get command
    cmd = {"command": "lease6-get", "arguments": {"subnet-id": 1, "identifier-type": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "No 'ip-address' provided and 'identifier-type' is " \
                           "either missing or not a string."

    # sending wrong identifier-type to lease6-get command
    cmd = {"command": "lease6-get", "arguments": {"subnet-id": 1, "identifier-type": "xxx",
                                                  "identifier": "00:03:00:01:66:55:44:33:22:11"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "Incorrect identifier type: xxx, the only supported values " \
                           "are: address, hw-address, duid"

    # duid
    # sending wrong duid identifier to lease6-get command
    cmd = {"command": "lease6-get", "arguments": {"subnet-id": 1, "identifier-type": "duid",
                                                  "identifier": ""}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "identifier is too short (0), at least 3 is required"

    # sending wrong duid identifier to lease6-get command
    cmd = {"command": "lease6-get", "arguments": {"subnet-id": 1, "identifier-type": "duid",
                                                  "identifier": " "}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "two consecutive separators (' ') specified in a decoded string ' '"

    # sending wrong duid identifier to lease6-get command
    cmd = {"command": "lease6-get", "arguments": {"subnet-id": 1, "identifier-type": "duid",
                                                  "identifier": "xxx"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'xxx' is not a valid string of hexadecimal digits"

    # sending wrong duid identifier to lease6-get command
    cmd = {"command": "lease6-get", "arguments": {"subnet-id": 1, "identifier-type": "duid",
                                                  "identifier": 2}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "No 'ip-address' provided and 'identifier' is either " \
                           "missing or not a string."

    # iaid
    # sending wrong iaid identifier to lease6-get command
    cmd = {"command": "lease6-get", "arguments": {"subnet-id": 1, "identifier-type": "duid",
                                                  "identifier": "00:03:00:01:66:55:44:33:22:11",
                                                  "iaid": ""}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "intValue() called on non-integer Element in (<wire>:0:25)"

    # sending wrong iaid identifier to lease6-get command
    cmd = {"command": "lease6-get", "arguments": {"subnet-id": 1, "identifier-type": "duid",
                                                  "identifier": "00:03:00:01:66:55:44:33:22:11",
                                                  "iaid": " "}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "intValue() called on non-integer Element in (<wire>:0:25)"

    # sending wrong iaid identifier to lease6-get command
    cmd = {"command": "lease6-get", "arguments": {"subnet-id": 1, "identifier-type": "duid",
                                                  "identifier": "00:03:00:01:66:55:44:33:22:11",
                                                  "iaid": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "intValue() called on non-integer Element in (<wire>:0:25)"

    # address
    # sending wrong address identifier to lease6-get command
    cmd = {"command": "lease6-get", "arguments": {"subnet-id": 1, "identifier-type": "address",
                                                  "identifier": 2}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "No 'ip-address' provided and 'identifier' is either " \
                           "missing or not a string."


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_v6_lease_cmds_update_negative():
    """
    Negative tests sending invalid or missing arguments to lease6-update
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # sending empty lease6-update command
    cmd = {"command": "lease6-update"}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "no parameters specified for lease6-update command"

    # sending no arguments in lease6-update command
    cmd = {"command": "lease6-update", "arguments": {}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "missing parameter 'ip-address' (<wire>:0:16)"

    # ip-address
    # sending wrong ip-address format to in lease6-update command
    cmd = {"command": "lease6-update", "arguments": {"ip-address": "xxx"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "Failed to convert 'xxx' to address: Failed to convert string " \
                           "to address 'xxx': Invalid argument(<wire>:0:31)"

    # sending wrong ip-address format to in lease6-update command
    cmd = {"command": "lease6-update", "arguments": {"ip-address": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'ip-address' (<wire>:0:31)"

    # sending wrong ip-address format to in lease6-update command
    cmd = {"command": "lease6-update", "arguments": {"ip-address": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'ip-address' (<wire>:0:31)"

    # duid
    # sending not enough arguments in lease6-update command
    cmd = {"command": "lease6-update", "arguments": {"ip-address": "2001:db8:1::1"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "missing parameter 'duid' (<wire>:0:16)"

    # sending wrong duid format to in lease6-update command
    cmd = {"command": "lease6-update", "arguments": {"ip-address": "2001:db8:1::1", "duid": "xxx"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'xxx' is not a valid string of hexadecimal digits"

    # sending wrong duid format to in lease6-update command
    cmd = {"command": "lease6-update", "arguments": {"ip-address": "2001:db8:1::1", "duid": " "}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "two consecutive separators (' ') specified in a decoded string ' '"

    # sending wrong duid format to in lease6-update command
    cmd = {"command": "lease6-update", "arguments": {"ip-address": "2001:db8:1::1", "duid": 2}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'duid' (<wire>:0:25)"

    # sending wrong duid format to in lease6-update command
    cmd = {"command": "lease6-update", "arguments": {"ip-address": "2001:db8:1::1", "duid": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'duid' (<wire>:0:25)"

    # subnet-id
    # sending ip out of subnet to lease6-update command
    cmd = {"command": "lease6-update", "arguments": {"ip-address": "2001:db8:2::1",
                                                     "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=4)
    assert resp["text"] == "subnet-id not specified and failed to find a subnet for " \
                           "address 2001:db8:2::1"

    # sending not enough arguments in lease6-update command
    cmd = {"command": "lease6-update", "arguments": {"ip-address": "2001:db8:1::1",
                                                     "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "missing parameter 'iaid' (<wire>:0:16)"

    # sending wrong subnet-id format to in lease6-update command
    cmd = {"command": "lease6-update", "arguments": {"ip-address": "2001:db8:1::1",
                                                     "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                     "subnet-id": 12345678901}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "out of range value (12345678901) specified for " \
                           "parameter 'subnet-id' (<wire>:0:105)"

    # sending wrong subnet-id format to in lease6-update command
    cmd = {"command": "lease6-update", "arguments": {"ip-address": "2001:db8:1::1",
                                                     "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                     "subnet-id": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'subnet-id' (<wire>:0:105)"

    # sending wrong subnet-id format to in lease6-update command
    cmd = {"command": "lease6-update", "arguments": {"ip-address": "2001:db8:1::1",
                                                     "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                     "subnet-id": "xxx"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'subnet-id' (<wire>:0:105)"

    # sending wrong subnet-id format to in lease6-update command
    cmd = {"command": "lease6-update", "arguments": {"ip-address": "2001:db8:1::1",
                                                     "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                     "subnet-id": " "}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'subnet-id' (<wire>:0:105)"

    # sending non-existent subnet-id to in lease6-update command
    cmd = {"command": "lease6-update", "arguments": {"ip-address": "2001:db8:1::1",
                                                     "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                     "subnet-id": 2}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=4)
    assert resp["text"] == "Invalid subnet-id: No IPv6 subnet with " \
                           "subnet-id=2 currently configured."

    # iaid
    # sending not enough arguments in lease6-update command
    cmd = {"command": "lease6-update", "arguments": {"ip-address": "2001:db8:1::1",
                                                     "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                     "subnet-id": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "missing parameter 'iaid' (<wire>:0:16)"

    # sending wrong iaid format to in lease6-update command
    cmd = {"command": "lease6-update", "arguments": {"ip-address": "2001:db8:1::1",
                                                     "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                     "subnet-id": 1,
                                                     "iaid": 12345678901}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "out of range value (12345678901) specified " \
                           "for parameter 'iaid' (<wire>:0:69)"

    # sending wrong iaid format to in lease6-update command
    cmd = {"command": "lease6-update", "arguments": {"ip-address": "2001:db8:1::1",
                                                     "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                     "subnet-id": 1,
                                                     "iaid": "1"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'iaid' (<wire>:0:69)"

    # sending wrong iaid format to in lease6-update command
    cmd = {"command": "lease6-update", "arguments": {"ip-address": "2001:db8:1::1",
                                                     "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                     "subnet-id": 1,
                                                     "iaid": "xxx"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'iaid' (<wire>:0:69)"

    # sending wrong iaid format to in lease6-update command
    cmd = {"command": "lease6-update", "arguments": {"ip-address": "2001:db8:1::1",
                                                     "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                     "subnet-id": 1,
                                                     "iaid": " "}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'iaid' (<wire>:0:69)"

    # sending wrong iaid format to in lease6-update command
    cmd = {"command": "lease6-update", "arguments": {"ip-address": "2001:db8:1::1",
                                                     "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                     "subnet-id": 1,
                                                     "iaid": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "invalid type specified for parameter 'iaid' (<wire>:0:69)"


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('file', ['overwrite', 'new'])
def test_v6_lease_cmds_write(file):
    """
    Check if lease6-write makes correct memfile.
    @param file: Select if memfile should be overwritten, or made as new file.
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # make sure that leases file is empty
    srv_msg.SA(address='2001:db8:1::1', duid='00:03:00:01:66:55:44:33:22:11')

    # prepare user-context JSON
    user_context = {
        "ISC": {
            "relay-info": [
                {
                    "hop": 0,
                    "link": "2001:db8:2::1000",
                    "options": "0x00120008706F727431323334",
                    "peer": "fe80::1"
                }
            ]
        },
        "version": [{"number": 1, "rev": 2}, {"id": 1, "no": 2}],
        "class": "!@#$%^&*(`)'_+=-?|\"\\\b\f\n\r\t",
        "tre,e": {"bra,nch1": {"treehouse": 1}, "bra,nch2": 2,
                  "bra,nch3": {"leaf1": 1,
                               "leaf2": ["vein1", "vein2"]}}
    }

    # adding lease by lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"subnet-id": 1,
                                                  "ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "iaid": 1234,
                                                  "hw-address": "1a:2b:3c:4d:5e:6f",
                                                  "preferred-lft": 500,
                                                  "valid-lft": 11111,
                                                  "fqdn-fwd": True,
                                                  "fqdn-rev": True,
                                                  "hostname": "urania.example.org",
                                                  "user-context": user_context}}
    srv_msg.send_ctrl_cmd(cmd)

    # checking if added lease exists in memfile
    srv_msg.check_leases({"duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                          "address": "2001:db8:1::1",
                          "iaid": 1234,
                          "hostname": "urania.example.org"})

    if file == 'overwrite':
        # Empty the memfile
        fabric_sudo_command(f'echo "Empty_File" > {world.f_cfg.get_leases_path()}')
        # Verify that memfile has no leases
        srv_msg.check_leases({"duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                              "address": "2001:db8:1::1",
                              "iaid": 1234,
                              "hostname": "urania.example.org"},
                             should_succeed=False)
        write_path = world.f_cfg.get_leases_path()
    else:  # file == new
        write_path = world.f_cfg.data_join('new-leases.csv')

    # checking if added lease is still in memory
    cmd = {"command": "lease6-get",
           "arguments": {"ip-address": "2001:db8:1::1", "type": "IA_NA"}}
    srv_msg.send_ctrl_cmd(cmd)

    # Execute lease6-write
    cmd = {"command": "lease6-write",
           "arguments": {"filename": write_path}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == f'IPv6 lease database into \'{write_path}\'.'

    # Check if lease file is restored
    srv_msg.check_leases({"duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                          "address": "2001:db8:1::1",
                          "iaid": 1234,
                          "hostname": "urania.example.org"})

    if file == 'overwrite':
        # Check if backup file is created
        cmd = {"command": "status-get", "arguments": {}}
        response = srv_msg.send_ctrl_cmd(cmd)
        pid = response['arguments']['pid']
        file_contains_line(f'{write_path}.bak{pid}', 'Empty_File')
    elif file == 'new':
        # Verify that new file contains lease
        file_contains_line(write_path, '2001:db8:1::1,1a:1b:1c:1d:1e:1f:20:21:22:23:24,11111')
        fabric_sudo_command(f'cp {write_path} {world.f_cfg.get_leases_path()}')

    srv_control.start_srv('DHCP', 'restarted')

    # checking if added lease is present after restart
    cmd = {"command": "lease6-get",
           "arguments": {"ip-address": "2001:db8:1::1", "type": "IA_NA"}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    resp = resp["arguments"]  # drop unnecessary info for comparison

    # compare sorted JSON prepared on start with sorted returned one
    assert sort_container(user_context) == sort_container(resp["user-context"])


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_v6_lease_cmds_write_no_persist():
    """
    Check if lease6-write makes correct memfile with persist: false.
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    world.dhcp_cfg.update({"lease-database": {"type": "memfile", "persist": False}})
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # make sure that leases file is empty
    srv_msg.SA(address='2001:db8:1::1', duid='00:03:00:01:66:55:44:33:22:11')

    # prepare user-context JSON
    user_context = {
        "ISC": {
            "relay-info": [
                {
                    "hop": 0,
                    "link": "2001:db8:2::1000",
                    "options": "0x00120008706F727431323334",
                    "peer": "fe80::1"
                }
            ]
        },
        "version": [{"number": 1, "rev": 2}, {"id": 1, "no": 2}],
        "class": "!@#$%^&*(`)'_+=-?|\"\\\b\f\n\r\t",
        "tre,e": {"bra,nch1": {"treehouse": 1}, "bra,nch2": 2,
                  "bra,nch3": {"leaf1": 1,
                               "leaf2": ["vein1", "vein2"]}}
    }

    # adding lease by lease6-add command
    cmd = {"command": "lease6-add", "arguments": {"subnet-id": 1,
                                                  "ip-address": "2001:db8:1::1",
                                                  "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                                                  "iaid": 1234,
                                                  "hw-address": "1a:2b:3c:4d:5e:6f",
                                                  "preferred-lft": 500,
                                                  "valid-lft": 11111,
                                                  "fqdn-fwd": True,
                                                  "fqdn-rev": True,
                                                  "hostname": "urania.example.org",
                                                  "user-context": user_context}}
    srv_msg.send_ctrl_cmd(cmd)

    # checking if added lease is in memory
    cmd = {"command": "lease6-get",
           "arguments": {"ip-address": "2001:db8:1::1", "type": "IA_NA"}}
    srv_msg.send_ctrl_cmd(cmd)

    # checking if added lease is absent in memfile
    srv_msg.check_leases({"duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                          "address": "2001:db8:1::1",
                          "iaid": 1234,
                          "hostname": "urania.example.org"},
                         should_succeed=False)

    # Execute lease4-write
    cmd = {"command": "lease6-write",
           "arguments": {"filename": world.f_cfg.get_leases_path()}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    assert resp["text"] == f'IPv6 lease database into \'{world.f_cfg.get_leases_path()}\'.'

    # Check if lease file is restored
    srv_msg.check_leases({"duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                          "address": "2001:db8:1::1",
                          "iaid": 1234,
                          "hostname": "urania.example.org"})

    # Restart with "persist": True
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'restarted')

    # checking if added lease is present after restart
    cmd = {"command": "lease6-get",
           "arguments": {"ip-address": "2001:db8:1::1", "type": "IA_NA"}}
    resp = srv_msg.send_ctrl_cmd(cmd)
    resp = resp["arguments"]  # drop unnecessary info for comparison

    # compare sorted JSON prepared on start with sorted returned one
    assert sort_container(user_context) == sort_container(resp["user-context"])


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_lease_cmds_write_negative(dhcp_version):
    """
    Test leaseX-write command negative responses
    """
    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    cmd = {"command": f'lease{dhcp_version[1]}-write'}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "no parameters specified for the command"

    cmd = {"command": f'lease{dhcp_version[1]}-write',
           "arguments": {}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'filename' parameter not specified"

    cmd = {"command": f'lease{dhcp_version[1]}-write',
           "arguments": {"test": 0}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'filename' parameter not specified"

    cmd = {"command": f'lease{dhcp_version[1]}-write',
           "arguments": {"filename": 0}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'filename' parameter must be a string"

    cmd = {"command": f'lease{dhcp_version[1]}-write',
           "arguments": {"filename": ""}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'filename' parameter is invalid: path: '' has no filename"


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_lease_cmds_write_path(dhcp_version):
    """
    Test leaseX-write command paths that it can write files to.

    :type dhcp_version: str
    :param dhcp_version: we accept v4 or v6
    """
    illegal_paths = [
        ['', 0, 'lease database into'],
        ['/tmp/', 1, '\'filename\' parameter is invalid: invalid path specified'],
        ['~/', 1, '\'filename\' parameter is invalid: invalid path specified'],
        ['/var/', 1, '\'filename\' parameter is invalid: invalid path specified'],
        ['/srv/', 1, '\'filename\' parameter is invalid: invalid path specified'],
        ['/etc/kea/', 1, '\'filename\' parameter is invalid: invalid path specified'],
    ]
    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    for path, exp_result, exp_text in illegal_paths:
        srv_msg.remove_file_from_server(path + 'kealeases.csv')
        cmd = {"command": f'lease{dhcp_version[1]}-write',
               "arguments": {"filename": path + 'kealeases.csv'}}
        resp = srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)
        assert exp_text in resp["text"], f"Expected {exp_text} in response, got {resp['text']}"
        if exp_result == 0:
            path = os.path.dirname(world.f_cfg.get_leases_path())
            verify_file_permissions(os.path.join(path, 'kealeases.csv'))
