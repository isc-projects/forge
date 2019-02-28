Feature: Host Reservation including options DHCPv6 stored in MySQL database
    Tests for Host Reservation feature for: prefixes, addresses and hostnames based on MAC and DUID.
    Host reservation records are stored in the MySQL database.

@v6 @host_reservation @kea_only @reserved_options
Scenario: v6.host.reservation.mysql.duid-ll-matching-option
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Use MySQL reservation system.
  Create new MySQL reservation identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
  Add dhcp6_subnet_id 1 to MySQL reservation record id 1.
  Add IPv6 address reservation 3000::100 with iaid $(EMPTY) to MySQL record id 1.
  Add option reservation code 7 value 10 space dhcp6 persistent 1 client class $(EMPTY) subnet id 1 and scope subnet to MySQL record id 1.
  Upload hosts reservation to MySQL database.

  Server is configured with preference option in subnet 0 with value 123.

  Send server configuration using SSH and config-file.
DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client requests option 7.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::100.
  Response MUST include option 7.
  Response option 7 MUST contain value 10.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:21.
  Client requests option 7.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response MUST include option 7.
  Response option 7 MUST contain value 123.

@v6 @host_reservation @kea_only @reserved_options
Scenario: v6.host.reservation.mysql.duid-ll-matching-option-no-address
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Use MySQL reservation system.
  Create new MySQL reservation identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
  Add dhcp6_subnet_id 1 to MySQL reservation record id 1.
  Add option reservation code 7 value 10 space dhcp6 persistent 1 client class $(EMPTY) subnet id 1 and scope subnet to MySQL record id 1.
  Upload hosts reservation to MySQL database.

  Server is configured with preference option in subnet 0 with value 123.

  Send server configuration using SSH and config-file.
DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client requests option 7.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST NOT contain address 3000::100.
  Response MUST include option 7.
  Response option 7 MUST contain value 10.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:21.
  Client requests option 7.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response MUST include option 7.
  Response option 7 MUST contain value 123.

@v6 @host_reservation @kea_only @reserved_options
Scenario: v6.host.reservation.mysql.duid-ll-matching-option-no-address
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Use MySQL reservation system.
  Create new MySQL reservation identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
  Add dhcp6_subnet_id 1 to MySQL reservation record id 1.
  Add option reservation code 7 value 10 space dhcp6 persistent 1 client class $(EMPTY) subnet id 1 and scope subnet to MySQL record id 1.
  Upload hosts reservation to MySQL database.

  Server is configured with preference option in subnet 0 with value 123.

  Send server configuration using SSH and config-file.
DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client requests option 7.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST NOT contain address 3000::100.
  Response MUST include option 7.
  Response option 7 MUST contain value 10.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client requests option 7.
  Client does include client-id.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST NOT include option 3.
  Response MUST include option 7.
  Response option 7 MUST contain value 10.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:21.
  Client requests option 7.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response MUST include option 7.
  Response option 7 MUST contain value 123.

@v6 @host_reservation @kea_only @reserved_options
Scenario: v6.host.reservation.mysql.duid-ll-matching-option-inforequest
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Use MySQL reservation system.
  Create new MySQL reservation identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
  Add dhcp6_subnet_id 1 to MySQL reservation record id 1.
  Add option reservation code 7 value 10 space dhcp6 persistent 1 client class $(EMPTY) subnet id 1 and scope subnet to MySQL record id 1.
  Upload hosts reservation to MySQL database.

  Server is configured with preference option in subnet 0 with value 123.

  Send server configuration using SSH and config-file.
DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client requests option 7.
  Client sends INFOREQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST NOT include option 3.
  Response MUST include option 7.
  Response option 7 MUST contain value 123.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client requests option 7.
  Client does include client-id.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST NOT include option 3.
  Response MUST include option 7.
  Response option 7 MUST contain value 10.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:21.
  Client requests option 7.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response MUST include option 7.
  Response option 7 MUST contain value 123.

@v6 @host_reservation @kea_only @reserved_options
Scenario: v6.host.reservation.mysql.option-multiple
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Use MySQL reservation system.
  Create new MySQL reservation identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
  Add dhcp6_subnet_id 1 to MySQL reservation record id 1.
  Add IPv6 address reservation 3000::100 with iaid $(EMPTY) to MySQL record id 1.
  Add option reservation code 7 value 10 space dhcp6 persistent 1 client class $(EMPTY) subnet id 1 and scope subnet to MySQL record id 1.
  Add option reservation code 21 value srv1.example.com,srv2.isc.org space dhcp6 persistent 1 client class $(EMPTY) subnet id 1 and scope subnet to MySQL record id 1.
  Add option reservation code 23 value 2001:db8::1,2001:db8::2 space dhcp6 persistent 1 client class $(EMPTY) subnet id 1 and scope subnet to MySQL record id 1.
  Add option reservation code 59 value http://www.kea-reserved.isc.org space dhcp6 persistent 1 client class $(EMPTY) subnet id 1 and scope subnet to MySQL record id 1.
  #Add option reservation code 60 value 10 space dhcp6 persistent 1 client class $(EMPTY) subnet id 1 and scope subnet to MySQL record id 1.

  Upload hosts reservation to MySQL database.

  Server is configured with preference option in subnet 0 with value 123.
  Server is configured with sip-server-dns option with value srv4.example.com,srv5.isc.org.
  #21
  Server is configured with dns-servers option with value 2001:db8::4,2001:db8::5.
  #23
  Server is configured with bootfile-url option with value http://www.kea.isc.org.
  #59
  Server is configured with bootfile-param option with value 000B48656C6C6F20776F726C640003666F6F.
  #60
  Server is configured with new-tzdb-timezone option with value Europe/Zurich.
  Send server configuration using SSH and config-file.
DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client requests option 7.
  Client requests option 21.
  Client requests option 23.
  Client requests option 42.
  Client requests option 59.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::100.
  Response MUST include option 7.
  Response option 7 MUST contain value 10.
  Response MUST include option 59.
  Response option 59 MUST contain optdata http://www.kea-reserved.isc.org.
  Response MUST include option 21.
  Response option 21 MUST contain address srv1.example.com,srv2.isc.org.
  Response MUST include option 23.
  Response option 23 MUST contain address 2001:db8::1,2001:db8::2.
  Response MUST include option 42.
  Response option 42 MUST contain optdata Europe/Zurich.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:21.
  Client requests option 7.
  Client requests option 21.
  Client requests option 42.
  Client requests option 23.
  Client requests option 59.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response MUST include option 7.
  Response option 7 MUST contain value 123.
  Response MUST include option 59.
  Response option 59 MUST contain optdata http://www.kea.isc.org.
  Response MUST include option 21.
  Response option 21 MUST contain address srv4.example.com,srv5.isc.org.
  Response MUST include option 23.
  Response option 23 MUST contain address 2001:db8::4,2001:db8::5.
  Response MUST include option 42.
  Response option 42 MUST contain optdata Europe/Zurich.

@v6 @host_reservation @kea_only @reserved_options
Scenario: v6.host.reservation.pgsql.hwaddrr-matching-option
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Use PostgreSQL reservation system.
  Create new PostgreSQL reservation identified by hw-address f6:f5:f4:f3:f2:01.
  Add dhcp6_subnet_id 1 to PostgreSQL reservation record id 1.
  Add IPv6 address reservation 3000::100 with iaid $(EMPTY) to PostgreSQL record id 1.
  Add option reservation code 7 value 10 space dhcp6 persistent 1 client class $(EMPTY) subnet id 1 and scope subnet to PostgreSQL record id 1.
  Upload hosts reservation to PostgreSQL database.

  Server is configured with preference option with value 12.
  Send server configuration using SSH and config-file.
DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01.
  Client requests option 7.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  #Response sub-option 5 from option 3 MUST contain address 3000::100.
  Response MUST include option 7.
  Response option 7 MUST contain value 10.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:22.
  Client requests option 7.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  #Response sub-option 5 from option 3 MUST contain address 3000::100.
  Response MUST include option 7.
  Response option 7 MUST contain value 12.

@v6 @host_reservation @kea_only @reserved_options
Scenario: v6.host.reservation.pgsql.hwaddrr-matching-option-no-address
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Use PostgreSQL reservation system.
  Create new PostgreSQL reservation identified by hw-address f6:f5:f4:f3:f2:01.
  Add dhcp6_subnet_id 1 to PostgreSQL reservation record id 1.
  Add option reservation code 7 value 10 space dhcp6 persistent 1 client class $(EMPTY) subnet id 1 and scope subnet to PostgreSQL record id 1.
  Upload hosts reservation to PostgreSQL database.

  Server is configured with preference option with value 12.
  Send server configuration using SSH and config-file.
DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01.
  Client requests option 7.
  Client does include client-id.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST NOT include option 3.
  Response MUST include option 7.
  Response option 7 MUST contain value 10.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:22.
  Client requests option 7.
  Client does include client-id.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST NOT include option 3.
  Response MUST include option 7.
  Response option 7 MUST contain value 12.

@v6 @host_reservation @kea_only @reserved_options
Scenario: v6.host.reservation.pgsql.hwaddrr-matching-option-inforequest
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Use PostgreSQL reservation system.
  Create new PostgreSQL reservation identified by hw-address f6:f5:f4:f3:f2:01.
  Add dhcp6_subnet_id 1 to PostgreSQL reservation record id 1.
  Add option reservation code 7 value 10 space dhcp6 persistent 1 client class $(EMPTY) subnet id 1 and scope subnet to PostgreSQL record id 1.
  Upload hosts reservation to PostgreSQL database.

  Server is configured with preference option with value 12.
  Send server configuration using SSH and config-file.
DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01.
  Client requests option 7.
  Client sends INFOREQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST NOT include option 3.
  Response MUST include option 7.
  Response option 7 MUST contain value 12.

  Test Procedure:
  Client sets DUID value to 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01.
  Client requests option 7.
  Client does include client-id.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST NOT include option 3.
  Response MUST include option 7.
  Response option 7 MUST contain value 10.

@v6 @host_reservation @kea_only @reserved_options
Scenario: v6.host.reservation.pgsql.option-multiple
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Use PostgreSQL reservation system.
  Create new PostgreSQL reservation identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
  Add dhcp6_subnet_id 1 to PostgreSQL reservation record id 1.
  Add IPv6 address reservation 3000::100 with iaid $(EMPTY) to PostgreSQL record id 1.
  Add option reservation code 7 value 10 space dhcp6 persistent 1 client class $(EMPTY) subnet id 1 and scope subnet to PostgreSQL record id 1.
  Add option reservation code 21 value srv1.example.com,srv2.isc.org space dhcp6 persistent 1 client class $(EMPTY) subnet id 1 and scope subnet to PostgreSQL record id 1.
  Add option reservation code 23 value 2001:db8::1,2001:db8::2 space dhcp6 persistent 1 client class $(EMPTY) subnet id 1 and scope subnet to PostgreSQL record id 1.
  Add option reservation code 59 value http://www.kea-reserved.isc.org space dhcp6 persistent 1 client class $(EMPTY) subnet id 1 and scope subnet to PostgreSQL record id 1.
  #Add option reservation code 60 value 10 space dhcp6 persistent 1 client class $(EMPTY) subnet id 1 and scope subnet to MySQL record id 1.

  Upload hosts reservation to PostgreSQL database.

  Server is configured with preference option in subnet 0 with value 123.
  Server is configured with sip-server-dns option with value srv4.example.com,srv5.isc.org.
  #21
  Server is configured with dns-servers option with value 2001:db8::4,2001:db8::5.
  #23
  Server is configured with bootfile-url option with value http://www.kea.isc.org.
  #59
  Server is configured with new-tzdb-timezone option with value Europe/Zurich.
  #60 and not reserved
  Send server configuration using SSH and config-file.
DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client requests option 7.
  Client requests option 21.
  Client requests option 23.
  Client requests option 42.
  Client requests option 59.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::100.
  Response MUST include option 7.
  Response option 7 MUST contain value 10.
  Response MUST include option 59.
  Response option 59 MUST contain optdata http://www.kea-reserved.isc.org.
  Response MUST include option 21.
  Response option 21 MUST contain address srv1.example.com,srv2.isc.org.
  Response MUST include option 23.
  Response option 23 MUST contain address 2001:db8::1,2001:db8::2.
  Response MUST include option 42.
  Response option 42 MUST contain optdata Europe/Zurich.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:21.
  Client requests option 7.
  Client requests option 21.
  Client requests option 23.
  Client requests option 59.
  Client requests option 42.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response MUST include option 7.
  Response option 7 MUST contain value 123.
  Response MUST include option 59.
  Response option 59 MUST contain optdata http://www.kea.isc.org.
  Response MUST include option 21.
  Response option 21 MUST contain address srv4.example.com,srv5.isc.org.
  Response MUST include option 23.
  Response option 23 MUST contain address 2001:db8::4,2001:db8::5.
  Response MUST include option 42.
  Response option 42 MUST contain optdata Europe/Zurich.