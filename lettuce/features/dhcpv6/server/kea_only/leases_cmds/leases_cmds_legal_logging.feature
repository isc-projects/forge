Feature: Kea leases manipulation commands with legal logging hook

@v6 @kea_only @controlchannel @hook @lease_cmds @legal_logging
  Scenario: hook.v6.lease.cmds.legal.logging.add
  Test Procedure:
  Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
  Server is configured with preference option with value 123.
  Server is configured with domain-search option with value domain1.example.com,domain2.isc.org.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_lease_cmds.so.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_legal_log.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

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
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command": "lease6-add","arguments": {"subnet-id": 1,"ip-address": "2001:db8:1::1","duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24","iaid": 1234}}

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
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

  Client download file from server stored in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: Administrator added a lease of address: 2001:db8:1::1 to a device with DUID: 1a:1b:1c:1d:1e:1f:20:21:22:23:24


@v6 @kea_only @controlchannel @hook @lease_cmds @legal_logging
  Scenario: hook.v6.lease.cmds.legal.logging.del-using-address
  Test Procedure:
  Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_lease_cmds.so.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_legal_log.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  Test Procedure:
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:22:33:44:55:66.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"lease6-del","arguments":{"ip-address": "2001:db8:1::1"}}

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:22:33:44:55:66.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.

  Client download file from server stored in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: Administrator deleted the lease for address: 2001:db8:1::1

@v6 @kea_only @controlchannel @hook @lease_cmds @legal_logging
  Scenario: hook.v6.lease.cmds.legal.logging.del-using-duid
  Test Procedure:
  Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_lease_cmds.so.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_legal_log.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client sets ia_id value to 666.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  Test Procedure:
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:22:33:44:55:66.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"lease6-del","arguments":{"subnet-id":1,"identifier": "00:03:00:01:66:55:44:33:22:11","identifier-type": "duid","iaid":666}}

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:22:33:44:55:66.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.

  Client download file from server stored in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: Administrator deleted a lease for a device identified by: duid of 00:03:00:01:66:55:44:33:22:11

@v6 @kea_only @controlchannel @hook @lease_cmds @legal_logging @disabled
  Scenario: hook.v6.lease.cmds.legal.logging.wipe
  Test Procedure:
  Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::2 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_lease_cmds.so.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_legal_log.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  Test Procedure:
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:22:33:44:55:66.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  Test Procedure:
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client sets DUID value to 00:03:00:01:11:22:33:44:55:66.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:11:11:11:11:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"lease6-wipe", "arguments": {"subnet-id":1}}

  Client download file from server stored in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.
  Fail test.
  #File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)

@v6 @kea_only @controlchannel @hook @lease_cmds @legal_logging
  Scenario: hook.v6.lease.cmds.legal.logging.update
  Test Procedure:
  Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::2 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_lease_cmds.so.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_legal_log.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client sets ia_id value to 666.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  Test Procedure:
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8:1::1,00:03:00:01:66:55:44:33:22:11,4000,
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: ,1,3000,0,666,128,0,0,,66:55:44:33:22:11,0

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST NOT contain line or phrase: 2001:db8:1::1,01:02:03:04:05:06:07:08
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST NOT contain line or phrase: ,urania.example.org,1a:1b:1c:1d:1e:1f,

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"lease6-update", "arguments":{"subnet-id": 1,"ip-address": "2001:db8:1::1","duid": "01:02:03:04:05:06:07:08","iaid": 1234,"hw-address": "1a:1b:1c:1d:1e:1f","preferred-lft": 500,"valid-lft": 1000,"hostname": "urania.example.org"}}
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: ,1,500,0,1234,128,0,0,urania.example.org,1a:1b:1c:1d:1e:1f,0
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8:1::1,01:02:03:04:05:06:07:08,1000

  Client download file from server stored in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: Administrator updated information on the lease of address: 2001:db8:1::1 to a device with DUID: 01:02:03:04:05:06:07:08, hardware address: 1a:1b:1c:1d:1e:1f for 0 hrs 16 mins 40 secs