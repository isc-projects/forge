"""Kea Hook hosts_cmds testing"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_msg
import misc
import srv_control


@pytest.mark.v6
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v6_hosts_cmds_librelaod():
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::50')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1::100"]}}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::100')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "libreload","arguments": {}}')
    # TODO This is cool, but we need to actually check that reload is happening.

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-del","arguments":{"subnet-id":1,"ip-address":"2001:db8:1::100"}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::50')


@pytest.mark.v6
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v6_hosts_cmds_reconfigure():
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::50')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1::100"]}}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::100')

    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'reconfigured')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1::100"]}}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::100')


@pytest.mark.v6
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v6_hosts_cmds_add_reservation_mysql():
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::50')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1::100"]}}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::100')


@pytest.mark.v6
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v6_hosts_cmds_del_reservation_mysql():
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::50')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1::100"]}}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::100')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-del","arguments":{"subnet-id":1,"ip-address":"2001:db8:1::100"}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::50')


@pytest.mark.v6
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v6_hosts_cmds_del_reservation_pgsql():
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::50')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1::100"]}}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::100')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-del","arguments":{"subnet-id":1,"ip-address":"2001:db8:1::100"}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::50')


@pytest.mark.v6
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v6_hosts_cmds_add_reservation_pgsql():
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::50')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1::100"]}}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::100')


@pytest.mark.v6
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v6_hosts_cmds_get_reservation_mysql():
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::50')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1::100"]}}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::100')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "reservation-get","arguments":{"subnet-id":1,"identifier-type": "duid","identifier":"00:03:00:01:f6:f5:f4:f3:f2:01"}}')


@pytest.mark.v6
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v6_hosts_cmds_get_reservation_pgsql():
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::50')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1::100"]}}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::100')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "reservation-get","arguments":{"subnet-id":1,"identifier-type": "duid","identifier":"00:03:00:01:f6:f5:f4:f3:f2:01"}}')


@pytest.mark.v6
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v6_hosts_cmds_add_reservation_mysql_flex_id():

    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_line('"host-reservation-identifiers": [ "flex-id" ]')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook('2', 'identifier-expression', 'relay6[0].option[18].hex')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8:1::1000')
    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'port1234')
    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
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
    srv_msg.response_check_suboption_content('Relayed Message',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::50')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"flex-id":"\'port1234\'","ip-addresses":["2001:db8:1::100"]}}}')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8:1::1000')
    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'port1234')
    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
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
    srv_msg.response_check_suboption_content('Relayed Message',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::100')


@pytest.mark.v6
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v6_hosts_cmds_add_reservation_pgsql_flex_id():
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_line('"host-reservation-identifiers": [ "flex-id" ]')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook('2', 'identifier-expression', 'relay6[0].option[18].hex')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8:1::1000')
    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'port1234')
    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
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
    srv_msg.response_check_suboption_content('Relayed Message',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::50')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"flex-id":"\'port1234\'","ip-addresses":["2001:db8:1::100"]}}}')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8:1::1000')
    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'port1234')
    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
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
    srv_msg.response_check_suboption_content('Relayed Message',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::100')


@pytest.mark.v6
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v6_hosts_cmds_add_reservation_complex_pgsql():
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_does_include('Client', None, 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::50')
    srv_msg.response_check_include_option('Response', None, '25')
    srv_msg.response_check_option_content('Response', '25', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content('Response', '13', '25', None, 'statuscode', '6')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1:0:cafe::1"],"prefixes":["2001:db8:2:abcd::/64"],"hostname":"foo.example.com","option-data":[{"name":"vendor-opts","data":"4491"},{"name":"tftp-servers","space":"vendor-4491","data":"3000:1::234"}]}}}')
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_does_include('Client', None, 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1:0:cafe::1')
    srv_msg.response_check_include_option('Response', None, '25')
    srv_msg.response_check_suboption_content('Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '2001:db8:2:abcd::')


@pytest.mark.v6
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v6_hosts_cmds_add_reservation_complex_mysql():
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_does_include('Client', None, 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::50')
    srv_msg.response_check_include_option('Response', None, '25')
    srv_msg.response_check_option_content('Response', '25', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content('Response', '13', '25', None, 'statuscode', '6')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1:0:cafe::1"],"prefixes":["2001:db8:2:abcd::/64"],"hostname":"foo.example.com","option-data":[{"name":"vendor-opts","data":"4491"},{"name":"tftp-servers","space":"vendor-4491","data":"3000:1::234"}]}}}')
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_does_include('Client', None, 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1:0:cafe::1')
    srv_msg.response_check_include_option('Response', None, '25')
    srv_msg.response_check_suboption_content('Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '2001:db8:2:abcd::')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v6_hosts_cmds_reservation_get_all():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_another_subnet_no_interface('3001::/64', '3001::1-3001::ff')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname1',
                                           '0',
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:01')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname2',
                                           '0',
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:02')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname3',
                                           '0',
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:03')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname4',
                                           '1',
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:04')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname5',
                                           '1',
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:05')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-get-all","arguments":{"subnet-id":1}}')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname1')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname2')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname3')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname4')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname5')
    srv_msg.json_response_parsing('text', None, '3 IPv6 host(s) found.')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v6_hosts_cmds_reservation_get_all_mysql():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_another_subnet_no_interface('3001::/64', '3001::1-3001::ff')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname1', 'MySQL', '1')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '1', 'MySQL', '1')
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:02')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname2', 'MySQL', '2')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '1', 'MySQL', '2')
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:03')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname3', 'MySQL', '3')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '1', 'MySQL', '3')
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:04')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname4', 'MySQL', '4')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '2', 'MySQL', '4')
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:05')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname5', 'MySQL', '5')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '2', 'MySQL', '5')
    srv_control.upload_db_reservation('MySQL')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-get-all","arguments":{"subnet-id":1}}')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname1')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname2')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname3')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname4')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname5')
    srv_msg.json_response_parsing('text', None, '3 IPv6 host(s) found.')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v6_hosts_cmds_reservation_get_all_pgsql():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_another_subnet_no_interface('3001::/64', '3001::1-3001::ff')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname1', 'PostgreSQL', '1')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '1', 'PostgreSQL', '1')
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:02')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname2', 'PostgreSQL', '2')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '1', 'PostgreSQL', '2')
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:03')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname3', 'PostgreSQL', '3')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '1', 'PostgreSQL', '3')
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:04')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname4', 'PostgreSQL', '4')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '2', 'PostgreSQL', '4')
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:05')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname5', 'PostgreSQL', '5')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '2', 'PostgreSQL', '5')
    srv_control.upload_db_reservation('PostgreSQL')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-get-all","arguments":{"subnet-id":1}}')

    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname1')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname2')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname3')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname4')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname5')
    srv_msg.json_response_parsing('text', None, '3 IPv6 host(s) found.')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v6_hosts_cmds_reservation_get_page():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_another_subnet_no_interface('3001::/64', '3001::1-3001::ff')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname1',
                                           '0',
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:01')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname2',
                                           '0',
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:02')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname3',
                                           '0',
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:03')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname4',
                                           '1',
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:04')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname5',
                                           '1',
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:05')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname6',
                                           '0',
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:06')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname7',
                                           '0',
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:07')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-get-page","arguments":{"subnet-id":1,"limit":3}}')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname1')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname2')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname3')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname4')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname5')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname6')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname7')
    srv_msg.json_response_parsing('text', None, '3 IPv6 host(s) found.')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-get-page","arguments":{"subnet-id":1,"limit":3,"from":3}}')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname6')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname7')
    srv_msg.json_response_parsing('text', None, '2 IPv6 host(s) found.')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v6_hosts_cmds_reservation_get_all_page_mysql():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_another_subnet_no_interface('3001::/64', '3001::1-3001::ff')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname1', 'MySQL', '1')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '1', 'MySQL', '1')
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:02')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname2', 'MySQL', '2')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '1', 'MySQL', '2')
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:03')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname3', 'MySQL', '3')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '1', 'MySQL', '3')
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:04')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname4', 'MySQL', '4')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '2', 'MySQL', '4')
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:05')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname5', 'MySQL', '5')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '2', 'MySQL', '5')

    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:06')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname6', 'MySQL', '6')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '1', 'MySQL', '6')
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:07')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname7', 'MySQL', '7')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '1', 'MySQL', '7')

    srv_control.upload_db_reservation('MySQL')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-get-page","arguments":{"subnet-id":1,"limit":3}}')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname7')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname6')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname3')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname4')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname5')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname1')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname2')
    srv_msg.json_response_parsing('text', None, '3 IPv6 host(s) found.')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v6_hosts_cmds_reservation_get_all_page_pgsql():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_another_subnet_no_interface('3001::/64', '3001::1-3001::ff')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname1', 'PostgreSQL', '1')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '1', 'PostgreSQL', '1')
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:02')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname2', 'PostgreSQL', '2')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '1', 'PostgreSQL', '2')
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:03')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname3', 'PostgreSQL', '3')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '1', 'PostgreSQL', '3')
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:04')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname4', 'PostgreSQL', '4')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '2', 'PostgreSQL', '4')
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:05')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname5', 'PostgreSQL', '5')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '2', 'PostgreSQL', '5')

    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:06')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname6', 'PostgreSQL', '6')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '1', 'PostgreSQL', '6')
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:07')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname7', 'PostgreSQL', '7')
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', '1', 'PostgreSQL', '7')

    srv_control.upload_db_reservation('PostgreSQL')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-get-page","arguments":{"subnet-id":1,"limit":3}}')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname6')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname7')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname3')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname4')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname5')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname1')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname2')
    srv_msg.json_response_parsing('text', None, '3 IPv6 host(s) found.')
