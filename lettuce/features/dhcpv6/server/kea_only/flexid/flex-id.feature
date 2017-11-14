Feature: Kea Hook flex-id testing

@v6 @flexid @kea_only
  Scenario: v6.hooks.flexid-1
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Reserve hostname reserved-hostname in subnet 0 for host uniquely identified by flex-id 'port1234'.
  For host reservation entry no. 0 in subnet 0 add address with value 3000::f.
  Add to config file line: "host-reservation-identifiers": [  "duid",  "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: substring(relay6[0].option[18].hex,0,8)
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to port1234.
  RelayAgent does include interface-id.
  RelayAgent forwards message encapsulated in 1 level.

  Pass Criteria:
  Server MUST respond with RELAYREPLY message.
  Response MUST include option 18.
  Response MUST include option 9.
  Response option 9 MUST contain Relayed Message.
  Relayed Message MUST include option 1.
  Relayed Message MUST include option 2.
  Relayed Message MUST include option 3.
  Relayed Message option 3 MUST contain sub-option 5.
  #Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:1::1.
  Relayed Message sub-option 5 from option 3 MUST contain address 3000::f.

@v6 @flexid @kea_only
  Scenario: v6.hooks.flexid-2
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Reserve hostname reserved-hostname in subnet 0 for host uniquely identified by flex-id 'port1234'.
  For host reservation entry no. 0 in subnet 0 add address with value 3000::f.
  Add to config file line: "host-reservation-identifiers": [  "duid",  "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: relay6[0].option[18].hex
  Send server configuration using SSH and config-file.
  DHCP server is started.

  #Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "config-reload","arguments":  {} }
  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to port1234.
  RelayAgent does include interface-id.
  RelayAgent forwards message encapsulated in 1 level.

  Pass Criteria:
  Server MUST respond with RELAYREPLY message.
  Response MUST include option 18.
  Response MUST include option 9.
  Response option 9 MUST contain Relayed Message.
  Relayed Message MUST include option 1.
  Relayed Message MUST include option 2.
  Relayed Message MUST include option 3.
  Relayed Message option 3 MUST contain sub-option 5.
  #Relayed Message sub-option 5 from option 3 MUST contain address 2001:db8:1::1.
  Relayed Message sub-option 5 from option 3 MUST contain address 3000::f.


@v6 @flexid @kea_only
  Scenario: v6.hooks.flexid-3
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Reserve hostname reserved-hostname in subnet 0 for host uniquely identified by flex-id 01:02:03:04:05:06.
  For host reservation entry no. 0 in subnet 0 add address with value 3000::f.
  Add to config file line: "host-reservation-identifiers": [  "duid",  "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: vendor[4491].option[1026].hex
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets enterprisenum value to 4491.
  Client does include vendor-class.
  Client adds suboption for vendor specific information with code: 1026 and data: 01:02:03:04:05:06.
  Client does include vendor-specific-info.

  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::f.

@v6 @flexid @kea_only
  Scenario: v6.hooks.flexid-mysql-1
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Add to config file line: "host-reservation-identifiers": [  "duid",  "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: relay6[0].option[18].hex

  Use MySQL reservation system.
  Create new MySQL reservation identified by flex-id 706f727431323334.
  Add hostname reserved-hostname to MySQL reservation record id 1.
  Add dhcp6_subnet_id 1 to MySQL reservation record id 1.
  Add IPv6 address reservation 3000::f with iaid $(EMPTY) to MySQL record id 1.
  Upload hosts reservation to MySQL database.

  Send server configuration using SSH and config-file.
  DHCP server is started.
  #Pause the Test.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to port1234.
  RelayAgent does include interface-id.
  RelayAgent forwards message encapsulated in 1 level.

  Pass Criteria:
  Server MUST respond with RELAYREPLY message.
  Response MUST include option 18.
  Response MUST include option 9.
  Response option 9 MUST contain Relayed Message.
  Relayed Message MUST include option 1.
  Relayed Message MUST include option 2.
  Relayed Message MUST include option 3.
  Relayed Message option 3 MUST contain sub-option 5.
  Relayed Message sub-option 5 from option 3 MUST contain address 3000::f.

@v6 @flexid @kea_only
  Scenario: v6.hooks.flexid-mysql-2
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Add to config file line: "host-reservation-identifiers": [  "duid",  "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: vendor[4491].option[1026].hex

  Use MySQL reservation system.
  Create new MySQL reservation identified by flex-id 01:02:03:04:05:06.
  Add hostname reserved-hostname to MySQL reservation record id 1.
  Add dhcp6_subnet_id 1 to MySQL reservation record id 1.
  Add IPv6 address reservation 3000::f with iaid $(EMPTY) to MySQL record id 1.
  Upload hosts reservation to MySQL database.

  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets enterprisenum value to 4491.
  Client does include vendor-class.
  Client adds suboption for vendor specific information with code: 1026 and data: 01:02:03:04:05:06.
  Client does include vendor-specific-info.

  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::f.

@v6 @flexid @kea_only
  Scenario: v6.hooks.flexid-pgsql-1
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Add to config file line: "host-reservation-identifiers": [  "duid",  "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: relay6[0].option[18].hex

  Use PostgreSQL reservation system.
  Create new PostgreSQL reservation identified by flex-id 706f727431323334.
  Add hostname reserved-hostname to PostgreSQL reservation record id 1.
  Add dhcp6_subnet_id 1 to PostgreSQL reservation record id 1.
  Add IPv6 address reservation 3000::f with iaid $(EMPTY) to PostgreSQL record id 1.
  Upload hosts reservation to PostgreSQL database.

  Send server configuration using SSH and config-file.
  DHCP server is started.
  #Pause the Test.

  Test Procedure:
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to port1234.
  RelayAgent does include interface-id.
  RelayAgent forwards message encapsulated in 1 level.

  Pass Criteria:
  Server MUST respond with RELAYREPLY message.
  Response MUST include option 18.
  Response MUST include option 9.
  Response option 9 MUST contain Relayed Message.
  Relayed Message MUST include option 1.
  Relayed Message MUST include option 2.
  Relayed Message MUST include option 3.
  Relayed Message option 3 MUST contain sub-option 5.

  Relayed Message sub-option 5 from option 3 MUST contain address 3000::f.

@v6 @flexid @kea_only
  Scenario: v6.hooks.flexid-pgsql-2
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Add to config file line: "host-reservation-identifiers": [  "duid",  "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: vendor[4491].option[1026].hex

  Use PostgreSQL reservation system.
  Create new PostgreSQL reservation identified by flex-id 01:02:03:04:05:06.
  Add hostname reserved-hostname to PostgreSQL reservation record id 1.
  Add dhcp6_subnet_id 1 to PostgreSQL reservation record id 1.
  Add IPv6 address reservation 3000::f with iaid $(EMPTY) to PostgreSQL record id 1.
  Upload hosts reservation to PostgreSQL database.

  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets enterprisenum value to 4491.
  Client does include vendor-class.
  Client adds suboption for vendor specific information with code: 1026 and data: 01:02:03:04:05:06.
  Client does include vendor-specific-info.

  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::f.

@v6 @flexid @kea_only
  Scenario: v6.hooks.flexid-replace-duid
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Reserve hostname reserved-hostname in subnet 0 for host uniquely identified by flex-id 01:02:03:04:05:06.
  For host reservation entry no. 0 in subnet 0 add address with value 3000::f.
  Add to config file line: "host-reservation-identifiers": [  "duid",  "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: vendor[4491].option[1026].hex
  To hook no. 1 add parameter named replace-client-id with value: true

  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client sets enterprisenum value to 4491.
  Client does include vendor-class.
  Client adds suboption for vendor specific information with code: 1026 and data: 01:02:03:04:05:06.
  Client does include vendor-specific-info.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::f.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sets enterprisenum value to 4491.
  Client does include vendor-class.
  Client adds suboption for vendor specific information with code: 1026 and data: 01:02:03:04:05:06.
  Client does include vendor-specific-info.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::f.

@v6 @flexid @kea_only
  Scenario: v6.hooks.flexid-replace-duid-renew

  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Reserve hostname reserved-hostname in subnet 0 for host uniquely identified by flex-id 01:02:03:04:05:06.
  For host reservation entry no. 0 in subnet 0 add address with value 3000::f.
  Add to config file line: "host-reservation-identifiers": [  "duid",  "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: vendor[4491].option[1026].hex
  To hook no. 1 add parameter named replace-client-id with value: true

  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client sets enterprisenum value to 4491.
  Client does include vendor-class.
  Client adds suboption for vendor specific information with code: 1026 and data: 01:02:03:04:05:06.
  Client does include vendor-specific-info.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::f.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sets enterprisenum value to 4491.
  Client does include vendor-class.
  Client adds suboption for vendor specific information with code: 1026 and data: 01:02:03:04:05:06.
  Client does include vendor-specific-info.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::f.

  # Client with different duid try to renew
  Test Procedure:
  Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sets enterprisenum value to 4491.
  Client does include vendor-class.
  Client adds suboption for vendor specific information with code: 1026 and data: 01:02:03:04:05:06.
  Client does include vendor-specific-info.
  Client sends RENEW message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::f.
  Response sub-option 5 from option 3 MUST NOT contain validlft 0.

@v6 @flexid @kea_only
  Scenario: v6.hooks.flexid-replace-duid-renew-failed
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Reserve hostname reserved-hostname in subnet 0 for host uniquely identified by flex-id 01:02:03:04:05:06.
  For host reservation entry no. 0 in subnet 0 add address with value 3000::f.
  Add to config file line: "host-reservation-identifiers": [  "duid",  "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: vendor[4491].option[1026].hex
  To hook no. 1 add parameter named replace-client-id with value: true
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client sets enterprisenum value to 4491.
  Client does include vendor-class.
  Client adds suboption for vendor specific information with code: 1026 and data: 01:02:03:04:05:06.
  Client does include vendor-specific-info.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::f.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sets enterprisenum value to 4491.
  Client does include vendor-class.
  Client adds suboption for vendor specific information with code: 1026 and data: 01:02:03:04:05:06.
  Client does include vendor-specific-info.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::f.

  # Client with the same DUID and different flex-id try to renew
  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sets enterprisenum value to 4491.
  Client does include vendor-class.
  Client adds suboption for vendor specific information with code: 1026 and data: 01:02:03:44:55:66.
  Client does include vendor-specific-info.
  Client sends RENEW message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::f.
  Response sub-option 5 from option 3 MUST contain validlft 0.

@v6 @flexid @kea_only
  Scenario: v6.hooks.flexid-replace-duid-release
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Reserve hostname reserved-hostname in subnet 0 for host uniquely identified by flex-id 01:02:03:04:05:06.
  For host reservation entry no. 0 in subnet 0 add address with value 3000::f.
  Add to config file line: "host-reservation-identifiers": [  "duid",  "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: vendor[4491].option[1026].hex
  To hook no. 1 add parameter named replace-client-id with value: true

  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client sets enterprisenum value to 4491.
  Client does include vendor-class.
  Client adds suboption for vendor specific information with code: 1026 and data: 01:02:03:04:05:06.
  Client does include vendor-specific-info.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::f.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sets enterprisenum value to 4491.
  Client does include vendor-class.
  Client adds suboption for vendor specific information with code: 1026 and data: 01:02:03:04:05:06.
  Client does include vendor-specific-info.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::f.

  # Client with different duid try to release
  Test Procedure:
  Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sets enterprisenum value to 4491.
  Client does include vendor-class.
  Client adds suboption for vendor specific information with code: 1026 and data: 01:02:03:04:05:06.
  Client does include vendor-specific-info.
  Client sends RELEASE message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 0.

@v6 @flexid @kea_only
  Scenario: v6.hooks.flexid-replace-duid-release-failed
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Reserve hostname reserved-hostname in subnet 0 for host uniquely identified by flex-id 01:02:03:04:05:06.
  For host reservation entry no. 0 in subnet 0 add address with value 3000::f.
  Add to config file line: "host-reservation-identifiers": [  "duid",  "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: vendor[4491].option[1026].hex
  To hook no. 1 add parameter named replace-client-id with value: true
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client sets enterprisenum value to 4491.
  Client does include vendor-class.
  Client adds suboption for vendor specific information with code: 1026 and data: 01:02:03:04:05:06.
  Client does include vendor-specific-info.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::f.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sets enterprisenum value to 4491.
  Client does include vendor-class.
  Client adds suboption for vendor specific information with code: 1026 and data: 01:02:03:04:05:06.
  Client does include vendor-specific-info.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::f.

  # Client with the same duid but different flex-id try to release (result should be nobiding)
  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sets enterprisenum value to 4491.
  Client does include vendor-class.
  Client adds suboption for vendor specific information with code: 1026 and data: 01:02:03:44:55:66.
  Client does include vendor-specific-info.
  Client sends RELEASE message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 3.

  #File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST contain line or phrase: 3000::f,01:02:03:04:05:06,4000,
  #File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea-leases6.csv MUST NOT contain line or phrase: 3000::f,01:02:03:04:05:06,0,
  
@v6 @flexid @kea_only
  Scenario: v6.hooks.flexid-replace-duid-release-mysql

  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Reserve hostname reserved-hostname in subnet 0 for host uniquely identified by flex-id 01:02:03:04:05:06.
  For host reservation entry no. 0 in subnet 0 add address with value 3000::f.
  Add to config file line: "host-reservation-identifiers": [  "duid",  "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: vendor[4491].option[1026].hex
  To hook no. 1 add parameter named replace-client-id with value: true

  Use MySQL reservation system.
  Create new MySQL reservation identified by flex-id 01:02:03:04:05:06.
  Add hostname reserved-hostname to MySQL reservation record id 1.
  Add dhcp6_subnet_id 1 to MySQL reservation record id 1.
  Add IPv6 address reservation 3000::f with iaid $(EMPTY) to MySQL record id 1.
  Upload hosts reservation to MySQL database.

  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client sets enterprisenum value to 4491.
  Client does include vendor-class.
  Client adds suboption for vendor specific information with code: 1026 and data: 11:22:33:44:55:66.
  Client does include vendor-specific-info.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST NOT contain address 3000::f.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client sets enterprisenum value to 4491.
  Client does include vendor-class.
  Client adds suboption for vendor specific information with code: 1026 and data: 01:02:03:04:05:06.
  Client does include vendor-specific-info.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::f.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sets enterprisenum value to 4491.
  Client does include vendor-class.
  Client adds suboption for vendor specific information with code: 1026 and data: 01:02:03:04:05:06.
  Client does include vendor-specific-info.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::f.

  # Client with different duid try to release
  Test Procedure:
  Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sets enterprisenum value to 4491.
  Client does include vendor-class.
  Client adds suboption for vendor specific information with code: 1026 and data: 01:02:03:04:05:06.
  Client does include vendor-specific-info.
  Client sends RELEASE message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 0.

@v6 @flexid @kea_only
  Scenario: v6.hooks.flexid-replace-duid-release-pgsql
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Reserve hostname reserved-hostname in subnet 0 for host uniquely identified by flex-id 01:02:03:04:05:06.
  For host reservation entry no. 0 in subnet 0 add address with value 3000::f.
  Add to config file line: "host-reservation-identifiers": [  "duid",  "flex-id" ]
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_flex_id.so.
  To hook no. 1 add parameter named identifier-expression with value: vendor[4491].option[1026].hex
  To hook no. 1 add parameter named replace-client-id with value: true

  Use PostgreSQL reservation system.
  Create new PostgreSQL reservation identified by flex-id 01:02:03:04:05:06.
  Add hostname reserved-hostname to PostgreSQL reservation record id 1.
  Add dhcp6_subnet_id 1 to PostgreSQL reservation record id 1.
  Add IPv6 address reservation 3000::f with iaid $(EMPTY) to PostgreSQL record id 1.
  Upload hosts reservation to PostgreSQL database.

  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client sets enterprisenum value to 4491.
  Client does include vendor-class.
  Client adds suboption for vendor specific information with code: 1026 and data: 01:02:03:04:05:06.
  Client does include vendor-specific-info.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::f.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sets enterprisenum value to 4491.
  Client does include vendor-class.
  Client adds suboption for vendor specific information with code: 1026 and data: 01:02:03:04:05:06.
  Client does include vendor-specific-info.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::f.

  # Client with different duid try to release
  Test Procedure:
  Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sets enterprisenum value to 4491.
  Client does include vendor-class.
  Client adds suboption for vendor specific information with code: 1026 and data: 01:02:03:04:05:06.
  Client does include vendor-specific-info.
  Client sends RELEASE message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 0.