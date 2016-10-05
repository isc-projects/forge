Feature: Client Classification DHCPv6
    it's not automated yet
    
@v6 @dhcp6
    Scenario: v6.classification-manual

	Test Procedure:
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

    Test Procedure:
	Client requests option 23.
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 23.
	Response option 23 MUST contain value 2001:db8::111.

	Test Procedure:
	Client requests option 23.
    Client sets DUID value to 00:03:00:01:66:55:44:33:22:22.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 23.
	Response option 23 MUST contain value 2001:db8::222.

	Test Procedure:
	Client requests option 23.
	Client requests option 24.
    Client sets DUID value to 00:03:00:01:77:66:44:33:22:22.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 24.
	Response MUST include option 23.
	Response option 23 MUST contain value 2001:db8::222.

    #Client_s
	Test Procedure:
	Client requests option 32.
    Client sets DUID value to 00:03:00:01:77:66:44:33:22:22.
    Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 32.
    Response option 32 MUST contain value 111.

    #client_r
    Test Procedure:
    Client saves IA_NA option from received message.
	Client requests option 21.
    Client sets DUID value to 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01.
    Client sends SOLICIT message.

    Client does include time.
	...using relay-agent encapsulated in 1 level.

	Pass Criteria:
	Server MUST respond with RELAYREPLY message.

    #client_p
    Test Procedure:
	Client requests option 21.
    Client sets DUID value to 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01.
    Client sends SOLICIT message.

    Client sets peeraddr value to 2000::11.
	...using relay-agent encapsulated in 1 level.

	Pass Criteria:
	Server MUST respond with RELAYREPLY message.

    #client_o
    Test Procedure:
	Client requests option 21.
    Client sets DUID value to 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01.
    Client sends SOLICIT message.

    Client sets linkaddr value to 3000::300.
	...using relay-agent encapsulated in 2 level.

	Pass Criteria:
	Server MUST respond with RELAYREPLY message.


@v6 @dhcp6
    Scenario: v6.classification-manual-vendor
	Test Procedure:
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
    Client sets enterprisenum value to 4491.
    #Client does include vendor-class.
    #Client adds suboption for vendor specific information with code: 1 and data: 32.
    #Client adds suboption for vendor specific information with code: 3 and data: 33.
    Client does include vendor-specific-info.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
    Client sets enterprisenum value to 4455.
    Client does include vendor-specific-info.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
    Client sets enterprisenum value to 5555.
    Client does include vendor-specific-info.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

    #class_j
	Test Procedure:
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
    Client sets enterprisenum value to 4491.
    Client does include vendor-class.
    Client adds suboption for vendor specific information with code: 1 and data: 32.
    Client adds suboption for vendor specific information with code: 3 and data: 33.
    Client does include vendor-specific-info.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
    Client sets enterprisenum value to 4455.
    Client does include vendor-class.
    Client adds suboption for vendor specific information with code: 1 and data: 32.
    Client adds suboption for vendor specific information with code: 2 and data: 33.
    Client does include vendor-specific-info.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
	Client sets enterprisenum value to 6666.
    Client sets vendor_class_data value to docsis3.0.
    Client does include vendor-class.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.


	Test Procedure:
	Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
	Client sets enterprisenum value to 1111.
    Client does include vendor-class.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
    Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
	Client sets enterprisenum value to 1.
    Client sets vendor_class_data value to docsis3.0.
    Client does include vendor-class.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.