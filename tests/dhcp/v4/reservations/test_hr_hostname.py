# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Host Reservation DHCPv4"""

import pytest

from src import misc
from src import srv_control
from src import srv_msg


@pytest.mark.v4
@pytest.mark.host_reservation
def test_v4_host_reservation_hostname_hostname_option():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.30-192.168.50.30')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_connectivity_options('enable-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-send-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-qualifying-suffix', 'my.domain.com')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-name',
                                           0,
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.30')
    srv_msg.client_does_include_with_value('hostname', 'some-name')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_include_option(12)
    srv_msg.response_check_option_content(12, 'value', 'reserved-name.my.domain.com')


@pytest.mark.v4
@pytest.mark.host_reservation
def test_v4_host_reservation_hostname_fqdn_option():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.30-192.168.50.30')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_connectivity_options('enable-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-send-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-qualifying-suffix', 'my.domain.com')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-name',
                                           0,
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'sth6.six.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(81)
    srv_msg.response_check_option_content(81, 'fqdn', 'reserved-name.my.domain.com.')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.30')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'sth6.six.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_include_option(81)
    srv_msg.response_check_option_content(81, 'fqdn', 'reserved-name.my.domain.com.')


@pytest.mark.v4
@pytest.mark.host_reservation
def test_v4_host_reservation_hostname_hostname_option_and_address():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.20-192.168.50.30')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_connectivity_options('enable-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-send-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-qualifying-suffix', 'my.domain.com')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-name',
                                           0,
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '192.168.50.5')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.forge_sleep(2, 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    # Client adds to the message hostname with value some-name.
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.5')
    srv_msg.client_does_include_with_value('hostname', 'some-name')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.5')
    srv_msg.response_check_include_option(12)
    srv_msg.response_check_option_content(12, 'value', 'reserved-name.my.domain.com')


@pytest.mark.v4
@pytest.mark.host_reservation
def test_v4_host_reservation_hostname_hostname_option_and_address_2():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.20-192.168.50.30')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_connectivity_options('enable-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-send-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-qualifying-suffix', 'my.domain.com')
    srv_control.host_reservation_in_subnet('ip-address',
                                           '192.168.50.5',
                                           0,
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'hostname', 'reserved-name')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.forge_sleep(2, 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    # Client adds to the message hostname with value some-name.
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.5')
    srv_msg.client_does_include_with_value('hostname', 'some-name')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.5')
    srv_msg.response_check_include_option(12)
    srv_msg.response_check_option_content(12, 'value', 'reserved-name.my.domain.com')


@pytest.mark.v4
@pytest.mark.host_reservation
def test_v4_host_reservation_hostname_hostname_option_and_address_3():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.30')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_connectivity_options('enable-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-send-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-qualifying-suffix', 'my.domain.com')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-name',
                                           0,
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '192.168.50.5')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.forge_sleep(2, 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    # Client adds to the message hostname with value some-name.
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.5')
    srv_msg.client_does_include_with_value('hostname', 'some-name')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.5')
    srv_msg.response_check_include_option(12)
    srv_msg.response_check_option_content(12, 'value', 'reserved-name.my.domain.com')


@pytest.mark.v4
@pytest.mark.host_reservation
def test_v4_host_reservation_hostname_multiple_entries():
    misc.test_setup()
    # outside of the pool
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.30-192.168.50.30')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_connectivity_options('enable-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-send-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-qualifying-suffix', 'my.domain.com')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-name',
                                           0,
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.host_reservation_in_subnet('hostname',
                                           'resderved-name',
                                           0,
                                           'hw-address',
                                           'ff:01:02:03:ff:44')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')


@pytest.mark.v4
@pytest.mark.host_reservation
def test_v4_host_reservation_hostname_duplicated_entries():
    misc.test_setup()
    # outside of the pool
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.30-192.168.50.30')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_connectivity_options('enable-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-send-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-qualifying-suffix', 'my.domain.com')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-name',
                                           0,
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.host_reservation_in_subnet('hostname',
                                           'resderved-name',
                                           0,
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started', should_succeed=False)
