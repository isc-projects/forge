
Feature: Standard DHCPv6 decline message 
    This feature is designed for checking server response for invalid decline messages. RFC 3315 section 15.8 Tests expecting lack of response, so each test also send valid massage to make sure that server is still running.
    
@v6 @decline_invalid
    Scenario: v6.decline.invalid.without_server_id
    ## Testing server ability to discard message that not meets 
    ## content requirements.
    ## In this case: DECLINE without SERVER_ID
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## without SERVER_ID	DECLINE -->
	##					  		     X	REPLY
	## 						SOLICIT -->
	## (copy server_id)				<--	ADVERTISE
	## correct message 		DECLINE -->
	##					  		    <--	REPLY
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
	Client requests option 7.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
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
	Client adds saved options. And Erase.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 2.
	Response MUST include option 13.
	
	References: RFC3315 section 15.8
	
@v6 @decline_invalid
    Scenario: v6.decline.invalid.wrong_server_id
    ## Testing server ability to discard message that not meets 
    ## content requirements.
    ## In this case: DECLINE with incorrect SERVER_ID
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## incorrect SERVER_ID	DECLINE -->
	##					  		     X	REPLY
	## 						SOLICIT -->
	## (copy server_id)				<--	ADVERTISE
	## correct message 		DECLINE -->
	##					  		    <--	REPLY
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
	Client requests option 7.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client does include wrong-server-id.
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
	Client adds saved options. And Erase.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 2.
	Response MUST include option 13.
	
	References: RFC3315 section 15.8
	
@v6 @decline_invalid 
    Scenario: v6.decline.invalid.without_client_id
    ## Testing server ability to discard message that not meets 
    ## content requirements.
    ## In this case: DECLINE without CLIENT_ID
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## without CLIENT_ID	DECLINE -->
	##					  		     X	REPLY
	## correct message 		DECLINE -->
	##					  		    <--	REPLY
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
	Client requests option 7.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client does NOT include client-id.
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 2.
	Response MUST include option 13.
	
	References: RFC3315 section 15.8

@v6 @decline_invalid
    Scenario: v6.decline.invalid.blank_client_id
    ## Testing server ability to discard message that not meets 
    ## content requirements.
    ## In this case: DECLINE with blank CLIENT_ID
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## incorrect CLIENT_ID	DECLINE -->
	##					  		     X	REPLY
	## correct message 		DECLINE -->
	##					  		    <--	REPLY
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
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client does include wrong-client-id.
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 2.
	Response MUST include option 13.
	
	References: RFC3315 section 15.8
		
@v6 @decline_invalid @invalid_option @outline
    Scenario: v6.decline.invalid.options-relay-msg
	## Temporary test replacing disabled outline scenario 
	## Testing server ability to discard message that not meets 
	## content requirements.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## with restricted 
	## option				DECLINE -->
	##					  		     X	REPLY
	## correct message 		DECLINE -->
	##					  		    <--	REPLY
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.
	
	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client adds saved options. And DONT Erase.
	Client does include relay-msg.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 2.
	Response MUST include option 13.
	
	References: RFC3315 section 15.8 22.8.

@v6 @decline_invalid @invalid_option @outline
    Scenario: v6.decline.invalid.options-rapid-commit
	## Temporary test replacing disabled outline scenario 
	## Testing server ability to discard message that not meets 
	## content requirements.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## with restricted 
	## option				DECLINE -->
	##					  		     X	REPLY
	## correct message 		DECLINE -->
	##					  		    <--	REPLY

	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.
	
	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client adds saved options. And DONT Erase.
	Client does include rapid-commit.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 2.
	Response MUST include option 13.
	
	References: RFC3315 section 15.8 22.8.

@v6 @decline_invalid @invalid_option @outline
    Scenario: v6.decline.invalid.options-interface-id
	## Temporary test replacing disabled outline scenario 
	## Testing server ability to discard message that not meets 
	## content requirements.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## with restricted 
	## option				DECLINE -->
	##					  		     X	REPLY
	## correct message 		DECLINE -->
	##					  		    <--	REPLY

	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.
	
	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client adds saved options. And DONT Erase.
	Client does include interface-id.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 2.
	Response MUST include option 13.
	
	References: RFC3315 section 15.8 22.8.

@v6 @decline_invalid @invalid_option @outline
    Scenario: v6.decline.invalid.options-reconfigure-accept
	## Temporary test replacing disabled outline scenario 
	## Testing server ability to discard message that not meets 
	## content requirements.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## with restricted 
	## option				DECLINE -->
	##					  		     X	REPLY
	## correct message 		DECLINE -->
	##					  		    <--	REPLY

	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.
	
	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client adds saved options. And DONT Erase.
	Client does include reconfigure-accept.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 2.
	Response MUST include option 13.
	
	References: RFC3315 section 15.8 22.8.

@v6 @decline_invalid @invalid_option @outline
    Scenario: v6.decline.invalid.options-preference
	## Temporary test replacing disabled outline scenario 
	## Testing server ability to discard message that not meets 
	## content requirements.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## with restricted 
	## option				DECLINE -->
	##					  		     X	REPLY
	## correct message 		DECLINE -->
	##					  		    <--	REPLY

	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.
	
	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client adds saved options. And DONT Erase.
	Client does include preference.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 2.
	Response MUST include option 13.
	
	References: RFC3315 section 15.8 22.8.
	
@v6 @decline_invalid @invalid_option @outline
    Scenario: v6.decline.invalid.options-server-unicast
	## Temporary test replacing disabled outline scenario 
	## Testing server ability to discard message that not meets 
	## content requirements.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## with restricted 
	## option				DECLINE -->
	##					  		     X	REPLY
	## correct message 		DECLINE -->
	##					  		    <--	REPLY

	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.
	
	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client adds saved options. And DONT Erase.
	Client does include server-unicast.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 2.
	Response MUST include option 13.
	
	References: RFC3315 section 15.8 22.8.
	
@v6 @decline_invalid @invalid_option @outline
    Scenario: v6.decline.invalid.options-status-code
	## Temporary test replacing disabled outline scenario 
	## Testing server ability to discard message that not meets 
	## content requirements.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## with restricted 
	## option				DECLINE -->
	##					  		     X	REPLY
	## correct message 		DECLINE -->
	##					  		    <--	REPLY

	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.
	
	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client adds saved options. And DONT Erase.
	Client does include status-code.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 2.
	Response MUST include option 13.
	
	References: RFC3315 section 15.8 22.8.
	
@v6 @decline_invalid @invalid_option @outline
    Scenario: v6.decline.invalid.options-reconfigure
	## Temporary test replacing disabled outline scenario 
	## Testing server ability to discard message that not meets 
	## content requirements.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## with restricted 
	## option				DECLINE -->
	##					  		     X	REPLY
	## correct message 		DECLINE -->
	##					  		    <--	REPLY

	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.
	
	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client adds saved options. And DONT Erase.
	Client does include reconfigure.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 2.
	Response MUST include option 13.
	
	References: RFC3315 section 15.8 22.8.