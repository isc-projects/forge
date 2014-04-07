Feature: DHCPv6 Renew
    Those are tests for renew - reply exchange.
    
@v6 @renew
    Scenario: v6.message.renew-reply
    ## Testing server ability to perform message exchange RENEW - REPLY 
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## correct message 		  RENEW -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA with suboption IA-Address
	##					
 	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::5-3000::55 pool.
	Server is started.
	
	Test Procedure:
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	References: RFC 3315, Section: 18.2.3.
	
@v6 @renew
    Scenario: v6.message.renew-reply-time-zero
    ## Testing server ability to perform message exchange RENEW - REPLY
    ## In case when we expect that address is not appropriate for the link. 
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## Save IA_NA with IA_Addr		<--	REPLY
	## 					Reconfigure Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## Create leases		REQUEST -->
	## for the same client			<--	REPLY
	## Use saved IA_NA 		  RENEW -->
	## (proper client ID, IA_NA, but wrong address)
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA with suboption IA-Address with validlft set to 0.
  	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::66-3000::66 pool.
	Server is started.
	
	Test Procedure:
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Client saves IA_NA option from received message.
	
	Server is configured with 3000::/64 subnet with 3000::100-3000::155 pool.
	Server is started.

	Test Procedure:
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client copies server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	Response sub-option 5 from option 3 MUST contain address 3000::66.
	Response sub-option 5 from option 3 MUST contain validlft 0.

	References: RFC 3315, Section: 18.2.3.