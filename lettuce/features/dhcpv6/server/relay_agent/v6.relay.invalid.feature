
Feature: DHCPv6 Relay Agent
    This is test for DHCPv6 message exchange between server and relay-agent with not permitted options in Relay-Forward message.

@v6 @dhcp6 @relay @relay_invalid @disabled
    Scenario: v6.relay.invalid-with_client_id

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	#add options to relay message
	RelayAgent does include client-id.
	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 1 level.

	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.

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

@v6 @dhcp6 @relay @relay_invalid @disabled
    Scenario: v6.relay.invalid-with_server_id
	#add just serverid

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.


	#add options to relay message
    RelayAgent sets server_id value to 00:01:00:01:52:7b:a8:f0:08:00:27:58:f1:e8.
	RelayAgent does include server-id.
	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 1 level.

	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.

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

@v6 @dhcp6 @relay @relay_invalid @invalid_option @outline @disabled
#TODO enable MAY condition in Forge then enable test
    Scenario: v6.relay.invalid-options-preference

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	#add options to relay message
	RelayAgent does include preference.
	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 1 level.

	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.

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

@v6 @dhcp6 @relay @relay_invalid @invalid_option @outline @disabled
#TODO enable MAY condition in Forge then enable test
    Scenario: v6.relay.invalid-options-time

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
    Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	#add options to relay message
	RelayAgent does include time.
	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 1 level.

	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.

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

@v6 @dhcp6 @relay @relay_invalid @invalid_option @outline @disabled
#TODO enable MAY condition in Forge then enable test
    Scenario: v6.relay.invalid-options-option-request

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	#add options to relay message
	Client requests option 7.
	RelayAgent does include interface-id.
RelayAgent forwards message encapsulated in 1 level.

	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.

	Test Procedure:
	Client requests option 7.
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

@v6 @dhcp6 @relay @relay_invalid @invalid_option @outline @disabled
#TODO enable MAY condition in Forge then enable test
    Scenario: v6.relay.invalid-options-server-unicast

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	#add options to relay message
	RelayAgent does include server-unicast.
	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 1 level.

	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.

	Test Procedure:
	Client requests option 7.
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

@v6 @dhcp6 @relay @relay_invalid @invalid_option @outline @disabled
#TODO enable MAY condition in Forge then enable test
    Scenario: v6.relay.invalid-options-status-code

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	#add options to relay message
	RelayAgent does include status-code.
	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 1 level.

	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.

	Test Procedure:
	Client requests option 7.
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

@v6 @dhcp6 @relay @relay_invalid @invalid_option @outline @disabled
#TODO enable MAY condition in Forge then enable test
    Scenario: v6.relay.invalid-options-rapid-commit

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	#add options to relay message
	RelayAgent does include rapid-commit.
	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 1 level.

	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.

	Test Procedure:
	Client requests option 7.
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

@v6 @dhcp6 @relay @relay_invalid @invalid_option @outline @disabled
#TODO enable MAY condition in Forge then enable test
    Scenario: v6.relay.invalid-options-reconfigure

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	#add options to relay message
	RelayAgent does include reconfigure.
	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 1 level.

	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.

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

@v6 @dhcp6 @relay @relay_invalid @invalid_option @outline @disabled
#TODO enable MAY condition in Forge then enable test
    Scenario: v6.relay.invalid-options-reconfigure-accept

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	#add options to relay message
	RelayAgent does include reconfigure-accept.
	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 1 level.

	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.

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