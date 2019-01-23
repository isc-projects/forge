Feature: Kea Hook hosts_cmds testing

@v6 @hosts_cmds @kea_only
  Scenario: v6.hosts.cmds.librelaod
  Test Setup:
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Use MySQL reservation system.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::50.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1::100"]}}}

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::100.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command": "libreload","arguments": {}}
  #TODO This is cool, but we need to actually check that reload is happening.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"reservation-del","arguments":{"subnet-id":1,"ip-address":"2001:db8:1::100"}}

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::50.

@v6 @hosts_cmds @kea_only
  Scenario: v6.hosts.cmds.reconfigure
  Test Setup:
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Use MySQL reservation system.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::50.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1::100"]}}}

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::100.

  Test Setup:
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Use MySQL reservation system.
  Send server configuration using SSH and config-file.

  DHCP server is reconfigured.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1::100"]}}}

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::100.

@v6 @hosts_cmds @kea_only
  Scenario: v6.hosts.cmds.add-reservation-mysql
  Test Setup:
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Use MySQL reservation system.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::50.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1::100"]}}}

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::100.

@v6 @hosts_cmds @kea_only
  Scenario: v6.hosts.cmds.del-reservation-mysql
  Test Setup:
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Use MySQL reservation system.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::50.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1::100"]}}}

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::100.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"reservation-del","arguments":{"subnet-id":1,"ip-address":"2001:db8:1::100"}}

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::50.

@v6 @hosts_cmds @kea_only
  Scenario: v6.hosts.cmds.del-reservation-pgsql
  Test Setup:
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Use PostgreSQL reservation system.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::50.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1::100"]}}}

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::100.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"reservation-del","arguments":{"subnet-id":1,"ip-address":"2001:db8:1::100"}}

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::50.

@v6 @hosts_cmds @kea_only
  Scenario: v6.hosts.cmds.add-reservation-pgsql
  Test Setup:
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Use PostgreSQL reservation system.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::50.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1::100"]}}}

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::100.


@v6 @hosts_cmds @kea_only
  Scenario: v6.hosts.cmds.get-reservation-mysql
  Test Setup:
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Use MySQL reservation system.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::50.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1::100"]}}}

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::100.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command": "reservation-get","arguments":{"subnet-id":1,"identifier-type": "duid","identifier":"00:03:00:01:f6:f5:f4:f3:f2:01"}}

@v6 @hosts_cmds @kea_only
  Scenario: v6.hosts.cmds.get-reservation-pgsql
  Test Setup:
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Use PostgreSQL reservation system.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::50.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1::100"]}}}

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::100.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command": "reservation-get","arguments":{"subnet-id":1,"identifier-type": "duid","identifier":"00:03:00:01:f6:f5:f4:f3:f2:01"}}


@v6 @hosts_cmds @kea_only
  Scenario: v6.hosts.cmds.add-reservation-mysql-flex-id

  Test Setup:
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so.
  Add to config file line: "host-reservation-identifiers": [ "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so.
  To hook no. 2 add parameter named identifier-expression with value: relay6[0].option[18].hex
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Use MySQL reservation system.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets linkaddr value to 2001:db8:1::1000.
  RelayAgent sets ifaceid value to port1234.
  RelayAgent does include interface-id.
  RelayAgent forwards message encapsulated in 1 level.

  Pass Criteria:
  Server MUST respond with RELAYREPLY message.
  Response MUST include option 18.
  Response MUST include option 9.
  Response option 9 MUST contain Relayed Message.
  Relayed Message MUST include option 1.
  Relayed Message MUST include option 2.
  Relayed Message MUST include option 3.
  Relayed Message option 3 MUST contain sub-option 5.
  Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:1::50.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"flex-id":"'port1234'","ip-addresses":["2001:db8:1::100"]}}}

  Test Procedure:
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets linkaddr value to 2001:db8:1::1000.
  RelayAgent sets ifaceid value to port1234.
  RelayAgent does include interface-id.
  RelayAgent forwards message encapsulated in 1 level.

  Pass Criteria:
  Server MUST respond with RELAYREPLY message.
  Response MUST include option 18.
  Response MUST include option 9.
  Response option 9 MUST contain Relayed Message.
  Relayed Message MUST include option 1.
  Relayed Message MUST include option 2.
  Relayed Message MUST include option 3.
  Relayed Message option 3 MUST contain sub-option 5.
  Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:1::100.


@v6 @hosts_cmds @kea_only
  Scenario: v6.hosts.cmds.add-reservation-pgsql-flex-id
  Test Setup:
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so.
  Add to config file line: "host-reservation-identifiers": [ "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so.
  To hook no. 2 add parameter named identifier-expression with value: relay6[0].option[18].hex
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Use PostgreSQL reservation system.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets linkaddr value to 2001:db8:1::1000.
  RelayAgent sets ifaceid value to port1234.
  RelayAgent does include interface-id.
  RelayAgent forwards message encapsulated in 1 level.

  Pass Criteria:
  Server MUST respond with RELAYREPLY message.
  Response MUST include option 18.
  Response MUST include option 9.
  Response option 9 MUST contain Relayed Message.
  Relayed Message MUST include option 1.
  Relayed Message MUST include option 2.
  Relayed Message MUST include option 3.
  Relayed Message option 3 MUST contain sub-option 5.
  Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:1::50.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"flex-id":"'port1234'","ip-addresses":["2001:db8:1::100"]}}}

  Test Procedure:
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets linkaddr value to 2001:db8:1::1000.
  RelayAgent sets ifaceid value to port1234.
  RelayAgent does include interface-id.
  RelayAgent forwards message encapsulated in 1 level.

  Pass Criteria:
  Server MUST respond with RELAYREPLY message.
  Response MUST include option 18.
  Response MUST include option 9.
  Response option 9 MUST contain Relayed Message.
  Relayed Message MUST include option 1.
  Relayed Message MUST include option 2.
  Relayed Message MUST include option 3.
  Relayed Message option 3 MUST contain sub-option 5.
  Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:1::100.


@v6 @hosts_cmds @kea_only
  Scenario: v6.hosts.cmds.add-reservation-complex-pgsql
  Test Setup:
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Use PostgreSQL reservation system.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client does include IA-PD.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::50.
  Response MUST include option 25.
  Response option 25 MUST contain sub-option 13.
  Response sub-option 13 from option 25 MUST contain statuscode 6.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1:0:cafe::1"],"prefixes":["2001:db8:2:abcd::/64"],"hostname":"foo.example.com","option-data":[{"name":"vendor-opts","data":"4491"},{"name":"tftp-servers","space":"vendor-4491","data":"3000:1::234"}]}}}
  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client does include IA-PD.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1:0:cafe::1.
  Response MUST include option 25.
  Response sub-option 26 from option 25 MUST contain prefix 2001:db8:2:abcd::.

@v6 @hosts_cmds @kea_only
  Scenario: v6.hosts.cmds.add-reservation-complex-mysql
  Test Setup:
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Use PostgreSQL reservation system.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client does include IA-PD.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::50.
  Response MUST include option 25.
  Response option 25 MUST contain sub-option 13.
  Response sub-option 13 from option 25 MUST contain statuscode 6.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1:0:cafe::1"],"prefixes":["2001:db8:2:abcd::/64"],"hostname":"foo.example.com","option-data":[{"name":"vendor-opts","data":"4491"},{"name":"tftp-servers","space":"vendor-4491","data":"3000:1::234"}]}}}
  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client does include IA-PD.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1:0:cafe::1.
  Response MUST include option 25.
  Response sub-option 26 from option 25 MUST contain prefix 2001:db8:2:abcd::.

@v6 @host_reservation @kea_only
Scenario: v6.hosts.cmds.reservation-get-all
Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server is configured with another subnet: 3001::/64 with 3001::1-3001::ff pool.
Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so.
Reserve hostname reserved-hostname1 in subnet 0 for host uniquely identified by hw-address f6:f5:f4:f3:f2:01.
Reserve hostname reserved-hostname2 in subnet 0 for host uniquely identified by hw-address f6:f5:f4:f3:f2:02.
Reserve hostname reserved-hostname3 in subnet 0 for host uniquely identified by hw-address f6:f5:f4:f3:f2:03.
Reserve hostname reserved-hostname4 in subnet 1 for host uniquely identified by hw-address f6:f5:f4:f3:f2:04.
Reserve hostname reserved-hostname5 in subnet 1 for host uniquely identified by hw-address f6:f5:f4:f3:f2:05.
Send server configuration using SSH and config-file.
DHCP server is started.

Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"reservation-get-all","arguments":{"subnet-id":1}}
JSON response in arguments MUST include value: reserved-hostname1
JSON response in arguments MUST include value: reserved-hostname2
JSON response in arguments MUST include value: reserved-hostname3
JSON response in arguments MUST NOT include value: reserved-hostname4
JSON response in arguments MUST NOT include value: reserved-hostname5
JSON response in text MUST include value: 3 IPv6 host(s) found.

@v6 @host_reservation @kea_only
Scenario: v6.hosts.cmds.reservation-get-all-mysql
Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server is configured with another subnet: 3001::/64 with 3001::1-3001::ff pool.
Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so.
Use MySQL reservation system.
Create new MySQL reservation identified by hw-address f6:f5:f4:f3:f2:01.
Add hostname reserved-hostname1 to MySQL reservation record id 1.
Add dhcp6_subnet_id 1 to MySQL reservation record id 1.
Create new MySQL reservation identified by hw-address f6:f5:f4:f3:f2:02.
Add hostname reserved-hostname2 to MySQL reservation record id 2.
Add dhcp6_subnet_id 1 to MySQL reservation record id 2.
Create new MySQL reservation identified by hw-address f6:f5:f4:f3:f2:03.
Add hostname reserved-hostname3 to MySQL reservation record id 3.
Add dhcp6_subnet_id 1 to MySQL reservation record id 3.
Create new MySQL reservation identified by hw-address f6:f5:f4:f3:f2:04.
Add hostname reserved-hostname4 to MySQL reservation record id 4.
Add dhcp6_subnet_id 2 to MySQL reservation record id 4.
Create new MySQL reservation identified by hw-address f6:f5:f4:f3:f2:05.
Add hostname reserved-hostname5 to MySQL reservation record id 5.
Add dhcp6_subnet_id 2 to MySQL reservation record id 5.
Upload hosts reservation to MySQL database.
Send server configuration using SSH and config-file.
DHCP server is started.

Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"reservation-get-all","arguments":{"subnet-id":1}}
JSON response in arguments MUST include value: reserved-hostname1
JSON response in arguments MUST include value: reserved-hostname2
JSON response in arguments MUST include value: reserved-hostname3
JSON response in arguments MUST NOT include value: reserved-hostname4
JSON response in arguments MUST NOT include value: reserved-hostname5
JSON response in text MUST include value: 3 IPv6 host(s) found.

@v6 @host_reservation @kea_only
Scenario: v6.hosts.cmds.reservation-get-all-pgsql
Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server is configured with another subnet: 3001::/64 with 3001::1-3001::ff pool.
Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so.
Use PostgreSQL reservation system.
Create new PostgreSQL reservation identified by hw-address f6:f5:f4:f3:f2:01.
Add hostname reserved-hostname1 to PostgreSQL reservation record id 1.
Add dhcp6_subnet_id 1 to PostgreSQL reservation record id 1.
Create new PostgreSQL reservation identified by hw-address f6:f5:f4:f3:f2:02.
Add hostname reserved-hostname2 to PostgreSQL reservation record id 2.
Add dhcp6_subnet_id 1 to PostgreSQL reservation record id 2.
Create new PostgreSQL reservation identified by hw-address f6:f5:f4:f3:f2:03.
Add hostname reserved-hostname3 to PostgreSQL reservation record id 3.
Add dhcp6_subnet_id 1 to PostgreSQL reservation record id 3.
Create new PostgreSQL reservation identified by hw-address f6:f5:f4:f3:f2:04.
Add hostname reserved-hostname4 to PostgreSQL reservation record id 4.
Add dhcp6_subnet_id 2 to PostgreSQL reservation record id 4.
Create new PostgreSQL reservation identified by hw-address f6:f5:f4:f3:f2:05.
Add hostname reserved-hostname5 to PostgreSQL reservation record id 5.
Add dhcp6_subnet_id 2 to PostgreSQL reservation record id 5.
Upload hosts reservation to PostgreSQL database.
Send server configuration using SSH and config-file.
DHCP server is started.

Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"reservation-get-all","arguments":{"subnet-id":1}}

JSON response in arguments MUST include value: reserved-hostname1
JSON response in arguments MUST include value: reserved-hostname2
JSON response in arguments MUST include value: reserved-hostname3
JSON response in arguments MUST NOT include value: reserved-hostname4
JSON response in arguments MUST NOT include value: reserved-hostname5
JSON response in text MUST include value: 3 IPv6 host(s) found.

@v6 @host_reservation @kea_only
Scenario: v6.hosts.cmds.reservation-get-page
Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server is configured with another subnet: 3001::/64 with 3001::1-3001::ff pool.
Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so.
Reserve hostname reserved-hostname1 in subnet 0 for host uniquely identified by hw-address f6:f5:f4:f3:f2:01.
Reserve hostname reserved-hostname2 in subnet 0 for host uniquely identified by hw-address f6:f5:f4:f3:f2:02.
Reserve hostname reserved-hostname3 in subnet 0 for host uniquely identified by hw-address f6:f5:f4:f3:f2:03.
Reserve hostname reserved-hostname4 in subnet 1 for host uniquely identified by hw-address f6:f5:f4:f3:f2:04.
Reserve hostname reserved-hostname5 in subnet 1 for host uniquely identified by hw-address f6:f5:f4:f3:f2:05.
Reserve hostname reserved-hostname6 in subnet 0 for host uniquely identified by hw-address f6:f5:f4:f3:f2:06.
Reserve hostname reserved-hostname7 in subnet 0 for host uniquely identified by hw-address f6:f5:f4:f3:f2:07.
Send server configuration using SSH and config-file.
DHCP server is started.

Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"reservation-get-page","arguments":{"subnet-id":1,"limit":3}}
JSON response in arguments MUST include value: reserved-hostname1
JSON response in arguments MUST include value: reserved-hostname2
JSON response in arguments MUST include value: reserved-hostname3
JSON response in arguments MUST NOT include value: reserved-hostname4
JSON response in arguments MUST NOT include value: reserved-hostname5
JSON response in arguments MUST NOT include value: reserved-hostname6
JSON response in arguments MUST NOT include value: reserved-hostname7
JSON response in text MUST include value: 3 IPv6 host(s) found.

Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"reservation-get-page","arguments":{"subnet-id":1,"limit":3,"from":3}}
JSON response in arguments MUST include value: reserved-hostname6
JSON response in arguments MUST include value: reserved-hostname7
JSON response in text MUST include value: 2 IPv6 host(s) found.


@v6 @host_reservation @kea_only
Scenario: v6.hosts.cmds.reservation-get-all-page-mysql
Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server is configured with another subnet: 3001::/64 with 3001::1-3001::ff pool.
Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so.
Use MySQL reservation system.
Create new MySQL reservation identified by hw-address f6:f5:f4:f3:f2:01.
Add hostname reserved-hostname1 to MySQL reservation record id 1.
Add dhcp6_subnet_id 1 to MySQL reservation record id 1.
Create new MySQL reservation identified by hw-address f6:f5:f4:f3:f2:02.
Add hostname reserved-hostname2 to MySQL reservation record id 2.
Add dhcp6_subnet_id 1 to MySQL reservation record id 2.
Create new MySQL reservation identified by hw-address f6:f5:f4:f3:f2:03.
Add hostname reserved-hostname3 to MySQL reservation record id 3.
Add dhcp6_subnet_id 1 to MySQL reservation record id 3.
Create new MySQL reservation identified by hw-address f6:f5:f4:f3:f2:04.
Add hostname reserved-hostname4 to MySQL reservation record id 4.
Add dhcp6_subnet_id 2 to MySQL reservation record id 4.
Create new MySQL reservation identified by hw-address f6:f5:f4:f3:f2:05.
Add hostname reserved-hostname5 to MySQL reservation record id 5.
Add dhcp6_subnet_id 2 to MySQL reservation record id 5.

Create new MySQL reservation identified by hw-address f6:f5:f4:f3:f2:06.
Add hostname reserved-hostname6 to MySQL reservation record id 6.
Add dhcp6_subnet_id 1 to MySQL reservation record id 6.
Create new MySQL reservation identified by hw-address f6:f5:f4:f3:f2:07.
Add hostname reserved-hostname7 to MySQL reservation record id 7.
Add dhcp6_subnet_id 1 to MySQL reservation record id 7.

Upload hosts reservation to MySQL database.
Send server configuration using SSH and config-file.
DHCP server is started.

Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"reservation-get-page","arguments":{"subnet-id":1,"limit":3}}
JSON response in arguments MUST include value: reserved-hostname1
JSON response in arguments MUST include value: reserved-hostname2
JSON response in arguments MUST include value: reserved-hostname3
JSON response in arguments MUST NOT include value: reserved-hostname4
JSON response in arguments MUST NOT include value: reserved-hostname5
JSON response in arguments MUST NOT include value: reserved-hostname6
JSON response in arguments MUST NOT include value: reserved-hostname7
JSON response in text MUST include value: 3 IPv6 host(s) found.

Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"reservation-get-page","arguments":{"subnet-id":1,"limit":3,"from":3}}
JSON response in arguments MUST include value: reserved-hostname6
JSON response in arguments MUST include value: reserved-hostname7
JSON response in text MUST include value: 2 IPv6 host(s) found.


@v6 @host_reservation @kea_only
Scenario: v6.hosts.cmds.reservation-get-all-page-pgsql
Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server is configured with another subnet: 3001::/64 with 3001::1-3001::ff pool.
Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so.
Use PostgreSQL reservation system.
Create new PostgreSQL reservation identified by hw-address f6:f5:f4:f3:f2:01.
Add hostname reserved-hostname1 to PostgreSQL reservation record id 1.
Add dhcp6_subnet_id 1 to PostgreSQL reservation record id 1.
Create new PostgreSQL reservation identified by hw-address f6:f5:f4:f3:f2:02.
Add hostname reserved-hostname2 to PostgreSQL reservation record id 2.
Add dhcp6_subnet_id 1 to PostgreSQL reservation record id 2.
Create new PostgreSQL reservation identified by hw-address f6:f5:f4:f3:f2:03.
Add hostname reserved-hostname3 to PostgreSQL reservation record id 3.
Add dhcp6_subnet_id 1 to PostgreSQL reservation record id 3.
Create new PostgreSQL reservation identified by hw-address f6:f5:f4:f3:f2:04.
Add hostname reserved-hostname4 to PostgreSQL reservation record id 4.
Add dhcp6_subnet_id 2 to PostgreSQL reservation record id 4.
Create new PostgreSQL reservation identified by hw-address f6:f5:f4:f3:f2:05.
Add hostname reserved-hostname5 to PostgreSQL reservation record id 5.
Add dhcp6_subnet_id 2 to PostgreSQL reservation record id 5.

Create new PostgreSQL reservation identified by hw-address f6:f5:f4:f3:f2:06.
Add hostname reserved-hostname6 to PostgreSQL reservation record id 6.
Add dhcp6_subnet_id 1 to PostgreSQL reservation record id 6.
Create new PostgreSQL reservation identified by hw-address f6:f5:f4:f3:f2:07.
Add hostname reserved-hostname7 to PostgreSQL reservation record id 7.
Add dhcp6_subnet_id 1 to PostgreSQL reservation record id 7.

Upload hosts reservation to PostgreSQL database.
Send server configuration using SSH and config-file.
DHCP server is started.

Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"reservation-get-page","arguments":{"subnet-id":1,"limit":3}}
JSON response in arguments MUST include value: reserved-hostname1
JSON response in arguments MUST include value: reserved-hostname2
JSON response in arguments MUST include value: reserved-hostname3
JSON response in arguments MUST NOT include value: reserved-hostname4
JSON response in arguments MUST NOT include value: reserved-hostname5
JSON response in arguments MUST NOT include value: reserved-hostname6
JSON response in arguments MUST NOT include value: reserved-hostname7
JSON response in text MUST include value: 3 IPv6 host(s) found.

Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"reservation-get-page","arguments":{"subnet-id":1,"limit":3,"from":3}}
JSON response in arguments MUST include value: reserved-hostname6
JSON response in arguments MUST include value: reserved-hostname7
JSON response in text MUST include value: 2 IPv6 host(s) found.