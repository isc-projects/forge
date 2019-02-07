"""Kea HA syncing"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_msg
from features import misc
from features import srv_control


@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.HA
@pytest.mark.HA_state
@pytest.mark.disabled
def test_v6_hooks_HA_page_size_sync():

    # HA SERVER 1
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ffff')
    srv_control.open_control_channel('unix', '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel('$(MGMT_ADDRESS)',
                                      '8080',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.configure_loggers('kea-dhcp6.dhcpsrv', 'DEBUG', '99', 'kea.log')
    srv_control.configure_loggers('kea-dhcp6.ha-hooks', 'DEBUG', '99', 'kea.log')
    srv_control.configure_loggers('kea-ctrl-agent', 'DEBUG', '99', 'kea.log-CTRL')

    srv_control.add_hooks('$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_lease_cmds.so')

    srv_control.add_ha_hook('$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_ha.so')

    srv_control.add_parameter_to_ha_hook('this-server-name', '"server1"')
    srv_control.add_parameter_to_ha_hook('mode', '"hot-standby"')
    srv_control.add_parameter_to_ha_hook('heartbeat-delay', '1000')
    srv_control.add_parameter_to_ha_hook('max-response-delay', '1001')
    srv_control.add_parameter_to_ha_hook('max-unacked-clients', '0')
    srv_control.add_parameter_to_ha_hook('max-ack-delay', '0')

    srv_control.add_parameter_to_ha_hook('sync-page-limit', '10')

    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server1","url":"http://$(MGMT_ADDRESS):8080/","role":"primary","auto-failover":true}')
    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server2","url":"http://$(MGMT_ADDRESS_2):8080/","role":"standby","auto-failover":true}')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    # HA SERVER 2
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ffff')
    srv_control.open_control_channel('unix', '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel('$(MGMT_ADDRESS_2)',
                                      '8080',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.configure_loggers('kea-dhcp6.dhcpsrv', 'DEBUG', '99', 'kea.log')
    srv_control.configure_loggers('kea-dhcp6.ha-hooks', 'DEBUG', '99', 'kea.log')
    srv_control.configure_loggers('kea-ctrl-agent', 'DEBUG', '99', 'kea.log-CTRL2')

    srv_control.add_hooks('$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_lease_cmds.so')

    srv_control.add_ha_hook('$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_ha.so')
    srv_control.add_parameter_to_ha_hook('this-server-name', '"server2"')
    srv_control.add_parameter_to_ha_hook('mode', '"hot-standby"')
    srv_control.add_parameter_to_ha_hook('heartbeat-delay', '1000')
    srv_control.add_parameter_to_ha_hook('max-response-delay', '1001')
    srv_control.add_parameter_to_ha_hook('max-unacked-clients', '0')
    srv_control.add_parameter_to_ha_hook('max-ack-delay', '0')

    srv_control.add_parameter_to_ha_hook('sync-page-limit', '10')

    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server1","url":"http://$(MGMT_ADDRESS):8080/","role": "primary","auto-failover":true}')
    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server2","url":"http://$(MGMT_ADDRESS_2):8080/","role": "standby","auto-failover":true}')

    srv_control.build_and_send_config_files('SSH', 'config-file')

    misc.test_procedure()
    srv_msg.forge_sleep('3', 'seconds')

    srv_msg.loops('SOLICIT', 'REPLY', '100')

    srv_control.start_srv('DHCP', 'started')

    srv_msg.forge_sleep('10', 'seconds')

    misc.pass_criteria()
    srv_msg.file_contains_line('$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               'DHCPSRV_MEMFILE_GET_PAGE6 obtaining at most 10 IPv6 leases starting from address 2001:db8:1::5b')
    srv_msg.remote_log_includes_line('$(MGMT_ADDRESS_2)',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                                     None,
                                     'HA_LEASES_SYNC_LEASE_PAGE_RECEIVED received 10 leases from server1')
    srv_msg.remote_log_includes_line('$(MGMT_ADDRESS_2)',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                                     None,
                                     'DHCPSRV_MEMFILE_GET_ADDR6 obtaining IPv6 lease for address 2001:db8:1::65 and lease type IA_NA')


@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.HA
@pytest.mark.HA_state
@pytest.mark.disabled
def test_v6_hooks_HA_page_size_sync_2():

    # HA SERVER 1
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ffff')
    srv_control.open_control_channel('unix', '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel('$(MGMT_ADDRESS)',
                                      '8080',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.configure_loggers('kea-dhcp6.dhcpsrv', 'DEBUG', '99', 'kea.log')
    srv_control.configure_loggers('kea-dhcp6.ha-hooks', 'DEBUG', '99', 'kea.log')
    srv_control.configure_loggers('kea-ctrl-agent', 'DEBUG', '99', 'kea.log-CTRL')

    srv_control.add_hooks('$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_lease_cmds.so')

    srv_control.add_ha_hook('$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_ha.so')

    srv_control.add_parameter_to_ha_hook('this-server-name', '"server1"')
    srv_control.add_parameter_to_ha_hook('mode', '"hot-standby"')
    srv_control.add_parameter_to_ha_hook('heartbeat-delay', '1000')
    srv_control.add_parameter_to_ha_hook('max-response-delay', '1001')
    srv_control.add_parameter_to_ha_hook('max-unacked-clients', '0')
    srv_control.add_parameter_to_ha_hook('max-ack-delay', '0')

    srv_control.add_parameter_to_ha_hook('sync-page-limit', '10')

    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server1","url":"http://$(MGMT_ADDRESS):8080/","role":"primary","auto-failover":true}')
    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server2","url":"http://$(MGMT_ADDRESS_2):8080/","role":"standby","auto-failover":true}')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    # HA SERVER 2
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ffff')
    srv_control.open_control_channel('unix', '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel('$(MGMT_ADDRESS_2)',
                                      '8080',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.configure_loggers('kea-dhcp6.dhcpsrv', 'DEBUG', '99', 'kea.log')
    srv_control.configure_loggers('kea-dhcp6.ha-hooks', 'DEBUG', '99', 'kea.log')
    srv_control.configure_loggers('kea-ctrl-agent', 'DEBUG', '99', 'kea.log-CTRL2')

    srv_control.add_hooks('$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_lease_cmds.so')

    srv_control.add_ha_hook('$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_ha.so')
    srv_control.add_parameter_to_ha_hook('this-server-name', '"server2"')
    srv_control.add_parameter_to_ha_hook('mode', '"hot-standby"')
    srv_control.add_parameter_to_ha_hook('heartbeat-delay', '1000')
    srv_control.add_parameter_to_ha_hook('max-response-delay', '1001')
    srv_control.add_parameter_to_ha_hook('max-unacked-clients', '0')
    srv_control.add_parameter_to_ha_hook('max-ack-delay', '0')

    srv_control.add_parameter_to_ha_hook('sync-page-limit', '15')

    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server1","url":"http://$(MGMT_ADDRESS):8080/","role": "primary","auto-failover":true}')
    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server2","url":"http://$(MGMT_ADDRESS_2):8080/","role": "standby","auto-failover":true}')

    srv_control.build_and_send_config_files('SSH', 'config-file')

    misc.test_procedure()
    srv_msg.forge_sleep('3', 'seconds')

    # create leases in HA 1
    srv_msg.loops('SOLICIT', 'REPLY', '100')

    srv_control.start_srv('DHCP', 'started')
    # sync HA 2 with HA 1
    srv_msg.forge_sleep('10', 'seconds')

    misc.pass_criteria()
    srv_msg.file_contains_line('$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               'DHCPSRV_MEMFILE_GET_PAGE6 obtaining at most 15 IPv6 leases starting from address 2001:db8:1::5')
    srv_msg.remote_log_includes_line('$(MGMT_ADDRESS_2)',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                                     None,
                                     'HA_LEASES_SYNC_LEASE_PAGE_RECEIVED received 15 leases from server1')
    srv_msg.remote_log_includes_line('$(MGMT_ADDRESS_2)',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                                     None,
                                     'DHCPSRV_MEMFILE_GET_ADDR6 obtaining IPv6 lease for address 2001:db8:1::65 and lease type IA_NA')

    srv_msg.remote_log_includes_line('$(MGMT_ADDRESS_2)',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                                     'NOT ',
                                     'DHCPSRV_MEMFILE_GET_PAGE6 obtaining at most 10 IPv6 leases starting from address 2001:')
    srv_msg.file_contains_line('$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               'NOT ',
                               'HA_LEASES_SYNC_LEASE_PAGE_RECEIVED received 10 leases from')
    srv_msg.remote_log_includes_line('$(MGMT_ADDRESS_2)',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                                     None,
                                     'HA_SYNC_SUCCESSFUL lease database synchronization with server1 completed successfully')

    # stop HA !
    srv_control.start_srv('DHCP', 'stopped')

    misc.test_procedure()
    srv_msg.forge_sleep('3', 'seconds')

    # create leases in HA 2
    srv_msg.loops('SOLICIT', 'REPLY', '100')
    srv_control.clear_leases('logs')

    srv_control.start_srv('DHCP', 'started')

    srv_msg.forge_sleep('10', 'seconds')

    misc.pass_criteria()
    srv_msg.file_contains_line('$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               'DHCPSRV_MEMFILE_ADD_ADDR6 adding IPv6 lease with address 2001:db8:1::c9')


@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.HA
@pytest.mark.HA_state
@pytest.mark.disabled
def test_v6_hooks_HA_page_size_sync_large():
    # This is to big to be run in forge setup, run manually, if by mistake someone will start it - uncomment lines at the bottom

    # HA SERVER 1
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ffff')
    srv_control.open_control_channel('unix', '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel('$(MGMT_ADDRESS)',
                                      '8080',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.configure_loggers('kea-dhcp6.dhcpsrv', 'DEBUG', '99', 'kea.log')
    srv_control.configure_loggers('kea-dhcp6.ha-hooks', 'DEBUG', '99', 'kea.log')
    srv_control.configure_loggers('kea-ctrl-agent', 'DEBUG', '99', 'kea.log-CTRL')

    srv_control.add_hooks('$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_lease_cmds.so')

    srv_control.add_ha_hook('$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_ha.so')

    srv_control.add_parameter_to_ha_hook('this-server-name', '"server1"')
    srv_control.add_parameter_to_ha_hook('mode', '"hot-standby"')
    srv_control.add_parameter_to_ha_hook('heartbeat-delay', '1000')
    srv_control.add_parameter_to_ha_hook('max-response-delay', '1001')
    srv_control.add_parameter_to_ha_hook('max-unacked-clients', '0')
    srv_control.add_parameter_to_ha_hook('max-ack-delay', '0')

    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server1","url":"http://$(MGMT_ADDRESS):8080/","role":"primary","auto-failover":true}')
    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server2","url":"http://$(MGMT_ADDRESS_2):8080/","role":"standby","auto-failover":true}')

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    # HA SERVER 2
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ffff')
    srv_control.open_control_channel('unix', '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel('$(MGMT_ADDRESS_2)',
                                      '8080',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.configure_loggers('kea-dhcp6', 'DEBUG', '99', 'kea.log')
    srv_control.configure_loggers('kea-ctrl-agent', 'DEBUG', '99', 'kea.log-CTRL2')

    srv_control.add_hooks('$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_lease_cmds.so')

    srv_control.add_ha_hook('$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_ha.so')
    srv_control.add_parameter_to_ha_hook('this-server-name', '"server2"')
    srv_control.add_parameter_to_ha_hook('mode', '"hot-standby"')
    srv_control.add_parameter_to_ha_hook('heartbeat-delay', '1000')
    srv_control.add_parameter_to_ha_hook('max-response-delay', '1001')
    srv_control.add_parameter_to_ha_hook('max-unacked-clients', '0')
    srv_control.add_parameter_to_ha_hook('max-ack-delay', '0')

    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server1","url":"http://$(MGMT_ADDRESS):8080/","role": "primary","auto-failover":true}')
    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server2","url":"http://$(MGMT_ADDRESS_2):8080/","role": "standby","auto-failover":true}')

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_msg.forge_sleep('3', 'seconds')
    # UNCOMMENT:
    # Exchange messages SOLICIT - REPLY 200000 times.

    srv_control.start_srv('DHCP', 'started')

    # UNCOMMENT:
    # Sleep for 3000 seconds.
