"""Kea Hook flex-id testing"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import misc
from features import srv_control
from features import srv_msg


@pytest.mark.v6
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v6_hooks_flexid_1(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-hostname',
                                           '0',
                                           'flex-id',
                                           '\'port1234\'')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'address', '3000::f')
    srv_control.add_line(step, '"host-reservation-identifiers": [  "duid",  "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step,
                                      '1',
                                      'identifier-expression',
                                      'substring(relay6[0].option[18].hex,0,8)')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'port1234')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
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
    # Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:1::1.
    srv_msg.response_check_suboption_content(step,
                                             'Relayed Message',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::f')


@pytest.mark.v6
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v6_hooks_flexid_libreload(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-hostname',
                                           '0',
                                           'flex-id',
                                           '\'port1234\'')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'address', '3000::f')
    srv_control.add_line(step, '"host-reservation-identifiers": [  "duid",  "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step,
                                      '1',
                                      'identifier-expression',
                                      'substring(relay6[0].option[18].hex,0,8)')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'port1234')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
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
    # Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:1::1.
    srv_msg.response_check_suboption_content(step,
                                             'Relayed Message',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::f')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "libreload","arguments": {}}')
    # if reload works - classification should work without changes

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'port1234')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
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
    # Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:1::1.
    srv_msg.response_check_suboption_content(step,
                                             'Relayed Message',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::f')


@pytest.mark.v6
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v6_hooks_flexid_reconfigure_1(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-hostname',
                                           '0',
                                           'flex-id',
                                           '\'port1234\'')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'address', '3000::f')
    srv_control.add_line(step, '"host-reservation-identifiers": [  "duid",  "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step,
                                      '1',
                                      'identifier-expression',
                                      'substring(relay6[0].option[18].hex,0,8)')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'port1234')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
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
    # Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:1::1.
    srv_msg.response_check_suboption_content(step,
                                             'Relayed Message',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::f')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-hostname',
                                           '0',
                                           'flex-id',
                                           '\'port1234\'')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'address', '3000::f')
    srv_control.add_line(step, '"host-reservation-identifiers": [  "duid",  "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step,
                                      '1',
                                      'identifier-expression',
                                      'substring(relay6[0].option[18].hex,0,8)')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'reconfigured')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'port1234')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
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
    # Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:1::1.
    srv_msg.response_check_suboption_content(step,
                                             'Relayed Message',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::f')


@pytest.mark.v6
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v6_hooks_flexid_reconfigure_2(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-hostname',
                                           '0',
                                           'flex-id',
                                           '\'port1234\'')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'address', '3000::f')
    srv_control.add_line(step, '"host-reservation-identifiers": [  "duid",  "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step,
                                      '1',
                                      'identifier-expression',
                                      'substring(relay6[0].option[18].hex,0,8)')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'port1234')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
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
    # Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:1::1.
    srv_msg.response_check_suboption_content(step,
                                             'Relayed Message',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::f')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-hostname',
                                           '0',
                                           'flex-id',
                                           '\'port4321\'')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'address', '3000::f')
    srv_control.add_line(step, '"host-reservation-identifiers": [  "duid",  "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step,
                                      '1',
                                      'identifier-expression',
                                      'substring(relay6[0].option[18].hex,0,8)')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'reconfigured')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'port1234')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
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
    srv_msg.response_check_suboption_content(step,
                                             'Relayed Message',
                                             '5',
                                             '3',
                                             'NOT ',
                                             'address',
                                             '3000::f')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'port4321')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
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
    srv_msg.response_check_suboption_content(step,
                                             'Relayed Message',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::f')


@pytest.mark.v6
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v6_hooks_flexid_2(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-hostname',
                                           '0',
                                           'flex-id',
                                           '\'port1234\'')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'address', '3000::f')
    srv_control.add_line(step, '"host-reservation-identifiers": [  "duid",  "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step,
                                      '1',
                                      'identifier-expression',
                                      'relay6[0].option[18].hex')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command": "config-reload","arguments":  {} }
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'port1234')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
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
    # Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:1::1.
    srv_msg.response_check_suboption_content(step,
                                             'Relayed Message',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::f')


@pytest.mark.v6
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v6_hooks_flexid_3(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-hostname',
                                           '0',
                                           'flex-id',
                                           '01:02:03:04:05:06')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'address', '3000::f')
    srv_control.add_line(step, '"host-reservation-identifiers": [  "duid",  "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step,
                                      '1',
                                      'identifier-expression',
                                      'vendor[4491].option[1026].hex')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'enterprisenum', '4491')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption(step, 'Client', '1026', '01:02:03:04:05:06')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-specific-info')

    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::f')


@pytest.mark.v6
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v6_hooks_flexid_mysql_1(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.add_line(step, '"host-reservation-identifiers": ["flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step,
                                      '1',
                                      'identifier-expression',
                                      'relay6[0].option[18].hex')

    srv_control.enable_db_backend_reservation(step, 'MySQL')
    srv_control.new_db_backend_reservation(step, 'MySQL', 'flex-id', '706f727431323334')
    srv_control.update_db_backend_reservation(step, 'hostname', 'reserved-hostname', 'MySQL', '1')
    srv_control.update_db_backend_reservation(step, 'dhcp6_subnet_id', '1', 'MySQL', '1')
    srv_control.ipv6_address_db_backend_reservation(step, '3000::f', '$(EMPTY)', 'MySQL', '1')
    srv_control.upload_db_reservation(step, 'MySQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')
    # Pause the Test.

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'port1234')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
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
    srv_msg.response_check_suboption_content(step,
                                             'Relayed Message',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::f')


@pytest.mark.v6
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v6_hooks_flexid_mysql_2(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.add_line(step, '"host-reservation-identifiers": [  "duid",  "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step,
                                      '1',
                                      'identifier-expression',
                                      'vendor[4491].option[1026].hex')

    srv_control.enable_db_backend_reservation(step, 'MySQL')
    srv_control.new_db_backend_reservation(step, 'MySQL', 'flex-id', '01:02:03:04:05:06')
    srv_control.update_db_backend_reservation(step, 'hostname', 'reserved-hostname', 'MySQL', '1')
    srv_control.update_db_backend_reservation(step, 'dhcp6_subnet_id', '1', 'MySQL', '1')
    srv_control.ipv6_address_db_backend_reservation(step, '3000::f', '$(EMPTY)', 'MySQL', '1')
    srv_control.upload_db_reservation(step, 'MySQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'enterprisenum', '4491')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption(step, 'Client', '1026', '01:02:03:04:05:06')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-specific-info')

    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::f')


@pytest.mark.v6
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v6_hooks_flexid_pgsql_1(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.add_line(step, '"host-reservation-identifiers": [  "duid",  "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step,
                                      '1',
                                      'identifier-expression',
                                      'relay6[0].option[18].hex')

    srv_control.enable_db_backend_reservation(step, 'PostgreSQL')
    srv_control.new_db_backend_reservation(step, 'PostgreSQL', 'flex-id', '706f727431323334')
    srv_control.update_db_backend_reservation(step,
                                              'hostname',
                                              'reserved-hostname',
                                              'PostgreSQL',
                                              '1')
    srv_control.update_db_backend_reservation(step, 'dhcp6_subnet_id', '1', 'PostgreSQL', '1')
    srv_control.ipv6_address_db_backend_reservation(step,
                                                    '3000::f',
                                                    '$(EMPTY)',
                                                    'PostgreSQL',
                                                    '1')
    srv_control.upload_db_reservation(step, 'PostgreSQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')
    # Pause the Test.

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'port1234')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
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

    srv_msg.response_check_suboption_content(step,
                                             'Relayed Message',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::f')


@pytest.mark.v6
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v6_hooks_flexid_pgsql_2(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.add_line(step, '"host-reservation-identifiers": [  "duid",  "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step,
                                      '1',
                                      'identifier-expression',
                                      'vendor[4491].option[1026].hex')

    srv_control.enable_db_backend_reservation(step, 'PostgreSQL')
    srv_control.new_db_backend_reservation(step, 'PostgreSQL', 'flex-id', '01:02:03:04:05:06')
    srv_control.update_db_backend_reservation(step,
                                              'hostname',
                                              'reserved-hostname',
                                              'PostgreSQL',
                                              '1')
    srv_control.update_db_backend_reservation(step, 'dhcp6_subnet_id', '1', 'PostgreSQL', '1')
    srv_control.ipv6_address_db_backend_reservation(step,
                                                    '3000::f',
                                                    '$(EMPTY)',
                                                    'PostgreSQL',
                                                    '1')
    srv_control.upload_db_reservation(step, 'PostgreSQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'enterprisenum', '4491')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption(step, 'Client', '1026', '01:02:03:04:05:06')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-specific-info')

    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::f')


@pytest.mark.v6
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v6_hooks_flexid_replace_duid(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-hostname',
                                           '0',
                                           'flex-id',
                                           '01:02:03:04:05:06')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'address', '3000::f')
    srv_control.add_line(step, '"host-reservation-identifiers": [  "duid",  "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step,
                                      '1',
                                      'identifier-expression',
                                      'vendor[4491].option[1026].hex')
    srv_control.add_parameter_to_hook(step, '1', 'replace-client-id', 'true')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value(step, 'Client', 'enterprisenum', '4491')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption(step, 'Client', '1026', '01:02:03:04:05:06')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-specific-info')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::f')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'enterprisenum', '4491')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption(step, 'Client', '1026', '01:02:03:04:05:06')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-specific-info')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::f')


@pytest.mark.v6
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v6_hooks_flexid_replace_duid_renew(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-hostname',
                                           '0',
                                           'flex-id',
                                           '01:02:03:04:05:06')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'address', '3000::f')
    srv_control.add_line(step, '"host-reservation-identifiers": [  "duid",  "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step,
                                      '1',
                                      'identifier-expression',
                                      'vendor[4491].option[1026].hex')
    srv_control.add_parameter_to_hook(step, '1', 'replace-client-id', 'true')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value(step, 'Client', 'enterprisenum', '4491')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption(step, 'Client', '1026', '01:02:03:04:05:06')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-specific-info')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::f')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'enterprisenum', '4491')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption(step, 'Client', '1026', '01:02:03:04:05:06')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-specific-info')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::f')

    # Client with different duid try to renew
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'enterprisenum', '4491')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption(step, 'Client', '1026', '01:02:03:04:05:06')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-specific-info')
    srv_msg.client_send_msg(step, 'RENEW')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::f')
    srv_msg.response_check_suboption_content(step, 'Response', '5', '3', 'NOT ', 'validlft', '0')


@pytest.mark.v6
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v6_hooks_flexid_replace_duid_renew_failed(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-hostname',
                                           '0',
                                           'flex-id',
                                           '01:02:03:04:05:06')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'address', '3000::f')
    srv_control.add_line(step, '"host-reservation-identifiers": [  "duid",  "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step,
                                      '1',
                                      'identifier-expression',
                                      'vendor[4491].option[1026].hex')
    srv_control.add_parameter_to_hook(step, '1', 'replace-client-id', 'true')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value(step, 'Client', 'enterprisenum', '4491')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption(step, 'Client', '1026', '01:02:03:04:05:06')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-specific-info')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::f')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'enterprisenum', '4491')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption(step, 'Client', '1026', '01:02:03:04:05:06')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-specific-info')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::f')

    # Client with the same DUID and different flex-id try to renew
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'enterprisenum', '4491')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption(step, 'Client', '1026', '01:02:03:44:55:66')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-specific-info')
    srv_msg.client_send_msg(step, 'RENEW')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::f')
    srv_msg.response_check_suboption_content(step, 'Response', '5', '3', None, 'validlft', '0')


@pytest.mark.v6
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v6_hooks_flexid_replace_duid_release(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-hostname',
                                           '0',
                                           'flex-id',
                                           '01:02:03:04:05:06')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'address', '3000::f')
    srv_control.add_line(step, '"host-reservation-identifiers": [  "duid",  "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step,
                                      '1',
                                      'identifier-expression',
                                      'vendor[4491].option[1026].hex')
    srv_control.add_parameter_to_hook(step, '1', 'replace-client-id', 'true')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value(step, 'Client', 'enterprisenum', '4491')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption(step, 'Client', '1026', '01:02:03:04:05:06')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-specific-info')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::f')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'enterprisenum', '4491')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption(step, 'Client', '1026', '01:02:03:04:05:06')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-specific-info')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::f')

    # Client with different duid try to release
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'enterprisenum', '4491')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption(step, 'Client', '1026', '01:02:03:04:05:06')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-specific-info')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content(step, 'Response', '13', '3', None, 'statuscode', '0')


@pytest.mark.v6
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v6_hooks_flexid_replace_duid_release_failed(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-hostname',
                                           '0',
                                           'flex-id',
                                           '01:02:03:04:05:06')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'address', '3000::f')
    srv_control.add_line(step, '"host-reservation-identifiers": [  "duid",  "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step,
                                      '1',
                                      'identifier-expression',
                                      'vendor[4491].option[1026].hex')
    srv_control.add_parameter_to_hook(step, '1', 'replace-client-id', 'true')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value(step, 'Client', 'enterprisenum', '4491')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption(step, 'Client', '1026', '01:02:03:04:05:06')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-specific-info')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::f')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'enterprisenum', '4491')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption(step, 'Client', '1026', '01:02:03:04:05:06')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-specific-info')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::f')

    # Client with the same duid but different flex-id try to release (result should be nobiding)
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'enterprisenum', '4491')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption(step, 'Client', '1026', '01:02:03:44:55:66')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-specific-info')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content(step, 'Response', '13', '3', None, 'statuscode', '3')

    # File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 3000::f,01:02:03:04:05:06,4000,
    # File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST NOT contain line or phrase: 3000::f,01:02:03:04:05:06,0,


@pytest.mark.v6
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v6_hooks_flexid_replace_duid_release_mysql(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-hostname',
                                           '0',
                                           'flex-id',
                                           '01:02:03:04:05:06')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'address', '3000::f')
    srv_control.add_line(step, '"host-reservation-identifiers": [  "duid",  "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step,
                                      '1',
                                      'identifier-expression',
                                      'vendor[4491].option[1026].hex')
    srv_control.add_parameter_to_hook(step, '1', 'replace-client-id', 'true')

    srv_control.enable_db_backend_reservation(step, 'MySQL')
    srv_control.new_db_backend_reservation(step, 'MySQL', 'flex-id', '01:02:03:04:05:06')
    srv_control.update_db_backend_reservation(step, 'hostname', 'reserved-hostname', 'MySQL', '1')
    srv_control.update_db_backend_reservation(step, 'dhcp6_subnet_id', '1', 'MySQL', '1')
    srv_control.ipv6_address_db_backend_reservation(step, '3000::f', '$(EMPTY)', 'MySQL', '1')
    srv_control.upload_db_reservation(step, 'MySQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value(step, 'Client', 'enterprisenum', '4491')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption(step, 'Client', '1026', '11:22:33:44:55:66')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-specific-info')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             'NOT ',
                                             'address',
                                             '3000::f')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value(step, 'Client', 'enterprisenum', '4491')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption(step, 'Client', '1026', '01:02:03:04:05:06')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-specific-info')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::f')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'enterprisenum', '4491')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption(step, 'Client', '1026', '01:02:03:04:05:06')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-specific-info')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::f')

    # Client with different duid try to release
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'enterprisenum', '4491')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption(step, 'Client', '1026', '01:02:03:04:05:06')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-specific-info')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content(step, 'Response', '13', '3', None, 'statuscode', '0')


@pytest.mark.v6
@pytest.mark.flexid
@pytest.mark.kea_only
def test_v6_hooks_flexid_replace_duid_release_pgsql(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-hostname',
                                           '0',
                                           'flex-id',
                                           '01:02:03:04:05:06')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'address', '3000::f')
    srv_control.add_line(step, '"host-reservation-identifiers": [  "duid",  "flex-id" ]')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step,
                                      '1',
                                      'identifier-expression',
                                      'vendor[4491].option[1026].hex')
    srv_control.add_parameter_to_hook(step, '1', 'replace-client-id', 'true')

    srv_control.enable_db_backend_reservation(step, 'PostgreSQL')
    srv_control.new_db_backend_reservation(step, 'PostgreSQL', 'flex-id', '01:02:03:04:05:06')
    srv_control.update_db_backend_reservation(step,
                                              'hostname',
                                              'reserved-hostname',
                                              'PostgreSQL',
                                              '1')
    srv_control.update_db_backend_reservation(step, 'dhcp6_subnet_id', '1', 'PostgreSQL', '1')
    srv_control.ipv6_address_db_backend_reservation(step,
                                                    '3000::f',
                                                    '$(EMPTY)',
                                                    'PostgreSQL',
                                                    '1')
    srv_control.upload_db_reservation(step, 'PostgreSQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value(step, 'Client', 'enterprisenum', '4491')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption(step, 'Client', '1026', '01:02:03:04:05:06')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-specific-info')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::f')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'enterprisenum', '4491')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption(step, 'Client', '1026', '01:02:03:04:05:06')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-specific-info')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::f')

    # Client with different duid try to release
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'enterprisenum', '4491')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption(step, 'Client', '1026', '01:02:03:04:05:06')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-specific-info')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content(step, 'Response', '13', '3', None, 'statuscode', '0')
