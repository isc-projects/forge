
Feature: temporary 
    My tests
@v6
	Scenario: cliclass
	Test Setup:
	Pause the test.
	Server is configured with 3000::/32 subnet with 3000::1-3000::2 pool.
	Run configuration command: config set Dhcp6/subnet6[0]/client-class "6666"
	#On space vendor-4491 server is configured with tftp-servers option with value 2001:558::76.
	Server is started.

	Client sets enterprisenum value to 6666.
	Client does include vendor-class.
	#Client adds suboption for vendor specific information with code: 1 and data: 32.
	#Client does include vendor-specific-info.
	
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	#Response MUST include option 17.
	#Response option 17 MUST contain sub-option 32.
	
	References: RFC3315 section 22.17
    
    
    
    
@v6
    Scenario: teraz
	## Testing server ability server ability perform RELEASE - REPLY message exchange.
	## Try to release non-existing leases.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						RELEASE -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA_NA with suboption status-code with code NoBinding
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 13. 
	Response sub-option 13 from option 3 MUST contain statuscode 3.
	
	References: RFC3315 section 18.2.6.	
@v6
    Scenario: teraz2
    Test Setup:

	## Server MUST discard any Solicit it receives with   
	## a unicast address destination
	## Message details 		Client		Server
	## GLOBAL_UNICAST dest  SOLICIT -->
	## 		   						 X	ADVERTISE
	## correct message		SOLICIT -->
	## 		   						<--	ADVERTISE	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::55-3000::55 pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	
	
	
	
	
	
	
    Scenario: b
    Test Setup:
	Server is configured with 3000::/64 subnet with 3000::2-3000::2 pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client copies server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Generate new IA.
	Client copies server-id option from received message.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Generate new client.
	Client copies server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.


    Scenario: bb
    Test Setup:
	Server is configured with 3000::/64 subnet with 3000::2-3000::2 pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client copies server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Generate new client.
	Client copies server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	
	
    Scenario: bszd
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
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Client sends CONFIRM message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 13.
	Response option 13 MUST contain status-code 0. 
	
	

    Scenario: a 
    #User define temporary variable: XX_1 with value 3:333.
    Test Setup:
	Server is configured with 3000::/64 subnet with 3000::2-3000::2 pool.
	Server is started.
    Test Setup:
	Server is configured with 3000::/64 subnet with 3000::2-3000::2 pool.
	Server is started.
    Test Setup:
	Server is configured with 3000::/64 subnet with 3000::2-3000::2 pool.
	Server is started.


	Scenario: test
    Test Setup:
    Client removes file from server located in: efsdfsd$(DIBBLER_INSTALL_DIR)asdasd/asdas.
    User define temporary variable: XX with value 3:333.
    Server is configured with $(XX) subnet with 3000::2-3000::2 pool.
    User define temporary variable: ASDASD with value 3:333.
	Run configuration command: uaihsd asdjh asdiojasd $(ASDASD) asdoij
    #If you want to set up variable just for one scenario:
    User define temporary variable: VALUE_NAME with value 3333.
    #If you want to add value to init_all.py:
    User define permanent variable: VALUE_NAME with value 432:4.
    
    #To use those and other values stored in init_all.py:
    Server is configured with $(VALUE_NAME) subnet with 3000::2-3000::2 pool.
    #or 
    Server is configured with $(VALUE_NAME)anything_withou_whitespaces subnet with 3000::2-3000::2 pool.
    
    #in last case you will 
    
    Server is configured with $(SDEG_____EDAA234JWE)ghfe subnet with 3000::2-3000::2 pool.
    #Client compares downloaded file from server with local file stored in: $SERVER_INSTALL_DIRasdasds.
    #Server is configured with $(SERVER_INSTALL_DIR)asdasd subnet with 3000::2-3000::2 pool.
    
    Client removes file from server located in: $(SERVER_INSTALL_DIR)/tmp/user_chk_outcome.txt.
    
    Server is started.
    #Client download file from server stored in: $SERVER_INSTALL_DIR2ugabuga.
    




	Scenario: test2
    Test Setup:
    Server is configured with 3000::/64 subnet with 3000::2-3000::2 pool.

    Server is started.
    Bring user a beer.
    Test Procedure:
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::2.




	    Scenario: toms
 	#Client download file from server stored in: /root/ugabuga
	#Client removes file from server located in: 
	
	Client sends local file stored in: ../../aaa to server, to location: /root/ugabuga

	
	
	Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
	Server is configured with information-refresh-time option with value 12345678.
	Server is configured with sntp-servers option with value 2001:db8::abc,3000::1,2000::1234.
	Server is configured with nisp-domain-name option with value ntp.example.com.
	Server is configured with nis-domain-name option with value ntp.example.com.
	Server is configured with nisp-servers option with value 2001:db8::abc,3000::1,2000::1234.
	Server is configured with nis-servers option with value 2001:db8::abc,3000::1,2000::1234.
	Server is configured with domain-search option with value domain1.example.com,domain2.isc.org.
	Server is configured with sip-server-addr option with value 2001:db8::1,2001:db8::2.
	Server is configured with sip-server-dns option with value srv1.example.com,srv2.isc.org.
	Server is configured with preference option with value 123.
	On space vendor-4491 server is configured with tftp-servers option with value 2001:558:ff18:16:10:253:175:76.
	On space vendor-4491 server is configured with config-file option with value normal_erouter_v6.cm.
	On space vendor-4491 server is configured with syslog-servers option with value 2001:558:ff18:10:10:253:124:101.
	On space vendor-4491 server is configured with time-servers option with value 2001:558:ff18:16:10:253:175:76.
	On space vendor-4491 server is configured with time-offset option with value -18000.
	
        Test Setup:
        Server is configured with 3000::/64 subnet with 3000::2-3000::2 pool.
        Run configuration command: config add Dhcp6/subnet6
        Run configuration command: config set Dhcp6/subnet6[1]/subnet "1000::/64"
        Run configuration command: config set Dhcp6/subnet6[1]/pool [ "1000::2-1000::2" ]
        Server is started.
        
        Test Procedure:
        Client sends SOLICIT message.

        Pass Criteria:
        Server MUST respond with ADVERTISE message.
        Response MUST include option 3.
        Response option 3 MUST contain sub-option 5.
        Response sub-option 5 from option 3 MUST contain address 1000::2.