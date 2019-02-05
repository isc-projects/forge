"""Kea Hook flex-id testing"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_control
from features import misc
from features import srv_msg


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_libreload(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-hostname',
                                           '0',
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'address', '192.168.50.10')
    srv_control.add_line(step, '"host-reservation-identifiers": [ "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step, '1', 'identifier-expression', 'option[60].hex')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "libreload","arguments": {}}')
    # if reload works - classification should work without changes

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_reconfigure(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-hostname',
                                           '0',
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'address', '192.168.50.10')
    srv_control.add_line(step, '"host-reservation-identifiers": [ "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step, '1', 'identifier-expression', 'option[60].hex')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-hostname',
                                           '0',
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'address', '192.168.50.10')
    srv_control.add_line(step, '"host-reservation-identifiers": [ "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step, '1', 'identifier-expression', 'option[60].hex')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'reconfigured')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_inside_pool(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-hostname',
                                           '0',
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'address', '192.168.50.10')
    srv_control.add_line(step, '"host-reservation-identifiers": [ "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step, '1', 'identifier-expression', 'option[60].hex')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure(step)
    # Client adds to the message vendor_class_id with value docsis3.0.
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_inside_pool_negative(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-hostname',
                                           '0',
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'address', '192.168.50.10')
    srv_control.add_line(step, '"host-reservation-identifiers": [ "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step, '1', 'identifier-expression', 'option[60].hex')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure(step)
    # Client adds to the message vendor_class_id with value docsis3.0.
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.1')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'NAK')


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_outside_pool(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.9')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-hostname',
                                           '0',
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'address', '192.168.50.10')
    srv_control.add_line(step, '"host-reservation-identifiers": [ "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step, '1', 'identifier-expression', 'option[60].hex')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_replace_mac_addr_inside_pool(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.10',
                                           '0',
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.add_line(step, '"host-reservation-identifiers": ["hw-address", "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step, '1', 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook(step, '1', 'replace-client-id', 'true')
    srv_control.set_conf_parameter_global(step, 'match-client-id', 'false')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # server should act normally, mac address should not be replaced
    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv',
                               None,
                               '192.168.50.10,ff:01:02:03:ff:04,,4000')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv',
                               None,
                               '192.168.50.10,ff:01:02:03:ff:04,,0')


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_replace_client_id_release_fail(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.10',
                                           '0',
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.add_line(step, '"host-reservation-identifiers": ["hw-address", "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step, '1', 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook(step, '1', 'replace-client-id', 'true')
    # enable matching client id
    srv_control.set_conf_parameter_global(step, 'match-client-id', 'true')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # server should act normally, mac address should not be replaced
    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    # Client adds to the message vendor_class_id with value docsis3.0.
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'NAK')


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_replace_client_id_release_1(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.10',
                                           '0',
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.add_line(step, '"host-reservation-identifiers": ["hw-address", "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step, '1', 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook(step, '1', 'replace-client-id', 'true')
    # enable matching client id
    srv_control.set_conf_parameter_global(step, 'match-client-id', 'true')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # server should act normally, mac address should not be replaced
    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22:33')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    # client sends message without option 60
    # Client adds to the message vendor_class_id with value docsis3.0.
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22:33:44:55')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv',
                               'NOT ',
                               'ff:01:02:03:ff:04:11:22:33')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv',
                               None,
                               '192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,4000')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv',
                               'NOT ',
                               '192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,0')


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_replace_client_id_release_2(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.10',
                                           '0',
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.add_line(step, '"host-reservation-identifiers": ["hw-address", "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step, '1', 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook(step, '1', 'replace-client-id', 'true')
    # enable matching client id
    srv_control.set_conf_parameter_global(step, 'match-client-id', 'true')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # server should act normally, mac address should not be replaced
    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22:33')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22:33:44:55')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv',
                               'NOT ',
                               'ff:01:02:03:ff:04:11:22:33')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv',
                               None,
                               '192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,4000')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv',
                               None,
                               '192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,0')


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_replace_client_id_renew_1(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.10',
                                           '0',
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.add_line(step, '"host-reservation-identifiers": ["hw-address", "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step, '1', 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook(step, '1', 'replace-client-id', 'true')
    # enable matching client id
    srv_control.set_conf_parameter_global(step, 'match-client-id', 'true')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # server should act normally, mac address should not be replaced
    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22:33:44:55')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '61')
    srv_msg.response_check_include_option(step, 'Response', None, '54')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv',
                               'NOT ',
                               'ff:01:02:03:ff:04:11:22:33')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv',
                               None,
                               '192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,4000')


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_replace_client_id_renew_2(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.10',
                                           '0',
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.add_line(step, '"host-reservation-identifiers": ["hw-address", "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step, '1', 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook(step, '1', 'replace-client-id', 'true')
    # enable matching client id
    srv_control.set_conf_parameter_global(step, 'match-client-id', 'true')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # server should act normally, mac address should not be replaced
    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    # Client adds to the message vendor_class_id with value docsis3.0.
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', 'NOT ', 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '61')
    srv_msg.response_check_include_option(step, 'Response', None, '54')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv',
                               'NOT ',
                               'ff:01:02:03:ff:04:11:22:33')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv',
                               None,
                               '192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,4000')


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_mysql_1(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.add_line(step, '"host-reservation-identifiers": ["hw-address", "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step, '1', 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook(step, '1', 'replace-client-id', 'true')
    # enable matching client id
    srv_control.set_conf_parameter_global(step, 'match-client-id', 'true')

    srv_control.enable_db_backend_reservation(step, 'MySQL')
    # 646f63736973332e30 = docsis3.0
    srv_control.new_db_backend_reservation(step, 'MySQL', 'flex-id', '646f63736973332e30')
    srv_control.update_db_backend_reservation(step, 'hostname', 'reserved-hostname', 'MySQL', '1')
    srv_control.update_db_backend_reservation(step, 'ipv4_address', '192.168.50.10', 'MySQL', '1')
    srv_control.update_db_backend_reservation(step, 'dhcp4_subnet_id', '1', 'MySQL', '1')
    srv_control.upload_db_reservation(step, 'MySQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')
    # Pause the Test.

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_mysql_negative(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.add_line(step, '"host-reservation-identifiers": ["hw-address", "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step, '1', 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook(step, '1', 'replace-client-id', 'true')
    # enable matching client id
    srv_control.set_conf_parameter_global(step, 'match-client-id', 'true')

    srv_control.enable_db_backend_reservation(step, 'MySQL')
    # 646f63736973332e30 = docsis3.0
    srv_control.new_db_backend_reservation(step, 'MySQL', 'flex-id', '646f63736973332e30')
    srv_control.update_db_backend_reservation(step, 'hostname', 'reserved-hostname', 'MySQL', '1')
    srv_control.update_db_backend_reservation(step, 'ipv4_address', '192.168.50.10', 'MySQL', '1')
    srv_control.update_db_backend_reservation(step, 'dhcp4_subnet_id', '1', 'MySQL', '1')
    srv_control.upload_db_reservation(step, 'MySQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'NAK')


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_pgsql_1(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.add_line(step, '"host-reservation-identifiers": ["hw-address", "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step, '1', 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook(step, '1', 'replace-client-id', 'true')
    # enable matching client id
    srv_control.set_conf_parameter_global(step, 'match-client-id', 'true')

    srv_control.enable_db_backend_reservation(step, 'PostgreSQL')
    srv_control.new_db_backend_reservation(step, 'PostgreSQL', 'flex-id', '646f63736973332e30')
    srv_control.update_db_backend_reservation(step,
                                              'hostname',
                                              'reserved-hostname',
                                              'PostgreSQL',
                                              '1')
    srv_control.update_db_backend_reservation(step,
                                              'ipv4_address',
                                              '192.168.50.10',
                                              'PostgreSQL',
                                              '1')
    srv_control.update_db_backend_reservation(step, 'dhcp4_subnet_id', '1', 'PostgreSQL', '1')
    srv_control.upload_db_reservation(step, 'PostgreSQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')
    # Pause the Test.

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v4_hooks_flexid_pgsql_negative(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.5')
    srv_control.add_line(step, '"host-reservation-identifiers": ["hw-address", "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step, '1', 'identifier-expression', 'option[60].hex')
    srv_control.add_parameter_to_hook(step, '1', 'replace-client-id', 'true')
    # enable matching client id
    srv_control.set_conf_parameter_global(step, 'match-client-id', 'true')

    srv_control.enable_db_backend_reservation(step, 'PostgreSQL')
    srv_control.new_db_backend_reservation(step, 'PostgreSQL', 'flex-id', '646f63736973332e30')
    srv_control.update_db_backend_reservation(step,
                                              'hostname',
                                              'reserved-hostname',
                                              'PostgreSQL',
                                              '1')
    srv_control.update_db_backend_reservation(step,
                                              'ipv4_address',
                                              '192.168.50.10',
                                              'PostgreSQL',
                                              '1')
    srv_control.update_db_backend_reservation(step, 'dhcp4_subnet_id', '1', 'PostgreSQL', '1')
    srv_control.upload_db_reservation(step, 'PostgreSQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')
    # Pause the Test.

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'NAK')
