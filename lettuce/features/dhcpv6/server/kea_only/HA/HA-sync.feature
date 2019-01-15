Feature: Kea HA syncing
  Tests for High Availability hook - sync.

@v6 @hook @HA @HA_state @disabled
Scenario: v6.hooks.HA.page-size-sync

# HA SERVER 1
Test Setup:
Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::ffff pool.
Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Server has control agent configured on HTTP connection with address $(MGMT_ADDRESS):8080 and socket unix path: $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Server logging system is configured with logger type kea-dhcp6.dhcpsrv, severity DEBUG, severity level 99 and log file kea.log.
Server logging system is configured with logger type kea-dhcp6.ha-hooks, severity DEBUG, severity level 99 and log file kea.log.
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
Server logging system is configured with logger type kea-dhcp6.dhcpsrv, severity DEBUG, severity level 99 and log file kea.log.
Server logging system is configured with logger type kea-dhcp6.ha-hooks, severity DEBUG, severity level 99 and log file kea.log.
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

Test Procedure:
Sleep for 3 seconds.

Exchange messages SOLICIT - REPLY 100 times.

Remote DHCP server is started on address $(MGMT_ADDRESS_2).

Sleep for 10 seconds.

Pass Criteria:
File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST contain line or phrase: DHCPSRV_MEMFILE_GET_PAGE6 obtaining at most 10 IPv6 leases starting from address 2001:db8:1::5b
Remote $(MGMT_ADDRESS_2) file stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST contain line or phrase: HA_LEASES_SYNC_LEASE_PAGE_RECEIVED received 10 leases from server1
Remote $(MGMT_ADDRESS_2) file stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST contain line or phrase: DHCPSRV_MEMFILE_GET_ADDR6 obtaining IPv6 lease for address 2001:db8:1::65 and lease type IA_NA



@v6 @hook @HA @HA_state @disabled
Scenario: v6.hooks.HA.page-size-sync-2

# HA SERVER 1
Test Setup:
Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::ffff pool.
Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Server has control agent configured on HTTP connection with address $(MGMT_ADDRESS):8080 and socket unix path: $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Server logging system is configured with logger type kea-dhcp6.dhcpsrv, severity DEBUG, severity level 99 and log file kea.log.
Server logging system is configured with logger type kea-dhcp6.ha-hooks, severity DEBUG, severity level 99 and log file kea.log.
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
Server logging system is configured with logger type kea-dhcp6.dhcpsrv, severity DEBUG, severity level 99 and log file kea.log.
Server logging system is configured with logger type kea-dhcp6.ha-hooks, severity DEBUG, severity level 99 and log file kea.log.
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

Test Procedure:
Sleep for 3 seconds.

# create leases in HA 1
Exchange messages SOLICIT - REPLY 100 times.

Remote DHCP server is started on address $(MGMT_ADDRESS_2).
# sync HA 2 with HA 1
Sleep for 10 seconds.

Pass Criteria:
File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST contain line or phrase: DHCPSRV_MEMFILE_GET_PAGE6 obtaining at most 15 IPv6 leases starting from address 2001:db8:1::5
Remote $(MGMT_ADDRESS_2) file stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST contain line or phrase: HA_LEASES_SYNC_LEASE_PAGE_RECEIVED received 15 leases from server1
Remote $(MGMT_ADDRESS_2) file stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST contain line or phrase: DHCPSRV_MEMFILE_GET_ADDR6 obtaining IPv6 lease for address 2001:db8:1::65 and lease type IA_NA

Remote $(MGMT_ADDRESS_2) file stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST NOT contain line or phrase: DHCPSRV_MEMFILE_GET_PAGE6 obtaining at most 10 IPv6 leases starting from address 2001:
File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST NOT contain line or phrase: HA_LEASES_SYNC_LEASE_PAGE_RECEIVED received 10 leases from
Remote $(MGMT_ADDRESS_2) file stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST contain line or phrase: HA_SYNC_SUCCESSFUL lease database synchronization with server1 completed successfully

# stop HA !
DHCP server is stopped.

Test Procedure:
Sleep for 3 seconds.

# create leases in HA 2
Exchange messages SOLICIT - REPLY 100 times.
Clear logs.

DHCP server is started.

Sleep for 10 seconds.

Pass Criteria:
File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST contain line or phrase: DHCPSRV_MEMFILE_ADD_ADDR6 adding IPv6 lease with address 2001:db8:1::c9


@v6 @hook @HA @HA_state @disabled
Scenario: v6.hooks.HA.page-size-sync-large
# This is to big to be run in forge setup, run manually, if by mistake someone will start it - uncomment lines at the bottom

# HA SERVER 1
Test Setup:
Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::ffff pool.
Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Server has control agent configured on HTTP connection with address $(MGMT_ADDRESS):8080 and socket unix path: $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Server logging system is configured with logger type kea-dhcp6.dhcpsrv, severity DEBUG, severity level 99 and log file kea.log.
Server logging system is configured with logger type kea-dhcp6.ha-hooks, severity DEBUG, severity level 99 and log file kea.log.
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
# UNCOMMENT:
# Exchange messages SOLICIT - REPLY 200000 times.

Remote DHCP server is started on address $(MGMT_ADDRESS_2).

# UNCOMMENT:
# Sleep for 3000 seconds.
