Feature: Shared-Networks
  Tests for shared-networks functionality in Kea.

@v6 @sharednetworks @sharedsubnets @kea_only
  Scenario: v6.sharednetworks.negative-missing-name
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Server is configured with another subnet: 2001:db8:d::/64 with 2001:db8:d::1-2001:db8:d::1 pool.
  #first shared subnet
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add configuration parameter interface-id with value "interface-abc" to shared-subnet 0 configuration.
  Send server configuration using SSH and config-file.

  #DHCP server is started.
  DHCP server failed to start. During configure process.

@v6 @sharednetworks @sharedsubnets @kea_only
  Scenario: v6.sharednetworks.negative-not-unique-names
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Server is configured with another subnet: 2001:db8:d::/64 with 2001:db8:d::1-2001:db8:d::1 pool.
  Server is configured with preference option in subnet 0 with value 123.
  Server is configured with dns-servers option in subnet 1 with value 2001:db8::1,2001:db8::2.
  #first shared subnet
  Add subnet 0 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface-id with value "interface-abc" to shared-subnet 0 configuration.
  #second shared-subnet
  Add subnet 1 to shared-subnet set 1.
  Add configuration parameter name with value "name-abc" to shared-subnet 1 configuration.
  Add configuration parameter interface-id with value "interface-xyz" to shared-subnet 1 configuration.
  Send server configuration using SSH and config-file.

  DHCP server failed to start. During configure process.

@v6 @sharednetworks @sharedsubnets @kea_only
  Scenario: v6.sharednetworks.single-shared-subnet-with-one-subnet-based-on-iface
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Add subnet 0 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 0 configuration.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
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
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.

@v6 @sharednetworks @sharedsubnets @kea_only
  Scenario: v6.sharednetworks.single-shared-subnet-with-one-subnet-based-on-relay-address
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Add subnet 0 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter relay with value {"ip-address":"2001:db8::abcd"} to shared-subnet 0 configuration.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  # there is no local subnet!

  Test Procedure:
  Client saves server-id option from received message.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-abc.
  RelayAgent does include interface-id.
  RelayAgent sets linkaddr value to 2001:db8::abcd.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include IA-NA.
  Client adds saved options. And DONT Erase.
  Client does include client-id.
  Client sends REQUEST message.

  RelayAgent sets ifaceid value to interface-abc.
  RelayAgent does include interface-id.
  RelayAgent sets linkaddr value to 2001:db8::abcd.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-abc.
  RelayAgent does include interface-id.
  RelayAgent sets linkaddr value to 2001:db8::abcd.
  RelayAgent forwards message encapsulated in 1 level.

  Pass Criteria:
  Server MUST respond with RELAYREPLY message.
  Response MUST include option 18.
  Response MUST include option 9.
  Response option 9 MUST contain Relayed Message.
  Relayed Message MUST include option 1.
  Relayed Message MUST include option 2.
  Relayed Message MUST include option 3.
  Relayed Message option 3 MUST contain sub-option 13.

  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8:a::1,00:03:00:01:f6:f5:f4:f3:f2:01

@v6 @sharednetworks @sharedsubnets @kea_only
  Scenario: v6.sharednetworks.single-shared-subnet-with-one-subnet-based-on-id
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Add subnet 0 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface-id with value "interface-abc" to shared-subnet 0 configuration.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  # there is no local subnet!

  Test Procedure:
  Client saves server-id option from received message.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-abc.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include IA-NA.
  Client adds saved options. And DONT Erase.
  Client does include client-id.
  Client sends REQUEST message.

  RelayAgent sets ifaceid value to interface-abc.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-abc.
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
  Relayed Message option 3 MUST contain sub-option 13.

  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8:a::1,00:03:00:01:f6:f5:f4:f3:f2:01

@v6 @sharednetworks @sharedsubnets @kea_only
  Scenario: v6.sharednetworks.single-shared-subnet-with-two-subnets-based-on-iface
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Server is configured with another subnet: 2001:db8:b::/64 with 2001:db8:b::1-2001:db8:b::1 pool.
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 0 configuration.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
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
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  #Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
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
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8:a::1,00:03:00:01:f6:f5:f4:f3:f2:01
  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8:b::1,00:03:00:01:f6:f5:f4:f3:f2:02

@v6 @sharednetworks @sharedsubnets @kea_only
  Scenario: v6.sharednetworks.single-shared-subnet-with-tree-subnets-based-on-iface-options-override
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Server is configured with another subnet: 2001:db8:b::/64 with 2001:db8:b::1-2001:db8:b::1 pool.
  Server is configured with another subnet: 2001:db8:c::/64 with 2001:db8:c::1-2001:db8:c::1 pool.
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add subnet 2 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 0 configuration.

  Server is configured with preference option with value 1.
  Server is configured with preference option in subnet 0 with value 33.
  Server is configured with preference option in subnet 1 with value 44.
  Server is configured with preference option in subnet 2 with value 55.

  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client requests option 7.
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response MUST include option 7.
  Response option 7 MUST NOT contain value 1.
  Response option 7 MUST contain value 33.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client requests option 7.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  #Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.
  Response MUST include option 7.
  Response option 7 MUST NOT contain value 1.
  Response option 7 MUST contain value 33.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 7.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response MUST include option 7.
  Response option 7 MUST NOT contain value 1.
  Response option 7 MUST contain value 44.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client requests option 7.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response MUST include option 7.
  Response option 7 MUST NOT contain value 1.
  Response option 7 MUST contain value 44.

@v6 @sharednetworks @sharedsubnets @kea_only
  Scenario: v6.sharednetworks.single-shared-subnet-with-three-subnets-based-on-id-options-override
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Server is configured with another subnet: 2001:db8:b::/64 with 2001:db8:b::1-2001:db8:b::1 pool.
  Server is configured with another subnet: 2001:db8:c::/64 with 2001:db8:c::1-2001:db8:c::1 pool.
  Server is configured with dns-servers option in subnet 1 with value 2001:db8::1,2001:db8::2.

  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add subnet 2 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface-id with value "interface-abc" to shared-subnet 0 configuration.

  Server is configured with preference option with value 1.
  Server is configured with preference option in subnet 0 with value 33.
  Server is configured with preference option in subnet 1 with value 44.
  Server is configured with preference option in subnet 2 with value 55.

  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client requests option 7.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.

  Test Procedure:
  Client saves server-id option from received message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  # there is no local subnet!

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 7.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-abc.
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
  Relayed Message MUST include option 7.
  Relayed Message option 7 MUST contain value 33.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include IA-NA.
  Client adds saved options. And DONT Erase.
  Client does include client-id.
  Client requests option 7.
  Client sends REQUEST message.

  RelayAgent sets ifaceid value to interface-abc.
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
  Relayed Message MUST include option 7.
  Relayed Message option 7 MUST contain value 33.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 7.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-abc.
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
  Relayed Message MUST include option 7.
  Relayed Message option 7 MUST contain value 44.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client does include IA-NA.
  Client adds saved options. And DONT Erase.
  Client does include client-id.
  Client requests option 7.
  Client sends REQUEST message.

  RelayAgent sets ifaceid value to interface-abc.
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
  Relayed Message MUST include option 7.
  Relayed Message option 7 MUST contain value 44.

@v6 @sharednetworks @sharedsubnets @kea_only
  Scenario: v6.sharednetworks.single-shared-subnet-with-two-subnets-based-on-id
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Server is configured with another subnet: 2001:db8:b::/64 with 2001:db8:b::1-2001:db8:b::1 pool.
  Server is configured with preference option in subnet 0 with value 123.
  Server is configured with dns-servers option in subnet 1 with value 2001:db8::1,2001:db8::2.
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface-id with value "interface-abc" to shared-subnet 0 configuration.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.

  Test Procedure:
  Client saves server-id option from received message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  # there is no local subnet!

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-abc.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include IA-NA.
  Client adds saved options. And DONT Erase.
  Client does include client-id.
  Client sends REQUEST message.

  RelayAgent sets ifaceid value to interface-abc.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-abc.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client does include IA-NA.
  Client adds saved options. And DONT Erase.
  Client does include client-id.
  Client sends REQUEST message.

  RelayAgent sets ifaceid value to interface-abc.
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

  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8:a::1,00:03:00:01:f6:f5:f4:f3:f2:01
  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8:b::1,00:03:00:01:f6:f5:f4:f3:f2:02

@v6 @sharednetworks @sharedsubnets @kea_only
  Scenario: v6.sharednetworks.single-shared-subnet-with-three-subnets-based-on-relay-address-options-override

  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Server is configured with another subnet: 2001:db8:b::/64 with 2001:db8:b::1-2001:db8:b::1 pool.
  Server is configured with another subnet: 2001:db8:c::/64 with 2001:db8:c::1-2001:db8:c::1 pool.
  Server is configured with dns-servers option in subnet 1 with value 2001:db8::1,2001:db8::2.

  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add subnet 2 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter relay with value {"ip-address":"2001:db8::abcd"} to shared-subnet 0 configuration.

  Server is configured with preference option with value 1.
  Server is configured with preference option in subnet 0 with value 33.
  Server is configured with preference option in subnet 1 with value 44.
  Server is configured with preference option in subnet 2 with value 55.

  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client requests option 7.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.

  Test Procedure:
  Client saves server-id option from received message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  # there is no local subnet!

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 7.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-abc.
  RelayAgent does include interface-id.
  RelayAgent sets linkaddr value to 2001:db8::abcd.
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
  Relayed Message MUST include option 7.
  Relayed Message option 7 MUST contain value 33.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include IA-NA.
  Client adds saved options. And DONT Erase.
  Client does include client-id.
  Client requests option 7.
  Client sends REQUEST message.

  RelayAgent sets ifaceid value to interface-abc.
  RelayAgent does include interface-id.
  RelayAgent sets linkaddr value to 2001:db8::abcd.
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
  Relayed Message MUST include option 7.
  Relayed Message option 7 MUST contain value 33.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 7.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-abc.
  RelayAgent does include interface-id.
  RelayAgent sets linkaddr value to 2001:db8::abcd.
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
  Relayed Message MUST include option 7.
  Relayed Message option 7 MUST contain value 44.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client does include IA-NA.
  Client adds saved options. And DONT Erase.
  Client does include client-id.
  Client requests option 7.
  Client sends REQUEST message.

  RelayAgent sets ifaceid value to interface-abc.
  RelayAgent does include interface-id.
  RelayAgent sets linkaddr value to 2001:db8::abcd.
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
  Relayed Message MUST include option 7.
  Relayed Message option 7 MUST contain value 44.

@v6 @sharednetworks @sharedsubnets @kea_only
Scenario: v6.sharednetworks.single-shared-subnet-with-two-subnets-based-on-relay-address
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Server is configured with another subnet: 2001:db8:b::/64 with 2001:db8:b::1-2001:db8:b::1 pool.
  Server is configured with preference option in subnet 0 with value 123.
  Server is configured with dns-servers option in subnet 1 with value 2001:db8::1,2001:db8::2.
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter relay with value {"ip-address":"2001:db8::abcd"} to shared-subnet 0 configuration.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.

  Test Procedure:
  Client saves server-id option from received message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  # there is no local subnet!

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-abc.
  RelayAgent does include interface-id.
  RelayAgent sets linkaddr value to 2001:db8::abcd.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include IA-NA.
  Client adds saved options. And DONT Erase.
  Client does include client-id.
  Client sends REQUEST message.

  RelayAgent sets ifaceid value to interface-abc.
  RelayAgent does include interface-id.
  RelayAgent sets linkaddr value to 2001:db8::abcd.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-abc.
  RelayAgent does include interface-id.
  RelayAgent sets linkaddr value to 2001:db8::abcd.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client does include IA-NA.
  Client adds saved options. And DONT Erase.
  Client does include client-id.
  Client sends REQUEST message.

  RelayAgent sets ifaceid value to interface-abc.
  RelayAgent does include interface-id.
  RelayAgent sets linkaddr value to 2001:db8::abcd.
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

  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8:a::1,00:03:00:01:f6:f5:f4:f3:f2:01
  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8:b::1,00:03:00:01:f6:f5:f4:f3:f2:02

@v6 @sharednetworks @sharedsubnets @kea_only
  Scenario: v6.sharednetworks.three-shared-subnet-with-two-subnets-based-on-id-and-iface-and-relay-address
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Server is configured with another subnet: 2001:db8:b::/64 with 2001:db8:b::1-2001:db8:b::1 pool.
  Server is configured with another subnet: 2001:db8:c::/64 with 2001:db8:c::1-2001:db8:c::1 pool.
  Server is configured with another subnet: 2001:db8:d::/64 with 2001:db8:d::1-2001:db8:d::1 pool.
  Server is configured with another subnet: 2001:db8:e::/64 with 2001:db8:e::1-2001:db8:e::1 pool.
  Server is configured with another subnet: 2001:db8:f::/64 with 2001:db8:f::1-2001:db8:f::1 pool.
  Server is configured with dns-servers option in subnet 1 with value 2001:db8::1,2001:db8::2.
  #first shared subnet
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface-id with value "interface-abc" to shared-subnet 0 configuration.
  #second shared-subnet
  Add subnet 2 to shared-subnet set 1.
  Add subnet 3 to shared-subnet set 1.
  Add configuration parameter name with value "name-xyz" to shared-subnet 1 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 1 configuration.
  Add subnet 4 to shared-subnet set 2.
  Add subnet 5 to shared-subnet set 2.
  Add configuration parameter name with value "name-something" to shared-subnet 2 configuration.
  Add configuration parameter relay with value {"ip-address":"2001:db8::1234"} to shared-subnet 2 configuration.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.

  Test Procedure:
  Client saves server-id option from received message.
  Response MUST include option 1.
  Response MUST include option 2.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-abcde.
  RelayAgent does include interface-id.
  RelayAgent sets linkaddr value to 2001:db8::1234.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include IA-NA.
  Client adds saved options. And DONT Erase.
  Client does include client-id.
  Client sends REQUEST message.

  RelayAgent sets ifaceid value to interface-abcde.
  RelayAgent does include interface-id.
  RelayAgent sets linkaddr value to 2001:db8::1234.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-abcde.
  RelayAgent does include interface-id.
  RelayAgent sets linkaddr value to 2001:db8::1234.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client does include IA-NA.
  Client adds saved options. And DONT Erase.
  Client does include client-id.
  Client sends REQUEST message.

  RelayAgent sets ifaceid value to interface-abcde.
  RelayAgent does include interface-id.
  RelayAgent sets linkaddr value to 2001:db8::1234.
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

  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8:e::1,00:03:00:01:f6:f5:f4:f3:f2:01
  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8:f::1,00:03:00:01:f6:f5:f4:f3:f2:02

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-abc.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include IA-NA.
  Client adds saved options. And DONT Erase.
  Client does include client-id.
  Client sends REQUEST message.

  RelayAgent sets ifaceid value to interface-abc.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-abc.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client does include IA-NA.
  Client adds saved options. And DONT Erase.
  Client does include client-id.
  Client sends REQUEST message.

  RelayAgent sets ifaceid value to interface-abc.
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

  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8:a::1,00:03:00:01:f6:f5:f4:f3:f2:01
  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8:b::1,00:03:00:01:f6:f5:f4:f3:f2:02

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
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
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  #Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
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
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8:c::1,00:03:00:01:f6:f5:f4:f3:f2:01
  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8:d::1,00:03:00:01:f6:f5:f4:f3:f2:02


@v6 @sharednetworks @sharedsubnets @kea_only
  Scenario: v6.sharednetworks.three-shared-subnet-with-two-subnets-options-override
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Server is configured with another subnet: 2001:db8:b::/64 with 2001:db8:b::1-2001:db8:b::1 pool.
  Server is configured with another subnet: 2001:db8:c::/64 with 2001:db8:c::1-2001:db8:c::1 pool.
  Server is configured with another subnet: 2001:db8:d::/64 with 2001:db8:d::1-2001:db8:d::1 pool.
  Server is configured with another subnet: 2001:db8:e::/64 with 2001:db8:e::1-2001:db8:e::1 pool.
  Server is configured with another subnet: 2001:db8:f::/64 with 2001:db8:f::1-2001:db8:f::1 pool.
  Server is configured with dns-servers option in subnet 1 with value 2001:db8::1,2001:db8::2.

  Server is configured with preference option with value 1.
  Server is configured with preference option in subnet 2 with value 33.
  Server is configured with preference option in subnet 3 with value 44.
  Server is configured with preference option in subnet 4 with value 55.
  Server is configured with preference option in subnet 5 with value 66.

  #first shared subnet
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface-id with value "interface-abc" to shared-subnet 0 configuration.
  #second shared-subnet
  Add subnet 2 to shared-subnet set 1.
  Add subnet 3 to shared-subnet set 1.
  Add configuration parameter name with value "name-xyz" to shared-subnet 1 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 1 configuration.
  Add subnet 4 to shared-subnet set 2.
  Add subnet 5 to shared-subnet set 2.
  Add configuration parameter name with value "name-something" to shared-subnet 2 configuration.
  Add configuration parameter relay with value {"ip-address":"2001:db8::1234"} to shared-subnet 2 configuration.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 7.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.

  Test Procedure:
  Client saves server-id option from received message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 7.
  Response option 7 MUST NOT contain value 11.
  Response option 7 MUST NOT contain value 1.
  Response option 7 MUST NOT contain value 55.
  Response option 7 MUST NOT contain value 66.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 7.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-abcde.
  RelayAgent does include interface-id.
  RelayAgent sets linkaddr value to 2001:db8::1234.
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
  Relayed Message MUST include option 7.
  Response option 7 MUST NOT contain value 11.
  Response option 7 MUST NOT contain value 1.
  Response option 7 MUST NOT contain value 33.
  Response option 7 MUST NOT contain value 44.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include IA-NA.
  Client adds saved options. And DONT Erase.
  Client does include client-id.
  Client requests option 7.
  Client sends REQUEST message.

  RelayAgent sets ifaceid value to interface-abcde.
  RelayAgent does include interface-id.
  RelayAgent sets linkaddr value to 2001:db8::1234.
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
  Relayed Message MUST include option 7.
  Response option 7 MUST NOT contain value 11.
  Response option 7 MUST NOT contain value 1.
  Response option 7 MUST NOT contain value 33.
  Response option 7 MUST NOT contain value 44.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 7.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-abcde.
  RelayAgent does include interface-id.
  RelayAgent sets linkaddr value to 2001:db8::1234.
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
  Relayed Message MUST include option 7.
  Response option 7 MUST NOT contain value 11.
  Response option 7 MUST NOT contain value 1.
  Response option 7 MUST NOT contain value 33.
  Response option 7 MUST NOT contain value 44.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client does include IA-NA.
  Client requests option 7.
  Client adds saved options. And DONT Erase.
  Client does include client-id.
  Client sends REQUEST message.

  RelayAgent sets ifaceid value to interface-abcde.
  RelayAgent does include interface-id.
  RelayAgent sets linkaddr value to 2001:db8::1234.
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
  Relayed Message MUST include option 7.
  Response option 7 MUST NOT contain value 11.
  Response option 7 MUST NOT contain value 1.
  Response option 7 MUST NOT contain value 33.
  Response option 7 MUST NOT contain value 44.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 7.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-abc.
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
  Relayed Message MUST include option 7.
  Response option 7 MUST NOT contain value 11.
  Response option 7 MUST NOT contain value 55.
  Response option 7 MUST NOT contain value 66.
  Response option 7 MUST NOT contain value 33.
  Response option 7 MUST NOT contain value 44.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include IA-NA.
  Client adds saved options. And DONT Erase.
  Client does include client-id.
  Client requests option 7.
  Client sends REQUEST message.

  RelayAgent sets ifaceid value to interface-abc.
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
  Relayed Message MUST include option 7.
  Response option 7 MUST NOT contain value 11.
  Response option 7 MUST NOT contain value 55.
  Response option 7 MUST NOT contain value 66.
  Response option 7 MUST NOT contain value 33.
  Response option 7 MUST NOT contain value 44.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 7.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-abc.
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
  Relayed Message MUST include option 7.
  Response option 7 MUST NOT contain value 11.
  Response option 7 MUST NOT contain value 55.
  Response option 7 MUST NOT contain value 66.
  Response option 7 MUST NOT contain value 33.
  Response option 7 MUST NOT contain value 44.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client does include IA-NA.
  Client adds saved options. And DONT Erase.
  Client does include client-id.
  Client requests option 7.
  Client sends REQUEST message.

  RelayAgent sets ifaceid value to interface-abc.
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

  Relayed Message MUST include option 7.
  Response option 7 MUST NOT contain value 11.
  Response option 7 MUST NOT contain value 55.
  Response option 7 MUST NOT contain value 66.
  Response option 7 MUST NOT contain value 33.
  Response option 7 MUST NOT contain value 44.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 7.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response MUST include option 7.
  Response option 7 MUST NOT contain value 1.
  Response option 7 MUST NOT contain value 55.
  Response option 7 MUST NOT contain value 66.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client requests option 7.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response MUST include option 7.
  Response option 7 MUST NOT contain value 1.
  Response option 7 MUST NOT contain value 55.
  Response option 7 MUST NOT contain value 66.
  #Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 7.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response MUST include option 7.
  Response option 7 MUST NOT contain value 1.
  Response option 7 MUST NOT contain value 55.
  Response option 7 MUST NOT contain value 66.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client requests option 7.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response MUST include option 7.
  Response option 7 MUST NOT contain value 1.
  Response option 7 MUST NOT contain value 55.
  Response option 7 MUST NOT contain value 66.

@v6 @sharednetworks @sharedsubnets @kea_only
Scenario: v6.sharednetworks.two-shared-subnet-with-two-subnets-based-on-relay-address
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Server is configured with another subnet: 2001:db8:b::/64 with 2001:db8:b::1-2001:db8:b::1 pool.
  Server is configured with another subnet: 2001:db8:c::/64 with 2001:db8:c::1-2001:db8:c::1 pool.
  Server is configured with another subnet: 2001:db8:d::/64 with 2001:db8:d::1-2001:db8:d::1 pool.
  Server is configured with preference option in subnet 0 with value 123.
  Server is configured with dns-servers option in subnet 1 with value 2001:db8::1,2001:db8::2.
  #first shared subnet
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter relay with value {"ip-address":"2001:db8::abcd"} to shared-subnet 0 configuration.
  #second shared-subnet
  Add subnet 2 to shared-subnet set 1.
  Add subnet 3 to shared-subnet set 1.
  Add configuration parameter name with value "name-xyz" to shared-subnet 1 configuration.
  Add configuration parameter relay with value {"ip-address":"2001:db8::1234"} to shared-subnet 1 configuration.

  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.

  Test Procedure:
  Client saves server-id option from received message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  # there is no local subnet!

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-abc.
  RelayAgent does include interface-id.
  RelayAgent sets linkaddr value to 2001:db8::abcd.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include IA-NA.
  Client adds saved options. And DONT Erase.
  Client does include client-id.
  Client sends REQUEST message.

  RelayAgent sets ifaceid value to interface-abc.
  RelayAgent does include interface-id.
  RelayAgent sets linkaddr value to 2001:db8::abcd.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-abc.
  RelayAgent does include interface-id.
  RelayAgent sets linkaddr value to 2001:db8::abcd.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client does include IA-NA.
  Client adds saved options. And DONT Erase.
  Client does include client-id.
  Client sends REQUEST message.

  RelayAgent sets ifaceid value to interface-abc.
  RelayAgent does include interface-id.
  RelayAgent sets linkaddr value to 2001:db8::abcd.
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

  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8:a::1,00:03:00:01:f6:f5:f4:f3:f2:01
  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8:b::1,00:03:00:01:f6:f5:f4:f3:f2:02

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-xyz.
  RelayAgent does include interface-id.
  RelayAgent sets linkaddr value to 2001:db8::1234.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include IA-NA.
  Client adds saved options. And DONT Erase.
  Client does include client-id.
  Client sends REQUEST message.

  RelayAgent sets ifaceid value to interface-xyz.
  RelayAgent does include interface-id.
  RelayAgent sets linkaddr value to 2001:db8::1234.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-xyz.
  RelayAgent does include interface-id.
  RelayAgent sets linkaddr value to 2001:db8::1234.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client does include IA-NA.
  Client adds saved options. And DONT Erase.
  Client does include client-id.
  Client sends REQUEST message.

  RelayAgent sets ifaceid value to interface-xyz.
  RelayAgent does include interface-id.
  RelayAgent sets linkaddr value to 2001:db8::1234.
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

  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8:c::1,00:03:00:01:f6:f5:f4:f3:f2:01
  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8:d::1,00:03:00:01:f6:f5:f4:f3:f2:02

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:03.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-xyz.
  RelayAgent does include interface-id.
  RelayAgent sets linkaddr value to 2001:db8::1234.
  RelayAgent forwards message encapsulated in 1 level.

  Pass Criteria:
  Server MUST respond with RELAYREPLY message.
  Response MUST include option 18.
  Response MUST include option 9.
  Response option 9 MUST contain Relayed Message.
  Relayed Message MUST include option 1.
  Relayed Message MUST include option 2.
  Relayed Message MUST include option 3.
  Relayed Message option 3 MUST contain sub-option 13.
  # no available addresses

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:03.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-abc.
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
  Relayed Message option 3 MUST contain sub-option 13.
  # no available addresses

@v6 @sharednetworks @sharedsubnets @kea_only
  Scenario: v6.sharednetworks.two-shared-subnet-with-two-subnets-based-on-id
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Server is configured with another subnet: 2001:db8:b::/64 with 2001:db8:b::1-2001:db8:b::1 pool.
  Server is configured with another subnet: 2001:db8:c::/64 with 2001:db8:c::1-2001:db8:c::1 pool.
  Server is configured with another subnet: 2001:db8:d::/64 with 2001:db8:d::1-2001:db8:d::1 pool.
  Server is configured with preference option in subnet 0 with value 123.
  Server is configured with dns-servers option in subnet 1 with value 2001:db8::1,2001:db8::2.
  #first shared subnet
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface-id with value "interface-abc" to shared-subnet 0 configuration.
  #second shared-subnet
  Add subnet 2 to shared-subnet set 1.
  Add subnet 3 to shared-subnet set 1.
  Add configuration parameter name with value "name-xyz" to shared-subnet 1 configuration.
  Add configuration parameter interface-id with value "interface-xyz" to shared-subnet 1 configuration.

  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.

  Test Procedure:
  Client saves server-id option from received message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  # there is no local subnet!

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-abc.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include IA-NA.
  Client adds saved options. And DONT Erase.
  Client does include client-id.
  Client sends REQUEST message.

  RelayAgent sets ifaceid value to interface-abc.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-abc.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client does include IA-NA.
  Client adds saved options. And DONT Erase.
  Client does include client-id.
  Client sends REQUEST message.

  RelayAgent sets ifaceid value to interface-abc.
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

  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8:a::1,00:03:00:01:f6:f5:f4:f3:f2:01
  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8:b::1,00:03:00:01:f6:f5:f4:f3:f2:02

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-xyz.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include IA-NA.
  Client adds saved options. And DONT Erase.
  Client does include client-id.
  Client sends REQUEST message.

  RelayAgent sets ifaceid value to interface-xyz.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-xyz.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client does include IA-NA.
  Client adds saved options. And DONT Erase.
  Client does include client-id.
  Client sends REQUEST message.

  RelayAgent sets ifaceid value to interface-xyz.
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

  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8:c::1,00:03:00:01:f6:f5:f4:f3:f2:01
  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8:d::1,00:03:00:01:f6:f5:f4:f3:f2:02

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:03.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-xyz.
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
  Relayed Message option 3 MUST contain sub-option 13.
  # no available addresses

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:03.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-abc.
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
  Relayed Message option 3 MUST contain sub-option 13.
  # no available addresses

@v6 @sharednetworks @sharedsubnets @kea_only
  Scenario: v6.sharednetworks.single-shared-subnet-with-three-subnets-classification
#  Test Setup:
#  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
#  Server is configured with another subnet: 2001:db8:b::/64 with 2001:db8:b::1-2001:db8:b::1 pool.
#  Server is configured with another subnet: 2001:db8:c::/64 with 2001:db8:c::1-2001:db8:c::1 pool.
#  Server is configured with dns-servers option in subnet 0 with value 2001:db8::1.
#  Server is configured with dns-servers option in subnet 1 with value 2001:db8::2.
#  Server is configured with dns-servers option in subnet 2 with value 2001:db8::3.
#
#  Add subnet 0 to shared-subnet set 0.
#  Add subnet 1 to shared-subnet set 0.
#  Add subnet 2 to shared-subnet set 0.
#  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
#  Add configuration parameter interface-id with value "interface-abc" to shared-subnet 0 configuration.
#
#  Send server configuration using SSH and config-file.
#
#  DHCP server is started.

  Test Setup:
  Client sends local file stored in: features/dhcpv6/server/kea_only/shared-configs/shared-networks-class-1.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/kea.conf.
  Client sends local file stored in: features/dhcpv6/server/kea_only/shared-configs/ctrl.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/keactrl.conf.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:f1.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 23.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:b::1.
  Response MUST include option 23.
  Response option 23 MUST contain addresses 2001:db8::666.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:f1.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client requests option 23.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:b::1.
  Response MUST include option 23.
  Response option 23 MUST contain addresses 2001:db8::666.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:f2.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 23.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:c::1.
  Response MUST include option 23.
  Response option 23 MUST contain addresses 2001:db8::1.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:f2.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client requests option 23.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:c::1.
  Response MUST include option 23.
  Response option 23 MUST contain addresses 2001:db8::1.

  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8:b::1,00:03:00:01:f6:f5:f4:f3:f2:f1
  File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8:c::1,00:03:00:01:f6:f5:f4:f3:f2:f2
  
@v6 @sharednetworks @sharedsubnets @kea_only
  Scenario: v6.sharednetworks.host.reservation.duplicate-reservation
  Test Setup:
  Server is configured with 3000::/30 subnet with 3000::1-3000::10 pool.
  Server is configured with another subnet: 2001:db8:d::/64 with 2001:db8:d::1-2001:db8:d::1 pool.
  Reserve address 3000::1 in subnet 0 for host uniquely identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
  Reserve address 3000::2 in subnet 0 for host uniquely identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Send server configuration using SSH and config-file.
  DHCP server failed to start. During configuration process.

@v6 @sharednetworks @sharedsubnets
  Scenario: v6.sharednetworks.host.reservation.all-values-duid
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Server is configured with another subnet: 3000::/64 with 3000::1-3000::ff pool.
  Server is configured with another subnet: 2001:db8:d::/64 with 2001:db8:d::1-2001:db8:d::1 pool.
  Reserve hostname reserved-hostname in subnet 0 for host uniquely identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
  For host reservation entry no. 0 in subnet 0 add address with value 3000::100.
  For host reservation entry no. 0 in subnet 0 add prefix with value 3001::/40.
  DDNS server is configured on 127.0.0.1 address and 53001 port.
  DDNS server is configured with enable-updates option set to true.
  DDNS server is configured with qualifying-suffix option set to my.domain.com.
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add subnet 2 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 0 configuration.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include IA-PD.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.

  Test Procedure:
  Client copies server-id option from received message.
  Client copies IA_NA option from received message.
  Client copies IA_PD option from received message.
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client sets FQDN_domain_name value to some-different-name.
  Client sets FQDN_flags value to S.
  Client does include fqdn.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::100.
  Response MUST include option 25.
  Response option 25 MUST contain sub-option 26.
  Response sub-option 26 from option 25 MUST contain prefix 3001::.
  Response MUST include option 39.
  Response option 39 MUST contain fqdn reserved-hostname.my.domain.com.
