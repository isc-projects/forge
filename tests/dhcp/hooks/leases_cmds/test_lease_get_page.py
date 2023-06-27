# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea lease-get-all and lease-get-page tests"""

import pytest

from src import misc
from src import srv_msg
from src import srv_control


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_control_channel_lease4_get_page_positive(backend):
    """
    Check correct responses of Kea lease-get-all and lease-get-page
    """
    misc.test_setup()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.14')
    srv_control.config_srv_another_subnet_no_interface('192.168.60.0/24', '192.168.60.5-192.168.60.14')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Check to see if lease4-get-all will return 0 leases
    cmd = {"command": "lease4-get-all",
           "arguments": {"subnets": [1]}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert resp["text"] == "0 IPv4 lease(s) found."

    cmd = {"command": "lease4-get-all"}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert resp["text"] == "0 IPv4 lease(s) found."

    # Check to see if lease4-get-page will return 0 leases
    cmd = {"command": "lease4-get-page",
           "arguments": {"from": "start", "limit": 10}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert resp["text"] == "0 IPv4 lease(s) found."

    # Add 10 leases to subnet 1
    for i in range(10):
        cmd = {"command": "lease4-add",
               "arguments": {"ip-address": "192.168.50." + str(i + 5),
                             "hw-address": "1a:1b:1c:1d:1e:" + f'{i + 5:02}'}}
        srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    # Check if lease4-get-all will return all added leases
    cmd = {"command": "lease4-get-all",
           "arguments": {"subnets": [1]}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    all_leases = resp["arguments"]["leases"]
    all_leases = sorted(all_leases, key=lambda d: d['hw-address'])

    for lease in all_leases:
        lease_nbr = all_leases.index(lease)
        del all_leases[lease_nbr]["cltt"]  # this value is dynamic so we delete it
        assert all_leases[lease_nbr] == {"fqdn-fwd": False,
                                         "fqdn-rev": False,
                                         "hostname": "",
                                         "hw-address": "1a:1b:1c:1d:1e:" + f'{lease_nbr + 5:02}',
                                         "ip-address": "192.168.50." + str(lease_nbr + 5),
                                         # "pool-id": 0, if id is 0 it's no longer returned
                                         "state": 0,
                                         "subnet-id": 1,
                                         "valid-lft": 4000
                                         }

        # let's add some leases for second subnet
    for i in range(10):
        cmd = {"command": "lease4-add",
               "arguments": {"ip-address": "192.168.60." + str(i + 5),
                             "hw-address": "2a:2b:2c:2d:2e:" + f'{i + 5:02}'}}
        srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    # Check if lease4-get-all will return all added leases in second subnet
    cmd = {"command": "lease4-get-all",
           "arguments": {"subnets": [2]}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    all_leases = resp["arguments"]["leases"]
    all_leases = sorted(all_leases, key=lambda d: d['hw-address'])

    for lease in all_leases:
        lease_nbr = all_leases.index(lease)
        del all_leases[lease_nbr]["cltt"]  # this value is dynamic so we delete it
        assert all_leases[lease_nbr] == {"fqdn-fwd": False,
                                         "fqdn-rev": False,
                                         "hostname": "",
                                         "hw-address": "2a:2b:2c:2d:2e:" + f'{lease_nbr + 5:02}',
                                         "ip-address": "192.168.60." + str(lease_nbr + 5),
                                         # "pool-id": 0, if id is 0 it's no longer returned
                                         "state": 0,
                                         "subnet-id": 2,
                                         "valid-lft": 4000
                                         }

    # let's get all leases from all subnets and check if they are all there
    cmd = {"command": "lease4-get-all"}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    all_leases = resp["arguments"]["leases"]
    all_leases = sorted(all_leases, key=lambda d: d['hw-address'])

    for lease in all_leases:
        lease_nbr = all_leases.index(lease)
        del all_leases[lease_nbr]["cltt"]  # this value is dynamic so we delete it
        if lease_nbr < 10:  # checking first 10 leases in subnet 1 and rest in subnet 2
            assert all_leases[lease_nbr] == {"fqdn-fwd": False,
                                             "fqdn-rev": False,
                                             "hostname": "",
                                             "hw-address": "1a:1b:1c:1d:1e:" + f'{lease_nbr + 5:02}',
                                             "ip-address": "192.168.50." + str(lease_nbr + 5),
                                             # "pool-id": 0, if id is 0 it's no longer returned
                                             "state": 0,
                                             "subnet-id": 1,
                                             "valid-lft": 4000
                                             }
        else:
            assert all_leases[lease_nbr] == {"fqdn-fwd": False,
                                             "fqdn-rev": False,
                                             "hostname": "",
                                             "hw-address": "2a:2b:2c:2d:2e:" + f'{lease_nbr - 5:02}',
                                             "ip-address": "192.168.60." + str(lease_nbr - 5),
                                             # "pool-id": 0, if id is 0 it's no longer returned
                                             "state": 0,
                                             "subnet-id": 2,
                                             "valid-lft": 4000
                                             }

    # let's get all leases from subnets 1 and 2 and check if they are all there
    cmd = {"command": "lease4-get-all",
           "arguments": {"subnets": [1, 2]}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    all_leases = resp["arguments"]["leases"]
    all_leases = sorted(all_leases, key=lambda d: d['hw-address'])

    for lease in all_leases:
        lease_nbr = all_leases.index(lease)
        del all_leases[lease_nbr]["cltt"]  # this value is dynamic so we delete it
        if lease_nbr < 10:  # checking first 10 leases in subnet 1 and rest in subnet 2
            assert all_leases[lease_nbr] == {"fqdn-fwd": False,
                                             "fqdn-rev": False,
                                             "hostname": "",
                                             "hw-address": "1a:1b:1c:1d:1e:" + f'{lease_nbr + 5:02}',
                                             "ip-address": "192.168.50." + str(lease_nbr + 5),
                                             # "pool-id": 0, if id is 0 it's no longer returned
                                             "state": 0,
                                             "subnet-id": 1,
                                             "valid-lft": 4000
                                             }
        else:
            assert all_leases[lease_nbr] == {"fqdn-fwd": False,
                                             "fqdn-rev": False,
                                             "hostname": "",
                                             "hw-address": "2a:2b:2c:2d:2e:" + f'{lease_nbr - 5:02}',
                                             "ip-address": "192.168.60." + str(lease_nbr - 5),
                                             # "pool-id": 0, if id is 0 it's no longer returned
                                             "state": 0,
                                             "subnet-id": 2,
                                             "valid-lft": 4000
                                             }

    # checking if lease4-get-page will return correct number of leases
    # with higher limit than number of leases
    cmd = {"command": "lease4-get-page",
           "arguments": {"limit": 100, "from": "start"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=0)
    assert len(all_leases) == 20 and resp["arguments"]["count"] == 20

    # checking if lease4-get-page returns leases in pages in span of 2 subnets
    per_page = 3
    counter = 0
    last_ip = ""
    cmd = {"command": "lease4-get-page",
           "arguments": {"limit": per_page, "from": "start"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    # write leases from all pages to "all_pages" buffer
    all_pages = []
    while 0 < resp["arguments"]["count"] <= per_page:
        all_leases = resp["arguments"]["leases"]
        for lease in all_leases:
            lease_nbr = all_leases.index(lease)
            del all_leases[lease_nbr]["cltt"]  # this value is dynamic so we delete it
            # add lease to buffer
            all_pages.append(all_leases[lease_nbr])
            # remember last ip to ask for next page
            last_ip = all_leases[lease_nbr]["ip-address"]
        counter += len(all_leases)
        # get next page
        cmd = {"command": "lease4-get-page",
               "arguments": {"limit": per_page, "from": last_ip}}
        resp = srv_msg.send_ctrl_cmd(cmd, exp_result=None)
    assert resp["result"] == 3 and resp["arguments"]["count"] == 0

    # Verify leases added to "all_pages" buffer
    all_pages = sorted(all_pages, key=lambda d: d['hw-address'])
    for lease in all_pages:
        lease_nbr = all_pages.index(lease)
        if lease_nbr < 10:  # subnet 1 and over 10th lease subnet 2
            assert all_pages[lease_nbr] == {"fqdn-fwd": False,
                                            "fqdn-rev": False,
                                            "hostname": "",
                                            "hw-address": "1a:1b:1c:1d:1e:" + f'{lease_nbr + 5:02}',
                                            "ip-address": "192.168.50." + str(
                                                lease_nbr + 5),
                                            # "pool-id": 0, if id is 0 it's no longer returned
                                            "state": 0,
                                            "subnet-id": 1,
                                            "valid-lft": 4000
                                            }
        else:
            assert all_pages[lease_nbr] == {"fqdn-fwd": False,
                                            "fqdn-rev": False,
                                            "hostname": "",
                                            "hw-address": "2a:2b:2c:2d:2e:" + f'{lease_nbr - 5:02}',
                                            "ip-address": "192.168.60." + str(lease_nbr - 5),
                                            # "pool-id": 0, if id is 0 it's no longer returned
                                            "state": 0,
                                            "subnet-id": 2,
                                            "valid-lft": 4000
                                            }


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_control_channel_lease4_get_page_negative():
    """
    Negative check for Kea lease-get-all and lease-get-page
    """
    misc.test_setup()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # lease4-get-all tests
    # Check to see if lease4-get-all will reply with subnets requirement
    cmd = {"command": "lease4-get-all",
           "arguments": {}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'subnets' parameter not specified"

    # Check to see if lease4-get-all will discard wrong parameter
    cmd = {"command": "lease4-get-all",
           "arguments": {"subnets": ["x"]}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "listed subnet identifiers must be numbers"

    # Check to see if lease4-get-all will discard wrong parameter
    cmd = {"command": "lease4-get-all",
           "arguments": {"subnets": "x"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'subnets' parameter must be a list"

    # Check to see if lease4-get-all will discard wrong parameter
    cmd = {"command": "lease4-get-all",
           "arguments": {"subnets": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'subnets' parameter must be a list"

    # lease4-get-page tests
    # Check if lease4-get-page without arguments section returns error
    cmd = {"command": "lease4-get-page"}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "no parameters specified for the lease4-get-page command"

    # Check if lease4-get-page without arguments returns error
    cmd = {"command": "lease4-get-page",
           "arguments": {}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'from' parameter not specified"

    # Check if lease4-get-page without limit argument returns error
    cmd = {"command": "lease4-get-page",
           "arguments": {"from": "start"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'limit' parameter not specified"

    # Check if lease4-get-page with wrong "from" argument returns error
    cmd = {"command": "lease4-get-page",
           "arguments": {"from": "x"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'from' parameter value is neither 'start' keyword nor a valid IPv4 address"

    # Check if lease4-get-page with wrong "from" argument returns error
    cmd = {"command": "lease4-get-page",
           "arguments": {"from": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'from' parameter must be a string"

    # Check if lease4-get-page with 0 "limit" argument returns error
    cmd = {"command": "lease4-get-page",
           "arguments": {"from": "start", "limit": 0}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "page size of retrieved leases must not be 0"

    # Check if lease4-get-page with 0 "limit" argument returns error
    cmd = {"command": "lease4-get-page",
           "arguments": {"from": "start", "limit": -5}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "page size of retrieved leases must not be greater than 4294967295"

    # Check if lease4-get-page with over max "limit" argument returns error
    cmd = {"command": "lease4-get-page",
           "arguments": {"from": "start", "limit": 4294967299}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "page size of retrieved leases must not be greater than 4294967295"

    # Check if lease4-get-page with wrong "limit" argument returns error
    cmd = {"command": "lease4-get-page",
           "arguments": {"from": "start", "limit": "x"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'limit' parameter must be a number"

    # Check if lease4-get-page with wrong "limit" argument returns error
    cmd = {"command": "lease4-get-page",
           "arguments": {"from": "start", "limit": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'limit' parameter must be a number"


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_v6_lease_get_page_positive(backend):
    """
    Check various options of lease6-get-page and lease6-get-all commands
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::10-2001:db8:1::21')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:2::/64',
                                                       '2001:db8:2::10-2001:db8:2::21')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # Check to see if lease6-get-all will return 0 leases
    cmd = {"command": "lease6-get-all",
           "arguments": {"subnets": [1]}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert resp["text"] == "0 IPv6 lease(s) found."

    cmd = {"command": "lease6-get-all"}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert resp["text"] == "0 IPv6 lease(s) found."

    # Check to see if lease6-get-page will return 0 leases
    cmd = {"command": "lease6-get-page",
           "arguments": {"from": "start", "limit": 10}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert resp["text"] == "0 IPv6 lease(s) found."

    # Add 10 leases to subnet 1
    for i in range(10):
        cmd = {"command": "lease6-add",
               "arguments": {"subnet-id": 1,
                             "ip-address": "2001:db8:1::" + str(i+10),
                             "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:" + f'{i+10:02}',
                             "iaid": 1230+i}}
        srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    # Check if lease6-get-all will return all added leases
    cmd = {"command": "lease6-get-all",
           "arguments": {"subnets": [1]}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    all_leases = resp["arguments"]["leases"]
    all_leases = sorted(all_leases, key=lambda d: d['duid'])
    for lease in all_leases:
        lease_nbr = all_leases.index(lease)
        del all_leases[lease_nbr]["cltt"]  # this value is dynamic so we delete it
        assert all_leases[lease_nbr] == {"duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:"
                                                 + f'{lease_nbr + 10:02}',
                                         "fqdn-fwd": False,
                                         "fqdn-rev": False,
                                         "hostname": "",
                                         "iaid": 1230 + lease_nbr,
                                         "ip-address": "2001:db8:1::" + str(lease_nbr+10),
                                         # "pool-id": 0, if id is 0 it's no longer returned
                                         "preferred-lft": 4000,
                                         "state": 0,
                                         "subnet-id": 1,
                                         "type": "IA_NA",
                                         "valid-lft": 4000}

    # let's add some leases for second subnet
    for i in range(10):
        cmd = {"command": "lease6-add",
               "arguments": {"subnet-id": 2,
                             "ip-address": "2001:db8:2::" + str(i+10),
                             "duid": "1a:1b:1c:1d:1e:1f:20:21:22:46:" + f'{i+10:02}',
                             "iaid": 2340+i}}
        srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    # Check if lease6-get-all will return all added leases in second subnet
    cmd = {"command": "lease6-get-all",
           "arguments": {"subnets": [2]}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=0)
    all_leases = resp["arguments"]["leases"]
    all_leases = sorted(all_leases, key=lambda d: d['duid'])
    for lease in all_leases:
        lease_nbr = all_leases.index(lease)
        del all_leases[lease_nbr]["cltt"]  # this value is dynamic so we delete it
        assert all_leases[lease_nbr] == {"duid": "1a:1b:1c:1d:1e:1f:20:21:22:46:"
                                                 + f'{lease_nbr + 10:02}',
                                         "fqdn-fwd": False,
                                         "fqdn-rev": False,
                                         "hostname": "",
                                         "iaid": 2340 + lease_nbr,
                                         "ip-address": "2001:db8:2::" + str(lease_nbr + 10),
                                         # "pool-id": 0, if id is 0 it's no longer returned
                                         "preferred-lft": 4000,
                                         "state": 0,
                                         "subnet-id": 2,
                                         "type": "IA_NA",
                                         "valid-lft": 4000}

    # let's get all leases from all subnets and check if they are all there
    cmd = {"command": "lease6-get-all"}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=0)
    all_leases = resp["arguments"]["leases"]
    all_leases = sorted(all_leases, key=lambda d: d['duid'])
    for lease in all_leases:
        lease_nbr = all_leases.index(lease)
        del all_leases[lease_nbr]["cltt"]  # this value is dynamic so we delete it
        if lease_nbr < 10:  # checking first 10 leases in subnet 1 and rest in subnet 2
            assert all_leases[lease_nbr] == {"duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:"
                                             + f'{lease_nbr + 10:02}',
                                             "fqdn-fwd": False,
                                             "fqdn-rev": False,
                                             "hostname": "",
                                             "iaid": 1230 + lease_nbr,
                                             "ip-address": "2001:db8:1::" + str(lease_nbr+10),
                                             # "pool-id": 0, if id is 0 it's no longer returned
                                             "preferred-lft": 4000,
                                             "state": 0,
                                             "subnet-id": 1,
                                             "type": "IA_NA",
                                             "valid-lft": 4000}
        else:
            assert all_leases[lease_nbr] == {"duid": "1a:1b:1c:1d:1e:1f:20:21:22:46:"
                                             + f'{lease_nbr:02}',
                                             "fqdn-fwd": False,
                                             "fqdn-rev": False,
                                             "hostname": "",
                                             "iaid": 2340 + lease_nbr - 10,
                                             "ip-address": "2001:db8:2::" + str(lease_nbr),
                                             # "pool-id": 0, if id is 0 it's no longer returned
                                             "preferred-lft": 4000,
                                             "state": 0,
                                             "subnet-id": 2,
                                             "type": "IA_NA",
                                             "valid-lft": 4000}

    # let's get all leases from subnets 1 and 2 and check if they are all there
    cmd = {"command": "lease6-get-all",
           "arguments": {"subnets": [1, 2]}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=0)
    all_leases = resp["arguments"]["leases"]
    all_leases = sorted(all_leases, key=lambda d: d['duid'])
    for lease in all_leases:
        lease_nbr = all_leases.index(lease)
        del all_leases[lease_nbr]["cltt"]  # this value is dynamic so we delete it
        if lease_nbr < 10:  # checking first 10 leases in subnet 1 and rest in subnet 2
            assert all_leases[lease_nbr] == {"duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:"
                                             + f'{lease_nbr + 10:02}',
                                             "fqdn-fwd": False,
                                             "fqdn-rev": False,
                                             "hostname": "",
                                             "iaid": 1230 + lease_nbr,
                                             "ip-address": "2001:db8:1::" + str(lease_nbr+10),
                                             # "pool-id": 0, if id is 0 it's no longer returned
                                             "preferred-lft": 4000,
                                             "state": 0,
                                             "subnet-id": 1,
                                             "type": "IA_NA",
                                             "valid-lft": 4000}
        else:
            assert all_leases[lease_nbr] == {"duid": "1a:1b:1c:1d:1e:1f:20:21:22:46:"
                                             + f'{lease_nbr:02}',
                                             "fqdn-fwd": False,
                                             "fqdn-rev": False,
                                             "hostname": "",
                                             "iaid": 2340 + lease_nbr - 10,
                                             "ip-address": "2001:db8:2::"
                                                           + str(lease_nbr),
                                             # "pool-id": 0, if id is 0 it's no longer returned
                                             "preferred-lft": 4000,
                                             "state": 0,
                                             "subnet-id": 2,
                                             "type": "IA_NA",
                                             "valid-lft": 4000}

    # checking if lease6-get-page will return correct number of leases with higher
    # limit than number of leases
    cmd = {"command": "lease6-get-page",
           "arguments": {"limit": 100, "from": "start"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=0)
    all_leases = resp["arguments"]["leases"]
    assert len(all_leases) == 20 and resp["arguments"]["count"] == 20

    # checking if lease6-get-page returns leases in pages in span of 2 subnets
    per_page = 3
    last_ip = ""
    cmd = {"command": "lease6-get-page",
           "arguments": {"limit": per_page, "from": "start"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    # write leases from all pages to "all_pages" buffer
    all_pages = []
    while 0 < resp["arguments"]["count"] <= per_page:
        all_leases = resp["arguments"]["leases"]
        for lease in all_leases:
            lease_nbr = all_leases.index(lease)
            del all_leases[lease_nbr]["cltt"]  # this value is dynamic so we delete it
            # add lease to buffer
            all_pages.append(all_leases[lease_nbr])
            # remember last ip to ask for next page
            last_ip = all_leases[lease_nbr]["ip-address"]
        # get next page
        cmd = {"command": "lease6-get-page",
               "arguments": {"limit": per_page, "from": last_ip}}
        resp = srv_msg.send_ctrl_cmd(cmd, exp_result=None)
    assert resp["result"] == 3 and resp["arguments"]["count"] == 0

    # Verify leases added to "all_pages" buffer
    all_pages = sorted(all_pages, key=lambda d: d['duid'])
    for lease in all_pages:
        lease_nbr = all_pages.index(lease)
        if lease_nbr < 10:  # subnet 1 and over 10th lease subnet 2
            assert all_pages[lease_nbr] == {"duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:"
                                                    + f'{lease_nbr + 10:02}',
                                            "fqdn-fwd": False,
                                            "fqdn-rev": False,
                                            "hostname": "",
                                            "iaid": 1230 + lease_nbr,
                                            "ip-address": "2001:db8:1::"
                                                          + str(lease_nbr + 10),
                                            # "pool-id": 0, if id is 0 it's no longer returned
                                            "preferred-lft": 4000,
                                            "state": 0,
                                            "subnet-id": 1,
                                            "type": "IA_NA",
                                            "valid-lft": 4000}
        else:
            assert all_pages[lease_nbr] == {"duid": "1a:1b:1c:1d:1e:1f:20:21:22:46:"
                                                    + f'{lease_nbr:02}',
                                            "fqdn-fwd": False,
                                            "fqdn-rev": False,
                                            "hostname": "",
                                            "iaid": 2340 + lease_nbr - 10,
                                            "ip-address": "2001:db8:2::"
                                                          + str(lease_nbr),
                                            # "pool-id": 0, if id is 0 it's no longer returned
                                            "preferred-lft": 4000,
                                            "state": 0,
                                            "subnet-id": 2,
                                            "type": "IA_NA",
                                            "valid-lft": 4000}


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_v6_lease_get_page_negative():
    """
    Negative check for Kea lease6-get-all and lease6-get-page
    """
    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # lease6-get-all tests
    # Check to see if lease6-get-all will reply with subnets requirement
    cmd = {"command": "lease6-get-all",
           "arguments": {}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'subnets' parameter not specified"

    # Check to see if lease6-get-all will discard wrong parameter
    cmd = {"command": "lease6-get-all",
           "arguments": {"subnets": ["x"]}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "listed subnet identifiers must be numbers"

    # Check to see if lease6-get-all will discard wrong parameter
    cmd = {"command": "lease6-get-all",
           "arguments": {"subnets": "x"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'subnets' parameter must be a list"

    # Check to see if lease6-get-all will discard wrong parameter
    cmd = {"command": "lease6-get-all",
           "arguments": {"subnets": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'subnets' parameter must be a list"

    # lease6-get-page tests
    # Check if lease6-get-page without arguments section returns error
    cmd = {"command": "lease6-get-page"}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "no parameters specified for the lease6-get-page command"

    # Check if lease6-get-page without arguments returns error
    cmd = {"command": "lease6-get-page",
           "arguments": {}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'from' parameter not specified"

    # Check if lease6-get-page without limit argument returns error
    cmd = {"command": "lease6-get-page",
           "arguments": {"from": "start"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'limit' parameter not specified"

    # Check if lease6-get-page with wrong "from" argument returns error
    cmd = {"command": "lease6-get-page",
           "arguments": {"from": "x"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'from' parameter value is neither 'start' " \
                           "keyword nor a valid IPv6 address"

    # Check if lease6-get-page with wrong "from" argument returns error
    cmd = {"command": "lease6-get-page",
           "arguments": {"from": 1}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'from' parameter must be a string"

    # Check if lease6-get-page with 0 "limit" argument returns error
    cmd = {"command": "lease6-get-page",
           "arguments": {"from": "start", "limit": 0}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "page size of retrieved leases must not be 0"

    # Check if lease6-get-page with 0 "limit" argument returns error
    cmd = {"command": "lease6-get-page",
           "arguments": {"from": "start", "limit": -5}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "page size of retrieved leases must not be greater than 4294967295"

    # Check if lease6-get-page with over max "limit" argument returns error
    cmd = {"command": "lease6-get-page",
           "arguments": {"from": "start", "limit": 4294967299}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "page size of retrieved leases must not be greater than 4294967295"

    # Check if lease6-get-page with wrong "limit" argument returns error
    cmd = {"command": "lease6-get-page",
           "arguments": {"from": "start", "limit": "x"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'limit' parameter must be a number"

    # Check if lease6-get-page with wrong "limit" argument returns error
    cmd = {"command": "lease6-get-page",
           "arguments": {"from": "start", "limit": True}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "'limit' parameter must be a number"
