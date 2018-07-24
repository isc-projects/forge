Feature: Host Reservation DHCPv6
    Tests for conflicts resolving in Host Reservation feature based both on MAC and DUID.
    For prefix, addresses and hostnames.

@v6 @host_reservation @kea_only
    Scenario: v6.host.reservation.duplicate-reservation
	Test Setup:
	Server is configured with 3000::/30 subnet with 3000::1-3000::10 pool.
	Reserve address 3000::1 in subnet 0 for host uniquely identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
	Reserve address 3000::2 in subnet 0 for host uniquely identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
	Send server configuration using SSH and config-file.
DHCP server failed to start. During configuration process.


@v6 @host_reservation @kea_only
    Scenario: v6.host.reservation.conflicts-two-entries-for-one-host-different-subnets
	Test Setup:
	Server is configured with 3000::/30 subnet with 3000::1-3000::10 pool.
	Server is configured with another subnet: 3001::/30 with 3001::1-3001::10 pool.
	Reserve address 3000::1 in subnet 0 for host uniquely identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
	Reserve address 3000::3 in subnet 1 for host uniquely identified by hw-address f6:f5:f4:f3:f2:01.
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


@v6 @host_reservation @kea_only
    Scenario: v6.host.reservation.conflicts-reconfigure-server-with-reservation-of-used-address
	Test Setup:
	Server is configured with 3000::/30 subnet with 3000::1-3000::2 pool.
	Send server configuration using SSH and config-file.
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

	Test Procedure:
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:22.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
    Client sets DUID value to 00:03:00:01:66:55:44:33:22:22.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

    # bigger prefix pool + reservation
	Test Setup:
	Server is configured with 3000::/30 subnet with 3000::1-3000::10 pool.
	Reserve address 3000::1 in subnet 0 for host uniquely identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
	Send server configuration using SSH and config-file.
DHCP server is reconfigured.

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
	Response sub-option 5 from option 3 MUST NOT contain address 3000::1.


@v6 @host_reservation @kea_only
    Scenario: v6.host.reservation.conflicts-reconfigure-server-with-reservation-of-used-address-2
	Test Setup:
	Server is configured with 3000::/30 subnet with 3000::1-3000::2 pool.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:22.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:22.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
	Response option 3 MUST contain sub-option 13.
	Response sub-option 13 from option 3 MUST contain statuscode 2.

    # bigger prefix pool + reservation
	Test Setup:
	Server is configured with 3000::/30 subnet with 3000::1-3000::10 pool.
	Reserve address 3000::1 in subnet 0 for host uniquely identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
	Send server configuration using SSH and config-file.
DHCP server is reconfigured.

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
	Response sub-option 5 from option 3 MUST NOT contain address 3000::1.


@v6 @host_reservation @kea_only
    Scenario: v6.host.reservation.conflicts-reconfigure-server-with-reservation-of-used-address-renew-before-expire
	Test Setup:
	Server is configured with 3000::/30 subnet with 3000::1-3000::2 pool.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:22.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:22.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

    ## SAVE VALUES
    Client saves IA_NA option from received message.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
	Response option 3 MUST contain sub-option 13.
	Response sub-option 13 from option 3 MUST contain statuscode 2.

    # bigger prefix pool + reservation
	Test Setup:
	Time renew-timer is configured with value 105.
	Time rebind-timer is configured with value 106.
	Time valid-lifetime is configured with value 107.
	Time preferred-lifetime is configured with value 108.
	Server is configured with 3000::/30 subnet with 3000::1-3000::3 pool.
	Reserve address 3000::2 in subnet 0 for host uniquely identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
	Send server configuration using SSH and config-file.
DHCP server is reconfigured.

	Test Procedure:
	Client copies server-id option from received message.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:22.
    Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	Response sub-option 5 from option 3 MUST contain validlft 0.
	Response sub-option 5 from option 3 MUST contain address 3000::2.
	Response sub-option 5 from option 3 MUST contain validlft 107.
	Response sub-option 5 from option 3 MUST contain address 3000::3.

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
	Response sub-option 5 from option 3 MUST contain address 3000::2.


@v6 @host_reservation @kea_only
    Scenario: v6.host.reservation.conflicts-reconfigure-server-with-reservation-of-used-address-renew-after-expire

    Test Setup:
	Time renew-timer is configured with value 5.
	Time rebind-timer is configured with value 6.
	Time preferred-lifetime is configured with value 7.
	Time valid-lifetime is configured with value 8.
	Server is configured with 3000::/30 subnet with 3000::1-3000::2 pool.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:22.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:22.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

    ## SAVE VALUES
    Client saves IA_NA option from received message.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
	Response option 3 MUST contain sub-option 13.
	Response sub-option 13 from option 3 MUST contain statuscode 2.

    # bigger prefix pool + reservation
	Test Setup:
	Time renew-timer is configured with value 5.
	Time rebind-timer is configured with value 6.
	Time preferred-lifetime is configured with value 7.
	Time valid-lifetime is configured with value 8.
	Server is configured with 3000::/30 subnet with 3000::1-3000::3 pool.
	Reserve address 3000::2 in subnet 0 for host uniquely identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
Send server configuration using SSH and config-file.

DHCP server is reconfigured.

	Test Procedure:
	Client copies server-id option from received message.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:22.
    Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	Response sub-option 5 from option 3 MUST contain validlft 0.
	Response sub-option 5 from option 3 MUST contain address 3000::2.
	Response sub-option 5 from option 3 MUST contain validlft 8.
	Response sub-option 5 from option 3 MUST contain address 3000::3.

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
	Response sub-option 5 from option 3 MUST contain address 3000::2.