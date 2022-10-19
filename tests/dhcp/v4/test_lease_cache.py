# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

""" testing lease caching for all backends """
# pylint: disable=invalid-name,line-too-long

import pytest

from src import srv_msg
from src import srv_control
from src import misc

from src.forge_cfg import world

# in v4 renew and rebind process differ between each other just with
# destination address. Testing this feature I will just use rebind.


def _get_config(exp_result=0):
    cmd = dict(command="config-get")
    return srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result, channel='socket')


def _get_cltt_from_lease(address, subnet_id=1):
    cmd = dict(command="lease4-get", arguments={"ip-address": address, "subnet-id": subnet_id})
    return srv_msg.send_ctrl_cmd(cmd, channel='socket')["arguments"]["cltt"]


def _assign_lease(mac, address, fqdn=None):
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', mac)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', address)

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', mac)
    srv_msg.client_does_include_with_value('requested_addr', address)
    if fqdn:
        srv_msg.client_sets_value('Client', 'FQDN_domain_name', fqdn)
        srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
        srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', address)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')


def _rebind_address(mac, address, fqdn=None):
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', mac)
    srv_msg.client_sets_value('Client', 'ciaddr', address)
    if fqdn:
        srv_msg.client_sets_value('Client', 'FQDN_domain_name', fqdn)
        srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
        srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', address)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')


@pytest.mark.v4
@pytest.mark.parametrize("backend", ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize("parameter", [{}, {"cache-threshold": .0}, {"cache-max-age": 0}])
def test_lease_cache_disabled(backend, parameter):
    # let's test is as disabled in configurations:
    # - not configured
    # - "cache-threshold": 0 which means disabled according to docs, but kea fail to start gitlab #1796
    # - "cache-max-age": 0 means disabled
    misc.test_setup()
    srv_control.open_control_channel()
    world.dhcp_cfg.update(parameter)
    world.dhcp_cfg.update({"rebind-timer": 10, "renew-timer": 10, "valid-lifetime": 10})
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    address = "192.168.50.10"
    _assign_lease("01:02:03:04:05:06", address)
    assign_time = _get_cltt_from_lease(address)

    # let's wait 1 second, if we would renew immediately, we could have new entry with the same value.
    srv_msg.forge_sleep(1, "seconds")
    _rebind_address("01:02:03:04:05:06", address)
    rebind_time = _get_cltt_from_lease(address)
    assert rebind_time > assign_time, "Received CLTT should be grater than previous value"


@pytest.mark.v4
@pytest.mark.parametrize("parameter", [{"cache-threshold": 0.5}, {"cache-max-age": 5}])
@pytest.mark.parametrize("backend", ['memfile', 'mysql', 'postgresql'])
def test_lease_cache_enabled(backend, parameter):
    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    address = "192.168.50.10"
    world.dhcp_cfg.update(parameter)
    # for a sake of testing we will set all timers to one value, both cache threshold
    # are set to the same value, 50% (which is 5s in this case) and 5 seconds
    world.dhcp_cfg.update({"rebind-timer": 10, "renew-timer": 10, "valid-lifetime": 10})

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _assign_lease("01:02:03:04:05:06", address)
    assign_time = _get_cltt_from_lease(address)

    srv_msg.forge_sleep(2, "seconds")

    # rebind address should not have higher CLTT - no entry to db
    _rebind_address("01:02:03:04:05:06", address)
    rebind_time = _get_cltt_from_lease(address)
    assert rebind_time == assign_time, "Received CLTT should be equal to previous values"

    srv_msg.forge_sleep(5, "seconds")
    # now we will reach cache threshold limit and rebind should have new entry
    _rebind_address("01:02:03:04:05:06", address)
    rebind_time = _get_cltt_from_lease(address)
    assert rebind_time > assign_time, "Received CLTT should be grater than assign value"

    # let's renew and rebind address with different fqdn, that should disable cache
    _assign_lease("01:02:03:04:05:06", address)
    assign_time = _get_cltt_from_lease(address)

    srv_msg.forge_sleep(2, "seconds")

    # rebound address with new fqdn should have higher CLTT - new entry to db
    _rebind_address("01:02:03:04:05:06", address, fqdn="abc")
    rebind_time1 = _get_cltt_from_lease(address)
    assert rebind_time1 > assign_time, "Received CLTT should be equal to previous value"

    # we need sleep to get different value than before
    srv_msg.forge_sleep(2, "seconds")

    # rebind address with new fqdn should have higher CLTT - new entry to db
    _rebind_address("01:02:03:04:05:06", address, fqdn="xyz")
    rebind_time = _get_cltt_from_lease(address)
    assert rebind_time > rebind_time1 > assign_time, "Received CLTT should be highest"


@pytest.mark.v4
@pytest.mark.parametrize("backend", ['memfile', 'mysql', 'postgresql'])
def test_lease_cache_different_levels(backend):
    # everywhere we have the same valid lifetime, but different cache values on each level
    # on global, shared network and subnet, with 3 subnets based on classification
    misc.test_setup()
    srv_control.create_new_class('Client_Class_1')
    srv_control.add_test_to_class(1, 'test', 'pkt4.mac == 0x665544332211')
    srv_control.create_new_class('Client_Class_2')
    srv_control.add_test_to_class(2, 'test', 'pkt4.mac == 0x112233445566')
    srv_control.create_new_class('Client_Class_3')
    srv_control.add_test_to_class(3, 'test', 'pkt4.mac == 0x111122222211')
    srv_control.open_control_channel()
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24', '192.168.51.10-192.168.51.10')
    srv_control.shared_subnet('192.168.50.0/24', 0)
    srv_control.shared_subnet('192.168.51.0/24', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)
    srv_control.config_srv_subnet('192.168.52.0/24', '192.168.52.10-192.168.52.10')

    world.dhcp_cfg.update({"cache-max-age": 10})  # global setting
    world.dhcp_cfg["subnet4"][0].update({"client-class": "Client_Class_1"})
    world.dhcp_cfg["shared-networks"][0]["subnet4"][0].update({"client-class": "Client_Class_2", "cache-max-age": 6})
    world.dhcp_cfg["shared-networks"][0]["subnet4"][1].update({"client-class": "Client_Class_3"})
    world.dhcp_cfg["shared-networks"][0].update({"cache-max-age": 2})

    # class 3 subnet 192.168.51.0/24 "cache-max-age": 2 from shared network level
    # class 2 subnet 192.168.50.0/24 "cache-max-age": 6 from subnet level
    # class 1 subnet 192.168.52.0/24 "cache-max-age": 10 from global level

    world.dhcp_cfg.update({"rebind-timer": 12, "renew-timer": 12, "valid-lifetime": 12})

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    ####################################################################################
    # check first client with cache threshold defined on shared network level, timeout 6
    duid = "11:22:33:44:55:66"
    address = "192.168.50.10"
    _assign_lease(duid, address)  # class 2
    assign_time = _get_cltt_from_lease(address)

    # wait for first timeout on different level
    srv_msg.forge_sleep(3, "seconds")

    # rebound address should not have higher CLTT - no entry to db
    _rebind_address(duid, address)
    rebind_time = _get_cltt_from_lease(address)
    assert rebind_time == assign_time, "Received CLTT should be equal to previous value"

    # wait to correct timeout, and than get new address from renew
    srv_msg.forge_sleep(4, "seconds")

    _rebind_address(duid, address)
    rebind_time = _get_cltt_from_lease(address)
    assert rebind_time > assign_time, "Received CLTT should be higher than value on assign"

    ##############################################################################
    # check second client with cache threshold defined on global level, timeout 10
    duid = "66:55:44:33:22:11"
    address = "192.168.52.10"
    _assign_lease(duid, address)  # class 2
    assign_time = _get_cltt_from_lease(address)

    # let's wait 7 seconds to get timeout of two different levels
    srv_msg.forge_sleep(7, "seconds")

    # rebound address should not have higher CLTT - no entry to db
    _rebind_address(duid, address)
    rebind_time = _get_cltt_from_lease(address)
    assert rebind_time == assign_time, "Received CLTT should be equal to previous value"

    # wait timeout, and than get new address from rebind
    srv_msg.forge_sleep(4, "seconds")
    _rebind_address(duid, address)
    rebind_time = _get_cltt_from_lease(address)
    assert rebind_time > assign_time, "Received CLTT should be higher than value on assign"

    #############################################################################
    # check second client with cache threshold defined on global level, timeout 2
    duid = "11:11:22:22:22:11"
    address = "192.168.51.10"
    _assign_lease(duid, address)  # class 2
    assign_time = _get_cltt_from_lease(address)

    # rebound address should not have higher CLTT - no entry to db
    _rebind_address(duid, address)
    rebind_time = _get_cltt_from_lease(address)
    assert rebind_time == assign_time, "Received CLTT should be equal to previous value"

    # wait timeout, and than get new address from rebind
    srv_msg.forge_sleep(3, "seconds")

    _rebind_address(duid, address)
    rebind_time = _get_cltt_from_lease(address)
    assert rebind_time > assign_time, "Received CLTT should be higher than value on assign"


@pytest.mark.v4
@pytest.mark.parametrize("parameter", [{"cache-threshold": 0.7}])
@pytest.mark.parametrize("backend", ['memfile', 'mysql', 'postgresql'])
def test_lease_cache_ddns(parameter, backend):
    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.define_temporary_lease_db_backend(backend)
    world.dhcp_cfg.update(parameter)

    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_control.start_srv('DNS', 'started', config_set=20)

    # add subnet without DDNS
    cmd = dict(command="subnet4-add", arguments={"subnet4": [{"ddns-send-updates": False,
                                                              "id": 1, "interface": "$(SERVER_IFACE)",
                                                              "pools": [{"pool": "192.168.50.10-192.168.50.10"}],
                                                              "subnet": "192.168.50.10/24"}]})
    srv_msg.send_ctrl_cmd_via_socket(cmd)

    # assign lease
    duid = "11:11:22:22:22:11"
    address = "192.168.50.10"
    _assign_lease(duid, address, fqdn="abc")
    # sleep 1 s
    srv_msg.forge_sleep(1, "seconds")
    assign_time = _get_cltt_from_lease(address)
    # renew/rebind lease, kea should not send update

    _rebind_address(duid, address, fqdn="abc")
    rebind_time = _get_cltt_from_lease(address)
    assert rebind_time == assign_time, "Received CLTT should be equal to previous value"

    # delete subnet
    cmd = dict(command="subnet4-del", arguments={"id": 1})
    srv_msg.send_ctrl_cmd_via_socket(cmd)
    # add subnet with ddns
    cmd = dict(command="subnet4-add", arguments={"subnet4": [{"ddns-generated-prefix": "abc",
                                                              "ddns-qualifying-suffix": "example.com",
                                                              "ddns-send-updates": True,
                                                              "id": 1, "interface": "$(SERVER_IFACE)",
                                                              "pools": [{"pool": "192.168.50.10-192.168.50.10"}],
                                                              "subnet": "192.168.50.10/24"}]})
    srv_msg.send_ctrl_cmd_via_socket(cmd)
    # sleep 1s
    srv_msg.forge_sleep(1, "seconds")
    # rebind lease, this time new entry should exist
    _rebind_address(duid, address, fqdn="abc")
    rebind_time = _get_cltt_from_lease(address)
    assert rebind_time > assign_time, "Received CLTT should be equal to previous value"
