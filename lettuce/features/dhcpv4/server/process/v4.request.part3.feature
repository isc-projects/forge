

Feature: DHCPv4 address request process
    Those are simple DHCPv4 tests for address assignment. During RENEWING/REBINDING state.
 
@v4 @dhcp4 @request
Scenario: v4.request.renewing.success

	Test Setup:
	Time renew-timer is configured with value 2.
	Time rebind-timer is configured with value 50.
	Time valid-lifetime is configured with value 500.
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	DHCP server is started.
	
	Test Procedure:
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
	Client sets ciaddr value to 192.168.50.1.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with ACK message.
	Response MUST contain yiaddr 192.168.50.1.
	Response MUST include option 54.
	Response option 54 MUST contain value $(SRV4_ADDR).
	
@v4 @dhcp4 @request
Scenario: v4.request.rebinding.success

	Test Setup:
	Time renew-timer is configured with value 2.
	Time rebind-timer is configured with value 3.
	Time valid-lifetime is configured with value 500.
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	DHCP server is started.
	
	Test Procedure:
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
	Sleep for 4 seconds.
	
	Test Procedure:
	Client sets ciaddr value to 192.168.50.1.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with ACK message.
	Response MUST contain yiaddr 192.168.50.1.
	Response MUST include option 54.
	Response option 54 MUST contain value $(SRV4_ADDR).

@v4 @dhcp4 @request
Scenario: v4.request.rebinding.fail

	Test Setup:
	Time renew-timer is configured with value 2.
	Time rebind-timer is configured with value 3.
	Time valid-lifetime is configured with value 4.
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	DHCP server is started.

	Test Procedure:
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

	#make sure that leases time expires
	Sleep for 5 seconds.

	Test Procedure:
	Client sets ciaddr value to 192.168.50.1.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with NAK message.
	Response MUST include option 54.
	Response option 54 MUST contain value $(SRV4_ADDR).