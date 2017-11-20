Feature: Client Classification DHCPv6
   Complex Client Classification

@v6 @dhcp6 @classification
Scenario: v6.client.classification.multiple-subnets
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Server is configured with another subnet: 2001:db8:b::/64 with 2001:db8:b::1-2001:db8:b::1 pool.
  Server is configured with another subnet: 2001:db8:c::/64 with 2001:db8:c::1-2001:db8:c::1 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: substring(option[1].hex,8,2) == 0xf2f1
  #To class no 1 add option dns-servers with value 2001:db8::666.
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.

  Add class called Client_Class_2.
  To class no 2 add parameter named: test with value: substring(option[1].hex,8,2) == 0xf2f2
  Server is configured with client-classification option in subnet 1 with name Client_Class_2.

  Add class called Client_Class_3.
  To class no 3 add parameter named: test with value: substring(option[1].hex,8,2) == 0xf299
  Server is configured with client-classification option in subnet 2 with name Client_Class_3.

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
  Client sets DUID value to 00:03:00:01:66:55:44:33:f2:f1.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:f2:f2.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:b::1.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:f2:99.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:c::1.

@v6 @dhcp6 @classification
Scenario: v6.client.classification.multiple-subnets-2
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Server is configured with another subnet: 2001:db8:b::/64 with 2001:db8:b::1-2001:db8:b::1 pool.
  Server is configured with another subnet: 2001:db8:c::/64 with 2001:db8:c::1-2001:db8:c::1 pool.
  Server is configured with another subnet: 2001:db8:d::/64 with 2001:db8:d::1-2001:db8:d::1 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: substring(option[1].hex,8,2) == 0xf2f1
  #To class no 1 add option dns-servers with value 2001:db8::666.
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.

  Add class called Client_Class_2.
  To class no 2 add parameter named: test with value: substring(option[1].hex,8,2) == 0xf2f2
  Server is configured with client-classification option in subnet 1 with name Client_Class_2.

  Add class called Client_Class_3.
  To class no 3 add parameter named: test with value: substring(option[1].hex,8,2) == 0xf299
  Server is configured with client-classification option in subnet 2 with name Client_Class_3.

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
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:d::1.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:f2:f1.
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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:f2:f2.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:b::1.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:f2:99.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:c::1.

  @v6 @dhcp6 @classification
Scenario: v6.client.classification.class-with-option
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: substring(option[1].hex,8,2) == 0xf2f1
  To class no 1 add option dns-servers with value 2001:db8::666.
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.

  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:f2:f1.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 23.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 23.
  Response option 23 MUST contain addresses 2001:db8::666.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:f2:f1.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST NOT include option 23.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

@v6 @dhcp6 @classification
Scenario: v6.client.classification.multiple-subnets-options
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Server is configured with another subnet: 2001:db8:b::/64 with 2001:db8:b::1-2001:db8:b::1 pool.
  Server is configured with another subnet: 2001:db8:c::/64 with 2001:db8:c::1-2001:db8:c::1 pool.
  Server is configured with another subnet: 2001:db8:d::/64 with 2001:db8:d::1-2001:db8:d::1 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: substring(option[1].hex,8,2) == 0xf2f1
  To class no 1 add option dns-servers with value 2001:db8::888.
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.

  Add class called Client_Class_2.
  To class no 2 add parameter named: test with value: substring(option[1].hex,8,2) == 0xf2f2
  To class no 2 add option dns-servers with value 2001:db8::777.
  Server is configured with client-classification option in subnet 1 with name Client_Class_2.

  Add class called Client_Class_3.
  To class no 3 add parameter named: test with value: substring(option[1].hex,8,2) == 0xf299
  To class no 3 add option dns-servers with value 2001:db8::999.
  Server is configured with client-classification option in subnet 2 with name Client_Class_3.

  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:11:11:11:11:11.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 23.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST NOT include option 23.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:d::1.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:f2:f1.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 23.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 23.
  Response option 23 MUST contain addresses 2001:db8::888.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:f2:f2.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 23.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 23.
  Response option 23 MUST contain addresses 2001:db8::777.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:b::1.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:f2:99.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 23.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 23.
  Response option 23 MUST contain addresses 2001:db8::999.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:c::1.

@v6 @dhcp6 @classification
Scenario: v6.client.classification.multiple-subnets-options-override-global
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Server is configured with another subnet: 2001:db8:b::/64 with 2001:db8:b::1-2001:db8:b::1 pool.
  Server is configured with another subnet: 2001:db8:c::/64 with 2001:db8:c::1-2001:db8:c::1 pool.
  Server is configured with another subnet: 2001:db8:d::/64 with 2001:db8:d::1-2001:db8:d::1 pool.

  Server is configured with dns-servers option with value 2001:db8::1,2001:db8::2.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: substring(option[1].hex,8,2) == 0xf2f1
  To class no 1 add option dns-servers with value 2001:db8::888.
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.

  Add class called Client_Class_2.
  To class no 2 add parameter named: test with value: substring(option[1].hex,8,2) == 0xf2f2
  To class no 2 add option dns-servers with value 2001:db8::777.
  Server is configured with client-classification option in subnet 1 with name Client_Class_2.

  Add class called Client_Class_3.
  To class no 3 add parameter named: test with value: substring(option[1].hex,8,2) == 0xf299
  To class no 3 add option dns-servers with value 2001:db8::999.
  Server is configured with client-classification option in subnet 2 with name Client_Class_3.

  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:11:11:11:11:11:11.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 23.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 23.
  Response option 23 MUST contain addresses 2001:db8::1,2001:db8::2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:d::1.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:f2:f1.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 23.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 23.
  Response option 23 MUST contain addresses 2001:db8::888.
  Response option 23 MUST NOT contain addresses 2001:db8::2.
  Response option 23 MUST NOT contain addresses 2001:db8::1.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:f2:f2.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 23.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 23.
  Response option 23 MUST contain addresses 2001:db8::777.
  Response option 23 MUST NOT contain addresses 2001:db8::2.
  Response option 23 MUST NOT contain addresses 2001:db8::1.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:b::1.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:f2:99.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 23.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 23.
  Response option 23 MUST contain addresses 2001:db8::999.
  Response option 23 MUST NOT contain addresses 2001:db8::2.
  Response option 23 MUST NOT contain addresses 2001:db8::1.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:c::1.

@v6 @dhcp6 @classification @sharedsubnets
Scenario: v6.client.classification.shared-subnet-options-override
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::10 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: substring(option[1].hex,8,2) == 0xf2f1
  To class no 1 add option dns-servers with value 2001:db8::888.
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.

  Add subnet 0 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 0 configuration.
  Add configuration parameter option-data with value [{"csv-format":true,"code":23,"data":"2001:db8::1","name":"dns-servers","space":"dhcp6"}] to shared-subnet 0 configuration.

  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:f2:f1.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 23.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 23.
  Response option 23 MUST contain addresses 2001:db8::888.
  Response option 23 MUST NOT contain addresses 2001:db8::1.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

@v6 @dhcp6 @classification @sharedsubnets
Scenario: v6.client.classification.shared-subnet-options-override-global
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::10 pool.
  Server is configured with dns-servers option with value 2001:db8::1,2001:db8::2.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: substring(option[1].hex,8,2) == 0xf2f1
  To class no 1 add option dns-servers with value 2001:db8::888.
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.

  Add subnet 0 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 0 configuration.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:f2:f1.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 23.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 23.
  Response option 23 MUST contain addresses 2001:db8::888.
  Response option 23 MUST NOT contain addresses 2001:db8::1.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.