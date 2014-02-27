

Feature: DHCPv4 address release process
    Those are simple DHCPv4 tests for address releasing.
    
@v4 @release
    Scenario: v4.release.success

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server is started.

    Test Procedure:
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
	Client does include requested_addr with value 192.168.50.1.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.
    
    Test Procedure:
    Client copies server_id option from received message.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.
    
    Pass Criteria:
    Server MUST NOT respond.
    
    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:11.
    Client does include client_id with value 00010203040111.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.
    
@v4 @release
    Scenario: v4.release.success-with-additional-offer

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server is started.

    Test Procedure:
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.
	Response option 54 MUST contain value $(SRV4_ADDR).
	
    Test Procedure:
    Client copies server_id option from received message.
	Client does include requested_addr with value 192.168.50.1.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.
	Response option 54 MUST contain value $(SRV4_ADDR).
	
    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:00.
    Client does include client_id with value 00010203040506.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with NAK message.
    Response MUST contain yiaddr 0.0.0.0.
    Response MUST contain ciaddr 0.0.0.0.
    Response MUST contain siaddr 0.0.0.0.
    Response MUST contain giaddr 0.0.0.0.
	Response option 54 MUST contain value $(SRV4_ADDR).
    
    Test Procedure:
    Client sets chaddr value to default.
    Client copies server_id option from received message.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.
    
    Pass Criteria:
    Server MUST NOT respond.
    
    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:11.
    Client does include client_id with value 00010203040111.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.
	Response option 54 MUST contain value $(SRV4_ADDR).
    
@v4 @release
    Scenario: v4.release.fail-with-different-chaddr-client-id

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server is started.

    Test Procedure:
    Client sets chaddr value to 00:1F:D0:00:00:11.
    Client does include client_id with value 00001FD0040111.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.
    Response option 54 MUST contain value $(SRV4_ADDR).
    Response option 61 MUST contain value 00001FD0040111.

    Test Procedure:
    Client sets chaddr value to 00:1f:d0:00:00:11.
    Client does include client_id with value 00001FD0040111.
    Client copies server_id option from received message.
	Client does include requested_addr with value 192.168.50.1.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.
    Response option 54 MUST contain value $(SRV4_ADDR).
    Response option 61 MUST contain value 00001FD0040111.

    Test Procedure:
    Client sets chaddr value to 00:1f:d0:11:22:33.
    Client does include client_id with value 00001FD0112233.
    Client copies server_id option from received message.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.

    #address not released
    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:00.
    Client does include client_id with value 00010203040111.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with NAK message.
    Response MUST contain yiaddr 0.0.0.0.
    Response MUST contain ciaddr 0.0.0.0.
    Response MUST contain siaddr 0.0.0.0.
    Response MUST contain giaddr 0.0.0.0.
    Response option 54 MUST contain value $(SRV4_ADDR).
    Response option 61 MUST contain value 00010203040111.

@v4 @release
    Scenario: v4.release.fail-with-same-chaddr-different-client-id

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server is started.

    Test Procedure:
    Client sets chaddr value to 00:1F:D0:00:00:11.
    Client does include client_id with value 00001FD0040111.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.
    Response option 54 MUST contain value $(SRV4_ADDR).
    Response option 61 MUST contain value 00001FD0040111.

    Test Procedure:
    Client sets chaddr value to 00:1f:d0:00:00:11.
    Client does include client_id with value 00001FD0040111.
    Client copies server_id option from received message.
	Client does include requested_addr with value 192.168.50.1.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.
    Response option 54 MUST contain value $(SRV4_ADDR).
    Response option 61 MUST contain value 00001FD0040111.

    Test Procedure:
    #client id changed!
    Client sets chaddr value to 00:1f:d0:00:00:11.
    Client does include client_id with value 00001FD0112233.
    Client copies server_id option from received message.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.

    #address not released
    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:00.
    Client does include client_id with value 00010203040111.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with NAK message.
    Response MUST contain yiaddr 0.0.0.0.
    Response MUST contain ciaddr 0.0.0.0.
    Response MUST contain siaddr 0.0.0.0.
    Response MUST contain giaddr 0.0.0.0.
    Response option 54 MUST contain value $(SRV4_ADDR).
    Response option 61 MUST contain value 00010203040111.

@v4 @release
    Scenario: v4.release.fail-with-different-chaddr-same-client-id

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server is started.

    Test Procedure:
    Client sets chaddr value to 00:1F:D0:00:00:11.
    Client does include client_id with value 00001FD0040111.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.
    Response option 54 MUST contain value $(SRV4_ADDR).
    Response option 61 MUST contain value 00001FD0040111.

    Test Procedure:
    Client sets chaddr value to 00:1f:d0:00:00:11.
    Client does include client_id with value 00001FD0040111.
    Client copies server_id option from received message.
	Client does include requested_addr with value 192.168.50.1.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.
    Response option 54 MUST contain value $(SRV4_ADDR).
    Response option 61 MUST contain value 00001FD0040111.

    Test Procedure:
    #chaddr changed!
    Client sets chaddr value to 00:1f:d0:11:11:11.
    Client does include client_id with value 00001FD0040111.
    Client copies server_id option from received message.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.

    #address not released
    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:00.
    Client does include client_id with value 00010203040111.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with NAK message.
    Response MUST contain yiaddr 0.0.0.0.
    Response MUST contain ciaddr 0.0.0.0.
    Response MUST contain siaddr 0.0.0.0.
    Response MUST contain giaddr 0.0.0.0.
    Response option 54 MUST contain value $(SRV4_ADDR).
    Response option 61 MUST contain value 00010203040111.
    
@v4 @release
Scenario: v4.release.only.chaddr.same-chaddr

	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Server is started.
	
	Test Procedure:
	Client sets chaddr value to 00:1F:D0:00:00:11.
	Client requests option 1.
	Client sends DISCOVER message.
	
	Pass Criteria:
	Server MUST respond with OFFER message.
	Response MUST include option 1.
	Response MUST contain yiaddr 192.168.50.1.
	Response option 1 MUST contain value 255.255.255.0.
	Response option 54 MUST contain value $(SRV4_ADDR).
	
	Test Procedure:
	Client sets chaddr value to 00:1f:d0:00:00:11.
	Client copies server_id option from received message.
	Client does include requested_addr with value 192.168.50.1.
	Client requests option 1.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with ACK message.
	Response MUST contain yiaddr 192.168.50.1.
	Response option 1 MUST contain value 255.255.255.0.
	Response option 54 MUST contain value $(SRV4_ADDR).
	
	Test Procedure:
	#client id changed!
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
	Client sends DISCOVER message.
	
	Pass Criteria:
	Server MUST respond with OFFER message.
	Response MUST include option 1.
	Response MUST contain yiaddr 192.168.50.1.
	Response option 1 MUST contain value 255.255.255.0.
	Response option 54 MUST contain value $(SRV4_ADDR).

@v4 @release
Scenario: v4.release.fail.only.chaddr.different-chaddr

	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Server is started.
	
	Test Procedure:
	Client sets chaddr value to 00:1F:D0:00:00:11.
	Client requests option 1.
	Client sends DISCOVER message.
	
	Pass Criteria:
	Server MUST respond with OFFER message.
	Response MUST include option 1.
	Response MUST contain yiaddr 192.168.50.1.
	Response option 1 MUST contain value 255.255.255.0.
	Response option 54 MUST contain value $(SRV4_ADDR).
	
	Test Procedure:
	Client sets chaddr value to 00:1f:d0:00:00:11.
	Client copies server_id option from received message.
	Client does include requested_addr with value 192.168.50.1.
	Client requests option 1.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with ACK message.
	Response MUST contain yiaddr 192.168.50.1.
	Response option 1 MUST contain value 255.255.255.0.
	Response option 54 MUST contain value $(SRV4_ADDR).
	
	Test Procedure:
	#chaddr changed!
	Client sets chaddr value to 00:1f:d0:11:11:11.
	Client copies server_id option from received message.
	Client sets ciaddr value to 192.168.50.1.
	Client sends RELEASE message.
	
	#address not released
	Pass Criteria:
	Server MUST NOT respond.
	
	Test Procedure:
	Client sets chaddr value to 00:00:00:00:00:00.
	Client requests option 1.
	Client sends DISCOVER message.
	
	Pass Criteria:
	Server MUST respond with NAK message.
    Response MUST contain yiaddr 0.0.0.0.
    Response MUST contain ciaddr 0.0.0.0.
    Response MUST contain siaddr 0.0.0.0.
    Response MUST contain giaddr 0.0.0.0.
	Response option 54 MUST contain value $(SRV4_ADDR).