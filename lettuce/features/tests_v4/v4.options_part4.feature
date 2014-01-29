

Feature: DHCPv4 options part4
    This is a simple DHCPv4 options validation. Its purpose is to check
    how server is configuring corner values. 

	# References in all tests are temporary empty, that's intentional.

@v4 @options @subnet
    Scenario: v4.options.malformed.values.pool

    Test Setup:
    Server is configured with 256.0.2.0/24 subnet with 256.0.2.1-256.0.2.10 pool.
    Server failed to start. During configuration process.

    #Test Setup:
    #Server is configured with 127.0.0.1/24 subnet with 127.0.0.1-127.0.0.1 pool.
    #Server failed to start. During configuration process.
    
    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is started.

@v4 @options @subnet
    Scenario: v4.options.malformed.values.ip-forwarding

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with ip-forwarding option with value 2.
    Server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with ip-forwarding option with value 1.
    Server is started.
    
@v4 @options @subnet
    Scenario: v4.options.malformed.values.subnet-mask

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with subnet-mask option with value 255.255.266.0.
    Server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with subnet-mask option with value 255.255.255.0.
    Server is started.
    
@v4 @options @subnet
    Scenario: v4.options.malformed.values.time-offset

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with time-offset option with value -2147483649.
    Server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with time-offset option with value -2147483648.
	Server is started.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with time-offset option with value 2147483647.
	Server is started.
	    
    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with time-offset option with value 2147483648.
    Server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with time-offset option with value 50.
    Server is started.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with time-offset option with value 0.
    Server is started.

@v4 @options @subnet
    Scenario: v4.options.malformed.values.boot-size

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with boot-size option with value 65536.
    Server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with boot-size option with value -1.
    Server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with boot-size option with value 655.
    Server is started.

@v4 @options @subnet
    Scenario: v4.options.malformed.values.policy-filter
	# Allowed only pairs of addresses
    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with policy-filter option with value 199.199.199.1.
    Server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with policy-filter option with value 199.199.199.1,50.50.50.1,60.60.60.5.
    Server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with policy-filter option with value 199.199.199.1,50.50.50.1.
    Server is started.

@v4 @options @subnet
    Scenario: v4.options.malformed.values.max-dgram-reassembly
	#Unsigned integer (0 to 65535) minimum value: 576
	
    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with max-dgram-reassembly option with value -1.
    Server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with max-dgram-reassembly option with value 0.
    Server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with max-dgram-reassembly option with value 575.
    Server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with max-dgram-reassembly option with value 65536.
    Server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with max-dgram-reassembly option with value 576.
    Server is started.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with max-dgram-reassembly option with value 65535.
    Server is started.
    
@v4 @options @subnet
    Scenario: v4.options.malformed.values.default-ip-ttl

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with default-ip-ttl option with value 0.
    Server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with default-ip-ttl option with value 1.
    Server is started.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with default-ip-ttl option with value 255.
	Server is started.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with default-ip-ttl option with value 256.
    Server failed to start. During configuration process.

@v4 @options @subnet
    Scenario: v4.options.malformed.values.path-mtu-aging-timeout
	#Unsigned integer (0 to 65535) minimum: 68

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with path-mtu-aging-timeout option with value 67.
    Server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with path-mtu-aging-timeout option with value -1.
    Server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with path-mtu-aging-timeout option with value 65536.
    Server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with path-mtu-aging-timeout option with value 65535.
    Server is started.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with path-mtu-aging-timeout option with value 68.
    Server is started.


@v4 @options @subnet
    Scenario: v4.options.malformed.values.static-routes
	# pair of addresses 0.0.0.0 forbidden

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with static-routes option with value 199.199.199.1.
    Server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with static-routes option with value 199.199.199.1,70.70.70.5,80.80.80.80.
    Server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with static-routes option with value 199.199.199.1,0.0.0.0.
    Server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with static-routes option with value 199.199.199.1,70.70.70.5,80.80.80.80,10.10.10.5.
    Server is started.

@v4 @options @subnet
    Scenario: v4.options.malformed.values.arp-cache-timeout

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with arp-cache-timeout option with value -1.
    Server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with arp-cache-timeout option with value 4294967296.
    Server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with arp-cache-timeout option with value 0.
	Server is started.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with arp-cache-timeout option with value 4294967295.
    Server is started.

@v4 @options @subnet
    Scenario: v4.options.malformed.values.default-tcp-ttl

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with default-tcp-ttl option with value 0.
    Server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with default-tcp-ttl option with value 256.
    Server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with default-tcp-ttl option with value 255.
    Server is started.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with default-tcp-ttl option with value 1.
    Server is started.
    
@v4 @options @subnet
    Scenario: v4.options.malformed.values.dhcp-option-overload

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with dhcp-option-overload option with value 0.
    Server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with dhcp-option-overload option with value 4.
    Server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with dhcp-option-overload option with value 1.
    Server is started.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with dhcp-option-overload option with value 2.
    Server is started.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with dhcp-option-overload option with value 3.
    Server is started.

@v4 @options @subnet
    Scenario: v4.options.malformed.values.dhcp-max-message-size

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with dhcp-max-message-size option with value 0.
    Server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with dhcp-max-message-size option with value 575.
	Server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with dhcp-max-message-size option with value 576.
	Server is started.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with dhcp-max-message-size option with value 65536.
    Server failed to start. During configuration process.

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.10 pool.
    Server is configured with dhcp-max-message-size option with value 65535.
    Server is started.
