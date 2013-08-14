
Feature: Standard DHCPv6 rebind message 
    This feature is designed for checking server response for invalid rebind messages. RFC 3315 section 15.7 Tests expecting lack of response, so each test also send valid massage to make sure that server is still running.
    
@v6 @rebind_invalid
    Scenario: v6.rebind.invalid.without_client_id

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client does NOT include client-id.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.
	
	Test Procedure:
	Client requests option 7.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	
	References: RFC3315 section 15.7
	
@v6 @rebind_invalid 
    Scenario: v6.rebind.invalid.blank_client_id

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client does include wrong-client-id.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.
	
	Test Procedure:
	Client requests option 7.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	
	References: RFC3315 section 15.7
	
@v6 @rebind_invalid
    Scenario: v6.rebind.invalid.with_server_id

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
	Client sends REBIND message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.
	
	Test Procedure:
	Client requests option 7.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	
	References: RFC3315 section 15.7
	
	
@v6 @rebind_invalid @invalid_option @outline
    Scenario Outline: v6.rebind.invalid.options.outline

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client does include <opt_name>.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.
	
	Test Procedure:
	Client requests option 7.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	
	References: RFC3315 section 15, 15.7
	
	Examples:
	| opt_name       |
	| relay-msg      |
	| rapid-commit   |
	| interface-id   |
	| preference     |
	| server-unicast |
	| status-code    | 
	| reconfigure    |