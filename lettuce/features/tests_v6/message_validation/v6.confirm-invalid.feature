
Feature: Standard DHCPv6 confirm message 
    This feature is designed for checking server response for invalid confirm messages. RFC 3315 section 15.5 Tests expecting lack of response, so each test also send valid massage to make sure that server is still running.
    
@v6 @confirm_invalid 
    Scenario: v6.confirm.invalid.without_client_id

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client does NOT include client-id.
	Client sends CONFIRM message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.
	
	Test Procedure:
	Client requests option 7.
	Client sends CONFIRM message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	
	References: RFC3315 section 15.5 
	
@v6 @confirm_invalid 
    Scenario: v6.confirm.invalid.wrong_client_id

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client does include wrong-client-id.
	Client sends CONFIRM message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.
	
	Test Procedure:
	Client requests option 7.
	Client sends CONFIRM message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	
	References: RFC3315 section 15.5 
	
@v6 @confirm_invalid 
    Scenario: v6.confirm.invalid.wrong_server_id

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client does include wrong-server-id.
	Client sends CONFIRM message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.
	
	Test Procedure:
	Client requests option 7.
	Client sends CONFIRM message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	
	References: RFC3315 section 15.5 
	
@v6 @confirm_invalid
    Scenario: v6.confirm.invalid.with_server_id

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
	Client sends CONFIRM message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.
	
	Test Procedure:
	Client requests option 7.
	Client sends CONFIRM message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	
	References: RFC3315 section 15.5 
	
@v6 @confirm_invalid @wrong_option 
    Scenario: v6.confirm.invalid.wrong_option

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client does include preference.
	Client sends CONFIRM message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.
	
	Test Procedure:
	Client requests option 7.
	Client sends CONFIRM message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	
	References: RFC3315 section 15.5. 22.8.