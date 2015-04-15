Feature: Host Reservation DHCPv4
    Tests for Host Reservation feature for address based on MAC address.

@v4 @host_reservation @kea_only
    Scenario: v4.host.reservation.one-address-inside-pool
    Test Setup:
    # outside of the pool
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.50 pool.
    Reserve address 192.168.50.10 in subnet 0 for host uniquely identified by ff:01:02:03:ff:04.
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
    Scenario: v4.host.reservation.one-address-outside-pool
    Test Setup:
    # outside of the pool
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.30-192.168.50.50 pool.
    Reserve address 192.168.50.10 in subnet 0 for host uniquely identified by ff:01:02:03:ff:04.
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

@v4 @host_reservation @kea_only
    Scenario: v4.host.reservation.one-address-inside-pool-different-mac
    Test Setup:
    # request address from different mac that has been reserved
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.50 pool.
    Reserve address 192.168.50.10 in subnet 0 for host uniquely identified by ff:01:02:03:ff:04.
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
    Scenario: v4.host.reservation.multiple-address-reservation-empty-pool
    Test Setup:
    # request address from different mac that has been reserved
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
    Reserve address 192.168.50.10 in subnet 0 for host uniquely identified by ff:01:02:03:ff:04.
    Reserve address 192.168.50.11 in subnet 0 for host uniquely identified by ff:01:02:03:ff:03.
    DHCP server is started.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:01.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST NOT respond with OFFER message.

@v4 @host_reservation @kea_only
    Scenario: v4.host.reservation.multiple-address-reservation-empty-pool-2
    Test Setup:
    # request address from different mac that has been reserved
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.12 pool.
    Reserve address 192.168.50.10 in subnet 0 for host uniquely identified by ff:01:02:03:ff:04.
    Reserve address 192.168.50.11 in subnet 0 for host uniquely identified by ff:01:02:03:ff:03.
    Reserve address 192.168.50.12 in subnet 0 for host uniquely identified by ff:01:02:03:ff:02.
    DHCP server is started.


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