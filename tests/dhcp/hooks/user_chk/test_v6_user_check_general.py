# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea6 User Check Hook Library"""

# pylint: disable=invalid-name

import glob
import pytest

from src import misc
from src import srv_control
from src import srv_msg


@pytest.mark.v6
@pytest.mark.user_check
@pytest.mark.IA_NA
def test_user_check_hook_IA_NA_no_registry():
    # Without a user registry and multiple subnets
    # Subnet selection will use subnet interface for subnet selection hint

    misc.test_setup()
    srv_msg.remove_file_from_server('/tmp/user_chk_registry.txt')
    srv_msg.remove_file_from_server('/tmp/user_chk_outcome.txt')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::5')
    srv_control.config_srv_another_subnet_no_interface('1000::/64', '1000::5-1000::5')
    srv_control.add_hooks('libdhcp_user_chk.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started', should_succeed=False)


@pytest.mark.v6
@pytest.mark.user_check
@pytest.mark.IA_NA
def test_user_check_hook_IA_NA_with_registry_unknown_user():
    # With a user registry and multiple subnets
    # an unknown user should get last subnet

    misc.test_setup()
    srv_msg.send_file_to_server(glob.glob("**/v6_registry_1.txt", recursive=True)[0],
                                '/tmp/user_chk_registry.txt')
    srv_msg.remove_file_from_server('/tmp/user_chk_outcome.txt')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::5')
    srv_control.config_srv_another_subnet_no_interface('1000::/64', '1000::5-1000::5')
    srv_control.add_hooks('libdhcp_user_chk.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    # Send a query from an unregistered user
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '1000::5')
    # Check the outcome file for correct content
    srv_msg.copy_remote('/tmp/user_chk_outcome.txt')
    srv_msg.compare_file(glob.glob("**/v6_outcome_1.txt", recursive=True)[0])


@pytest.mark.v6
@pytest.mark.user_check
@pytest.mark.IA_NA
def test_user_check_hook_IA_NA_with_registry_known_user():
    # With a user registry and multiple subnets
    # an known user should get first subnet

    misc.test_setup()
    srv_msg.send_file_to_server(glob.glob("**/v6_registry_1.txt", recursive=True)[0],
                                '/tmp/user_chk_registry.txt')
    srv_msg.remove_file_from_server('/tmp/user_chk_outcome.txt')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::5')
    srv_control.config_srv_another_subnet_no_interface('1000::/64', '1000::5-1000::5')
    srv_control.add_hooks('libdhcp_user_chk.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    # Send a query from a registered user
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:11:02:03:04:05:06')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '3000::5')
    # Check the outcome file for correct content
    srv_msg.copy_remote('/tmp/user_chk_outcome.txt')
    srv_msg.compare_file(glob.glob("**/v6_outcome_2.txt", recursive=True)[0])
