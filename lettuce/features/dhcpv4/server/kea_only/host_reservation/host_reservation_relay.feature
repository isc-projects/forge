Feature: Host Reservation DHCPv4
  Tests for Host Reservation feature based on Relay Agent supplied info, negative tests and reserved classes.

@v4 @host_reservation @kea_only
Scenario: v4.host.reservation.circuit-id
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Reserve address 192.168.50.10 in subnet 0 for host uniquely identified by circuit-id 060106020603.
  #"host-reservation-identifiers": [ "hw-address", "duid", "circuit-id", "client-id" ]
  Add to config file line: "host-reservation-identifiers": [ "circuit-id" ]
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.1.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message relay_agent_information with value 16616263.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.10.

  Test Procedure:
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message relay_agent_information with value 16616263.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

@v4 @host_reservation @kea_only
Scenario: v4.host.reservation.circuit-id-negative
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Reserve address 192.168.50.10 in subnet 0 for host uniquely identified by circuit-id 060106020603.
  #"host-reservation-identifiers": [ "hw-address", "duid", "circuit-id", "client-id" ]
  Add to config file line: "host-reservation-identifiers": [ "hw-address", "duid", "client-id" ]
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.1.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message relay_agent_information with value 16616263.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST NOT contain yiaddr 192.168.50.10.


@v4 @host_reservation @kea_only
Scenario: v4.host.reservation.duid
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Reserve address 192.168.50.10 in subnet 0 for host uniquely identified by duid 04:33:44.
  #"host-reservation-identifiers": [ "hw-address", "duid", "circuit-id", "client-id" ]
  Add to config file line: "host-reservation-identifiers": [ "duid" ]
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.1.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message client_id with value ff:01:02:03:ff:04:33:44.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.10.

  Test Procedure:
  Client copies server_id option from received message.
  Client adds to the message client_id with value ff:01:02:03:ff:04:33:44.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

@v4 @host_reservation @kea_only
Scenario: v4.host.reservation.duid-negative
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Reserve address 192.168.50.10 in subnet 0 for host uniquely identified by duid 04:33:44.
  #"host-reservation-identifiers": [ "hw-address", "duid", "circuit-id", "client-id" ]
  Add to config file line: "host-reservation-identifiers": [ "hw-address", "circuit-id", "client-id" ]
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.1.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message client_id with value ff:01:02:03:ff:04:33:44.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST NOT contain yiaddr 192.168.50.10.

@v4 @host_reservation @kea_only
Scenario: v4.host.reservation.hwaddr-negative
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Reserve address 192.168.50.10 in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:11.
  #"host-reservation-identifiers": [ "hw-address", "duid", "circuit-id", "client-id" ]
  Add to config file line: "host-reservation-identifiers": [ "circuit-id", "duid", "client-id" ]
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.1.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:11.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST NOT contain yiaddr 192.168.50.10.

@v4 @host_reservation @kea_only
Scenario: v4.host.reservation.client-id-negative
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Reserve address 192.168.50.10 in subnet 0 for host uniquely identified by client-id ff:01:02:03:ff:11:22.
  #"host-reservation-identifiers": [ "hw-address", "duid", "circuit-id", "client-id" ]
  Add to config file line: "host-reservation-identifiers": [ "circuit-id", "duid", "hw-address" ]
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message client_id with value ff:01:02:03:ff:04:33:44.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.1.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:11.
  Client adds to the message client_id with value ff:01:02:03:ff:11:22.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST NOT contain yiaddr 192.168.50.10.

@v4 @host_reservation @kea_only
Scenario: v4.host.reservation.reserved-classes-1
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.

  Add class called ipxe_efi_x64.
  To class no 1 add parameter named: next-server with value: 192.0.2.254
  To class no 1 add parameter named: server-hostname with value: hal9000
  To class no 1 add parameter named: boot-file-name with value: /dev/null
  To class no 1 add option interface-mtu with value 321.

  To subnet 0 configuration section in the config file add line: ,"reservations": [{"hw-address": "aa:bb:cc:dd:ee:ff","ip-address": "192.168.50.10","client-classes": [ "ipxe_efi_x64" ]}]
  Add to config file line: "host-reservation-identifiers": [ "hw-address" ]
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:55.
  Client requests option 26.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST NOT include option 26.
  Response MUST contain yiaddr 192.168.50.1.

  Test Procedure:
  Client sets chaddr value to aa:bb:cc:dd:ee:ff.
  Client requests option 26.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 26.
  Response option 26 MUST contain value 321.

  Test Procedure:
  Client requests option 26.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client sets chaddr value to aa:bb:cc:dd:ee:ff.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 26.
  Response option 26 MUST contain value 321.
  Response MUST contain siaddr 192.0.2.254.
  Response MUST contain file /dev/null.
  Response MUST contain sname hal9000.

@v4 @host_reservation @kea_only
Scenario: v4.host.reservation.reserved-classes-2
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.

  Add class called ipxe_efi_x64.
  To class no 1 add parameter named: server-hostname with value: hal9000
  To class no 1 add parameter named: boot-file-name with value: /dev/null

  Add class called class-abc.
  To class no 2 add parameter named: next-server with value: 192.0.2.254
  To class no 2 add option interface-mtu with value 321.

  To subnet 0 configuration section in the config file add line: ,"reservations": [{"hw-address": "aa:bb:cc:dd:ee:ff","ip-address": "192.168.50.10","client-classes": [ "ipxe_efi_x64", "class-abc" ]}]
  Add to config file line: "host-reservation-identifiers": [ "hw-address" ]
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:55.
  Client requests option 26.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST NOT include option 26.
  Response MUST contain yiaddr 192.168.50.1.

  Test Procedure:
  Client sets chaddr value to aa:bb:cc:dd:ee:ff.
  Client requests option 26.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 26.
  Response option 26 MUST contain value 321.

  Test Procedure:
  Client requests option 26.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client sets chaddr value to aa:bb:cc:dd:ee:ff.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 26.
  Response option 26 MUST contain value 321.
  Response MUST contain siaddr 192.0.2.254.
  Response MUST contain file /dev/null.
  Response MUST contain sname hal9000.