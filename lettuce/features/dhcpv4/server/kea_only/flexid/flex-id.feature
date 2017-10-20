Feature: Kea Hook flex-id testing

@v4 @flexid @kea_only
  Scenario: v4.hooks.flexid-inside-pool
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
  #Client adds to the message vendor_class_id with value docsis3.0.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

@v4 @flexid @kea_only
  Scenario: v4.hooks.flexid-inside-pool-negative
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
  #Client adds to the message vendor_class_id with value docsis3.0.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client adds to the message vendor_class_id with value docsis3.1.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with NAK message.

@v4 @flexid @kea_only
  Scenario: v4.hooks.flexid-outside-pool
  Test Setup:
  Client sends local file stored in: features/dhcpv4/server/kea_only/flexid/hook_2.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/kea.conf.
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
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

@v4 @flexid @kea_only
  Scenario: v4.hooks.flexid-replace-mac-addr-inside-pool
  Test Setup:
  Client sends local file stored in: features/dhcpv4/server/kea_only/flexid/hook_1_replace.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/kea.conf.
  Client sends local file stored in: features/dhcpv4/server/kea_only/flexid/ctrl.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/keactrl.conf.
  # matching client id is disabled
  DHCP server is started.
  #Pause the Test.

  # server should act normally, mac address should not be replaced
  Test Procedure:
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.10.

  Test Procedure:
  Client adds to the message vendor_class_id with value docsis3.0.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client adds to the message vendor_class_id with value docsis3.0.
  Client copies server_id option from received message.
  Client sets ciaddr value to 192.168.50.10.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends RELEASE message.

  Pass Criteria:
  Server MUST NOT respond.

  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.50.10,ff:01:02:03:ff:04,,4000
  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.50.10,ff:01:02:03:ff:04,,0

@v4 @flexid @kea_only
  Scenario: v4.hooks.flexid-replace-client-id-release-fail
  Test Setup:
  Client sends local file stored in: features/dhcpv4/server/kea_only/flexid/hook_2_replace.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/kea.conf.
  Client sends local file stored in: features/dhcpv4/server/kea_only/flexid/ctrl.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/keactrl.conf.

  DHCP server is started.
  #Pause the Test.

  # server should act normally, mac address should not be replaced
  Test Procedure:
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.10.

  Test Procedure:
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client sets chaddr value to ff:01:02:03:ff:04.
  #Client adds to the message vendor_class_id with value docsis3.0.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with NAK message.

@v4 @flexid @kea_only
  Scenario: v4.hooks.flexid-replace-client-id-release-1
  Test Setup:
  Client sends local file stored in: features/dhcpv4/server/kea_only/flexid/hook_2_replace.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/kea.conf.
  Client sends local file stored in: features/dhcpv4/server/kea_only/flexid/ctrl.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/keactrl.conf.

  DHCP server is started.

  # server should act normally, mac address should not be replaced
  Test Procedure:
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.10.

  Test Procedure:
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22:33.
  Client copies server_id option from received message.
  Client sets ciaddr value to 192.168.50.10.
  Client sets chaddr value to ff:01:02:03:ff:04.
  #client sends message without option 60
  #Client adds to the message vendor_class_id with value docsis3.0.
  Client sends RELEASE message.

  Pass Criteria:
  Server MUST NOT respond.

  Test Procedure:
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22:33:44:55.
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.10.

  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases4.csv MUST NOT contain line or phrase: ff:01:02:03:ff:04:11:22:33
  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,4000
  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases4.csv MUST NOT contain line or phrase: 192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,0


@v4 @flexid @kea_only
  Scenario: v4.hooks.flexid-replace-client-id-release-2
  Test Setup:
  Client sends local file stored in: features/dhcpv4/server/kea_only/flexid/hook_2_replace.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/kea.conf.
  Client sends local file stored in: features/dhcpv4/server/kea_only/flexid/ctrl.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/keactrl.conf.

  DHCP server is started.

  # server should act normally, mac address should not be replaced
  Test Procedure:
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.10.

  Test Procedure:
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22:33.
  Client copies server_id option from received message.
  Client sets ciaddr value to 192.168.50.10.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sends RELEASE message.

  Pass Criteria:
  Server MUST NOT respond.

  Test Procedure:
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22:33:44:55.
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.10.

  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases4.csv MUST NOT contain line or phrase: ff:01:02:03:ff:04:11:22:33
  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,4000
  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,0

@v4 @flexid @kea_only
  Scenario: v4.hooks.flexid-replace-client-id-renew-1
  Test Setup:
  Client sends local file stored in: features/dhcpv4/server/kea_only/flexid/hook_2_replace.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/kea.conf.
  Client sends local file stored in: features/dhcpv4/server/kea_only/flexid/ctrl.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/keactrl.conf.

  DHCP server is started.

  # server should act normally, mac address should not be replaced
  Test Procedure:
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.10.

  Test Procedure:
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22:33:44:55.
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 61.
  Response MUST include option 54.

  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases4.csv MUST NOT contain line or phrase: ff:01:02:03:ff:04:11:22:33
  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,4000

@v4 @flexid @kea_only
  Scenario: v4.hooks.flexid-replace-client-id-renew-2
  Test Setup:
  Client sends local file stored in: features/dhcpv4/server/kea_only/flexid/hook_2_replace.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/kea.conf.
  Client sends local file stored in: features/dhcpv4/server/kea_only/flexid/ctrl.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/keactrl.conf.

  DHCP server is started.

  # server should act normally, mac address should not be replaced
  Test Procedure:
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.10.

  Test Procedure:
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  #Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST NOT contain yiaddr 192.168.50.10.
  Response MUST include option 61.
  Response MUST include option 54.

  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases4.csv MUST NOT contain line or phrase: ff:01:02:03:ff:04:11:22:33
  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,4000

@v4 @flexid @kea_only
  Scenario: v4.hooks.flexid-mysql-1
  Test Setup:
  Client sends local file stored in: features/dhcpv4/server/kea_only/flexid/hook_mysql_1.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/kea.conf.
  Client sends local file stored in: features/dhcpv4/server/kea_only/flexid/ctrl.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/keactrl.conf.

  Use MySQL reservation system.
  # 646f63736973332e30 = docsis3.0
  Create new MySQL reservation identified by flex-id 646f63736973332e30.
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
  Client adds to the message vendor_class_id with value docsis3.0.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

@v4 @flexid @kea_only
  Scenario: v4.hooks.flexid-mysql-negative
  Test Setup:
  Client sends local file stored in: features/dhcpv4/server/kea_only/flexid/hook_mysql_1.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/kea.conf.
  Client sends local file stored in: features/dhcpv4/server/kea_only/flexid/ctrl.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/keactrl.conf.

  Use MySQL reservation system.
  # 646f63736973332e30 = docsis3.0
  Create new MySQL reservation identified by flex-id 646f63736973332e30.
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
  Server MUST respond with NAK message.

@v4 @flexid @kea_only
  Scenario: v4.hooks.flexid-pgsql-1
  Test Setup:
  Client sends local file stored in: features/dhcpv4/server/kea_only/flexid/hook_pgsql_1.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/kea.conf.
  Client sends local file stored in: features/dhcpv4/server/kea_only/flexid/ctrl.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/keactrl.conf.

  Use PostgreSQL reservation system.
  Create new PostgreSQL reservation identified by flex-id 646f63736973332e30.
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
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

@v4 @flexid @kea_only
  Scenario: v4.hooks.flexid-pgsql-negative
  Test Setup:
  Client sends local file stored in: features/dhcpv4/server/kea_only/flexid/hook_pgsql_1.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/kea.conf.
  Client sends local file stored in: features/dhcpv4/server/kea_only/flexid/ctrl.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/keactrl.conf.

  Use PostgreSQL reservation system.
  Create new PostgreSQL reservation identified by flex-id 646f63736973332e30.
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
  Server MUST respond with NAK message.