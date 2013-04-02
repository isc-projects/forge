Feature: Standard DHCPv6 address validation
    This feature is for checking respond on messages send on UNICAST address. Solicit, Confirm, Rebind, Info-Request should be discarded. 
    
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
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client chooses UNICAST address.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST NOT respond with REPLY message.
	
	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	
	References: RFC3315 section 15