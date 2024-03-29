# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Relay-Supplied Options"""

import pytest

from src import misc
from src import references
from src import srv_control
from src import srv_msg


@pytest.mark.v6
@pytest.mark.options
@pytest.mark.rsoo
def test_v6_options_rsoo_default_option():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.set_conf_parameter_subnet('interface-id', 'abc', 0)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_sets_value('RelayAgent', 'erpdomain', 'relay-supplied.domain.com')
    srv_msg.client_does_include('Relay-Supplied-Option', 'erp-local-domain-name')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_does_include('RelayAgent', 'rsoo')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(65)
    srv_msg.response_check_option_content(65, 'erpdomain', 'relay-supplied.domain.com.')

    references.references_check('RFC642')


@pytest.mark.v6
@pytest.mark.options
@pytest.mark.rsoo
def test_v6_options_rsoo_custom_option_list():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.set_conf_parameter_subnet('interface-id', 'abc', 0)
    srv_control.set_conf_parameter_global('relay-supplied-options', ["12"])
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(12)
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_sets_value('RelayAgent', 'srvaddr', '2000::1')
    srv_msg.client_does_include('Relay-Supplied-Option', 'server-unicast')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_does_include('RelayAgent', 'rsoo')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(12)
    srv_msg.response_check_option_content(12, 'srvaddr', '2000::1')

    references.references_check('RFC642')


@pytest.mark.v6
@pytest.mark.options
@pytest.mark.rsoo
def test_v6_options_rsoo_custom_option_list_default_option_65():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.set_conf_parameter_subnet('interface-id', 'abc', 0)
    srv_control.set_conf_parameter_global('relay-supplied-options', ["12"])
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_sets_value('RelayAgent', 'erpdomain', 'relay-supplied.domain.com')
    srv_msg.client_does_include('Relay-Supplied-Option', 'erp-local-domain-name')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_does_include('RelayAgent', 'rsoo')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(65)
    srv_msg.response_check_option_content(65, 'erpdomain', 'relay-supplied.domain.com.')

    references.references_check('RFC642')


@pytest.mark.v6
@pytest.mark.options
@pytest.mark.rsoo
def test_v6_options_rsoo_custom_option_list_server_has_option_configured_also():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.set_conf_parameter_subnet('interface-id', 'abc', 0)
    srv_control.set_conf_parameter_global('relay-supplied-options', ["12"])
    srv_control.config_srv_opt('unicast', '3000::1')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(12)
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_sets_value('RelayAgent', 'srvaddr', '2000::1')
    srv_msg.client_does_include('Relay-Supplied-Option', 'server-unicast')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_does_include('RelayAgent', 'rsoo')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(12)
    srv_msg.response_check_option_content(12, 'srvaddr', '2000::1', expect_include=False)
    srv_msg.response_check_option_content(12, 'srvaddr', '3000::1')

    references.references_check('RFC642')
