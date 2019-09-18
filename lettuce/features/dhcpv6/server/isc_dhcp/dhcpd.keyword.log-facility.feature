Feature: ISC_DHCP DHCPv6 Keywords
    Tests ISC_DHCP dhcpd configuration keywords 
	
@v6 @dhcpd @keyword @log-facility
    Scenario: v6.dhcpd.keyword.log-facility.success
    ## Testing log-facility server option
    ##
    ## Verifies that log-facility option (there by forge default setup)
    ## succeeds in capturing dhcpd logging.
    ##
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::2 pool.
    Send server configuration using SSH and config-file.
	DHCP Server is started.

    # No steps required
	Test Procedure:

	Pass Criteria:
    DHCP log MUST contain line: dhcpd: Server starting service.

@v6 @dhcpd @keyword @log-facility
    Scenario: v6.dhcpd.keyword.log-facility.fail
    ## Testing log-facility server option
    ##
    ## Verifies that by setting log-facility to an invalid 
    ## value, causes dhcpd logging to not be directed to log file.
    ##
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::2 pool.
    Run configuration command: log-facility bogus; 
    Send server configuration using SSH and config-file.
    DHCP server failed to start. During configuration process.

    # No steps required
	Test Procedure:

	Pass Criteria:
    # @todo - pre-startup errors only go to syslog, we need to look at
    # console output captured by Forge.  Don't yet have a step in Forge
    # for looking at console output. 
    # DHCP log contains 1 of line: server.cfg_processed line 6: unknown value
