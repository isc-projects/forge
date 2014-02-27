

Feature: DHCPv4 address release process
    Those are simple DHCPv4 tests for address releasing.
    
@v4 @request
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
    
@v4 @request
    Scenario: v4.release.success-other

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
    Client sets chaddr value to 00:00:00:00:00:00.
    Client does include client_id with value 00010203040506.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with NAK message.
    
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