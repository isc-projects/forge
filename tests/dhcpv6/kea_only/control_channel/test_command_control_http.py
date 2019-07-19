"""Kea Control Channel Agent - HTTP"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_msg
import srv_control


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_dhcp_disable_timer():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')

    srv_msg.send_ctrl_cmd_via_http('{"command": "dhcp-disable","service": ["dhcp6"], "arguments": {"max-period": 5}}',
                                   '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.forge_sleep('7', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_dhcp_disable():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')

    srv_msg.send_ctrl_cmd_via_http('{"command": "dhcp-disable","service": ["dhcp6"]}',
                                   '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_dhcp_disable_and_enable():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')

    srv_msg.send_ctrl_cmd_via_http('{"command": "dhcp-disable","service": ["dhcp6"]}',
                                   '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.send_ctrl_cmd_via_http('{"command": "dhcp-enable","service": ["dhcp6"]}',
                                   '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_config_set_basic():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    # Server has control agent configured on HTTP connection with address $(SRV4_ADDR):8000 and socket unix path: control_socket.
    srv_control.generate_config_files()

    srv_msg.send_ctrl_cmd_via_http('{"command": "config-set", "service": ["dhcp6"], "arguments":  $(SERVER_CONFIG) }',
                                   '$(SRV4_ADDR)')

    srv_msg.forge_sleep('$(SLEEP_TIME_2)', 'seconds')
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::1')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_change_socket_during_reconfigure():
    # change address test needed also
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    result = srv_msg.send_ctrl_cmd_via_http('{"command":"config-get", "service": ["dhcp6"], "arguments": {} }',
                                            '$(SRV4_ADDR)')
    assert result[0]['result'] == 0

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel(socket_name='control_socket2')
    srv_control.agent_control_channel('$(SRV4_ADDR)',
                                      socket_name='control_socket2')
    srv_control.generate_config_files()

    # reconfigure dhcp6 (new subnet, new socket)
    srv_msg.send_ctrl_cmd_via_http('{"command": "config-set", "service": ["dhcp6"],"arguments":  $(SERVER_CONFIG) }',
                                   '$(SRV4_ADDR)')
    # reconfigure control-agent to switch to new dhcp4 socket
    srv_msg.send_ctrl_cmd_via_http('{"command": "config-set", "arguments":  $(SERVER_CONFIG) }',
                                   '$(SRV4_ADDR)')
    srv_msg.forge_sleep('$(SLEEP_TIME_2)', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::1')

    result = srv_msg.send_ctrl_cmd_via_http('{"command":"config-get", "service": ["dhcp6"], "arguments": {} }',
                                            '$(SRV4_ADDR)')
    assert result[0]['result'] == 0


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_after_restart_load_config_file():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.generate_config_files()

    srv_msg.send_ctrl_cmd_via_http('{"command": "config-set", "service": ["dhcp6"],"arguments":  $(SERVER_CONFIG) }',
                                   '$(SRV4_ADDR)')

    srv_msg.forge_sleep('$(SLEEP_TIME_2)', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::1')

    srv_control.start_srv('DHCP', 'restarted')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_get_config():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_http('{"command": "config-get","service":["dhcp6"],"arguments": {} }',
                                   '$(SRV4_ADDR)')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_test_config():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_prefix('2001:db8:1::', '0', '90', '96')
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.config_srv_id('LLT', '00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8')
    srv_control.config_srv_opt('sip-server-addr', '2001:db8::1,2001:db8::2')
    srv_control.config_srv_opt('new-posix-timezone', r'EST5EDT4\\,M3.2.0/02:00\\,M11.1.0/02:00')
    srv_control.host_reservation_in_subnet('address',
                                           '3000::1',
                                           '0',
                                           'duid',
                                           '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.generate_config_files()

    srv_msg.send_ctrl_cmd_via_http('{"command": "config-test","service": ["dhcp6"], "arguments":  $(SERVER_CONFIG) }',
                                   '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_prefix('2001:db8:1::', '0', '90', '96')
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.config_srv_id('LLT', '00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8')
    srv_control.config_srv_opt('sip-server-addr', '2001:db8::1,2001:db8::2')
    srv_control.config_srv_opt('new-posix-timezone', r'EST5EDT4\\,M3.2.0/02:00\\,M11.1.0/02:00')
    # WRONG ADDRESS RESERVATION
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.0.5',
                                           '0',
                                           'duid',
                                           '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.generate_config_files()

    response = srv_msg.send_ctrl_cmd_via_http('{"command": "config-test","service": ["dhcp6"], "arguments":  $(SERVER_CONFIG) }',
                                              '$(SRV4_ADDR)',
                                              exp_result=1)
    assert "invalid prefix '192.168.0.5' for new IPv6 reservation" in response[0]['text']

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_config_write():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_http('{"command": "list-commands", "service": ["dhcp6"],"arguments": {} }',
                                   '$(SRV4_ADDR)')
    srv_msg.send_ctrl_cmd_via_http('{"command": "config-write", "service": ["dhcp6"],"arguments": {"filename": "config-modified-2017-03-15.json"}}',  # TODO probably confing file location/name',
                                   '$(SRV4_ADDR)')
    # TODO: it seems that the code here is not finished

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.generate_config_files()

    srv_msg.send_ctrl_cmd_via_socket('{"command": "config-set", "service": ["dhcp6"],"arguments":  $(SERVER_CONFIG) }')

    srv_msg.forge_sleep('$(SLEEP_TIME_2)', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::1')

    srv_control.start_srv('DHCP', 'restarted')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_http_reload_config():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_msg.send_ctrl_cmd_via_http('{"command":"config-reload","service":["dhcp6"],"arguments":{}}',
                                   '$(SRV4_ADDR)')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::1')

    srv_control.start_srv('DHCP', 'restarted')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::1')
