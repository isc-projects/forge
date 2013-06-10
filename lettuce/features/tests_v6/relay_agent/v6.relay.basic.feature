
Feature: DHCPv6 Relay Agent 
    This is a simple DHCPv6 message exchange between server and relay-agent.  

@v6 @relay @basic 
    Scenario: v6.realy.message.solicit-advertise

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.
	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST respond with RELAY-REPLY message.

	References: RFC3315 section 18.2.8
