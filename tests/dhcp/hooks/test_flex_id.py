# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea Hook flex-id testing"""

import pytest

from src import misc
from src import srv_msg
from src import srv_control
from src.forge_cfg import world
from src.protosupport.multi_protocol_functions import lease_file_contains, lease_file_doesnt_contain
from src.protosupport.multi_protocol_functions import wait_for_message_in_log


@pytest.mark.disabled
@pytest.mark.v4
@pytest.mark.flexid
def test_v4_flexid_libreload():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           0,
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '192.168.50.10')
    srv_control.add_line({"host-reservation-identifiers": ["flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1, 'identifier-expression', 'option[60].hex')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "libreload","arguments": {}}')
    # if reload works - classification should work without changes

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')


@pytest.mark.v4
@pytest.mark.flexid
def test_v4_flexid_reconfigure():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           0,
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '192.168.50.10')
    srv_control.add_line({"host-reservation-identifiers": ["flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1, 'identifier-expression', 'option[60].hex')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           0,
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '192.168.50.10')
    srv_control.add_line({"host-reservation-identifiers": ["flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1, 'identifier-expression', 'option[60].hex')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'reconfigured')
    wait_for_message_in_log('DHCP4_DYNAMIC_RECONFIGURATION', 1)
    wait_for_message_in_log('DHCP4_CONFIG_COMPLETE', 2)

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')


@pytest.mark.v4
@pytest.mark.flexid
def test_v4_flexid_inside_pool():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           0,
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '192.168.50.10')
    srv_control.add_line({"host-reservation-identifiers": ["flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1, 'identifier-expression', 'option[60].hex')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')

    misc.test_procedure()
    # Client adds to the message vendor_class_id with value docsis3.0.
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.flexid
def test_v4_flexid_inside_pool_negative():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           0,
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '192.168.50.10')
    srv_control.add_line({"host-reservation-identifiers": ["flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1, 'identifier-expression', 'option[60].hex')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')

    misc.test_procedure()
    # Client adds to the message vendor_class_id with value docsis3.0.
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.1')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'NAK')


@pytest.mark.v4
@pytest.mark.flexid
def test_v4_flexid_outside_pool():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.9')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           0,
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '192.168.50.10')
    srv_control.add_line({"host-reservation-identifiers": ["flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1, 'identifier-expression', 'option[60].hex')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.flexid
def test_v4_flexid_replace_mac_addr_inside_pool():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet('ip-address',
                                           '192.168.50.10',
                                           0,
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.add_line({"host-reservation-identifiers": ["hw-address", "flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1, 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook(1, 'replace-client-id', True)
    srv_control.set_conf_parameter_global('match-client-id', False)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # server should act normally, mac address should not be replaced
    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
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
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    lease_file_contains('192.168.50.10,ff:01:02:03:ff:04,,4000')
    lease_file_contains('192.168.50.10,ff:01:02:03:ff:04,,0')


@pytest.mark.v4
@pytest.mark.flexid
def test_v4_flexid_replace_client_id_release_fail():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.host_reservation_in_subnet('ip-address',
                                           '192.168.50.10',
                                           0,
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.add_line({"host-reservation-identifiers": ["hw-address", "flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1, 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook(1, 'replace-client-id', True)
    # enable matching client id
    srv_control.set_conf_parameter_global('match-client-id', True)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # server should act normally, mac address should not be replaced
    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    # Client adds to the message vendor_class_id with value docsis3.0.
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'NAK')


@pytest.mark.v4
@pytest.mark.flexid
def test_v4_flexid_replace_client_id_release_1():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.host_reservation_in_subnet('ip-address',
                                           '192.168.50.10',
                                           0,
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.add_line({"host-reservation-identifiers": ["hw-address", "flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1, 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook(1, 'replace-client-id', True)
    # enable matching client id
    srv_control.set_conf_parameter_global('match-client-id', True)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # server should act normally, mac address should not be replaced
    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22:33')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    # client sends message without option 60
    # Client adds to the message vendor_class_id with value docsis3.0.
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22:33:44:55')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')

    lease_file_doesnt_contain('ff:01:02:03:ff:04:11:22:33')
    lease_file_contains('192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,4000')
    lease_file_doesnt_contain('192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,0')


@pytest.mark.v4
@pytest.mark.flexid
def test_v4_flexid_replace_client_id_release_2():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.host_reservation_in_subnet('ip-address',
                                           '192.168.50.10',
                                           0,
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.add_line({"host-reservation-identifiers": ["hw-address", "flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1, 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook(1, 'replace-client-id', True)
    # enable matching client id
    srv_control.set_conf_parameter_global('match-client-id', True)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # server should act normally, mac address should not be replaced
    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22:33')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22:33:44:55')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')

    lease_file_doesnt_contain('ff:01:02:03:ff:04:11:22:33')
    lease_file_contains('192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,4000')
    lease_file_contains('192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,0')


@pytest.mark.v4
@pytest.mark.flexid
def test_v4_flexid_replace_client_id_renew_1():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.host_reservation_in_subnet('ip-address',
                                           '192.168.50.10',
                                           0,
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.add_line({"host-reservation-identifiers": ["hw-address", "flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1, 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook(1, 'replace-client-id', True)
    # enable matching client id
    srv_control.set_conf_parameter_global('match-client-id', True)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # server should act normally, mac address should not be replaced
    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22:33:44:55')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_include_option(54)

    lease_file_doesnt_contain('ff:01:02:03:ff:04:11:22:33')
    lease_file_contains('192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,4000')


@pytest.mark.v4
@pytest.mark.flexid
def test_v4_flexid_replace_client_id_renew_2():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.host_reservation_in_subnet('ip-address',
                                           '192.168.50.10',
                                           0,
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.add_line({"host-reservation-identifiers": ["hw-address", "flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1, 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook(1, 'replace-client-id', True)
    # enable matching client id
    srv_control.set_conf_parameter_global('match-client-id', True)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # server should act normally, mac address should not be replaced
    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    # Client adds to the message vendor_class_id with value docsis3.0.
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10', expected=False)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_include_option(54)

    lease_file_doesnt_contain('ff:01:02:03:ff:04:11:22:33')
    lease_file_contains('192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,4000')


@pytest.mark.v4
@pytest.mark.flexid
def test_v4_flexid_mysql_1():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.add_line({"host-reservation-identifiers": ["hw-address", "flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1, 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook(1, 'replace-client-id', True)
    # enable matching client id
    srv_control.set_conf_parameter_global('match-client-id', True)

    srv_control.enable_db_backend_reservation('MySQL')
    # 646f63736973332e30 = docsis3.0
    srv_control.new_db_backend_reservation('MySQL', 'flex-id', '646f63736973332e30')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'MySQL', 1)
    srv_control.update_db_backend_reservation('ipv4_address', '192.168.50.10', 'MySQL', 1)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'MySQL', 1)
    srv_control.upload_db_reservation('MySQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    # Pause the Test.

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.flexid
def test_v4_flexid_mysql_negative():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.add_line({"host-reservation-identifiers": ["hw-address", "flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1, 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook(1, 'replace-client-id', True)
    # enable matching client id
    srv_control.set_conf_parameter_global('match-client-id', True)

    srv_control.enable_db_backend_reservation('MySQL')
    # 646f63736973332e30 = docsis3.0
    srv_control.new_db_backend_reservation('MySQL', 'flex-id', '646f63736973332e30')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'MySQL', 1)
    srv_control.update_db_backend_reservation('ipv4_address', '192.168.50.10', 'MySQL', 1)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'MySQL', 1)
    srv_control.upload_db_reservation('MySQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
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
    srv_msg.send_wait_for_message('MUST', 'NAK')


@pytest.mark.v4
@pytest.mark.flexid
def test_v4_flexid_pgsql_1():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.add_line({"host-reservation-identifiers": ["hw-address", "flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1, 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook(1, 'replace-client-id', True)
    # enable matching client id
    srv_control.set_conf_parameter_global('match-client-id', True)

    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.new_db_backend_reservation('PostgreSQL', 'flex-id', '646f63736973332e30')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'PostgreSQL', 1)
    srv_control.update_db_backend_reservation('ipv4_address', '192.168.50.10', 'PostgreSQL', 1)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'PostgreSQL', 1)
    srv_control.upload_db_reservation('PostgreSQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    # Pause the Test.

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.flexid
def test_v4_flexid_pgsql_negative():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.add_line({"host-reservation-identifiers": ["hw-address", "flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1, 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook(1, 'replace-client-id', True)
    # enable matching client id
    srv_control.set_conf_parameter_global('match-client-id', True)

    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.new_db_backend_reservation('PostgreSQL', 'flex-id', '646f63736973332e30')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'PostgreSQL', 1)
    srv_control.update_db_backend_reservation('ipv4_address', '192.168.50.10', 'PostgreSQL', 1)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'PostgreSQL', 1)
    srv_control.upload_db_reservation('PostgreSQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    # Pause the Test.

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
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
    srv_msg.send_wait_for_message('MUST', 'NAK')


@pytest.mark.v6
@pytest.mark.flexid
def test_v6_flexid_1():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ff')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           0,
                                           'flex-id',
                                           '\'port1234\'')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '2001:db8:1::f')
    srv_control.add_line({"host-reservation-identifiers": ["duid", "flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1,
                                      'identifier-expression',
                                      'substring(relay6[0].option[18].hex,0,8)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'port1234')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:1::1.
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')


@pytest.mark.disabled
@pytest.mark.v6
@pytest.mark.flexid
def test_v6_flexid_libreload():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ff')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           0,
                                           'flex-id',
                                           '\'port1234\'')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '2001:db8:1::f')
    srv_control.add_line({"host-reservation-identifiers": ["duid", "flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1,
                                      'identifier-expression',
                                      'substring(relay6[0].option[18].hex,0,8)')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'port1234')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:1::1.
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "libreload","arguments": {}}')
    # if reload works - classification should work without changes

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'port1234')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:1::1.
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')


@pytest.mark.v6
@pytest.mark.flexid
def test_v6_flexid_reconfigure_1():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ff')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           0,
                                           'flex-id',
                                           '\'port1234\'')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '2001:db8:1::f')
    srv_control.add_line({"host-reservation-identifiers": ["duid", "flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1,
                                      'identifier-expression',
                                      'substring(relay6[0].option[18].hex,0,8)')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'port1234')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:1::1.
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ff')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           0,
                                           'flex-id',
                                           '\'port1234\'')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '2001:db8:1::f')
    srv_control.add_line({"host-reservation-identifiers": ["duid", "flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1,
                                      'identifier-expression',
                                      'substring(relay6[0].option[18].hex,0,8)')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'reconfigured')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'port1234')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:1::1.
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')


@pytest.mark.v6
@pytest.mark.flexid
def test_v6_flexid_reconfigure_2():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ff')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           0,
                                           'flex-id',
                                           '\'port1234\'')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '2001:db8:1::f')
    srv_control.add_line({"host-reservation-identifiers": ["duid", "flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1,
                                      'identifier-expression',
                                      'substring(relay6[0].option[18].hex,0,8)')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'port1234')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:1::1.
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ff')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           0,
                                           'flex-id',
                                           '\'port4321\'')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '2001:db8:1::f')
    srv_control.add_line({"host-reservation-identifiers": ["duid", "flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1,
                                      'identifier-expression',
                                      'substring(relay6[0].option[18].hex,0,8)')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'reconfigured')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'port1234')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f', expect_include=False)

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'port4321')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')


@pytest.mark.v6
@pytest.mark.flexid
def test_v6_flexid_2():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ff')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           0,
                                           'flex-id',
                                           '\'port1234\'')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '2001:db8:1::f')
    srv_control.add_line({"host-reservation-identifiers": ["duid", "flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1, 'identifier-expression', 'relay6[0].option[18].hex')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Using UNIX socket on server in path control_socket send {"command": "config-reload","arguments":  {} }
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'port1234')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:1::1.
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')


@pytest.mark.v6
@pytest.mark.flexid
def test_v6_flexid_3():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ff')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           0,
                                           'flex-id',
                                           '01:02:03:04:05:06')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '2001:db8:1::f')
    srv_control.add_line({"host-reservation-identifiers": ["duid", "flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1,
                                      'identifier-expression',
                                      'vendor[4491].option[1026].hex')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1026, '01:02:03:04:05:06')
    srv_msg.client_does_include('Client', 'vendor-specific-info')

    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')


@pytest.mark.v6
@pytest.mark.flexid
def test_v6_flexid_mysql_1():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ff')
    srv_control.add_line({"host-reservation-identifiers": ["flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1, 'identifier-expression', 'relay6[0].option[18].hex')

    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.new_db_backend_reservation('MySQL', 'flex-id', '706f727431323334')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'MySQL', 1)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'MySQL', 1)
    srv_control.ipv6_address_db_backend_reservation('2001:db8:1::f', '$(EMPTY)', 'MySQL', 1)
    srv_control.upload_db_reservation('MySQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    # Pause the Test.

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'port1234')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')


@pytest.mark.v6
@pytest.mark.flexid
def test_v6_flexid_mysql_2():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ff')
    srv_control.add_line({"host-reservation-identifiers": ["duid", "flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1,
                                      'identifier-expression',
                                      'vendor[4491].option[1026].hex')

    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.new_db_backend_reservation('MySQL', 'flex-id', '01:02:03:04:05:06')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'MySQL', 1)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'MySQL', 1)
    srv_control.ipv6_address_db_backend_reservation('2001:db8:1::f', '$(EMPTY)', 'MySQL', 1)
    srv_control.upload_db_reservation('MySQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1026, '01:02:03:04:05:06')
    srv_msg.client_does_include('Client', 'vendor-specific-info')

    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')


@pytest.mark.v6
@pytest.mark.flexid
def test_v6_flexid_pgsql_1():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ff')
    srv_control.add_line({"host-reservation-identifiers": ["duid", "flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1, 'identifier-expression', 'relay6[0].option[18].hex')

    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.new_db_backend_reservation('PostgreSQL', 'flex-id', '706f727431323334')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'PostgreSQL', 1)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'PostgreSQL', 1)
    srv_control.ipv6_address_db_backend_reservation('2001:db8:1::f', '$(EMPTY)', 'PostgreSQL', 1)
    srv_control.upload_db_reservation('PostgreSQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    # Pause the Test.

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'port1234')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')


@pytest.mark.v6
@pytest.mark.flexid
def test_v6_flexid_pgsql_2():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ff')
    srv_control.add_line({"host-reservation-identifiers": ["duid", "flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1,
                                      'identifier-expression',
                                      'vendor[4491].option[1026].hex')

    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.new_db_backend_reservation('PostgreSQL', 'flex-id', '01:02:03:04:05:06')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'PostgreSQL', 1)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'PostgreSQL', 1)
    srv_control.ipv6_address_db_backend_reservation('2001:db8:1::f', '$(EMPTY)', 'PostgreSQL', 1)
    srv_control.upload_db_reservation('PostgreSQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1026, '01:02:03:04:05:06')
    srv_msg.client_does_include('Client', 'vendor-specific-info')

    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')


@pytest.mark.v6
@pytest.mark.flexid
def test_v6_flexid_replace_duid():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ff')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           0,
                                           'flex-id',
                                           '01:02:03:04:05:06')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '2001:db8:1::f')
    srv_control.add_line({"host-reservation-identifiers": ["duid", "flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1,
                                      'identifier-expression',
                                      'vendor[4491].option[1026].hex')
    srv_control.add_parameter_to_hook(1, 'replace-client-id', True)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1026, '01:02:03:04:05:06')
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1026, '01:02:03:04:05:06')
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')


@pytest.mark.v6
@pytest.mark.flexid
def test_v6_flexid_replace_duid_renew():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ff')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           0,
                                           'flex-id',
                                           '01:02:03:04:05:06')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '2001:db8:1::f')
    srv_control.add_line({"host-reservation-identifiers": ["duid", "flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1,
                                      'identifier-expression',
                                      'vendor[4491].option[1026].hex')
    srv_control.add_parameter_to_hook(1, 'replace-client-id', True)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1026, '01:02:03:04:05:06')
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1026, '01:02:03:04:05:06')
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')

    # Client with different duid try to renew
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1026, '01:02:03:04:05:06')
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')
    srv_msg.response_check_suboption_content(5, 3, 'validlft', 0, expect_include=False)


@pytest.mark.v6
@pytest.mark.flexid
def test_v6_flexid_replace_duid_renew_failed():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ff')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           0,
                                           'flex-id',
                                           '01:02:03:04:05:06')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '2001:db8:1::f')
    srv_control.add_line({"host-reservation-identifiers": ["duid", "flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1,
                                      'identifier-expression',
                                      'vendor[4491].option[1026].hex')
    srv_control.add_parameter_to_hook(1, 'replace-client-id', True)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1026, '01:02:03:04:05:06')
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1026, '01:02:03:04:05:06')
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')

    # Client with the same DUID and different flex-id try to renew
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1026, '01:02:03:44:55:66')
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')
    srv_msg.response_check_suboption_content(5, 3, 'validlft', 0)


@pytest.mark.v6
@pytest.mark.flexid
def test_v6_flexid_replace_duid_release():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ff')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           0,
                                           'flex-id',
                                           '01:02:03:04:05:06')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '2001:db8:1::f')
    srv_control.add_line({"host-reservation-identifiers": ["duid", "flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1,
                                      'identifier-expression',
                                      'vendor[4491].option[1026].hex')
    srv_control.add_parameter_to_hook(1, 'replace-client-id', True)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1026, '01:02:03:04:05:06')
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1026, '01:02:03:04:05:06')
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')

    # Client with different duid try to release
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1026, '01:02:03:04:05:06')
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 0)


@pytest.mark.v6
@pytest.mark.flexid
def test_v6_flexid_replace_duid_release_failed():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ff')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           0,
                                           'flex-id',
                                           '01:02:03:04:05:06')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '2001:db8:1::f')
    srv_control.add_line({"host-reservation-identifiers": ["duid", "flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1,
                                      'identifier-expression',
                                      'vendor[4491].option[1026].hex')
    srv_control.add_parameter_to_hook(1, 'replace-client-id', True)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1026, '01:02:03:04:05:06')
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1026, '01:02:03:04:05:06')
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')

    # Client with the same duid but different flex-id try to release (result should be nobiding)
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1026, '01:02:03:44:55:66')
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 3)

    # TODO File stored in kea-leases6.csv MUST contain line or phrase: 2001:db8:1::f,01:02:03:04:05:06,4000,
    # TODO File stored in kea-leases6.csv MUST NOT contain line or phrase: 2001:db8:1::f,01:02:03:04:05:06,0,


@pytest.mark.v6
@pytest.mark.flexid
def test_v6_flexid_replace_duid_release_mysql():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ff')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           0,
                                           'flex-id',
                                           '01:02:03:04:05:06')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '2001:db8:1::f')
    srv_control.add_line({"host-reservation-identifiers": ["duid", "flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1,
                                      'identifier-expression',
                                      'vendor[4491].option[1026].hex')
    srv_control.add_parameter_to_hook(1, 'replace-client-id', True)

    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.new_db_backend_reservation('MySQL', 'flex-id', '01:02:03:04:05:06')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'MySQL', 1)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'MySQL', 1)
    srv_control.ipv6_address_db_backend_reservation('2001:db8:1::f', '$(EMPTY)', 'MySQL', 1)
    srv_control.upload_db_reservation('MySQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1026, '11:22:33:44:55:66')
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f', expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1026, '01:02:03:04:05:06')
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1026, '01:02:03:04:05:06')
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')

    # Client with different duid try to release
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1026, '01:02:03:04:05:06')
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 0)


@pytest.mark.v6
@pytest.mark.flexid
def test_v6_flexid_replace_duid_release_pgsql():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ff')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           0,
                                           'flex-id',
                                           '01:02:03:04:05:06')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '2001:db8:1::f')
    srv_control.add_line({"host-reservation-identifiers": ["duid", "flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(1,
                                      'identifier-expression',
                                      'vendor[4491].option[1026].hex')
    srv_control.add_parameter_to_hook(1, 'replace-client-id', True)

    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.new_db_backend_reservation('PostgreSQL', 'flex-id', '01:02:03:04:05:06')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'PostgreSQL', 1)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'PostgreSQL', 1)
    srv_control.ipv6_address_db_backend_reservation('2001:db8:1::f', '$(EMPTY)', 'PostgreSQL', 1)
    srv_control.upload_db_reservation('PostgreSQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1026, '01:02:03:04:05:06')
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1026, '01:02:03:04:05:06')
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::f')

    # Client with different duid try to release
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1026, '01:02:03:04:05:06')
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 0)


# Checks what leases are received when IAIDs are the same or different.
@pytest.mark.v6
@pytest.mark.flexid
def test_v6_iaids():
    # No flex ID
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::f')
    world.dhcp_cfg['subnet6'][0]['pd-pools'] = [
        {
            'delegated-len': 120,
            'prefix': '2001:db8:2::',
            'prefix-len': 80
        }
    ]
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Different leases for different IAIDs
    srv_msg.SARR('2001:db8:1::1', iaid=1)
    srv_msg.SARR('2001:db8:1::1', iaid=1)
    srv_msg.SARR('2001:db8:1::2', iaid=2)
    srv_msg.SARR('2001:db8:1::3', iaid=0)
    srv_msg.SARR('2001:db8:1::4', iaid=0, duid='00:03:00:01:f6:f5:f4:f3:f2:ff')
    srv_msg.SARR(delegated_prefix='2001:db8:2::', iaid=1)
    srv_msg.SARR(delegated_prefix='2001:db8:2::', iaid=1)
    srv_msg.SARR(delegated_prefix='2001:db8:2::100', iaid=2)
    srv_msg.SARR(delegated_prefix='2001:db8:2::200', iaid=0)
    srv_msg.SARR(delegated_prefix='2001:db8:2::300', iaid=0, duid='00:03:00:01:f6:f5:f4:f3:f2:ff')


# Checks the behavior of ignore-iaid.
@pytest.mark.v6
@pytest.mark.flexid
def test_v6_flexid_ignore_iaid():
    # Flex ID with ignore-iaid.
    # The value for identifier-expression is not relevant, but is mandatory.
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::f')
    world.dhcp_cfg['subnet6'][0]['pd-pools'] = [
        {
            'delegated-len': 120,
            'prefix': '2001:db8:2::',
            'prefix-len': 80
        }
    ]
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook('libdhcp_flex_id.so', 'identifier-expression', 'option[1].hex')
    srv_control.add_parameter_to_hook('libdhcp_flex_id.so', 'ignore-iaid', True)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Regardless of IAID, the lease is the same. Unless the DUID changes.
    srv_msg.SARR('2001:db8:1::1', iaid=1)
    srv_msg.SARR('2001:db8:1::1', iaid=1)
    srv_msg.SARR('2001:db8:1::1', iaid=2)
    srv_msg.SARR('2001:db8:1::1', iaid=0)
    srv_msg.SARR('2001:db8:1::2', iaid=0, duid='00:03:00:01:f6:f5:f4:f3:f2:ff')
    srv_msg.SARR(delegated_prefix='2001:db8:2::', iaid=1)
    srv_msg.SARR(delegated_prefix='2001:db8:2::', iaid=1)
    srv_msg.SARR(delegated_prefix='2001:db8:2::', iaid=2)
    srv_msg.SARR(delegated_prefix='2001:db8:2::', iaid=0)
    srv_msg.SARR(delegated_prefix='2001:db8:2::100', iaid=0, duid='00:03:00:01:f6:f5:f4:f3:f2:ff')


# Checks the behavior of ignore-iaid when a packet contains multiple IA requests.
# ignore-iaid should have no effect in this case.
@pytest.mark.v6
@pytest.mark.flexid
def test_v6_flexid_ignore_iaid_multiple_ias():
    # Flex ID with ignore-iaid.
    # The value for identifier-expression is not important, but is mandatory.
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::f')
    world.dhcp_cfg['subnet6'][0]['pd-pools'] = [
        {
            'delegated-len': 120,
            'prefix': '2001:db8:2::',
            'prefix-len': 80
        }
    ]
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook('libdhcp_flex_id.so', 'identifier-expression', 'option[1].hex')
    srv_control.add_parameter_to_hook('libdhcp_flex_id.so', 'ignore-iaid', True)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Check SARR + reply-renew twice with two IA_NAs and two IA_PDs. It should behave like
    # ignore-iaid is disabled. The second time, the client should get the same leases.
    for _ in range(2):
        # Send a solicit.
        srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_sets_value('Client', 'ia_id', 1)
        srv_msg.client_does_include('Client', 'IA_Address')
        srv_msg.client_does_include('Client', 'IA-NA')
        srv_msg.client_sets_value('Client', 'ia_id', 2)
        srv_msg.client_does_include('Client', 'IA_Address')
        srv_msg.client_does_include('Client', 'IA-NA')
        srv_msg.client_sets_value('Client', 'ia_pd', 3)
        srv_msg.client_does_include('Client', 'IA_Prefix')
        srv_msg.client_does_include('Client', 'IA-PD')
        srv_msg.client_sets_value('Client', 'ia_pd', 4)
        srv_msg.client_does_include('Client', 'IA_Prefix')
        srv_msg.client_does_include('Client', 'IA-PD')
        srv_msg.client_send_msg('SOLICIT')

        # Expect an advertise.
        srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
        srv_msg.response_check_include_option('client-id')
        srv_msg.response_check_include_option('server-id')
        srv_msg.check_IA_NA('2001:db8:1::1')
        srv_msg.check_IA_NA('2001:db8:1::2')
        srv_msg.check_IA_NA('2001:db8:1::3', expect=False)
        srv_msg.check_IA_PD('2001:db8:2::')
        srv_msg.check_IA_PD('2001:db8:2::100')
        srv_msg.check_IA_NA('2001:db8:1::200', expect=False)

        # Send a request.
        srv_msg.client_copy_option('IA_NA', copy_all=True)
        srv_msg.client_copy_option('IA_PD', copy_all=True)
        srv_msg.client_copy_option('server-id')
        srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_send_msg('REQUEST')

        # Expect a reply.
        srv_msg.send_wait_for_message('MUST', 'REPLY')
        srv_msg.check_IA_NA('2001:db8:1::1')
        srv_msg.check_IA_NA('2001:db8:1::2')
        srv_msg.check_IA_NA('2001:db8:1::3', expect=False)
        srv_msg.check_IA_PD('2001:db8:2::')
        srv_msg.check_IA_PD('2001:db8:2::100')
        srv_msg.check_IA_NA('2001:db8:1::200', expect=False)
        # Send a renew.
        srv_msg.client_copy_option('IA_NA', copy_all=True)
        srv_msg.client_copy_option('IA_PD', copy_all=True)
        srv_msg.client_copy_option('server-id')
        srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_send_msg('RENEW')

        # Expect a reply.
        srv_msg.send_wait_for_message('MUST', 'REPLY')
        srv_msg.check_IA_NA('2001:db8:1::1')
        srv_msg.check_IA_NA('2001:db8:1::2')
        srv_msg.check_IA_NA('2001:db8:1::3', expect=False)
        srv_msg.check_IA_PD('2001:db8:2::')
        srv_msg.check_IA_PD('2001:db8:2::100')
        srv_msg.check_IA_NA('2001:db8:1::200', expect=False)

    # Check SARR + reply-renew twice with two IA_NAs and two IA_PDs, and changing IAIDs.
    # It should behave like ignore-iaid is disabled.
    for i in range(1, 3):
        # Send a solicit.
        srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_sets_value('Client', 'ia_id', 100 * i + 5)
        srv_msg.client_does_include('Client', 'IA_Address')
        srv_msg.client_does_include('Client', 'IA-NA')
        srv_msg.client_sets_value('Client', 'ia_id', 100 * i + 6)
        srv_msg.client_does_include('Client', 'IA_Address')
        srv_msg.client_does_include('Client', 'IA-NA')
        srv_msg.client_sets_value('Client', 'ia_pd', 100 * i + 7)
        srv_msg.client_does_include('Client', 'IA_Prefix')
        srv_msg.client_does_include('Client', 'IA-PD')
        srv_msg.client_sets_value('Client', 'ia_pd', 100 * i + 8)
        srv_msg.client_does_include('Client', 'IA_Prefix')
        srv_msg.client_does_include('Client', 'IA-PD')
        srv_msg.client_send_msg('SOLICIT')

        # Expect an advertise.
        srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
        srv_msg.response_check_include_option('client-id')
        srv_msg.response_check_include_option('server-id')
        # Next free address is 3.
        srv_msg.check_IA_NA(f'2001:db8:1::{1 + 2 * i:x}')
        srv_msg.check_IA_NA(f'2001:db8:1::{2 + 2 * i:x}')
        srv_msg.check_IA_NA(f'2001:db8:1::{3 + 2 * i:x}', expect=False)
        # Next free PD is 200.
        srv_msg.check_IA_PD(f'2001:db8:2::{2 * i:x}00')
        srv_msg.check_IA_PD(f'2001:db8:2::{1 + 2 * i:x}00')
        srv_msg.check_IA_PD(f'2001:db8:2::{2 + 2 * i:x}00', expect=False)

        # Send a request.
        srv_msg.client_copy_option('IA_NA', copy_all=True)
        srv_msg.client_copy_option('IA_PD', copy_all=True)
        srv_msg.client_copy_option('server-id')
        srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_send_msg('REQUEST')

        # Expect a reply.
        srv_msg.send_wait_for_message('MUST', 'REPLY')
        srv_msg.check_IA_NA(f'2001:db8:1::{1 + 2 * i:x}')
        srv_msg.check_IA_NA(f'2001:db8:1::{2 + 2 * i:x}')
        srv_msg.check_IA_NA(f'2001:db8:1::{3 + 2 * i:x}', expect=False)
        srv_msg.check_IA_PD(f'2001:db8:2::{2 * i:x}00')
        srv_msg.check_IA_PD(f'2001:db8:2::{1 + 2 * i:x}00')
        srv_msg.check_IA_PD(f'2001:db8:2::{2 + 2 * i:x}00', expect=False)

        # Send a renew.
        srv_msg.client_copy_option('IA_NA', copy_all=True)
        srv_msg.client_copy_option('IA_PD', copy_all=True)
        srv_msg.client_copy_option('server-id')
        srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_send_msg('RENEW')

        # Expect a reply.
        srv_msg.send_wait_for_message('MUST', 'REPLY')
        srv_msg.check_IA_NA(f'2001:db8:1::{1 + 2 * i:x}')
        srv_msg.check_IA_NA(f'2001:db8:1::{2 + 2 * i:x}')
        srv_msg.check_IA_NA(f'2001:db8:1::{3 + 2 * i:x}', expect=False)
        srv_msg.check_IA_PD(f'2001:db8:2::{2 * i:x}00')
        srv_msg.check_IA_PD(f'2001:db8:2::{1 + 2 * i:x}00')
        srv_msg.check_IA_PD(f'2001:db8:2::{2 + 2 * i:x}00', expect=False)

    # Check SARR + reply-renew twice with one IA_NA and two IA_PDs, and changing IAIDs.
    # The ignore-iaid should only take effect for the single IA_NA.
    for i in range(1, 3):
        # Send a solicit.
        srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_sets_value('Client', 'ia_id', 100 * i + 9)
        srv_msg.client_does_include('Client', 'IA_Address')
        srv_msg.client_does_include('Client', 'IA-NA')
        srv_msg.client_sets_value('Client', 'ia_pd', 100 * i + 10)
        srv_msg.client_does_include('Client', 'IA_Prefix')
        srv_msg.client_does_include('Client', 'IA-PD')
        srv_msg.client_sets_value('Client', 'ia_pd', 100 * i + 11)
        srv_msg.client_does_include('Client', 'IA_Prefix')
        srv_msg.client_does_include('Client', 'IA-PD')
        srv_msg.client_send_msg('SOLICIT')

        # Expect an advertise.
        srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
        srv_msg.response_check_include_option('client-id')
        srv_msg.response_check_include_option('server-id')
        # Next free address is 7.
        srv_msg.check_IA_NA('2001:db8:1::7')
        srv_msg.check_IA_NA('2001:db8:1::8', expect=False)
        # Next free PD is 600.
        srv_msg.check_IA_PD(f'2001:db8:2::{4 + 2 * i:x}00')
        srv_msg.check_IA_PD(f'2001:db8:2::{5 + 2 * i:x}00')
        srv_msg.check_IA_PD(f'2001:db8:2::{6 + 2 * i:x}00', expect=False)

        # Send a request.
        srv_msg.client_copy_option('IA_NA', copy_all=True)
        srv_msg.client_copy_option('IA_PD', copy_all=True)
        srv_msg.client_copy_option('server-id')
        srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_send_msg('REQUEST')

        # Expect a reply.
        srv_msg.send_wait_for_message('MUST', 'REPLY')
        srv_msg.check_IA_NA('2001:db8:1::7')
        srv_msg.check_IA_NA('2001:db8:1::8', expect=False)
        srv_msg.check_IA_PD(f'2001:db8:2::{4 + 2 * i:x}00')
        srv_msg.check_IA_PD(f'2001:db8:2::{5 + 2 * i:x}00')
        srv_msg.check_IA_PD(f'2001:db8:2::{6 + 2 * i:x}00', expect=False)

        # Send a renew.
        srv_msg.client_copy_option('IA_NA', copy_all=True)
        srv_msg.client_copy_option('IA_PD', copy_all=True)
        srv_msg.client_copy_option('server-id')
        srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_send_msg('RENEW')

        # Expect a reply.
        srv_msg.send_wait_for_message('MUST', 'REPLY')
        srv_msg.check_IA_NA('2001:db8:1::7')
        srv_msg.check_IA_NA('2001:db8:1::8', expect=False)
        srv_msg.check_IA_PD(f'2001:db8:2::{4 + 2 * i:x}00')
        srv_msg.check_IA_PD(f'2001:db8:2::{5 + 2 * i:x}00')
        srv_msg.check_IA_PD(f'2001:db8:2::{6 + 2 * i:x}00', expect=False)

    # Check SARR + reply-renew twice with two IA_NAs and one IA_PD, and changing IAIDs.
    # The ignore-iaid should only take effect for the single IA_PD.
    for i in range(1, 3):
        # Send a solicit.
        srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_sets_value('Client', 'ia_id', 100 * i + 12)
        srv_msg.client_does_include('Client', 'IA_Address')
        srv_msg.client_does_include('Client', 'IA-NA')
        srv_msg.client_sets_value('Client', 'ia_id', 100 * i + 13)
        srv_msg.client_does_include('Client', 'IA_Address')
        srv_msg.client_does_include('Client', 'IA-NA')
        srv_msg.client_sets_value('Client', 'ia_pd', 100 * i + 14)
        srv_msg.client_does_include('Client', 'IA_Prefix')
        srv_msg.client_does_include('Client', 'IA-PD')
        srv_msg.client_send_msg('SOLICIT')

        # Expect an advertise.
        srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
        srv_msg.response_check_include_option('client-id')
        srv_msg.response_check_include_option('server-id')
        # Next free address is 8.
        srv_msg.check_IA_NA(f'2001:db8:1::{6 + 2 * i:x}')
        srv_msg.check_IA_NA(f'2001:db8:1::{7 + 2 * i:x}')
        srv_msg.check_IA_NA(f'2001:db8:1::{8 + 2 * i:x}', expect=False)
        # Next free PD is a00.
        srv_msg.check_IA_PD('2001:db8:2::a00')
        srv_msg.check_IA_PD('2001:db8:2::b00', expect=False)

        # Send a request.
        srv_msg.client_copy_option('IA_NA', copy_all=True)
        srv_msg.client_copy_option('IA_PD', copy_all=True)
        srv_msg.client_copy_option('server-id')
        srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_send_msg('REQUEST')

        # Expect a reply.
        srv_msg.send_wait_for_message('MUST', 'REPLY')
        srv_msg.check_IA_NA(f'2001:db8:1::{6 + 2 * i:x}')
        srv_msg.check_IA_NA(f'2001:db8:1::{7 + 2 * i:x}')
        srv_msg.check_IA_NA(f'2001:db8:1::{8 + 2 * i:x}', expect=False)
        srv_msg.check_IA_PD('2001:db8:2::a00')
        srv_msg.check_IA_PD('2001:db8:2::b00', expect=False)

        # Send a renew.
        srv_msg.client_copy_option('IA_NA', copy_all=True)
        srv_msg.client_copy_option('IA_PD', copy_all=True)
        srv_msg.client_copy_option('server-id')
        srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_send_msg('RENEW')

        # Expect a reply.
        srv_msg.send_wait_for_message('MUST', 'REPLY')
        srv_msg.check_IA_NA(f'2001:db8:1::{6 + 2 * i:x}')
        srv_msg.check_IA_NA(f'2001:db8:1::{7 + 2 * i:x}')
        srv_msg.check_IA_NA(f'2001:db8:1::{8 + 2 * i:x}', expect=False)
        srv_msg.check_IA_PD('2001:db8:2::a00')
        srv_msg.check_IA_PD('2001:db8:2::b00', expect=False)


# kea#181
# support#21803
@pytest.mark.v6
@pytest.mark.flexid
def test_v6_flexid_reservation_changing_duid():
    """
    Checks that there is a way to configure Kea such that a returning client that changes its DUID
    gets the same reserved address. This can be done with a flex ID reservation. Clients that change
    their DUID sometimes arise in PXE-booting scenarios.
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/32', '2001:db8::1-2001:db8::4')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook('libdhcp_flex_id.so', 'identifier-expression', 'option[79].hex')
    srv_control.add_parameter_to_hook('libdhcp_flex_id.so', 'replace-client-id', True)
    world.dhcp_cfg['host-reservation-identifiers'] = ['flex-id']
    world.dhcp_cfg['subnet6'][0]['reservations'] = [
        {
            'flex-id': '00:01:52:54:00:52:da:87',
            'ip-addresses': ['2001:db8::8']
        }
    ]

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Send a solicit.
    srv_msg.client_sets_value('Client', 'DUID', '00:01:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_does_include('Client', 'client-link-layer-addr')
    srv_msg.client_send_msg('SOLICIT')

    # Expect an advertise.
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option('client-id')
    srv_msg.response_check_include_option('server-id')
    srv_msg.check_IA_NA('2001:db8::8')

    # Send a request.
    srv_msg.client_copy_option('IA_NA', copy_all=True)
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'DUID', '00:01:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'client-link-layer-addr')
    srv_msg.client_send_msg('REQUEST')

    # Expect a reply.
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.check_IA_NA('2001:db8::8')

    # Send a renew.
    srv_msg.client_copy_option('IA_NA', copy_all=True)
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'DUID', '00:01:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'client-link-layer-addr')
    srv_msg.client_send_msg('RENEW')

    # Expect a reply.
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.check_IA_NA('2001:db8::8')

    # Send a solicit.
    srv_msg.client_sets_value('Client', 'DUID', '00:01:00:01:f7:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_does_include('Client', 'client-link-layer-addr')
    srv_msg.client_send_msg('SOLICIT')

    # Expect an advertise.
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option('client-id')
    srv_msg.response_check_include_option('server-id')
    srv_msg.check_IA_NA('2001:db8::8')

    # Send a request.
    srv_msg.client_copy_option('IA_NA', copy_all=True)
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'DUID', '00:01:00:01:f7:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'client-link-layer-addr')
    srv_msg.client_send_msg('REQUEST')

    # Expect a reply.
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.check_IA_NA('2001:db8::8')

    # Send a renew.
    srv_msg.client_copy_option('IA_NA', copy_all=True)
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'DUID', '00:01:00:01:f7:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'client-link-layer-addr')
    srv_msg.client_send_msg('RENEW')

    # Expect a reply.
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.check_IA_NA('2001:db8::8')
