Feature: Kea HA states
  Tests for High Availability hook - pause in each state.


@v4 @hook @HA
Scenario: v4.hooks.HA.state.hold-lb-always

# HA SERVER 1
Test Setup:
Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
Server has control agent configured on HTTP connection with address $(MGMT_ADDRESS):8080 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
Server logging system is configured with logger type kea-dhcp4, severity DEBUG, severity level 99 and log file kea.log.
Server logging system is configured with logger type kea-ctrl-agent, severity DEBUG, severity level 99 and log file kea.log-CTRL.
Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_lease_cmds.so.

Add High-Availability hook library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_ha.so.
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
Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
Server has control agent configured on HTTP connection with address $(MGMT_ADDRESS_2):8080 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
Server logging system is configured with logger type kea-dhcp4, severity DEBUG, severity level 99 and log file kea.log.
Server logging system is configured with logger type kea-ctrl-agent, severity DEBUG, severity level 99 and log file kea.log-CTRL2.
Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_lease_cmds.so.

Add High-Availability hook library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_ha.so.
To HA hook configuration add this-server-name with value: "server2"
To HA hook configuration add mode with value: "load-balancing"
To HA hook configuration add heartbeat-delay with value: 1000
To HA hook configuration add max-response-delay with value: 1001
To HA hook configuration add max-unacked-clients with value: 0
To HA hook configuration add max-ack-delay with value: 0

To HA hook configuration add peers with value: {"name":"server1","url":"http://$(MGMT_ADDRESS):8080/","role": "primary","auto-failover":true}
To HA hook configuration add peers with value: {"name":"server2","url":"http://$(MGMT_ADDRESS_2):8080/","role": "secondary","auto-failover":true}

Send server configuration using SSH and config-file and destination address $(MGMT_ADDRESS_2).
DHCP server is started on remote address $(MGMT_ADDRESS_2).

Sleep for 5 seconds.

Test Procedure:
Client requests option 1.
Client sends DISCOVER message.

Pass Criteria:
Server MUST NOT respond.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"
JSON response in result MUST include value: 0

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"
JSON response in result MUST include value: 0

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"

# continue server1 from WAITING
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 7 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "syncing"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"

#continue server1 from SYNCING
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 10 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Test Procedure:
Client requests option 1.
Client sends DISCOVER message.

Pass Criteria:
Server MUST NOT respond.

Sleep for 3 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Test Procedure:
Client requests option 1.
Client sends DISCOVER message.

Pass Criteria:
Server MUST NOT respond.

#continue server1 from READY
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 5 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

Test Procedure:
Client requests option 1.
Client sends DISCOVER message.

Pass Criteria:
Server MUST respond with OFFER message.

DHCP server is stopped on remote address $(MGMT_ADDRESS_2).

Sleep for 10 seconds.

# server1 has to keep load-balancing
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

#continue server1 from load-balancing
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues
Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"

Test Procedure:
Client requests option 1.
Client sends DISCOVER message.

Pass Criteria:
Server MUST respond with OFFER message.

DHCP server is started on remote address $(MGMT_ADDRESS_2).

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"
Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

# continue server1 from partner-down
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

DHCP server is stopped on remote address $(MGMT_ADDRESS_2).

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

# continue AGAIN from load-balancing
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"

DHCP server is started on remote address $(MGMT_ADDRESS_2).

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

Test Procedure:
Client requests option 1.
Client sends DISCOVER message.

Pass Criteria:
Server MUST respond with OFFER message.




@v4 @hook @HA
Scenario: v4.hooks.HA.state.hold-lb-once

# HA SERVER 1
Test Setup:
Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
Server has control agent configured on HTTP connection with address $(MGMT_ADDRESS):8080 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
Server logging system is configured with logger type kea-dhcp4, severity DEBUG, severity level 99 and log file kea.log.
Server logging system is configured with logger type kea-ctrl-agent, severity DEBUG, severity level 99 and log file kea.log-CTRL.
Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_lease_cmds.so.

Add High-Availability hook library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_ha.so.
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
Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
Server has control agent configured on HTTP connection with address $(MGMT_ADDRESS_2):8080 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
Server logging system is configured with logger type kea-dhcp4, severity DEBUG, severity level 99 and log file kea.log.
Server logging system is configured with logger type kea-ctrl-agent, severity DEBUG, severity level 99 and log file kea.log-CTRL2.
Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_lease_cmds.so.

Add High-Availability hook library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_ha.so.
To HA hook configuration add this-server-name with value: "server2"
To HA hook configuration add mode with value: "load-balancing"
To HA hook configuration add heartbeat-delay with value: 1000
To HA hook configuration add max-response-delay with value: 1001
To HA hook configuration add max-unacked-clients with value: 0
To HA hook configuration add max-ack-delay with value: 0
To HA hook configuration add peers with value: {"name":"server1","url":"http://$(MGMT_ADDRESS):8080/","role": "primary","auto-failover":true}
To HA hook configuration add peers with value: {"name":"server2","url":"http://$(MGMT_ADDRESS_2):8080/","role": "secondary","auto-failover":true}

Send server configuration using SSH and config-file and destination address $(MGMT_ADDRESS_2).
DHCP server is started on remote address $(MGMT_ADDRESS_2).
Sleep for 5 seconds.

Test Procedure:
Client requests option 1.
Client sends DISCOVER message.

Pass Criteria:
Server MUST NOT respond.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"
JSON response in result MUST include value: 0

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"
JSON response in result MUST include value: 0

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"

# continue server1 from WAITING
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 7 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "syncing"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"

#continue server1 from SYNCING
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 10 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Test Procedure:
Client requests option 1.
Client sends DISCOVER message.

Pass Criteria:
Server MUST NOT respond.

Sleep for 3 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Test Procedure:
Client requests option 1.
Client sends DISCOVER message.

Pass Criteria:
Server MUST NOT respond.

#continue server1 from READY
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 5 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

Test Procedure:
Client requests option 1.
Client sends DISCOVER message.

Pass Criteria:
Server MUST respond with OFFER message.

DHCP server is stopped on remote address $(MGMT_ADDRESS_2).

Sleep for 10 seconds.

# server1 has to keep load-balancing
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

#continue server1 from load-balancing
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues
Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"

Test Procedure:
Client requests option 1.
Client sends DISCOVER message.

Pass Criteria:
Server MUST respond with OFFER message.

DHCP server is started on remote address $(MGMT_ADDRESS_2).

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"
Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"
Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

DHCP server is stopped on remote address $(MGMT_ADDRESS_2).
Sleep for 10 seconds.

# this time - no paused states!
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine is not paused
Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine is not paused
Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine is not paused
Sleep for 5 seconds.

DHCP server is started on remote address $(MGMT_ADDRESS_2).

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine is not paused
Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "load-balancing"

Sleep for 3 seconds.

Test Procedure:
Client requests option 1.
Client sends DISCOVER message.

Pass Criteria:
Server MUST respond with OFFER message.













@v4 @hook @HA
Scenario: v4.hooks.HA.state.hold-hs-once

# HA SERVER 1
Test Setup:
Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
Server has control agent configured on HTTP connection with address $(MGMT_ADDRESS):8080 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
Server logging system is configured with logger type kea-dhcp4, severity DEBUG, severity level 99 and log file kea.log.
Server logging system is configured with logger type kea-ctrl-agent, severity DEBUG, severity level 99 and log file kea.log-CTRL.

Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_lease_cmds.so.

Add High-Availability hook library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_ha.so.
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
Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
Server has control agent configured on HTTP connection with address $(MGMT_ADDRESS_2):8080 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
Server logging system is configured with logger type kea-dhcp4, severity DEBUG, severity level 99 and log file kea.log.
Server logging system is configured with logger type kea-ctrl-agent, severity DEBUG, severity level 99 and log file kea.log-CTRL2.

Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_lease_cmds.so.

Add High-Availability hook library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_ha.so.
To HA hook configuration add this-server-name with value: "server2"
To HA hook configuration add mode with value: "hot-standby"
To HA hook configuration add heartbeat-delay with value: 1000
To HA hook configuration add max-response-delay with value: 1001
To HA hook configuration add max-unacked-clients with value: 0
To HA hook configuration add max-ack-delay with value: 0

To HA hook configuration add peers with value: {"name":"server1","url":"http://$(MGMT_ADDRESS):8080/","role": "primary","auto-failover":true}
To HA hook configuration add peers with value: {"name":"server2","url":"http://$(MGMT_ADDRESS_2):8080/","role": "standby","auto-failover":true}

Send server configuration using SSH and config-file and destination address $(MGMT_ADDRESS_2).
DHCP server is started on remote address $(MGMT_ADDRESS_2).
Sleep for 5 seconds.

Test Procedure:
Client requests option 1.
Client sends DISCOVER message.

Pass Criteria:
Server MUST NOT respond.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"
JSON response in result MUST include value: 0

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"
JSON response in result MUST include value: 0

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"

# continue server1 from WAITING
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 7 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "syncing"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"

#continue server1 from SYNCING
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 10 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Test Procedure:
Client requests option 1.
Client sends DISCOVER message.

Pass Criteria:
Server MUST NOT respond.

Sleep for 3 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Test Procedure:
Client requests option 1.
Client sends DISCOVER message.

Pass Criteria:
Server MUST NOT respond.

#continue server1 from READY
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 5 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

Test Procedure:
Client requests option 1.
Client sends DISCOVER message.

Pass Criteria:
Server MUST respond with OFFER message.

DHCP server is stopped on remote address $(MGMT_ADDRESS_2).

Sleep for 10 seconds.

# server1 has to keep hot-standby
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

#continue server1 from hot-standby
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues
Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"

Test Procedure:
Client requests option 1.
Client sends DISCOVER message.

Pass Criteria:
Server MUST respond with OFFER message.

DHCP server is started on remote address $(MGMT_ADDRESS_2).

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"
Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"
Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

DHCP server is stopped on remote address $(MGMT_ADDRESS_2).
Sleep for 10 seconds.

# this time - no paused states!
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine is not paused
Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine is not paused
Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine is not paused
Sleep for 5 seconds.

DHCP server is started on remote address $(MGMT_ADDRESS_2).

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine is not paused
Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

Sleep for 3 seconds.

Test Procedure:
Client requests option 1.
Client sends DISCOVER message.

Pass Criteria:
Server MUST respond with OFFER message.


@v4 @hook @HA
Scenario: v4.hooks.HA.state.hold-hs-always

# HA SERVER 1
Test Setup:
Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
Server has control agent configured on HTTP connection with address $(MGMT_ADDRESS):8080 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
Server logging system is configured with logger type kea-dhcp4, severity DEBUG, severity level 99 and log file kea.log.
Server logging system is configured with logger type kea-ctrl-agent, severity DEBUG, severity level 99 and log file kea.log-CTRL.

Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_lease_cmds.so.

Add High-Availability hook library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_ha.so.
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
Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
Server has control agent configured on HTTP connection with address $(MGMT_ADDRESS_2):8080 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
Server logging system is configured with logger type kea-dhcp4, severity DEBUG, severity level 99 and log file kea.log.
Server logging system is configured with logger type kea-ctrl-agent, severity DEBUG, severity level 99 and log file kea.log-CTRL2.

Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_lease_cmds.so.

Add High-Availability hook library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_ha.so.
To HA hook configuration add this-server-name with value: "server2"
To HA hook configuration add mode with value: "hot-standby"
To HA hook configuration add heartbeat-delay with value: 1000
To HA hook configuration add max-response-delay with value: 1001
To HA hook configuration add max-unacked-clients with value: 0
To HA hook configuration add max-ack-delay with value: 0

To HA hook configuration add peers with value: {"name":"server1","url":"http://$(MGMT_ADDRESS):8080/","role": "primary","auto-failover":true}
To HA hook configuration add peers with value: {"name":"server2","url":"http://$(MGMT_ADDRESS_2):8080/","role": "standby","auto-failover":true}

Send server configuration using SSH and config-file and destination address $(MGMT_ADDRESS_2).
DHCP server is started on remote address $(MGMT_ADDRESS_2).

Sleep for 5 seconds.

Test Procedure:
Client requests option 1.
Client sends DISCOVER message.

Pass Criteria:
Server MUST NOT respond.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"
JSON response in result MUST include value: 0

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"
JSON response in result MUST include value: 0

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"

# continue server1 from WAITING
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 7 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "syncing"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "waiting"

#continue server1 from SYNCING
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 10 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Test Procedure:
Client requests option 1.
Client sends DISCOVER message.

Pass Criteria:
Server MUST NOT respond.

Sleep for 3 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Test Procedure:
Client requests option 1.
Client sends DISCOVER message.

Pass Criteria:
Server MUST NOT respond.

#continue server1 from READY
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 5 seconds.
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

Test Procedure:
Client requests option 1.
Client sends DISCOVER message.

Pass Criteria:
Server MUST respond with OFFER message.

DHCP server is stopped on remote address $(MGMT_ADDRESS_2).

Sleep for 10 seconds.

# server1 has to keep hot-standby
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

#continue server1 from hot-standby
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues
Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"

Test Procedure:
Client requests option 1.
Client sends DISCOVER message.

Pass Criteria:
Server MUST respond with OFFER message.

DHCP server is started on remote address $(MGMT_ADDRESS_2).

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"
Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

# continue server1 from partner-down
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

DHCP server is stopped on remote address $(MGMT_ADDRESS_2).

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

# continue AGAIN from hot-standby
Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"

DHCP server is started on remote address $(MGMT_ADDRESS_2).

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"
Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Sleep for 5 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "partner-down"

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "ready"

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-continue","service":["dhcp4"],"arguments": {} }
JSON response in text MUST include value: HA state machine continues

Sleep for 10 seconds.

Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

Using existing HTTP $(MGMT_ADDRESS_2):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
JSON response in arguments MUST include value: "state": "hot-standby"

Test Procedure:
Client requests option 1.
Client sends DISCOVER message.

Pass Criteria:
Server MUST respond with OFFER message.
