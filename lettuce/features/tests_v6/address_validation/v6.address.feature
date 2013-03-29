Feature: Standard DHCPv6 address validation
    This feature is for checking respond on messages send on UNICAST address. Solicit, Confirm, Rebind, Info-Request should be discarded. 
    
@basic @v6 
    Scenario: v6.basic.message.advertise

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
	