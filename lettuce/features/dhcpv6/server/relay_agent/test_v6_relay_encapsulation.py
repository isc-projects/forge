"""DHCPv6 Relay Agent encapsulation and Interface ID"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import misc
from features import srv_control
from features import references
from features import srv_msg


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.relay
def test_v6_relay_message_interfaceid(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv(step, 'interface-id', '0', '15')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', 's')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    # Response MUST include ADVERTISE message.

    references.references_check(step, 'RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.relay
def test_v6_relay_encapsulate_31lvl(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '31', 's')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    # Response MUST include ADVERTISE message.

    references.references_check(step, 'RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.relay
def test_v6_relay_encapsulate_15lvl(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '15', 's')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    # Response MUST include ADVERTISE message.

    references.references_check(step, 'RFC3315')
