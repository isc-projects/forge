
Feature: DHCPv6 Relay Agent 
    This is a simple DHCPv6 message exchange between server and relay-agent.  

@v6 @relay 
    Scenario: v6.relay.message.solicit-advertise
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.
	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
	Response MUST include option 9.
	Response option 9 MUST contain message 2.
	#message 2 - Advertise
	
	References: RFC3315 section 18.2.8
	
@v6 @relay 
    Scenario: v6.relay.message.solicit-reply

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client does include rapid-commit.
	Client sends SOLICIT message.
	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
	#Response MUST include REPLY message.
	
	References: RFC3315 section 18.2.8
	
@v6 @relay
    Scenario: v6.relay.message.request-reply

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 7.
	Client sends REQUEST message.
	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
	#Response MUST include REPLY message.
	
	References: RFC3315 section 18.2.8
	
	
@v6 @relay 
    Scenario: v6.relay.message.confirm-reply

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client sends CONFIRM message.
	...using relay-agent encapsulated in 1 level.

	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
	#Response MUST include REPLY message.
	
	References: RFC3315 section 18.2.8
	
@v6 @relay
    Scenario: v6.relay.message.renew-reply

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 7.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends RENEW message.
	...using relay-agent encapsulated in 1 level.

	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
	#Response MUST include REPLY message.
	
	References: RFC3315 section 18.2.8 
	
@v6 @relay
    Scenario: v6.relay.message.rebind-reply

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 7.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client sends REBIND message.
	...using relay-agent encapsulated in 1 level.

	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
	#Response MUST include REPLY message.
	
	References: RFC3315 section 18.2.8
	 
@v6 @relay 
    Scenario: v6.relay.message.release-reply

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 7.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends RELEASE message.
	...using relay-agent encapsulated in 1 level.

	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
	#Response MUST include REPLY message.
	
	References: RFC3315 section 18.2.8 
	
@v6 @relay 
    Scenario: v6.relay.message.decline-reply

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends DECLINE message.
	...using relay-agent encapsulated in 1 level.

	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
	#Response MUST include REPLY message.
	
	References: RFC3315 section 18.2.8
	
@v6 @relay  
    Scenario: v6.relay.message.information_request-reply
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends INFOREQUEST message.
	...using relay-agent encapsulated in 1 level.

	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
	#Response MUST include REPLY message.
	
	References: RFC3315 section 18.2.8
	