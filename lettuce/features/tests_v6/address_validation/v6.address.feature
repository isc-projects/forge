Feature: Standard DHCPv6 address validation
    This feature is for checking respond on messages send on UNICAST address. Solicit, Confirm, Rebind, Info-Request should be discarded. Request should be answered with Reply message containing option StatusCode with code 5. 
    
@basic @v6 @unicast
    Scenario: v6.basic.message.unicast.solicit

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client chooses UNICAST address.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond with ADVERTISE message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	References: RFC3315 section 15
	
	
@basic @v6 @unicast
    Scenario: v6.basic.message.unicast.confirm	
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client chooses UNICAST address.
	Client sends CONFIRM message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.
	
	Test Procedure:
	Client requests option 7.
	Client sends CONFIRM message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	
	References: RFC3315 section 15	
	
	
@basic @v6 @unicast 
    Scenario: v6.basic.message.unicast.rebind	
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client chooses UNICAST address.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.
	
	Test Procedure:
	Client requests option 7.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	
	References: RFC3315 section 15
	
@basic @v6 @unicast 
    Scenario: v6.basic.message.unicast.inforequest	
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.
	
	Test Procedure:
	Client requests option 7.
	Client chooses UNICAST address.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.
	
	Test Procedure:
	Client requests option 7.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	
	References: RFC3315 section 15
	
@basic @v6 @unicast @status_code
    Scenario: v6.basic.message.unicast.request	
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.
	
	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 7.
	Client chooses UNICAST address.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	#Response MUST include option 13.
	#Response option 13 MUST contain statuscode 5.
	
	References: RFC3315 section 18.2.1
	
@basic @v6 @unicast @status_code
    Scenario: v6.basic.message.unicast.renew	
	
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
	Client requests option 7.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 7.
	Client chooses UNICAST address.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	#Response MUST include option 13.
	#Response option 13 MUST contain statuscode 5.
	
	References: RFC3315 section 18.2.3
	
@basic @v6 @unicast @status_code
    Scenario: v6.basic.message.unicast.release	
	
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
	Client requests option 7.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client chooses UNICAST address.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	#Response MUST include option 3.
	#Response option 3 MUST contain option 13. 
	Response option 13 MUST contain statuscode 0.
	#Scapy bug, uncomment this after bug fixing, kea6 failing this test! 
	
	References: RFC3315 section 18.2.6.
	