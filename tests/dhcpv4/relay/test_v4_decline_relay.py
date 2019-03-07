"""DHCPv4 address decline process"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_msg
import misc
import srv_control


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.relay
@pytest.mark.decline
def test_v4_relay_decline_success():

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
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'ciaddr', '0.0.0.0')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_send_msg('DECLINE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value('client_id', '00010203040111')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.relay
@pytest.mark.decline
def test_v4_relay_decline_fail_without_serverid():

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
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_sets_value('Client', 'ciaddr', '0.0.0.0')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_send_msg('DECLINE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value('client_id', '00010203040111')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'NAK')
