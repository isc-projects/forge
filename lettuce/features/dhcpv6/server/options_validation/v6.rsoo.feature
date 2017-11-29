Feature: Relay-Supplied Options
  Tests for Relay-Supplied Options.

@v6 @dhcp6 @options @rsoo
Scenario: v6.options.rsoo-default-option

  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Add configuration parameter interface-id with value "abc" to subnet 0 configuration.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to abc.
  RelayAgent sets erpdomain value to relay-supplied.domain.com.
  Relay-Supplied-Option does include erp-local-domain-name.
  RelayAgent does include interface-id.
  RelayAgent does include rsoo.
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
  Relayed Message MUST include option 65.
  Relayed Message option 65 MUST contain erpdomain relay-supplied.domain.com.

  References: RFC6422

@v6 @dhcp6 @options @rsoo
Scenario: v6.options.rsoo-custom-option-list

  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Add configuration parameter interface-id with value "abc" to subnet 0 configuration.
  Add configuration parameter relay-supplied-options with value ["12"] to global configuration.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 12.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to abc.
  RelayAgent sets srvaddr value to 2000::1.
  Relay-Supplied-Option does include server-unicast.
  RelayAgent does include interface-id.
  RelayAgent does include rsoo.
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
  Relayed Message MUST include option 12.
  Relayed Message option 12 MUST contain srvaddr 2000::1.

  References: RFC6422

@v6 @dhcp6 @options @rsoo
Scenario: v6.options.rsoo-custom-option-list-default-option-65

  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Add configuration parameter interface-id with value "abc" to subnet 0 configuration.
  Add configuration parameter relay-supplied-options with value ["12"] to global configuration.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to abc.
  RelayAgent sets erpdomain value to relay-supplied.domain.com.
  Relay-Supplied-Option does include erp-local-domain-name.
  RelayAgent does include interface-id.
  RelayAgent does include rsoo.
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
  Relayed Message MUST include option 65.
  Relayed Message option 65 MUST contain erpdomain relay-supplied.domain.com.

  References: RFC6422

@v6 @dhcp6 @options @rsoo
Scenario: v6.options.rsoo-custom-option-list-server-has-option-configured-also

  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Add configuration parameter interface-id with value "abc" to subnet 0 configuration.
  Add configuration parameter relay-supplied-options with value ["12"] to global configuration.
  Server is configured with unicast option with value 3000::1.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 12.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to abc.
  RelayAgent sets srvaddr value to 2000::1.
  Relay-Supplied-Option does include server-unicast.
  RelayAgent does include interface-id.
  RelayAgent does include rsoo.
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
  Relayed Message MUST include option 12.
  Relayed Message option 12 MUST NOT contain srvaddr 2000::1.
  Relayed Message option 12 MUST contain srvaddr 3000::1.

  References: RFC6422