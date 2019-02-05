"""Kea Control Channel Script"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_control
from features import srv_msg
from features import misc


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_keashell_dhcp_disable_timer(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '127.0.0.1',
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

    srv_msg.execute_shell_with_args(step,
                                    'python',
                                    '$(SOFTWARE_INSTALL_DIR)/sbin/kea-shell',
                                    '--host 127.0.0.1 --port 8000 --service dhcp4 dhcp-disable <<<\'"max-period": 5\'')

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
def test_control_channel_keashell_dhcp_disable(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '127.0.0.1',
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

    srv_msg.execute_shell_with_args(step,
                                    'python',
                                    '$(SOFTWARE_INSTALL_DIR)/sbin/kea-shell',
                                    '--host 127.0.0.1 --port 8000 --service dhcp4 dhcp-disable <<<\'\'')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_keashell_dhcp_disable_and_enable(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '127.0.0.1',
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

    srv_msg.execute_shell_with_args(step,
                                    'python',
                                    '$(SOFTWARE_INSTALL_DIR)/sbin/kea-shell',
                                    '--host 127.0.0.1 --port 8000 --service dhcp4 dhcp-disable <<<\'\'')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    srv_msg.execute_shell_with_args(step,
                                    'python',
                                    '$(SOFTWARE_INSTALL_DIR)/sbin/kea-shell',
                                    '--host 127.0.0.1 --port 8000 --service dhcp4 dhcp-enable <<<\'\'')

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
def test_control_channel_keashell_set_config_basic(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '127.0.0.1',
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

    # this command is with new configuration
    srv_msg.execute_shell_with_args(step,
                                    'python',
                                    '$(SOFTWARE_INSTALL_DIR)/sbin/kea-shell',
                                    '--host 127.0.0.1 --port 8000 --service dhcp4 config-set <<<\'"Dhcp4":{"renew-timer":1000,"rebind-timer":2000,"valid-lifetime":4000,"interfaces-config":{"interfaces":["$(SERVER_IFACE)"]},"subnet4":[{"subnet":"192.168.51.0/24","interface":"$(SERVER_IFACE)","pools":[{"pool":"192.168.51.1-192.168.51.1"}]}],"lease-database":{"type":"memfile"},"control-socket":{"socket-type":"unix","socket-name":"$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket"}}\'')

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
def test_control_channel_keashell_after_restart_load_config_file(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '127.0.0.1',
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

    srv_msg.execute_shell_with_args(step,
                                    'python',
                                    '$(SOFTWARE_INSTALL_DIR)/sbin/kea-shell',
                                    '--host 127.0.0.1 --port 8000 --service dhcp4 config-set <<<\'"Dhcp4":{"renew-timer":1000,"rebind-timer":2000,"valid-lifetime":4000,"interfaces-config":{"interfaces":["$(SERVER_IFACE)"]},"subnet4":[{"subnet":"192.168.51.0/24","interface":"$(SERVER_IFACE)","pools":[{"pool":"192.168.51.1-192.168.51.1"}]}],"lease-database":{"type":"memfile"},"control-socket":{"socket-type":"unix","socket-name":"$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket"}}\'')

    srv_msg.forge_sleep(step, '$(SLEEP_TIME_2)', 'seconds')

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
def test_control_channel_keashell_get_config(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '127.0.0.1',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    srv_msg.execute_shell_with_args(step,
                                    'python',
                                    '$(SOFTWARE_INSTALL_DIR)/sbin/kea-shell',
                                    '--host 127.0.0.1 --port 8000 --service dhcp4 config-get <<<\'\'')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.kea_only
@pytest.mark.disabled
def test_control_channel_keashell_test_config(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '127.0.0.1',
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

    srv_msg.execute_shell_with_args(step,
                                    'python',
                                    '$(SOFTWARE_INSTALL_DIR)/sbin/kea-shell',
                                    '--host 127.0.0.1 --port 8000 --service dhcp4 config-test <<<\'$(SERVER_CONFIG)\'')

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

    srv_msg.execute_shell_with_args(step,
                                    'python',
                                    '$(SOFTWARE_INSTALL_DIR)/sbin/kea-shell',
                                    '--host 127.0.0.1 --port 8000 --service dhcp4 config-set <<<\'$(SERVER_CONFIG)\'')
    srv_msg.forge_sleep(step, '$(SLEEP_TIME_2)', 'seconds')

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
def test_control_channel_keashell_write_config(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '127.0.0.1',
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
                                      'localhost',
                                      '8000',
                                      'UNIX',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.generate_config_files(step)

    srv_msg.execute_shell_with_args(step,
                                    'python',
                                    '$(SOFTWARE_INSTALL_DIR)/sbin/kea-shell',
                                    '--host 127.0.0.1 --port 8000 --service dhcp4 config-set <<<\'"Dhcp4":{"renew-timer":1000,"rebind-timer":2000,"valid-lifetime":4000,"interfaces-config":{"interfaces":["$(SERVER_IFACE)"]},"subnet4":[{"subnet":"192.168.51.0/24","interface":"$(SERVER_IFACE)","pools":[{"pool":"192.168.51.1-192.168.51.1"}]}],"lease-database":{"type":"memfile"},"control-socket":{"socket-type":"unix","socket-name":"$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket"}}\'')
    srv_msg.forge_sleep(step, '$(SLEEP_TIME_2)', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    srv_msg.execute_shell_with_args(step,
                                    'python',
                                    '$(SOFTWARE_INSTALL_DIR)/sbin/kea-shell',
                                    '--host 127.0.0.1 --port 8000 --service dhcp4 config-write <<<\'\'')

    # TODO tests needed for not valid/not permitted paths
    srv_control.start_srv(step, 'DHCP', 'restarted')

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
def test_control_channel_socket_reload_config(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '127.0.0.1',
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
                                      '127.0.0.1',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_msg.execute_shell_with_args(step,
                                    'python',
                                    '$(SOFTWARE_INSTALL_DIR)/sbin/kea-shell',
                                    '--host 127.0.0.1 --port 8000 --service dhcp4 config-reload <<<\'\'')

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
