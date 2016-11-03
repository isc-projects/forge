Feature: DHCPv4 options part5
    This is a simple DHCPv5 options validation.

	# References in all tests are temporary empty, that's intentional.

@v4 @dhcp4 @options
    Scenario: v4.options.nisplus-domain-name

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with nisplus-domain-name option with value nisplus-domain.com.
    DHCP server is started.

    Test Procedure:
    Client requests option 64.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 64.
    Response option 64 MUST contain value nisplus-domain.com.

@v4 @dhcp4 @options
    Scenario: v4.options.nisplus-servers

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with nisplus-servers option with value 199.1.1.1,200.1.1.2.
    DHCP server is started.

    Test Procedure:
    Client requests option 65.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 65.
    Response option 65 MUST contain value 200.1.1.2.
    Response option 65 MUST contain value 199.1.1.1.

@v4 @dhcp4 @options
    Scenario: v4.options.mobile-ip-home-agent

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with mobile-ip-home-agent option with value 166.1.1.1,177.1.1.2.
    DHCP server is started.

    Test Procedure:
    Client requests option 68.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 68.
    Response option 68 MUST contain value 166.1.1.1.
    Response option 68 MUST contain value 177.1.1.2.

@v4 @dhcp4 @options
    Scenario: v4.options.smtp-server

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with smtp-server option with value 199.1.1.1,200.1.1.2.
    DHCP server is started.

    Test Procedure:
    Client requests option 69.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 69.
    Response option 69 MUST contain value 200.1.1.2.
    Response option 69 MUST contain value 199.1.1.1.

@v4 @dhcp4 @options
    Scenario: v4.options.pop-server

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with pop-server option with value 199.1.1.1,200.1.1.2.
    DHCP server is started.

    Test Procedure:
    Client requests option 70.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 70.
    Response option 70 MUST contain value 200.1.1.2.
    Response option 70 MUST contain value 199.1.1.1.

@v4 @dhcp4 @options
    Scenario: v4.options.nntp-server

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with nntp-server option with value 199.1.1.1,200.1.1.2.
    DHCP server is started.

    Test Procedure:
    Client requests option 71.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 71.
    Response option 71 MUST contain value 200.1.1.2.
    Response option 71 MUST contain value 199.1.1.1.

@v4 @dhcp4 @options
    Scenario: v4.options.www-server

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with www-server option with value 199.1.1.1,200.1.1.2.
    DHCP server is started.

    Test Procedure:
    Client requests option 72.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 72.
    Response option 72 MUST contain value 200.1.1.2.
    Response option 72 MUST contain value 199.1.1.1.

@v4 @dhcp4 @options
    Scenario: v4.options.finger-server

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with finger-server option with value 199.1.1.1,200.1.1.2.
    DHCP server is started.

    Test Procedure:
    Client requests option 73.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 73.
    Response option 73 MUST contain value 200.1.1.2.
    Response option 73 MUST contain value 199.1.1.1.

@v4 @dhcp4 @options
    Scenario: v4.options.irc-server

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with irc-server option with value 199.1.1.1,200.1.1.2.
    DHCP server is started.

    Test Procedure:
    Client requests option 74.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 74.
    Response option 74 MUST contain value 200.1.1.2.
    Response option 74 MUST contain value 199.1.1.1.

@v4 @dhcp4 @options
    Scenario: v4.options.streettalk-server

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with streettalk-server option with value 199.1.1.1,200.1.1.2.
    DHCP server is started.

    Test Procedure:
    Client requests option 75.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 75.
    Response option 75 MUST contain value 200.1.1.2.
    Response option 75 MUST contain value 199.1.1.1.

@v4 @dhcp4 @options
    Scenario: v4.options.streettalk-directory-assistance-server

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with streettalk-directory-assistance-server option with value 199.1.1.1,200.1.1.2.
    DHCP server is started.

    Test Procedure:
    Client requests option 76.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 76.
    Response option 76 MUST contain value 200.1.1.2.
    Response option 76 MUST contain value 199.1.1.1.

@v4 @dhcp4 @options
    Scenario: v4.options.not-requested-options

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with routers option with value 100.100.100.10,50.50.50.5.
    Server is configured with domain-name-servers option with value 199.199.199.1,100.100.100.1.
    #this should include fqdn option, 15
    DHCP server is started.

    Test Procedure:
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 6.
    Response option 6 MUST contain value 199.199.199.1.
    Response option 6 MUST contain value 100.100.100.1.
    Response MUST include option 3.
    Response option 3 MUST contain value 100.100.100.10.
    Response option 3 MUST contain value 50.50.50.5.


#future tests:
#vendor-class-identifier	60	binary	false
#nwip-suboptions	63	binary	false
#user-class	77	binary	false
#authenticate	90	binary	false
#domain-search	119	binary	false
#vivco-suboptions	124	binary	false
#vivso-suboptions	125	binary
