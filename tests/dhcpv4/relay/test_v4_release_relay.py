"""DHCPv4 address release process"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_control
import srv_msg
import misc


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.relay
@pytest.mark.release
def test_v4_relay_release_success():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    # this is setting for every message in this test
    srv_msg.network_variable('source_port', '67')
    srv_msg.network_variable('source_address', '$(GIADDR4)')
    srv_msg.network_variable('destination_address', '$(SRV4_ADDR)')

    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    # Response MUST contain giaddr $(GIADDR4).
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value('client_id', '00010203040111')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    # Response MUST contain giaddr $(GIADDR4).
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.relay
@pytest.mark.release
def test_v4_relay_release_success_with_additional_offer():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.network_variable('source_port', '67')
    srv_msg.network_variable('source_address', '$(GIADDR4)')
    srv_msg.network_variable('destination_address', '$(SRV4_ADDR)')

    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_save_option('server_id')
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_sets_value('Client', 'chaddr', 'default')
    srv_msg.client_add_saved_option(None)
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value('client_id', '00010203040111')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.relay
@pytest.mark.release
def test_v4_relay_release_only_chaddr_same_chaddr():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.network_variable('source_port', '67')
    srv_msg.network_variable('source_address', '$(GIADDR4)')
    srv_msg.network_variable('destination_address', '$(SRV4_ADDR)')

    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_sets_value('Client', 'chaddr', '00:1f:d0:00:00:11')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    misc.test_procedure()
    # client id changed!
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_sets_value('Client', 'chaddr', '00:1f:d0:00:00:11')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg('RELEASE')

    # address not released
    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:00')
    srv_msg.client_requests_option('1')
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')
