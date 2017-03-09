Feature: Kea6 Legal logging hook
Testing hook that is creating additional file with detailed logs about clients

@v6 @dhcp6 @kea_only @legal_logging
Scenario: v6.loggers.legal-log-hook-address-assigned-duid

Test Procedure:
Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)var/kea/kea-legal*.txt.

Test Setup:
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
Time preferred-lifetime is configured with value 400.
Time valid-lifetime is configured with value 600.
Server is configured with 3000::/64 subnet with 3000::5-3000::50 pool.
Server is configured with 3001:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/libdhcp_legal_log.so.
Send server configuration using SSH and config-file.
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

Client download file from server stored in: $(SOFTWARE_INSTALL_DIR)var/kea/kea-legal*.txt.
File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-legal*.txt MUST contain line or phrase: Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)

@v6 @dhcp6 @kea_only @legal_logging
Scenario: v6.loggers.legal-log-hook-address-renewed-duid

Test Procedure:
Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)var/kea/kea-legal*.txt.

Test Setup:
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
Time preferred-lifetime is configured with value 400.
Time valid-lifetime is configured with value 600.
Server is configured with 3000::/64 subnet with 3000::5-3000::50 pool.
Server is configured with 3001:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/libdhcp_legal_log.so.
Send server configuration using SSH and config-file.
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

Client download file from server stored in: $(SOFTWARE_INSTALL_DIR)var/kea/kea-legal*.txt.
File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-legal*.txt MUST contain line or phrase: Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)
File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-legal*.txt MUST contain line or phrase: Address:3000::5 has been renewed for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)

@v6 @dhcp6 @kea_only @legal_logging
Scenario: v6.loggers.legal-log-hook-address-rebind-duid

Test Procedure:
Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)var/kea/kea-legal*.txt.

Test Setup:
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
Time preferred-lifetime is configured with value 400.
Time valid-lifetime is configured with value 600.
Server is configured with 3000::/64 subnet with 3000::5-3000::50 pool.
Server is configured with 3001:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/libdhcp_legal_log.so.
Send server configuration using SSH and config-file.
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
Client copies IA_NA option from received message.
Client does include client-id.
Client sends REBIND message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Client download file from server stored in: $(SOFTWARE_INSTALL_DIR)var/kea/kea-legal*.txt.
File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-legal*.txt MUST contain line or phrase: Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)
# Spec sais that when we are rebinding address it will be logged 'renewed', misleadding :/
File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-legal*.txt MUST contain line or phrase: Address:3000::5 has been renewed for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)

@v6 @dhcp6 @kea_only @legal_logging
Scenario: v6.loggers.legal-log-hook-address-assigned-docsis-modem

Test Procedure:
Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)var/kea/kea-legal*.txt.

Test Setup:
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
Time preferred-lifetime is configured with value 400.
Time valid-lifetime is configured with value 600.
Server is configured with 3000::/64 subnet with 3000::5-3000::50 pool.
Server is configured with 3001:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/libdhcp_legal_log.so.
Run configuration command: "mac-sources": [ "docsis-modem" ]
Send server configuration using SSH and config-file.
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
Client sets enterprisenum value to 4491.
Client does include vendor-class.
Client adds suboption for vendor specific information with code: 36 and data: f6:f5:f4:f3:f2:01.
Client does include vendor-specific-info.
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client does include client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Client download file from server stored in: $(SOFTWARE_INSTALL_DIR)var/kea/kea-legal*.txt.
File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-legal*.txt MUST contain line or phrase: Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:01 (from DOCSIS MODEM)

@v6 @dhcp6 @kea_only @legal_logging
Scenario: v6.loggers.legal-log-hook-address-assigned-docsis-cmts

Test Procedure:
Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)var/kea/kea-legal*.txt.

Test Setup:
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
Time preferred-lifetime is configured with value 400.
Time valid-lifetime is configured with value 600.
Server is configured with 3000::/64 subnet with 3000::5-3000::50 pool.
Server is configured with 3001:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/libdhcp_legal_log.so.
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
Client download file from server stored in: $(SOFTWARE_INSTALL_DIR)var/kea/kea-legal*.txt.
File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-legal*.txt MUST contain line or phrase: Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:01 and hardware address: hwtype=1 00:f5:f4:00:f2:01 (from DOCSIS CMTS)

@v6 @dhcp6 @kea_only @legal_logging
Scenario: v6.loggers.legal-log-hook-address-assigned-relay

Test Procedure:
Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)var/kea/kea-legal*.txt.

Test Setup:
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
Time preferred-lifetime is configured with value 400.
Time valid-lifetime is configured with value 600.
Server is configured with 3000::/64 subnet with 3000::5-3000::50 pool.
Server is configured with 3001:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/libdhcp_legal_log.so.
Send server configuration using SSH and config-file.
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
Client copies IA_NA option from received message.
Client sets DUID value to 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01.
Client copies server-id option from received message.
Client requests option 7.
Client does include client-id.
Client sends REQUEST message.

Client sets enterprisenum value to 666.
Client sets subscriber_id value to 50.
Client does include remote-id.
Client does include subscriber-id.
RelayAgent sets linkaddr value to 3000::1005.
RelayAgent sets ifaceid value to abc.
RelayAgent does include interface-id.
RelayAgent forwards message encapsulated in 5 level.

Pass Criteria:
Server MUST respond with RELAYREPLY message.
Response MUST include option 18.
Response MUST include option 9.
Client download file from server stored in: $(SOFTWARE_INSTALL_DIR)var/kea/kea-legal*.txt.
File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-legal*.txt MUST contain line or phrase: Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01 and hardware address: hwtype=1 f6:f5:f4:f3:f2:01 (from DUID) connected via relay
File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-legal*.txt MUST contain line or phrase: connected via relay at address:
File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-legal*.txt MUST contain line or phrase: for client on link address: 3000::1005, hop count: 5
