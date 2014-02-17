

Feature: DHCPv4 options part3
    This is a simple DHCPv4 options validation. Its purpose is to check
    if requested option are assigned properly.

	# References in all tests are temporary empty, that's intentional.

@v4 @options @subnet
    Scenario: v4.options.ip-forwarding

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with ip-forwarding option with value True.
    Server is started.

    Test Procedure:
    Client requests option 19.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 19.
    Response option 19 MUST contain value 1.
    Response option 19 MUST NOT contain value 0.

@v4 @options @subnet
    Scenario: v4.options.non-local-source-routing

 	Test Setup:   
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with non-local-source-routing option with value True.
    Server is started.

    Test Procedure:
    Client requests option 20.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 20.
    Response option 20 MUST contain value 1.
    Response option 20 MUST NOT contain value 0.

@v4 @options @subnet
    Scenario: v4.options.perform-mask-discovery

	Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with perform-mask-discovery option with value False.
    Server is started.

    Test Procedure:
    Client requests option 29.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 29.
    Response option 29 MUST contain value 0.
    Response option 29 MUST NOT contain value 1.

@v4 @options @subnet
    Scenario: v4.options.mask-supplier

	Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with mask-supplier option with value True.
    Server is started.

    Test Procedure:
    Client requests option 30.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 30.
    Response option 30 MUST contain value 1.
    Response option 30 MUST NOT contain value 0.

@v4 @options @subnet
    Scenario: v4.options.router-discovery

	Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with router-discovery option with value True.
    Server is started.

    Test Procedure:
    Client requests option 31.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 31.
    Response option 31 MUST contain value 1.
    Response option 31 MUST NOT contain value 0.

@v4 @options @subnet
    Scenario: v4.options.trailer-encapsulation

	Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with trailer-encapsulation option with value True.
    Server is started.

    Test Procedure:
    Client requests option 34.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 34.
    Response option 34 MUST contain value 1.
    Response option 34 MUST NOT contain value 0.

@v4 @options @subnet
    Scenario: v4.options.ieee802-3-encapsulation

	Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with ieee802-3-encapsulation option with value True.
    Server is started.

    Test Procedure:
    Client requests option 36.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 36.
    Response option 36 MUST contain value 1.
    Response option 36 MUST NOT contain value 0.

@v4 @options @subnet
    Scenario: v4.options.tcp-keepalive-garbage

	Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with tcp-keepalive-garbage option with value True.
    Server is started.

    Test Procedure:
    Client requests option 39.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 39.
    Response option 39 MUST contain value 1.
    Response option 39 MUST NOT contain value 0.


#future tests:
#vendor-class-identifier	60	binary	false
#nwip-suboptions	63	binary	false
#user-class	77	binary	false
#authenticate	90	binary	false
#domain-search	119	binary	false
#vivco-suboptions	124	binary	false
#vivso-suboptions	125	binary