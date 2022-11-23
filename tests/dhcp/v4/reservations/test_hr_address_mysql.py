# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Host Reservation DHCPv4 stored in MySQL database."""

import pytest

from src import srv_msg
from src import misc
from src import srv_control


@pytest.mark.v4
@pytest.mark.host_reservation
def test_v4_host_reservation_mysql_one_address_inside_pool():
    misc.test_setup()
    # outside of the pool
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'ff:01:02:03:ff:04')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'MySQL', 1)
    srv_control.update_db_backend_reservation('ipv4_address', '192.168.50.10', 'MySQL', 1)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'MySQL', 1)
    srv_control.upload_db_reservation('MySQL')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    result = srv_msg.send_ctrl_cmd_via_http('{"command":"config-get", "service": ["dhcp4"], "arguments": {} }',
                                            '$(SRV4_ADDR)')
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.host_reservation
def test_v4_host_reservation_mysql_one_address_inside_pool_option():
    misc.test_setup()
    # outside of the pool
    # TODO update names
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'ff:01:02:03:ff:04')
    srv_control.update_db_backend_reservation('next_server', '11.1.1.1', 'MySQL', 1)
    srv_control.update_db_backend_reservation('server_hostname',
                                              'hostname-server.com',
                                              'MySQL',
                                              1)
    srv_control.update_db_backend_reservation('boot_file_name', 'file-name', 'MySQL', 1)
    srv_control.update_db_backend_reservation('ipv4_address', '192.168.50.10', 'MySQL', 1)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'MySQL', 1)
    srv_control.option_db_record_reservation(11,
                                             '10.0.0.1',
                                             'dhcp4',
                                             1,
                                             '$(EMPTY)',
                                             1,
                                             'host',
                                             'MySQL',
                                             1)
    srv_control.config_srv_opt('resource-location-servers', '199.199.199.1,150.150.150.1')
    srv_control.upload_db_reservation('MySQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(11)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(11)
    srv_msg.response_check_option_content(11, 'value', '10.0.0.1')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.host_reservation
def test_v4_host_reservation_mysql_one_address_outside_pool_dual_backend():
    misc.test_setup()
    # outside of the pool
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.30-192.168.50.50')
    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'ff:01:02:03:ff:04')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'MySQL', 1)
    srv_control.update_db_backend_reservation('ipv4_address', '192.168.50.10', 'MySQL', 1)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'MySQL', 1)
    srv_control.upload_db_reservation('MySQL')
    srv_control.host_reservation_in_subnet('ip-address',
                                           '192.168.50.11',
                                           0,
                                           'hw-address',
                                           'ff:01:02:03:ff:03')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:03')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.11')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.11')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:03')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.11')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.host_reservation
def test_v4_host_reservation_mysql_one_address_inside_pool_different_mac():
    misc.test_setup()
    # request address from different mac that has been reserved
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'ff:01:02:03:ff:04')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'MySQL', 1)
    srv_control.update_db_backend_reservation('ipv4_address', '192.168.50.10', 'MySQL', 1)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'MySQL', 1)
    srv_control.upload_db_reservation('MySQL')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10', expected=False)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'NAK')
    srv_msg.response_check_content('yiaddr', '0.0.0.0')


@pytest.mark.v4
@pytest.mark.host_reservation
def test_v4_host_reservation_one_address_empty_pool():
    misc.test_setup()
    # request address from different mac that has been reserved
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.host_reservation_in_subnet('ip-address',
                                           '192.168.50.10',
                                           0,
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()


@pytest.mark.v4
@pytest.mark.host_reservation
def test_v4_host_reservation_mysql_multiple_address_reservation_empty_pool():
    misc.test_setup()
    # request address from different mac that has been reserved
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'ff:01:02:03:ff:04')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'MySQL', 1)
    srv_control.update_db_backend_reservation('ipv4_address', '192.168.50.10', 'MySQL', 1)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'MySQL', 1)

    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'ff:01:02:03:ff:03')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'MySQL', 2)
    srv_control.update_db_backend_reservation('ipv4_address', '192.168.50.11', 'MySQL', 2)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'MySQL', 2)
    srv_control.upload_db_reservation('MySQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()


@pytest.mark.v4
@pytest.mark.host_reservation
def test_v4_host_reservation_multiple_mysql_address_reservation_empty_pool_2():
    misc.test_setup()
    # request address from different mac that has been reserved
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.12')
    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'ff:01:02:03:ff:04')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'MySQL', 1)
    srv_control.update_db_backend_reservation('ipv4_address', '192.168.50.10', 'MySQL', 1)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'MySQL', 1)

    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'ff:01:02:03:ff:03')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'MySQL', 2)
    srv_control.update_db_backend_reservation('ipv4_address', '192.168.50.11', 'MySQL', 2)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'MySQL', 2)

    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'ff:01:02:03:ff:02')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'MySQL', 3)
    srv_control.update_db_backend_reservation('ipv4_address', '192.168.50.12', 'MySQL', 3)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'MySQL', 3)

    srv_control.upload_db_reservation('MySQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:03')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:03')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:02')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:02')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()
