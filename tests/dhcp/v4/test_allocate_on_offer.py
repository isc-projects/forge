# Copyright (C) 2019-2022 Internet Systems Consortium.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Pre allocation on offer tests"""

import pytest

from src import srv_msg
from src import srv_control
from src import misc

from src.forge_cfg import world


@pytest.mark.v4
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('level', ['global', 'shared-network', 'subnet', 'class'])
@pytest.mark.parametrize('allocator', ['iterative', 'random', 'flq'])
def test_pre_allocation_on_offer(backend, level, allocator):
    """
    Check pre allocation on offer on different configuration levels with different backends and allocators
    """
    vlt = 123
    misc.test_setup()
    srv_control.set_time('renew-timer', 1)
    srv_control.set_time('rebind-timer', 2)
    srv_control.set_time('valid-lifetime', vlt)
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')

    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.2', allocator=allocator)
    if level == 'global':
        world.dhcp_cfg.update({'offer-lifetime': 10})
    elif level == 'shared-network':
        srv_control.shared_subnet('192.168.50.0/24', 0)
        srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
        srv_control.set_conf_parameter_shared_subnet('interface', world.f_cfg.iface, 0)
        srv_control.set_conf_parameter_shared_subnet('offer-lifetime', 10, 0)
    elif level == 'subnet':
        world.dhcp_cfg['subnet4'][0].update({'offer-lifetime': 10})
    elif level == 'class':
        srv_control.create_new_class('Management')
        srv_control.add_test_to_class(1, 'test', "pkt4.mac == 0x001122334455")
        srv_control.add_test_to_class(1, 'offer-lifetime', 10)
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
    srv_msg.response_check_include_option(58)
    srv_msg.response_check_option_content(58, 'value', 1)
    srv_msg.response_check_include_option(59)
    srv_msg.response_check_option_content(59, 'value', 2)
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', vlt)

    # but saved in the lease should be minimal offer-lifetime
    cmd = {"command": "lease4-get-by-hw-address",
           "arguments": {"hw-address": "00:11:22:33:44:55"}}
    resp = srv_msg.send_ctrl_cmd(cmd)['arguments']['leases'][0]
    assert resp["hw-address"] == "00:11:22:33:44:55", "Incorrect mac address saved"
    assert resp["ip-address"] == "192.168.50.1", "Incorrect address saved"
    assert resp["state"] == 0, "Incorrect state of a lease"
    assert resp["subnet-id"] == 1, "Incorrect subnet id"
    assert resp["valid-lft"] == 10, "On offer we expect to have 'offer-lifetime'"

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:11:22:33:44:55')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', msg.yiaddr)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', msg.yiaddr)
    srv_msg.response_check_include_option(58)
    srv_msg.response_check_option_content(58, 'value', 1)
    srv_msg.response_check_include_option(59)
    srv_msg.response_check_option_content(59, 'value', 2)
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', vlt)

    cmd = {"command": "lease4-get-by-hw-address",
           "arguments": {"hw-address": "00:11:22:33:44:55"}}
    resp = srv_msg.send_ctrl_cmd(cmd)['arguments']['leases'][0]
    assert resp["hw-address"] == "00:11:22:33:44:55", "Incorrect mac address saved"
    assert resp["ip-address"] == "192.168.50.1", "Incorrect address saved"
    assert resp["state"] == 0, "Incorrect state of a lease"
    assert resp["subnet-id"] == 1, "Incorrect subnet id"
    assert resp["valid-lft"] == vlt, "Lease was fully assigned, it should have valid lifetime value"

    # check leases
    my_lease = srv_msg.get_all_leases()
    srv_msg.check_leases(my_lease, backend=backend)
