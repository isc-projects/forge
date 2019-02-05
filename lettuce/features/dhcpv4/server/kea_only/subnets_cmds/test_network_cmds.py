"""Kea Subnet manipulation commands"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_control
from features import misc
from features import srv_msg


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v4_network_cmds_list(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.52.0/24',
                                                       '192.168.52.1-192.168.52.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.53.0/24',
                                                       '192.168.53.1-192.168.53.1')
    # first shared subnet
    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '0')
    # second shared-subnet
    srv_control.shared_subnet(step, '2', '1')
    srv_control.shared_subnet(step, '3', '1')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-xyz"', '1')
    srv_control.set_conf_parameter_shared_subnet(step,
                                                 'relay',
                                                 '{"ip-address":"$(GIADDR4)"}',
                                                 '1')

    srv_control.config_srv(step, 'time-servers', '0', '199.199.199.10')
    srv_control.config_srv(step, 'time-servers', '2', '199.199.199.100')
    srv_control.config_srv(step, 'time-servers', '3', '199.199.199.200')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_subnet_cmds.so')

    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"network4-list","arguments":{}}')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v4_network_cmds_get_by_name(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.52.0/24',
                                                       '192.168.52.1-192.168.52.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.53.0/24',
                                                       '192.168.53.1-192.168.53.1')
    # first shared subnet
    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '0')
    # second shared-subnet
    srv_control.shared_subnet(step, '2', '1')
    srv_control.shared_subnet(step, '3', '1')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-xyz"', '1')
    srv_control.set_conf_parameter_shared_subnet(step,
                                                 'relay',
                                                 '{"ip-address":"$(GIADDR4)"}',
                                                 '1')

    srv_control.config_srv(step, 'time-servers', '0', '199.199.199.10')
    srv_control.config_srv(step, 'time-servers', '2', '199.199.199.100')
    srv_control.config_srv(step, 'time-servers', '3', '199.199.199.200')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_subnet_cmds.so')

    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"network4-get","arguments":{"name":"name-xyz"}}')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v4_network_cmds_add(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '$(EMPTY)', '$(EMPTY)')
    srv_control.config_srv_opt(step, 'domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"network4-list","arguments":{}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"network4-add","arguments":{"shared-networks": [{"name": "name-xyz","rebind-timer": 100,"renew-timer": 100,"valid-lifetime": 400,"subnet4": [{"interface": "$(SERVER_IFACE)", "pools": [{"pool": "192.168.50.1/32"}],"rebind-timer": 2000,"renew-timer": 1000,"subnet": "192.168.50.0/24","valid-lifetime": 4000}]}]}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"network4-get","arguments":{"name": "name-xyz"}}')

    srv_msg.forge_sleep(step, '3', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '6')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v4_network_cmds_add_conflict(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.52.0/24',
                                                       '192.168.52.1-192.168.52.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.53.0/24',
                                                       '192.168.53.1-192.168.53.1')
    # first shared subnet
    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '0')
    # second shared-subnet
    srv_control.shared_subnet(step, '2', '1')
    srv_control.shared_subnet(step, '3', '1')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-xyz"', '1')
    srv_control.set_conf_parameter_shared_subnet(step,
                                                 'relay',
                                                 '{"ip-address":"$(GIADDR4)"}',
                                                 '1')

    srv_control.config_srv(step, 'time-servers', '0', '199.199.199.10')
    srv_control.config_srv(step, 'time-servers', '2', '199.199.199.100')
    srv_control.config_srv(step, 'time-servers', '3', '199.199.199.200')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_subnet_cmds.so')

    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"network4-list","arguments":{}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"network4-add","arguments":{"shared-networks": [{"match-client-id": true,"name": "name-xyz","option-data": [],"rebind-timer": 0,"relay": {"ip-address": "0.0.0.0"},"renew-timer": 0,"reservation-mode": "all","subnet4": [{"4o6-interface": "","4o6-interface-id": "","4o6-subnet": "","boot-file-name": "","id": 3,"match-client-id": true,"next-server": "0.0.0.0","option-data": [{"always-send": false,"code": 4,"csv-format": false,"data": "C7C7C764","name": "time-servers","space": "dhcp4"}],"pools": [{"option-data": [],"pool": "192.168.52.1/32"}],"rebind-timer": 2000,"relay": {"ip-address": "192.168.50.249"},"renew-timer": 1000,"reservation-mode": "all","server-hostname": "","subnet": "192.168.52.0/24","valid-lifetime": 4000},{"4o6-interface": "","4o6-interface-id": "","4o6-subnet": "","boot-file-name": "","id": 4,"match-client-id": true,"next-server": "0.0.0.0","option-data": [{"always-send": false,"code": 4,"csv-format": false,"data": "C7C7C7C8","name": "time-servers","space": "dhcp4"}],"pools": [{"option-data": [],"pool": "192.168.53.1/32"}],"rebind-timer": 2000,"relay": {"ip-address": "192.168.50.249"},"renew-timer": 1000,"reservation-mode": "all","server-hostname": "","subnet": "192.168.53.0/24","valid-lifetime": 4000}],"valid-lifetime": 0}]}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"network4-get","arguments":{"name": "name-xyz"}}')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v4_network_cmds_del(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.1')
    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '0')

    srv_control.config_srv(step, 'time-servers', '0', '199.199.199.10')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_subnet_cmds.so')

    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '6')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"network4-list","arguments":{}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"network4-del","arguments":{"name":"name-abc","subnets-action": "delete"}}')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v4_network_cmds_del_keep_subnet(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.1')
    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '0')

    srv_control.config_srv(step, 'time-servers', '0', '199.199.199.10')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_subnet_cmds.so')

    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '6')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"network4-list","arguments":{}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"network4-del","arguments":{"name":"name-abc","subnets-action": "keep"}}')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '6')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"network4-list","arguments":{}}')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v4_network_cmds_del_non_existing(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.52.0/24',
                                                       '192.168.52.1-192.168.52.1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.53.0/24',
                                                       '192.168.53.1-192.168.53.1')
    # first shared subnet
    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '0')
    # second shared-subnet
    srv_control.shared_subnet(step, '2', '1')
    srv_control.shared_subnet(step, '3', '1')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-xyz"', '1')
    srv_control.set_conf_parameter_shared_subnet(step,
                                                 'relay',
                                                 '{"ip-address":"$(GIADDR4)"}',
                                                 '1')

    srv_control.config_srv(step, 'time-servers', '0', '199.199.199.10')
    srv_control.config_srv(step, 'time-servers', '2', '199.199.199.100')
    srv_control.config_srv(step, 'time-servers', '3', '199.199.199.200')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_subnet_cmds.so')

    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"network4-del","arguments":{"name":"name-xxyz,"subnets-action": "delete""}}')
    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"network4-list","arguments":{}}')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v4_network_cmds_del_global_options(step):
    misc.test_setup(step)
    srv_control.config_srv_opt(step, 'domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '$(EMPTY)')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.1')
    # first shared subnet
    srv_control.shared_subnet(step, '1', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '0')

    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '6')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "network4-del","arguments":{"name":"name-abc","subnets-action": "delete"}}')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    # That needs subnet with empty pool to work
    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '6')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg(step, 'INFORM')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_include_option(step, 'Response', None, '6')
    srv_msg.response_check_option_content(step, 'Response', '6', None, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(step, 'Response', '6', None, 'value', '100.100.100.1')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v4_network_cmds_add_and_del(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '$(EMPTY)', '$(EMPTY)')
    srv_control.config_srv_opt(step, 'domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command":"network4-add","arguments":{"shared-networks": [{"name": "name-xyz","rebind-timer": 100,"renew-timer": 100,"valid-lifetime": 400,"subnet4": [{"interface": "$(SERVER_IFACE)", "pools": [{"pool": "192.168.50.1/32"}],"rebind-timer": 2000,"renew-timer": 1000,"subnet": "192.168.50.0/24","valid-lifetime": 4000}]}]}}')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_requests_option(step, '6')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    srv_msg.send_through_socket_server_site(step,
                                            '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket',
                                            '{"command": "network4-del","arguments":{"name":"name-xyz","subnets-action": "delete"}}')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)
