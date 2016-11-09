Feature: DHCPv6 Stateless clients


@v6 @stateless
  Scenario: v6.stateless.with-subnet-empty-pool

  Test Setup:
  Server is configured with 3000::/64 subnet with $(EMPTY) pool.
  Server is configured with preference option with value 123.
  Server is configured with domain-search option with value domain1.example.com,domain2.isc.org.
  Server is configured with nis-servers option with value 2001:db8::abc,3000::1,2000::1234.
  DHCP server is started.

  Test Procedure:
  Client requests option 27.
  Client requests option 24.
  Client requests option 7.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 27.
  Response option 27 MUST contain addresses 2001:db8::abc,3000::1,2000::1234.
  Response MUST include option 24.
  Response option 24 MUST contain domains domain1.example.com,domain2.isc.org.
  Response MUST include option 7.
  Response option 7 MUST contain prefval 123.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

@v6 @stateless
  Scenario: v6.stateless.with-subnet-empty-pool-inforequest

  Test Setup:
  Server is configured with 3000::/64 subnet with $(EMPTY) pool.
  Server is configured with preference option with value 123.
  Server is configured with domain-search option with value domain1.example.com,domain2.isc.org.
  Server is configured with nis-servers option with value 2001:db8::abc,3000::1,2000::1234.
  DHCP server is started.

  Test Procedure:
  Client requests option 27.
  Client requests option 24.
  Client requests option 7.
  Client does include client-id.
  Client sends INFOREQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 27.
  Response option 27 MUST contain addresses 2001:db8::abc,3000::1,2000::1234.
  Response MUST include option 24.
  Response option 24 MUST contain domains domain1.example.com,domain2.isc.org.
  Response MUST include option 7.
  Response option 7 MUST contain prefval 123.


@v6 @stateless
  Scenario: v6.stateless.without-subnet

  Test Setup:
  Server is configured with $(EMPTY) subnet with $(EMPTY) pool.
  Server is configured with preference option with value 123.
  Server is configured with domain-search option with value domain1.example.com,domain2.isc.org.
  Server is configured with nis-servers option with value 2001:db8::abc,3000::1,2000::1234.
  DHCP server is started.

  Test Procedure:
  Client requests option 27.
  Client requests option 24.
  Client requests option 7.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 27.
  Response option 27 MUST contain addresses 2001:db8::abc,3000::1,2000::1234.
  Response MUST include option 24.
  Response option 24 MUST contain domains domain1.example.com,domain2.isc.org.
  Response MUST include option 7.
  Response option 7 MUST contain prefval 123.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

@v6 @stateless
  Scenario: v6.stateless.without-subnet-inforequest

  Test Setup:
  Server is configured with $(EMPTY) subnet with $(EMPTY) pool.
  Server is configured with preference option with value 123.
  Server is configured with domain-search option with value domain1.example.com,domain2.isc.org.
  Server is configured with nis-servers option with value 2001:db8::abc,3000::1,2000::1234.
  DHCP server is started.

  Test Procedure:
  Client requests option 27.
  Client requests option 24.
  Client requests option 7.
  Client does include client-id.
  Client sends INFOREQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 27.
  Response option 27 MUST contain addresses 2001:db8::abc,3000::1,2000::1234.
  Response MUST include option 24.
  Response option 24 MUST contain domains domain1.example.com,domain2.isc.org.
  Response MUST include option 7.
  Response option 7 MUST contain prefval 123.