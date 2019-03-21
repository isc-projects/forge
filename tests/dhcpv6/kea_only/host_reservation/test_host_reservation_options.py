"""Host Reservation including options DHCPv6 stored in MySQL database"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_control
import misc
import srv_msg


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
@pytest.mark.reserved_options
def test_v6_host_reservation_mysql_duid_ll_matching_option():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.new_db_backend_reservation('MySQL', 'duid', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '1', 'MySQL', '1')
    srv_control.ipv6_address_db_backend_reservation('3000::100', '$(EMPTY)', 'MySQL', '1')
    srv_control.option_db_record_reservation('7',
                                             '10',
                                             'dhcp6',
                                             '1',
                                             '$(EMPTY)',
                                             '1',
                                             'subnet',
                                             'MySQL',
                                             '1')
    srv_control.upload_db_reservation('MySQL')

    srv_control.config_srv('preference', '0', '123')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::100')
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'value', '10')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:21')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'value', '123')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
@pytest.mark.reserved_options
def test_v6_host_reservation_mysql_duid_ll_matching_option_no_address_1():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.new_db_backend_reservation('MySQL', 'duid', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '1', 'MySQL', '1')
    srv_control.option_db_record_reservation('7',
                                             '10',
                                             'dhcp6',
                                             '1',
                                             '$(EMPTY)',
                                             '1',
                                             'subnet',
                                             'MySQL',
                                             '1')
    srv_control.upload_db_reservation('MySQL')

    srv_control.config_srv('preference', '0', '123')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', 'NOT ', 'addr', '3000::100')
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'value', '10')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:21')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'value', '123')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
@pytest.mark.reserved_options
def test_v6_host_reservation_mysql_duid_ll_matching_option_no_address_2():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.new_db_backend_reservation('MySQL', 'duid', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '1', 'MySQL', '1')
    srv_control.option_db_record_reservation('7',
                                             '10',
                                             'dhcp6',
                                             '1',
                                             '$(EMPTY)',
                                             '1',
                                             'subnet',
                                             'MySQL',
                                             '1')
    srv_control.upload_db_reservation('MySQL')

    srv_control.config_srv('preference', '0', '123')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', 'NOT ', 'addr', '3000::100')
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'value', '10')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', 'NOT ', '3')
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'value', '10')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:21')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'value', '123')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
@pytest.mark.reserved_options
def test_v6_host_reservation_mysql_duid_ll_matching_option_inforequest():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.new_db_backend_reservation('MySQL', 'duid', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '1', 'MySQL', '1')
    srv_control.option_db_record_reservation('7',
                                             '10',
                                             'dhcp6',
                                             '1',
                                             '$(EMPTY)',
                                             '1',
                                             'subnet',
                                             'MySQL',
                                             '1')
    srv_control.upload_db_reservation('MySQL')

    srv_control.config_srv('preference', '0', '123')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_requests_option('7')
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', 'NOT ', '3')
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'value', '123')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', 'NOT ', '3')
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'value', '10')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:21')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'value', '123')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
@pytest.mark.reserved_options
def test_v6_host_reservation_mysql_option_multiple():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.new_db_backend_reservation('MySQL', 'duid', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '1', 'MySQL', '1')
    srv_control.ipv6_address_db_backend_reservation('3000::100', '$(EMPTY)', 'MySQL', '1')
    srv_control.option_db_record_reservation('7',
                                             '10',
                                             'dhcp6',
                                             '1',
                                             '$(EMPTY)',
                                             '1',
                                             'subnet',
                                             'MySQL',
                                             '1')
    srv_control.option_db_record_reservation('21',
                                             'srv1.example.com,srv2.isc.org',
                                             'dhcp6',
                                             '1',
                                             '$(EMPTY)',
                                             '1',
                                             'subnet',
                                             'MySQL',
                                             '1')
    srv_control.option_db_record_reservation('23',
                                             '2001:db8::1,2001:db8::2',
                                             'dhcp6',
                                             '1',
                                             '$(EMPTY)',
                                             '1',
                                             'subnet',
                                             'MySQL',
                                             '1')
    srv_control.option_db_record_reservation('59',
                                             'http://www.kea-reserved.isc.org',
                                             'dhcp6',
                                             '1',
                                             '$(EMPTY)',
                                             '1',
                                             'subnet',
                                             'MySQL',
                                             '1')
    # Add option reservation code 60 value 10 space dhcp6 persistent 1 client class $(EMPTY) subnet id 1 and scope subnet to MySQL record id 1.

    srv_control.upload_db_reservation('MySQL')

    srv_control.config_srv('preference', '0', '123')
    srv_control.config_srv_opt('sip-server-dns', 'srv4.example.com,srv5.isc.org')
    # 21
    srv_control.config_srv_opt('dns-servers', '2001:db8::4,2001:db8::5')
    # 23
    srv_control.config_srv_opt('bootfile-url', 'http://www.kea.isc.org')
    # 59
    srv_control.config_srv_opt('bootfile-param', '000B48656C6C6F20776F726C640003666F6F')
    # 60
    srv_control.config_srv_opt('new-tzdb-timezone', 'Europe/Zurich')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_requests_option('7')
    srv_msg.client_requests_option('21')
    srv_msg.client_requests_option('23')
    srv_msg.client_requests_option('42')
    srv_msg.client_requests_option('59')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::100')
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'value', '10')
    srv_msg.response_check_include_option('Response', None, '59')
    srv_msg.response_check_option_content('Response',
                                          '59',
                                          None,
                                          'optdata',
                                          'http://www.kea-reserved.isc.org')
    srv_msg.response_check_include_option('Response', None, '21')
    srv_msg.response_check_option_content('Response',
                                          '21',
                                          None,
                                          'addr',
                                          'srv1.example.com.,srv2.isc.org.')
    srv_msg.response_check_include_option('Response', None, '23')
    srv_msg.response_check_option_content('Response',
                                          '23',
                                          None,
                                          'addr',
                                          '2001:db8::1,2001:db8::2')
    srv_msg.response_check_include_option('Response', None, '42')
    srv_msg.response_check_option_content('Response', '42', None, 'optdata', 'Europe/Zurich')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:21')
    srv_msg.client_requests_option('7')
    srv_msg.client_requests_option('21')
    srv_msg.client_requests_option('42')
    srv_msg.client_requests_option('23')
    srv_msg.client_requests_option('59')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'value', '123')
    srv_msg.response_check_include_option('Response', None, '59')
    srv_msg.response_check_option_content('Response',
                                          '59',
                                          None,
                                          'optdata',
                                          'http://www.kea.isc.org')
    srv_msg.response_check_include_option('Response', None, '21')
    srv_msg.response_check_option_content('Response',
                                          '21',
                                          None,
                                          'addr',
                                          'srv4.example.com.,srv5.isc.org.')
    srv_msg.response_check_include_option('Response', None, '23')
    srv_msg.response_check_option_content('Response',
                                          '23',
                                          None,
                                          'addr',
                                          '2001:db8::4,2001:db8::5')
    srv_msg.response_check_include_option('Response', None, '42')
    srv_msg.response_check_option_content('Response', '42', None, 'optdata', 'Europe/Zurich')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
@pytest.mark.reserved_options
def test_v6_host_reservation_pgsql_hwaddrr_matching_option():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '1', 'PostgreSQL', '1')
    srv_control.ipv6_address_db_backend_reservation('3000::100', '$(EMPTY)', 'PostgreSQL', '1')
    srv_control.option_db_record_reservation('7',
                                             '10',
                                             'dhcp6',
                                             '1',
                                             '$(EMPTY)',
                                             '1',
                                             'subnet',
                                             'PostgreSQL',
                                             '1')
    srv_control.upload_db_reservation('PostgreSQL')

    srv_control.config_srv_opt('preference', '12')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    # Response sub-option 5 from option 3 MUST contain address 3000::100.
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'value', '10')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    # Response sub-option 5 from option 3 MUST contain address 3000::100.
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'value', '12')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
@pytest.mark.reserved_options
def test_v6_host_reservation_pgsql_hwaddrr_matching_option_no_address():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '1', 'PostgreSQL', '1')
    srv_control.option_db_record_reservation('7',
                                             '10',
                                             'dhcp6',
                                             '1',
                                             '$(EMPTY)',
                                             '1',
                                             'subnet',
                                             'PostgreSQL',
                                             '1')
    srv_control.upload_db_reservation('PostgreSQL')

    srv_control.config_srv_opt('preference', '12')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', 'NOT ', '3')
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'value', '10')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', 'NOT ', '3')
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'value', '12')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
@pytest.mark.reserved_options
def test_v6_host_reservation_pgsql_hwaddrr_matching_option_inforequest():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '1', 'PostgreSQL', '1')
    srv_control.option_db_record_reservation('7',
                                             '10',
                                             'dhcp6',
                                             '1',
                                             '$(EMPTY)',
                                             '1',
                                             'subnet',
                                             'PostgreSQL',
                                             '1')
    srv_control.upload_db_reservation('PostgreSQL')

    srv_control.config_srv_opt('preference', '12')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')
    srv_msg.client_requests_option('7')
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', 'NOT ', '3')
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'value', '12')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', 'NOT ', '3')
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'value', '10')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
@pytest.mark.reserved_options
def test_v6_host_reservation_pgsql_option_multiple():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.new_db_backend_reservation('PostgreSQL', 'duid', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '1', 'PostgreSQL', '1')
    srv_control.ipv6_address_db_backend_reservation('3000::100', '$(EMPTY)', 'PostgreSQL', '1')
    srv_control.option_db_record_reservation('7',
                                             '10',
                                             'dhcp6',
                                             '1',
                                             '$(EMPTY)',
                                             '1',
                                             'subnet',
                                             'PostgreSQL',
                                             '1')
    srv_control.option_db_record_reservation('21',
                                             'srv1.example.com,srv2.isc.org',
                                             'dhcp6',
                                             '1',
                                             '$(EMPTY)',
                                             '1',
                                             'subnet',
                                             'PostgreSQL',
                                             '1')
    srv_control.option_db_record_reservation('23',
                                             '2001:db8::1,2001:db8::2',
                                             'dhcp6',
                                             '1',
                                             '$(EMPTY)',
                                             '1',
                                             'subnet',
                                             'PostgreSQL',
                                             '1')
    srv_control.option_db_record_reservation('59',
                                             'http://www.kea-reserved.isc.org',
                                             'dhcp6',
                                             '1',
                                             '$(EMPTY)',
                                             '1',
                                             'subnet',
                                             'PostgreSQL',
                                             '1')
    # Add option reservation code 60 value 10 space dhcp6 persistent 1 client class $(EMPTY) subnet id 1 and scope subnet to MySQL record id 1.

    srv_control.upload_db_reservation('PostgreSQL')

    srv_control.config_srv('preference', '0', '123')
    srv_control.config_srv_opt('sip-server-dns', 'srv4.example.com,srv5.isc.org')
    # 21
    srv_control.config_srv_opt('dns-servers', '2001:db8::4,2001:db8::5')
    # 23
    srv_control.config_srv_opt('bootfile-url', 'http://www.kea.isc.org')
    # 59
    srv_control.config_srv_opt('new-tzdb-timezone', 'Europe/Zurich')
    # 60 and not reserved
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_requests_option('7')
    srv_msg.client_requests_option('21')
    srv_msg.client_requests_option('23')
    srv_msg.client_requests_option('42')
    srv_msg.client_requests_option('59')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::100')
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'value', '10')
    srv_msg.response_check_include_option('Response', None, '59')
    srv_msg.response_check_option_content('Response',
                                          '59',
                                          None,
                                          'optdata',
                                          'http://www.kea-reserved.isc.org')
    srv_msg.response_check_include_option('Response', None, '21')
    srv_msg.response_check_option_content('Response',
                                          '21',
                                          None,
                                          'addr',
                                          'srv1.example.com.,srv2.isc.org.')
    srv_msg.response_check_include_option('Response', None, '23')
    srv_msg.response_check_option_content('Response',
                                          '23',
                                          None,
                                          'addr',
                                          '2001:db8::1,2001:db8::2')
    srv_msg.response_check_include_option('Response', None, '42')
    srv_msg.response_check_option_content('Response', '42', None, 'optdata', 'Europe/Zurich')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:21')
    srv_msg.client_requests_option('7')
    srv_msg.client_requests_option('21')
    srv_msg.client_requests_option('23')
    srv_msg.client_requests_option('59')
    srv_msg.client_requests_option('42')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'value', '123')
    srv_msg.response_check_include_option('Response', None, '59')
    srv_msg.response_check_option_content('Response',
                                          '59',
                                          None,
                                          'optdata',
                                          'http://www.kea.isc.org')
    srv_msg.response_check_include_option('Response', None, '21')
    srv_msg.response_check_option_content('Response',
                                          '21',
                                          None,
                                          'addr',
                                          'srv4.example.com.,srv5.isc.org.')
    srv_msg.response_check_include_option('Response', None, '23')
    srv_msg.response_check_option_content('Response',
                                          '23',
                                          None,
                                          'addr',
                                          '2001:db8::4,2001:db8::5')
    srv_msg.response_check_include_option('Response', None, '42')
    srv_msg.response_check_option_content('Response', '42', None, 'optdata', 'Europe/Zurich')
