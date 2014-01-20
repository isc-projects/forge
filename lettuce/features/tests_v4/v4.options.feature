

Feature: DHCPv4 options
    This is a simple DHCPv4 options validation. Its purpose is to check
    if requested option are assigned properly.

@v4 @options @subnet
    Scenario: v4.options.subnet-mask
    # Checks that server is able to serve subnet-mask option to clients.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with subnet-mask option with value 255.255.255.0.
    Server is started.

    Test Procedure:
    Client requests option 1.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response option 1 MUST contain value 255.255.255.0.
    
    #References: v4.options, v4.prl, RFC2131

@v4 @options @subnet
    Scenario: v4.options.time-offset

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with time-offset option with value 50.
    Server is started. 

    Test Procedure:
    Client requests option 2.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 2.
    Response option 2 MUST contain value 50.

@v4 @options @subnet
    Scenario: v4.options.routers

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with routers option with value 100.100.100.0.
    Server is started. 

    Test Procedure:
    Client requests option 3.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 3.
    Response option 3 MUST contain value 100.100.100.0.
    
@v4 @options @subnet
    Scenario: v4.options.time-servers

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with time-servers option with value 199.199.199.1,199.199.199.2.
    Server is started. 

    Test Procedure:
    Client requests option 4.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 4.
    #multiple options not available right now
    #Response option 4 MUST contain value 199.199.199.1,199.199.199.2.
    
@v4 @options @subnet
    Scenario: v4.options.name-servers

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with name-servers option with value 199.199.199.1.
    Server is started. 

    Test Procedure:
    Client requests option 5.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 5.
    Response option 5 MUST contain value 199.199.199.1.

@v4 @options @subnet
    Scenario: v4.options.domain-name-servers

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with domain-name-servers option with value 199.199.199.1.
    Server is started. 

    Test Procedure:
    Client requests option 6.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 6.
    Response option 6 MUST contain value 199.199.199.1.
    
@v4 @options @subnet
    Scenario: v4.options.log-servers

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with log-servers option with value 199.199.199.1.
    Server is started. 

    Test Procedure:
    Client requests option 7.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 7.
    Response option 7 MUST contain value 199.199.199.1.
    
@v4 @options @subnet
    Scenario: v4.options.cookie-servers

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with cookie-servers option with value 199.199.199.1.
    Server is started. 

    Test Procedure:
    Client requests option 8.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 8.
    Response option 8 MUST contain value 199.199.199.1.
    
@v4 @options @subnet
    Scenario: v4.options.lpr-servers

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with lpr-servers option with value 199.199.199.1.
    Server is started. 

    Test Procedure:
    Client requests option 9.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 9.
    Response option 9 MUST contain value 199.199.199.1.
    
@v4 @options @subnet
    Scenario: v4.options.impress-servers

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with impress-servers option with value 199.199.199.1.
    Server is started. 

    Test Procedure:
    Client requests option 10.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 10.
    Response option 10 MUST contain value 199.199.199.1.
    
@v4 @options @subnet
    Scenario: v4.options.resource-location-servers

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with resource-location-servers option with value 199.199.199.1.
    Server is started. 

    Test Procedure:
    Client requests option 11.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 11.
    Response option 11 MUST contain value 199.199.199.1.
    
@v4 @options @subnet
    Scenario: v4.options.host-name

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with host-name option with value isc.example.com.
    Server is started. 

    Test Procedure:
    Client requests option 12.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 12.
    Response option 12 MUST contain value isc.example.com.
    
@v4 @options @subnet
    Scenario: v4.options.boot-size

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with boot-size option with value 55.
    Server is started. 

    Test Procedure:
    Client requests option 13.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 13.
    Response option 13 MUST contain value 55.
    
@v4 @options @subnet
    Scenario: v4.options.merit-dump

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with merit-dump option with value some-string.
    Server is started. 

    Test Procedure:
    Client requests option 14.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 14.
    Response option 14 MUST contain value some-string.
    
@v4 @options @subnet
    Scenario: v4.options.domain-name

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    #Server is configured with domain-name option with value True.
    Server is started. 

    Test Procedure:
    #Client requests option .
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    #Response MUST include option .
    #Response option  MUST contain value .
    
@v4 @options @subnet
    Scenario: v4.options.swap-server

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with swap-server option with value 199.199.199.1.
    Server is started. 

    Test Procedure:
    Client requests option 16.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 16.
    Response option 16 MUST contain value 199.199.199.1.
    
@v4 @options @subnet
    Scenario: v4.options.root-path

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with root-path option with value /some/location/example/.
    Server is started. 

    Test Procedure:
    Client requests option 17.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 17.
    Response option 17 MUST contain value /some/location/example/.
    
@v4 @options @subnet
    Scenario: v4.options.extensions-path

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with extensions-path option with value /some/location/example/.
    Server is started. 

    Test Procedure:
    Client requests option 18.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 18.
    Response option 18 MUST contain value /some/location/example/.
    
@v4 @options @subnet
    Scenario: v4.options.policy-filter

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with policy-filter option with value 199.199.199.1.
    Server is started. 

    Test Procedure:
    Client requests option 21.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 21.
    Response option 21 MUST contain value 199.199.199.1.
    
@v4 @options @subnet
    Scenario: v4.options.max-dgram-reassembly

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with max-dgram-reassembly option with value 48.
    Server is started. 

    Test Procedure:
    Client requests option 22.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 22.
    Response option 22 MUST contain value 48.
    
@v4 @options @subnet
    Scenario: v4.options.default-ip-ttl

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with default-ip-ttl option with value 86.
    Server is started. 

    Test Procedure:
    Client requests option 23.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 23.
    Response option 23 MUST contain value 86.
    
@v4 @options @subnet
    Scenario: v4.options.path-mtu-aging-timeout

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with path-mtu-aging-timeout option with value 85.
    Server is started. 

    Test Procedure:
    Client requests option 24.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 24.
    Response option 24 MUST contain value 85.
    
@v4 @options @subnet
    Scenario: v4.options.path-mtu-plateau-table

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with path-mtu-plateau-table option with value 48.
    Server is started. 

    Test Procedure:
    Client requests option 25.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 25.
    Response option 25 MUST contain value 48.
    
@v4 @options @subnet
    Scenario: v4.options.interface-mtu

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with interface-mtu option with value 321.
    Server is started. 

    Test Procedure:
    Client requests option 26.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 26.
    Response option 26 MUST contain value 321.
    
@v4 @options @subnet
    Scenario: v4.options.broadcast-address

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with broadcast-address option with value 255.255.255.0.
    Server is started. 

    Test Procedure:
    Client requests option 28.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 28.
    Response option 28 MUST contain value 255.255.255.0.
    
@v4 @options @subnet
    Scenario: v4.options.router-solicitation-address

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with router-solicitation-address option with value 199.199.199.1.
    Server is started. 

    Test Procedure:
    Client requests option 32.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 32.
    Response option 32 MUST contain value 199.199.199.1.
    
@v4 @options @subnet
    Scenario: v4.options.static-routes

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with static-routes option with value 199.199.199.1.
    Server is started. 

    Test Procedure:
    Client requests option 33.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 33.
    Response option 33 MUST contain value 199.199.199.1.
    
@v4 @options @subnet
    Scenario: v4.options.arp-cache-timeout

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with arp-cache-timeout option with value 48.
    Server is started. 

    Test Procedure:
    Client requests option 35.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 35.
    Response option 35 MUST contain value 48.
    
@v4 @options @subnet
    Scenario: v4.options.default-tcp-ttl

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with default-tcp-ttl option with value 44.
    Server is started. 

    Test Procedure:
    Client requests option 37.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 37.
    Response option 37 MUST contain value 44.
    
@v4 @options @subnet
    Scenario: v4.options.tcp-keepalive-internal

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with tcp-keepalive-internal option with value 4896.
    Server is started. 

    Test Procedure:
    Client requests option 38.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 38.
    Response option 38 MUST contain value 4896.
    
@v4 @options @subnet
    Scenario: v4.options.nis-domain

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with nis-domain option with value some.domain.com.
    Server is started. 

    Test Procedure:
    Client requests option 40.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 40.
    Response option 40 MUST contain value some.domain.com.
    
@v4 @options @subnet
    Scenario: v4.options.nis-servers

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with nis-servers option with value 199.199.199.1.
    Server is started. 

    Test Procedure:
    Client requests option 41.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 41.
    Response option 41 MUST contain value 199.199.199.1.
    
@v4 @options @subnet
    Scenario: v4.options.ntp-servers

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with ntp-servers option with value 199.199.199.1.
    Server is started. 

    Test Procedure:
    Client requests option 41.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 41.
    Response option 41 MUST contain value 199.199.199.1.
    
@v4 @options @subnet
    Scenario: v4.options.netbios-name-servers

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with netbios-name-servers option with value 188.188.188.2.
    Server is started. 

    Test Procedure:
    Client requests option 44.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 44.
    Response option 44 MUST contain value 188.188.188.2.
    
@v4 @options @subnet
    Scenario: v4.options.netbios-dd-server

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with netbios-dd-server option with value 188.188.188.2.
    Server is started. 

    Test Procedure:
    Client requests option 45.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 45.
    Response option 45 MUST contain value 188.188.188.2.
    
@v4 @options @subnet
    Scenario: v4.options.netbios-node-type

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with netbios-node-type option with value 55.
    Server is started. 

    Test Procedure:
    Client requests option 46.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 46.
    Response option 46 MUST contain value 55.
    
@v4 @options @subnet
    Scenario: v4.options.netbios-scope

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with netbios-scope option with value global.
    Server is started. 

    Test Procedure:
    Client requests option 47.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 47.
    Response option 47 MUST contain value global.
    
@v4 @options @subnet
    Scenario: v4.options.font-servers

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with font-servers option with value 188.188.188.2.
    Server is started. 

    Test Procedure:
    Client requests option 48.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 48.
    Response option 48 MUST contain value 188.188.188.2.
    
@v4 @options @subnet
    Scenario: v4.options.x-display-manager

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with x-display-manager option with value 188.188.188.2.
    Server is started. 

    Test Procedure:
    Client requests option 49.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 49.
    Response option 49 MUST contain value 188.188.188.2.
    
@v4 @options @subnet
    Scenario: v4.options.dhcp-requested-address

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with dhcp-requested-address option with value 188.188.188.2.
    Server is started. 

    Test Procedure:
    Client requests option 50.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 50.
    Response option 50 MUST contain value 188.188.188.2.
    
@v4 @options @subnet
    Scenario: v4.options.dhcp-option-overload

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with dhcp-option-overload option with value 88.
    Server is started. 

    Test Procedure:
    Client requests option 52.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 52.
    Response option 52 MUST contain value 88.
    
@v4 @options @subnet
    Scenario: v4.options.dhcp-message

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with dhcp-message option with value some-message.
    Server is started. 

    Test Procedure:
    Client requests option 56.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 56.
    Response option 56 MUST contain value some-message.
    
@v4 @options @subnet
    Scenario: v4.options.dhcp-max-message-size

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with dhcp-max-message-size option with value 2349.
    Server is started. 

    Test Procedure:
    Client requests option 57.
    Client sends DISCOVER message and expect OFFER response.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 57.
    Response option 57 MUST contain value 2349.
