Feature: Shared-Networks
  Tests for shared-networks functionality in Kea.

@v4 @sharednetworks @sharedsubnets @kea_only
  Scenario: v4.sharednetworks.negative-missing-name
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Server is configured with another subnet: 192.168.51.0/24 with 192.168.51.1-192.168.51.1 pool.
  #first shared subnet
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 0 configuration.
  Send server configuration using SSH and config-file.

  #DHCP server is started.
  DHCP server failed to start. During configure process.

@v4 @sharednetworks @sharedsubnets @kea_only
  Scenario: v4.sharednetworks.negative-not-unique-names
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Server is configured with another subnet: 192.168.51.0/24 with 192.168.51.1-192.168.51.1 pool.
  #first shared subnet
  Add subnet 0 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 0 configuration.
  #second shared-subnet
  Add subnet 1 to shared-subnet set 1.
  Add configuration parameter name with value "name-abc" to shared-subnet 1 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 1 configuration.
  Send server configuration using SSH and config-file.

  DHCP server failed to start. During configure process.

@v4 @sharednetworks @sharedsubnets @kea_only
  Scenario: v4.sharednetworks.single-shared-subnet-with-one-subnet-based-on-iface
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Add subnet 0 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 0 configuration.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.1.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.1.
  Client requests option 1.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

@v4 @sharednetworks @sharedsubnets @kea_only
  Scenario: v4.sharednetworks.single-shared-subnet-with-one-subnet-based-on-relay-address
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Add subnet 0 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter relay with value {"ip-address":"$(GIADDR4)"} to shared-subnet 0 configuration.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  # local client should not get anything!
  # let's fix it finally :/
#  Test Procedure:
#  Client requests option 1.
#  Client sets chaddr value to ff:01:02:03:ff:04.
#  Client sends DISCOVER message.
#
#  Pass Criteria:
#  Server MUST NOT respond.

  Test Procedure:
  Set network variable source_port with value 67.
  Set network variable source_address with value $(GIADDR4).
  Set network variable destination_address with value $(SRV4_ADDR).
  Client sets giaddr value to $(GIADDR4).
  Client sets chaddr value to 00:00:00:00:00:11.
  Client sets hops value to 1.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.1.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client sets giaddr value to $(GIADDR4).
  Client sets hops value to 1.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.1.
  Client requests option 1.
  Client sets chaddr value to 00:00:00:00:00:11.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Set network variable source_port with value 67.
  Set network variable source_address with value $(GIADDR4).
  Set network variable destination_address with value $(SRV4_ADDR).
  Client sets giaddr value to $(GIADDR4).
  Client sets chaddr value to 00:00:00:00:00:22.
  Client sets hops value to 1.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST NOT respond.

@v4 @sharednetworks @sharedsubnets @kea_only
  Scenario: v4.sharednetworks.single-shared-subnet-with-two-subnets-based-on-iface
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Server is configured with another subnet: 192.168.51.0/24 with 192.168.51.1-192.168.51.1 pool.
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 0 configuration.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:22.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.1.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:22.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.1.
  Client requests option 1.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:33.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.51.1.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:33.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.51.1.
  Client requests option 1.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.51.1.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.50.1,00:00:00:00:00:22
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.51.1,00:00:00:00:00:33

@v4 @sharednetworks @sharedsubnets @kea_only
  Scenario: v4.sharednetworks.single-shared-subnet-with-tree-subnets-based-on-iface-options-override
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Server is configured with another subnet: 192.168.51.0/24 with 192.168.51.1-192.168.51.1 pool.
  Server is configured with another subnet: 192.168.52.0/24 with 192.168.52.1-192.168.52.1 pool.
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add subnet 2 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 0 configuration.

  Server is configured with time-servers option with value 199.199.199.1.
  Server is configured with time-servers option in subnet 0 with value 199.199.199.10.
  Server is configured with time-servers option in subnet 1 with value 199.199.199.100.
  Server is configured with time-servers option in subnet 2 with value 199.199.199.200.

  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:22.
  Client requests option 1.
  Client requests option 4.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 4.
  Response option 4 MUST contain value 199.199.199.10.
  Response option 4 MUST NOT contain value 199.199.199.100.
  Response option 4 MUST NOT contain value 199.199.199.200.
  Response option 4 MUST NOT contain value 199.199.199.1.

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:22.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.1.
  Client requests option 1.
  Client requests option 4.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 4.
  Response option 4 MUST contain value 199.199.199.10.
  Response option 4 MUST NOT contain value 199.199.199.100.
  Response option 4 MUST NOT contain value 199.199.199.200.
  Response option 4 MUST NOT contain value 199.199.199.1.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.50.1,00:00:00:00:00:22

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:33.
  Client requests option 1.
  Client requests option 4.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.51.1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 4.
  Response option 4 MUST contain value 199.199.199.100.
  Response option 4 MUST NOT contain value 199.199.199.10.
  Response option 4 MUST NOT contain value 199.199.199.200.
  Response option 4 MUST NOT contain value 199.199.199.1.

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:33.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.51.1.
  Client requests option 1.
  Client requests option 4.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.51.1.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 4.
  Response option 4 MUST contain value 199.199.199.100.
  Response option 4 MUST NOT contain value 199.199.199.10.
  Response option 4 MUST NOT contain value 199.199.199.200.
  Response option 4 MUST NOT contain value 199.199.199.1.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.51.1,00:00:00:00:00:33

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:44.
  Client requests option 1.
  Client requests option 4.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.52.1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 4.
  Response option 4 MUST contain value 199.199.199.200.
  Response option 4 MUST NOT contain value 199.199.199.100.
  Response option 4 MUST NOT contain value 199.199.199.10.
  Response option 4 MUST NOT contain value 199.199.199.1.

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:44.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.52.1.
  Client requests option 1.
  Client requests option 4.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.52.1.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 4.
  Response option 4 MUST contain value 199.199.199.200.
  Response option 4 MUST NOT contain value 199.199.199.100.
  Response option 4 MUST NOT contain value 199.199.199.100.
  Response option 4 MUST NOT contain value 199.199.199.1.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.52.1,00:00:00:00:00:44

@v4 @sharednetworks @sharedsubnets @kea_only
  Scenario: v4.sharednetworks.single-shared-subnet-with-three-subnets-based-on-relay-address-options-override

  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Server is configured with another subnet: 192.168.51.0/24 with 192.168.51.1-192.168.51.1 pool.
  Server is configured with another subnet: 192.168.52.0/24 with 192.168.52.1-192.168.52.1 pool.
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add subnet 2 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter relay with value {"ip-address":"$(GIADDR4)"} to shared-subnet 0 configuration.

  Server is configured with time-servers option with value 199.199.199.1.
  Server is configured with time-servers option in subnet 0 with value 199.199.199.10.
  Server is configured with time-servers option in subnet 1 with value 199.199.199.100.
  Server is configured with time-servers option in subnet 2 with value 199.199.199.200.

  Send server configuration using SSH and config-file.

  DHCP server is started.

  #1
    Test Procedure:
  Set network variable source_port with value 67.
  Set network variable source_address with value $(GIADDR4).
  Set network variable destination_address with value $(SRV4_ADDR).
  Client sets giaddr value to $(GIADDR4).
  Client sets chaddr value to 00:00:00:00:00:11.
  Client sets hops value to 1.
  Client requests option 1.
  Client requests option 4.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 4.
  Response option 4 MUST contain value 199.199.199.10.
  Response option 4 MUST NOT contain value 199.199.199.100.
  Response option 4 MUST NOT contain value 199.199.199.200.
  Response option 4 MUST NOT contain value 199.199.199.1.

  Test Procedure:
  Client sets giaddr value to $(GIADDR4).
  Client sets hops value to 1.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.1.
  Client requests option 1.
  Client requests option 4.
  Client sets chaddr value to 00:00:00:00:00:11.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 4.
  Response option 4 MUST contain value 199.199.199.10.
  Response option 4 MUST NOT contain value 199.199.199.100.
  Response option 4 MUST NOT contain value 199.199.199.200.
  Response option 4 MUST NOT contain value 199.199.199.1.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.50.1,00:00:00:00:00:11

  #2
  Test Procedure:
  Set network variable source_port with value 67.
  Set network variable source_address with value $(GIADDR4).
  Set network variable destination_address with value $(SRV4_ADDR).
  Client sets giaddr value to $(GIADDR4).
  Client sets chaddr value to 00:00:00:00:00:22.
  Client sets hops value to 1.
  Client requests option 1.
  Client requests option 4.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.51.1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 4.
  Response option 4 MUST contain value 199.199.199.100.
  Response option 4 MUST NOT contain value 199.199.199.10.
  Response option 4 MUST NOT contain value 199.199.199.200.
  Response option 4 MUST NOT contain value 199.199.199.1.

  Test Procedure:
  Client sets giaddr value to $(GIADDR4).
  Client sets hops value to 1.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.51.1.
  Client requests option 1.
  Client requests option 4.
  Client sets chaddr value to 00:00:00:00:00:22.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.51.1.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 4.
  Response option 4 MUST contain value 199.199.199.100.
  Response option 4 MUST NOT contain value 199.199.199.10.
  Response option 4 MUST NOT contain value 199.199.199.200.
  Response option 4 MUST NOT contain value 199.199.199.1.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.51.1,00:00:00:00:00:22

  #3
  Test Procedure:
  Set network variable source_port with value 67.
  Set network variable source_address with value $(GIADDR4).
  Set network variable destination_address with value $(SRV4_ADDR).
  Client sets giaddr value to $(GIADDR4).
  Client sets chaddr value to 00:00:00:00:00:33.
  Client sets hops value to 1.
  Client requests option 1.
  Client requests option 4.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.52.1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 4.
  Response option 4 MUST contain value 199.199.199.200.
  Response option 4 MUST NOT contain value 199.199.199.10.
  Response option 4 MUST NOT contain value 199.199.199.100.
  Response option 4 MUST NOT contain value 199.199.199.1.

  Test Procedure:
  Client sets giaddr value to $(GIADDR4).
  Client sets hops value to 1.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.52.1.
  Client requests option 1.
  Client requests option 4.
  Client sets chaddr value to 00:00:00:00:00:33.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.52.1.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 4.
  Response option 4 MUST contain value 199.199.199.200.
  Response option 4 MUST NOT contain value 199.199.199.10.
  Response option 4 MUST NOT contain value 199.199.199.100.
  Response option 4 MUST NOT contain value 199.199.199.1.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.52.1,00:00:00:00:00:33

  #4
  Test Procedure:
  Set network variable source_port with value 67.
  Set network variable source_address with value $(GIADDR4).
  Set network variable destination_address with value $(SRV4_ADDR).
  Client sets giaddr value to $(GIADDR4).
  Client sets chaddr value to 00:00:00:00:00:44.
  Client sets hops value to 1.
  Client requests option 1.
  Client requests option 4.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST NOT respond.

@v4 @sharednetworks @sharedsubnets @kea_only
Scenario: v4.sharednetworks.two-shared-subnet-with-two-subnets-based-on-relay-address-and-iface
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Server is configured with another subnet: 192.168.51.0/24 with 192.168.51.1-192.168.51.1 pool.
  Server is configured with another subnet: 192.168.52.0/24 with 192.168.52.1-192.168.52.1 pool.
  Server is configured with another subnet: 192.168.53.0/24 with 192.168.53.1-192.168.53.1 pool.
  #first shared subnet
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 0 configuration.
  #second shared-subnet
  Add subnet 2 to shared-subnet set 1.
  Add subnet 3 to shared-subnet set 1.
  Add configuration parameter name with value "name-xyz" to shared-subnet 1 configuration.
  Add configuration parameter relay with value {"ip-address":"$(GIADDR4)"} to shared-subnet 1 configuration.

  Server is configured with time-servers option in subnet 0 with value 199.199.199.10.
  Server is configured with time-servers option in subnet 2 with value 199.199.199.100.
  Server is configured with time-servers option in subnet 3 with value 199.199.199.200.

  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:aa.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.1.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:aa.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.1.
  Client requests option 1.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:bb.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.51.1.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:bb.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.51.1.
  Client requests option 1.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.51.1.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.50.1,00:00:00:00:00:aa
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.51.1,00:00:00:00:00:bb

  Test Procedure:
  Set network variable source_port with value 67.
  Set network variable source_address with value $(GIADDR4).
  Set network variable destination_address with value $(SRV4_ADDR).
  Client sets giaddr value to $(GIADDR4).
  Client sets chaddr value to 00:00:00:00:00:22.
  Client sets hops value to 1.
  Client requests option 1.
  Client requests option 4.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.52.1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 4.
  Response option 4 MUST contain value 199.199.199.100.
  Response option 4 MUST NOT contain value 199.199.199.10.
  Response option 4 MUST NOT contain value 199.199.199.200.
  Response option 4 MUST NOT contain value 199.199.199.1.

  Test Procedure:
  Client sets giaddr value to $(GIADDR4).
  Client sets hops value to 1.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.52.1.
  Client requests option 1.
  Client requests option 4.
  Client sets chaddr value to 00:00:00:00:00:22.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.52.1.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 4.
  Response option 4 MUST contain value 199.199.199.100.
  Response option 4 MUST NOT contain value 199.199.199.10.
  Response option 4 MUST NOT contain value 199.199.199.200.
  Response option 4 MUST NOT contain value 199.199.199.1.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.52.1,00:00:00:00:00:22

  #3
  Test Procedure:
  Set network variable source_port with value 67.
  Set network variable source_address with value $(GIADDR4).
  Set network variable destination_address with value $(SRV4_ADDR).
  Client sets giaddr value to $(GIADDR4).
  Client sets chaddr value to 00:00:00:00:00:33.
  Client sets hops value to 1.
  Client requests option 1.
  Client requests option 4.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.53.1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 4.
  Response option 4 MUST contain value 199.199.199.200.
  Response option 4 MUST NOT contain value 199.199.199.10.
  Response option 4 MUST NOT contain value 199.199.199.100.
  Response option 4 MUST NOT contain value 199.199.199.1.

  Test Procedure:
  Client sets giaddr value to $(GIADDR4).
  Client sets hops value to 1.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.53.1.
  Client requests option 1.
  Client requests option 4.
  Client sets chaddr value to 00:00:00:00:00:33.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.53.1.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 4.
  Response option 4 MUST contain value 199.199.199.200.
  Response option 4 MUST NOT contain value 199.199.199.10.
  Response option 4 MUST NOT contain value 199.199.199.100.
  Response option 4 MUST NOT contain value 199.199.199.1.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.53.1,00:00:00:00:00:33


@v4 @sharednetworks @sharedsubnets @kea_only
  Scenario: v4.sharednetworks.single-shared-subnet-with-three-subnets-client-classification

  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Server is configured with another subnet: 192.168.51.0/24 with 192.168.51.1-192.168.51.1 pool.
  Server is configured with another subnet: 192.168.52.0/24 with 192.168.52.1-192.168.52.1 pool.
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add subnet 2 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 0 configuration.

  Server is configured with time-servers option with value 199.199.199.1.
  Server is configured with time-servers option in subnet 0 with value 199.199.199.10.
  Server is configured with time-servers option in subnet 1 with value 199.199.199.100.
  Server is configured with time-servers option in subnet 2 with value 199.199.199.200.

  Add class called Client_f2f1.
  To class no 1 add parameter named: test with value: option[61].hex == 0xff010203ff04f1f2
  Server is configured with client-classification option in subnet 1 with name Client_f2f1.

  Add class called Client_f2f2.
  To class no 2 add parameter named: test with value: option[61].hex == 0xff010203ff04f2f2
  Server is configured with client-classification option in subnet 2 with name Client_f2f2.

  Add class called Client_f2f0.
  To class no 3 add parameter named: test with value: option[61].hex == 0xff010203ff04f299
  Server is configured with client-classification option in subnet 0 with name Client_f2f0.

  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:22.
  Client adds to the message client_id with value ff:01:02:03:ff:04:f1:f2.
  Client requests option 1.
  Client requests option 4.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.51.1.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:22.
  Client adds to the message client_id with value ff:01:02:03:ff:04:f1:f2.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.51.1.
  Client requests option 1.
  Client requests option 4.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.51.1.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

#  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.50.1,00:00:00:00:00:22

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:33.
  Client adds to the message client_id with value ff:01:02:03:ff:04:f2:f2.
  Client requests option 1.
  Client requests option 4.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.52.1.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:33.
  Client adds to the message client_id with value ff:01:02:03:ff:04:f2:f2.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.52.1.
  Client requests option 1.
  Client requests option 4.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.52.1.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

#  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.51.1,00:00:00:00:00:33

@v4 @sharednetworks @sharedsubnets @kea_only
  Scenario: v4.sharednetworks.single-shared-subnet-with-three-subnets-client-classification-server-identifier
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Server is configured with another subnet: 192.168.51.0/24 with 192.168.51.1-192.168.51.1 pool.
  Server is configured with another subnet: 192.168.52.0/24 with 192.168.52.1-192.168.52.1 pool.
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add subnet 2 to shared-subnet set 0.

  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 0 configuration.

  Server is configured with dhcp-server-identifier option in subnet 1 with value 11.22.33.123.
  Server is configured with dhcp-server-identifier option in subnet 2 with value 44.44.44.222.

  Add class called Client_f2f1.
  To class no 1 add parameter named: test with value: option[61].hex == 0xff010203ff04f1f2
  Server is configured with client-classification option in subnet 1 with name Client_f2f1.

  Add class called Client_f2f2.
  To class no 2 add parameter named: test with value: option[61].hex == 0xff010203ff04f2f2
  Server is configured with client-classification option in subnet 2 with name Client_f2f2.

  Add class called Client_f2f0.
  To class no 3 add parameter named: test with value: option[61].hex == 0xff010203ff04f2f3
  Server is configured with client-classification option in subnet 0 with name Client_f2f0.

  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:22.
  Client adds to the message client_id with value ff:01:02:03:ff:04:f1:f2.
  Client requests option 1.
  Client requests option 4.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.51.1.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 54.
  Response option 54 MUST NOT contain value 44.44.44.222.
  Response option 54 MUST contain value 11.22.33.123.

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:22.
  Client adds to the message client_id with value ff:01:02:03:ff:04:f1:f2.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.51.1.
  Client requests option 1.
  Client requests option 4.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.51.1.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 54.
  Response option 54 MUST NOT contain value 44.44.44.222.
  Response option 54 MUST contain value 11.22.33.123.

#  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.50.1,00:00:00:00:00:22

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:33.
  Client adds to the message client_id with value ff:01:02:03:ff:04:f2:f2.
  Client requests option 1.
  Client requests option 4.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.52.1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 54.
  Response option 54 MUST NOT contain value 11.22.33.123.
  Response option 54 MUST contain value 44.44.44.222.

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:33.
  Client adds to the message client_id with value ff:01:02:03:ff:04:f2:f2.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.52.1.
  Client requests option 1.
  Client requests option 4.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.52.1.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 54.
  Response option 54 MUST NOT contain value 11.22.33.123.
  Response option 54 MUST contain value 44.44.44.222.

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:44.
  Client adds to the message client_id with value ff:01:02:03:ff:04:f2:f3.
  Client requests option 1.
  Client requests option 4.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 54.
  Response option 54 MUST NOT contain value 11.22.33.123.
  Response option 54 MUST NOT contain value 44.44.44.222.
  Response option 54 MUST contain value $(SRV4_ADDR).

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:44.
  Client adds to the message client_id with value ff:01:02:03:ff:04:f2:f3.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.1.
  Client requests option 1.
  Client requests option 4.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 54.
  Response option 54 MUST NOT contain value 11.22.33.123.
  Response option 54 MUST NOT contain value 44.44.44.222.
  Response option 54 MUST contain value $(SRV4_ADDR).
#  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.51.1,00:00:00:00:00:33

  @v4 @sharednetworks @sharedsubnets @kea_only
  Scenario: v4.sharednetworks.single-shared-subnet-with-three-subnets-client-classification-server-identifier-negative

  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Server is configured with another subnet: 192.168.51.0/24 with 192.168.51.1-192.168.51.1 pool.
  Server is configured with another subnet: 192.168.52.0/24 with 192.168.52.1-192.168.52.1 pool.
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add subnet 2 to shared-subnet set 0.

  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 0 configuration.

  Server is configured with dhcp-server-identifier option in subnet 1 with value 11.22.33.123.
  Server is configured with dhcp-server-identifier option in subnet 2 with value 44.44.44.222.

  Add class called Client_f2f1.
  To class no 1 add parameter named: test with value: option[61].hex == 0xff010203ff04f1f2
  Server is configured with client-classification option in subnet 1 with name Client_f2f1.

  Add class called Client_f2f2.
  To class no 2 add parameter named: test with value: option[61].hex == 0xff010203ff04f2f2
  Server is configured with client-classification option in subnet 2 with name Client_f2f2.

  Add class called Client_f2f0.
  To class no 3 add parameter named: test with value: option[61].hex == 0xff010203ff04f2f3
  Server is configured with client-classification option in subnet 0 with name Client_f2f0.

  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:22.
  Client adds to the message client_id with value ff:01:02:03:ff:04:f1:f2.
  Client requests option 1.
  Client requests option 4.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.51.1.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 54.
  Response option 54 MUST NOT contain value 44.44.44.222.
  Response option 54 MUST contain value 11.22.33.123.

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:22.
  Client adds to the message client_id with value ff:01:02:03:ff:04:f1:f2.
  Client adds to the message requested_addr with value 192.168.51.1.
  Client adds to the message server_id with value $(SRV4_ADDR).
    # that is weird, shouldn't it fail? those server id's dont match
  Client requests option 1.
  Client requests option 4.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.51.1.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 54.
  Response option 54 MUST NOT contain value 44.44.44.222.
  Response option 54 MUST contain value 11.22.33.123.

#  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.50.1,00:00:00:00:00:22

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:33.
  Client adds to the message client_id with value ff:01:02:03:ff:04:f2:f2.
  Client requests option 1.
  Client requests option 4.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.52.1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 54.
  Response option 54 MUST NOT contain value 11.22.33.123.
  Response option 54 MUST contain value 44.44.44.222.

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:33.
  Client adds to the message client_id with value ff:01:02:03:ff:04:f2:f2.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.52.1.
  Client requests option 1.
  Client requests option 4.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.52.1.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 54.
  Response option 54 MUST NOT contain value 11.22.33.123.
  Response option 54 MUST contain value 44.44.44.222.

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:44.
  Client adds to the message client_id with value ff:01:02:03:ff:04:f2:f3.
  Client requests option 1.
  Client requests option 4.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 54.
  Response option 54 MUST NOT contain value 11.22.33.123.
  Response option 54 MUST NOT contain value 44.44.44.222.
  Response option 54 MUST contain value $(SRV4_ADDR).

  Test Procedure:
  Client sets chaddr value to 00:00:00:00:00:44.
  Client adds to the message client_id with value ff:01:02:03:ff:04:f2:f3.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.1.
  Client requests option 1.
  Client requests option 4.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 54.
  Response option 54 MUST NOT contain value 11.22.33.123.
  Response option 54 MUST NOT contain value 44.44.44.222.
  Response option 54 MUST contain value $(SRV4_ADDR).
#  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.51.1,00:00:00:00:00:33
