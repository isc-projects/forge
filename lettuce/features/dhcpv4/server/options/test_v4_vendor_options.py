"""DHCPv4 vendor specific information"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_control
from features import srv_msg
from features import misc


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.vendor
def test_v4_options_vendor_encapsulated_space(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.config_srv_custom_opt_space(step,
                                            'vendor-encapsulated-options-space',
                                            'foo',
                                            '1',
                                            'uint16',
                                            '66')
    srv_control.config_srv_opt(step, 'vendor-encapsulated-options', '$(EMPTY)')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option(step, '43')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(step, 'Response', None, '43')
    # option 43 should have suboption code: 1 length: 2 with value 66 (hex:42)
    srv_msg.response_check_option_content(step, 'Response', '43', None, 'value', 'HEX:01020042')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.vendor
@pytest.mark.private
def test_v4_options_vendor_encapsulated_space_private_iPXE(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.config_srv_custom_opt_space(step, 'APC', 'cookie', '1', 'string', 'global-value')
    srv_control.config_srv_custom_opt_space(step,
                                            'PXE',
                                            'mtftp-ip',
                                            '1',
                                            'ipv4-address',
                                            '0.0.0.0')

    srv_control.create_new_class(step, 'APC')
    srv_control.add_test_to_class(step,
                                  '1',
                                  'test',
                                  'option[vendor-class-identifier].text == \'APC\'')
    srv_control.add_test_to_class(step,
                                  '1',
                                  'option-def',
                                  '[{"name":"vendor-encapsulated-options","code":43,"type":"empty","encapsulate":"APC"}]')
    srv_control.add_test_to_class(step,
                                  '1',
                                  'option-data',
                                  '[{"name":"cookie","space":"APC","data":"1APC"},{"name": "vendor-encapsulated-options"}]')

    srv_control.create_new_class(step, 'PXE')
    srv_control.add_test_to_class(step,
                                  '2',
                                  'test',
                                  'option[vendor-class-identifier].text == \'PXE\'')
    srv_control.add_test_to_class(step,
                                  '2',
                                  'option-def',
                                  '[{"name": "vendor-encapsulated-options","code":43,"type": "empty","encapsulate": "PXE"}]')
    srv_control.add_test_to_class(step,
                                  '2',
                                  'option-data',
                                  '[{"name": "mtftp-ip","space": "PXE","data": "1.2.3.4"},{"name": "vendor-encapsulated-options"}]')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option(step, '43')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'PXE')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '43')
    # option 43 should have suboption code: 1 length: 4 with value(v4 address) 1.2.3.4
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '43',
                                          None,
                                          'value',
                                          'HEX:010401020304')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option(step, '43')
    srv_msg.client_does_include_with_value(step, 'client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'APC')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '43')
    # option 43 should have suboption code: 1 length: 4 with value 1APC hex:31415043, entire option 43 has length 6
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '43',
                                          None,
                                          'value',
                                          'HEX:010431415043')
