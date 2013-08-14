
Feature: Standard DHCPv6 solicit message 
    This feature is designed for checking server response for invalid solicit messages. RFC 3315 section 15.2 Tests expecting lack of response, so each test also send valid massage to make sure that server is still running. Also parts of tests with valid message refers to RFC 17.2.1  
    
@v6 @solicit_invalid
    Scenario: v6.solicit.invalid.without_client_id

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client does NOT include client-id.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.
	
	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	References: RFC3315 section 15.2, 17.2.1
	
@v6 @solicit_invalid
    Scenario: v6.solicit.invalid.with_server_id

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client requests option 7.
	Client copies server-id option from received message.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.
	
	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	References: RFC3315 section 15.2, 17.2.1

@v6 @solicit_invalid 
    Scenario: v6.solicit.invalid.with_blank_client_id

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client does include wrong-client-id.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.
	
	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	References: RFC3315 section 15.2, 17.2.1
	
@v6 @solicit_invalid @invalid_option @outline
    Scenario Outline: v6.solicit.invalid.options.outline
	#This is outline scenario, Examples will be filled in <...>, each example makes new test scenario.
	 
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client does include <opt_name>.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.
	
	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	
	References: RFC3315 section 15.2, 17.2.1

	Examples:
	| opt_name       |
	| relay-msg      |
	| interface-id   |
