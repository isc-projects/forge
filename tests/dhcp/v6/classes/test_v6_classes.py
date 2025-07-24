# Copyright (C) 2022-2024 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""DHCPv6 Client Classification request process"""

# pylint: disable=line-too-long

import pytest

from src import misc
from src import srv_control
from src import srv_msg

from src.forge_cfg import world


@pytest.mark.v6
@pytest.mark.classification
def test_v6_classification_onesubnet_advertise_success():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.config_client_classification(0, 'VENDOR_CLASS_firstclass')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'vendor_class_data', 'firstclass')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::1')


@pytest.mark.v6
@pytest.mark.classification
@pytest.mark.default_classes
def test_v6_classification_onesubnet_advertise_fail():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.config_client_classification(0, 'VENDOR_CLASS_firstclass')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)


@pytest.mark.v6
@pytest.mark.classification
def test_v6_classification_onesubnet_request_success():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    # Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_firstclass.
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    # Client sets vendor_class_data value to firstclass.
    # Client does include vendor-class.
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'vendor_class_data', 'firstclass')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::1')


@pytest.mark.v6
@pytest.mark.classification
def test_v6_classification_twosubnets_request_success():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.config_client_classification(0, 'VENDOR_CLASS_firstclass')
    srv_control.config_srv_another_subnet_no_interface('3001::/64', '3001::100-3001::100')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'vendor_class_data', 'firstclass')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'vendor_class_data', 'firstclass')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::1')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3001::100')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3001::100')


@pytest.mark.v6
@pytest.mark.classification
def test_v6_classification_twosubnets_request_fail():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.config_client_classification(0, 'VENDOR_CLASS_firstclass')
    srv_control.config_srv_another_subnet_no_interface('3001::/64', '3001::100-3001::100')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '000300010a0027ffff02')
    srv_msg.client_sets_value('Client', 'vendor_class_data', 'firstclass')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '000300010a0027ffff02')
    srv_msg.client_sets_value('Client', 'vendor_class_data', 'firstclass')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '000300010a0027ffff02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3001::100')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '000300010a0027ffff02')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3001::100')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '000300010a0027ffff03')
    srv_msg.client_sets_value('Client', 'vendor_class_data', 'firstclass')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '000300010a0027ffff03')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)


@pytest.mark.v6
@pytest.mark.classification
def test_v6_classification_twoclasses_request_success():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.config_client_classification(0, 'VENDOR_CLASS_firstclass')
    srv_control.config_srv_another_subnet_no_interface('3001::/64', '3001::100-3001::100')
    srv_control.config_client_classification(1, 'VENDOR_CLASS_secondclass')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '000300010a0027ffff03')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'vendor_class_data', 'firstclass')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'vendor_class_data', 'firstclass')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'vendor_class_data', 'secondclass')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3001::100')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'vendor_class_data', 'secondclass')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3001::100')


@pytest.mark.v6
@pytest.mark.classification
def test_v6_classification_multiple_subnets():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')

    srv_control.create_new_class('Client_Class_1')
    srv_control.add_test_to_class(1, 'test', 'substring(option[1].hex,8,2) == 0xf2f1')
    # To class no 1 add option dns-servers with value 2001:db8::666.
    srv_control.config_client_classification(0, 'Client_Class_1')

    srv_control.create_new_class('Client_Class_2')
    srv_control.add_test_to_class(2, 'test', 'substring(option[1].hex,8,2) == 0xf2f2')
    srv_control.config_client_classification(1, 'Client_Class_2')

    srv_control.create_new_class('Client_Class_3')
    srv_control.add_test_to_class(3, 'test', 'substring(option[1].hex,8,2) == 0xf299')
    srv_control.config_client_classification(2, 'Client_Class_3')

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:11:11:11:11:11:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f1')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:a::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f2')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:b::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:99')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:c::1')


@pytest.mark.v6
@pytest.mark.classification
def test_v6_classification_multiple_subnets_2():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')

    srv_control.create_new_class('Client_Class_1')
    srv_control.add_test_to_class(1, 'test', 'substring(option[1].hex,8,2) == 0xf2f1')
    # To class no 1 add option dns-servers with value 2001:db8::666.
    srv_control.config_client_classification(0, 'Client_Class_1')

    srv_control.create_new_class('Client_Class_2')
    srv_control.add_test_to_class(2, 'test', 'substring(option[1].hex,8,2) == 0xf2f2')
    srv_control.config_client_classification(1, 'Client_Class_2')

    srv_control.create_new_class('Client_Class_3')
    srv_control.add_test_to_class(3, 'test', 'substring(option[1].hex,8,2) == 0xf299')
    srv_control.config_client_classification(2, 'Client_Class_3')

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:11:11:11:11:11:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:d::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f1')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:a::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f2')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:b::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:99')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:c::1')


@pytest.mark.v6
@pytest.mark.classification
def test_v6_classification_class_with_option():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')

    srv_control.create_new_class('Client_Class_1')
    srv_control.add_test_to_class(1, 'test', 'substring(option[1].hex,8,2) == 0xf2f1')
    srv_control.add_option_to_defined_class(1, 'dns-servers', '2001:db8::666')
    srv_control.config_client_classification(0, 'Client_Class_1')

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f1')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::666')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:a::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f1')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(23, expect_include=False)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:a::1')


@pytest.mark.v6
@pytest.mark.classification
def test_v6_classification_multiple_subnets_options():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')

    srv_control.create_new_class('Client_Class_1')
    srv_control.add_test_to_class(1, 'test', 'substring(option[1].hex,8,2) == 0xf2f1')
    srv_control.add_option_to_defined_class(1, 'dns-servers', '2001:db8::888')
    srv_control.config_client_classification(0, 'Client_Class_1')

    srv_control.create_new_class('Client_Class_2')
    srv_control.add_test_to_class(2, 'test', 'substring(option[1].hex,8,2) == 0xf2f2')
    srv_control.add_option_to_defined_class(2, 'dns-servers', '2001:db8::777')
    srv_control.config_client_classification(1, 'Client_Class_2')

    srv_control.create_new_class('Client_Class_3')
    srv_control.add_test_to_class(3, 'test', 'substring(option[1].hex,8,2) == 0xf299')
    srv_control.add_option_to_defined_class(3, 'dns-servers', '2001:db8::999')
    srv_control.config_client_classification(2, 'Client_Class_3')

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:11:11:11:11:11:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(23, expect_include=False)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:d::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f1')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::888')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:a::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f2')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::777')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:b::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:99')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::999')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:c::1')


@pytest.mark.v6
@pytest.mark.classification
def test_v6_classification_multiple_subnets_options_override_global():
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
    srv_control.add_test_to_class(1, 'test', 'substring(option[1].hex,8,2) == 0xf2f1')
    srv_control.add_option_to_defined_class(1, 'dns-servers', '2001:db8::888')
    srv_control.config_client_classification(0, 'Client_Class_1')

    srv_control.create_new_class('Client_Class_2')
    srv_control.add_test_to_class(2, 'test', 'substring(option[1].hex,8,2) == 0xf2f2')
    srv_control.add_option_to_defined_class(2, 'dns-servers', '2001:db8::777')
    srv_control.config_client_classification(1, 'Client_Class_2')

    srv_control.create_new_class('Client_Class_3')
    srv_control.add_test_to_class(3, 'test', 'substring(option[1].hex,8,2) == 0xf299')
    srv_control.add_option_to_defined_class(3, 'dns-servers', '2001:db8::999')
    srv_control.config_client_classification(2, 'Client_Class_3')

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:11:11:11:11:11:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::1,2001:db8::2')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:d::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f1')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::888')
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::2', expect_include=False)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::1', expect_include=False)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:a::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f2')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::777')
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::2', expect_include=False)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::1', expect_include=False)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:b::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:99')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::999')
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::2', expect_include=False)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::1', expect_include=False)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:c::1')


@pytest.mark.v6
@pytest.mark.classification
@pytest.mark.sharedsubnets
def test_v6_classification_shared_subnet_options_override():
    # we discussed classification on numerous occasions. This is actually working
    # as designed, I don't like this design, I still don't know why option defined
    # in shared-network should takes precedence before option defined in class and
    # it's only one level which does this (option in class takes precedence against
    # option defined globally, subnet and pool).

    # I gave up, I'm changing this test to reflect kea current operation.
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::10')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')

    srv_control.create_new_class('Client_Class_1')
    srv_control.add_test_to_class(1, 'test', 'substring(option[1].hex,8,2) == 0xf2f1')
    srv_control.add_option_to_defined_class(1, 'dns-servers', '2001:db8::888')
    srv_control.config_client_classification(0, 'Client_Class_1')

    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.shared_subnet('2001:db8:b::/64', 0)

    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)
    srv_control.set_conf_parameter_shared_subnet('option-data',
                                                 '{"csv-format":true,"code":23,"data":"2001:db8::1","name":"dns-servers","space":"dhcp6"}',
                                                 0)

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f2')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::888', expect_include=False)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::1')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:b::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f1')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(23)
    # the way this test worked previously
    # srv_msg.response_check_option_content(23, 'addresses', '2001:db8::888')
    # srv_msg.response_check_option_content(23, 'addresses', '2001:db8::1', expect_include=False)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::888', expect_include=False)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::1')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:a::1')


@pytest.mark.v6
@pytest.mark.classification
@pytest.mark.sharedsubnets
def test_v6_classification_shared_subnet_options_override_global():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::10')
    srv_control.config_srv_opt('dns-servers', '2001:db8::1,2001:db8::2')
    srv_control.create_new_class('Client_Class_1')
    srv_control.add_test_to_class(1, 'test', 'substring(option[1].hex,8,2) == 0xf2f1')
    srv_control.add_option_to_defined_class(1, 'dns-servers', '2001:db8::888')
    srv_control.config_client_classification(0, 'Client_Class_1')

    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f1')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:a::1')
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::888')
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::1', expect_include=False)


@pytest.mark.v6
@pytest.mark.classification
@pytest.mark.sharedsubnets
def test_v6_classification_shared_subnet_options_subnet():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::10')
    srv_control.create_new_class('Client_Class_1')
    srv_control.add_test_to_class(1, 'test', 'option[1].hex == 0x0003000166554433f2f1')
    srv_control.add_option_to_defined_class(1, 'dns-servers', '2001:db8::888')
    srv_control.config_client_classification(0, 'Client_Class_1')

    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:f2:f1')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:a::1')
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::888')


def _get_address(duid, address, class_id=None):
    misc.test_procedure()
    srv_msg.client_sets_value("Client", "DUID", duid)
    srv_msg.client_does_include("Client", "client-id")
    srv_msg.client_does_include("Client", "IA-NA")
    srv_msg.client_sets_value("Client", "vendor_class_data", class_id)
    srv_msg.client_does_include("Client", "vendor-class")
    srv_msg.client_send_msg("SOLICIT")

    misc.pass_criteria()
    srv_msg.send_wait_for_message("MUST", "ADVERTISE")
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, "sub-option", 5)
    srv_msg.response_check_suboption_content(5, 3, "addr", address)

    misc.test_procedure()
    srv_msg.client_sets_value("Client", "vendor_class_data", class_id)
    srv_msg.client_does_include("Client", "vendor-class")
    srv_msg.client_sets_value("Client", "DUID", duid)
    srv_msg.client_copy_option("IA_NA")
    srv_msg.client_copy_option("server-id")
    srv_msg.client_does_include("Client", "client-id")
    srv_msg.client_send_msg("REQUEST")

    misc.pass_criteria()
    srv_msg.send_wait_for_message("MUST", "REPLY")
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, "sub-option", 5)
    srv_msg.response_check_suboption_content(5, 3, "addr", address)


@pytest.mark.v6
@pytest.mark.classification
@pytest.mark.parametrize("level", ['global', 'shared-networks'])
def test_v6_classification_vendor_different_levels(level):
    """test_v6_classification_vendor_different_levels Check vendor classes when shared networks are used and when those are not used.

    :param level: subnets configured in shared-networks or global
    :type level: string
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::10', id=1)
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64', '2001:db8:b::1-2001:db8:b::10', id=2)
    srv_control.config_srv_another_subnet_no_interface('2001:db8:c::/64', '2001:db8:c::1-2001:db8:c::10', id=3)

    for i, j in zip(["a", "b", "c"], range(3)):
        srv_control.config_client_classification(j, f'VENDOR_CLASS_subnet-{i}')

    if level == 'shared-networks':
        srv_control.shared_subnet('2001:db8:a::/64', 0)
        srv_control.shared_subnet('2001:db8:b::/64', 0)
        srv_control.shared_subnet('2001:db8:c::/64', 0)
        srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
        srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    srv_control.build_and_send_config_files()
    srv_control.start_srv("DHCP", "started")

    for i in ["a", "b", "c"]:
        _get_address(duid=f"00:03:00:01:00:00:00:00:11:0{i.upper()}", address=f"2001:db8:{i}::1", class_id=f'subnet-{i}')


@pytest.mark.v6
@pytest.mark.classification
@pytest.mark.parametrize('backend', ['configfile', 'MySQL', 'PostgreSQL'])
@pytest.mark.parametrize('level', ['subnet', 'pool'])
def test_v6_network_selection_with_class_reservations(backend, level):
    """Check if client class in global reservation is working correctly after subnet/pool selection.
    :param backend: backend to use
    :type backend: string
    :param level: subnet or pool
    :type level: string
    """
    misc.test_setup()
    # configure subnet(s) and pool(s)
    if level == 'subnet':
        srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::10', id=1)
        srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64', '2001:db8:b::1-2001:db8:b::10', id=2)
    else:  # level == 'pool
        srv_control.config_srv_subnet('2001:db8::/32', '2001:db8:a::1-2001:db8:a::10', id=1)
        srv_control.new_pool('2001:db8:b::1-2001:db8:b::10', 0)

    # Define "reserved" and "normal" class
    srv_control.create_new_class('reserved_class')
    srv_control.add_option_to_defined_class(1, 'dns-servers', '2001:db8::888')

    srv_control.create_new_class('normal_clients')
    srv_control.add_option_to_defined_class(2, 'dns-servers', '2001:db4::444')
    srv_control.add_test_to_class(2, 'test', 'not member(\'reserved_class\')')

    # Add class to subnet or pool
    if level == 'subnet':
        srv_control.config_client_classification(0, 'reserved_class')
        srv_control.config_client_classification(1, 'normal_clients')
    else:  # level == 'pool'
        srv_control.config_pool_client_classification(0, 0, 'reserved_class')
        srv_control.config_pool_client_classification(0, 1, 'normal_clients')

    # Enable global reservations
    world.dhcp_cfg.update({
        "reservations-global": True,
        "reservations-in-subnet": False
    })

    # Define reservation for "reserved" class in configfile or database
    if backend == 'configfile':
        world.dhcp_cfg.update({
            "reservations": [
                {
                    "client-classes": [
                        "reserved_class"
                    ],
                    "duid": "00:03:00:01:66:55:44:33:f2:f1"
                }
            ]
        })
    else:  # backend == 'MySQL' or backend == 'PostgreSQL'
        srv_control.enable_db_backend_reservation(backend)
        srv_control.new_db_backend_reservation(backend, 'duid', '00:03:00:01:66:55:44:33:f2:f1')
        srv_control.update_db_backend_reservation('dhcp6_subnet_id', 0, backend, 1)
        srv_control.update_db_backend_reservation('dhcp6_client_classes', 'reserved_class', backend, 1)
        srv_control.upload_db_reservation(backend)

    # Configure shared network
    if level == 'subnet':
        srv_control.shared_subnet('2001:db8:a::/64', 0)
        srv_control.shared_subnet('2001:db8:b::/64', 0)
    else:  # level == 'pool'
        srv_control.shared_subnet('2001:db8::/32', 0)

    srv_control.set_conf_parameter_shared_subnet('name', 'name-abc', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '$(SERVER_IFACE)', 0)

    # Start Kea
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Send SARR for client without reservation.
    misc.test_procedure()
    srv_msg.client_sets_value("Client", "DUID", "00:03:00:01:66:55:44:33:f2:f5")
    srv_msg.client_does_include("Client", "client-id")
    srv_msg.client_does_include("Client", "IA-NA")
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg("SOLICIT")

    misc.pass_criteria()
    srv_msg.send_wait_for_message("MUST", "ADVERTISE")
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, "sub-option", 5)
    srv_msg.response_check_suboption_content(5, 3, "addr", "2001:db8:b::1")
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db4::444')

    misc.test_procedure()
    srv_msg.client_sets_value("Client", "DUID", "00:03:00:01:66:55:44:33:f2:f5")
    srv_msg.client_copy_option("IA_NA")
    srv_msg.client_copy_option("server-id")
    srv_msg.client_does_include("Client", "client-id")
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg("REQUEST")

    misc.pass_criteria()
    srv_msg.send_wait_for_message("MUST", "REPLY")
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, "sub-option", 5)
    srv_msg.response_check_suboption_content(5, 3, "addr", "2001:db8:b::1")
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db4::444')

    # Send SARR for client with reservation.
    misc.test_procedure()
    srv_msg.client_sets_value("Client", "DUID", "00:03:00:01:66:55:44:33:f2:f1")
    srv_msg.client_does_include("Client", "client-id")
    srv_msg.client_does_include("Client", "IA-NA")
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg("SOLICIT")

    misc.pass_criteria()
    srv_msg.send_wait_for_message("MUST", "ADVERTISE")
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, "sub-option", 5)
    srv_msg.response_check_suboption_content(5, 3, "addr", "2001:db8:a::1")
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::888')

    misc.test_procedure()
    srv_msg.client_sets_value("Client", "DUID", "00:03:00:01:66:55:44:33:f2:f1")
    srv_msg.client_copy_option("IA_NA")
    srv_msg.client_copy_option("server-id")
    srv_msg.client_does_include("Client", "client-id")
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg("REQUEST")

    misc.pass_criteria()
    srv_msg.send_wait_for_message("MUST", "REPLY")
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, "sub-option", 5)
    srv_msg.response_check_suboption_content(5, 3, "addr", "2001:db8:a::1")
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::888')


@pytest.mark.v6
@pytest.mark.classification
def test_v6_classification_tagging_gating():
    """ Verifies that (non-vendor) requested options can be gated by option class tagging.
    Duplicate of Unittest.
    """

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::10', id=1)

    # Define "right" class
    srv_control.create_new_class('right')
    srv_control.add_test_to_class(1, "test", "substring(option[1].hex,7,3) == '111'")

    # Add options for different classes
    srv_control.config_srv_custom_opt('no_classes', '1249', 'string', 'oompa')
    srv_control.config_srv_custom_opt('wrong_class', '1250', 'string', 'loompa', client_classes=["wrong"])
    srv_control.config_srv_custom_opt('right_class', '1251', 'string', 'doompadee', client_classes=["right"])

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Send discover message with options for different classes
    # Client should receive option for no-class
    misc.test_procedure()
    srv_msg.client_sets_value("Client", "DUID", "00:03:00:01:66:55:44:11:11:11")
    srv_msg.client_does_include("Client", "client-id")
    srv_msg.client_does_include("Client", "IA-NA")
    srv_msg.client_requests_option(1249)
    srv_msg.client_requests_option(1250)
    srv_msg.client_requests_option(1251)
    srv_msg.client_send_msg("SOLICIT")

    misc.pass_criteria()
    srv_msg.send_wait_for_message("MUST", "ADVERTISE")
    srv_msg.response_check_include_option(1249)
    srv_msg.response_check_include_option(1250, expect_include=False)
    srv_msg.response_check_include_option(1251, expect_include=False)
    srv_msg.response_check_option_content(1249, 'value', 'oompa'.encode().hex())

    misc.test_procedure()
    srv_msg.client_sets_value("Client", "DUID", "00:03:00:01:66:55:44:11:11:11")
    srv_msg.client_copy_option("IA_NA")
    srv_msg.client_copy_option("server-id")
    srv_msg.client_does_include("Client", "client-id")
    srv_msg.client_requests_option(1249)
    srv_msg.client_requests_option(1250)
    srv_msg.client_requests_option(1251)
    srv_msg.client_send_msg("REQUEST")

    misc.pass_criteria()
    srv_msg.send_wait_for_message("MUST", "REPLY")
    srv_msg.response_check_include_option(1249)
    srv_msg.response_check_include_option(1250, expect_include=False)
    srv_msg.response_check_include_option(1251, expect_include=False)
    srv_msg.response_check_option_content(1249, 'value', 'oompa'.encode().hex())

    # Client should receive option for "right" class
    misc.test_procedure()
    srv_msg.client_sets_value("Client", "DUID", "00:03:00:01:66:55:44:31:31:31")
    srv_msg.client_does_include("Client", "client-id")
    srv_msg.client_does_include("Client", "IA-NA")
    srv_msg.client_requests_option(1249)
    srv_msg.client_requests_option(1250)
    srv_msg.client_requests_option(1251)
    srv_msg.client_send_msg("SOLICIT")

    misc.pass_criteria()
    srv_msg.send_wait_for_message("MUST", "ADVERTISE")
    srv_msg.response_check_include_option(1249)
    srv_msg.response_check_include_option(1250, expect_include=False)
    srv_msg.response_check_include_option(1251)
    srv_msg.response_check_option_content(1249, 'value', 'oompa'.encode().hex())
    srv_msg.response_check_option_content(1251, 'value', 'doompadee'.encode().hex())

    misc.test_procedure()
    srv_msg.client_sets_value("Client", "DUID", "00:03:00:01:66:55:44:31:31:31")
    srv_msg.client_copy_option("IA_NA")
    srv_msg.client_copy_option("server-id")
    srv_msg.client_does_include("Client", "client-id")
    srv_msg.client_requests_option(1249)
    srv_msg.client_requests_option(1250)
    srv_msg.client_requests_option(1251)
    srv_msg.client_send_msg("REQUEST")

    misc.pass_criteria()
    srv_msg.send_wait_for_message("MUST", "REPLY")
    srv_msg.response_check_include_option(1249)
    srv_msg.response_check_include_option(1250, expect_include=False)
    srv_msg.response_check_include_option(1251)
    srv_msg.response_check_option_content(1249, 'value', 'oompa'.encode().hex())
    srv_msg.response_check_option_content(1251, 'value', 'doompadee'.encode().hex())
