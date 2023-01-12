# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea4 User Check Hook Library - Logging"""

# pylint: disable=line-too-long

import glob
import pytest

from src import misc
from src import srv_control
from src import srv_msg

from src.protosupport.multi_protocol_functions import log_contains


@pytest.mark.v4
@pytest.mark.user_check
def test_user_check_hook_no_registry_logging():
    # Without a user registry and multiple subnets
    # Subnet selection will use subnet interface for subnet selection hint

    misc.test_setup()
    srv_msg.remove_file_from_server('/tmp/user_chk_registry.txt')
    srv_msg.remove_file_from_server('/tmp/user_chk_outcome.txt')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.config_srv_another_subnet_no_interface('10.0.0.0/24', '10.0.0.5-10.0.0.5')
    srv_control.add_hooks('libdhcp_user_chk.so')
    srv_control.configure_loggers('kea-dhcp4.callouts', 'ERROR', 'None')
    srv_control.configure_loggers('kea-dhcp4.hooks', 'ERROR', 'None')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started', should_succeed=False)

    # DHCP server is started.
    #
    # Test Procedure:
    # Client requests option 1.
    # Client sends DISCOVER message.
    #
    # Pass Criteria:
    # Server MUST respond with OFFER message.
    # Response MUST include option 1.
    # Response MUST contain yiaddr 192.168.50.5.
    # Response option 1 MUST contain value 255.255.255.0.
    #
    # Test Procedure:
    # Client copies server_id option from received message.
    # Client adds to the message requested_addr with value 192.168.50.5.
    # Client requests option 1.
    # Client sends REQUEST message.
    #
    # Pass Criteria:
    # Server MUST respond with ACK message.
    # Client download file from server stored in: /tmp/user_chk_outcome.txt.
    # Client download file from server stored in: /tmp/user_chk_registry.txt.
    # File stored in kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp4\.hooks
    # File stored in kea.log MUST contain line or phrase: ERROR \[kea-dhcp4\.hooks
    # File stored in kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp4\.callouts


@pytest.mark.v4
@pytest.mark.user_check
def test_user_check_hook_with_registry_unknown_user_logging():
    # With a user registry and multiple subnets
    # an unknown user should get last subnet

    misc.test_setup()
    srv_msg.send_file_to_server(glob.glob("**/v4_registry_1.txt", recursive=True)[0],
                                '/tmp/user_chk_registry.txt')
    srv_msg.remove_file_from_server('/tmp/user_chk_outcome.txt')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.config_srv_another_subnet_no_interface('10.0.0.0/24', '10.0.0.5-10.0.0.5')
    srv_control.add_hooks('libdhcp_user_chk.so')
    srv_control.configure_loggers('kea-dhcp4.callouts', 'DEBUG', 99)
    srv_control.configure_loggers('kea-dhcp4.hooks', 'INFO', 'None')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    # Send a query from an unregistered user
    srv_msg.client_sets_value('Client', 'chaddr', '0c:0e:0a:01:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '10.0.0.5')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    # Check the outcome file for correct content
    srv_msg.copy_remote('/tmp/user_chk_outcome.txt')
    srv_msg.compare_file(glob.glob("**/v4_outcome_1.txt", recursive=True)[0],)
    log_contains(r'INFO  \[kea-dhcp4\.hooks')
    log_contains(r'DEBUG \[kea-dhcp4\.callouts')


@pytest.mark.v4
@pytest.mark.user_check
def test_user_check_hook_with_registry_unknown_user_logging_2():
    # With a user registry and multiple subnets
    # an unknown user should get last subnet

    misc.test_setup()
    srv_msg.send_file_to_server(glob.glob("**/v4_registry_1.txt", recursive=True)[0],
                                '/tmp/user_chk_registry.txt')
    srv_msg.remove_file_from_server('/tmp/user_chk_outcome.txt')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.config_srv_another_subnet_no_interface('10.0.0.0/24', '10.0.0.5-10.0.0.5')
    srv_control.add_hooks('libdhcp_user_chk.so')
    # Server logging system is configured with logger type kea-dhcp4.callouts, severity DEBUG, severity level 99 and log file kea.log.
    # Server logging system is configured with logger type kea-dhcp4.hooks, severity INFO, severity level None and log file kea.log.
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', '0c:0e:0a:01:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '10.0.0.5')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    # Check the outcome file for correct content
    srv_msg.copy_remote('/tmp/user_chk_outcome.txt')
    srv_msg.compare_file(glob.glob("**/v4_outcome_1.txt", recursive=True)[0])
    # File stored in kea.log MUST contain line or phrase: INFO  \[kea-dhcp4\.hooks
    # File stored in kea.log MUST contain line or phrase: DEBUG \[kea-dhcp4\.callouts

    misc.test_setup()
    srv_msg.send_file_to_server(glob.glob("**/v4_registry_1.txt", recursive=True)[0],
                                '/tmp/user_chk_registry.txt')
    srv_msg.remove_file_from_server('/tmp/user_chk_outcome.txt')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.config_srv_another_subnet_no_interface('10.0.0.0/24', '10.0.0.5-10.0.0.5')
    srv_control.add_hooks('libdhcp_user_chk.so')
    # Server logging system is configured with logger type kea-dhcp4.callouts, severity DEBUG, severity level 99 and log file kea.log.
    # Server logging system is configured with logger type kea-dhcp4.hooks, severity INFO, severity level None and log file kea.log.
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', '0c:0e:0a:01:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '10.0.0.5')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    # Check the outcome file for correct content
    srv_msg.copy_remote('/tmp/user_chk_outcome.txt')
    srv_msg.compare_file(glob.glob("**/v4_outcome_1.txt", recursive=True)[0])
    # File stored in kea.log MUST contain line or phrase: INFO  \[kea-dhcp4\.hooks
    # File stored in kea.log MUST contain line or phrase: DEBUG \[kea-dhcp4\.callouts
