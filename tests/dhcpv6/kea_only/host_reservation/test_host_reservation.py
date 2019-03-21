"""Host Reservation DHCPv6"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_control
import srv_msg
import misc


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v6_host_reservation_all_values_mac():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           '0',
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:01')
    srv_control.host_reservation_in_subnet_add_value('0', '0', 'address', '3000::100')
    srv_control.host_reservation_in_subnet_add_value('0', '0', 'prefix', '3001::/40')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('qualifying-suffix', 'my.domain.com')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'IA-PD')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'some-different-name')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::100')
    srv_msg.response_check_include_option('Response', None, '25')
    srv_msg.response_check_option_content('Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content('Response', '26', '25', None, 'prefix', '3001::')
    srv_msg.response_check_include_option('Response', None, '39')
    srv_msg.response_check_option_content('Response',
                                          '39',
                                          None,
                                          'fqdn',
                                          'reserved-hostname.my.domain.com.')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v6_host_reservation_all_values_duid():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           '0',
                                           'duid',
                                           '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.host_reservation_in_subnet_add_value('0', '0', 'address', '3000::100')
    srv_control.host_reservation_in_subnet_add_value('0', '0', 'prefix', '3001::/40')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('qualifying-suffix', 'my.domain.com')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'IA-PD')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'some-different-name')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::100')
    srv_msg.response_check_include_option('Response', None, '25')
    srv_msg.response_check_option_content('Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content('Response', '26', '25', None, 'prefix', '3001::')
    srv_msg.response_check_include_option('Response', None, '39')
    srv_msg.response_check_option_content('Response',
                                          '39',
                                          None,
                                          'fqdn',
                                          'reserved-hostname.my.domain.com.')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v6_host_reservation_all_values_duid_2():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_prefix('2001:db8:1::', '0', '32', '33')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           '0',
                                           'duid',
                                           '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.host_reservation_in_subnet_add_value('0', '0', 'address', '3000::100')
    srv_control.host_reservation_in_subnet_add_value('0', '0', 'prefix', '2001:db8:1::/40')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('qualifying-suffix', 'my.domain.com')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'IA-PD')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_sets_value('Client', 'DUID', '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'some-different-name')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', 'NOT ', 'addr', '3000::100')
    srv_msg.response_check_include_option('Response', None, '25')
    srv_msg.response_check_option_content('Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content('Response',
                                             '26',
                                             '25',
                                             'NOT ',
                                             'prefix',
                                             '2001:db8:1::')
    srv_msg.response_check_include_option('Response', None, '39')
    srv_msg.response_check_option_content('Response',
                                          '39',
                                          'NOT ',
                                          'fqdn',
                                          'reserved-hostname.my.domain.com.')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v6_host_reservation_classes_1():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.add_line_to_subnet('0',
                                   ',"reservations": [{"duid": "00:03:00:01:f6:f5:f4:f3:f2:22","client-classes": [ "reserved-class1"]}]')

    srv_control.create_new_class('reserved-class1')
    srv_control.add_option_to_defined_class('1', 'sip-server-addr', '2001:db8::1,2001:db8::2')
    srv_control.add_option_to_defined_class('1', 'preference', '123')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_requests_option('7')
    srv_msg.client_requests_option('22')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', 'NOT ', '22')
    srv_msg.response_check_include_option('Response', 'NOT ', '7')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_requests_option('7')
    srv_msg.client_requests_option('22')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '22')
    srv_msg.response_check_option_content('Response',
                                          '22',
                                          None,
                                          'addresses',
                                          '2001:db8::1,2001:db8::2')
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'prefval', '123')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v6_host_reservation_classes_2():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.add_line_to_subnet('0',
                                   ',"reservations": [{"duid": "00:03:00:01:f6:f5:f4:f3:f2:22","client-classes": [ "reserved-class1", "reserved-class2" ]}]')

    srv_control.create_new_class('reserved-class1')
    srv_control.add_option_to_defined_class('1', 'sip-server-addr', '2001:db8::1,2001:db8::2')

    srv_control.create_new_class('reserved-class2')
    srv_control.add_option_to_defined_class('2', 'preference', '123')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_requests_option('7')
    srv_msg.client_requests_option('22')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', 'NOT ', '22')
    srv_msg.response_check_include_option('Response', 'NOT ', '7')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_requests_option('7')
    srv_msg.client_requests_option('22')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '22')
    srv_msg.response_check_option_content('Response',
                                          '22',
                                          None,
                                          'addresses',
                                          '2001:db8::1,2001:db8::2')
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'prefval', '123')
