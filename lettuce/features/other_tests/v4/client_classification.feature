Feature: Client Classification DHCPv4
    not automated

@v4
    Scenario: v4.client.classification.manual

    Test Procedure:
    Client sets chaddr value to ff:01:02:03:04:05.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.


    Test Procedure:
    Client sets chaddr value to ff:01:02:03:04:06.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.

    Test Procedure:
    Client sets yiaddr value to 192.168.50.66.
    Client sets ciaddr value to 192.168.50.1.
    Client sets siaddr value to 192.168.50.1.
    Client sets chaddr value to ff:01:02:03:04:06.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.

    Test Procedure:
    Client sets yiaddr value to 192.168.50.1.
    Client sets ciaddr value to 192.168.50.77.
    Client sets chaddr value to ff:01:02:03:04:06.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.

    Test Procedure:
    Client sets siaddr value to 192.168.50.88.
    Client sets yiaddr value to 192.168.50.1.
    Client sets ciaddr value to 192.168.50.1.
    Client sets chaddr value to ff:01:02:03:04:06.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.

    Test Procedure:
    Client sets siaddr value to 192.168.50.11.
    Client sets yiaddr value to 192.168.50.22.
    Client sets ciaddr value to 192.168.50.33.
    Client sets chaddr value to ff:01:02:03:04:06.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.

    Test Procedure:
    Client sets siaddr value to 192.168.50.1.
    Client sets yiaddr value to 192.168.50.2.
    Client sets ciaddr value to 192.168.50.3.
    Client sets chaddr value to ff:01:01:01:01:01.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.