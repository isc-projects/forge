Feature: Multiple Identity Association Option in single DHCPv6 message
    This feature testing ability distinguish multiple IA_NA options and concurrent processing of those options.
  
@v6 @multipleIA
    Scenario: v6.multipleIA.addresses
  
 	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Generate new IA.
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Generate new IA.
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client copies server-id option from received message.
	Client adds saved options. And Erase.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.  
	Response MUST include option 3.
	Response option 3 MUST contain address 3000::1.
	Response option 3 MUST contain address 3000::2.
	Response option 3 MUST contain address 3000::3.
	
	
@v6 @multipleIA
    Scenario: v6.multipleIA.addresses.release.success
  
 	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Generate new IA.
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Generate new IA.
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client copies server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.  
	Response MUST include option 3.
	Response option 3 MUST contain address 3000::1.
	Response option 3 MUST contain address 3000::2.
	Response option 3 MUST contain address 3000::3.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 13. 
	Response option 13 MUST contain statuscode 0.
	
@v6 @multipleIA
    Scenario: v6.multipleIA.addresses.release.partial.success
  
 	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Generate new IA.
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Generate new IA.
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client copies server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.  
	Response MUST include option 3.
	Response option 3 MUST contain address 3000::1.
	Response option 3 MUST contain address 3000::2.
	Response option 3 MUST contain address 3000::3.
	
	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 13. 
	Response option 13 MUST contain statuscode 0.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 13. 
	Response option 13 MUST contain statuscode 0.
	Response option 13 MUST contain statuscode 3.	
	
@v6 @multipleIA
    Scenario: v6.multipleIA.addresses.rebind.partial.success
  
 	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Generate new IA.
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Generate new IA.
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client copies server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.  
	Response MUST include option 3.
	Response option 3 MUST contain address 3000::1.
	Response option 3 MUST contain address 3000::2.
	Response option 3 MUST contain address 3000::3.
	
	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 13. 
	Response option 13 MUST contain statuscode 0.
	
	Test Procedure:
	Client adds saved options. And DONT Erase.
	Client sends REBIND message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 13. 
	Response option 13 MUST contain statuscode 0.
	Response option 13 MUST contain statuscode 3.	
	
@v6 @multipleIA
    Scenario: v6.multipleIA.addresses.noaddravail
 	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::2 pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Generate new IA.
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Generate new IA.
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client copies server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.  
	Response MUST include option 3.
	Response option 3 MUST contain address 3000::1.
	Response option 3 MUST contain address 3000::2.
	Response option 3 MUST contain sub-option 13. 
	Response option 13 MUST contain statuscode 2.