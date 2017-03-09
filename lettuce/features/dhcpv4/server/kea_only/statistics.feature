Feature: Kea Statistics
    Feature to test all Statistics and control channel in Kea4. Temporary disabled.

@disabled
Scenario: stats_4
	Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
    Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
	Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
	Client adds to the message requested_addr with value 192.168.50.1.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.

    Pass Criteria:
    Server MUST NOT respond.

	Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "list-commands","arguments": {}}
	Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"statistic-get-all","arguments":{}}

    Test Procedure:
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
	Client adds to the message requested_addr with value 192.168.50.1.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.

    Pass Criteria:
    Server MUST NOT respond.

	Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"statistic-get-all","arguments":{}}

    Test Procedure:
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.1.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.

    Test Procedure:
    Client copies server_id option from received message.
    Client sets ciaddr value to 0.0.0.0.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client sends DECLINE message.

    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client requests option 1.
	Client sets ciaddr value to 192.168.50.9.
    Client sends INFORM message.

    Pass Criteria:
    Server MUST respond with ACK message.

    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt4-received"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt4-discover-received"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt4-offer-received"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt4-request-received"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt4-ack-received"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt4-nak-received"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt4-release-received"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt4-decline-received"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt4-inform-received"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt4-unknown-received"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt4-sent"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt4-offer-sent"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt4-ack-sent"}}

	Test Procedure:
	Client requests option 1.
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.

	Test Procedure:
	Client copies server_id option from received message.
	Client adds to the message requested_addr with value 192.168.50.1.
	Client requests option 1.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with ACK message.

	Test Procedure:
	Client copies server_id option from received message.
	Client adds to the message requested_addr with value 192.168.50.1.
	Client sets chaddr value to 00:00:00:00:00:00.
	Client sets ciaddr value to 255.255.255.255.
	Client requests option 1.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with NAK message.

    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt4-nak-sent"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt4-parse-failed"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt4-receive-drop"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "subnet[1].total-addresses"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "subnet[1].assigned-addresses"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-remove","arguments": {"name": "pkt4-received"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt4-received"}}

	Test Procedure:
	Client requests option 1.
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.

	Test Procedure:
	Client copies server_id option from received message.
	Client adds to the message requested_addr with value 192.168.50.1.
	Client requests option 1.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with NAK message.

    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt4-received"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-reset","arguments": {"name": "pkt4-received"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt4-received"}}

	Test Procedure:
	Client requests option 1.
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.

	Test Procedure:
	Client copies server_id option from received message.
	Client adds to the message requested_addr with value 192.168.50.1.
	Client requests option 1.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with NAK message.

    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt4-received"}}


	Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server is configured with another subnet: 192.168.51.0/24 with 192.168.51.1-192.168.51.1 pool.
    Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
	Send server configuration using SSH and config-file.
Reconfigure DHCP server.

	Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"statistic-get-all","arguments":{}}

	Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server is configured with another subnet: 192.168.51.0/24 with 192.168.51.1-192.168.51.1 pool.
    Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket2.
	Send server configuration using SSH and config-file.
Reconfigure DHCP server.

	Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket2 send {"command":"statistic-get-all","arguments":{}}
	Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"statistic-get-all","arguments":{}}

	Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server is configured with another subnet: 192.168.51.0/24 with 192.168.51.1-192.168.51.1 pool.
	Send server configuration using SSH and config-file.
Reconfigure DHCP server.

	Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"statistic-get-all","arguments":{}}

@disabled
Scenario: X
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with another subnet: 3000:100::/64 with 3000:100::5-3000:100::ff pool.
    Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 92 delegated prefix length.
    Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket2.
	Send server configuration using SSH and config-file.
Reconfigure DHCP server.

	Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket2 send {"command":"statistic-get-all","arguments":{}}

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 92 delegated prefix length.
	Send server configuration using SSH and config-file.
Reconfigure DHCP server.

	Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"statistic-get-all","arguments":{}}

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 92 delegated prefix length.
    Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket2.
	Send server configuration using SSH and config-file.
Reconfigure DHCP server.

	Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket2 send {"command":"statistic-get-all","arguments":{}}

    Restart DHCP server.

    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket2 send {"command":"statistic-get-all","arguments":{}}
