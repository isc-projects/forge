Feature: ISC_DHCP DHCPv4 Keywords
    Tests ISC_DHCP dhcpd configuration keywords 

@v4 @dhcpd @keyword @use-host-decl-names @ddns
    Scenario: v4.dhcpd.keyword.use-host-decl-names-on.ddns
    ## Tests use-host-decl-names enabled in conjunction with ddns updates
    ## The  test consists of a single server configuration and instance which
    ## is used to execute the following test cases:
    ##
    ## Case 1:
    ## Get a lease for fixed host which has no host-name option.
    ## Server should send the host declarartion name back in to the client
    ## as the hostname option and use it in forward DNS name.
    ##
    ## Case 2:
    ## Get a lease for fixed host which has a host-name option.
    ## Server should send the hostname option defined in the host 
    ## declarartion back to the client, and and use it in forward DNS name.
    ##
    ## Case 3:
    ## Get a lease for fixed host has a host-name option, client sends hostname.
    ## Server should send back the hostname option defined in the host
    ## declaration but should use the hostname provided by the client in the
    ## forward DNS name.
    ##
    ## Case 4:
    ## Get a lease for a dynamic client.
    ## Server should NOT send back a hostname option and should not attempt
    ## a DNS update.
    ##
    ## Case 5:
    ## Get a lease for a dynamic client that sends hostname option.
    ## Server should NOT send back a hostname option and should not attempt
    ## a DNS update.
    ##
    ## NOTE: Currently Scapy does not support FQDN option for DHCPv4. Use of
    ## FQDN as the source for DDNS forward name cannot be tested via Forge
    ## at this time.
    ##
	Test Setup:
    Run configuration command: ping-check off;
    Run configuration command: use-host-decl-names on;
    Run configuration command: ddns-update-style interim;
    Run configuration command: ddns-updates on;
    Run configuration command: update-static-leases on;
    Run configuration command: ddns-domainname "four.example.com";

    Run configuration command: zone four.example.com. {
    Run configuration command:     primary 127.0.0.1;
    Run configuration command: }

    Run configuration command: subnet 192.168.50.0 netmask 255.255.255.0 {
    Run configuration command:     pool {
    Run configuration command:         range 192.168.50.100 192.168.50.101;
    Run configuration command:     }
    Run configuration command: }

    Run configuration command: host one {
    Run configuration command:     option dhcp-client-identifier "1111";
    Run configuration command:     fixed-address 192.168.50.201;
    Run configuration command: }

    Run configuration command: host two {
    Run configuration command:     option dhcp-client-identifier "2222";
    Run configuration command:     option host-name "two_opt";
    Run configuration command:     fixed-address 192.168.50.202;
    Run configuration command: }

    Run configuration command: host three {
    Run configuration command:     option dhcp-client-identifier "3333";
    Run configuration command:     option host-name "three_opt";
    Run configuration command:     fixed-address 192.168.50.203;
    Run configuration command: }
  Send server configuration using SSH and config-file.
	DHCP Server is started.

    ########################################################################
    ## Case 1:
    ## Get a lease for fixed host which has no host-name option
    ## Server should send the host declarartion name back in to the client
    ## as the hostname option and use it in forward DNS name.
    ########################################################################
	Test Procedure:
    Client adds to the message client_id with value 31:31:31:31.
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.201.
    Response MUST include option 12.
    Response option 12 MUST contain value one.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.201.
    Client adds to the message client_id with value 31:31:31:31.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.201.
    DHCP log MUST contain line: DDNS_STATE_ADD_FW_NXDOMAIN 192.168.50.201 for one.four.example.com

    ########################################################################
    ## Case 2:
    ## Get a lease for fixed host which has a host-name option
    ## Server should send the hostname option defined in the host 
    ## declarartion back to the client, and and use it in forward DNS name.
    ########################################################################
	Test Procedure:
    Client adds to the message client_id with value 32:32:32:32.
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.202.
    Response MUST include option 12.
    Response option 12 MUST contain value two_opt.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.202.
    Client adds to the message client_id with value 32:32:32:32.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.202.
    DHCP log MUST contain line: DDNS_STATE_ADD_FW_NXDOMAIN 192.168.50.202 for two_opt.four.example.com

    ########################################################################
    ## Case 3:
    ## Get a lease for fixed host has a host-name option, client sends hostname.
    ## Server should send back the hostname option defined in the host
    ## declaration but should use the hostname provided by the client in the
    ## forward DNS name.
    ########################################################################
	Test Procedure:
    Client adds to the message client_id with value 33:33:33:33.
    Client adds to the message hostname with value clnt_host.
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.203.
    Response MUST include option 12.
    Response option 12 MUST contain value three_opt.

    Test Procedure:
    Client adds to the message client_id with value 33:33:33:33.
    Client adds to the message hostname with value clnt_host.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.203.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.203.
    DHCP log MUST contain line: DDNS_STATE_ADD_FW_NXDOMAIN 192.168.50.203 for clnt_host.four.example.com

    ########################################################################
    ## Case 4:
    ## Get a lease for a dynamic client.
    ## Server should NOT send back a hostname option and should not attempt
    ## a DNS update.
    ########################################################################
	Test Procedure:
    Client adds to the message client_id with value 34:34:34:34.
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.100.
    #Response MUST NOT include option 12.

    Test Procedure:
    Client adds to the message client_id with value 34:34:34:34.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.100.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.100.
    DHCP log MUST NOT contain line: DDNS_STATE_ADD_FW_NXDOMAIN 192.168.50.100

    ########################################################################
    ## Case 5:
    ## Get a lease for a dynamic client that sends hostname option.
    ## Server should NOT send back a hostname option and should not attempt
    ## a DNS update.
    ########################################################################
	Test Procedure: 
    Client adds to the message client_id with value 34:34:34:34.
    Client adds to the message hostname with value clnt_host.
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response MUST contain yiaddr 192.168.50.100.
    Response MUST NOT include option 12.

    Test Procedure:
    Client adds to the message client_id with value 34:34:34:34.
    Client adds to the message hostname with value clnt_host.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.100.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.100.
    DHCP log MUST contain line: DDNS_STATE_ADD_FW_NXDOMAIN 192.168.50.100 for clnt_host.four.example.com

