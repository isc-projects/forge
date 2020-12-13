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


def _get_address(duid, address, ia_id, ia_pd=None, fqdn=None, flags='S'):
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', ia_id)
    srv_msg.client_does_include('Client', 'IA-NA')
    if ia_pd is not None:
        srv_msg.client_sets_value('Client', 'ia_pd', ia_pd)
        srv_msg.client_does_include('Client', 'IA-PD')
    if fqdn is not None:
        srv_msg.client_sets_value('Client', 'FQDN_domain_name', fqdn)
        srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
        srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', address)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    if ia_pd is not None:
        srv_msg.client_copy_option('IA_PD')
    if fqdn is not None:
        srv_msg.client_sets_value('Client', 'FQDN_domain_name', fqdn)
        srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
        srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', address)
    if fqdn is not None:
        srv_msg.response_check_include_option(39)
        srv_msg.response_check_option_content(39, 'flags', flags)
        srv_msg.response_check_option_content(39, 'fqdn', fqdn)


# lease6-get-by-duid, lease6-get-by-hostname
@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_lease6_get_by():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::5-2001:db8:a::6')
    srv_control.config_srv_prefix('2000::', 0, 90, 96)
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::10-2001:db8:b::11')
    srv_control.config_srv_prefix('2001::', 1, 90, 96)

    world.dhcp_cfg.update({"ddns-send-updates": False})
    world.dhcp_cfg["subnet6"][0].update({"ddns-send-updates": True,
                                         "ddns-generated-prefix": "six",
                                         "ddns-qualifying-suffix": "example.com"})
    world.dhcp_cfg["subnet6"][1].update({"ddns-send-updates": False})

    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.shared_subnet('2001:db8:b::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.open_control_channel()

    srv_control.add_ddns_server('127.0.0.1', 53001)
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_forward_ddns('six.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('a.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'EMPTY_KEY')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    _get_address("00:03:00:01:08:08:08:08:08:08", "2001:db8:a::5", ia_id=5, fqdn="six.hostname.com.")
    _get_address("00:03:00:01:09:09:09:09:09:09", "2001:db8:a::6", ia_pd=1, ia_id=6)
    _get_address("00:03:00:01:10:10:10:10:10:10", "2001:db8:b::10", ia_id=10)
    _get_address("00:03:00:01:11:11:11:11:11:11", "2001:db8:b::11", fqdn="xyz.com.", ia_id=11, flags='ON')

    by_id_1 = _send_cmd("lease6-get-by-duid", extra_param={"duid": "00:03:00:01:08:08:08:08:08:08"})
    del by_id_1["arguments"]["leases"][0]["cltt"]
    assert by_id_1["arguments"]["leases"][0] == {"fqdn-fwd": True,
                                                 "fqdn-rev": True,
                                                 "hw-address": "08:08:08:08:08:08",
                                                 "hostname": "six.hostname.com.",
                                                 "duid": "00:03:00:01:08:08:08:08:08:08",
                                                 "ip-address": "2001:db8:a::5",
                                                 "iaid": 5,
                                                 "preferred-lft": 3000,
                                                 "type": "IA_NA",
                                                 "state": 0,
                                                 "subnet-id": 1,
                                                 "valid-lft": 4000}

    by_host_1 = _send_cmd("lease6-get-by-hostname", extra_param={"hostname": "six.hostname.com."})
    del by_host_1["arguments"]["leases"][0]["cltt"]
    assert by_host_1["arguments"]["leases"][0] == {"fqdn-fwd": True,
                                                   "fqdn-rev": True,
                                                   "hw-address": "08:08:08:08:08:08",
                                                   "hostname": "six.hostname.com.",
                                                   "duid": "00:03:00:01:08:08:08:08:08:08",
                                                   "ip-address": "2001:db8:a::5",
                                                   "iaid": 5,
                                                   "preferred-lft": 3000,
                                                   "type": "IA_NA",
                                                   "state": 0,
                                                   "subnet-id": 1,
                                                   "valid-lft": 4000}

    by_id_1 = _send_cmd("lease6-get-by-duid", extra_param={"duid": "00:03:00:01:09:09:09:09:09:09"})
    assert len(by_id_1["arguments"]["leases"]) == 2
    for lease in by_id_1["arguments"]["leases"]:
        del lease["cltt"]
    for lease in by_id_1["arguments"]["leases"]:
        if lease["ip-address"] == "2001:db8:a::6":
            assert lease == {"fqdn-fwd": False,
                             "fqdn-rev": False,
                             "duid": "00:03:00:01:09:09:09:09:09:09",
                             "ip-address": "2001:db8:a::6",
                             "hostname": "",
                             "hw-address": "09:09:09:09:09:09",
                             "state": 0,
                             "subnet-id": 1,
                             "iaid": 6,
                             "preferred-lft": 3000,
                             "type": "IA_NA",
                             "valid-lft": 4000}

        elif lease["ip-address"] == "2000::":
            assert lease == {"duid": "00:03:00:01:09:09:09:09:09:09",
                             "fqdn-fwd": False,
                             "fqdn-rev": False,
                             "hostname": "",
                             "hw-address": "09:09:09:09:09:09",
                             "iaid": 1,
                             "ip-address": "2000::",
                             "preferred-lft": 3000,
                             "prefix-len": 96,
                             "state": 0,
                             "subnet-id": 1,
                             "type": "IA_PD",
                             "valid-lft": 4000}

    by_id_1 = _send_cmd("lease6-get-by-duid", extra_param={"duid": "00:03:00:01:11:11:11:11:11:11"})
    del by_id_1["arguments"]["leases"][0]["cltt"]
    assert by_id_1["arguments"]["leases"][0] == {"fqdn-fwd": False,
                                                 "fqdn-rev": False,
                                                 "hw-address": "11:11:11:11:11:11",
                                                 "hostname": "xyz.com.",
                                                 "duid": "00:03:00:01:11:11:11:11:11:11",
                                                 "ip-address": "2001:db8:b::11",
                                                 "iaid": 11,
                                                 "preferred-lft": 3000,
                                                 "type": "IA_NA",
                                                 "state": 0,
                                                 "subnet-id": 2,
                                                 "valid-lft": 4000}

    _send_cmd("lease6-get-by-hostname", extra_param={"hostname": "abc.com."}, exp_result=3)
    _send_cmd("lease6-get-by-duid", extra_param={"duid": "00:03:00:01:12:12:12:11:11:11"}, exp_result=3)

    _send_cmd("lease6-get-by-hostname", exp_result=1)
    _send_cmd("lease6-get-by-duid", exp_result=1)
