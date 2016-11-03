
Feature: Standard DHCPv6 decline message 
    This feature is designed for checking server response for invalid decline messages. RFC 3315 section 15.8 Tests expecting lack of response, so each test also send valid massage to make sure that server is still running.
    
@v6 @dhcp6 @decline_invalid
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
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code
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
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	#Response MUST include option 13.
	
	References: RFC3315 section 15.8
	
@v6 @dhcp6 @decline_invalid
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
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code
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
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
    Client sets server_id value to 00:01:00:01:52:7b:a8:f0:44:33:22:22:11:11.
	Client does include wrong-server-id.
	Client does include client-id.
    Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	#Response MUST include option 13. RFC 7550 change
	
	References: RFC3315 section 15.8


@v6 @dhcp6 @decline_invalid
    Scenario: v6.decline.invalid.empty_server_id
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
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code
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
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
    #Client sets server_id value to 00:01:00:01:52:7b:a8:f0:44:33:22:22:11:11.
	Client does include empty-server-id.
	Client does include client-id.
    Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	#Response MUST include option 13. RFC 7550 change

	References: RFC3315 section 15.8


@v6 @dhcp6 @decline_invalid
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
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code
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
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	#message wont contain client-id option
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
    Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	#Response MUST include option 13. RFC 7550 change
	
	References: RFC3315 section 15.8

@v6 @dhcp6 @decline_invalid
    Scenario: v6.decline.invalid.double_client_id
    ## Testing server ability to discard message that not meets
    ## content requirements.
    ## In this case: DECLINE without CLIENT_ID
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## 2x CLIENT_ID	        DECLINE -->
	##					  		     X	REPLY
	## correct message 		DECLINE -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code
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
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
    Client does include client-id.
    Client does include client-id.
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
    Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	#Response MUST include option 13. RFC 7550 change

	References: RFC3315 section 15.8

@v6 @dhcp6 @decline_invalid
    Scenario: v6.decline.invalid.wrong_client_id
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
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code
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
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
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
	Client does include client-id.
    Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	#Response MUST include option 13. RFC 7550 change
	
	References: RFC3315 section 15.8


@v6 @dhcp6 @decline_invalid
    Scenario: v6.decline.invalid.empty_client_id
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
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code
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
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client does include empty-client-id.
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
    Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	#Response MUST include option 13. RFC 7550 change

	References: RFC3315 section 15.8

@v6 @dhcp6 @decline_invalid @invalid_option @outline
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
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code
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
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client does include relay-msg.
    Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	#Response MUST include option 13. RFC 7550 change
	
	References: RFC3315 section 15.8 22.8. table A: Appearance of Options in Message Types

@v6 @dhcp6 @decline_invalid @invalid_option @outline
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
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code
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
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client adds saved options. And DONT Erase.
	Client does include rapid-commit.
	Client does include client-id.
    Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	#Response MUST include option 13. RFC 7550 change
	
	References: RFC3315 section 15.8 22.8. table A: Appearance of Options in Message Types

@v6 @dhcp6 @decline_invalid @invalid_option @outline
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
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code
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
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client adds saved options. And DONT Erase.
	Client does include interface-id.
	Client does include client-id.
    Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	#Response MUST include option 13. RFC 7550 change
	
	References: RFC3315 section 15.8 22.8. table A: Appearance of Options in Message Types

@v6 @dhcp6 @decline_invalid @invalid_option @outline
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
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.
	
	Test Procedure:
	Client requests option 7.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client adds saved options. And DONT Erase.
	Client does include reconfigure-accept.
	Client does include client-id.
    Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	#Response MUST include option 13. RFC 7550 change
	
	References: RFC3315 section 15.8 22.8. table A: Appearance of Options in Message Types

@v6 @dhcp6 @decline_invalid @invalid_option @outline
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
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code
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
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client adds saved options. And DONT Erase.
	Client does include preference.
	Client does include client-id.
    Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	#Response MUST include option 13. RFC 7550 change
	
	References: RFC3315 section 15.8 22.8. table A: Appearance of Options in Message Types
	
@v6 @dhcp6 @decline_invalid @invalid_option @outline
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
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code
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
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client adds saved options. And DONT Erase.
	Client does include server-unicast.
	Client does include client-id.
    Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	#Response MUST include option 13. RFC 7550 change
	
	References: RFC3315 section 15.8 22.8. table A: Appearance of Options in Message Types
	
@v6 @dhcp6 @decline_invalid @invalid_option @outline
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
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code
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
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client adds saved options. And DONT Erase.
	Client does include status-code.
	Client does include client-id.
    Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	#Response MUST include option 13. RFC 7550 change
	
	References: RFC3315 section 15.8 22.8. table A: Appearance of Options in Message Types
	
@v6 @dhcp6 @decline_invalid @invalid_option @outline
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
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code
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
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client adds saved options. And DONT Erase.
	Client does include reconfigure.
	Client does include client-id.
    Client sends DECLINE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	#Response MUST include option 13. RFC 7550 change
	
	References: RFC3315 section 15.8 22.8. table A: Appearance of Options in Message Types