
Feature: Standard DHCPv6 options part 2
    This is a simple DHCPv6 options validation. Its purpose is to check if
    requested options are assigned properly. Also testing information-request message.

@v6 @options @preference
    Scenario: v6.options.inforequest-preference-

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with preference option with value 123.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 7.
	Response option 7 MUST contain value 123.

	References: RFC3315 section 22.8

@v6 @options @sip
    Scenario: v6.options.inforequest-sip-domains

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with sip-server-dns option with value srv1.example.com,srv2.isc.org.
	Server is started.

	Test Procedure:
	Client requests option 21.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 21.
	Response option 21 MUST contain domains srv1.example.com,srv2.isc.org.

	References: RFC3319

@v6 @options @sip @rfc3319
    Scenario: v6.options.inforequest-sip-servers

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with sip-server-addr option with value 2001:db8::1,2001:db8::2.
	Server is started.

	Test Procedure:
	Client requests option 22.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 22.
	Response option 22 MUST contain addresses 2001:db8::1,2001:db8::2.

	References: RFC3319


@v6 @options @dns @rfc3646
    Scenario: v6.options.inforequest-dns-servers

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with dns-servers option with value 2001:db8::1,2001:db8::2.
	Server is started.

	Test Procedure:
	Client requests option 23.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 23.
	Response option 23 MUST contain addresses 2001:db8::1,2001:db8::2.

	Test Procedure:

	References: v6.options, v6.oro, RFC3646

@v6 @options @rfc3646
    Scenario: v6.options.inforequest-domains

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with domain-search option with value domain1.example.com,domain2.isc.org.
	Server is started.

	Test Procedure:
	Client requests option 24.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 24.
	Response option 24 MUST contain domains domain1.example.com,domain2.isc.org.

	References: RFC3646 

@v6 @options @nis @rfc3898
    Scenario: v6.options.inforequest-nis-servers

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with nis-servers option with value 2001:db8::abc,3000::1,2000::1234.
	Server is started.

	Test Procedure:
	Client requests option 27.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 27.
	Response option 27 MUST contain addresses 2001:db8::abc,3000::1,2000::1234.

	References: RFC3898

@v6 @options @nis @nisp @rfc3898
    Scenario: v6.options.inforequest-nisp-servers

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with nisp-servers option with value 2001:db8::abc,3000::1,2000::1234.
	Server is started.

	Test Procedure:
	Client requests option 28.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 28.
	Response option 28 MUST contain addresses 2001:db8::abc,3000::1,2000::1234.

	References: RFC3898

	
@v6 @options @nis @rfc3898
    Scenario: v6.options.inforequest-nisdomain

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with nis-domain-name option with value ntp.example.com.
	Server is started.

	Test Procedure:
	Client requests option 29.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 29.
	Response option 29 MUST contain domain ntp.example.com.

	References: RFC3898


@v6 @options @rfc3898
    Scenario: v6.options.inforequest-nispdomain

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with nisp-domain-name option with value ntp.example.com.
	Server is started.

	Test Procedure:
	Client requests option 30.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 30.
	Response option 30 MUST contain domain ntp.example.com.

	References: RFC3898 

@v6 @options @sntp @rfc4075
    Scenario: v6.options.sntp-servers.inforequest

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with sntp-servers option with value 2001:db8::abc,3000::1,2000::1234.
	Server is started.

	Test Procedure:
	Client requests option 31.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 31.
	Response option 31 MUST contain addresses 2001:db8::abc,3000::1,2000::1234.

	References: RFC4075
	
@v6 @options @rfc4242
    Scenario: v6.options.inforequest-info-refresh

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with information-refresh-time option with value 12345678.
	Server is started.

	Test Procedure:
	Client requests option 32.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 32.
	Response option 32 MUST contain value 12345678.
	
	References: RFC4242

@v6 @options
    Scenario: v6.options.inforequest-multiple

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with preference option with value 123.
	Server is configured with sip-server-dns option with value srv1.example.com,srv2.isc.org.
	Server is configured with dns-servers option with value 2001:db8::1,2001:db8::2.
	Server is configured with domain-search option with value domain1.example.com,domain2.isc.org.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client requests option 23.
	Client requests option 24.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 7.
	Response MUST include option 23.
	Response MUST include option 24.
	Response option 7 MUST contain value 123.
	Response option 23 MUST contain addresses 2001:db8::1,2001:db8::2.
	Response option 24 MUST contain domains domain1.example.com,domain2.isc.org.

	References: RFC3315 section 22.8

@v6 @options @dns @rfc3646
    Scenario: v6.options.inforequest-negative

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with dns-servers option with value 2001:db8::1,2001:db8::2.
	Server is started.

	Test Procedure:
	Client requests option 24.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST NOT include option 24.

	Test Procedure:
	Client requests option 23.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 23.

	References: RFC3646
