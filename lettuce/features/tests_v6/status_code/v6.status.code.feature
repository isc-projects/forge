Feature: DHCPv6 Status Codes 
    Those are tests for DHCPv6 status codes. RFC 3315 24.4  Test for Status Code - UseMulticast are in address_validation feature.

@v6 @status_code
    Scenario: v6.statuscode.noaddravail.solicit

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
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
	Client requests option 7.
	Generate new client-id.
	Client sends SOLICIT message.
	
	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	#Response MUST include option 3.
	#Response option 3 MUST contain option 13. 
	#Response option 13 MUST contain statuscode 2.
	#Scapy bug, uncomment this after bug fixing, kea6 passes
	
	References: RFC3315 section 17.2.2.
	
@v6 @status_code
    Scenario: v6.statuscode.noaddravail.request

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client saves server-id option from received message.
	Client requests option 7.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Generate new IA.
	Client adds saved options. And Erase.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	#Response MUST include option 3.
	#Response option 3 MUST contain option 13. 
	#Response option 13 MUST contain statuscode 2.
	#Scapy bug, uncomment this after bug fixing, kea6 passes 
	
	References: RFC3315 section 18.2.1.
	
	
@v6 @status_code
    Scenario: v6.statuscode.nobinding.renew
	#when client id not known
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.
	
	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 7.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	#Response MUST include option 3.
	#Response option 3 MUST contain option 13. 
	#Response option 13 MUST contain statuscode 3.
	#Scapy bug, uncomment this after bug fixing, kea6 passes 
	
	References: RFC3315 section 18.2.3

@v6 @status_code
    Scenario: v6.statuscode.nobinding.release
	#no address included to release
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
	Client saves server-id option from received message.
	Client requests option 7.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Generate new IA.
	Client adds saved options. And Erase.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	#Response MUST include option 3.
	#Response option 3 MUST contain option 13. 
	#Response option 13 MUST contain statuscode 3.
	#Scapy bug, uncomment this after bug fixing, kea6 passes 
	
	References: RFC3315 section 18.2.6.
	
@v6 @status_code
    Scenario: v6.statuscode.nobinding.release.restart
	#no address to release
	#also can be design with decline
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
	Client copies server-id option from received message.
	
	#MAKE HERE RESTART DHCP 
	
	Client requests option 7.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	#Response MUST include option 3.
	#Response option 3 MUST contain option 13. 
	#Response option 13 MUST contain statuscode 3.
	#Scapy bug, uncomment this after bug fixing, kea6 passes 
	
	References: RFC3315 section 18.2.6.
	
@v6 @status_code
    Scenario: v6.statuscode.success.release
	
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
	Client copies server-id option from received message.
	Client requests option 7.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	#Response MUST include option 3.
	#Response option 3 MUST contain option 13. 
	#Response option 13 MUST contain statuscode 0.
	#Scapy bug, uncomment this after bug fixing, kea6 passes 
	
	References: RFC3315 section 18.2.6.