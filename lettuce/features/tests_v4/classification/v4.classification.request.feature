

Feature: DHCPv4 Client Classification - request process
    Tests for Client Classification performed through option vendor class identification.
    
@v4 @classification
    Scenario: v4.client.classification.one.class.one-subnet

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
	
@v4 @classification
    Scenario: v4.client.classification.one.class.two-subnets-same-values

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
    Client sets chaddr value to 00:00:00:00:00:00.
    Client does include client_id with value 00010203040506.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.100.
    Response option 1 MUST contain value 255.255.255.0.
    Response option 54 MUST contain value $(SRV4_ADDR).
    Response option 61 MUST contain value 00010203040506.

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
    Response option 54 MUST contain value $(SRV4_ADDR).
    Response option 61 MUST contain value 00010203040506.

@v4 @classification
    Scenario: v4.client.classification.one.class.two-subnets-different-class-id-included

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_my-own-class.
	Server is configured with another subnet: 192.168.50.0/24 with 192.168.50.100-192.168.50.100 pool.
    Server is started.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:00.
    Client does include client_id with value 00010203040506.
    Client does include vendor_class_id with value my-other-class.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.100.
    Response option 1 MUST contain value 255.255.255.0.
    Response option 54 MUST contain value $(SRV4_ADDR).
    Response option 61 MUST contain value 00010203040506.

@v4 @classification
    Scenario: v4.client.classification.one.class.two-subnets-different-chaddr

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_my-own-class.
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
    Response option 54 MUST contain value $(SRV4_ADDR).

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
    Response option 54 MUST contain value $(SRV4_ADDR).
    
    Test Procedure:
    Client sets chaddr value to 00:1f:06:06:06:06.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.100.
    Response option 1 MUST contain value 255.255.255.0.
    Response option 54 MUST contain value $(SRV4_ADDR).

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
    Response option 54 MUST contain value $(SRV4_ADDR).

@v4 @classification
    Scenario: v4.client.classification.one.class.empty-pool-with-classification

	# test if server is assigning addresses from pool without classification after 
	# all addresses form pool with classification has been assigned
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
	Client sets chaddr value to 00:00:11:11:11:11.
	Client does include vendor_class_id with value my-own-class.
	Client requests option 1.
	Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with NAK message.
    Response MUST contain yiaddr 0.0.0.0.
	Response option 54 MUST contain value $(SRV4_ADDR).

@v4 @classification
    Scenario: v4.client.classification.one.class.empty-pool-without-classification

	# test if server is assigning addresses from pool with classification after 
	# all addresses form pool without classification has been assigned
    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_my-own-class.
	Server is configured with another subnet: 192.168.50.0/24 with 192.168.50.100-192.168.50.100 pool.
    Server is started.

	Test Procedure:
	Client sets chaddr value to 00:00:00:00:00:00.
	Client does include client_id with value 00010203040506.
	Client requests option 1.
	Client sends DISCOVER message.
	
	Pass Criteria:
	Server MUST respond with OFFER message.
	Response MUST contain yiaddr 192.168.50.100.
	Response option 1 MUST contain value 255.255.255.0.
	Response option 54 MUST contain value $(SRV4_ADDR).
	Response option 61 MUST contain value 00010203040506.
	
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
	Response option 54 MUST contain value $(SRV4_ADDR).
	Response option 61 MUST contain value 00010203040506.

	Test Procedure:
	Client sets chaddr value to 00:00:11:11:11:11.
	Client requests option 1.
	Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with NAK message.
    Response MUST contain yiaddr 0.0.0.0.
	Response option 54 MUST contain value $(SRV4_ADDR).

@v4 @classification
    Scenario: v4.client.classification.multiple.classes.two-subnets-different-chaddr

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_my-own-class.
	Server is configured with another subnet: 192.168.50.0/24 with 192.168.50.100-192.168.50.100 pool.
	Server is configured with client-classification option in subnet 1 with name VENDOR_CLASS_my-other-class.
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
    Response option 54 MUST contain value $(SRV4_ADDR).

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
    Response option 54 MUST contain value $(SRV4_ADDR).
    
    Test Procedure:
    Client sets chaddr value to 00:1f:06:06:06:06.
    Client does include vendor_class_id with value my-other-class.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.100.
    Response option 1 MUST contain value 255.255.255.0.
    Response option 54 MUST contain value $(SRV4_ADDR).

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
    Response option 54 MUST contain value $(SRV4_ADDR).
    
@v4 @classification
    Scenario: v4.client.classification.multiple.classes.three-subnets-different-chaddr

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_my-own-class.
	Server is configured with another subnet: 192.168.50.0/24 with 192.168.50.100-192.168.50.100 pool.
	Server is configured with client-classification option in subnet 1 with name VENDOR_CLASS_my-other-class.
	Server is configured with another subnet: 192.168.50.0/24 with 192.168.50.150-192.168.50.150 pool.
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
    Response option 54 MUST contain value $(SRV4_ADDR).

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
    Response option 54 MUST contain value $(SRV4_ADDR).
    
    Test Procedure:
    Client sets chaddr value to 00:1f:06:06:06:06.
    Client does include vendor_class_id with value my-other-class.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.100.
    Response option 1 MUST contain value 255.255.255.0.
    Response option 54 MUST contain value $(SRV4_ADDR).

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
    Response option 54 MUST contain value $(SRV4_ADDR).

@v4 @classification
    Scenario: v4.client.classification.multiple.classes.three-subnets-different-values

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_my-own-class.
	Server is configured with another subnet: 192.168.50.0/24 with 192.168.50.100-192.168.50.100 pool.
	Server is configured with client-classification option in subnet 1 with name VENDOR_CLASS_my-other-class.
	Server is configured with another subnet: 192.168.50.0/24 with 192.168.50.150-192.168.50.150 pool.
    Server is started.

    Test Procedure:
    Client sets chaddr value to 00:1f:05:05:05:05.
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
    Client sets chaddr value to 00:1f:05:05:05:05.
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
    Client does include client_id with value 00030405060708.
    Client sets chaddr value to 00:1f:06:06:06:06.
    Client does include vendor_class_id with value my-other-class.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.100.
    Response option 1 MUST contain value 255.255.255.0.
    Response option 54 MUST contain value $(SRV4_ADDR).
    Response option 61 MUST contain value 00030405060708.

    Test Procedure:
    Client does include client_id with value 00030405060708.
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
    Response option 54 MUST contain value $(SRV4_ADDR).

    Test Procedure:
    Client sets chaddr value to 00:1f:11:22:33:44.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.150.
    Response option 1 MUST contain value 255.255.255.0.
    Response option 54 MUST contain value $(SRV4_ADDR).

    Test Procedure:
    Client sets chaddr value to 00:1f:11:22:33:44.
    Client copies server_id option from received message.
	Client does include requested_addr with value 192.168.50.150.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.150.
    Response option 1 MUST contain value 255.255.255.0.
    Response option 54 MUST contain value $(SRV4_ADDR).
    
@v4 @classification
    Scenario: v4.client.classification.one.class.docsis3-boot-file-name

	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_docsis3.0.
	Server is configured with another subnet: 192.168.50.0/24 with 192.168.50.100-192.168.50.100 pool.
	Server is configured with boot-file-name option in subnet 0 with value somefilename.
	Server is configured with boot-file-name option with value someotherfilename.
    Server is started.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:00.
    Client does include client_id with value 00010203040506.
    Client does include vendor_class_id with value docsis3.0.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain file somefilename.
    Response MUST contain yiaddr 192.168.50.1.
    Response MUST NOT contain file someotherfilename.
    Response option 1 MUST contain value 255.255.255.0.
    Response option 54 MUST contain value $(SRV4_ADDR).
    Response option 61 MUST contain value 00010203040506.

@v4 @classification
    Scenario: v4.client.classification.one.class.docsis3-next-server

	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_docsis3.0.
	Server is configured with another subnet: 192.168.50.0/24 with 192.168.50.100-192.168.50.100 pool.
	Server is configured with boot-file-name option in subnet 0 with value somefilename.
	Run configuration command: config set Dhcp4/subnet4[0]/next-server 192.0.2.234
    Server is started.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:00.
    Client does include client_id with value 00010203040506.
    Client does include vendor_class_id with value docsis3.0.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain file somefilename.
    Response MUST contain yiaddr 192.168.50.1.
    Response MUST contain siaddr 192.0.2.234.
    Response option 1 MUST contain value 255.255.255.0.
    Response option 54 MUST contain value $(SRV4_ADDR).
    Response option 61 MUST contain value 00010203040506.

@v4 @classification
    Scenario: v4.client.classification.one.class.eRouter1-global-next-server

	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_eRouter1.0.
	Server is configured with another subnet: 192.168.50.0/24 with 192.168.50.100-192.168.50.100 pool.
	Server is configured with boot-file-name option in subnet 0 with value somefilename.
	Run configuration command: config set Dhcp4/next-server 192.0.2.2
    Server is started.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:00.
    Client does include client_id with value 00010203040506.
    Client does include vendor_class_id with value eRouter1.0.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST NOT contain file somefilename.
    Response MUST contain yiaddr 192.168.50.1.
    Response MUST contain siaddr 0.0.0.0.
    Response MUST NOT contain siaddr 192.0.2.2.
    Response option 1 MUST contain value 255.255.255.0.
    Response option 54 MUST contain value $(SRV4_ADDR).
    Response option 61 MUST contain value 00010203040506.

@v4 @classification
    Scenario: v4.client.classification.one.class.eRouter1-subnet-next-server

	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_eRouter1.0.
	Server is configured with another subnet: 192.168.50.0/24 with 192.168.50.100-192.168.50.100 pool.
	Server is configured with boot-file-name option in subnet 0 with value somefilename.
	Run configuration command: config set Dhcp4/subnet4[0]/next-server 192.0.2.234
    Server is started.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:00.
    Client does include client_id with value 00010203040506.
    Client does include vendor_class_id with value eRouter1.0.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST NOT contain file somefilename.
    Response MUST contain yiaddr 192.168.50.1.
    Response MUST contain siaddr 0.0.0.0.
    Response MUST NOT contain siaddr 192.0.2.234.
    Response option 1 MUST contain value 255.255.255.0.
    Response option 54 MUST contain value $(SRV4_ADDR).
    Response option 61 MUST contain value 00010203040506.

@v4 @classification
    Scenario: v4.client.classification.one.class.eRouter1-two-next-servers

	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_eRouter1.0.
	Server is configured with another subnet: 192.168.50.0/24 with 192.168.50.100-192.168.50.100 pool.
	Server is configured with boot-file-name option in subnet 0 with value somefilename.
	Run configuration command: config set Dhcp4/next-server 192.0.2.2
	Run configuration command: config set Dhcp4/subnet4[0]/next-server 192.0.2.234
    Server is started.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:00.
    Client does include client_id with value 00010203040506.
    Client does include vendor_class_id with value eRouter1.0.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST NOT contain file somefilename.
    Response MUST contain yiaddr 192.168.50.1.
    Response MUST contain siaddr 0.0.0.0.
    Response MUST NOT contain siaddr 192.0.2.234.
    Response MUST NOT contain siaddr 192.0.2.2.
    Response option 1 MUST contain value 255.255.255.0.
    Response option 54 MUST contain value $(SRV4_ADDR).
    Response option 61 MUST contain value 00010203040506.

@v4 @classification
    Scenario: v4.client.classification.multiple.classes.three-subnets-docsis-erouter
    
    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_eRouter1.0.
	Run configuration command: config set Dhcp4/subnet4[0]/next-server 192.0.50.1
	Server is configured with boot-file-name option in subnet 0 with value filename.
	
	Server is configured with another subnet: 192.168.50.0/24 with 192.168.50.50-192.168.50.50 pool.
	Server is configured with client-classification option in subnet 1 with name VENDOR_CLASS_docsis3.0.
	Run configuration command: config set Dhcp4/subnet4[1]/next-server 192.0.50.50
	Server is configured with boot-file-name option in subnet 1 with value somefilename.
	
	Server is configured with another subnet: 192.168.50.0/24 with 192.168.50.100-192.168.50.100 pool.
	Run configuration command: config set Dhcp4/next-server 192.0.50.100
    Server is started.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:00.
    Client does include client_id with value 00010203040506.
    Client does include vendor_class_id with value eRouter1.0.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST NOT contain siaddr 192.0.50.1.
    Response MUST NOT contain siaddr 192.0.50.50.
    Response MUST NOT contain siaddr 192.0.50.100.
    Response MUST NOT contain file somefilename.
    Response MUST NOT contain file filename.
	Response MUST contain yiaddr 192.168.50.1.
    Response MUST contain siaddr 0.0.0.0.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:00.
    Client does include client_id with value 00010203040506.
    Client does include vendor_class_id with value docsis3.0.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.

    Response MUST NOT contain siaddr 192.0.50.1.
    Response MUST NOT contain siaddr 192.0.50.100.
    Response MUST NOT contain siaddr 0.0.0.0.
    Response MUST NOT contain file filename.
    
	Response MUST contain siaddr 192.0.50.50.
    Response MUST contain file somefilename.
	Response MUST contain yiaddr 192.168.50.50.
	
    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:00.
    Client does include client_id with value 00010203040506.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST NOT contain siaddr 192.0.50.1.
    Response MUST NOT contain siaddr 192.0.50.50.
    Response MUST NOT contain siaddr 0.0.0.0.
    Response MUST NOT contain file filename.
    Response MUST NOT contain file somefilename.
	
	Response MUST contain yiaddr 192.168.50.100.
    Response MUST contain siaddr 192.0.50.100.
	