"""DHCPv6 Relay Agent"""

# pylint: disable=invalid-name,line-too-long

import pytest

import references
import misc
import srv_control
import srv_msg


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.relay
def test_v6_relay_message_solicit_advertise():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')
    # Response option 9 MUST contain message 2.
    # message 2 - Advertise

    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.relay
@pytest.mark.unicast
def test_v6_relay_message_unicast_global():

    misc.test_setup()
    srv_control.config_srv_subnet_with_iface('$(SERVER_IFACE)',
                                             '$(SRV_IPV6_ADDR_GLOBAL)',
                                             '3000::/64',
                                             '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.unicast_addres('GLOBAL', None)
    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')

    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.relay
@pytest.mark.unicast
@pytest.mark.disabled
def test_v6_relay_message_unicast_local():

    misc.test_setup()
    # Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    srv_control.config_srv_subnet_with_iface('$(SERVER_IFACE)',
                                             '$(SRV_IPV6_ADDR_LINK_LOCAL)',
                                             '3000::/64',
                                             '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.unicast_addres(None, 'LINK_LOCAL')
    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()
    srv_msg.response_check_include_option('Response', None, '9')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')

    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.relay
def test_v6_relay_message_solicit_reply():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'rapid-commit')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')
    # Response MUST include REPLY message.

    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.relay
def test_v6_relay_message_request_reply():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')
    # Response MUST include REPLY message.

    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.relay
def test_v6_relay_message_confirm_reply():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('CONFIRM')

    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')
    # Response MUST include REPLY message.

    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.relay
def test_v6_relay_message_renew_reply():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('RENEW')

    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')
    # Response MUST include REPLY message.

    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.relay
def test_v6_relay_message_rebind_reply():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REBIND')

    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')
    # Response MUST include REPLY message.

    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.relay
def test_v6_relay_message_release_reply():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('RELEASE')

    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')
    # Response MUST include REPLY message.

    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.relay
def test_v6_relay_message_decline_reply():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('DECLINE')

    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')
    # Response MUST include REPLY message.

    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.relay
def test_v6_relay_message_information_request_reply():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('INFOREQUEST')

    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')
    # Response MUST include REPLY message.

    references.references_check('RFC3315')
