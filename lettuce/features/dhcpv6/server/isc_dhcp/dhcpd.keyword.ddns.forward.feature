## These tests exercise the DDNS udpate keywords for forward updates.
## They are intended as sanity checks to validate that the keywords are
## recognized and do influence dhcpd behavior.  They do not involve actual
## DNS server(s) nor are they intended to validate DDNS updating end-to-end.
##
## These tests use dhcpd log content for validation and as such require
## dhcpd to be compiled with  DEBUG_DNS_UPDATES defined.  This is most easily
##  by "export CPPFLAGS=-DDEBUG_DNS_UPDATES" prior to running make.
##
## These tests generally consist of a SARR cycle, with the client supplying
## an FQDN on the request.  The server log and/or the FQDN in the response
## are checked for the expected outcome.
##
Feature: ISC_DHCP DHCPv6 Keywords
    Tests ISC_DHCP dhcpd configuration keywords

@v6 @dhcpd @keyword @ddns @forward
    Scenario: v6.dhcpd.keyword.ddns.forward.add
    ##
    ## Testing: Checks that a forward add is attempted when the configuration
    ## is valid but minimal and client sends a request with valid fqdn
    ##
    Test Setup:
    Server is configured with 3000::/32 subnet with 3000::2-3000::2 pool.
    Run configuration command: ddns-updates true;
    Run configuration command: ddns-domainname "six.example.com";
    Run configuration command: fqdn-reply true;
    Run configuration command: ddns-update-style interim;
    Run configuration command: zone six.example.com. {primary 175.16.1.1; }
  Send server configuration using SSH and config-file.
    DHCP Server is started.

    ##
    ## Grab a lease
    ##
	Test Procedure:
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.

	Test Procedure:
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
    Client sets FQDN_flags value to S.
    Client sets FQDN_domain_name value to myhost.bubba.com.
    Client does include fqdn.
    Client requests option 39.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::2.
    DHCP log MUST contain line: DDNS_STATE_ADD_FW_NXDOMAIN 3000::2 for myhost.six.example.com

@v6 @dhcpd @keyword @ddns @forward
    Scenario: v6.dhcpd.keyword.ddns.forward.do-forward-updates.false
    ##
    ## Testing: Checks that a forward add is not attempted if do-forward-updates
    ## is set to false.
    ##
    Test Setup:
    Server is configured with 3000::/32 subnet with 3000::2-3000::2 pool.
    Run configuration command: ddns-updates true;
    Run configuration command: ddns-domainname "six.example.com";
    Run configuration command: ddns-update-style interim;
    Run configuration command: do-forward-updates false;
    Run configuration command: zone EXAMPLE.ORG. {primary 127.0.0.1;}
  Send server configuration using SSH and config-file.
    DHCP Server is started.

    ##
    ## Grab a lease
    ##
	Test Procedure:
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.

	Test Procedure:
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
    Client sets FQDN_flags value to S.
    Client sets FQDN_domain_name value to six.example.com.
    Client does include fqdn.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::2.
    DHCP log MUST NOT contain line: DDNS_STATE_ADD_FW_NXDOMAIN 3000::2

@v6 @dhcpd @keyword @ddns @forward
    Scenario: v6.dhcpd.keyword.ddns.forward.no-client-fqdn
    ##
    ## Testing: Checks that forward ddns updates are not attempted when
    ## no client FQDN option is supplied.
    ##
    Test Setup:
    Server is configured with 3000::/32 subnet with 3000::2-3000::2 pool.
    Run configuration command: ddns-updates true;
    Run configuration command: ddns-domainname "six.example.com";
    Run configuration command: ddns-update-style interim;
    Run configuration command: do-forward-updates true;
    Run configuration command: zone EXAMPLE.ORG. {primary 127.0.0.1;}
  Send server configuration using SSH and config-file.
    DHCP Server is started.

    ##
    ## Grab a lease
    ##
	Test Procedure:
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.

	Test Procedure:
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::2.
    DHCP log MUST NOT contain line: DDNS_STATE_ADD_FW_NXDOMAIN 3000::2

@v6 @dhcpd @keyword @ddns @forward
    Scenario: v6.dhcpd.keyword.ddns.forward.ddns-hostname
    ##
    ## Testing: Checks that hostname used as the FQDN in the forward add
    ## can be specified using ddns-hostname.
    ##
    Test Setup:
    Server is configured with 3000::/32 subnet with 3000::2-3000::2 pool.
    Run configuration command: ddns-updates true;
    Run configuration command: ddns-domainname "six.example.com";
    Run configuration command: ddns-hostname "cfg_host";
    Run configuration command: ddns-update-style interim;
    Run configuration command: zone six.example.com. {primary 175.16.1.1; }
  Send server configuration using SSH and config-file.
    DHCP Server is started.

    ##
    ## Grab a lease
    ##
	Test Procedure:
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.

	Test Procedure:
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
    Client sets FQDN_flags value to S.
    Client sets FQDN_domain_name value to myhost.bubba.com.
    Client does include fqdn.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::2.
    DHCP log MUST contain line: DDNS_STATE_ADD_FW_NXDOMAIN 3000::2 for cfg_host.six.example.com

@v6 @dhcpd @keyword @ddns @forward
    Scenario: v6.dhcpd.keyword.ddns.forward.ddns-ttl
    ##
    ## Testing: Checks that TTL sent with the forward add can be specified
    ## using ddns-ttl.
    ##
    Test Setup:
    Server is configured with 3000::/32 subnet with 3000::2-3000::2 pool.
    Run configuration command: ddns-updates true;
    Run configuration command: ddns-domainname "six.example.com";
    Run configuration command: ddns-ttl 7701;
    Run configuration command: ddns-update-style interim;
    Run configuration command: zone six.example.com. {primary 175.16.1.1; }
  Send server configuration using SSH and config-file.
    DHCP Server is started.

    ##
    ## Grab a lease
    ##
	Test Procedure:
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client does include client-id.
    Client does include IA_Address.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 3.

	Test Procedure:
    Client copies IA_NA option from received message.
	Client copies client-id option from received message.
	Client copies server-id option from received message.
    Client sets FQDN_flags value to S.
    Client sets FQDN_domain_name value to myhost.bubba.com.
    Client does include fqdn.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::2.
    DHCP log MUST contain line: ttl: 7701

