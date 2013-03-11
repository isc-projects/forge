
Feature: Standard DHCPv6 options
    This is a simple DHCPv6 options validation. Its purpose is to check if
    requested options are assigned properly.

    @v6
    Scenario: v6.options.preference
    	# Checks that server is able to serve preference option to clients.

    	Test Setup:
        Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
        Server is configured with preference option with value 123.
        Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message and expect ADVERTISE response.

	Pass Criteria:
	Server MUST respond with advertise message.
	Response MUST include option 7.
	Response option 7 MUST contain value 123.

	References: v6.options, v6.oro, RFC3315 section 22.8, 



    @v6
    Scenario: v6.options.sip-domains
    	# Checks that server is able to serve SIP domains option to clients.

    	Test Setup:
        Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
        Server is configured with sip-server-dns option with value srv1.example.com,srv2.isc.org.
        Server is started.

	Test Procedure:
	Client requests option 21.
	Client sends SOLICIT message and expect ADVERTISE response.

	Pass Criteria:
	Server MUST respond with advertise message.
	Response MUST include option 21.
	Response option 21 MUST contain domains srv1.example.com,srv2.isc.org.

	References: v6.options RFC3319

	Tags: v6 options SIP sip-domain automated

    Scenario: v6.options.sip-servers
    	# Checks that server is able to serve SIP servers option to clients.

    	Test Setup:
        Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
        Server is configured with sip-server-addr option with value 2001:db8::1,2001:db8::2.
        Server is started.

	Test Procedure:
	Client requests option 22.
	Client sends SOLICIT message and expect ADVERTISE response.

	Pass Criteria:
	Server MUST respond with advertise message.
	Response MUST include option 22.
	Response option 22 MUST contain addresses 2001:db8::1,2001:db8::2.

	References: v6.options RFC3319

	Tags: v6 options dns-servers automated

    
    Scenario: v6.options.dns-servers
    	# Checks that server is able to serve dns-servers option to clients.

    	Test Setup:
        Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
        Server is configured with dns-servers option with value 2001:db8::1,2001:db8::2.
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
        Server is configured with domain-search option with value domain1.example.com,domain2.isc.org.
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

    Scenario: v6.options.nis-servers
    	# Checks that server is able to serve NIS server option to clients.

    	Test Setup:
        Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
        Server is configured with nis-servers option with value 2001:db8::abc,3000::1,2000::1234.
        Server is started.

	Test Procedure:
	Client requests option 27.
	Client sends SOLICIT message and expect ADVERTISE response.

	Pass Criteria:
	Server MUST respond with advertise message.
	Response MUST include option 27.
	Response option 27 MUST contain addresses 2001:db8::abc,3000::1,2000::1234.

	References: v6.options, v6.oro, RFC3898

	Tags: v6 options nis nis-server automated

    Scenario: v6.options.nisp-servers
    	# Checks that server is able to serve NIS+ servers option to clients.

    	Test Setup:
        Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
        Server is configured with nisp-servers option with value 2001:db8::abc,3000::1,2000::1234.
        Server is started.

	Test Procedure:
	Client requests option 28.
	Client sends SOLICIT message and expect ADVERTISE response.

	Pass Criteria:
	Server MUST respond with advertise message.
	Response MUST include option 28.
	Response option 28 MUST contain addresses 2001:db8::abc,3000::1,2000::1234.

	References: v6.options, v6.oro, RFC3898

	Tags: v6 options nisplus nisp nis+ nisp-servers automated

    Scenario: v6.options.nisdomain
    	# Checks that server is able to serve NIS domain option to clients.

    	Test Setup:
        Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
        Server is configured with nis-domain-name option with value ntp.example.com.
        Server is started.

	Test Procedure:
	Client requests option 29.
	Client sends SOLICIT message and expect ADVERTISE response.

	Pass Criteria:
	Server MUST respond with advertise message.
	Response MUST include option 29.
	Response option 29 MUST contain domain ntp.example.com.

	References: v6.options, v6.oro, RFC3898

	Tags: v6 options nis-domain nis automated

    Scenario: v6.options.nispdomain
    	# Checks that server is able to serve NIS+ domain option to clients.

    	Test Setup:
        Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
        Server is configured with nisp-domain-name option with value ntp.example.com.
        Server is started.

	Test Procedure:
	Client requests option 30.
	Client sends SOLICIT message and expect ADVERTISE response.

	Pass Criteria:
	Server MUST respond with advertise message.
	Response MUST include option 30.
	Response option 30 MUST contain domain ntp.example.com.

	References: v6.options, v6.oro, RFC3898 

	Tags: v6 options nisplus nis+ nisp-domain nis automated


    Scenario: v6.options.sntp-servers
    	# Checks that server is able to serve sntp-servers option to clients.

    	Test Setup:
        Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
        Server is configured with sntp-servers option with value 2001:db8::abc,3000::1,2000::1234.
        Server is started.

	Test Procedure:
	Client requests option 31.
	Client sends SOLICIT message and expect ADVERTISE response.

	Pass Criteria:
	Server MUST respond with advertise message.
	Response MUST include option 31.
	Response option 31 MUST contain addresses 2001:db8::abc,3000::1,2000::1234.

	References: v6.options, v6.oro, RFC4075

	Tags: v6 options sntp servers automated

    Scenario: v6.options.info-refresh
    	# Checks that server is able to serve sntp-servers option to clients.

    	Test Setup:
        Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
        Server is configured with information-refresh-time option with value 12345678.
        Server is started.

	Test Procedure:
	Client requests option 32.
	Client sends SOLICIT message and expect ADVERTISE response.

	Pass Criteria:
	Server MUST respond with advertise message.
	Response MUST include option 32.
	Response option 32 MUST contain value 12345678.

	References: v6.options, v6.oro, RFC4242

	Tags: v6 options info-refresh-time automated

