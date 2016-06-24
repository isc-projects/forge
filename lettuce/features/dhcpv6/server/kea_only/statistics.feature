Feature: Kea Statistics
    Feature to test all Statistics and control channel in Kea4. Temporary disabled.

@disabled
Scenario: stats_6
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 92 delegated prefix length.
    Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
	DHCP server is started.

    Test Procedure:
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

    Test Procedure:
	Client does NOT include IA-NA.
	Client does NOT include client-id.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST NOT respond.

	Exchange messages SOLICIT - ADVERTISE 50 times.

	Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "list-commands","arguments": {}}
	Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"statistic-get-all","arguments":{}}

	Exchange messages SOLICIT - ADVERTISE 50 times.

	Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"statistic-get-all","arguments":{}}

    Exchange messages SOLICIT - ADVERTISE 50 times.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client requests option 7.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client sends CONFIRM message.

	Pass Criteria:
	Server MUST respond with REPLY message.

    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt6-received"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt6-receive-drop"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt6-parse-failed"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt6-solicit-received"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt6-confirm-received"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt6-advertise-received"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt6-reply-received"}}

	Test Procedure:
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.

    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt6-renew-received"}}

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST respond with REPLY message.

    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt6-rebind-received"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt6-release-received"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt6-decline-received"}}

	Test Procedure:
	Client requests option 7.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt6-infrequest-received"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt6-unknown-received"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt6-sent"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt6-advertise-sent"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt6-reply-sent"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "subnet[1].total-nas"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "subnet[1].assigned-nas"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "subnet[1].total-pds"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "subnet[1].assigned-pds"}}

    Exchange messages REQUEST - REPLY 50 times.

    Test Procedure:
	Client does NOT include IA-NA.
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client does NOT include IA-NA.
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client does NOT include IA-NA.
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.

    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt6-advertise-sent"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt6-reply-sent"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "subnet[1].total-nas"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "subnet[1].assigned-nas"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "subnet[1].total-pds"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "subnet[1].assigned-pds"}}

    Exchange messages REQUEST - REPLY 50 times.

    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get-all","arguments":{}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "subnet[1].total-nas"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "subnet[1].assigned-nas"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-reset","arguments": {"name": "pkt6-request-received"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}

    Exchange messages SOLICIT - ADVERTISE 50 times.

    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}

    Exchange messages REQUEST - REPLY 50 times.

    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-remove","arguments": {"name": "pkt6-request-received"}}
    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}

    Exchange messages SOLICIT - ADVERTISE 50 times.

    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}

    Exchange messages REQUEST - REPLY 50 times.

    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client requests option 7.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "statistic-get","arguments": {"name": "pkt6-decline-received"}}

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with another subnet: 3000:100::/64 with 3000:100::5-3000:100::ff pool.
    Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 92 delegated prefix length.
    Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket2.
	Reconfigure DHCP server.

	Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket2 send {"command":"statistic-get-all","arguments":{}}

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 92 delegated prefix length.
	Reconfigure DHCP server.

	Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"statistic-get-all","arguments":{}}

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 92 delegated prefix length.
    Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket2.
	Reconfigure DHCP server.

	Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket2 send {"command":"statistic-get-all","arguments":{}}

    Restart DHCP server.

    Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket2 send {"command":"statistic-get-all","arguments":{}}
