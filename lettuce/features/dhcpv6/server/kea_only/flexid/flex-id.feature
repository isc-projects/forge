Feature: Kea Hook flex-id testing

@v6 @flexid @kea_only
  Scenario: flexid_1
  Test Setup:
  Client sends local file stored in: features/dhcpv6/server/kea_only/flexid/hook_1.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/kea.conf.
  Client sends local file stored in: features/dhcpv6/server/kea_only/flexid/ctrl.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/keactrl.conf.
  DHCP server is started.
  #Pause the Test.

  #Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "config-reload","arguments":  {} }
  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

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
  #Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:1::1.
  Relayed Message sub-option 5 from option 3 MUST contain address 3000::f.

@v6 @flexid @kea_only
  Scenario: flexid_2
  Test Setup:
  Client sends local file stored in: features/dhcpv6/server/kea_only/flexid/hook_2.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/kea.conf.
  Client sends local file stored in: features/dhcpv6/server/kea_only/flexid/ctrl.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/keactrl.conf.
  DHCP server is started.
  #Pause the Test.

  #Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "config-reload","arguments":  {} }
  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

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
  #Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:1::1.
  Relayed Message sub-option 5 from option 3 MUST contain address 3000::f.


@v6 @flexid @kea_only
  Scenario: flexid_3
  Test Setup:
  Client sends local file stored in: features/dhcpv6/server/kea_only/flexid/hook_3.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/kea.conf.
  Client sends local file stored in: features/dhcpv6/server/kea_only/flexid/ctrl.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/keactrl.conf.
  DHCP server is started.
  #Pause the Test.

  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  #Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_flex_id.so.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.
  DHCP server is started.
  #Pause the Test.

  Test Procedure:
    Client sets enterprisenum value to 4491.
  Client does include vendor-class.
  Client adds suboption for vendor specific information with code: 1026 and data: 01:02:03:04:05:06.
  Client does include vendor-specific-info.

  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	Response sub-option 5 from option 3 MUST contain address 3000::f.


  @v6 @flexid @kea_only
  Scenario: flexid_mysql_1
  Test Setup:
  Client sends local file stored in: features/dhcpv6/server/kea_only/flexid/hook_mysql_1.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/kea.conf.
  Client sends local file stored in: features/dhcpv6/server/kea_only/flexid/ctrl.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/keactrl.conf.

  Use MySQL reservation system.
  Create new MySQL reservation identified by flex-id port1234.
  Add hostname reserved-hostname to MySQL reservation record id 1.
  Add dhcp6_subnet_id 1 to MySQL reservation record id 1.
  Add IPv6 address reservation 3000::f with iaid $(EMPTY) to MySQL record id 1.
  Upload hosts reservation to MySQL database.

  DHCP server is started.
  #Pause the Test.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

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
  Relayed Message sub-option 5 from option 3 MUST contain address 3000::f.

@v6 @flexid @kea_only
  Scenario: flexid_pgsql_1
  Test Setup:
  Client sends local file stored in: features/dhcpv6/server/kea_only/flexid/hook_pgsql_1.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/kea.conf.
  Client sends local file stored in: features/dhcpv6/server/kea_only/flexid/ctrl.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/keactrl.conf.

  Use PostgreSQL reservation system.
  Create new PostgreSQL reservation identified by flex-id port1234.
  Add hostname reserved-hostname to PostgreSQL reservation record id 1.
  Add dhcp6_subnet_id 1 to PostgreSQL reservation record id 1.
  Add IPv6 address reservation 3000::f with iaid $(EMPTY) to PostgreSQL record id 1.
  Upload hosts reservation to PostgreSQL database.

  DHCP server is started.
  #Pause the Test.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

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

  Relayed Message sub-option 5 from option 3 MUST contain address 3000::f.
