##
Feature: ISC_DHCP DHCPv6 func
    Tests ISC_DHCP dhcpd pond and pool lease counters
	
@v6 @dhcpd @func @lease-counters
    Scenario: v6.dhcpd.lease-counters
    ##
    ## Checks that the count of total, active, and abandoned leases is
    ## and abandoned-best-match are logged correctly when a declined
    ## address is subsequently reclaimed:
    ##
    ## Step 1: Client 1 gets an address then declines it
    ## Step 2: Client 2 gets an address
    ## Step 3: Client 1 solicits, but is denied
    ##  - should see total 2, active 2, abandoned 1
    ##  - should see best match message for DUID 1
    ## Step 4: Client 1 requests denied address
    ##  - server should reclaim and grant it
    ## Step 5: Client 3 solicits but is denieed
    ##  - should see total 2, active 2, abandoned 0
    ##  - should NOT see best match message for DUID 3
    ##
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::100-3000::101 pool.
    Send server configuration using SSH and config-file.
	DHCP Server is started.
  
    ####################################################
    ## Step 1: Client 1 gets an address then declines it
    ####################################################
	Test Procedure:
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client does include client-id.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	
	Test Procedure:
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Client saves into set no. 1 IA_NA option from received message.
	Client saves into set no. 1 client-id option from received message.
	Client saves into set no. 1 server-id option from received message.

    Test Procedure:
    Client adds saved options in set no. 1. And DONT Erase.
    Client sends DECLINE message.

    Pass Criteria:
    Server MUST respond with REPLY message.

    ####################################################
    ## Step 2: Client 2 gets an address
    ####################################################
	Test Procedure:
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:02.
    Client does include client-id.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	
	Test Procedure:
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
    Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.

    ####################################################
    ## Step 3: Client 1 solicits, but is denied
    ##  - should see total 2, active 2, abandoned 1
    ##  - should see best match message for DUID 1
    ####################################################
	Test Procedure:
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client does include client-id.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 13.
    Response sub-option 13 from option 3 MUST contain statuscode 2.
    DHCP log contains 1 of line: shared network 3000::/64: 2 total, 1 active,  1 abandoned
    DHCP log contains 1 of line: Best match for DUID 00:03:00:01:ff:ff:ff:ff:ff:01 is an abandoned address

    ####################################################
    ## Step 4: Client 1 reclaims denied address
    ##  - server should reclaim and grant it
    ####################################################
	Test Procedure:
    Client adds saved options in set no. 1. and Erase.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.

    ####################################################
    ## Step 5: Client 3 solicits but is denieed
    ##  - should see total 2, active 2, abandoned 0
    ##  - should NOT see best match message for DUID 3
    ####################################################
	Test Procedure:
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:03.
    Client does include client-id.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 13.
    Response sub-option 13 from option 3 MUST contain statuscode 2.
    DHCP log contains 1 of line: shared network 3000::/64: 2 total, 2 active,  0 abandoned
    DHCP log contains 0 of line: Best match for DUID 00:03:00:01:ff:ff:ff:ff:ff:03 is an abandoned address
