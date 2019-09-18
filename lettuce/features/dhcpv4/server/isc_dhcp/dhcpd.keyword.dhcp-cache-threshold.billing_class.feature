## These tests verify the dhcp-cache-threshold keyword in conjunction with
## billing classes 
Feature: ISC_DHCP DHCPv4 Keywords
    Tests ISC_DHCP dhcpd configuration keywords 

@v4 @dhcpd @keyword @dhcp-cache-threshold
    Scenario: v4.dhcpd.keyword.dhcp-cache-threshold.billing_class
    ## Verifies that cache-threshold logic takes billing class
    ## into account. In short, if the billing class associated with a 
    ## lease changes it must be superseded, not resused.
    ##
    ## Setup:
    ## Client gets initial lease, with no billing class.
    ##
    ## Case 1: 
    ## Client adds vendor-class-id when renewing with DORA before the 
    ## threshold expires.  
    ## - Server maps client to billing class and should NOT resuse the lease
    ##
    ## Case 2: 
    ## Client uses same vendor-class-id and renews with DORA before the
    ## threshold expires.
    ## - Server should reuse the lease
    ##
    ## Case 3: 
    ## Client uses same vendor-class-id and renews with RA before the
    ## threshold expires.
    ## - Server should reuse the lease
    ##
    ## Case 4: 
    ## Client changes vendor-class-id when renewing with DORA before the 
    ## threshold expires.  
    ## - Server maps client to different billing class and should NOT 
    ## resuse the lease
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
    Run configuration command:  class "vnd1001" {
    Run configuration command:     match if (option vendor-class-identifier = "vnd1001");
    Run configuration command:     lease limit 4;
    Run configuration command: }
    Run configuration command: class "vnd1003" {
    Run configuration command:     match if (option vendor-class-identifier = "vnd1003");
    Run configuration command:     lease limit 4;
    Run configuration command: }
  Send server configuration using SSH and config-file.
	DHCP Server is started.

    ###################################################################
    # Setup: Get the initial lease, no billing class
    ###################################################################
	Test Procedure: # Setup
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
    ## Case 1: 
    ## Client adds vendor-class-id when renewing with DORA before the 
    ## threshold expires.  
    ## - Server maps client to billing class and should NOT resuse the 
    ## lease
    ###################################################################
	Test Procedure: # Case 1
    Sleep for 1 seconds.
    Client adds to the message vendor_class_id with value vnd1001.
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.100.

    Test Procedure:
    Client adds to the message vendor_class_id with value vnd1001.
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
    ## Case 2: 
    ## Client uses same vendor-class-id and renews with DORA before the
    ## threshold expires.
    ## - Server should reuse the lease
    ###################################################################
	Test Procedure: # Case 2 
    Sleep for 1 seconds.
    Client adds to the message vendor_class_id with value vnd1001.
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.100.

    Test Procedure:
    Client adds to the message vendor_class_id with value vnd1001.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.100.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.100. 
    Response MUST include option 51.
    Response option 51 MUST NOT contain value 50. 
    DHCP log contains 2 of line: under 20% threshold

    ###################################################################
    ## Case 3: 
    ## Client uses same vendor-class-id and renews with RA before the
    ## threshold expires.
    ## - Server should reuse the lease
    ###################################################################
    Test Procedure: # Case 4
    Sleep for 1 seconds.
    Client adds to the message vendor_class_id with value vnd1001.
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
    ## Case 4: 
    ## Client changes vendor-class-id when renewing with DORA before the 
    ## threshold expires.  
    ## - Server maps client to different billing class and should NOT 
    ## resuse the lease
    ###################################################################
	Test Procedure:  # Case 5 
    Sleep for 20 seconds. 
    Client adds to the message vendor_class_id with value vnd1003.
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.100.

    Test Procedure:
    Client adds to the message vendor_class_id with value vnd1003.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.100.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.100. 
    Response MUST include option 51.
    Response option 51 MUST contain value 50. 
    DHCP log contains 3 of line: under 20% threshold

    ###################################################################
    ## Case 5: 
    ## Client uses same vendor-class-id and renews with RA before the
    ## threshold expires.
    ## - Server should reuse the lease
    ###################################################################
    Test Procedure: # Case 5
    Sleep for 1 seconds.
    Client adds to the message vendor_class_id with value vnd1003.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.100.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.100. 
    Response MUST include option 51.
    # When forge supports comparison change this to less than 50
    Response option 51 MUST NOT contain value 50. 
    DHCP log contains 4 of line: under 20% threshold

    ###################################################################
    ## Case 6: 
    ## Client omits vendor-class-id when renewing with DORA before the 
    ## threshold expires.  
    ## - Server removes billing class and should NOT resuse the lease
    ###################################################################
	Test Procedure:  # Case 6 
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
    DHCP log contains 4 of line: under 20% threshold
