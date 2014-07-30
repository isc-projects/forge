
Feature: DHCPv6 Relay Agent 
    This is test for DHCPv6 message exchange between server and relay-agent with not permitted options in Relay-Forward message.  

@v6 @relay @relay_invalid
    Scenario: v6.relay.invalid.with_client_id

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.
	
	#add options to relay message
	Client does include wrong-client-id.
	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST respond with RELAYREPLY message.

	References: RFC3315 section 18.2.8	
	
@v6 @relay @relay_invalid
    Scenario: v6.relay.invalid.with_server_id
	#add just serverid
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.
	
	#add options to relay message
	Client does include wrong-server-id.
	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST respond with RELAYREPLY message.

	References: RFC3315 section 18.2.8

@v6 @relay @relay_invalid @invalid_option @outline
    Scenario: v6.relay.invalid.options-preference
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.
	
	#add options to relay message
	Client does include preference.
	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST respond with RELAYREPLY message.

	References: RFC3315 section 18.2.8
	
@v6 @relay @relay_invalid @invalid_option @outline
    Scenario: v6.relay.invalid.options-time
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.
	
	#add options to relay message
	Client does include time.
	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST respond with RELAYREPLY message.

	References: RFC3315 section 18.2.8
	
@v6 @relay @relay_invalid @invalid_option @outline
    Scenario: v6.relay.invalid.options-option-request
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.
	
	#add options to relay message
	Client does include option-request.
	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.
	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST respond with RELAYREPLY message.

	References: RFC3315 section 18.2.8
	
@v6 @relay @relay_invalid @invalid_option @outline
    Scenario: v6.relay.invalid.options-server-unicast
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.
	
	#add options to relay message
	Client does include server-unicast.
	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST respond with RELAYREPLY message.

	References: RFC3315 section 18.2.8
	
@v6 @relay @relay_invalid @invalid_option @outline
    Scenario: v6.relay.invalid.options-status-code
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.
	
	#add options to relay message
	Client does include status-code.
	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST respond with RELAYREPLY message.

	References: RFC3315 section 18.2.8
	
@v6 @relay @relay_invalid @invalid_option @outline
    Scenario: v6.relay.invalid.options-rapid-commit
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.
	
	#add options to relay message
	Client does include rapid-commit.
	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST respond with RELAYREPLY message.

	References: RFC3315 section 18.2.8
	
@v6 @relay @relay_invalid @invalid_option @outline
    Scenario: v6.relay.invalid.options-reconfigure
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.
	
	#add options to relay message
	Client does include reconfigure.
	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST respond with RELAYREPLY message.

	References: RFC3315 section 18.2.8
	
@v6 @relay @relay_invalid @invalid_option @outline
    Scenario: v6.relay.invalid.options-reconfigure-accept
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.
	
	#add options to relay message
	Client does include reconfigure-accept.
	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST respond with RELAYREPLY message.

	References: RFC3315 section 18.2.8
