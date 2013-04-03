
Feature: Standard DHCPv6 renew message 
    This feature is designed for checking server response for invalid renew messages. RFC 3315 section 15.6 Tests expecting lack of response, so each test also send valid massage to make sure that server is still running.
    
@v6 @renew_invalid
    Scenario: v6.renew.invalid.without_server_id

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.6
	
@v6 @renew_invalid
    Scenario: v6.renew.invalid.wrong_server_id

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client does include wrong-server-id.
	Client requests option 7.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.6 
	
@v6 @renew_invalid 
    Scenario: v6.renew.invalid.without_client_id

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
	Client does NOT include client-id.
	Client requests option 7.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.6

@v6 @renew_invalid
    Scenario: v6.renew.invalid.wrong_client_id

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
	Client does include wrong-client-id.
	Client requests option 7.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.6
	
@v6 @renew_invalid @wrong_option
    Scenario: v6.renew.invalid.wrong_option

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
	Client requests option 0.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15, 15.6