## These tests verify the echo-client-id keyword. 
##
## These tests generally consist peforming a DORA followed by an invalid
## request/nak for a given configuration.  Each response is than checked that
## it either does or does not contain the echoed client-id.
##
## While echo-client-id can be specified on a per subnet basis, Forge currently
## lacks a way to specify the client interface on the fly, which makes sending
## requests from different subnets during the same test problematic.
Feature: ISC_DHCP DHCPv4 Keywords
    Tests ISC_DHCP dhcpd configuration keywords 
	
@v4 @dhcpd @keyword @echo-client-id
    Scenario: v4.dhcpd.keyword.echo-client-id-off-offer-ack-nak
    ## Checks that the default behavior is echo-client-id off and that the
    ## does not echo back a received client-id.
    ##
	## Message details 		Client		Server
	## 						DISCOVER -->
	## 		   						<--	OFFER
	## 						REQUEST -->
	## 		   						<--	ACK
	## 						REQUEST -->
	## 		   						<--	NAK
	## Pass Criteria:
    ##
    ## OFFER received without client-id option
    ##
	Test Setup:
    Run configuration command:  ping-check off;
    Run configuration command:  subnet 192.168.50.0 netmask 255.255.255.0 {
    Run configuration command:  authoritative;
    Run configuration command:     range 192.168.50.100 192.168.50.101; }
  Send server configuration using SSH and config-file.
	DHCP Server is started.

	Test Procedure:
    # set client-id to 'rec1234'
    Client adds to the message client_id with value 72656331323334.
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.100.
    Response option 1 MUST contain value 255.255.255.0.
    Response MUST NOT include option 61.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.100.
    Client adds to the message client_id with value 72656331323334.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.100. 
    Response MUST NOT include option 61.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message client_id with value 72656331323334.
    # Use an out-of-subnet address to force NAK
    Client adds to the message requested_addr with value 172.16.1.100.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with NAK message.
    Response MUST NOT include option 61.

@v4 @dhcpd @keyword @echo-client-id
    Scenario: v4.dhcpd.keyword.echo-client-id-on-offer-ack-nak
    ## Checks that the when echo-client-id is  enabled the server echoes 
    ## back a client-id IF received.
    ##
    ## The following sequence is performed twice, once with the client
    ## sending a client_id and once without:
	## Message details 		Client		Server
	## 						DISCOVER -->
	## 		   						<--	OFFER
	## 						REQUEST -->
	## 		   						<--	ACK
	## 						REQUEST -->
	## 		   						<--	NAK
	## Pass Criteria:
    ##
    ## OFFER,ACK and NAK received with client-id option
    ##
	Test Setup:
    Run configuration command:  ping-check off;
    Run configuration command:  echo-client-id on;
    Run configuration command:  subnet 192.168.50.0 netmask 255.255.255.0 {
    Run configuration command:  authoritative;
    Run configuration command:     range 192.168.50.100 192.168.50.101; }
  Send server configuration using SSH and config-file.
	DHCP Server is started.

	Test Procedure:
    # set client-id to 'rec1234'
    Client adds to the message client_id with value 72656331323334.
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.100.
    Response option 1 MUST contain value 255.255.255.0.
    Response option 61 MUST contain value 72656331323334.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message client_id with value 72656331323334.
    Client adds to the message requested_addr with value 192.168.50.100.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response option 61 MUST contain value 72656331323334.
    Response MUST contain yiaddr 192.168.50.100. 

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message client_id with value 72656331323334.
    # Use an out-of-subnet address to force NAK
    Client adds to the message requested_addr with value 172.16.1.100.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with NAK message.
    Response option 61 MUST contain value 72656331323334.

    ###############################################################
    # Repeat the sequence without a client sending an id
    ###############################################################
	Test Procedure:
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.101.
    Response MUST NOT include option 61.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.101.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST NOT include option 61.

    Test Procedure:
    Client copies server_id option from received message.
    # Use an out-of-subnet address to force NAK
    Client adds to the message requested_addr with value 172.16.1.101.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with NAK message.
    Response MUST NOT include option 61.



@v4 @dhcpd @keyword @echo-client-id
    Scenario: v4.dhcpd.keyword.echo-client-id-per-class
    ## Tests the echo-client-id can be specified on class basis.
    ## The following message sequence is performed once for a client
    ## which belongs to class "echo" and once for a client which does not.
    ## In the former, echo-client-id enabled, in the latter it is not:
    ##
	## Message details 		Client		Server
	## 						DISCOVER -->
	## 		   						<--	OFFER
	## 						REQUEST -->
	## 		   						<--	ACK
	## 						REQUEST -->
	## 		   						<--	NAK
	## Pass Criteria:
    ##
    ## OFFER,ACK and NAK received with client-id option for first subnet,
    ## not received for the second.
    ##
	Test Setup:
    Run configuration command: ping-check off;
    Run configuration command: class "echo" {
    Run configuration command:     match if (substring(option host-name, 0, 4) = "echo");
    Run configuration command:     echo-client-id on;
    Run configuration command: }
    Run configuration command: class "noecho" {
    Run configuration command:     match if (substring(option host-name, 0, 6) = "noecho");
    Run configuration command: }
    Run configuration command: subnet 192.168.50.0 netmask 255.255.255.0 {
    Run configuration command:     authoritative;
    Run configuration command:     pool {
    Run configuration command:         range 192.168.50.100 192.168.50.101;
    Run configuration command:     }
    Run configuration command: }

    # set client-id to 'rec1234'
    Client adds to the message client_id with value 72656331323334.
    Client adds to the message hostname with value echo.
  Send server configuration using SSH and config-file.
	DHCP Server is started.

	Test Procedure:
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.100.
    Response option 1 MUST contain value 255.255.255.0.
    Response option 61 MUST contain value 72656331323334.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message hostname with value echo.
    Client adds to the message client_id with value 72656331323334.
    Client adds to the message requested_addr with value 192.168.50.100.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.100.
    Response option 61 MUST contain value 72656331323334.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message hostname with value echo.
    Client adds to the message client_id with value 72656331323334.
    # Use an out-of-subnet address to force NAK
    Client adds to the message requested_addr with value 172.16.1.100.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with NAK message.
    Response option 61 MUST contain value 72656331323334.

    ########################################################## 
    # Now test with a client that is NOT in class "echo"
    ########################################################## 
    Test Procedure:
    Client adds to the message client_id with value 72656331323334.
    Client adds to the message hostname with value noecho.
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.100.
    Response option 1 MUST contain value 255.255.255.0.
    Response MUST NOT include option 61.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message hostname with value noecho.
    Client adds to the message client_id with value 72656331323334.
    Client adds to the message requested_addr with value 192.168.50.100.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.100.
    Response MUST NOT include option 61.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message hostname with value noecho.
    Client adds to the message client_id with value 72656331323334.
    # Use an out-of-subnet address to force NAK
    Client adds to the message requested_addr with value 172.16.1.100.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with NAK message.
    Response MUST NOT include option 61.

@v4 @dhcpd @keyword @echo-client-id
    Scenario: v4.dhcpd.keyword.echo-client-id-vs-config-id
    ##
	## Message details 		Client		Server
	## 						DISCOVER -->
	## 		   						<--	OFFER
	## 						REQUEST -->
	## 		   						<--	ACK
	## 						REQUEST -->
	## 		   						<--	NAK
	## Pass Criteria:
    ##
    ## OFFER,ACK and NAK received with client-id option
    ##
	Test Setup:
    Run configuration command:  ping-check off;
    Run configuration command:  subnet 192.168.50.0 netmask 255.255.255.0 {
    Run configuration command:  authoritative;
    Run configuration command:  echo-client-id on;
    Run configuration command:  option dhcp-client-identifier "cfg1234";
    Run configuration command:     range 192.168.50.100 192.168.50.101; }
  Send server configuration using SSH and config-file.
	DHCP Server is started.

	Test Procedure:
    # set client-id to 'rec1234'
    Client adds to the message client_id with value 72656331323334.
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.100.
    Response option 1 MUST contain value 255.255.255.0.
    Response option 61 MUST contain value 72656331323334.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message client_id with value 72656331323334.
    Client adds to the message requested_addr with value 192.168.50.100.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response option 61 MUST contain value 72656331323334.
    Response MUST contain yiaddr 192.168.50.100. 

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message client_id with value 72656331323334.
    # Use an out-of-subnet address to force NAK
    Client adds to the message requested_addr with value 172.16.1.100.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with NAK message.
    # Received id is available even on NAKs
    Response option 61 MUST contain value 72656331323334.

    ###############################################################
    # Repeat the sequence without a client sending an id, should
    # get configured id
    ###############################################################
	Test Procedure:
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.101.
    Response option 61 MUST contain value 63666731323334.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.101.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response option 61 MUST contain value 63666731323334.

    Test Procedure:
    Client copies server_id option from received message.
    # Use an out-of-subnet address to force NAK
    Client adds to the message requested_addr with value 172.16.1.101.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with NAK message.
    # Configured id is set at selected subnet level, in this case it
    # is not there to send.
    Response MUST NOT include option 61.

@v4 @dhcpd @keyword @echo-client-id
    Scenario: v4.dhcpd.keyword.echo-client-id-off-and-PRL
    # Verifies the following scenarios with ehco-client-id disabled:
    #   DISCOVER with client-id but no PRL
    #   DISCOVER with client-id and a PRL which does NOT ask for client-id
    #   DISCOVER with client-id and a PRL which does asks for client-id
    #   DISCOVER without client-id but no PRL
    #   DISCOVER without client-id and a PRL which does NOT ask for client-id
    #   DISCOVER without client-id and a PRL which does asks for client-id
    #
	Test Setup:
    Run configuration command:  ping-check off;
    Run configuration command:  subnet 192.168.50.0 netmask 255.255.255.0 {
    Run configuration command:  authoritative;
    Run configuration command:  option root-path "/opt/var/stuff";
    Run configuration command:  option dhcp-client-identifier "cfg1234";
    Run configuration command:     range 192.168.50.100 192.168.50.120; }
  Send server configuration using SSH and config-file.
	DHCP Server is started.

    # Send DISCOVER with client-id but without PRL
    # Should get configured id in OFFER
	Test Procedure:
    Client adds to the message client_id with value 72656331323334.
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response option 61 MUST contain value 63666731323334.

    # Send DISCOVER with client-id and a PRL which does NOT ask for client-id
    # Should NOT client-id in OFFER
	Test Procedure:
    Client requests option 17.
    Client adds to the message client_id with value 72656331323334.
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response option 17 MUST contain value /opt/var/stuff.
    Response MUST NOT include option 61.

    # Send DISCOVER with client-id and a PRL which does asks for client-id
    # Should get configured-id in OFFER
	Test Procedure:
    Client requests option 17.
    Client requests option 61.
    Client adds to the message client_id with value 72656331323334.
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response option 17 MUST contain value /opt/var/stuff.
    Response option 61 MUST contain value 63666731323334.

    # Send DISCOVER WIHTOUT client-id or PRL
    # Should get configured-id in OFFER
	Test Procedure:
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response option 61 MUST contain value 63666731323334.

    # Send DISCOVER WITHOUT client-id but a PRL which does NOT ask for 
    # client-id.  
    # Should NOT get configured client-id in OFFER
	Test Procedure:
    Client requests option 17.
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response option 17 MUST contain value /opt/var/stuff.
    Response MUST NOT include option 61.

    # Send DISCOVER WITHOUT client-id but a PRL which does asks for client-id
    # Should get configured client-id in OFFER
	Test Procedure:
    Client requests option 17.
    Client requests option 61.
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response option 17 MUST contain value /opt/var/stuff.
    Response option 61 MUST contain value 63666731323334.


@v4 @dhcpd @keyword @echo-client-id
    Scenario: v4.dhcpd.keyword.echo-client-id-on-and-PRL
    # Verifies the following scenarios with ehco-client-id enabled:
    #   DISCOVER with client-id but no PRL
    #   DISCOVER with client-id and a PRL which does NOT ask for client-id
    #   DISCOVER with client-id and a PRL which does asks for client-id
    #   DISCOVER without client-id but no PRL
    #   DISCOVER without client-id and a PRL which does NOT ask for client-id
    #   DISCOVER without client-id and a PRL which does asks for client-id
    #
	Test Setup:
    Run configuration command:  ping-check off;
    Run configuration command:  subnet 192.168.50.0 netmask 255.255.255.0 {
    Run configuration command:  authoritative;
    Run configuration command:  echo-client-id on;
    Run configuration command:  option root-path "/opt/var/stuff";
    Run configuration command:  option dhcp-client-identifier "cfg1234";
    Run configuration command:     range 192.168.50.100 192.168.50.120; }
  Send server configuration using SSH and config-file.
	DHCP Server is started.

    # Send DISCOVER with client-id but without PRL
    # Should get client-id we sent back in OFFER
	Test Procedure:
    Client adds to the message client_id with value 72656331323334.
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response option 61 MUST contain value 72656331323334.

    # Send DISCOVER with client-id and a PRL which does NOT ask for client-id
    # Should get client-id we sent back in OFFER
	Test Procedure:
    Client requests option 17.
    Client adds to the message client_id with value 72656331323334.
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response option 17 MUST contain value /opt/var/stuff.
    Response option 61 MUST contain value 72656331323334.

    # Send DISCOVER with client-id and a PRL which does asks for client-id
    # Should get client-id we sent back in OFFER
	Test Procedure:
    Client requests option 17.
    Client requests option 61.
    Client adds to the message client_id with value 72656331323334.
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response option 17 MUST contain value /opt/var/stuff.
    Response option 61 MUST contain value 72656331323334.

    # Send DISCOVER WIHTOUT client-id or PRL
    # Should get configured-id in OFFER
	Test Procedure:
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response option 61 MUST contain value 63666731323334.

    # Send DISCOVER WITHOUT client-id but a PRL which does NOT ask for 
    # client-id.  
    # Should get configured client-id in OFFER
	Test Procedure:
    Client requests option 17.
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response option 17 MUST contain value /opt/var/stuff.
    Response option 61 MUST contain value 63666731323334.

    # Send DISCOVER WITHOUT client-id but a PRL which does asks for client-id
    # Should get configured client-id in OFFER
	Test Procedure:
    Client requests option 17.
    Client requests option 61.
	Client sends DISCOVER message.

	Pass Criteria:
	Server MUST respond with OFFER message.
    Response option 17 MUST contain value /opt/var/stuff.
    Response option 61 MUST contain value 63666731323334.
