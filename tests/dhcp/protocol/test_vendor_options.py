"""DHCPv4 vendor specific information"""

# pylint: disable=invalid-name,line-too-long

import pytest

from src import references
from src import srv_control
from src import srv_msg
from src import misc

from src.forge_cfg import world


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
                                  "data": "id:ipphone.mitel.com;sw_tftp=11.11.11.11;call_srv=10.10.10.10"}]}]
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


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.vendor
def test_v4_options_vivso_suboptions_siemens_defined_in_class():
    # kea gitlab #1683
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')

    option = [{"name": "vlanid", "code": 2, "array": False,
               "encapsulate": "", "record-types": "",
               "space": "vendor-339", "type": "uint32"},
              {"name": "dls", "code": 3, "array": False,
               "encapsulate": "", "record-types": "",
               "space": "vendor-339", "type": "string"}]

    my_class = [{"name": "VENDOR_CLASS_339",
                 "option-def": option,
                 "option-data": [
                     {"name": "vivso-suboptions", "data": "339"},
                     {"always-send": True, "data": "123",
                      "name": "vlanid", "space": "vendor-339"},
                     {"always-send": True, "data": "sdlp://192.0.2.11:18443",
                      "name": "dls", "space": "vendor-339"}]}]

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


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.vendor
def test_v4_options_vendor_encapsulated_siemens_defined_in_class():
    # kea gitlab #1683
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
                                 "type": "empty", "encapsulate": "339"}] + option,
                 "option-data": [{"name": "vendor-encapsulated-options"},
                                 {"always-send": True, "data": "123",
                                  "name": "vlanid", "space": "339"},
                                 {"always-send": True, "data": "sdlp://192.0.2.11:18443",
                                  "name": "dls", "space": "339"}]}]

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
def test_v4_options_vendor_encapsulated_options_space_siemens():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')

    option = [{"name": "vlanid", "code": 2, "array": False,
               "encapsulate": "", "record-types": "",
               "space": "vendor-encapsulated-options-space", "type": "uint32"},
              {"name": "dls", "code": 3, "array": False,
               "encapsulate": "", "record-types": "",
               "space": "vendor-encapsulated-options-space", "type": "string"}]

    my_class = [{"name": "VENDOR_CLASS_339",
                 "option-def": [{"name": "vendor-encapsulated-options", "code": 43,
                                 "type": "empty",
                                 "encapsulate": "vendor-encapsulated-options-space"}],
                 "option-data": [{"name": "vendor-encapsulated-options"},
                                 {"always-send": True, "data": "123", "name": "vlanid",
                                  "space": "vendor-encapsulated-options-space"},
                                 {"always-send": True, "data": "sdlp://192.0.2.11:18443", "name": "dls",
                                  "space": "vendor-encapsulated-options-space"}]}]

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
def test_v4_options_vendor_encapsulated_options_space_global_level():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')

    option_def = [{"name": "vlanid", "code": 2, "array": False,
                   "encapsulate": "", "record-types": "",
                   "space": "vendor-encapsulated-options-space", "type": "uint32"},
                  {"name": "dls", "code": 3, "array": False,
                   "encapsulate": "", "record-types": "",
                   "space": "vendor-encapsulated-options-space", "type": "string"}]

    option_data = [{"name": "vendor-encapsulated-options"},
                   {"always-send": True, "data": "123", "name": "vlanid",
                    "space": "vendor-encapsulated-options-space"},
                   {"always-send": True, "data": "sdlp://192.0.2.11:18443", "name": "dls",
                    "space": "vendor-encapsulated-options-space"}]

    world.dhcp_cfg["option-def"] = option_def
    world.dhcp_cfg["option-data"] = option_data

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
    srv_msg.response_check_option_content(43, 'value', 'HEX:02040000007B031773646C703A2F2F3139322E302E322E31313A3138343433')


@pytest.mark.disabled
@pytest.mark.v4
@pytest.mark.options
@pytest.mark.vendor
def test_v4_options_custom():
    """
    Check if v4 custom option is actually send back by Kea
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.config_srv_custom_opt('foo', 189, 'uint8', 123, always_send=True)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option(189)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(189)  # TODO this should be checked but scapy is unable to do it


@pytest.mark.v6
@pytest.mark.options
@pytest.mark.vendor
def test_v6_options_vendor_tftp_servers():
    #  Testing server ability to configure it with vendor-specific options
    #  and share it with user.
    #  In this case: for vendor id vendor-4491 set option tftp-servers with value: 2001:558::76
    #  Send vendor class and vendor specific information option (with option request).
    #  Vendor tests are beta version.
    #  with client via Advertise message.
    #  							 Client		Server
    #  vendor-class
    #  specific-info-req (32)	SOLICIT -->
    #  vendor-spec-info 				<--	ADVERTISE
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					vendor specific information (code 17) with suboption
    # 					TFTP Server address (code 32)
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/32', '3000::1-3000::2')
    srv_control.config_srv_opt_space('vendor-4491', 'tftp-servers', '2001:558::76')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1, 32)
    srv_msg.client_does_include('Client', 'vendor-specific-info')

    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(17)
    srv_msg.response_check_option_content(17, 'sub-option', 32)

    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.options
@pytest.mark.vendor
def test_v6_options_vendor_config_file():
    #  Testing server ability to configure it with vendor-specific options
    #  and share it with user.
    #  In this case: for vendor id vendor-4491 set option config-file with value normal_erouter_v6.cm.
    #  Send vendor class and vendor specific information option (with option request).
    #  Vendor tests are beta version.
    #  with client via Advertise message.
    #  							 Client		Server
    #  vendor-class
    #  specific-info-req (33)	SOLICIT -->
    #  vendor-spec-info 				<--	ADVERTISE
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					vendor specific information (code 17) with suboption
    # 					Configuration file name (code 33)
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/32', '3000::1-3000::2')
    srv_control.config_srv_opt_space('vendor-4491', 'config-file', 'normal_erouter_v6.cm')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1, 33)
    srv_msg.client_does_include('Client', 'vendor-specific-info')

    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(17)
    srv_msg.response_check_option_content(17, 'sub-option', 33)

    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.options
@pytest.mark.vendor
def test_v6_options_vendor_syslog_servers():
    #  Testing server ability to configure it with vendor-specific options
    #  and share it with user.
    #  In this case: for vendor id vendor-4491 set option syslog-servers with address 2001::101.
    #  Send vendor class and vendor specific information option (with option request).
    #  Vendor tests are beta version.
    #  with client via Advertise message.
    #  							 Client		Server
    #  vendor-class
    #  specific-info-req (34)	SOLICIT -->
    #  vendor-spec-info 				<--	ADVERTISE
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					vendor specific information (code 17) with suboption
    # 					sys log servers (code 34)
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/32', '3000::1-3000::2')
    srv_control.config_srv_opt_space('vendor-4491', 'syslog-servers', '2001::101')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1, 34)
    srv_msg.client_does_include('Client', 'vendor-specific-info')

    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(17)
    srv_msg.response_check_option_content(17, 'sub-option', 34)

    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.options
@pytest.mark.vendor
def test_v6_options_vendor_time_servers():
    #  Testing server ability to configure it with vendor-specific options
    #  and share it with user.
    #  In this case: for vendor id vendor-4491 set option time-servers option with value 2001::76.
    #  Send vendor class and vendor specific information option (with option request).
    #  Vendor tests are beta version.
    #  with client via Advertise message.
    #  							 Client		Server
    #  vendor-class
    #  specific-info-req (37)	SOLICIT -->
    #  vendor-spec-info 				<--	ADVERTISE
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					vendor specific information (code 17) with suboption
    # 					time protocol servers (code 37)

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/32', '3000::1-3000::2')
    srv_control.config_srv_opt_space('vendor-4491', 'time-servers', '2001::76')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1, 37)
    srv_msg.client_does_include('Client', 'vendor-specific-info')

    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(17)
    srv_msg.response_check_option_content(17, 'sub-option', 37)

    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.options
@pytest.mark.vendor
def test_v6_options_vendor_time_offset():
    #  Testing server ability to configure it with vendor-specific options
    #  and share it with user.
    #  In this case: for vendor id vendor-4491 set option time-offset with value -18000
    #  Send vendor class and vendor specific information option (with option request).
    #  Vendor tests are beta version.
    #  with client via Advertise message.
    #  							 Client		Server
    #  vendor-class
    #  specific-info-req (38)	SOLICIT -->
    #  vendor-spec-info 				<--	ADVERTISE
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					vendor specific information (code 17) with suboption
    # 					time offset (code 38)
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/32', '3000::1-3000::2')
    srv_control.config_srv_opt_space('vendor-4491', 'time-offset', '-18000')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1, 38)
    srv_msg.client_does_include('Client', 'vendor-specific-info')

    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(17)
    srv_msg.response_check_option_content(17, 'sub-option', 38)

    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.options
@pytest.mark.vendor
def test_v6_options_vendor_multiple():
    #  Testing server ability to configure it with vendor-specific options
    #  and share it with user.
    #  In this case: for vendor id vendor-4491 set option time-offset with value -18000
    #  and for vendor id vendor-4491 set option tftp-servers with value: 2001:558:ff18:16:10:253:175:76
    #  and for vendor id vendor-4491 set option config-file with value normal_erouter_v6.cm
    #  and for vendor id vendor-4491 set option syslog-servers with address 2001:558:ff18:10:10:253:124:101
    #  and for vendor id vendor-4491 set option time-servers option with value 2001:558:ff18:16:10:253:175:76
    #  and for vendor id vendor-4491 set option time-offset with value -10000
    #  Send vendor class and vendor specific information option (with option request).
    #  Vendor tests are beta version.
    #  with client via Advertise message.
    #  							 Client		Server
    #  vendor-class
    #  specific-info-req (all codes)SOLICIT -->
    #  vendor-spec-info 				<--	ADVERTISE
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					vendor specific information (code 17) with suboption
    # 					TFTP Server address (code 32)
    # 					Configuration file name (code 33)
    # 					sys log servers (code 34)
    # 					time offset (code 38)
    # 					time protocol servers (code 37)

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/32', '3000::1-3000::2')
    srv_control.config_srv_opt_space('vendor-4491',
                                     'tftp-servers',
                                     '2001:558:ff18:16:10:253:175:76')
    srv_control.config_srv_opt_space('vendor-4491', 'config-file', 'normal_erouter_v6.cm')
    srv_control.config_srv_opt_space('vendor-4491',
                                     'syslog-servers',
                                     '2001:558:ff18:10:10:253:124:101')
    srv_control.config_srv_opt_space('vendor-4491',
                                     'time-servers',
                                     '2001:558:ff18:16:10:253:175:76')
    srv_control.config_srv_opt_space('vendor-4491', 'time-offset', '-10000')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1, 32)
    srv_msg.add_vendor_suboption('Client', 1, 33)
    srv_msg.add_vendor_suboption('Client', 1, 34)
    srv_msg.add_vendor_suboption('Client', 1, 37)
    srv_msg.add_vendor_suboption('Client', 1, 38)
    srv_msg.client_does_include('Client', 'vendor-specific-info')

    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(17)
    srv_msg.response_check_option_content(17, 'sub-option', 32)
    srv_msg.response_check_option_content(17, 'sub-option', 33)
    srv_msg.response_check_option_content(17, 'sub-option', 34)
    srv_msg.response_check_option_content(17, 'sub-option', 37)
    srv_msg.response_check_option_content(17, 'sub-option', 38)

    references.references_check('RFC3315')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.vendor
def test_v4_option_125_encapsulated():
    """
    Test checking for specific bug in Kea #1585.
    Configuration specifies custom class that return option 43 with encapsulated option 125.
    """

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')

    option = [{"name": "cookie", "code": 125, "type": "string", "space": "ABC"}]

    my_class = [{"name": "ABC",
                 "test": "(option[vendor-class-identifier].text == 'ABC')",
                 "option-def": [{"name": "vendor-encapsulated-options", "code": 43,
                                 "type": "empty",
                                 "encapsulate": "ABC"}],
                 "option-data": [{"name": "cookie", "space": "ABC", "data": "1ABCDE"},
                                 {"name": "vendor-encapsulated-options"}]
                 }]

    world.dhcp_cfg["option-def"] = option
    world.dhcp_cfg["client-classes"] = my_class

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option(43)
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    # Include vendor-class-identifier to trigger class selection
    srv_msg.client_does_include_with_value('vendor_class_id', 'ABC')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(43)
    # Check if option 43 contains sub-option 125 with value "1ABCDE"
    # (HEX(7D) = 125, 06 - length, HEX(314142434445)="1ABCDE")
    srv_msg.response_check_option_content(43, 'value', 'HEX:7D06314142434445')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.50')
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option(43)
    # Include vendor-class-identifier to trigger class selection
    srv_msg.client_does_include_with_value('vendor_class_id', 'ABC')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(43)
    # Check if option 43 contains sub-option 125 with value "1ABCDE"
    # (HEX(7D) = 125, 06 - length, HEX(314142434445)="1ABCDE")
    srv_msg.response_check_option_content(43, 'value', 'HEX:7D06314142434445')

    srv_msg.check_leases({'address': '192.168.50.50'})
