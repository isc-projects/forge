Feature: DHCPv6 Prefix Delegation 
    Test for Prefix Delegation using Request messages, based on RFC 3633.

@v6 @dhcp6 @PD @rfc3633
    Scenario: prefix.delegation.onlyPD_request
  
 	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 92 delegated prefix length.
	DHCP server is started.
	
	Test Procedure:
	Client does NOT include IA-NA.
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.

	Test Procedure:
	Client does NOT include IA-NA.
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.

	References: RFC 3633, Section: 12.2

@v6 @dhcp6 @PD @rfc3633
    Scenario: prefix.delegation.IA_and_PD_request
  
 	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
	Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 92 delegated prefix length.
	DHCP server is started.
	
	Test Procedure:
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	Response sub-option 5 from option 3 MUST contain address 3000::1.
		
	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	Response sub-option 5 from option 3 MUST contain address 3000::1.
	
	References: RFC 3633

@v6 @dhcp6 @PD @rfc3633
	Scenario: prefix.delegation.onlyPD_request_release

 	Test Setup:	
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 91 delegated prefix length.
	#pool of two prefixes
	DHCP server is started.
	
	Test Procedure:
	Client does include IA-PD.
	Client does NOT include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client does NOT include IA-NA.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	
	Test Procedure:
	Client copies IA_PD option from received message.
	Client copies server-id option from received message.
	Client does NOT include IA-NA.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 13.
	Response sub-option 13 from option 25 MUST contain statuscode 0.
	# tests MUST NOT include 'NoBinding'...
	
	References: RFC 3633, Section: 12.2

@v6 @dhcp6 @PD @rfc3633
	Scenario: prefix.delegation.onlyPD_multiple_request_release
 	
 	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 91 delegated prefix length.
	#pool of two prefixes
	DHCP server is started.
	
	Test Procedure:
	Client does include IA-PD.
	Client does NOT include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client does NOT include IA-NA.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	
	Test Procedure:
	Client copies IA_PD option from received message.
	Client copies server-id option from received message.
	Client does NOT include IA-NA.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 13.
	Response sub-option 13 from option 25 MUST contain statuscode 0.
	
	Test Procedure:
	Generate new IA_PD.
	Client does include IA-PD.
	Client does NOT include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client does NOT include IA-NA.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	
	Test Procedure:
	Generate new IA_PD.
	Client does include IA-PD.
	Client does NOT include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	# if it fails, it means that release process fails.
	
	References: RFC 3633, Section: 12.2
	
@v6 @dhcp6 @PD @rfc3633
	Scenario: prefix.delegation.IA_and_PD_request_release
 	
 	Test Setup:	
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 91 delegated prefix length.
	#pool of two prefixes
	DHCP server is started.
	
	Test Procedure:
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client copies IA_NA option from received message.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
		
	Test Procedure:
	Client copies IA_PD option from received message.
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response MUST include option 3.
	# tests MUST NOT include 'NoBinding'...
	
	References: RFC 3633
	
@v6 @dhcp6 @PD @rfc3633
	Scenario: prefix.delegation.IA_and_PD_multiple_request_release
 	
 	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 91 delegated prefix length.
	#pool of two prefixes
	DHCP server is started.
	
	Test Procedure:
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client copies IA_NA option from received message.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
		
	Test Procedure:
	Client copies IA_PD option from received message.
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	# tests MUST NOT include 'NoBinding'...	

	Test Procedure:
	Generate new IA_PD.
	Generate new IA.
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client copies IA_NA option from received message.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Generate new IA_PD.
	Generate new IA.
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	References: RFC 3633

@v6 @dhcp6 @PD @rfc3633
    Scenario: prefix.delegation.noprefixavail_release
  	#assign 2 prefixes, try third, fail, release one, assign one more time with success.
 	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 91 delegated prefix length.
	#pool of two prefixes
	DHCP server is started.
	
	Test Procedure:
	Client does include IA-PD.
	Client does NOT include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client does NOT include IA-NA.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	#success
	
	Test Procedure:
	Generate new IA_PD.
	Client does include IA-PD.
	Client does NOT include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client does NOT include IA-NA.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	#both prefixes assigned.
	
	Test Procedure:
	Client saves IA_PD option from received message.
	Generate new IA_PD.
	Client does include IA-PD.
	Client does NOT include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 13.	
	Response sub-option 13 from option 25 MUST contain statuscode 6. 
	
	Test Procedure:
	Client adds saved options. And DONT Erase.
	Client copies server-id option from received message.
	Client does NOT include IA-NA.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 13.	
	Response sub-option 13 from option 25 MUST contain statuscode 0.
	
	Test Procedure:
	Generate new IA_PD.
	Client does include IA-PD.
	Client does NOT include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	
	References: RFC 3633, Section: 11.2 12.2

@v6 @dhcp6 @PD @rfc3633
    Scenario: prefix.delegation.noprefixavail
   	
   	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 91 delegated prefix length.
	#pool of two prefixes
	DHCP server is started.
	
	Test Procedure:
	Client does include IA-PD.
	Client does NOT include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client does NOT include IA-NA.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	
	Test Procedure:
	Generate new IA_PD.
	Client does include IA-PD.
	Client does NOT include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client does NOT include IA-NA.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	#both prefixes assigned.
	
	Test Procedure:
	Generate new IA_PD.
	Client does include IA-PD.
	Client does NOT include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 13.	
	Response sub-option 13 from option 25 MUST contain statuscode 6. 
		
	References: RFC 3633, Section: 11.2

@v6 @dhcp6 @PD @rfc3633
    Scenario: prefix.delegation.release_nobinding

 	Test Setup:
	Server is configured with 3000::/32 subnet with 3000::1-3000::2 pool.
	Server is configured with 3000:: prefix in subnet 0 with 32 prefix length and 33 delegated prefix length.
	DHCP server is started.
	
	Test Procedure:
	Client does NOT include IA-NA.
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client does NOT include IA-NA.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 13.
	Response sub-option 13 from option 25 MUST contain statuscode 3.

	References: RFC 3633/3315

@v6 @dhcp6 @PD @rfc3633
    Scenario: prefix.delegation.release_dual_nobinding
 	Test Setup:
	Server is configured with 3000::/32 subnet with 3000::1-3000::2 pool.
	Server is configured with 3000:: prefix in subnet 0 with 32 prefix length and 33 delegated prefix length.
	DHCP server is started.
	
	Test Procedure:
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client copies IA_NA option from received message.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 13.
	Response sub-option 13 from option 25 MUST contain statuscode 3.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 13.
	Response sub-option 13 from option 3 MUST contain statuscode 3.
	
	References: RFC 3633/3315

@v6 @dhcp6 @PD @rfc3633
    Scenario: prefix.delegation.release_nobinding2

 	Test Setup:
	Server is configured with 3000::/32 subnet with 3000::1-3000::2 pool.
	Server is configured with 3000:: prefix in subnet 0 with 32 prefix length and 33 delegated prefix length.
	DHCP server is started.
	
	Test Procedure:
	Client does NOT include IA-NA.
	Client does include IA-PD.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.

	Test Procedure:
	Client does NOT include IA-NA.
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.

	Test Procedure:
	Client copies server-id option from received message.
	Client saves IA_PD option from received message.
	Client adds saved options. And DONT Erase.
	Client does NOT include IA-NA.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	#must not contain status code == 3.

	Test Procedure:
	Client copies server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client does NOT include IA-NA.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 13.
	Response sub-option 13 from option 25 MUST contain statuscode 3.

	References: RFC 3633/3315

@v6 @dhcp6 @PD @rfc3633
    Scenario: prefix.delegation.onlyPD-relay
  
 	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 92 delegated prefix length.
	DHCP server is started.
	
	Test Procedure:
	Client does NOT include IA-NA.
	Client does include IA-PD.
	Client sends SOLICIT message.

	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST respond with RELAYREPLY message.
	Response MUST include option 9. 
	#add test after Scapy fix
	
	References: RFC 3633, Section: 14

@v6 @dhcp6 @PD @rfc3633
    Scenario: prefix.delegation.assign_saved_iapd

    Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	#two prefixes - 3000::/91; 3000::20:0:0/91;
	Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 91 delegated prefix length.
	DHCP server is started.

	Test Procedure:
	Client does include IA-PD.
	Client does NOT include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client does NOT include IA-NA.
	#1st prefix
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.

	Test Procedure:
	Generate new IA_PD.
	Client does include IA-PD.
	Client does NOT include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.

	Test Procedure:
	Client copies server-id option from received message.
	Client saves IA_PD option from received message.
	Client does NOT include IA-NA.
	Client adds saved options. And DONT Erase.
	#2nd prefix
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	#both prefixes assigned.

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	Server is configured with 3000:: prefix in subnet 0 with 80 prefix length and 95 delegated prefix length.
	DHCP server is started.

    Test Procedure:
	Client adds saved options. And Erase.
	Client does NOT include IA-NA.
	Client sends SOLICIT message.

    Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.

    Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client does NOT include IA-NA.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	Response sub-option 26 from option 25 MUST contain prefix 3000::20:0:0.

    References: RFC 3633, Section: 11.2

@v6 @dhcp6 @PD @rfc3633
    Scenario: prefix.delegation.compare_prefixes_after_client_reboot

    Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::300 pool.
	Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 96 delegated prefix length.
	DHCP server is started.

	Test Procedure:
	Client does include IA-PD.
	Client does NOT include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client does NOT include IA-NA.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	# save prefix value
	Save prefix value from 26 option.

	Test Procedure:
	Client does include IA-PD.
	Client does NOT include IA-NA.
	# client reboot
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 25.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_PD option from received message.
	Client does NOT include IA-NA.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 25.
	Response option 25 MUST contain sub-option 26.
	# compare assigned prefix with the saved one
	Received prefix value in option 26 is the same as saved value.

    References: RFC 3633


@v6 @dhcp6 @PD
Scenario: prefix.delegation.just-PD-configured-PD-requested

    Test Setup:
    Server is configured with 3000::/64 subnet with $(EMPTY) pool.
    Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 96 delegated prefix length.
    DHCP server is started.

    Test Procedure:
    Client does NOT include IA-NA.
    Client does include IA-PD.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response MUST NOT include option 3.

    Test Procedure:
    Client copies server-id option from received message.
    Client copies IA_PD option from received message.
    Client does NOT include IA-NA.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response MUST NOT include option 3.


@v6 @dhcp6 @PD
Scenario: prefix.delegation.just-PD-configured-PD-and-IA-requested

    Test Setup:
    Server is configured with 3000::/64 subnet with $(EMPTY) pool.
    Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 96 delegated prefix length.
    DHCP server is started.

    Test Procedure:
    Client does include IA-PD.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 13.
    Response sub-option 13 from option 3 MUST contain statuscode 2.

    Test Procedure:
    Client copies server-id option from received message.
    Client copies IA_PD option from received message.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 13.
    Response sub-option 13 from option 3 MUST contain statuscode 2.

