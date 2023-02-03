# Copyright (C) 2023 Internet Systems Consortium.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


"""DHCPv6 bulk leasequery tests"""

from multiprocessing import Pool
import time
import random
import string
import pytest

from src import srv_control
from src import misc
from src import srv_msg
from src.forge_cfg import world

from tests.HA.steps import increase_mac


def _get_lease(mac="01:02:0c:03:0a:00", leases_count=10, remote_id=None,
               relay_id=None, addr_count=1, pd_count=1, relay=True, link_addr='2001:db8:1::1000'):
    leases = []
    for _ in range(leases_count):
        mac = increase_mac(mac)
        duid = "00:03:00:01:" + mac

        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'DUID', duid)
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_sets_value('Client', 'ia_id', 1)
        srv_msg.client_does_include('Client', 'IA-NA')
        srv_msg.client_send_msg('SOLICIT')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

        for _ in range(addr_count):
            srv_msg.client_sets_value('Client', 'ia_id', random.randint(1, 9000))
            srv_msg.client_does_include('Client', 'IA-NA')

        for _ in range(pd_count):
            srv_msg.client_sets_value('Client', 'ia_pd', random.randint(1, 9000))
            srv_msg.client_does_include('Client', 'IA-PD')

        srv_msg.client_copy_option('server-id')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_send_msg('REQUEST')

        if remote_id is not None:
            srv_msg.client_sets_value('Client', 'remote_id', remote_id)
            srv_msg.client_does_include('RelayAgent', 'remote-id')
        if relay_id is not None:
            srv_msg.client_sets_value('Client', 'relay_id', relay_id)
            srv_msg.client_does_include('RelayAgent', 'relay-id')

        if relay:
            srv_msg.client_sets_value('RelayAgent', 'linkaddr', link_addr)
            srv_msg.client_does_include('RelayAgent', 'interface-id')
            srv_msg.create_relay_forward()

            misc.pass_criteria()
            srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
            srv_msg.response_check_include_option(9)
            srv_msg.response_check_option_content(9, 'Relayed', 'Message')
            srv_msg.response_check_include_option(1)
            srv_msg.response_check_include_option(2)
        else:
            misc.pass_criteria()
            srv_msg.send_wait_for_message('MUST', 'REPLY')
            srv_msg.response_check_include_option(1)
            srv_msg.response_check_include_option(2)

        leases += srv_msg.get_all_leases()
    return leases


def _send_leasequery(lq_type, sleep=0, relay_id=None, remote_id=None, lq_address="0::0",
                     duid=None):
    time.sleep(sleep)
    srv_msg.client_sets_value('Client', 'tr_id', random.randint(1, 2000))
    if relay_id is not None:
        srv_msg.client_sets_value('Client', 'relay_id', relay_id)
        srv_msg.client_does_include('Client', 'relay-id')
    if remote_id is not None:
        srv_msg.client_sets_value('Client', 'remote_id', remote_id)
        srv_msg.client_does_include('Client', 'remote-id')

    srv_msg.client_sets_value('Client', 'lq-query-type', lq_type)
    srv_msg.client_sets_value('Client', 'lq-query-address', lq_address)
    srv_msg.client_does_include('Client', 'lq-query')

    if duid:
        srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_does_include('Client', 'client-id')  # this will be added to lease-query message
    srv_msg.client_send_msg('LEASEQUERY')

    srv_msg.send_wait_for_message('MUST', 'LEASEQUERY-REPLY', protocol='TCP')


def _check_leasequery_relay_data(linkaddr=None):
    # check leasequery option - relay data
    # in this test it's pretty easy, except linkaddr everything should be the same
    opt_47 = srv_msg.response_check_option_content(45, 'sub-option', 47)[0]
    # srv_msg.response_check_option_content is returning list of all options 47 included in option 45
    # opt_47.show()
    opt_47 = opt_47.message
    assert opt_47.ifaceid == b'15', "Relay data included incorrect interface id"
    assert opt_47.enterprisenum == 0, "Relay data included incorrect enterprisenum"
    assert opt_47.remoteid == b"\n\x00'\x00\x00\x01", "Relay data included incorrect remote id"
    if linkaddr:
        assert opt_47.linkaddr == linkaddr, "Relay data included incorrect linkaddr"


def _check_address_and_duid_in_single_lq_message(duid, addr=None, prefix=None):
    srv_msg.response_check_include_option(45)
    srv_msg.response_check_option_content(45, 'sub-option', 1)
    srv_msg.response_check_suboption_content(1, 45, 'duid', duid)
    if addr:
        srv_msg.response_check_option_content(45, 'sub-option', 5)
        srv_msg.response_check_suboption_content(5, 45, 'addr', addr)
        # if LQ message has address or prefix, not both, let's check this
        srv_msg.response_check_option_content(45, 'sub-option', 26, expect_include=False)
    else:
        srv_msg.response_check_option_content(45, 'sub-option', 26)
        srv_msg.response_check_suboption_content(26, 45, 'prefix', prefix)
        # if LQ message has address or prefix, not both, let's check this
        srv_msg.response_check_option_content(45, 'sub-option', 5, expect_include=False)


@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.parametrize('backend', ['memfile'])
def test_v6_multiple_networks(backend):
    """
    Configure 4 different subnets and assign multiple leases from each. Than send multiple
    bulk leasequery messages with different query types to check if returned leases are correct
    """
    bulk_leasequery_configuration = {"parameters": {
                "requesters": [world.f_cfg.client_ipv6_addr_global],
                "advanced": {
                     "bulk-query-enabled": True,
                     "active-query-enabled": False,
                     "extended-info-tables-enabled": True,
                     "lease-query-ip": world.f_cfg.srv_ipv6_addr_global,
                     "lease-query-tcp-port": 547,
                     "max-requester-connections": 10,
                     "max-concurrent-queries": 4,
                     "max-requester-idle-time":  3000,
                     "max-leases-per-fetch": 5,
                }}}

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::100')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::100')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::100')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::100')
    srv_control.config_srv_prefix('2001:db8:2::', 0, 64, 80)
    srv_control.config_srv_prefix('2001:db8:3::', 1, 64, 80)
    srv_control.config_srv_prefix('2001:db8:4::', 2, 64, 80)
    srv_control.config_srv_prefix('2001:db8:5::', 3, 64, 80)

    world.dhcp_cfg['store-extended-info'] = True
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    # adding hook and required parameters
    srv_control.add_hooks('libdhcp_lease_query.so')
    # Set permitted requester to forge machine ip
    srv_control.add_parameter_to_hook('libdhcp_lease_query.so', bulk_leasequery_configuration["parameters"])

    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')
    cmd = {"command": "config-get", "arguments": {}}

    # we just care about leasequery config
    resp = srv_msg.send_ctrl_cmd(cmd)["arguments"]["Dhcp6"]["hooks-libraries"]
    for hook in resp:
        if "libdhcp_lease_query.so" in hook["library"]:
            assert hook["parameters"] == bulk_leasequery_configuration["parameters"], "Returned config is different" \
                                                                                      " from configured."
            break
    else:
        assert False, "leasequery hook configuration is missing!"

    # how many clients we will generate for each subnet, this will also affect number of leasequery data messages!
    # each client will get 2 addresses and 2 prefixes, this is 4 leases per client per subnets, 4 subnets are used in
    # this test so highest number of leasequery messages kea will return is 81 (1 reply, 79 data, 1 done)
    # for easier debugging change clients_per_subnet to 1
    clients_per_subnet = 5

    # collect multiple leases from each subnet, simulating relay with both relay id and remote id
    all_leases = _get_lease(mac="01:02:0c:03:0a:00", link_addr="2001:db8:a::1000",
                            remote_id="0a0027000001", relay_id='00:03:00:01:ff:ff:ff:ff:ff:01',
                            leases_count=clients_per_subnet, pd_count=2, addr_count=2)
    all_leases += _get_lease(mac="01:02:0d:03:0a:00", link_addr="2001:db8:b::1000",
                             remote_id="0a0027000001", relay_id='00:03:00:01:ff:ff:ff:ff:ff:01',
                             leases_count=clients_per_subnet, pd_count=2, addr_count=2)
    all_leases += _get_lease(mac="01:02:0e:03:0a:00", link_addr="2001:db8:c::1000",
                             remote_id="0a0027000001", relay_id='00:03:00:01:ff:ff:ff:ff:ff:01',
                             leases_count=clients_per_subnet, pd_count=2, addr_count=2)
    all_leases += _get_lease(mac="01:02:0f:03:0a:00", link_addr="2001:db8:d::1000",
                             remote_id="0a0027000001", relay_id='00:03:00:01:ff:ff:ff:ff:ff:01',
                             leases_count=clients_per_subnet, pd_count=2, addr_count=2)

    # let's check all leases using remote id (lq query type 5):
    _send_leasequery(5, remote_id='0a0027000001')
    srv_msg.tcp_messages_include(leasequery_reply=1, leasequery_data=clients_per_subnet * 16 - 1, leasequery_done=1)

    # check if all addresses assigned are returned correctly:
    for lease in filter(lambda d: d["prefix_len"] == 0, all_leases):
        srv_msg.tcp_get_message(address=lease["address"])
        _check_address_and_duid_in_single_lq_message(lease["duid"], addr=lease["address"])
        _check_leasequery_relay_data(lease["address"].split("::")[0]+"::1000")

    # and check also if all prefixes assigned are returned correctly
    for lease in filter(lambda d: d["prefix_len"] != 0, all_leases):
        srv_msg.tcp_get_message(prefix=lease["address"])
        _check_address_and_duid_in_single_lq_message(lease["duid"], prefix=lease["address"])
        _check_leasequery_relay_data()

    # let's check all leases using relay id (lq query type 3):
    _send_leasequery(3, relay_id='00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.tcp_messages_include(leasequery_reply=1, leasequery_data=clients_per_subnet * 16 - 1, leasequery_done=1)

    # check if all addresses assigned are returned correctly:
    for lease in filter(lambda d: d["prefix_len"] == 0, all_leases):
        srv_msg.tcp_get_message(address=lease["address"])
        _check_address_and_duid_in_single_lq_message(lease["duid"], addr=lease["address"])
        _check_leasequery_relay_data(lease["address"].split("::")[0]+"::1000")

    # and check also if all prefixes assigned are returned correctly
    for lease in filter(lambda d: d["prefix_len"] != 0, all_leases):
        srv_msg.tcp_get_message(prefix=lease["address"])
        _check_address_and_duid_in_single_lq_message(lease["duid"], prefix=lease["address"])
        _check_leasequery_relay_data()

    # let's check just subsets, using query by link - type 4
    # this will return just addresses, so we expect smaller number of leasequery data messages
    # also we collect addresses from each subnet separately
    _send_leasequery(4, lq_address="2001:db8:a::")
    srv_msg.tcp_messages_include(leasequery_reply=1, leasequery_data=clients_per_subnet * 2 - 1, leasequery_done=1)
    for lease in filter(lambda d: "2001:db8:a" in d["address"], all_leases):
        srv_msg.tcp_get_message(address=lease["address"])
        _check_address_and_duid_in_single_lq_message(lease["duid"], addr=lease["address"])

    _send_leasequery(4, lq_address="2001:db8:b::")
    srv_msg.tcp_messages_include(leasequery_reply=1, leasequery_data=clients_per_subnet * 2 - 1, leasequery_done=1)
    for lease in filter(lambda d: "2001:db8:b" in d["address"], all_leases):
        srv_msg.tcp_get_message(address=lease["address"])
        _check_address_and_duid_in_single_lq_message(lease["duid"], addr=lease["address"])

    _send_leasequery(4, lq_address="2001:db8:c::")
    srv_msg.tcp_messages_include(leasequery_reply=1, leasequery_data=clients_per_subnet * 2 - 1, leasequery_done=1)
    for lease in filter(lambda d: "2001:db8:c" in d["address"], all_leases):
        srv_msg.tcp_get_message(address=lease["address"])
        _check_address_and_duid_in_single_lq_message(lease["duid"], addr=lease["address"])

    _send_leasequery(4, lq_address="2001:db8:d::")
    srv_msg.tcp_messages_include(leasequery_reply=1, leasequery_data=clients_per_subnet * 2 - 1, leasequery_done=1)
    for lease in filter(lambda d: "2001:db8:d" in d["address"], all_leases):
        srv_msg.tcp_get_message(address=lease["address"])
        _check_address_and_duid_in_single_lq_message(lease["duid"], addr=lease["address"])

    # now let's add leases for clients that were used in subnet "2001:db8:a::" but in subnet "2001:db8:b::"
    new_leases = _get_lease(mac="01:02:0c:03:0a:00", link_addr="2001:db8:b::1000",
                            remote_id="0a0027000001", relay_id='00:03:00:01:ff:ff:ff:ff:ff:01',
                            leases_count=clients_per_subnet, pd_count=2, addr_count=2)
    # and repeat checking subnets "2001:db8:a::" and "2001:db8:b::" to make sure clients are returned in proper subnets
    # so subnet "2001:db8:a::" should be the same
    _send_leasequery(4, lq_address="2001:db8:a::")
    srv_msg.tcp_messages_include(leasequery_reply=1, leasequery_data=clients_per_subnet * 2 - 1, leasequery_done=1)
    for lease in filter(lambda d: "2001:db8:a" in d["address"], all_leases):
        srv_msg.tcp_get_message(address=lease["address"])
        _check_address_and_duid_in_single_lq_message(lease["duid"], addr=lease["address"])

    # but subnet "2001:db8:b::" should have more leases, twice more than previously
    _send_leasequery(4, lq_address="2001:db8:b::")
    srv_msg.tcp_messages_include(leasequery_reply=1, leasequery_data=clients_per_subnet * 4 - 1, leasequery_done=1)
    for lease in filter(lambda d: "2001:db8:b" in d["address"], all_leases + new_leases):
        srv_msg.tcp_get_message(address=lease["address"])
        _check_address_and_duid_in_single_lq_message(lease["duid"], addr=lease["address"])

    # now let's use remote-id and relay-id, we should get more than previously
    # let's check all leases using remote id (lq query type 5):
    _send_leasequery(5, remote_id='0a0027000001')
    srv_msg.tcp_messages_include(leasequery_reply=1, leasequery_data=clients_per_subnet * 20 - 1, leasequery_done=1)

    # check if all addresses assigned are returned correctly:
    for lease in filter(lambda d: d["prefix_len"] == 0, all_leases + new_leases):
        srv_msg.tcp_get_message(address=lease["address"])
        _check_address_and_duid_in_single_lq_message(lease["duid"], addr=lease["address"])
        _check_leasequery_relay_data(lease["address"].split("::")[0]+"::1000")

    # and check also if all prefixes assigned are returned correctly
    for lease in filter(lambda d: d["prefix_len"] != 0, all_leases + new_leases):
        srv_msg.tcp_get_message(prefix=lease["address"])
        _check_address_and_duid_in_single_lq_message(lease["duid"], prefix=lease["address"])
        _check_leasequery_relay_data()

    # let's check all leases using relay id (lq query type 3):
    _send_leasequery(3, relay_id='00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.tcp_messages_include(leasequery_reply=1, leasequery_data=clients_per_subnet * 20 - 1, leasequery_done=1)

    # check if all addresses assigned are returned correctly:
    for lease in filter(lambda d: d["prefix_len"] == 0, all_leases + new_leases):
        srv_msg.tcp_get_message(address=lease["address"])
        _check_address_and_duid_in_single_lq_message(lease["duid"], addr=lease["address"])
        _check_leasequery_relay_data(lease["address"].split("::")[0]+"::1000")

    # and check also if all prefixes assigned are returned correctly
    for lease in filter(lambda d: d["prefix_len"] != 0, all_leases + new_leases):
        srv_msg.tcp_get_message(prefix=lease["address"])
        _check_address_and_duid_in_single_lq_message(lease["duid"], prefix=lease["address"])
        _check_leasequery_relay_data()

    # now let's use query by remote id AND linkaddress, Kea should:
    # * not return prefixes at all (it's not supported)
    # * return addresses only from "2001:db8:b::" (from all_leases and new_leases)
    _send_leasequery(5, remote_id='0a0027000001', lq_address="2001:db8:b::")
    srv_msg.tcp_messages_include(leasequery_reply=1, leasequery_data=clients_per_subnet * 4 - 1, leasequery_done=1)
    for lease in filter(lambda d: "2001:db8:b" in d["address"], all_leases + new_leases):
        srv_msg.tcp_get_message(address=lease["address"])
        _check_address_and_duid_in_single_lq_message(lease["duid"], addr=lease["address"])

    # and the same this but checking relay-id:
    _send_leasequery(3, relay_id='00:03:00:01:ff:ff:ff:ff:ff:01', lq_address="2001:db8:b::")
    srv_msg.tcp_messages_include(leasequery_reply=1, leasequery_data=clients_per_subnet * 4 - 1, leasequery_done=1)
    for lease in filter(lambda d: "2001:db8:b" in d["address"], all_leases + new_leases):
        srv_msg.tcp_get_message(address=lease["address"])
        _check_address_and_duid_in_single_lq_message(lease["duid"], addr=lease["address"])


@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.parametrize('backend', ['memfile'])
def test_v6_assign_and_reply_simultaneously(backend):
    """
    Let's trigger BLQ over TCP while assigning leases
    :param backend: string, backends used in this test
    """

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ffff')
    srv_control.config_srv_prefix('2001:db8:2::', 0, 64, 128)
    world.dhcp_cfg['store-extended-info'] = True
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    # adding hook and required parameters
    srv_control.add_hooks('libdhcp_lease_query.so')
    # Set permitted requester to forge machine ip
    blq = {
        "requesters": [world.f_cfg.client_ipv6_addr_global],
        "advanced": {
            "bulk-query-enabled": True,
            "active-query-enabled": False,
            "extended-info-tables-enabled": True,
            "lease-query-ip": world.f_cfg.srv_ipv6_addr_global,
            "lease-query-tcp-port": 547,
            "max-requester-connections": 10,
            "max-concurrent-queries": 4,
            "max-requester-idle-time":  3000,
            "max-leases-per-fetch": 5,
        }}

    srv_control.add_parameter_to_hook('libdhcp_lease_query.so', blq)

    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # let's get quite a lot of leases
    first_set_of_leases = _get_lease(mac="01:02:0c:44:0a:00", remote_id="0a0027000001",
                                     leases_count=10, pd_count=4, addr_count=4)
    # we will have 81 messages via TCP
    _send_leasequery(5, remote_id='0a0027000001')
    srv_msg.tcp_messages_include(leasequery_reply=1, leasequery_data=79, leasequery_done=1)

    # check if all addresses assigned are returned correctly:
    for lease in filter(lambda d: d["prefix_len"] == 0, first_set_of_leases):
        srv_msg.tcp_get_message(address=lease["address"])
        _check_address_and_duid_in_single_lq_message(lease["duid"], addr=lease["address"])

    # and check also if all prefixes assigned are returned correctly
    for lease in filter(lambda d: d["prefix_len"] != 0, first_set_of_leases):
        srv_msg.tcp_get_message(prefix=lease["address"])
        _check_address_and_duid_in_single_lq_message(lease["duid"], prefix=lease["address"])

    # open two processes one for triggering BLQ and second for assigning the leases
    # forge may be bit slow to get it 100% right this is why proper test is in performance setup
    # so let's just check addresses and prefixes before and after simultaneous work
    with Pool() as pool:
        process_to_get_leases = pool.apply_async(_get_lease, kwds={"leases_count": 15, "pd_count": 1, "addr_count": 2,
                                                                   "remote_id": "0a0027000001"})
        pool.apply_async(_send_leasequery, args=(5,), kwds={"sleep": 3, "remote_id": "0a0027000001"})
        pool.close()
        pool.join()

    leases_set_no2 = process_to_get_leases.get()

    # now let's check if returned addresses were actually assigned
    # let's check if all received addresses were assigned previously and keep in mind that we could have more
    # assigned addresses then blq returned (don't check last message leasequery done)

    # pylint: disable=cell-var-from-loop
    # this error keeps popping up, in this case I think it's false positive
    # to evaluate this you can print address of values ia_address and ia_prefix
    # print(hex(id(ia_address)))

    for i in range(len(world.tcpmsg) - 1):
        srv_msg.tcp_get_message(order=i)
        msg = srv_msg.response_check_include_option(45)
        # get address option
        ia_address = srv_msg.get_option(msg, 5)
        lease = []
        if len(ia_address) > 0:
            # amongst all generated leases find one with returned address
            lease += list(filter(lambda d: d["address"] == ia_address[0].addr, first_set_of_leases + leases_set_no2))
            assert len(lease) > 0, f"Received via BLQ address {ia_address[0].addr} was not assigned!"
        # if no IA address option was found, there has to be IA Prefix
        else:
            ia_prefix = srv_msg.get_option(msg, 26)
            lease += list(filter(lambda d: d["address"] == ia_prefix[0].prefix, first_set_of_leases + leases_set_no2))
            assert len(lease) > 0, f"Received via BLQ prefix {ia_prefix[0].prefix} was not assigned!"
        # and at the end let's check if duids of lease assigned and received via BLQ is equal
        srv_msg.response_check_include_option(45)
        srv_msg.response_check_option_content(45, 'sub-option', 1)
        srv_msg.response_check_suboption_content(1, 45, 'duid', lease[0]['duid'])
    # now let's check how many responses we got
    _send_leasequery(5, remote_id='0a0027000001')
    srv_msg.tcp_messages_include(leasequery_reply=1, leasequery_data=124, leasequery_done=1)

    # check if all addresses assigned are returned correctly:
    for lease in filter(lambda d: d["prefix_len"] == 0, leases_set_no2 + first_set_of_leases):
        srv_msg.tcp_get_message(address=lease["address"])
        _check_address_and_duid_in_single_lq_message(lease["duid"], addr=lease["address"])

    # and check also if all prefixes assigned are returned correctly
    for lease in filter(lambda d: d["prefix_len"] != 0, leases_set_no2 + first_set_of_leases):
        srv_msg.tcp_get_message(prefix=lease["address"])
        _check_address_and_duid_in_single_lq_message(lease["duid"], prefix=lease["address"])


@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.parametrize('backend', ['memfile'])
def test_v6_message_build(backend):
    """
    Check if leasequery reply, data and done messages are correctly composed
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ffff')
    srv_control.config_srv_prefix('2001:db8:2::', 0, 64, 128)
    world.dhcp_cfg['store-extended-info'] = True
    srv_control.config_srv_id('LLT', '00:01:00:02:52:7b:a8:f0:08:00:27:58:99:99')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    # adding hook and required parameters
    srv_control.add_hooks('libdhcp_lease_query.so')
    # Set permitted requester to forge machine ip
    blq = {
        "requesters": [world.f_cfg.client_ipv6_addr_global],
        "advanced": {
            "bulk-query-enabled": True,
            "active-query-enabled": False,
            "extended-info-tables-enabled": True,
            "lease-query-ip": world.f_cfg.srv_ipv6_addr_global,
            "lease-query-tcp-port": 547,
            "max-requester-connections": 10,
            "max-concurrent-queries": 10,
            "max-requester-idle-time":  3000,
            "max-leases-per-fetch": 50,
        }}
    srv_control.add_parameter_to_hook('libdhcp_lease_query.so', blq)

    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')
    _get_lease(mac="01:02:0c:03:0a:00", link_addr="2001:db8:1::1000",
               remote_id="0a0027000001", relay_id='00:03:00:01:ff:ff:ff:ff:ff:01',
               leases_count=1, pd_count=0, addr_count=2)
    _send_leasequery(5, remote_id='0a0027000001', duid='00:03:00:01:11:11:11:11:11:01')
    srv_msg.tcp_messages_include(leasequery_reply=1, leasequery_data=1, leasequery_done=1)

    srv_msg.tcp_get_message(order=0)
    srv_msg.response_check_include_option(1)
    # client id should be the same as the one included in leasequery, not leases, not relay
    srv_msg.response_check_option_content(1, 'duid', '00:03:00:01:11:11:11:11:11:01')
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_option_content(2, 'duid', '00:01:00:02:52:7b:a8:f0:08:00:27:58:99:99')
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'statuscode', 0)
    srv_msg.response_check_include_option(45)

    srv_msg.tcp_get_message(order=1)
    # leasequery data can't have client or server id or status code, just lease query client data (45)
    srv_msg.response_check_include_option(1, expect_include=False)
    srv_msg.response_check_include_option(2, expect_include=False)
    srv_msg.response_check_include_option(13, expect_include=False)
    srv_msg.response_check_include_option(45)

    # leasequery done should be empty
    srv_msg.tcp_get_message(order=2)
    srv_msg.response_check_include_option(1, expect_include=False)
    srv_msg.response_check_include_option(2, expect_include=False)
    srv_msg.response_check_include_option(13, expect_include=False)
    srv_msg.response_check_include_option(45, expect_include=False)


@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.parametrize('backend', ['memfile'])
def test_v6_negative(backend):
    """
    Couple negative cases
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ffff')
    world.dhcp_cfg['store-extended-info'] = True
    srv_control.config_srv_id('LLT', '00:01:00:02:52:7b:a8:f0:08:00:27:58:99:99')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    # adding hook and required parameters
    srv_control.add_hooks('libdhcp_lease_query.so')
    # Set permitted requester to forge machine ip
    blq = {
        "requesters": [world.f_cfg.client_ipv6_addr_global],
        "advanced": {
            "bulk-query-enabled": True,
            "active-query-enabled": False,
            "extended-info-tables-enabled": True,
            "lease-query-ip": world.f_cfg.srv_ipv6_addr_global,
            "lease-query-tcp-port": 547,
            "max-requester-connections": 10,
            "max-concurrent-queries": 10,
            "max-requester-idle-time":  3000,
            "max-leases-per-fetch": 50,
        }}

    srv_control.add_parameter_to_hook('libdhcp_lease_query.so', blq)
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')
    # incorrect query id
    srv_msg.client_sets_value('Client', 'lq-query-type', 17)
    srv_msg.client_sets_value('Client', 'lq-query-address', "0::0")
    srv_msg.client_does_include('Client', 'lq-query')
    srv_msg.client_does_include('Client', 'client-id')  # this will be added to lease-query message
    srv_msg.client_send_msg('LEASEQUERY')

    srv_msg.send_wait_for_message('MUST', 'LEASEQUERY-REPLY', protocol='TCP')
    srv_msg.tcp_messages_include(leasequery_reply=1)

    srv_msg.tcp_get_message(order=0)
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'statuscode', 7)
    srv_msg.response_check_include_option(45, expect_include=False)

    # missing duid
    srv_msg.client_sets_value('Client', 'lq-query-type', 5)
    srv_msg.client_sets_value('Client', 'lq-query-address', "0::0")
    srv_msg.client_does_include('Client', 'lq-query')
    srv_msg.client_send_msg('LEASEQUERY')

    srv_msg.send_wait_for_message('', None, expect_response=False, protocol='TCP')

    # incorrect server-id
    srv_msg.client_sets_value('Client', 'lq-query-type', 5)
    srv_msg.client_sets_value('Client', 'lq-query-address', "0::0")
    srv_msg.client_does_include('Client', 'lq-query')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'server_id', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'server-id')
    srv_msg.client_send_msg('LEASEQUERY')

    srv_msg.send_wait_for_message('', None, expect_response=False, protocol='TCP')

    # missing relay-id
    srv_msg.client_sets_value('Client', 'lq-query-type', 3)
    srv_msg.client_sets_value('Client', 'lq-query-address', "0::0")
    srv_msg.client_does_include('Client', 'lq-query')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('LEASEQUERY')

    srv_msg.send_wait_for_message('MUST', 'LEASEQUERY-REPLY', protocol='TCP')
    srv_msg.tcp_messages_include(leasequery_reply=1)
    srv_msg.tcp_get_message(order=0)
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'statuscode', 8)
    srv_msg.response_check_include_option(45, expect_include=False)

    # missing remote-id
    srv_msg.client_sets_value('Client', 'lq-query-type', 5)
    srv_msg.client_sets_value('Client', 'lq-query-address', "0::0")
    srv_msg.client_does_include('Client', 'lq-query')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('LEASEQUERY')

    srv_msg.send_wait_for_message('MUST', 'LEASEQUERY-REPLY', protocol='TCP')
    srv_msg.tcp_messages_include(leasequery_reply=1)
    srv_msg.tcp_get_message(order=0)
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'statuscode', 8)
    srv_msg.response_check_include_option(45, expect_include=False)

    # missing address
    srv_msg.client_sets_value('Client', 'lq-query-type', 4)
    srv_msg.client_sets_value('Client', 'lq-query-address', "0::0")
    srv_msg.client_does_include('Client', 'lq-query')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('LEASEQUERY')

    srv_msg.send_wait_for_message('MUST', 'LEASEQUERY-REPLY', protocol='TCP')
    srv_msg.tcp_messages_include(leasequery_reply=1)
    srv_msg.tcp_get_message(order=0)
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'statuscode', 8)
    srv_msg.response_check_include_option(45, expect_include=False)

    # not configured
    srv_msg.client_sets_value('Client', 'lq-query-type', 4)
    srv_msg.client_sets_value('Client', 'lq-query-address', "3001::0")
    srv_msg.client_does_include('Client', 'lq-query')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('LEASEQUERY')

    srv_msg.send_wait_for_message('MUST', 'LEASEQUERY-REPLY', protocol='TCP')
    srv_msg.tcp_messages_include(leasequery_reply=1)
    srv_msg.tcp_get_message(order=0)
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'statuscode', 9)
    srv_msg.response_check_include_option(45, expect_include=False)

    # nothing found
    srv_msg.client_sets_value('Client', 'lq-query-type', 4)
    srv_msg.client_sets_value('Client', 'lq-query-address', "2001:db8:1::")
    srv_msg.client_does_include('Client', 'lq-query')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('LEASEQUERY')

    srv_msg.send_wait_for_message('MUST', 'LEASEQUERY-REPLY', protocol='TCP')
    srv_msg.tcp_messages_include(leasequery_reply=1)
    srv_msg.tcp_get_message(order=0)
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(13)
    # this time status code is success but nothing returned anyway
    srv_msg.response_check_option_content(13, 'statuscode', 0)
    srv_msg.response_check_include_option(45, expect_include=False)


@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.parametrize('backend', ['memfile'])
def test_v6_junk_over_tcp(backend):
    """
    Let's see if kea survive junk sent over multiple channels
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ffff')
    srv_control.config_srv_prefix('2001:db8:2::', 0, 64, 128)
    world.dhcp_cfg['store-extended-info'] = True
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    # adding hook and required parameters
    srv_control.add_hooks('libdhcp_lease_query.so')
    # Set permitted requester to forge machine ip
    blq = {
        "requesters": [world.f_cfg.client_ipv6_addr_global],
        "advanced": {
            "bulk-query-enabled": True,
            "active-query-enabled": False,
            "extended-info-tables-enabled": True,
            "lease-query-ip": world.f_cfg.srv_ipv6_addr_global,
            "lease-query-tcp-port": 547,
            "max-requester-connections": 10,
            "max-concurrent-queries": 10,
            "max-requester-idle-time":  3000,
            "max-leases-per-fetch": 50,
        }}

    srv_control.add_parameter_to_hook('libdhcp_lease_query.so', blq)
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    junk = b''
    characters_to_send = random.choices(string.printable, k=5000)
    # if that test at one point will fail, we have to know what was sent (no matter of logging level):
    print("String that will be sent to kea:")
    print("".join(characters_to_send))
    for character in characters_to_send:
        junk += bytes(character, 'UTF-8')
    print("in bytes:\n", junk)
    srv_msg.send_over_tcp(junk, number_of_connections=7)
    # sent generated junk but multiplied
    srv_msg.send_over_tcp(junk * 10, number_of_connections=7)

    # let's check if kea still works
    all_leases = _get_lease(mac="01:02:0c:03:0a:00", link_addr="2001:db8:1::1000",
                            remote_id="0a0027000001", relay_id='00:03:00:01:ff:ff:ff:ff:ff:01',
                            leases_count=1, pd_count=2, addr_count=2)
    _send_leasequery(5, remote_id='0a0027000001')
    srv_msg.tcp_messages_include(leasequery_reply=1, leasequery_data=3, leasequery_done=1)

    # check if all addresses assigned are returned correctly:
    for lease in filter(lambda d: d["prefix_len"] == 0, all_leases):
        srv_msg.tcp_get_message(address=lease["address"])
        _check_address_and_duid_in_single_lq_message(lease["duid"], addr=lease["address"])
        _check_leasequery_relay_data(lease["address"].split("::")[0]+"::1000")

    # and check also if all prefixes assigned are returned correctly
    for lease in filter(lambda d: d["prefix_len"] != 0, all_leases):
        srv_msg.tcp_get_message(prefix=lease["address"])
        _check_address_and_duid_in_single_lq_message(lease["duid"], prefix=lease["address"])
        _check_leasequery_relay_data()


@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.parametrize('backend', ['memfile'])
def test_v6_multiple_relays(backend):
    """
    Test of v6 lease query messages asking for ip address, se multiple relay ids and remote ids in the same subnet
    """
    bulk_leasequery_configuration = {"parameters": {
                "requesters": [world.f_cfg.client_ipv6_addr_global],
                "advanced": {
                     "bulk-query-enabled": True,
                     "active-query-enabled": False,
                     "extended-info-tables-enabled": True,
                     "lease-query-ip": world.f_cfg.srv_ipv6_addr_global,
                     "lease-query-tcp-port": 547,
                     "max-requester-connections": 10,
                     "max-concurrent-queries": 4,
                     "max-requester-idle-time":  3000,
                     "max-leases-per-fetch": 5,
                }}}

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::100')

    world.dhcp_cfg['store-extended-info'] = True
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    # adding hook and required parameters
    srv_control.add_hooks('libdhcp_lease_query.so')
    # Set permitted requester to forge machine ip
    srv_control.add_parameter_to_hook('libdhcp_lease_query.so', bulk_leasequery_configuration["parameters"])

    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # collect multiple leases from each subnet, simulating relay with both relay id and remote id
    leases_relay_1 = _get_lease(mac="01:02:0c:03:0a:00", link_addr="2001:db8:a::1000",
                                remote_id="0a0027000001", relay_id='00:03:00:01:ff:ff:ff:ff:ff:01',
                                leases_count=5, pd_count=0, addr_count=2)

    leases_relay_2 = _get_lease(mac="01:02:0d:03:0a:00", link_addr="2001:db8:a::1000",
                                remote_id="0a0027111111", relay_id='00:03:00:01:ff:00:00:00:00:01',
                                leases_count=5, pd_count=0, addr_count=2)

    # let's check all leases using remote id (lq query type 5):
    _send_leasequery(5, remote_id="0a0027000001")
    srv_msg.tcp_messages_include(leasequery_reply=1, leasequery_data=9, leasequery_done=1)
    for lease in leases_relay_1:
        srv_msg.tcp_get_message(address=lease["address"])
        _check_address_and_duid_in_single_lq_message(lease["duid"], addr=lease["address"])

    _send_leasequery(3, relay_id="00:03:00:01:ff:ff:ff:ff:ff:01")
    srv_msg.tcp_messages_include(leasequery_reply=1, leasequery_data=9, leasequery_done=1)
    for lease in leases_relay_1:
        srv_msg.tcp_get_message(address=lease["address"])
        _check_address_and_duid_in_single_lq_message(lease["duid"], addr=lease["address"])

    _send_leasequery(5, remote_id="0a0027111111")
    srv_msg.tcp_messages_include(leasequery_reply=1, leasequery_data=9, leasequery_done=1)
    for lease in leases_relay_2:
        srv_msg.tcp_get_message(address=lease["address"])
        _check_address_and_duid_in_single_lq_message(lease["duid"], addr=lease["address"])

    _send_leasequery(3, relay_id="00:03:00:01:ff:00:00:00:00:01")
    srv_msg.tcp_messages_include(leasequery_reply=1, leasequery_data=9, leasequery_done=1)
    for lease in leases_relay_2:
        srv_msg.tcp_get_message(address=lease["address"])
        _check_address_and_duid_in_single_lq_message(lease["duid"], addr=lease["address"])
