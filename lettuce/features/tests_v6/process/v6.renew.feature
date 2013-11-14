Feature: DHCPv6 Renew
    Those are tests for renew - reply exchange.
    
@v6 @renew
    Scenario: v6.message.renew-reply
  
 	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::5-3000::55 pool.
	Server is started.
	
	Test Procedure:
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	

	References: RFC 3315, Section: 18.2.3.
	
@v6 @renew
    Scenario: v6.message.renew-reply-time-zero
  
  	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::55-3000::55 pool.
	Server is started.
	
	Test Procedure:
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Server is configured with 3000::/64 subnet with 3000::100-3000::155 pool.
	Server is started.

	Test Procedure:
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client copies server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	Response sub-option 5 from option 3 MUST contain address 3000::55.
	Response sub-option 5 from option 3 MUST contain validlft 0.

	References: RFC 3315, Section: 18.2.3.