Feature: DHCPv6 Prefix Delegation 
    Test for Prefix Delegation using Request messages, based on RFC 3633.

@v6 @PD @rfc3633
    Scenario: prefix.delegation.onlyPD_request
  
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

	Test Procedure:
	Client does NOT include IA-NA.
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.

	References: RFC 3633, Section: 12.2

@v6 @PD @rfc3633
    Scenario: prefix.delegation.IA_and_PD_request
  
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
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	Response sub-option 5 from option 3 MUST contain address 3000::1.
	
	References: RFC 3633

@v6 @PD @rfc3633
	Scenario: prefix.delegation.onlyPD_request_release
	
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
	Client copies IA_PD option from received message.
	Client copies server-id option from received message.
	Client does NOT include IA-NA.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 13.
	Response sub-option 13 from option 25 MUST contain statuscode 0.
	# tests MUST NOT include 'NoBinding'...
	
	References: RFC 3633, Section: 12.2

@v6 @PD @rfc3633
	Scenario: prefix.delegation.onlyPD_multiple_request_release

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
	Client copies IA_PD option from received message.
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
	Response option 25 MUST contain sub-option 26.
	# if it fails, it means that release process fails.
	
	References: RFC 3633, Section: 12.2
	
@v6 @PD @rfc3633
	Scenario: prefix.delegation.IA_and_PD_request_release
	
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 91 delegated prefix length.
	#pool of two prefixes
	Server is started.
	
	Test Procedure:
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client copies IA_NA option from received message.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
		
	Test Procedure:
	Client copies IA_PD option from received message.
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response MUST include option 3.
	# tests MUST NOT include 'NoBinding'...
	
	References: RFC 3633
	
@v6 @PD @rfc3633
	Scenario: prefix.delegation.IA_and_PD_multiple_request_release

	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 91 delegated prefix length.
	#pool of two prefixes
	Server is started.
	
	Test Procedure:
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client copies IA_NA option from received message.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
		
	Test Procedure:
	Client copies IA_PD option from received message.
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response MUST include option 3.
	# tests MUST NOT include 'NoBinding'...	

	Test Procedure:
	Generate new IA_PD.
	Generate new IA.
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client copies IA_NA option from received message.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Generate new IA_PD.
	Generate new IA.
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	References: RFC 3633
	
@v6 @PD @rfc3633
	Scenario: prefix.delegation.request_release_restart

 	Test Setup:
	Server is configured with 3000::/32 subnet with 3000::1-3000::2 pool.
	Server is configured with 3000:: prefix in subnet 0 with 32 prefix length and 33 delegated prefix length.
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

	Restart server.
	
	Test Procedure:
	Client copies IA_PD option from received message.
	Client copies server-id option from received message.
	Client does NOT include IA-NA.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 13.
	Response sub-option 13 from option 25 MUST contain statuscode 3.

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
	#Response sub-option 26 from option 25 MUST contain prefix 3000::.

	Test Procedure:
	Generate new IA_PD.
	Client does include IA-PD.
	Client does NOT include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.

	References: RFC 3633, Section: 12.2
	
@v6 @PD @rfc3633
	Scenario: prefix.delegation.request_release_restart	

 	Test Setup:
	Server is configured with 3000::/32 subnet with 3000::1-3000::2 pool.
	Server is configured with 3000:: prefix in subnet 0 with 32 prefix length and 33 delegated prefix length.
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

	Restart server.
	
	Test Procedure:
	Client copies IA_PD option from received message.
	Client copies server-id option from received message.
	Client does NOT include IA-NA.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 13.
	Response sub-option 13 from option 25 MUST contain statuscode 3.

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
	#Response sub-option 26 from option 25 MUST contain prefix 3000::.

	Test Procedure:
	Generate new IA_PD.
	Client does include IA-PD.
	Client does NOT include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.

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
	Response option 25 MUST contain sub-option 13.
	Response sub-option 13 from option 25 MUST contain statuscode 6.

	References: RFC 3633, Section: 12.2
	
@v6 @PD @rfc3633
    Scenario: prefix.delegation.noprefixavail_release
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
	#success
	
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
	Response option 25 MUST contain sub-option 26.
	
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
    Scenario: prefix.delegation.release_nobinding

 	Test Setup:
	Server is configured with 3000::/32 subnet with 3000::1-3000::2 pool.
	Server is configured with 3000:: prefix in subnet 0 with 32 prefix length and 33 delegated prefix length.
	Server is started.
	
	Test Procedure:
	Client does NOT include IA-NA.
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client does NOT include IA-NA.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 13.
	Response sub-option 13 from option 25 MUST contain statuscode 3.

	References: RFC 3633/3315

@v6 @PD @rfc3633
    Scenario: prefix.delegation.release_dual_nobinding
 	Test Setup:
	Server is configured with 3000::/32 subnet with 3000::1-3000::2 pool.
	Server is configured with 3000:: prefix in subnet 0 with 32 prefix length and 33 delegated prefix length.
	Server is started.
	
	Test Procedure:
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client copies IA_NA option from received message.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 13.
	Response sub-option 13 from option 25 MUST contain statuscode 3.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 13.
	Response sub-option 13 from option 3 MUST contain statuscode 3.
	
	References: RFC 3633/3315

@v6 @PD @rfc3633
    Scenario: prefix.delegation.release_nobinding2

 	Test Setup:
	Server is configured with 3000::/32 subnet with 3000::1-3000::2 pool.
	Server is configured with 3000:: prefix in subnet 0 with 32 prefix length and 33 delegated prefix length.
	Server is started.
	
	Test Procedure:
	Client does NOT include IA-NA.
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.

	Test Procedure:
	Client does NOT include IA-NA.
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.

	Test Procedure:
	Client copies server-id option from received message.
	Client saves IA_PD option from received message.
	Client adds saved options. And DONT Erase.
	Client does NOT include IA-NA.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	#must not contain status code == 3.

	Test Procedure:
	Client copies server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client does NOT include IA-NA.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 13.
	Response sub-option 13 from option 25 MUST contain statuscode 3.

	References: RFC 3633/3315

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


@v6 @PD @rfc3633
    Scenario: prefix.delegation.ignore_lifetimes

    Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::200 pool.
	Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
	Server is started.

	Test Procedure:
	# Client sets preflft value bigger than validlft. Server MUST ignore those values.
	Client sets preflft value to 4444.
    Client sets validlft value to 2345.
    Client does NOT include IA-NA.
    Client does include IA_Prefix.

	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response sub-option 26 from option 25 MUST NOT contain preflft 4444.
	Response sub-option 26 from option 25 MUST NOT contain validlft 2345.

	Test Procedure:
	Client copies server-id option from received message.
	# Now, preflft > validlft. Server should take those values.
	Client sets preflft value to 3500.
	Client sets validlft value to 5000.
	Client does NOT include IA-NA.
	Client does include IA_Prefix.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response sub-option 26 from option 25 MUST contain preflft 3500.
	Response sub-option 26 from option 25 MUST contain validlft 5000.

	References: RFC 3633, Section: 10


@v6 @PD @rfc3633
    Scenario: prefix.delegation.ignore_timers

    Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::200 pool.
	Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
	Server is started.

	Test Procedure:
	# Client sets T1, T2 values bigger than preflft. Server MUST ignore those values.
	Client sets T1 value to 2500.
	Client sets T2 value to 3500.
	Client sets preflft value to 2000.
    Client does NOT include IA-NA.
    Client does include IA_Prefix.

	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response option 25 MUST NOT contain T1 2500.
	Response option 25 MUST NOT contain T2 3500.

	Test Procedure:
	Client copies server-id option from received message.
	# Now, T1, T2 < preflft. Server should take those values.
	Client sets T1 value to 1500.
	Client sets T2 value to 2500.
	Client sets preflft value to 3500.
	Client does NOT include IA-NA.
	Client does include IA_Prefix.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response option 25 MUST contain T1 1500.
	Response option 25 MUST contain T1 2500.

	References: RFC 3633, Section: 10