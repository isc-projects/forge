Feature: DHCPv6 Prefix Delegation 
    Testing Server's politics about Confirm and Decline messages, based on RFC 3633.

@v6 @dhcp6 @PD @rfc3633
    Scenario: prefix.delegation.IA_and_PD_confirm

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::2-3000::2 pool.
	Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 96 delegated prefix length.
	DHCP server is started.
	
	Test Procedure:
	Client requests option 7.
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response sub-option 26 from option 25 MUST contain prefix 3000::.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	Response sub-option 5 from option 3 MUST contain address 3000::2.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies IA_PD option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies IA_PD option from received message.
	Client sends CONFIRM message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 2.
	Response MUST NOT include option 25.

	References: RFC 3633 Section 12.1.
	
@v6 @dhcp6 @PD @rfc3633
    Scenario: prefix.delegation.IA_and_PD_decline

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::5-3000::5 pool.
	Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 96 delegated prefix length.
	DHCP server is started.
	
	Test Procedure:
	Client requests option 7.
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	Response sub-option 5 from option 3 MUST contain address 3000::5.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies IA_PD option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies IA_PD option from received message.
	Client copies server-id option from received message.
	Client sends DECLINE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST NOT include option 25.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 13.
	
	References: RFC 3633 Section 12.1.