Feature: Standard DHCPv6 address validation
    This feature is for checking respond on messages send on GLOBAL UNICAST address. Solicit, Confirm, Rebind, Info-Request should be discarded. Request should be answered with Reply message containing option StatusCode with code 5. 
    
@basic @v6 @unicast
    Scenario: v6.basic.message.unicast.global.solicit

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client chooses GLOBAL UNICAST address.
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
    Scenario: v6.basic.message.unicast.global.confirm	
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client chooses GLOBAL UNICAST address.
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
    Scenario: v6.basic.message.unicast.global.rebind	
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client chooses GLOBAL UNICAST address.
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
    Scenario: v6.basic.message.unicast.global.inforequest	
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.
	
	Test Procedure:
	Client requests option 7.
	Client chooses GLOBAL UNICAST address.
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
    Scenario: v6.basic.message.unicast.global.request	
	
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
	Client chooses GLOBAL UNICAST address.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain statuscode 5.
	
	References: RFC3315 section 18.2.1
	
@basic @v6 @unicast @status_code
    Scenario: v6.basic.message.unicast.global.renew	
	
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
	Client chooses GLOBAL UNICAST address.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain statuscode 5.
	
	References: RFC3315 section 18.2.3
	
@basic @v6 @unicast @status_code
    Scenario: v6.basic.message.unicast.global.release	
	
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
	Client chooses GLOBAL UNICAST address.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 13. 
	Response sub-option 13 from option 3 MUST contain statuscode 5.
	
	References: RFC3315 section 18.2.6.

@basic @v6 @unicast
    Scenario: v6.basic.message.unicast.local.solicit

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client chooses LINK_LOCAL UNICAST address.
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
    Scenario: v6.basic.message.unicast.local.confirm	
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client chooses LINK_LOCAL UNICAST address.
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
    Scenario: v6.basic.message.unicast.local.rebind	
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client chooses LINK_LOCAL UNICAST address.
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
    Scenario: v6.basic.message.unicast.local.inforequest	
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.
	
	Test Procedure:
	Client requests option 7.
	Client chooses LINK_LOCAL UNICAST address.
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
    Scenario: v6.basic.message.unicast.local.request	
	
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
	Client chooses LINK_LOCAL UNICAST address.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain statuscode 5.
	
	References: RFC3315 section 18.2.1
	
@basic @v6 @unicast @status_code
    Scenario: v6.basic.message.unicast.local.renew	
	
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
	Client chooses LINK_LOCAL UNICAST address.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain statuscode 5.
	
	References: RFC3315 section 18.2.3
	
@basic @v6 @unicast @status_code
    Scenario: v6.basic.message.unicast.local.release	
	
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
	Client chooses LINK_LOCAL UNICAST address.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 13. 
	Response sub-option 13 from option 3 MUST contain statuscode 5.
	
	References: RFC3315 section 18.2.6.
	