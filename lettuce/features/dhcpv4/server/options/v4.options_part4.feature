

Feature: DHCPv4 options part4
    This is a simple DHCPv4 options validation. Its purpose is to check
    how server handling with configuration of corner values. 

	# References in all tests are temporary empty, that's intentional.

@v4 @dhcp4 @options @subnet
    Scenario: v4.options.malformed.values.pool

    Test Setup:
    Server is configured with 256.0.2.0/24 subnet with 256.0.2.1-256.0.2.10 pool.
    DHCP server failed to start. During configuration process.

    #Test Setup:
    #Server is configured with 127.0.0.1/24 subnet with 127.0.0.1-127.0.0.1 pool.
    #DHCP server failed to start. During configuration process.
    
    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    DHCP server is started.

@v4 @dhcp4 @options @subnet
    Scenario: v4.options.malformed.values.ip-forwarding

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with ip-forwarding option with value 2.
    DHCP server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with ip-forwarding option with value 1.
    DHCP server is started.
    
@v4 @dhcp4 @options @subnet
    Scenario: v4.options.malformed.values.subnet-mask

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with subnet-mask option with value 255.255.266.0.
    DHCP server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with subnet-mask option with value 255.255.255.0.
    DHCP server is started.
    
@v4 @dhcp4 @options @subnet
    Scenario: v4.options.malformed.values.time-offset

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with time-offset option with value -2147483649.
    DHCP server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with time-offset option with value -2147483648.
	DHCP server is started.

    DHCP server is stopped.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with time-offset option with value 2147483647.
	DHCP server is started.
	    
    DHCP server is stopped.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with time-offset option with value 2147483648.
    DHCP server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with time-offset option with value 50.
    DHCP server is started.

    DHCP server is stopped.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with time-offset option with value 0.
    DHCP server is started.

@v4 @dhcp4 @options @subnet
    Scenario: v4.options.malformed.values.boot-size

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with boot-size option with value 65536.
    DHCP server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with boot-size option with value -1.
    DHCP server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with boot-size option with value 655.
    DHCP server is started.

@v4 @dhcp4 @options @subnet
    Scenario: v4.options.malformed.values.policy-filter
	# Allowed only pairs of addresses
    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with policy-filter option with value 199.199.199.1.
    DHCP server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with policy-filter option with value 199.199.199.1,50.50.50.1,60.60.60.5.
    DHCP server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with policy-filter option with value 199.199.199.1,50.50.50.1.
    DHCP server is started.

@v4 @dhcp4 @options @subnet
    Scenario: v4.options.malformed.values.max-dgram-reassembly
	#Unsigned integer (0 to 65535) minimum value: 576
	
    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with max-dgram-reassembly option with value -1.
    DHCP server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with max-dgram-reassembly option with value 0.
    DHCP server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with max-dgram-reassembly option with value 575.
    DHCP server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with max-dgram-reassembly option with value 65536.
    DHCP server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with max-dgram-reassembly option with value 576.
    DHCP server is started.

    DHCP server is stopped.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with max-dgram-reassembly option with value 65535.
    DHCP server is started.
    
@v4 @dhcp4 @options @subnet
    Scenario: v4.options.malformed.values.default-ip-ttl

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with default-ip-ttl option with value 0.
    DHCP server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with default-ip-ttl option with value 1.
    DHCP server is started.

    DHCP server is stopped.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with default-ip-ttl option with value 255.
	DHCP server is started.

    DHCP server is stopped.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with default-ip-ttl option with value 256.
    DHCP server failed to start. During configuration process.

@v4 @dhcp4 @options @subnet
    Scenario: v4.options.malformed.values.path-mtu-aging-timeout
	#Unsigned integer (0 to 65535) minimum: 68

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with path-mtu-aging-timeout option with value 67.
    DHCP server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with path-mtu-aging-timeout option with value -1.
    DHCP server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with path-mtu-aging-timeout option with value 65536.
    DHCP server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with path-mtu-aging-timeout option with value 65535.
    DHCP server is started.

    DHCP server is stopped.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with path-mtu-aging-timeout option with value 68.
    DHCP server is started.

@v4 @dhcp4 @options @subnet
    Scenario: v4.options.malformed.values.static-routes
	# pair of addresses 0.0.0.0 forbidden

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with static-routes option with value 199.199.199.1.
    DHCP server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with static-routes option with value 199.199.199.1,70.70.70.5,80.80.80.80.
    DHCP server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with static-routes option with value 199.199.199.1,0.0.0.0.
    DHCP server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with static-routes option with value 199.199.199.1,70.70.70.5,80.80.80.80,10.10.10.5.
    DHCP server is started.

@v4 @dhcp4 @options @subnet
    Scenario: v4.options.malformed.values.arp-cache-timeout

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with arp-cache-timeout option with value -1.
    DHCP server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with arp-cache-timeout option with value 4294967296.
    DHCP server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with arp-cache-timeout option with value 0.
	DHCP server is started.

    DHCP server is stopped.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with arp-cache-timeout option with value 4294967295.
    DHCP server is started.

@v4 @dhcp4 @options @subnet
    Scenario: v4.options.malformed.values.default-tcp-ttl

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with default-tcp-ttl option with value 0.
    DHCP server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with default-tcp-ttl option with value 256.
    DHCP server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with default-tcp-ttl option with value 255.
    DHCP server is started.

    DHCP server is stopped.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with default-tcp-ttl option with value 1.
    DHCP server is started.
    
@v4 @dhcp4 @options @subnet
    Scenario: v4.options.malformed.values.dhcp-option-overload

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with dhcp-option-overload option with value 0.
    DHCP server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with dhcp-option-overload option with value 4.
    DHCP server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with dhcp-option-overload option with value 1.
    DHCP server is started.

    DHCP server is stopped.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with dhcp-option-overload option with value 2.
    DHCP server is started.

    DHCP server is stopped.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with dhcp-option-overload option with value 3.
    DHCP server is started.

@v4 @dhcp4 @options @subnet
    Scenario: v4.options.malformed.values.dhcp-max-message-size

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with dhcp-max-message-size option with value 0.
    DHCP server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with dhcp-max-message-size option with value 575.
	DHCP server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with dhcp-max-message-size option with value 576.
	DHCP server is started.

    DHCP server is stopped.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with dhcp-max-message-size option with value 65536.
    DHCP server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server is configured with dhcp-max-message-size option with value 65535.
    DHCP server is started.
