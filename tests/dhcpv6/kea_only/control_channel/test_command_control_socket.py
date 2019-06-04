"""Kea Control Channel - socket"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_msg
import misc
import srv_control


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_onlyn
def test_control_channel_socket_dhcp_disable_timer():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel()
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

    srv_msg.send_ctrl_cmd_via_socket('{"command": "dhcp-disable", "arguments": {"max-period": 5}}')

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
def test_control_channel_socket_dhcp_disable():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel()
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
    srv_msg.send_ctrl_cmd_via_socket('{"command": "dhcp-disable" }')

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
def test_control_channel_socket_dhcp_disable_and_enable():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel()
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

    srv_msg.send_ctrl_cmd_via_socket('{"command": "dhcp-disable" }')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.send_ctrl_cmd_via_socket('{"command": "dhcp-enable" }')

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
def test_control_channel_socket_config_set_basic():
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


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_socket_change_socket_during_reconfigure():
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
    srv_control.open_control_channel('control_socket2')
    srv_control.generate_config_files()

    srv_msg.send_ctrl_cmd_via_socket('{"command": "config-set","arguments":  $(SERVER_CONFIG) }')

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
    # this should fail as socket has been changed
    srv_msg.send_ctrl_cmd_via_socket('{"command": "list-commands","arguments": {}}', exp_failed=True)
    # this should pass (with new socket)
    srv_msg.send_ctrl_cmd_via_socket('{"command": "list-commands","arguments": {}}',
                                     socket_name='control_socket2')
    srv_msg.json_response_parsing('arguments', None, 'leases-reclaim')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_socket_after_restart_load_config_file():

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
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
@pytest.mark.disabled
def test_control_channel_socket_big_config_file():
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
    srv_control.config_srv_subnet('2001:db8:1:1::/64', '2001:db8:1:1::1-2001:db8:1:1::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:1:2::/64',
                                                       '2001:db8:1:2::1-2001:db8:1:2::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:1:3::/64',
                                                       '2001:db8:1:3::1-2001:db8:1:3::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:1:4::/64',
                                                       '2001:db8:1:4::1-2001:db8:1:4::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:1:5::/64',
                                                       '2001:db8:1:5::1-2001:db8:1:5::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:1:6::/64',
                                                       '2001:db8:1:6::1-2001:db8:1:6::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:1:7::/64',
                                                       '2001:db8:1:7::1-2001:db8:1:7::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:1:8::/64',
                                                       '2001:db8:1:8::1-2001:db8:1:8::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:1:9::/64',
                                                       '2001:db8:1:9::1-2001:db8:1:9::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:1:10::/64',
                                                       '2001:db8:1:10::1-2001:db8:1:10::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:1:11::/64',
                                                       '2001:db8:1:11::1-2001:db8:1:11::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:1:12::/64',
                                                       '2001:db8:1:12::1-2001:db8:1:12::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:1:13::/64',
                                                       '2001:db8:1:13::1-2001:db8:1:13::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:1:14::/64',
                                                       '2001:db8:1:14::1-2001:db8:1:14::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:1:15::/64',
                                                       '2001:db8:1:15::1-2001:db8:1:15::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:1:16::/64',
                                                       '2001:db8:1:16::1-2001:db8:1:16::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:1:17::/64',
                                                       '2001:db8:1:17::1-2001:db8:1:17::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:1:18::/64',
                                                       '2001:db8:1:18::1-2001:db8:1:18::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:1:19::/64',
                                                       '2001:db8:1:19::1-2001:db8:1:19::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:1:20::/64',
                                                       '2001:db8:1:20::1-2001:db8:1:20::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:1:21::/64',
                                                       '2001:db8:1:21::1-2001:db8:1:21::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:1:22::/64',
                                                       '2001:db8:1:22::1-2001:db8:1:22::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:1:23::/64',
                                                       '2001:db8:1:23::1-2001:db8:1:23::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:1:24::/64',
                                                       '2001:db8:1:24::1-2001:db8:1:24::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:1:25::/64',
                                                       '2001:db8:1:25::1-2001:db8:1:25::1')

    srv_control.config_srv_opt('preference', '123')
    srv_control.config_srv_opt('sip-server-dns', 'srv1.example.com,srv2.isc.org')
    srv_control.config_srv_opt('dns-servers', '2001:db8::1,2001:db8::2')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv_opt('sip-server-addr', '2001:db8::1,2001:db8::2')
    srv_control.config_srv_opt('nisp-servers', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv_opt('nis-servers', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv_opt('nis-domain-name', 'ntp.example.com')
    srv_control.config_srv_opt('nisp-domain-name', 'ntp.example.com')
    srv_control.config_srv_opt('sntp-servers', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv_opt('information-refresh-time', '12345678')
    srv_control.config_srv_opt('unicast', '3000::66')
    srv_control.config_srv_opt('bcmcs-server-dns', 'very.good.domain.name.com')
    srv_control.config_srv_opt('bcmcs-server-addr', '3000::66,3000::77')
    srv_control.config_srv_opt('pana-agent', '3000::66,3000::77')
    srv_control.config_srv_opt('new-posix-timezone', 'EST5EDT4')
    srv_control.config_srv_opt('new-tzdb-timezone', 'Europe/Zurich')
    srv_control.config_srv_opt('bootfile-url', 'http://www.kea.isc.org')
    srv_control.config_srv_opt('bootfile-param', '000B48656C6C6F20776F726C640003666F6F')
    srv_control.config_srv_opt('erp-local-domain-name', 'erp-domain.isc.org')
    srv_control.config_srv_custom_opt('foo', '100', 'uint8', '123')

    srv_control.config_srv('preference', '0', '123')
    srv_control.config_srv('sip-server-dns', '0', 'srv1.example.com,srv2.isc.org')
    srv_control.config_srv('dns-servers', '0', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('domain-search', '0', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv('sip-server-addr', '0', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('nisp-servers', '0', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-servers', '0', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-domain-name', '0', 'ntp.example.com')
    srv_control.config_srv('nisp-domain-name', '0', 'ntp.example.com')
    srv_control.config_srv('sntp-servers', '0', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('information-refresh-time', '0', '12345678')
    srv_control.config_srv('unicast', '0', '3000::66')
    srv_control.config_srv('bcmcs-server-dns', '0', 'very.good.domain.name.com')
    srv_control.config_srv('bcmcs-server-addr', '0', '3000::66,3000::77')
    srv_control.config_srv('pana-agent', '0', '3000::66,3000::77')
    srv_control.config_srv('new-posix-timezone', '0', 'EST5EDT4')
    srv_control.config_srv('new-tzdb-timezone', '0', 'Europe/Zurich')
    srv_control.config_srv('bootfile-url', '0', 'http://www.kea.isc.org')
    srv_control.config_srv('bootfile-param', '0', '000B48656C6C6F20776F726C640003666F6F')
    srv_control.config_srv('erp-local-domain-name', '0', 'erp-domain.isc.org')
    srv_control.config_srv('domain-search', '0', 'subnet.example.com')
    srv_control.config_srv_custom_opt('foo', '101', 'uint8', '123')

    srv_control.config_srv_custom_opt('foo', '109', 'uint16', '12313')
    srv_control.config_srv_custom_opt('foo', '111', 'uint16', '12313')
    srv_control.config_srv_custom_opt('foo', '112', 'uint16', '12312')
    srv_control.config_srv_custom_opt('foo', '113', 'uint16', '12313')
    srv_control.config_srv_custom_opt('foo', '114', 'uint16', '12311')
    srv_control.config_srv_custom_opt('foo', '115', 'uint16', '1231')
    srv_control.config_srv_custom_opt('foo', '116', 'uint16', '12313')
    srv_control.config_srv_custom_opt('foo', '117', 'uint16', '1231')
    srv_control.config_srv_custom_opt('foo', '118', 'uint16', '1231')
    srv_control.config_srv_custom_opt('foo', '119', 'uint16', '1231')
    srv_control.config_srv_custom_opt('foo', '120', 'uint16', '1231')
    srv_control.config_srv_custom_opt('foo', '121', 'uint16', '12313')
    srv_control.config_srv_custom_opt('foo', '122', 'uint16', '1231')

    srv_control.config_srv_custom_opt('fowqrgfo',
                                      '123',
                                      'string',
                                      '123123123456789edrftgyhujikrctvybnui23')
    srv_control.config_srv_custom_opt('fowefwefwvro',
                                      '124',
                                      'string',
                                      '12312312!@#$%^&*(*&^%$JKHBGV<&IMUNTY3')
    srv_control.config_srv_custom_opt('fowerwerfvro',
                                      '125',
                                      'string',
                                      '12312312<IMU^N%$^HGB$VTBYNU&I2')
    srv_control.config_srv_custom_opt('foogretnbu8oimu',
                                      '126',
                                      'string',
                                      '123123122@#%$#^$&%*I*KJHNBV3')
    srv_control.config_srv_custom_opt('foo', '127', 'string', '123123123J%^$HBYU*N(KIJMNUTYBRT1')
    srv_control.config_srv_custom_opt('fojumnygbfcdo',
                                      '128',
                                      'string',
                                      '123123J&%MNY$TBERVF+{\"?PO:><JKMHJ123')
    srv_control.config_srv_custom_opt('fbtrbrtn78980oo',
                                      '129',
                                      'string',
                                      '12312312<IMU^TNYRBFVD3')
    srv_control.config_srv_custom_opt('foo8iumjyhgnfv',
                                      '130',
                                      'string',
                                      '1231231<I&MYUTNYHFGVD23')
    srv_control.config_srv_custom_opt('foumhnbo', '131', 'string', '123123123')
    srv_control.config_srv_custom_opt('fomunhygbvo', '132', 'string', '123123123')
    srv_control.config_srv_custom_opt('fmuhnoo', '133', 'string', '123123123')
    srv_control.config_srv_custom_opt('fomunhgo', '134', 'string', '123123123')
    srv_control.config_srv_custom_opt('foimujhno', '135', 'string', '123123123')
    srv_control.config_srv_custom_opt('dawfwrbrbumobt',
                                      '136',
                                      'string',
                                      '1231231wsedrftgyhujikolp;lokijhgfdszswxdecfvgtbyhnujuyhtgf5rdew23e4r5t6y7u81234567890-=!@#$%^&*()_+{:>}|?><23')
    srv_control.config_srv_custom_opt('dawfwrbrbumobt',
                                      '137',
                                      'string',
                                      '123123123wrexcrvtbuynium435678ui8oikmnbgvfcder5t6y7u8iko,mjnbvcfdxse34r567yu8ijkmn')
    srv_control.config_srv_custom_opt('dawfwrbrbumobt',
                                      '138',
                                      'string',
                                      '12312312i87654e3wsdxcfvgyh7u8ijkmolplk,9j8unbyg6tfr54edswzedcfrtghyujikmolkoiujhyt65rfdesw3')
    srv_control.config_srv_custom_opt('dawfwrbrbumobt',
                                      '139',
                                      'string',
                                      '12312312@!#$R%^TY&*UI()OP_P_)O(*&U^%TR%$#E@Q!3')
    srv_control.config_srv_custom_opt('dawfwrbrbumobt',
                                      '140',
                                      'string',
                                      '1231231wsedrftgyhujikolp;lokijhgfdszswxdecfvgtbyhnujuyhtgf5rdew23e4r5t6y7u81234567890-=!@#$%^&*()_+{:>}|?><23')
    srv_control.config_srv_custom_opt('dawfwrbrbumobt',
                                      '141',
                                      'string',
                                      '123123123wrexcrvtbuynium435678ui8oikmnbgvfcder5t6y7u8iko,mjnbvcfdxse34r567yu8ijkmn')
    srv_control.config_srv_custom_opt('dawfwrbrbumobt',
                                      '142',
                                      'string',
                                      '12312312i87654e3wsdxcfvgyh7u8ijkmolplk,9j8unbyg6tfr54edswzedcfrtghyujikmolkoiujhyt65rfdesw3')
    srv_control.config_srv_custom_opt('dawfwrbrbumobt',
                                      '143',
                                      'string',
                                      '12312312@!#$R%^TY&*UI()OP_P_)O(*&U^%TR%$#E@Q!3')
    srv_control.config_srv_custom_opt('dawfwrbrbumobt',
                                      '144',
                                      'string',
                                      '1231231wsedrftgyhujikolp;lokijhgfdszswxdecfvgtbyhnujuyhtgf5rdew23e4r5t6y7u81234567890-=!@#$%^&*()_+{:>}|?><23')
    srv_control.config_srv_custom_opt('dawfwrbrbumobt',
                                      '145',
                                      'string',
                                      '123123123wrexcrvtbuynium435678ui8oikmnbgvfcder5t6y7u8iko,mjnbvcfdxse34r567yu8ijkmn')
    srv_control.config_srv_custom_opt('dawfwrbrbumobt',
                                      '146',
                                      'string',
                                      '12312312i87654e3wsdxcfvgyh7u8ijkmolplk,9j8unbyg6tfr54edswzedcfrtghyujikmolkoiujhyt65rfdesw3')
    srv_control.config_srv_custom_opt('dawfwrbrbumobt',
                                      '147',
                                      'string',
                                      '12312312@!#$R%^TY&*UI()OP_P_)O(*&U^%TR%$#E@Q!3')
    srv_control.config_srv_custom_opt('dawfwrbrbumobt',
                                      '148',
                                      'string',
                                      '1231231wsedrftgyhujikolp;lokijhgfdszswxdecfvgtbyhnujuyhtgf5rdew23e4r5t6y7u81234567890-=!@#$%^&*()_+{:>}|?><23')
    srv_control.config_srv_custom_opt('dawfwrbrbumobt',
                                      '149',
                                      'string',
                                      '123123123wrexcrvtbuynium435678ui8oikmnbgvfcder5t6y7u8iko,mjnbvcfdxse34r567yu8ijkmn')
    srv_control.config_srv_custom_opt('dawfwrbrbumobt',
                                      '150',
                                      'string',
                                      '12312312i87654e3wsdxcfvgyh7u8ijkmolplk,9j8unbyg6tfr54edswzedcfrtghyujikmolkoiujhyt65rfdesw3')
    srv_control.config_srv_custom_opt('dawfwrbrbumobt',
                                      '151',
                                      'string',
                                      '12312312@!#$R%^TY&*UI()OP_P_)O(*&U^%TR%$#E@Q!3')

    # Server is configured with custom option dawfwrbrbumobt/152 with type string and value 12312312@!#$R%^TY&*UI()OP_P_)O(*&U^%TR%$#E@Q!3.
    # Server is configured with custom option dawfwrbrbumobt/153 with type string and value 1231231wsedrftgyhujikolp;lokijhgfdszswxdecfvgtbyhnujuyhtgf5rdew23e4r5t6y7u81234567890-=!@#$%^&*()_+{:>}|?><23.
    # Server is configured with custom option dawfwrbrbumobt/154 with type string and value 123123123wrexcrvtbuynium435678ui8oikmnbgvfcder5t6y7u8iko,mjnbvcfdxse34r567yu8ijkmn.
    # Server is configured with custom option dawfwrbrbumobt/155 with type string and value 12312312i87654e3wsdxcfvgyh7u8ijkmolplk,9j8unbyg6tfr54edswzedcfrtghyujikmolkoiujhyt65rfdesw3.
    # Server is configured with custom option dawfwrbrbumobt/156 with type string and value 12312312@!#$R%^TY&*UI()OP_P_)O(*&U^%TR%$#E@Q!3.
    # Server is configured with custom option dawfwrbrbumobt/157 with type string and value 1231231wsedrftgyhujikolp;lokijhgfdszswxdecfvgtbyhnujuyhtgf5rdew23e4r5t6y7u81234567890-=!@#$%^&*()_+{:>}|?><23.
    # Server is configured with custom option dawfwrbrbumobt/158 with type string and value 123123123wrexcrvtbuynium435678ui8oikmnbgvfcder5t6y7u8iko,mjnbvcfdxse34r567yu8ijkmn.
    # Server is configured with custom option dawfwrbrbumobt/159 with type string and value 12312312i87654e3wsdxcfvgyh7u8ijkmolplk,9j8unbyg6tfr54edswzedcfrtghyujikmolkoiujhyt65rfdesw3.
    # Server is configured with custom option dawfwrbrbumobt/160 with type string and value 12312312@!#$R%^TY&*UI()OP_P_)O(*&U^%TR%$#E@Q!3.
    #
    # Server is configured with custom option dawfwrbrbumobt/161 with type string and value 12312312@!#$R%^TY&*UI()OP_P_)O(*&U^%TR%$#E@Q!3.
    # Server is configured with custom option dawfwrbrbumobt/162 with type string and value 1231231wsedrftgyhujikolp;lokijhgfdszswxdecfvgtbyhnujuyhtgf5rdew23e4r5t6y7u81234567890-=!@#$%^&*()_+{:>}|?><23.
    # Server is configured with custom option dawfwrbrbumobt/163 with type string and value 123123123wrexcrvtbuynium435678ui8oikmnbgvfcder5t6y7u8iko,mjnbvcfdxse34r567yu8ijkmn.
    # Server is configured with custom option dawfwrbrbumobt/164 with type string and value 12312312i87654e3wsdxcfvgyh7u8ijkmolplk,9j8unbyg6tfr54edswzedcfrtghyujikmolkoiujhyt65rfdesw3.
    # Server is configured with custom option dawfwrbrbumobt/165 with type string and value 12312312@!#$R%^TY&*UI()OP_P_)O(*&U^%TR%$#E@Q!3.
    # Server is configured with custom option dawfwrbrbumobt/166 with type string and value 1231231wsedrftgyhujikolp;lokijhgfdszswxdecfvgtbyhnujuyhtgf5rdew23e4r5t6y7u81234567890-=!@#$%^&*()_+{:>}|?><23.
    # Server is configured with custom option dawfwrbrbumobt/167 with type string and value 123123123wrexcrvtbuynium435678ui8oikmnbgvfcder5t6y7u8iko,mjnbvcfdxse34r567yu8ijkmn.
    # Server is configured with custom option dawfwrbrbumobt/168 with type string and value 12312312i87654e3wsdxcfvgyh7u8ijkmolplk,9j8unbyg6tfr54edswzedcfrtghyujikmolkoiujhyt65rfdesw3.
    # Server is configured with custom option dawfwrbrbumobt/169 with type string and value 12312312@!#$R%^TY&*UI()OP_P_)O(*&U^%TR%$#E@Q!3.
    # Server is configured with preference option in subnet 1 with value 123.
    # Server is configured with sip-server-dns option in subnet 1 with value srv1.example.com,srv2.isc.org.
    # Server is configured with dns-servers option in subnet 1 with value 2001:db8::1,2001:db8::2.
    # Server is configured with domain-search option in subnet 1 with value domain1.example.com,domain2.isc.org.
    # Server is configured with sip-server-addr option in subnet 1 with value 2001:db8::1,2001:db8::2.
    # Server is configured with nisp-servers option in subnet 1 with value 2001:db8::abc,3000::1,2000::1234.
    # Server is configured with nis-servers option in subnet 1 with value 2001:db8::abc,3000::1,2000::1234.
    # Server is configured with nis-domain-name option in subnet 1 with value ntp.example.com.
    # Server is configured with nisp-domain-name option in subnet 1 with value ntp.example.com.
    # Server is configured with sntp-servers option in subnet 1 with value 2001:db8::abc,3000::1,2000::1234.
    # Server is configured with information-refresh-time option in subnet 1 with value 12345678.
    # Server is configured with unicast option in subnet 1 with value 3000::66.
    # Server is configured with bcmcs-server-dns option in subnet 1 with value very.good.domain.name.com.
    # Server is configured with bcmcs-server-addr option in subnet 1 with value 3000::66,3000::77.
    # Server is configured with pana-agent option in subnet 1 with value 3000::66,3000::77.
    # Server is configured with new-posix-timezone option in subnet 1 with value EST5EDT4.
    # Server is configured with new-tzdb-timezone option in subnet 1 with value Europe/Zurich.
    # Server is configured with bootfile-url option in subnet 1 with value http://www.kea.isc.org.
    # Server is configured with bootfile-param option in subnet 1 with value 000B48656C6C6F20776F726C640003666F6F.
    # Server is configured with erp-local-domain-name option in subnet 1 with value erp-domain.isc.org.
    # Server is configured with domain-search option in subnet 0 with value subnet.example.com.
    # Server is configured with custom option foo/102 with type uint8 and value 123.
    # Server is configured with preference option in subnet 2 with value 123.
    # Server is configured with sip-server-dns option in subnet 2 with value srv1.example.com,srv2.isc.org.
    # Server is configured with dns-servers option in subnet 2 with value 2001:db8::1,2001:db8::2.
    # Server is configured with domain-search option in subnet 2 with value domain1.example.com,domain2.isc.org.
    # Server is configured with sip-server-addr option in subnet 2 with value 2001:db8::1,2001:db8::2.
    # Server is configured with nisp-servers option in subnet 2 with value 2001:db8::abc,3000::1,2000::1234.
    # Server is configured with nis-servers option in subnet 2 with value 2001:db8::abc,3000::1,2000::1234.
    # Server is configured with nis-domain-name option in subnet 2 with value ntp.example.com.
    # Server is configured with nisp-domain-name option in subnet 2 with value ntp.example.com.
    # Server is configured with sntp-servers option in subnet 2 with value 2001:db8::abc,3000::1,2000::1234.
    # Server is configured with information-refresh-time option in subnet 2 with value 12345678.
    # Server is configured with unicast option in subnet 2 with value 3000::66.
    # Server is configured with bcmcs-server-dns option in subnet 2 with value very.good.domain.name.com.
    # Server is configured with bcmcs-server-addr option in subnet 2 with value 3000::66,3000::77.
    # Server is configured with pana-agent option in subnet 2 with value 3000::66,3000::77.
    # Server is configured with new-posix-timezone option in subnet 2 with value EST5EDT4.
    # Server is configured with new-tzdb-timezone option in subnet 2 with value Europe/Zurich.
    # Server is configured with bootfile-url option in subnet 2 with value http://www.kea.isc.org.
    # Server is configured with bootfile-param option in subnet 2 with value 000B48656C6C6F20776F726C640003666F6F.
    # Server is configured with erp-local-domain-name option in subnet 2 with value erp-domain.isc.org.
    # Server is configured with domain-search option in subnet 0 with value subnet.example.com.
    # Server is configured with custom option foo/103 with type uint8 and value 123.
    # Server is configured with preference option in subnet 3 with value 123.
    # Server is configured with sip-server-dns option in subnet 3 with value srv1.example.com,srv2.isc.org.
    # Server is configured with dns-servers option in subnet 3 with value 2001:db8::1,2001:db8::2.
    # Server is configured with domain-search option in subnet 3 with value domain1.example.com,domain2.isc.org.
    # Server is configured with sip-server-addr option in subnet 3 with value 2001:db8::1,2001:db8::2.
    # Server is configured with nisp-servers option in subnet 3 with value 2001:db8::abc,3000::1,2000::1234.
    # Server is configured with nis-servers option in subnet 3 with value 2001:db8::abc,3000::1,2000::1234.
    # Server is configured with nis-domain-name option in subnet 3 with value ntp.example.com.
    # Server is configured with nisp-domain-name option in subnet 3 with value ntp.example.com.
    # Server is configured with sntp-servers option in subnet 3 with value 2001:db8::abc,3000::1,2000::1234.
    # Server is configured with information-refresh-time option in subnet 3 with value 12345678.
    # Server is configured with unicast option in subnet 3 with value 3000::66.
    # Server is configured with bcmcs-server-dns option in subnet 3 with value very.good.domain.name.com.
    # Server is configured with bcmcs-server-addr option in subnet 3 with value 3000::66,3000::77.
    # Server is configured with pana-agent option in subnet 3 with value 3000::66,3000::77.
    # Server is configured with new-posix-timezone option in subnet 3 with value EST5EDT4.
    # Server is configured with new-tzdb-timezone option in subnet 3 with value Europe/Zurich.
    # Server is configured with bootfile-url option in subnet 3 with value http://www.kea.isc.org.
    # Server is configured with bootfile-param option in subnet 3 with value 000B48656C6C6F20776F726C640003666F6F.
    # Server is configured with erp-local-domain-name option in subnet 3 with value erp-domain.isc.org.
    # Server is configured with domain-search option in subnet 0 with value subnet.example.com.
    # Server is configured with custom option foo/104 with type uint8 and value 123.
    #
    #
    # Server is configured with preference option in subnet 4 with value 123.
    # Server is configured with sip-server-dns option in subnet 4 with value srv1.example.com,srv2.isc.org.
    # Server is configured with dns-servers option in subnet 4 with value 2001:db8::1,2001:db8::2.
    # Server is configured with domain-search option in subnet 4 with value domain1.example.com,domain2.isc.org.
    # Server is configured with sip-server-addr option in subnet 4 with value 2001:db8::1,2001:db8::2.
    # Server is configured with nisp-servers option in subnet 4 with value 2001:db8::abc,3000::1,2000::1234.
    # Server is configured with nis-servers option in subnet 4 with value 2001:db8::abc,3000::1,2000::1234.
    # Server is configured with nis-domain-name option in subnet 4 with value ntp.example.com.
    # Server is configured with nisp-domain-name option in subnet 4 with value ntp.example.com.
    # Server is configured with sntp-servers option in subnet 4 with value 2001:db8::abc,3000::1,2000::1234.
    # Server is configured with information-refresh-time option in subnet 4 with value 12345678.
    # Server is configured with unicast option in subnet 4 with value 3000::66.
    # Server is configured with bcmcs-server-dns option in subnet 4 with value very.good.domain.name.com.
    # Server is configured with bcmcs-server-addr option in subnet 4 with value 3000::66,3000::77.
    # Server is configured with pana-agent option in subnet 4 with value 3000::66,3000::77.
    # Server is configured with new-posix-timezone option in subnet 4 with value EST5EDT4.
    # Server is configured with new-tzdb-timezone option in subnet 4 with value Europe/Zurich.
    # Server is configured with bootfile-url option in subnet 4 with value http://www.kea.isc.org.
    # Server is configured with bootfile-param option in subnet 4 with value 000B48656C6C6F20776F726C640003666F6F.
    # Server is configured with erp-local-domain-name option in subnet 4 with value erp-domain.isc.org.
    # Server is configured with domain-search option in subnet 0 with value subnet.example.com.
    # Server is configured with custom option foo/105 with type uint8 and value 123.
    srv_control.config_srv('preference', '5', '123')
    srv_control.config_srv('sip-server-dns', '5', 'srv1.example.com,srv2.isc.org')
    srv_control.config_srv('dns-servers', '5', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('domain-search', '5', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv('sip-server-addr', '5', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('nisp-servers', '5', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-servers', '5', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-domain-name', '5', 'ntp.example.com')
    srv_control.config_srv('nisp-domain-name', '5', 'ntp.example.com')
    srv_control.config_srv('sntp-servers', '5', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('information-refresh-time', '5', '12345678')
    srv_control.config_srv('unicast', '5', '3000::66')
    srv_control.config_srv('bcmcs-server-dns', '5', 'very.good.domain.name.com')
    srv_control.config_srv('bcmcs-server-addr', '5', '3000::66,3000::77')
    srv_control.config_srv('pana-agent', '5', '3000::66,3000::77')
    srv_control.config_srv('new-posix-timezone', '5', 'EST5EDT4')
    srv_control.config_srv('new-tzdb-timezone', '5', 'Europe/Zurich')
    srv_control.config_srv('bootfile-url', '5', 'http://www.kea.isc.org')
    srv_control.config_srv('bootfile-param', '5', '000B48656C6C6F20776F726C640003666F6F')
    srv_control.config_srv('erp-local-domain-name', '5', 'erp-domain.isc.org')
    srv_control.config_srv('domain-search', '0', 'subnet.example.com')
    srv_control.config_srv_custom_opt('foo', '106', 'uint8', '123')

    srv_control.config_srv('preference', '6', '123')
    srv_control.config_srv('sip-server-dns', '6', 'srv1.example.com,srv2.isc.org')
    srv_control.config_srv('dns-servers', '6', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('domain-search', '6', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv('sip-server-addr', '6', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('nisp-servers', '6', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-servers', '6', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-domain-name', '6', 'ntp.example.com')
    srv_control.config_srv('nisp-domain-name', '6', 'ntp.example.com')
    srv_control.config_srv('sntp-servers', '6', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('information-refresh-time', '6', '12345678')
    srv_control.config_srv('unicast', '6', '3000::66')
    srv_control.config_srv('bcmcs-server-dns', '6', 'very.good.domain.name.com')
    srv_control.config_srv('bcmcs-server-addr', '6', '3000::66,3000::77')
    srv_control.config_srv('pana-agent', '6', '3000::66,3000::77')
    srv_control.config_srv('new-posix-timezone', '6', 'EST5EDT4')
    srv_control.config_srv('new-tzdb-timezone', '6', 'Europe/Zurich')
    srv_control.config_srv('bootfile-url', '6', 'http://www.kea.isc.org')
    srv_control.config_srv('bootfile-param', '6', '000B48656C6C6F20776F726C640003666F6F')
    srv_control.config_srv('erp-local-domain-name', '6', 'erp-domain.isc.org')
    srv_control.config_srv('domain-search', '0', 'subnet.example.com')
    srv_control.config_srv_custom_opt('foo', '108', 'uint8', '123')

    srv_control.config_srv('preference', '7', '123')
    srv_control.config_srv('sip-server-dns', '7', 'srv1.example.com,srv2.isc.org')
    srv_control.config_srv('dns-servers', '7', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('domain-search', '7', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv('sip-server-addr', '7', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('nisp-servers', '7', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-servers', '7', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-domain-name', '7', 'ntp.example.com')
    srv_control.config_srv('nisp-domain-name', '7', 'ntp.example.com')
    srv_control.config_srv('sntp-servers', '7', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('information-refresh-time', '7', '12345678')
    srv_control.config_srv('unicast', '7', '3000::66')
    srv_control.config_srv('bcmcs-server-dns', '7', 'very.good.domain.name.com')
    srv_control.config_srv('bcmcs-server-addr', '7', '3000::66,3000::77')
    srv_control.config_srv('pana-agent', '7', '3000::66,3000::77')
    srv_control.config_srv('new-posix-timezone', '7', 'EST5EDT4')
    srv_control.config_srv('new-tzdb-timezone', '7', 'Europe/Zurich')
    srv_control.config_srv('bootfile-url', '7', 'http://www.kea.isc.org')
    srv_control.config_srv('bootfile-param', '7', '000B48656C6C6F20776F726C640003666F6F')
    srv_control.config_srv('erp-local-domain-name', '7', 'erp-domain.isc.org')
    srv_control.config_srv('domain-search', '0', 'subnet.example.com')
    srv_control.config_srv_custom_opt('foo', '107', 'uint8', '123')

    srv_control.config_srv('preference', '8', '123')
    srv_control.config_srv('sip-server-dns', '8', 'srv1.example.com,srv2.isc.org')
    srv_control.config_srv('dns-servers', '8', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('domain-search', '8', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv('sip-server-addr', '8', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('nisp-servers', '8', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-servers', '8', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-domain-name', '8', 'ntp.example.com')
    srv_control.config_srv('nisp-domain-name', '8', 'ntp.example.com')
    srv_control.config_srv('sntp-servers', '8', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('information-refresh-time', '8', '12345678')
    srv_control.config_srv('unicast', '8', '3000::66')
    srv_control.config_srv('bcmcs-server-dns', '8', 'very.good.domain.name.com')
    srv_control.config_srv('bcmcs-server-addr', '8', '3000::66,3000::77')
    srv_control.config_srv('pana-agent', '8', '3000::66,3000::77')
    srv_control.config_srv('new-posix-timezone', '8', 'EST5EDT4')
    srv_control.config_srv('new-tzdb-timezone', '8', 'Europe/Zurich')
    srv_control.config_srv('bootfile-url', '8', 'http://www.kea.isc.org')
    srv_control.config_srv('bootfile-param', '8', '000B48656C6C6F20776F726C640003666F6F')
    srv_control.config_srv('erp-local-domain-name', '8', 'erp-domain.isc.org')
    srv_control.config_srv('domain-search', '8', 'subnet.example.com')

    srv_control.config_srv('preference', '9', '123')
    srv_control.config_srv('sip-server-dns', '9', 'srv1.example.com,srv2.isc.org')
    srv_control.config_srv('dns-servers', '9', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('domain-search', '9', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv('sip-server-addr', '9', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('nisp-servers', '9', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-servers', '9', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-domain-name', '9', 'ntp.example.com')
    srv_control.config_srv('nisp-domain-name', '9', 'ntp.example.com')
    srv_control.config_srv('sntp-servers', '9', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('information-refresh-time', '9', '12345678')
    srv_control.config_srv('unicast', '9', '3000::66')
    srv_control.config_srv('bcmcs-server-dns', '9', 'very.good.domain.name.com')
    srv_control.config_srv('bcmcs-server-addr', '9', '3000::66,3000::77')
    srv_control.config_srv('pana-agent', '9', '3000::66,3000::77')
    srv_control.config_srv('new-posix-timezone', '9', 'EST5EDT4')
    srv_control.config_srv('new-tzdb-timezone', '9', 'Europe/Zurich')
    srv_control.config_srv('bootfile-url', '9', 'http://www.kea.isc.org')
    srv_control.config_srv('bootfile-param', '9', '000B48656C6C6F20776F726C640003666F6F')
    srv_control.config_srv('erp-local-domain-name', '9', 'erp-domain.isc.org')
    srv_control.config_srv('domain-search', '9', 'subnet.example.com')

    srv_control.config_srv('preference', '10', '123')
    srv_control.config_srv('sip-server-dns', '10', 'srv1.example.com,srv2.isc.org')
    srv_control.config_srv('dns-servers', '10', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('domain-search', '10', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv('sip-server-addr', '10', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('nisp-servers', '10', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-servers', '10', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-domain-name', '10', 'ntp.example.com')
    srv_control.config_srv('nisp-domain-name', '10', 'ntp.example.com')
    srv_control.config_srv('sntp-servers', '10', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('information-refresh-time', '10', '12345678')
    srv_control.config_srv('unicast', '10', '3000::66')
    srv_control.config_srv('bcmcs-server-dns', '10', 'very.good.domain.name.com')
    srv_control.config_srv('bcmcs-server-addr', '10', '3000::66,3000::77')
    srv_control.config_srv('pana-agent', '10', '3000::66,3000::77')
    srv_control.config_srv('new-posix-timezone', '10', 'EST5EDT4')
    srv_control.config_srv('new-tzdb-timezone', '10', 'Europe/Zurich')
    srv_control.config_srv('bootfile-url', '10', 'http://www.kea.isc.org')
    srv_control.config_srv('bootfile-param', '10', '000B48656C6C6F20776F726C640003666F6F')
    srv_control.config_srv('erp-local-domain-name', '10', 'erp-domain.isc.org')
    srv_control.config_srv('domain-search', '10', 'subnet.example.com')

    srv_control.config_srv('preference', '11', '123')
    srv_control.config_srv('sip-server-dns', '11', 'srv1.example.com,srv2.isc.org')
    srv_control.config_srv('dns-servers', '11', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('domain-search', '11', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv('sip-server-addr', '11', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('nisp-servers', '11', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-servers', '11', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-domain-name', '11', 'ntp.example.com')
    srv_control.config_srv('nisp-domain-name', '11', 'ntp.example.com')
    srv_control.config_srv('sntp-servers', '11', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('information-refresh-time', '11', '12345678')
    srv_control.config_srv('unicast', '11', '3000::66')
    srv_control.config_srv('bcmcs-server-dns', '11', 'very.good.domain.name.com')
    srv_control.config_srv('bcmcs-server-addr', '11', '3000::66,3000::77')
    srv_control.config_srv('pana-agent', '11', '3000::66,3000::77')
    srv_control.config_srv('new-posix-timezone', '11', 'EST5EDT4')
    srv_control.config_srv('new-tzdb-timezone', '11', 'Europe/Zurich')
    srv_control.config_srv('bootfile-url', '11', 'http://www.kea.isc.org')
    srv_control.config_srv('bootfile-param', '11', '000B48656C6C6F20776F726C640003666F6F')
    srv_control.config_srv('erp-local-domain-name', '11', 'erp-domain.isc.org')
    srv_control.config_srv('domain-search', '11', 'subnet.example.com')
    srv_control.config_srv('preference', '12', '123')
    srv_control.config_srv('sip-server-dns', '12', 'srv1.example.com,srv2.isc.org')
    srv_control.config_srv('dns-servers', '12', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('domain-search', '12', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv('sip-server-addr', '12', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('nisp-servers', '12', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-servers', '12', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-domain-name', '12', 'ntp.example.com')
    srv_control.config_srv('nisp-domain-name', '12', 'ntp.example.com')
    srv_control.config_srv('sntp-servers', '12', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('information-refresh-time', '12', '12345678')
    srv_control.config_srv('unicast', '12', '3000::66')
    srv_control.config_srv('bcmcs-server-dns', '12', 'very.good.domain.name.com')
    srv_control.config_srv('bcmcs-server-addr', '12', '3000::66,3000::77')
    srv_control.config_srv('pana-agent', '12', '3000::66,3000::77')
    srv_control.config_srv('new-posix-timezone', '12', 'EST5EDT4')
    srv_control.config_srv('new-tzdb-timezone', '12', 'Europe/Zurich')
    srv_control.config_srv('bootfile-url', '12', 'http://www.kea.isc.org')
    srv_control.config_srv('bootfile-param', '12', '000B48656C6C6F20776F726C640003666F6F')
    srv_control.config_srv('erp-local-domain-name', '12', 'erp-domain.isc.org')
    srv_control.config_srv('domain-search', '12', 'subnet.example.com')

    srv_control.config_srv('preference', '13', '123')
    srv_control.config_srv('sip-server-dns', '13', 'srv1.example.com,srv2.isc.org')
    srv_control.config_srv('dns-servers', '13', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('domain-search', '13', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv('sip-server-addr', '13', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('nisp-servers', '13', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-servers', '13', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-domain-name', '13', 'ntp.example.com')
    srv_control.config_srv('nisp-domain-name', '13', 'ntp.example.com')
    srv_control.config_srv('sntp-servers', '13', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('information-refresh-time', '13', '12345678')
    srv_control.config_srv('unicast', '13', '3000::66')
    srv_control.config_srv('bcmcs-server-dns', '13', 'very.good.domain.name.com')
    srv_control.config_srv('bcmcs-server-addr', '13', '3000::66,3000::77')
    srv_control.config_srv('pana-agent', '13', '3000::66,3000::77')
    srv_control.config_srv('new-posix-timezone', '13', 'EST5EDT4')
    srv_control.config_srv('new-tzdb-timezone', '13', 'Europe/Zurich')
    srv_control.config_srv('bootfile-url', '13', 'http://www.kea.isc.org')
    srv_control.config_srv('bootfile-param', '13', '000B48656C6C6F20776F726C640003666F6F')
    srv_control.config_srv('erp-local-domain-name', '13', 'erp-domain.isc.org')
    srv_control.config_srv('domain-search', '13', 'subnet.example.com')
    srv_control.config_srv('preference', '14', '123')
    srv_control.config_srv('sip-server-dns', '14', 'srv1.example.com,srv2.isc.org')
    srv_control.config_srv('dns-servers', '14', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('domain-search', '14', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv('sip-server-addr', '14', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('nisp-servers', '14', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-servers', '14', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-domain-name', '14', 'ntp.example.com')
    srv_control.config_srv('nisp-domain-name', '14', 'ntp.example.com')
    srv_control.config_srv('sntp-servers', '14', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('information-refresh-time', '14', '12345678')
    srv_control.config_srv('unicast', '14', '3000::66')
    srv_control.config_srv('bcmcs-server-dns', '14', 'very.good.domain.name.com')
    srv_control.config_srv('bcmcs-server-addr', '14', '3000::66,3000::77')
    srv_control.config_srv('pana-agent', '14', '3000::66,3000::77')
    srv_control.config_srv('new-posix-timezone', '14', 'EST5EDT4')
    srv_control.config_srv('new-tzdb-timezone', '14', 'Europe/Zurich')
    srv_control.config_srv('bootfile-url', '14', 'http://www.kea.isc.org')
    srv_control.config_srv('bootfile-param', '14', '000B48656C6C6F20776F726C640003666F6F')
    srv_control.config_srv('erp-local-domain-name', '14', 'erp-domain.isc.org')
    srv_control.config_srv('domain-search', '14', 'subnet.example.com')
    srv_control.config_srv('preference', '15', '123')
    srv_control.config_srv('sip-server-dns', '15', 'srv1.example.com,srv2.isc.org')
    srv_control.config_srv('dns-servers', '15', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('domain-search', '15', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv('sip-server-addr', '15', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('nisp-servers', '15', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-servers', '15', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-domain-name', '15', 'ntp.example.com')
    srv_control.config_srv('nisp-domain-name', '15', 'ntp.example.com')
    srv_control.config_srv('sntp-servers', '15', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('information-refresh-time', '15', '12345678')
    srv_control.config_srv('unicast', '15', '3000::66')
    srv_control.config_srv('bcmcs-server-dns', '15', 'very.good.domain.name.com')
    srv_control.config_srv('bcmcs-server-addr', '15', '3000::66,3000::77')
    srv_control.config_srv('pana-agent', '15', '3000::66,3000::77')
    srv_control.config_srv('new-posix-timezone', '15', 'EST5EDT4')
    srv_control.config_srv('new-tzdb-timezone', '15', 'Europe/Zurich')
    srv_control.config_srv('bootfile-url', '15', 'http://www.kea.isc.org')
    srv_control.config_srv('bootfile-param', '15', '000B48656C6C6F20776F726C640003666F6F')
    srv_control.config_srv('erp-local-domain-name', '15', 'erp-domain.isc.org')
    srv_control.config_srv('domain-search', '15', 'subnet.example.com')
    srv_control.config_srv('preference', '16', '123')
    srv_control.config_srv('sip-server-dns', '16', 'srv1.example.com,srv2.isc.org')
    srv_control.config_srv('dns-servers', '16', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('domain-search', '16', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv('sip-server-addr', '16', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('nisp-servers', '16', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-servers', '16', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-domain-name', '16', 'ntp.example.com')
    srv_control.config_srv('nisp-domain-name', '16', 'ntp.example.com')
    srv_control.config_srv('sntp-servers', '16', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('information-refresh-time', '16', '12345678')
    srv_control.config_srv('unicast', '16', '3000::66')
    srv_control.config_srv('bcmcs-server-dns', '16', 'very.good.domain.name.com')
    srv_control.config_srv('bcmcs-server-addr', '16', '3000::66,3000::77')
    srv_control.config_srv('pana-agent', '16', '3000::66,3000::77')
    srv_control.config_srv('new-posix-timezone', '16', 'EST5EDT4')
    srv_control.config_srv('new-tzdb-timezone', '16', 'Europe/Zurich')
    srv_control.config_srv('bootfile-url', '16', 'http://www.kea.isc.org')
    srv_control.config_srv('bootfile-param', '16', '000B48656C6C6F20776F726C640003666F6F')
    srv_control.config_srv('erp-local-domain-name', '16', 'erp-domain.isc.org')
    srv_control.config_srv('domain-search', '16', 'subnet.example.com')
    srv_control.config_srv('preference', '17', '123')
    srv_control.config_srv('sip-server-dns', '17', 'srv1.example.com,srv2.isc.org')
    srv_control.config_srv('dns-servers', '17', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('domain-search', '17', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv('sip-server-addr', '17', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('nisp-servers', '17', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-servers', '17', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-domain-name', '17', 'ntp.example.com')
    srv_control.config_srv('nisp-domain-name', '17', 'ntp.example.com')
    srv_control.config_srv('sntp-servers', '17', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('information-refresh-time', '17', '12345678')
    srv_control.config_srv('unicast', '17', '3000::66')
    srv_control.config_srv('bcmcs-server-dns', '17', 'very.good.domain.name.com')
    srv_control.config_srv('bcmcs-server-addr', '17', '3000::66,3000::77')
    srv_control.config_srv('pana-agent', '17', '3000::66,3000::77')
    srv_control.config_srv('new-posix-timezone', '17', 'EST5EDT4')
    srv_control.config_srv('new-tzdb-timezone', '17', 'Europe/Zurich')
    srv_control.config_srv('bootfile-url', '17', 'http://www.kea.isc.org')
    srv_control.config_srv('bootfile-param', '17', '000B48656C6C6F20776F726C640003666F6F')
    srv_control.config_srv('erp-local-domain-name', '17', 'erp-domain.isc.org')
    srv_control.config_srv('domain-search', '17', 'subnet.example.com')
    srv_control.config_srv('preference', '18', '123')
    srv_control.config_srv('sip-server-dns', '18', 'srv1.example.com,srv2.isc.org')
    srv_control.config_srv('dns-servers', '18', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('domain-search', '18', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv('sip-server-addr', '18', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('nisp-servers', '18', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-servers', '18', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-domain-name', '18', 'ntp.example.com')
    srv_control.config_srv('nisp-domain-name', '18', 'ntp.example.com')
    srv_control.config_srv('sntp-servers', '18', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('information-refresh-time', '18', '12345678')
    srv_control.config_srv('unicast', '18', '3000::66')
    srv_control.config_srv('bcmcs-server-dns', '18', 'very.good.domain.name.com')
    srv_control.config_srv('bcmcs-server-addr', '18', '3000::66,3000::77')
    srv_control.config_srv('pana-agent', '18', '3000::66,3000::77')
    srv_control.config_srv('new-posix-timezone', '18', 'EST5EDT4')
    srv_control.config_srv('new-tzdb-timezone', '18', 'Europe/Zurich')
    srv_control.config_srv('bootfile-url', '18', 'http://www.kea.isc.org')
    srv_control.config_srv('bootfile-param', '18', '000B48656C6C6F20776F726C640003666F6F')
    srv_control.config_srv('erp-local-domain-name', '18', 'erp-domain.isc.org')
    srv_control.config_srv('domain-search', '18', 'subnet.example.com')
    srv_control.config_srv('preference', '19', '123')
    srv_control.config_srv('sip-server-dns', '19', 'srv1.example.com,srv2.isc.org')
    srv_control.config_srv('dns-servers', '19', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('domain-search', '19', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv('sip-server-addr', '19', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('nisp-servers', '19', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-servers', '19', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-domain-name', '19', 'ntp.example.com')
    srv_control.config_srv('nisp-domain-name', '19', 'ntp.example.com')
    srv_control.config_srv('sntp-servers', '19', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('information-refresh-time', '19', '12345678')
    srv_control.config_srv('unicast', '19', '3000::66')
    srv_control.config_srv('bcmcs-server-dns', '19', 'very.good.domain.name.com')
    srv_control.config_srv('bcmcs-server-addr', '19', '3000::66,3000::77')
    srv_control.config_srv('pana-agent', '19', '3000::66,3000::77')
    srv_control.config_srv('new-posix-timezone', '19', 'EST5EDT4')
    srv_control.config_srv('new-tzdb-timezone', '19', 'Europe/Zurich')
    srv_control.config_srv('bootfile-url', '19', 'http://www.kea.isc.org')
    srv_control.config_srv('bootfile-param', '19', '000B48656C6C6F20776F726C640003666F6F')
    srv_control.config_srv('erp-local-domain-name', '19', 'erp-domain.isc.org')
    srv_control.config_srv('domain-search', '19', 'subnet.example.com')

    srv_control.config_srv('preference', '20', '123')
    srv_control.config_srv('sip-server-dns', '20', 'srv1.example.com,srv2.isc.org')
    srv_control.config_srv('dns-servers', '20', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('domain-search', '20', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv('sip-server-addr', '20', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('nisp-servers', '20', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-servers', '20', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-domain-name', '20', 'ntp.example.com')
    srv_control.config_srv('nisp-domain-name', '20', 'ntp.example.com')
    srv_control.config_srv('sntp-servers', '20', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('information-refresh-time', '20', '12345678')
    srv_control.config_srv('unicast', '20', '3000::66')
    srv_control.config_srv('bcmcs-server-dns', '20', 'very.good.domain.name.com')
    srv_control.config_srv('bcmcs-server-addr', '20', '3000::66,3000::77')
    srv_control.config_srv('pana-agent', '20', '3000::66,3000::77')
    srv_control.config_srv('new-posix-timezone', '20', 'EST5EDT4')
    srv_control.config_srv('new-tzdb-timezone', '20', 'Europe/Zurich')
    srv_control.config_srv('bootfile-url', '20', 'http://www.kea.isc.org')
    srv_control.config_srv('bootfile-param', '20', '000B48656C6C6F20776F726C640003666F6F')
    srv_control.config_srv('erp-local-domain-name', '20', 'erp-domain.isc.org')
    srv_control.config_srv('domain-search', '20', 'subnet.example.com')
    srv_control.config_srv('preference', '21', '123')
    srv_control.config_srv('sip-server-dns', '21', 'srv1.example.com,srv2.isc.org')
    srv_control.config_srv('dns-servers', '21', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('domain-search', '21', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv('sip-server-addr', '21', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('nisp-servers', '21', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-servers', '21', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-domain-name', '21', 'ntp.example.com')
    srv_control.config_srv('nisp-domain-name', '21', 'ntp.example.com')
    srv_control.config_srv('sntp-servers', '21', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('information-refresh-time', '21', '12345678')
    srv_control.config_srv('unicast', '21', '3000::66')
    srv_control.config_srv('bcmcs-server-dns', '21', 'very.good.domain.name.com')
    srv_control.config_srv('bcmcs-server-addr', '21', '3000::66,3000::77')
    srv_control.config_srv('pana-agent', '21', '3000::66,3000::77')
    srv_control.config_srv('new-posix-timezone', '21', 'EST5EDT4')
    srv_control.config_srv('new-tzdb-timezone', '21', 'Europe/Zurich')
    srv_control.config_srv('bootfile-url', '21', 'http://www.kea.isc.org')
    srv_control.config_srv('bootfile-param', '21', '000B48656C6C6F20776F726C640003666F6F')
    srv_control.config_srv('erp-local-domain-name', '21', 'erp-domain.isc.org')
    srv_control.config_srv('domain-search', '21', 'subnet.example.com')
    srv_control.config_srv('preference', '22', '123')
    srv_control.config_srv('sip-server-dns', '22', 'srv1.example.com,srv2.isc.org')
    srv_control.config_srv('dns-servers', '22', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('domain-search', '22', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv('sip-server-addr', '22', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('nisp-servers', '22', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-servers', '22', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-domain-name', '22', 'ntp.example.com')
    srv_control.config_srv('nisp-domain-name', '22', 'ntp.example.com')
    srv_control.config_srv('sntp-servers', '22', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('information-refresh-time', '22', '12345678')
    srv_control.config_srv('unicast', '22', '3000::66')
    srv_control.config_srv('bcmcs-server-dns', '22', 'very.good.domain.name.com')
    srv_control.config_srv('bcmcs-server-addr', '22', '3000::66,3000::77')
    srv_control.config_srv('pana-agent', '22', '3000::66,3000::77')
    srv_control.config_srv('new-posix-timezone', '22', 'EST5EDT4')
    srv_control.config_srv('new-tzdb-timezone', '22', 'Europe/Zurich')
    srv_control.config_srv('bootfile-url', '22', 'http://www.kea.isc.org')
    srv_control.config_srv('bootfile-param', '22', '000B48656C6C6F20776F726C640003666F6F')
    srv_control.config_srv('erp-local-domain-name', '22', 'erp-domain.isc.org')
    srv_control.config_srv('domain-search', '22', 'subnet.example.com')
    srv_control.config_srv('preference', '23', '123')
    srv_control.config_srv('sip-server-dns', '23', 'srv1.example.com,srv2.isc.org')
    srv_control.config_srv('dns-servers', '23', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('domain-search', '23', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv('sip-server-addr', '23', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('nisp-servers', '23', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-servers', '23', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-domain-name', '23', 'ntp.example.com')
    srv_control.config_srv('nisp-domain-name', '23', 'ntp.example.com')
    srv_control.config_srv('sntp-servers', '23', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('information-refresh-time', '23', '12345678')
    srv_control.config_srv('unicast', '23', '3000::66')
    srv_control.config_srv('bcmcs-server-dns', '23', 'very.good.domain.name.com')
    srv_control.config_srv('bcmcs-server-addr', '23', '3000::66,3000::77')
    srv_control.config_srv('pana-agent', '23', '3000::66,3000::77')
    srv_control.config_srv('new-posix-timezone', '23', 'EST5EDT4')
    srv_control.config_srv('new-tzdb-timezone', '23', 'Europe/Zurich')
    srv_control.config_srv('bootfile-url', '23', 'http://www.kea.isc.org')
    srv_control.config_srv('bootfile-param', '23', '000B48656C6C6F20776F726C640003666F6F')
    srv_control.config_srv('erp-local-domain-name', '23', 'erp-domain.isc.org')
    srv_control.config_srv('domain-search', '23', 'subnet.example.com')
    srv_control.config_srv('preference', '24', '123')
    srv_control.config_srv('sip-server-dns', '24', 'srv1.example.com,srv2.isc.org')
    srv_control.config_srv('dns-servers', '24', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('domain-search', '24', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv('sip-server-addr', '24', '2001:db8::1,2001:db8::2')
    srv_control.config_srv('nisp-servers', '24', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-servers', '24', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('nis-domain-name', '24', 'ntp.example.com')
    srv_control.config_srv('nisp-domain-name', '24', 'ntp.example.com')
    srv_control.config_srv('sntp-servers', '24', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv('information-refresh-time', '24', '12345678')
    srv_control.config_srv('unicast', '24', '3000::66')
    srv_control.config_srv('bcmcs-server-dns', '24', 'very.good.domain.name.com')
    srv_control.config_srv('bcmcs-server-addr', '24', '3000::66,3000::77')
    srv_control.config_srv('pana-agent', '24', '3000::66,3000::77')
    srv_control.config_srv('new-posix-timezone', '24', 'EST5EDT4')
    srv_control.config_srv('new-tzdb-timezone', '24', 'Europe/Zurich')
    srv_control.config_srv('bootfile-url', '24', 'http://www.kea.isc.org')
    srv_control.config_srv('bootfile-param', '24', '000B48656C6C6F20776F726C640003666F6F')
    srv_control.config_srv('erp-local-domain-name', '24', 'erp-domain.isc.org')
    srv_control.config_srv('domain-search', '24', 'subnet.example.com')
    srv_control.config_srv_opt_space('vendor-4491',
                                     'tftp-servers',
                                     '2001:558:ff18:16:10:253:175:76')
    srv_control.config_srv_opt_space('vendor-4491', 'config-file', 'normal_erouter_v6.cm')
    srv_control.config_srv_opt_space('vendor-4491',
                                     'syslog-servers',
                                     '2001:558:ff18:10:10:253:124:101')
    srv_control.config_srv_opt_space('vendor-4491',
                                     'time-servers',
                                     '2001:558:ff18:16:10:253:175:76')
    srv_control.config_srv_opt_space('vendor-4491', 'time-offset', '-10000')
    srv_control.open_control_channel()

    srv_control.configure_loggers('kea-dhcp6.dhcp6', 'INFO', 'None')
    srv_control.configure_loggers('kea-dhcp6.dhcpsrv', 'INFO', 'None')
    srv_control.configure_loggers('kea-dhcp6.options', 'DEBUG', '99')
    srv_control.configure_loggers('kea-dhcp6.packets', 'DEBUG', '99')
    srv_control.configure_loggers('kea-dhcp6.leases', 'WARN', 'None')
    srv_control.configure_loggers('kea-dhcp6.alloc-engine', 'DEBUG', '50')
    srv_control.configure_loggers('kea-dhcp6.bad-packets', 'DEBUG', '25')
    srv_control.configure_loggers('kea-dhcp6.options', 'INFO', 'None')
    srv_control.generate_config_files()

    srv_msg.send_ctrl_cmd_via_socket('{"command": "config-set","arguments":  $(SERVER_CONFIG) }')

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
                                             '2001:db8:1:1::1')

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
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')
