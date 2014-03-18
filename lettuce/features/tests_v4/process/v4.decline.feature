

Feature: DHCPv4 address decline process
    Those are simple DHCPv4 tests for declining assigned address.
    
@v4 @decline
Scenario: v4.decline.success

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server is started.

    Test Procedure:
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.1.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.

    Test Procedure:
    Client copies server_id option from received message.
    Client sets ciaddr value to 0.0.0.0.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client sends DECLINE message.

    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:11.
    Client adds to the message client_id with value 00010203040111.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.1.

@v4 @decline
Scenario: v4.decline.fail-without-serverid

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server is started.

    Test Procedure:
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.1.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.

    Test Procedure:
    Client sets ciaddr value to 0.0.0.0.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client sends DECLINE message.

    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:11.
    Client adds to the message client_id with value 00010203040111.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with NAK message.

@v4 @decline
Scenario: v4.decline.fail-without-serverid

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server is started.

    Test Procedure:
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.1.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.

    Test Procedure:
    Client sets ciaddr value to 0.0.0.0.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client sends DECLINE message.

    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:11.
    Client adds to the message client_id with value 00010203040111.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with NAK message.

@v4 @decline
Scenario: v4.decline.fail-without-requested-ip-address

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server is started.

    Test Procedure:
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.1.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.

    Test Procedure:
    Client sets ciaddr value to 0.0.0.0.
    Client copies server_id option from received message.
    Client sends DECLINE message.

    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:11.
    Client adds to the message client_id with value 00010203040111.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with NAK message.

@v4 @decline
Scenario: v4.decline.fail-without-client-id

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server is started.

    Test Procedure:
    Client adds to the message client_id with value 00010203040111.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.1.
    Response MUST include option 61.
    Response option 61 MUST contain value 00010203040111.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client adds to the message client_id with value 00010203040111.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response MUST include option 61.
    Response option 61 MUST contain value 00010203040111.

    Test Procedure:
    Client sets ciaddr value to 0.0.0.0.
    Client copies server_id option from received message.
    Client sends DECLINE message.

    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:11.
    Client adds to the message client_id with value 00010203040999.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with NAK message.

@v4 @decline
Scenario: v4.decline.fail-different-client-id

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server is started.

    Test Procedure:
    Client adds to the message client_id with value 00010203040111.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.1.
    Response MUST include option 61.
    Response option 61 MUST contain value 00010203040111.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client adds to the message client_id with value 00010203040111.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response MUST include option 61.
    Response option 61 MUST contain value 00010203040111.

    Test Procedure:
    Client adds to the message client_id with value 00010203040666.
    Client sets ciaddr value to 0.0.0.0.
    Client copies server_id option from received message.
    Client sends DECLINE message.

    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:11.
    Client adds to the message client_id with value 00010203040999.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with NAK message.


@v4 @decline
Scenario: v4.decline.fail-different-chaddr

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server is started.

    Test Procedure:
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.1.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.

    Test Procedure:
    Client copies server_id option from received message.
    Client sets chaddr value to 00:00:00:00:00:11.
    Client sets ciaddr value to 0.0.0.0.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client sends DECLINE message.

    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:11.
    Client adds to the message client_id with value 00010203040111.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with NAK message.