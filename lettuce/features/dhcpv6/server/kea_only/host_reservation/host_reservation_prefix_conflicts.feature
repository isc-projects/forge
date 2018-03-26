Feature: Host Reservation DHCPv6
    Tests for conflicts resolving in Host Reservation feature based both on MAC and DUID.
    For prefix, addresses and hostnames.

@v6 @host_reservation @kea_only @disabled
    Scenario: v6.host.reservation.conflicts-two-entries-for-one-host-1
	Test Setup:
	Server is configured with 3000::/30 subnet with 3000::1-3000::10 pool.
	Server is configured with 2001:db8:1:: prefix in subnet 0 with 32 prefix length and 34 delegated prefix length.
	Reserve prefix 2001:db8:1:0:4000::/34 in subnet 0 for host uniquely identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
	Reserve prefix 2001:db8:1:0:8000::/34 in subnet 0 for host uniquely identified by hw-address f6:f5:f4:f3:f2:01.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include IA-PD.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.
    #We could check logs for: "more than one reservation found for the host belonging"

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:33:22:11.
	Client does include IA-PD.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
    Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.

@v6 @host_reservation @kea_only @disabled
    Scenario: v6.host.reservation.conflicts-two-entries-for-one-host-2
	Test Setup:
	Server is configured with 3000::/30 subnet with 3000::1-3000::10 pool.
	Server is configured with 2001:db8:1:: prefix in subnet 0 with 32 prefix length and 34 delegated prefix length.
	Reserve prefix 2001:db8:1:0:4000::/34 in subnet 0 for host uniquely identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
	Reserve hostname xyz in subnet 0 for host uniquely identified by hw-address f6:f5:f4:f3:f2:01.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include IA-PD.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.
    #We could check logs for: "more than one reservation found for the host belonging"

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:33:22:11.
	Client does include IA-PD.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
    Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.

@v6 @host_reservation @kea_only @disabled
    Scenario: v6.host.reservation.conflicts-two-entries-for-one-host-3
	Test Setup:
	Server is configured with 3000::/30 subnet with 3000::1-3000::10 pool.
	Server is configured with 2001:db8:1:: prefix in subnet 0 with 32 prefix length and 34 delegated prefix length.
	Reserve prefix 2001:db8:1:0:4000::/34 in subnet 0 for host uniquely identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
	Reserve address 3000::3 in subnet 0 for host uniquely identified by hw-address f6:f5:f4:f3:f2:01.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include IA-PD.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.
    #We could check logs for: "more than one reservation found for the host belonging"

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:33:22:11.
	Client does include IA-PD.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
    Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.

@v6 @host_reservation @kea_only
    Scenario: v6.host.reservation.conflicts-two-entries-for-one-host-different-subnets
	Test Setup:
	Server is configured with 3000::/30 subnet with 3000::1-3000::10 pool.
	Server is configured with 2001:db8:1:: prefix in subnet 0 with 32 prefix length and 34 delegated prefix length.
	Server is configured with another subnet: 3001::/30 with 3001::1-3001::10 pool.
	Reserve prefix 2001:db8:1:0:4000::/34 in subnet 0 for host uniquely identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
	Reserve address 3000::3 in subnet 1 for host uniquely identified by hw-address f6:f5:f4:f3:f2:01.
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
    Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
    Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.


@v6 @host_reservation @kea_only
    Scenario: v6.host.reservation.conflicts-reconfigure-server-with-reservation-of-used-prefix
	Test Setup:
	Server is configured with 3000::/30 subnet with 3000::1-3000::10 pool.
	Server is configured with 2001:db8:1:: prefix in subnet 0 with 32 prefix length and 33 delegated prefix length.
	Send server configuration using SSH and config-file.
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
	Client copies IA_NA option from received message.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

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
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:22.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

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
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:33.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

    # bigger prefix pool + reservation
	Test Setup:
	Server is configured with 3000::/30 subnet with 3000::1-3000::10 pool.
	Server is configured with 2001:db8:1:: prefix in subnet 0 with 32 prefix length and 34 delegated prefix length.
	Reserve prefix 2001:db8:8001::/34 in subnet 0 for host uniquely identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
Send server configuration using SSH and config-file.

Reconfigure DHCP server.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include IA-PD.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client does include IA-PD.
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response sub-option 26 from option 25 MUST NOT contain prefix 2001:db8:8001::.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

@v6 @host_reservation @kea_only
    Scenario: v6.host.reservation.conflicts-reconfigure-server-with-reservation-of-used-prefix-2
	Test Setup:
	Server is configured with 3000::/30 subnet with 3000::1-3000::10 pool.
	Server is configured with 2001:db8:1:: prefix in subnet 0 with 32 prefix length and 33 delegated prefix length.
	Send server configuration using SSH and config-file.
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
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

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
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:22.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client does include IA-PD.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
    Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
    Response MUST include option 25.
	Response option 25 MUST contain sub-option 13.
	Response sub-option 13 from option 25 MUST contain statuscode 6.

    # bigger prefix pool + reservation
	Test Setup:
	Server is configured with 3000::/30 subnet with 3000::1-3000::10 pool.
	Server is configured with 2001:db8:1:: prefix in subnet 0 with 32 prefix length and 36 delegated prefix length.
	Reserve prefix 2001:db8:8001::/34 in subnet 0 for host uniquely identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
Send server configuration using SSH and config-file.

Reconfigure DHCP server.

	Test Procedure:
	Client does include IA-PD.
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
    Client sets plen value to 32.
    Client sets prefix value to 2001:db8:1:0:8000::.
    Client does include IA_Prefix.
	Client does include IA-PD.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response sub-option 26 from option 25 MUST NOT contain prefix 2001:db8:8001::.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.


@v6 @host_reservation @kea_only
    Scenario: v6.host.reservation.conflicts-reconfigure-server-with-reservation-of-used-prefix-renew-before-expire

	Test Setup:
	Server is configured with 3000::/30 subnet with 3000::1-3000::2 pool.
	Server is configured with 2001:db8:1:: prefix in subnet 0 with 32 prefix length and 33 delegated prefix length.
	Send server configuration using SSH and config-file.
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
    Client copies IA_NA option from received message.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

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
    Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:22.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
    ## SAVE VALUES
    Client saves IA_PD option from received message.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include IA-PD.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
	Response option 3 MUST contain sub-option 13.
	Response sub-option 13 from option 3 MUST contain statuscode 2.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 13.
	Response sub-option 13 from option 25 MUST contain statuscode 6.

	Test Procedure:
	Client copies server-id option from received message.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:22.
    Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Setup:
	Server is configured with 3000::/30 subnet with 3000::1-3000::2 pool.
	Server is configured with 2001:db8:1:: prefix in subnet 0 with 32 prefix length and 35 delegated prefix length.
	Reserve prefix 2001:db8:1:0:8000::/33 in subnet 0 for host uniquely identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
	Reserve prefix 2001:db8:1::/33 in subnet 0 for host uniquely identified by hw-address 00:03:00:01:f6:f5:f4:f3:f2:02.
Send server configuration using SSH and config-file.

Reconfigure DHCP server.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include IA-PD.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
	Response option 3 MUST contain sub-option 13.
	Response sub-option 13 from option 3 MUST contain statuscode 2.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response sub-option 26 from option 25 MUST NOT contain prefix 2001:db8:1::.
	Response sub-option 26 from option 25 MUST contain prefix 2001:db8:1:0:8000::.

    #Sleep for 17 seconds.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:22.
    Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response sub-option 26 from option 25 MUST NOT contain prefix 2001:db8:1::.
	Response sub-option 26 from option 25 MUST NOT contain prefix 2001:db8:1:0:8000::.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.


@v6 @host_reservation @kea_only
    Scenario: v6.host.reservation.conflicts-reconfigure-server-with-reservation-of-used-prefix-renew-after-expire

	Test Setup:
	Time renew-timer is configured with value 5.
	Time rebind-timer is configured with value 6.
	Time valid-lifetime is configured with value 7.
	Time preferred-lifetime is configured with value 8.
	Server is configured with 3000::/30 subnet with 3000::1-3000::2 pool.
	Server is configured with 2001:db8:1:: prefix in subnet 0 with 32 prefix length and 33 delegated prefix length.
	Send server configuration using SSH and config-file.
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
	Client copies IA_NA option from received message.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

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
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:22.
	Client does include client-id.
    Client sends REQUEST message.


	Pass Criteria:
	Server MUST respond with REPLY message.
    ## SAVE VALUES
    Client saves IA_PD option from received message.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:44.
	Client does include IA-PD.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
	Response option 3 MUST contain sub-option 13.
	Response sub-option 13 from option 3 MUST contain statuscode 2.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 13.
	Response sub-option 13 from option 25 MUST contain statuscode 6.

	Test Procedure:
	Client copies server-id option from received message.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:22.
    Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Setup:
	Time renew-timer is configured with value 5.
	Time rebind-timer is configured with value 6.
	Time valid-lifetime is configured with value 7.
	Time preferred-lifetime is configured with value 8.
	Server is configured with 3000::/30 subnet with 3000::1-3000::10 pool.
	Server is configured with 2001:db8:1:: prefix in subnet 0 with 32 prefix length and 33 delegated prefix length.
	Reserve prefix 2001:db8:1:0:8000::/33 in subnet 0 for host uniquely identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
	Reserve prefix 2001:db8:1::/33 in subnet 0 for host uniquely identified by duid 00:03:00:01:f6:f5:f4:f3:f2:02.
Send server configuration using SSH and config-file.

Reconfigure DHCP server.

    Sleep for 15 seconds.

    # prefix expired should be able
	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include IA-PD.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response sub-option 26 from option 25 MUST contain prefix 2001:db8:1:0:8000::.

	Test Procedure:
	Client does include IA-PD.
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client copies IA_NA option from received message.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response sub-option 26 from option 25 MUST contain prefix 2001:db8:1:0:8000::.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:22.
    Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	#Response sub-option 26 from option 25 MUST NOT contain prefix 2001:db8:1::. # this can be in message but with validlifetime 0
	# todo: associate validlifetimes with address from single suboption.
	Response sub-option 26 from option 25 MUST NOT contain prefix 2001:db8:1:0:8000::.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.