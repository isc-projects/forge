Feature: Host Reservation DHCPv4
    Tests for Host Reservation feature conflict resolution with address reservation based on MAC address.

@v4 @host_reservation @kea_only
    Scenario: v4.host.reservation.conflicts-duplicate-reservations
    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.50 pool.
    Reserve address 192.168.50.10 in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:04.
    Reserve address 192.168.50.12 in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:04.
    Send server configuration using SSH and config-file.
DHCP server failed to start. During configuration process.


@v4 @host_reservation @kea_only
    Scenario: v4.host.reservation.conflicts-duplicate-reservations-different-subnets
    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.50 pool.
    Server is configured with another subnet: 192.168.51.0/24 with 192.168.51.1-192.168.51.50 pool.
    Reserve address 192.168.50.10 in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:04.
    Reserve address 192.168.50.12 in subnet 1 for host uniquely identified by hw-address ff:01:02:03:ff:04.
    Send server configuration using SSH and config-file.
DHCP server is started.


@v4 @host_reservation @kea_only
    Scenario: v4.host.reservation.conflicts-reconfigure-server-with-reservation-of-used-address

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.2 pool.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:11.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.

    Test Procedure:
    Client copies server_id option from received message.
    Client sets chaddr value to ff:01:02:03:ff:11.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:55.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Test Procedure:
    Client copies server_id option from received message.
    Client sets chaddr value to ff:01:02:03:ff:55.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.


    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.3 pool.
    Reserve address 192.168.50.2 in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:77.
    Send server configuration using SSH and config-file.
Reconfigure DHCP server.


    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:77.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST NOT contain yiaddr 192.168.50.2.

@v4 @host_reservation @kea_only
    Scenario: v4.host.reservation.conflicts-reconfigure-server-with-reservation-of-used-address-2

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.2 pool.
    Reserve address 192.168.50.2 in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:11.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:11.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.

    Test Procedure:
    Client copies server_id option from received message.
    Client sets chaddr value to ff:01:02:03:ff:11.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.2.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:55.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Test Procedure:
    Client copies server_id option from received message.
    Client sets chaddr value to ff:01:02:03:ff:55.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.


    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.3 pool.
    Reserve address 192.168.50.2 in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:77.

    Send server configuration using SSH and config-file.
Reconfigure DHCP server.


    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:77.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST NOT contain yiaddr 192.168.50.2.


@v4 @host_reservation @kea_only
    Scenario: v4.host.reservation.conflicts-reconfigure-server-with-reservation-of-used-address-3
    Test Setup:
    # reconfigure different address for same MAC from outside of the pool
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.5-192.168.50.9 pool.
    Reserve address 192.168.50.10 in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:04.
    Send server configuration using SSH and config-file.
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
    Response MUST contain yiaddr 192.168.50.10.


    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.5-192.168.50.9 pool.
    Reserve address 192.168.50.30 in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:04.

    Send server configuration using SSH and config-file.
Reconfigure DHCP server.


    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:04.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.30.
    Client sets chaddr value to ff:01:02:03:ff:04.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.30.


@v4 @host_reservation @kea_only
    Scenario: v4.host.reservation.conflicts-reconfigure-server-switched-mac-in-reservations-in-pool
    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.5-192.168.50.30 pool.
    Reserve address 192.168.50.10 in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:04.
    Send server configuration using SSH and config-file.
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
    Response MUST contain yiaddr 192.168.50.10.


    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.5-192.168.50.30 pool.
    Reserve address 192.168.50.10 in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:01.

    Send server configuration using SSH and config-file.
Reconfigure DHCP server.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:01.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST NOT contain yiaddr 192.168.50.10.

@v4 @host_reservation @kea_only
    Scenario: v4.host.reservation.conflicts-reconfigure-server-switched-mac-in-reservations-out-of-pool
    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.5-192.168.50.30 pool.
    Reserve address 192.168.50.50 in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:04.
    Send server configuration using SSH and config-file.
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
    Response MUST contain yiaddr 192.168.50.50.


    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.5-192.168.50.30 pool.
    Reserve address 192.168.50.50 in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:01.

    Send server configuration using SSH and config-file.
Reconfigure DHCP server.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:01.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST NOT contain yiaddr 192.168.50.50.


@v4 @host_reservation @kea_only
    Scenario: v4.host.reservation.conflicts-reconfigure-server-add-reservation-for-host-that-has-leases
    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.5-192.168.50.5 pool.
    Send server configuration using SSH and config-file.
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
    Response MUST contain yiaddr 192.168.50.5.


    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.5-192.168.50.5 pool.
    Reserve address 192.168.50.50 in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:04.

    Send server configuration using SSH and config-file.
Reconfigure DHCP server.

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
    Response MUST contain yiaddr 192.168.50.50.

    Test Procedure:
    Client copies server_id option from received message.
    Client sets chaddr value to ff:01:02:03:ff:04.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.50.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:01.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.

    Test Procedure:
    Client copies server_id option from received message.
    Client sets chaddr value to ff:01:02:03:ff:01.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.5.

@v4 @host_reservation @kea_only
    Scenario: v4.host.reservation.conflicts-renew-address-that-has-been-reserved-during-reconfiguration

    Test Setup:
    Time renew-timer is configured with value 3.
    Time rebind-timer is configured with value 50.
    Time valid-lifetime is configured with value 500.
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.5-192.168.50.5 pool.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:01.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:01.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.5.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.5.

    Sleep for 5 seconds.

    Test Setup:
    Time renew-timer is configured with value 3.
    Time rebind-timer is configured with value 50.
    Time valid-lifetime is configured with value 500.
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.5-192.168.50.10 pool.
    Reserve address 192.168.50.5 in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:04.
    Send server configuration using SSH and config-file.
Reconfigure DHCP server.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:04.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST NOT contain yiaddr 192.168.50.5.

    Test Procedure:
    Client adds to the message requested_addr with value 192.168.50.5.
    Client sets chaddr value to ff:01:02:03:ff:01.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with NAK message.

    Sleep for 6 seconds.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:04.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.5.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:04.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.5.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.5.

@v4 @host_reservation @kea_only
    Scenario: v4.host.reservation.conflicts-renew-address-using-different-mac-that-has-been-reserved-during-reconfiguration

    Test Setup:
    Time renew-timer is configured with value 3.
    Time rebind-timer is configured with value 50.
    Time valid-lifetime is configured with value 500.
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.5-192.168.50.5 pool.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:01.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:01.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.5.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.5.

    Sleep for 5 seconds.

    Test Setup:
    Time renew-timer is configured with value 3.
    Time rebind-timer is configured with value 50.
    Time valid-lifetime is configured with value 500.
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.5-192.168.50.10 pool.
    Reserve address 192.168.50.5 in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:04.
    Send server configuration using SSH and config-file.
Reconfigure DHCP server.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:04.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST NOT contain yiaddr 192.168.50.5.

    Test Procedure:
    Client adds to the message requested_addr with value 192.168.50.5.
    Client sets chaddr value to ff:01:02:03:ff:01.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with NAK message.

    Sleep for 6 seconds.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:04.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.5.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with NAK message.

@v4 @host_reservation @kea_only
    Scenario: v4.host.reservation.conflicts-renew-address-which-reservation-changed-during-reconfigure

    Test Setup:
    Time renew-timer is configured with value 3.
    Time rebind-timer is configured with value 50.
    Time valid-lifetime is configured with value 500.
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.5-192.168.50.5 pool.
    Reserve address 192.168.50.5 in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:01.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:01.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:01.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.5.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.5.

    Sleep for 5 seconds.

    Test Setup:
    Time renew-timer is configured with value 3.
    Time rebind-timer is configured with value 50.
    Time valid-lifetime is configured with value 500.
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.5-192.168.50.10 pool.
    Reserve address 192.168.50.5 in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:04.
    Send server configuration using SSH and config-file.
Reconfigure DHCP server.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:04.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST NOT contain yiaddr 192.168.50.5.

    Test Procedure:
    Client adds to the message requested_addr with value 192.168.50.5.
    Client sets chaddr value to ff:01:02:03:ff:01.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with NAK message.

    Sleep for 6 seconds.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:04.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.5.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:04.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.5.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.5.


@v4 @host_reservation @kea_only
    Scenario: v4.host.reservation.conflicts-renew-address-which-reservation-changed-during-reconfigure-2

    Test Setup:
    Time renew-timer is configured with value 3.
    Time rebind-timer is configured with value 50.
    Time valid-lifetime is configured with value 500.
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.50 pool.
    Reserve address 192.168.50.5 in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:01.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:01.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:01.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.5.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.5.

    Sleep for 5 seconds.

    Test Setup:
    Time renew-timer is configured with value 3.
    Time rebind-timer is configured with value 50.
    Time valid-lifetime is configured with value 500.
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.5-192.168.50.60 pool.
    Reserve address 192.168.50.50 in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:01.
    Send server configuration using SSH and config-file.
Reconfigure DHCP server.

    Test Procedure:
    Client adds to the message requested_addr with value 192.168.50.5.
    Client sets chaddr value to ff:01:02:03:ff:01.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with NAK message.

    Sleep for 6 seconds.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:01.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.50.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:01.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.50.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.50.


@v4 @host_reservation @kea_only
    Scenario: v4.host.reservation.conflicts-rebind-address-which-reservation-changed-during-reconfigure

    Test Setup:
    Time renew-timer is configured with value 3.
    Time rebind-timer is configured with value 4.
    Time valid-lifetime is configured with value 500.
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.5-192.168.50.5 pool.
    Reserve address 192.168.50.5 in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:01.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:01.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:01.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.5.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.5.

    Sleep for 5 seconds.

    Test Setup:
    Time renew-timer is configured with value 3.
    Time rebind-timer is configured with value 4.
    Time valid-lifetime is configured with value 500.
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.5-192.168.50.10 pool.
    Reserve address 192.168.50.5 in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:04.
    Send server configuration using SSH and config-file.
Reconfigure DHCP server.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:04.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST NOT contain yiaddr 192.168.50.5.

    Test Procedure:
    Client adds to the message requested_addr with value 192.168.50.5.
    Client sets chaddr value to ff:01:02:03:ff:01.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with NAK message.

    Sleep for 6 seconds.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:04.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.5.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:04.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.5.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.5.


@v4 @host_reservation @kea_only
    Scenario: v4.host.reservation.conflicts-rebind-address-which-reservation-changed-during-reconfigure-2

    Test Setup:
    Time renew-timer is configured with value 3.
    Time rebind-timer is configured with value 4.
    Time valid-lifetime is configured with value 500.
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.50 pool.
    Reserve address 192.168.50.5 in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:01.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:01.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:01.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.5.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.5.

    Sleep for 5 seconds.

    Test Setup:
    Time renew-timer is configured with value 3.
    Time rebind-timer is configured with value 4.
    Time valid-lifetime is configured with value 500.
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.5-192.168.50.60 pool.
    Reserve address 192.168.50.50 in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:01.
    Send server configuration using SSH and config-file.
Reconfigure DHCP server.

    Test Procedure:
    Client adds to the message requested_addr with value 192.168.50.5.
    Client sets chaddr value to ff:01:02:03:ff:01.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with NAK message.

    Sleep for 6 seconds.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:01.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.50.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:01.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.50.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.50.

