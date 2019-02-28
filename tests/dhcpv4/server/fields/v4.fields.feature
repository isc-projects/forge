

Feature: DHCPv4 message fields
    This is a simple DHCPv4 message fields validation. Its purpose is to check
    if server is checking received values not just copy-paste.

	# References in all tests are temporary empty, that's intentional.

@v4 @dhcp4 @fields
Scenario: v4.message.fields.chaddr
	# that test needs more work with chaddr
	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
	Send server configuration using SSH and config-file.
DHCP server is started.
	
	Test Procedure:
	Client requests option 1.
	Client sets chaddr value to ff:01:02:03:ff:04.
	Client sends DISCOVER message.
	
	Pass Criteria:
	Server MUST respond with OFFER message.
	#Response MUST contain chaddr ff:01:02:03:ff:04.

@v4 @dhcp4 @fields @ciaddr
Scenario: v4.message.fields.ciaddr-correct-offer

	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
	Send server configuration using SSH and config-file.
DHCP server is started.
	
	Test Procedure:
	Client requests option 1.
	Client sets ciaddr value to $(CIADDR).
	Client sends DISCOVER message.
	
	Pass Criteria:
	Server MUST respond with OFFER message.
	Response MUST contain ciaddr 0.0.0.0.
	Response MUST NOT contain ciaddr $(CIADDR).
	
@v4 @dhcp4 @fields @ciaddr
Scenario: v4.message.fields.ciaddr-incorrect-offer
	
	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
	Send server configuration using SSH and config-file.
DHCP server is started.
	
	Test Procedure:
	Client requests option 1.
	Client sets ciaddr value to 255.255.255.255.
	Client sends DISCOVER message.
	
	Pass Criteria:
	Server MUST respond with OFFER message.
	Response MUST contain ciaddr 0.0.0.0.
	Response MUST NOT contain ciaddr 255.255.255.255.

@v4 @dhcp4 @fields @ciaddr
Scenario: v4.message.fields.ciaddr-incorrect-nak

	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Send server configuration using SSH and config-file.
DHCP server is started.
	
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
	Response MUST contain ciaddr 0.0.0.0.
	Response MUST NOT contain ciaddr 255.255.255.255.

@v4 @dhcp4 @fields @ciaddr
Scenario: v4.message.fields.ciaddr-correct-nak

	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Send server configuration using SSH and config-file.
DHCP server is started.
	
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
	Client sets ciaddr value to 192.168.50.1.
	Client requests option 1.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with NAK message.
	Response MUST contain ciaddr 0.0.0.0.
	Response MUST NOT contain ciaddr 192.168.50.1.

@v4 @dhcp4 @fields @siaddr
Scenario: v4.message.fields.siaddr-correct-offer

	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
	Send server configuration using SSH and config-file.
DHCP server is started.
	
	Test Procedure:
	Client requests option 1.
	Client sets siaddr value to $(CIADDR).
	Client sends DISCOVER message.
	
	Pass Criteria:
	Server MUST respond with OFFER message.
	Response MUST contain siaddr 0.0.0.0.
	Response MUST NOT contain siaddr $(CIADDR).
	
@v4 @dhcp4 @fields @siaddr
Scenario: v4.message.fields.siaddr-incorrect-offer
	
	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
	Send server configuration using SSH and config-file.
DHCP server is started.
	
	Test Procedure:
	Client requests option 1.
	Client sets siaddr value to 255.255.255.255.
	Client sends DISCOVER message.
	
	Pass Criteria:
	Server MUST respond with OFFER message.
	Response MUST contain siaddr 0.0.0.0.
	Response MUST NOT contain siaddr 255.255.255.255.

@v4 @dhcp4 @fields @siaddr
Scenario: v4.message.fields.siaddr-incorrect-nak

	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Send server configuration using SSH and config-file.
DHCP server is started.
	
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
	Client sets siaddr value to 255.255.255.255.
	Client requests option 1.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with NAK message.
	Response MUST contain siaddr 0.0.0.0.
	Response MUST NOT contain siaddr 255.255.255.255.

@v4 @dhcp4 @fields @siaddr
Scenario: v4.message.fields.siaddr-correct-nak   
	
	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Send server configuration using SSH and config-file.
DHCP server is started.
	
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
	Client sets siaddr value to 192.168.50.1.
	Client requests option 1.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with NAK message.
	Response MUST contain siaddr 0.0.0.0.
	Response MUST NOT contain siaddr 192.168.50.1.
	
@v4 @dhcp4 @fields @siaddr
Scenario: v4.message.fields.siaddr-correct-offer-configured-global

	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
	Next server global value is configured with address 192.0.2.234.
	Send server configuration using SSH and config-file.
DHCP server is started.
	
	Test Procedure:
	Client requests option 1.
	Client sends DISCOVER message.
	
	Pass Criteria:
	Server MUST respond with OFFER message.
	Response MUST contain siaddr 192.0.2.234.

@v4 @dhcp4 @fields @siaddr
Scenario: v4.message.fields.siaddr-correct-offer-configured-local

	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
	Next server value on subnet 0 is configured with address 192.0.2.234.
	Send server configuration using SSH and config-file.
DHCP server is started.
	
	Test Procedure:
	Client requests option 1.
	Client sends DISCOVER message.
	
	Pass Criteria:
	Server MUST respond with OFFER message.
	Response MUST contain siaddr 192.0.2.234.

@v4 @dhcp4 @fields @siaddr
Scenario: v4.message.fields.siaddr-correct-nak-configured-local
	
	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Next server value on subnet 0 is configured with address 192.0.2.234.
	Send server configuration using SSH and config-file.
DHCP server is started.
	
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
	Client requests option 1.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with NAK message.
	Response MUST contain siaddr 192.0.2.234.

@v4 @dhcp4 @fields @siaddr
Scenario: v4.message.fields.siaddr-correct-nak-configured-global
	
	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Next server global value is configured with address 192.0.2.234.
	Send server configuration using SSH and config-file.
DHCP server is started.
	
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
	Client requests option 1.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with NAK message.
	Response MUST contain siaddr 192.0.2.234.