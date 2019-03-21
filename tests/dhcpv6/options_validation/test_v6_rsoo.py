"""Relay-Supplied Options"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import references
import srv_control
import srv_msg


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.rsoo
def test_v6_options_rsoo_default_option():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.set_conf_parameter_subnet('interface-id', '"abc"', '0')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_sets_value('RelayAgent', 'erpdomain', 'relay-supplied.domain.com')
    srv_msg.client_does_include('Relay-Supplied-Option', None, 'erp-local-domain-name')
    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.client_does_include('RelayAgent', None, 'rsoo')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')
    srv_msg.response_check_option_content('Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option('Relayed Message', None, '1')
    srv_msg.response_check_include_option('Relayed Message', None, '2')
    srv_msg.response_check_include_option('Relayed Message', None, '3')
    srv_msg.response_check_option_content('Relayed Message', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option('Relayed Message', None, '65')
    srv_msg.response_check_option_content('Relayed Message',
                                          '65',
                                          None,
                                          'erpdomain',
                                          'relay-supplied.domain.com.')

    references.references_check('RFC642')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.rsoo
def test_v6_options_rsoo_custom_option_list():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.set_conf_parameter_subnet('interface-id', '"abc"', '0')
    srv_control.set_conf_parameter_global('relay-supplied-options', '["12"]')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_requests_option('12')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_sets_value('RelayAgent', 'srvaddr', '2000::1')
    srv_msg.client_does_include('Relay-Supplied-Option', None, 'server-unicast')
    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.client_does_include('RelayAgent', None, 'rsoo')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')
    srv_msg.response_check_option_content('Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option('Relayed Message', None, '1')
    srv_msg.response_check_include_option('Relayed Message', None, '2')
    srv_msg.response_check_include_option('Relayed Message', None, '3')
    srv_msg.response_check_option_content('Relayed Message', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option('Relayed Message', None, '12')
    srv_msg.response_check_option_content('Relayed Message', '12', None, 'srvaddr', '2000::1')

    references.references_check('RFC642')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.rsoo
def test_v6_options_rsoo_custom_option_list_default_option_65():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.set_conf_parameter_subnet('interface-id', '"abc"', '0')
    srv_control.set_conf_parameter_global('relay-supplied-options', '["12"]')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_sets_value('RelayAgent', 'erpdomain', 'relay-supplied.domain.com')
    srv_msg.client_does_include('Relay-Supplied-Option', None, 'erp-local-domain-name')
    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.client_does_include('RelayAgent', None, 'rsoo')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')
    srv_msg.response_check_option_content('Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option('Relayed Message', None, '1')
    srv_msg.response_check_include_option('Relayed Message', None, '2')
    srv_msg.response_check_include_option('Relayed Message', None, '3')
    srv_msg.response_check_option_content('Relayed Message', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option('Relayed Message', None, '65')
    srv_msg.response_check_option_content('Relayed Message',
                                          '65',
                                          None,
                                          'erpdomain',
                                          'relay-supplied.domain.com.')

    references.references_check('RFC642')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.rsoo
def test_v6_options_rsoo_custom_option_list_server_has_option_configured_also():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.set_conf_parameter_subnet('interface-id', '"abc"', '0')
    srv_control.set_conf_parameter_global('relay-supplied-options', '["12"]')
    srv_control.config_srv_opt('unicast', '3000::1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_requests_option('12')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_sets_value('RelayAgent', 'srvaddr', '2000::1')
    srv_msg.client_does_include('Relay-Supplied-Option', None, 'server-unicast')
    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.client_does_include('RelayAgent', None, 'rsoo')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')
    srv_msg.response_check_option_content('Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option('Relayed Message', None, '1')
    srv_msg.response_check_include_option('Relayed Message', None, '2')
    srv_msg.response_check_include_option('Relayed Message', None, '3')
    srv_msg.response_check_option_content('Relayed Message', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option('Relayed Message', None, '12')
    srv_msg.response_check_option_content('Relayed Message', '12', 'NOT ', 'srvaddr', '2000::1')
    srv_msg.response_check_option_content('Relayed Message', '12', None, 'srvaddr', '3000::1')

    references.references_check('RFC642')
