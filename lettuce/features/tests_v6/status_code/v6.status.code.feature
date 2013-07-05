
Feature: DHCPv6 Relay Agent 
    Those are tests for DHCPv6 status codes. RFC 3315 24.4  

@v6 @status_code
    Scenario: v6.statuscode.noaddravail

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client requests option 7.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Generate new client-id.
	Client sends SOLICIT message.
	
	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	#Response option 3 MUST contain option 13. Scapy bug 
	
	References: RFC3315 section 5.3
	
