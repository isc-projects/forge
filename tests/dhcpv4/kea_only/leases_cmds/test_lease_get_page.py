"""Kea lease-get-all and lease-get-page tests"""

# pylint: disable=invalid-name,line-too-long
import pytest

import misc
import srv_msg
import srv_control


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize("channel", ['socket', 'http'])
def test_control_channel_lease4_get_page(channel):
    """
     Check Kea lease-get-all and lease-get-page
     """
    misc.test_setup()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.14')
    srv_control.config_srv_another_subnet_no_interface('192.168.60.0/24', '192.168.60.5-192.168.60.14')
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

    for lease_nbr in range(len(resp["arguments"]["leases"])):
        del resp["arguments"]["leases"][lease_nbr]["cltt"]
        assert resp["arguments"]["leases"][lease_nbr] == {"fqdn-fwd": False,
                                                          "fqdn-rev": False,
                                                          "hostname": "",
                                                          "hw-address": "1a:1b:1c:1d:1e:" + f'{lease_nbr + 5:02}',
                                                          "ip-address": "192.168.50." + str(lease_nbr + 5),
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

    for lease_nbr in range(len(resp["arguments"]["leases"])):
        del resp["arguments"]["leases"][lease_nbr]["cltt"]
        assert resp["arguments"]["leases"][lease_nbr] == {"fqdn-fwd": False,
                                                          "fqdn-rev": False,
                                                          "hostname": "",
                                                          "hw-address": "2a:2b:2c:2d:2e:" + f'{lease_nbr + 5:02}',
                                                          "ip-address": "192.168.60." + str(lease_nbr + 5),
                                                          "state": 0,
                                                          "subnet-id": 2,
                                                          "valid-lft": 4000
                                                          }

    # let's get all leases from all subnets and check if they are all there
    cmd = {"command": "lease4-get-all"}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=0)
    for lease_nbr in range(len(resp["arguments"]["leases"])):
        del resp["arguments"]["leases"][lease_nbr]["cltt"]
        if lease_nbr < 10:  # subnet 1 and over 10th lease subnet 2
            assert resp["arguments"]["leases"][lease_nbr] == {"fqdn-fwd": False,
                                                              "fqdn-rev": False,
                                                              "hostname": "",
                                                              "hw-address": "1a:1b:1c:1d:1e:" + f'{lease_nbr + 5:02}',
                                                              "ip-address": "192.168.50." + str(lease_nbr + 5),
                                                              "state": 0,
                                                              "subnet-id": 1,
                                                              "valid-lft": 4000
                                                              }
        else:
            assert resp["arguments"]["leases"][lease_nbr] == {"fqdn-fwd": False,
                                                              "fqdn-rev": False,
                                                              "hostname": "",
                                                              "hw-address": "2a:2b:2c:2d:2e:" + f'{lease_nbr - 5:02}',
                                                              "ip-address": "192.168.60." + str(lease_nbr - 5),
                                                              "state": 0,
                                                              "subnet-id": 2,
                                                              "valid-lft": 4000
                                                              }

    # checking if lease4-get-page returns leases in pages in span of 2 subnets
    per_page = 3
    counter = 0
    last_ip = ""
    cmd = {"command": "lease4-get-page",
           "arguments": {"limit": per_page, "from": "start"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=0)
    while 0 < resp["arguments"]["count"] <= per_page:
        for lease_nbr in range(len(resp["arguments"]["leases"])):
            del resp["arguments"]["leases"][lease_nbr]["cltt"]
            if lease_nbr + counter < 10:  # subnet 1 and over 10th lease subnet 2
                assert resp["arguments"]["leases"][lease_nbr] == {"fqdn-fwd": False,
                                                                  "fqdn-rev": False,
                                                                  "hostname": "",
                                                                  "hw-address": "1a:1b:1c:1d:1e:" + f'{lease_nbr + counter + 5:02}',
                                                                  "ip-address": "192.168.50." + str(
                                                                      lease_nbr + counter + 5),
                                                                  "state": 0,
                                                                  "subnet-id": 1,
                                                                  "valid-lft": 4000
                                                                  }
            else:
                assert resp["arguments"]["leases"][lease_nbr] == {"fqdn-fwd": False,
                                                                  "fqdn-rev": False,
                                                                  "hostname": "",
                                                                  "hw-address": "2a:2b:2c:2d:2e:" + f'{lease_nbr + counter - 5:02}',
                                                                  "ip-address": "192.168.60." + str(
                                                                      lease_nbr + counter - 5),
                                                                  "state": 0,
                                                                  "subnet-id": 2,
                                                                  "valid-lft": 4000
                                                                  }
            last_ip = resp["arguments"]["leases"][lease_nbr]["ip-address"]
        counter += len(resp["arguments"]["leases"])

        cmd = {"command": "lease4-get-page",
               "arguments": {"limit": per_page, "from": last_ip}}
        resp = srv_msg.send_ctrl_cmd(cmd, exp_result=None)
    assert resp["result"] == 3 and resp["arguments"]["count"] == 0
