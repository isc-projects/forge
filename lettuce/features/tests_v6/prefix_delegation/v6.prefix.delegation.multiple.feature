Feature: DHCPv6 Prefix Delegation 
    Test for Prefix Delegation using Request messages,multiple IA/PD in one request, based on RFC 3633.
	
@v6 @PD @rfc3633 @multiplePD
    Scenario: prefix.delegation.multiple.request
    
   	Test Setup:
	Server is configured with 3000::/32 subnet with 3000::5-3000::5 pool.
	Server is configured with 3000:: prefix in subnet 0 with 32 prefix length and 34 delegated prefix length.
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
	Response sub-option 26 from option 25 MUST contain prefix 3000:0:4000.
	Response sub-option 26 from option 25 MUST contain prefix 3000:0:8000.
	Response sub-option 26 from option 25 MUST contain prefix 3000:0:c000.	

	References: RFC 3633, Section: 12.2

@v6 @PD @rfc3633 @multiplePD
    Scenario: prefix.delegation.multiple.PD_and_IA_request
	Test Setup:
	Server is configured with 3000::/32 subnet with 3000::1-3000::4 pool.
	Server is configured with 3000:: prefix in subnet 0 with 32 prefix length and 34 delegated prefix length.
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
	Response MUST include option 3. 
	Response sub-option 13 from option 3 MUST contain address 3000::1.
	Response sub-option 13 from option 3 MUST contain address 3000::2.
	Response sub-option 13 from option 3 MUST contain address 3000::3.
	Response sub-option 13 from option 3 MUST contain address 3000::4.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response sub-option 26 from option 25 MUST contain prefix 3000::.
	Response sub-option 26 from option 25 MUST contain prefix 3000:0:4000.
	Response sub-option 26 from option 25 MUST contain prefix 3000:0:8000.
	Response sub-option 26 from option 25 MUST contain prefix 3000:0:c000.	
	
	References: RFC 3633, Section: 12.2
	
@v6 @PD @rfc3633 @multiplePD
    Scenario: prefix.delegation.multiple.PD_and_IA_request_partial_success
	Test Setup:
	Server is configured with 3000::/32 subnet with 3000::1-3000::2 pool.
	Server is configured with 3000:: prefix in subnet 0 with 32 prefix length and 33 delegated prefix length.
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
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 13.
	Response sub-option 13 from option 3 MUST contain address 3000::1.
	Response sub-option 13 from option 3 MUST contain address 3000::2.
	Response sub-option 13 from option 3 MUST contain statuscode 2.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26. 
	Response sub-option 26 from option 25 MUST contain prefix 3000::.
	Response sub-option 26 from option 25 MUST contain prefix 3000:0:8000::.
	Response sub-option 13 from option 25 MUST contain statuscode 6.

	References: RFC 3633, Section: 12.2
	
@v6 @PD @rfc3633
    Scenario: prefix.delegation.multiple.PD_and_IA_request_partial_fail
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
	Response sub-option 13 from option 3 MUST contain statuscode 2.	
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26. 
	Response sub-option 26 from option 25 MUST contain prefix 3000::.

	References: RFC 3633, Section: 12.2