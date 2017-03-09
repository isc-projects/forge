Feature: DHCPv6 Relay Agent
  This feature will test ability to assign subnets to specific relay agents based on interface id values.

@v6 @dhcp6 @relay @kea_only
  Scenario: v6.relay.interface-local-and-relay-interface-in-the-same-subnet

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::10 pool.
  To subnet 0 configuration section in the config file add line: ,"relay": {"ip-address": "3000::1005"}
  To subnet 0 configuration section in the config file add line: ,"interface":"eth2"
  Add configuration parameter interface-id with value "abc" to subnet 0 configuration.
  Send server configuration using SSH and config-file.
DHCP server failed to start. During configuration process.

  References: Kea User's Guide Section: DHCPv6 Relays

@v6 @dhcp6 @relay @kea_only
  Scenario: v6.relay.interface-two-subnets

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::10 pool.
  Add configuration parameter interface-id with value "abc" to subnet 0 configuration.
  Server is configured with another subnet: 2001:db8:2::/64 with 2001:db8:2::1-2001:db8:2::10 pool.
  Add configuration parameter interface-id with value "xyz" to subnet 1 configuration.
  Send server configuration using SSH and config-file.
DHCP server is started.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to abc.
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
  Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:1::1.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to xyz.
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
  Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:2::1.

  References: Kea User's Guide Section: DHCPv6 Relays

@v6 @dhcp6 @relay @kea_only
  Scenario: v6.relay.relayaddress-two-subnets

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::10 pool.
  To subnet 0 configuration section in the config file add line: ,"relay": {"ip-address": "3000::1005"}
  Server is configured with another subnet: 2001:db8:2::/64 with 2001:db8:2::1-2001:db8:2::10 pool.
  To subnet 1 configuration section in the config file add line: ,"relay": {"ip-address": "3000::2005"}
  Add configuration parameter interface-id with value "xyz" to subnet 1 configuration.
  Send server configuration using SSH and config-file.
DHCP server is started.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets linkaddr value to 3000::1005.
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
  Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:1::1.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets linkaddr value to 3000::2005.
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
  Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:2::1.

  References: Kea User's Guide Section: DHCPv6 Relays

@v6 @dhcp6 @relay @kea_only @disabled
  # that is against the spec
  Scenario: v6.relay.relayaddress-interface-id-just-one-matching

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::10 pool.
  Add configuration parameter interface-id with value "xyz" to subnet 0 configuration.
  To subnet 0 configuration section in the config file add line: ,"relay": {"ip-address": "3000::1005"}
  Send server configuration using SSH and config-file.
DHCP server is started.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets linkaddr value to 3000::3005.
  RelayAgent sets ifaceid value to xyz.
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
  Relayed Message option 3 MUST NOT contain sub-option 5.
  Relayed Message option 3 MUST contain sub-option 13.
  Relayed Message sub-option 13 from option 3 MUST contain statuscode 2.

@v6 @dhcp6 @relay @kea_only @disabled
  # that is against the spec
  Scenario: v6.relay.relayaddress-interface-id-just-one-matching-2

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::10 pool.
  Add configuration parameter interface-id with value "xyz" to subnet 0 configuration.
  To subnet 0 configuration section in the config file add line: ,"relay": {"ip-address": "3000::1005"}
  Send server configuration using SSH and config-file.
DHCP server is started.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets linkaddr value to 3000::1005.
  RelayAgent sets ifaceid value to abc.
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
  Relayed Message option 3 MUST NOT contain sub-option 5.
  Relayed Message option 3 MUST contain sub-option 13.
  Relayed Message sub-option 13 from option 3 MUST contain statuscode 2.


@v6 @dhcp6 @relay @kea_only @disabled
  # that is against the spec
  Scenario: v6.relay.relayaddress-interface-id-just-one-matching-3

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::10 pool.
  Add configuration parameter interface-id with value "xyz" to subnet 0 configuration.
  To subnet 0 configuration section in the config file add line: ,"relay": {"ip-address": "3000::1005"}
  Send server configuration using SSH and config-file.
DHCP server is started.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets linkaddr value to 2001:db8:1::1000.
  RelayAgent sets ifaceid value to abc.
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
  Relayed Message option 3 MUST NOT contain sub-option 5.
  Relayed Message option 3 MUST contain sub-option 13.
  Relayed Message sub-option 13 from option 3 MUST contain statuscode 2.


@v6 @dhcp6 @relay @kea_only
  Scenario: v6.relay.relayaddress-interface-id-two-subnets

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::10 pool.
  Add configuration parameter interface-id with value "xyz" to subnet 0 configuration.
  To subnet 0 configuration section in the config file add line: ,"relay": {"ip-address": "3000::1005"}
  Server is configured with another subnet: 2001:db8:2::/64 with 2001:db8:2::1-2001:db8:2::10 pool.
  Add configuration parameter interface-id with value "abc" to subnet 1 configuration.
  To subnet 1 configuration section in the config file add line: ,"relay": {"ip-address": "3000::1005"}
  Send server configuration using SSH and config-file.
DHCP server is started.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets linkaddr value to 3000::1005.
  RelayAgent sets ifaceid value to xyz.
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
  Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:1::1.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets linkaddr value to 3000::1005.
  RelayAgent sets ifaceid value to abc.
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
  Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:2::1.

  References: Kea User's Guide Section: DHCPv6 Relays

@v6 @dhcp6 @relay @kea_only
  Scenario: v6.relay.relayaddress-interface-id-two-subnets-2

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::10 pool.
  Add configuration parameter interface-id with value "xyz" to subnet 0 configuration.
  To subnet 0 configuration section in the config file add line: ,"relay": {"ip-address": "3000::2005"}
  Server is configured with another subnet: 2001:db8:2::/64 with 2001:db8:2::1-2001:db8:2::10 pool.
  Add configuration parameter interface-id with value "abc" to subnet 1 configuration.
  To subnet 1 configuration section in the config file add line: ,"relay": {"ip-address": "3000::1005"}
  Send server configuration using SSH and config-file.
DHCP server is started.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets linkaddr value to 3000::2005.
  RelayAgent sets ifaceid value to xyz.
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
  Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:1::1.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets linkaddr value to 3000::1005.
  RelayAgent sets ifaceid value to abc.
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
  Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:2::1.

  References: Kea User's Guide Section: DHCPv6 Relays

@v6 @dhcp6 @relay @kea_only
  Scenario: v6.relay.relayaddress-not-matching

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::10 pool.
  To subnet 0 configuration section in the config file add line: ,"relay": {"ip-address": "3000::2005"}
  Send server configuration using SSH and config-file.
DHCP server is started.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets linkaddr value to 2001:db8:2::100.
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
  Relayed Message sub-option 13 from option 3 MUST contain statuscode 2.


@v6 @dhcp6 @relay @kea_only
  Scenario: v6.relay.relayaddress-within-subnet

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::10 pool.
  To subnet 0 configuration section in the config file add line: ,"relay": {"ip-address": "3000::2005"}
  Send server configuration using SSH and config-file.
DHCP server is started.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets linkaddr value to 2001:db8:1::100.
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
  Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:1::1.


@v6 @dhcp6 @relay @kea_only
  Scenario: v6.relay.interface-one-subnet-not-matching-id

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::10 pool.
  Add configuration parameter interface-id with value "xyz" to subnet 0 configuration.
  Send server configuration using SSH and config-file.
DHCP server is started.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to abc.
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
  Relayed Message sub-option 13 from option 3 MUST contain statuscode 2.

  References: Kea User's Guide Section: DHCPv6 Relays

@v6 @dhcp6 @relay @kea_only
  Scenario: v6.relay.interface-two-subnets-direct-client

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
  Add configuration parameter interface-id with value "abc" to subnet 0 configuration.
  Server is configured with another subnet: 2001:db8:2::/64 with 2001:db8:2::1-2001:db8:2::10 pool.
  Send server configuration using SSH and config-file.
DHCP server is started.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to xyz.
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
  Relayed Message sub-option 13 from option 3 MUST contain statuscode 2.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST NOT contain address 2001:db8:1::1.

  References: Kea User's Guide Section: DHCPv6 Relays

@v6 @dhcp6 @relay @kea_only
  Scenario: v6.relay.interface-two-subnets-same-interface-id

  Test Setup:
  #that is basically misconfiguration!
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
  Add configuration parameter interface-id with value "abc" to subnet 0 configuration.
  Server is configured with another subnet: 2001:db8:2::/64 with 2001:db8:2::11-2001:db8:2::20 pool.
  Add configuration parameter interface-id with value "abc" to subnet 1 configuration.
  Send server configuration using SSH and config-file.
DHCP server is started.

  ## just saving server-id - start
  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.

  Test Procedure:
  Client saves server-id option from received message.
  ## just saving server-id - end

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to abc.
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
  Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:1::1.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client sets IA_Address value to 2001:db8:1::1.
  Client does include IA_Address.
  Client does include IA-NA.
  Client adds saved options. And DONT Erase.
  Client does include client-id.
  Client sends REQUEST message.

  RelayAgent sets ifaceid value to abc.
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
  Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:1::1.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:33:22:01.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to abc.
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
  Relayed Message sub-option 13 from option 3 MUST contain statuscode 2.

  References: Kea User's Guide Section: DHCPv6 Relays
