

Feature: DHCPv4 Client Classification - default classes
    Tests for Client Classification for classes: docsis3.0 and eRouter1.0. 
    Performed through option vendor class identification.

@v4 @classification @default_classes
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
	Response MUST include option 1.
	Response MUST include option 54.
	Response MUST include option 61.
	Response option 1 MUST contain value 255.255.255.0.
	Response option 54 MUST contain value $(SRV4_ADDR).
	Response option 61 MUST contain value 00010203040506.

@v4 @classification @default_classes
	Scenario: v4.client.classification.one.class.docsis3-next-server
	
	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_docsis3.0.
	Server is configured with another subnet: 192.168.50.0/24 with 192.168.50.100-192.168.50.100 pool.
	Server is configured with boot-file-name option in subnet 0 with value somefilename.
	Next server value on subnet 0 is configured with address 192.0.2.234.
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
	Response MUST include option 1.
	Response MUST include option 54.
	Response MUST include option 61.
	Response option 1 MUST contain value 255.255.255.0.
	Response option 54 MUST contain value $(SRV4_ADDR).
	Response option 61 MUST contain value 00010203040506.

@v4 @classification @default_classes
	Scenario: v4.client.classification.one.class.eRouter1-global-next-server
	
	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_eRouter1.0.
	Server is configured with another subnet: 192.168.50.0/24 with 192.168.50.100-192.168.50.100 pool.
	Server is configured with boot-file-name option in subnet 0 with value somefilename.
	Next server global value is configured with address 192.0.2.2.
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

	Response MUST include option 1.
	Response MUST include option 54.
	Response MUST include option 61.
	Response option 1 MUST contain value 255.255.255.0.
	Response option 54 MUST contain value $(SRV4_ADDR).
	Response option 61 MUST contain value 00010203040506.

@v4 @classification @default_classes
	Scenario: v4.client.classification.one.class.eRouter1-subnet-next-server
	
	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_eRouter1.0.
	Server is configured with another subnet: 192.168.50.0/24 with 192.168.50.100-192.168.50.100 pool.
	Server is configured with boot-file-name option in subnet 0 with value somefilename.
	Next server value on subnet 0 is configured with address 192.0.2.234.
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

	Response MUST include option 1.
	Response MUST include option 54.
	Response MUST include option 61.
	Response option 1 MUST contain value 255.255.255.0.
	Response option 54 MUST contain value $(SRV4_ADDR).
	Response option 61 MUST contain value 00010203040506.

@v4 @classification @default_classes
	Scenario: v4.client.classification.one.class.eRouter1-two-next-servers
	
	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_eRouter1.0.
	Server is configured with another subnet: 192.168.50.0/24 with 192.168.50.100-192.168.50.100 pool.
	Server is configured with boot-file-name option in subnet 0 with value somefilename.
	Next server global value is configured with address 192.0.2.2.
	Next server value on subnet 0 is configured with address 192.0.2.234.
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
	Response MUST include option 1.
	Response MUST include option 54.
	Response MUST include option 61.
	Response option 1 MUST contain value 255.255.255.0.
	Response option 54 MUST contain value $(SRV4_ADDR).
	Response option 61 MUST contain value 00010203040506.

@v4 @classification @default_classes
	Scenario: v4.client.classification.multiple.classes.three-subnets-docsis-erouter
	
	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_eRouter1.0.
	Next server value on subnet 0 is configured with address 192.0.50.1.
	Server is configured with boot-file-name option in subnet 0 with value filename.
	
	Server is configured with another subnet: 192.168.50.0/24 with 192.168.50.50-192.168.50.50 pool.
	Server is configured with client-classification option in subnet 1 with name VENDOR_CLASS_docsis3.0.
	Next server value on subnet 1 is configured with address 192.0.50.50.
	Server is configured with boot-file-name option in subnet 1 with value somefilename.
	
	Server is configured with another subnet: 192.168.50.0/24 with 192.168.50.100-192.168.50.100 pool.
	Next server global value is configured with address 192.0.50.100.
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

	Response MUST include option 1.
	Response MUST include option 54.
	Response MUST include option 61.
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
	Response MUST NOT contain siaddr 192.0.50.1.
	Response MUST NOT contain siaddr 192.0.50.50.
	Response MUST NOT contain siaddr 0.0.0.0.
	Response MUST NOT contain file filename.
	Response MUST NOT contain file somefilename.
	
	Response MUST contain yiaddr 192.168.50.100.
	Response MUST contain siaddr 192.0.50.100.

	Response MUST include option 1.
	Response MUST include option 54.
	Response MUST include option 61.
	Response option 1 MUST contain value 255.255.255.0.
	Response option 54 MUST contain value $(SRV4_ADDR).
	Response option 61 MUST contain value 00010203040506.	