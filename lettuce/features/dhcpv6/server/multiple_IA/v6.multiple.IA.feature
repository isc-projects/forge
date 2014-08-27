Feature: Multiple Identity Association Option in single DHCPv6 message
    This feature testing ability distinguish multiple IA_NA options and concurrent processing of those options.
  
@v6 @dhcp6 @multipleIA
    Scenario: v6.multipleIA.addresses
	## Testing server ability to parse and allocate addresses
	## when multiple IA option are included in one message.
	## 					Client		Server
	## 					SOLICIT -->
	## save IA_NA				<--	ADVERTISE
	## 					SOLICIT -->
	## save IA_NA				<--	ADVERTISE
	## 					SOLICIT -->
	## save IA_NA				<--	ADVERTISE
	## include all IA's REQUEST -->
	## 				 		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					IA-NA
	##					IA-Address with 3000::1 address
	##					IA-Address with 3000::2 address
	##					IA-Address with 3000::3 address	
 	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Client saves IA_NA option from received message.
	Generate new IA.
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Client saves IA_NA option from received message.
	Generate new IA.
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Client saves IA_NA option from received message.
	Client copies server-id option from received message.
	Client adds saved options. And Erase.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.  
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	Response sub-option 5 from option 3 MUST contain address 3000::1.
	Response sub-option 5 from option 3 MUST contain address 3000::2.
	Response sub-option 5 from option 3 MUST contain address 3000::3.
	
@v6 @dhcp6 @multipleIA
    Scenario: v6.multipleIA.addresses-release-success
	## Testing server ability to parse multiple IA's included into message
	## and release included addresses.
	## 					Client		Server
	## 					SOLICIT -->
	## 							<--	ADVERTISE
	## 					REQUEST -->
	## save IA_NA	 		    <--	REPLY
	## new IA			SOLICIT -->
	## 							<--	ADVERTISE
	## 					REQUEST -->
	## save IA_NA	 		    <--	REPLY
	## new IA			SOLICIT -->
	## 							<--	ADVERTISE
	## 					REQUEST -->
	## save IA_NA	 		    <--	REPLY
	## include all IA'a RELEASE -->
	## 							<--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					Status code 'success'
 	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
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
	Client saves IA_NA option from received message.
	Generate new IA.
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
	Client saves IA_NA option from received message.
	Generate new IA.
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
	Client saves IA_NA option from received message.
	Client copies server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain status-code 0. 
	
@v6 @dhcp6 @multipleIA
    Scenario: v6.multipleIA.addresses-release-partial-success
	## Testing server ability to parse multiple IA's included into message
	## and release included addresses. One of the IA's are released twice.
	## first time: success, next: NoBinding
	## 					Client		Server
	## 					SOLICIT -->
	## 							<--	ADVERTISE
	## 					REQUEST -->
	## save IA_NA	 		    <--	REPLY
	## new IA			SOLICIT -->
	## 							<--	ADVERTISE
	## 					REQUEST -->
	## save IA_NA	 		    <--	REPLY
	## new IA			SOLICIT -->
	## 							<--	ADVERTISE
	## 					REQUEST -->
	## save IA_NA	 		    <--	REPLY
	## include last IA_NA RELEASE -->
	## 							<--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					Status code 'success'
	##
	## include all IA_NA's RELEASE -->
	## 							<--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					IA_NA option
	##					IA_Address with status code: NoBinding
 	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
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
	Client saves IA_NA option from received message.
	Generate new IA.
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
	Client saves IA_NA option from received message.
	Generate new IA.
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
	Client saves IA_NA option from received message.
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain status-code 0. 
		
	Test Procedure:
	Client copies server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	#Response option 13 MUST contain status-code 0. IS IT TRURE? RFC 3315 is not clear about that.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 13. 
	Response sub-option 13 from option 3 MUST contain statuscode 3.
	
@v6 @dhcp6 @multipleIA
    Scenario: v6.multipleIA.addresses-rebind-partial-success
	## Testing servers ability to rebind two IA form three received
	## One IA_NA released before. 
	## 					Client		Server
	## 					SOLICIT -->
	## 							<--	ADVERTISE
	## 					REQUEST -->
	## save IA_NA	 		    <--	REPLY
	## new IA			SOLICIT -->
	## 							<--	ADVERTISE
	## 					REQUEST -->
	## save IA_NA	 		    <--	REPLY
	## new IA			SOLICIT -->
	## 							<--	ADVERTISE
	## 					REQUEST -->
	## save IA_NA	 		    <--	REPLY
	## include last IA_NA RELEASE -->
	## 							<--	REPLY
	## include all IA_NA's REBIND -->
	## 							<--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					IA_NA option (for T1/T2)
	##					IA_Address (for lifetimes)
	##					IA_Address (for lifetimes)
	##					One status code/error? RFC is not clear 
	##					abut what should happen in such case. 
 	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
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
	Client saves IA_NA option from received message.
	Generate new IA.
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
	Client saves IA_NA option from received message.
	Generate new IA.
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
	Client saves IA_NA option from received message.
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain status-code 0. 

	Test Procedure:
	Client adds saved options. And Erase.
	Client sends REBIND message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	Response option 3 MUST contain sub-option 13.
	#Response sub-option 13 from option 3 MUST contain statuscode 3.
	
@v6 @dhcp6 @multipleIA
    Scenario: v6.multipleIA.addresses-noaddravail
   	## Testing server ability to assign two addresses and 
   	## send one status code: NoAddrAvail in one message.
	## 					Client		Server
	## 					SOLICIT -->
	## save IA_NA				<--	ADVERTISE
	## new IA			SOLICIT -->
	## save IA_NA				<--	ADVERTISE
	## new IA			SOLICIT -->
	## save IA_NA				<--	ADVERTISE
	## with all IA_NA's	REQUEST -->
	## 				 		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					IA_NA option 
	##					IA_Address with address 3000::1
	##					IA_Address with address 3000::2
	##					IA_NA with status code: NoAddrAvail 

 	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::2 pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client saves IA_NA option from received message.
	Generate new IA.
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client saves IA_NA option from received message.
	Generate new IA.
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client copies server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response option 3 MUST contain sub-option 5.
	Response sub-option 5 from option 3 MUST contain address 3000::1.
	Response sub-option 5 from option 3 MUST contain address 3000::2.
	Response option 3 MUST contain sub-option 13.
	Response sub-option 13 from option 3 MUST contain statuscode 2.