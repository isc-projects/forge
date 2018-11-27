Feature: Kea Hook flex-id testing

@v4 @flexid @kea_only
  Scenario: v4.hooks.flexid-libreload
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.50 pool.
  Reserve hostname reserved-hostname in subnet 0 for host uniquely identified by flex-id 'docsis3.0'.
  For host reservation entry no. 0 in subnet 0 add address with value 192.168.50.10.
  Add to config file line: "host-reservation-identifiers": [ "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: option[60].hex
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.10.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command": "libreload","arguments": {}}
  # if reload works - classification should work without changes

  Test Procedure:
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.10.

@v4 @flexid @kea_only
  Scenario: v4.hooks.flexid-reconfigure
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.50 pool.
  Reserve hostname reserved-hostname in subnet 0 for host uniquely identified by flex-id 'docsis3.0'.
  For host reservation entry no. 0 in subnet 0 add address with value 192.168.50.10.
  Add to config file line: "host-reservation-identifiers": [ "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: option[60].hex
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.10.

  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.50 pool.
  Reserve hostname reserved-hostname in subnet 0 for host uniquely identified by flex-id 'docsis3.0'.
  For host reservation entry no. 0 in subnet 0 add address with value 192.168.50.10.
  Add to config file line: "host-reservation-identifiers": [ "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: option[60].hex
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Send server configuration using SSH and config-file.
  DHCP server is reconfigured.

  Test Procedure:
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.10.

@v4 @flexid @kea_only
  Scenario: v4.hooks.flexid-inside-pool
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.50 pool.
  Reserve hostname reserved-hostname in subnet 0 for host uniquely identified by flex-id 'docsis3.0'.
  For host reservation entry no. 0 in subnet 0 add address with value 192.168.50.10.
  Add to config file line: "host-reservation-identifiers": [ "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: option[60].hex
  Send server configuration using SSH and config-file.
  DHCP server is started.

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
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.50 pool.
  Reserve hostname reserved-hostname in subnet 0 for host uniquely identified by flex-id 'docsis3.0'.
  For host reservation entry no. 0 in subnet 0 add address with value 192.168.50.10.
  Add to config file line: "host-reservation-identifiers": [ "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: option[60].hex
  Send server configuration using SSH and config-file.
  DHCP server is started.

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
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.9 pool.
  Reserve hostname reserved-hostname in subnet 0 for host uniquely identified by flex-id 'docsis3.0'.
  For host reservation entry no. 0 in subnet 0 add address with value 192.168.50.10.
  Add to config file line: "host-reservation-identifiers": [ "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: option[60].hex
  Send server configuration using SSH and config-file.
  DHCP server is started.

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
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.50 pool.
  Reserve address 192.168.50.10 in subnet 0 for host uniquely identified by flex-id 'docsis3.0'.
  Add to config file line: "host-reservation-identifiers": ["hw-address", "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: option[60].hex
  To hook no. 1 add parameter named replace-client-id with value: true
  Add configuration parameter match-client-id with value false to global configuration.
  Send server configuration using SSH and config-file.
  DHCP server is started.

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

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.50.10,ff:01:02:03:ff:04,,4000
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.50.10,ff:01:02:03:ff:04,,0

@v4 @flexid @kea_only
  Scenario: v4.hooks.flexid-replace-client-id-release-fail
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.5 pool.
  Reserve address 192.168.50.10 in subnet 0 for host uniquely identified by flex-id 'docsis3.0'.
  Add to config file line: "host-reservation-identifiers": ["hw-address", "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: option[60].hex
  To hook no. 1 add parameter named replace-client-id with value: true
  # enable matching client id
  Add configuration parameter match-client-id with value true to global configuration.
  Send server configuration using SSH and config-file.
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
  #Client adds to the message vendor_class_id with value docsis3.0.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with NAK message.

@v4 @flexid @kea_only
  Scenario: v4.hooks.flexid-replace-client-id-release-1
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.5 pool.
  Reserve address 192.168.50.10 in subnet 0 for host uniquely identified by flex-id 'docsis3.0'.
  Add to config file line: "host-reservation-identifiers": ["hw-address", "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: option[60].hex
  To hook no. 1 add parameter named replace-client-id with value: true
  # enable matching client id
  Add configuration parameter match-client-id with value true to global configuration.
  Send server configuration using SSH and config-file.
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

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST NOT contain line or phrase: ff:01:02:03:ff:04:11:22:33
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,4000
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST NOT contain line or phrase: 192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,0


@v4 @flexid @kea_only
  Scenario: v4.hooks.flexid-replace-client-id-release-2
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.5 pool.
  Reserve address 192.168.50.10 in subnet 0 for host uniquely identified by flex-id 'docsis3.0'.
  Add to config file line: "host-reservation-identifiers": ["hw-address", "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: option[60].hex
  To hook no. 1 add parameter named replace-client-id with value: true
  # enable matching client id
  Add configuration parameter match-client-id with value true to global configuration.
  Send server configuration using SSH and config-file.
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

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST NOT contain line or phrase: ff:01:02:03:ff:04:11:22:33
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,4000
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,0

@v4 @flexid @kea_only
  Scenario: v4.hooks.flexid-replace-client-id-renew-1
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.5 pool.
  Reserve address 192.168.50.10 in subnet 0 for host uniquely identified by flex-id 'docsis3.0'.
  Add to config file line: "host-reservation-identifiers": ["hw-address", "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: option[60].hex
  To hook no. 1 add parameter named replace-client-id with value: true
  # enable matching client id
  Add configuration parameter match-client-id with value true to global configuration.
  Send server configuration using SSH and config-file.
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

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST NOT contain line or phrase: ff:01:02:03:ff:04:11:22:33
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,4000

@v4 @flexid @kea_only
  Scenario: v4.hooks.flexid-replace-client-id-renew-2
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.5 pool.
  Reserve address 192.168.50.10 in subnet 0 for host uniquely identified by flex-id 'docsis3.0'.
  Add to config file line: "host-reservation-identifiers": ["hw-address", "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: option[60].hex
  To hook no. 1 add parameter named replace-client-id with value: true
  # enable matching client id
  Add configuration parameter match-client-id with value true to global configuration.
  Send server configuration using SSH and config-file.
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

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST NOT contain line or phrase: ff:01:02:03:ff:04:11:22:33
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.50.10,ff:01:02:03:ff:04,00:64:6f:63:73:69:73:33:2e:30,4000

@v4 @flexid @kea_only
  Scenario: v4.hooks.flexid-mysql-1
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.5 pool.
  Add to config file line: "host-reservation-identifiers": ["hw-address", "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: option[60].hex
  To hook no. 1 add parameter named replace-client-id with value: true
  # enable matching client id
  Add configuration parameter match-client-id with value true to global configuration.

  Use MySQL reservation system.
  # 646f63736973332e30 = docsis3.0
  Create new MySQL reservation identified by flex-id 646f63736973332e30.
  Add hostname reserved-hostname to MySQL reservation record id 1.
  Add ipv4_address 192.168.50.10 to MySQL reservation record id 1.
  Add dhcp4_subnet_id 1 to MySQL reservation record id 1.
  Upload hosts reservation to MySQL database.

  Send server configuration using SSH and config-file.
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
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.5 pool.
  Add to config file line: "host-reservation-identifiers": ["hw-address", "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: option[60].hex
  To hook no. 1 add parameter named replace-client-id with value: true
  # enable matching client id
  Add configuration parameter match-client-id with value true to global configuration.

  Use MySQL reservation system.
  # 646f63736973332e30 = docsis3.0
  Create new MySQL reservation identified by flex-id 646f63736973332e30.
  Add hostname reserved-hostname to MySQL reservation record id 1.
  Add ipv4_address 192.168.50.10 to MySQL reservation record id 1.
  Add dhcp4_subnet_id 1 to MySQL reservation record id 1.
  Upload hosts reservation to MySQL database.

  Send server configuration using SSH and config-file.
  DHCP server is started.

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
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.5 pool.
  Add to config file line: "host-reservation-identifiers": ["hw-address", "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: option[60].hex
  To hook no. 1 add parameter named replace-client-id with value: true
  # enable matching client id
  Add configuration parameter match-client-id with value true to global configuration.

  Use PostgreSQL reservation system.
  Create new PostgreSQL reservation identified by flex-id 646f63736973332e30.
  Add hostname reserved-hostname to PostgreSQL reservation record id 1.
  Add ipv4_address 192.168.50.10 to PostgreSQL reservation record id 1.
  Add dhcp4_subnet_id 1 to PostgreSQL reservation record id 1.
  Upload hosts reservation to PostgreSQL database.

  Send server configuration using SSH and config-file.
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
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.5 pool.
  Add to config file line: "host-reservation-identifiers": ["hw-address", "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: option[60].hex
  To hook no. 1 add parameter named replace-client-id with value: true
  # enable matching client id
  Add configuration parameter match-client-id with value true to global configuration.

  Use PostgreSQL reservation system.
  Create new PostgreSQL reservation identified by flex-id 646f63736973332e30.
  Add hostname reserved-hostname to PostgreSQL reservation record id 1.
  Add ipv4_address 192.168.50.10 to PostgreSQL reservation record id 1.
  Add dhcp4_subnet_id 1 to PostgreSQL reservation record id 1.
  Upload hosts reservation to PostgreSQL database.

  Send server configuration using SSH and config-file.
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