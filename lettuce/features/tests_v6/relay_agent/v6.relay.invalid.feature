
Feature: DHCPv6 Relay Agent 
    This is test for DHCPv6 message exchange between server and relay-agent with not permitted options in Reply-Forward message.  

@v6 @relay @relay_invalid
    Scenario: v6.relay.wrongoption.preference
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.
	
	#add options to relay message
	Client does include preference.
	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.

	References: RFC3315 section 18.2.8

@v6 @relay @relay_invalid
    Scenario: v6.relay.wrongoption.rapidcommit

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.
	
	#add options to relay message
	Client does include rapid-commit.
	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.

	References: RFC3315 section 18.2.8

@v6 @relay @relay_invalid
    Scenario: v6.relay.wrongoption.clientid

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.
	
	#add options to relay message
	Client does include wrong-client-id.
	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.

	References: RFC3315 section 18.2.8	
	
@v6 @relay @relay_invalid
    Scenario: v6.relay.wrongoption.serverid

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.
	
	#add options to relay message
	Client does include wrong-server-id.
	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.

	References: RFC3315 section 18.2.8
	
	
@v6 @relay @relay_invalid
    Scenario: v6.relay.wrongoption.time

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.
	
	#add options to relay message
	Client does include time.
	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.

	References: RFC3315 section 18.2.8