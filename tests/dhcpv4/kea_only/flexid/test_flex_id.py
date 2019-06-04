"""Kea Hook flex-id testing"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_msg
import srv_control


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_libreload():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           '0',
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.host_reservation_in_subnet_add_value('0', '0', 'address', '192.168.50.10')
    srv_control.add_line('"host-reservation-identifiers": [ "flex-id" ]')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook('1', 'identifier-expression', 'option[60].hex')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "libreload","arguments": {}}')
    # if reload works - classification should work without changes

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_reconfigure():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           '0',
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.host_reservation_in_subnet_add_value('0', '0', 'address', '192.168.50.10')
    srv_control.add_line('"host-reservation-identifiers": [ "flex-id" ]')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook('1', 'identifier-expression', 'option[60].hex')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           '0',
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.host_reservation_in_subnet_add_value('0', '0', 'address', '192.168.50.10')
    srv_control.add_line('"host-reservation-identifiers": [ "flex-id" ]')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook('1', 'identifier-expression', 'option[60].hex')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'reconfigured')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_inside_pool():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           '0',
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.host_reservation_in_subnet_add_value('0', '0', 'address', '192.168.50.10')
    srv_control.add_line('"host-reservation-identifiers": [ "flex-id" ]')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook('1', 'identifier-expression', 'option[60].hex')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure()
    # Client adds to the message vendor_class_id with value docsis3.0.
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_inside_pool_negative():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           '0',
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.host_reservation_in_subnet_add_value('0', '0', 'address', '192.168.50.10')
    srv_control.add_line('"host-reservation-identifiers": [ "flex-id" ]')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook('1', 'identifier-expression', 'option[60].hex')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure()
    # Client adds to the message vendor_class_id with value docsis3.0.
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.1')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'NAK')


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_outside_pool():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.9')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           '0',
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.host_reservation_in_subnet_add_value('0', '0', 'address', '192.168.50.10')
    srv_control.add_line('"host-reservation-identifiers": [ "flex-id" ]')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook('1', 'identifier-expression', 'option[60].hex')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_replace_mac_addr_inside_pool():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.10',
                                           '0',
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.add_line('"host-reservation-identifiers": ["hw-address", "flex-id" ]')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook('1', 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook('1', 'replace-client-id', 'true')
    srv_control.set_conf_parameter_global('match-client-id', 'false')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    # server should act normally, mac address should not be replaced
    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.lease_file_contains('192.168.50.10,ff:01:02:03:ff:04,,4000')
    srv_msg.lease_file_contains('192.168.50.10,ff:01:02:03:ff:04,,0')


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_replace_client_id_release_fail():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.10',
                                           '0',
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.add_line('"host-reservation-identifiers": ["hw-address", "flex-id" ]')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook('1', 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook('1', 'replace-client-id', 'true')
    # enable matching client id
    srv_control.set_conf_parameter_global('match-client-id', 'true')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    # server should act normally, mac address should not be replaced
    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    # Client adds to the message vendor_class_id with value docsis3.0.
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'NAK')


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_replace_client_id_release_1():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.10',
                                           '0',
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.add_line('"host-reservation-identifiers": ["hw-address", "flex-id" ]')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook('1', 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook('1', 'replace-client-id', 'true')
    # enable matching client id
    srv_control.set_conf_parameter_global('match-client-id', 'true')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    # server should act normally, mac address should not be replaced
    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

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
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')

    srv_msg.lease_file_doesnt_contain('ff:01:02:03:ff:04:11:22:33')
    srv_msg.lease_file_contains('192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,4000')
    srv_msg.lease_file_doesnt_contain('192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,0')


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_replace_client_id_release_2():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.10',
                                           '0',
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.add_line('"host-reservation-identifiers": ["hw-address", "flex-id" ]')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook('1', 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook('1', 'replace-client-id', 'true')
    # enable matching client id
    srv_control.set_conf_parameter_global('match-client-id', 'true')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    # server should act normally, mac address should not be replaced
    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

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
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')

    srv_msg.lease_file_doesnt_contain('ff:01:02:03:ff:04:11:22:33')
    srv_msg.lease_file_contains('192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,4000')
    srv_msg.lease_file_contains('192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,0')


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_replace_client_id_renew_1():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.10',
                                           '0',
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.add_line('"host-reservation-identifiers": ["hw-address", "flex-id" ]')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook('1', 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook('1', 'replace-client-id', 'true')
    # enable matching client id
    srv_control.set_conf_parameter_global('match-client-id', 'true')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    # server should act normally, mac address should not be replaced
    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22:33:44:55')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '61')
    srv_msg.response_check_include_option('Response', None, '54')

    srv_msg.lease_file_doesnt_contain('ff:01:02:03:ff:04:11:22:33')
    srv_msg.lease_file_contains('192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,4000')


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_replace_client_id_renew_2():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.50.10',
                                           '0',
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.add_line('"host-reservation-identifiers": ["hw-address", "flex-id" ]')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook('1', 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook('1', 'replace-client-id', 'true')
    # enable matching client id
    srv_control.set_conf_parameter_global('match-client-id', 'true')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    # server should act normally, mac address should not be replaced
    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    # Client adds to the message vendor_class_id with value docsis3.0.
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', 'NOT ', 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '61')
    srv_msg.response_check_include_option('Response', None, '54')

    srv_msg.lease_file_doesnt_contain('ff:01:02:03:ff:04:11:22:33')
    srv_msg.lease_file_contains('192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,4000')


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_mysql_1():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.add_line('"host-reservation-identifiers": ["hw-address", "flex-id" ]')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook('1', 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook('1', 'replace-client-id', 'true')
    # enable matching client id
    srv_control.set_conf_parameter_global('match-client-id', 'true')

    srv_control.enable_db_backend_reservation('MySQL')
    # 646f63736973332e30 = docsis3.0
    srv_control.new_db_backend_reservation('MySQL', 'flex-id', '646f63736973332e30')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'MySQL', '1')
    srv_control.update_db_backend_reservation('ipv4_address', '192.168.50.10', 'MySQL', '1')
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', '1', 'MySQL', '1')
    srv_control.upload_db_reservation('MySQL')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')
    # Pause the Test.

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_mysql_negative():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.add_line('"host-reservation-identifiers": ["hw-address", "flex-id" ]')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook('1', 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook('1', 'replace-client-id', 'true')
    # enable matching client id
    srv_control.set_conf_parameter_global('match-client-id', 'true')

    srv_control.enable_db_backend_reservation('MySQL')
    # 646f63736973332e30 = docsis3.0
    srv_control.new_db_backend_reservation('MySQL', 'flex-id', '646f63736973332e30')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'MySQL', '1')
    srv_control.update_db_backend_reservation('ipv4_address', '192.168.50.10', 'MySQL', '1')
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', '1', 'MySQL', '1')
    srv_control.upload_db_reservation('MySQL')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'NAK')


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_pgsql_1():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.add_line('"host-reservation-identifiers": ["hw-address", "flex-id" ]')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook('1', 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook('1', 'replace-client-id', 'true')
    # enable matching client id
    srv_control.set_conf_parameter_global('match-client-id', 'true')

    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.new_db_backend_reservation('PostgreSQL', 'flex-id', '646f63736973332e30')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'PostgreSQL', '1')
    srv_control.update_db_backend_reservation('ipv4_address', '192.168.50.10', 'PostgreSQL', '1')
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', '1', 'PostgreSQL', '1')
    srv_control.upload_db_reservation('PostgreSQL')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')
    # Pause the Test.

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_pgsql_negative():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.add_line('"host-reservation-identifiers": ["hw-address", "flex-id" ]')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook('1', 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook('1', 'replace-client-id', 'true')
    # enable matching client id
    srv_control.set_conf_parameter_global('match-client-id', 'true')

    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.new_db_backend_reservation('PostgreSQL', 'flex-id', '646f63736973332e30')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'PostgreSQL', '1')
    srv_control.update_db_backend_reservation('ipv4_address', '192.168.50.10', 'PostgreSQL', '1')
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', '1', 'PostgreSQL', '1')
    srv_control.upload_db_reservation('PostgreSQL')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')
    # Pause the Test.

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'NAK')
