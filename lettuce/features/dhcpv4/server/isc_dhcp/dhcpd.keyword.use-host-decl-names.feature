Feature: ISC_DHCP DHCPv4 Keywords
    Tests ISC_DHCP dhcpd configuration keywords 
    ## NOTE These tests require that CLI_MAC be set to the actual
    ## mac of interface specifed by IFACE. 

@v4 @dhcpd @keyword @use-host-decl-names
    Scenario: v4.dhcpd.keyword.use-host-decl-names-on
    ## Tests use-host-decl-names enabled for both a BOOTP and DHCP.
    ##
	## Message details 		Client		  Server
	## 						BOOTP_REQUEST -->
	## 		   						<--	BOOTP_REPLY
	## 						DISCOVER -->
	## 		   						<-- OFFER	
    ##
	## Pass Criteria: In both instances the server's response should contain
    ## the host-name option whose value is the name of the host declaration. 
    ##
	Test Setup:
    Run configuration command: ping-check off;
    Run configuration command: always-reply-rfc1048 on;
    Run configuration command: subnet 192.168.50.0 netmask 255.255.255.0 {
    Run configuration command:      authoritative; 
    Run configuration command: }
    Run configuration command: group {
    Run configuration command:     use-host-decl-names on;
    Run configuration command:     host cartmen {
    Run configuration command:         hardware ethernet $(CLI_MAC);
    Run configuration command:         fixed-address 192.168.50.10;
    Run configuration command:     }
    Run configuration command: }
  Send server configuration using SSH and config-file.
	DHCP Server is started.

    # Do BOOTP_REQUEST, BOOTP_REPLY should have host-name = cartmen
	Test Procedure:
	Client sends BOOTP_REQUEST message.

	Pass Criteria:
	Server MUST respond with BOOTP_REPLY message.
    Response MUST contain yiaddr 192.168.50.10.
    Response MUST include option 12.
    Response option 12 MUST contain value cartmen.

    # Do DISCOVER, OFFER should have host-name = cartmen
	Test Procedure:
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.10.
    Response MUST include option 12.
    Response option 12 MUST contain value cartmen.

@v4 @dhcpd @keyword @use-host-decl-names
    Scenario: v4.dhcpd.keyword.use-host-decl-names-off
    ## Tests use-host-decl-names enabled for both a BOOTP and DHCP.
    ##
	## Message details 		Client		  Server
	## 						BOOTP_REQUEST -->
	## 		   						<--	BOOTP_REPLY
	## 						DISCOVER -->
	## 		   						<-- OFFER	
    ##
	## Pass Criteria: In both instances the server's response should NOT
    ## contain the host-name option.
    ##
	Test Setup:
    Run configuration command: ping-check off;
    Run configuration command: always-reply-rfc1048 on;
    Run configuration command: subnet 192.168.50.0 netmask 255.255.255.0 {
    Run configuration command:      authoritative; 
    Run configuration command: }
    Run configuration command: group {
    Run configuration command:     use-host-decl-names off;
    Run configuration command:     host cartmen {
    Run configuration command:         hardware ethernet $(CLI_MAC); 
    Run configuration command:         fixed-address 192.168.50.10;
    Run configuration command:     }
    Run configuration command: }
  Send server configuration using SSH and config-file.
	DHCP Server is started.

    # Do BOOTP_REQUEST, BOOTP_REPLY should not contain host-name.
	Test Procedure:
	Client sends BOOTP_REQUEST message.

	Pass Criteria:
	Server MUST respond with BOOTP_REPLY message.
    Response MUST contain yiaddr 192.168.50.10.
    Response MUST NOT include option 12.

    # Do DISCCOVER, OFFER should not contain host-name.
	Test Procedure:
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.10.
    Response MUST NOT include option 12.

@v4 @dhcpd @keyword @use-host-decl-names
    Scenario: v4.dhcpd.keyword.use-host-decl-names-override
    ## Tests use-host-decl-names enabled but overridden by host-name option
    ## defined within the host-declaration.
    ##
	## Message details 		Client		  Server
	## 						BOOTP_REQUEST -->
	## 		   						<--	BOOTP_REPLY
	## 						DISCOVER -->
	## 		   						<-- OFFER	
    ##
	## Pass Criteria: In both instances the server's response should
    ## contain the host-name option whose value is that of the defined
    ## host-name option.
    ##
	Test Setup:
    Run configuration command: ping-check off;
    Run configuration command: always-reply-rfc1048 on;
    Run configuration command: subnet 192.168.50.0 netmask 255.255.255.0 {
    Run configuration command:      authoritative; 
    Run configuration command: }
    Run configuration command: group {
    Run configuration command:     use-host-decl-names on;
    Run configuration command:     host cartmen {
    Run configuration command:         hardware ethernet $(CLI_MAC); 
    Run configuration command:         fixed-address 192.168.50.10;
    Run configuration command:         option host-name "notcartmen";
    Run configuration command:     }
    Run configuration command: }
  Send server configuration using SSH and config-file.
	DHCP Server is started.

    # Do BOOTP_REQUEST, BOOTP_REPLY should have host-name = notcartmen
	Test Procedure:
	Client sends BOOTP_REQUEST message.

	Pass Criteria:
	Server MUST respond with BOOTP_REPLY message.
    Response MUST contain yiaddr 192.168.50.10.
    Response MUST include option 12.
    Response option 12 MUST contain value notcartmen.

    # Do DISCOVER, OFFER should have host-name = notcartmen
	Test Procedure:
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.10.
    Response MUST include option 12.
    Response option 12 MUST contain value notcartmen.
