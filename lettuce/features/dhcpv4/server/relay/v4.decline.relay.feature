

Feature: DHCPv4 address decline process
    Those are simple DHCPv4 tests for declining assigned address in relay traffic.
    
@v4 @dhcp4 @relay @decline
Scenario: v4.relay.decline.success

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
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.1.

    Test Procedure:
    Client sets giaddr value to $(GIADDR4).
    Client sets hops value to 1.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.

    Test Procedure:
    Client sets giaddr value to $(GIADDR4).
    Client sets hops value to 1.
    Client copies server_id option from received message.
    Client sets ciaddr value to 0.0.0.0.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client sends DECLINE message.

    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets giaddr value to $(GIADDR4).
    Client sets hops value to 1.
    Client sets chaddr value to 00:00:00:00:00:11.
    Client adds to the message client_id with value 00010203040111.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.1.

@v4 @dhcp4 @relay @decline
Scenario: v4.relay.decline.fail-without-serverid

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
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.1.

    Test Procedure:
    Client sets giaddr value to $(GIADDR4).
    Client sets hops value to 1.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.

    Test Procedure:
    Client sets giaddr value to $(GIADDR4).
    Client sets hops value to 1.
    Client sets ciaddr value to 0.0.0.0.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client sends DECLINE message.

    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets giaddr value to $(GIADDR4).
    Client sets hops value to 1.
    Client sets chaddr value to 00:00:00:00:00:11.
    Client adds to the message client_id with value 00010203040111.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with NAK message.