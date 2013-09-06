Feature: DHCPv6 values
    Those are tests for DHCPv6 values like lifetime, address.. Check that DHCPv6 server wont send invalid values to client
	#this feature still needs some work:
	#	implement: testing values
	#	implement: Server MAY respond - test goes further if received, or stops when don't and return true.   
@v6 @values
    Scenario: v6.values.address1

	Test Setup:
	Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::0-2001:db8:1::1 pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response option 3 MUST contain sub-option 13. 
	Response option 13 MUST contain statuscode 2.

	References: RFC3315 section 11

@v6 @values
    Scenario: v6.values.address2

	Test Setup:
	Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::0-2001:db8:1::0 pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response option 3 MUST contain sub-option 13. 
	Response option 13 MUST contain statuscode 2.

	References: RFC3315 section 11	
	
@v6 @values
    Scenario: v6.values.address3
	#that test will probably fail in step 'server is configured in case servers like ISC-DHCPv6, OS wont assign multicast address

	Test Setup:
	Server is configured with ff02::/64 subnet with ff02::1-ff02::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response option 3 MUST contain sub-option 13. 
	Response option 13 MUST contain statuscode 2.

	References: RFC3315 section 11	
	
@v6 @values
    Scenario: v6.values.address4

	Test Setup:
	Server is configured with ::/64 subnet with ::1-::1 pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response option 3 MUST contain sub-option 13. 
	Response option 13 MUST contain statuscode 2.

	References: RFC3315 section 11	