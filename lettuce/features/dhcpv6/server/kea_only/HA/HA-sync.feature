Feature: Kea HA syncing
  Tests for High Availability hook - sync.

@v6 @hook @HA @HA_state @disabled
Scenario: v6.hooks.HA.page-size-sync

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

To HA hook configuration add sync-page-limit with value: 10

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

To HA hook configuration add sync-page-limit with value: 10

To HA hook configuration add peers with value: {"name":"server1","url":"http://$(MGMT_ADDRESS):8080/","role": "primary","auto-failover":true}
To HA hook configuration add peers with value: {"name":"server2","url":"http://$(MGMT_ADDRESS_2):8080/","role": "standby","auto-failover":true}

Send server configuration using SSH and config-file and destination address $(MGMT_ADDRESS_2).

Sleep for 3 seconds.

Exchange messages SOLICIT - REPLY 100 times.

Remote DHCP server is started on address $(MGMT_ADDRESS_2).

Sleep for 10 seconds.
# Server 2 should have all the leases by now, so we are looking for sync logs and address in logs


@v6 @hook @HA @HA_state @disabled
Scenario: v6.hooks.HA.page-size-sync-2

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

To HA hook configuration add sync-page-limit with value: 10

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

To HA hook configuration add sync-page-limit with value: 15

To HA hook configuration add peers with value: {"name":"server1","url":"http://$(MGMT_ADDRESS):8080/","role": "primary","auto-failover":true}
To HA hook configuration add peers with value: {"name":"server2","url":"http://$(MGMT_ADDRESS_2):8080/","role": "standby","auto-failover":true}

Send server configuration using SSH and config-file and destination address $(MGMT_ADDRESS_2).

Sleep for 3 seconds.

# create leases in HA 1
Exchange messages SOLICIT - REPLY 100 times.

Remote DHCP server is started on address $(MGMT_ADDRESS_2).
# sync HA 2 with HA 1
Sleep for 10 seconds.

# stop HA !
DHCP server is stopped.

Sleep for 3 seconds.

# create leases in HA 2
Exchange messages SOLICIT - REPLY 100 times.

Clear logs.

DHCP server is started.

# sync HA 1 with HA 2, we suppose to have all leases here now
Sleep for 10 seconds.

#File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST contain line or phrase: { "arguments": { "from": "2001:db8:1::b", "limit": 10 }, "command": "lease6-get-page", "service": [ "dhcp6" ] }
#File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST contain line or phrase: "state": "hot-standby" }, "result": 0, "text": "HA peer status returned." } ]

# if last lease was transferred everything is ok
File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST contain line or phrase: DHCPSRV_MEMFILE_ADD_ADDR6 adding IPv6 lease with address 2001:db8:1::c9


@v6 @hook @HA @HA_state @disabled
Scenario: v6.hooks.HA.page-size-sync-large
# This is to big to be run in forge setup, run manually

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

Sleep for 3 seconds.

Exchange messages SOLICIT - REPLY 200000 times.

Remote DHCP server is started on address $(MGMT_ADDRESS_2).

Sleep for 3000 seconds.
