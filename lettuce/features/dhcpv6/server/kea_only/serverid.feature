Feature: Configure Kea's server-id.


@v6 @dhcp6 @kea_only @server-id @teraz
    Scenario: v6.server-id.llt

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server-id configured with type LLT value 00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8.
	DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
    Response MUST include option 1.
    Response option 1 MUST NOT contain duid 00:01:00:01:52:7b:a8:f0:08:00:27:58:f1:e8.
    Response MUST include option 2.
    Response option 2 MUST contain duid 00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8.

@v6 @dhcp6 @kea_only @server-id  @teraz
    Scenario: v6.server-id.en

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server-id configured with type EN value 00:02:00:00:09:BF:87:AB:EF:7A:5B:B5:45.
	DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
    Response MUST include option 2.
    #Response option 2 MUST contain duid 00:02:00:00:09:BF:87:AB:EF:7A:5B:B5:45.
    Response MUST include option 1.
    #Response option 1 MUST NOT contain duid 00:02:00:00:09:BF:87:AB:EF:7A:5B:B5:45.

@v6 @dhcp6 @kea_only @server-id @teraz
    Scenario: v6.server-id.ll

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server-id configured with type LL value 00:03:00:01:ff:ff:ff:ff:ff:01.
	DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
    Response MUST include option 2.
    Response option 2 MUST contain duid 00:03:00:01:ff:ff:ff:ff:ff:01.
    Response MUST include option 1.
    Response option 1 MUST NOT contain duid 00:03:00:01:ff:ff:ff:ff:ff:01.


