"""DHCPv6 Relay Agent"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_control
from features import references
from features import misc
from features import srv_msg


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.relay
def test_v6_relay_message_solicit_advertise(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    # Response option 9 MUST contain message 2.
    # message 2 - Advertise

    references.references_check(step, 'RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.relay
@pytest.mark.unicast
def test_v6_relay_message_unicast_global(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet_with_iface(step,
                                             '$(SERVER_IFACE)',
                                             '$(SRV_IPV6_ADDR_GLOBAL)',
                                             '3000::/64',
                                             '3000::1-3000::ff')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.unicast_addres(step, 'GLOBAL', None)
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')

    references.references_check(step, 'RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.relay
@pytest.mark.unicast
@pytest.mark.disabled
def test_v6_relay_message_unicast_local(step):

    misc.test_setup(step)
    # Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    srv_control.config_srv_subnet_with_iface(step,
                                             '$(SERVER_IFACE)',
                                             '$(SRV_IPV6_ADDR_LINK_LOCAL)',
                                             '3000::/64',
                                             '3000::1-3000::ff')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.unicast_addres(step, None, 'LINK_LOCAL')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)
    srv_msg.response_check_include_option(step, 'Response', None, '9')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')

    references.references_check(step, 'RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.relay
def test_v6_relay_message_solicit_reply(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'rapid-commit')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    # Response MUST include REPLY message.

    references.references_check(step, 'RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.relay
def test_v6_relay_message_request_reply(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    # Response MUST include REPLY message.

    references.references_check(step, 'RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.relay
def test_v6_relay_message_confirm_reply(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'CONFIRM')

    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    # Response MUST include REPLY message.

    references.references_check(step, 'RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.relay
def test_v6_relay_message_renew_reply(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'RENEW')

    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    # Response MUST include REPLY message.

    references.references_check(step, 'RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.relay
def test_v6_relay_message_rebind_reply(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REBIND')

    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    # Response MUST include REPLY message.

    references.references_check(step, 'RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.relay
def test_v6_relay_message_release_reply(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'RELEASE')

    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    # Response MUST include REPLY message.

    references.references_check(step, 'RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.relay
def test_v6_relay_message_decline_reply(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'DECLINE')

    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    # Response MUST include REPLY message.

    references.references_check(step, 'RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.relay
def test_v6_relay_message_information_request_reply(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'INFOREQUEST')

    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    # Response MUST include REPLY message.

    references.references_check(step, 'RFC3315')
