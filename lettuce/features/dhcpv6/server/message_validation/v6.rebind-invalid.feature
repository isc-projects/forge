
Feature: Standard DHCPv6 rebind message 
    This feature is designed for checking server response for invalid rebind messages. RFC 3315 section 15.7 Tests expecting lack of response, so each test also send valid massage to make sure that server is still running.
    
@v6 @rebind_invalid
    Scenario: v6.rebind.invalid.without_client_id
    ## Testing server ability to discard message that not meets 
    ## content requirements.
    ## In this case: REBIND without CLIENT_ID option.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## without CLIENT_ID	REBIND -->
	##					  		     X	REPLY
	## correct message 		REBIND -->
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
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client does NOT include client-id.
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	References: RFC3315 section 15.7
	
@v6 @rebind_invalid 
    Scenario: v6.rebind.invalid.blank_client_id
    ## Testing server ability to discard message that not meets 
    ## content requirements.
    ## In this case: REBIND with invalid CLIENT_ID option.
	## Message details 			Client		Server
	## 							SOLICIT -->
	## 		   							<--	ADVERTISE
	## 							REQUEST -->
	## 		   							<--	REPLY
	## with incorrect CLIENT_ID	 REBIND -->
	##					  		     	X	REPLY
	## correct message 			 REBIND -->
	##					  		    	<--	REPLY
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
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client does include wrong-client-id.
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	References: RFC3315 section 15.7
	
@v6 @rebind_invalid
    Scenario: v6.rebind.invalid.with_server_id
    ## Testing server ability to discard message that not meets 
    ## content requirements.
    ## In this case: REBIND with SERVER_ID option.
	## Message details		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## with SERVER_ID	     REBIND -->
	##					  	     	 X	REPLY
	## correct message 		 REBIND -->
	##					  	    	<--	REPLY
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
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies server-id option from received message.
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	References: RFC3315 section 15.7
	
@v6 @rebind_invalid @invalid_option @outline
    Scenario: v6.rebind.invalid.options-relay-msg
    ## Temporary test replacing disabled outline scenario
    ## Testing server ability to discard message that not meets 
    ## content requirements.
	## Message details		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## with restricted 
	## option	     		 REBIND -->
	##					  	     	 X	REPLY
	## correct message 		 REBIND -->
	##					  	    	<--	REPLY
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
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client does include relay-msg.
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	References: RFC3315 section 15, 15.7, table A: Appearance of Options in Message Types
	
@v6 @rebind_invalid @invalid_option @outline
    Scenario: v6.rebind.invalid.options-rapid-commit
    ## Temporary test replacing disabled outline scenario
    ## Testing server ability to discard message that not meets 
    ## content requirements.
	## Message details		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## with restricted 
	## option	     		 REBIND -->
	##					  	     	 X	REPLY
	## correct message 		 REBIND -->
	##					  	    	<--	REPLY
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
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client does include rapid-commit.
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	References: RFC3315 section 15, 15.7, table A: Appearance of Options in Message Types
		
@v6 @rebind_invalid @invalid_option @outline
    Scenario: v6.rebind.invalid.options-interface-id
    ## Temporary test replacing disabled outline scenario
    ## Testing server ability to discard message that not meets 
    ## content requirements.
	## Message details		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## with restricted 
	## option	     		 REBIND -->
	##					  	     	 X	REPLY
	## correct message 		 REBIND -->
	##					  	    	<--	REPLY
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
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client does include interface-id.
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	References: RFC3315 section 15, 15.7, table A: Appearance of Options in Message Types
	
@v6 @rebind_invalid @invalid_option @outline
    Scenario: v6.rebind.invalid.options-preference
    ## Temporary test replacing disabled outline scenario
    ## Testing server ability to discard message that not meets 
    ## content requirements.
	## Message details		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## with restricted 
	## option	     		 REBIND -->
	##					  	     	 X	REPLY
	## correct message 		 REBIND -->
	##					  	    	<--	REPLY
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
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client does include preference.
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	References: RFC3315 section 15, 15.7, table A: Appearance of Options in Message Types
	
@v6 @rebind_invalid @invalid_option @outline
    Scenario: v6.rebind.invalid.options-server-unicast
    ## Temporary test replacing disabled outline scenario
    ## Testing server ability to discard message that not meets 
    ## content requirements.
	## Message details		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## with restricted 
	## option	     		 REBIND -->
	##					  	     	 X	REPLY
	## correct message 		 REBIND -->
	##					  	    	<--	REPLY
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
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client does include server-unicast.
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	References: RFC3315 section 15, 15.7, table A: Appearance of Options in Message Types
	
@v6 @rebind_invalid @invalid_option @outline
    Scenario: v6.rebind.invalid.options-status-code 
    ## Temporary test replacing disabled outline scenario
    ## Testing server ability to discard message that not meets 
    ## content requirements.
	## Message details		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## with restricted 
	## option	     		 REBIND -->
	##					  	     	 X	REPLY
	## correct message 		 REBIND -->
	##					  	    	<--	REPLY
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
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client does include status-code.
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	References: RFC3315 section 15, 15.7, table A: Appearance of Options in Message Types

@v6 @rebind_invalid @invalid_option @outline
    Scenario: v6.rebind.invalid.options-reconfigure 
    ## Temporary test replacing disabled outline scenario
    ## Testing server ability to discard message that not meets 
    ## content requirements.
	## Message details		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## with restricted 
	## option	     		 REBIND -->
	##					  	     	 X	REPLY
	## correct message 		 REBIND -->
	##					  	    	<--	REPLY
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
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client does include reconfigure.
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	References: RFC3315 section 15, 15.7, table A: Appearance of Options in Message Types
