Feature: DHCPv6 Renew
    Those are tests for renew - reply exchange.

@v6 @dhcp6 @renew
    Scenario: v6.message.renew-reply
    ## Testing server ability to perform message exchange RENEW - REPLY 
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	## correct message 		  RENEW -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA with suboption IA-Address
	##					
 	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::5-3000::55 pool.
	Send server configuration using SSH and config-file.
DHCP server is started.
	
	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
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
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	References: RFC 3315, Section: 18.2.3.
	
@v6 @dhcp6 @renew
	Scenario: v6.message.renew-reply-different-clients-the-same-iaid
	## Two clients try to renew address, using the same IA_ID but different Client-ID

	Test Setup:
	Time renew-timer is configured with value 50.
	Time rebind-timer is configured with value 60.
	Time preferred-lifetime is configured with value 70.
	Time valid-lifetime is configured with value 80.
	Server is configured with 3000::/64 subnet with 3000::1-3000::2 pool.
	Send server configuration using SSH and config-file.
	DHCP server is started.

	Test Procedure:
	Client sets ia_id value to 666.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
	Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client sets ia_id value to 666.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client does include client-id.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client sets ia_id value to 666.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:22.
	Client does include client-id.
	Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client sets ia_id value to 666.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:22.
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client does include client-id.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	#client try to renew address that is not his
	Client sets ia_id value to 666.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client does include client-id.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
  	Response sub-option 5 from option 3 MUST contain validlft 0.
  	Response sub-option 5 from option 3 MUST contain address 3000::2.
	Response sub-option 5 from option 3 MUST contain validlft 80.
  	Response sub-option 5 from option 3 MUST contain address 3000::1.
	References: RFC 3315, Section: 18.2.3.


@v6 @dhcp6 @renew
	Scenario: v6.message.renew-reply-different-clients-the-same-iaid-2
	## Two clients try to renew address, using the same IA_ID but different Client-ID

	Test Setup:
	Time renew-timer is configured with value 50.
	Time rebind-timer is configured with value 60.
	Time preferred-lifetime is configured with value 70.
	Time valid-lifetime is configured with value 80.
	Server is configured with 3000::/64 subnet with 3000::1-3000::2 pool.
	Send server configuration using SSH and config-file.
	DHCP server is started.

	Test Procedure:
	Client sets ia_id value to 666.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
	Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client sets ia_id value to 666.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client does include client-id.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client sets ia_id value to 666.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:22.
	Client does include client-id.
	Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client sets ia_id value to 666.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:22.
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client does include client-id.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	#client try to renew address that is his
	Client sets ia_id value to 666.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:22.
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client does include client-id.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
  	#Response sub-option 5 from option 3 MUST contain validlft 0.
  	Response sub-option 5 from option 3 MUST contain address 3000::2.
	Response sub-option 5 from option 3 MUST contain validlft 80.
  	Response sub-option 5 from option 3 MUST NOT contain address 3000::1.
	References: RFC 3315, Section: 18.2.3.

	@v6 @dhcp6 @renew
	Scenario: v6.message.renew-reply-different-clients-the-same-iaid-expired
	## Two clients try to renew address, using the same IA_ID but different Client-ID

	Test Setup:
	Time renew-timer is configured with value 5.
  	Time rebind-timer is configured with value 6.
  	Time preferred-lifetime is configured with value 7.
  	Time valid-lifetime is configured with value 8.
	Server is configured with 3000::/64 subnet with 3000::1-3000::2 pool.
	Send server configuration using SSH and config-file.
	DHCP server is started.

	Test Procedure:
	Client sets ia_id value to 666.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
	Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client sets ia_id value to 666.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client does include client-id.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client sets ia_id value to 666.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:22.
	Client does include client-id.
	Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client sets ia_id value to 666.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:22.
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client does include client-id.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Sleep for 10 seconds.

	Test Procedure:

	Client sets ia_id value to 666.

	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client does include client-id.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	Response option 3 MUST contain sub-option 5.
  	Response sub-option 5 from option 3 MUST contain address 3000::2.
  	Response sub-option 5 from option 3 MUST contain address 3000::1.
	References: RFC 3315, Section: 18.2.3.

@v6 @dhcp6 @renew
	Scenario: v6.message.renew-reply-different-clients-the-same-iaid-expired-2
	## Two clients try to renew address, using the same IA_ID but different Client-ID

	Test Setup:
	Time renew-timer is configured with value 5.
	Time rebind-timer is configured with value 6.
	Time preferred-lifetime is configured with value 7.
	Time valid-lifetime is configured with value 8.
	Server is configured with 3000::/64 subnet with 3000::1-3000::2 pool.
	Send server configuration using SSH and config-file.
	DHCP server is started.

	Test Procedure:
	Client sets ia_id value to 666.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client does include client-id.
	Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client sets ia_id value to 666.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client does include client-id.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client sets ia_id value to 666.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:22.
	Client does include client-id.
	Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client sets ia_id value to 666.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:22.
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client does include client-id.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	Sleep for 10 seconds.

	Test Procedure:
	#client try to renew address that is his
	Client sets ia_id value to 666.
	Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:22.
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client does include client-id.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
  	#Response sub-option 5 from option 3 MUST contain validlft 0.
  	Response sub-option 5 from option 3 MUST contain address 3000::2.
	Response sub-option 5 from option 3 MUST contain validlft 8.
  	Response sub-option 5 from option 3 MUST NOT contain address 3000::1.
	References: RFC 3315, Section: 18.2.3.

	@v6 @dhcp6 @renew
    Scenario: v6.message.renew-reply-time-zero
    ## Testing server ability to perform message exchange RENEW - REPLY
    ## In case when we expect that address is not appropriate for the link. 
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## Save IA_NA with IA_Addr		<--	REPLY
	## 					Reconfigure Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## Create leases		REQUEST -->
	## for the same client			<--	REPLY
	## Use saved IA_NA 		  RENEW -->
	## (proper client ID, IA_NA, but wrong address)
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA-NA with suboption IA-Address with validlft set to 0.
  	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::66-3000::66 pool.
	Send server configuration using SSH and config-file.
DHCP server is started.
	
	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Client saves IA_NA option from received message.

    Server reconfigure:
	Server is configured with 3000::/64 subnet with 3000::100-3000::155 pool.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client copies server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client does include client-id.
    Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	Response sub-option 5 from option 3 MUST contain address 3000::66.
	Response sub-option 5 from option 3 MUST contain validlft 0.

	References: RFC 3315, Section: 18.2.3.