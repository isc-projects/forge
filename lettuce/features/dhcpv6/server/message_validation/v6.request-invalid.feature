
Feature: Standard DHCPv6 request message 
    This feature is designed for checking server response for invalid request messages. RFC 3315 section 15.4 Tests expecting lack of response, so each test also send valid massage to make sure that server is still running.
    
@v6 @request_invalid 
    Scenario: v6.request.invalid.without_server_id
    ## Testing server ability to discard message that not meets 
    ## content requirements.
    ## In this case: REQUEST without SERVER_ID option.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## without SERVER_ID	REQUEST -->
	##					  		     X	REPLY
	## 						SOLICIT -->
	## copy SERVER_ID				<--	ADVERTISE
	## correct message 		REQUEST -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	##					IA-Address

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client adds saved options. And Erase.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	References: RFC3315 section 15.4
	
@v6 @request_invalid 
    Scenario: v6.request.invalid.without_client_id
    ## Testing server ability to discard message that not meets 
    ## content requirements.
    ## In this case: REQUEST without CLIENT_ID option.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## without CLIENT_ID	REQUEST -->
	##					  		     X	REPLY
	## correct message 		REQUEST -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	##					IA-Address
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves server-id option from received message.
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client does NOT include client-id.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	References: RFC3315 section 15.4 

@v6 @request_invalid
    Scenario: v6.request.invalid.wrong_server_id
    ## Testing server ability to discard message that not meets 
    ## content requirements.
    ## In this case: REQUEST with incorrect SERVER_ID option.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## incorrect SERVER_ID	REQUEST -->
	##					  		     X	REPLY
	## 						SOLICIT -->
	## copy SERVER_ID				<--	ADVERTISE
	## correct message 		REQUEST -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	##					IA-Address
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client does include wrong-server-id.
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client adds saved options. And Erase.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	References: RFC3315 section 15.4 
	
@v6 @request_invalid
    Scenario: v6.request.invalid.blank_client_id
    ## Testing server ability to discard message that not meets 
    ## content requirements.
    ## In this case: REQUEST with incorrect CLIENT_ID option.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## incorrect CLIENT_ID	REQUEST -->
	##					  		     X	REPLY
	## correct message 		REQUEST -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	##					IA-Address
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves server-id option from received message.
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client does include wrong-client-id.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	References: RFC3315 section 15.4 
	
@v6 @request_invalid @invalid_option @outline
    Scenario: v6.request.invalid.options-relay-msg
	## Temporary test replacing disabled outline scenario 
	## Testing server ability to discard message that not meets 
	## content requirements.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## with restricted 
	## option				REQUEST -->
	##					  		     X	REPLY
	## correct message 		REQUEST -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	##					IA-Address
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client does include relay-msg.
	Client saves server-id option from received message.
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	References: RFC3315 section 15.4, table A: Appearance of Options in Message Types
	
@v6 @request_invalid @invalid_option @outline
    Scenario: v6.request.invalid.options-rapid-commit
	## Temporary test replacing disabled outline scenario 
	## Testing server ability to discard message that not meets 
	## content requirements.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## with restricted 
	## option				REQUEST -->
	##					  		     X	REPLY
	## correct message 		REQUEST -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	##					IA-Address
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client does include rapid-commit.
	Client saves server-id option from received message.
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	References: RFC3315 section 15.4, table A: Appearance of Options in Message Types 
	
@v6 @request_invalid @invalid_option @outline
    Scenario: v6.request.invalid.options-interface-id
	## Temporary test replacing disabled outline scenario 
	## Testing server ability to discard message that not meets 
	## content requirements.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## with restricted 
	## option				REQUEST -->
	##					  		     X	REPLY
	## correct message 		REQUEST -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	##					IA-Address
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client does include interface-id.
	Client saves server-id option from received message.
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	References: RFC3315 section 15.4, table A: Appearance of Options in Message Types
	
@v6 @request_invalid @invalid_option @outline
    Scenario: v6.request.invalid.options-preference
	## Temporary test replacing disabled outline scenario 
	## Testing server ability to discard message that not meets 
	## content requirements.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## with restricted 
	## option				REQUEST -->
	##					  		     X	REPLY
	## correct message 		REQUEST -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	##					IA-Address
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client does include preference.
	Client saves server-id option from received message.
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	References: RFC3315 section 15.4, table A: Appearance of Options in Message Types
	
@v6 @request_invalid @invalid_option @outline
    Scenario: v6.request.invalid.options-server-unicast
	## Temporary test replacing disabled outline scenario 
	## Testing server ability to discard message that not meets 
	## content requirements.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## with restricted 
	## option				REQUEST -->
	##					  		     X	REPLY
	## correct message 		REQUEST -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	##					IA-Address
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client does include server-unicast.
	Client saves server-id option from received message.
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	References: RFC3315 section 15.4, table A: Appearance of Options in Message Types
	
@v6 @request_invalid @invalid_option @outline
    Scenario: v6.request.invalid.options-status-code
	## Temporary test replacing disabled outline scenario 
	## Testing server ability to discard message that not meets 
	## content requirements.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## with restricted 
	## option				REQUEST -->
	##					  		     X	REPLY
	## correct message 		REQUEST -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	##					IA-Address
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client does include status-code.
	Client saves server-id option from received message.
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	References: RFC3315 section 15.4, table A: Appearance of Options in Message Types
	
@v6 @request_invalid @invalid_option @outline
    Scenario: v6.request.invalid.options-reconfigure
	## Temporary test replacing disabled outline scenario 
	## Testing server ability to discard message that not meets 
	## content requirements.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## with restricted 
	## option				REQUEST -->
	##					  		     X	REPLY
	## correct message 		REQUEST -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	##					IA-Address
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client does include reconfigure.
	Client saves server-id option from received message.
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	References: RFC3315 section 15.4, table A: Appearance of Options in Message Types
