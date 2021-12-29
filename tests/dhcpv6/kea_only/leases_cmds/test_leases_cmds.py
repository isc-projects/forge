"""Kea leases manipulation commands"""

# pylint: disable=invalid-name,line-too-long,unused-argument

import pytest

import srv_msg
import misc
import srv_control

from dhcp4_scen import DHCPv6_STATUS_CODES

@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize("channel", ['socket', 'http'])
def test_hook_v6_lease_cmds_list(channel):
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
                "lease4-get-page",
                "lease4-update",
                "lease4-wipe",
                "lease6-add",
                "lease6-del",
                "lease6-get",
                "lease6-get-all",
                "lease6-get-by-duid",
                "lease6-get-by-hostname",
                "lease6-update",
                "lease6-wipe"]:
        assert cmd in resp["arguments"]


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_hook_v6_lease_cmds_add_valid(backend):
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

    # checking if leases are not available - lease6-add should occupy the one and only lease from subnet
    srv_msg.SA(address='2001:db8:1::1', duid='00:03:00:01:66:55:44:33:22:11', status_code=DHCPv6_STATUS_CODES['NoAddrsAvail'])

    # checking if lease exists in database
    srv_msg.check_leases({"duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                          "address": "2001:db8:1::1",
                          "valid_lifetime": 4000,
                          "iaid": 1234},
                         backend=backend)


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_hook_v6_lease_cmds_add_expired_with_options(backend):
    """
    Add expired lease using lease6-add with additional options, check with Solicit and check content of database/lease file
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
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_hook_v6_lease_cmds_add_valid_with_options(backend):
    """
    Add valid lease using lease6-add with additional options, check with Solicit and check content of database/lease file
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
    srv_msg.SA(address='2001:db8:1::1', duid='00:03:00:01:66:55:44:33:22:11', status_code=DHCPv6_STATUS_CODES['NoAddrsAvail'])

    # checking if added lease is got by Control Agent
    cmd = {"command": "lease6-get",
           "arguments": {"ip-address": "2001:db8:1::1","type": "IA_NA"}}
    srv_msg.send_ctrl_cmd(cmd)

    # checking if added lease exists in database
    srv_msg.check_leases({"duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                          "address": "2001:db8:1::1",
                          "iaid": 1234,
                          "hostname": "urania.example.org"},
                         backend=backend)


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_hook_v6_lease_cmds_add_notvalid():
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
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "Invalid subnet-id: No IPv6 subnet with subnet-id=11 currently configured."

    # checking ip outside of subnet
    cmd = {"command": "lease6-add",
           "arguments": {"subnet-id": 1,
                         "ip-address": "2001:db8:2::1",
                         "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                         "iaid": 1234}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "The address 2001:db8:2::1 does not belong to subnet 2001:db8:1::/64, subnet-id=1"


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_hook_v6_lease_cmds_del_using_address():
    """
    Get lease by SARR, delete it with lease6-del and check if it is available again
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # Get lease
    srv_msg.SARR(address='2001:db8:1::1', duid='00:03:00:01:66:55:44:33:22:11')

    # be sure none are left
    srv_msg.SA(address='2001:db8:1::1', duid='00:03:00:01:66:55:44:33:55:66', status_code=DHCPv6_STATUS_CODES['NoAddrsAvail'])

    # delete lease
    cmd = {"command": "lease6-del",
           "arguments": {"ip-address": "2001:db8:1::1"}}
    srv_msg.send_ctrl_cmd(cmd)

    # check if leases are available
    srv_msg.SA(address='2001:db8:1::1', duid='00:03:00:01:66:55:44:33:55:66')


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_hook_v6_lease_cmds_del_using_duid():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_sets_value('Client', 'ia_id', 666)
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
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
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
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)

    srv_msg.send_ctrl_cmd_via_socket('{"command":"lease6-del","arguments":{"subnet-id":1,"identifier": "00:03:00:01:66:55:44:33:22:11","identifier-type": "duid","iaid":666}}')
    # Using UNIX socket on server in path control_socket send {"command":"lease6-get","arguments":{"ip-address": "2001:db8:1::1"}}

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
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_hook_v6_lease_cmds_get_using_address():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
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
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
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
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)

    srv_msg.send_ctrl_cmd_via_socket('{"command":"lease6-get","arguments":{"ip-address": "2001:db8:1::1"}}')


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_hook_v6_lease_cmds_get_using_duid():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_sets_value('Client', 'ia_id', 666)
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
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"lease6-get","arguments":{"subnet-id":1,"identifier": "00:03:00:01:66:55:44:33:22:11","identifier-type": "duid","iaid":666}}')


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_hook_v6_lease_cmds_wipe():
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
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_hook_v6_lease_cmds_update():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::2')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_sets_value('Client', 'ia_id', 666)
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

    srv_msg.lease_file_contains('2001:db8:1::1,00:03:00:01:66:55:44:33:22:11,4000,')
    srv_msg.lease_file_contains(',1,3000,0,666,128,0,0,,66:55:44:33:22:11,0')

    srv_msg.lease_file_doesnt_contain('2001:db8:1::1,01:02:03:04:05:06:07:08')
    srv_msg.lease_file_doesnt_contain(',urania.example.org,1a:1b:1c:1d:1e:1f,')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"lease6-update", "arguments":{"subnet-id": 1,"ip-address": "2001:db8:1::1","duid": "01:02:03:04:05:06:07:08","iaid": 1234,"hw-address": "1a:1b:1c:1d:1e:1f","preferred-lft": 500,"valid-lft": 1000,"hostname": "urania.example.org"}}')
    srv_msg.lease_file_contains(',1,500,0,1234,128,0,0,urania.example.org,1a:1b:1c:1d:1e:1f,0')
    srv_msg.lease_file_contains('2001:db8:1::1,01:02:03:04:05:06:07:08,1000')
