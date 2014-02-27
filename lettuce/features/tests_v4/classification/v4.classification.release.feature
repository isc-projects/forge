

Feature: DHCPv4 Client Classification release process
    Tests for Client Classification performed through option vendor class identification.
    
@v4 @classification @release
    Scenario: v4.client.classification.release.same-chaddr-client-id

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_my-own-class.
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
    Client sets chaddr value to 00:00:00:00:00:00.
    Client does include client_id with value 00010203040506.
    Client copies server_id option from received message.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.
    
    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets chaddr value to 00:1F:D0:11:22:33.
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

@v4 @classification @release
    Scenario: v4.client.classification.release.different-chaddr-client-id

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_my-own-class.
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
    Client sets chaddr value to 00:00:00:11:22:33.
    Client does include client_id with value 00010203123456.
    Client copies server_id option from received message.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.
    
    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets chaddr value to 00:1F:D0:11:22:33.
    #Client does include client_id with value 00010203040506.
    Client does include vendor_class_id with value my-own-class.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with NAK message.
    Response option 54 MUST contain value $(SRV4_ADDR).
    #Response option 61 MUST contain value 00010203040506.
    Response MUST contain yiaddr 0.0.0.0.
    Response MUST contain ciaddr 0.0.0.0.
    Response MUST contain siaddr 0.0.0.0.
    Response MUST contain giaddr 0.0.0.0.