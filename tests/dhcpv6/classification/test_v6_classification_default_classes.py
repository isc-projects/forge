"""DHCPv6 Client Classification - default classes"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_msg
import srv_control


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.classification
@pytest.mark.default_classes
def test_v6_client_classification_onesubnet_docsis3_advertise_success():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.config_client_classification('0', 'VENDOR_CLASS_docsis3.0')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'vendor_class_data', 'docsis3.0')
    srv_msg.client_does_include('Client', None, 'vendor-class')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.classification
@pytest.mark.default_classes
def test_v6_client_classification_onesubnet_docsis3_advertise_fail():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.config_client_classification('0', 'VENDOR_CLASS_docsis3.0')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content('Response', '13', '3', None, 'statuscode', '2')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.classification
@pytest.mark.default_classes
def test_v6_client_classification_onesubnet_docsis3_request_success():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.config_client_classification('0', 'VENDOR_CLASS_docsis3.0')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'vendor_class_data', 'docsis3.0')
    srv_msg.client_does_include('Client', None, 'vendor-class')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'vendor_class_data', 'docsis3.0')
    srv_msg.client_does_include('Client', None, 'vendor-class')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.classification
@pytest.mark.default_classes
def test_v6_client_classification_onesubnet_docsis3_request_fail():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.config_client_classification('0', 'VENDOR_CLASS_docsis3.0')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.client_sets_value('Client', 'vendor_class_data', 'docsis3.0')
    srv_msg.client_does_include('Client', None, 'vendor-class')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content('Response', '13', '3', None, 'statuscode', '2')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.classification
@pytest.mark.default_classes
def test_v6_client_classification_onesubnet_eRouter1_0_advertise_success():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.config_client_classification('0', 'VENDOR_CLASS_eRouter1.0')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'vendor_class_data', 'eRouter1.0')
    srv_msg.client_does_include('Client', None, 'vendor-class')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.classification
@pytest.mark.default_classes
def test_v6_client_classification_onesubnet_eRouter1_0_advertise_fail():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.config_client_classification('0', 'VENDOR_CLASS_eRouter1.0')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content('Response', '13', '3', None, 'statuscode', '2')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.classification
@pytest.mark.default_classes
def test_v6_client_classification_onesubnet_eRouter1_0_request_success():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.config_client_classification('0', 'VENDOR_CLASS_eRouter1.0')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'vendor_class_data', 'eRouter1.0')
    srv_msg.client_does_include('Client', None, 'vendor-class')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'vendor_class_data', 'eRouter1.0')
    srv_msg.client_does_include('Client', None, 'vendor-class')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.classification
@pytest.mark.default_classes
def test_v6_client_classification_onesubnet_eRouter1_0_request_fail():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.config_client_classification('0', 'VENDOR_CLASS_eRouter1.0')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.client_sets_value('Client', 'vendor_class_data', 'eRouter1.0')
    srv_msg.client_does_include('Client', None, 'vendor-class')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content('Response', '13', '3', None, 'statuscode', '2')
