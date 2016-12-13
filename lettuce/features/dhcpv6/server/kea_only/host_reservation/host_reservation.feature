Feature: Host Reservation DHCPv6
    Tests for Host Reservation feature for: prefixes, addresses and hostnames based on MAC and DUID.

@v6 @host_reservation @kea_only
    Scenario: v6.host.reservation.all-values-mac
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Reserve hostname reserved-hostname in subnet 0 for host uniquely identified by f6:f5:f4:f3:f2:01.
	For host reservation entry no. 0 in subnet 0 add address with value 3000::100.
	For host reservation entry no. 0 in subnet 0 add prefix with value 3001::/40.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    DDNS server is configured with qualifying-suffix option set to my.domain.com.
	DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include IA-PD.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client copies IA_PD option from received message.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
    Client sets FQDN_domain_name value to some-different-name.
    Client sets FQDN_flags value to S.
    Client does include fqdn.
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

@v6 @host_reservation @kea_only
    Scenario: v6.host.reservation.all-values-duid
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Reserve hostname reserved-hostname in subnet 0 for host uniquely identified by 00:03:00:01:f6:f5:f4:f3:f2:01.
	For host reservation entry no. 0 in subnet 0 add address with value 3000::100.
	For host reservation entry no. 0 in subnet 0 add prefix with value 3001::/40.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    DDNS server is configured with qualifying-suffix option set to my.domain.com.
	DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include IA-PD.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client copies IA_PD option from received message.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
    Client sets FQDN_domain_name value to some-different-name.
    Client sets FQDN_flags value to S.
    Client does include fqdn.
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

@v6 @host_reservation @kea_only
    Scenario: v6.host.reservation.all-values-duid-2

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with 2001:db8:1:: prefix in subnet 0 with 32 prefix length and 33 delegated prefix length.
	Reserve hostname reserved-hostname in subnet 0 for host uniquely identified by 00:03:00:01:f6:f5:f4:f3:f2:01.
	For host reservation entry no. 0 in subnet 0 add address with value 3000::100.
	For host reservation entry no. 0 in subnet 0 add prefix with value 2001:db8:1::/40.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    DDNS server is configured with qualifying-suffix option set to my.domain.com.
	DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01.
	Client does include IA-PD.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client copies IA_PD option from received message.
	Client sets DUID value to 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01.
    Client sets FQDN_domain_name value to some-different-name.
    Client sets FQDN_flags value to S.
    Client does include fqdn.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST NOT contain address 3000::100.
    Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response sub-option 26 from option 25 MUST NOT contain prefix 2001:db8:1::.
    Response MUST include option 39.
    Response option 39 MUST NOT contain fqdn reserved-hostname.my.domain.com.