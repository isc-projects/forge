Feature: Kea6 legal logging

@v4 @dhcp4 @kea_only @user_check
    Scenario: v4_legal_log.1

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.50 pool.
    Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/libdhcp_legal_log.so.
    DHCP server is started.
    
    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:00.
    Client adds to the message client_id with value 00010203040506.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.1.
	Response MUST include option 1.
	Response MUST include option 54.
	Response MUST include option 61.
    Response option 1 MUST contain value 255.255.255.0.
    Response option 61 MUST contain value 00010203040506.

    Test Procedure:
    Client adds to the message client_id with value 00010203040506.
    Client sets chaddr value to 00:00:00:00:00:00.
    Client copies server_id option from received message.
	Client adds to the message requested_addr with value 192.168.50.1.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
	Response MUST include option 1.
	Response MUST include option 54.
	Response MUST include option 61.
    Response option 1 MUST contain value 255.255.255.0.
    Response option 61 MUST contain value 00010203040506.


    Test Procedure:
    Client adds to the message client_id with value 00010203040577.
    Set network variable source_port with value 67.
    Set network variable source_address with value $(GIADDR4).
    Set network variable destination_address with value $(SRV4_ADDR).
    Client sets giaddr value to $(GIADDR4).
    Client sets hops value to 1.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.2.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client adds to the message client_id with value 00010203040577.
    Client sets giaddr value to $(GIADDR4).
    Client sets hops value to 1.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.2.
    Client requests option 1.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.2.
	Response MUST include option 1.
    Response option 1 MUST contain value 255.255.255.0.


@v4 @dhcp4 @kea_only @user_check
Scenario: v4_legal_log.2
    	Test Setup:
	Time renew-timer is configured with value 2.
	Time rebind-timer is configured with value 50.
	Time valid-lifetime is configured with value 500.
	Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/libdhcp_legal_log.so.
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	DHCP server is started.

	Test Procedure:
    Set network variable source_port with value 67.
    Set network variable source_address with value $(GIADDR4).
    Set network variable destination_address with value $(SRV4_ADDR).
    Client sets giaddr value to $(GIADDR4).
    Client sets hops value to 1.
	Client requests option 1.
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
	Response MUST contain yiaddr 192.168.50.1.
	Response MUST include option 1.
	Response MUST include option 54.
	Response option 1 MUST contain value 255.255.255.0.
	Response option 54 MUST contain value $(SRV4_ADDR).

	Test Procedure:
    Client sets giaddr value to $(GIADDR4).
    Client sets hops value to 1.
	Client copies server_id option from received message.
	Client adds to the message requested_addr with value 192.168.50.1.
	Client requests option 1.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with ACK message.
	Response MUST contain yiaddr 192.168.50.1.
	Response MUST include option 1.
	Response MUST include option 54.
	Response option 1 MUST contain value 255.255.255.0.
	Response option 54 MUST contain value $(SRV4_ADDR).

	#make sure that T1 time expires and client will be in RENEWING state.
	Sleep for 3 seconds.

	Test Procedure:
    Client sets giaddr value to $(GIADDR4).
    Client sets hops value to 1.
	Client sets ciaddr value to 192.168.50.1.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with ACK message.
	Response MUST contain yiaddr 192.168.50.1.
	Response MUST include option 54.
	Response option 54 MUST contain value $(SRV4_ADDR).