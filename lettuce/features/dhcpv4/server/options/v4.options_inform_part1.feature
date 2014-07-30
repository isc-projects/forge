

Feature: DHCPv4 options requested via DHCP_INFORM message part1
    This is a simple DHCPv4 options validation requested via DHCP_INFORM message.
    Its purpose is to check if requested option are assigned properly.

	# References in all tests are temporary empty, that's intentional.

@v4 @options @subnet @dhcp_inform
    Scenario: v4.options.inform.subnet-mask
    # Checks that server is able to serve subnet-mask option to clients.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with subnet-mask option with value 255.255.255.0.
    DHCP server is started.

    Test Procedure:
    Client requests option 1.
	Client sets ciaddr value to 192.168.50.9.
    Client sends INFORM message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST include option 1.
    Response option 1 MUST contain value 255.255.255.0.
    
    #References: v4.options, v4.prl, RFC2131

@v4 @options @subnet @dhcp_inform
    Scenario: v4.options.inform.time-offset

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with time-offset option with value 50.
    DHCP server is started.

    Test Procedure:
    Client requests option 2.
	Client sets ciaddr value to 192.168.50.9.
    Client sends INFORM message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST include option 2.
    Response option 2 MUST contain value 50.

@v4 @options @subnet @dhcp_inform
    Scenario: v4.options.inform.routers

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with routers option with value 100.100.100.10,50.50.50.5.
    DHCP server is started.

    Test Procedure:
    Client requests option 3.
	Client sets ciaddr value to 192.168.50.9.
    Client sends INFORM message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST include option 3.
    Response option 3 MUST contain value 100.100.100.10.
    Response option 3 MUST contain value 50.50.50.5.
    
@v4 @options @subnet @dhcp_inform
    Scenario: v4.options.inform.time-servers

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with time-servers option with value 199.199.199.1,199.199.199.2.
    DHCP server is started.

    Test Procedure:
    Client requests option 4.
	Client sets ciaddr value to 192.168.50.9.
    Client sends INFORM message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST include option 4.
    Response option 4 MUST contain value 199.199.199.1.
    Response option 4 MUST contain value 199.199.199.2.
    
@v4 @options @subnet @dhcp_inform
    Scenario: v4.options.inform.name-servers

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with name-servers option with value 199.199.199.1,100.100.100.1.
    DHCP server is started.

    Test Procedure:
    Client requests option 5.
	Client sets ciaddr value to 192.168.50.9.
    Client sends INFORM message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST include option 5.
    Response option 5 MUST contain value 199.199.199.1.
    Response option 5 MUST contain value 100.100.100.1.

@v4 @options @subnet @dhcp_inform
    Scenario: v4.options.inform.domain-name-servers

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with domain-name-servers option with value 199.199.199.1,100.100.100.1.
    DHCP server is started.

    Test Procedure:
    Client requests option 6.
	Client sets ciaddr value to 192.168.50.9.
    Client sends INFORM message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST include option 6.
    Response option 6 MUST contain value 199.199.199.1.
    Response option 6 MUST contain value 100.100.100.1.
    
@v4 @options @subnet @dhcp_inform
    Scenario: v4.options.inform.log-servers

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with log-servers option with value 199.199.199.1,100.100.100.1.
    DHCP server is started.

    Test Procedure:
    Client requests option 7.
	Client sets ciaddr value to 192.168.50.9.
    Client sends INFORM message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST include option 7.
    Response option 7 MUST contain value 199.199.199.1.
    Response option 7 MUST contain value 100.100.100.1.
    
@v4 @options @subnet @dhcp_inform
    Scenario: v4.options.inform.cookie-servers

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with cookie-servers option with value 199.199.199.1,100.100.100.1.
    DHCP server is started.

    Test Procedure:
    Client requests option 8.
	Client sets ciaddr value to 192.168.50.9.
    Client sends INFORM message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST include option 8.
    Response option 8 MUST contain value 199.199.199.1.
    Response option 8 MUST contain value 100.100.100.1.
    
@v4 @options @subnet @dhcp_inform
    Scenario: v4.options.inform.lpr-servers

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with lpr-servers option with value 199.199.199.1,150.150.150.1.
    DHCP server is started.

    Test Procedure:
    Client requests option 9.
	Client sets ciaddr value to 192.168.50.9.
    Client sends INFORM message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST include option 9.
    Response option 9 MUST contain value 199.199.199.1.
    Response option 9 MUST contain value 150.150.150.1.
    
@v4 @options @subnet @dhcp_inform
    Scenario: v4.options.inform.impress-servers

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with impress-servers option with value 199.199.199.1,150.150.150.1.
    DHCP server is started.

    Test Procedure:
    Client requests option 10.
	Client sets ciaddr value to 192.168.50.9.
    Client sends INFORM message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST include option 10.
    Response option 10 MUST contain value 199.199.199.1.
    Response option 10 MUST contain value 150.150.150.1.
    
@v4 @options @subnet @dhcp_inform
    Scenario: v4.options.inform.resource-location-servers

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with resource-location-servers option with value 199.199.199.1,150.150.150.1.
    DHCP server is started.

    Test Procedure:
    Client requests option 11.
	Client sets ciaddr value to 192.168.50.9.
    Client sends INFORM message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST include option 11.
    Response option 11 MUST contain value 199.199.199.1.
    Response option 11 MUST contain value 150.150.150.1.
    
@v4 @options @subnet @dhcp_inform
    Scenario: v4.options.inform.host-name

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with host-name option with value isc.example.com.
    DHCP server is started.

    Test Procedure:
    Client requests option 12.
	Client sets ciaddr value to 192.168.50.9.
    Client sends INFORM message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST include option 12.
    Response option 12 MUST contain value isc.example.com.
    
@v4 @options @subnet @dhcp_inform
    Scenario: v4.options.inform.boot-size

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with boot-size option with value 55.
    DHCP server is started.

    Test Procedure:
    Client requests option 13.
	Client sets ciaddr value to 192.168.50.9.
    Client sends INFORM message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST include option 13.
    Response option 13 MUST contain value 55.
    
@v4 @options @subnet @dhcp_inform
    Scenario: v4.options.inform.merit-dump

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with merit-dump option with value some-string.
    DHCP server is started.

    Test Procedure:
    Client requests option 14.
	Client sets ciaddr value to 192.168.50.9.
    Client sends INFORM message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST include option 14.
    Response option 14 MUST contain value some-string.
    
@v4 @options @subnet @dhcp_inform
    Scenario: v4.options.inform.swap-server

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with swap-server option with value 199.199.199.1.
    DHCP server is started.

    Test Procedure:
    Client requests option 16.
	Client sets ciaddr value to 192.168.50.9.
    Client sends INFORM message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST include option 16.
    Response option 16 MUST contain value 199.199.199.1.
    
@v4 @options @subnet @dhcp_inform
    Scenario: v4.options.inform.root-path

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with root-path option with value /some/location/example/.
    DHCP server is started.

    Test Procedure:
    Client requests option 17.
	Client sets ciaddr value to 192.168.50.9.
    Client sends INFORM message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST include option 17.
    Response option 17 MUST contain value /some/location/example/.
    
@v4 @options @subnet @dhcp_inform
    Scenario: v4.options.inform.extensions-path

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with extensions-path option with value /some/location/example/.
    DHCP server is started.

    Test Procedure:
    Client requests option 18.
	Client sets ciaddr value to 192.168.50.9.
    Client sends INFORM message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST include option 18.
    Response option 18 MUST contain value /some/location/example/.
    
@v4 @options @subnet @dhcp_inform
    Scenario: v4.options.inform.policy-filter

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with policy-filter option with value 199.199.199.1,50.50.50.1.
    DHCP server is started.

    Test Procedure:
    Client requests option 21.
	Client sets ciaddr value to 192.168.50.9.
    Client sends INFORM message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST include option 21.
    Response option 21 MUST contain value 199.199.199.1.
    Response option 21 MUST contain value 50.50.50.1.
    
@v4 @options @subnet @dhcp_inform
    Scenario: v4.options.inform.max-dgram-reassembly

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with max-dgram-reassembly option with value 600.
    DHCP server is started.

    Test Procedure:
    Client requests option 22.
	Client sets ciaddr value to 192.168.50.9.
    Client sends INFORM message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST include option 22.
    Response option 22 MUST contain value 600.
    
@v4 @options @subnet @dhcp_inform
    Scenario: v4.options.inform.default-ip-ttl

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with default-ip-ttl option with value 86.
    DHCP server is started.

    Test Procedure:
    Client requests option 23.
	Client sets ciaddr value to 192.168.50.9.
    Client sends INFORM message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST include option 23.
    Response option 23 MUST contain value 86.
    
@v4 @options @subnet @dhcp_inform
    Scenario: v4.options.inform.path-mtu-aging-timeout

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with path-mtu-aging-timeout option with value 85.
    DHCP server is started.

    Test Procedure:
    Client requests option 24.
	Client sets ciaddr value to 192.168.50.9.
    Client sends INFORM message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST include option 24.
    Response option 24 MUST contain value 85.