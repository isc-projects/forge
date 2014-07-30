

Feature: DHCPv6 Client Classification - default classes
    Tests for Client Classification for classes: docsis3.0 and eRouter1.0.
    Performed through option vendor class.

@v6 @classification @default_classes
    Scenario: v6.client.classification.onesubnet.docsis3.advertise.success

    Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
    Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_docsis3.0.
    DHCP server is started.

    Test Procedure:
    Client sets vendor_class_data value to docsis3.0.
    Client does include vendor-class.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::1.

@v6 @classification @default_classes
    Scenario: v6.client.classification.onesubnet.docsis3.advertise.fail

    Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
    Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_docsis3.0.
    DHCP server is started.

    Test Procedure:
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 13.
    Response sub-option 13 from option 3 MUST contain statuscode 2.

@v6 @classification @default_classes
    Scenario: v6.client.classification.onesubnet.docsis3.request.success

    Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
    Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_docsis3.0.
    DHCP server is started.

    Test Procedure:
    Client sets vendor_class_data value to docsis3.0.
    Client does include vendor-class.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::1.

    Test Procedure:
    Client sets vendor_class_data value to docsis3.0.
    Client does include vendor-class.
    Client copies IA_NA option from received message.
    Client copies server-id option from received message.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::1.

@v6 @classification @default_classes
    Scenario: v6.client.classification.onesubnet.docsis3.request.fail

    Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
    Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_docsis3.0.
    DHCP server is started.

    Test Procedure:
    Client requests option 7.
    Client sets vendor_class_data value to docsis3.0.
    Client does include vendor-class.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::1.

    Test Procedure:
    Client copies IA_NA option from received message.
    Client copies server-id option from received message.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 13.
    Response sub-option 13 from option 3 MUST contain statuscode 2.

@v6 @classification @default_classes
    Scenario: v6.client.classification.onesubnet.eRouter1.0.advertise.success

    Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
    Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_eRouter1.0.
    DHCP server is started.

    Test Procedure:
    Client sets vendor_class_data value to eRouter1.0.
    Client does include vendor-class.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::1.

@v6 @classification @default_classes
    Scenario: v6.client.classification.onesubnet.eRouter1.0.advertise.fail

    Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
    Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_eRouter1.0.
    DHCP server is started.

    Test Procedure:
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 13.
    Response sub-option 13 from option 3 MUST contain statuscode 2.

@v6 @classification @default_classes
    Scenario: v6.client.classification.onesubnet.eRouter1.0.request.success

    Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
    Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_eRouter1.0.
    DHCP server is started.

    Test Procedure:
    Client sets vendor_class_data value to eRouter1.0.
    Client does include vendor-class.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::1.

    Test Procedure:
    Client sets vendor_class_data value to eRouter1.0.
    Client does include vendor-class.
    Client copies IA_NA option from received message.
    Client copies server-id option from received message.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::1.

@v6 @classification @default_classes
    Scenario: v6.client.classification.onesubnet.eRouter1.0.request.fail

    Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
    Server is configured with client-classification option in subnet 0 with name VENDOR_CLASS_eRouter1.0.
    DHCP server is started.

    Test Procedure:
    Client requests option 7.
    Client sets vendor_class_data value to eRouter1.0.
    Client does include vendor-class.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::1.

    Test Procedure:
    Client copies IA_NA option from received message.
    Client copies server-id option from received message.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 13.
    Response sub-option 13 from option 3 MUST contain statuscode 2.
