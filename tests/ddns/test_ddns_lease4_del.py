# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""DDNS lease resend and lease get tests"""

import pytest

from src import misc
from src import srv_control
from src import srv_msg
from src.forge_cfg import world


def _delete_lease(extra_param=None, exp_result=0):
    cmd = dict(command="lease4-del", arguments={})
    if isinstance(extra_param, dict):
        cmd["arguments"].update(extra_param)
    return srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result, channel='socket')


def _resend_ddns(address, exp_result=0):
    cmd = dict(command="lease4-resend-ddns", arguments={"ip-address": address})
    return srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result, channel='socket')


def _check_fqdn_record(fqdn, address='', expect='notempty'):
    # check new DNS entry
    misc.test_procedure()
    srv_msg.dns_question_record(fqdn, 'A', 'IN')
    srv_msg.client_send_dns_query()
    if expect == 'empty':
        misc.pass_criteria()
        srv_msg.send_wait_for_query('MUST')
        srv_msg.dns_option('ANSWER', expect_include=False)
    else:
        misc.pass_criteria()
        srv_msg.send_wait_for_query('MUST')
        srv_msg.dns_option('ANSWER')
        srv_msg.dns_option_content('ANSWER', 'rdata', address)
        srv_msg.dns_option_content('ANSWER', 'rrname', fqdn)


def _check_address_record(arpa, fqdn='', expect="notempty"):
    misc.test_procedure()
    srv_msg.dns_question_record(arpa, 'PTR', 'IN')
    srv_msg.client_send_dns_query()
    if expect == 'empty':
        misc.pass_criteria()
        srv_msg.send_wait_for_query('MUST')
        srv_msg.dns_option('ANSWER', expect_include=False)
    else:
        misc.pass_criteria()
        srv_msg.send_wait_for_query('MUST')
        srv_msg.dns_option('ANSWER')
        srv_msg.dns_option_content('ANSWER', 'rdata', fqdn)
        srv_msg.dns_option_content('ANSWER', 'rrname', arpa)


def _get_address(mac, fqdn, address):
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', mac)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', address)

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', address)
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', fqdn)
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', address)
    srv_msg.response_check_include_option(81)
    srv_msg.response_check_option_content(81, 'flags', 1)
    srv_msg.response_check_option_content(81, 'fqdn', fqdn)


def _get_address_and_update_ddns(mac=None, fqdn=None, address=None, arpa=None):
    # checking if record is indeed empty on start
    _check_fqdn_record(fqdn, expect='empty')
    # getting new address that should also generate DDNS entry
    _get_address(mac, fqdn, address)
    # checking both forward and reverse DNS entries
    _check_fqdn_record(fqdn, address=address)
    _check_address_record(arpa, fqdn=fqdn)


@pytest.mark.v4
@pytest.mark.ddns
def test_ddns4_all_levels_lease4_del_with_dns():
    misc.test_setup()
    srv_control.add_unix_socket()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.10-192.168.51.10')
    srv_control.config_srv_another_subnet_no_interface('192.168.52.0/24',
                                                       '192.168.52.10-192.168.52.10')

    # let's get 3 different ddns settings, global, shared-network and subnet.
    world.dhcp_cfg.update({"ddns-send-updates": True,
                           "ddns-generated-prefix": "six",
                           "ddns-qualifying-suffix": "example.com"})

    world.dhcp_cfg["subnet4"][1].update({"ddns-send-updates": True,
                                         "ddns-generated-prefix": "abc",
                                         "ddns-qualifying-suffix": "example.com"})

    srv_control.shared_subnet('192.168.50.0/24', 0)
    srv_control.shared_subnet('192.168.51.0/24', 0)
    srv_control.shared_subnet('192.168.52.0/24', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    world.dhcp_cfg["shared-networks"][0].update({"ddns-send-updates": True,
                                                 "ddns-generated-prefix": "xyz",
                                                 "ddns-qualifying-suffix": "example.com"})
    # kea-ddns config
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_connectivity_options('enable-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-send-updates', True)
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_forward_ddns('five.example.com.', 'EMPTY_KEY')
    srv_control.add_forward_ddns('three.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('51.168.192.in-addr.arpa.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('52.168.192.in-addr.arpa.', 'EMPTY_KEY')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    srv_control.start_srv('DNS', 'started', config_set=32)

    # let's get 3 different leases with DNS record
    _get_address_and_update_ddns(mac='ff:ff:ff:ff:ff:01', fqdn='sth4.four.example.com.',
                                 address='192.168.50.10', arpa='10.50.168.192.in-addr.arpa.')

    _get_address_and_update_ddns(mac='ff:ff:ff:ff:ff:02', fqdn='some.five.example.com.',
                                 address='192.168.51.10', arpa='10.51.168.192.in-addr.arpa.')

    _get_address_and_update_ddns(mac='ff:ff:ff:ff:ff:03', fqdn='record.three.example.com.',
                                 address='192.168.52.10', arpa='10.52.168.192.in-addr.arpa.')

    # remove all leases using lease4-del with removing ddns entry
    resp = _delete_lease(extra_param={"ip-address": "192.168.50.10", "update-ddns": True}, exp_result=0)
    assert resp["text"] == "IPv4 lease deleted."
    resp = _delete_lease(extra_param={"ip-address": "192.168.51.10", "update-ddns": True}, exp_result=0)
    assert resp["text"] == "IPv4 lease deleted."
    resp = _delete_lease(extra_param={"ip-address": "192.168.52.10", "update-ddns": True}, exp_result=0)
    assert resp["text"] == "IPv4 lease deleted."

    # check if DNS record was indeed removed
    _check_fqdn_record("sth4.four.example.com.", expect='empty')
    _check_fqdn_record("some.five.example.com.", expect='empty')
    _check_fqdn_record("record.three.example.com.", expect='empty')

    _check_address_record("sth4.four.example.com.", expect='empty')
    _check_address_record("some.five.example.com.", expect='empty')
    _check_address_record("record.three.example.com.", expect='empty')

    # try to add back by resending ddns, all should fail
    _resend_ddns('192.168.51.10', exp_result=3)
    _resend_ddns('192.168.50.10', exp_result=3)
    _resend_ddns('192.168.52.10', exp_result=3)

    _check_fqdn_record("sth4.four.example.com.", expect='empty')
    _check_fqdn_record("some.five.example.com.", expect='empty')
    _check_fqdn_record("record.three.example.com.", expect='empty')

    _check_address_record("sth4.four.example.com.", expect='empty')
    _check_address_record("some.five.example.com.", expect='empty')
    _check_address_record("record.three.example.com.", expect='empty')


@pytest.mark.v4
@pytest.mark.ddns
def test_ddns4_all_levels_lease4_del_without_dns():
    misc.test_setup()
    srv_control.add_unix_socket()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.10-192.168.51.10')
    srv_control.config_srv_another_subnet_no_interface('192.168.52.0/24',
                                                       '192.168.52.10-192.168.52.10')

    # let's get 3 different ddns settings, global, shared-network and subnet.
    world.dhcp_cfg.update({"ddns-send-updates": True,
                           "ddns-generated-prefix": "six",
                           "ddns-qualifying-suffix": "example.com"})

    world.dhcp_cfg["subnet4"][1].update({"ddns-send-updates": True,
                                         "ddns-generated-prefix": "abc",
                                         "ddns-qualifying-suffix": "example.com"})

    srv_control.shared_subnet('192.168.50.0/24', 0)
    srv_control.shared_subnet('192.168.51.0/24', 0)
    srv_control.shared_subnet('192.168.52.0/24', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    world.dhcp_cfg["shared-networks"][0].update({"ddns-send-updates": True,
                                                 "ddns-generated-prefix": "xyz",
                                                 "ddns-qualifying-suffix": "example.com"})
    # kea-ddns config
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_connectivity_options('enable-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-send-updates', True)
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_forward_ddns('five.example.com.', 'EMPTY_KEY')
    srv_control.add_forward_ddns('three.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('51.168.192.in-addr.arpa.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('52.168.192.in-addr.arpa.', 'EMPTY_KEY')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    srv_control.start_srv('DNS', 'started', config_set=32)

    # let's get 3 different leases with DNS record again
    _get_address_and_update_ddns(mac='ff:ff:ff:ff:ff:01', fqdn='sth4.four.example.com.',
                                 address='192.168.50.10', arpa='10.50.168.192.in-addr.arpa.')

    _get_address_and_update_ddns(mac='ff:ff:ff:ff:ff:02', fqdn='some.five.example.com.',
                                 address='192.168.51.10', arpa='10.51.168.192.in-addr.arpa.')

    _get_address_and_update_ddns(mac='ff:ff:ff:ff:ff:03', fqdn='record.three.example.com.',
                                 address='192.168.52.10', arpa='10.52.168.192.in-addr.arpa.')

    # remove them without removing DNS entry
    _delete_lease(extra_param={"ip-address": "192.168.50.10"}, exp_result=0)
    _delete_lease(extra_param={"ip-address": "192.168.51.10"}, exp_result=0)
    _delete_lease(extra_param={"ip-address": "192.168.52.10"}, exp_result=0)

    # and we should keep DNS records intact
    _check_fqdn_record("sth4.four.example.com.", address="192.168.50.10")
    _check_fqdn_record("some.five.example.com.", address="192.168.51.10")
    _check_fqdn_record("record.three.example.com.", address="192.168.52.10")

    _check_address_record('10.50.168.192.in-addr.arpa.', fqdn="sth4.four.example.com.")
    _check_address_record('10.51.168.192.in-addr.arpa.', fqdn="some.five.example.com.")
    _check_address_record('10.52.168.192.in-addr.arpa.', fqdn="record.three.example.com.")
