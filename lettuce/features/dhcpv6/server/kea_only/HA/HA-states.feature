Feature: Kea HA states
  Tests for High Availability hook - pause in each state.


@v6 @hook @HA @HA_state
Scenario: v6.hooks.HA.state.hold-lb-always

# HA SERVER 1
Test Setup:
Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Server has control agent configured on HTTP connection with address $(MGMT_ADDRESS):8080 and socket unix path: $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
Server logging system is configured with logger type kea-ctrl-agent, severity DEBUG, severity level 99 and log file kea.log-CTRL.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_lease_cmds.so.

Add High-Availability hook library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_ha.so.
To HA hook configuration add machine-state with value: {"state":"waiting","pause":"always"}
To HA hook configuration add machine-state with value: {"state":"syncing","pause":"always"}
To HA hook configuration add machine-state with value: {"state":"ready","pause":"always"}
To HA hook configuration add machine-state with value: {"state":"load-balancing","pause":"always"}
To HA hook configuration add machine-state with value: {"state":"partner-down","pause":"always"}
To HA hook configuration add this-server-name with value: "server1"
To HA hook configuration add mode with value: "load-balancing"
To HA hook configuration add heartbeat-delay with value: 1000
To HA hook configuration add max-response-delay with value: 1001
To HA hook configuration add max-unacked-clients with value: 0
To HA hook configuration add max-ack-delay with value: 0

To HA hook configuration add peers with value: {"name":"server1","url":"http://$(MGMT_ADDRESS):8080/","role":"primary","auto-failover":true}
To HA hook configuration add peers with value: {"name":"server2","url":"http://$(MGMT_ADDRESS_2):8080/","role":"secondary","auto-failover":true}

Send server configuration using SSH and config-file.
DHCP server is started.

# HA SERVER 2
Test Setup:
Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Server has control agent configured on HTTP connection with address $(MGMT_ADDRESS_2):8080 and socket unix path: $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
Server logging system is configured with logger type kea-ctrl-agent, severity DEBUG, severity level 99 and log file kea.log-CTRL2.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_lease_cmds.so.

Add High-Availability hook library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_ha.so.
To HA hook configuration add this-server-name with value: "server2"
To HA hook configuration add mode with value: "load-balancing"
To HA hook configuration add heartbeat-delay with value: 1000
To HA hook configuration add max-response-delay with value: 1001
To HA hook configuration add max-unacked-clients with value: 0
To HA hook configuration add max-ack-delay with value: 0

To HA hook configuration add peers with value: {"name":"server1","url":"http://$(MGMT_ADDRESS):8080/","role": "primary","auto-failover":true}
To HA hook configuration add peers with value: {"name":"server2","url":"http://$(MGMT_ADDRESS_2):8080/","role": "secondary","auto-failover":true}

Send server configuration using SSH and config-file and destination address $(MGMT_ADDRESS_2).
Remote DHCP server is started on address $(MGMT_ADDRESS_2).

Sleep for 5 seconds.

Test Procedure:
Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"
JSON response in result MUST include value: 0

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"
JSON response in result MUST include value: 0

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"

# continue server1 from WAITING
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 7 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "syncing"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"

#continue server1 from SYNCING
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 10 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Test Procedure:
Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond.

Sleep for 3 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Test Procedure:
Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond.

#continue server1 from READY
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 5 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

Test Procedure:
Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Remote DHCP server is stopped on address $(MGMT_ADDRESS_2).

Sleep for 10 seconds.

# server1 has to keep load-balancing
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

#continue server1 from load-balancing
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues
Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"

Test Procedure:
Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Remote DHCP server is started on address $(MGMT_ADDRESS_2).

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"
Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

# continue server1 from partner-down
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

Remote DHCP server is stopped on address $(MGMT_ADDRESS_2).

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

# continue AGAIN from load-balancing
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"

Remote DHCP server is started on address $(MGMT_ADDRESS_2).

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

Test Procedure:
Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.


@v6 @hook @HA @HA_state
Scenario: v6.hooks.HA.state.hold-lb-once

# HA SERVER 1
Test Setup:
Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Server has control agent configured on HTTP connection with address $(MGMT_ADDRESS):8080 and socket unix path: $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
Server logging system is configured with logger type kea-ctrl-agent, severity DEBUG, severity level 99 and log file kea.log-CTRL.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_lease_cmds.so.

Add High-Availability hook library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_ha.so.
To HA hook configuration add machine-state with value: {"state":"waiting","pause":"once"}
To HA hook configuration add machine-state with value: {"state":"syncing","pause":"once"}
To HA hook configuration add machine-state with value: {"state":"ready","pause":"once"}
To HA hook configuration add machine-state with value: {"state":"load-balancing","pause":"once"}
To HA hook configuration add machine-state with value: {"state":"partner-down","pause":"once"}

To HA hook configuration add this-server-name with value: "server1"
To HA hook configuration add mode with value: "load-balancing"
To HA hook configuration add heartbeat-delay with value: 1000
To HA hook configuration add max-response-delay with value: 1001
To HA hook configuration add max-unacked-clients with value: 0
To HA hook configuration add max-ack-delay with value: 0
To HA hook configuration add peers with value: {"name":"server1","url":"http://$(MGMT_ADDRESS):8080/","role":"primary","auto-failover":true}
To HA hook configuration add peers with value: {"name":"server2","url":"http://$(MGMT_ADDRESS_2):8080/","role":"secondary","auto-failover":true}

Send server configuration using SSH and config-file.
DHCP server is started.

# HA SERVER 2
Test Setup:
Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Server has control agent configured on HTTP connection with address $(MGMT_ADDRESS_2):8080 and socket unix path: $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
Server logging system is configured with logger type kea-ctrl-agent, severity DEBUG, severity level 99 and log file kea.log-CTRL2.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_lease_cmds.so.

Add High-Availability hook library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_ha.so.
To HA hook configuration add this-server-name with value: "server2"
To HA hook configuration add mode with value: "load-balancing"
To HA hook configuration add heartbeat-delay with value: 1000
To HA hook configuration add max-response-delay with value: 1001
To HA hook configuration add max-unacked-clients with value: 0
To HA hook configuration add max-ack-delay with value: 0
To HA hook configuration add peers with value: {"name":"server1","url":"http://$(MGMT_ADDRESS):8080/","role": "primary","auto-failover":true}
To HA hook configuration add peers with value: {"name":"server2","url":"http://$(MGMT_ADDRESS_2):8080/","role": "secondary","auto-failover":true}

Send server configuration using SSH and config-file and destination address $(MGMT_ADDRESS_2).
Remote DHCP server is started on address $(MGMT_ADDRESS_2).
Sleep for 5 seconds.

Test Procedure:
Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"
JSON response in result MUST include value: 0

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"
JSON response in result MUST include value: 0

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"

# continue server1 from WAITING
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 7 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "syncing"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"

#continue server1 from SYNCING
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 10 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Test Procedure:
Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond.

Sleep for 3 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Test Procedure:
Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond.

#continue server1 from READY
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 5 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

Test Procedure:
Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Remote DHCP server is stopped on address $(MGMT_ADDRESS_2).

Sleep for 10 seconds.

# server1 has to keep load-balancing
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

#continue server1 from load-balancing
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues
Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"

Test Procedure:
Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Remote DHCP server is started on address $(MGMT_ADDRESS_2).

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"
Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"
Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

Remote DHCP server is stopped on address $(MGMT_ADDRESS_2).
Sleep for 10 seconds.

# this time - no paused states!
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine is not paused
Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine is not paused
Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine is not paused
Sleep for 5 seconds.

Remote DHCP server is started on address $(MGMT_ADDRESS_2).

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine is not paused
Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

Sleep for 3 seconds.

Test Procedure:
Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

@v6 @hook @HA @HA_state
Scenario: v6.hooks.HA.state.hold-hs-once

# HA SERVER 1
Test Setup:
Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Server has control agent configured on HTTP connection with address $(MGMT_ADDRESS):8080 and socket unix path: $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
Server logging system is configured with logger type kea-ctrl-agent, severity DEBUG, severity level 99 and log file kea.log-CTRL.

Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_lease_cmds.so.

Add High-Availability hook library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_ha.so.
To HA hook configuration add machine-state with value: {"state":"waiting","pause":"once"}
To HA hook configuration add machine-state with value: {"state":"syncing","pause":"once"}
To HA hook configuration add machine-state with value: {"state":"ready","pause":"once"}
To HA hook configuration add machine-state with value: {"state":"hot-standby","pause":"once"}
To HA hook configuration add machine-state with value: {"state":"partner-down","pause":"once"}
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
Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
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
Sleep for 5 seconds.

Test Procedure:
Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"
JSON response in result MUST include value: 0

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"
JSON response in result MUST include value: 0

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"

# continue server1 from WAITING
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 7 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "syncing"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"

#continue server1 from SYNCING
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 10 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Test Procedure:
Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond.

Sleep for 3 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Test Procedure:
Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond.

#continue server1 from READY
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 5 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

Test Procedure:
Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Remote DHCP server is stopped on address $(MGMT_ADDRESS_2).

Sleep for 10 seconds.

# server1 has to keep hot-standby
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

#continue server1 from hot-standby
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues
Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"

Test Procedure:
Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Remote DHCP server is started on address $(MGMT_ADDRESS_2).

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"
Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"
Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

Remote DHCP server is stopped on address $(MGMT_ADDRESS_2).
Sleep for 10 seconds.

# this time - no paused states!
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine is not paused
Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine is not paused
Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine is not paused
Sleep for 5 seconds.

Remote DHCP server is started on address $(MGMT_ADDRESS_2).

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine is not paused
Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

Sleep for 3 seconds.

Test Procedure:
Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

@v6 @hook @HA @HA_state
Scenario: v6.hooks.HA.state.hold-hs-always

# HA SERVER 1
Test Setup:
Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Server has control agent configured on HTTP connection with address $(MGMT_ADDRESS):8080 and socket unix path: $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
Server logging system is configured with logger type kea-ctrl-agent, severity DEBUG, severity level 99 and log file kea.log-CTRL.

Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_lease_cmds.so.

Add High-Availability hook library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_ha.so.
To HA hook configuration add machine-state with value: {"state":"waiting","pause":"always"}
To HA hook configuration add machine-state with value: {"state":"syncing","pause":"always"}
To HA hook configuration add machine-state with value: {"state":"ready","pause":"always"}
To HA hook configuration add machine-state with value: {"state":"hot-standby","pause":"always"}
To HA hook configuration add machine-state with value: {"state":"partner-down","pause":"always"}
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
Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
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

Sleep for 5 seconds.

Test Procedure:
Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"
JSON response in result MUST include value: 0

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"
JSON response in result MUST include value: 0

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"

# continue server1 from WAITING
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 7 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "syncing"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"

#continue server1 from SYNCING
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 10 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Test Procedure:
Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond.

Sleep for 3 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Test Procedure:
Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond.

#continue server1 from READY
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 5 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

Test Procedure:
Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Remote DHCP server is stopped on address $(MGMT_ADDRESS_2).

Sleep for 10 seconds.

# server1 has to keep hot-standby
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

#continue server1 from hot-standby
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues
Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"

Test Procedure:
Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Remote DHCP server is started on address $(MGMT_ADDRESS_2).

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"
Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

# continue server1 from partner-down
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

Remote DHCP server is stopped on address $(MGMT_ADDRESS_2).

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

# continue AGAIN from hot-standby
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"

Remote DHCP server is started on address $(MGMT_ADDRESS_2).

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp6"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp6"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

Test Procedure:
Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.