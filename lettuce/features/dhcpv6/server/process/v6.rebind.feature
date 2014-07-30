Feature: DHCPv6 Rebind
    Those are tests for rebind - reply exchange.
    
@v6 @rebind
    Scenario: v6.message.rebind-reply-zerotime
	## Testing server ability server ability perform REBIND - REPLY message exchange.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## 						Server Reconfiguration 
	## correct message 		REBIND -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA (with time T1 = 0 T2 = 0)
	##					IA-Address
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.
	
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

	Test Setup:
	Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::ffff pool.
	DHCP server is started.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response option 3 MUST contain T1 0.
	Response option 3 MUST contain T2 0.
	
	References: RFC3315 sections 5.3, 18.2.4 
	
@v6 @rebind
    Scenario: v6.message.rebind-reply-newtime
	## Testing server ability server ability perform REBIND - REPLY message exchange.
	## Additional server configuration: 
	## 		renew-timer = 111
	##		rebind-timer = 222
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## correct message 		REBIND -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA (with time T1 = 111 T2 = 222)
	##					IA-Address
	Test Setup:
	Time renew-timer is configured with value 111.
	Time rebind-timer is configured with value 222.
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.
	
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
	Client copies IA_NA option from received message.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	Response option 3 MUST contain T1 111.
	Response option 3 MUST contain T2 222.
		
	References: RFC3315 sections 5.3, 18.1.4 
	