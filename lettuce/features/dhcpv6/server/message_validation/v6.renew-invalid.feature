
Feature: Standard DHCPv6 renew message 
    This feature is designed for checking server response for invalid renew messages. RFC 3315 section 15.6 Tests expecting lack of response, so each test also send valid massage to make sure that server is still running.
    
@v6 @dhcp6 @renew_invalid
    Scenario: v6.message.negative.tests.renew-without_server_id
    ## Testing server ability to discard message that not meets 
    ## content requirements.
    ## In this case: RENEW without SERVER_ID option.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## without SERVER_ID	  RENEW -->
	##					  		     X	REPLY
	## 						SOLICIT -->
	## copy SERVER_ID				<--	ADVERTISE
	## correct message 		  RENEW -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	##					IA-Address
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
    Client sends RENEW message.

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
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	References: RFC3315 section 15.6
	
@v6 @dhcp6 @renew_invalid
    Scenario: v6.message.negative.tests.renew-wrong_server_id
    ## Testing server ability to discard message that not meets 
    ## content requirements.
    ## In this case: RENEW with incorrect SERVER_ID option.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## incorrect SERVER_ID    RENEW -->
	##					  		     X	REPLY
	## 						SOLICIT -->
	## copy SERVER_ID				<--	ADVERTISE	
	## correct message 		  RENEW -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	##					IA-Address

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
    Client sets server_id value to 00:01:00:01:52:7b:a8:f0:44:33:22:22:11:11.
	Client does include wrong-server-id.
	Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends RENEW message.

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
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	References: RFC3315 section 15.6 
	
@v6 @dhcp6 @renew_invalid
    Scenario: v6.message.negative.tests.renew-empty_server_id
    ## Testing server ability to discard message that not meets
    ## content requirements.
    ## In this case: RENEW with incorrect SERVER_ID option.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## incorrect SERVER_ID    RENEW -->
	##					  		     X	REPLY
	## 						SOLICIT -->
	## copy SERVER_ID				<--	ADVERTISE
	## correct message 		  RENEW -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	##					IA-Address

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
	Client does include empty-server-id.
	Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends RENEW message.

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
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	References: RFC3315 section 15.6

@v6 @dhcp6 @renew_invalid
    Scenario: v6.message.negative.tests.renew-without_client_id
    ## Testing server ability to discard message that not meets 
    ## content requirements.
    ## In this case: RENEW without CLIENT_ID option.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## without CLIENT_ID      RENEW -->
	##					  		     X	REPLY
	## correct message 		  RENEW -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	##					IA-Address

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
    Client sends RENEW message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	References: RFC3315 section 15.6

@v6 @dhcp6 @renew_invalid
    Scenario: v6.message.negative.tests.renew-double_client_id
    ## Testing server ability to discard message that not meets
    ## content requirements.
    ## In this case: RENEW without CLIENT_ID option.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## 2x CLIENT_ID         RENEW -->
	##					  		     X	REPLY
	## correct message 		  RENEW -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	##					IA-Address

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
    Client sends RENEW message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	References: RFC3315 section 15.6

@v6 @dhcp6 @renew_invalid
    Scenario: v6.message.negative.tests.renew-wrong_client_id
    ## Testing server ability to discard message that not meets 
    ## content requirements.
    ## In this case: RENEW without CLIENT_ID option.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## without CLIENT_ID      RENEW -->
	##					  		     X	REPLY
	## correct message 		  RENEW -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	##					IA-Address

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
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::2.
    Response sub-option 5 from option 3 MUST contain validlft 4000.
    Response sub-option 5 from option 3 MUST contain address 3000::1.
    Response sub-option 5 from option 3 MUST contain validlft 0.

	Test Procedure:
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	References: RFC3315 section 15.6


@v6 @dhcp6 @renew_invalid
    Scenario: v6.message.negative.tests.renew-empty_client_id
    ## Testing server ability to discard message that not meets
    ## content requirements.
    ## In this case: RENEW without CLIENT_ID option.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## without CLIENT_ID      RENEW -->
	##					  		     X	REPLY
	## correct message 		  RENEW -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	##					IA-Address

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
    Client sends RENEW message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	References: RFC3315 section 15.6


@v6 @dhcp6 @renew_invalid @invalid_option @outline @disabled
#TODO enable MAY condition in Forge then enable test

    Scenario: v6.message.negative.tests.renew-options-relay-msg
	## Temporary test replacing disabled outline scenario 
	## Testing server ability to discard message that not meets 
	## content requirements.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## with restricted 
	## option				  RENEW -->
	##					  		     X	REPLY
	## correct message 		  RENEW -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	##					IA-Address
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
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client does include client-id.
	Client does include relay-msg.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	References: RFC3315 section 15.6, table A: Appearance of Options in Message Types
	
@v6 @dhcp6 @renew_invalid @invalid_option @outline @disabled
#TODO enable MAY condition in Forge then enable test

    Scenario: v6.message.negative.tests.renew-options-rapid-commit
	## Temporary test replacing disabled outline scenario 
	## Testing server ability to discard message that not meets 
	## content requirements.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## with restricted 
	## option				  RENEW -->
	##					  		     X	REPLY
	## correct message 		  RENEW -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	##					IA-Address
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
	Client does include rapid-commit.
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	References: RFC3315 section 15.6, table A: Appearance of Options in Message Types
	
@v6 @dhcp6 @renew_invalid @invalid_option @outline @disabled
#TODO enable MAY condition in Forge then enable test

    Scenario: v6.message.negative.tests.renew-options-interface-id
	## Temporary test replacing disabled outline scenario 
	## Testing server ability to discard message that not meets 
	## content requirements.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## with restricted 
	## option				  RENEW -->
	##					  		     X	REPLY
	## correct message 		  RENEW -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	##					IA-Address
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
	Client does include interface-id.
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	References: RFC3315 section 15.6, table A: Appearance of Options in Message Types
		
@v6 @dhcp6 @renew_invalid @invalid_option @outline @disabled
#TODO enable MAY condition in Forge then enable test

    Scenario: v6.message.negative.tests.renew-options-preference
	## Temporary test replacing disabled outline scenario 
	## Testing server ability to discard message that not meets 
	## content requirements.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## with restricted 
	## option				  RENEW -->
	##					  		     X	REPLY
	## correct message 		  RENEW -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	##					IA-Address
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
	Client does include preference.
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	References: RFC3315 section 15.6, table A: Appearance of Options in Message Types
	
@v6 @dhcp6 @renew_invalid @invalid_option @outline @disabled
#TODO enable MAY condition in Forge then enable test

    Scenario: v6.message.negative.tests.renew-options-server-unicast
	## Temporary test replacing disabled outline scenario 
	## Testing server ability to discard message that not meets 
	## content requirements.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## with restricted 
	## option				  RENEW -->
	##					  		     X	REPLY
	## correct message 		  RENEW -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	##					IA-Address
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
	Client does include server-unicast.
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	References: RFC3315 section 15.6, table A: Appearance of Options in Message Types
	
@v6 @dhcp6 @renew_invalid @invalid_option @outline @disabled
#TODO enable MAY condition in Forge then enable test

    Scenario: v6.message.negative.tests.renew-options-status-code
	## Temporary test replacing disabled outline scenario 
	## Testing server ability to discard message that not meets 
	## content requirements.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## with restricted 
	## option				  RENEW -->
	##					  		     X	REPLY
	## correct message 		  RENEW -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	##					IA-Address
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
	Client does include status-code.
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	References: RFC3315 section 15.6, table A: Appearance of Options in Message Types

@v6 @dhcp6 @renew_invalid @invalid_option @outline @disabled
#TODO enable MAY condition in Forge then enable test

    Scenario: v6.message.negative.tests.renew-options-reconfigure
	## Temporary test replacing disabled outline scenario 
	## Testing server ability to discard message that not meets 
	## content requirements.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## with restricted 
	## option				  RENEW -->
	##					  		     X	REPLY
	## correct message 		  RENEW -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	##					IA-Address
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
	Client does include reconfigure.
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	References: RFC3315 section 15.6, table A: Appearance of Options in Message Types
