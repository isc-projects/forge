Feature: ISC_DHCP DHCPv6 Keywords fixed-address6
    Tests ISC_DHCP dhcpd configuration keywords fixed-address6
	
@v6 @dhcpd @keyword @fixed-address6
    Scenario: v6.dhcpd.keyword.fixed-address6
    ##
    ## Tests address assignment when fixed-address6 is used.
    ##
    ## Server is configured with one subnet 3000::/64, with one pool of two 
    ## addresses 3000::1 - 3000::2.  One address, 3000::1, is reserved to a 
    ## specific client (DUID2) using the host statement and fixed-address6.
    ##
    ## Stage 1: Client with DUID1 asks for and should be granted 3000::2,
    ## the only address available to Clients who are NOT DUID2
    ##
    ## Stage 2: Client with DUID3 solicts an address but should be denied
    ##
    ## Stage 3: Client with DUID2 solicits and should be should be granted
    ## 3000::1, the reserved address.
    ##
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::2 pool.
    Run configuration command: host specialclient {
    Run configuration command:   host-identifier option dhcp6.client-id 00:03:00:01:ff:ff:ff:ff:ff:02;
    Run configuration command:   fixed-address6 3000::1; }
    Send server configuration using SSH and config-file.
	DHCP Server is started.

    # Stage 1: DUID1 asks for an address

	Test Procedure: 01
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

    # Server should offer 3000::2

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::2.

    # DUID1 accepts the address	

	Test Procedure: 02
	Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure: 03
	Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client sends CONFIRM message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 13.
	Response option 13 MUST contain status-code 0. 

    #  Stage 2: DUID3 asks for an address 

	Test Procedure: 04
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:03.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

    # Server should response with NoAddrAvail

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
	Response option 3 MUST contain sub-option 13.
	Response sub-option 13 from option 3 MUST contain statuscode 2. 

    #  Stage 3: DUID2 asks for an address

	Test Procedure: 05
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:02.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

    # Server should offer the reserved address, 3000::1

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::1.

	Test Procedure: 06
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::1.

    Test Procedure: 07
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
    Client sends CONFIRM message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 1.
    Response MUST include option 2.
    Response MUST include option 13.
    Response option 13 MUST contain status-code 0.
