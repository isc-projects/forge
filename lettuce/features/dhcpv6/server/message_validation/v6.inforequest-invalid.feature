Feature: Standard DHCPv6 information request message 
    This feature is designed for checking server response for invalid information request messages. RFC 3315 section 15.12 Tests expecting lack of response, so each test also send valid massage to make sure that server is still running.
    
@v6 @dhcp6 @inforequest_invalid
    Scenario: v6.message.negative.tests.inforequest-with_server_id
    ## Testing server ability to discard message that not meets 
    ## content requirements.
    ## In this case: INFOREQUEST with SERVER_ID
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## with SERVER_ID	INFOREQUEST -->
	##					  		     X	REPLY
	## correct message 	INFOREQUEST -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
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
    Client sets server_id value to 00:01:00:01:52:7b:a8:f0:44:33:22:22:11:11.
	Client does include server-id.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
    Client does include client-id.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.

	References: RFC3315 section 15.12, 


@v6 @dhcp6 @inforequest_invalid
    Scenario: v6.message.negative.tests.inforequest-with_empty_server_id
    ## Testing server ability to discard message that not meets
    ## content requirements.
    ## In this case: INFOREQUEST with SERVER_ID
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## with SERVER_ID	INFOREQUEST -->
	##					  		     X	REPLY
	## correct message 	INFOREQUEST -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
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
    #Client sets server_id value to 00:01:00:01:52:7b:a8:f0:44:33:22:22:11:11.
	Client does include empty-server-id.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
    Client does include client-id.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.

	References: RFC3315 section 15.12,


@v6 @dhcp6 @inforequest_invalid
    Scenario: v6.message.negative.tests.inforequest-without_client_id
    ## Testing server ability to discard message that not meets 
    ## content requirements.
    ## In this case: INFOREQUEST without CLIENT_ID
	##
	## Message details 		Client		Server
	## without CLIENT_ID INFOREQUEST -->
	##					  		     X	REPLY
	## correct message 	INFOREQUEST -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
 	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.
	   
	Test Procedure:
	#message wont contain client-id option
	Client requests option 7.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client does include client-id.
	Client requests option 7.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.

	References: RFC3315 section 15.12


@v6 @dhcp6 @inforequest_invalid
    Scenario: v6.message.negative.tests.inforequest-double_client_id
    ## Testing server ability to discard message that not meets
    ## content requirements.
    ## In this case: INFOREQUEST without CLIENT_ID
	##
	## Message details 		Client		Server
	## without CLIENT_ID INFOREQUEST -->
	##					  		     X	REPLY
	## correct message 	INFOREQUEST -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
 	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client does include client-id.
	Client does include client-id.
    Client requests option 7.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client does include client-id.
	Client requests option 7.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.

	References: RFC3315 section 15.12

@v6 @dhcp6 @inforequest_invalid
    Scenario: v6.message.negative.tests.inforequest-with_IA_NA
    ## Testing server ability to discard message that not meets 
    ## content requirements.
    ## In this case: INFOREQUEST with IA_NA option
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## with IA_NA		INFOREQUEST -->
	##					  		     X	REPLY
	## correct message 	INFOREQUEST -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	
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
	Client does include client-id.
	Client requests option 7.
	Client copies IA_NA option from received message.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client does include client-id.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.

	References: RFC3315 section 15.12, 

@v6 @dhcp6 @inforequest_invalid @invalid_option @outline @disabled
#TODO enable MAY condition in Forge then enable test

    Scenario: v6.message.negative.tests.inforequest-options-relay-msg
    ## Temporary test replacing disabled outline scenario
    ## Testing server ability to discard message that not meets 
    ## content requirements.
    ##
	## Message details 		Client		Server
	##
	## with restricted 
	## option			INFOREQUEST -->
	##					  		     X	REPLY
	## correct message 	INFOREQUEST -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
  	Client does include client-id.
	Client does include relay-msg.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client does include client-id.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.

	References: RFC3315 section 15.12 table A: Appearance of Options in Message Types

@v6 @dhcp6 @inforequest_invalid @invalid_option @outline @disabled
#TODO enable MAY condition in Forge then enable test

    Scenario: v6.message.negative.tests.inforequest-options-rapid-commit
    ## Temporary test replacing disabled outline scenario
    ## Testing server ability to discard message that not meets 
    ## content requirements.
    ##
	## Message details 		Client		Server
	##
	## with restricted 
	## option			INFOREQUEST -->
	##					  		     X	REPLY
	## correct message 	INFOREQUEST -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include rapid-commit.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.

	References: RFC3315 section 15.12 table A: Appearance of Options in Message Types

@v6 @dhcp6 @inforequest_invalid @invalid_option @outline @disabled
#TODO enable MAY condition in Forge then enable test

    Scenario: v6.message.negative.tests.inforequest-options-interface-id
    ## Temporary test replacing disabled outline scenario
    ## Testing server ability to discard message that not meets 
    ## content requirements.
    ##
	## Message details 		Client		Server
	##
	## with restricted 
	## option			INFOREQUEST -->
	##					  		     X	REPLY
	## correct message 	INFOREQUEST -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include interface-id.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.

	References: RFC3315 section 15.12 table A: Appearance of Options in Message Types

@v6 @dhcp6 @inforequest_invalid @invalid_option @outline @disabled
#TODO enable MAY condition in Forge then enable test

    Scenario: v6.message.negative.tests.inforequest-options-preference
    ## Temporary test replacing disabled outline scenario
    ## Testing server ability to discard message that not meets 
    ## content requirements.
    ##
	## Message details 		Client		Server
	##
	## with restricted 
	## option			INFOREQUEST -->
	##					  		     X	REPLY
	## correct message 	INFOREQUEST -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include preference.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.

	References: RFC3315 section 15.12 table A: Appearance of Options in Message Types

@v6 @dhcp6 @inforequest_invalid @invalid_option @outline @disabled
#TODO enable MAY condition in Forge then enable test

    Scenario: v6.message.negative.tests.inforequest-options-server-unicast
    ## Temporary test replacing disabled outline scenario
    ## Testing server ability to discard message that not meets 
    ## content requirements.
    ##
	## Message details 		Client		Server
	##
	## with restricted 
	## option			INFOREQUEST -->
	##					  		     X	REPLY
	## correct message 	INFOREQUEST -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include server-unicast.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.

	References: RFC3315 section 15.12 table A: Appearance of Options in Message Types

@v6 @dhcp6 @inforequest_invalid @invalid_option @outline @disabled
#TODO enable MAY condition in Forge then enable test

    Scenario: v6.message.negative.tests.inforequest-options-status-code
    ## Temporary test replacing disabled outline scenario
    ## Testing server ability to discard message that not meets 
    ## content requirements.
    ##
	## Message details 		Client		Server
	##
	## with restricted 
	## option			INFOREQUEST -->
	##					  		     X	REPLY
	## correct message 	INFOREQUEST -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include status-code.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.

	References: RFC3315 section 15.12 table A: Appearance of Options in Message Types

@v6 @dhcp6 @inforequest_invalid @invalid_option @outline @disabled
#TODO enable MAY condition in Forge then enable test

    Scenario: v6.message.negative.tests.inforequest-options-reconfigure
    ## Temporary test replacing disabled outline scenario
    ## Testing server ability to discard message that not meets 
    ## content requirements.
    ##
	## Message details 		Client		Server
	##
	## with restricted 
	## option			INFOREQUEST -->
	##					  		     X	REPLY
	## correct message 	INFOREQUEST -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include reconfigure.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.

	References: RFC3315 section 15.12 table A: Appearance of Options in Message Types
	