Feature: DHCPv6 values
    Those are tests for DHCPv6 values like lifetime, address.. Check that DHCPv6 server wont send invalid values to client

@v6 @dhcp6 @values
    Scenario: v6.values.address1
	#that test will probably fail in step 'server is configured in case servers like ISC-DHCPv6, OS wont assign multicast address

	Test Setup:
	Server is configured with ff02::/64 subnet with ff02::1-ff02::ff pool.
	Send server configuration using SSH and config-file.
DHCP server failed to start. During configuration process.

	References: RFC3315 section 11	
	
@v6 @dhcp6 @values
    Scenario: v6.values.address2

	Test Setup:
	Server is configured with ::/64 subnet with ::1-::1 pool.
	Send server configuration using SSH and config-file.
DHCP server failed to start. During configuration process.
	
	References: RFC3315 section 11	