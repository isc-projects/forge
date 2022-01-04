"""Kea leases manipulation commands"""

# pylint: disable=invalid-name,line-too-long,unused-argument
import time
import pytest

import misc
import srv_msg
import srv_control


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
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize("channel", ['socket', 'http'])
def test_hook_lease_cmds_list(channel):
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
                "leases-reclaim"]:
        assert cmd in resp["arguments"]


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_hook_v4_lease_cmds_update(backend):
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
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_hook_v4_lease_cmds_get():
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
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_hook_v4_lease_cmds_add(backend):
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
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
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
                    "state": 0,
                    "subnet-id": 1,
                    "valid-lft": 1111}

    # and now check database/lease file directly
    leases_lst = [{"hwaddr": "ff:01:02:03:ff:04", "address": "192.168.50.5", "valid_lifetime": 999},
                  {"hwaddr": "ff:01:02:03:ff:04", "address": "192.168.150.50", "valid_lifetime": 2222},
                  {"hwaddr": "ff:01:02:03:04:05", "address": "192.168.50.150", "valid_lifetime": 1111}]
    srv_msg.check_leases(leases_lst, backend=backend)


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_hook_v4_lease_cmds_add_with_additional_values(backend):
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
                    "state": 1,
                    "subnet-id": 1,
                    "valid-lft": 7777}
    srv_msg.check_leases({"hwaddr": "1a:1b:1c:1d:1e:1f", "address": "192.168.50.5", "valid_lifetime": 7777},
                         backend=backend)


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_hook_v4_lease_cmds_del(backend):
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
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
@pytest.mark.parametrize('backend', ['memfile'])
def test_hook_v4_lease_cmds_wipe(backend):
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
    assert resp["text"] == "Deleted 2 IPv4 lease(s) from subnet(s) 1"

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
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_hook_v4_lease_cmds_lease_add_negative():
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
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert resp["text"] == "Invalid subnet-id: No IPv4 subnet with subnet-id=44 currently configured."

    cmd = {"command": "lease4-add",
           "arguments": {"subnet-id": 1,
                         "ip-address": "192.0.0.5",
                         "hw-address": "1a:1b:1c:1d:1e:1f"}}
    resp = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
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
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.lease_cmds
def test_hook_v4_lease_cmds_lease_get_negative():
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
    #TODO: test fails, kea#2260

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
