Feature: Host Reservation DHCPv6
    Tests for Host Reservation feature based on MAC address.

@v6 @host_reservation @kea_only
    Scenario: v6.host.reservation.mac.requesting-reserved-address-inside-the-pool
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Reserve address 3000::10 in subnet 0 for host uniquely identified by f6:f5:f4:f3:f2:01.
	DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.


	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response option 3 MUST contain sub-option 5.
	Response sub-option 5 from option 3 MUST NOT contain address 3000::10.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
    Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	Response sub-option 5 from option 3 MUST contain address 3000::10.


@v6 @host_reservation @kea_only
    Scenario: v6.host.reservation.mac.requesting-reserved-address-outside-the-pool
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::10 pool.
	Reserve address 3000::ff in subnet 0 for host uniquely identified by f6:f5:f4:f3:f2:01.
	DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response option 3 MUST contain sub-option 5.
	Response sub-option 5 from option 3 MUST NOT contain address 3000::ff.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	Response sub-option 5 from option 3 MUST contain address 3000::ff.


@v6 @host_reservation @kea_only
    Scenario: v6.host.reservation.mac.requesting-reserved-prefix
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::10 pool.
	Reserve prefix 3000::/90 in subnet 0 for host uniquely identified by f6:f5:f4:f3:f2:01.
	DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
	Client does include IA-PD.
	Client does include client-id.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client does include IA-PD.
	Client copies server-id option from received message.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 13.
	Response sub-option 13 from option 25 MUST contain statuscode 6.
	Response MUST NOT include option 3.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client does include IA-PD.
	Client copies server-id option from received message.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response sub-option 26 from option 25 MUST contain prefix 3000::.
	Response MUST NOT include option 3.


@v6 @host_reservation @kea_only
    Scenario: v6.host.reservation.mac.requesting-reserved-prefix-PD-not-requested
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::10 pool.
	Reserve prefix 3000::/90 in subnet 0 for host uniquely identified by f6:f5:f4:f3:f2:01.
	DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
	Client does include IA-PD.
	Client does include client-id.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client does include IA-PD.
	Client copies server-id option from received message.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 13.
	Response sub-option 13 from option 25 MUST contain statuscode 6.
	Response MUST NOT include option 3.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST NOT include option 25.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

@v6 @host_reservation @kea_only
    Scenario: v6.host.reservation.mac.requesting-reserved-prefix-outside
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::10 pool.
	Reserve prefix 3011::/90 in subnet 0 for host uniquely identified by f6:f5:f4:f3:f2:01.
	DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
	Client does include IA-PD.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client does include IA-PD.
	Client copies server-id option from received message.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 13.
	Response sub-option 13 from option 25 MUST contain statuscode 6.
	Response MUST NOT include option 3.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client does include IA-PD.
	Client copies server-id option from received message.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response sub-option 26 from option 25 MUST contain prefix 3011::.
	Response MUST NOT include option 3.


@v6 @host_reservation @kea_only
    Scenario: v6.host.reservation.mac.requesting-reserved-prefix-inside-empty-pool
	Test Setup:
	Server is configured with 3000::/30 subnet with 3000::1-3000::10 pool.
	Server is configured with 2001:db8:1:: prefix in subnet 0 with 32 prefix length and 33 delegated prefix length.
	Reserve prefix 2001:db8:1:0:4000::/34 in subnet 0 for host uniquely identified by f6:f5:f4:f3:f2:01.
	DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
	Client does include IA-PD.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client does include IA-PD.
	Client copies server-id option from received message.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
	Client does include client-id.
    Client does include IA-NA.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response sub-option 26 from option 25 MUST NOT contain prefix 2001:db8:1:0:4000::.
	Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:22.
	Client does include IA-PD.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client does include IA-PD.
	Client copies server-id option from received message.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:22.
	Client does include client-id.
    Client does include IA-NA.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response sub-option 26 from option 25 MUST NOT contain prefix 2001:db8:1:0:4000::.
	Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:33.
	Client does include IA-PD.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client does include IA-PD.
    Client does include IA-NA.
	Client copies server-id option from received message.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:33.
	Client does include client-id.
    Client sends REQUEST message.


	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 13.
	Response sub-option 13 from option 25 MUST contain statuscode 6.
	Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client does include IA-PD.
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response sub-option 26 from option 25 MUST contain prefix 2001:db8:1:0:4000::.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.