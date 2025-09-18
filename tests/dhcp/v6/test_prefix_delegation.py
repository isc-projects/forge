# Copyright (C) 2022-2023 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""DHCPv6 Prefix Delegation"""

# pylint: disable=invalid-name

import pytest

from src.forge_cfg import world
from src import references
from src import misc
from src import srv_msg
from src import srv_control
from src.protosupport.multi_protocol_functions import wait_for_message_in_log


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
    srv_msg.response_check_suboption_content(26, 25, 'iaprefopts',
                                             bytes(bytearray([0, 67, 0, 2, 91, 128])))
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
    srv_control.disable_leases_affinity()
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
    # https://gitlab.isc.org/isc-projects/kea/-/issues/2698
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 91)
    # pool of two prefixes
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
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

    # Kea needs time to update leases after release due to issue kea#2698
    wait_for_message_in_log('2001:db8:1::20:0:0,00:03:00:01:ff:ff:ff:ff:ff:01,0',
                            log_file=world.f_cfg.get_leases_path())

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
    srv_control.config_srv_prefix('2001:db8::', 0, 32, 33)
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
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3, expect_include=False)
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
    srv_control.config_srv_prefix('2001:db8::', 0, 32, 33)
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
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
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
    srv_control.config_srv_prefix('2001:db8::', 0, 32, 34)
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
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8::')
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
    srv_control.config_srv_prefix('2001:db8::', 0, 32, 34)
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
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8::')
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
    srv_control.config_srv_prefix('2001:db8::', 0, 32, 33)
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
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8::')
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:8000::')
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


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_length_hints_baseline_sarr():
    """
    Doesn't test anything extraordinary. Rather servers as a baseline for the other
    test_prefix_length_hints_* tests to make sure that in absence of prefix hints, the configuration
    works correctly.
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8:0:0:1::/80')
    srv_control.config_srv_prefix('2001:db8:0:0:2::', 0, 80, 88)
    srv_control.config_srv_prefix('2001:db8:0:0:3::', 0, 80, 96)
    srv_control.config_srv_prefix('2001:db8:0:0:4::', 0, 80, 104)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.check_IA_NA('2001:db8:0:0:1::')
    srv_msg.check_IA_PD('2001:db8:0:0:2::/88')

    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.check_IA_NA('2001:db8:0:0:1::')
    srv_msg.check_IA_PD('2001:db8:0:0:2::/88')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_length_hints_sarr_with_exact_hint():
    """
    Client requests a prefix that is specifically configured as a delegated prefix in Kea.
    Kea provides the requested lease.
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8:0:0:1::/80')
    srv_control.config_srv_prefix('2001:db8:0:0:2::', 0, 80, 88)
    srv_control.config_srv_prefix('2001:db8:0:0:3::', 0, 80, 96)
    srv_control.config_srv_prefix('2001:db8:0:0:4::', 0, 80, 104)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_sets_value('Client', 'prefix', '2001:db8:0:0:3::')
    srv_msg.client_sets_value('Client', 'plen', 96)
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.check_IA_NA('2001:db8:0:0:1::')
    srv_msg.check_IA_PD('2001:db8:0:0:3::/96')

    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_sets_value('Client', 'prefix', '2001:db8:0:0:3::')
    srv_msg.client_sets_value('Client', 'plen', 96)
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.check_IA_NA('2001:db8:0:0:1::')
    srv_msg.check_IA_PD('2001:db8:0:0:3::/96')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_length_hints_sarr_with_exact_length_but_different_prefix():
    """
    Client requests a prefix that is NOT specifically configured as a delegated prefix in Kea.
    The prefix address and prefix length are part of the configuration, but in different pools.
    Kea prioritizes keeping the prefix length the same.
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8:0:0:1::/80')
    srv_control.config_srv_prefix('2001:db8:0:0:2::', 0, 80, 88)
    srv_control.config_srv_prefix('2001:db8:0:0:3::', 0, 80, 96)
    srv_control.config_srv_prefix('2001:db8:0:0:4::', 0, 80, 104)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_sets_value('Client', 'prefix', '2001:db8:0:0:2::')
    srv_msg.client_sets_value('Client', 'plen', 96)
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.check_IA_NA('2001:db8:0:0:1::')
    srv_msg.check_IA_PD('2001:db8:0:0:3::/96')

    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_sets_value('Client', 'prefix', '2001:db8:0:0:2::')
    srv_msg.client_sets_value('Client', 'plen', 96)
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    # Stubborn clients that request a different lease than advertised, get another increment in the
    # prefix from the allocation engine. Alternatively, we could have done srv_msg.client_copy_option('IA_PD')
    # in the request and have the same lease as advertised in the reply.
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.check_IA_NA('2001:db8:0:0:1::')
    srv_msg.check_IA_PD('2001:db8::3:1:0:0/96')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_length_hints_sarr_with_lowest_hint():
    """
    Client requests the prefix that has the largest address space (lowest prefix length) configured as
    a delegated prefix in Kea. Kea provides the requested lease.
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8:0:0:1::/80')
    srv_control.config_srv_prefix('2001:db8:0:0:2::', 0, 80, 88)
    srv_control.config_srv_prefix('2001:db8:0:0:3::', 0, 80, 96)
    srv_control.config_srv_prefix('2001:db8:0:0:4::', 0, 80, 104)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_sets_value('Client', 'prefix', '2001:db8:0:0:2::')
    srv_msg.client_sets_value('Client', 'plen', 88)
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.check_IA_NA('2001:db8:0:0:1::')
    srv_msg.check_IA_PD('2001:db8:0:0:2::/88')

    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_sets_value('Client', 'prefix', '2001:db8:0:0:2::')
    srv_msg.client_sets_value('Client', 'plen', 88)
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.check_IA_NA('2001:db8:0:0:1::')
    srv_msg.check_IA_PD('2001:db8:0:0:2::/88')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_length_hints_sarr_with_lower_hint():
    """
    Client requests the prefix with a prefix length that is in between the prefix lengths of
    configured pools. Kea provides the lease with the larger address space (lower prefix length).
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8:0:0:1::/80')
    srv_control.config_srv_prefix('2001:db8:0:0:2::', 0, 80, 88)
    srv_control.config_srv_prefix('2001:db8:0:0:3::', 0, 80, 96)
    srv_control.config_srv_prefix('2001:db8:0:0:4::', 0, 80, 104)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_sets_value('Client', 'prefix', '2001:db8:0:0:3::')
    srv_msg.client_sets_value('Client', 'plen', 92)
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.check_IA_NA('2001:db8:0:0:1::')
    srv_msg.check_IA_PD('2001:db8:0:0:2::/88')

    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_sets_value('Client', 'prefix', '2001:db8:0:0:3::')
    srv_msg.client_sets_value('Client', 'plen', 92)
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    # Stubborn clients that request a different lease than advertised, get another increment in the
    # prefix from the allocation engine. Alternatively, we could have done srv_msg.client_copy_option('IA_PD')
    # in the request and have the same lease as advertised in the reply.
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.check_IA_NA('2001:db8:0:0:1::')
    srv_msg.check_IA_PD('2001:db8::2:100:0:0/88')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_length_hints_sarr_with_higher_hint():
    """
    Client requests the prefix with a prefix length that is in between the prefix lengths of
    configured pools. Kea provides the lease with the larger address space (lower prefix length).
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8:0:0:1::/80')
    srv_control.config_srv_prefix('2001:db8:0:0:2::', 0, 80, 88)
    srv_control.config_srv_prefix('2001:db8:0:0:3::', 0, 80, 96)
    srv_control.config_srv_prefix('2001:db8:0:0:4::', 0, 80, 104)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_sets_value('Client', 'prefix', '2001:db8:0:0:3::')
    srv_msg.client_sets_value('Client', 'plen', 100)
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.check_IA_NA('2001:db8:0:0:1::')
    srv_msg.check_IA_PD('2001:db8:0:0:3::/96')

    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_sets_value('Client', 'prefix', '2001:db8:0:0:3::')
    srv_msg.client_sets_value('Client', 'plen', 100)
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.check_IA_NA('2001:db8:0:0:1::')
    srv_msg.check_IA_PD('2001:db8:0:0:3::/96')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_length_hints_sarr_with_highest_hint():
    """
    Client requests the prefix that has the smallest address space (highest prefix length) configured as
    a delegated prefix in Kea. Kea provides the requested lease.
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8:0:0:1::/80')
    srv_control.config_srv_prefix('2001:db8:0:0:2::', 0, 80, 88)
    srv_control.config_srv_prefix('2001:db8:0:0:3::', 0, 80, 96)
    srv_control.config_srv_prefix('2001:db8:0:0:4::', 0, 80, 104)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_sets_value('Client', 'prefix', '2001:db8:0:0:4::')
    srv_msg.client_sets_value('Client', 'plen', 104)
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.check_IA_NA('2001:db8:0:0:1::')
    srv_msg.check_IA_PD('2001:db8:0:0:4::/104')

    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_sets_value('Client', 'prefix', '2001:db8:0:0:4::')
    srv_msg.client_sets_value('Client', 'plen', 104)
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.check_IA_NA('2001:db8:0:0:1::')
    srv_msg.check_IA_PD('2001:db8:0:0:4::/104')
