
Feature: Standard DHCPv6 decline message 
    This feature is designed for checking server response for invalid decline messages. RFC 3315 section 15.8 Tests expecting lack of response, so each test also send valid massage to make sure that server is still running.
    
@v6 @decline_invalid
    Scenario: v6.decline.invalid.without_server_id

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.8
	
@v6 @decline_invalid
    Scenario: v6.decline.invalid.wrong_server_id

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client does include wrong-server-id.
	Client requests option 7.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.8 
	
@v6 @decline_invalid 
    Scenario: v6.decline.invalid.without_client_id

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
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.8

@v6 @decline_invalid
    Scenario: v6.decline.invalid.blank_client_id

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
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.8
	
@v6 @decline_invalid @invalid_option @outline
    Scenario: v6.decline.invalid.options-relay-msg
	#valid messages exchange performed twice, before and after invalid message
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
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client does include relay-msg.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.8 22.8.

@v6 @decline_invalid @invalid_option @outline
    Scenario: v6.decline.invalid.options-rapid-commit
	#valid messages exchange performed twice, before and after invalid message
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
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client does include rapid-commit.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.8 22.8.

@v6 @decline_invalid @invalid_option @outline
    Scenario: v6.decline.invalid.options-interface-id
	#valid messages exchange performed twice, before and after invalid message
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
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client does include interface-id.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.8 22.8.

@v6 @decline_invalid @invalid_option @outline
    Scenario: v6.decline.invalid.options-reconfigure-accept
	#valid messages exchange performed twice, before and after invalid message
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
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client does include reconfigure-accept.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.8 22.8.

@v6 @decline_invalid @invalid_option @outline
    Scenario: v6.decline.invalid.options-preference
	#valid messages exchange performed twice, before and after invalid message
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
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client does include preference.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.8 22.8.

@v6 @decline_invalid @invalid_option @outline
    Scenario: v6.decline.invalid.options-server-unicast
	#valid messages exchange performed twice, before and after invalid message
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
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client does include server-unicast.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.8 22.8.

@v6 @decline_invalid @invalid_option @outline
    Scenario: v6.decline.invalid.options-status-code
	#valid messages exchange performed twice, before and after invalid message
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
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client does include status-code.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.8 22.8.

@v6 @decline_invalid @invalid_option @outline
    Scenario: v6.decline.invalid.options-reconfigure
	#valid messages exchange performed twice, before and after invalid message
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
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client does include reconfigure.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.8 22.8.
