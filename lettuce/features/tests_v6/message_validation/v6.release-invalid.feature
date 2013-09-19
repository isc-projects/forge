
Feature: Standard DHCPv6 release message 
    This feature is designed for checking server response for invalid release messages. RFC 3315 section 15.9 Tests expecting lack of response, so each test also send valid massage to make sure that server is still running.
    
@v6 @release_invalid
    Scenario: v6.release.invalid.without_server_id

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.9
	
@v6 @release_invalid
    Scenario: v6.release.invalid.wrong_server_id

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client does include wrong-server-id.
	Client requests option 7.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.9 
	
@v6 @release_invalid 
    Scenario: v6.release.invalid.without_client_id

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
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.9

@v6 @release_invalid
    Scenario: v6.release.invalid.blank_client_id

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
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.9
	
	
@v6 @release_invalid @invalid_option @outline
    Scenario: v6.release.invalid.options-relay-msg

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
	Client does include relay-msg.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.9

@v6 @release_invalid @invalid_option @outline
    Scenario: v6.release.invalid.options-rapid-commit

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
	Client does include rapid-commit.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.9

@v6 @release_invalid @invalid_option @outline
    Scenario: v6.release.invalid.options-interface-id

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
	Client does include interface-id.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.9
	
@v6 @release_invalid @invalid_option @outline
    Scenario: v6.release.invalid.options-reconfigure-accept

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
	Client does include reconfigure-accept.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.9
	
@v6 @release_invalid @invalid_option @outline
    Scenario: v6.release.invalid.options-preference

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
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.9
	
@v6 @release_invalid @invalid_option @outline
    Scenario: v6.release.invalid.options-server-unicast

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
	Client does include server-unicast.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.9
	
@v6 @release_invalid @invalid_option @outline
    Scenario: v6.release.invalid.options-status-code

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
	Client does include status-code.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.9
	
@v6 @release_invalid @invalid_option @outline
    Scenario: v6.release.invalid.options-reconfigure

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
	Client does include reconfigure.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 15.9
	