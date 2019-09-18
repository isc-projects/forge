Feature: ISC_DHCP DHCPv6 Keywords
    Tests ISC_DHCP dhcpd configuration keywords 
	
@v6 @dhcpd @keyword @server-duid
    Scenario: v6.dhcpd.keyword.server-duid-ll
    ## Testing server-duid LL
    ##
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## Pass Criteria:
    ##
    ## server DUID matches the configured LL value
    ##
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::2 pool.
    Run configuration command: server-duid LL ethernet 00:16:6f:49:7d:9b; 
    Send server configuration using SSH and config-file.
	DHCP Server is started.

	Test Procedure: 01
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 2.
    Response option 2 must contain duid 00:03:00:01:00:16:6f:49:7d:9b; 
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

@v6 @dhcpd @keyword @server-duid
    Scenario: v6.dhcpd.keyword.server-duid-llt
    ## Testing server-duid LLT
    ##
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## Pass Criteria:
    ##
    ## server DUID matches the configured LLT value
    ##
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::2 pool.
    Run configuration command: server-duid LLT ethernet 9999 00:16:6f:49:7d:9b;
    Send server configuration using SSH and config-file.
	DHCP Server is started.

	Test Procedure: 02
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 2.
    Response option 2 must contain duid 00:01:00:01:27:0f:00:16:6f:49:7d:9b; 
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

@v6 @dhcpd @keyword @server-duid
    Scenario: v6.dhcpd.keyword.server-duid-en
    ## Testing server-duid EN 
    ##
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## Pass Criteria:
    ##
    ## server DUID matches the configured EN value
    ##
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::2 pool.
    Run configuration command: server-duid EN 2495 "peter-pan";
    Send server configuration using SSH and config-file.
	DHCP Server is started.

	Test Procedure: 03
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 2.
    Response option 2 must contain duid 00022495peter-pan.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
