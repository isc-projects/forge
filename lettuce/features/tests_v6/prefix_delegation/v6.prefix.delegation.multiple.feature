Feature: DHCPv6 Prefix Delegation 
    Test for Prefix Delegation using Request messages,multiple IA/PD in one request, based on RFC 3633.
	
@v6 @PD @rfc3633 @multiplePD
    Scenario: prefix.delegation.multiple.request
    
   	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 96 delegated prefix length.
	Server is started.
	
	Test Procedure:
	Client does NOT include IA-NA.
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	
	Test Procedure:
	Client saves IA_PD option from received message.
	Generate new IA_PD.
	Client does NOT include IA-NA.
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	
	Test Procedure:
	Client saves IA_PD option from received message.
	Generate new IA_PD.
	Client does NOT include IA-NA.
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_PD option from received message.
	Generate new IA_PD.
	Client does NOT include IA-NA.
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client saves IA_PD option from received message.
	Client adds saved options. And Erase.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.  
	Response option 25 MUST contain sub-option 26. 
	Response sub-option 26 from option 25 MUST contain prefix 3000::.

	References: RFC 3633, Section: 12.2

@v6 @PD @rfc3633 @multiplePD
    Scenario: prefix.delegation.multiple.PD-and-IA-request
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::4 pool.
	Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 92 delegated prefix length.
	#pool for 4 addresses and 4 prefix, all 8 with success
	
	Server is started.
	
	Test Procedure:
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	
	Test Procedure:
	Client saves IA_NA option from received message.
	Client saves IA_PD option from received message.
	Generate new IA.
	Generate new IA_PD.
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	
	Test Procedure:
	Client saves IA_NA option from received message.
	Client saves IA_PD option from received message.
	Generate new IA.
	Generate new IA_PD.
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client saves IA_PD option from received message.
	Generate new IA.
	Generate new IA_PD.
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client saves IA_NA option from received message.
	Client saves IA_PD option from received message.
	Client adds saved options. And Erase.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.  
	Response MUST include option 25.
	Response MUST include option 3.
	Response option 25 MUST contain sub-option 26.
	Response sub-option 26 from option 25 MUST contain prefix 3000::.
	#4x IA address and 4x prefix
	
	References: RFC 3633, Section: 12.2
	
@v6 @PD @rfc3633 @multiplePD
    Scenario: prefix.delegation.multiple.PD-and-IA-request-partial-success
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::2 pool.
	Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 91 delegated prefix length.
	#pool for 2 addresses and 2 prefix, half success
	
	Server is started.
	
	Test Procedure:
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	
	Test Procedure:
	Client saves IA_NA option from received message.
	Client saves IA_PD option from received message.
	Generate new IA.
	Generate new IA_PD.
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	
	Test Procedure:
	Client saves IA_NA option from received message.
	Client saves IA_PD option from received message.
	Generate new IA.
	Generate new IA_PD.
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client saves IA_PD option from received message.
	Generate new IA.
	Generate new IA_PD.
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client saves IA_NA option from received message.
	Client saves IA_PD option from received message.
	Client adds saved options. And Erase.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.  
	Response MUST include option 25.
	Response MUST include option 3.
	Response option 25 MUST contain sub-option 26. 
	Response option 25 MUST contain sub-option 13. 
	Response sub-option 26 from option 25 MUST contain prefix 3000::.
	#4x IA address and 4x prefix, both 2 success and 2 fails
	
	References: RFC 3633, Section: 12.2
	
@v6 @PD @rfc3633
    Scenario: prefix.delegation.multiple.PD-and-IA-request-partial-fail
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::2 pool.
	Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 92 delegated prefix length.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Generate new IA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Generate new IA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client does include IA-PD.	
	Client copies server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 13.
	Response sub-option 13 from option 3 MUST contain statuscode 0.
	Response sub-option 13 from option 3 MUST contain statuscode 2.	
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 13.
	Response sub-option 13 from option 25 MUST contain statuscode 0.

	References: RFC 3633, Section: 12.2