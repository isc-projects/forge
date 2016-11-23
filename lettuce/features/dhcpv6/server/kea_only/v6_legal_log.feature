Feature: Kea6 legal logging lib


@v6 @dhcp6 @kea_only @legal_logging
    Scenario: legal_log.1

    Test Setup:
    Server is configured with 3000::/64 subnet with 3000::5-3000::50 pool.
    Server is configured with 3001:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
    Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/libdhcp_legal_log.so.
    DHCP server is started.


	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
	Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client does include client-id.
Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client does include client-id.
Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.



    Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Test Procedure:
	Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client does include client-id.
Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.


	Test Procedure:
    Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
	Client does NOT include IA-NA.
	Client does include IA-PD.
	Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
	Client does NOT include IA-NA.
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client does include client-id.
Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:03.
	Client requests option 7.
	Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:03.
	Client copies server-id option from received message.
	Client requests option 7.
	Client does include client-id.
Client sends REQUEST message.
	RelayAgent forwards message encapsulated in 1 level.

	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
	#Response MUST include REPLY message.


@v6 @dhcp6 @kea_only @legal_logging
    Scenario: legal_log.2

    Test Setup:
    Server is configured with 3000::/64 subnet with 3000::5-3000::50 pool.
    Server is configured with 3001:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
    Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/libdhcp_legal_log.so.
    DHCP server is started.


	Test Procedure:
	Client sets DUID value to 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01.

	Client requests option 7.
	Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:

	Client sets DUID value to 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01.
	Client copies server-id option from received message.
	Client requests option 7.
	Client does include client-id.
Client sends REQUEST message.
    Client sets enterprisenum value to 666.
	Client sets subscriber_id value to 50.
    Client does include remote-id.
    Client does include subscriber-id.
	RelayAgent forwards message encapsulated in 1 level.


	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
	#Response MUST include REPLY message.

