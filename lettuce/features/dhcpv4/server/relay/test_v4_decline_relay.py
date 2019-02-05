"""DHCPv4 address decline process"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_msg
from features import misc
from features import srv_control


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.relay
@pytest.mark.decline
def test_v4_relay_decline_success(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    # this is setting for every message in this test
    srv_msg.network_variable(step, 'source_port', '67')
    srv_msg.network_variable(step, 'source_address', '$(GIADDR4)')
    srv_msg.network_variable(step, 'destination_address', '$(SRV4_ADDR)')

    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '0.0.0.0')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'DECLINE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040111')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.relay
@pytest.mark.decline
def test_v4_relay_decline_fail_without_serverid(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    # this is setting for every message in this test
    srv_msg.network_variable(step, 'source_port', '67')
    srv_msg.network_variable(step, 'source_address', '$(GIADDR4)')
    srv_msg.network_variable(step, 'destination_address', '$(SRV4_ADDR)')

    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '0.0.0.0')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.1')
    srv_msg.client_send_msg(step, 'DECLINE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value(step, 'Client', 'hops', '1')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_does_include_with_value(step, 'client_id', '00010203040111')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'NAK')
