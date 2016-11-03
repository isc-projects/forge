Feature: Host Reservation including options DHCPv6 stored in MySQL database
    Tests for Host Reservation feature for: prefixes, addresses and hostnames based on MAC and DUID.
    Host reservation records are stored in the MySQL database.



@v6 @host_reservation @kea_only
Scenario: v6.host.reservation.mysql.duid-ll-matching-option
    Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Create new MySQL reservation identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
    Add dhcp6_subnet_id 1 to MySQL reservation record id 1.
    Add IPv6 address reservation 3000::100 with iaid $(EMPTY) to MySQL record id 1.
    Add option reservation code 7 value 10 space dhcp6 persistent 1 client class $(EMPTY) subnet id 1 and scope subnet to MySQL record id 1.
    Upload hosts reservation to MySQL database.

    #Server is configured with preference option with value 12.
    Server is configured with preference option in subnet 0 with value 123.

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


@v6 @host_reservation @kea_only @marcin
Scenario: v6.host.reservation.mysql.duid-ll-not-matching
    Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Create new MySQL reservation identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
    Add dhcp6_subnet_id 1 to MySQL reservation record id 1.
    Add IPv6 address reservation 3000::100 with iaid $(EMPTY) to MySQL record id 1.
    Upload hosts reservation to MySQL database.
    DHCP server is started.

    Test Procedure:
    Client sets DUID value to 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01.
    Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    #Response MUST include option 3.
    #Response option 3 MUST contain sub-option 5.
    #Response sub-option 5 from option 3 MUST NOT contain address 3000::100.


    Test Procedure:
    Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:11.
    Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    #Response MUST include option 3.
    #Response option 3 MUST contain sub-option 5.
    #Response sub-option 5 from option 3 MUST NOT contain address 3000::100.

@v6 @host_reservation @kea_only @marcin
Scenario: v6.host.reservation.mysql.duid-llt-matching
    Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Create new MySQL reservation identified by duid 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01.
    #Create new MySQL reservation identified by hw-address f6:f5:f4:f3:f2:01.
    Add dhcp6_subnet_id 1 to MySQL reservation record id 1.
    Add IPv6 address reservation 3000::100 with iaid $(EMPTY) to MySQL record id 1.
    Upload hosts reservation to MySQL database.

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


@v6 @host_reservation @kea_only @marcin
Scenario: v6.host.reservation.mysql.duid-llt-not-matching
    Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Create new MySQL reservation identified by duid 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01.
    #Create new MySQL reservation identified by hw-address f6:f5:f4:f3:f2:01.
    Add dhcp6_subnet_id 1 to MySQL reservation record id 1.
    Add IPv6 address reservation 3000::100 with iaid $(EMPTY) to MySQL record id 1.
    Upload hosts reservation to MySQL database.

    DHCP server is started.


    Test Procedure:
    Client sets DUID value to 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:11.
    Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    #Response MUST include option 3.
    #Response option 3 MUST contain sub-option 5.
    #Response sub-option 5 from option 3 MUST NOT contain address 3000::100.


    Test Procedure:
    Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:11.
    Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    #Response MUST include option 3.
    #Response option 3 MUST contain sub-option 5.
    #Response sub-option 5 from option 3 MUST NOT contain address 3000::100.

@v6 @host_reservation @kea_only @marcin
Scenario: v6.host.reservation.mysql.hwaddrr-not-matching
    Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Use MySQL reservation system.
    Create new MySQL reservation identified by hw-address f6:f5:f4:f3:f2:01.
    Add dhcp6_subnet_id 1 to MySQL reservation record id 1.
    Add IPv6 address reservation 3000::100 with iaid $(EMPTY) to MySQL record id 1.
    Upload hosts reservation to MySQL database.

    DHCP server is started.


    Test Procedure:
    Client sets DUID value to 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:11.
    Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    #Response MUST include option 3.
    #Response option 3 MUST contain sub-option 5.
    #Response sub-option 5 from option 3 MUST NOT contain address 3000::100.


    Test Procedure:
    Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:11.
    Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    #Response MUST include option 3.
    #Response option 3 MUST contain sub-option 5.
    #Response sub-option 5 from option 3 MUST NOT contain address 3000::100.


@v6 @host_reservation @kea_only @marcin
Scenario: v6.host.reservation.mysql.hwaddrr-matching
    Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Use MySQL reservation system.
    Create new MySQL reservation identified by hw-address f6:f5:f4:f3:f2:01.
    Add dhcp6_subnet_id 1 to MySQL reservation record id 1.
    Add IPv6 address reservation 3000::100 with iaid $(EMPTY) to MySQL record id 1.
    Upload hosts reservation to MySQL database.

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





























@v6 @host_reservation @kea_only
Scenario: v6.host.reservation.pgsql.duid-ll-matching
    Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Create new PostgreSQL reservation identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
    Add dhcp6_subnet_id 1 to PostgreSQL reservation record id 1.
    Add IPv6 address reservation 3000::100 with iaid $(EMPTY) to PostgreSQL record id 1.
    Upload hosts reservation to PostgreSQL database.
    DHCP server is started.

    Test Procedure:
    Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
    Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.
    Pause the Test.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::100.









@v6 @host_reservation @kea_only @marcin
Scenario: v6.host.reservation.pgsql.hwaddrr-not-matching
    Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Use PostgreSQL reservation system.
    Create new PostgreSQL reservation identified by hw-address f6:f5:f4:f3:f2:01.
    Add dhcp6_subnet_id 1 to PostgreSQL reservation record id 1.
    Add IPv6 address reservation 3000::100 with iaid $(EMPTY) to MySQL record id 1.
    Upload hosts reservation to PostgreSQL database.

    DHCP server is started.


    Test Procedure:
    Client sets DUID value to 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:11.
    Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    #Response MUST include option 3.
    #Response option 3 MUST contain sub-option 5.
    #Response sub-option 5 from option 3 MUST NOT contain address 3000::100.


    Test Procedure:
    Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:11.
    Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    #Response MUST include option 3.
    #Response option 3 MUST contain sub-option 5.
    #Response sub-option 5 from option 3 MUST NOT contain address 3000::100.

@v6 @host_reservation @kea_only @marcin
Scenario: v6.host.reservation.pgsql.hwaddrr-matching
    Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Use PostgreSQL reservation system.
    Create new PostgreSQL reservation identified by hw-address f6:f5:f4:f3:f2:01.
    Add dhcp6_subnet_id 1 to PostgreSQL reservation record id 1.
    Add IPv6 address reservation 3000::100 with iaid $(EMPTY) to PostgreSQL record id 1.
    Upload hosts reservation to PostgreSQL database.

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
    #Response sub-option 5 from option 3 MUST contain address 3000::100.


    Test Procedure:
    Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
    Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    #Response sub-option 5 from option 3 MUST contain address 3000::100.

@v6 @host_reservation @kea_only @marcin
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
    #Server is configured with preference option in subnet 0 with value 123.
    DHCP server is started.

    #Pause the Test.

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
    Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
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
