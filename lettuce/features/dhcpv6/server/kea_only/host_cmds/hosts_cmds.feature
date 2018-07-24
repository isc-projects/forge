Feature: Kea Hook hosts_cmds testing

@v6 @hosts_cmds @kea_only
  Scenario: v6.hosts.cmds.librelaod
  Test Setup:
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
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

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1::100"]}}}

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

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "libreload","arguments": {}}
  #TODO This is cool, but we need to actually check that reload is happening.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-del","arguments":{"subnet-id":1,"ip-address":"2001:db8:1::100"}}

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
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
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

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1::100"]}}}

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
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Use MySQL reservation system.
  Send server configuration using SSH and config-file.

  DHCP server is reconfigured.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1::100"]}}}

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
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
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

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1::100"]}}}

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
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
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

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1::100"]}}}

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

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-del","arguments":{"subnet-id":1,"ip-address":"2001:db8:1::100"}}

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
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
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

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1::100"]}}}

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

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-del","arguments":{"subnet-id":1,"ip-address":"2001:db8:1::100"}}

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
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
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

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1::100"]}}}

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
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
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

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1::100"]}}}

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

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "reservation-get","arguments":{"subnet-id":1,"identifier-type": "duid","identifier":"00:03:00:01:f6:f5:f4:f3:f2:01"}}

@v6 @hosts_cmds @kea_only
  Scenario: v6.hosts.cmds.get-reservation-pgsql
  Test Setup:
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
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

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1::100"]}}}

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

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "reservation-get","arguments":{"subnet-id":1,"identifier-type": "duid","identifier":"00:03:00:01:f6:f5:f4:f3:f2:01"}}


@v6 @hosts_cmds @kea_only
  Scenario: v6.hosts.cmds.add-reservation-mysql-flex-id

  Test Setup:
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Add to config file line: "host-reservation-identifiers": [ "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_flex_id.so.
  To hook no. 2 add parameter named identifier-expression with value: relay6[0].option[18].hex
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
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

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"flex-id":"'port1234'","ip-addresses":["2001:db8:1::100"]}}}

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
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Add to config file line: "host-reservation-identifiers": [ "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_flex_id.so.
  To hook no. 2 add parameter named identifier-expression with value: relay6[0].option[18].hex
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
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

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"flex-id":"'port1234'","ip-addresses":["2001:db8:1::100"]}}}

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
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
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

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1:cafe::1"],"prefixes":["2001:db8:2:abcd::/64"],"hostname":"foo.example.com","option-data":[{"name":"vendor-opts","data":"4491"},{"name":"tftp-servers","space":"vendor-4491","data":"3000:1::234"}]}}}
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
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1:cafe::1.
  Response MUST include option 25.
  Response sub-option 26 from option 25 MUST contain prefix 2001:db8:2:abcd::.

@v6 @hosts_cmds @kea_only
  Scenario: v6.hosts.cmds.add-reservation-complex-mysql
  Test Setup:
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
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

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"duid":"00:03:00:01:f6:f5:f4:f3:f2:01","ip-addresses":["2001:db8:1:cafe::1"],"prefixes":["2001:db8:2:abcd::/64"],"hostname":"foo.example.com","option-data":[{"name":"vendor-opts","data":"4491"},{"name":"tftp-servers","space":"vendor-4491","data":"3000:1::234"}]}}}
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
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1:cafe::1.
  Response MUST include option 25.
  Response sub-option 26 from option 25 MUST contain prefix 2001:db8:2:abcd::.
