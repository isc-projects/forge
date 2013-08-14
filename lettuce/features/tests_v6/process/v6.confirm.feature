Feature: DHCPv6 Confirm 
    Those are tests for confirm - reply exchange.
	
@v6 @status_code @confirm
    Scenario: v6.statuscode.success.confirm

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

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
	#Response MUST include option 3.
	#Response option 3 MUST contain option 13. 
	#Response option 13 MUST contain statuscode 0.
	#Scapy bug, uncomment this after bug fixing, kea6 fails 
	
	References: RFC3315 sections 18.1.2, 18.2.2
	
@v6 @status_code @confirm
    Scenario: v6.statuscode.notonlink.confirm

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

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

	Test Setup:
	Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::ffff pool.
	Server is started.

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
	Client adds saved options. And Erase.
	#add IA NA from beginning of the test. makes it NotOnlink 
	Client sends CONFIRM message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	#Response option 3 MUST contain option 13. 
	#Response option 13 MUST contain statuscode 4.
	#Scapy bug, uncomment this after bug fixing, kea6 fails 
	
	References: RFC3315 sections 18.1.2, 18.2.2
	