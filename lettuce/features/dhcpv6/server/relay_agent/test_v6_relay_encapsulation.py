"""DHCPv6 Relay Agent encapsulation and Interface ID"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_control
from features import srv_msg
from features import references
from features import misc


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.relay
def test_v6_relay_message_interfaceid():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv('interface-id', '0', '15')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward('1', 's')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')
    # Response MUST include ADVERTISE message.

    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.relay
def test_v6_relay_encapsulate_31lvl():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward('31', 's')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')
    # Response MUST include ADVERTISE message.

    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.relay
def test_v6_relay_encapsulate_15lvl():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward('15', 's')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')
    # Response MUST include ADVERTISE message.

    references.references_check('RFC3315')
