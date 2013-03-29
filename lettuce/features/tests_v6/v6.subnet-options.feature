
Feature: DHCPv6 options defined in subnet
    This is a simple DHCPv6 options validation. Its purpose is to check if
    requested options are assigned properly.

    Scenario: v6.options.preference
	# Checks that server is able to serve sntp-servers option to clients.

	Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server is configured with preference option in subnet 0 with value 123.
    Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message and expect ADVERTISE response.

	Pass Criteria:
	Server MUST respond with advertise message.
	Response MUST include option 7.
	Response option 7 MUST contain value 123.

	References: v6.options, v6.oro, RFC3315 section 22.8

	Tags: v6 options preference automated

    Scenario: v6.options.dns-servers
	# Checks that server is able to serve dns-servers option to clients.

	Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server is configured with dns-servers option in subnet 0 with value 2001:db8::1,2001:db8::2.
    Server is started.

	Test Procedure:
	Client requests option 23.
	Client sends SOLICIT message and expect ADVERTISE response.

	Pass Criteria:
	Server MUST respond with advertise message.
	Response MUST include option 23.
	Response option 23 MUST contain addresses 2001:db8::1,2001:db8::2.

	References: v6.options, v6.oro, RFC3646

	Tags: v6 options dns-servers automated

    Scenario: v6.options.domains
	# Checks that server is able to serve domains option to clients.

	Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server is configured with domain-search option in subnet 0 with value domain1.example.com,domain2.isc.org.
    Server is started.

	Test Procedure:
	Client requests option 24.
	Client sends SOLICIT message and expect ADVERTISE response.

	Pass Criteria:
	Server MUST respond with advertise message.
	Response MUST include option 24.
	Response option 24 MUST contain domains domain1.example.com,domain2.isc.org.

	References: v6.options, v6.oro, RFC3646 

	Tags: v6 options domain automated


    Scenario: v6.options.override
	# Checks that server uses the option defined in subnet, if both subnet and global
	# options are defined.

	Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server is configured with domain-search option with value global.example.com.
    Server is configured with domain-search option in subnet 0 with value subnet.example.com.
    Server is started.

	Test Procedure:
	Client requests option 24.
	Client sends SOLICIT message and expect ADVERTISE response.

	Pass Criteria:
	Server MUST respond with advertise message.
	Response MUST include option 24.
	Response option 24 MUST contain domains subnet.example.com.

	References: v6.options, v6.oro, RFC3646 

	Tags: v6 options domain automated
