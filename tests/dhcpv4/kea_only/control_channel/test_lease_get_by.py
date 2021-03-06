"""Kea Control Channel - socket"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_msg
import srv_control
from forge_cfg import world


def _send_cmd(cmd, extra_param=None, exp_result=0):
    cmd = dict(command=cmd, arguments={})
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


# lease4-get-by-client-id, lease4-get-by-hostname, lease4-get-by-hw-adderss
@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_lease4_get_by():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.6')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.10-192.168.51.11')

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
    srv_control.open_control_channel()

    srv_control.add_ddns_server('127.0.0.1', 53001)
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _get_address("08:08:08:08:08:08", "192.168.50.5", cli_id="00010203040506", fqdn="four.hostname.com.")
    _get_address("09:09:09:09:09:09", "192.168.50.6", cli_id="00010203040507")
    _get_address("10:10:10:10:10:10", "192.168.51.10")
    _get_address("11:11:11:11:11:11", "192.168.51.11", fqdn="xyz.com.")

    # let's get 08:08:08:08:08:08 for in a different ways
    by_id_1 = _send_cmd("lease4-get-by-client-id", extra_param={"client-id": "00010203040506"})
    del by_id_1["arguments"]["leases"][0]["cltt"]
    assert by_id_1["arguments"]["leases"][0] == {"fqdn-fwd": True,
                                                 "fqdn-rev": True,
                                                 "client-id": "00:01:02:03:04:05:06",
                                                 "hostname": "four.hostname.com.",
                                                 "hw-address": "08:08:08:08:08:08",
                                                 "ip-address": "192.168.50.5",
                                                 "state": 0,
                                                 "subnet-id": 1,
                                                 "valid-lft": 4000}

    by_host_1 = _send_cmd("lease4-get-by-hostname", extra_param={"hostname": "four.hostname.com."})
    del by_host_1["arguments"]["leases"][0]["cltt"]
    assert by_host_1["arguments"]["leases"][0] == {"fqdn-fwd": True,
                                                   "fqdn-rev": True,
                                                   "client-id": "00:01:02:03:04:05:06",
                                                   "hostname": "four.hostname.com.",
                                                   "hw-address": "08:08:08:08:08:08",
                                                   "ip-address": "192.168.50.5",
                                                   "state": 0,
                                                   "subnet-id": 1,
                                                   "valid-lft": 4000}
    by_hw_1 = _send_cmd("lease4-get-by-hw-address", extra_param={"hw-address": "08:08:08:08:08:08"})
    del by_hw_1["arguments"]["leases"][0]["cltt"]
    assert by_hw_1["arguments"]["leases"][0] == {"fqdn-fwd": True,
                                                 "fqdn-rev": True,
                                                 "client-id": "00:01:02:03:04:05:06",
                                                 "hostname": "four.hostname.com.",
                                                 "hw-address": "08:08:08:08:08:08",
                                                 "ip-address": "192.168.50.5",
                                                 "state": 0,
                                                 "subnet-id": 1,
                                                 "valid-lft": 4000}

    # let's get 09:09:09:09:09:09 for in a different ways
    by_id_1 = _send_cmd("lease4-get-by-client-id", extra_param={"client-id": "00010203040507"})
    del by_id_1["arguments"]["leases"][0]["cltt"]
    assert by_id_1["arguments"]["leases"][0] == {"fqdn-fwd": False,
                                                 "fqdn-rev": False,
                                                 "client-id": "00:01:02:03:04:05:07",
                                                 "hw-address": "09:09:09:09:09:09",
                                                 "ip-address": "192.168.50.6",
                                                 "hostname": "",
                                                 "state": 0,
                                                 "subnet-id": 1,
                                                 "valid-lft": 4000}

    by_hw_1 = _send_cmd("lease4-get-by-hw-address", extra_param={"hw-address": "09:09:09:09:09:09"})
    del by_hw_1["arguments"]["leases"][0]["cltt"]
    assert by_hw_1["arguments"]["leases"][0] == {"fqdn-fwd": False,
                                                 "fqdn-rev": False,
                                                 "client-id": "00:01:02:03:04:05:07",
                                                 "hw-address": "09:09:09:09:09:09",
                                                 "ip-address": "192.168.50.6",
                                                 "hostname": "",
                                                 "state": 0,
                                                 "subnet-id": 1,
                                                 "valid-lft": 4000}

    # let's get 11:11:11:11:11:11 for in a different ways
    # THOSE TWO ARE FAILING
    by_host_1 = _send_cmd("lease4-get-by-hostname", extra_param={"hostname": "xyz.com."})
    del by_host_1["arguments"]["leases"][0]["cltt"]
    assert by_host_1["arguments"]["leases"][0] == {"fqdn-fwd": False,
                                                   "fqdn-rev": False,
                                                   # "client-id": "", #TODO I think it should be added
                                                   "hostname": "xyz.com.",
                                                   "hw-address": "11:11:11:11:11:11",
                                                   "ip-address": "192.168.51.11",
                                                   "state": 0,
                                                   "subnet-id": 2,
                                                   "valid-lft": 4000}
    by_hw_1 = _send_cmd("lease4-get-by-hw-address", extra_param={"hw-address": "11:11:11:11:11:11"})
    del by_hw_1["arguments"]["leases"][0]["cltt"]
    assert by_hw_1["arguments"]["leases"][0] == {"fqdn-fwd": False,
                                                 "fqdn-rev": False,
                                                 # "client-id": "", #TODO I think it should be added
                                                 "hostname": "xyz.com.",
                                                 "hw-address": "11:11:11:11:11:11",
                                                 "ip-address": "192.168.51.11",
                                                 "state": 0,
                                                 "subnet-id": 2,
                                                 "valid-lft": 4000}

    by_hw_1 = _send_cmd("lease4-get-by-hw-address", extra_param={"hw-address": "10:10:10:10:10:10"})
    del by_hw_1["arguments"]["leases"][0]["cltt"]
    assert by_hw_1["arguments"]["leases"][0] == {"fqdn-fwd": False,
                                                 "fqdn-rev": False,
                                                 # "client-id": "", #TODO I think it should be added
                                                 "hw-address": "10:10:10:10:10:10",
                                                 "ip-address": "192.168.51.10",
                                                 "hostname": "",
                                                 "state": 0,
                                                 "subnet-id": 2,
                                                 "valid-lft": 4000}

    _send_cmd("lease4-get-by-hw-address", extra_param={"hw-address": "11:11:12:12:13:13"}, exp_result=3)
    _send_cmd("lease4-get-by-hostname", extra_param={"hostname": "abc.com."}, exp_result=3)
    _send_cmd("lease4-get-by-client-id", extra_param={"client-id": "111111111111"}, exp_result=3)

    _send_cmd("lease4-get-by-hw-address", exp_result=1)
    _send_cmd("lease4-get-by-hostname", exp_result=1)
    _send_cmd("lease4-get-by-client-id", exp_result=1)
