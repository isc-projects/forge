Feature: DHCPv6 Prefix Delegation 
    Test for Prefix Delegation using Request messages, based on RFC 3633.

@v6 @dhcp6 @PD @rfc3633
    Scenario: prefix.delegation.onlyPD_renew
  
 	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	Server is configured with 2001:db8:1:: prefix in subnet 0 with 90 prefix length and 92 delegated prefix length.
	DHCP server is started.
	
	Test Procedure:
	Client does include IA-PD.
	Client does include client-id.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26. 
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26. 

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	
	References: RFC 3633, Section: 12.2

@v6 @dhcp6 @PD @rfc3633 @disabled
    #disabled after rfc 7550
    Scenario: prefix.delegation.onlyPD_renew_nobinding
    # this tests will be disabled after RFC 7550 tests will be added
 	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	Server is configured with 2001:db8:1:: prefix in subnet 0 with 90 prefix length and 92 delegated prefix length.
	DHCP server is started.
	
	Test Procedure:
	Client does include IA-PD.
	Client does include client-id.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 13.
	Response sub-option 13 from option 25 MUST contain statuscode 3.
	
	References: RFC 3633, Section: 12.2

@v6 @dhcp6 @PD @rfc3633 @disabled
    #disabled after rfc 7550
    Scenario: prefix.delegation.onlyPD_renew_nobinding_new_IA_PD
    # this tests will be disabled after RFC 7550 tests will be added

 	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	Server is configured with 2001:db8:1:: prefix in subnet 0 with 90 prefix length and 92 delegated prefix length.
	DHCP server is started.

	Test Procedure:
	Client does include IA-PD.
	Client does include client-id.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Generate new IA_PD.
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 13.
	Response sub-option 13 from option 25 MUST contain statuscode 3.	
	
	References: RFC 3633, Section: 12.2	

@v6 @dhcp6 @PD @rfc3633
    Scenario: prefix.delegation.IA_and_PD_renew
  
    # this tests will be disabled after RFC 7550 tests will be added

 	Test Setup:
	#Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
    Server is configured with 3000::/64 subnet with 3000::ffff:ffff:1-3000::ffff:ffff:3 pool.
	Server is configured with 2001:db8:1:: prefix in subnet 0 with 90 prefix length and 92 delegated prefix length.
	DHCP server is started.
	
	Test Procedure:
	Client does include IA-PD.
	Client does include client-id.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client saves IA_PD option from received message.
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client does include client-id.
    Client does include IA-NA.
    Client sends RENEW message.


	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26. 
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain validlft 4000.

	References: RFC 3633, Section: 12.2

@v6 @dhcp6 @PD @rfc3633 @disabled
  # disabled after RFC 7550
	Scenario: prefix.delegation.IA_and_PD_renew_nobindig
	
    # this tests will be disabled after RFC 7550 tests will be added

 	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	Server is configured with 2001:db8:1:: prefix in subnet 0 with 90 prefix length and 92 delegated prefix length.
	DHCP server is started.
	
	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client does include IA-PD.
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	#Response sub-option 13 from option 25 MUST contain statuscode 3. changed after rfc7550
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 13.
	Response sub-option 13 from option 3 MUST contain statuscode 3.

	References: RFC 3633, Section: 12.2
