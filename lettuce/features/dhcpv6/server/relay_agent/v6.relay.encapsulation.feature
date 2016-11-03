Feature: DHCPv6 Relay Agent encapsulation and Interface ID 
    This is a simple DHCPv6 message exchange between server and relay-agent using message encapsulation and Interface ID  

@v6 @dhcp6 @relay
    Scenario: v6.relay.message.interfaceid

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with interface-id option in subnet 0 with value 15.
	DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 1 levels.
	
	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
    Response MUST include option 18.
    Response MUST include option 9.
	#Response MUST include ADVERTISE message.
	
	References: RFC3315 section 18.2.8

@v6 @dhcp6 @relay
    Scenario: v6.relay.encapsulate.31lvl

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 31 levels.
	
	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
    Response MUST include option 18.
    Response MUST include option 9.
	#Response MUST include ADVERTISE message.
	
	References: RFC3315 section 18.2.8 20.

@v6 @dhcp6 @relay
    Scenario: v6.relay.encapsulate.15lvl

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
    Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 15 levels.
	
	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
    Response MUST include option 18.
    Response MUST include option 9.
	#Response MUST include ADVERTISE message.
	
	References: RFC3315 section 18.2.8 20.