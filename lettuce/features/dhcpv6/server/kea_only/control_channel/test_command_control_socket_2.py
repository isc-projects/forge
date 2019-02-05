"""Kea Control Channel - socket"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import misc
from features import srv_msg
from features import srv_control


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_socket_config_get(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "config-get","arguments": {}}')
    # Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command": "list-commands","arguments": {}}
    # compare json result with config file


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_socket_config_test(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    # To global section of the config add file line: "expired-leases-processing":{"flush-reclaimed-timer-wait-time": 0,"hold-reclaimed-time": 0,"max-reclaim-leases": 100,"max-reclaim-time": 0,"reclaim-timer-wait-time": 0,"unwarned-reclaim-cycles": 5}
    # To global section of the config add file line: "expired-leases-processing":{"flush-reclaimed-timer-wait-time": 0,"hold-reclaimed-time": 0,"max-reclaim-leases": 100,"max-reclaim-time": 0,"reclaim-timer-wait-time": 0,"unwarned-reclaim-cycles": 5}

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::f')
    srv_control.config_srv_prefix(step, '2001:db8:1::', '0', '90', '96')
    srv_control.open_control_channel(step,
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

    # Sleep for 10 seconds.
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "config-test","arguments": $(SERVER_CONFIG) }')
    # should be ok

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::f')
    srv_control.config_srv_prefix(step, '2001:db8:1::', '0', '90', '96')
    srv_control.open_control_channel(step,
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
    #
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "config-test","arguments": $(SERVER_CONFIG) }')
    # should NOT be ok


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_socket_config_write(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
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
    srv_control.generate_config_files(step)

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "config-set","arguments":  $(SERVER_CONFIG) }')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "config-write","arguments":  { "filename": "$(SOFTWARE_INSTALL_DIR)/etc/kea/kea.conf"} }')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:22')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
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

    # Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command": "list-commands","arguments": {}}
    # Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command": "config-write","parameters":  { "filename": "abc"} }
    # Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command": "config-write","arguments":  { "filename": "whatever"} }
    # Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command": "config-write","arguments":  { "filename": "installed/git/etc/kea/kea.conf"} }
    # Pause the Test.
    srv_control.start_srv(step, 'DHCP', 'restarted')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:33')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
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
def test_control_channel_socket_config_reload(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
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

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "list-commands","arguments": {}}')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    # Generate server configuration file.
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "config-reload","arguments":  {} }')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
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
