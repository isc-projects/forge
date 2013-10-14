Feature: DHCPv6 Prefix Delegation 
    Test for basic Prefix Delegation, based on RFC 3633

@v6 @PD @rfc3633
    Scenario: prefix.delegation.server_configuration
    
	Test Procedure:
	Server is configured with 3000::/32 subnet with 3000::1-3000::2 pool.
	Server is configured with 3000:: prefix in subnet 0 with 5 prefix length and 33 delegated prefix length.
	Server failed to start. During configuration process.	

	References: RFC 3633

@v6 @PD @rfc3633
    Scenario: prefix.delegation.onlyPD
  
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
	Response MUST include option 25.
	Response sub-option 26 from option 25 MUST contain prefix 3000::.
	
	References: RFC 3633, Section: 9

@v6 @PD @rfc3633
    Scenario: prefix.delegation.IA_and_PD
  
	Server is configured with 3000::/64 subnet with 3000::2-3000::2 pool.
	Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 91 delegated prefix length.
	Server is started.
	
	Test Procedure:
	Client requests option 7.
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	Response sub-option 26 from option 25 MUST contain prefix 3000::.
	Response MUST include option 3.
	Response sub-option 5 from option 3 MUST contain address 3000::2.

	References: RFC 3633, Section: 9
	
@v6 @PD @rfc3633
    Scenario: prefix.delegation.without_server_configuration
  
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	Server is started.
	
	Test Procedure:
	Client requests option 7.
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 13.
	Response sub-option 13 from option 25 MUST contain statuscode 6.
	
	Server is configured with 3000::/64 subnet with 3000::3-3000::3 pool.
	Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 96 delegated prefix length.
	Server is started.
	
	Test Procedure:
	Client requests option 7.
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	Response sub-option 26 from option 25 MUST contain prefix 3000::.
	Response MUST include option 3.
	Response sub-option 5 from option 3 MUST contain address 3000::3.

	References: RFC 3633, Section: 9.
	