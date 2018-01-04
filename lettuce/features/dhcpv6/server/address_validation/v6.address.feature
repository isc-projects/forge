Feature: Standard DHCPv6 address validation
    This feature is for checking respond on messages send on GLOBAL UNICAST address. Solicit, Confirm, Rebind, Info-Request should be discarded. Request should be answered with Reply message containing option StatusCode with code 5. 
    
@basic @v6 @dhcp6 @unicast
    Scenario: v6.basic.message.unicast.global-solicit
	## Server MUST discard any Solicit it receives with   
	## a unicast address destination
	## Message details 		Client		Server
	## GLOBAL_UNICAST dest  SOLICIT -->
	## 		   						 X	ADVERTISE
	## correct message		SOLICIT -->
	## 		   						<--	ADVERTISE	
	Test Setup:
  Server is configured on interface $(SERVER_IFACE) and address $(SRV_IPV6_ADDR_GLOBAL) with 3000::/64 subnet with 3000::1-3000::ff pool.
	#Server is configured with
	Send server configuration using SSH and config-file.
  DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client chooses GLOBAL UNICAST address.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.

	Test Procedure:
	Client requests option 7.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	References: RFC3315 section 15
	
@basic @v6 @dhcp6 @unicast
    Scenario: v6.basic.message.unicast.global-confirm
	## Server MUST discard any Confirm it receives with   
	## a unicast address destination
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## GLOBAL_UNICAST dest	CONFIRM -->
	##					  		     X	REPLY
	## correct message 		CONFIRM -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id

	Test Setup:
	#Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Server is configured on interface $(SERVER_IFACE) and address $(SRV_IPV6_ADDR_GLOBAL) with 3000::/64 subnet with 3000::1-3000::ff pool.
	Send server configuration using SSH and config-file.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client requests option 7.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client chooses GLOBAL UNICAST address.
	Client does include client-id.
    Client sends CONFIRM message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.
	
	Test Procedure:
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends CONFIRM message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 13.
		
	References: RFC3315 section 15	
	
@basic @v6 @dhcp6 @unicast
    Scenario: v6.basic.message.unicast.global-rebind
	## Server MUST discard any Rebind it receives with   
	## a unicast address destination.
	## Message details		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## GLOBAL_UNICAST dest	 REBIND -->
	##					  	     	 X	REPLY
	## correct message 		 REBIND -->
	##					  	    	<--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA

    Test Setup:
	Server is configured on interface $(SERVER_IFACE) and address $(SRV_IPV6_ADDR_GLOBAL) with 3000::/64 subnet with 3000::1-3000::ff pool.
	Send server configuration using SSH and config-file.
DHCP server is started.
	
	Test Procedure:
	Client requests option 7.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client chooses GLOBAL UNICAST address.
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends REBIND message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends REBIND message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	
	References: RFC3315 section 15
	
@basic @v6 @dhcp6 @unicast
    Scenario: v6.basic.message.unicast.global-inforequest
	## Server MUST discard any Information-Request it receives with   
	## a unicast address destination.
	## Message details 		Client		Server
	## GLOBAL_UNICAST dest INFOREQUEST -->
	##					  		       X	REPLY
	## correct message 	   INFOREQUEST -->
	##					  		       <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	
	Test Setup:
	Server is configured on interface $(SERVER_IFACE) and address $(SRV_IPV6_ADDR_GLOBAL) with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server is configured with preference option with value 123.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client chooses GLOBAL UNICAST address.
    #message wont contain client-id option
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
    #message wont contain client-id option
	Client requests option 7.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST NOT include option 1.
	Response MUST include option 2.
    Response MUST include option 7.
	
	References: RFC3315 section 15
	
@basic @v6 @dhcp6 @unicast @status_code @disabled #REASON: lacking support of status code 'Use Multicast'
    Scenario: v6.basic.message.unicast.global-request
	## Server MUST discard any Request message it receives with   
	## a unicast address destination, and send back REPLY with
	## UseMulticast status code.
	## In this test if it fails with 'NoAddrAvail' at the end
	## it means that server has send back REPLY with UseMulticast 
	## status code but also assigned address.
	## Message details		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## GLOBAL_UNICAST dest	REQUEST -->
	## 		   						<--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status code option with UseMulticast		
	##
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## correct message		REQUEST -->
	## 		   						<--	REPLY
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA_NA
	##					IA_Address with address 3000::1.
	
	Test Setup:
	Server is configured on interface $(SERVER_IFACE) and address $(SRV_IPV6_ADDR_GLOBAL) with 3000::/64 subnet with 3000::1-3000::ff pool.
	Send server configuration using SSH and config-file.
DHCP server is started.
	
	Test Procedure:
	Client requests option 7.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Client saves server-id option from received message.
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client chooses GLOBAL UNICAST address.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain statuscode 5.

	Test Procedure:
	Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	Response sub-option 5 from option 3 MUST contain address 3000::1.
	
	References: RFC3315 section 18.2.1
	
@basic @v6 @dhcp6 @unicast @status_code @disabled #REASON: lacking support of status code 'Use Multicast'
    Scenario: v6.basic.message.unicast.global-renew
	## Server MUST discard any RENEW message it receives with   
	## a unicast address destination, and send back REPLY with
	## UseMulticast status code.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## GLOBAL UNICAST dest	  RENEW -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status code with UseMulticast 
	## correct message 		  RENEW -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA
	##					IA-Address
	Test Setup:
	Server is configured on interface $(SERVER_IFACE) and address $(SRV_IPV6_ADDR_GLOBAL) with 3000::/64 subnet with 3000::1-3000::ff pool.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client requests option 7.
    Client does include IA-NA.
	Client does include client-id.
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
	Client chooses GLOBAL UNICAST address.
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain statuscode 5.

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
	
	References: RFC3315 section 18.2.3
	
@basic @v6 @dhcp6 @unicast @status_code  @disabled #REASON: lacking support of status code 'Use Multicast'
    Scenario: v6.basic.message.unicast.global-release
	## Server MUST discard any RELEASE message it receives with   
	## a unicast address destination, and send back REPLY with
	## UseMulticast status code.
	##
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## GLOBAL UNICAST dest	RELEASE -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code with UseMulticast
	## correct message 		RELEASE -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code with Success
	Test Setup:
	#Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Server is configured on interface $(SERVER_IFACE) and address $(SRV_IPV6_ADDR_GLOBAL) with 3000::/64 subnet with 3000::1-3000::ff pool.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client requests option 7.
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
	Client chooses GLOBAL UNICAST address.
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends RELEASE message.

    Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain statuscode 5.

	Test Procedure:
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 13.
	
	References: RFC3315 section 18.2.6.

@basic @v6 @dhcp6 @unicast
    Scenario: v6.basic.message.unicast.local-solicit
	## Server MUST discard any Solicit it receives with   
	## a unicast address destination
	## Message details 		Client		Server
	## LINK_LOCAL_UNICAST dest  SOLICIT -->
	## 		   						 X	ADVERTISE
	## correct message		SOLICIT -->
	## 		   						<--	ADVERTISE	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client chooses LINK_LOCAL UNICAST address.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.

	Test Procedure:
	Client requests option 7.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	References: RFC3315 section 15

@basic @v6 @dhcp6 @unicast
    Scenario: v6.basic.message.unicast.local-confirm
	## Server MUST discard any Confirm it receives with   
	## a unicast address destination
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## LINK_LOCAL_UNICAST dest	CONFIRM -->
	##					  		     X	REPLY
	## correct message 		CONFIRM -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client requests option 7.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client chooses LINK_LOCAL UNICAST address.
	Client does include client-id.
    Client sends CONFIRM message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.
	
	Test Procedure:
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends CONFIRM message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 13.
	
	References: RFC3315 section 15	

@basic @v6 @dhcp6 @unicast
    Scenario: v6.basic.message.unicast.local-rebind
	## Server MUST discard any Rebind it receives with   
	## a unicast address destination.
	## Message details		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## LINK_LOCAL
	## UNICAST dest	 		 REBIND -->
	##					  	     	 X	REPLY
	## correct message 		 REBIND -->
	##					  	    	<--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA

    Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Send server configuration using SSH and config-file.
DHCP server is started.
	
	Test Procedure:
	Client requests option 7.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client chooses LINK_LOCAL UNICAST address.
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends REBIND message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends REBIND message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.

	References: RFC3315 section 15
	
@basic @v6 @dhcp6 @unicast
    Scenario: v6.basic.message.unicast.local-inforequest
	## Server MUST discard any Information-Request it receives with   
	## a unicast address destination.
	## Message details 		Client		Server
	## LINK_LOCAL
	## UNICAST dest		   INFOREQUEST -->
	##					  		       X	REPLY
	## correct message 	   INFOREQUEST -->
	##					  		       <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server is configured with preference option with value 123.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client chooses LINK_LOCAL UNICAST address.
    #message wont contain client-id option
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.

	Test Procedure:
	Client requests option 7.
    #message wont contain client-id option
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST NOT include option 1.
	Response MUST include option 2.
    Response MUST include option 7.
	
	References: RFC3315 section 15
	
@basic @v6 @dhcp6 @unicast @status_code @disabled #REASON: lacking support of status code 'Use Multicast'
    Scenario: v6.basic.message.unicast.local-request
	## Server MUST discard any Request message it receives with   
	## a unicast address destination, and send back REPLY with
	## UseMulticast status code.
	## In this test if it fails with 'NoAddrAvail' at the end
	## it means that server has send back REPLY with UseMulticast 
	## status code but also assigned address.
	## Message details		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## LINK_LOCAL
	## UNICAST dest			REQUEST -->
	## 		   						<--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status code option with UseMulticast		
	##
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## correct message		REQUEST -->
	## 		   						<--	REPLY
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA_NA
	##					IA_Address with address 3000::1.
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
	Send server configuration using SSH and config-file.
DHCP server is started.
	
	Test Procedure:
	Client requests option 7.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Client saves server-id option from received message.
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client chooses LINK_LOCAL UNICAST address.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain statuscode 5.

	Test Procedure:
	Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	Response sub-option 5 from option 3 MUST contain address 3000::1.
	
	References: RFC3315 section 18.2.1
	
@basic @v6 @dhcp6 @unicast @status_code @disabled #REASON: lacking support of status code 'Use Multicast'
    Scenario: v6.basic.message.unicast.local-renew
	## Server MUST discard any RENEW message it receives with   
	## a unicast address destination, and send back REPLY with
	## UseMulticast status code.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## LINK_LOCAL
	## UNICAST dest			  RENEW -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status code with UseMulticast 
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
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client requests option 7.
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
	Client chooses LINK_LOCAL UNICAST address.
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain statuscode 5.

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
		
	References: RFC3315 section 18.2.3
	
@basic @v6 @dhcp6 @unicast @status_code @disabled #REASON: lacking support of status code 'Use Multicast'
    Scenario: v6.basic.message.unicast.local-release
	## Server MUST discard any RELEASE message it receives with   
	## a unicast address destination, and send back REPLY with
	## UseMulticast status code.
	##
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## LINK_LOCAL
	## UNICAST dest			RELEASE -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code with UseMulticast
	## correct message 		RELEASE -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code with Success
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client requests option 7.
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
	Client chooses LINK_LOCAL UNICAST address.
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain statuscode 5.

	Test Procedure:
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 13.
	
	References: RFC3315 section 18.2.6.