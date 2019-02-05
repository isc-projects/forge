"""Logging in Kea"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_control
from features import srv_msg
from features import misc


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.logging
def test_v4_loggers_options_debug(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.configure_loggers(step, 'kea-dhcp4.options', 'DEBUG', '99', 'kea.log')
    srv_control.config_srv_opt(step, 'time-offset', '50')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '2')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040111')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'DEBUG \[kea-dhcp4.options')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.logging
def test_v4_loggers_options_info(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.configure_loggers(step, 'kea-dhcp4.options', 'INFO', 'None', 'kea.log')
    srv_control.config_srv_opt(step, 'time-offset', '50')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '2')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040111')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               'NOT ',
                               r'DEBUG \[kea-dhcp4.options')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.logging
def test_v4_loggers_bad_packets_debug(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.configure_loggers(step, 'kea-dhcp4.bad-packets', 'DEBUG', '99', 'kea.log')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '2')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.100')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'NAK')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'DEBUG \[kea-dhcp4.bad-packets')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.logging
def test_v4_loggers_bad_packets_info(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.configure_loggers(step, 'kea-dhcp4.bad-packets', 'INFO', 'None', 'kea.log')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '2')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.100')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'NAK')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               'NOT ',
                               r'DEBUG \[kea-dhcp4.bad-packets')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.logging
def test_v4_loggers_dhcp4(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.configure_loggers(step, 'kea-dhcp4.dhcp4', 'DEBUG', '99', 'kea.log')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '2')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040111')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'DEBUG \[kea-dhcp4.dhcp4')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'INFO  \[kea-dhcp4.dhcp4')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.logging
def test_v4_loggers_dhcp4_info(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.configure_loggers(step, 'kea-dhcp4.dhcp4', 'INFO', 'None', 'kea.log')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '2')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040111')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               'NOT ',
                               r'DEBUG \[kea-dhcp4.dhcp4')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'INFO  \[kea-dhcp4.dhcp4')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.logging
def test_v4_loggers_alloc_engine(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.configure_loggers(step, 'kea-dhcp4.alloc-engine', 'DEBUG', '99', 'kea.log')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '2')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040111')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'DEBUG \[kea-dhcp4.alloc-engine')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.logging
def test_v4_loggers_dhcpsrv_debug(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.configure_loggers(step, 'kea-dhcp4.dhcpsrv', 'DEBUG', '99', 'kea.log')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '2')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040111')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'DEBUG \[kea-dhcp4.dhcpsrv')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'INFO  \[kea-dhcp4.dhcpsrv')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.logging
def test_v4_loggers_dhcpsrv_info(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.configure_loggers(step, 'kea-dhcp4.dhcpsrv', 'INFO', 'None', 'kea.log')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '2')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040111')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               'NOT ',
                               r'DEBUG \[kea-dhcp4.dhcpsrv')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'INFO  \[kea-dhcp4.dhcpsrv')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.logging
def test_v4_loggers_leases_debug(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.configure_loggers(step, 'kea-dhcp4.leases', 'DEBUG', '99', 'kea.log')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '2')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:21')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'INFO  \[kea-dhcp4.leases')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'DEBUG \[kea-dhcp4.leases')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.logging
def test_v4_loggers_leases_info(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.configure_loggers(step, 'kea-dhcp4.leases', 'INFO', 'None', 'kea.log')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '2')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040111')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               'NOT ',
                               r'DEBUG \[kea-dhcp4.leases')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.logging
def test_v4_loggers_packets_debug(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.configure_loggers(step, 'kea-dhcp4.packets', 'DEBUG', '99', 'kea.log')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '2')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040111')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'DEBUG \[kea-dhcp4.packets')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.logging
def test_v4_loggers_packets_info(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.configure_loggers(step, 'kea-dhcp4.packets', 'INFO', 'None', 'kea.log')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '2')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040111')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               'NOT ',
                               r'DEBUG \[kea-dhcp4.packets')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.logging
def test_v4_loggers_hosts_debug(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.configure_loggers(step, 'kea-dhcp4.hosts', 'DEBUG', '99', 'kea.log')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '2')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040111')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'DEBUG \[kea-dhcp4.hosts')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.logging
def test_v4_loggers_hosts_info(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.configure_loggers(step, 'kea-dhcp4.hosts', 'INFO', 'None', 'kea.log')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '2')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040111')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               'NOT ',
                               r'DEBUG \[kea-dhcp4.hosts')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.logging
def test_v4_loggers_all(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.configure_loggers(step, 'kea-dhcp4', 'DEBUG', '99', 'kea.log')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '2')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:33')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:33')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:31')
    srv_msg.client_save_option_count(step, '1', 'server_id')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:33')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '2')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040111')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'DEBUG \[kea-dhcp4.packets')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'DEBUG \[kea-dhcp4.dhcpsrv')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'DEBUG \[kea-dhcp4.alloc-engine')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'DEBUG \[kea-dhcp4.dhcp4')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'DEBUG \[kea-dhcp4.options')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'DEBUG \[kea-dhcp4.leases')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'INFO  \[kea-dhcp4.leases')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.logging
def test_v4_loggers_all_different_levels_same_file(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.configure_loggers(step, 'kea-dhcp4.dhcp4', 'INFO', 'None', 'kea.log')
    srv_control.configure_loggers(step, 'kea-dhcp4.dhcpsrv', 'INFO', 'None', 'kea.log')
    srv_control.configure_loggers(step, 'kea-dhcp4.options', 'DEBUG', '99', 'kea.log')
    srv_control.configure_loggers(step, 'kea-dhcp4.packets', 'DEBUG', '99', 'kea.log')
    srv_control.configure_loggers(step, 'kea-dhcp4.leases', 'WARN', 'None', 'kea.log')
    srv_control.configure_loggers(step, 'kea-dhcp4.alloc-engine', 'DEBUG', '50', 'kea.log')
    srv_control.configure_loggers(step, 'kea-dhcp4.bad-packets', 'DEBUG', '25', 'kea.log')
    srv_control.configure_loggers(step, 'kea-dhcp4.options', 'INFO', 'None', 'kea.log')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '2')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040111')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '2')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.100')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'NAK')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'DEBUG \[kea-dhcp4.packets')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               'NOT ',
                               r'DEBUG \[kea-dhcp4.leases')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'DEBUG \[kea-dhcp4.alloc-engine')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               'NOT ',
                               r'DEBUG \[kea-dhcp4.dhcp4')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'INFO  \[kea-dhcp4.dhcp4')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               'NOT ',
                               r'DEBUG \[kea-dhcp4.dhcpsrv')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'INFO  \[kea-dhcp4.dhcpsrv')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               'NOT ',
                               r'DEBUG \[kea-dhcp4.options')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.logging
def test_v4_loggers_all_different_levels_different_file(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.configure_loggers(step, 'kea-dhcp4.dhcp4', 'INFO', 'None', 'kea.log1')
    srv_control.configure_loggers(step, 'kea-dhcp4.dhcpsrv', 'INFO', 'None', 'kea.log2')
    srv_control.configure_loggers(step, 'kea-dhcp4.options', 'DEBUG', '99', 'kea.log3')
    srv_control.configure_loggers(step, 'kea-dhcp4.packets', 'DEBUG', '99', 'kea.log4')
    srv_control.configure_loggers(step, 'kea-dhcp4.leases', 'WARN', 'None', 'kea.log5')
    srv_control.configure_loggers(step, 'kea-dhcp4.alloc-engine', 'DEBUG', '50', 'kea.log6')
    srv_control.configure_loggers(step, 'kea-dhcp4.bad-packets', 'DEBUG', '25', 'kea.log6')
    srv_control.configure_loggers(step, 'kea-dhcp4.options', 'INFO', 'None', 'kea.log6')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '2')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040111')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '2')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.100')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'NAK')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log4',
                               None,
                               r'DEBUG \[kea-dhcp4.packets')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log5',
                               'NOT ',
                               r'DEBUG \[kea-dhcp4.leases')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log6',
                               None,
                               r'DEBUG \[kea-dhcp4.alloc-engine')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log1',
                               'NOT ',
                               r'DEBUG \[kea-dhcp4.dhcp4')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log1',
                               None,
                               r'INFO  \[kea-dhcp4.dhcp4')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log2',
                               'NOT ',
                               r'DEBUG \[kea-dhcp4.dhcpsrv')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log2',
                               None,
                               r'INFO  \[kea-dhcp4.dhcpsrv')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log3',
                               'NOT ',
                               r'DEBUG \[kea-dhcp4.options')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.logging
def test_ddns4_logging_all_types_debug(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'abc.com')
    srv_control.add_forward_ddns(step,
                                 'four.example.com.',
                                 'forge.sha1.key',
                                 '192.168.50.252',
                                 '53')
    srv_control.add_reverse_ddns(step,
                                 '50.168.192.in-addr.arpa.',
                                 'forge.sha1.key',
                                 '192.168.50.252',
                                 '53')
    srv_control.add_keys(step, 'forge.sha1.key', 'HMAC-SHA1', 'PN4xKZ/jDobCMlo4rpr70w==')
    srv_control.configure_loggers(step, 'kea-dhcp-ddns', 'DEBUG', '99', 'kea.log')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_save_option_count(step, '1', 'server_id')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'aa.four.example.com.')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '81')
    srv_msg.response_check_option_content(step, 'Response', '81', None, 'flags', '1.')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '81',
                                          None,
                                          'fqdn',
                                          'aa.four.example.com.')

    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'INFO  \[kea-dhcp-ddns.dhcpddns')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'DEBUG \[kea-dhcp-ddns.dhcpddns')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'DEBUG \[kea-dhcp-ddns.libdhcp-ddns')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'DEBUG \[kea-dhcp-ddns.d2-to-dns')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'ERROR \[kea-dhcp-ddns.d2-to-dns')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               r'DEBUG \[kea-dhcp-ddns.dhcp-to-d2')
