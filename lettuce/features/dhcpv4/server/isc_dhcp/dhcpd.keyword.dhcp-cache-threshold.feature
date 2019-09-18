## These tests verify the dhcp-cache-threshold keyword. 
Feature: ISC_DHCP DHCPv4 Keywords
    Tests ISC_DHCP dhcpd configuration keywords 
	
@v4 @dhcpd @keyword @dhcp-cache-threshold
    Scenario: v4.dhcpd.keyword.dhcp-cache-threshold.default_on.dora
    ## Verifies that by default the threshold is set to 25%, and
    ## renewing via DORA works correctly. 
    ##
    ## Case 1:
    ## Client gets initial lease
    ##
    ## Case 2:
    ## Client renews lease with DORA before threshold is reached
    ## - Server should reuse the original lease.
    ## 
    ## Case 3:
    ## Client renews lease with DORA after threshold is reached
    ## - Server should extend the lease
    ##
	Test Setup:
    Run configuration command:  ping-check off;
    Run configuration command:  ddns-updates off;
    Run configuration command:  max-lease-time 90;
    Run configuration command:  default-lease-time 90;
    Run configuration command:  subnet 192.168.50.0 netmask 255.255.255.0 {
    Run configuration command:      authoritative;
    Run configuration command:      pool {
    Run configuration command:          range 192.168.50.100 192.168.50.101;
    Run configuration command:      }
    Run configuration command:  }
  Send server configuration using SSH and config-file.
	DHCP Server is started.

    ###################################################################
    # Case 1: Get the initial lease
    ###################################################################
	Test Procedure:
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.100.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.100.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.100. 
    Response MUST include option 51.
    Response option 51 MUST contain value 90. 
    DHCP log contains 0 of line: under 25% threshold

    ###################################################################
    # Case 2: Renew with DORA before threshold expires
    ###################################################################
	Test Procedure:
    Sleep for 1 seconds.
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.100.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.100.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.100. 
    Response MUST include option 51.
    # When forge supports comparison change this to less than 90
    Response option 51 MUST NOT contain value 90. 
    DHCP log contains 2 of line: under 25% threshold

    ###################################################################
    # Case 3: Renew with DORA after threshold expires
    ###################################################################
	Test Procedure:
    Sleep for 25 seconds. 
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.100.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.100.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.100. 
    Response MUST include option 51.
    Response option 51 MUST contain value 90. 
    DHCP log contains 2 of line: under 25% threshold

@v4 @dhcpd @keyword @dhcp-cache-threshold
    Scenario: v4.dhcpd.keyword.dhcp-cache-threshold.default.ra
    ## Verifies that by default the threshold is set to 25% and. 
    ## client renewing using RAs works correctly.
    ##
    ## Case 1:
    ## Client gets initial lease
    ##
    ## Case 2:
    ## Client renews lease with RA before threshold is reached
    ## - Server should reuse the original lease.
    ## 
    ## Case 3:
    ## Client renews lease with RA after threshold is reached
    ## - Server should extend the lease
    ##
	Test Setup:
    Run configuration command:  ping-check off;
    Run configuration command:  ddns-updates off;
    Run configuration command:  max-lease-time 90;
    Run configuration command:  default-lease-time 90;
    Run configuration command:  subnet 192.168.50.0 netmask 255.255.255.0 {
    Run configuration command:      authoritative;
    Run configuration command:      pool {
    Run configuration command:          range 192.168.50.100 192.168.50.101;
    Run configuration command:      }
    Run configuration command:  }
  Send server configuration using SSH and config-file.
	DHCP Server is started.

    ###################################################################
    # Case 1: Get the initial lease
    ###################################################################
	Test Procedure:
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.100.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.100.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.100. 
    Response MUST include option 51.
    Response option 51 MUST contain value 90. 
    DHCP log contains 0 of line: under 25% threshold 

    ###################################################################
    # Case 2: Renew with RA before threshold expires
    ###################################################################
    Test Procedure:
    Sleep for 1 seconds.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.100.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.100. 
    Response MUST include option 51.
    # When forge supports comparison change this to less than 90
    Response option 51 MUST NOT contain value 90. 
    DHCP log contains 1 of line: under 25% threshold

    ###################################################################
    # Case 3: Renew with RA after threshold expires
    ###################################################################
    Test Procedure:
    Sleep for 25 seconds. 
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.100.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.100. 
    Response MUST include option 51.
    Response option 51 MUST contain value 90. 
    DHCP log contains 1 of line: under 25% threshold

@v4 @dhcpd @keyword @dhcp-cache-threshold
    Scenario: v4.dhcpd.keyword.dhcp-cache-threshold.off
    ##
    ## Case 1:
    ## Client gets initial lease
    ##
    ## Case 2:
    ## Client renews lease with DORA before the default threshold has passed
    ## - Server should extend the lease.
    ## 
    ## Case 3:
    ## Client renews lease with DORA after the default threshold has passed 
    ## - Server should extend the lease
    ##
	Test Setup:
    Run configuration command:  ping-check off;
    Run configuration command:  ddns-updates off;
    Run configuration command:  max-lease-time 90;
    Run configuration command:  default-lease-time 90;
    Run configuration command:  subnet 192.168.50.0 netmask 255.255.255.0 {
    Run configuration command:      authoritative;
    Run configuration command:      pool {
    Run configuration command:          range 192.168.50.100 192.168.50.101;
    Run configuration command:      }
    Run configuration command:  }
    Run configuration command:  dhcp-cache-threshold 0;
  Send server configuration using SSH and config-file.
	DHCP Server is started.

    ###################################################################
    # Case 1: Get the initial lease
    ###################################################################
	Test Procedure:
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.100.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.100.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.100. 
    Response MUST include option 51.
    Response option 51 MUST contain value 90. 
    DHCP log contains 0 of line: under 25% threshold

    ###################################################################
    # Case 2: Renew with DORA before default threshold expires
    ###################################################################
	Test Procedure:
    Sleep for 1 seconds.
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.100.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.100.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.100. 
    Response MUST include option 51.
    Response option 51 MUST contain value 90. 
    DHCP log contains 0 of line: under 25% threshold

    ###################################################################
    # Case 3: Renew with DORA after default threshold expires
    ###################################################################
	Test Procedure:
    Sleep for 25 seconds. 
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.100.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.100.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.100. 
    Response MUST include option 51.
    Response option 51 MUST contain value 90. 
    DHCP log contains 0 of line: under 25% threshold

@v4 @dhcpd @keyword @dhcp-cache-threshold
    Scenario: v4.dhcpd.keyword.dhcp-cache-threshold.config_on
    ## Verifies that the threshold can set to a custom value and
    ## that renewing works correctly. 
    ##
    ## Case 1:
    ## Client gets initial lease
    ##
    ## Case 2:
    ## Client renews lease with DORA before threshold is reached
    ## - Server should reuse the original lease.
    ##
    ## Case 3:
    ## Client renews lease with RA before threshold is reached
    ## - Server should reuse the original lease.
    ## 
    ## Case 4:
    ## Client renews lease with DORA after threshold is reached
    ## - Server should extend the lease
    ##
	Test Setup:
    Run configuration command:  ping-check off;
    Run configuration command:  ddns-updates off;
    Run configuration command:  max-lease-time 50;
    Run configuration command:  default-lease-time 50;
    Run configuration command:  subnet 192.168.50.0 netmask 255.255.255.0 {
    Run configuration command:      authoritative;
    Run configuration command:      pool {
    Run configuration command:          range 192.168.50.100 192.168.50.101;
    Run configuration command:      }
    Run configuration command:  }
    Run configuration command:  dhcp-cache-threshold 20;
  Send server configuration using SSH and config-file.
	DHCP Server is started.

    ###################################################################
    # Case 1: Get the initial lease
    ###################################################################
	Test Procedure:
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.100.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.100.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.100. 
    Response MUST include option 51.
    Response option 51 MUST contain value 50. 
    DHCP log contains 0 of line: under 20% threshold 

    ###################################################################
    # Case 2: Renew with DORA before threshold expires
    ###################################################################
	Test Procedure:
    Sleep for 1 seconds.
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.100.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.100.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.100. 
    Response MUST include option 51.
    # When forge supports comparison change this to less than 50
    Response option 51 MUST NOT contain value 50. 
    DHCP log contains 2 of line: under 20% threshold

    ###################################################################
    # Case 3: Renew with RA before threshold expires
    ###################################################################
    Test Procedure:
    Sleep for 1 seconds.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.100.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.100. 
    Response MUST include option 51.
    # When forge supports comparison change this to less than 50
    Response option 51 MUST NOT contain value 50. 
    DHCP log contains 3 of line: under 20% threshold


    ###################################################################
    # Case 3: Renew with DORA after threshold expires
    ###################################################################
	Test Procedure:
    Sleep for 20 seconds. 
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.100.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.100.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.100. 
    Response MUST include option 51.
    Response option 51 MUST contain value 50. 
    DHCP log contains 3 of line: under 20% threshold

