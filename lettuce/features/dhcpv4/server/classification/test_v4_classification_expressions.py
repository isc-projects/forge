"""Client Classification DHCPv4"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_msg
from features import srv_control
from features import misc


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_member(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'option[61].hex == 0xff010203ff041122')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')

    srv_control.create_new_class(step, 'Client_Class_2')
    srv_control.add_test_to_class(step, '2', 'test', 'member(\'Client_Class_1\')')
    srv_control.add_test_to_class(step, '2', 'server-hostname', 'hal9000')

    srv_control.config_client_classification(step, '0', 'Client_Class_2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:11:11:11:11:11:22')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'sname', 'hal9000')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.50')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_content(step, 'Response', None, 'sname', 'hal9000')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_unknown_pool(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '$(EMPTY)')
    srv_control.add_line_to_subnet(step,
                                   '0',
                                   ',"pools":[{"pool": "192.168.50.50-192.168.50.50","client-class": "UNKNOWN"}]')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-name',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:11:11:11:11:22')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:11:11:11:11:11:22')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.50')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:11:11:11:11:11:22')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:11:11:11:11:22')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_known_pool(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '$(EMPTY)')
    srv_control.add_line_to_subnet(step,
                                   '0',
                                   ',"pools":[{"pool": "192.168.50.55-192.168.50.55","client-class": "KNOWN"}]')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-name',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.55')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.55')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.55')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_known_unknown_pool(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '$(EMPTY)')
    srv_control.add_line_to_subnet(step,
                                   '0',
                                   ',"pools":[{"pool": "192.168.50.50-192.168.50.50","client-class": "UNKNOWN"},{"pool": "192.168.50.55-192.168.50.55","client-class": "KNOWN"}]')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-name',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:11:11:11:11:22')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:11:11:11:11:11:22')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.50')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:11:11:11:11:11:22')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:11:11:11:11:22')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.55')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.55')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.55')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_option_hex(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'option[61].hex == 0xff010203ff041122')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:11:11:11:11:11:22')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.50')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_option_exists(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'option[61].exists')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.50')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_relay_option_exists(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'relay4[3].exists')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    # command below will add option 82 with calculated length and suboption code 3, length 1, value 1.
    srv_msg.client_does_include_with_value(step, 'relay_agent_information', '311')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.50')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'relay_agent_information', '311')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_transid(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'pkt4.transid == 66')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'tr_id', '1111')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'tr_id', '66')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'tr_id', '66')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.50')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_siaddr(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'pkt4.siaddr == 1.1.1.1')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'siaddr', '192.0.0.14')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:00:01:02:03:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'siaddr', '1.1.1.1')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_yiaddr(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'pkt4.yiaddr == 1.1.1.1')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'yiaddr', '192.0.0.14')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:00:01:02:03:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'yiaddr', '1.1.1.1')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
@pytest.mark.disabled
def test_v4_client_classification_giaddr(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'pkt4.giaddr == $(GIADDR4)')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '192.0.0.14')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:00:01:02:03:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.50')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_ciaddr(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'pkt4.ciaddr == 192.0.0.1')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.0.0.14')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:00:01:02:03:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.0.0.1')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.0.0.1')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.50')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_htype(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'pkt4.htype == 6')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'htype', '4')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:00:01:02:03:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'htype', '6')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'htype', '6')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.50')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_mac(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'pkt4.mac == 0xff010203ff04')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:00:01:02:03:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.50')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_vendor(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'vendor[*].exists')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    # command below will add option 125 with calculated length enterprise number 4444
    srv_msg.client_does_include_with_value(step,
                                           'vendor_specific_information',
                                           '0000115a03010101')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.50')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step,
                                           'vendor_specific_information',
                                           '0000115a03010101')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_specific_vendor(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'vendor[4444].exists')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    # command below will add option 125 with calculated length enterprise number 4442 with suboption length 3 code 1 data 1
    srv_msg.client_does_include_with_value(step,
                                           'vendor_specific_information',
                                           '0000115a03010101')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    # command below will add option 125 with calculated length enterprise number 4444 with suboption length 3 code 1 data 1
    srv_msg.client_does_include_with_value(step,
                                           'vendor_specific_information',
                                           '0000115c03010101')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.50')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    # command below will add option 125 with calculated length enterprise number 4444 with suboption length 3 code 1 data 1
    srv_msg.client_does_include_with_value(step,
                                           'vendor_specific_information',
                                           '0000115c03010101')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_specific_vendor_2(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'vendor.enterprise == 4444')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    # command below will add option 125 with calculated length enterprise number 4442 with suboption length 3 code 1 data 1
    srv_msg.client_does_include_with_value(step,
                                           'vendor_specific_information',
                                           '0000115a03010101')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    # command below will add option 125 with calculated length enterprise number 4444 with suboption length 3 code 1 data 1
    srv_msg.client_does_include_with_value(step,
                                           'vendor_specific_information',
                                           '0000115c03010101')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.50')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    # command below will add option 125 with calculated length enterprise number 4444 with suboption length 3 code 1 data 1
    srv_msg.client_does_include_with_value(step,
                                           'vendor_specific_information',
                                           '0000115c03010101')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_vendor_suboption_exists(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'vendor[4444].option[1].exists')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    # command below will add option 125 with calculated length enterprise number 4442 with suboption length 3 code 2 data 1
    srv_msg.client_does_include_with_value(step,
                                           'vendor_specific_information',
                                           '0000115a03020101')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    # command below will add option 125 with calculated length enterprise number 4444 with suboption length 3 code 1 data 1
    srv_msg.client_does_include_with_value(step,
                                           'vendor_specific_information',
                                           '0000115c03010101')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.50')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    # command below will add option 125 with calculated length enterprise number 4444 with suboption length 3 code 1 data 1
    srv_msg.client_does_include_with_value(step,
                                           'vendor_specific_information',
                                           '0000115c03010101')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_vendor_suboption_value(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'vendor[4444].option[1].hex == 0x01')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    # command below will add option 125 with calculated length enterprise number 4442 with suboption length 3 code 1 data 2
    srv_msg.client_does_include_with_value(step,
                                           'vendor_specific_information',
                                           '0000115a03010102')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    # command below will add option 125 with calculated length enterprise number 4444 with suboption length 3 code 1 data 1
    srv_msg.client_does_include_with_value(step,
                                           'vendor_specific_information',
                                           '0000115c03010101')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.50')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    # command below will add option 125 with calculated length enterprise number 4444 with suboption length 3 code 1 data 1
    srv_msg.client_does_include_with_value(step,
                                           'vendor_specific_information',
                                           '0000115c03010101')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_vendor_class_exists(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'vendor-class[*].exists')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    # command below will add option 124 with calculated length enterprise number 4444 with suboption length 3 code 1 data 1
    srv_msg.client_does_include_with_value(step, 'vendor_class', '0000115c03010101')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.50')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    # command below will add option 124 with calculated length enterprise number 4444 with suboption length 3 code 1 data 1
    srv_msg.client_does_include_with_value(step, 'vendor_class', '0000115c03010101')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_specific_vendor_class(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'vendor-class[4444].exists')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    # command below will add option 124 with calculated length enterprise number 4442 with suboption length 3 code 1 data 1
    srv_msg.client_does_include_with_value(step, 'vendor_class', '0000115a03010101')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    # command below will add option 124 with calculated length enterprise number 4444 with suboption length 3 code 1 data 1
    srv_msg.client_does_include_with_value(step, 'vendor_class', '0000115c03010101')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.50')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    # command below will add option 124 with calculated length enterprise number 4444 with suboption length 3 code 1 data 1
    srv_msg.client_does_include_with_value(step, 'vendor_class', '0000115c03010101')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_specific_vendor_class_2(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'vendor-class.enterprise == 4444')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    # command below will add option 124 with calculated length enterprise number 4442 with suboption length 3 code 1 data 1
    srv_msg.client_does_include_with_value(step, 'vendor_class', '0000115a03010101')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    # command below will add option 124 with calculated length enterprise number 4444 with suboption length 3 code 1 data 1
    srv_msg.client_does_include_with_value(step, 'vendor_class', '0000115c03010101')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.50')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    # command below will add option 124 with calculated length enterprise number 4444 with suboption length 3 code 1 data 1
    srv_msg.client_does_include_with_value(step, 'vendor_class', '0000115c03010101')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_expressions_not_equal(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'not(vendor-class.enterprise == 5555)')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:01')
    # command below will add option 124 with calculated length enterprise number 5555 with suboption length 3 code 1 data 1
    srv_msg.client_does_include_with_value(step, 'vendor_class', '000015b303010101')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:02')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    # command below will add option 124 with calculated length enterprise number 4444 with suboption length 3 code 1 data 1
    srv_msg.client_does_include_with_value(step, 'vendor_class', '0000115c03010101')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:03')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    # command below will add option 124 with calculated length enterprise number 4442 with suboption length 3 code 1 data 1
    srv_msg.client_does_include_with_value(step, 'vendor_class', '0000115a03010101')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_expressions_and(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step,
                                  '1',
                                  'test',
                                  '(vendor.enterprise == 4444) and (vendor[4444].option[1].hex == 0x01)')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    # command below will add option 125 with calculated length enterprise number 4444 with suboption length 3 code 1 data 2
    srv_msg.client_does_include_with_value(step,
                                           'vendor_specific_information',
                                           '0000115c03010102')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    # command below will add option 125 with calculated length enterprise number 4444 with suboption length 3 code 1 data 1
    srv_msg.client_does_include_with_value(step,
                                           'vendor_specific_information',
                                           '0000115c03010101')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.50')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    # command below will add option 125 with calculated length enterprise number 4444 with suboption length 3 code 1 data 1
    srv_msg.client_does_include_with_value(step,
                                           'vendor_specific_information',
                                           '0000115c03010101')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_expressions_or(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step,
                                  '1',
                                  'test',
                                  '(vendor.enterprise == 4444) or (vendor[*].option[1].hex == 0x01)')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    # command below will add option 125 with calculated length enterprise number 4442 with suboption length 3 code 1 data 2
    srv_msg.client_does_include_with_value(step,
                                           'vendor_specific_information',
                                           '0000115a03010102')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    # command below will add option 125 with calculated length enterprise number 4442 with suboption length 3 code 1 data 1
    srv_msg.client_does_include_with_value(step,
                                           'vendor_specific_information',
                                           '0000115a03010101')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    # command below will add option 125 with calculated length enterprise number 4444 with suboption length 3 code 1 data 2
    srv_msg.client_does_include_with_value(step,
                                           'vendor_specific_information',
                                           '0000115c03010102')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.50')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    # command below will add option 125 with calculated length enterprise number 4444 with suboption length 3 code 1 data 2
    srv_msg.client_does_include_with_value(step,
                                           'vendor_specific_information',
                                           '0000115c03010102')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_expressions_substring(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step, '1', 'test', 'substring(option[61].hex,4,2) == 0x0405')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:04:05:06:22')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:44:33:55:05:11:22')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:44:33:04:05:11:22')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_expressions_concat(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step,
                                  '1',
                                  'test',
                                  'concat(substring(option[61].hex,0,1),substring(option[61].hex,7,all)) == 0xff22')
    srv_control.config_client_classification(step, '0', 'Client_Class_1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:04:05:06:22')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:44:33:55:05:11:11')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:44:33:11:22')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:04:05:06:22:00')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:44:33:66:66:11:22')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_expressions_ifelse(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')

    srv_control.create_new_class(step, 'Client_Class_1')
    srv_control.add_test_to_class(step,
                                  '1',
                                  'test',
                                  'ifelse(vendor[4444].option[1].exists, vendor[4444].option[1].hex, \'none\') == 0x01')
    # 0021 == 33
    srv_control.config_client_classification(step, '0', 'Client_Class_1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    # command below will add option 125 with calculated length enterprise number 4444 with suboption length 3 code 1 data 2
    srv_msg.client_does_include_with_value(step,
                                           'vendor_specific_information',
                                           '0000115c03010102')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    # command below will add option 125 with calculated length enterprise number 4444 with suboption length 3 code 1 data 1
    srv_msg.client_does_include_with_value(step,
                                           'vendor_specific_information',
                                           '0000115c03010101')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.50')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    # command below will add option 125 with calculated length enterprise number 4444 with suboption length 3 code 1 data 1
    srv_msg.client_does_include_with_value(step,
                                           'vendor_specific_information',
                                           '0000115c03010101')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
