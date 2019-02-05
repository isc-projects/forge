"""DHCPv6 Relay Agent"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_msg
from features import references
from features import misc
from features import srv_control


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.relay
@pytest.mark.relay_invalid
@pytest.mark.disabled
def test_v6_relay_invalid_with_client_id(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    # add options to relay message
    srv_msg.client_does_include(step, 'RelayAgent', None, 'client-id')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

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
@pytest.mark.relay_invalid
@pytest.mark.disabled
def test_v6_relay_invalid_with_server_id(step):
    # add just serverid

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    # add options to relay message
    srv_msg.client_sets_value(step,
                              'RelayAgent',
                              'server_id',
                              '00:01:00:01:52:7b:a8:f0:08:00:27:58:f1:e8')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'server-id')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

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
@pytest.mark.relay_invalid
@pytest.mark.invalid_option
@pytest.mark.outline
@pytest.mark.disabled
def test_v6_relay_invalid_options_preference(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    # add options to relay message
    srv_msg.client_does_include(step, 'RelayAgent', None, 'preference')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

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
@pytest.mark.relay_invalid
@pytest.mark.invalid_option
@pytest.mark.outline
@pytest.mark.disabled
def test_v6_relay_invalid_options_time(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    # add options to relay message
    srv_msg.client_does_include(step, 'RelayAgent', None, 'time')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

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
@pytest.mark.relay_invalid
@pytest.mark.invalid_option
@pytest.mark.outline
@pytest.mark.disabled
def test_v6_relay_invalid_options_option_request(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    # add options to relay message
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '7')
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
@pytest.mark.relay_invalid
@pytest.mark.invalid_option
@pytest.mark.outline
@pytest.mark.disabled
def test_v6_relay_invalid_options_server_unicast(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    # add options to relay message
    srv_msg.client_does_include(step, 'RelayAgent', None, 'server-unicast')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '7')
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
@pytest.mark.relay_invalid
@pytest.mark.invalid_option
@pytest.mark.outline
@pytest.mark.disabled
def test_v6_relay_invalid_options_status_code(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    # add options to relay message
    srv_msg.client_does_include(step, 'RelayAgent', None, 'status-code')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '7')
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
@pytest.mark.relay_invalid
@pytest.mark.invalid_option
@pytest.mark.outline
@pytest.mark.disabled
def test_v6_relay_invalid_options_rapid_commit(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    # add options to relay message
    srv_msg.client_does_include(step, 'RelayAgent', None, 'rapid-commit')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '7')
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
@pytest.mark.relay_invalid
@pytest.mark.invalid_option
@pytest.mark.outline
@pytest.mark.disabled
def test_v6_relay_invalid_options_reconfigure(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    # add options to relay message
    srv_msg.client_does_include(step, 'RelayAgent', None, 'reconfigure')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

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
@pytest.mark.relay_invalid
@pytest.mark.invalid_option
@pytest.mark.outline
@pytest.mark.disabled
def test_v6_relay_invalid_options_reconfigure_accept(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    # add options to relay message
    srv_msg.client_does_include(step, 'RelayAgent', None, 'reconfigure-accept')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

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
