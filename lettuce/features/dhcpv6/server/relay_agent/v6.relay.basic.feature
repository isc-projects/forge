
Feature: DHCPv6 Relay Agent 
    This is a simple DHCPv6 message exchange between server and relay-agent.  

@v6 @dhcp6 @relay
    Scenario: v6.relay.message-solicit-advertise
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
    Response MUST include option 18.
	Response MUST include option 9.
	#Response option 9 MUST contain message 2.
	#message 2 - Advertise
	
	References: RFC3315 section 18.2.8

@v6 @dhcp6 @relay @unicast
    Scenario: v6.relay.message-unicast-global
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Client chooses GLOBAL UNICAST address.
	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
    Response MUST include option 18.
	Response MUST include option 9.

	References: RFC3315 section 18.2.8

@v6 @dhcp6 @relay @unicast
    Scenario: v6.relay.message-unicast-local
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Client chooses LINK_LOCAL UNICAST address.
	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.
	Response MUST include option 9.
	
	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
    Response MUST include option 18.
	Response MUST include option 9.
	
	References: RFC3315 section 18.2.8
	
@v6 @dhcp6 @relay
    Scenario: v6.relay.message-solicit-reply

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client does include rapid-commit.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

    RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
    Response MUST include option 18.
	Response MUST include option 9.
	#Response MUST include REPLY message.
	
	References: RFC3315 section 18.2.8
	
@v6 @dhcp6 @relay
    Scenario: v6.relay.message-request-reply

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client requests option 7.
	Client does include client-id.
    Client sends REQUEST message.

	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
    Response MUST include option 18.
	Response MUST include option 9.
	#Response MUST include REPLY message.
	
	References: RFC3315 section 18.2.8
	
	
@v6 @dhcp6 @relay
    Scenario: v6.relay.message-confirm-reply

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client requests option 7.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client does include client-id.
    Client sends CONFIRM message.

	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 1 level.

	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
    Response MUST include option 18.
	Response MUST include option 9.
	#Response MUST include REPLY message.
	
	References: RFC3315 section 18.2.8
	
@v6 @dhcp6 @relay
    Scenario: v6.relay.message-renew-reply

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
    Client copies IA_NA option from received message.
    Client requests option 7.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends RENEW message.

	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 1 level.

	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
    Response MUST include option 18.
	Response MUST include option 9.
	#Response MUST include REPLY message.
	
	References: RFC3315 section 18.2.8 
	
@v6 @dhcp6 @relay
    Scenario: v6.relay.message-rebind-reply

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client does include client-id.
    Client sends REBIND message.

	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 1 level.

	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
    Response MUST include option 18.
	Response MUST include option 9.
	#Response MUST include REPLY message.
	
	References: RFC3315 section 18.2.8
	 
@v6 @dhcp6 @relay
    Scenario: v6.relay.message-release-reply

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends RELEASE message.

	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 1 level.

	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
    Response MUST include option 18.
	Response MUST include option 9.
	#Response MUST include REPLY message.
	
	References: RFC3315 section 18.2.8 
	
@v6 @dhcp6 @relay
    Scenario: v6.relay.message-decline-reply

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends DECLINE message.

	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 1 level.

	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
    Response MUST include option 18.
	Response MUST include option 9.
	#Response MUST include REPLY message.
	
	References: RFC3315 section 18.2.8
	
@v6 @dhcp6 @relay
    Scenario: v6.relay.message-information_request-reply
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends INFOREQUEST message.

	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 1 level.

	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
    Response MUST include option 18.
	Response MUST include option 9.
	#Response MUST include REPLY message.
	
	References: RFC3315 section 18.2.8
	