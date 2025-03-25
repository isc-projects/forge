# Copyright (C) 2023-2025 Internet Systems Consortium.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Pre allocation on offer tests"""

import time
import pytest

from src import srv_msg
from src import srv_control
from src import misc

from src.forge_cfg import world
from tests.HA.steps import HOT_STANDBY, wait_until_ha_state


def _check_lease(mac: str, addr: str, vlt: int, state: int = 0, dest: str = world.f_cfg.mgmt_address):
    """Send lease4-get-by-hw-address command and parse it's output
    :param mac: mac address of a lease
    :param addr: ip address of a lease
    :param vlt: valid lifetime value saved by kea
    :param state: state of a lease saved by kea
    :param dest: address of a command destination, default world.f_cfg.mgmt_address,
    can be also world.f_cfg.mgmt_address_2
    """
    cmd = {"command": "lease4-get-by-hw-address",
           "arguments": {"hw-address": mac}}
    resp = srv_msg.send_ctrl_cmd(cmd, address=dest)['arguments']['leases'][0]
    assert resp["hw-address"] == mac, "Incorrect mac address saved"
    assert resp["ip-address"] == addr, "Incorrect address saved"
    assert resp["state"] == state, "Incorrect state of a lease"
    assert resp["subnet-id"] == 1, "Incorrect subnet id"
    assert resp["valid-lft"] == vlt, "On offer we expect to have 'offer-lifetime'"


def _check_times_in_message(valid_lifetime: int):
    """
    Simple check of all timers returned by kea
    :param valid_lifetime: value of a lease lifetime
    """
    srv_msg.response_check_include_option(58)
    srv_msg.response_check_option_content(58, 'value', 1)
    srv_msg.response_check_include_option(59)
    srv_msg.response_check_option_content(59, 'value', 2)
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', valid_lifetime)


@pytest.mark.v4
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('level', ['global', 'shared-network', 'subnet', 'class'])
@pytest.mark.parametrize('allocator', ['iterative', 'random', 'flq'])
def test_basic_configuration(backend, level, allocator):
    """
    Check pre allocation on offer on different configuration levels with different backends and allocators
    :param backend:
    :type backend:
    :param level:
    :type level:
    :param allocator:
    :type allocator:
    """
    vlt = 123
    offer_lifetime = 10
    misc.test_setup()
    srv_control.set_time('renew-timer', 1)
    srv_control.set_time('rebind-timer', 2)
    srv_control.set_time('valid-lifetime', vlt)
    srv_control.define_lease_db_backend(backend)
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')

    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.2', allocator=allocator)
    if level == 'global':
        world.dhcp_cfg.update({'offer-lifetime': offer_lifetime})
    elif level == 'shared-network':
        srv_control.shared_subnet('192.168.50.0/24', 0)
        srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
        srv_control.set_conf_parameter_shared_subnet('interface', world.f_cfg.iface, 0)
        srv_control.set_conf_parameter_shared_subnet('offer-lifetime', offer_lifetime, 0)
    elif level == 'subnet':
        world.dhcp_cfg['subnet4'][0].update({'offer-lifetime': offer_lifetime})
    elif level == 'class':
        srv_control.create_new_class('Management')
        srv_control.add_test_to_class(1, 'test', "pkt4.mac == 0x001122334455")
        srv_control.add_test_to_class(1, 'offer-lifetime', offer_lifetime)
        srv_control.config_client_classification(0, 'Management')
    else:
        assert False, f"Missing elif for {level}"
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:11:22:33:44:55')
    srv_msg.client_send_msg('DISCOVER')

    # on offer we want configured times
    misc.pass_criteria()
    msg = srv_msg.send_wait_for_message('MUST', 'OFFER')[0]
    _check_times_in_message(vlt)

    # but saved in the lease should be minimal offer-lifetime
    _check_lease("00:11:22:33:44:55", "192.168.50.1", offer_lifetime)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:11:22:33:44:55')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', msg.yiaddr)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', msg.yiaddr)
    _check_times_in_message(vlt)

    _check_lease("00:11:22:33:44:55", "192.168.50.1", vlt)

    # check leases
    my_lease = srv_msg.get_all_leases()
    srv_msg.check_leases(my_lease, backend=backend)


@pytest.mark.v4
@pytest.mark.ha
def test_ha_configuration():
    """
    Check if pre allocated lease was send to other not of HA setup. It shouldn't.
    """

    # HA SERVER 1
    misc.test_setup()
    offer_lifetime = 10
    vlt = 123
    srv_control.set_time('renew-timer', 1)
    srv_control.set_time('rebind-timer', 2)
    srv_control.set_time('valid-lifetime', vlt)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.2')
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel('$(MGMT_ADDRESS)')
    world.dhcp_cfg.update({'offer-lifetime': offer_lifetime})
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_hooks('libdhcp_ha.so')

    srv_control.update_ha_hook_parameter(HOT_STANDBY)
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 100,
                                          "max-response-delay": 1500,
                                          "max-unacked-clients": 0,
                                          'sync-page-limit': 2,
                                          "this-server-name": "server1"})

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # HA SERVER 2
    misc.test_setup()
    srv_control.set_time('renew-timer', 1)
    srv_control.set_time('rebind-timer', 2)
    srv_control.set_time('valid-lifetime', vlt)
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)

    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.2', world.f_cfg.server2_iface)
    world.dhcp_cfg.update({'offer-lifetime': offer_lifetime})
    srv_control.add_unix_socket()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_hooks('libdhcp_ha.so')
    srv_control.add_http_control_channel(world.f_cfg.mgmt_address_2)

    srv_control.update_ha_hook_parameter(HOT_STANDBY)
    srv_control.update_ha_hook_parameter({"heartbeat-delay": 1000,
                                          "max-ack-delay": 100,
                                          "max-response-delay": 1500,
                                          "max-unacked-clients": 0,
                                          'sync-page-limit': 2,
                                          "this-server-name": "server2"})
    world.dhcp_cfg['interfaces-config']['interfaces'] = [world.f_cfg.server2_iface]
    srv_control.build_and_send_config_files(dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    wait_until_ha_state('hot-standby')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:11:22:33:44:55')
    srv_msg.client_send_msg('DISCOVER')

    # on offer we want configured times
    misc.pass_criteria()
    msg = srv_msg.send_wait_for_message('MUST', 'OFFER')[0]
    _check_times_in_message(vlt)

    # but saved in the lease should be minimal offer-lifetime
    _check_lease("00:11:22:33:44:55", "192.168.50.1", offer_lifetime)

    # check other HA node
    cmd = {"command": "lease4-get-by-hw-address",
           "arguments": {"hw-address": "00:11:22:33:44:55"}}
    srv_msg.send_ctrl_cmd(cmd, address=world.f_cfg.mgmt_address_2, exp_result=3)

    srv_msg.forge_sleep(1)
    # repeat check, maybe update was delayed?
    cmd = {"command": "lease4-get-by-hw-address",
           "arguments": {"hw-address": "00:11:22:33:44:55"}}
    srv_msg.send_ctrl_cmd(cmd, address=world.f_cfg.mgmt_address_2, exp_result=3)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:11:22:33:44:55')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', msg.yiaddr)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', msg.yiaddr)
    _check_times_in_message(vlt)

    _check_lease("00:11:22:33:44:55", "192.168.50.1", vlt)
    _check_lease("00:11:22:33:44:55", "192.168.50.1", vlt, dest=world.f_cfg.mgmt_address_2)

    # check leases
    my_lease = srv_msg.get_all_leases()
    srv_msg.check_leases(my_lease, backend='memfile')
    srv_msg.check_leases(my_lease, dest=world.f_cfg.mgmt_address_2, backend='memfile')


@pytest.mark.v4
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_with_lease_affinity(backend):
    """
    Check:
    * if lease affinity apply to leases allocated on offer
    * if lease state 2 can be allocated on offer
    :param backend:
    :type backend:
    """
    vlt = 5
    offer_lifetime = 4
    affinity = 7
    misc.test_setup()
    srv_control.set_time('renew-timer', 1)
    srv_control.set_time('rebind-timer', 2)
    srv_control.set_time('valid-lifetime', vlt)
    srv_control.define_lease_db_backend(backend)
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')

    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.2', offer_lifetime=offer_lifetime)

    affinity_cfg = {
        "hold-reclaimed-time": affinity,  # how long kea will keep lease (extension of valid life time)
        "reclaim-timer-wait-time": 2,
        "flush-reclaimed-timer-wait-time": 2
    }
    world.dhcp_cfg.update({"expired-leases-processing": affinity_cfg})

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:11:22:33:44:55')
    srv_msg.client_send_msg('DISCOVER')

    # on offer we want configured times
    misc.pass_criteria()
    msg = srv_msg.send_wait_for_message('MUST', 'OFFER')[0]
    _check_times_in_message(vlt)

    # but saved in the lease should be minimal offer-lifetime
    _check_lease("00:11:22:33:44:55", "192.168.50.1", offer_lifetime)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:11:22:33:44:55')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', msg.yiaddr)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', msg.yiaddr)
    _check_times_in_message(vlt)

    _check_lease("00:11:22:33:44:55", "192.168.50.1", vlt)

    # let's wait for expiration, and reclaim timer
    srv_msg.forge_sleep(vlt+4)

    _check_lease("00:11:22:33:44:55", "192.168.50.1", vlt, state=2)

    # let's preallocate lease for new client
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '11:22:33:44:55:66')
    srv_msg.client_send_msg('DISCOVER')

    # on offer we want configured times
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    _check_times_in_message(vlt)

    _check_lease("11:22:33:44:55:66", "192.168.50.2", offer_lifetime)

    # let's preallocate lease for another new client (3rd) it should preallocate .1 address that has state 2
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '22:33:44:55:66:77')
    srv_msg.client_send_msg('DISCOVER')

    # on offer we want configured times
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    _check_times_in_message(vlt)

    start = time.time()
    _check_lease("22:33:44:55:66:77", "192.168.50.1", offer_lifetime)

    # now we have two leases allocated on offer
    # let's wait for expiration of offer lifetime
    while time.time() - start <= offer_lifetime + 4:
        pass

    _check_lease("11:22:33:44:55:66", "192.168.50.2", offer_lifetime, state=2)
    _check_lease("22:33:44:55:66:77", "192.168.50.1", offer_lifetime, state=2)

    # let's wait for affinity and offer lifetime and check if leases were removed:
    while time.time() - start <= offer_lifetime + affinity + 4:
        pass

    for mac in ["00:11:22:33:44:55", "11:22:33:44:55:66", "22:33:44:55:66:77"]:
        cmd = {"command": "lease4-get-by-hw-address",
               "arguments": {"hw-address": mac}}
        srv_msg.send_ctrl_cmd(cmd, exp_result=3)
