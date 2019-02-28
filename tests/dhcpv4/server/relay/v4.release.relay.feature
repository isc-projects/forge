

Feature: DHCPv4 address release process
    Those are simple DHCPv4 tests for address releasing in relay traffic.
    
@v4 @dhcp4 @relay @release
    Scenario: v4.relay.release-success

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    # this is setting for every message in this test
    Set network variable source_port with value 67.
    Set network variable source_address with value $(GIADDR4).
    Set network variable destination_address with value $(SRV4_ADDR).

    Client sets giaddr value to $(GIADDR4).
    Client sets hops value to 1.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    #Response MUST contain giaddr $(GIADDR4).
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client sets giaddr value to $(GIADDR4).
    Client sets hops value to 1.
    Client copies server_id option from received message.
	Client adds to the message requested_addr with value 192.168.50.1.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.
    
    Test Procedure:
    Client sets giaddr value to $(GIADDR4).
    Client sets hops value to 1.
    Client copies server_id option from received message.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.
    
    Pass Criteria:
    Server MUST NOT respond.
    
    Test Procedure:
    Client sets giaddr value to $(GIADDR4).
    Client sets hops value to 1.
    Client sets chaddr value to 00:00:00:00:00:11.
    Client adds to the message client_id with value 00010203040111.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Client sets giaddr value to $(GIADDR4).
    Client sets hops value to 1.
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    #Response MUST contain giaddr $(GIADDR4).
    Response option 1 MUST contain value 255.255.255.0.
    
@v4 @dhcp4 @relay @release
    Scenario: v4.relay.release-success-with-additional-offer

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Set network variable source_port with value 67.
    Set network variable source_address with value $(GIADDR4).
    Set network variable destination_address with value $(SRV4_ADDR).

    Client sets giaddr value to $(GIADDR4).
    Client sets hops value to 1.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.1.
	Response MUST include option 1.
	Response MUST include option 54.
    Response option 1 MUST contain value 255.255.255.0.
	Response option 54 MUST contain value $(SRV4_ADDR).
	
    Test Procedure:
    Client sets giaddr value to $(GIADDR4).
    Client sets hops value to 1.
    Client copies server_id option from received message.
	Client adds to the message requested_addr with value 192.168.50.1.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
	Response MUST include option 1.
	Response MUST include option 54.
    Response option 1 MUST contain value 255.255.255.0.
	Response option 54 MUST contain value $(SRV4_ADDR).
	
    Test Procedure:
    Client saves server_id option from received message.
    Client sets giaddr value to $(GIADDR4).
    Client sets hops value to 1.
    Client sets chaddr value to 00:00:00:00:00:00.
    Client adds to the message client_id with value 00010203040506.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST NOT respond.
    
    Test Procedure:
    Client sets giaddr value to $(GIADDR4).
    Client sets hops value to 1.
    Client sets chaddr value to default.
    Client adds saved options. And Erase.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.
    
    Pass Criteria:
    Server MUST NOT respond.
    
    Test Procedure:
    Client sets giaddr value to $(GIADDR4).
    Client sets hops value to 1.
    Client sets chaddr value to 00:00:00:00:00:11.
    Client adds to the message client_id with value 00010203040111.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
	Response MUST include option 1.
	Response MUST include option 54.
    Response option 1 MUST contain value 255.255.255.0.
	Response option 54 MUST contain value $(SRV4_ADDR).

@v4 @dhcp4 @relay @release
Scenario: v4.relay.release-only-chaddr-same-chaddr

	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Send server configuration using SSH and config-file.
DHCP server is started.
	
	Test Procedure:
    Set network variable source_port with value 67.
    Set network variable source_address with value $(GIADDR4).
    Set network variable destination_address with value $(SRV4_ADDR).

    Client sets giaddr value to $(GIADDR4).
    Client sets hops value to 1.
	Client sets chaddr value to 00:1F:D0:00:00:11.
	Client requests option 1.
	Client sends DISCOVER message.
	
	Pass Criteria:
	Server MUST respond with OFFER message.
	Response MUST contain yiaddr 192.168.50.1.
	Response MUST include option 1.
	Response MUST include option 54.
	Response option 1 MUST contain value 255.255.255.0.
	Response option 54 MUST contain value $(SRV4_ADDR).
	
	Test Procedure:
    Client sets giaddr value to $(GIADDR4).
    Client sets hops value to 1.
	Client sets chaddr value to 00:1f:d0:00:00:11.
	Client copies server_id option from received message.
	Client adds to the message requested_addr with value 192.168.50.1.
	Client requests option 1.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with ACK message.
	Response MUST contain yiaddr 192.168.50.1.
	Response MUST include option 1.
	Response MUST include option 54.
	Response option 1 MUST contain value 255.255.255.0.
	Response option 54 MUST contain value $(SRV4_ADDR).
	
	Test Procedure:
	#client id changed!
    Client sets giaddr value to $(GIADDR4).
    Client sets hops value to 1.
	Client sets chaddr value to 00:1f:d0:00:00:11.
	Client copies server_id option from received message.
	Client sets ciaddr value to 192.168.50.1.
	Client sends RELEASE message.
	
	#address not released
	Pass Criteria:
	Server MUST NOT respond.
	
	Test Procedure:
	Client sets chaddr value to 00:00:00:00:00:00.
	Client requests option 1.
    Client sets giaddr value to $(GIADDR4).
    Client sets hops value to 1.
	Client sends DISCOVER message.
	
	Pass Criteria:
	Server MUST respond with OFFER message.
	Response MUST include option 1.
	Response MUST contain yiaddr 192.168.50.1.
	Response MUST include option 1.
	Response MUST include option 54.
	Response option 1 MUST contain value 255.255.255.0.
	Response option 54 MUST contain value $(SRV4_ADDR).