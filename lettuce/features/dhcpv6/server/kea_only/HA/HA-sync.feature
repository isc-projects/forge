Feature: Kea HA syncing
  Tests for High Availability hook - sync.

@v6 @hook @HA @HA_state
Scenario: v6.hooks.HA.state.hold-hs-partial-sync

# HA SERVER 1
Test Setup:
Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::ffff pool.
Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Server has control agent configured on HTTP connection with address $(MGMT_ADDRESS):8080 and socket unix path: $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
Server logging system is configured with logger type kea-ctrl-agent, severity DEBUG, severity level 99 and log file kea.log-CTRL.

Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_lease_cmds.so.

Add High-Availability hook library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_ha.so.

To HA hook configuration add this-server-name with value: "server1"
To HA hook configuration add mode with value: "hot-standby"
To HA hook configuration add heartbeat-delay with value: 1000
To HA hook configuration add max-response-delay with value: 1001
To HA hook configuration add max-unacked-clients with value: 0
To HA hook configuration add max-ack-delay with value: 0

To HA hook configuration add peers with value: {"name":"server1","url":"http://$(MGMT_ADDRESS):8080/","role":"primary","auto-failover":true}
To HA hook configuration add peers with value: {"name":"server2","url":"http://$(MGMT_ADDRESS_2):8080/","role":"standby","auto-failover":true}

Send server configuration using SSH and config-file.
DHCP server is started.

# HA SERVER 2
Test Setup:
Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::ffff pool.
Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Server has control agent configured on HTTP connection with address $(MGMT_ADDRESS_2):8080 and socket unix path: $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
Server logging system is configured with logger type kea-ctrl-agent, severity DEBUG, severity level 99 and log file kea.log-CTRL2.

Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_lease_cmds.so.

Add High-Availability hook library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_ha.so.
To HA hook configuration add this-server-name with value: "server2"
To HA hook configuration add mode with value: "hot-standby"
To HA hook configuration add heartbeat-delay with value: 1000
To HA hook configuration add max-response-delay with value: 1001
To HA hook configuration add max-unacked-clients with value: 0
To HA hook configuration add max-ack-delay with value: 0

To HA hook configuration add peers with value: {"name":"server1","url":"http://$(MGMT_ADDRESS):8080/","role": "primary","auto-failover":true}
To HA hook configuration add peers with value: {"name":"server2","url":"http://$(MGMT_ADDRESS_2):8080/","role": "standby","auto-failover":true}

Send server configuration using SSH and config-file and destination address $(MGMT_ADDRESS_2).
Remote DHCP server is started on address $(MGMT_ADDRESS_2).

#Pause the Test.