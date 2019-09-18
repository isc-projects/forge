#
Feature: ISC_DHCP DHCPv6 Keywords
    Tests ISC_DHCP dhcpd configuration keywords 
	
@v6 @dhcpd @keyword @log-threshold
    Scenario: v6.dhcpd.keyword.log-threshold-none
    ##
    ## Testing: That log messages for crossing the high and 
    ## low thresholds do not appear if log-threshold values
    ## are not set.
    ##
    ## Stage 1: Consume all leases from the pool and verify that the 
    ## high threshold message is not logged
    ##
    ## Stage 2: Release all leases
    ## 
    ## Stage 3: request a lease, and verify that the low threshold log message
    ## does not appear.
    ##
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::4 pool.
    Send server configuration using SSH and config-file.
	DHCP Server is started.

    ##
    ## Stage 1: Consume all leases 
    ##

    # Grab first lease. Expect no threshold logs.
	Test Procedure: 01
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	
	Test Procedure: 02
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    # save lease info for release
    Client saves into set no. 1 IA_NA option from received message.
	Client saves into set no. 1 client-id option from received message.
	Client saves into set no. 1 server-id option from received message.
    DHCP log MUST NOT contain line: Pool threshold

    # Grab second lease. Expect no threshold logs.
	Test Procedure: 03
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:02.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	
	Test Procedure: 04
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    # save lease info for release
    Client saves into set no. 2 IA_NA option from received message.
	Client saves into set no. 2 client-id option from received message.
	Client saves into set no. 2 server-id option from received message.
    DHCP log MUST NOT contain line: Pool threshold

    # Grab third lease. Expect no threshold logs.
	Test Procedure: 05
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:03.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	
	Test Procedure: 06
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    # save lease info for release
    Client saves into set no. 3 IA_NA option from received message.
	Client saves into set no. 3 client-id option from received message.
	Client saves into set no. 3 server-id option from received message.
    DHCP log MUST NOT contain line: Pool threshold

    # Grab fourth lease. Expect no threshold logs.
	Test Procedure: 07
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:04.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	
	Test Procedure: 08
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    # save lease info for release
    Client saves into set no. 4 IA_NA option from received message.
	Client saves into set no. 4 client-id option from received message.
	Client saves into set no. 4 server-id option from received message.
    DHCP log MUST NOT contain line: Pool threshold

    ##
    ## Stage 2: Release leases until we cross low threshold.
    ##

    # Release the first lease, should not see low threshold log.
	Test Procedure: 09
    Client adds saved options in set no. 1. And Erase.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain status-code 0. 
    DHCP log MUST NOT contain line: Pool threshold reset

    # Release the second lease, should not see low threshold log.
	Test Procedure: 10
    Client adds saved options in set no. 2. And Erase.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain status-code 0. 
    DHCP log MUST NOT contain line: Pool threshold reset

    # Release third lease, should not see low threshold log.
	Test Procedure: 11
    Client adds saved options in set no. 3. And Erase.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain status-code 0. 
    DHCP log MUST NOT contain line: Pool threshold reset

    # Release fourth lease, should not see low threshold log.
	Test Procedure: 12
    Client adds saved options in set no. 4. And Erase.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain status-code 0. 
    DHCP log MUST NOT contain line: Pool threshold reset

    ##
    ## Stage 3: Grab a lease, should not see threshold reset log.
    ##

	Test Procedure: 13
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	
	Test Procedure: 14
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    DHCP log MUST NOT contain line: Pool threshold reset

@v6 @dhcpd @keyword @log-threshold
    Scenario: v6.dhcpd.keyword.log-threshold-high-gt-low
    ##
    ## Testing: That log messages for crossing the high and low 
    ## thresholds are output at the correct times when both
    ## high and low are set, and high threshold is larger than low 
    ## threshold.
    ##
    ## Stage 1: consume enough leases from the pool to verify the
    ## that the high threshold message is logged
    ##
    ## Stage 2: release enough leases to fall under the low threshold.
    ##
    ## Stage 3: request a lease, and verify the low threshold log
    ## message appears. (thresholds are testing only during allocation
    ## not release... asinine but true).
    ## 
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::4 pool.
    Run configuration command: log-threshold-low 30;
    Run configuration command: log-threshold-high 60;
    Send server configuration using SSH and config-file.
	DHCP Server is started.

    ##
    ## Stage 1: Consume leases until we exceed high threshold
    ##

    # Grab first lease. Expect no threshold logs.
	Test Procedure: 15
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	
	Test Procedure: 16
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    # save lease info for release
    Client saves into set no. 1 IA_NA option from received message.
    Client saves into set no. 1 client-id option from received message.
	Client saves into set no. 1 server-id option from received message.
    DHCP log MUST NOT contain line: Pool threshold

    # Grab second lease. Expect threshold high log.
	Test Procedure: 17
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:02.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	
	Test Procedure: 18
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    # save lease info for release
    Client saves into set no. 2 IA_NA option from received message.
    Client saves into set no. 2 client-id option from received message.
	Client saves into set no. 2 server-id option from received message.
    DHCP log contains 1 of line: Pool threshold exceeded

    # Grab third lease. Expect only 1 threshold high log.
	Test Procedure: 19
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:03.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	
	Test Procedure: 20
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    # save lease info for release
    Client saves into set no. 3 IA_NA option from received message.
    Client saves into set no. 3 client-id option from received message.
	Client saves into set no. 3 server-id option from received message.
    DHCP log contains 1 of line: Pool threshold exceeded

    ##
    ## Stage 2: Release leases until we cross low threshold.
    ##

    # Release the first lease, should not see low threshold log.
	Test Procedure: 21
    Client adds saved options in set no. 1. And Erase.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain status-code 0. 
    DHCP log MUST NOT contain line: Pool threshold reset

    # Release the second lease, should not see low threshold log.
	Test Procedure: 22
    Client adds saved options in set no. 2. And Erase.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain status-code 0. 
    DHCP log MUST NOT contain line: Pool threshold reset

    # Release third lease, should not see low threshold log.
	Test Procedure: 23
    Client adds saved options in set no. 3. And Erase.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain status-code 0. 
    DHCP log MUST NOT contain line: Pool threshold reset

    ##
    ## Stage 3: Grab a lease, should see threshold reset log.
    ##

	Test Procedure: 24
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	
	Test Procedure: 25
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    DHCP log contains 1 of line: Pool threshold reset

@v6 @dhcpd @keyword @log-threshold
    Scenario: v6.dhcpd.keyword.log-threshold-low-gt-high
    ##
    ## Testing: When low threshold is greater than high threshold
    ## the high threshold log should be output on each grant once exceeded.
    ## and low threshold crossing never logs.
    ##
    ## Stage 1: consume enough leases from the pool to verify
    ## that the high threshold message is logged. Verify the high
    ## threshold message repeats.
    ##
    ## Stage 2: release all the leases
    ##
    ## Stage 3: request a lease, and verify that no new threshold logs
    ## are output.
    ## 
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::4 pool.
    Run configuration command: log-threshold-low 65;
    Run configuration command: log-threshold-high 60;
    Send server configuration using SSH and config-file.
	DHCP Server is started.

    ##
    ## Stage 1: Consume leases until we exceed high threshold
    ##

    # Grab first lease. Expect no threshold logs.
	Test Procedure: 26
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	
	Test Procedure: 27
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    # save lease info for release
    Client saves into set no. 1 IA_NA option from received message.
	Client saves into set no. 1 client-id option from received message.
	Client saves into set no. 1 server-id option from received message.
    DHCP log contains 0 of line: Pool threshold exceeded

    # Grab second lease. Expect threshold high log.
	Test Procedure: 28
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:02.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	
	Test Procedure: 29
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    # save lease info for release
    Client saves into set no. 2 IA_NA option from received message.
	Client saves into set no. 2 client-id option from received message.
	Client saves into set no. 2 server-id option from received message.
    DHCP log contains 1 of line: Pool threshold exceeded

    # Grab third lease. Expect another threshold high log.
	Test Procedure: 30
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:03.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	
	Test Procedure: 31
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    # save lease info for release
    Client saves into set no. 3 IA_NA option from received message.
	Client saves into set no. 3 client-id option from received message.
	Client saves into set no. 3 server-id option from received message.
    DHCP log contains 2 of line: Pool threshold exceeded

    ##
    ## Stage 2: Release leases until we cross low threshold.
    ##

    # Release the first lease, should not see low threshold log.
	Test Procedure: 32
    Client adds saved options in set no. 1. And Erase.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain status-code 0. 
    DHCP log MUST NOT contain line: Pool threshold reset

    # Release the second lease, should not see low threshold log.
	Test Procedure: 33
    Client adds saved options in set no. 2. And Erase.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain status-code 0. 
    DHCP log MUST NOT contain line: Pool threshold reset

    # Release third lease, should not see low threshold log.
	Test Procedure: 34
    Client adds saved options in set no. 3. And Erase.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain status-code 0. 
    DHCP log MUST NOT contain line: Pool threshold reset

    ##
    ## Stage 3: Grab a lease, should not see threshold reset log.
    ##

	Test Procedure: 35
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	
	Test Procedure: 36
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    # make sure we added no new threshold logs
    DHCP log contains 2 of line: Pool threshold exceeded
    DHCP log contains 0 of line: Pool threshold reset

@v6 @dhcpd @keyword @log-threshold
    Scenario: v6.dhcpd.keyword.log-threshold-high-only
    ##
    ## Testing: When only the high threshold is specified
    ## than the threshold exceeded log only occurs once each
    ## time it is exceeded.  In other words, once exceeded it
    ## does not repeat with each grant.  Since low threshold
    ## defaults to 0, that log should never appear.
    ##
    ## Stage 1: consume enough leases from the pool to verify the
    ## that the high threshold message is logged. Verify the high
    ## threshold message does not repeat.
    ##
    ## Stage 2: release all the leases
    ##
    ## Stage 3: request a lease, and verify that no new threshold logs
    ## are output.
    ## 

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::4 pool.
    Run configuration command: log-threshold-high 60;
    Send server configuration using SSH and config-file.
	DHCP Server is started.

    ##
    ## Stage 1: Consume leases until we exceed high threshold
    ##

    # Grab first lease. Expect no threshold logs.
	Test Procedure: 36
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	
	Test Procedure: 38
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    # save lease info for release
    Client saves into set no. 1 IA_NA option from received message.
    Client saves into set no. 1 client-id option from received message.
	Client saves into set no. 1 server-id option from received message.
    DHCP log contains 0 of line: Pool threshold exceeded

    # Grab second lease. Expect threshold high log.
	Test Procedure: 39
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:02.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	
	Test Procedure: 40
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    # save lease info for release
    Client saves into set no. 2 IA_NA option from received message.
    Client saves into set no. 2 client-id option from received message.
	Client saves into set no. 2 server-id option from received message.
    DHCP log contains 1 of line: Pool threshold exceeded

    # Grab third lease. Expect only 1 threshold high log.
	Test Procedure: 41
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:03.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	
	Test Procedure: 42
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    # save lease info for release
    Client saves into set no. 3 IA_NA option from received message.
    Client saves into set no. 3 client-id option from received message.
	Client saves into set no. 3 server-id option from received message.
    DHCP log contains 1 of line: Pool threshold exceeded

    ##
    ## Stage 2: Release leases until we cross low threshold.
    ##

    # Release the first lease, should not see low threshold log.
	Test Procedure: 43
    Client adds saved options in set no. 1. And Erase.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain status-code 0. 
    DHCP log contains 0 of line: Pool threshold reset

    # Release the second lease, should not see low threshold log.
	Test Procedure: 44
    Client adds saved options in set no. 2. And Erase.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain status-code 0. 
    DHCP log contains 0 of line: Pool threshold reset

    # Release third lease, should not see low threshold log.
	Test Procedure: 45
    Client adds saved options in set no. 3. And Erase.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain status-code 0. 
    DHCP log contains 0 of line: Pool threshold reset

    ##
    ## Stage 3: Grab a lease, should see threshold reset log.
    ##

	Test Procedure: 46
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	
	Test Procedure: 47
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    DHCP log contains 1 of line: Pool threshold exceeded
    DHCP log contains 0 of line: Pool threshold reset

@v6 @dhcpd @keyword @toms
    Scenario: v6.dhcpd.keyword.log-threshold-low-only
    ##
    ## Testing: That log messages for crossing the high and 
    ## low thresholds do not appear if only log-threshold-low
    ## value is set.
    ##
    ## Stage 1: Consume all leases from the pool and verify that the 
    ## high threshold message is not logged
    ##
    ## Stage 2: Release all leases
    ## 
    ## Stage 3: request a lease, and verify that the low threshold log does not
    ## message appear.
    ##
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::4 pool.
    Run configuration command: log-threshold-low 30;
    Send server configuration using SSH and config-file.
	DHCP Server is started.

    ##
    ## Stage 1: Consume leases
    ##

    # Grab first lease. Expect no threshold logs.
	Test Procedure: 48
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	
	Test Procedure: 49
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    # save lease info for release
    Client saves into set no. 1 IA_NA option from received message.
    Client saves into set no. 1 client-id option from received message.
	Client saves into set no. 1 server-id option from received message.
    DHCP log contains 0 of line: Pool threshold exceeded

    # Grab second lease. Expect no threshold log.
	Test Procedure: 50
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:02.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	
	Test Procedure: 51
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    # save lease info for release
    Client saves into set no. 2 IA_NA option from received message.
    Client saves into set no. 2 client-id option from received message.
	Client saves into set no. 2 server-id option from received message.
    DHCP log contains 0 of line: Pool threshold exceeded

    # Grab third lease. Expect no threshold high log.
	Test Procedure: 52
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:03.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	
	Test Procedure: 53
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    # save lease info for release
    Client saves into set no. 3 IA_NA option from received message.
    Client saves into set no. 3 client-id option from received message.
	Client saves into set no. 3 server-id option from received message.
    DHCP log contains 0 of line: Pool threshold exceeded

    # Grab fourth lease. Expect no threshold logs.
	Test Procedure: 54
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:04.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	
	Test Procedure: 55
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    # save lease info for release
    Client saves into set no. 4 IA_NA option from received message.
    Client saves into set no. 4 client-id option from received message.
	Client saves into set no. 4 server-id option from received message.
    DHCP log contains 0 of line: Pool threshold exceeded

    ##
    ## Stage 2: Release leases until we cross low threshold.
    ##

    # Release the first lease, should not see low threshold log.
	Test Procedure: 56
    Client adds saved options in set no. 1. And Erase.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain status-code 0. 
    DHCP log contains 0 of line: Pool threshold reset

    # Release the second lease, should not see low threshold log.
	Test Procedure: 57
    Client adds saved options in set no. 2. And Erase.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain status-code 0. 
    DHCP log contains 0 of line: Pool threshold reset

    # Release third lease, should not see low threshold log.
	Test Procedure: 58
    Client adds saved options in set no. 3. And Erase.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain status-code 0. 
    DHCP log contains 0 of line: Pool threshold reset

    # Release fourth lease, should not see low threshold log.
	Test Procedure: 59
    Client adds saved options in set no. 4. And Erase.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 13.
	Response option 13 MUST contain status-code 0. 
    DHCP log contains 0 of line: Pool threshold reset

    ##
    ## Stage 3: Grab a lease, should not see threshold reset log.
    ##

	Test Procedure: 60
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	
	Test Procedure: 61
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    DHCP log contains 0 of line: Pool threshold exceeded
    DHCP log contains 0 of line: Pool threshold reset

@v6 @dhcpd @keyword @log-threshold
    Scenario: v6.dhcpd.keyword.log-threshold-too-large
    ##
    ## Checks that the server emits a log message stating that log-threshold
    ## is disabled for a shared-network when the total number of addresses in 
    ## a given pond is too large to track.  For obvious reasons, we do not
    ## attempt to test that threshold logic is actually skipped.
    ##
	Test Setup:
    Run configuration command:  shared-network net1 {
    Run configuration command:  subnet6 3000::/16 {
    Run configuration command:   range6 3000:1::0/63;
    Run configuration command:   range6 3000:D::0/66;
    Run configuration command:   range6 3000:E::0/66;
    Run configuration command:  }
    Send server configuration using SSH and config-file.
	DHCP Server is started.

	Pass Criteria:
    DHCP log contains 1 of line: Threshold logging disabled for shared subnet of ranges: 3000:1::/63, 3000:d::/66, 3000:e::/66
