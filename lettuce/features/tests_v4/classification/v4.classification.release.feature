

Feature: DHCPv4 Client Classification release process
    Tests for Client Classification performed through option vendor class identification.
    
@v4 @classification
    Scenario: v4.client.classification.release.one.class.one-subnet

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_my-own-class.
	Server is configured with another subnet: 192.168.50.0/24 with 192.168.50.100-192.168.50.100 pool.
    Server is started.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:00.
    Client does include client_id with value 00010203040506.
    Client does include vendor_class_id with value my-own-class.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.
    Response option 54 MUST contain value $(SRV4_ADDR).
    Response option 61 MUST contain value 00010203040506.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:00.
    Client does include client_id with value 00010203040506.
    Client copies server_id option from received message.
	Client does include requested_addr with value 192.168.50.1.
	Client does include vendor_class_id with value my-own-class.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.
    Response option 54 MUST contain value $(SRV4_ADDR).
    Response option 61 MUST contain value 00010203040506.
	
    Test Procedure:
    Client copies server_id option from received message.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.
    
    Pass Criteria:
    Server MUST NOT respond.