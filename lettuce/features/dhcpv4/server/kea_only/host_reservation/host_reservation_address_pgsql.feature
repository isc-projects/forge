Feature: Host Reservation DHCPv4 stored in PostgreSQL database.
    Tests for Host Reservation feature for address based on MAC address.

@v4 @host_reservation @kea_only
    Scenario: v4.host.reservation.pgsql.one-address-inside-pool
    Test Setup:
    # outside of the pool
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.50 pool.
  Use PostgreSQL reservation system.
	Create new PostgreSQL reservation identified by hw-address ff:01:02:03:ff:04.
	Add hostname reserved-hostname to PostgreSQL reservation record id 1.
	Add ipv4_address 192.168.50.10 to PostgreSQL reservation record id 1.
	Add dhcp4_subnet_id 1 to PostgreSQL reservation record id 1.
    Upload hosts reservation to PostgreSQL database.


    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:04.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.10.

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

@v4 @host_reservation @kea_only @disabled
  Scenario: v4.host.reservation.pgsql.client-id-one-address-inside-pool
  Test Setup:
  # outside of the pool
  #TODO update names
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.50 pool.
  Use PostgreSQL reservation system.
  Create new PostgreSQL reservation identified by client-id 00010203040577.
  Add to config file line: "host-reservation-identifiers": [ "hw-address", "duid", "client-id" ]
  Add hostname reserved-hostname to PostgreSQL reservation record id 1.
  Add ipv4_address 192.168.50.10 to PostgreSQL reservation record id 1.
  Add dhcp4_subnet_id 1 to PostgreSQL reservation record id 1.
  Upload hosts reservation to PostgreSQL database.

  Send server configuration using SSH and config-file.
DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message client_id with value 00010203040577.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.10.

  Test Procedure:
  Client adds to the message client_id with value 00010203040577.
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
    Scenario: v4.host.reservation.pgsql.one-address-inside-pool-option
    Test Setup:
    # outside of the pool
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.50 pool.
  Use PostgreSQL reservation system.
	Create new PostgreSQL reservation identified by hw-address ff:01:02:03:ff:04.
	Add next_server 11.1.1.1 to PostgreSQL reservation record id 1.
	Add server_hostname hostname-server.com to PostgreSQL reservation record id 1.
	Add boot_file_name file-name to PostgreSQL reservation record id 1.
	Add ipv4_address 192.168.50.10 to PostgreSQL reservation record id 1.
	Add dhcp4_subnet_id 1 to PostgreSQL reservation record id 1.
    Add option reservation code 11 value 10.0.0.1 space dhcp4 persistent 1 client class $(EMPTY) subnet id 1 and scope subnet to PostgreSQL record id 1.
    Server is configured with resource-location-servers option with value 199.199.199.1,150.150.150.1.
    Upload hosts reservation to PostgreSQL database.


    Send server configuration using SSH and config-file.
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
    Scenario: v4.host.reservation.pgsql.one-address-outside-pool-dual-backend
    Test Setup:
    # outside of the pool
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.30-192.168.50.50 pool.
  Use PostgreSQL reservation system.
    Create new PostgreSQL reservation identified by hw-address ff:01:02:03:ff:04.
	Add hostname reserved-hostname to PostgreSQL reservation record id 1.
	Add ipv4_address 192.168.50.10 to PostgreSQL reservation record id 1.
	Add dhcp4_subnet_id 1 to PostgreSQL reservation record id 1.
	Upload hosts reservation to PostgreSQL database.
	Reserve address 192.168.50.11 in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:03.
	Send server configuration using SSH and config-file.
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
    Scenario: v4.host.reservation.pgsql.one-address-outside-pool-dual-backend
    Test Setup:
    # outside of the pool
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.30-192.168.50.50 pool.
  Use PostgreSQL reservation system.
    Create new PostgreSQL reservation identified by hw-address ff:01:02:03:ff:04.
	Add hostname reserved-hostname to PostgreSQL reservation record id 1.
  Add next_server 1.1.1.1 to PostgreSQL reservation record id 1.
	Add ipv4_address 192.168.50.10 to PostgreSQL reservation record id 1.
	Add dhcp4_subnet_id 1 to PostgreSQL reservation record id 1.
	Upload hosts reservation to PostgreSQL database.
	Reserve address 192.168.50.11 in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:03.
	Send server configuration using SSH and config-file.
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
    Scenario: v4.host.reservation.pgsql.one-address-inside-pool-different-mac
    Test Setup:
    # request address from different mac that has been reserved
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.50 pool.
  Use PostgreSQL reservation system.
    Create new PostgreSQL reservation identified by hw-address ff:01:02:03:ff:04.

	Add hostname reserved-hostname to PostgreSQL reservation record id 1.
	Add ipv4_address 192.168.50.10 to PostgreSQL reservation record id 1.
	Add dhcp4_subnet_id 1 to PostgreSQL reservation record id 1.
	Upload hosts reservation to PostgreSQL database.
    Send server configuration using SSH and config-file.
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
    Reserve address 192.168.50.10 in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:04.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:01.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST NOT respond with OFFER message.


@v4 @host_reservation @kea_only
    Scenario: v4.host.reservation.pgsql.multiple-address-reservation-empty-pool
    Test Setup:
    # request address from different mac that has been reserved
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
Use PostgreSQL reservation system.
    Create new PostgreSQL reservation identified by hw-address ff:01:02:03:ff:04.
	Add hostname reserved-hostname to PostgreSQL reservation record id 1.
	Add ipv4_address 192.168.50.10 to PostgreSQL reservation record id 1.
	Add dhcp4_subnet_id 1 to PostgreSQL reservation record id 1.

    Create new PostgreSQL reservation identified by hw-address ff:01:02:03:ff:03.
	Add hostname reserved-hostname to PostgreSQL reservation record id 2.
	Add ipv4_address 192.168.50.11 to PostgreSQL reservation record id 2.
	Add dhcp4_subnet_id 1 to PostgreSQL reservation record id 2.
	Upload hosts reservation to PostgreSQL database.

    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:01.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST NOT respond with OFFER message.

@v4 @host_reservation @kea_only
    Scenario: v4.host.reservation.multiple.pgsql-address-reservation-empty-pool-2
    Test Setup:
    # request address from different mac that has been reserved
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.12 pool.
Use PostgreSQL reservation system.
    Create new PostgreSQL reservation identified by hw-address ff:01:02:03:ff:04.
	Add hostname reserved-hostname to PostgreSQL reservation record id 1.
	Add ipv4_address 192.168.50.10 to PostgreSQL reservation record id 1.
	Add dhcp4_subnet_id 1 to PostgreSQL reservation record id 1.

    Create new PostgreSQL reservation identified by hw-address ff:01:02:03:ff:03.
	Add hostname reserved-hostname to PostgreSQL reservation record id 2.
	Add ipv4_address 192.168.50.11 to PostgreSQL reservation record id 2.
	Add dhcp4_subnet_id 1 to PostgreSQL reservation record id 2.

    Create new PostgreSQL reservation identified by hw-address ff:01:02:03:ff:02.
	Add hostname reserved-hostname to PostgreSQL reservation record id 3.
	Add ipv4_address 192.168.50.12 to PostgreSQL reservation record id 3.
	Add dhcp4_subnet_id 1 to PostgreSQL reservation record id 3.

	Upload hosts reservation to PostgreSQL database.

    Send server configuration using SSH and config-file.
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


