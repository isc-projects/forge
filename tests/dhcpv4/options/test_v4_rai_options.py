'''DHCPv4 RAI options'''

import pytest

import misc
import srv_control
import srv_msg

from protosupport.multi_protocol_functions import convert_address_to_hex, increase_address


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.kea_only
def test_v4_rai_option11_server_identifier_override():
    # RFC 5107 DHCP Server Identifier Override Suboption
    # Gitlab kea#1695
    misc.test_setup()
    srv_control.config_srv_subnet(
        '192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Usual scenario
    misc.test_procedure()
    srv_msg.client_does_include_with_value('server_id', '$(SRV4_ADDR)')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_option_content(54, 'value', '$(SRV4_ADDR)')

    # Send with a different server ID.
    misc.test_procedure()
    address = increase_address('$(SRV4_ADDR)', '32')
    srv_msg.client_does_include_with_value('server_id', address)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    # Send with a different server ID and a matching server override ID.
    misc.test_procedure()
    # b for code 11, 4 for option length
    rai_content = '0b04' + convert_address_to_hex(address)
    srv_msg.client_does_include_with_value('server_id', address)
    srv_msg.client_does_include_with_value(
        'relay_agent_information', rai_content)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_option_content(54, 'value', address)
    srv_msg.response_check_include_option(82)
    srv_msg.response_check_option_content(82, 'value', rai_content)
