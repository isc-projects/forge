"""Relay-Supplied Options"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import references
from features import srv_msg
from features import srv_control
from features import misc


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.rsoo
def test_v6_options_rsoo_default_option(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.set_conf_parameter_subnet(step, 'interface-id', '"abc"', '0')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_sets_value(step, 'RelayAgent', 'erpdomain', 'relay-supplied.domain.com')
    srv_msg.client_does_include(step, 'Relay-Supplied-Option', None, 'erp-local-domain-name')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'rsoo')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '65')
    srv_msg.response_check_option_content(step,
                                          'Relayed Message',
                                          '65',
                                          None,
                                          'erpdomain',
                                          'relay-supplied.domain.com')

    references.references_check(step, 'RFC642')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.rsoo
def test_v6_options_rsoo_custom_option_list(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.set_conf_parameter_subnet(step, 'interface-id', '"abc"', '0')
    srv_control.set_conf_parameter_global(step, 'relay-supplied-options', '["12"]')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '12')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_sets_value(step, 'RelayAgent', 'srvaddr', '2000::1')
    srv_msg.client_does_include(step, 'Relay-Supplied-Option', None, 'server-unicast')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'rsoo')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '12')
    srv_msg.response_check_option_content(step,
                                          'Relayed Message',
                                          '12',
                                          None,
                                          'srvaddr',
                                          '2000::1')

    references.references_check(step, 'RFC642')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.rsoo
def test_v6_options_rsoo_custom_option_list_default_option_65(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.set_conf_parameter_subnet(step, 'interface-id', '"abc"', '0')
    srv_control.set_conf_parameter_global(step, 'relay-supplied-options', '["12"]')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_sets_value(step, 'RelayAgent', 'erpdomain', 'relay-supplied.domain.com')
    srv_msg.client_does_include(step, 'Relay-Supplied-Option', None, 'erp-local-domain-name')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'rsoo')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '65')
    srv_msg.response_check_option_content(step,
                                          'Relayed Message',
                                          '65',
                                          None,
                                          'erpdomain',
                                          'relay-supplied.domain.com')

    references.references_check(step, 'RFC642')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.rsoo
def test_v6_options_rsoo_custom_option_list_server_has_option_configured_also(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.set_conf_parameter_subnet(step, 'interface-id', '"abc"', '0')
    srv_control.set_conf_parameter_global(step, 'relay-supplied-options', '["12"]')
    srv_control.config_srv_opt(step, 'unicast', '3000::1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '12')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_sets_value(step, 'RelayAgent', 'srvaddr', '2000::1')
    srv_msg.client_does_include(step, 'Relay-Supplied-Option', None, 'server-unicast')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'rsoo')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '12')
    srv_msg.response_check_option_content(step,
                                          'Relayed Message',
                                          '12',
                                          'NOT ',
                                          'srvaddr',
                                          '2000::1')
    srv_msg.response_check_option_content(step,
                                          'Relayed Message',
                                          '12',
                                          None,
                                          'srvaddr',
                                          '3000::1')

    references.references_check(step, 'RFC642')
