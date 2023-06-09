# Copyright (C) 2022-2023 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""DHCPv4 vendor specific information"""

# pylint: disable=invalid-name
# pylint: disable=line-too-long

import binascii
import random
import socket
import string

import pytest

from src import references
from src import srv_control
from src import srv_msg
from src import misc

from src.forge_cfg import world


def _dorara(vendor_id: int, address: str, vivso_suboptions: str):
    """
    Do a DORA exchange plus another RA exchange to test the renew case.
    Expect the given IPv4 address in the yiaddr field and the given vivso suboption content.
    :param vendor_id: the vendor ID included in the client's discover
    :param address: the expected IPv4 address value for the yiaddr field
    :param vivso_suboptions: the expected content for option 125.
                             If None, it is expected that the option is not received.
    """
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', ''.join(random.choices(string.hexdigits, k=12)).lower())
    srv_msg.client_requests_option('vivso-suboptions')
    srv_msg.client_does_include_with_value('vendor_class_id', vendor_id)
    srv_msg.client_does_include_with_value('client_id', ''.join(random.choices(string.hexdigits, k=16)).lower())
    srv_msg.client_send_msg('DISCOVER')

    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', address)
    srv_msg.response_check_include_option('subnet-mask')
    srv_msg.response_check_option_content('subnet-mask', 'value', '255.255.255.0')
    if vivso_suboptions is None:
        srv_msg.response_check_include_option('vivso-suboptions', False)
    else:
        srv_msg.response_check_include_option('vivso-suboptions')
        srv_msg.response_check_option_content('vivso-suboptions', 'value', vivso_suboptions)

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', address)
    srv_msg.client_requests_option('vivso-suboptions')
    srv_msg.client_does_include_with_value('vendor_class_id', vendor_id)
    srv_msg.client_send_msg('REQUEST')

    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', address)
    srv_msg.response_check_include_option('subnet-mask')
    srv_msg.response_check_option_content('subnet-mask', 'value', '255.255.255.0')
    if vivso_suboptions is None:
        srv_msg.response_check_include_option('vivso-suboptions', False)
    else:
        srv_msg.response_check_include_option('vivso-suboptions')
        srv_msg.response_check_option_content('vivso-suboptions', 'value', vivso_suboptions)

    # Renew
    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', address)
    srv_msg.client_requests_option('vivso-suboptions')
    srv_msg.client_does_include_with_value('vendor_class_id', vendor_id)
    srv_msg.client_send_msg('REQUEST')

    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', address)
    srv_msg.response_check_include_option('subnet-mask')
    srv_msg.response_check_option_content('subnet-mask', 'value', '255.255.255.0')
    if vivso_suboptions is None:
        srv_msg.response_check_include_option('vivso-suboptions', False)
    else:
        srv_msg.response_check_include_option('vivso-suboptions')
        srv_msg.response_check_option_content('vivso-suboptions', 'value', vivso_suboptions)


def _sarrrr(vendor_id: int, address: str, vendor_option: str):
    """
    Do a SARR exchange plus another renew-reply exchange.
    Expect the given IPv4 address in the yiaddr field and the given vendor option content.
    :param vendor_id: the vendor ID included in the client's discover
    :param address: the expected IPv4 address value for the yiaddr field
    :param vendor_option: the expected content for option 17.
                          If None, it is expected that the option is not received.
    """
    duid = random.choices(string.hexdigits, k=12)
    duid = '00:03:00:01:' + ':'.join(''.join(duid[i:i+2]) for i in range(0, len(duid), 2))

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_sets_value('Client', 'ia_id', random.randrange(1, 1000000))
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_sets_value('Client', 'enterprisenum', vendor_id)
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1, 123)
    srv_msg.add_vendor_suboption('Client', 1, 124)
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.check_IA_NA(address)
    if vendor_option is None:
        srv_msg.response_check_include_option('vendor-specific-info', False)
    else:
        srv_msg.response_check_include_option('vendor-specific-info')
        srv_msg.response_check_option_content('vendor-specific-info', 'value', vendor_option)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_sets_value('Client', 'IA_Address', address)
    srv_msg.client_sets_value('Client', 'enterprisenum', vendor_id)
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1, 123)
    srv_msg.add_vendor_suboption('Client', 1, 124)
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_send_msg('REQUEST')

    # Expect a reply.
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.check_IA_NA(address)
    if vendor_option is None:
        srv_msg.response_check_include_option('vendor-specific-info', False)
    else:
        srv_msg.response_check_include_option('vendor-specific-info')
        srv_msg.response_check_option_content('vendor-specific-info', 'value', vendor_option)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_sets_value('Client', 'IA_Address', address)
    srv_msg.client_sets_value('Client', 'enterprisenum', vendor_id)
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1, 123)
    srv_msg.add_vendor_suboption('Client', 1, 124)
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_send_msg('RENEW')

    # Expect a reply.
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.check_IA_NA(address)

    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.check_IA_NA(address)
    if vendor_option is None:
        srv_msg.response_check_include_option('vendor-specific-info', False)
    else:
        srv_msg.response_check_include_option('vendor-specific-info')
        srv_msg.response_check_option_content('vendor-specific-info', 'value', vendor_option)


def _vivso_content(vendor_id: int, suboptions):
    """
    Create the hexstring content of a vivso option 125 for the given vendor ID and given suboptions.
    :param vendor_id: the vendor ID in the client's message
    :param suboptions: tuple of tuples of (suboption_code, suboption_content)
    """
    # Add all suboptions.
    hex_suboptions = ''
    for code, content in suboptions:
        length = int(len(content)/2)
        hex_suboptions += f'{code:0{2}x}{length:0{2}x}{content}'

    # Add vendor ID, length of all suboptions, suboptions.
    length = int(len(hex_suboptions)/2)
    result = f'{vendor_id:0{8}x}{length:0{2}x}{hex_suboptions}'

    return 'HEX:' + result.upper()


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
    srv_msg.response_check_option_content(125, 'value', 'HEX:000004033F823D69643A697070686F6E652E'
                                                        '6D6974656C2E636F6D3B73775F746674703D3131'
                                                        '2E31312E31312E31313B63616C6C5F7372763D31302E31302E31302E3130')


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
    srv_msg.response_check_option_content(43, 'value', 'HEX:69643A697070686F6E652E6D6974656C2E636'
                                                       'F6D3B73775F746674703D31312E31312E31312E31'
                                                       '313B63616C6C5F7372763D31302E31302E31302E3130')


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
    srv_msg.response_check_option_content(43, 'value',
                                          'HEX:02040000007B031773646C703A2F2F3139322E302E322E31313A3138343433')


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
    srv_msg.response_check_option_content(125, 'value', 'HEX:000001531F02040000007B031773646C703A2'
                                                        'F2F3139322E302E322E31313A3138343433')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.vendor
def test_v4_options_vivso_suboptions_siemens_multiple_suboptions():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')

    option = [{"name": "vlanid", "code": 2, "array": False,
               "encapsulate": "", "record-types": "",
               "space": "vendor-339", "type": "uint32"},
              {"name": "vlanid", "code": 2, "array": False,
               "encapsulate": "", "record-types": "",
               "space": "vendor-400", "type": "string"},
              {"name": "dls", "code": 3, "array": False,
               "encapsulate": "", "record-types": "",
               "space": "vendor-339", "type": "string"},
              {"name": "dls", "code": 3, "array": False,
               "encapsulate": "", "record-types": "",
               "space": "vendor-400", "type": "uint32"}]

    my_class = [{"name": "VENDOR_CLASS_339",
                 "option-data": [
                     {"name": "vivso-suboptions", "data": "339"},
                     {"always-send": True, "data": "123",
                      "name": "vlanid", "space": "vendor-339"},
                     {"always-send": True, "data": "sdlp://192.0.2.11:18443",
                      "name": "dls", "space": "vendor-339"}]},
                {"name": "VENDOR_CLASS_400",
                 "option-data": [
                     {"name": "vivso-suboptions", "data": "400"},
                     {"always-send": True, "data": "some_text",
                      "name": "vlanid", "space": "vendor-400"},
                     {"always-send": True, "data": "321",
                      "name": "dls", "space": "vendor-400"}]}]

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
    srv_msg.response_check_option_content(125, 'value', 'HEX:000001531F02040000007B031773646C70'
                                                        '3A2F2F3139322E302E322E31313A3138343433')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option(125)
    srv_msg.client_does_include_with_value('vendor_class_id', '400')
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(125)
    srv_msg.response_check_option_content(125, 'value', 'HEX:00000190110209736F6D655F74657874030400000141')


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
    srv_msg.response_check_option_content(43, 'value', 'HEX:02040000007B031773646C703A2F2F'
                                                       '3139322E302E322E31313A3138343433')


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
    srv_msg.response_check_option_content(43, 'value', 'HEX:02040000007B031773646C703A2F2F'
                                                       '3139322E302E322E31313A3138343433')


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


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.vendor
def test_multiple_v4_options_vivso_suboptions():
    """
    Check that multiple vendors can get multiple custom options.
    Harden the test so that options from different vendors have the same codes.
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.0.2.0/24', '192.0.2.10-192.0.2.250')
    world.dhcp_cfg['option-def'] = [
        {
            'code': 123,
            'name': 'my-123-option',
            'space': 'vendor-1234',
            'type': 'boolean'
        },
        {
            'code': 124,
            'name': 'my-124-option',
            'space': 'vendor-1234',
            'type': 'int32'
        },
        {
            'code': 123,
            'name': 'your-123-option',
            'space': 'vendor-5678',
            'type': 'ipv4-address'
        },
        {
            'code': 124,
            'name': 'your-124-option',
            'space': 'vendor-5678',
            'type': 'string'
        }
    ]
    world.dhcp_cfg['client-classes'] = [
        {
            'name': 'VENDOR_CLASS_1234',
            'option-data': [
                {
                    'data': '1234',
                    'name': 'vivso-suboptions'
                },
                {
                    'always-send': True,
                    'code': 123,
                    'data': '1',
                    'space': 'vendor-1234'
                },
                {
                    'always-send': True,
                    'code': 124,
                    'data': '512',
                    'space': 'vendor-1234'
                }
            ]
        },
        {
            'name': 'VENDOR_CLASS_5678',
            'option-data': [
                {
                    'data': '5678',
                    'name': 'vivso-suboptions'
                },
                {
                    'always-send': True,
                    'code': 123,
                    'data': '192.0.2.2',
                    'space': 'vendor-5678'
                },
                {
                    'always-send': True,
                    'code': 124,
                    'data': 'text',
                    'space': 'vendor-5678'
                }
            ]
        }
    ]
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _dorara(1234, '192.0.2.10', _vivso_content(1234, ((123, '01'), (124, f'{512:0{8}x}'))))
    _dorara(5678, '192.0.2.11', _vivso_content(5678,
                                               ((123, binascii.hexlify(socket.inet_aton('192.0.2.2')).decode().upper()),
                                                (124, 'text'.encode('utf-8').hex()))))
    _dorara(9999, '192.0.2.12', None)

    # Again for good measure.
    _dorara(1234, '192.0.2.13', _vivso_content(1234, ((123, '01'), (124, f'{512:0{8}x}'))))
    _dorara(5678, '192.0.2.14', _vivso_content(5678,
                                               ((123, binascii.hexlify(socket.inet_aton('192.0.2.2')).decode().upper()),
                                                (124, 'text'.encode('utf-8').hex()))))
    _dorara(9999, '192.0.2.15', None)


@pytest.mark.v6
@pytest.mark.options
@pytest.mark.vendor
def test_v6_two_vendors_two_options_each():
    """
    Check that multiple vendors can get multiple custom options.
    Harden the test so that options from different vendors have the same codes.
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::/64')
    world.dhcp_cfg['option-def'] = [
        {
            'code': 123,
            'name': 'my-123-option',
            'space': 'vendor-1234',
            'type': 'boolean'
        },
        {
            'code': 124,
            'name': 'my-124-option',
            'space': 'vendor-1234',
            'type': 'int32'
        },
        {
            'code': 123,
            'name': 'your-123-option',
            'space': 'vendor-5678',
            'type': 'ipv6-address'
        },
        {
            'code': 124,
            'name': 'your-124-option',
            'space': 'vendor-5678',
            'type': 'string'
        }
    ]
    world.dhcp_cfg['option-data'] = [
        {
            'always-send': True,
            'code': 123,
            'data': '1',
            'space': 'vendor-1234'
        },
        {
            'always-send': True,
            'code': 124,
            'data': '512',
            'space': 'vendor-1234'
        },
        {
            'always-send': True,
            'code': 123,
            'data': '2001:db8::db8:2001',
            'space': 'vendor-5678'
        },
        {
            'always-send': True,
            'code': 124,
            'data': 'text',
            'space': 'vendor-5678'
        }
    ]
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _sarrrr(1234, '2001:db8::', "<VENDOR_SPECIFIC_OPTION  optcode=123 optlen=1 optdata='01' |>,"
                                "<VENDOR_SPECIFIC_OPTION  optcode=124 optlen=4 optdata='00000200' |>")
    _sarrrr(5678, '2001:db8::1', "<VENDOR_SPECIFIC_OPTION  optcode=123 optlen=16 optdata='20010db800000000000000000db82001' |>,"
                                 "<VENDOR_SPECIFIC_OPTION  optcode=124 optlen=4 optdata='text' |>")
    _sarrrr(9999, '2001:db8::2', None)

    # Again for good measure.
    _sarrrr(1234, '2001:db8::3', "<VENDOR_SPECIFIC_OPTION  optcode=123 optlen=1 optdata='01' |>,"
                                 "<VENDOR_SPECIFIC_OPTION  optcode=124 optlen=4 optdata='00000200' |>")
    _sarrrr(5678, '2001:db8::4', "<VENDOR_SPECIFIC_OPTION  optcode=123 optlen=16 optdata='20010db800000000000000000db82001' |>,"
                                 "<VENDOR_SPECIFIC_OPTION  optcode=124 optlen=4 optdata='text' |>")
    _sarrrr(9999, '2001:db8::5', None)
