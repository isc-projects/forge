"""DHCPv4 Client Classification - default classes"""

# pylint: disable=invalid-name,line-too-long

import pytest

from src import misc
from src import srv_control
from src import srv_msg


@pytest.mark.v4
@pytest.mark.classification
@pytest.mark.default_classes
@pytest.mark.disabled
def test_v4_classification_one_class_docsis3_boot_file_name():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_client_classification(0, 'VENDOR_CLASS_docsis3.0')
    srv_control.config_srv_another_subnet_no_interface('192.168.50.0/24',
                                                       '192.168.50.100-192.168.50.100')
    srv_control.config_srv('boot-file-name', 0, 'somefilename')
    srv_control.config_srv_opt('boot-file-name', 'someotherfilename')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('file', 'somefilename')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_content('file', 'someotherfilename', expected=False)
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')


@pytest.mark.v4
@pytest.mark.classification
@pytest.mark.default_classes
@pytest.mark.disabled
def test_v4_classification_one_class_docsis3_next_server():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_client_classification(0, 'VENDOR_CLASS_docsis3.0')
    srv_control.config_srv_another_subnet_no_interface('192.168.50.0/24',
                                                       '192.168.50.100-192.168.50.100')
    srv_control.config_srv('boot-file-name', 0, 'somefilename')
    srv_control.subnet_add_siaddr(0, '192.0.2.234')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('file', 'somefilename')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_content('siaddr', '192.0.2.234')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')


@pytest.mark.v4
@pytest.mark.classification
@pytest.mark.default_classes
@pytest.mark.disabled
def test_v4_classification_one_class_eRouter1_global_next_server():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_client_classification(0, 'VENDOR_CLASS_eRouter1.0')
    srv_control.config_srv_another_subnet_no_interface('192.168.50.0/24',
                                                       '192.168.50.100-192.168.50.100')
    srv_control.config_srv('boot-file-name', 0, 'somefilename')
    srv_control.global_add_siaddr('192.0.2.2')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_does_include_with_value('vendor_class_id', 'eRouter1.0')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('file', 'somefilename', expected=False)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_content('siaddr', '0.0.0.0')
    srv_msg.response_check_content('siaddr', '192.0.2.2', expected=False)

    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')


@pytest.mark.v4
@pytest.mark.classification
@pytest.mark.default_classes
@pytest.mark.disabled
def test_v4_classification_one_class_eRouter1_subnet_next_server():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_client_classification(0, 'VENDOR_CLASS_eRouter1.0')
    srv_control.config_srv_another_subnet_no_interface('192.168.50.0/24',
                                                       '192.168.50.100-192.168.50.100')
    srv_control.config_srv('boot-file-name', 0, 'somefilename')
    srv_control.subnet_add_siaddr(0, '192.0.2.234')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_does_include_with_value('vendor_class_id', 'eRouter1.0')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('file', 'somefilename', expected=False)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_content('siaddr', '0.0.0.0')
    srv_msg.response_check_content('siaddr', '192.0.2.234', expected=False)

    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')


@pytest.mark.v4
@pytest.mark.classification
@pytest.mark.default_classes
@pytest.mark.disabled
def test_v4_classification_one_class_eRouter1_two_next_servers():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_client_classification(0, 'VENDOR_CLASS_eRouter1.0')
    srv_control.config_srv_another_subnet_no_interface('192.168.50.0/24',
                                                       '192.168.50.100-192.168.50.100')
    srv_control.config_srv('boot-file-name', 0, 'somefilename')
    srv_control.global_add_siaddr('192.0.2.2')
    srv_control.subnet_add_siaddr(0, '192.0.2.234')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_does_include_with_value('vendor_class_id', 'eRouter1.0')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('file', 'somefilename', expected=False)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_content('siaddr', '0.0.0.0')
    srv_msg.response_check_content('siaddr', '192.0.2.234', expected=False)
    srv_msg.response_check_content('siaddr', '192.0.2.2', expected=False)
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')


@pytest.mark.v4
@pytest.mark.classification
@pytest.mark.default_classes
@pytest.mark.disabled
def test_v4_classification_multiple_classes_three_subnets_docsis_erouter():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_client_classification(0, 'VENDOR_CLASS_eRouter1.0')
    srv_control.subnet_add_siaddr(0, '192.0.50.1')
    srv_control.config_srv('boot-file-name', 0, 'filename')

    srv_control.config_srv_another_subnet_no_interface('192.168.50.0/24',
                                                       '192.168.50.50-192.168.50.50')
    srv_control.config_client_classification(1, 'VENDOR_CLASS_docsis3.0')
    srv_control.subnet_add_siaddr(1, '192.0.50.50')
    srv_control.config_srv('boot-file-name', 1, 'somefilename')

    srv_control.config_srv_another_subnet_no_interface('192.168.50.0/24',
                                                       '192.168.50.100-192.168.50.100')
    srv_control.global_add_siaddr('192.0.50.100')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_does_include_with_value('vendor_class_id', 'eRouter1.0')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('siaddr', '192.0.50.1', expected=False)
    srv_msg.response_check_content('siaddr', '192.0.50.50', expected=False)
    srv_msg.response_check_content('siaddr', '192.0.50.100', expected=False)
    srv_msg.response_check_content('file', 'somefilename', expected=False)
    srv_msg.response_check_content('file', 'filename', expected=False)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_content('siaddr', '0.0.0.0')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')

    srv_msg.response_check_content('siaddr', '192.0.50.1', expected=False)
    srv_msg.response_check_content('siaddr', '192.0.50.100', expected=False)
    srv_msg.response_check_content('siaddr', '0.0.0.0', expected=False)
    srv_msg.response_check_content('file', 'filename', expected=False)

    srv_msg.response_check_content('siaddr', '192.0.50.50')
    srv_msg.response_check_content('file', 'somefilename')
    srv_msg.response_check_content('yiaddr', '192.168.50.50')

    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
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
    srv_msg.response_check_content('siaddr', '192.0.50.1', expected=False)
    srv_msg.response_check_content('siaddr', '192.0.50.50', expected=False)
    srv_msg.response_check_content('siaddr', '0.0.0.0', expected=False)
    srv_msg.response_check_content('file', 'filename', expected=False)
    srv_msg.response_check_content('file', 'somefilename', expected=False)

    srv_msg.response_check_content('yiaddr', '192.168.50.100')
    srv_msg.response_check_content('siaddr', '192.0.50.100')

    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')
