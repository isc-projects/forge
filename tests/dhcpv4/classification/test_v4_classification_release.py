"""DHCPv4 Client Classification release process"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_msg
import misc
import srv_control


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
@pytest.mark.release
def test_v4_client_classification_release_same_chaddr_client_id():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_client_classification('0', 'VENDOR_CLASS_my-own-class')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content('Response', '61', None, 'value', '00010203040506')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content('Response', '61', None, 'value', '00010203040506')

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
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content('Response', '61', None, 'value', '00010203040506')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
@pytest.mark.release
def test_v4_client_classification_release_different_chaddr_client_id():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_client_classification('0', 'VENDOR_CLASS_my-own-class')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content('Response', '61', None, 'value', '00010203040506')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_does_include_with_value('vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content('Response', '61', None, 'value', '00010203040506')

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
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()
    # we should check logs here..
