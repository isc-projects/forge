Feature: DHCPv6 Client Classification request process
    Tests request process for Client Classification performed through option vendor class.

@v6 @dhcp6 @classification
    Scenario: v6.client.classification-onesubnet-advertise-success

    Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
    Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_firstclass.
    DHCP server is started.

    Test Procedure:
    Client sets vendor_class_data value to firstclass.
    Client does include vendor-class.
    Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::1.

@v6 @dhcp6 @classification @default_classes
    Scenario: v6.client.classification-onesubnet-advertise-fail

    Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
    Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_firstclass.
    DHCP server is started.

    Test Procedure:
    Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 13.
    Response sub-option 13 from option 3 MUST contain statuscode 2.

@v6 @dhcp6 @classification
    Scenario: v6.client.classification-onesubnet-request-success
    
    Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
    #Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_firstclass.
    DHCP server is started.
    
    Test Procedure:
    #Client sets vendor_class_data value to firstclass.
    #Client does include vendor-class.
    Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::1.
    
    Test Procedure:
    Client sets vendor_class_data value to firstclass.
    Client does include vendor-class.
    Client copies IA_NA option from received message.
    Client copies server-id option from received message.
    Client does include client-id.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::1.


@v6 @dhcp6 @classification
    Scenario: v6.client.classification-twosubnets-request-success
    
    Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
    Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_firstclass.
    Server is configured with another subnet: 3000::/64 with 3000::100-3000::100 pool.
    DHCP server is started.
    
    Test Procedure:
    Client sets vendor_class_data value to firstclass.
    Client does include vendor-class.
    Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::1.
    
    Test Procedure:
    Client sets vendor_class_data value to firstclass.
    Client does include vendor-class.
    Client copies IA_NA option from received message.
    Client copies server-id option from received message.
    Client does include client-id.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::1.
    
    Test Procedure:
    Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::100.
    
    Test Procedure:
    Client copies IA_NA option from received message.
    Client copies server-id option from received message.
    Client does include client-id.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::100.

@v6 @dhcp6 @classification
    Scenario: v6.client.classification-twosubnets-request-fail
    
    Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
    Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_firstclass.
    Server is configured with another subnet: 3000::/64 with 3000::100-3000::100 pool.
    DHCP server is started.
    
    Test Procedure:
    Client sets DUID value to 000300010a0027ffff02.
    Client sets vendor_class_data value to firstclass.
    Client does include vendor-class.
    Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::1.
    
    Test Procedure:
    Client sets DUID value to 000300010a0027ffff02.
    Client sets vendor_class_data value to firstclass.
    Client does include vendor-class.
    Client copies IA_NA option from received message.
    Client copies server-id option from received message.
    Client does include client-id.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::1.
    
    Test Procedure:
    Client sets DUID value to 000300010a0027ffff02.
    Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::100.
    
    Test Procedure:
    Client sets DUID value to 000300010a0027ffff02.
    Client copies IA_NA option from received message.
    Client copies server-id option from received message.
    Client does include client-id.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::100.
    
    Test Procedure:
    Client sets DUID value to 000300010a0027ffff03.
    Client sets vendor_class_data value to firstclass.
    Client does include vendor-class.
    Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 13.
    Response sub-option 13 from option 3 MUST contain statuscode 2.
    
    Test Procedure:
    Client sets DUID value to 000300010a0027ffff03.
    Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 13.
    Response sub-option 13 from option 3 MUST contain statuscode 2.

@v6 @dhcp6 @classification
    Scenario: v6.client.classification-twoclasses-request-success
    
    Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
    Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_firstclass.
    Server is configured with another subnet: 3000::/64 with 3000::100-3000::100 pool.
    Server is configured with client-classification option in subnet 1 with name VENDOR_CLASS_secondclass.
    DHCP server is started.
    
    Test Procedure:
    Client sets DUID value to 000300010a0027ffff03.
    Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 13.
    Response sub-option 13 from option 3 MUST contain statuscode 2.
    
    Test Procedure:
    Client sets vendor_class_data value to firstclass.
    Client does include vendor-class.
    Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::1.
    
    Test Procedure:
    Client sets vendor_class_data value to firstclass.
    Client does include vendor-class.
    Client copies IA_NA option from received message.
    Client copies server-id option from received message.
    Client does include client-id.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::1.
    
    Test Procedure:
    Client sets vendor_class_data value to secondclass.
    Client does include vendor-class.
    Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::100.
    
    Test Procedure:
    Client sets vendor_class_data value to secondclass.
    Client does include vendor-class.
    Client copies IA_NA option from received message.
    Client copies server-id option from received message.
    Client does include client-id.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::100.
