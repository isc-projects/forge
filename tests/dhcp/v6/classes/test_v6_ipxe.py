# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""DHCPv6 iPXE boot tests"""

# pylint: disable=invalid-name

import pytest

from src import misc
from src import srv_control
from src import srv_msg


@pytest.mark.v6
@pytest.mark.iPXE
def test_v6_IPXE_1():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '$(EMPTY)')
    srv_control.create_new_class('a-ipxe')
    srv_control.add_test_to_class(1, 'test', 'substring(option[15].hex,2,4) == \'iPXE\'')
    srv_control.add_option_to_defined_class(1,
                                            'bootfile-url',
                                            'http://[2001:db8::1]/ubuntu.cfg')
    # Server is configured with client-classification option in subnet 0 with name a-ipxe.
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'archtypes', 7)
    srv_msg.client_does_include('Client', 'client-arch-type')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_sets_value('Client', 'user_class_data', 'iPXE')
    srv_msg.client_does_include('Client', 'user-class')
    srv_msg.client_requests_option(59)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(59)
    srv_msg.response_check_option_content(59, 'optdata', 'http://[2001:db8::1]/ubuntu.cfg')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)


@pytest.mark.v6
@pytest.mark.iPXE
def test_v6_IPXE_2():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '$(EMPTY)')
    srv_control.create_new_class('a-ipxe')
    srv_control.add_test_to_class(1, 'test', 'option[61].hex == 0x0007')
    srv_control.add_option_to_defined_class(1, 'bootfile-url', 'http://[2001:db8::1]/ipxe.efi')
    # Server is configured with client-classification option in subnet 0 with name a-ipxe.
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'archtypes', 7)
    srv_msg.client_does_include('Client', 'client-arch-type')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(59)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(59)
    srv_msg.response_check_option_content(59, 'optdata', 'http://[2001:db8::1]/ipxe.efi')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)


@pytest.mark.v6
@pytest.mark.iPXE
def test_v6_IPXE_combined():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '$(EMPTY)')

    srv_control.create_new_class('a-ipxe')
    srv_control.add_test_to_class(1, 'test', 'substring(option[15].hex,2,4) == \'iPXE\'')
    srv_control.add_option_to_defined_class(1,
                                            'bootfile-url',
                                            'http://[2001:db8::1]/ubuntu.cfg')

    srv_control.create_new_class('b-ipxe')
    srv_control.add_test_to_class(2, 'test', 'option[61].hex == 0x0007')
    srv_control.add_option_to_defined_class(2, 'bootfile-url', 'http://[2001:db8::1]/ipxe.efi')

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'archtypes', 7)
    srv_msg.client_does_include('Client', 'client-arch-type')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(59)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(59)
    srv_msg.response_check_option_content(59, 'optdata', 'http://[2001:db8::1]/ipxe.efi')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'archtypes', 7)
    srv_msg.client_does_include('Client', 'client-arch-type')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_sets_value('Client', 'user_class_data', 'iPXE')
    srv_msg.client_does_include('Client', 'user-class')
    srv_msg.client_requests_option(59)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(59)
    srv_msg.response_check_option_content(59, 'optdata', 'http://[2001:db8::1]/ubuntu.cfg')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)
