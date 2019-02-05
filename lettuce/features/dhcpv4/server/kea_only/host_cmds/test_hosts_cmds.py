"""Kea Hook hosts_cmds testing"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import misc
from features import srv_msg
from features import srv_control


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_libreload(step):
    misc.test_setup(step)
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')

    srv_control.enable_db_backend_reservation(step, 'MySQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"hw-address":"ff:01:02:03:ff:04","ip-address":"192.168.50.100"}}}')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.100')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.100')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.100')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "libreload","arguments": {}}')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"reservation-del","arguments":{"subnet-id":1,"ip-address":"192.168.50.100"}}')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_reconfigure(step):
    misc.test_setup(step)
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')

    srv_control.enable_db_backend_reservation(step, 'MySQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"hw-address":"ff:01:02:03:ff:04","ip-address":"192.168.50.100"}}}')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.100')

    misc.test_setup(step)
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')

    srv_control.enable_db_backend_reservation(step, 'MySQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'reconfigured')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"hw-address":"ff:01:02:03:ff:04","ip-address":"192.168.50.100"}}}')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.100')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_add_reservation_mysql(step):
    misc.test_setup(step)
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')

    srv_control.enable_db_backend_reservation(step, 'MySQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"hw-address":"ff:01:02:03:ff:04","ip-address":"192.168.50.100"}}}')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.100')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.100')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.100')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_del_reservation_mysql(step):
    misc.test_setup(step)
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')

    srv_control.enable_db_backend_reservation(step, 'MySQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"hw-address":"ff:01:02:03:ff:04","ip-address":"192.168.50.100"}}}')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.100')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"reservation-del","arguments":{"subnet-id":1,"ip-address":"192.168.50.100"}}')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_del_reservation_mysql_2(step):
    misc.test_setup(step)
    # address reserved without using command
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')

    srv_control.enable_db_backend_reservation(step, 'MySQL')
    srv_control.new_db_backend_reservation(step, 'MySQL', 'hw-address', 'ff:01:02:03:ff:04')
    srv_control.update_db_backend_reservation(step, 'hostname', 'reserved-hostname', 'MySQL', '1')
    srv_control.update_db_backend_reservation(step,
                                              'ipv4_address',
                                              '192.168.50.100',
                                              'MySQL',
                                              '1')
    srv_control.update_db_backend_reservation(step, 'dhcp4_subnet_id', '1', 'MySQL', '1')
    srv_control.upload_db_reservation(step, 'MySQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.100')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"reservation-del","arguments":{"subnet-id":1,"ip-address":"192.168.50.100"}}')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_del_reservation_pgsql(step):
    misc.test_setup(step)
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')

    srv_control.enable_db_backend_reservation(step, 'PostgreSQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"hw-address":"ff:01:02:03:ff:04","ip-address":"192.168.50.100"}}}')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.100')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"reservation-del","arguments":{"subnet-id":1,"ip-address":"192.168.50.100"}}')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_del_reservation_pgsql_2(step):
    misc.test_setup(step)
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')

    srv_control.enable_db_backend_reservation(step, 'PostgreSQL')
    srv_control.new_db_backend_reservation(step, 'PostgreSQL', 'hw-address', 'ff:01:02:03:ff:04')
    srv_control.update_db_backend_reservation(step,
                                              'hostname',
                                              'reserved-hostname',
                                              'PostgreSQL',
                                              '1')
    srv_control.update_db_backend_reservation(step,
                                              'ipv4_address',
                                              '192.168.50.100',
                                              'PostgreSQL',
                                              '1')
    srv_control.update_db_backend_reservation(step, 'dhcp4_subnet_id', '1', 'PostgreSQL', '1')
    srv_control.upload_db_reservation(step, 'PostgreSQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.100')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"reservation-del","arguments":{"subnet-id":1,"ip-address":"192.168.50.100"}}')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.50')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_add_reservation_pgsql(step):
    misc.test_setup(step)
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')

    srv_control.enable_db_backend_reservation(step, 'PostgreSQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"hw-address":"ff:01:02:03:ff:04","ip-address":"192.168.50.100"}}}')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.100')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.100')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.100')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_get_reservation_mysql(step):
    misc.test_setup(step)
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')

    srv_control.enable_db_backend_reservation(step, 'MySQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"hw-address":"ff:01:02:03:ff:04","ip-address":"192.168.50.100"}}}')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.100')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "reservation-get","arguments":{"subnet-id":1,"identifier-type": "hw-address","identifier":"ff:01:02:03:ff:04"}}')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_get_reservation_mysql_2(step):
    misc.test_setup(step)
    # address reserved without using command
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')

    srv_control.enable_db_backend_reservation(step, 'MySQL')
    srv_control.new_db_backend_reservation(step, 'MySQL', 'hw-address', 'ff:01:02:03:ff:04')
    srv_control.update_db_backend_reservation(step, 'hostname', 'reserved-hostname', 'MySQL', '1')
    srv_control.update_db_backend_reservation(step,
                                              'ipv4_address',
                                              '192.168.50.100',
                                              'MySQL',
                                              '1')
    srv_control.update_db_backend_reservation(step, 'dhcp4_subnet_id', '1', 'MySQL', '1')
    srv_control.upload_db_reservation(step, 'MySQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.100')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "reservation-get","arguments":{"subnet-id":1,"identifier-type": "hw-address","identifier":"ff:01:02:03:ff:04"}}')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_get_reservation_pgsql(step):
    misc.test_setup(step)
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')

    srv_control.enable_db_backend_reservation(step, 'PostgreSQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"hw-address":"ff:01:02:03:ff:04","ip-address":"192.168.50.100"}}}')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.100')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "reservation-get","arguments":{"subnet-id":1,"identifier-type": "hw-address","identifier":"ff:01:02:03:ff:04"}}')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_get_reservation_pgsql_2(step):
    misc.test_setup(step)
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')

    srv_control.enable_db_backend_reservation(step, 'PostgreSQL')
    srv_control.new_db_backend_reservation(step, 'PostgreSQL', 'hw-address', 'ff:01:02:03:ff:04')
    srv_control.update_db_backend_reservation(step,
                                              'hostname',
                                              'reserved-hostname',
                                              'PostgreSQL',
                                              '1')
    srv_control.update_db_backend_reservation(step,
                                              'ipv4_address',
                                              '192.168.50.100',
                                              'PostgreSQL',
                                              '1')
    srv_control.update_db_backend_reservation(step, 'dhcp4_subnet_id', '1', 'PostgreSQL', '1')
    srv_control.upload_db_reservation(step, 'PostgreSQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.100')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "reservation-get","arguments":{"subnet-id":1,"identifier-type": "hw-address","identifier":"ff:01:02:03:ff:04"}}')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_add_reservation_mysql_flex_id(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')

    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step, '2', 'identifier-expression', 'option[60].hex')
    srv_control.add_line(step, '"host-reservation-identifiers": [ "flex-id" ]')

    srv_control.enable_db_backend_reservation(step, 'MySQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"flex-id":"\'docsis3.0\'","ip-address":"192.168.50.100"}}}')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.100')

    misc.test_procedure(step)
    # Client adds to the message vendor_class_id with value docsis3.0.
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.100')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.100')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_add_reservation_mysql_flex_id_nak(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')

    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step, '2', 'identifier-expression', 'option[60].hex')
    srv_control.add_line(step, '"host-reservation-identifiers": [ "flex-id" ]')

    srv_control.enable_db_backend_reservation(step, 'MySQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"flex-id":"\'docsis3.0\'","ip-address":"192.168.50.100"}}}')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.100')

    misc.test_procedure(step)
    # Client adds to the message vendor_class_id with value docsis3.0.
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'NAK')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_add_reservation_pgsql_flex_id(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')

    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step, '2', 'identifier-expression', 'option[60].hex')
    srv_control.add_line(step, '"host-reservation-identifiers": [ "flex-id" ]')

    srv_control.enable_db_backend_reservation(step, 'PostgreSQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"flex-id":"\'docsis3.0\'","ip-address":"192.168.50.100"}}}')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.100')

    misc.test_procedure(step)
    # Client adds to the message vendor_class_id with value docsis3.0.
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.100')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.100')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_add_reservation_pgsql_flex_id_nak(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')

    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(step, '2', 'identifier-expression', 'option[60].hex')
    srv_control.add_line(step, '"host-reservation-identifiers": [ "flex-id" ]')

    srv_control.enable_db_backend_reservation(step, 'PostgreSQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"flex-id":"\'docsis3.0\'","ip-address":"192.168.50.100"}}}')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.100')

    misc.test_procedure(step)
    # Client adds to the message vendor_class_id with value docsis3.0.
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'NAK')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_add_reservation_complex_pgsql(step):
    misc.test_setup(step)
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.enable_db_backend_reservation(step, 'PostgreSQL')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', '01:0a:0b:0c:0d:0e:0f')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"client-id":"01:0a:0b:0c:0d:0e:0f","ip-address":"192.0.2.205","next-server":"192.0.2.1","server-hostname":"hal9000","boot-file-name":"/dev/null","option-data":[{"name":"domain-name-servers","data":"10.1.1.202,10.1.1.203"}],"client-classes":["special_snowflake","office"]}}}')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', '01:0a:0b:0c:0d:0e:0f')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.0.2.205')
    srv_msg.response_check_include_option(step, 'Response', None, '6')
    srv_msg.response_check_option_content(step, 'Response', '6', None, 'value', '10.1.1.203')
    srv_msg.response_check_option_content(step, 'Response', '6', None, 'value', '10.1.1.202')
    srv_msg.response_check_content(step, 'Response', None, 'sname', 'hal9000')
    srv_msg.response_check_content(step, 'Response', None, 'file', '/dev/null')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.0.2.205')
    srv_msg.client_does_include_with_value(step, 'client_id', '01:0a:0b:0c:0d:0e:0f')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '01:0a:0b:0c:0d:0e:0f')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.0.2.205')
    srv_msg.response_check_include_option(step, 'Response', None, '6')
    srv_msg.response_check_option_content(step, 'Response', '6', None, 'value', '10.1.1.203')
    srv_msg.response_check_option_content(step, 'Response', '6', None, 'value', '10.1.1.202')
    srv_msg.response_check_content(step, 'Response', None, 'sname', 'hal9000')
    srv_msg.response_check_content(step, 'Response', None, 'file', '/dev/null')


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
def test_v4_hosts_cmds_add_reservation_complex_mysql(step):
    misc.test_setup(step)
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.enable_db_backend_reservation(step, 'MySQL')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', '01:0a:0b:0c:0d:0e:0f')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.50')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"client-id":"01:0a:0b:0c:0d:0e:0f","ip-address":"192.0.2.205","next-server":"192.0.2.1","server-hostname":"hal9000","boot-file-name":"/dev/null","option-data":[{"name":"domain-name-servers","data":"10.1.1.202,10.1.1.203"}],"client-classes":["special_snowflake","office"]}}}')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', '01:0a:0b:0c:0d:0e:0f')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.0.2.205')
    srv_msg.response_check_include_option(step, 'Response', None, '6')
    srv_msg.response_check_option_content(step, 'Response', '6', None, 'value', '10.1.1.203')
    srv_msg.response_check_option_content(step, 'Response', '6', None, 'value', '10.1.1.202')
    srv_msg.response_check_content(step, 'Response', None, 'sname', 'hal9000')
    srv_msg.response_check_content(step, 'Response', None, 'file', '/dev/null')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.0.2.205')
    srv_msg.client_does_include_with_value(step, 'client_id', '01:0a:0b:0c:0d:0e:0f')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '01:0a:0b:0c:0d:0e:0f')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.0.2.205')
    srv_msg.response_check_include_option(step, 'Response', None, '6')
    srv_msg.response_check_option_content(step, 'Response', '6', None, 'value', '10.1.1.203')
    srv_msg.response_check_option_content(step, 'Response', '6', None, 'value', '10.1.1.202')
    srv_msg.response_check_content(step, 'Response', None, 'sname', 'hal9000')
    srv_msg.response_check_content(step, 'Response', None, 'file', '/dev/null')
