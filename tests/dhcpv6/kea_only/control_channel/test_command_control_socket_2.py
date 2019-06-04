"""Kea Control Channel - socket"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_msg
import srv_control
from forge_cfg import world


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_socket_config_get():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel()

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "config-get","arguments": {}}')
    # Using UNIX socket on server in path control_socket send {"command": "list-commands","arguments": {}}
    # compare json result with config file


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_socket_config_test():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel()
    # To global section of the config add file line: "expired-leases-processing":{"flush-reclaimed-timer-wait-time": 0,"hold-reclaimed-time": 0,"max-reclaim-leases": 100,"max-reclaim-time": 0,"reclaim-timer-wait-time": 0,"unwarned-reclaim-cycles": 5}
    # To global section of the config add file line: "expired-leases-processing":{"flush-reclaimed-timer-wait-time": 0,"hold-reclaimed-time": 0,"max-reclaim-leases": 100,"max-reclaim-time": 0,"reclaim-timer-wait-time": 0,"unwarned-reclaim-cycles": 5}

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.config_srv_prefix('2001:db8:1::', '0', '90', '96')
    srv_control.open_control_channel('control_socket_ANOTHER_ONE')
    srv_control.config_srv_id('LLT', '00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8')
    srv_control.config_srv_opt('sip-server-addr', '2001:db8::1,2001:db8::2')
    srv_control.config_srv_opt('new-posix-timezone', r'EST5EDT4\\,M3.2.0/02:00\\,M11.1.0/02:00')
    srv_control.host_reservation_in_subnet('address',
                                           '3000::1',
                                           '0',
                                           'duid',
                                           '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.generate_config_files()

    # Sleep for 10 seconds.
    srv_msg.send_ctrl_cmd_via_socket('{"command": "config-test","arguments": $(SERVER_CONFIG) }')
    # should be ok

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.config_srv_prefix('2001:db8:1::', '0', '90', '96')
    srv_control.open_control_channel('control_socket_ANOTHER_ONE')
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
    #
    srv_msg.send_ctrl_cmd_via_socket('{"command": "config-test","arguments": $(SERVER_CONFIG) }', exp_result=1)
    # should NOT be ok


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_socket_config_write():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
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
    srv_control.generate_config_files()

    srv_msg.send_ctrl_cmd_via_socket('{"command": "config-set","arguments":  $(SERVER_CONFIG) }')
    srv_msg.send_ctrl_cmd_via_socket({"command": "config-write",
                                      "arguments": {"filename": world.f_cfg.get_dhcp_conf_path()}})

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:22')
    srv_msg.client_does_include('Client', None, 'client-id')
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

    # Using UNIX socket on server in path control_socket send {"command": "list-commands","arguments": {}}
    # Using UNIX socket on server in path control_socket send {"command": "config-write","parameters":  { "filename": "abc"} }
    # Using UNIX socket on server in path control_socket send {"command": "config-write","arguments":  { "filename": "whatever"} }
    # Using UNIX socket on server in path control_socket send {"command": "config-write","arguments":  { "filename": "installed/git/etc/kea/kea.conf"} }
    # Pause the Test.
    srv_control.start_srv('DHCP', 'restarted')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:33')
    srv_msg.client_does_include('Client', None, 'client-id')
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
def test_control_channel_socket_config_reload():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "list-commands","arguments": {}}')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    # Generate server configuration file.
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "config-reload","arguments":  {} }')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
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
