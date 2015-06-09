

Feature: DHCPv4 address request process
    Those are simple DHCPv4 tests for address assignment. During INIT-REBOOT state.
 
@v4 @dhcp4 @request
Scenario: v4.request.initreboot.success

	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
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
	Response MUST include option 1.
	Response option 1 MUST contain value 255.255.255.0.
	
	Test Procedure:
	Client adds to the message requested_addr with value 192.168.50.1.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with ACK message.
	Response MUST contain yiaddr 192.168.50.1.
	Response MUST include option 1.
	Response option 1 MUST contain value 255.255.255.0.

@v4 @dhcp4 @request
Scenario: v4.request.initreboot.fail

	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
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
	Response MUST include option 1.
	Response option 1 MUST contain value 255.255.255.0.
	
	Test Procedure:
	Client adds to the message requested_addr with value 185.0.50.0.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with NAK message.
	Response option 54 MUST contain value $(SRV4_ADDR).

@v4 @dhcp4 @request
Scenario: v4.request.initreboot.no-leases

	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
	DHCP server is started.
	
	Test Procedure:
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST NOT respond.

	Test Procedure:
	Client sends DISCOVER message.
	
	Pass Criteria:
	Server MUST respond with OFFER message.
