"""Kea Control Channel Agent - HTTP"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_msg
from features import srv_control
from features import misc


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_dhcp_disable_timer(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '$(SRV4_ADDR)',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
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
                                             '3000::1')

    srv_msg.send_through_http(step,
                              '$(SRV4_ADDR)',
                              '8000',
                              '{"command": "dhcp-disable","service": ["dhcp6"], "arguments": {"max-period": 5}}')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    srv_msg.forge_sleep(step, '7', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_dhcp_disable(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '$(SRV4_ADDR)',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
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
                                             '3000::1')

    srv_msg.send_through_http(step,
                              '$(SRV4_ADDR)',
                              '8000',
                              '{"command": "dhcp-disable","service": ["dhcp6"]}')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_dhcp_disable_and_enable(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '$(SRV4_ADDR)',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
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
                                             '3000::1')

    srv_msg.send_through_http(step,
                              '$(SRV4_ADDR)',
                              '8000',
                              '{"command": "dhcp-disable","service": ["dhcp6"]}')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    srv_msg.send_through_http(step,
                              '$(SRV4_ADDR)',
                              '8000',
                              '{"command": "dhcp-enable","service": ["dhcp6"]}')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_config_set_basic(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '$(SRV4_ADDR)',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
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
                                             '3000::1')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    # Server has control agent configured on HTTP connection with address $(SRV4_ADDR):8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
    srv_control.generate_config_files(step)

    srv_msg.send_through_http(step,
                              '$(SRV4_ADDR)',
                              '8000',
                              '{"command": "config-set", "service": ["dhcp6"], "arguments":  $(SERVER_CONFIG) }')

    srv_msg.forge_sleep(step, '$(SLEEP_TIME_2)', 'seconds')
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
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
                                             '2001:db8:1::1')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_change_socket_during_reconfigure(step):
    # change address test needed also
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::f')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '$(SRV4_ADDR)',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
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
                                             '3000::1')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '$(SRV4_ADDR)',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket2')
    srv_control.generate_config_files(step)

    srv_msg.send_through_http(step,
                              '$(SRV4_ADDR)',
                              '8000',
                              '{"command": "config-set", "service": ["dhcp6"],"arguments":  $(SERVER_CONFIG) }')
    srv_msg.forge_sleep(step, '$(SLEEP_TIME_2)', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
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
                                             '2001:db8:1::1')
    srv_msg.send_through_http(step,
                              '$(SRV4_ADDR)',
                              '8000',
                              '{"command":"list-commands","arguments": {} }')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_after_restart_load_config_file(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '$(SRV4_ADDR)',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
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
                                             '3000::1')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.agent_control_channel(step,
                                      '$(SRV4_ADDR)',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.generate_config_files(step)

    srv_msg.send_through_http(step,
                              '$(SRV4_ADDR)',
                              '8000',
                              '{"command": "config-set", "service": ["dhcp6"],"arguments":  $(SERVER_CONFIG) }')

    srv_msg.forge_sleep(step, '$(SLEEP_TIME_2)', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
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
                                             '2001:db8:1::1')

    srv_control.start_srv(step, 'DHCP', 'restarted')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
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
                                             '3000::1')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_get_config(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '$(SRV4_ADDR)',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    srv_msg.send_through_http(step,
                              '$(SRV4_ADDR)',
                              '8000',
                              '{"command": "config-get","service":["dhcp6"],"arguments": {} }')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_test_config(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::1')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '$(SRV4_ADDR)',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
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
                                             '3000::1')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_prefix(step, '2001:db8:1::', '0', '90', '96')
    srv_control.agent_control_channel(step,
                                      '$(SRV4_ADDR)',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket_ANOTHER_ONE')
    srv_control.config_srv_id(step, 'LLT', '00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8')
    srv_control.config_srv_opt(step, 'sip-server-addr', '2001:db8::1,2001:db8::2')
    srv_control.config_srv_opt(step,
                               'new-posix-timezone',
                               'EST5EDT4\\,M3.2.0/02:00\\,M11.1.0/02:00')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '3000::1',
                                           '0',
                                           'duid',
                                           '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.generate_config_files(step)

    srv_msg.send_through_http(step,
                              '$(SRV4_ADDR)',
                              '8000',
                              '{"command": "config-test","service": ["dhcp6"], "arguments":  $(SERVER_CONFIG) }')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
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
                                             '3000::1')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_prefix(step, '2001:db8:1::', '0', '90', '96')
    srv_control.agent_control_channel(step,
                                      '$(SRV4_ADDR)',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket_ANOTHER_ONE')
    srv_control.config_srv_id(step, 'LLT', '00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8')
    srv_control.config_srv_opt(step, 'sip-server-addr', '2001:db8::1,2001:db8::2')
    srv_control.config_srv_opt(step,
                               'new-posix-timezone',
                               'EST5EDT4\\,M3.2.0/02:00\\,M11.1.0/02:00')
    # WRONG ADDRESS RESERVATION
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.0.5',
                                           '0',
                                           'duid',
                                           '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.generate_config_files(step)

    srv_msg.send_through_http(step,
                              '$(SRV4_ADDR)',
                              '8000',
                              '{"command": "config-test","service": ["dhcp6"], "arguments":  $(SERVER_CONFIG) }')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
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
                                             '3000::1')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_config_write(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '$(SRV4_ADDR)',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_msg.send_through_http(step,
                              '$(SRV4_ADDR)',
                              '8000',
                              '{"command": "list-commands", "service": ["dhcp6"],"arguments": {} }')
    srv_msg.send_through_http(step,
                              '$(SRV4_ADDR)',
                              '8000',
                              '{"command": "config-write", "service": ["dhcp6"],"arguments": {"filename": "config-modified-2017-03-15.json"} } #TODO probably confing file location/name')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::1')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.agent_control_channel(step,
                                      '$(SRV4_ADDR)',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.generate_config_files(step)

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "config-set", "service": ["dhcp6"],"arguments":  $(SERVER_CONFIG) }')

    srv_msg.forge_sleep(step, '$(SLEEP_TIME_2)', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
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
                                             '2001:db8:1::1')

    srv_control.start_srv(step, 'DHCP', 'restarted')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
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
                                             '3000::1')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_reload_config(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '$(SRV4_ADDR)',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
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
                                             '3000::1')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '$(SRV4_ADDR)',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_msg.send_through_http(step,
                              '$(SRV4_ADDR)',
                              '8000',
                              '{"command":"config-reload","service":["dhcp6"],"arguments":{}}')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
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
                                             '2001:db8:1::1')

    srv_control.start_srv(step, 'DHCP', 'restarted')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
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
                                             '2001:db8:1::1')
