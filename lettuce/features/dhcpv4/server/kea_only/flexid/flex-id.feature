Feature: Kea Hook flex-id testing

@v4 @flexid @kea_only
  Scenario: flexid_1
  Test Setup:
  Client sends local file stored in: features/dhcpv4/server/kea_only/flexid/hook_1.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/kea.conf.
  Client sends local file stored in: features/dhcpv4/server/kea_only/flexid/ctrl.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/keactrl.conf.

  DHCP server is started.
  #Pause the Test.

  Test Procedure:
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.10.

  Test Procedure:
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

@v4 @flexid @kea_only
  Scenario: flexid_mysql_1
  Test Setup:
  Client sends local file stored in: features/dhcpv4/server/kea_only/flexid/hook_mysql_1.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/kea.conf.
  Client sends local file stored in: features/dhcpv4/server/kea_only/flexid/ctrl.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/keactrl.conf.

  Use MySQL reservation system.
  Create new MySQL reservation identified by flex-id docsis3.0.
  Add hostname reserved-hostname to MySQL reservation record id 1.
  Add ipv4_address 192.168.50.10 to MySQL reservation record id 1.
  Add dhcp4_subnet_id 1 to MySQL reservation record id 1.
  Upload hosts reservation to MySQL database.

  DHCP server is started.
  #Pause the Test.

  Test Procedure:
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.10.

  Test Procedure:
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

@v4 @flexid @kea_only
  Scenario: flexid_pgsql_1
  Test Setup:
  Client sends local file stored in: features/dhcpv4/server/kea_only/flexid/hook_pgsql_1.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/kea.conf.
  Client sends local file stored in: features/dhcpv4/server/kea_only/flexid/ctrl.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/keactrl.conf.

  Use PostgreSQL reservation system.
  Create new PostgreSQL reservation identified by flex-id docsis3.0.
  Add hostname reserved-hostname to PostgreSQL reservation record id 1.
  Add ipv4_address 192.168.50.10 to PostgreSQL reservation record id 1.
  Add dhcp4_subnet_id 1 to PostgreSQL reservation record id 1.
  Upload hosts reservation to PostgreSQL database.

  DHCP server is started.
  #Pause the Test.

  Test Procedure:
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.10.

  Test Procedure:
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
