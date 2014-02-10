

Feature: DHCPv4 options part1
    Those are simple DHCPv4 assigned address tests.
    
@v4 @request
    Scenario: v4.request.success

    Test Setup:
    Server is configured with 192.0.2.0/24 subnet with 192.0.2.1-192.0.2.1 pool.
    Server is started.

    Test Procedure:
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.0.2.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
	Client does include requested_addr with value 192.0.2.1.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.0.2.1.
    Response option 1 MUST contain value 255.255.255.0.

