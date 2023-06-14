# Copyright (C) 2023 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""DDNS ttl percentage setting tests"""

# pylint: disable=invalid-name

import pytest

from src import misc
from src import srv_msg
from src import srv_control

from src.forge_cfg import world


def _check_dns_record(dhcp_version, ttl=None, expect_dns_record=True):
    hostname = 'aa.four.example.com.'
    record_type = 'A'
    address = '192.168.50.10'
    ptr = '10.50.168.192.in-addr.arpa.'
    if dhcp_version == "v6":
        hostname = 'sth6.six.example.com.'
        record_type = 'AAAA'
        address = '2001:db8:1::50'
        ptr = '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.'

    misc.test_procedure()
    srv_msg.dns_question_record(hostname, record_type, 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST')
    if expect_dns_record:
        srv_msg.dns_option('ANSWER')
        srv_msg.dns_option_content('ANSWER', 'rdata', address)
        srv_msg.dns_option_content('ANSWER', 'rrname', hostname)
        srv_msg.dns_option_content('ANSWER', 'ttl', ttl)
    else:
        srv_msg.dns_option('ANSWER', expect_include=False)

    misc.test_procedure()
    srv_msg.dns_question_record(ptr, 'PTR', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST')
    if expect_dns_record:
        srv_msg.dns_option('ANSWER')
        srv_msg.dns_option_content('ANSWER', 'rdata', hostname)
        srv_msg.dns_option_content('ANSWER', 'rrname', ptr)
        srv_msg.dns_option_content('ANSWER', 'ttl', ttl)
    else:
        srv_msg.dns_option('ANSWER', expect_include=False)


def _get_lease(dhcp_version):
    if dhcp_version == 'v4':
        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
        srv_msg.client_send_msg('DISCOVER')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'OFFER')
        srv_msg.response_check_content('yiaddr', '192.168.50.10')

        misc.test_procedure()
        srv_msg.client_copy_option('server_id')
        srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
        srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
        srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'aa.four.example.com.')
        srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
        srv_msg.client_does_include('Client', 'fqdn')
        srv_msg.client_send_msg('REQUEST')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'ACK')
        srv_msg.response_check_content('yiaddr', '192.168.50.10')
        srv_msg.response_check_include_option(81)
        srv_msg.response_check_option_content(81, 'flags', 1)
        srv_msg.response_check_option_content(81, 'fqdn', 'aa.four.example.com.')
    else:
        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_does_include('Client', 'IA-NA')
        srv_msg.client_send_msg('SOLICIT')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
        srv_msg.client_copy_option('IA_NA')
        srv_msg.client_copy_option('server-id')
        srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'sth6.six.example.com.')
        srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
        srv_msg.client_does_include('Client', 'fqdn')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_send_msg('REQUEST')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'REPLY')
        srv_msg.response_check_include_option(39)
        srv_msg.response_check_option_content(39, 'flags', 'S')
        # we always expect this one fqdn back
        srv_msg.response_check_option_content(39, 'fqdn', 'sth6.six.example.com.')
        srv_msg.response_check_include_option(3)
        srv_msg.response_check_option_content(3, 'sub-option', 5)
        srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::50')


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.parametrize('level', ['global', 'shared_networks', 'subnet'])
@pytest.mark.parametrize('ttl', [None, 0.66, 1.0])
def test_ddns_ttl_different_levels(dhcp_version, level, ttl):
    """
    Check if ddns-ttl-percent works correctly on different levels
    """
    misc.test_setup()
    vlt = 10000
    # dhcp
    srv_control.set_time('valid-lifetime', vlt)
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
        srv_control.shared_subnet('192.168.50.0/24', 0)
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
        srv_control.shared_subnet('2001:db8:1::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    # dns
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    if dhcp_version == 'v4':
        srv_control.add_ddns_server_options('generated-prefix', 'four')
        srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
        srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')
        srv_control.use_dns_set_number(20)
    else:
        srv_control.add_ddns_server_options('generated-prefix', 'six')
        srv_control.add_forward_ddns('six.example.com.', 'EMPTY_KEY')
        srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'EMPTY_KEY')
        srv_control.use_dns_set_number(1)

    # ttl on different levels
    if ttl:
        cfg = {"ddns-ttl-percent": ttl}
        if level == 'global':
            world.dhcp_cfg.update(cfg)
        elif level == 'shared_networks':
            world.dhcp_cfg.update({"ddns-ttl-percent": 0.5})  # let's check if globals are overwritten
            world.dhcp_cfg['shared-networks'][0].update(cfg)
        elif level == 'subnet':
            world.dhcp_cfg.update({"ddns-ttl-percent": 0.5})  # let's check if globals are overwritten
            world.dhcp_cfg['shared-networks'][0].update({"ddns-ttl-percent": 0.5})  # and network
            world.dhcp_cfg['shared-networks'][0][f'subnet{dhcp_version[1]}'][0].update(cfg)
        else:
            assert False, "ddns-ttl-percent can be configured only on global, networks or subnet"
    # send
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    srv_control.start_srv('DNS', 'started')

    _check_dns_record(dhcp_version, expect_dns_record=False)
    _get_lease(dhcp_version)

    # if ddns-ttl-percent was configured calculate it based on valid lifetime and ttl percentage value,
    # if not it will be 1/3 - it's kea default
    _check_dns_record(dhcp_version, ttl=int(vlt * ttl) if ttl else int(vlt * 1/3))
