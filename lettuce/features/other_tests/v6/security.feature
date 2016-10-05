Feature: security
    kea4206



@v6 @dhcp6 @confirm @4206
    Scenario: v6.confirm.invalid.blank_client_idINFO
    ## Testing server ability to discard message that not meets
    ## content requirements.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## with blank CLIENT_ID	CONFIRM -->
	##					  		     X	REPLY
	## correct message 		CONFIRM -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server logging system is configured with logger type kea-dhcp6, severity INFO, severity level None and log file kea.log.
	DHCP server is started.

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
	Client does include wrong-client-id.
	Client sends CONFIRM message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client requests option 7.
	Client sends CONFIRM message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 13.

	References: RFC3315 section 15.5


@v6 @dhcp6 @confirm @4206
    Scenario: v6.confirm.invalid.blank_client_idFATAL
    ## Testing server ability to discard message that not meets
    ## content requirements.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## with blank CLIENT_ID	CONFIRM -->
	##					  		     X	REPLY
	## correct message 		CONFIRM -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server logging system is configured with logger type kea-dhcp6, severity FATAL, severity level None and log file kea.log.
	DHCP server is started.

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
	Client does include wrong-client-id.
	Client sends CONFIRM message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client requests option 7.
	Client sends CONFIRM message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 13.

	References: RFC3315 section 15.5


@v6 @dhcp6 @confirm @4206
    Scenario: v6.confirm.invalid.blank_client_idERROR
    ## Testing server ability to discard message that not meets
    ## content requirements.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## with blank CLIENT_ID	CONFIRM -->
	##					  		     X	REPLY
	## correct message 		CONFIRM -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server logging system is configured with logger type kea-dhcp6, severity ERROR, severity level None and log file kea.log.
	DHCP server is started.

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
	Client does include wrong-client-id.
	Client sends CONFIRM message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client requests option 7.
	Client sends CONFIRM message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 13.

	References: RFC3315 section 15.5

@v6 @dhcp6 @confirm @4206
    Scenario: v6.confirm.invalid.blank_client_idWARN
    ## Testing server ability to discard message that not meets
    ## content requirements.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## with blank CLIENT_ID	CONFIRM -->
	##					  		     X	REPLY
	## correct message 		CONFIRM -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server logging system is configured with logger type kea-dhcp6, severity WARN, severity level None and log file kea.log.
	DHCP server is started.

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
	Client does include wrong-client-id.
	Client sends CONFIRM message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client requests option 7.
	Client sends CONFIRM message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 13.

	References: RFC3315 section 15.5

@v6 @dhcp6 @confirm @4206
    Scenario: v6.confirm.invalid.blank_client_idDEBUG
    ## Testing server ability to discard message that not meets
    ## content requirements.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## with blank CLIENT_ID	CONFIRM -->
	##					  		     X	REPLY
	## correct message 		CONFIRM -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
	DHCP server is started.

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
	Client does include wrong-client-id.
	Client sends CONFIRM message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client requests option 7.
	Client sends CONFIRM message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 13.

	References: RFC3315 section 15.5


@v6 @dhcp6 @decline @4206
    Scenario: v6.decline.invalid.blank_client_idDEBUG
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
	Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
	DHCP server is started.

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
	Response MUST include option 1.
	Response MUST include option 2.

	References: RFC3315 section 15.8
@v6 @dhcp6 @decline @4206
    Scenario: v6.decline.invalid.blank_client_idINFO
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
	Server logging system is configured with logger type kea-dhcp6, severity INFO, severity level None and log file kea.log.
	DHCP server is started.

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
	Response MUST include option 1.
	Response MUST include option 2.

	References: RFC3315 section 15.8
@v6 @dhcp6 @decline @4206
    Scenario: v6.decline.invalid.blank_client_idFATAL
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
	Server logging system is configured with logger type kea-dhcp6, severity FATAL, severity level None and log file kea.log.
	DHCP server is started.

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
	Response MUST include option 1.
	Response MUST include option 2.

	References: RFC3315 section 15.8
@v6 @dhcp6 @decline @4206
    Scenario: v6.decline.invalid.blank_client_idERROR
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
	Server logging system is configured with logger type kea-dhcp6, severity ERROR, severity level None and log file kea.log.
	DHCP server is started.

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
	Response MUST include option 1.
	Response MUST include option 2.

	References: RFC3315 section 15.8
@v6 @dhcp6 @decline @4206
    Scenario: v6.decline.invalid.blank_client_idWARN
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
	Server logging system is configured with logger type kea-dhcp6, severity WARN, severity level None and log file kea.log.
	DHCP server is started.

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
	Response MUST include option 1.
	Response MUST include option 2.

	References: RFC3315 section 15.8


@v6 @dhcp6 @rebind @4206
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
	DHCP server is started.

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

@v6 @dhcp6 @rebind @4206
    Scenario: v6.rebind.invalid.blank_client_idFATAL
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
	Server logging system is configured with logger type kea-dhcp6, severity FATAL, severity level None and log file kea.log.
	DHCP server is started.

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

@v6 @dhcp6 @rebind @4206
    Scenario: v6.rebind.invalid.blank_client_idERROR
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
	Server logging system is configured with logger type kea-dhcp6, severity ERROR, severity level None and log file kea.log.
	DHCP server is started.

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

@v6 @dhcp6 @rebind @4206
    Scenario: v6.rebind.invalid.blank_client_idWARN
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
	Server logging system is configured with logger type kea-dhcp6, severity WARN, severity level None and log file kea.log.
	DHCP server is started.

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

@v6 @dhcp6 @rebind @4206
    Scenario: v6.rebind.invalid.blank_client_idINFO
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
	Server logging system is configured with logger type kea-dhcp6, severity INFO, severity level None and log file kea.log.
	DHCP server is started.

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

@v6 @dhcp6 @rebind @4206
    Scenario: v6.rebind.invalid.blank_client_idDEBUG
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
	Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
	DHCP server is started.

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


@v6 @dhcp6 @release @4206
    Scenario: v6.release.invalid.blank_client_idFATAL
    ## Testing server ability to discard message that not meets
    ## content requirements.
    ## In this case: RELEASE without CLIENT_ID option.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## without CLIENT_ID    RELEASE -->
	##					  		     X	REPLY
	## correct message 		RELEASE -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server logging system is configured with logger type kea-dhcp6, severity FATAL, severity level None and log file kea.log.
	DHCP server is started.

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
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 13.

	References: RFC3315 section 15.9


@v6 @dhcp6 @release @4206
    Scenario: v6.release.invalid.blank_client_idERROR
    ## Testing server ability to discard message that not meets
    ## content requirements.
    ## In this case: RELEASE without CLIENT_ID option.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## without CLIENT_ID    RELEASE -->
	##					  		     X	REPLY
	## correct message 		RELEASE -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server logging system is configured with logger type kea-dhcp6, severity ERROR, severity level None and log file kea.log.
	DHCP server is started.

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
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 13.

	References: RFC3315 section 15.9


@v6 @dhcp6 @release @4206
    Scenario: v6.release.invalid.blank_client_idWARN
    ## Testing server ability to discard message that not meets
    ## content requirements.
    ## In this case: RELEASE without CLIENT_ID option.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## without CLIENT_ID    RELEASE -->
	##					  		     X	REPLY
	## correct message 		RELEASE -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server logging system is configured with logger type kea-dhcp6, severity WARN, severity level None and log file kea.log.
	DHCP server is started.

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
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 13.

	References: RFC3315 section 15.9


@v6 @dhcp6 @release @4206
    Scenario: v6.release.invalid.blank_client_idINFO
    ## Testing server ability to discard message that not meets
    ## content requirements.
    ## In this case: RELEASE without CLIENT_ID option.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## without CLIENT_ID    RELEASE -->
	##					  		     X	REPLY
	## correct message 		RELEASE -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server logging system is configured with logger type kea-dhcp6, severity INFO, severity level None and log file kea.log.
	DHCP server is started.

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
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 13.

	References: RFC3315 section 15.9


@v6 @dhcp6 @release @4206
    Scenario: v6.release.invalid.blank_client_idDEBUG
    ## Testing server ability to discard message that not meets
    ## content requirements.
    ## In this case: RELEASE without CLIENT_ID option.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## without CLIENT_ID    RELEASE -->
	##					  		     X	REPLY
	## correct message 		RELEASE -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
	DHCP server is started.

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
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 13.

	References: RFC3315 section 15.9



@v6 @dhcp6 @renew @4206
    Scenario: v6.renew.invalid.blank_client_idFATAL
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
	Server logging system is configured with logger type kea-dhcp6, severity FATAL, severity level None and log file kea.log.
	DHCP server is started.

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
	Client sends RENEW message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

@v6 @dhcp6 @renew @4206
    Scenario: v6.renew.invalid.blank_client_idERROR
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
	Server logging system is configured with logger type kea-dhcp6, severity ERROR, severity level None and log file kea.log.
	DHCP server is started.

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
	Client sends RENEW message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

@v6 @dhcp6 @renew @4206
    Scenario: v6.renew.invalid.blank_client_idWARN
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
	Server logging system is configured with logger type kea-dhcp6, severity WARN, severity level None and log file kea.log.
	DHCP server is started.

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
	Client sends RENEW message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

@v6 @dhcp6 @renew @4206
    Scenario: v6.renew.invalid.blank_client_idINFO
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
	Server logging system is configured with logger type kea-dhcp6, severity INFO, severity level None and log file kea.log.
	DHCP server is started.

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
	Client sends RENEW message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

@v6 @dhcp6 @renew @4206
    Scenario: v6.renew.invalid.blank_client_idDEBUG
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
	Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
	DHCP server is started.

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
	Client sends RENEW message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.


@v6 @dhcp6 @request @4206
    Scenario: v6.request.invalid.blank_client_idFATAL
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
	Server logging system is configured with logger type kea-dhcp6, severity FATAL, severity level None and log file kea.log.
	DHCP server is started.

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

@v6 @dhcp6 @request @4206
    Scenario: v6.request.invalid.blank_client_idERROR
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
	Server logging system is configured with logger type kea-dhcp6, severity ERROR, severity level None and log file kea.log.
	DHCP server is started.

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

@v6 @dhcp6 @request @4206
    Scenario: v6.request.invalid.blank_client_idWARN
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
	Server logging system is configured with logger type kea-dhcp6, severity WARN, severity level None and log file kea.log.
	DHCP server is started.

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

@v6 @dhcp6 @request @4206
    Scenario: v6.request.invalid.blank_client_idINFO
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
	Server logging system is configured with logger type kea-dhcp6, severity INFO, severity level None and log file kea.log.
	DHCP server is started.

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

@v6 @dhcp6 @request @4206
    Scenario: v6.request.invalid.blank_client_idDEBUG
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
	Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
	DHCP server is started.

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


@v6 @dhcp6 @solicit @4206
    Scenario: v6.solicit.invalid.with_blank_client_idFATAL
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
	Server logging system is configured with logger type kea-dhcp6, severity FATAL, severity level None and log file kea.log.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include wrong-client-id.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.

@v6 @dhcp6 @solicit @4206
    Scenario: v6.solicit.invalid.with_blank_client_idERROR
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
	Server logging system is configured with logger type kea-dhcp6, severity ERROR, severity level None and log file kea.log.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include wrong-client-id.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.

@v6 @dhcp6 @solicit @4206
    Scenario: v6.solicit.invalid.with_blank_client_idWARN
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
	Server logging system is configured with logger type kea-dhcp6, severity WARN, severity level None and log file kea.log.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include wrong-client-id.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.

@v6 @dhcp6 @solicit @4206
    Scenario: v6.solicit.invalid.with_blank_client_idINFO
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
	Server logging system is configured with logger type kea-dhcp6, severity INFO, severity level None and log file kea.log.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include wrong-client-id.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.

@v6 @dhcp6 @solicit @4206
    Scenario: v6.solicit.invalid.with_blank_client_idDEBUG
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
	Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
	DHCP server is started.
	Test Procedure:
	Client requests option 7.
	Client does include wrong-client-id.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.

@v6 @dhcp6 @solicit @4206
    Scenario: v6.solicit.invalid.with_blank_client_idDEBUG44
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
	Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 44 and log file kea.log.
	DHCP server is started.
	Test Procedure:
	Client requests option 7.
	Client does include wrong-client-id.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.

@v6 @dhcp6 @solicit @4206
    Scenario: v6.solicit.invalid.with_blank_client_idDEBUG45
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
	Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 45 and log file kea.log.
	DHCP server is started.
	Test Procedure:
	Client requests option 7.
	Client does include wrong-client-id.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.

@v6 @dhcp6 @solicit @4206 @detailed
    Scenario: v6.solicit.invalid.with_blank_client_idDEBUGalloc-engine
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
	Server logging system is configured with logger type kea-dhcp6.alloc-engine, severity DEBUG, severity level 99 and log file kea.log.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include wrong-client-id.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.

@v6 @dhcp6 @solicit @4206 @detailed
    Scenario: v6.solicit.invalid.with_blank_client_idDEBUGbad-packets
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
	Server logging system is configured with logger type kea-dhcp6.bad-packets, severity DEBUG, severity level 99 and log file kea.log.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include wrong-client-id.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.

@v6 @dhcp6 @solicit @4206 @detailed
    Scenario: v6.solicit.invalid.with_blank_client_idDEBUGcallouts
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
	Server logging system is configured with logger type kea-dhcp6.callouts, severity DEBUG, severity level 99 and log file kea.log.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include wrong-client-id.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.

@v6 @dhcp6 @solicit @4206 @detailed
    Scenario: v6.solicit.invalid.with_blank_client_idDEBUGcommands
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
	Server logging system is configured with logger type kea-dhcp6.commands, severity DEBUG, severity level 99 and log file kea.log.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include wrong-client-id.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.

@v6 @dhcp6 @solicit @4206 @detailed
    Scenario: v6.solicit.invalid.with_blank_client_idDEBUGddns
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
	Server logging system is configured with logger type kea-dhcp6.ddns, severity DEBUG, severity level 99 and log file kea.log.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include wrong-client-id.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.

@v6 @dhcp6 @solicit @4206 @detailed
    Scenario: v6.solicit.invalid.with_blank_client_idDEBUG.dhcp6
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
	Server logging system is configured with logger type kea-dhcp6.dhcp6, severity DEBUG, severity level 99 and log file kea.log.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include wrong-client-id.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.

@v6 @dhcp6 @solicit @4206 @detailed
    Scenario: v6.solicit.invalid.with_blank_client_idDEBUGdhcpsrv
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
	Server logging system is configured with logger type kea-dhcp6.dhcpsrv, severity DEBUG, severity level 99 and log file kea.log.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include wrong-client-id.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.

@v6 @dhcp6 @solicit @4206 @detailed
    Scenario: v6.solicit.invalid.with_blank_client_idDEBUGeval
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
	Server logging system is configured with logger type kea-dhcp6.eval, severity DEBUG, severity level 99 and log file kea.log.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include wrong-client-id.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.

@v6 @dhcp6 @solicit @4206 @detailed
    Scenario: v6.solicit.invalid.with_blank_client_idDEBUGhooks
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
	Server logging system is configured with logger type kea-dhcp6.hooks, severity DEBUG, severity level 99 and log file kea.log.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include wrong-client-id.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.

@v6 @dhcp6 @solicit @4206 @detailed
    Scenario: v6.solicit.invalid.with_blank_client_idDEBUGhosts
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
	Server logging system is configured with logger type kea-dhcp6.hosts, severity DEBUG, severity level 99 and log file kea.log.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include wrong-client-id.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.

@v6 @dhcp6 @solicit @4206 @detailed
    Scenario: v6.solicit.invalid.with_blank_client_idDEBUGleases
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
	Server logging system is configured with logger type kea-dhcp6.leases, severity DEBUG, severity level 99 and log file kea.log.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include wrong-client-id.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.

@v6 @dhcp6 @solicit @4206 @detailed
    Scenario: v6.solicit.invalid.with_blank_client_idDEBUGoptions
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
	Server logging system is configured with logger type kea-dhcp6.options, severity DEBUG, severity level 99 and log file kea.log.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include wrong-client-id.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.

@v6 @dhcp6 @solicit @4206 @detailed
    Scenario: v6.solicit.invalid.with_blank_client_idDEBUpackets
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
	Server logging system is configured with logger type kea-dhcp6.packets, severity DEBUG, severity level 99 and log file kea.log.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include wrong-client-id.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.



@v6 @dhcp6 @request @4206
    Scenario: v6.request.invalid.value1
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
	Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
	DHCP server is started.

	Test Procedure:
    #Client sets address value to $(EMPTY).
    Client does include IA_Address.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.


	Test Procedure:
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.


