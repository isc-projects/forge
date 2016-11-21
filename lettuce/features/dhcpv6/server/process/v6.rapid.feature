Feature: DHCPv6 Rapid commit
    Those are tests for DHCPv6 release process.
    
@v6 @dhcp6 @rapid @kea_only
  Scenario: v6.rapid.commit.as-global-parameter
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Add configuration parameter rapid-commit with value True to global configuration.
  DHCP server failed to start. During configuration process.

@v6 @dhcp6 @rapid
  Scenario: v6.rapid.commit.basic-one-subnet
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Add configuration parameter rapid-commit with value True to subnet 0 configuration.
  DHCP server is started.

  Test Procedure:
  Client does include rapid-commit.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response MUST include option 14.
  References: RFC3315 section 17.2.1.

@v6 @dhcp6 @rapid
  Scenario: v6.rapid.commit.basic-one-subnet-rapid-not-included
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Add configuration parameter rapid-commit with value True to subnet 0 configuration.
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
  Response option 3 MUST contain sub-option 5.
  Response MUST NOT include option 14.

  Test Procedure:
  Client copies server-id option from received message.
  Client copies IA_NA option from received message.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response MUST NOT include option 14.

@v6 @dhcp6 @rapid
  Scenario: v6.rapid.commit.basic-two-subnets
  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::ff pool.
  Add configuration parameter rapid-commit with value True to subnet 0 configuration.
  Server is configured with another subnet: 2001:db8:2::/64 with 2001:db8:2::5-2001:db8:2::5 pool.
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
  Response option 3 MUST contain sub-option 5.
  Response MUST NOT include option 14.

  Test Procedure:
  Client copies server-id option from received message.
  Client copies IA_NA option from received message.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.
  Response MUST NOT include option 14.