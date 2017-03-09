Feature: Host Reservation DHCPv4
    Tests for Host Reservation feature for hostname based on MAC address.

@v4 @host_reservation @kea_only
    Scenario: v4.host.reservation.hostname-hostname-option
    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.30-192.168.50.30 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    DDNS server is configured with qualifying-suffix option set to my.domain.com.
    Reserve hostname reserved-name in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:04.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:04.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.30.
    Client adds to the message hostname with value some-name.
    Client sets chaddr value to ff:01:02:03:ff:04.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST include option 12.
    Response option 12 MUST contain value reserved-name.my.domain.com.


@v4 @host_reservation @kea_only
    Scenario: v4.host.reservation.hostname-fqdn-option
    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.30-192.168.50.30 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    DDNS server is configured with qualifying-suffix option set to my.domain.com.
    Reserve hostname reserved-name in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:04.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:04.
    Client sets FQDN_domain_name value to sth6.six.example.com..
    Client sets FQDN_flags value to S.
    Client does include fqdn.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 81.
    Response option 81 MUST contain fqdn reserved-name.my.domain.com..

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.30.
    Client sets FQDN_domain_name value to sth6.six.example.com..
    Client sets FQDN_flags value to S.
    Client does include fqdn.
    Client sets chaddr value to ff:01:02:03:ff:04.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST include option 81.
    Response option 81 MUST contain fqdn reserved-name.my.domain.com..


@v4 @host_reservation @kea_only
    Scenario: v4.host.reservation.hostname-hostname-option-and-address
    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.20-192.168.50.30 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    DDNS server is configured with qualifying-suffix option set to my.domain.com.
    Reserve hostname reserved-name in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:04.
    For host reservation entry no. 0 in subnet 0 add address with value 192.168.50.5.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Sleep for 2 seconds.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:04.
    #Client adds to the message hostname with value some-name.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.5.
    Client adds to the message hostname with value some-name.
    Client sets chaddr value to ff:01:02:03:ff:04.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.5.
    Response MUST include option 12.
    Response option 12 MUST contain value reserved-name.my.domain.com.


@v4 @host_reservation @kea_only
    Scenario: v4.host.reservation.hostname-hostname-option-and-address-2
    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.20-192.168.50.30 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    DDNS server is configured with qualifying-suffix option set to my.domain.com.
    Reserve address 192.168.50.5 in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:04.
    For host reservation entry no. 0 in subnet 0 add hostname with value reserved-name.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Sleep for 2 seconds.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:04.
    #Client adds to the message hostname with value some-name.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.5.
    Client adds to the message hostname with value some-name.
    Client sets chaddr value to ff:01:02:03:ff:04.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.5.
    Response MUST include option 12.
    Response option 12 MUST contain value reserved-name.my.domain.com.

@v4 @host_reservation @kea_only
    Scenario: v4.host.reservation.hostname-hostname-option-and-address-3
    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.30 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    DDNS server is configured with qualifying-suffix option set to my.domain.com.
    Reserve hostname reserved-name in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:04.
    For host reservation entry no. 0 in subnet 0 add address with value 192.168.50.5.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Sleep for 2 seconds.

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:ff:04.
    #Client adds to the message hostname with value some-name.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.5.
    Client adds to the message hostname with value some-name.
    Client sets chaddr value to ff:01:02:03:ff:04.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.5.
    Response MUST include option 12.
    Response option 12 MUST contain value reserved-name.my.domain.com.


@v4 @host_reservation @kea_only
    Scenario: v4.host.reservation.hostname-multiple-entries
    Test Setup:
    # outside of the pool
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.30-192.168.50.30 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    DDNS server is configured with qualifying-suffix option set to my.domain.com.
    Reserve hostname reserved-name in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:04.
    Reserve hostname resderved-name in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:44.
    Send server configuration using SSH and config-file.
DHCP server is started.


@v4 @host_reservation @kea_only
    Scenario: v4.host.reservation.hostname-duplicated-entries
    Test Setup:
    # outside of the pool
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.30-192.168.50.30 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    DDNS server is configured with qualifying-suffix option set to my.domain.com.
    Reserve hostname reserved-name in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:04.
    Reserve hostname resderved-name in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:04.
    Send server configuration using SSH and config-file.
DHCP server failed to start. During configuration process.


