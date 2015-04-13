Feature: MAC in DHCPv6
    All tests are designed to check Kea ability to extract MAC address from message using various techniques.

@v6 @MACinDHCP6 @kea_only
    Scenario: v6.mac.in.dhcp6.duid-type3
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Run configuration command: "mac-sources": [ "duid" ]
	DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client requests option 7.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: ,f6:f5:f4:f3:f2:01

@v6 @MACinDHCP6 @kea_only
    Scenario: v6.mac.in.dhcp6.duid-type1
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Run configuration command: "mac-sources": [ "duid" ]
	DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:01:00:01:55:2b:fa:0c:08:00:27:58:f1:e8.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client sets DUID value to 00:01:00:01:52:7b:a8:f0:08:00:27:58:f1:e8.
	Client copies server-id option from received message.
	Client requests option 7.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: ,08:00:27:58:f1:e8

@v6 @MACinDHCP6 @kea_only
    Scenario: v6.mac.in.dhcp6.any
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Run configuration command: "mac-sources": [ "any" ]
	DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 7.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: ,f6:f5:f4:f3:f2:01


@v6 @MACinDHCP6 @kea_only
    Scenario: v6.mac.in.dhcp6.ipv6-link-local
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Run configuration command: "mac-sources": [ "ipv6-link-local" ]
	DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 7.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: ,$(CLI_MAC)


@v6 @MACinDHCP6 @kea_only
    Scenario: v6.mac.in.dhcp6.client-link-addr-1
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Run configuration command: "mac-sources": [ "client-link-addr-option" ]
	DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-link-layer-addr.
	Client sends SOLICIT message.


	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends REQUEST message.
	Client does include client-link-layer-addr.
	Client sets peeraddr value to $(CLI_LINK_LOCAL).
	...using relay-agent encapsulated in 1 level.

	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: ,$(CLI_MAC)


@v6 @MACinDHCP6 @kea_only
    Scenario: v6.mac.in.dhcp6.client-link-addr-2
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Run configuration command: "mac-sources": [ "rfc6939" ]
	DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client sends SOLICIT message.


	Pass Criteria:
	Server MUST respond with ADVERTISE message.

    #Sleep for 5 seconds.
	Test Procedure:

	Client copies server-id option from received message.
	Client sends REQUEST message.
	Client does include client-link-layer-addr.
	Client sets peeraddr value to $(CLI_LINK_LOCAL).
	...using relay-agent encapsulated in 1 level.

	Pass Criteria:
	Server MUST respond with RELAYREPLY message. #we need to check logs
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: ,$(CLI_MAC)


@v6 @MACinDHCP6 @kea_only
    Scenario: v6.mac.in.dhcp6.remote-id-1
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Run configuration command: "mac-sources": [ "rfc4649" ]
	DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client sends SOLICIT message.


	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends REQUEST message.
	Client sets remote_id value to 0a0027000001.
    Client does include remote-id.

	Client sets peeraddr value to fe80::800:27ff:fe00:2.
	...using relay-agent encapsulated in 1 level.


	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: ,0a:00:27:00:00:01


@v6 @MACinDHCP6 @kea_only
    Scenario: v6.mac.in.dhcp6.remote-id-2
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Run configuration command: "mac-sources": [ "remote-id" ]
	DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client sends SOLICIT message.


	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends REQUEST message.
    Client sets remote_id value to 0a0027000001.
    Client does include remote-id.
	Client sets peeraddr value to fe80::800:27ff:fe00:2.
	...using relay-agent encapsulated in 1 level.

	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: ,0a:00:27:00:00:01


@v6 @MACinDHCP6 @kea_only
    Scenario: v6.mac.in.dhcp6.subscriber-id-1
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Run configuration command: "mac-sources": [ "subscriber-id" ]
	DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client sends SOLICIT message.


	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends REQUEST message.
	Client sets subscriber_id value to 0a:00:27:00:00:02.
    Client does include subscriber-id.
	Client sets peeraddr value to fe80::800:27ff:fe00:2.
	...using relay-agent encapsulated in 1 level.

	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: ,0a:00:27:00:00:02


@v6 @MACinDHCP6 @kea_only
    Scenario: v6.mac.in.dhcp6.subscriber-id-2
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Run configuration command: "mac-sources": [ "rfc4580" ]
	DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client sends SOLICIT message.


	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends REQUEST message.
	Client sets subscriber_id value to 0a0027000002.
    Client does include subscriber-id.
	Client sets peeraddr value to fe80::800:27ff:fe00:2.
	...using relay-agent encapsulated in 1 level.

	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: ,0a:00:27:00:00:02

@v6 @MACinDHCP6 @kea_only
    Scenario: v6.mac.in.dhcp6.docsis-modem
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Run configuration command: "mac-sources": [ "docsis-modem" ]
	DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.

	Client sets enterprisenum value to 4491.
	Client does include vendor-class.
	Client adds suboption for vendor specific information with code: 36 and data: f6:f5:f4:f3:f2:01.
	Client does include vendor-specific-info.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: ,f6:f5:f4:f3:f2:01


@v6 @MACinDHCP6 @kea_only
    Scenario: v6.mac.in.dhcp6.docsic-cmts
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Run configuration command: "mac-sources": [ "docsis-cmts" ]
	DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client sends SOLICIT message.


	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends REQUEST message.

	Client sets enterprisenum value to 4491.
	Client does include vendor-class.
	Client adds suboption for vendor specific information with code: 1026 and data: 00:f5:f4:00:f2:01.
	Client does include vendor-specific-info.
	...using relay-agent encapsulated in 1 level.

	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: ,00:f5:f4:00:f2:01