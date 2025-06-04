# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

""" testing lease caching for all backends """

# pylint: disable=unused-argument

import pytest

from src import srv_msg
from src import srv_control
from src import misc

from src.forge_cfg import world


def _get_config(exp_result=0):
    cmd = dict(command="config-get")
    return srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result, channel='socket')


def _get_cltt_from_lease(address, subnet_id=1):
    cmd = dict(command="lease6-get", arguments={"ip-address": address, "subnet-id": subnet_id})
    return srv_msg.send_ctrl_cmd(cmd, channel='socket')["arguments"]["cltt"]


def _assign_lease(duid, address, fqdn=None):
    world.savedmsg = {}
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.client_save_option('server-id')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_add_saved_option()
    if fqdn:
        srv_msg.client_sets_value('Client', 'FQDN_domain_name', fqdn)
        srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
        srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', address)


def _renew_address(duid, address, fqdn=None):
    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_does_include('Client', 'client-id')
    if fqdn:
        srv_msg.client_sets_value('Client', 'FQDN_domain_name', fqdn)
        srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
        srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', address)


def _rebind_address(duid, address, fqdn=None):
    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_does_include('Client', 'client-id')
    if fqdn:
        srv_msg.client_sets_value('Client', 'FQDN_domain_name', fqdn)
        srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
        srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_send_msg('REBIND')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', address)


@pytest.mark.v6
@pytest.mark.v4
@pytest.mark.parametrize("parameter", ["cache-threshold", "cache-max-age"])
@pytest.mark.parametrize("value", ["abc", True])
def test_lease_cache_incorrect_values(dhcp_version, parameter, value):
    # both for v4 and v6, we don't need to repeat this tests in v4 set
    ver = int(world.proto[1])
    misc.test_setup()
    srv_control.add_unix_socket()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    if ver == 4:
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    else:
        srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    cache = {parameter: value}
    world.dhcp_cfg[f'subnet{ver}'][0].update(cache)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started', should_succeed=False)


@pytest.mark.v6
@pytest.mark.parametrize("backend", ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize("parameter", [{}, {"cache-max-age": 0}])  # , {"cache-threshold": .0} temporary removed
def test_lease_cache_disabled(backend, parameter):
    # let's test is as disabled in configurations:
    # - not configured
    # - "cache-threshold": 0 which means disabled according to docs, but kea fail to start gitlab #1796
    # - "cache-max-age": 0 means disabled
    misc.test_setup()
    srv_control.add_unix_socket()
    world.dhcp_cfg.update(parameter)
    world.dhcp_cfg.update({"preferred-lifetime": 10, "rebind-timer": 10,
                           "renew-timer": 10, "valid-lifetime": 10})
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.define_lease_db_backend(backend)
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    # Disable lease cache
    world.dhcp_cfg.update({'cache-threshold': 0.0})
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    address = "2001:db8:a::1"
    _assign_lease("00:03:00:01:01:02:03:04:05:06", address)
    assign_time = _get_cltt_from_lease(address)

    # let's wait 1 second, if we would renew immediately, we could have new entry with the same value.
    srv_msg.forge_sleep(1, "seconds")
    _renew_address("00:03:00:01:01:02:03:04:05:06", address)
    renew_time = _get_cltt_from_lease(address)
    assert renew_time > assign_time, "Received CLTT should be grater than previous value"

    srv_msg.forge_sleep(1, "seconds")
    _rebind_address("00:03:00:01:01:02:03:04:05:06", address)
    rebind_time = _get_cltt_from_lease(address)
    assert rebind_time > renew_time, "Received CLTT should be grater than previous value"


@pytest.mark.v6
@pytest.mark.parametrize("parameter", [{"cache-threshold": 0.5}, {"cache-max-age": 5}])
@pytest.mark.parametrize("backend", ['memfile', 'mysql', 'postgresql'])
def test_lease_cache_enabled(backend, parameter):
    misc.test_setup()
    srv_control.add_unix_socket()
    srv_control.define_lease_db_backend(backend)
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    address = "2001:db8:a::1"
    world.dhcp_cfg.update(parameter)
    # for a sake of testing we will set all timers to one value, both cache threshold
    # are set to the same value, 50% (which is 5s in this case) and 5 seconds
    world.dhcp_cfg.update({"preferred-lifetime": 10, "rebind-timer": 10,
                           "renew-timer": 10, "valid-lifetime": 10})

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _assign_lease("00:03:00:01:01:02:03:04:05:06", address)
    assign_time = _get_cltt_from_lease(address)

    # renewed address should not have higher CLTT - no entry to db
    _renew_address("00:03:00:01:01:02:03:04:05:06", address)
    renew_time = _get_cltt_from_lease(address)
    assert renew_time == assign_time, "Received CLTT should be equal to previous value"

    # rebind address should not have higher CLTT - no entry to db
    _rebind_address("00:03:00:01:01:02:03:04:05:06", address)
    rebind_time = _get_cltt_from_lease(address)
    assert rebind_time == renew_time == assign_time, "Received CLTT should be equal to previous values"

    srv_msg.forge_sleep(7, "seconds")
    # now we will reach cache threshold limit and renew should have new entry
    _renew_address("00:03:00:01:01:02:03:04:05:06", address)
    renew_time = _get_cltt_from_lease(address)
    assert renew_time > assign_time, "Received CLTT should be grater than assign value"

    # let's rebind address that was renewed, we still should have the same value
    srv_msg.forge_sleep(2, "seconds")
    _rebind_address("00:03:00:01:01:02:03:04:05:06", address)
    rebind_time = _get_cltt_from_lease(address)
    assert rebind_time == renew_time > assign_time, \
        "Received CLTT should be equal to value got on renew but higher than on assign"

    # let's timeout threshold and rebind address
    srv_msg.forge_sleep(5, "seconds")
    _rebind_address("00:03:00:01:01:02:03:04:05:06", address)
    rebind_time = _get_cltt_from_lease(address)
    assert rebind_time > renew_time > assign_time, "Received CLTT should be highest"

    # let's renew and rebind address with different fqdn, that should disable cache
    _assign_lease("00:03:00:01:01:02:03:04:05:06", address)
    assign_time = _get_cltt_from_lease(address)

    # we need sleep to be sure we get different value than before
    srv_msg.forge_sleep(1, "seconds")

    # renewed address with new fqdn should have higher CLTT - new entry to db
    _renew_address("00:03:00:01:01:02:03:04:05:06", address, fqdn="abc")
    renew_time = _get_cltt_from_lease(address)
    assert renew_time > assign_time, "Received CLTT should be higher than on assign"

    # we need sleep to get different value than before
    srv_msg.forge_sleep(2, "seconds")

    # rebind address with new fqdn should have higher CLTT - new entry to db
    _rebind_address("00:03:00:01:01:02:03:04:05:06", address, fqdn="xyz")
    rebind_time = _get_cltt_from_lease(address)
    assert rebind_time > renew_time > assign_time, "Received CLTT should be highest"


@pytest.mark.v6
@pytest.mark.parametrize("backend", ['memfile', 'mysql', 'postgresql'])
def test_lease_cache_different_levels(backend):
    # everywhere we have the same validlifetime, but different cache values on each level
    # on global, shared network and subnet, with 3 subnets based on classification
    misc.test_setup()
    srv_control.create_new_class('Client_Class_1')
    srv_control.add_test_to_class(1, 'test', 'option[1].hex == 0x00030001665544332211')
    srv_control.create_new_class('Client_Class_2')
    srv_control.add_test_to_class(2, 'test', 'option[1].hex == 0x00030001112233445566')
    srv_control.create_new_class('Client_Class_3')
    srv_control.add_test_to_class(3, 'test', 'option[1].hex == 0x00030001111122222211')
    srv_control.add_unix_socket()
    srv_control.define_lease_db_backend(backend)
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:c::/64', '2001:db8:c::1-2001:db8:c::1')
    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.shared_subnet('2001:db8:b::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    world.dhcp_cfg.update({"cache-max-age": 10})  # global setting
    world.dhcp_cfg["subnet6"][0].update({"client-classes": ["Client_Class_1"]})
    world.dhcp_cfg["shared-networks"][0]["subnet6"][0].update({"client-classes": ["Client_Class_2"],
                                                               "cache-max-age": 6})
    world.dhcp_cfg["shared-networks"][0]["subnet6"][1].update({"client-classes": ["Client_Class_3"]})
    world.dhcp_cfg["shared-networks"][0].update({"cache-max-age": 2})

    # class 3 subnet 2001:db8:b:: "cache-max-age": 2 from shared network level
    # class 2 subnet 2001:db8:a:: "cache-max-age": 6 from subnet level
    # class 1 subnet 2001:db8:c:: "cache-max-age": 10 from global level

    world.dhcp_cfg.update({"preferred-lifetime": 12, "rebind-timer": 12,
                           "renew-timer": 12, "valid-lifetime": 12})

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    ####################################################################################
    # check first client with cache threshold defined on shared network level, timeout 6
    duid = "00:03:00:01:11:22:33:44:55:66"
    address = "2001:db8:a::1"
    _assign_lease(duid, address)  # class 2
    assign_time = _get_cltt_from_lease(address)

    # wait for first timeout on different level
    srv_msg.forge_sleep(3, "seconds")

    # renewed address should not have higher CLTT - no entry to db
    _renew_address(duid, address)
    renew_time = _get_cltt_from_lease(address)
    assert renew_time == assign_time, "Received CLTT should be equal to previous value"
    # rebind address should not have higher CLTT - no entry to db
    _rebind_address(duid, address)
    rebind_time = _get_cltt_from_lease(address)
    assert rebind_time == renew_time == assign_time, "Received CLTT should be equal to previous values"

    # wait to correct timeout, and than get new address from renew
    srv_msg.forge_sleep(4, "seconds")

    _renew_address(duid, address)
    renew_time = _get_cltt_from_lease(address)
    assert renew_time > assign_time, "Received CLTT should be higher than value on assign"

    ##############################################################################
    # check second client with cache threshold defined on global level, timeout 10
    duid = "00:03:00:01:66:55:44:33:22:11"
    address = "2001:db8:c::1"
    _assign_lease(duid, address)  # class 2
    assign_time = _get_cltt_from_lease(address)

    # let's wait 7 seconds to get timeout of two different levels
    srv_msg.forge_sleep(7, "seconds")

    # renewed address should not have higher CLTT - no entry to db
    _renew_address(duid, address)
    renew_time = _get_cltt_from_lease(address)
    assert renew_time == assign_time, "Received CLTT should be equal to previous value"
    # rebind address should not have higher CLTT - no entry to db
    _rebind_address(duid, address)
    rebind_time = _get_cltt_from_lease(address)
    assert rebind_time == renew_time == assign_time, "Received CLTT should be equal to previous values"
    # wait timeout, and than get new address from renew
    srv_msg.forge_sleep(4, "seconds")
    _renew_address(duid, address)
    renew_time = _get_cltt_from_lease(address)
    assert renew_time > assign_time, "Received CLTT should be higher than value on assign"

    #############################################################################
    # check second client with cache threshold defined on global level, timeout 2
    duid = "00:03:00:01:11:11:22:22:22:11"
    address = "2001:db8:b::1"
    _assign_lease(duid, address)  # class 2
    assign_time = _get_cltt_from_lease(address)
    # renewed address should not have higher CLTT - no entry to db
    _renew_address(duid, address)
    renew_time = _get_cltt_from_lease(address)
    assert renew_time == assign_time, "Received CLTT should be equal to previous value"
    # rebind address should not have higher CLTT - no entry to db
    _rebind_address(duid, address)
    rebind_time = _get_cltt_from_lease(address)
    assert rebind_time == renew_time == assign_time, "Received CLTT should be equal to previous values"

    # wait timeout, and than get new address from renew
    srv_msg.forge_sleep(3, "seconds")

    _renew_address(duid, address)
    renew_time = _get_cltt_from_lease(address)
    assert renew_time > assign_time, "Received CLTT should be higher than value on assign"


@pytest.mark.v6
@pytest.mark.parametrize("parameter", [{"cache-threshold": 0.7}])
@pytest.mark.parametrize("backend", ['memfile', 'mysql', 'postgresql'])
def test_lease_cache_ddns(parameter, backend):
    misc.test_setup()
    srv_control.add_unix_socket()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.define_lease_db_backend(backend)
    world.dhcp_cfg.update(parameter)

    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_connectivity_options('enable-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-send-updates', True)
    srv_control.add_forward_ddns('six.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('a.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'EMPTY_KEY')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_control.start_srv('DNS', 'started', config_set=31)

    # add subnet without DDNS
    cmd = dict(command="subnet6-add", arguments={"subnet6": [{"ddns-send-updates": False,
                                                              "id": 1, "interface": "$(SERVER_IFACE)",
                                                              "pools": [{"pool": "2001:db8:a::1/128"}],
                                                              "subnet": "2001:db8:a::/64"}]})
    srv_msg.send_ctrl_cmd_via_socket(cmd)

    # assign lease
    duid = "00:03:00:01:11:11:22:22:22:11"
    address = "2001:db8:a::1"
    _assign_lease(duid, address, fqdn="abc")
    # sleep 1 s
    srv_msg.forge_sleep(1, "seconds")
    assign_time = _get_cltt_from_lease(address)
    # renew/rebind lease, kea should not send update

    _renew_address(duid, address, fqdn="abc")
    renew_time = _get_cltt_from_lease(address)
    assert renew_time == assign_time, "Received CLTT should be equal to previous value"

    _rebind_address(duid, address, fqdn="abc")
    rebind_time = _get_cltt_from_lease(address)
    assert rebind_time == renew_time == assign_time, "Received CLTT should be equal to previous values"

    # delete subnet
    cmd = dict(command="subnet6-del", arguments={"id": 1})
    srv_msg.send_ctrl_cmd_via_socket(cmd)
    # add subnet with ddns
    cmd = dict(command="subnet6-add", arguments={"subnet6": [{"ddns-generated-prefix": "abc",
                                                              "ddns-qualifying-suffix": "example.com",
                                                              "ddns-send-updates": True,
                                                              "id": 1, "interface": "$(SERVER_IFACE)",
                                                              "pools": [{"pool": "2001:db8:a::1/128"}],
                                                              "subnet": "2001:db8:a::/64"}]})
    srv_msg.send_ctrl_cmd_via_socket(cmd)
    # sleep 1s
    srv_msg.forge_sleep(1, "seconds")
    # renew lease, this time new entry should exist
    _renew_address(duid, address, fqdn="abc")
    renew_time = _get_cltt_from_lease(address)
    assert renew_time > assign_time, "Received CLTT should be equal to previous value"

    # rebind address, this time should be equal to renewed and higher to assigned
    _rebind_address(duid, address, fqdn="abc")
    rebind_time = _get_cltt_from_lease(address)
    assert rebind_time == renew_time > assign_time, "Received CLTT should be equal to previous values"
