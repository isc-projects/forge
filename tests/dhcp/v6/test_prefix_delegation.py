# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""DHCPv6 Prefix Delegation"""

# pylint: disable=invalid-name

import pytest

from src import references
from src import misc
from src import srv_msg
from src import srv_control


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_onlyPD_advertise():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 96)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_IA_and_PD():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::2-3000::2')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 91)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::2')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_without_server_configuration():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 25, 'statuscode', 6)

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::3-3000::3')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 96)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:1::')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::3')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_exclude_prefix():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/48', '2001:db8:a::1-2001:db8:a::1')
    srv_control.add_line_to_subnet(0, {"pd-pools": [{"prefix": "2001:db8:1::", "prefix-len": 90,
                                                     "delegated-len": 90, "excluded-prefix": "2001:db8:1::20:0:0",
                                                     "excluded-prefix-len": 91}]})

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(67)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    # Response option 26 MUST contain sub-option 67.
    # Test works, but forge lacks support for extracting sub-options of sub-options
    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_onlyPD_request():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 92)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_IA_and_PD_request():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 92)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::1')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::1')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_onlyPD_request_release():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 91)
    # pool of two prefixes
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 25, 'statuscode', 0)
    # tests MUST NOT include 'NoBinding'...

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_onlyPD_multiple_request_release():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 91)
    srv_control.disable_leases_affinity()
    # pool of two prefixes
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 25, 'statuscode', 0)

    misc.test_procedure()
    srv_msg.generate_new('IA_PD')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)

    misc.test_procedure()
    srv_msg.generate_new('IA_PD')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    # if it fails, it means that release process fails.

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_IA_and_PD_request_release():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 91)
    # pool of two prefixes
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_include_option(3)
    # tests MUST NOT include 'NoBinding'...

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_IA_and_PD_multiple_request_release():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 91)
    # pool of two prefixes
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(13)
    # tests MUST NOT include 'NoBinding'...

    misc.test_procedure()
    srv_msg.generate_new('IA_PD')
    srv_msg.generate_new('IA')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.generate_new('IA_PD')
    srv_msg.generate_new('IA')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_noprefixavail_release():
    # assign 2 prefixes, try third, fail, release one, assign one more time with success.
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 91)
    # pool of two prefixes
    srv_control.disable_leases_affinity()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    # success

    misc.test_procedure()
    srv_msg.generate_new('IA_PD')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    # both prefixes assigned.

    misc.test_procedure()
    srv_msg.client_save_option('IA_PD')
    srv_msg.generate_new('IA_PD')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 25, 'statuscode', 6)

    misc.test_procedure()
    srv_msg.client_add_saved_option()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 25, 'statuscode', 0)

    #Kea needs time to update leases after release
    #srv_msg.forge_sleep(1)

    misc.test_procedure()
    srv_msg.generate_new('IA_PD')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_noprefixavail():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 91)
    # pool of two prefixes

    srv_msg.disable_lease_affinity()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)

    misc.test_procedure()
    srv_msg.generate_new('IA_PD')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    # both prefixes assigned.

    misc.test_procedure()
    srv_msg.generate_new('IA_PD')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 25, 'statuscode', 6)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_release_nobinding():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/32', '3000::1-3000::2')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 32, 33)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 25, 'statuscode', 3)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_release_dual_nobinding():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/32', '3000::1-3000::2')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 32, 33)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 25, 'statuscode', 3)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 3)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_release_nobinding2():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/32', '3000::1-3000::2')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 32, 33)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_save_option('IA_PD')
    srv_msg.client_add_saved_option()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    # must not contain status code == 3.

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_add_saved_option()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 25, 'statuscode', 3)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_onlyPD_relay():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 92)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_include_option(9)
    # add test after Scapy fix

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_assign_saved_iapd():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    # two prefixes - 3000::/91; 3000::20:0:0/91;
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 91)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    # 1st prefix
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)

    misc.test_procedure()
    srv_msg.generate_new('IA_PD')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_save_option('IA_PD')
    srv_msg.client_add_saved_option()
    # 2nd prefix
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    # both prefixes assigned.

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 80, 95)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_add_saved_option(erase=True)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:1::20:0:0')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.disabled
def test_prefix_delegation_compare_prefixes_after_client_reboot():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::300')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 96)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    # save prefix value
    prefix1 = srv_msg.get_suboption('IA_PD', 'IA-Prefix')[0]

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    # client reboot
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    # compare assigned prefix with the saved one
    prefix2 = srv_msg.get_suboption('IA_PD', 'IA-Prefix')[0]
    assert prefix1.prefix == prefix2.prefix

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
def test_prefix_delegation_just_PD_configured_PD_requested():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '$(EMPTY)')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 96)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_include_option(3, expect_include=False)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_include_option(3, expect_include=False)


@pytest.mark.v6
@pytest.mark.PD
def test_prefix_delegation_just_PD_configured_PD_and_IA_requested():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '$(EMPTY)')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 96)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_onlyPD_renew():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 92)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.disabled
def test_prefix_delegation_onlyPD_renew_nobinding():
    # this tests will be disabled after RFC 7550 tests will be added
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 92)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 25, 'statuscode', 3)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.disabled
def test_prefix_delegation_onlyPD_renew_nobinding_new_IA_PD():
    # this tests will be disabled after RFC 7550 tests will be added

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 92)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.generate_new('IA_PD')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 25, 'statuscode', 3)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_IA_and_PD_renew():

    # this tests will be disabled after RFC 7550 tests will be added
    misc.test_setup()
    # Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
    srv_control.config_srv_subnet('3000::/64', '3000::ffff:ffff:1-3000::ffff:ffff:3')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 92)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_save_option('IA_PD')
    srv_msg.client_add_saved_option(erase=True)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'validlft', 4000)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.disabled
def test_prefix_delegation_IA_and_PD_renew_nobindig():

    # this tests will be disabled after RFC 7550 tests will be added
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 92)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    # Response sub-option 13 from option 25 MUST contain statuscode 3. changed after rfc7550
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 3)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_rebind_success():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 92)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:1::')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_save_option('IA_PD')
    srv_msg.client_add_saved_option()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:1::')

    misc.test_procedure()
    srv_msg.client_add_saved_option()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REBIND')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    # Response option 25 MUST contain T1 . #set this after server configuration!

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.disabled
def test_prefix_delegation_rebind_fail():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 92)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_save_option('IA_PD')
    srv_msg.client_add_saved_option()
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 90)
    srv_msg.client_sets_value('Client', 'prefix', '3001::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('REBIND')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'T1', 0)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_rebind_fail_dropped():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 92)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')

    misc.test_setup()
    srv_control.config_srv_subnet('3001::/64', '3001::1-3001::ffff')
    srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 92)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REBIND')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_IA_and_PD_confirm():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::2-3000::2')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 96)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:1::')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::2')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('CONFIRM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(25, expect_include=False)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_IA_and_PD_decline():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::5')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 96)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::5')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('DECLINE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(25, expect_include=False)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.multiplePD
def test_prefix_delegation_multiple_request():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/32', '3000::5-3000::5')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 32, 34)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_save_option('IA_PD')
    srv_msg.generate_new('IA_PD')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_save_option('IA_PD')
    srv_msg.generate_new('IA_PD')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_save_option('IA_PD')
    srv_msg.generate_new('IA_PD')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_save_option('IA_PD')
    srv_msg.client_add_saved_option(erase=True)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:1::')
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:4000::')
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:8000::')
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:c000::')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.multiplePD
def test_prefix_delegation_multiple_PD_and_IA_request():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/32', '3000::1-3000::4')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 32, 34)
    # pool for 4 addresses and 4 prefix, all 8 with success

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_save_option('IA_NA')
    srv_msg.client_save_option('IA_PD')
    srv_msg.generate_new('IA')
    srv_msg.generate_new('IA_PD')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_save_option('IA_NA')
    srv_msg.client_save_option('IA_PD')
    srv_msg.generate_new('IA')
    srv_msg.generate_new('IA_PD')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_save_option('IA_NA')
    srv_msg.client_save_option('IA_PD')
    srv_msg.generate_new('IA')
    srv_msg.generate_new('IA_PD')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_save_option('IA_NA')
    srv_msg.client_save_option('IA_PD')
    srv_msg.client_add_saved_option(erase=True)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::1')
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::2')
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::3')
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::4')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:1::')
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:4000::')
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:8000::')
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:c000::')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.multiplePD
def test_prefix_delegation_multiple_PD_and_IA_request_partial_success():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/32', '3000::1-3000::2')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 32, 33)
    # pool for 2 addresses and 2 prefix, half success
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_save_option('IA_NA')
    srv_msg.client_save_option('IA_PD')
    srv_msg.generate_new('IA')
    srv_msg.generate_new('IA_PD')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_save_option('IA_NA')
    srv_msg.client_save_option('IA_PD')
    srv_msg.generate_new('IA')
    srv_msg.generate_new('IA_PD')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_save_option('IA_NA')
    srv_msg.client_save_option('IA_PD')
    srv_msg.generate_new('IA')
    srv_msg.generate_new('IA_PD')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_save_option('IA_NA')
    srv_msg.client_save_option('IA_PD')
    srv_msg.client_add_saved_option(erase=True)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::1')
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::2')
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:1::')
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:8000::')
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:8001::')
    srv_msg.response_check_suboption_content(13, 25, 'statuscode', 6)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_multiple_PD_and_IA_request_partial_fail():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::2')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 92)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_save_option('IA_NA')
    srv_msg.generate_new('IA')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_save_option('IA_NA')
    srv_msg.generate_new('IA')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_save_option('IA_NA')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_add_saved_option()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::1')
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::2')
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:1::')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_multiple_PD_and_IA_advertise_fail():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 92)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    misc.test_procedure()
    srv_msg.generate_new('IA')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)
