Feature: Standard DHCPv6 information request message 
    This feature is designed for checking server response for invalid information request messages. RFC 3315 section 15.12 Tests expecting lack of response, so each test also send valid massage to make sure that server is still running.
    
@v6 @inforequest_invalid
    Scenario: v6.inforequest.invalid.without_server_id

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.12
	
@v6 @inforequest_invalid
    Scenario: v6.inforequest.invalid.wrong_server_id

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client does include wrong-server-id.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.12 

@v6 @inforequest_invalid @wrong_option
    Scenario: v6.inforequest.invalid.wrong_option

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
	Client does include preference.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15, 15.12 

@v6 @inforequest_invalid 
    Scenario: v6.inforequest.invalid.with_IA

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.12 
	
	
		