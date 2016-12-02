Feature: Host Reservation DHCPv4 stored in MySQL database.
    Tests for Host Reservation feature for address based on MAC address.

@v4 @host_reservation @kea_only
  Scenario: v4.host.reservation.mysql.one-address-inside-pool
  Test Setup:
  # outside of the pool
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.50 pool.
  Use MySQL reservation system.
  Create new MySQL reservation identified by hw-address ff:01:02:03:ff:04.
  Add hostname reserved-hostname to MySQL reservation record id 1.
  Add ipv4_address 192.168.50.10 to MySQL reservation record id 1.
  Add dhcp4_subnet_id 1 to MySQL reservation record id 1.
  Upload hosts reservation to MySQL database.
  
  DHCP server is started.
  
  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.
  
  Pass Criteria:
  Server MUST respond with OFFER message.
  
  Test Procedure:
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.
  
  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  
@v4 @host_reservation @kea_only
  Scenario: v4.host.reservation.mysql.one-address-inside-pool-option
  Test Setup:
  # outside of the pool
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.50 pool.
  Use MySQL reservation system.
  Create new MySQL reservation identified by hw-address ff:01:02:03:ff:04.
  Add next_server 11.1.1.1 to MySQL reservation record id 1.
  Add server_hostname hostname-server.com to MySQL reservation record id 1.
  Add boot_file_name file-name to MySQL reservation record id 1.
  Add ipv4_address 192.168.50.10 to MySQL reservation record id 1.
  Add dhcp4_subnet_id 1 to MySQL reservation record id 1.
  Add option reservation code 11 value 10.0.0.1 space dhcp4 persistent 1 client class $(EMPTY) subnet id 1 and scope subnet to MySQL record id 1.
  Server is configured with resource-location-servers option with value 199.199.199.1,150.150.150.1.
  Upload hosts reservation to MySQL database.
  
  DHCP server is started.
  
  Test Procedure:
  Client requests option 11.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.
  
  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 11.
  Response option 11 MUST contain value 10.0.0.1.
  
  Test Procedure:
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.
  
  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  
@v4 @host_reservation @kea_only
  Scenario: v4.host.reservation.mysql.one-address-outside-pool-dual-backend
  Test Setup:
  # outside of the pool
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.30-192.168.50.50 pool.
  Use MySQL reservation system.
  Create new MySQL reservation identified by hw-address ff:01:02:03:ff:04.
  Add hostname reserved-hostname to MySQL reservation record id 1.
  Add ipv4_address 192.168.50.10 to MySQL reservation record id 1.
  Add dhcp4_subnet_id 1 to MySQL reservation record id 1.
  Upload hosts reservation to MySQL database.
  Reserve address 192.168.50.11 in subnet 0 for host uniquely identified by ff:01:02:03:ff:03.
  DHCP server is started.
  
  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.
  
  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.10.
  Response option 1 MUST contain value 255.255.255.0.
  
  Test Procedure:
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.
  
  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  
  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:03.
  Client sends DISCOVER message.
  
  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.11.
  Response option 1 MUST contain value 255.255.255.0.
  
  Test Procedure:
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.11.
  Client sets chaddr value to ff:01:02:03:ff:03.
  Client sends REQUEST message.
  
  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.11.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  
@v4 @host_reservation @kea_only
  Scenario: v4.host.reservation.mysql.one-address-inside-pool-different-mac
  Test Setup:
  # request address from different mac that has been reserved
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.50 pool.
  Use MySQL reservation system.
  Create new MySQL reservation identified by hw-address ff:01:02:03:ff:04.
  Add hostname reserved-hostname to MySQL reservation record id 1.
  Add ipv4_address 192.168.50.10 to MySQL reservation record id 1.
  Add dhcp4_subnet_id 1 to MySQL reservation record id 1.
  Upload hosts reservation to MySQL database.
  DHCP server is started.
  
  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:01.
  Client sends DISCOVER message.
  
  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST NOT contain yiaddr 192.168.50.10.
  Response option 1 MUST contain value 255.255.255.0.
  
  Test Procedure:
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client sets chaddr value to ff:01:02:03:ff:01.
  Client sends REQUEST message.
  
  Pass Criteria:
  Server MUST respond with NAK message.
  Response MUST contain yiaddr 0.0.0.0.
  
@v4 @host_reservation @kea_only
  Scenario: v4.host.reservation.one-address-empty-pool
  Test Setup:
  # request address from different mac that has been reserved
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
  Reserve address 192.168.50.10 in subnet 0 for host uniquely identified by ff:01:02:03:ff:04.
  DHCP server is started.
  
  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:01.
  Client sends DISCOVER message.
  
  Pass Criteria:
  Server MUST NOT respond with OFFER message.
  
@v4 @host_reservation @kea_only
  Scenario: v4.host.reservation.mysql.multiple-address-reservation-empty-pool
  Test Setup:
  # request address from different mac that has been reserved
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
  Use MySQL reservation system.
  Create new MySQL reservation identified by hw-address ff:01:02:03:ff:04.
  Add hostname reserved-hostname to MySQL reservation record id 1.
  Add ipv4_address 192.168.50.10 to MySQL reservation record id 1.
  Add dhcp4_subnet_id 1 to MySQL reservation record id 1.
  
  Create new MySQL reservation identified by hw-address ff:01:02:03:ff:03.
  Add hostname reserved-hostname to MySQL reservation record id 2.
  Add ipv4_address 192.168.50.11 to MySQL reservation record id 2.
  Add dhcp4_subnet_id 1 to MySQL reservation record id 2.
  Upload hosts reservation to MySQL database.
  
  DHCP server is started.
  
  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:01.
  Client sends DISCOVER message.
  
  Pass Criteria:
  Server MUST NOT respond with OFFER message.
  
@v4 @host_reservation @kea_only
  Scenario: v4.host.reservation.multiple.mysql-address-reservation-empty-pool-2
  Test Setup:
  # request address from different mac that has been reserved
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.12 pool.
  Use MySQL reservation system.
  Create new MySQL reservation identified by hw-address ff:01:02:03:ff:04.
  Add hostname reserved-hostname to MySQL reservation record id 1.
  Add ipv4_address 192.168.50.10 to MySQL reservation record id 1.
  Add dhcp4_subnet_id 1 to MySQL reservation record id 1.
  
  Create new MySQL reservation identified by hw-address ff:01:02:03:ff:03.
  Add hostname reserved-hostname to MySQL reservation record id 2.
  Add ipv4_address 192.168.50.11 to MySQL reservation record id 2.
  Add dhcp4_subnet_id 1 to MySQL reservation record id 2.
  
  Create new MySQL reservation identified by hw-address ff:01:02:03:ff:02.
  Add hostname reserved-hostname to MySQL reservation record id 3.
  Add ipv4_address 192.168.50.12 to MySQL reservation record id 3.
  Add dhcp4_subnet_id 1 to MySQL reservation record id 3.
  
  Upload hosts reservation to MySQL database.
  
  DHCP server is started.
  
  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:01.
  Client sends DISCOVER message.
  
  Pass Criteria:
  Server MUST NOT respond with OFFER message.
  
  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.
  
  Pass Criteria:
  Server MUST respond with OFFER message.
  
  Test Procedure:
  Client copies server_id option from received message.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.
  
  Pass Criteria:
  Server MUST respond with ACK message.
  
  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:03.
  Client sends DISCOVER message.
  
  Pass Criteria:
  Server MUST respond with OFFER message.
  
  Test Procedure:
  Client copies server_id option from received message.
  Client sets chaddr value to ff:01:02:03:ff:03.
  Client sends REQUEST message.
  
  Pass Criteria:
  Server MUST respond with ACK message.
  
  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:02.
  Client sends DISCOVER message.
  
  Pass Criteria:
  Server MUST respond with OFFER message.
  
  Test Procedure:
  Client copies server_id option from received message.
  Client sets chaddr value to ff:01:02:03:ff:02.
  Client sends REQUEST message.
  
  Pass Criteria:
  Server MUST respond with ACK message.
  
  
  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:01.
  Client sends DISCOVER message.
  
  Pass Criteria:
  Server MUST NOT respond with OFFER message.