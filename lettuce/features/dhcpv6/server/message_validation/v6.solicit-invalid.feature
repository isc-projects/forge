
Feature: Standard DHCPv6 solicit message 
    This feature is designed for checking server response for invalid solicit messages. RFC 3315 section 15.2 Tests expecting lack of response, so each test also send valid massage to make sure that server is still running. Also parts of tests with valid message refers to RFC 17.2.1  
    
@v6 @dhcp6 @solicit_invalid
    Scenario: v6.solicit.invalid.without_client_id
    ## Testing server ability to discard message that not meets 
    ## content requirements.
    ## In this case: SOLICIT without CLIENT_ID option.
	## Message details 		Client		Server
	## without CLIENT_ID	SOLICIT -->
	## 		   						 X	ADVERTISE
	## correct message 		SOLICIT -->
	## 		   						<--	ADVERTISE
	## Pass Criteria:
	## 				Advertise MUST include option:
	##					client-id
	##					server-id
	##					IA-NA

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	#message wont contain client-id option
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.
	
	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	
	References: RFC3315 section 15.2, 17.2.1

@v6 @dhcp6 @solicit_invalid
    Scenario: v6.solicit.invalid.double_client_id
    ## Testing server ability to discard message that not meets
    ## content requirements.
    ## In this case: SOLICIT without CLIENT_ID option.
	## Message details 		Client		Server
	## without CLIENT_ID	SOLICIT -->
	## 		   						 X	ADVERTISE
	## correct message 		SOLICIT -->
	## 		   						<--	ADVERTISE
	## Pass Criteria:
	## 				Advertise MUST include option:
	##					client-id
	##					server-id
	##					IA-NA

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client does include client-id.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.

	References: RFC3315 section 15.2, 17.2.1


@v6 @dhcp6 @solicit_invalid
    Scenario: v6.solicit.invalid.with_server_id
    ## Testing server ability to discard message that not meets 
    ## content requirements.
    ## In this case: SOLICIT with SERVER_ID option.
	## Message details 		Client		Server
	## 				 		SOLICIT -->
	## 		   						<--	ADVERTISE
	## with SERVER_ID		SOLICIT -->
	## 		   						 X	ADVERTISE
	## correct message 		SOLICIT -->
	## 		   						<--	ADVERTISE
	## Pass Criteria:
	## 				Advertise MUST include option:
	##					client-id
	##					server-id
	##					IA-NA

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
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.
	
	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.

	References: RFC3315 section 15.2, 17.2.1

@v6 @dhcp6 @solicit_invalid
    Scenario: v6.solicit.invalid.with_blank_client_id
    ## Testing server ability to discard message that not meets 
    ## content requirements.
    ## In this case: SOLICIT with incorrect CLIENT_ID option.
	## Message details 		Client		Server
	## incorrect CLIENT_ID	SOLICIT -->
	## 		   						 X	ADVERTISE
	## correct message 		SOLICIT -->
	## 		   						<--	ADVERTISE
	## Pass Criteria:
	## 				Advertise MUST include option:
	##					client-id
	##					server-id
	##					IA-NA

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include empty-client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.
	
	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.

	References: RFC3315 section 15.2, 17.2.1


@v6 @dhcp6 @solicit_invalid @invalid_option
    Scenario: v6.solicit.invalid.options-relaymsg
	## Temporary test replacing disabled outline scenario 
	## Testing server ability to discard message that not meets 
	## content requirements.
	## Message details 		Client		Server
	## with restricted 
	## option				SOLICIT -->
	## 		   						 X	ADVERTISE
	## correct message 		SOLICIT -->
	## 		   						<--	ADVERTISE
	## Pass Criteria:
	## 				Advertise MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
		 
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
	Client does include relay-msg.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.
	
	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
		
	References: RFC3315 section 15.2, 17.2.1, table A: Appearance of Options in Message Types

@v6 @dhcp6 @solicit_invalid @invalid_option
    Scenario: v6.solicit.invalid.options-interfaceid
	## Temporary test replacing disabled outline scenario 
	## Testing server ability to discard message that not meets 
	## content requirements.
	## Message details 		Client		Server
	## with restricted 
	## option				SOLICIT -->
	## 		   						 X	ADVERTISE
	## correct message 		SOLICIT -->
	## 		   						<--	ADVERTISE 
	## Pass Criteria:
	## 				Advertise MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client does include interface-id.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.
	
	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
		
	References: RFC3315 section 15.2, 17.2.1, table A: Appearance of Options in Message Types

@v6 @dhcp6 @solicit_invalid @invalid_option
    Scenario: v6.solicit.invalid.options-preference
	## Temporary test replacing disabled outline scenario 
	## Testing server ability to discard message that not meets 
	## content requirements.
	## Message details 		Client		Server
	## with restricted 
	## option				SOLICIT -->
	## 		   						 X	ADVERTISE
	## correct message 		SOLICIT -->
	## 		   						<--	ADVERTISE 
	## Pass Criteria:
	## 				Advertise MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client does include preference.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.
	
	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
		
	References: RFC3315 section 15.2, 17.2.1, table A: Appearance of Options in Message Types

@v6 @dhcp6 @solicit_invalid @invalid_option
    Scenario: v6.solicit.invalid.options-serverunicast
	## Temporary test replacing disabled outline scenario 
	## Testing server ability to discard message that not meets 
	## content requirements.
	## Message details 		Client		Server
	## with restricted 
	## option				SOLICIT -->
	## 		   						 X	ADVERTISE
	## correct message 		SOLICIT -->
	## 		   						<--	ADVERTISE 
	## Pass Criteria:
	## 				Advertise MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client does include server-unicast.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.
	
	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
		
	References: RFC3315 section 15.2, 17.2.1, table A: Appearance of Options in Message Types

@v6 @dhcp6 @solicit_invalid @invalid_option
    Scenario: v6.solicit.invalid.options-statuscode
	## Temporary test replacing disabled outline scenario 
	## Testing server ability to discard message that not meets 
	## content requirements.
	## Message details 		Client		Server
	## with restricted 
	## option				SOLICIT -->
	## 		   						 X	ADVERTISE
	## correct message 		SOLICIT -->
	## 		   						<--	ADVERTISE 
	## Pass Criteria:
	## 				Advertise MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client does include status-code.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.
	
	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.

	References: RFC3315 section 15.2, 17.2.1, table A: Appearance of Options in Message Types

@v6 @dhcp6 @solicit_invalid @invalid_option
    Scenario: v6.solicit.invalid.options-reconfigure
	## Temporary test replacing disabled outline scenario 
	## Testing server ability to discard message that not meets 
	## content requirements.
	## Message details 		Client		Server
	## with restricted 
	## option				SOLICIT -->
	## 		   						 X	ADVERTISE
	## correct message 		SOLICIT -->
	## 		   						<--	ADVERTISE
	## Pass Criteria:
	## 				Advertise MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client does include reconfigure.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.
	
	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
		
	References: RFC3315 section 15.2, 17.2.1, table A: Appearance of Options in Message Types