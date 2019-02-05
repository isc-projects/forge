"""Shared-Networks"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_msg
from features import misc
from features import srv_control


@pytest.mark.v4
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v4_sharednetworks_negative_missing_name(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.1')
    # first shared subnet
    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '0')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    # DHCP server is started.
    srv_control.start_srv_during_process(step, 'DHCP', 'configure')


@pytest.mark.v4
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v4_sharednetworks_negative_not_unique_names(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.1')
    # first shared subnet
    srv_control.shared_subnet(step, '0', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '0')
    # second shared-subnet
    srv_control.shared_subnet(step, '1', '1')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '1')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv_during_process(step, 'DHCP', 'configure')


@pytest.mark.v4
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v4_sharednetworks_single_shared_subnet_with_one_subnet_based_on_iface(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.shared_subnet(step, '0', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '0')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v4_sharednetworks_single_shared_subnet_with_one_subnet_based_on_relay_address(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.shared_subnet(step, '0', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step,
                                                 'relay',
                                                 '{"ip-address":"$(GIADDR4)"}',
                                                 '0')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    # local client should not get anything!
    # let's fix it finally :/
    # Test Procedure:
    # Client requests option 1.
    # Client sets chaddr value to ff:01:02:03:ff:04.
    # Client sends DISCOVER message.
    #
    # Pass Criteria:
    # Server MUST NOT respond.
    misc.test_procedure(step)
    srv_msg.network_variable(step, 'source_port', '67')
    srv_msg.network_variable(step, 'source_address', '$(GIADDR4)')
    srv_msg.network_variable(step, 'destination_address', '$(SRV4_ADDR)')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.network_variable(step, 'source_port', '67')
    srv_msg.network_variable(step, 'source_address', '$(GIADDR4)')
    srv_msg.network_variable(step, 'destination_address', '$(SRV4_ADDR)')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)


@pytest.mark.v4
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v4_sharednetworks_single_shared_subnet_with_two_subnets_based_on_iface(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.1')
    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '0')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:33')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:33')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.51.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv',
                               None,
                               '192.168.50.1,00:00:00:00:00:22')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv',
                               None,
                               '192.168.51.1,00:00:00:00:00:33')


@pytest.mark.v4
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v4_sharednetworks_single_shared_subnet_with_tree_subnets_based_on_iface_options_override(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.52.0/24',
                                                       '192.168.52.1-192.168.52.1')
    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')
    srv_control.shared_subnet(step, '2', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '0')

    srv_control.config_srv_opt(step, 'time-servers', '199.199.199.1')
    srv_control.config_srv(step, 'time-servers', '0', '199.199.199.10')
    srv_control.config_srv(step, 'time-servers', '1', '199.199.199.100')
    srv_control.config_srv(step, 'time-servers', '2', '199.199.199.200')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '4')
    srv_msg.response_check_option_content(step, 'Response', '4', None, 'value', '199.199.199.10')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.100')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.200')
    srv_msg.response_check_option_content(step, 'Response', '4', 'NOT ', 'value', '199.199.199.1')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '4')
    srv_msg.response_check_option_content(step, 'Response', '4', None, 'value', '199.199.199.10')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.100')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.200')
    srv_msg.response_check_option_content(step, 'Response', '4', 'NOT ', 'value', '199.199.199.1')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv',
                               None,
                               '192.168.50.1,00:00:00:00:00:22')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:33')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '4')
    srv_msg.response_check_option_content(step, 'Response', '4', None, 'value', '199.199.199.100')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.10')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.200')
    srv_msg.response_check_option_content(step, 'Response', '4', 'NOT ', 'value', '199.199.199.1')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:33')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.51.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '4')
    srv_msg.response_check_option_content(step, 'Response', '4', None, 'value', '199.199.199.100')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.10')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.200')
    srv_msg.response_check_option_content(step, 'Response', '4', 'NOT ', 'value', '199.199.199.1')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv',
                               None,
                               '192.168.51.1,00:00:00:00:00:33')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:44')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.52.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '4')
    srv_msg.response_check_option_content(step, 'Response', '4', None, 'value', '199.199.199.200')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.100')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.10')
    srv_msg.response_check_option_content(step, 'Response', '4', 'NOT ', 'value', '199.199.199.1')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:44')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.52.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.52.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '4')
    srv_msg.response_check_option_content(step, 'Response', '4', None, 'value', '199.199.199.200')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.100')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.100')
    srv_msg.response_check_option_content(step, 'Response', '4', 'NOT ', 'value', '199.199.199.1')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv',
                               None,
                               '192.168.52.1,00:00:00:00:00:44')


@pytest.mark.v4
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v4_sharednetworks_single_shared_subnet_with_three_subnets_based_on_relay_address_options_override(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.52.0/24',
                                                       '192.168.52.1-192.168.52.1')
    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')
    srv_control.shared_subnet(step, '2', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step,
                                                 'relay',
                                                 '{"ip-address":"$(GIADDR4)"}',
                                                 '0')

    srv_control.config_srv_opt(step, 'time-servers', '199.199.199.1')
    srv_control.config_srv(step, 'time-servers', '0', '199.199.199.10')
    srv_control.config_srv(step, 'time-servers', '1', '199.199.199.100')
    srv_control.config_srv(step, 'time-servers', '2', '199.199.199.200')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    # 1
    misc.test_procedure(step)
    srv_msg.network_variable(step, 'source_port', '67')
    srv_msg.network_variable(step, 'source_address', '$(GIADDR4)')
    srv_msg.network_variable(step, 'destination_address', '$(SRV4_ADDR)')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '4')
    srv_msg.response_check_option_content(step, 'Response', '4', None, 'value', '199.199.199.10')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.100')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.200')
    srv_msg.response_check_option_content(step, 'Response', '4', 'NOT ', 'value', '199.199.199.1')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '4')
    srv_msg.response_check_option_content(step, 'Response', '4', None, 'value', '199.199.199.10')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.100')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.200')
    srv_msg.response_check_option_content(step, 'Response', '4', 'NOT ', 'value', '199.199.199.1')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv',
                               None,
                               '192.168.50.1,00:00:00:00:00:11')

    # 2
    misc.test_procedure(step)
    srv_msg.network_variable(step, 'source_port', '67')
    srv_msg.network_variable(step, 'source_address', '$(GIADDR4)')
    srv_msg.network_variable(step, 'destination_address', '$(SRV4_ADDR)')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '4')
    srv_msg.response_check_option_content(step, 'Response', '4', None, 'value', '199.199.199.100')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.10')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.200')
    srv_msg.response_check_option_content(step, 'Response', '4', 'NOT ', 'value', '199.199.199.1')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.51.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '4')
    srv_msg.response_check_option_content(step, 'Response', '4', None, 'value', '199.199.199.100')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.10')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.200')
    srv_msg.response_check_option_content(step, 'Response', '4', 'NOT ', 'value', '199.199.199.1')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv',
                               None,
                               '192.168.51.1,00:00:00:00:00:22')

    # 3
    misc.test_procedure(step)
    srv_msg.network_variable(step, 'source_port', '67')
    srv_msg.network_variable(step, 'source_address', '$(GIADDR4)')
    srv_msg.network_variable(step, 'destination_address', '$(SRV4_ADDR)')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:33')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.52.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '4')
    srv_msg.response_check_option_content(step, 'Response', '4', None, 'value', '199.199.199.200')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.10')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.100')
    srv_msg.response_check_option_content(step, 'Response', '4', 'NOT ', 'value', '199.199.199.1')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.52.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:33')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.52.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '4')
    srv_msg.response_check_option_content(step, 'Response', '4', None, 'value', '199.199.199.200')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.10')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.100')
    srv_msg.response_check_option_content(step, 'Response', '4', 'NOT ', 'value', '199.199.199.1')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv',
                               None,
                               '192.168.52.1,00:00:00:00:00:33')

    # 4
    misc.test_procedure(step)
    srv_msg.network_variable(step, 'source_port', '67')
    srv_msg.network_variable(step, 'source_address', '$(GIADDR4)')
    srv_msg.network_variable(step, 'destination_address', '$(SRV4_ADDR)')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:44')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)


@pytest.mark.v4
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v4_sharednetworks_two_shared_subnet_with_two_subnets_based_on_relay_address_and_iface(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.52.0/24',
                                                       '192.168.52.1-192.168.52.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.53.0/24',
                                                       '192.168.53.1-192.168.53.1')
    # first shared subnet
    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '0')
    # second shared-subnet
    srv_control.shared_subnet(step, '2', '1')
    srv_control.shared_subnet(step, '3', '1')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-xyz"', '1')
    srv_control.set_conf_parameter_shared_subnet(step,
                                                 'relay',
                                                 '{"ip-address":"$(GIADDR4)"}',
                                                 '1')

    srv_control.config_srv(step, 'time-servers', '0', '199.199.199.10')
    srv_control.config_srv(step, 'time-servers', '2', '199.199.199.100')
    srv_control.config_srv(step, 'time-servers', '3', '199.199.199.200')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:aa')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:aa')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:bb')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:bb')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.51.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv',
                               None,
                               '192.168.50.1,00:00:00:00:00:aa')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv',
                               None,
                               '192.168.51.1,00:00:00:00:00:bb')

    misc.test_procedure(step)
    srv_msg.network_variable(step, 'source_port', '67')
    srv_msg.network_variable(step, 'source_address', '$(GIADDR4)')
    srv_msg.network_variable(step, 'destination_address', '$(SRV4_ADDR)')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.52.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '4')
    srv_msg.response_check_option_content(step, 'Response', '4', None, 'value', '199.199.199.100')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.10')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.200')
    srv_msg.response_check_option_content(step, 'Response', '4', 'NOT ', 'value', '199.199.199.1')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.52.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.52.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '4')
    srv_msg.response_check_option_content(step, 'Response', '4', None, 'value', '199.199.199.100')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.10')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.200')
    srv_msg.response_check_option_content(step, 'Response', '4', 'NOT ', 'value', '199.199.199.1')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv',
                               None,
                               '192.168.52.1,00:00:00:00:00:22')

    # 3
    misc.test_procedure(step)
    srv_msg.network_variable(step, 'source_port', '67')
    srv_msg.network_variable(step, 'source_address', '$(GIADDR4)')
    srv_msg.network_variable(step, 'destination_address', '$(SRV4_ADDR)')
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:33')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.53.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '4')
    srv_msg.response_check_option_content(step, 'Response', '4', None, 'value', '199.199.199.200')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.10')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.100')
    srv_msg.response_check_option_content(step, 'Response', '4', 'NOT ', 'value', '199.199.199.1')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.53.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:33')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.53.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '4')
    srv_msg.response_check_option_content(step, 'Response', '4', None, 'value', '199.199.199.200')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.10')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '4',
                                          'NOT ',
                                          'value',
                                          '199.199.199.100')
    srv_msg.response_check_option_content(step, 'Response', '4', 'NOT ', 'value', '199.199.199.1')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv',
                               None,
                               '192.168.53.1,00:00:00:00:00:33')


@pytest.mark.v4
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v4_sharednetworks_single_shared_subnet_with_three_subnets_client_classification(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.52.0/24',
                                                       '192.168.52.1-192.168.52.1')
    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')
    srv_control.shared_subnet(step, '2', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '0')

    srv_control.config_srv_opt(step, 'time-servers', '199.199.199.1')
    srv_control.config_srv(step, 'time-servers', '0', '199.199.199.10')
    srv_control.config_srv(step, 'time-servers', '1', '199.199.199.100')
    srv_control.config_srv(step, 'time-servers', '2', '199.199.199.200')

    srv_control.create_new_class(step, 'Client_f2f1')
    srv_control.add_test_to_class(step, '1', 'test', 'option[61].hex == 0xff010203ff04f1f2')
    srv_control.config_client_classification(step, '1', 'Client_f2f1')

    srv_control.create_new_class(step, 'Client_f2f2')
    srv_control.add_test_to_class(step, '2', 'test', 'option[61].hex == 0xff010203ff04f2f2')
    srv_control.config_client_classification(step, '2', 'Client_f2f2')

    srv_control.create_new_class(step, 'Client_f2f0')
    srv_control.add_test_to_class(step, '3', 'test', 'option[61].hex == 0xff010203ff04f299')
    srv_control.config_client_classification(step, '0', 'Client_f2f0')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:f1:f2')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:f1:f2')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.51.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    # File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.50.1,00:00:00:00:00:22
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:33')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:f2:f2')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.52.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:33')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:f2:f2')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.52.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.52.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    # File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.51.1,00:00:00:00:00:33


@pytest.mark.v4
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v4_sharednetworks_single_shared_subnet_with_three_subnets_client_classification_server_identifier(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.52.0/24',
                                                       '192.168.52.1-192.168.52.1')
    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')
    srv_control.shared_subnet(step, '2', '0')

    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '0')

    srv_control.config_srv(step, 'dhcp-server-identifier', '1', '11.22.33.123')
    srv_control.config_srv(step, 'dhcp-server-identifier', '2', '44.44.44.222')

    srv_control.create_new_class(step, 'Client_f2f1')
    srv_control.add_test_to_class(step, '1', 'test', 'option[61].hex == 0xff010203ff04f1f2')
    srv_control.config_client_classification(step, '1', 'Client_f2f1')

    srv_control.create_new_class(step, 'Client_f2f2')
    srv_control.add_test_to_class(step, '2', 'test', 'option[61].hex == 0xff010203ff04f2f2')
    srv_control.config_client_classification(step, '2', 'Client_f2f2')

    srv_control.create_new_class(step, 'Client_f2f0')
    srv_control.add_test_to_class(step, '3', 'test', 'option[61].hex == 0xff010203ff04f2f3')
    srv_control.config_client_classification(step, '0', 'Client_f2f0')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:f1:f2')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '54', 'NOT ', 'value', '44.44.44.222')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '11.22.33.123')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:f1:f2')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.51.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '54', 'NOT ', 'value', '44.44.44.222')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '11.22.33.123')

    # File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.50.1,00:00:00:00:00:22
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:33')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:f2:f2')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.52.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '54', 'NOT ', 'value', '11.22.33.123')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '44.44.44.222')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:33')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:f2:f2')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.52.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.52.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '54', 'NOT ', 'value', '11.22.33.123')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '44.44.44.222')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:44')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:f2:f3')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '54', 'NOT ', 'value', '11.22.33.123')
    srv_msg.response_check_option_content(step, 'Response', '54', 'NOT ', 'value', '44.44.44.222')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '$(SRV4_ADDR)')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:44')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:f2:f3')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '54', 'NOT ', 'value', '11.22.33.123')
    srv_msg.response_check_option_content(step, 'Response', '54', 'NOT ', 'value', '44.44.44.222')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '$(SRV4_ADDR)')
    # File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.51.1,00:00:00:00:00:33


@pytest.mark.v4
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v4_sharednetworks_single_shared_subnet_with_three_subnets_client_classification_server_identifier_negative(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.52.0/24',
                                                       '192.168.52.1-192.168.52.1')
    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')
    srv_control.shared_subnet(step, '2', '0')

    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '0')

    srv_control.config_srv(step, 'dhcp-server-identifier', '1', '11.22.33.123')
    srv_control.config_srv(step, 'dhcp-server-identifier', '2', '44.44.44.222')

    srv_control.create_new_class(step, 'Client_f2f1')
    srv_control.add_test_to_class(step, '1', 'test', 'option[61].hex == 0xff010203ff04f1f2')
    srv_control.config_client_classification(step, '1', 'Client_f2f1')

    srv_control.create_new_class(step, 'Client_f2f2')
    srv_control.add_test_to_class(step, '2', 'test', 'option[61].hex == 0xff010203ff04f2f2')
    srv_control.config_client_classification(step, '2', 'Client_f2f2')

    srv_control.create_new_class(step, 'Client_f2f0')
    srv_control.add_test_to_class(step, '3', 'test', 'option[61].hex == 0xff010203ff04f2f3')
    srv_control.config_client_classification(step, '0', 'Client_f2f0')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:f1:f2')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '54', 'NOT ', 'value', '44.44.44.222')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '11.22.33.123')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:f1:f2')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.51.1')
    srv_msg.client_does_include_with_value(step, 'server_id', '$(SRV4_ADDR)')
    # that is weird, shouldn't it fail? those server id's dont match
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '54', 'NOT ', 'value', '44.44.44.222')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '11.22.33.123')

    # File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.50.1,00:00:00:00:00:22
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:33')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:f2:f2')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.52.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '54', 'NOT ', 'value', '11.22.33.123')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '44.44.44.222')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:33')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:f2:f2')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.52.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.52.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '54', 'NOT ', 'value', '11.22.33.123')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '44.44.44.222')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:44')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:f2:f3')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '54', 'NOT ', 'value', '11.22.33.123')
    srv_msg.response_check_option_content(step, 'Response', '54', 'NOT ', 'value', '44.44.44.222')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '$(SRV4_ADDR)')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:44')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:f2:f3')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '54')
    srv_msg.response_check_option_content(step, 'Response', '54', 'NOT ', 'value', '11.22.33.123')
    srv_msg.response_check_option_content(step, 'Response', '54', 'NOT ', 'value', '44.44.44.222')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '$(SRV4_ADDR)')
    # File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.51.1,00:00:00:00:00:33  # pylint: disable=line-too-long
