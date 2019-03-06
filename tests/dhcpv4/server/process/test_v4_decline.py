"""DHCPv4 address decline process"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_msg
import srv_control


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.decline
def test_v4_decline_success_long_decline_period():
    # address in decline period
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.set_conf_parameter_global('decline-probation-period', '3600')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_does_include_with_value('client_id', '00010203040122')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_does_include_with_value('client_id', '00010203040122')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_does_include_with_value('client_id', '00010203040122')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'ciaddr', '0.0.0.0')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_send_msg('DECLINE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value('client_id', '00010203040111')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.decline
def test_v4_decline_success_short_decline_period():
    # address in decline period
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.set_conf_parameter_global('decline-probation-period', '2')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_does_include_with_value('client_id', '00010203040122')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_does_include_with_value('client_id', '00010203040122')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_does_include_with_value('client_id', '00010203040122')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'ciaddr', '0.0.0.0')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_send_msg('DECLINE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value('client_id', '00010203040111')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.forge_sleep('3', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:44')
    srv_msg.client_does_include_with_value('client_id', '00010203040144')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.decline
def test_v4_decline_fail_without_serverid():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value('client_id', '00010203040111')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value('client_id', '00010203040111')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value('client_id', '00010203040111')
    srv_msg.client_sets_value('Client', 'ciaddr', '0.0.0.0')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_send_msg('DECLINE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_does_include_with_value('client_id', '00010203040122')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value('client_id', '00010203040111')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')

    # @v4 @dhcp4 @decline
    # Scenario: v4.decline.fail-without-serverid
    #
    # Test Setup:
    # Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    # Send server configuration using SSH and config-file.
    # DHCP server is started.
    #
    # Test Procedure:
    # Client sends DISCOVER message.
    #
    # Pass Criteria:
    # Server MUST respond with OFFER message.
    # Response MUST contain yiaddr 192.168.50.1.
    #
    # Test Procedure:
    # Client copies server_id option from received message.
    # Client adds to the message requested_addr with value 192.168.50.1.
    # Client sends REQUEST message.
    #
    # Pass Criteria:
    # Server MUST respond with ACK message.
    # Response MUST contain yiaddr 192.168.50.1.
    #
    # Test Procedure:
    # Client sets ciaddr value to 0.0.0.0.
    # Client adds to the message requested_addr with value 192.168.50.1.
    # Client sends DECLINE message.
    #
    # Pass Criteria:
    # Server MUST NOT respond.
    #
    # Test Procedure:
    # Client sets chaddr value to 00:00:00:00:00:11.
    # Client adds to the message client_id with value 00010203040111.
    # Client sends DISCOVER message.
    #
    # Pass Criteria:
    # Server MUST respond with NAK message.


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.decline
def test_v4_decline_fail_without_requested_ip_address():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value('client_id', '00010203040111')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value('client_id', '00010203040111')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value('client_id', '00010203040111')
    srv_msg.client_sets_value('Client', 'ciaddr', '0.0.0.0')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_send_msg('DECLINE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_does_include_with_value('client_id', '00010203040122')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value('client_id', '00010203040111')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    # client should get back this address because it's not in declined period


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.decline
def test_v4_decline_fail_client_id_not_included():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_does_include_with_value('client_id', '00010203040122')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '61')
    srv_msg.response_check_option_content('Response', '61', None, 'value', '00010203040122')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_does_include_with_value('client_id', '00010203040122')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '61')
    srv_msg.response_check_option_content('Response', '61', None, 'value', '00010203040122')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'ciaddr', '0.0.0.0')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_send_msg('DECLINE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value('client_id', '00010203040999')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_does_include_with_value('client_id', '00010203040122')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '61')
    srv_msg.response_check_option_content('Response', '61', None, 'value', '00010203040122')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.decline
def test_v4_decline_fail_different_client_id():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '00010203040111')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '61')
    srv_msg.response_check_option_content('Response', '61', None, 'value', '00010203040111')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_does_include_with_value('client_id', '00010203040111')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '61')
    srv_msg.response_check_option_content('Response', '61', None, 'value', '00010203040111')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '00010203040666')
    srv_msg.client_sets_value('Client', 'ciaddr', '0.0.0.0')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_send_msg('DECLINE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value('client_id', '00010203040999')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'NAK')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.decline
def test_v4_decline_fail_different_chaddr():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_sets_value('Client', 'ciaddr', '0.0.0.0')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_send_msg('DECLINE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value('client_id', '00010203040111')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'NAK')
