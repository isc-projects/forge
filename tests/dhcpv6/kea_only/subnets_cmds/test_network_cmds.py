"""Kea shared networks manipulation commands"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_msg
import srv_control
import misc


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v6_network_cmds_list():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:e::/64',
                                                       '2001:db8:e::1-2001:db8:e::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:f::/64',
                                                       '2001:db8:f::1-2001:db8:f::1')
    srv_control.config_srv('dns-servers', '1', '2001:db8::1,2001:db8::2')
    # first shared subnet
    srv_control.shared_subnet('0', '0')
    srv_control.shared_subnet('1', '0')
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet('interface-id', '"interface-abc"', '0')
    # second shared-subnet
    srv_control.shared_subnet('2', '1')
    srv_control.shared_subnet('3', '1')
    srv_control.set_conf_parameter_shared_subnet('name', '"name-xyz"', '1')
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', '1')
    srv_control.shared_subnet('4', '2')
    srv_control.shared_subnet('5', '2')
    srv_control.set_conf_parameter_shared_subnet('name', '"name-something"', '2')
    srv_control.set_conf_parameter_shared_subnet('relay', '{"ip-address":"2001:db8::1234"}', '2')
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-list","arguments":{}}')


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v6_network_cmds_get_by_name():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:e::/64',
                                                       '2001:db8:e::1-2001:db8:e::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:f::/64',
                                                       '2001:db8:f::1-2001:db8:f::1')
    srv_control.config_srv('dns-servers', '1', '2001:db8::1,2001:db8::2')
    # first shared subnet
    srv_control.shared_subnet('0', '0')
    srv_control.shared_subnet('1', '0')
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet('interface-id', '"interface-abc"', '0')
    # second shared-subnet
    srv_control.shared_subnet('2', '1')
    srv_control.shared_subnet('3', '1')
    srv_control.set_conf_parameter_shared_subnet('name', '"name-xyz"', '1')
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', '1')
    srv_control.shared_subnet('4', '2')
    srv_control.shared_subnet('5', '2')
    srv_control.set_conf_parameter_shared_subnet('name', '"name-something"', '2')
    srv_control.set_conf_parameter_shared_subnet('relay', '{"ip-address":"2001:db8::1234"}', '2')
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-get","arguments":{"name":"name-xyz"}}')


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v6_network_cmds_add_on_interface():
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.config_srv_opt('preference', '123')
    # Server is configured with domain-search option with value domain1.example.com,domain2.isc.org.
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
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
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content('Response', '13', '3', None, 'statuscode', '2')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "network6-add","arguments": {"shared-networks": [{"name": "name-abc","preferred-lifetime": 3000,"rebind-timer": 2000,"renew-timer": 1000,"valid-lifetime": 4000,"subnet6":[{"subnet":"2001:db8:a::/64","interface": "$(SERVER_IFACE)","pools":[{"pool":"2001:db8:a::1-2001:db8:a::1"}]}]}]}}')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-get","arguments":{"name": "name-abc"}}')
    srv_msg.forge_sleep('5', 'seconds')
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


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v6_network_cmds_add_on_interface_id():
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.config_srv_opt('preference', '123')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
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
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content('Response', '13', '3', None, 'statuscode', '2')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-add","arguments":{"shared-networks":[{"name": "name-abc","interface-id": "interface-abc","preferred-lifetime": 3000,"rebind-timer": 2000,"renew-timer": 1000,"valid-lifetime": 4000,"subnet6":[{"id":1,"pools": [{"pool": "2001:db8:1::1-2001:db8:1::10"}],"preferred-lifetime": 3000,"rebind-timer": 2000,"renew-timer": 1000,"reservation-mode": "all","subnet": "2001:db8:1::/64","valid-lifetime": 4000}]}]}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-get","arguments":{"name": "name-abc"}}')
    srv_msg.forge_sleep('5', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
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


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v6_network_cmds_add_on_relay_addr():
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.config_srv_opt('preference', '123')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
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
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content('Response', '13', '3', None, 'statuscode', '2')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-add","arguments":{"shared-networks":[{"name": "name-abc","relay":{"ip-address":"2001:db8::abcd"},"preferred-lifetime": 3000,"rebind-timer": 2000,"renew-timer": 1000,"valid-lifetime": 4000,"subnet6":[{"id":1,"pools": [{"pool": "2001:db8:1::1-2001:db8:1::10"}],"preferred-lifetime": 3000,"rebind-timer": 2000,"renew-timer": 1000,"reservation-mode": "all","subnet": "2001:db8:1::/64","valid-lifetime": 4000}]}]}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-get","arguments":{"name": "name-abc"}}')
    srv_msg.forge_sleep('5', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::abcd')
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


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v6_network_cmds_add_conflict():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    # first shared subnet
    srv_control.shared_subnet('0', '0')
    srv_control.shared_subnet('1', '0')
    srv_control.set_conf_parameter_shared_subnet('name', '"name-xyz"', '0')
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', '0')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-list","arguments":{}}')
    response = srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-add","arguments":{"shared-networks": [{"interface": "$(SERVER_IFACE)","name": "name-xyz","option-data": [],"preferred-lifetime": 0,"rapid-commit": false,"rebind-timer": 0,"relay": {"ip-address": "::"},"renew-timer": 0,"reservation-mode": "all","subnet6": [{"id": 3,"interface": "$(SERVER_IFACE)","option-data": [],"pd-pools": [],"pools": [{"option-data": [],"pool": "2001:db8:c::1/128"}],"preferred-lifetime": 3000,"rapid-commit": false,"rebind-timer": 2000,"relay": {"ip-address": "::"},"renew-timer": 1000,"reservation-mode": "all","subnet": "2001:db8:c::/64","valid-lifetime": 4000},{"id": 4,"interface": "$(SERVER_IFACE)","option-data": [],"pd-pools": [],"pools": [{"option-data": [],"pool": "2001:db8:d::1/128"}],"preferred-lifetime": 3000,"rapid-commit": false,"rebind-timer": 2000,"relay": {"ip-address": "::"},"renew-timer": 1000,"reservation-mode": "all","subnet": "2001:db8:d::/64","valid-lifetime": 4000}],"valid-lifetime": 0}]}}',
                                                exp_result=1)
    assert response['text'] == "duplicate network 'name-xyz' found in the configuration"

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

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_save_option('server-id')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

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

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:22')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:44:44')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content('Response', '13', '3', None, 'statuscode', '2')


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v6_network_cmds_del():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:e::/64',
                                                       '2001:db8:e::1-2001:db8:e::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:f::/64',
                                                       '2001:db8:f::1-2001:db8:f::1')
    srv_control.config_srv('dns-servers', '1', '2001:db8::1,2001:db8::2')
    # first shared subnet
    srv_control.shared_subnet('0', '0')
    srv_control.shared_subnet('1', '0')
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet('interface-id', '"interface-abc"', '0')
    # second shared-subnet
    srv_control.shared_subnet('2', '1')
    srv_control.shared_subnet('3', '1')
    srv_control.set_conf_parameter_shared_subnet('name', '"name-xyz"', '1')
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', '1')
    srv_control.shared_subnet('4', '2')
    srv_control.shared_subnet('5', '2')
    srv_control.set_conf_parameter_shared_subnet('name', '"name-something"', '2')
    srv_control.set_conf_parameter_shared_subnet('relay', '{"ip-address":"2001:db8::1234"}', '2')
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-list","arguments":{}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "network6-del","arguments":{"name":"name-xyz","subnets-action": "delete"}}')
    # Using UNIX socket on server in path control_socket send {"command": "network6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}
    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-list","arguments":{}}')


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v6_network_cmds_del_2():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    # first shared subnet
    srv_control.shared_subnet('0', '0')
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', '0')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
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

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-list","arguments":{}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "network6-del","arguments":{"name":"name-abc","subnets-action": "delete"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-list","arguments":{}}', exp_result=3)

    srv_msg.forge_sleep('5', 'seconds')
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
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content('Response', '13', '3', None, 'statuscode', '2')


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v6_network_cmds_del_non_existing():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:e::/64',
                                                       '2001:db8:e::1-2001:db8:e::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:f::/64',
                                                       '2001:db8:f::1-2001:db8:f::1')
    srv_control.config_srv('dns-servers', '1', '2001:db8::1,2001:db8::2')
    # first shared subnet
    srv_control.shared_subnet('0', '0')
    srv_control.shared_subnet('1', '0')
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet('interface-id', '"interface-abc"', '0')
    # second shared-subnet
    srv_control.shared_subnet('2', '1')
    srv_control.shared_subnet('3', '1')
    srv_control.set_conf_parameter_shared_subnet('name', '"name-xyz"', '1')
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', '1')
    srv_control.shared_subnet('4', '2')
    srv_control.shared_subnet('5', '2')
    srv_control.set_conf_parameter_shared_subnet('name', '"name-something"', '2')
    srv_control.set_conf_parameter_shared_subnet('relay', '{"ip-address":"2001:db8::1234"}', '2')
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-list","arguments":{}}')
    response = srv_msg.send_ctrl_cmd_via_socket('{"command": "network6-del","arguments":{"name":"name-xyzc"}}', exp_result=3)
    assert response['text'] == "no shared network with name 'name-xyzc' found"
    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-list","arguments":{}}')


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.network_cmds
def test_hook_v6_network_cmds_add_and_del():
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.config_srv_opt('preference', '123')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
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
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content('Response', '13', '3', None, 'statuscode', '2')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "network6-add","arguments": {"shared-networks": [{"name": "name-abc","preferred-lifetime": 3000,"rebind-timer": 2000,"renew-timer": 1000,"valid-lifetime": 4000,"subnet6":[{"subnet":"2001:db8:a::/64","interface": "$(SERVER_IFACE)","pools":[{"pool":"2001:db8:a::1-2001:db8:a::1"}]}]}]}}')

    srv_msg.forge_sleep('5', 'seconds')
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
                                             '2001:db8:a::1')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "network6-del","arguments":{"name":"name-abc","subnets-action": "delete"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"network6-list","arguments":{}}', exp_result=3)

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
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content('Response', '13', '3', None, 'statuscode', '2')
