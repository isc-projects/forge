

Feature: DHCPv4 Client Classification
    Tests for Client Classification performed through option vendor class identification.
    
@v4 @classification
    Scenario: v4.client.classification.one.class.one-subnet

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Server is configured with client-classification option in subnet 0 with name my-own-class.
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
    
@v4 @classification
    Scenario: v4.client.classification.one.class.two-subnets-same-values

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Server is configured with client-classification option in subnet 0 with name my-own-class.
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
    
    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:00.
    Client does include client_id with value 00010203040506.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.100.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:00.
    Client does include client_id with value 00010203040506.
    Client copies server_id option from received message.
	Client does include requested_addr with value 192.168.50.100.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.100.
    Response option 1 MUST contain value 255.255.255.0.

@v4 @classification
    Scenario: v4.client.classification.one.class.two-subnets-different-chaddr

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Server is configured with client-classification option in subnet 0 with name my-own-class.
	Server is configured with another subnet: 192.168.50.0/24 with 192.168.50.100-192.168.50.100 pool.
    Server is started.

    Test Procedure:
    Client sets chaddr value to 00:1f:05:05:05:05.
    Client does include vendor_class_id with value my-own-class.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client sets chaddr value to 00:1f:05:05:05:05.
    Client copies server_id option from received message.
	Client does include requested_addr with value 192.168.50.1.
	Client does include vendor_class_id with value my-own-class.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.
    
    Test Procedure:
    Client sets chaddr value to 00:1f:06:06:06:06.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.100.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client sets chaddr value to 00:1f:06:06:06:06.
    Client copies server_id option from received message.
	Client does include requested_addr with value 192.168.50.100.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.100.
    Response option 1 MUST contain value 255.255.255.0.    

@v4 @classification
    Scenario: v4.client.classification.multiple.classes.two-subnets-different-chaddr

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Server is configured with client-classification option in subnet 0 with name my-own-class.
	Server is configured with another subnet: 192.168.50.0/24 with 192.168.50.100-192.168.50.100 pool.
	Server is configured with client-classification option in subnet 1 with name my-other-class.
    Server is started.

    Test Procedure:
    Client sets chaddr value to 00:1f:05:05:05:05.
    Client does include vendor_class_id with value my-own-class.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client sets chaddr value to 00:1f:05:05:05:05.
    Client copies server_id option from received message.
	Client does include requested_addr with value 192.168.50.1.
	Client does include vendor_class_id with value my-own-class.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.
    
    Test Procedure:
    Client sets chaddr value to 00:1f:06:06:06:06.
    Client does include vendor_class_id with value my-other-class.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.100.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client sets chaddr value to 00:1f:06:06:06:06.
    Client copies server_id option from received message.
	Client does include requested_addr with value 192.168.50.100.
	Client does include vendor_class_id with value my-other-class.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.100.
    Response option 1 MUST contain value 255.255.255.0.
    
@v4 @classification
    Scenario: v4.client.classification.multiple.classes.three-subnets-different-chaddr

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Server is configured with client-classification option in subnet 0 with name my-own-class.
	Server is configured with another subnet: 192.168.50.0/24 with 192.168.50.100-192.168.50.100 pool.
	Server is configured with client-classification option in subnet 1 with name my-other-class.
    Server is started.

    Test Procedure:
    Client sets chaddr value to 00:1f:05:05:05:05.
    Client does include vendor_class_id with value my-own-class.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client sets chaddr value to 00:1f:05:05:05:05.
    Client copies server_id option from received message.
	Client does include requested_addr with value 192.168.50.1.
	Client does include vendor_class_id with value my-own-class.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.
    
    Test Procedure:
    Client sets chaddr value to 00:1f:06:06:06:06.
    Client does include vendor_class_id with value my-other-class.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.100.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client sets chaddr value to 00:1f:06:06:06:06.
    Client copies server_id option from received message.
	Client does include requested_addr with value 192.168.50.100.
	Client does include vendor_class_id with value my-other-class.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.100.
    Response option 1 MUST contain value 255.255.255.0.
    