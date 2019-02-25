Feature: Kea6 legal logging

@v4 @dhcp4 @kea_only @legal_logging
Scenario: v4.legal.log.assigned-address
  Test Procedure:
  Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.

  Test Setup:
  Time renew-timer is configured with value 3.
  Time rebind-timer is configured with value 50.
  Time valid-lifetime is configured with value 600.
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.50 pool.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_legal_log.so.
  Send server configuration using SSH and config-file.
DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message client_id with value 00010203040506.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response MUST include option 54.
  Response MUST include option 61.
  Response option 1 MUST contain value 255.255.255.0.
  Response option 61 MUST contain value 00010203040506.

  Test Procedure:
  Client adds to the message client_id with value 00010203040506.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.1.
  Client requests option 1.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response MUST include option 54.
  Response MUST include option 61.
  Response option 1 MUST contain value 255.255.255.0.
  Response option 61 MUST contain value 00010203040506.

  Client download file from server stored in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: to a device with hardware address: hwtype=1 ff:01:02:03:ff:04, client-id: 00:01:02:03:04:05:06

Scenario: v4.legal.log.assigned-address-pgsql
  Test Procedure:
  Remove all records from table logs in PostgreSQL database.

  Test Setup:
  Time renew-timer is configured with value 3.
  Time rebind-timer is configured with value 50.
  Time valid-lifetime is configured with value 600.
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.50 pool.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_legal_log.so.
  To hook no. 1 add parameter named name with value: $(DB_NAME)
  To hook no. 1 add parameter named password with value: $(DB_PASSWD)
  To hook no. 1 add parameter named type with value: postgresql
  To hook no. 1 add parameter named user with value: $(DB_USER)
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message client_id with value 00010203040506.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response MUST include option 54.
  Response MUST include option 61.
  Response option 1 MUST contain value 255.255.255.0.
  Response option 61 MUST contain value 00010203040506.

  Test Procedure:
  Client adds to the message client_id with value 00010203040506.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.1.
  Client requests option 1.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response MUST include option 54.
  Response MUST include option 61.
  Response option 1 MUST contain value 255.255.255.0.
  Response option 61 MUST contain value 00010203040506.

  Table logs in PostgreSQL database MUST contain line or phrase: Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs
  Table logs in PostgreSQL database MUST contain line or phrase: to a device with hardware address: hwtype=1 ff:01:02:03:ff:04, client-id: 00:01:02:03:04:05:06

Scenario: v4.legal.log.assigned-address-mysql
  Test Procedure:
  Remove all records from table logs in MySQL database.

  Test Setup:
  Time renew-timer is configured with value 3.
  Time rebind-timer is configured with value 50.
  Time valid-lifetime is configured with value 600.
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.50 pool.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_legal_log.so.
  To hook no. 1 add parameter named name with value: $(DB_NAME)
  To hook no. 1 add parameter named password with value: $(DB_PASSWD)
  To hook no. 1 add parameter named type with value: mysql
  To hook no. 1 add parameter named user with value: $(DB_USER)
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message client_id with value 00010203040506.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response MUST include option 54.
  Response MUST include option 61.
  Response option 1 MUST contain value 255.255.255.0.
  Response option 61 MUST contain value 00010203040506.

  Test Procedure:
  Client adds to the message client_id with value 00010203040506.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.1.
  Client requests option 1.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response MUST include option 54.
  Response MUST include option 61.
  Response option 1 MUST contain value 255.255.255.0.
  Response option 61 MUST contain value 00010203040506.

  Table logs in MySQL database MUST contain line or phrase: Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs
  Table logs in MySQL database MUST contain line or phrase: to a device with hardware address: hwtype=1 ff:01:02:03:ff:04, client-id: 00:01:02:03:04:05:06

@v4 @dhcp4 @kea_only @legal_logging
Scenario: v4.legal.log.assigned-address-without-client-id
  Test Procedure:
  Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.

  Test Setup:
  Time renew-timer is configured with value 3.
  Time rebind-timer is configured with value 50.
  Time valid-lifetime is configured with value 600.
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.50 pool.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_legal_log.so.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response MUST include option 54.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.1.
  Client requests option 1.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response MUST include option 54.
  Response option 1 MUST contain value 255.255.255.0.

  Client download file from server stored in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: to a device with hardware address: hwtype=1 ff:01:02:03:ff:04
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST NOT contain line or phrase: client-id:

@v4 @dhcp4 @kea_only @legal_logging
Scenario: v4.legal.log.assigned-address-without-client-id-pgsql
  Test Procedure:
  Remove all records from table logs in PostgreSQL database.

  Test Setup:
  Time renew-timer is configured with value 3.
  Time rebind-timer is configured with value 50.
  Time valid-lifetime is configured with value 600.
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.50 pool.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_legal_log.so.
  To hook no. 1 add parameter named name with value: $(DB_NAME)
  To hook no. 1 add parameter named password with value: $(DB_PASSWD)
  To hook no. 1 add parameter named type with value: postgresql
  To hook no. 1 add parameter named user with value: $(DB_USER)
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response MUST include option 54.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.1.
  Client requests option 1.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response MUST include option 54.
  Response option 1 MUST contain value 255.255.255.0.

  Table logs in PostgreSQL database MUST contain line or phrase: Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs
  Table logs in PostgreSQL database MUST contain line or phrase: to a device with hardware address: hwtype=1 ff:01:02:03:ff:04
  Table logs in PostgreSQL database MUST NOT contain line or phrase: client-id:


@v4 @dhcp4 @kea_only @legal_logging
Scenario: v4.legal.log.assigned-address-without-client-id-mysql
  Test Procedure:
  Remove all records from table logs in MySQL database.

  Test Setup:
  Time renew-timer is configured with value 3.
  Time rebind-timer is configured with value 50.
  Time valid-lifetime is configured with value 600.
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.50 pool.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_legal_log.so.
  To hook no. 1 add parameter named name with value: $(DB_NAME)
  To hook no. 1 add parameter named password with value: $(DB_PASSWD)
  To hook no. 1 add parameter named type with value: mysql
  To hook no. 1 add parameter named user with value: $(DB_USER)
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response MUST include option 54.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.1.
  Client requests option 1.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response MUST include option 54.
  Response option 1 MUST contain value 255.255.255.0.

  Table logs in MySQL database MUST contain line or phrase: Address: 192.168.50.1 has been assigned for 0 hrs 10 mins 0 secs
  Table logs in MySQL database MUST contain line or phrase: to a device with hardware address: hwtype=1 ff:01:02:03:ff:04
  Table logs in MySQL database MUST NOT contain line or phrase: client-id:


@v4 @dhcp4 @kea_only @legal_logging
  Scenario: v4.legal.log.assigned-address-via-relay-pgsql
  Test Procedure:
  Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.

  Test Setup:
  Time renew-timer is configured with value 3.
  Time rebind-timer is configured with value 50.
  Time valid-lifetime is configured with value 600.
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.2-192.168.50.2 pool.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_legal_log.so.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client adds to the message client_id with value 00010203040577.
  Set network variable source_port with value 67.
  Set network variable source_address with value $(GIADDR4).
  Set network variable destination_address with value $(SRV4_ADDR).
  Client sets giaddr value to $(GIADDR4).
  Client sets chaddr value to 00:00:00:00:00:00.
  Client sets hops value to 1.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.2.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:00.
  Client adds to the message client_id with value 00010203040577.
  Client sets giaddr value to $(GIADDR4).
  Client sets hops value to 1.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.2.
  Client requests option 1.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.2.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

  Client download file from server stored in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: Address: 192.168.50.2 has been assigned for 0 hrs 10 mins 0 secs to a device with hardware address: hwtype=1 00:00:00:00:00:00,
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: client-id: 00:01:02:03:04:05:77 connected via relay at address: $(GIADDR4)

@v4 @dhcp4 @kea_only @legal_logging
  Scenario: v4.legal.log.assigned-address-via-relay-pgsql
  Test Procedure:
  Remove all records from table logs in PostgreSQL database.

  Test Setup:
  Time renew-timer is configured with value 3.
  Time rebind-timer is configured with value 50.
  Time valid-lifetime is configured with value 600.
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.2-192.168.50.2 pool.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_legal_log.so.
  To hook no. 1 add parameter named name with value: $(DB_NAME)
  To hook no. 1 add parameter named password with value: $(DB_PASSWD)
  To hook no. 1 add parameter named type with value: postgresql
  To hook no. 1 add parameter named user with value: $(DB_USER)
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client adds to the message client_id with value 00010203040577.
  Set network variable source_port with value 67.
  Set network variable source_address with value $(GIADDR4).
  Set network variable destination_address with value $(SRV4_ADDR).
  Client sets giaddr value to $(GIADDR4).
  Client sets chaddr value to 00:00:00:00:00:00.
  Client sets hops value to 1.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.2.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:00.
  Client adds to the message client_id with value 00010203040577.
  Client sets giaddr value to $(GIADDR4).
  Client sets hops value to 1.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.2.
  Client requests option 1.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.2.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

  Table logs in PostgreSQL database MUST contain line or phrase: Address: 192.168.50.2 has been assigned for 0 hrs 10 mins 0 secs to a device with hardware address: hwtype=1 00:00:00:00:00:00,
  Table logs in PostgreSQL database MUST contain line or phrase: client-id: 00:01:02:03:04:05:77 connected via relay at address: $(GIADDR4)

@v4 @dhcp4 @kea_only @legal_logging
  Scenario: v4.legal.log.assigned-address-via-relay-mysql
  Test Procedure:
  Remove all records from table logs in MySQL database.

  Test Setup:
  Time renew-timer is configured with value 3.
  Time rebind-timer is configured with value 50.
  Time valid-lifetime is configured with value 600.
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.2-192.168.50.2 pool.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_legal_log.so.
  To hook no. 1 add parameter named name with value: $(DB_NAME)
  To hook no. 1 add parameter named password with value: $(DB_PASSWD)
  To hook no. 1 add parameter named type with value: mysql
  To hook no. 1 add parameter named user with value: $(DB_USER)
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client adds to the message client_id with value 00010203040577.
  Set network variable source_port with value 67.
  Set network variable source_address with value $(GIADDR4).
  Set network variable destination_address with value $(SRV4_ADDR).
  Client sets giaddr value to $(GIADDR4).
  Client sets chaddr value to 00:00:00:00:00:00.
  Client sets hops value to 1.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.2.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:00.
  Client adds to the message client_id with value 00010203040577.
  Client sets giaddr value to $(GIADDR4).
  Client sets hops value to 1.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.2.
  Client requests option 1.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.2.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

  Table logs in MySQL database MUST contain line or phrase: Address: 192.168.50.2 has been assigned for 0 hrs 10 mins 0 secs to a device with hardware address: hwtype=1 00:00:00:00:00:00,
  Table logs in MySQL database MUST contain line or phrase: client-id: 00:01:02:03:04:05:77 connected via relay at address: $(GIADDR4)

@v4 @dhcp4 @kea_only @legal_logging
  Scenario: v4.legal.log.renewed-address
  Test Procedure:
  Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.

  Test Setup:
  Time renew-timer is configured with value 3.
  Time rebind-timer is configured with value 50.
  Time valid-lifetime is configured with value 600.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_legal_log.so.
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Set network variable source_port with value 67.
  Set network variable source_address with value $(GIADDR4).
  Set network variable destination_address with value $(SRV4_ADDR).
  Client sets giaddr value to $(GIADDR4).
  Client sets hops value to 1.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response MUST include option 54.
  Response option 1 MUST contain value 255.255.255.0.
  Response option 54 MUST contain value $(SRV4_ADDR).

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sets giaddr value to $(GIADDR4).
  Client sets hops value to 1.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.1.
  Client requests option 1.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response MUST include option 54.
  Response option 1 MUST contain value 255.255.255.0.
  Response option 54 MUST contain value $(SRV4_ADDR).

  #make sure that T1 time expires and client will be in RENEWING state.
  Sleep for 3 seconds.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sets giaddr value to $(GIADDR4).
  Client sets hops value to 1.
  Client sets ciaddr value to 192.168.50.1.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 54.
  Response option 54 MUST contain value $(SRV4_ADDR).

  Client download file from server stored in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: Address: 192.168.50.1 has been renewed for 0 hrs 10 mins 0 secs
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: to a device with hardware address: hwtype=1 ff:01:02:03:ff:04 connected via relay at address: $(GIADDR4)

@v4 @dhcp4 @kea_only @legal_logging
  Scenario: v4.legal.log.renewed-address-pgsql
  Test Procedure:
  Remove all records from table logs in PostgreSQL database.

  Test Setup:
  Time renew-timer is configured with value 3.
  Time rebind-timer is configured with value 50.
  Time valid-lifetime is configured with value 600.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_legal_log.so.
  To hook no. 1 add parameter named name with value: $(DB_NAME)
  To hook no. 1 add parameter named password with value: $(DB_PASSWD)
  To hook no. 1 add parameter named type with value: postgresql
  To hook no. 1 add parameter named user with value: $(DB_USER)
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Set network variable source_port with value 67.
  Set network variable source_address with value $(GIADDR4).
  Set network variable destination_address with value $(SRV4_ADDR).
  Client sets giaddr value to $(GIADDR4).
  Client sets hops value to 1.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response MUST include option 54.
  Response option 1 MUST contain value 255.255.255.0.
  Response option 54 MUST contain value $(SRV4_ADDR).

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sets giaddr value to $(GIADDR4).
  Client sets hops value to 1.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.1.
  Client requests option 1.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response MUST include option 54.
  Response option 1 MUST contain value 255.255.255.0.
  Response option 54 MUST contain value $(SRV4_ADDR).

  #make sure that T1 time expires and client will be in RENEWING state.
  Sleep for 3 seconds.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sets giaddr value to $(GIADDR4).
  Client sets hops value to 1.
  Client sets ciaddr value to 192.168.50.1.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 54.
  Response option 54 MUST contain value $(SRV4_ADDR).

  Table logs in PostgreSQL database MUST contain line or phrase: ddress: 192.168.50.1 has been renewed for 0 hrs 10 mins 0 secs
  Table logs in PostgreSQL database MUST contain line or phrase: to a device with hardware address: hwtype=1 ff:01:02:03:ff:04 connected via relay at address: $(GIADDR4)

@v4 @dhcp4 @kea_only @legal_logging
  Scenario: v4.legal.log.renewed-address-mysql
  Test Procedure:
  Remove all records from table logs in MySQL database.

  Test Setup:
  Time renew-timer is configured with value 3.
  Time rebind-timer is configured with value 50.
  Time valid-lifetime is configured with value 600.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_legal_log.so.
  To hook no. 1 add parameter named name with value: $(DB_NAME)
  To hook no. 1 add parameter named password with value: $(DB_PASSWD)
  To hook no. 1 add parameter named type with value: mysql
  To hook no. 1 add parameter named user with value: $(DB_USER)
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Set network variable source_port with value 67.
  Set network variable source_address with value $(GIADDR4).
  Set network variable destination_address with value $(SRV4_ADDR).
  Client sets giaddr value to $(GIADDR4).
  Client sets hops value to 1.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response MUST include option 54.
  Response option 1 MUST contain value 255.255.255.0.
  Response option 54 MUST contain value $(SRV4_ADDR).

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sets giaddr value to $(GIADDR4).
  Client sets hops value to 1.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.1.
  Client requests option 1.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response MUST include option 54.
  Response option 1 MUST contain value 255.255.255.0.
  Response option 54 MUST contain value $(SRV4_ADDR).

  #make sure that T1 time expires and client will be in RENEWING state.
  Sleep for 3 seconds.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sets giaddr value to $(GIADDR4).
  Client sets hops value to 1.
  Client sets ciaddr value to 192.168.50.1.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 54.
  Response option 54 MUST contain value $(SRV4_ADDR).

  Table logs in MySQL database MUST contain line or phrase: ddress: 192.168.50.1 has been renewed for 0 hrs 10 mins 0 secs
  Table logs in MySQL database MUST contain line or phrase: to a device with hardware address: hwtype=1 ff:01:02:03:ff:04 connected via relay at address: $(GIADDR4)

@v4 @dhcp4 @kea_only @legal_logging
  Scenario: v4.legal.log.rebind-address
  Test Procedure:
  Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.

  Test Setup:
  Time renew-timer is configured with value 3.
  Time rebind-timer is configured with value 4.
  Time valid-lifetime is configured with value 600.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_legal_log.so.
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Set network variable source_port with value 67.
  Set network variable source_address with value $(GIADDR4).
  Set network variable destination_address with value $(SRV4_ADDR).
  Client sets giaddr value to $(GIADDR4).
  Client sets hops value to 1.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response MUST include option 54.
  Response option 1 MUST contain value 255.255.255.0.
  Response option 54 MUST contain value $(SRV4_ADDR).

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sets giaddr value to $(GIADDR4).
  Client sets hops value to 1.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.1.
  Client requests option 1.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response MUST include option 54.
  Response option 1 MUST contain value 255.255.255.0.
  Response option 54 MUST contain value $(SRV4_ADDR).

  #make sure that T2 time expires and client will be in REBIND state.
  Sleep for 5 seconds.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sets giaddr value to $(GIADDR4).
  Client sets hops value to 1.
  Client sets ciaddr value to 192.168.50.1.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 54.
  Response option 54 MUST contain value $(SRV4_ADDR).

  Client download file from server stored in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: Address: 192.168.50.1 has been renewed for 0 hrs 10 mins 0 secs
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: to a device with hardware address: hwtype=1 ff:01:02:03:ff:04 connected via relay at address: $(GIADDR4)

@v4 @dhcp4 @kea_only @legal_logging
  Scenario: v4.legal.log.rebind-address-mysql
  Test Procedure:
  Remove all records from table logs in MySQL database.

  Test Setup:
  Time renew-timer is configured with value 3.
  Time rebind-timer is configured with value 4.
  Time valid-lifetime is configured with value 600.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_legal_log.so.
  To hook no. 1 add parameter named name with value: $(DB_NAME)
  To hook no. 1 add parameter named password with value: $(DB_PASSWD)
  To hook no. 1 add parameter named type with value: mysql
  To hook no. 1 add parameter named user with value: $(DB_USER)
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Set network variable source_port with value 67.
  Set network variable source_address with value $(GIADDR4).
  Set network variable destination_address with value $(SRV4_ADDR).
  Client sets giaddr value to $(GIADDR4).
  Client sets hops value to 1.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response MUST include option 54.
  Response option 1 MUST contain value 255.255.255.0.
  Response option 54 MUST contain value $(SRV4_ADDR).

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sets giaddr value to $(GIADDR4).
  Client sets hops value to 1.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.1.
  Client requests option 1.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response MUST include option 54.
  Response option 1 MUST contain value 255.255.255.0.
  Response option 54 MUST contain value $(SRV4_ADDR).

  #make sure that T2 time expires and client will be in REBIND state.
  Sleep for 5 seconds.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sets giaddr value to $(GIADDR4).
  Client sets hops value to 1.
  Client sets ciaddr value to 192.168.50.1.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 54.
  Response option 54 MUST contain value $(SRV4_ADDR).

  Table logs in MySQL database MUST contain line or phrase: Address: 192.168.50.1 has been renewed for 0 hrs 10 mins 0 secs
  Table logs in MySQL database MUST contain line or phrase: to a device with hardware address: hwtype=1 ff:01:02:03:ff:04 connected via relay at address: $(GIADDR4)


@v4 @dhcp4 @kea_only @legal_logging
  Scenario: v4.legal.log.rebind-address-pgsql
  Test Procedure:
  Remove all records from table logs in PostgreSQL database.

  Test Setup:
  Time renew-timer is configured with value 3.
  Time rebind-timer is configured with value 4.
  Time valid-lifetime is configured with value 600.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_legal_log.so.
  To hook no. 1 add parameter named name with value: $(DB_NAME)
  To hook no. 1 add parameter named password with value: $(DB_PASSWD)
  To hook no. 1 add parameter named type with value: postgresql
  To hook no. 1 add parameter named user with value: $(DB_USER)
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Set network variable source_port with value 67.
  Set network variable source_address with value $(GIADDR4).
  Set network variable destination_address with value $(SRV4_ADDR).
  Client sets giaddr value to $(GIADDR4).
  Client sets hops value to 1.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response MUST include option 54.
  Response option 1 MUST contain value 255.255.255.0.
  Response option 54 MUST contain value $(SRV4_ADDR).

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sets giaddr value to $(GIADDR4).
  Client sets hops value to 1.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.1.
  Client requests option 1.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response MUST include option 54.
  Response option 1 MUST contain value 255.255.255.0.
  Response option 54 MUST contain value $(SRV4_ADDR).

  #make sure that T2 time expires and client will be in REBIND state.
  Sleep for 5 seconds.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sets giaddr value to $(GIADDR4).
  Client sets hops value to 1.
  Client sets ciaddr value to 192.168.50.1.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 54.
  Response option 54 MUST contain value $(SRV4_ADDR).

  Table logs in PostgreSQL database MUST contain line or phrase: Address: 192.168.50.1 has been renewed for 0 hrs 10 mins 0 secs
  Table logs in PostgreSQL database MUST contain line or phrase: to a device with hardware address: hwtype=1 ff:01:02:03:ff:04 connected via relay at address: $(GIADDR4)