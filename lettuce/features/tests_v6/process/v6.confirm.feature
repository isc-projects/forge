Feature: DHCPv6 Confirm 
    Those are tests for confirm - reply exchange.
	
@v6 @status_code @confirm
    Scenario: v6.statuscode.success-confirm
    ## Testing server ability perform CONFIRM - REPLY message exchange. 
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## correct message 		CONFIRM -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code with code 0
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client requests option 7.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client sends CONFIRM message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 13.
	Response option 13 MUST contain status-code 0. 
	
	References: RFC3315 sections 18.1.2, 18.2.2
	
@v6 @status_code @confirm
    Scenario: v6.statuscode.notonlink-confirm
    ## Testing server ability perform CONFIRM - REPLY message exchange,
    ## with unsuccessful confirmation process.  
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 	Save IA_NA with IA_Address	<--	REPLY
	## 						Server Reconfiguration
	## 						SOLICIT -->
	## Make at least				<--	ADVERTISE
	##  one leases			REQUEST -->
	## 								<--	REPLY
	## with saved IA_NA		CONFIRM -->
	## NotOnLink error	  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code with code 4
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::1000 pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client requests option 7.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client saves IA_NA option from received message.

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::2000-3000::3000 pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	#add IA NA from beginning of the test. makes it NotOnlink 
	Client sends CONFIRM message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 13. 
	Response sub-option 13 from option 3 MUST contain statuscode 4.
	
	References: RFC3315 sections 18.1.2, 18.2.2
	