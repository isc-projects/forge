"""Kea Control Channel Agent - HTTP"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_msg
import srv_control


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_dhcp_disable_timer():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    srv_msg.send_ctrl_cmd_via_http('{"command": "dhcp-disable","service": ["dhcp4"], "arguments": {"max-period": 5}}',
                                   '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.forge_sleep('7', 'seconds')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_dhcp_disable():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    srv_msg.send_ctrl_cmd_via_http('{"command": "dhcp-disable","service": ["dhcp4"]}',
                                   '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_dhcp_disable_and_enable():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    srv_msg.send_ctrl_cmd_via_http('{"command": "dhcp-disable","service": ["dhcp4"]}',
                                   '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.send_ctrl_cmd_via_http('{"command": "dhcp-enable","service": ["dhcp4"]}',
                                   '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_config_set_basic():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.generate_config_files()

    srv_msg.send_ctrl_cmd_via_http('{"command": "config-set", "service": ["dhcp4"], "arguments":  $(SERVER_CONFIG) }',
                                   '$(SRV4_ADDR)')
    srv_msg.send_ctrl_cmd_via_http('{"command": "list-commands", "service": ["dhcp4"],"arguments":  $(SERVER_CONFIG) }',
                                   '$(SRV4_ADDR)')

    srv_msg.forge_sleep('$(SLEEP_TIME_2)', 'seconds')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_change_socket_during_reconfigure():
    # change address test needed also
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    result = srv_msg.send_ctrl_cmd_via_http('{"command":"config-get", "service": ["dhcp4"], "arguments": {} }',
                                            '$(SRV4_ADDR)')
    assert result[0]['result'] == 0

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.open_control_channel(socket_name='control_socket2')
    srv_control.agent_control_channel('$(SRV4_ADDR)',
                                      socket_name='control_socket2')
    srv_control.generate_config_files()

    # reconfigure dhcp4 (new subnet, new socket)
    srv_msg.send_ctrl_cmd_via_http('{"command": "config-set", "service": ["dhcp4"],"arguments":  $(SERVER_CONFIG) }',
                                   '$(SRV4_ADDR)')
    # reconfigure control-agent to switch to new dhcp4 socket
    srv_msg.send_ctrl_cmd_via_http('{"command": "config-set", "arguments":  $(SERVER_CONFIG) }',
                                   '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    result = srv_msg.send_ctrl_cmd_via_http('{"command":"config-get", "service": ["dhcp4"], "arguments": {} }',
                                            '$(SRV4_ADDR)')
    assert result[0]['result'] == 0


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_after_restart_load_config_file():

    # initial configuration is taken from file
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    # now configuration is set over control-agent
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.generate_config_files()

    srv_msg.send_ctrl_cmd_via_http('{"command": "config-set", "service": ["dhcp4"],"arguments":  $(SERVER_CONFIG) }',
                                   '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    # and now goes restart so configuration again is taken from files
    srv_control.start_srv('DHCP', 'restarted')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_get_config():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_http('{"command": "config-get","service":["dhcp4"],"arguments": {} }',
                                   '$(SRV4_ADDR)')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.kea_only
@pytest.mark.disabled
def test_control_channel_http_test_config():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('qualifying-suffix', 'my.domain.com')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-name',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.host_reservation_in_subnet_add_value('0', '0', 'address', '192.168.50.5')
    srv_control.generate_config_files()

    srv_msg.send_ctrl_cmd_via_http('{"command": "config-test","service": ["dhcp4"], "arguments":  $(SERVER_CONFIG) }',
                                   '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('qualifying-suffix', 'my.domain.com')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-name',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.host_reservation_in_subnet_add_value('0', '0', 'address', '3000::1')
    srv_control.generate_config_files()

    srv_msg.send_ctrl_cmd_via_http('{"command": "config-test","service": ["dhcp4"], "arguments":  $(SERVER_CONFIG) }',
                                   '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_config_write():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_http('{"command": "list-commands", "service": ["dhcp4"],"arguments": {} }',
                                   '$(SRV4_ADDR)')
    srv_msg.send_ctrl_cmd_via_http('{"command": "config-write", "service": ["dhcp4"],"arguments": {"filename": "config-modified-2017-03-15.json"}}',  # TODO probably confing file location/name',
                                   '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.generate_config_files()

    srv_msg.send_ctrl_cmd_via_socket('{"command": "config-set", "service": ["dhcp4"],"arguments":  $(SERVER_CONFIG) }')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    srv_control.start_srv('DHCP', 'restarted')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_reload_config():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_msg.send_ctrl_cmd_via_http('{"command":"config-reload","service":["dhcp4"],"arguments":{}}',
                                   '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    srv_control.start_srv('DHCP', 'restarted')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
