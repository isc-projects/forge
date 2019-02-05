"""Client Classification DHCPv6"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_control
from features import srv_msg
from features import misc


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.classification
def test_v6_client_classification_multiple_subnets(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'substring(option[1].hex,8,2) == 0xf2f1')
    # To class no 1 add option dns-servers with value 2001:db8::666.
    srv_control.config_client_classification(step, '0', 'Client_Class_1')

    srv_control.create_new_class(step, 'Client_Class_2')
    srv_control.add_test_to_class(step, '2', 'test', 'substring(option[1].hex,8,2) == 0xf2f2')
    srv_control.config_client_classification(step, '1', 'Client_Class_2')

    srv_control.create_new_class(step, 'Client_Class_3')
    srv_control.add_test_to_class(step, '3', 'test', 'substring(option[1].hex,8,2) == 0xf299')
    srv_control.config_client_classification(step, '2', 'Client_Class_3')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:11:11:11:11:11:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content(step, 'Response', '13', '3', None, 'statuscode', '2')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f1')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:a::1')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f2')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:b::1')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:f2:99')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:c::1')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.classification
def test_v6_client_classification_multiple_subnets_2(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'substring(option[1].hex,8,2) == 0xf2f1')
    # To class no 1 add option dns-servers with value 2001:db8::666.
    srv_control.config_client_classification(step, '0', 'Client_Class_1')

    srv_control.create_new_class(step, 'Client_Class_2')
    srv_control.add_test_to_class(step, '2', 'test', 'substring(option[1].hex,8,2) == 0xf2f2')
    srv_control.config_client_classification(step, '1', 'Client_Class_2')

    srv_control.create_new_class(step, 'Client_Class_3')
    srv_control.add_test_to_class(step, '3', 'test', 'substring(option[1].hex,8,2) == 0xf299')
    srv_control.config_client_classification(step, '2', 'Client_Class_3')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:11:11:11:11:11:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:d::1')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f1')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:a::1')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f2')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:b::1')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:f2:99')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:c::1')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.classification
def test_v6_client_classification_class_with_option(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'substring(option[1].hex,8,2) == 0xf2f1')
    srv_control.add_option_to_defined_class(step, '1', 'dns-servers', '2001:db8::666')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f1')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '23')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '23')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::666')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:a::1')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f1')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '23')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:a::1')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.classification
def test_v6_client_classification_multiple_subnets_options(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'substring(option[1].hex,8,2) == 0xf2f1')
    srv_control.add_option_to_defined_class(step, '1', 'dns-servers', '2001:db8::888')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')

    srv_control.create_new_class(step, 'Client_Class_2')
    srv_control.add_test_to_class(step, '2', 'test', 'substring(option[1].hex,8,2) == 0xf2f2')
    srv_control.add_option_to_defined_class(step, '2', 'dns-servers', '2001:db8::777')
    srv_control.config_client_classification(step, '1', 'Client_Class_2')

    srv_control.create_new_class(step, 'Client_Class_3')
    srv_control.add_test_to_class(step, '3', 'test', 'substring(option[1].hex,8,2) == 0xf299')
    srv_control.add_option_to_defined_class(step, '3', 'dns-servers', '2001:db8::999')
    srv_control.config_client_classification(step, '2', 'Client_Class_3')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:11:11:11:11:11:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '23')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '23')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:d::1')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f1')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '23')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '23')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::888')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:a::1')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f2')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '23')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '23')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::777')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:b::1')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:f2:99')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '23')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '23')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::999')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:c::1')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.classification
def test_v6_client_classification_multiple_subnets_options_override_global(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')

    srv_control.config_srv_opt(step, 'dns-servers', '2001:db8::1,2001:db8::2')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'substring(option[1].hex,8,2) == 0xf2f1')
    srv_control.add_option_to_defined_class(step, '1', 'dns-servers', '2001:db8::888')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')

    srv_control.create_new_class(step, 'Client_Class_2')
    srv_control.add_test_to_class(step, '2', 'test', 'substring(option[1].hex,8,2) == 0xf2f2')
    srv_control.add_option_to_defined_class(step, '2', 'dns-servers', '2001:db8::777')
    srv_control.config_client_classification(step, '1', 'Client_Class_2')

    srv_control.create_new_class(step, 'Client_Class_3')
    srv_control.add_test_to_class(step, '3', 'test', 'substring(option[1].hex,8,2) == 0xf299')
    srv_control.add_option_to_defined_class(step, '3', 'dns-servers', '2001:db8::999')
    srv_control.config_client_classification(step, '2', 'Client_Class_3')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:11:11:11:11:11:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '23')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '23')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::1,2001:db8::2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:d::1')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f1')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '23')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '23')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::888')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          'NOT ',
                                          'addresses',
                                          '2001:db8::2')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          'NOT ',
                                          'addresses',
                                          '2001:db8::1')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:a::1')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f2')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '23')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '23')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::777')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          'NOT ',
                                          'addresses',
                                          '2001:db8::2')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          'NOT ',
                                          'addresses',
                                          '2001:db8::1')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:b::1')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:f2:99')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '23')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '23')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::999')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          'NOT ',
                                          'addresses',
                                          '2001:db8::2')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          'NOT ',
                                          'addresses',
                                          '2001:db8::1')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:c::1')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.classification
@pytest.mark.sharedsubnets
def test_v6_client_classification_shared_subnet_options_override(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::10')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'substring(option[1].hex,8,2) == 0xf2f1')
    srv_control.add_option_to_defined_class(step, '1', 'dns-servers', '2001:db8::888')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')

    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')

    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '0')
    srv_control.set_conf_parameter_shared_subnet(step,
                                                 'option-data',
                                                 '[{"csv-format":true,"code":23,"data":"2001:db8::1","name":"dns-servers","space":"dhcp6"}]',
                                                 '0')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f2')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '23')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '23')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          'NOT ',
                                          'addresses',
                                          '2001:db8::888')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::1')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:b::1')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f1')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '23')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '23')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::888')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          'NOT ',
                                          'addresses',
                                          '2001:db8::1')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:a::1')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.classification
@pytest.mark.sharedsubnets
def test_v6_client_classification_shared_subnet_options_override_francis(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::10')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'substring(option[1].hex,8,2) == 0xf2f1')
    srv_control.add_test_to_class(step, '1', 'only-if-required', 'true')
    srv_control.add_option_to_defined_class(step, '1', 'dns-servers', '2001:db8::888')
    # Server is configured with client-classification option in subnet 0 with name Client_Class_1.
    srv_control.config_require_client_classification(step, '0', 'Client_Class_1')

    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')

    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '0')
    srv_control.set_conf_parameter_shared_subnet(step,
                                                 'option-data',
                                                 '[{"csv-format":true,"code":23,"data":"2001:db8::1","name":"dns-servers","space":"dhcp6"}]',
                                                 '0')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f2')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '23')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '23')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          'NOT ',
                                          'addresses',
                                          '2001:db8::888')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::1')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:b::1')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f1')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '23')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '23')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::888')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          'NOT ',
                                          'addresses',
                                          '2001:db8::1')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:a::1')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.classification
@pytest.mark.sharedsubnets
def test_v6_client_classification_shared_subnet_options_override_global(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::10')
    srv_control.config_srv_opt(step, 'dns-servers', '2001:db8::1,2001:db8::2')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'substring(option[1].hex,8,2) == 0xf2f1')
    srv_control.add_option_to_defined_class(step, '1', 'dns-servers', '2001:db8::888')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')

    srv_control.shared_subnet(step, '0', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '0')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f1')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '23')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '23')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::888')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          'NOT ',
                                          'addresses',
                                          '2001:db8::1')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:a::1')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.classification
@pytest.mark.sharedsubnets
def test_v6_client_classification_shared_subnet_options_override_subnet(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::10')
    srv_control.config_srv(step, 'dns-servers', '0', '2001:db8::1,2001:db8::2')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'substring(option[1].hex,8,2) == 0xf2f1')
    srv_control.add_option_to_defined_class(step, '1', 'dns-servers', '2001:db8::888')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')

    srv_control.shared_subnet(step, '0', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '0')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f1')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '23')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '23')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::888')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          'NOT ',
                                          'addresses',
                                          '2001:db8::1')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:a::1')
