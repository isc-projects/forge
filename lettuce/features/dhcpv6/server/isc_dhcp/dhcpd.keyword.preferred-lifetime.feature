Feature: ISC_DHCP DHCPv6 Keywords
    Tests ISC_DHCP dhcpd configuration keywords 
	
@v6 @dhcpd @keyword @preferred-lifetime
    Scenario: v6.dhcpd.keyword.preferred-lifetime-not-set
    ## Testing lease times offered when preferred-lifetime 
    ## is NOT specified.
    ##
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## Pass Criteria:
    ##
    ## valid lifetime offered should be default of 43200.
    ## preferred lifetime should be 27000 (62.5% of valid lifetime)
    ##
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::2 pool.
    Time preferred-lifetime is not configured.
    Time valid-lifetime is not configured.
    Send server configuration using SSH and config-file.
	DHCP Server is started.

	Test Procedure: 01
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain validlft 43200.
    Response sub-option 5 from option 3 MUST contain preflft 27000.

@v6 @dhcpd @keyword @preferred-lifetime
    Scenario: v6.dhcpd.keyword.preferred-lifetime-set
    ## Testing lease times offered when preferred-lifetime 
    ## is specified.
    ##
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## Pass Criteria:
    ##
    ## valid lifetime should be default value of 43200
    ## preferred lifetime should be configured value of 1000
    ##
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::2 pool.
    Time preferred-lifetime is configured with value 1000.
    Time valid-lifetime is not configured.
    Send server configuration using SSH and config-file.
	DHCP Server is started.
 
	Test Procedure: 02
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain validlft 43200.
    Response sub-option 5 from option 3 MUST contain preflft 1000.
