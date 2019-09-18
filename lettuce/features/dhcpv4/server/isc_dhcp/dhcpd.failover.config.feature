Feature: ISC_DHCP DHCPv4 Failover Configuration
    Tests ISC_DHCP dhcpd v4 failover configuration
	
@v4 @dhcpd @failover @sanity_check
    Scenario: v4.dhcpd.failover.sanity_check.good_config
    ##
    ## Verifies that failover config for two peers passes
    ## sanity checking
    ##
	Test Setup:
    Run configuration command:  failover peer "fonet" {
    Run configuration command:      primary;
    Run configuration command:      address 175.16.1.30;
    Run configuration command:      port 519;
    Run configuration command:      peer address 175.16.1.30;
    Run configuration command:      peer port 520;
    Run configuration command:      mclt 30;
    Run configuration command:      split 128;
    Run configuration command:      load balance max seconds 2;
    Run configuration command:  }
    Run configuration command:  failover peer "beebonet" {
    Run configuration command:      primary;
    Run configuration command:      address 175.16.1.30;
    Run configuration command:      port 521;
    Run configuration command:      peer address 175.16.1.30;
    Run configuration command:      peer port 522;
    Run configuration command:      mclt 30;
    Run configuration command:      split 128;
    Run configuration command:      load balance max seconds 2;
    Run configuration command:  }
    Run configuration command:  subnet 192.168.50.0 netmask 255.255.255.0 {
    Run configuration command:      pool {
    Run configuration command:        failover peer "fonet";
    Run configuration command:        range 192.168.50.50 192.168.50.50;
    Run configuration command:      }
    Run configuration command:      pool {
    Run configuration command:        failover peer "beebonet";
    Run configuration command:        range 192.168.50.150 192.168.50.200;
    Run configuration command:      }
    Run configuration command:  }
    Send server configuration using SSH and config-file.
	DHCP Server is started.

    # No steps required
	Test Procedure:

	Pass Criteria:
    DHCP log MUST contain line: failover peer fonet: I move from recover to startup 
    DHCP log MUST contain line: failover peer beebonet: I move from recover to startup 


@v4 @dhcpd @failover @sanity_check
    Scenario: v4.dhcpd.failover.sanity_check.no_pools
    ##
    ## Verifies that failover sanity checking detects when 
    ## peers are not referenced in pools.
    ##
	Test Setup:
    Run configuration command:  failover peer "fonet" {
    Run configuration command:      primary;
    Run configuration command:      address 175.16.1.30;
    Run configuration command:      port 519;
    Run configuration command:      peer address 175.16.1.30;
    Run configuration command:      peer port 520;
    Run configuration command:      mclt 30;
    Run configuration command:      split 128;
    Run configuration command:      load balance max seconds 2;
    Run configuration command:  }
    Run configuration command:  failover peer "beebonet" {
    Run configuration command:      primary;
    Run configuration command:      address 175.16.1.30;
    Run configuration command:      port 521;
    Run configuration command:      peer address 175.16.1.30;
    Run configuration command:      peer port 522;
    Run configuration command:      mclt 30;
    Run configuration command:      split 128;
    Run configuration command:      load balance max seconds 2;
    Run configuration command:  }
    Run configuration command:  subnet 192.168.50.0 netmask 255.255.255.0 {
    Run configuration command:      pool {
    Run configuration command:        range 192.168.50.50 192.168.50.50;
    Run configuration command:      }
    Run configuration command:      pool {
    Run configuration command:        range 192.168.50.150 192.168.50.200;
    Run configuration command:      }
    Run configuration command:  }
    Send server configuration using SSH and config-file.
    DHCP server failed to start. During configuration process.

	Test Procedure:
    # No steps required

	Pass Criteria:
    # @todo Forge does not yet support searching console output.  Pre-startup
    # errors like these occur before logging is initted, so the console is the
    # only place to see them.
    # DHCP console MUST contain line: ERROR: Failover peer, fobonet, has no referring pools 
    # DHCP console MUST contain line: ERROR: Failover peer, beebonet, has no referring pools 
