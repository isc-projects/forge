Feature: Client Classification DHCPv6
  Expressions In Classification

@v6 @dhcp6 @classification
Scenario: v6.client.classification.option-hex
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: option[1].hex == 0x00030001665544332211
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:11:11:11:11:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

@v6 @dhcp6 @classification
Scenario: v6.client.classification.option-exists
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: option[25].exists
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:11:11:11:11:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client does include IA-PD.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

@v6 @dhcp6 @classification
Scenario: v6.client.classification.relay-option-exists
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Add configuration parameter interface-id with value "abc" to subnet 0 configuration.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: relay6[0].option[16].exists
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:11:11:11:11:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to abc.
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
  Relayed Message option 3 MUST contain sub-option 13.
  Relayed Message sub-option 13 from option 3 MUST contain statuscode 2.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to abc.
  RelayAgent does include interface-id.
  RelayAgent does include vendor-class.
  RelayAgent forwards message encapsulated in 1 level.

  Pass Criteria:
  Server MUST respond with RELAYREPLY message.
  Response MUST include option 18.
  Response MUST include option 9.
  Response option 9 MUST contain Relayed Message.
  Relayed Message MUST include option 1.
  Relayed Message MUST include option 2.
  Relayed Message MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

@v6 @dhcp6 @classification
Scenario: v6.client.classification.relay-peer
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Add configuration parameter interface-id with value "abc" to subnet 0 configuration.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: relay6[0].peeraddr == 3000::1005
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:11:11:11:11:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets peeraddr value to 3000::1001.
  RelayAgent sets ifaceid value to abc.
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
  Relayed Message option 3 MUST contain sub-option 13.
  Relayed Message sub-option 13 from option 3 MUST contain statuscode 2.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets peeraddr value to 3000::1005.
  RelayAgent sets ifaceid value to abc.
  RelayAgent does include interface-id.
  RelayAgent does include vendor-class.
  RelayAgent forwards message encapsulated in 1 level.

  Pass Criteria:
  Server MUST respond with RELAYREPLY message.
  Response MUST include option 18.
  Response MUST include option 9.
  Response option 9 MUST contain Relayed Message.
  Relayed Message MUST include option 1.
  Relayed Message MUST include option 2.
  Relayed Message MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

@v6 @dhcp6 @classification
Scenario: v6.client.classification.relay-linkaddr
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Add configuration parameter interface-id with value "abc" to subnet 0 configuration.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: relay6[0].linkaddr == 3000::1005
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:11:11:11:11:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets linkaddr value to 3000::1001.
  RelayAgent sets ifaceid value to abc.
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
  Relayed Message option 3 MUST contain sub-option 13.
  Relayed Message sub-option 13 from option 3 MUST contain statuscode 2.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets linkaddr value to 3000::1005.
  RelayAgent sets ifaceid value to abc.
  RelayAgent does include interface-id.
  RelayAgent does include vendor-class.
  RelayAgent forwards message encapsulated in 1 level.

  Pass Criteria:
  Server MUST respond with RELAYREPLY message.
  Response MUST include option 18.
  Response MUST include option 9.
  Response option 9 MUST contain Relayed Message.
  Relayed Message MUST include option 1.
  Relayed Message MUST include option 2.
  Relayed Message MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

@v6 @dhcp6 @classification @disabled
  # what is real use of this evaluation?
Scenario: v6.client.classification.msgtype
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Add configuration parameter interface-id with value "abc" to subnet 0 configuration.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: pkt6.msgtype == 12
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:11:11:11:11:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets linkaddr value to 3000::1005.
  RelayAgent sets ifaceid value to abc.
  RelayAgent does include interface-id.
  RelayAgent does include vendor-class.
  RelayAgent forwards message encapsulated in 1 level.

  Pass Criteria:
  Server MUST respond with RELAYREPLY message.
  Response MUST include option 18.
  Response MUST include option 9.
  Response option 9 MUST contain Relayed Message.
  Relayed Message MUST include option 1.
  Relayed Message MUST include option 2.
  Relayed Message MUST include option 3.


@v6 @dhcp6 @classification
Scenario: v6.client.classification.transid
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: pkt6.transid == 66
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:11:11:11:11:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sets tr_id value to 1.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sets tr_id value to 66.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

@v6 @dhcp6 @classification
Scenario: v6.client.classification.vendor
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: vendor[*].exists
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:11:11:11:11:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client does include vendor-specific-info.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

@v6 @dhcp6 @classification
Scenario: v6.client.classification.specific-vendor
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: vendor[4444].exists
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:11:11:11:11:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sets enterprisenum value to 5555.
  Client does include vendor-specific-info.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sets enterprisenum value to 4444.
  Client does include vendor-specific-info.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

@v6 @dhcp6 @classification
Scenario: v6.client.classification.specific-vendor-2
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: vendor.enterprise == 4444
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:11:11:11:11:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sets enterprisenum value to 5555.
  Client does include vendor-specific-info.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sets enterprisenum value to 4444.
  Client does include vendor-specific-info.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

@v6 @dhcp6 @classification
Scenario: v6.client.classification.vendor-suboption-exists
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: vendor[4444].option[1].exists
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:11:11:11:11:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sets enterprisenum value to 4444.
  Client does include vendor-specific-info.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sets enterprisenum value to 4444.
  Client adds suboption for vendor specific information with code: 1 and data: 33.
  Client does include vendor-specific-info.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

@v6 @dhcp6 @classification
Scenario: v6.client.classification.vendor-suboption-value
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: vendor[4444].option[1].hex == 0x0021
  # 0021 == 33
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:11:11:11:11:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sets enterprisenum value to 4444.
  Client adds suboption for vendor specific information with code: 1 and data: 44.
  Client does include vendor-specific-info.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sets enterprisenum value to 4444.
  Client adds suboption for vendor specific information with code: 1 and data: 33.
  Client does include vendor-specific-info.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

@v6 @dhcp6 @classification
Scenario: v6.client.classification.vendor-class-exists
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: vendor-class[*].exists
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:11:11:11:11:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sets enterprisenum value to 4444.
  Client does include vendor-class.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

@v6 @dhcp6 @classification
Scenario: v6.client.classification.specific-vendor-class
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: vendor-class[4444].exists
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:11:11:11:11:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sets enterprisenum value to 5555.
  Client does include vendor-class.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sets enterprisenum value to 4444.
  Client does include vendor-class.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

@v6 @dhcp6 @classification
Scenario: v6.client.classification.specific-vendor-class-2
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: vendor-class.enterprise == 4444
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:11:11:11:11:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sets enterprisenum value to 5555.
  Client does include vendor-class.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sets enterprisenum value to 4444.
  Client does include vendor-class.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

@v6 @dhcp6 @classification
Scenario: v6.client.classification.expressions-not-equal
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: not(vendor-class.enterprise == 5555)
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:11:11:11:11:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sets enterprisenum value to 5555.
  Client does include vendor-class.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sets enterprisenum value to 4444.
  Client does include vendor-class.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sets enterprisenum value to 6666.
  Client does include vendor-class.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

@v6 @dhcp6 @classification
Scenario: v6.client.classification.expressions-and
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: (vendor.enterprise == 4444) and (vendor[4444].option[1].hex == 0x0021)
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:11:11:11:11:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sets enterprisenum value to 4444.
  Client does include vendor-specific-info.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:11:11:11:11:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sets enterprisenum value to 4444.
  Client adds suboption for vendor specific information with code: 1 and data: 22.
  Client does include vendor-specific-info.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sets enterprisenum value to 4444.
  Client adds suboption for vendor specific information with code: 1 and data: 33.
  Client does include vendor-specific-info.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

@v6 @dhcp6 @classification
Scenario: v6.client.classification.expressions-or
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: (vendor.enterprise == 4444) or (vendor[*].option[1].hex == 0x0021)
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:11:11:11:11:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sets enterprisenum value to 5555.
  Client does include vendor-specific-info.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:11:11:11:11:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sets enterprisenum value to 5555.
  Client adds suboption for vendor specific information with code: 1 and data: 22.
  Client does include vendor-specific-info.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:11:11:11:11:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sets enterprisenum value to 4444.
  Client adds suboption for vendor specific information with code: 1 and data: 22.
  Client does include vendor-specific-info.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sets enterprisenum value to 5555.
  Client adds suboption for vendor specific information with code: 1 and data: 33.
  Client does include vendor-specific-info.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

@v6 @dhcp6 @classification
Scenario: v6.client.classification.expressions-substring
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: substring(option[1].hex,6,all) == 0x44332211
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:11:11:11:11:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

@v6 @dhcp6 @classification
Scenario: v6.client.classification.expressions-concat
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: concat(substring(option[1].hex,0,3),substring(option[1].hex,8,all)) == 0x0003002211
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:11:11:11:11:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

@v6 @dhcp6 @classification
Scenario: v6.client.classification.expressions-ifelse
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: ifelse(vendor[4444].option[1].exists, vendor[4444].option[1].hex, 'none') == 0x0021
  # 0021 == 33
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:11:11:11:11:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sets enterprisenum value to 4444.
  Client adds suboption for vendor specific information with code: 1 and data: 44.
  Client does include vendor-specific-info.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sets enterprisenum value to 4444.
  Client adds suboption for vendor specific information with code: 1 and data: 33.
  Client does include vendor-specific-info.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.