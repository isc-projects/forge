"""Kea Control Channel Agent - HTTP"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_control
from features import misc
from features import srv_msg


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_dhcp_disable_timer(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
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
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    srv_msg.send_through_http(step,
                              '$(SRV4_ADDR)',
                              '8000',
                              '{"command": "dhcp-disable","service": ["dhcp4"], "arguments": {"max-period": 5}}')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    srv_msg.forge_sleep(step, '7', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_dhcp_disable(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
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
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    srv_msg.send_through_http(step,
                              '$(SRV4_ADDR)',
                              '8000',
                              '{"command": "dhcp-disable","service": ["dhcp4"]}')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_dhcp_disable_and_enable(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
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
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    srv_msg.send_through_http(step,
                              '$(SRV4_ADDR)',
                              '8000',
                              '{"command": "dhcp-disable","service": ["dhcp4"]}')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    srv_msg.send_through_http(step,
                              '$(SRV4_ADDR)',
                              '8000',
                              '{"command": "dhcp-enable","service": ["dhcp4"]}')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_config_set_basic(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
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
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '$(SRV4_ADDR)',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.generate_config_files(step)

    srv_msg.send_through_http(step,
                              '$(SRV4_ADDR)',
                              '8000',
                              '{"command": "config-set", "service": ["dhcp4"], "arguments":  $(SERVER_CONFIG) }')
    srv_msg.send_through_http(step,
                              '$(SRV4_ADDR)',
                              '8000',
                              '{"command": "list-commands", "service": ["dhcp4"],"arguments":  $(SERVER_CONFIG) }')

    srv_msg.forge_sleep(step, '$(SLEEP_TIME_2)', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_change_socket_during_reconfigure(step):
    # change address test needed also
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
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
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.51.0/24', '192.168.51.1-192.168.51.1')
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
                              '{"command": "config-set", "service": ["dhcp4"],"arguments":  $(SERVER_CONFIG) }')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    srv_msg.send_through_http(step,
                              '$(SRV4_ADDR)',
                              '8000',
                              '{"command":"list-commands","arguments": {} }')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_after_restart_load_config_file(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
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
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.agent_control_channel(step,
                                      '$(SRV4_ADDR)',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.generate_config_files(step)

    srv_msg.send_through_http(step,
                              '$(SRV4_ADDR)',
                              '8000',
                              '{"command": "config-set", "service": ["dhcp4"],"arguments":  $(SERVER_CONFIG) }')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    srv_control.start_srv(step, 'DHCP', 'restarted')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_get_config(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
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
                              '{"command": "config-get","service":["dhcp4"],"arguments": {} }')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.kea_only
@pytest.mark.disabled
def test_control_channel_http_test_config(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
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
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.agent_control_channel(step,
                                      '$(SRV4_ADDR)',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket_ANOTHER_ONE')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'my.domain.com')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-name',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'address', '192.168.50.5')
    srv_control.generate_config_files(step)

    srv_msg.send_through_http(step,
                              '$(SRV4_ADDR)',
                              '8000',
                              '{"command": "config-test","service": ["dhcp4"], "arguments":  $(SERVER_CONFIG) }')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.agent_control_channel(step,
                                      '$(SRV4_ADDR)',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket_ANOTHER_ONE')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'my.domain.com')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-name',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'address', '3000::1')
    srv_control.generate_config_files(step)

    srv_msg.send_through_http(step,
                              '$(SRV4_ADDR)',
                              '8000',
                              '{"command": "config-test","service": ["dhcp4"], "arguments":  $(SERVER_CONFIG) }')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_config_write(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
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
                              '{"command": "list-commands", "service": ["dhcp4"],"arguments": {} }')
    srv_msg.send_through_http(step,
                              '$(SRV4_ADDR)',
                              '8000',
                              '{"command": "config-write", "service": ["dhcp4"],"arguments": {"filename": "config-modified-2017-03-15.json"} } #TODO probably confing file location/name')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.agent_control_channel(step,
                                      '$(SRV4_ADDR)',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.generate_config_files(step)

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "config-set", "service": ["dhcp4"],"arguments":  $(SERVER_CONFIG) }')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    srv_control.start_srv(step, 'DHCP', 'restarted')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_reload_config(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
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
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.51.0/24', '192.168.51.1-192.168.51.1')
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
                              '{"command":"config-reload","service":["dhcp4"],"arguments":{}}')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    srv_control.start_srv(step, 'DHCP', 'restarted')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
