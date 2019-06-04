"""Kea Hook hosts_cmds testing"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_control
import misc
import srv_msg


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_libreload():
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()

    srv_control.enable_db_backend_reservation('MySQL')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"hw-address":"ff:01:02:03:ff:04","ip-address":"192.168.50.100"}}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.100')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.100')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.100')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "libreload","arguments": {}}')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-del","arguments":{"subnet-id":1,"ip-address":"192.168.50.100"}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_reconfigure():
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()

    srv_control.enable_db_backend_reservation('MySQL')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"hw-address":"ff:01:02:03:ff:04","ip-address":"192.168.50.100"}}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.100')

    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()

    srv_control.enable_db_backend_reservation('MySQL')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'reconfigured')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"hw-address":"ff:01:02:03:ff:04","ip-address":"192.168.50.100"}}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.100')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_add_reservation_mysql():
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()

    srv_control.enable_db_backend_reservation('MySQL')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"hw-address":"ff:01:02:03:ff:04","ip-address":"192.168.50.100"}}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.100')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.100')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.100')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_del_reservation_mysql():
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()

    srv_control.enable_db_backend_reservation('MySQL')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"hw-address":"ff:01:02:03:ff:04","ip-address":"192.168.50.100"}}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.100')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-del","arguments":{"subnet-id":1,"ip-address":"192.168.50.100"}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_del_reservation_mysql_2():
    misc.test_setup()
    # address reserved without using command
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()

    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'ff:01:02:03:ff:04')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'MySQL', '1')
    srv_control.update_db_backend_reservation('ipv4_address', '192.168.50.100', 'MySQL', '1')
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', '1', 'MySQL', '1')
    srv_control.upload_db_reservation('MySQL')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.100')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-del","arguments":{"subnet-id":1,"ip-address":"192.168.50.100"}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_del_reservation_pgsql():
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()

    srv_control.enable_db_backend_reservation('PostgreSQL')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"hw-address":"ff:01:02:03:ff:04","ip-address":"192.168.50.100"}}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.100')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-del","arguments":{"subnet-id":1,"ip-address":"192.168.50.100"}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_del_reservation_pgsql_2():
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()

    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'ff:01:02:03:ff:04')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'PostgreSQL', '1')
    srv_control.update_db_backend_reservation('ipv4_address', '192.168.50.100', 'PostgreSQL', '1')
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', '1', 'PostgreSQL', '1')
    srv_control.upload_db_reservation('PostgreSQL')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.100')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-del","arguments":{"subnet-id":1,"ip-address":"192.168.50.100"}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.50')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_add_reservation_pgsql():
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()

    srv_control.enable_db_backend_reservation('PostgreSQL')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"hw-address":"ff:01:02:03:ff:04","ip-address":"192.168.50.100"}}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.100')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.100')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.100')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_get_reservation_mysql():
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()

    srv_control.enable_db_backend_reservation('MySQL')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"hw-address":"ff:01:02:03:ff:04","ip-address":"192.168.50.100"}}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.100')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "reservation-get","arguments":{"subnet-id":1,"identifier-type": "hw-address","identifier":"ff:01:02:03:ff:04"}}')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_get_reservation_mysql_2():
    misc.test_setup()
    # address reserved without using command
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()

    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'ff:01:02:03:ff:04')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'MySQL', '1')
    srv_control.update_db_backend_reservation('ipv4_address', '192.168.50.100', 'MySQL', '1')
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', '1', 'MySQL', '1')
    srv_control.upload_db_reservation('MySQL')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.100')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "reservation-get","arguments":{"subnet-id":1,"identifier-type": "hw-address","identifier":"ff:01:02:03:ff:04"}}')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_get_reservation_pgsql():
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()

    srv_control.enable_db_backend_reservation('PostgreSQL')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"hw-address":"ff:01:02:03:ff:04","ip-address":"192.168.50.100"}}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.100')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "reservation-get","arguments":{"subnet-id":1,"identifier-type": "hw-address","identifier":"ff:01:02:03:ff:04"}}')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_get_reservation_pgsql_2():
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()

    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'ff:01:02:03:ff:04')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'PostgreSQL', '1')
    srv_control.update_db_backend_reservation('ipv4_address', '192.168.50.100', 'PostgreSQL', '1')
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', '1', 'PostgreSQL', '1')
    srv_control.upload_db_reservation('PostgreSQL')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.100')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "reservation-get","arguments":{"subnet-id":1,"identifier-type": "hw-address","identifier":"ff:01:02:03:ff:04"}}')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_add_reservation_mysql_flex_id():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()

    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook('2', 'identifier-expression', 'option[60].hex')
    srv_control.add_line('"host-reservation-identifiers": [ "flex-id" ]')

    srv_control.enable_db_backend_reservation('MySQL')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"flex-id":"\'docsis3.0\'","ip-address":"192.168.50.100"}}}')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.100')

    misc.test_procedure()
    # Client adds to the message vendor_class_id with value docsis3.0.
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.100')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.100')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_add_reservation_mysql_flex_id_nak():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()

    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook('2', 'identifier-expression', 'option[60].hex')
    srv_control.add_line('"host-reservation-identifiers": [ "flex-id" ]')

    srv_control.enable_db_backend_reservation('MySQL')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"flex-id":"\'docsis3.0\'","ip-address":"192.168.50.100"}}}')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.100')

    misc.test_procedure()
    # Client adds to the message vendor_class_id with value docsis3.0.
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'NAK')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_add_reservation_pgsql_flex_id():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()

    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook('2', 'identifier-expression', 'option[60].hex')
    srv_control.add_line('"host-reservation-identifiers": [ "flex-id" ]')

    srv_control.enable_db_backend_reservation('PostgreSQL')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"flex-id":"\'docsis3.0\'","ip-address":"192.168.50.100"}}}')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.100')

    misc.test_procedure()
    # Client adds to the message vendor_class_id with value docsis3.0.
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.100')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.100')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_add_reservation_pgsql_flex_id_nak():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()

    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook('2', 'identifier-expression', 'option[60].hex')
    srv_control.add_line('"host-reservation-identifiers": [ "flex-id" ]')

    srv_control.enable_db_backend_reservation('PostgreSQL')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"flex-id":"\'docsis3.0\'","ip-address":"192.168.50.100"}}}')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.100')

    misc.test_procedure()
    # Client adds to the message vendor_class_id with value docsis3.0.
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'NAK')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_add_reservation_complex_pgsql():
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()
    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '01:0a:0b:0c:0d:0e:0f')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')

    response = srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"client-id":"01:0a:0b:0c:0d:0e:0f","ip-address":"192.0.2.205","next-server":"192.0.2.1","server-hostname":"hal9000","boot-file-name":"/dev/null","option-data":[{"name":"domain-name-servers","data":"10.1.1.202,10.1.1.203"}],"client-classes":["special_snowflake","office"]}}}')
    assert response['result'] == 0
    # TODO: it fails with: "specified reservation '192.0.2.205' is not matching the IPv4 subnet prefix '192.168.50.0/24'", how should Kea behave actually?

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '01:0a:0b:0c:0d:0e:0f')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.0.2.205')
    srv_msg.response_check_include_option('Response', None, '6')
    srv_msg.response_check_option_content('Response', '6', None, 'value', '10.1.1.203')
    srv_msg.response_check_option_content('Response', '6', None, 'value', '10.1.1.202')
    srv_msg.response_check_content('Response', None, 'sname', 'hal9000')
    srv_msg.response_check_content('Response', None, 'file', '/dev/null')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.0.2.205')
    srv_msg.client_does_include_with_value('client_id', '01:0a:0b:0c:0d:0e:0f')
    srv_msg.client_sets_value('Client', 'chaddr', '01:0a:0b:0c:0d:0e:0f')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.0.2.205')
    srv_msg.response_check_include_option('Response', None, '6')
    srv_msg.response_check_option_content('Response', '6', None, 'value', '10.1.1.203')
    srv_msg.response_check_option_content('Response', '6', None, 'value', '10.1.1.202')
    srv_msg.response_check_content('Response', None, 'sname', 'hal9000')
    srv_msg.response_check_content('Response', None, 'file', '/dev/null')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_add_reservation_complex_mysql():
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()
    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '01:0a:0b:0c:0d:0e:0f')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')

    result = srv_msg.send_ctrl_cmd_via_socket('{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"client-id":"01:0a:0b:0c:0d:0e:0f","ip-address":"192.0.2.205","next-server":"192.0.2.1","server-hostname":"hal9000","boot-file-name":"/dev/null","option-data":[{"name":"domain-name-servers","data":"10.1.1.202,10.1.1.203"}],"client-classes":["special_snowflake","office"]}}}')
    assert result['result'] == 0
    # TODO: it fails with: "specified reservation '192.0.2.205' is not matching the IPv4 subnet prefix '192.168.50.0/24'", how should Kea behave actually?

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '01:0a:0b:0c:0d:0e:0f')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.0.2.205')
    srv_msg.response_check_include_option('Response', None, '6')
    srv_msg.response_check_option_content('Response', '6', None, 'value', '10.1.1.203')
    srv_msg.response_check_option_content('Response', '6', None, 'value', '10.1.1.202')
    srv_msg.response_check_content('Response', None, 'sname', 'hal9000')
    srv_msg.response_check_content('Response', None, 'file', '/dev/null')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.0.2.205')
    srv_msg.client_does_include_with_value('client_id', '01:0a:0b:0c:0d:0e:0f')
    srv_msg.client_sets_value('Client', 'chaddr', '01:0a:0b:0c:0d:0e:0f')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.0.2.205')
    srv_msg.response_check_include_option('Response', None, '6')
    srv_msg.response_check_option_content('Response', '6', None, 'value', '10.1.1.203')
    srv_msg.response_check_option_content('Response', '6', None, 'value', '10.1.1.202')
    srv_msg.response_check_content('Response', None, 'sname', 'hal9000')
    srv_msg.response_check_content('Response', None, 'file', '/dev/null')
