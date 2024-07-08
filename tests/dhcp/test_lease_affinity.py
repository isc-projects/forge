# Copyright (C) 2023 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea lease affinity feature"""


import time
import pytest
from scapy.layers.dhcp6 import DHCP6OptIA_NA, DHCP6OptIA_PD

from src import misc
from src import srv_control
from src import srv_msg

from src.forge_cfg import world


def _get_lease(mac: str = "f6:f5:f4:f3:f2:f1", addr: str = None, prefix: str = None,
               request: bool = False, backend: str = None, time1: int = 1, time2: int = 2,
               preflft: int = 3, validlft: int = 8):
    """
    Get lease with address and/or prefix. Perform detailed check on messages and saved lease
    :param mac: client mac address (used to build duid)
    :param addr: expected address
    :param prefix: expected prefix
    :param request: if address/prefix should request in IA address IA prefix option
    :param backend: lease backend type
    :param time1: T1 time
    :param time2: T2 time
    :param preflft: preferred lifetime
    :param validlft: valid lifetime
    :return: {lease, IA NA option, IA PD option}
    """
    ia_na_option = None
    ia_pd_option = None
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', f'00:03:00:01:{mac}')
    srv_msg.client_does_include('Client', 'client-id')
    if addr:
        if request:
            srv_msg.client_sets_value('Client', 'IA_Address', addr)
            srv_msg.client_does_include('Client', 'IA_Address')
        srv_msg.client_does_include('Client', 'IA-NA')
    if prefix:
        if request:
            srv_msg.client_sets_value('Client', 'prefix', prefix)
            srv_msg.client_does_include('Client', 'IA_Prefix')
        srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    if addr:
        srv_msg.response_check_include_option(3)
        srv_msg.response_check_option_content(3, 'sub-option', 5)
        srv_msg.response_check_suboption_content(5, 3, 'addr', addr)
        srv_msg.response_check_option_content(3, 'T1', time1)
        srv_msg.response_check_option_content(3, 'T2', time2)
        srv_msg.response_check_suboption_content(5, 3, 'preflft', preflft)
        srv_msg.response_check_suboption_content(5, 3, 'validlft', validlft)

    if prefix:
        srv_msg.response_check_include_option(25)
        srv_msg.response_check_option_content(25, 'sub-option', 26)
        srv_msg.response_check_suboption_content(26, 25, 'prefix', prefix)
        srv_msg.response_check_option_content(25, 'T1', time1)
        srv_msg.response_check_option_content(25, 'T2', time2)
        srv_msg.response_check_suboption_content(26, 25, 'preflft', preflft)
        srv_msg.response_check_suboption_content(26, 25, 'validlft', validlft)
        srv_msg.response_check_suboption_content(26, 25, 'plen', 126)

    misc.test_procedure()
    if addr:
        srv_msg.client_copy_option('IA_NA')
    if prefix:
        srv_msg.client_copy_option('IA_PD')
    srv_msg.client_sets_value('Client', 'server_id', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'server-id')
    srv_msg.client_sets_value('Client', 'DUID', f'00:03:00:01:{mac}')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    if addr:
        ia_na_option = srv_msg.response_check_include_option(3)
        srv_msg.response_check_option_content(3, 'sub-option', 5)
        srv_msg.response_check_suboption_content(5, 3, 'addr', addr)
        srv_msg.response_check_option_content(3, 'T1', time1)
        srv_msg.response_check_option_content(3, 'T2', time2)
        srv_msg.response_check_suboption_content(5, 3, 'preflft', preflft)
        srv_msg.response_check_suboption_content(5, 3, 'validlft', validlft)

    if prefix:
        ia_pd_option = srv_msg.response_check_include_option(25)
        srv_msg.response_check_option_content(25, 'sub-option', 26)
        srv_msg.response_check_suboption_content(26, 25, 'prefix', prefix)
        srv_msg.response_check_option_content(25, 'T1', time1)
        srv_msg.response_check_option_content(25, 'T2', time2)
        srv_msg.response_check_suboption_content(26, 25, 'preflft', preflft)
        srv_msg.response_check_suboption_content(26, 25, 'validlft', validlft)
        srv_msg.response_check_suboption_content(26, 25, 'plen', 126)

    # check leases
    my_lease = srv_msg.get_all_leases()
    srv_msg.check_leases(my_lease, backend=backend)
    return {'lease': my_lease, 'ia': ia_na_option, 'pd': ia_pd_option}


def _renew_lease(mac: str = "f6:f5:f4:f3:f2:f1",
                 ia_na_option: DHCP6OptIA_NA = None, ia_pd_option: DHCP6OptIA_PD = None, backend: str = None,
                 time1: int = 1, time2: int = 2, preflft: int = 3, validlft: int = 8):
    """
    Renew leases and execute detailed checks on message
    :param mac: client mac address (used to build duid)
    :param ia_na_option: IA NA option
    :param ia_pd_option: IA PD option
    :param backend: lease backend time
    :param time1: T1 time
    :param time2: T2 time
    :param preflft: preferred lifetime
    :param validlft: valid lifetime
    """
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'server_id', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'server-id')
    srv_msg.client_sets_value('Client', 'DUID', f'00:03:00:01:{mac}')
    srv_msg.client_does_include('Client', 'client-id')
    if ia_na_option:
        srv_msg.add_scapy_option(ia_na_option)
    if ia_pd_option:
        srv_msg.add_scapy_option(ia_pd_option)
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    if ia_na_option:
        srv_msg.response_check_include_option(3)
        srv_msg.response_check_option_content(3, 'iaid', ia_na_option.iaid)
        srv_msg.response_check_option_content(3, 'T1', time1)
        srv_msg.response_check_option_content(3, 'T2', time2)
        srv_msg.response_check_option_content(3, 'sub-option', 5)
        srv_msg.response_check_suboption_content(5, 3, 'preflft', preflft)
        srv_msg.response_check_suboption_content(5, 3, 'validlft', validlft)
    if ia_pd_option:
        srv_msg.response_check_include_option(25)
        srv_msg.response_check_option_content(25, 'iaid', ia_pd_option.iaid)
        srv_msg.response_check_option_content(25, 'T1', time1)
        srv_msg.response_check_option_content(25, 'T2', time2)
        srv_msg.response_check_option_content(25, 'sub-option', 26)
        srv_msg.response_check_suboption_content(26, 25, 'preflft', preflft)
        srv_msg.response_check_suboption_content(26, 25, 'validlft', validlft)
        srv_msg.response_check_suboption_content(26, 25, 'plen', 126)

    my_lease = srv_msg.get_all_leases()
    srv_msg.check_leases(my_lease, backend=backend)


def _release_lease(mac: str = "f6:f5:f4:f3:f2:f1", ia_na_option: DHCP6OptIA_NA = None,
                   ia_pd_option: DHCP6OptIA_PD = None):
    """
    Release address and/or prefix and detailed checks on the message
    :param mac: client mac address (used to build duid)
    :param ia_na_option: IA NA option
    :param ia_pd_option: IA PD option
    """
    misc.test_procedure()

    srv_msg.client_sets_value('Client', 'server_id', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'server-id')
    srv_msg.client_sets_value('Client', 'DUID', f'00:03:00:01:{mac}')
    srv_msg.client_does_include('Client', 'client-id')
    if ia_na_option:
        srv_msg.add_scapy_option(ia_na_option)
    if ia_pd_option:
        srv_msg.add_scapy_option(ia_pd_option)
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    if ia_na_option:
        srv_msg.response_check_include_option(3)
        srv_msg.response_check_option_content(3, 'iaid', ia_na_option.iaid)
        srv_msg.response_check_option_content(3, 'T1', 0)
        srv_msg.response_check_option_content(3, 'T2', 0)
        srv_msg.response_check_option_content(3, 'sub-option', 13)
        srv_msg.response_check_suboption_content(13, 3, 'statuscode', 0)

    if ia_pd_option:
        srv_msg.response_check_include_option(25)
        srv_msg.response_check_option_content(25, 'iaid', ia_pd_option.iaid)
        srv_msg.response_check_option_content(25, 'T1', 0)
        srv_msg.response_check_option_content(25, 'T2', 0)
        srv_msg.response_check_option_content(25, 'sub-option', 13)
        srv_msg.response_check_suboption_content(13, 25, 'statuscode', 0)


@pytest.mark.v6
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_v6_lease_affinity(backend):
    """
    Test lease affinity.
    - client X will get lease, expire, and request again
    - client X will get lease, release, and request again
    - client X will get lease, expire, another client will ask for this lease
    - client X will get lease last one in the pool, expire, client Y will ask for new lease, shouldn't get
    - check states of leases after valid life time expire
    - check leases after valid life time + affinity expire
    - check if lease state changes after expiration
    - check if leases were removed on time
    It's making detailed checks on all messages
    """
    vlt = 10
    affinity = 10
    misc.test_setup()
    srv_control.set_time('renew-timer', 1)
    srv_control.set_time('rebind-timer', 2)
    srv_control.set_time('preferred-lifetime', 3)
    srv_control.set_time('valid-lifetime', vlt)

    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::11-2001:db8:1::14')
    srv_control.config_srv_prefix('2001:db8:2::', 0, 124, 126)
    srv_control.config_srv_id('LL', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')

    affinity_cfg = {
        "hold-reclaimed-time": affinity,  # how long kea will keep lease (extension of valid life time)
        "reclaim-timer-wait-time": 2,
        "flush-reclaimed-timer-wait-time": 2
    }
    world.dhcp_cfg.update({"expired-leases-processing": affinity_cfg})

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # check if there are no leases
    cmd = {"command": "lease6-get-all"}
    srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    # addresses: 2001:db8:1::11, 2001:db8:1::12, 2001:db8:1::13, 2001:db8:1::14
    # prefixes: 2001:db8:2::, 2001:db8:2::4, 2001:db8:2::8, 2001:db8:2::c

    _get_lease(mac="f6:f5:f4:f3:f2:11", addr='2001:db8:1::11', prefix='2001:db8:2::', backend=backend, validlft=vlt)
    _get_lease(mac="f6:f5:f4:f3:f2:22", addr='2001:db8:1::12', prefix='2001:db8:2::4', backend=backend, validlft=vlt)
    _get_lease(mac="f6:f5:f4:f3:f2:33", addr='2001:db8:1::13', prefix='2001:db8:2::8', backend=backend, validlft=vlt)
    _get_lease(mac="f6:f5:f4:f3:f2:44", addr='2001:db8:1::14', prefix='2001:db8:2::c', backend=backend, validlft=vlt)

    start = time.time()
    # we should be out of addresses and prefixes
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:66:99')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 25, 'statuscode', 6)

    cmd = {"command": "lease6-get-all"}
    leases_ccch = srv_msg.send_ctrl_cmd(cmd)  # get leases from command control channel
    for lease in leases_ccch['arguments']['leases']:
        assert lease['state'] == 0, f"Address is not in proper state! {lease}"
        assert lease['valid-lft'] == vlt, f"Address has incorrect valid lifetime {lease}"

    # let's wait for expiration of all addresses and prefixes, and reclamation process should be executed
    while time.time() - start <= vlt + 3:
        pass

    cmd = {"command": "lease6-get-all"}
    leases_ccch = srv_msg.send_ctrl_cmd(cmd)
    for lease in leases_ccch['arguments']['leases']:
        # state 2 is a reclaimed lease
        assert lease['state'] == 2, f"Address is not in proper state! {lease}"
        assert lease['valid-lft'] == vlt, f"Address has incorrect valid lifetime {lease}"

    # all addresses are expired and reclaimed new client should get address and prefix, first in line
    _get_lease(mac="f6:f5:f4:f3:66:99", addr='2001:db8:1::11', prefix='2001:db8:2::', backend=backend, validlft=vlt)

    # 4th client should be able to get it's old lease
    client = _get_lease(mac="f6:f5:f4:f3:f2:44", addr='2001:db8:1::14', prefix='2001:db8:2::c',
                        backend=backend, validlft=vlt)
    # and make sure it can renew it
    _renew_lease(mac="f6:f5:f4:f3:f2:44", ia_na_option=client['ia'], ia_pd_option=client['pd'],
                 backend=backend, validlft=vlt)
    # than release it (let's check Kea #2766)
    _release_lease(mac="f6:f5:f4:f3:f2:44", ia_na_option=client['ia'], ia_pd_option=client['pd'])
    # get lease and check state
    cmd = {"command": "lease6-get-by-duid",
           "arguments": {"duid": "00:03:00:01:f6:f5:f4:f3:f2:44"}}

    lease_ccch = srv_msg.send_ctrl_cmd(cmd)  # get leases from command control channel
    for lease in lease_ccch['arguments']['leases']:
        # release changes state to relesed (3)
        assert lease['state'] == 3, f"Address is not in proper state! {lease}"
        assert lease['valid-lft'] == 0, f"Address has incorrect valid lifetime {lease}"

    # and ask for it again
    _get_lease(mac="f6:f5:f4:f3:f2:44", addr='2001:db8:1::14', prefix='2001:db8:2::c', backend=backend, validlft=vlt)
    second_start = time.time()

    lease_ccch = srv_msg.send_ctrl_cmd(cmd)  # get leases from command control channel
    for lease in lease_ccch['arguments']['leases']:
        assert lease['state'] == 0, f"Address is not in proper state! {lease} it's cant be 2 or 3"
        assert lease['valid-lft'] == vlt, f"Address has incorrect valid lifetime {lease}"

    # clients f6:f5:f4:f3:66:99 f6:f5:f4:f3:f2:44 should only have state 0, all the rest 2
    cmd = {"command": "lease6-get-all"}
    leases_ccch = srv_msg.send_ctrl_cmd(cmd)  # get leases from command control channel
    for lease in leases_ccch['arguments']['leases']:
        state = 0 if lease["duid"] in ["00:03:00:01:f6:f5:f4:f3:66:99", "00:03:00:01:f6:f5:f4:f3:f2:44"] else 2
        assert lease['state'] == state, f"Lease has incorrect lease state! {lease}"

    while time.time() - second_start <= vlt + 3:
        pass

    # all leases should be reclaimed
    cmd = {"command": "lease6-get-all"}
    leases_ccch = srv_msg.send_ctrl_cmd(cmd)
    for lease in leases_ccch['arguments']['leases']:
        # state 2 is a reclaimed lease
        assert lease['state'] == 2, f"Address is not in proper state! {lease}"
        assert lease['valid-lft'] == vlt, f"Address has incorrect valid lifetime {lease}"

    # let's wait until all leases will be removed
    while time.time() - second_start <= vlt + affinity + 3:
        pass

    # check if there are no leases
    cmd = {"command": "lease6-get-all"}
    srv_msg.send_ctrl_cmd(cmd, exp_result=3)


def _get_lease_4(mac: str = "f6:f5:f4:f3:f2:f1", addr: str = None,
                 backend: str = None, renew_time: int = 1, rebind_time: int = 2, valid_lft: int = 7):
    """
    Get ip v4 address as lease
    :param mac: mac address
    :param addr: IP v4 address we expect to get
    :param backend: lease backend type
    :param renew_time: renew time
    :param rebind_time: rebind time
    :param valid_lft: valid lifetime
    :return: dict with lease details
    """
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', mac)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', addr)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', mac)
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', addr)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', addr)
    srv_msg.response_check_include_option(58)
    srv_msg.response_check_option_content(58, 'value', renew_time)
    srv_msg.response_check_include_option(59)
    srv_msg.response_check_option_content(59, 'value', rebind_time)
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', valid_lft)

    # check leases
    my_lease = srv_msg.get_all_leases()
    srv_msg.check_leases(my_lease, backend=backend)
    return my_lease


def _renew_lease_4(mac: str = "f6:f5:f4:f3:f2:f1", addr: str = None,
                   renew_time: int = 1, rebind_time: int = 2, valid_lft: int = 7):
    """
    Renew ip v4 address
    :param mac: mac address
    :param addr: IP v4 address we expect to get
    :param renew_time: renew time
    :param rebind_time: rebind time
    :param valid_lft: valid lifetime
    """
    srv_msg.client_sets_value('Client', 'chaddr', mac)
    srv_msg.client_sets_value('Client', 'ciaddr', addr)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', addr)
    srv_msg.response_check_content('chaddr', mac)
    srv_msg.response_check_include_option(58)
    srv_msg.response_check_option_content(58, 'value', renew_time)
    srv_msg.response_check_include_option(59)
    srv_msg.response_check_option_content(59, 'value', rebind_time)
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', valid_lft)


def _release_lease_4(mac: str = "f6:f5:f4:f3:f2:f1", addr=None):
    """
    Release ip v4 address
    :param mac: mac address
    :param addr: IP v4 address we expect to get
    """
    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', mac)
    srv_msg.client_sets_value('Client', 'ciaddr', addr)
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, expect_response=False)


@pytest.mark.v4
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_v4_lease_affinity(backend):
    """
    Test lease affinity.
    - client X will get lease, expire, and request again
    - client X will get lease, release, and request again
    - client X will get lease, expire, another client will ask for this lease
    - client X will get lease last one in the pool, expire, client Y will ask for new lease, shouldn't get
    - check states of leases after valid life time expire
    - check leases after valid life time + affinity expire
    - check if lease state changes after expiration
    - check if leases were removed on time
    It's making detailed checks on all messages
    """
    vlt = 10
    affinity = 10
    misc.test_setup()
    srv_control.set_time('renew-timer', 1)
    srv_control.set_time('rebind-timer', 2)
    srv_control.set_time('valid-lifetime', vlt)

    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.11-192.168.50.14')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')

    affinity_cfg = {
        "hold-reclaimed-time": affinity,  # how long kea will keep lease (extension of valid life time)
        "reclaim-timer-wait-time": 2,
        "flush-reclaimed-timer-wait-time": 2
    }
    world.dhcp_cfg.update({"expired-leases-processing": affinity_cfg})

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # check if there are no leases
    cmd = {"command": "lease4-get-all"}
    srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    _get_lease_4(mac="f6:f5:f4:f3:f2:11", addr='192.168.50.11', backend=backend, valid_lft=vlt)
    _get_lease_4(mac="f6:f5:f4:f3:f2:22", addr='192.168.50.12', backend=backend, valid_lft=vlt)
    _get_lease_4(mac="f6:f5:f4:f3:f2:33", addr='192.168.50.13', backend=backend, valid_lft=vlt)
    _get_lease_4(mac="f6:f5:f4:f3:f2:44", addr='192.168.50.14', backend=backend, valid_lft=vlt)

    start = time.time()

    # we should be out of addresses
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'f6:f5:f4:00:11:22')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, expect_response=False)

    cmd = {"command": "lease4-get-all"}
    leases_ccch = srv_msg.send_ctrl_cmd(cmd)  # get leases from command control channel
    for lease in leases_ccch['arguments']['leases']:
        assert lease['state'] == 0, f"Address is not in proper state! {lease}"
        assert lease['valid-lft'] == vlt, f"Address has incorrect valid lifetime {lease}"

    # let's wait for expiration of all addresses, and reclamation process should be executed
    while time.time() - start <= vlt + 3:
        pass

    cmd = {"command": "lease4-get-all"}
    leases_ccch = srv_msg.send_ctrl_cmd(cmd)
    for lease in leases_ccch['arguments']['leases']:
        # state 2 is a reclaimed lease
        assert lease['state'] == 2, f"Address is not in proper state! {lease}"
        assert lease['valid-lft'] == vlt, f"Address has incorrect valid lifetime {lease}"

    # all addresses are expired and reclaimed new client should get address, first in line
    _get_lease_4(mac="f6:f5:f4:f3:66:99", addr='192.168.50.11', backend=backend, valid_lft=vlt)
    # 4th client should be able to get it's old lease
    _get_lease_4(mac="f6:f5:f4:f3:f2:44", addr='192.168.50.14', backend=backend, valid_lft=vlt)
    # and make sure it can renew it
    _renew_lease_4(mac="f6:f5:f4:f3:f2:44", addr='192.168.50.14', valid_lft=vlt)
    # than release it (let's check Kea #2766)
    _release_lease_4(mac="f6:f5:f4:f3:f2:44", addr='192.168.50.14')

    # get lease and check state
    cmd = {"command": "lease4-get-by-hw-address",
           "arguments": {"hw-address": "f6:f5:f4:f3:f2:44"}}

    lease_ccch = srv_msg.send_ctrl_cmd(cmd)  # get leases from command control channel
    for lease in lease_ccch['arguments']['leases']:
        # release do not change state of a lease
        assert lease['valid-lft'] == 0, f"Address has incorrect valid lifetime {lease}"

    # and ask for it again
    _get_lease_4(mac="f6:f5:f4:f3:f2:44", addr='192.168.50.14', backend=backend, valid_lft=vlt)
    second_start = time.time()

    lease_ccch = srv_msg.send_ctrl_cmd(cmd)  # get leases from command control channel
    for lease in lease_ccch['arguments']['leases']:
        assert lease['state'] == 0, f"Address is not in proper state! {lease} it's cant be 2 or 3"
        assert lease['valid-lft'] == vlt, f"Address has incorrect valid lifetime {lease}"

    # clients f6:f5:f4:f3:66:99 f6:f5:f4:f3:f2:44 should only have state 0, all the rest 2
    cmd = {"command": "lease4-get-all"}
    leases_ccch = srv_msg.send_ctrl_cmd(cmd)  # get leases from command control channel
    for lease in leases_ccch['arguments']['leases']:
        state = 0 if lease["hw-address"] in ["f6:f5:f4:f3:66:99", "f6:f5:f4:f3:f2:44"] else 2
        assert lease['state'] == state, f"Lease has incorrect lease state! {lease}"

    while time.time() - second_start <= vlt + 3:
        pass

    # all leases should be reclaimed
    cmd = {"command": "lease4-get-all"}
    leases_ccch = srv_msg.send_ctrl_cmd(cmd)
    for lease in leases_ccch['arguments']['leases']:
        # state 2 is a reclaimed lease
        assert lease['state'] == 2, f"Address is not in proper state! {lease}"
        assert lease['valid-lft'] == vlt, f"Address has incorrect valid lifetime {lease}"

    # let's wait until all leases will be removed
    while time.time() - second_start <= vlt + affinity + 3:
        pass

    # check if there are no leases
    cmd = {"command": "lease4-get-all"}
    srv_msg.send_ctrl_cmd(cmd, exp_result=3)
