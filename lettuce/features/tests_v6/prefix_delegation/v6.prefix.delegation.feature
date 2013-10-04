Feature: DHCPv6 Prefix Delegation 
    Test for Prefix Delegation using Request messages, based on RFC 3633.

@v6 @PD @rfc3633
    Scenario: prefix.delegation.onlyPD-request
  
 	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 92 delegated prefix length.
	Server is started.
	
	Test Procedure:
	Client does NOT include IA-NA.
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response sub-option 26 from option 25 MUST contain prefix 3000::.
	Response option 25 MUST contain sub-option 13.
	Response sub-option 13 from option 25 MUST contain statuscode 0.
	
	Test Procedure:
	Client does NOT include IA-NA.
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response sub-option 26 from option 25 MUST contain prefix 3000::.
	
	References: RFC 3633, Section: 12.2

@v6 @PD @rfc3633
    Scenario: prefix.delegation.IA-and-PD-request
  
 	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
	Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 92 delegated prefix length.
	Server is started.
	
	Test Procedure:
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response sub-option 26 from option 25 MUST contain prefix 3000::.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	Response sub-option 5 from option 3 MUST contain address 3000::1.
		
	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response sub-option 26 from option 25 MUST contain prefix 3000::.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	Response sub-option 5 from option 3 MUST contain address 3000::1.
	
	References: RFC 3633, Section:

@v6 @PD @rfc3633
	Scenario: prefix.delegation.request-release
	
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 91 delegated prefix length.
	#pool of two prefixes
	Server is started.
	
	Test Procedure:
	Client does include IA-PD.
	Client does NOT include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client does NOT include IA-NA.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response sub-option 26 from option 25 MUST contain prefix 3000::.
	
	Test Procedure:
	Client copies IA_PD option from received message.
	Client copies server-id option from received message.
	Client does NOT include IA-NA.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 13. 
	Response sub-option 13 from option 25 MUST contain statuscode 0.
	
	References: RFC 3633, Section: 12.2

@v6 @PD @rfc3633
    Scenario: prefix.delegation.noprefixavail-release
  	#assign 2 prefixes, try third, fail, release one, assign one more time with success.
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 91 delegated prefix length.
	#pool of two prefixes
	Server is started.
	
	Test Procedure:
	Client does include IA-PD.
	Client does NOT include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client does NOT include IA-NA.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	
	Test Procedure:
	Generate new IA_PD.
	Client does include IA-PD.
	Client does NOT include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client does NOT include IA-NA.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	#both prefixes assigned.
	
	Test Procedure:
	Client saves IA_PD option from received message.
	Generate new IA_PD.
	Client does include IA-PD.
	Client does NOT include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 13.	
	Response sub-option 13 from option 25 MUST contain statuscode 6. 
	
	Test Procedure:
	Client adds saved options. And DONT Erase.
	Client copies server-id option from received message.
	Client does NOT include IA-NA.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 13. 
	Response sub-option 13 from option 25 MUST contain statuscode 0. 

	Test Procedure:
	Generate new IA_PD.
	Client does include IA-PD.
	Client does NOT include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 13.	
	Response sub-option 13 from option 25 MUST contain statuscode 6. 
	
	References: RFC 3633, Section: 11.2 12.2

@v6 @PD @rfc3633
    Scenario: prefix.delegation.noprefixavail
  
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 91 delegated prefix length.
	#pool of two prefixes
	Server is started.
	
	Test Procedure:
	Client does include IA-PD.
	Client does NOT include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client does NOT include IA-NA.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	
	Test Procedure:
	Generate new IA_PD.
	Client does include IA-PD.
	Client does NOT include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client does NOT include IA-NA.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	#both prefixes assigned.
	
	Test Procedure:
	Generate new IA_PD.
	Client does include IA-PD.
	Client does NOT include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 13.	
	Response sub-option 13 from option 25 MUST contain statuscode 6. 
		
	References: RFC 3633, Section: 11.2

@v6 @PD @rfc3633
    Scenario: prefix.delegation.onlyPD-relay
  
 	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 92 delegated prefix length.
	Server is started.
	
	Test Procedure:
	Client does NOT include IA-NA.
	Client does include IA-PD.
	Client sends SOLICIT message.

	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
	Response MUST include option 9. 
	#add test after Scapy fix
	
	References: RFC 3633, Section: 14