Feature: Host Reservation DHCPv6 stored in PostgreSQL database.
    Tests for Host Reservation feature for: prefixes, addresses and hostnames based on MAC and DUID.
    Host reservation records are stored in the PostgreSQL database.

@v6 @host_reservation @kea_only @pgsql
Scenario: v6.host.reservation.pgsql.all-values-mac

  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Use PostgreSQL reservation system.
  Create new PostgreSQL reservation identified by hw-address f6:f5:f4:f3:f2:01.
  Add hostname reserved-hostname to PostgreSQL reservation record id 1.
  Add dhcp6_subnet_id 1 to PostgreSQL reservation record id 1.
  Add IPv6 prefix reservation 3001:: 40 with iaid $(EMPTY) to PostgreSQL record id 1.
  Add IPv6 address reservation 3000::100 with iaid $(EMPTY) to PostgreSQL record id 1.
  Add IPv6 address reservation 3000::101 with iaid $(EMPTY) to PostgreSQL record id 1.
  Add option reservation code 32 value 10 space dhcp6 persistent 1 client class $(EMPTY) subnet id 1 and scope subnet to PostgreSQL record id 1.
  Upload hosts reservation to PostgreSQL database.
  DDNS server is configured on 127.0.0.1 address and 53001 port.
  DDNS server is configured with enable-updates option set to true.
  DDNS server is configured with qualifying-suffix option set to my.domain.com.
  Send server configuration using SSH and config-file.
DHCP server is started.

  Test Procedure:
  Client sets ia_id value to 666.
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include IA-PD.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  Test Procedure:
  Client copies server-id option from received message.
  Client copies IA_NA option from received message.
  Client copies IA_PD option from received message.
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client sets FQDN_domain_name value to some-different-name.
  Client sets FQDN_flags value to S.
  Client does include fqdn.
  Client requests option 32.
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

  Test Procedure:
  Client sets ia_id value to 777.
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include IA-PD.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  Test Procedure:
  Client copies server-id option from received message.
  Client copies IA_NA option from received message.
  Client copies IA_PD option from received message.
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client sets FQDN_domain_name value to some-different-name.
  Client sets FQDN_flags value to S.
  Client does include fqdn.
  Client requests option 32.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST NOT contain address 3000::100.

@v6 @host_reservation @kea_only @pgsql
Scenario: v6.host.reservation.pgsql.duid-ll-matching
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Use PostgreSQL reservation system.
  Create new PostgreSQL reservation identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
  Add dhcp6_subnet_id 1 to PostgreSQL reservation record id 1.
  Add IPv6 address reservation 3000::100 with iaid $(EMPTY) to PostgreSQL record id 1.
  Upload hosts reservation to PostgreSQL database.

  Send server configuration using SSH and config-file.
DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::100.

@v6 @host_reservation @kea_only @pgsql
Scenario: v6.host.reservation.pgsql.hwaddrr-not-matching
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Use PostgreSQL reservation system.
  Create new PostgreSQL reservation identified by hw-address f6:f5:f4:f3:f2:01.
  Add dhcp6_subnet_id 1 to PostgreSQL reservation record id 1.
  Add IPv6 address reservation 3000::100 with iaid $(EMPTY) to PostgreSQL record id 1.
  Upload hosts reservation to PostgreSQL database.

  Send server configuration using SSH and config-file.
DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST NOT contain address 3000::100.


  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST NOT contain address 3000::100.

@v6 @host_reservation @kea_only @pgsql
Scenario: v6.host.reservation.pgsql.hwaddrr-matching
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Use PostgreSQL reservation system.
  Create new PostgreSQL reservation identified by hw-address f6:f5:f4:f3:f2:01.
  Add dhcp6_subnet_id 1 to PostgreSQL reservation record id 1.
  Add IPv6 address reservation 3000::100 with iaid $(EMPTY) to PostgreSQL record id 1.
  Upload hosts reservation to PostgreSQL database.

  Send server configuration using SSH and config-file.
DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::100.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::100.

@v6 @host_reservation @kea_only @pgsql
Scenario: v6.host.reservation.pgsql.hwaddrr-matching-dual-backend
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Use PostgreSQL reservation system.
  Create new PostgreSQL reservation identified by hw-address f6:f5:f4:f3:f2:11.
  Add dhcp6_subnet_id 1 to PostgreSQL reservation record id 1.
  Add IPv6 address reservation 3000::100 with iaid $(EMPTY) to PostgreSQL record id 1.
  Upload hosts reservation to PostgreSQL database.

  Reserve address 3000::fff in subnet 0 for host uniquely identified by hw-address f6:f5:f4:f3:f2:22.
  Send server configuration using SSH and config-file.
DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::100.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:22.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::fff.