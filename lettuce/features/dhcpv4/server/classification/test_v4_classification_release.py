"""DHCPv4 Client Classification release process"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_msg
from features import srv_control
from features import misc


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
@pytest.mark.release
def test_v4_client_classification_release_same_chaddr_client_id(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_client_classification(step, '0', 'VENDOR_CLASS_my-own-class')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040506')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '00010203040506')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040506')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '00010203040506')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040506')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:11:22:33')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040506')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '00010203040506')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
@pytest.mark.release
def test_v4_client_classification_release_different_chaddr_client_id(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_client_classification(step, '0', 'VENDOR_CLASS_my-own-class')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040506')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '00010203040506')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040506')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(step, 'Response', '54', None, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '00010203040506')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:11:22:33')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203123456')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:11:22:33')
    # Client adds to the message client_id with value 00010203040506.
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'my-own-class')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)
    # we should check logs here..
