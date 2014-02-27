

Feature: DHCPv4 address request process
    Those are simple DHCPv4 tests for address assignment.

@v4 @request
    Scenario: v4.request.success-chaddr

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
	Response MUST include option 1.
    Response option 1 MUST contain value 255.255.255.0.

@v4 @request
    Scenario: v4.request.success-chaddr-empty-pool

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server is started.

    Test Procedure:
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
    Client copies server_id option from received message.
    Client does include requested_addr with value 192.168.50.1.
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
    Client requests option 1.
    Client sets chaddr value to ff:01:02:03:ff:04.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with NAK message.
    Response MUST contain yiaddr 0.0.0.0.
    Response MUST contain ciaddr 0.0.0.0.
    Response MUST contain siaddr 0.0.0.0.
    Response MUST contain giaddr 0.0.0.0.
	Response MUST include option 54.
    Response option 54 MUST contain value $(SRV4_ADDR).

@v4 @request
    Scenario: v4.request.success-client-id

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server is started.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:00.
    Client does include client_id with value 00010203040506.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.1.
	Response MUST include option 1.
	Response MUST include option 54.
	Response MUST include option 61.
    Response option 1 MUST contain value 255.255.255.0.
    Response option 61 MUST contain value 00010203040506.

    Test Procedure:
    Client does include client_id with value 00010203040506.
    Client sets chaddr value to 00:00:00:00:00:00.
    Client copies server_id option from received message.
	Client does include requested_addr with value 192.168.50.1.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
	Response MUST include option 1.
	Response MUST include option 54.
	Response MUST include option 61.
    Response option 1 MUST contain value 255.255.255.0.
    Response option 61 MUST contain value 00010203040506.

@v4 @request
    Scenario: v4.request.success-client-id-empty-pool

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server is started.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:00.
    Client does include client_id with value 00010203040506.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.1.
	Response MUST include option 1.
	Response MUST include option 54.
	Response MUST include option 61.
    Response option 1 MUST contain value 255.255.255.0.
	Response option 61 MUST contain value 00010203040506.

    Test Procedure:
    Client does include client_id with value 00010203040506.
    Client sets chaddr value to 00:00:00:00:00:00.
    Client copies server_id option from received message.
	Client does include requested_addr with value 192.168.50.1.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
	Response MUST include option 1.
	Response MUST include option 54.
	Response MUST include option 61.
    Response option 1 MUST contain value 255.255.255.0.
    Response option 61 MUST contain value 00010203040506.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:00.
    Client does include client_id with value 00020304050607.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with NAK message.
    Response MUST contain yiaddr 0.0.0.0.
    Response MUST contain ciaddr 0.0.0.0.
    Response MUST contain siaddr 0.0.0.0.
    Response MUST contain giaddr 0.0.0.0.
	Response MUST include option 54.
	Response option 54 MUST contain value $(SRV4_ADDR).
	
@v4 @request
    Scenario: v4.request.success-second-request-fail

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server is started.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:00.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:00.
    Client copies server_id option from received message.
	Client does include requested_addr with value 192.168.50.1.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
	Response MUST include option 1.
	Response MUST include option 54.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client sets chaddr value to 00:00:00:22:11:00.
    Client copies server_id option from received message.
	Client does include requested_addr with value 192.168.50.1.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with NAK message.
    Response MUST contain yiaddr 0.0.0.0.
    Response MUST contain ciaddr 0.0.0.0.
    Response MUST contain siaddr 0.0.0.0.
    Response MUST contain giaddr 0.0.0.0.
	Response MUST include option 54.
	Response option 54 MUST contain value $(SRV4_ADDR).