"""Kea HA states"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_control
import srv_msg


@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.HA
@pytest.mark.HA_state
def test_v6_hooks_HA_state_hold_lb_always():

    # HA SERVER 1
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(MGMT_ADDRESS)')
    srv_control.configure_loggers('kea-dhcp6', 'DEBUG', '99')
    srv_control.configure_loggers('kea-ctrl-agent', 'DEBUG', '99', 'kea.log-CTRL')
    srv_control.add_hooks('libdhcp_lease_cmds.so')

    srv_control.add_ha_hook('libdhcp_ha.so')
    srv_control.add_parameter_to_ha_hook('machine-state', '{"state":"waiting","pause":"always"}')
    srv_control.add_parameter_to_ha_hook('machine-state', '{"state":"syncing","pause":"always"}')
    srv_control.add_parameter_to_ha_hook('machine-state', '{"state":"ready","pause":"always"}')
    srv_control.add_parameter_to_ha_hook('machine-state',
                                         '{"state":"load-balancing","pause":"always"}')
    srv_control.add_parameter_to_ha_hook('machine-state',
                                         '{"state":"partner-down","pause":"always"}')
    srv_control.add_parameter_to_ha_hook('this-server-name', '"server1"')
    srv_control.add_parameter_to_ha_hook('mode', '"load-balancing"')
    srv_control.add_parameter_to_ha_hook('heartbeat-delay', '1000')
    srv_control.add_parameter_to_ha_hook('max-response-delay', '1001')
    srv_control.add_parameter_to_ha_hook('max-unacked-clients', '0')
    srv_control.add_parameter_to_ha_hook('max-ack-delay', '0')

    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server1","url":"http://$(MGMT_ADDRESS):8000/","role":"primary","auto-failover":true}')
    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server2","url":"http://$(MGMT_ADDRESS_2):8000/","role":"secondary","auto-failover":true}')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    # HA SERVER 2
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(MGMT_ADDRESS_2)')
    srv_control.configure_loggers('kea-dhcp6', 'DEBUG', '99')
    srv_control.configure_loggers('kea-ctrl-agent', 'DEBUG', '99', 'kea.log-CTRL2')
    srv_control.add_hooks('libdhcp_lease_cmds.so')

    srv_control.add_ha_hook('libdhcp_ha.so')
    srv_control.add_parameter_to_ha_hook('this-server-name', '"server2"')
    srv_control.add_parameter_to_ha_hook('mode', '"load-balancing"')
    srv_control.add_parameter_to_ha_hook('heartbeat-delay', '1000')
    srv_control.add_parameter_to_ha_hook('max-response-delay', '1001')
    srv_control.add_parameter_to_ha_hook('max-unacked-clients', '0')
    srv_control.add_parameter_to_ha_hook('max-ack-delay', '0')

    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server1","url":"http://$(MGMT_ADDRESS):8000/","role": "primary","auto-failover":true}')
    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server2","url":"http://$(MGMT_ADDRESS_2):8000/","role": "secondary","auto-failover":true}')

    srv_control.build_and_send_config_files_dest_addr('SSH', 'config-file', '$(MGMT_ADDRESS_2)')
    srv_control.remote_start_srv('DHCP', 'started', '$(MGMT_ADDRESS_2)')

    srv_msg.forge_sleep('5', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "waiting"')
    srv_msg.json_response_parsing('result', None, '0')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "waiting"')
    srv_msg.json_response_parsing('result', None, '0')

    srv_msg.forge_sleep('10', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "waiting"')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "waiting"')

    # continue server1 from WAITING
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine continues')

    srv_msg.forge_sleep('7', 'seconds')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "syncing"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "waiting"')

    # continue server1 from SYNCING
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine continues')

    srv_msg.forge_sleep('10', 'seconds')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.forge_sleep('3', 'seconds')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    # continue server1 from READY
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine continues')

    srv_msg.forge_sleep('5', 'seconds')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "load-balancing"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "load-balancing"')

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

    srv_control.remote_start_srv('DHCP', 'stopped', '$(MGMT_ADDRESS_2)')

    srv_msg.forge_sleep('10', 'seconds')

    # server1 has to keep load-balancing
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "load-balancing"')

    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "load-balancing"')

    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "load-balancing"')

    # continue server1 from load-balancing
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine continues')
    srv_msg.forge_sleep('10', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.forge_sleep('10', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')

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

    srv_control.remote_start_srv('DHCP', 'started', '$(MGMT_ADDRESS_2)')

    srv_msg.forge_sleep('10', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')

    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')

    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')
    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')

    # continue server1 from partner-down
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine continues')

    srv_msg.forge_sleep('10', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "load-balancing"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "load-balancing"')

    srv_control.remote_start_srv('DHCP', 'stopped', '$(MGMT_ADDRESS_2)')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "load-balancing"')

    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "load-balancing"')

    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "load-balancing"')

    # continue AGAIN from load-balancing
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine continues')

    srv_msg.forge_sleep('10', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')

    srv_control.remote_start_srv('DHCP', 'started', '$(MGMT_ADDRESS_2)')

    srv_msg.forge_sleep('10', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')

    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')

    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')

    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine continues')

    srv_msg.forge_sleep('10', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "load-balancing"')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "load-balancing"')

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


@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.HA
@pytest.mark.HA_state
def test_v6_hooks_HA_state_hold_lb_once():

    # HA SERVER 1
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(MGMT_ADDRESS)')
    srv_control.configure_loggers('kea-dhcp6', 'DEBUG', '99')
    srv_control.configure_loggers('kea-ctrl-agent', 'DEBUG', '99', 'kea.log-CTRL')
    srv_control.add_hooks('libdhcp_lease_cmds.so')

    srv_control.add_ha_hook('libdhcp_ha.so')
    srv_control.add_parameter_to_ha_hook('machine-state', '{"state":"waiting","pause":"once"}')
    srv_control.add_parameter_to_ha_hook('machine-state', '{"state":"syncing","pause":"once"}')
    srv_control.add_parameter_to_ha_hook('machine-state', '{"state":"ready","pause":"once"}')
    srv_control.add_parameter_to_ha_hook('machine-state',
                                         '{"state":"load-balancing","pause":"once"}')
    srv_control.add_parameter_to_ha_hook('machine-state',
                                         '{"state":"partner-down","pause":"once"}')

    srv_control.add_parameter_to_ha_hook('this-server-name', '"server1"')
    srv_control.add_parameter_to_ha_hook('mode', '"load-balancing"')
    srv_control.add_parameter_to_ha_hook('heartbeat-delay', '1000')
    srv_control.add_parameter_to_ha_hook('max-response-delay', '1001')
    srv_control.add_parameter_to_ha_hook('max-unacked-clients', '0')
    srv_control.add_parameter_to_ha_hook('max-ack-delay', '0')
    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server1","url":"http://$(MGMT_ADDRESS):8000/","role":"primary","auto-failover":true}')
    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server2","url":"http://$(MGMT_ADDRESS_2):8000/","role":"secondary","auto-failover":true}')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    # HA SERVER 2
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(MGMT_ADDRESS_2)')
    srv_control.configure_loggers('kea-dhcp6', 'DEBUG', '99')
    srv_control.configure_loggers('kea-ctrl-agent', 'DEBUG', '99', 'kea.log-CTRL2')
    srv_control.add_hooks('libdhcp_lease_cmds.so')

    srv_control.add_ha_hook('libdhcp_ha.so')
    srv_control.add_parameter_to_ha_hook('this-server-name', '"server2"')
    srv_control.add_parameter_to_ha_hook('mode', '"load-balancing"')
    srv_control.add_parameter_to_ha_hook('heartbeat-delay', '1000')
    srv_control.add_parameter_to_ha_hook('max-response-delay', '1001')
    srv_control.add_parameter_to_ha_hook('max-unacked-clients', '0')
    srv_control.add_parameter_to_ha_hook('max-ack-delay', '0')
    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server1","url":"http://$(MGMT_ADDRESS):8000/","role": "primary","auto-failover":true}')
    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server2","url":"http://$(MGMT_ADDRESS_2):8000/","role": "secondary","auto-failover":true}')

    srv_control.build_and_send_config_files_dest_addr('SSH', 'config-file', '$(MGMT_ADDRESS_2)')
    srv_control.remote_start_srv('DHCP', 'started', '$(MGMT_ADDRESS_2)')
    srv_msg.forge_sleep('5', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "waiting"')
    srv_msg.json_response_parsing('result', None, '0')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "waiting"')
    srv_msg.json_response_parsing('result', None, '0')

    srv_msg.forge_sleep('10', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "waiting"')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "waiting"')

    # continue server1 from WAITING
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine continues')

    srv_msg.forge_sleep('7', 'seconds')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "syncing"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "waiting"')

    # continue server1 from SYNCING
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine continues')

    srv_msg.forge_sleep('10', 'seconds')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.forge_sleep('3', 'seconds')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    # continue server1 from READY
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine continues')

    srv_msg.forge_sleep('5', 'seconds')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "load-balancing"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "load-balancing"')

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

    srv_control.remote_start_srv('DHCP', 'stopped', '$(MGMT_ADDRESS_2)')

    srv_msg.forge_sleep('10', 'seconds')

    # server1 has to keep load-balancing
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "load-balancing"')

    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "load-balancing"')

    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "load-balancing"')

    # continue server1 from load-balancing
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine continues')
    srv_msg.forge_sleep('10', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')

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

    srv_control.remote_start_srv('DHCP', 'started', '$(MGMT_ADDRESS_2)')

    srv_msg.forge_sleep('10', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')
    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')
    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine continues')

    srv_msg.forge_sleep('10', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "load-balancing"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "load-balancing"')

    srv_control.remote_start_srv('DHCP', 'stopped', '$(MGMT_ADDRESS_2)')
    srv_msg.forge_sleep('10', 'seconds')

    # this time - no paused states!
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine is not paused')
    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine is not paused')
    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine is not paused')
    srv_msg.forge_sleep('5', 'seconds')

    srv_control.remote_start_srv('DHCP', 'started', '$(MGMT_ADDRESS_2)')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "waiting"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine is not paused')

    srv_msg.forge_sleep('10', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "load-balancing"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "load-balancing"')

    srv_msg.forge_sleep('3', 'seconds')

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


@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.HA
@pytest.mark.HA_state
def test_v6_hooks_HA_state_hold_hs_once():

    # HA SERVER 1
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(MGMT_ADDRESS)')
    srv_control.configure_loggers('kea-dhcp6', 'DEBUG', '99')
    srv_control.configure_loggers('kea-ctrl-agent', 'DEBUG', '99', 'kea.log-CTRL')

    srv_control.add_hooks('libdhcp_lease_cmds.so')

    srv_control.add_ha_hook('libdhcp_ha.so')
    srv_control.add_parameter_to_ha_hook('machine-state', '{"state":"waiting","pause":"once"}')
    srv_control.add_parameter_to_ha_hook('machine-state', '{"state":"syncing","pause":"once"}')
    srv_control.add_parameter_to_ha_hook('machine-state', '{"state":"ready","pause":"once"}')
    srv_control.add_parameter_to_ha_hook('machine-state',
                                         '{"state":"hot-standby","pause":"once"}')
    srv_control.add_parameter_to_ha_hook('machine-state',
                                         '{"state":"partner-down","pause":"once"}')
    srv_control.add_parameter_to_ha_hook('this-server-name', '"server1"')
    srv_control.add_parameter_to_ha_hook('mode', '"hot-standby"')
    srv_control.add_parameter_to_ha_hook('heartbeat-delay', '1000')
    srv_control.add_parameter_to_ha_hook('max-response-delay', '1001')
    srv_control.add_parameter_to_ha_hook('max-unacked-clients', '0')
    srv_control.add_parameter_to_ha_hook('max-ack-delay', '0')

    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server1","url":"http://$(MGMT_ADDRESS):8000/","role":"primary","auto-failover":true}')
    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server2","url":"http://$(MGMT_ADDRESS_2):8000/","role":"standby","auto-failover":true}')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    # HA SERVER 2
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(MGMT_ADDRESS_2)')
    srv_control.configure_loggers('kea-dhcp6', 'DEBUG', '99')
    srv_control.configure_loggers('kea-ctrl-agent', 'DEBUG', '99', 'kea.log-CTRL2')

    srv_control.add_hooks('libdhcp_lease_cmds.so')

    srv_control.add_ha_hook('libdhcp_ha.so')
    srv_control.add_parameter_to_ha_hook('this-server-name', '"server2"')
    srv_control.add_parameter_to_ha_hook('mode', '"hot-standby"')
    srv_control.add_parameter_to_ha_hook('heartbeat-delay', '1000')
    srv_control.add_parameter_to_ha_hook('max-response-delay', '1001')
    srv_control.add_parameter_to_ha_hook('max-unacked-clients', '0')
    srv_control.add_parameter_to_ha_hook('max-ack-delay', '0')

    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server1","url":"http://$(MGMT_ADDRESS):8000/","role": "primary","auto-failover":true}')
    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server2","url":"http://$(MGMT_ADDRESS_2):8000/","role": "standby","auto-failover":true}')

    srv_control.build_and_send_config_files_dest_addr('SSH', 'config-file', '$(MGMT_ADDRESS_2)')
    srv_control.remote_start_srv('DHCP', 'started', '$(MGMT_ADDRESS_2)')
    srv_msg.forge_sleep('5', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "waiting"')
    srv_msg.json_response_parsing('result', None, '0')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "waiting"')
    srv_msg.json_response_parsing('result', None, '0')

    srv_msg.forge_sleep('10', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "waiting"')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "waiting"')

    # continue server1 from WAITING
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine continues')

    srv_msg.forge_sleep('7', 'seconds')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "syncing"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "waiting"')

    # continue server1 from SYNCING
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine continues')

    srv_msg.forge_sleep('10', 'seconds')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.forge_sleep('3', 'seconds')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    # continue server1 from READY
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine continues')

    srv_msg.forge_sleep('5', 'seconds')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "hot-standby"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "hot-standby"')

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

    srv_control.remote_start_srv('DHCP', 'stopped', '$(MGMT_ADDRESS_2)')

    srv_msg.forge_sleep('10', 'seconds')

    # server1 has to keep hot-standby
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "hot-standby"')

    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "hot-standby"')

    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "hot-standby"')

    # continue server1 from hot-standby
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine continues')
    srv_msg.forge_sleep('10', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')

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

    srv_control.remote_start_srv('DHCP', 'started', '$(MGMT_ADDRESS_2)')

    srv_msg.forge_sleep('10', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')
    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')
    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine continues')

    srv_msg.forge_sleep('10', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "hot-standby"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "hot-standby"')

    srv_control.remote_start_srv('DHCP', 'stopped', '$(MGMT_ADDRESS_2)')
    srv_msg.forge_sleep('10', 'seconds')

    # this time - no paused states!
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine is not paused')
    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine is not paused')
    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine is not paused')
    srv_msg.forge_sleep('5', 'seconds')

    srv_control.remote_start_srv('DHCP', 'started', '$(MGMT_ADDRESS_2)')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "waiting"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine is not paused')
    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "hot-standby"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "hot-standby"')

    srv_msg.forge_sleep('3', 'seconds')

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


@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.HA
@pytest.mark.HA_state
def test_v6_hooks_HA_state_hold_hs_always():

    # HA SERVER 1
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(MGMT_ADDRESS)')
    srv_control.configure_loggers('kea-dhcp6', 'DEBUG', '99')
    srv_control.configure_loggers('kea-ctrl-agent', 'DEBUG', '99', 'kea.log-CTRL')

    srv_control.add_hooks('libdhcp_lease_cmds.so')

    srv_control.add_ha_hook('libdhcp_ha.so')
    srv_control.add_parameter_to_ha_hook('machine-state', '{"state":"waiting","pause":"always"}')
    srv_control.add_parameter_to_ha_hook('machine-state', '{"state":"syncing","pause":"always"}')
    srv_control.add_parameter_to_ha_hook('machine-state', '{"state":"ready","pause":"always"}')
    srv_control.add_parameter_to_ha_hook('machine-state',
                                         '{"state":"hot-standby","pause":"always"}')
    srv_control.add_parameter_to_ha_hook('machine-state',
                                         '{"state":"partner-down","pause":"always"}')
    srv_control.add_parameter_to_ha_hook('this-server-name', '"server1"')
    srv_control.add_parameter_to_ha_hook('mode', '"hot-standby"')
    srv_control.add_parameter_to_ha_hook('heartbeat-delay', '1000')
    srv_control.add_parameter_to_ha_hook('max-response-delay', '1001')
    srv_control.add_parameter_to_ha_hook('max-unacked-clients', '0')
    srv_control.add_parameter_to_ha_hook('max-ack-delay', '0')

    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server1","url":"http://$(MGMT_ADDRESS):8000/","role":"primary","auto-failover":true}')
    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server2","url":"http://$(MGMT_ADDRESS_2):8000/","role":"standby","auto-failover":true}')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    # HA SERVER 2
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(MGMT_ADDRESS_2)')
    srv_control.configure_loggers('kea-dhcp6', 'DEBUG', '99')
    srv_control.configure_loggers('kea-ctrl-agent', 'DEBUG', '99', 'kea.log-CTRL2')

    srv_control.add_hooks('libdhcp_lease_cmds.so')

    srv_control.add_ha_hook('libdhcp_ha.so')
    srv_control.add_parameter_to_ha_hook('this-server-name', '"server2"')
    srv_control.add_parameter_to_ha_hook('mode', '"hot-standby"')
    srv_control.add_parameter_to_ha_hook('heartbeat-delay', '1000')
    srv_control.add_parameter_to_ha_hook('max-response-delay', '1001')
    srv_control.add_parameter_to_ha_hook('max-unacked-clients', '0')
    srv_control.add_parameter_to_ha_hook('max-ack-delay', '0')

    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server1","url":"http://$(MGMT_ADDRESS):8000/","role": "primary","auto-failover":true}')
    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server2","url":"http://$(MGMT_ADDRESS_2):8000/","role": "standby","auto-failover":true}')

    srv_control.build_and_send_config_files_dest_addr('SSH', 'config-file', '$(MGMT_ADDRESS_2)')
    srv_control.remote_start_srv('DHCP', 'started', '$(MGMT_ADDRESS_2)')

    srv_msg.forge_sleep('5', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "waiting"')
    srv_msg.json_response_parsing('result', None, '0')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "waiting"')
    srv_msg.json_response_parsing('result', None, '0')

    srv_msg.forge_sleep('10', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "waiting"')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "waiting"')

    # continue server1 from WAITING
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine continues')

    srv_msg.forge_sleep('7', 'seconds')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "syncing"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "waiting"')

    # continue server1 from SYNCING
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine continues')

    srv_msg.forge_sleep('10', 'seconds')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.forge_sleep('3', 'seconds')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    # continue server1 from READY
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine continues')

    srv_msg.forge_sleep('5', 'seconds')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "hot-standby"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "hot-standby"')

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

    srv_control.remote_start_srv('DHCP', 'stopped', '$(MGMT_ADDRESS_2)')

    srv_msg.forge_sleep('10', 'seconds')

    # server1 has to keep hot-standby
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "hot-standby"')

    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "hot-standby"')

    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "hot-standby"')

    # continue server1 from hot-standby
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine continues')
    srv_msg.forge_sleep('10', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.forge_sleep('10', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')

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

    srv_control.remote_start_srv('DHCP', 'started', '$(MGMT_ADDRESS_2)')

    srv_msg.forge_sleep('10', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')

    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')

    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')
    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')

    # continue server1 from partner-down
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine continues')

    srv_msg.forge_sleep('10', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "hot-standby"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "hot-standby"')

    srv_control.remote_start_srv('DHCP', 'stopped', '$(MGMT_ADDRESS_2)')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "hot-standby"')

    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "hot-standby"')

    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "hot-standby"')

    # continue AGAIN from hot-standby
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine continues')

    srv_msg.forge_sleep('10', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')

    srv_control.remote_start_srv('DHCP', 'started', '$(MGMT_ADDRESS_2)')

    srv_msg.forge_sleep('10', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')

    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')

    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')
    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')

    srv_msg.forge_sleep('5', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "partner-down"')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "ready"')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-continue","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('text', None, 'HA state machine continues')

    srv_msg.forge_sleep('10', 'seconds')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS)')
    srv_msg.json_response_parsing('arguments', None, '"state": "hot-standby"')

    srv_msg.send_ctrl_cmd_via_http('{"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }',
                                   '$(MGMT_ADDRESS_2)')
    srv_msg.json_response_parsing('arguments', None, '"state": "hot-standby"')

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
