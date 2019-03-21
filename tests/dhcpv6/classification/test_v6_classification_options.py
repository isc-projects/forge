"""Client Classification DHCPv6"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_msg
import misc
import srv_control


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.classification
def test_v6_client_classification_multiple_subnets():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')

    srv_control.create_new_class('Client_Class_1')
    srv_control.add_test_to_class('1', 'test', 'substring(option[1].hex,8,2) == 0xf2f1')
    # To class no 1 add option dns-servers with value 2001:db8::666.
    srv_control.config_client_classification('0', 'Client_Class_1')

    srv_control.create_new_class('Client_Class_2')
    srv_control.add_test_to_class('2', 'test', 'substring(option[1].hex,8,2) == 0xf2f2')
    srv_control.config_client_classification('1', 'Client_Class_2')

    srv_control.create_new_class('Client_Class_3')
    srv_control.add_test_to_class('3', 'test', 'substring(option[1].hex,8,2) == 0xf299')
    srv_control.config_client_classification('2', 'Client_Class_3')

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:11:11:11:11:11:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content('Response', '13', '3', None, 'statuscode', '2')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f1')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:a::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f2')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:b::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:99')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:c::1')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.classification
def test_v6_client_classification_multiple_subnets_2():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')

    srv_control.create_new_class('Client_Class_1')
    srv_control.add_test_to_class('1', 'test', 'substring(option[1].hex,8,2) == 0xf2f1')
    # To class no 1 add option dns-servers with value 2001:db8::666.
    srv_control.config_client_classification('0', 'Client_Class_1')

    srv_control.create_new_class('Client_Class_2')
    srv_control.add_test_to_class('2', 'test', 'substring(option[1].hex,8,2) == 0xf2f2')
    srv_control.config_client_classification('1', 'Client_Class_2')

    srv_control.create_new_class('Client_Class_3')
    srv_control.add_test_to_class('3', 'test', 'substring(option[1].hex,8,2) == 0xf299')
    srv_control.config_client_classification('2', 'Client_Class_3')

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:11:11:11:11:11:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:d::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f1')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:a::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f2')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:b::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:99')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:c::1')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.classification
def test_v6_client_classification_class_with_option():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')

    srv_control.create_new_class('Client_Class_1')
    srv_control.add_test_to_class('1', 'test', 'substring(option[1].hex,8,2) == 0xf2f1')
    srv_control.add_option_to_defined_class('1', 'dns-servers', '2001:db8::666')
    srv_control.config_client_classification('0', 'Client_Class_1')

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f1')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_requests_option('23')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '23')
    srv_msg.response_check_option_content('Response', '23', None, 'addresses', '2001:db8::666')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:a::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f1')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', 'NOT ', '23')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:a::1')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.classification
def test_v6_client_classification_multiple_subnets_options():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')

    srv_control.create_new_class('Client_Class_1')
    srv_control.add_test_to_class('1', 'test', 'substring(option[1].hex,8,2) == 0xf2f1')
    srv_control.add_option_to_defined_class('1', 'dns-servers', '2001:db8::888')
    srv_control.config_client_classification('0', 'Client_Class_1')

    srv_control.create_new_class('Client_Class_2')
    srv_control.add_test_to_class('2', 'test', 'substring(option[1].hex,8,2) == 0xf2f2')
    srv_control.add_option_to_defined_class('2', 'dns-servers', '2001:db8::777')
    srv_control.config_client_classification('1', 'Client_Class_2')

    srv_control.create_new_class('Client_Class_3')
    srv_control.add_test_to_class('3', 'test', 'substring(option[1].hex,8,2) == 0xf299')
    srv_control.add_option_to_defined_class('3', 'dns-servers', '2001:db8::999')
    srv_control.config_client_classification('2', 'Client_Class_3')

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:11:11:11:11:11:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_requests_option('23')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', 'NOT ', '23')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:d::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f1')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_requests_option('23')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '23')
    srv_msg.response_check_option_content('Response', '23', None, 'addresses', '2001:db8::888')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:a::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f2')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_requests_option('23')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '23')
    srv_msg.response_check_option_content('Response', '23', None, 'addresses', '2001:db8::777')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:b::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:99')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_requests_option('23')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '23')
    srv_msg.response_check_option_content('Response', '23', None, 'addresses', '2001:db8::999')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:c::1')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.classification
def test_v6_client_classification_multiple_subnets_options_override_global():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')

    srv_control.config_srv_opt('dns-servers', '2001:db8::1,2001:db8::2')

    srv_control.create_new_class('Client_Class_1')
    srv_control.add_test_to_class('1', 'test', 'substring(option[1].hex,8,2) == 0xf2f1')
    srv_control.add_option_to_defined_class('1', 'dns-servers', '2001:db8::888')
    srv_control.config_client_classification('0', 'Client_Class_1')

    srv_control.create_new_class('Client_Class_2')
    srv_control.add_test_to_class('2', 'test', 'substring(option[1].hex,8,2) == 0xf2f2')
    srv_control.add_option_to_defined_class('2', 'dns-servers', '2001:db8::777')
    srv_control.config_client_classification('1', 'Client_Class_2')

    srv_control.create_new_class('Client_Class_3')
    srv_control.add_test_to_class('3', 'test', 'substring(option[1].hex,8,2) == 0xf299')
    srv_control.add_option_to_defined_class('3', 'dns-servers', '2001:db8::999')
    srv_control.config_client_classification('2', 'Client_Class_3')

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:11:11:11:11:11:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_requests_option('23')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '23')
    srv_msg.response_check_option_content('Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::1,2001:db8::2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:d::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f1')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_requests_option('23')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '23')
    srv_msg.response_check_option_content('Response', '23', None, 'addresses', '2001:db8::888')
    srv_msg.response_check_option_content('Response', '23', 'NOT ', 'addresses', '2001:db8::2')
    srv_msg.response_check_option_content('Response', '23', 'NOT ', 'addresses', '2001:db8::1')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:a::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f2')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_requests_option('23')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '23')
    srv_msg.response_check_option_content('Response', '23', None, 'addresses', '2001:db8::777')
    srv_msg.response_check_option_content('Response', '23', 'NOT ', 'addresses', '2001:db8::2')
    srv_msg.response_check_option_content('Response', '23', 'NOT ', 'addresses', '2001:db8::1')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:b::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:99')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_requests_option('23')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '23')
    srv_msg.response_check_option_content('Response', '23', None, 'addresses', '2001:db8::999')
    srv_msg.response_check_option_content('Response', '23', 'NOT ', 'addresses', '2001:db8::2')
    srv_msg.response_check_option_content('Response', '23', 'NOT ', 'addresses', '2001:db8::1')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:c::1')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.classification
@pytest.mark.sharedsubnets
def test_v6_client_classification_shared_subnet_options_override():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::10')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')

    srv_control.create_new_class('Client_Class_1')
    srv_control.add_test_to_class('1', 'test', 'substring(option[1].hex,8,2) == 0xf2f1')
    srv_control.add_option_to_defined_class('1', 'dns-servers', '2001:db8::888')
    srv_control.config_client_classification('0', 'Client_Class_1')

    srv_control.shared_subnet('0', '0')
    srv_control.shared_subnet('1', '0')

    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', '0')
    srv_control.set_conf_parameter_shared_subnet('option-data',
                                                 '[{"csv-format":true,"code":23,"data":"2001:db8::1","name":"dns-servers","space":"dhcp6"}]',
                                                 '0')

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f2')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_requests_option('23')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '23')
    srv_msg.response_check_option_content('Response', '23', 'NOT ', 'addresses', '2001:db8::888')
    srv_msg.response_check_option_content('Response', '23', None, 'addresses', '2001:db8::1')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:b::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f1')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_requests_option('23')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '23')
    srv_msg.response_check_option_content('Response', '23', None, 'addresses', '2001:db8::888')
    srv_msg.response_check_option_content('Response', '23', 'NOT ', 'addresses', '2001:db8::1')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:a::1')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.classification
@pytest.mark.sharedsubnets
def test_v6_client_classification_shared_subnet_options_override_francis():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::10')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')

    srv_control.create_new_class('Client_Class_1')
    srv_control.add_test_to_class('1', 'test', 'substring(option[1].hex,8,2) == 0xf2f1')
    srv_control.add_test_to_class('1', 'only-if-required', 'true')
    srv_control.add_option_to_defined_class('1', 'dns-servers', '2001:db8::888')
    # Server is configured with client-classification option in subnet 0 with name Client_Class_1.
    srv_control.config_require_client_classification('0', 'Client_Class_1')

    srv_control.shared_subnet('0', '0')
    srv_control.shared_subnet('1', '0')

    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', '0')
    srv_control.set_conf_parameter_shared_subnet('option-data',
                                                 '[{"csv-format":true,"code":23,"data":"2001:db8::1","name":"dns-servers","space":"dhcp6"}]',
                                                 '0')

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f2')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_requests_option('23')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '23')
    srv_msg.response_check_option_content('Response', '23', 'NOT ', 'addresses', '2001:db8::888')
    srv_msg.response_check_option_content('Response', '23', None, 'addresses', '2001:db8::1')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:b::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f1')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_requests_option('23')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '23')
    srv_msg.response_check_option_content('Response', '23', None, 'addresses', '2001:db8::888')
    srv_msg.response_check_option_content('Response', '23', 'NOT ', 'addresses', '2001:db8::1')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:a::1')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.classification
@pytest.mark.sharedsubnets
def test_v6_client_classification_shared_subnet_options_override_global():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::10')
    srv_control.config_srv_opt('dns-servers', '2001:db8::1,2001:db8::2')

    srv_control.create_new_class('Client_Class_1')
    srv_control.add_test_to_class('1', 'test', 'substring(option[1].hex,8,2) == 0xf2f1')
    srv_control.add_option_to_defined_class('1', 'dns-servers', '2001:db8::888')
    srv_control.config_client_classification('0', 'Client_Class_1')

    srv_control.shared_subnet('0', '0')
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', '0')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f1')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_requests_option('23')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '23')
    srv_msg.response_check_option_content('Response', '23', None, 'addresses', '2001:db8::888')
    srv_msg.response_check_option_content('Response', '23', 'NOT ', 'addresses', '2001:db8::1')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:a::1')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.classification
@pytest.mark.sharedsubnets
def test_v6_client_classification_shared_subnet_options_override_subnet():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::10')
    srv_control.config_srv('dns-servers', '0', '2001:db8::1,2001:db8::2')

    srv_control.create_new_class('Client_Class_1')
    srv_control.add_test_to_class('1', 'test', 'substring(option[1].hex,8,2) == 0xf2f1')
    srv_control.add_option_to_defined_class('1', 'dns-servers', '2001:db8::888')
    srv_control.config_client_classification('0', 'Client_Class_1')

    srv_control.shared_subnet('0', '0')
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', '0')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f1')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_requests_option('23')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '23')
    srv_msg.response_check_option_content('Response', '23', None, 'addresses', '2001:db8::888')
    srv_msg.response_check_option_content('Response', '23', 'NOT ', 'addresses', '2001:db8::1')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:a::1')
