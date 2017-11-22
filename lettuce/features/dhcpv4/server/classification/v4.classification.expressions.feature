Feature: Client Classification DHCPv4
  Expressions In Classification

@v4 @dhcp4 @classification
Scenario: v4.client.classification.option-hex
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: option[61].hex == 0xff010203ff041122
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message client_id with value ff:01:11:11:11:11:11:22.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST NOT respond.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.

  Test Procedure:
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.50.
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.50.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

@v4 @dhcp4 @classification
Scenario: v4.client.classification.option-exists
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: option[61].exists
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST NOT respond.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.

  Test Procedure:
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.50.
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.50.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

@v4 @dhcp4 @classification @disabled
Scenario: v4.client.classification.relay-option-exists
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: relay4[*].exists
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  #TODO needs support for option 82
  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST NOT respond.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.

  Test Procedure:
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.50.
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.50.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.


@v4 @dhcp4 @classification
Scenario: v4.client.classification.transid
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: pkt4.transid == 66
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets tr_id value to 1111.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST NOT respond.

  Test Procedure:
  Client sets tr_id value to 66.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.

  Test Procedure:
  Client sets tr_id value to 66.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.50.
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.50.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  
@v4 @dhcp4 @classification
Scenario: v4.client.classification.siaddr
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: pkt4.siaddr == 1.1.1.1
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets siaddr value to 192.0.0.14.
  Client sets chaddr value to ff:00:01:02:03:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST NOT respond.

  Test Procedure:
  Client sets siaddr value to 1.1.1.1.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.

@v4 @dhcp4 @classification
Scenario: v4.client.classification.yiaddr
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: pkt4.yiaddr == 1.1.1.1
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets yiaddr value to 192.0.0.14.
  Client sets chaddr value to ff:00:01:02:03:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST NOT respond.

  Test Procedure:
  Client sets yiaddr value to 1.1.1.1.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.


@v4 @dhcp4 @classification @disabled
Scenario: v4.client.classification.giaddr
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: pkt4.giaddr == $(GIADDR4)
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets giaddr value to 192.0.0.14.
  Client sets chaddr value to ff:00:01:02:03:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST NOT respond.

  Test Procedure:
  Client sets giaddr value to $(GIADDR4).
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.

  Test Procedure:
  Client sets giaddr value to $(GIADDR4).
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.50.
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.50.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

@v4 @dhcp4 @classification
Scenario: v4.client.classification.ciaddr
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: pkt4.ciaddr == 192.0.0.1
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets ciaddr value to 192.0.0.14.
  Client sets chaddr value to ff:00:01:02:03:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST NOT respond.

  Test Procedure:
  Client sets ciaddr value to 192.0.0.1.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.

  Test Procedure:
  Client sets ciaddr value to 192.0.0.1.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.50.
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.50.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

@v4 @dhcp4 @classification
Scenario: v4.client.classification.htype
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: pkt4.htype == 6
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets htype value to 4.
  Client sets chaddr value to ff:00:01:02:03:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST NOT respond.

  Test Procedure:
  Client sets htype value to 6.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.

  Test Procedure:
  Client sets htype value to 6.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.50.
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.50.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

@v4 @dhcp4 @classification
Scenario: v4.client.classification.mac
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: pkt4.mac == 0xff010203ff04
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:00:01:02:03:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST NOT respond.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.

  Test Procedure:
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.50.
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.50.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  

@v4 @dhcp4 @classification @disabled
Scenario: v4.client.classification.vendor
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool. # TODO needs option support

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: vendor[*].exists
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

@v4 @dhcp4 @classification @disabled
Scenario: v4.client.classification.specific-vendor
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool. # TODO needs option support

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: vendor[4444].exists
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

@v4 @dhcp4 @classification @disabled
Scenario: v4.client.classification.specific-vendor-2
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool. # TODO needs option support

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: vendor.enterprise == 4444
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

@v4 @dhcp4 @classification @disabled
Scenario: v4.client.classification.vendor-suboption-exists
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool. # TODO needs option support

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: vendor[4444].option[1].exists
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

@v4 @dhcp4 @classification @disabled
Scenario: v4.client.classification.vendor-suboption-value
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool. # TODO needs option support

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: vendor[4444].option[1].hex == 0x0021
  # 0021 == 33
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

@v4 @dhcp4 @classification @disabled
Scenario: v4.client.classification.vendor-class-exists
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool. # TODO needs option support

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: vendor-class[*].exists
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

@v4 @dhcp4 @classification @disabled
Scenario: v4.client.classification.specific-vendor-class
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool. # TODO needs option support

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: vendor-class[4444].exists
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

@v4 @dhcp4 @classification @disabled
Scenario: v4.client.classification.specific-vendor-class-2
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool. # TODO needs option support

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: vendor-class.enterprise == 4444
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

@v4 @dhcp4 @classification @disabled
Scenario: v4.client.classification.expressions-not-equal
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool. # TODO needs option support

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: not(vendor-class.enterprise == 5555)
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

@v4 @dhcp4 @classification @disabled
Scenario: v4.client.classification.expressions-and
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool. # TODO needs option support

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: (vendor.enterprise == 4444) and (vendor[4444].option[1].hex == 0x0021)
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

@v4 @dhcp4 @classification @disabled
Scenario: v4.client.classification.expressions-or
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool. # TODO needs option support

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: (vendor.enterprise == 4444) or (vendor[*].option[1].hex == 0x0021)
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

@v4 @dhcp4 @classification @disabled
Scenario: v4.client.classification.expressions-substring
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool. # TODO needs option support

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: substring(option[1].hex,6,all) == 0x44332211
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

@v4 @dhcp4 @classification @disabled
Scenario: v4.client.classification.expressions-concat
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool. # TODO needs option support

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: concat(substring(option[1].hex,0,3),substring(option[1].hex,8,all)) == 0x0003002211
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.

@v4 @dhcp4 @classification @disabled
Scenario: v4.client.classification.expressions-ifelse
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool. # TODO needs option support

  Add class called Client_Class_1.
  To class no 1 add parameter named: test with value: ifelse(vendor[4444].option[1].exists, vendor[4444].option[1].hex, 'none') == 0x0021
  # 0021 == 33
  Server is configured with client-classification option in subnet 0 with name Client_Class_1.
  Send server configuration using SSH and config-file.

  DHCP server is started.
