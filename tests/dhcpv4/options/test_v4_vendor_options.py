"""DHCPv4 vendor specific information"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_control
import srv_msg
import misc

from forge_cfg import world

@pytest.mark.v4
@pytest.mark.options
@pytest.mark.vendor
def test_v4_options_vendor_encapsulated_space():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.config_srv_custom_opt_space('vendor-encapsulated-options-space',
                                            'foo',
                                            1,
                                            'uint16',
                                            66)
    srv_control.config_srv_opt('vendor-encapsulated-options', '$(EMPTY)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option(43)
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(43)
    # option 43 should have suboption code: 1 length: 2 with value 66 (hex:42)
    srv_msg.response_check_option_content(43, 'value', 'HEX:01020042')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.vendor
@pytest.mark.private
def test_v4_options_vendor_encapsulated_space_private_iPXE():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.config_srv_custom_opt_space('APC', 'cookie', 1, 'string', 'global-value')
    srv_control.config_srv_custom_opt_space('PXE', 'mtftp-ip', 1, 'ipv4-address', '0.0.0.0')

    srv_control.create_new_class('APC')
    srv_control.add_test_to_class(1, 'test', 'option[vendor-class-identifier].text == \'APC\'')
    srv_control.add_test_to_class(1,
                                  'option-def',
                                  {"name": "vendor-encapsulated-options", "code": 43,
                                   "type": "empty", "encapsulate": "APC"})
    srv_control.add_test_to_class(1,
                                  'option-data',
                                  {"name": "cookie", "space": "APC", "data": "1APC"})
    srv_control.add_test_to_class(1,
                                  'option-data',
                                  {"name": "vendor-encapsulated-options"})

    srv_control.create_new_class('PXE')
    srv_control.add_test_to_class(2, 'test', 'option[vendor-class-identifier].text == \'PXE\'')
    srv_control.add_test_to_class(2,
                                  'option-def',
                                  {"name": "vendor-encapsulated-options", "code": 43,
                                   "type": "empty", "encapsulate": "PXE"})
    srv_control.add_test_to_class(2,
                                  'option-data',
                                  {"name": "mtftp-ip", "space": "PXE", "data": "1.2.3.4"})
    srv_control.add_test_to_class(2,
                                  'option-data',
                                  {"name": "vendor-encapsulated-options"})

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option(43)
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_does_include_with_value('vendor_class_id', 'PXE')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(43)
    # option 43 should have suboption code: 1 length: 4 with value(v4 address) 1.2.3.4
    srv_msg.response_check_option_content(43, 'value', 'HEX:010401020304')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option(43)
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_does_include_with_value('vendor_class_id', 'APC')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(43)
    # option 43 should have suboption code: 1 length: 4 with value 1APC hex:31415043, entire option 43 has length 6
    srv_msg.response_check_option_content(43, 'value', 'HEX:010431415043')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.vendor
def test_v4_options_vivso_suboptions_mitel():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')

    option = [{"array": False, "code": 130, "encapsulate": "", "name": "mitel-option",
              "record-types": "", "space": "vendor-1027", "type": "string"}]

    my_class = [{"name": "VENDOR_CLASS_1027",
                 "option-data": [{"name": "vivso-suboptions", "data": "1027"},
                                 {"name": "mitel-option", "space": "vendor-1027",
                                  "data": "id:ipphone.mitel.com;sw_tftp=11.11.11.11;call_srv=10.10.10.10",
                                  "always-send": True}]}]

    world.dhcp_cfg["option-def"] = option
    world.dhcp_cfg["client-classes"] = my_class

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option(125)
    srv_msg.client_does_include_with_value('vendor_class_id', '1027')
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(125)
    srv_msg.response_check_option_content(125, 'value', 'HEX:000004033F823D69643A697070686F6E652E6D6974656C2E636F6D3B73775F746674703D31312E31312E31312E31313B63616C6C5F7372763D31302E31302E31302E3130')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.vendor
def test_v4_options_vendor_encapsulated_mitel():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')

    my_class = [{"name": "VENDOR_CLASS_1027",
                 "option-def": [{"name": "vendor-encapsulated-options",
                                 "code": 43, "type": "string"}],
                 "option-data": [{"name": "vendor-encapsulated-options",
                                  "data": "id:ipphone.mitel.com;sw_tftp=11.11.11.11;call_srv=10.10.10.10"}]
                 }]
    world.dhcp_cfg["client-classes"] = my_class

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option(43)
    srv_msg.client_does_include_with_value('vendor_class_id', '1027')
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(43)
    srv_msg.response_check_option_content(43, 'value', 'HEX:69643A697070686F6E652E6D6974656C2E636F6D3B73775F746674703D31312E31312E31312E31313B63616C6C5F7372763D31302E31302E31302E3130')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.vendor
def test_v4_options_vendor_encapsulated_unifi_address():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')

    my_class = [{"name": "VENDOR_CLASS_ubnt",
                 "option-def": [{"name": "vendor-encapsulated-options",
                                 "type": "ipv4-address", "code": 43}],
                 "option-data": [{"name": "vendor-encapsulated-options",
                                  "data": "192.0.2.11"}]}]

    world.dhcp_cfg["client-classes"] = my_class

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option(43)
    srv_msg.client_does_include_with_value('vendor_class_id', 'ubnt')
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(43)
    srv_msg.response_check_option_content(43, 'value', 'HEX:C000020B')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.vendor
def test_v4_options_vivso_suboptions_unifi_address():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')

    option = [{"name": "unifi-address", "code": 1, "array": False,
               "space": "vendor-41112", "type": "ipv4-address"}]

    my_class = [{"name": "VENDOR_CLASS_41112",
                 "option-data": [
                     {"name": "vivso-suboptions", "data": "41112"},
                     {"name": "unifi-address", "space": "vendor-41112",
                      "data": "192.0.2.11", "always-send": True}]}]

    world.dhcp_cfg["option-def"] = option
    world.dhcp_cfg["client-classes"] = my_class

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option(125)
    srv_msg.client_does_include_with_value('vendor_class_id', '41112')
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(125)
    srv_msg.response_check_option_content(125, 'value', 'HEX:0000A098060104C000020B')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.vendor
def test_v4_options_vendor_encapsulated_siemens():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')

    option = [{"name": "vlanid", "code": 2, "array": False,
               "encapsulate": "", "record-types": "",
               "space": "339", "type": "uint32"},
              {"name": "dls", "code": 3, "array": False,
               "encapsulate": "", "record-types": "",
               "space": "339", "type": "string"}]

    my_class = [{"name": "VENDOR_CLASS_339",
                 "option-def": [{"name": "vendor-encapsulated-options", "code": 43,
                                 "type": "empty", "encapsulate": "339"}],
                 "option-data": [{"name": "vendor-encapsulated-options"},
                                 {"always-send": True, "data": "123",
                                  "name": "vlanid", "space": "339"},
                                 {"always-send": True, "data": "sdlp://192.0.2.11:18443",
                                  "name": "dls", "space": "339"}]}]
    world.dhcp_cfg["option-def"] = option
    world.dhcp_cfg["client-classes"] = my_class

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option(43)
    srv_msg.client_does_include_with_value('vendor_class_id', '339')
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(43)
    srv_msg.response_check_option_content(43, 'value', 'HEX:02040000007B031773646C703A2F2F3139322E302E322E31313A3138343433')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.vendor
def test_v4_options_vivso_suboptions_siemens():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')

    option = [{"name": "vlanid", "code": 2, "array": False,
               "encapsulate": "", "record-types": "",
               "space": "vendor-339", "type": "uint32"},
              {"name": "dls", "code": 3, "array": False,
               "encapsulate": "", "record-types": "",
               "space": "vendor-339", "type": "string"}]

    my_class = [{"name": "VENDOR_CLASS_339",
                 "option-data": [
                     {"name": "vivso-suboptions", "data": "339"},
                     {"always-send": True, "data": "123",
                      "name": "vlanid", "space": "vendor-339"},
                     {"always-send": True, "data": "sdlp://192.0.2.11:18443",
                      "name": "dls", "space": "vendor-339"}]}]

    world.dhcp_cfg["option-def"] = option
    world.dhcp_cfg["client-classes"] = my_class

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option(125)
    srv_msg.client_does_include_with_value('vendor_class_id', '339')
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(125)
    srv_msg.response_check_option_content(125, 'value', 'HEX:000001531F02040000007B031773646C703A2F2F3139322E302E322E31313A3138343433')