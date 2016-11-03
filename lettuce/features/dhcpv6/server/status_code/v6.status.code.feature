Feature: DHCPv6 Status Codes 
    Those are tests for DHCPv6 status codes. RFC 3315 24.4  Test for Status Code - UseMulticast are in address_validation feature or process feature.

@v6 @dhcp6 @status_code
    Scenario: v6.statuscode.noaddravail-solicit

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
	DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Generate new client.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 13. 
	Response sub-option 13 from option 3 MUST contain statuscode 2.
	
	References: RFC3315 section 17.2.2.
	
@v6 @dhcp6 @status_code @request
    Scenario: v6.statuscode.noaddravail-request

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
	DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client saves server-id option from received message.
	Client requests option 7.
	Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	Generate new IA.
    Generate new client.
	Client adds saved options. And Erase.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 13. 
	Response sub-option 13 from option 3 MUST contain statuscode 2.
	
	References: RFC3315 section 18.2.1.
	
	
@v6 @dhcp6 @status_code @renew
    Scenario: v6.statuscode.nobinding-renew
	#when client id not known
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.
	
	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client does include client-id.
    Client sends RENEW message.


	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
#   changed after rfc7550
#	Response option 3 MUST contain sub-option 13.
#	Response sub-option 13 from option 3 MUST contain statuscode 3.
	Response option 3 MUST contain sub-option 5.
	Response sub-option 5 from option 3 MUST contain address 3000::1.
	
	References: RFC3315 section 18.2.3
	
@v6 @dhcp6 @status_code @renew @disabled
    # rfc 7550
    Scenario: v6.statuscode.nobinding-renew-newIA
	#when client id not known
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.
	
	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client does include client-id.
    Before sending a message set filed named iaid to 66 as type int.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
#   changed after rfc7550
#	Response option 3 MUST contain sub-option 13.
#	Response sub-option 13 from option 3 MUST contain statuscode 3.
	
	References: RFC3315 section 18.2.3