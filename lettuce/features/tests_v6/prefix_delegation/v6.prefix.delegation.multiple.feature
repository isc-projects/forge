Feature: DHCPv6 Prefix Delegation 
    Test for Prefix Delegation using Request messages,multiple IA/PD in one request, based on RFC 3633.
	
@v6 @PD @rfc3633 @multiplePD
    Scenario: prefix.delegation.multiplePD.request
    
   	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	#
	
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
	Response MUST include option 25.
	Response option 25 MUST contain prefix 3000:1::3. #depends on configuration!
	#and other...

@v6 @PD @rfc3633 @multiplePD
    Scenario: prefix.delegation.multiplePD.and.IA.request
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::4 pool.
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
	Response option 25 MUST contain prefix 3000:1::3. #depends on configuration!
	#and other...
	#4x IA address and 4x prefix
	
	
@v6 @PD @rfc3633 @multiplePD
    Scenario: prefix.delegation.multiplePD.and.IA.request.partial.success
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::2 pool.
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
	Response option 25 MUST contain prefix 3000:1::3. #depends on configuration!
	#and other...
	#4x IA address and 4x prefix, both 2 success and 2 fails