Feature: Host Reservation DHCPv6
     Tests for Host Reservation feature for hostname based on DUID and MAC address.

@v6 @host_reservation @kea_only
    Scenario: v6.host.reservation.mac.hostname-with-ddns
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Reserve hostname reserved-hostname in subnet 0 for host uniquely identified by f6:f5:f4:f3:f2:01.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    DDNS server is configured with qualifying-suffix option set to my.domain.com.
	DHCP server is started.

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
    Client sets FQDN_domain_name value to some-different-name.
    Client sets FQDN_flags value to S.
    Client does include fqdn.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response MUST include option 39.
    Response option 39 MUST contain fqdn reserved-hostname.my.domain.com.


@v6 @host_reservation @kea_only
    Scenario: v6.host.reservation.mac.hostname-without-ddns

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Reserve hostname reserved-hostname in subnet 0 for host uniquely identified by f6:f5:f4:f3:f2:01.
	DHCP server is started.

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
    Client sets FQDN_domain_name value to some-different-name.
    Client sets FQDN_flags value to S.
    Client does include fqdn.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response MUST include option 39.
    Response option 39 MUST contain fqdn reserved-hostname.


@v6 @host_reservation @kea_only
    Scenario: v6.host.reservation.duid.hostname-with-ddns

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Reserve hostname reserved-hostname in subnet 0 for host uniquely identified by 00:03:00:01:f6:f5:f4:f3:f2:01.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    DDNS server is configured with qualifying-suffix option set to my.domain.com.
	DHCP server is started.

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
    Client sets FQDN_domain_name value to some-different-name.
    Client sets FQDN_flags value to S.
    Client does include fqdn.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 39.
    Response option 39 MUST contain fqdn reserved-hostname.my.domain.com.

@v6 @host_reservation @kea_only
    Scenario: v6.host.reservation.duid.hostname-without-ddns

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Reserve hostname reserved-hostname in subnet 0 for host uniquely identified by 00:03:00:01:f6:f5:f4:f3:f2:01.
	DHCP server is started.

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
    Client sets FQDN_domain_name value to some-different-name.
    Client sets FQDN_flags value to S.
    Client does include fqdn.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 39.
    Response option 39 MUST contain fqdn reserved-hostname.