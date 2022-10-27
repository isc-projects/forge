# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Host Reservation DHCPv6 stored in PostgreSQL database."""

import pytest

from src import srv_msg
from src import misc
from src import srv_control


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.pgsql
def test_v6_host_reservation_pgsql_all_values_mac():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'PostgreSQL', 1)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'PostgreSQL', 1)
    srv_control.ipv6_prefix_db_backend_reservation('3001::', 40, '$(EMPTY)', 'PostgreSQL', 1)
    srv_control.ipv6_address_db_backend_reservation('3000::100', '$(EMPTY)', 'PostgreSQL', 1)
    srv_control.ipv6_address_db_backend_reservation('3000::101', '$(EMPTY)', 'PostgreSQL', 1)
    srv_control.option_db_record_reservation(32,
                                             10,
                                             'dhcp6',
                                             1,
                                             '$(EMPTY)',
                                             1,
                                             'host',
                                             'PostgreSQL',
                                             1)
    srv_control.upload_db_reservation('PostgreSQL')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_ddns_server_options('qualifying-suffix', 'my.domain.com')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'ia_id', 666)
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'some-different-name')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_requests_option(32)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::100')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '3001::')
    srv_msg.response_check_include_option(39)
    srv_msg.response_check_option_content(39, 'fqdn', 'reserved-hostname.my.domain.com.')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'ia_id', '777')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'some-different-name')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_requests_option(32)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::100', expect_include=False)


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.pgsql
def test_v6_host_reservation_pgsql_duid_ll_matching():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.new_db_backend_reservation('PostgreSQL', 'duid', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'PostgreSQL', 1)
    srv_control.ipv6_address_db_backend_reservation('3000::100', '$(EMPTY)', 'PostgreSQL', 1)
    srv_control.upload_db_reservation('PostgreSQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::100')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.pgsql
def test_v6_host_reservation_pgsql_hwaddrr_not_matching():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'PostgreSQL', 1)
    srv_control.ipv6_address_db_backend_reservation('3000::100', '$(EMPTY)', 'PostgreSQL', 1)
    srv_control.upload_db_reservation('PostgreSQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::100', expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::100', expect_include=False)


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.pgsql
def test_v6_host_reservation_pgsql_hwaddrr_matching():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'PostgreSQL', 1)
    srv_control.ipv6_address_db_backend_reservation('3000::100', '$(EMPTY)', 'PostgreSQL', 1)
    srv_control.upload_db_reservation('PostgreSQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::100')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::100')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.pgsql
def test_v6_host_reservation_pgsql_hwaddrr_matching_dual_backend():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:11')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'PostgreSQL', 1)
    srv_control.ipv6_address_db_backend_reservation('3000::100', '$(EMPTY)', 'PostgreSQL', 1)
    srv_control.upload_db_reservation('PostgreSQL')

    srv_control.host_reservation_in_subnet('ip-address',
                                           '3000::fff',
                                           0,
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:22')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::100')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::fff')
