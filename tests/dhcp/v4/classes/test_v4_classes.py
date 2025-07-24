# Copyright (C) 2022-2024 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""DHCPv4 Client Classification release process"""

import pytest

from src import srv_msg
from src import misc
from src import srv_control

from src.forge_cfg import world


@pytest.mark.v4
@pytest.mark.classification
def test_v4_classification_one_class_one_subnet():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_client_classification(0, 'VENDOR_CLASS_my-own-class')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')


@pytest.mark.v4
@pytest.mark.classification
def test_v4_classification_one_class_two_subnets_same_values():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_client_classification(0, 'VENDOR_CLASS_my-own-class')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.100-192.168.51.100')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.51.100')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.51.100')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.51.100')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')


@pytest.mark.v4
@pytest.mark.classification
def test_v4_classification_one_class_two_subnets_different_class_id_included():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_client_classification(0, 'VENDOR_CLASS_my-own-class')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.100-192.168.51.100')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-other-class')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.51.100')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')


@pytest.mark.v4
@pytest.mark.classification
def test_v4_classification_one_class_two_subnets_different_chaddr():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_client_classification(0, 'VENDOR_CLASS_my-own-class')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.100-192.168.51.100')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1f:05:05:05:05')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1f:05:05:05:05')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1f:06:06:06:06')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.51.100')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1f:06:06:06:06')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.51.100')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.51.100')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')


@pytest.mark.v4
@pytest.mark.classification
def test_v4_classification_one_class_empty_pool_with_classification():

    # test if server is assigning addresses from pool without classification after
    # all addresses form pool with classification has been assigned
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_client_classification(0, 'VENDOR_CLASS_my-own-class')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.100-192.168.51.100')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:11:11:11:11')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()


@pytest.mark.v4
@pytest.mark.classification
def test_v4_classification_one_class_empty_pool_without_classification():

    # test if server is assigning addresses from pool with classification after
    # all addresses form pool without classification has been assigned
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_client_classification(0, 'VENDOR_CLASS_my-own-class')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.100-192.168.51.100')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.51.100')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.51.100')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.51.100')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:11:11:11:11')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()


@pytest.mark.v4
@pytest.mark.classification
def test_v4_classification_multiple_classes_two_subnets_different_chaddr():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_client_classification(0, 'VENDOR_CLASS_my-own-class')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.100-192.168.51.100')
    srv_control.config_client_classification(1, 'VENDOR_CLASS_my-other-class')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1f:05:05:05:05')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1f:05:05:05:05')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1f:06:06:06:06')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-other-class')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.51.100')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1f:06:06:06:06')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.51.100')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-other-class')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.51.100')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')


@pytest.mark.v4
@pytest.mark.classification
def test_v4_classification_multiple_classes_three_subnets_different_chaddr():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_client_classification(0, 'VENDOR_CLASS_my-own-class')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.100-192.168.51.100')
    srv_control.config_client_classification(1, 'VENDOR_CLASS_my-other-class')
    srv_control.config_srv_another_subnet_no_interface('192.168.52.0/24',
                                                       '192.168.52.150-192.168.52.150')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1f:05:05:05:05')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1f:05:05:05:05')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1f:06:06:06:06')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-other-class')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.51.100')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1f:06:06:06:06')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.51.100')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-other-class')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.51.100')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')


@pytest.mark.v4
@pytest.mark.classification
def test_v4_classification_multiple_classes_three_subnets_different_values():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_client_classification(0, 'VENDOR_CLASS_my-own-class')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.100-192.168.51.100')
    srv_control.config_client_classification(1, 'VENDOR_CLASS_my-other-class')
    srv_control.config_srv_another_subnet_no_interface('192.168.52.0/24',
                                                       '192.168.52.150-192.168.52.150')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1f:05:05:05:05')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1f:05:05:05:05')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '00030405060708')
    srv_msg.client_sets_value('Client', 'chaddr', '00:1f:06:06:06:06')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-other-class')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.51.100')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00030405060708')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '00030405060708')
    srv_msg.client_sets_value('Client', 'chaddr', '00:1f:06:06:06:06')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.51.100')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-other-class')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_content('yiaddr', '192.168.51.100')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1f:11:22:33:44')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.52.150')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1f:11:22:33:44')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.52.150')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.52.150')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')


@pytest.mark.v4
@pytest.mark.classification
@pytest.mark.release
def test_v4_classification_release_same_chaddr_client_id():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_client_classification(0, 'VENDOR_CLASS_my-own-class')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:11:22:33')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')


@pytest.mark.v4
@pytest.mark.classification
@pytest.mark.release
def test_v4_classification_release_different_chaddr_client_id():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_client_classification(0, 'VENDOR_CLASS_my-own-class')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:11:22:33')
    srv_msg.client_does_include_with_value('client_id', '00010203123456')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:11:22:33')
    # Client adds to the message client_id with value 00010203040506.
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()
    # we should check logs here..


def _get_address(mac, address, class_id=None):
    misc.test_procedure()
    srv_msg.client_sets_value("Client", "chaddr", mac)
    srv_msg.client_does_include_with_value('vendor_class_id', class_id)
    srv_msg.client_send_msg("DISCOVER")

    misc.pass_criteria()
    srv_msg.send_wait_for_message("MUST", "OFFER")
    srv_msg.response_check_content("yiaddr", address)

    misc.test_procedure()
    srv_msg.client_sets_value("Client", "chaddr", mac)
    srv_msg.client_copy_option("server_id")
    srv_msg.client_does_include_with_value('vendor_class_id', class_id)
    srv_msg.client_does_include_with_value("requested_addr", address)
    srv_msg.client_send_msg("REQUEST")

    misc.pass_criteria()
    srv_msg.send_wait_for_message("MUST", "ACK")
    srv_msg.response_check_content("yiaddr", address)


@pytest.mark.v4
@pytest.mark.classification
@pytest.mark.parametrize("level", ['global', 'shared-networks'])
def test_v4_classification_vendor_different_levels(level):
    """test_v4_classification_vendor_different_levels Check vendor classes
    when shared networks are used and when those are not used.

    :param level: subnets configured in shared-networks or global
    :type level: string
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.15', id=1)
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24', '192.168.51.10-192.168.51.15', id=2)
    srv_control.config_srv_another_subnet_no_interface('192.168.52.0/24', '192.168.52.10-192.168.52.15', id=3)

    for i in range(3):
        srv_control.config_client_classification(i, f'VENDOR_CLASS_subnet-{i}')

    if level == 'shared-networks':
        srv_control.shared_subnet('192.168.50.0/24', 0)
        srv_control.shared_subnet('192.168.51.0/24', 0)
        srv_control.shared_subnet('192.168.52.0/24', 0)
        srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
        srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    srv_control.build_and_send_config_files()
    srv_control.start_srv("DHCP", "started")

    for i in range(3):
        _get_address(mac=f"00:00:00:00:00:0{i}", address=f"192.168.5{i}.10", class_id=f'subnet-{i}')


@pytest.mark.v4
@pytest.mark.classification
@pytest.mark.parametrize('backend', ['configfile', 'MySQL', 'PostgreSQL'])
@pytest.mark.parametrize('level', ['subnet', 'pool'])
def test_v4_network_selection_with_class_reservations(backend, level):
    """Check if client class in global reservation is working correctly after subnet/pool selection.

    :param backend: configfile, MySQL or PostgreSQL
    :type backend: string
    :param level: subnet or pool
    :type level: string
    """
    misc.test_setup()
    # configure subnet(s) and pool(s)
    if level == 'subnet':
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10', id=1)
        srv_control.config_srv_another_subnet_no_interface('192.168.60.0/24', '192.168.60.1-192.168.60.10', id=2)
    else:  # level == 'pool
        srv_control.config_srv_subnet('192.168.0.0/16', '192.168.50.1-192.168.50.10', id=1)
        srv_control.new_pool('192.168.60.1-192.168.60.10', 0)

    # Define "reserved" and "normal" class
    srv_control.create_new_class('reserved_class')
    srv_control.add_test_to_class(1, 'server-hostname', 'Johny5')

    srv_control.create_new_class('normal_clients')
    srv_control.add_test_to_class(2, 'server-hostname', 'hal9000')
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
                    "hw-address": "ff:01:02:03:ff:04"
                }
            ]
        })
    else:  # backend == 'MySQL' or backend == 'PostgreSQL'
        srv_control.enable_db_backend_reservation(backend)
        srv_control.new_db_backend_reservation(backend, 'hw-address', 'ff:01:02:03:ff:04')
        srv_control.update_db_backend_reservation('dhcp4_subnet_id', 0, backend, 1)
        srv_control.update_db_backend_reservation('dhcp4_client_classes', 'reserved_class', backend, 1)
        srv_control.upload_db_reservation(backend)

    # Configure shared network
    if level == 'subnet':
        srv_control.shared_subnet('192.168.50.0/24', 0)
        srv_control.shared_subnet('192.168.60.0/24', 0)
    else:  # level == 'pool'
        srv_control.shared_subnet('192.168.0.0/16', 0)

    srv_control.set_conf_parameter_shared_subnet('name', 'name-abc', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '$(SERVER_IFACE)', 0)

    # Start Kea
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Send DORA for client without reservation.
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:05')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.60.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_content('sname', 'hal9000')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:05')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.60.1')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.60.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_content('sname', 'hal9000')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')

    # Send DORA for client with reservation.
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('client_id', '00030405060708')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_content('sname', 'Johny5')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00030405060708')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('client_id', '00030405060708')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_content('sname', 'Johny5')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00030405060708')


@pytest.mark.v4
@pytest.mark.classification
def test_v4_classification_tagging_gating():
    """ Verifies that (non-vendor) requested options can be gated by option class tagging.
    Duplicate of Unittest.
    """

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.100', id=1)

    # Define "right" class
    srv_control.create_new_class('right')
    srv_control.add_test_to_class(1, "test", "substring(option[61].hex,0,3) == '111'")

    # Add options for different classes
    srv_control.config_srv_custom_opt('no_classes', '249', 'string', 'oompa')
    srv_control.config_srv_custom_opt('wrong_class', '250', 'string', 'loompa', client_classes=["wrong"])
    srv_control.config_srv_custom_opt('right_class', '251', 'string', 'doompadee', client_classes=["right"])

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Send discover message with options for different classes
    # Client should receive option for no-class
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_requests_option(249)
    srv_msg.client_requests_option(250)
    srv_msg.client_requests_option(251)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(249)
    srv_msg.response_check_include_option(250, expect_include=False)
    srv_msg.response_check_include_option(251, expect_include=False)
    srv_msg.response_check_option_content(249, 'value', 'oompa')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')

    # Client should receive option for "right" class
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:22')
    srv_msg.client_does_include_with_value('client_id', '313131')
    srv_msg.client_requests_option(249)
    srv_msg.client_requests_option(250)
    srv_msg.client_requests_option(251)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.2')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(249)
    srv_msg.response_check_include_option(250, expect_include=False)
    srv_msg.response_check_include_option(251)
    srv_msg.response_check_option_content(249, 'value', 'oompa')
    srv_msg.response_check_option_content(251, 'value', 'doompadee')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '313131')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:22')
    srv_msg.client_does_include_with_value('client_id', '313131')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.2')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.2')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '313131')


@pytest.mark.v4
@pytest.mark.classification
def test_v4_classification_tagging_gating_vivso():
    """ Verifies that VIVSO suboption can be gated by option class tagging.
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.100', id=1)

    # Define class data
    srv_control.create_new_class('melon')
    srv_control.add_test_to_class(1, "test", "substring(option[61].hex,0,3) == '111'")

    # Add options for different classes
    srv_control.config_srv_opt('vivso-suboptions', "1234", client_classes=["melon"])

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Client should receive option vendor
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_does_include_with_value('client_id', '313131')
    srv_msg.client_requests_option('vivso-suboptions')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.client_does_include_with_value('vendor_specific_information', '1234')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_does_include_with_value('client_id', '313131')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option('vivso-suboptions')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '313131')
    srv_msg.client_does_include_with_value('vendor_specific_information', '1234')

    # Client should not recive option.
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:22')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_requests_option('vivso-suboptions')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.2')
    srv_msg.response_check_include_option(43, expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:22')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.2')
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option('vivso-suboptions')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.2')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')
    srv_msg.response_check_include_option(43, expect_include=False)


@pytest.mark.v4
@pytest.mark.classification
def test_v4_classification_tagging_gating_standart():
    """ Verifies that standart suboption can be gated by option class tagging.
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.100', id=1)

    # Define "right" class
    srv_control.create_new_class('melon')
    srv_control.add_test_to_class(1, "test", "substring(option[61].hex,0,3) == '111'")

    # Add options for different classes
    srv_control.config_srv_opt("routers", "192.0.2.1", client_classes=["melon"])
    srv_control.config_srv_opt("domain-name", "example.com", client_classes=["melon"])
    srv_control.config_srv_opt("domain-name-servers", "192.0.2.3", client_classes=["melon"])
    srv_control.config_srv_opt("dhcp-server-identifier", "192.0.2.0", client_classes=["melon"])

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Client should receive option for no-class
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_does_include_with_value('client_id', '313131')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'value', '192.0.2.1')
    srv_msg.response_check_include_option(15)
    srv_msg.response_check_option_content(15, 'value', 'example.com')
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, 'value', '192.0.2.3')
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_option_content(54, 'value', '192.0.2.0')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_does_include_with_value('client_id', '313131')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option('vivso-suboptions')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(61, 'value', '313131')
    srv_msg.response_check_option_content(54, 'value', '192.0.2.0')

    # Client should receive option for "right" class
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:22')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.2')
    srv_msg.response_check_include_option(3, expect_include=False)
    srv_msg.response_check_include_option(15, expect_include=False)
    srv_msg.response_check_include_option(6, expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:22')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.2')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.2')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')
    srv_msg.response_check_include_option(3, expect_include=False)
    srv_msg.response_check_include_option(15, expect_include=False)
    srv_msg.response_check_include_option(6, expect_include=False)
