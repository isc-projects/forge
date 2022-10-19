# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""DDNS configured on non global level"""

# pylint: disable=invalid-name,line-too-long

import pytest

from src import misc
from src import srv_control
from src import srv_msg
from src.forge_cfg import world


def _resend_ddns(address, exp_result=0):
    cmd = dict(command="lease6-resend-ddns", arguments={"ip-address": address})
    return srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result, channel='socket')


def _check_fqdn_record(fqdn, address='', expect='notempty'):
    misc.test_procedure()
    srv_msg.dns_question_record(fqdn, 'AAAA', 'IN')
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


def _check_address_record(fqdn, arpa):
    misc.test_procedure()
    srv_msg.dns_question_record(arpa, 'PTR', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST')
    srv_msg.dns_option('ANSWER')
    srv_msg.dns_option_content('ANSWER', 'rdata', fqdn)
    srv_msg.dns_option_content('ANSWER', 'rrname', arpa)


def _get_address(duid, fqdn):
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    if fqdn is not None:
        srv_msg.client_sets_value('Client', 'FQDN_domain_name', fqdn)
        srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
        srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    if fqdn is not None:
        srv_msg.response_check_include_option(39)
        srv_msg.response_check_option_content(39, 'flags', 'S')
        srv_msg.response_check_option_content(39, 'fqdn', fqdn)


def _get_address_and_update_ddns(duid=None, fqdn=None, address=None, arpa=None):
    # checking if record is indeed empty on start
    _check_fqdn_record(fqdn, expect='empty')
    # getting new address that should also generate DDNS entry
    _get_address(duid, fqdn)
    # checking both forward and reverse DNS entries
    _check_fqdn_record(fqdn, address=address)
    _check_address_record(fqdn, arpa)


@pytest.mark.v6
@pytest.mark.ddns
def test_ddns6_global():
    misc.test_setup()
    # simple case, global ddns configuration - get and address and dns entry
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_forward_ddns('six.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('a.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'EMPTY_KEY')

    world.dhcp_cfg.update({"ddns-send-updates": True,
                           "ddns-generated-prefix": "six",
                           "ddns-qualifying-suffix": "example.com"})

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_control.start_srv('DNS', 'started', config_set=31)

    _get_address_and_update_ddns(duid='00:03:00:01:ff:ff:ff:ff:ff:01', fqdn='sth6.six.example.com.',
                                 address='2001:db8:a::1',
                                 arpa='1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.a.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')


@pytest.mark.v6
@pytest.mark.ddns
def test_ddns6_shared_network():
    misc.test_setup()
    # simple case, ddns configuration in shared network - get and address and dns entry
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_forward_ddns('six.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('a.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'EMPTY_KEY')

    world.dhcp_cfg["shared-networks"][0].update({"ddns-send-updates": True,
                                                 "ddns-generated-prefix": "abc",
                                                 "ddns-qualifying-suffix": "example.com"})

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_control.start_srv('DNS', 'started', config_set=31)

    _get_address_and_update_ddns(duid='00:03:00:01:ff:ff:ff:ff:ff:01', fqdn='sth6.six.example.com.',
                                 address='2001:db8:a::1',
                                 arpa='1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.a.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')


@pytest.mark.v6
@pytest.mark.ddns
def test_ddns6_subnet():
    misc.test_setup()
    # simple case, ddns configuration in subnet - get and address and dns entry
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')

    world.dhcp_cfg["subnet6"][0].update({"ddns-send-updates": True,
                                         "ddns-generated-prefix": "abc",
                                         "ddns-qualifying-suffix": "example.com"})

    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_forward_ddns('six.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('a.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'EMPTY_KEY')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_control.start_srv('DNS', 'started', config_set=31)

    _get_address_and_update_ddns(duid='00:03:00:01:ff:ff:ff:ff:ff:01', fqdn='sth6.six.example.com.',
                                 address='2001:db8:a::1',
                                 arpa='1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.a.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')


@pytest.mark.v6
@pytest.mark.ddns
def test_ddns6_all_levels_resend_command():
    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')

    # let's get 3 different ddns settings, global, shared-network and subnet.
    world.dhcp_cfg.update({"ddns-send-updates": True,
                           "ddns-generated-prefix": "six",
                           "ddns-qualifying-suffix": "example.com"})

    world.dhcp_cfg["subnet6"][1].update({"ddns-send-updates": True,
                                         "ddns-generated-prefix": "abc",
                                         "ddns-qualifying-suffix": "example.com"})

    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.shared_subnet('2001:db8:b::/64', 0)
    srv_control.shared_subnet('2001:db8:c::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    world.dhcp_cfg["shared-networks"][0].update({"ddns-send-updates": True,
                                                 "ddns-generated-prefix": "xyz",
                                                 "ddns-qualifying-suffix": "example.com"})

    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_forward_ddns('six.example.com.', 'EMPTY_KEY')
    srv_control.add_forward_ddns('abc.example.com.', 'EMPTY_KEY')
    srv_control.add_forward_ddns('xyz.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('a.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('b.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('c.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'EMPTY_KEY')

    # srv_control.print_cfg()
    # srv_control.print_cfg(service='DDNS')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_control.start_srv('DNS', 'started', config_set=31)

    _get_address_and_update_ddns(duid='00:03:00:01:ff:ff:ff:ff:ff:01', fqdn='sth6.six.example.com.',
                                 address='2001:db8:a::1',
                                 arpa='1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.a.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')

    _get_address_and_update_ddns(duid='00:03:00:01:ff:ff:ff:ff:ff:02', fqdn='some.abc.example.com.',
                                 address='2001:db8:b::1',
                                 arpa='1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.b.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')

    _get_address_and_update_ddns(duid='00:03:00:01:ff:ff:ff:ff:ff:03', fqdn='record.xyz.example.com.',
                                 address='2001:db8:c::1',
                                 arpa='1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.c.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')

    # stop bind, remove data files, start bind with empty zones
    srv_control.start_srv('DNS', 'stopped')
    srv_control.clear_some_data('all', service='DNS')
    srv_control.start_srv('DNS', 'started', config_set=31)
    # check is all records were removed
    _check_fqdn_record("sth6.six.example.com.", expect='empty')
    _check_fqdn_record("some.abc.example.com.", expect='empty')
    _check_fqdn_record("record.xyz.example.com.", expect='empty')

    response = _resend_ddns('2001:db8:a::10', exp_result=3)
    assert response["text"] == "No lease found for: 2001:db8:a::10"
    response = _resend_ddns('2001:db8:a::1', exp_result=0)
    assert response["text"] == "NCR generated for: 2001:db8:a::1, hostname: sth6.six.example.com."
    response = _resend_ddns('2001:db8:b::1', exp_result=0)
    assert response["text"] == "NCR generated for: 2001:db8:b::1, hostname: some.abc.example.com."
    response = _resend_ddns('2001:db8:c::1', exp_result=0)
    assert response["text"] == "NCR generated for: 2001:db8:c::1, hostname: record.xyz.example.com."

    _check_fqdn_record("sth6.six.example.com.", address='2001:db8:a::1')
    _check_fqdn_record("some.abc.example.com.", address='2001:db8:b::1')
    _check_fqdn_record("record.xyz.example.com.", address='2001:db8:c::1')

    _check_address_record("sth6.six.example.com.",
                          '1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.a.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')
    _check_address_record("some.abc.example.com.",
                          '1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.b.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')
    _check_address_record("record.xyz.example.com.",
                          '1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.c.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')


@pytest.mark.v6
@pytest.mark.ddns
def test_ddns6_all_levels_resend_without_ddns():
    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')

    world.dhcp_cfg["subnet6"][0].update({"ddns-send-updates": True,
                                         "ddns-generated-prefix": "six",
                                         "ddns-qualifying-suffix": "example.com"})

    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.shared_subnet('2001:db8:b::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_forward_ddns('six.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('a.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'EMPTY_KEY')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    srv_control.start_srv('DNS', 'started', config_set=31)

    _get_address_and_update_ddns(duid='00:03:00:01:ff:ff:ff:ff:ff:01', fqdn='sth6.six.example.com.',
                                 address='2001:db8:a::1',
                                 arpa='1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.a.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')

    _get_address(duid='00:03:00:01:ff:ff:ff:ff:ff:02', fqdn=None)

    _check_fqdn_record("some.abc.example.com.", expect='empty')

    # stop bind, remove data files, start bind with empty zones
    srv_control.start_srv('DNS', 'stopped')
    srv_control.clear_some_data('all', service='DNS')
    srv_control.start_srv('DNS', 'started', config_set=31)
    # check is all records were removed
    _check_fqdn_record("sth6.six.example.com.", expect='empty')
    _check_fqdn_record("some.abc.example.com.", expect='empty')
    _check_fqdn_record("record.xyz.example.com.", expect='empty')

    response = _resend_ddns('2001:db8:b::1', exp_result=4)
    assert response["text"] == 'Lease for: 2001:db8:b::1, has no hostname, nothing to update'
    response = _resend_ddns('2001:db8:a::1', exp_result=0)
    assert response["text"] == "NCR generated for: 2001:db8:a::1, hostname: sth6.six.example.com."

    _check_fqdn_record("sth6.six.example.com.", address='2001:db8:a::1')

    _check_address_record("sth6.six.example.com.",
                          '1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.a.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')
    _check_fqdn_record("some.abc.example.com.", expect='empty')
