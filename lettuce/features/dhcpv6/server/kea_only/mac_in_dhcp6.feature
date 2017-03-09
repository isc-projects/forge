Feature: MAC in DHCPv6
    All tests are designed to check Kea ability to extract MAC address from message using various techniques.

@v6 @MACinDHCP6 @kea_only
    Scenario: v6.mac.in.dhcp6.duid-type3
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Run configuration command: "mac-sources": [ "duid" ]
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: ,f6:f5:f4:f3:f2:01,0
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: Hardware addr: f6:f5:f4:f3:f2:01

@v6 @MACinDHCP6 @kea_only
    Scenario: v6.mac.in.dhcp6.duid-type1
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Run configuration command: "mac-sources": [ "duid" ]
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:01:00:01:55:2b:fa:0c:08:00:27:58:f1:e8.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client sets DUID value to 00:01:00:01:52:7b:a8:f0:08:00:27:58:f1:e8.
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client requests option 7.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: ,08:00:27:58:f1:e8
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: Hardware addr: 08:00:27:58:f1:e8

@v6 @MACinDHCP6 @kea_only
    Scenario: v6.mac.in.dhcp6.any
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Run configuration command: "mac-sources": [ "any" ]
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: ,f6:f5:f4:f3:f2:01
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: Hardware addr: f6:f5:f4:f3:f2:01


@v6 @MACinDHCP6 @kea_only
    Scenario: v6.mac.in.dhcp6.ipv6-link-local
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Run configuration command: "mac-sources": [ "ipv6-link-local" ]
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client requests option 7.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: ,$(CLI_MAC)
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: Hardware addr: $(CLI_MAC)


@v6 @MACinDHCP6 @kea_only
    Scenario: v6.mac.in.dhcp6.client-link-addr-1
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Run configuration command: "mac-sources": [ "client-link-addr-option" ]
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-link-layer-addr.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	RelayAgent does include client-link-layer-addr.
	RelayAgent sets peeraddr value to $(CLI_LINK_LOCAL).
	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 1 level.

	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
    Response MUST include option 18.
    Response MUST include option 9.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: ,$(CLI_MAC)
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: Hardware addr: $(CLI_MAC)


@v6 @MACinDHCP6 @kea_only
    Scenario: v6.mac.in.dhcp6.client-link-addr-2
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Run configuration command: "mac-sources": [ "rfc6939" ]
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	RelayAgent does include client-link-layer-addr.
	RelayAgent sets peeraddr value to $(CLI_LINK_LOCAL).
	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 1 level.

	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
    Response MUST include option 18.
    Response MUST include option 9. #we need to check logs
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: ,$(CLI_MAC)
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: Hardware addr: $(CLI_MAC)


@v6 @MACinDHCP6 @kea_only
    Scenario: v6.mac.in.dhcp6.remote-id-1
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Run configuration command: "mac-sources": [ "rfc4649" ]
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Client sets remote_id value to 0a0027000001.
    RelayAgent does include remote-id.
	RelayAgent sets peeraddr value to fe80::800:27ff:fe00:2.
	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 1 level.

	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
    Response MUST include option 18.
    Response MUST include option 9.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: ,0a:00:27:00:00:01
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: Hardware addr: 0a:00:27:00:00:01


@v6 @MACinDHCP6 @kea_only
    Scenario: v6.mac.in.dhcp6.remote-id-2
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Run configuration command: "mac-sources": [ "remote-id" ]
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

    RelayAgent sets remote_id value to 0a0027000001.
    RelayAgent does include remote-id.
	RelayAgent sets peeraddr value to fe80::800:27ff:fe00:2.
	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 1 level.

	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
    Response MUST include option 18.
    Response MUST include option 9.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: ,0a:00:27:00:00:01
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: Hardware addr: 0a:00:27:00:00:01


@v6 @MACinDHCP6 @kea_only
    Scenario: v6.mac.in.dhcp6.subscriber-id-1
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Run configuration command: "mac-sources": [ "subscriber-id" ]
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	RelayAgent sets subscriber_id value to f6:f5:f4:f3:f2:01.
    RelayAgent does include subscriber-id.
	RelayAgent sets peeraddr value to fe80::800:27ff:fe00:2.
	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 1 level.

	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
    Response MUST include option 18.
    Response MUST include option 9.
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: ,0a:00:27:00:00:02
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: Hardware addr: 0a:00:27:00:00:02


@v6 @MACinDHCP6 @kea_only
    Scenario: v6.mac.in.dhcp6.subscriber-id-2
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Run configuration command: "mac-sources": [ "rfc4580" ]
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	RelayAgent sets subscriber_id value to 0a0027000002.
    RelayAgent does include subscriber-id.
	RelayAgent sets peeraddr value to fe80::800:27ff:fe00:2.
	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 1 level.

	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
    Response MUST include option 18.
    Response MUST include option 9.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: ,0a:00:27:00:00:02
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: Hardware addr: 0a:00:27:00:00:02


@v6 @MACinDHCP6 @kea_only
    Scenario: v6.mac.in.dhcp6.docsis-modem
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Run configuration command: "mac-sources": [ "docsis-modem" ]
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sets enterprisenum value to 4491.
	Client does include vendor-class.
	Client adds suboption for vendor specific information with code: 36 and data: f6:f5:f4:f3:f2:01.
	Client does include vendor-specific-info.
    Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: ,f6:f5:f4:f3:f2:01
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: Hardware addr: f6:f5:f4:f3:f2:01


@v6 @MACinDHCP6 @kea_only
    Scenario: v6.mac.in.dhcp6.docsic-cmts
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Run configuration command: "mac-sources": [ "docsis-cmts" ]
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	RelayAgent sets enterprisenum value to 4491.
	RelayAgent does include vendor-class.
	RelayAgent adds suboption for vendor specific information with code: 1026 and data: 00:f5:f4:00:f2:01.
	RelayAgent does include vendor-specific-info.
	RelayAgent does include interface-id.
    RelayAgent forwards message encapsulated in 1 level.

	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
    Response MUST include option 18.
    Response MUST include option 9.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: ,00:f5:f4:00:f2:01
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: Hardware addr: 00:f5:f4:00:f2:01