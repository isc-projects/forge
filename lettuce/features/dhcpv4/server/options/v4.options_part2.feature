

Feature: DHCPv4 options part2
    This is a simple DHCPv4 options validation. Its purpose is to check
    if requested option are assigned properly.

	# References in all tests are temporary empty, that's intentional.
    
@v4 @options @subnet
    Scenario: v4.options.path-mtu-plateau-table

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with path-mtu-plateau-table option with value 100,300,500.
    DHCP server is started.

    Test Procedure:
    Client requests option 25.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 25.
    Response option 25 MUST contain value 100.
    Response option 25 MUST contain value 300.
	Response option 25 MUST contain value 500.

@v4 @options @subnet
    Scenario: v4.options.interface-mtu

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with interface-mtu option with value 321.
    DHCP server is started.

    Test Procedure:
    Client requests option 26.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 26.
    Response option 26 MUST contain value 321.

@v4 @options @subnet
    Scenario: v4.options.broadcast-address

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with broadcast-address option with value 255.255.255.0.
    DHCP server is started.

    Test Procedure:
    Client requests option 28.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 28.
    Response option 28 MUST contain value 255.255.255.0.

@v4 @options @subnet
    Scenario: v4.options.router-solicitation-address

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with router-solicitation-address option with value 199.199.199.1.
    DHCP server is started.

    Test Procedure:
    Client requests option 32.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 32.
    Response option 32 MUST contain value 199.199.199.1.

@v4 @options @subnet
    Scenario: v4.options.static-routes

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with static-routes option with value 199.199.199.1,70.70.70.1.
    DHCP server is started.

    Test Procedure:
    Client requests option 33.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 33.
    Response option 33 MUST contain value 199.199.199.1.
    Response option 33 MUST contain value 70.70.70.1.

@v4 @options @subnet
    Scenario: v4.options.arp-cache-timeout

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with arp-cache-timeout option with value 48.
    DHCP server is started.

    Test Procedure:
    Client requests option 35.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 35.
    Response option 35 MUST contain value 48.

@v4 @options @subnet
    Scenario: v4.options.default-tcp-ttl

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with default-tcp-ttl option with value 44.
    DHCP server is started.

    Test Procedure:
    Client requests option 37.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 37.
    Response option 37 MUST contain value 44.

@v4 @options @subnet
    Scenario: v4.options.tcp-keepalive-internal

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with tcp-keepalive-internal option with value 4896.
    DHCP server is started.

    Test Procedure:
    Client requests option 38.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 38.
    Response option 38 MUST contain value 4896.

@v4 @options @subnet
    Scenario: v4.options.nis-domain

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with nis-domain option with value some.domain.com.
    DHCP server is started.

    Test Procedure:
    Client requests option 40.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 40.
    Response option 40 MUST contain value some.domain.com.

@v4 @options @subnet
    Scenario: v4.options.nis-servers

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with nis-servers option with value 199.199.199.1,100.100.100.15.
    DHCP server is started.

    Test Procedure:
    Client requests option 41.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 41.
    Response option 41 MUST contain value 199.199.199.1.
    Response option 41 MUST contain value 100.100.100.15.

@v4 @options @subnet
    Scenario: v4.options.ntp-servers

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with ntp-servers option with value 199.199.199.1,100.100.100.15.
    DHCP server is started.

    Test Procedure:
    Client requests option 42.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 42.
    Response option 42 MUST contain value 199.199.199.1.
    Response option 42 MUST contain value 100.100.100.15.

@v4 @options @subnet
    Scenario: v4.options.netbios-name-servers

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with netbios-name-servers option with value 188.188.188.2,100.100.100.15.
    DHCP server is started.

    Test Procedure:
    Client requests option 44.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 44.
    Response option 44 MUST contain value 188.188.188.2.
    Response option 44 MUST contain value 100.100.100.15.

@v4 @options @subnet
    Scenario: v4.options.netbios-dd-server

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with netbios-dd-server option with value 188.188.188.2,70.70.70.1.
    DHCP server is started.

    Test Procedure:
    Client requests option 45.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 45.
    Response option 45 MUST contain value 188.188.188.2.
    Response option 45 MUST contain value 70.70.70.1.

@v4 @options @subnet
    Scenario: v4.options.netbios-node-type

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with netbios-node-type option with value 8.
    DHCP server is started.

    Test Procedure:
    Client requests option 46.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 46.
    Response option 46 MUST contain value 8.
    
@v4 @options @subnet
    Scenario: v4.options.netbios-scope

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with netbios-scope option with value global.
    DHCP server is started.

    Test Procedure:
    Client requests option 47.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 47.
    Response option 47 MUST contain value global.
    
@v4 @options @subnet
    Scenario: v4.options.font-servers

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with font-servers option with value 188.188.188.2,100.100.100.1.
    DHCP server is started.

    Test Procedure:
    Client requests option 48.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 48.
    Response option 48 MUST contain value 188.188.188.2.
    Response option 48 MUST contain value 100.100.100.1.

@v4 @options @subnet
    Scenario: v4.options.x-display-manager

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with x-display-manager option with value 188.188.188.2,150.150.150.10.
    DHCP server is started.

    Test Procedure:
    Client requests option 49.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 49.
    Response option 49 MUST contain value 188.188.188.2.
    Response option 49 MUST contain value 150.150.150.10.

@v4 @options @subnet
    Scenario: v4.options.dhcp-requested-address

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with dhcp-requested-address option with value 188.188.188.2.
    DHCP server is started.

    Test Procedure:
    Client requests option 50.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 50.
    Response option 50 MUST contain value 188.188.188.2.

@v4 @options @subnet
    Scenario: v4.options.dhcp-option-overload

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with dhcp-option-overload option with value 1.
    DHCP server is started.

    Test Procedure:
    Client requests option 52.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 52.
    Response option 52 MUST contain value 1.

@v4 @options @subnet
    Scenario: v4.options.dhcp-message

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with dhcp-message option with value some-message.
    DHCP server is started.

    Test Procedure:
    Client requests option 56.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 56.
    Response option 56 MUST contain value some-message.

@v4 @options @subnet
    Scenario: v4.options.dhcp-max-message-size

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with dhcp-max-message-size option with value 2349.
    DHCP server is started.

    Test Procedure:
    Client requests option 57.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 57.
    Response option 57 MUST contain value 2349.

@v4 @options @subnet
    Scenario: v4.options.renew-timer

    Test Setup:
    Time renew-timer is configured with value 999.
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    DHCP server is started.

    Test Procedure:
    Client requests option 58.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 58.
    Response option 58 MUST contain value 999.
    
@v4 @options @subnet
    Scenario: v4.options.rebind-timer

    Test Setup:
    Time rebind-timer is configured with value 1999.
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    DHCP server is started.

    Test Procedure:
    Client requests option 59.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 59.
    Response option 59 MUST contain value 1999.
    
@v4 @options @subnet
    Scenario: v4.options.nwip-domain-name

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with nwip-domain-name option with value some.domain.com.
    DHCP server is started.

    Test Procedure:
    Client requests option 62.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 62.
    Response option 62 MUST contain value some.domain.com.

@v4 @options @subnet
    Scenario: v4.options.boot-file-name

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with boot-file-name option with value somefilename.
    DHCP server is started.

    Test Procedure:
    Client requests option 67.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 67.
    Response option 67 MUST contain value somefilename.

@v4 @options @subnet
    Scenario: v4.options.client-last-transaction-time

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with client-last-transaction-time option with value 3424.
    DHCP server is started.

    Test Procedure:
    Client requests option 91.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 91.
    Response option 91 MUST contain value 3424. 

@v4 @options @subnet
    Scenario: v4.options.associated-ip

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with associated-ip option with value 188.188.188.2,199.188.188.12.
    DHCP server is started.

    Test Procedure:
    Client requests option 92.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 92.
    Response option 92 MUST contain value 188.188.188.2.
	Response option 92 MUST contain value 199.188.188.12.

@v4 @options @subnet
    Scenario: v4.options.subnet-selection

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with subnet-selection option with value 188.188.188.2.
    DHCP server is started.

    Test Procedure:
    Client requests option 118.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 118.
    Response option 118 MUST contain value 188.188.188.2.    