"""Host Reservation DHCPv6"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_control
from features import misc
from features import srv_msg


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v6_host_reservation_all_values_mac(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-hostname',
                                           '0',
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:01')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'address', '3000::100')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'prefix', '3001::/40')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'my.domain.com')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'IA_PD')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'some-different-name')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::100')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3001::')
    srv_msg.response_check_include_option(step, 'Response', None, '39')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '39',
                                          None,
                                          'fqdn',
                                          'reserved-hostname.my.domain.com')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v6_host_reservation_all_values_duid(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-hostname',
                                           '0',
                                           'duid',
                                           '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'address', '3000::100')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'prefix', '3001::/40')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'my.domain.com')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'IA_PD')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'some-different-name')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::100')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3001::')
    srv_msg.response_check_include_option(step, 'Response', None, '39')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '39',
                                          None,
                                          'fqdn',
                                          'reserved-hostname.my.domain.com')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v6_host_reservation_all_values_duid_2(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_prefix(step, '2001:db8:1::', '0', '32', '33')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-hostname',
                                           '0',
                                           'duid',
                                           '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'address', '3000::100')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'prefix', '2001:db8:1::/40')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'my.domain.com')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'IA_PD')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'some-different-name')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             'NOT ',
                                             'address',
                                             '3000::100')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             'NOT ',
                                             'prefix',
                                             '2001:db8:1::')
    srv_msg.response_check_include_option(step, 'Response', None, '39')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '39',
                                          'NOT ',
                                          'fqdn',
                                          'reserved-hostname.my.domain.com')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v6_host_reservation_classes_1(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::1')
    srv_control.add_line_to_subnet(step,
                                   '0',
                                   ',"reservations": [{"duid": "00:03:00:01:f6:f5:f4:f3:f2:22","client-classes": [ "reserved-class1"]}]')

    srv_control.create_new_class(step, 'reserved-class1')
    srv_control.add_option_to_defined_class(step,
                                            '1',
                                            'sip-server-addr',
                                            '2001:db8::1,2001:db8::2')
    srv_control.add_option_to_defined_class(step, '1', 'preference', '123')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_requests_option(step, '22')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '22')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '7')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_requests_option(step, '22')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '22')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '22',
                                          None,
                                          'addresses',
                                          '2001:db8::1,2001:db8::2')
    srv_msg.response_check_include_option(step, 'Response', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', None, 'prefval', '123')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v6_host_reservation_classes_2(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::1')
    srv_control.add_line_to_subnet(step,
                                   '0',
                                   ',"reservations": [{"duid": "00:03:00:01:f6:f5:f4:f3:f2:22","client-classes": [ "reserved-class1", "reserved-class2" ]}]')

    srv_control.create_new_class(step, 'reserved-class1')
    srv_control.add_option_to_defined_class(step,
                                            '1',
                                            'sip-server-addr',
                                            '2001:db8::1,2001:db8::2')

    srv_control.create_new_class(step, 'reserved-class2')
    srv_control.add_option_to_defined_class(step, '2', 'preference', '123')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_requests_option(step, '22')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '22')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '7')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_requests_option(step, '22')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '22')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '22',
                                          None,
                                          'addresses',
                                          '2001:db8::1,2001:db8::2')
    srv_msg.response_check_include_option(step, 'Response', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', None, 'prefval', '123')
