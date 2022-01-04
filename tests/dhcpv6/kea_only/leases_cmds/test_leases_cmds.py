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

    # checking if leases are not available -
    # lease6-add should occupy the one and only lease from subnet
    srv_msg.SA(address='2001:db8:1::1', duid='00:03:00:01:66:55:44:33:22:11',
               status_code=DHCPv6_STATUS_CODES['NoAddrsAvail'])

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
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_hook_v6_lease_cmds_add_valid_with_options(backend):
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
    srv_msg.SA(address='2001:db8:1::1', duid='00:03:00:01:66:55:44:33:22:11',
               status_code=DHCPv6_STATUS_CODES['NoAddrsAvail'])

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
    assert resp["text"] == "Invalid subnet-id: No IPv6 subnet with " \
                           "subnet-id=11 currently configured."

    # checking ip outside of subnet
    cmd = {"command": "lease6-add",
           "arguments": {"subnet-id": 1,
                         "ip-address": "2001:db8:2::1",
                         "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
                         "iaid": 1234}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "The address 2001:db8:2::1 does not belong " \
                           "to subnet 2001:db8:1::/64, subnet-id=1"


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_hook_v6_lease_cmds_del_using_address(backend):
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
    srv_msg.SA(address='2001:db8:1::1', duid='00:03:00:01:66:55:44:33:55:66',
               status_code=DHCPv6_STATUS_CODES['NoAddrsAvail'])

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
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_hook_v6_lease_cmds_del_using_duid(backend):
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
    srv_msg.SA(address='2001:db8:1::1', duid='00:03:00:01:66:55:44:33:55:66',
               status_code=DHCPv6_STATUS_CODES['NoAddrsAvail'])

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
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_hook_v6_lease_cmds_get_using_address(backend):
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
    srv_msg.SA(address='2001:db8:1::1', duid='00:03:00:01:66:55:44:33:55:66',
               status_code=DHCPv6_STATUS_CODES['NoAddrsAvail'])

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
                                 "preferred-lft": 3000,
                                 "state": 0,
                                 "subnet-id": 1,
                                 "type": "IA_NA",
                                 "valid-lft": 4000}


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_hook_v6_lease_cmds_get_using_duid(backend):
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
    srv_msg.SA(address='2001:db8:1::1', duid='00:03:00:01:66:55:44:33:55:66',
               status_code=DHCPv6_STATUS_CODES['NoAddrsAvail'])

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
                                 "preferred-lft": 3000,
                                 "state": 0,
                                 "subnet-id": 1,
                                 "type": "IA_NA",
                                 "valid-lft": 4000}


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
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_hook_v6_lease_cmds_update(backend):
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
                                 "subnet-id": 1,
                                 "type": "IA_NA",
                                 "valid-lft": 1000}


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_hook_v6_lease_cmds_add_negative():
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
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
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
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
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
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_hook_v6_lease_cmds_add_options_negative():
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
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_hook_v6_lease_cmds_del_negative():
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
    assert resp["text"] == "Empty DUIDs are not allowed"

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
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_hook_v6_lease_cmds_get_negative():
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
    assert resp["text"] == "Empty DUIDs are not allowed"

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
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_hook_v6_lease_cmds_update_negative():
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
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
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
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
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
