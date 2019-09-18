# Tests ISC_DHCPD keywork prefix-length-mode
Feature: ISC_DHCP DHCPv6 Keywords Prefix Length Mode
    Tests ISC_DHCPD permutations of prefix-length-mode keyword

@v6 @dhcp6 @PD @rfc3633 @keyword @prefix-length-mode
    Scenario: dhcpd.keyword.prefix-length-mode.default
    # Tests default setting for prefix_len_mode which should be match
    # prefix-length-mode = PLM_PREFER.
    # Uses a series of solicits with varying plens to check the offer
    # outcome.
    #
    # Solicit plen    Offer Outcome
    # --------------------------------------
    # /0              3000:db8:0:100::/56
    # /48             3000:db8:0:100::/56
    # /60             3000:db8:0:100::/56
    # /64             3000:db8:1:100::/64
    # /72             3000:db8:0:100::/56

    Test Setup:
    Run configuration command: ddns-updates off;
    Run configuration command: authoritative;
    Run configuration command: subnet6 3000::/16 {
    Run configuration command:  pool6 {
    Run configuration command:   prefix6 3000:db8:0:100:: 3000:db8:0:100:: /56;
    Run configuration command:  }
    Run configuration command:  pool6 {
    Run configuration command:   prefix6 3000:db8:1:100:: 3000:db8:1:100:: /64;
    Run configuration command:  }
    Send server configuration using SSH and config-file.
    DHCP server is started.

    # /0              3000:db8:0:100::/56
    Test Procedure: 01 
    Client does include client-id.
    Client sets plen value to 0.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.
    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response sub-option 26 from option 25 MUST contain plen 56.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

    # /48             3000:db8:0:100::/56
    Test Procedure: 02
    Client does include client-id.
    Client sets plen value to 48.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response sub-option 26 from option 25 MUST contain plen 56.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

    # /60             3000:db8:0:100::/56
    Test Procedure: 03
    Client does include client-id.
    Client sets plen value to 60.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.
    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response sub-option 26 from option 25 MUST contain plen 56.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

    # /64             3000:db8:1:100::/64
    Test Procedure: 04
    Client does include client-id.
    Client sets plen value to 64.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.
    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response sub-option 26 from option 25 MUST contain plen 64.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:1:100::.

    # /72             3000:db8:0:100::/56
    Test Procedure: 05
    Client does include client-id.
    Client sets plen value to 72.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.
    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response sub-option 26 from option 25 MUST contain plen 56.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

@v6 @dhcp6 @PD @rfc3633 @keyword @prefix-length-mode
    Scenario: dhcpd.keyword.prefix-length-mode.ignore
    # Tests prefix-length-mode = ignore
    # Uses a series of solicits with varying plens to check the offer
    # outcome.
    #
    # Solicit plen    Offer Outcome
    # --------------------------------------
    # /0              3000:db8:0:100::/56
    # /48             3000:db8:0:100::/56
    # /60             3000:db8:0:100::/56
    # /64             3000:db8:0:100::/56
    # /72             3000:db8:0:100::/56

    Test Setup:
    Run configuration command: ddns-updates off;
    Run configuration command: authoritative;
    Run configuration command: prefix-length-mode ignore;
    Run configuration command: subnet6 3000::/16 {
    Run configuration command:  pool6 {
    Run configuration command:   prefix6 3000:db8:0:100:: 3000:db8:0:100:: /56;
    Run configuration command:  }
    Run configuration command:  pool6 {
    Run configuration command:   prefix6 3000:db8:1:100:: 3000:db8:1:100:: /64;
    Run configuration command:  }
    Send server configuration using SSH and config-file.
    DHCP server is started.

    # /0              3000:db8:0:100::/56
    Test Procedure: 06
    Client does include client-id.
    Client sets plen value to 0.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.
    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response sub-option 26 from option 25 MUST contain plen 56.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

    # /48             3000:db8:0:100::/56
    Test Procedure: 07
    Client does include client-id.
    Client sets plen value to 48.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.
    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response sub-option 26 from option 25 MUST contain plen 56.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

    # /60             3000:db8:0:100::/56
    Test Procedure: 08
    Client does include client-id.
    Client sets plen value to 60.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.
    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response sub-option 26 from option 25 MUST contain plen 56.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

    # /64             3000:db8:1:100::/56
    Test Procedure: 09
    Client does include client-id.
    Client sets plen value to 64.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.
    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response sub-option 26 from option 25 MUST contain plen 56.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

    # /72             3000:db8:1:100::/56
    Test Procedure: 10
    Client does include client-id.
    Client sets plen value to 72.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.
    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response sub-option 26 from option 25 MUST contain plen 56.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

@v6 @dhcp6 @PD @rfc3633 @keyword @prefix-length-mode
    Scenario: dhcpd.keyword.prefix-length-mode.prefer
    # Tests prefix-length-mode = prefer
    # Uses a series of solicits with varying plens to check the offer
    # outcome.
    #
    # Solicit plen    Offer Outcome
    # --------------------------------------
    # /0              3000:db8:0:100::/56
    # /48             3000:db8:0:100::/56
    # /60             3000:db8:0:100::/56
    # /64             3000:db8:1:100::/64
    # /72             3000:db8:0:100::/56

    Test Setup:
    Run configuration command: ddns-updates off;
    Run configuration command: authoritative;
    Run configuration command: prefix-length-mode prefer;
    Run configuration command: subnet6 3000::/16 {
    Run configuration command:  pool6 {
    Run configuration command:   prefix6 3000:db8:0:100:: 3000:db8:0:100:: /56;
    Run configuration command:  }
    Run configuration command:  pool6 {
    Run configuration command:   prefix6 3000:db8:1:100:: 3000:db8:1:100:: /64;
    Run configuration command:  }
    Send server configuration using SSH and config-file.
    DHCP server is started.

    # /0              3000:db8:0:100::/56
    Test Procedure: 11
    Client does include client-id.
    Client sets plen value to 0.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.
    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response sub-option 26 from option 25 MUST contain plen 56.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

    # /48             3000:db8:0:100::/56
    Test Procedure: 12
    Client does include client-id.
    Client sets plen value to 48.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response sub-option 26 from option 25 MUST contain plen 56.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

    # /60             3000:db8:0:100::/56
    Test Procedure: 13
    Client does include client-id.
    Client sets plen value to 60.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.
    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response sub-option 26 from option 25 MUST contain plen 56.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

    # /64             3000:db8:1:100::/64
    Test Procedure: 14
    Client does include client-id.
    Client sets plen value to 64.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.
    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response sub-option 26 from option 25 MUST contain plen 64.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:1:100::.

    # /72             3000:db8:0:100::/56
    Test Procedure: 15
    Client does include client-id.
    Client sets plen value to 72.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.
    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response sub-option 26 from option 25 MUST contain plen 56.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

@v6 @dhcp6 @PD @rfc3633 @keyword @prefix-length-mode
    Scenario: dhcpd.keyword.prefix-length-mode.exact
    # Tests default setting for prefix-length-mode = exact.
    #
    # Uses a series of solicits with varying plens to check the offer
    # outcome.
    #
    # Solicit plen    Offer Outcome
    # --------------------------------------
    # /0              3000:db8:0:100::/56
    # /48             None available
    # /60             None available
    # /64             3000:db8:1:100::/64
    # /72             None available

    Test Setup:
    Run configuration command: ddns-updates off;
    Run configuration command: authoritative;
    Run configuration command: prefix-length-mode exact;
    Run configuration command: subnet6 3000::/16 {
    Run configuration command:  pool6 {
    Run configuration command:   prefix6 3000:db8:0:100:: 3000:db8:0:100:: /56;
    Run configuration command:  }
    Run configuration command:  pool6 {
    Run configuration command:   prefix6 3000:db8:1:100:: 3000:db8:1:100:: /64;
    Run configuration command:  }
    Send server configuration using SSH and config-file.
    DHCP server is started.

    # /0              3000:db8:0:100::/56
    Test Procedure: 16
    Client does include client-id.
    Client sets plen value to 0.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.
    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response sub-option 26 from option 25 MUST contain plen 56.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

    # /48             None available
    Test Procedure: 17
    Client does include client-id.
    Client sets plen value to 48.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.
    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 13.
    Response sub-option 13 from option 25 MUST contain statuscode 6.

    # /60             None available
    Test Procedure: 18
    Client does include client-id.
    Client sets plen value to 60.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.
    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 13.
    Response sub-option 13 from option 25 MUST contain statuscode 6.

    # /64             3000:db8:1:100::/64
    Test Procedure: 19
    Client does include client-id.
    Client sets plen value to 64.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.
    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response sub-option 26 from option 25 MUST contain plen 64.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:1:100::.

    # /72             None available
    Test Procedure: 20
    Client does include client-id.
    Client sets plen value to 72.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.
    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 13.
    Response sub-option 13 from option 25 MUST contain statuscode 6.

@v6 @dhcp6 @PD @rfc3633 @keyword @prefix-length-mode
    Scenario: dhcpd.keyword.prefix-length-mode.minimum
    # Tests default setting for prefix-length-mode = minimum, which should select:
    # an exact match if it exists, then the first available whose prefix
    # length is greater than preferred length, otherwise fail
    #
    # Uses a series of solicits with varying plens to check the offer
    # outcome.
    #
    # Solicit plen    Offer Outcome
    # --------------------------------------
    # /0              3000:db8:0:100::/56
    # /48             3000:db8:0:100::/56
    # /60             3000:db8:1:100::/64
    # /64             3000:db8:1:100::/64
    # /72             None available

    Test Setup:
    Run configuration command: ddns-updates off;
    Run configuration command: authoritative;
    Run configuration command: prefix-length-mode minimum;
    Run configuration command: subnet6 3000::/16 {
    Run configuration command:  pool6 {
    Run configuration command:   prefix6 3000:db8:0:100:: 3000:db8:0:100:: /56;
    Run configuration command:  }
    Run configuration command:  pool6 {
    Run configuration command:   prefix6 3000:db8:1:100:: 3000:db8:1:100:: /64;
    Run configuration command:  }
    Send server configuration using SSH and config-file.
    DHCP server is started.

    # /0              3000:db8:0:100::/56
    Test Procedure: 21
    Client does include client-id.
    Client sets plen value to 0.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.
    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response sub-option 26 from option 25 MUST contain plen 56.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

    # /48             3000:db8:0:100::/56
    Test Procedure: 22
    Client does include client-id.
    Client sets plen value to 48.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.
    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response sub-option 26 from option 25 MUST contain plen 56.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

    # /60             3000:db8:1:100::/64
    Test Procedure: 23
    Client does include client-id.
    Client sets plen value to 60.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.
    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response sub-option 26 from option 25 MUST contain plen 64.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:1:100::.

    # /64             3000:db8:1:100::/64
    Test Procedure: 24
    Client does include client-id.
    Client sets plen value to 64.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.
    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response sub-option 26 from option 25 MUST contain plen 64.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:1:100::.

    # /72             None available
    Test Procedure: 25
    Client does include client-id.
    Client sets plen value to 72.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.
    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 13.
    Response sub-option 13 from option 25 MUST contain statuscode 6.

@v6 @dhcp6 @PD @rfc3633 @keyword @prefix-length-mode
    Scenario: dhcpd.keyword.prefix-length-mode.maximum
    # Tests default setting for prefix-length-mode = maximum, which should select:
    # an exact match if it exists, then the first available whose prefix
    # length is less than preferred length, otherwise fail
    #
    # Uses a series of solicits with varying plens to check the offer
    # outcome.
    #
    # Solicit plen    Offer Outcome
    # --------------------------------------
    # /0              3000:db8:0:100::/56
    # /48             None available
    # /60             3000:db8:1:100::/56
    # /64             3000:db8:1:100::/64
    # /72             3000:db8:0:100::/56

    Test Setup:
    Run configuration command: ddns-updates off;
    Run configuration command: authoritative;
    Run configuration command: prefix-length-mode maximum;
    Run configuration command: subnet6 3000::/16 {
    Run configuration command:  pool6 {
    Run configuration command:   prefix6 3000:db8:0:100:: 3000:db8:0:100:: /56;
    Run configuration command:  }
    Run configuration command:  pool6 {
    Run configuration command:   prefix6 3000:db8:1:100:: 3000:db8:1:100:: /64;
    Run configuration command:  }
    Send server configuration using SSH and config-file.
    DHCP server is started.

    # /0              3000:db8:0:100::/56
    Test Procedure: 26
    Client does include client-id.
    Client sets plen value to 0.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.
    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response sub-option 26 from option 25 MUST contain plen 56.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.


    # /48             None available
    Test Procedure: 27
    Client does include client-id.
    Client sets plen value to 48.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.
    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 13.
    Response sub-option 13 from option 25 MUST contain statuscode 6.

    # /60            3000:db8:1:100::/56
    Test Procedure: 28
    Client does include client-id.
    Client sets plen value to 60.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.
    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response sub-option 26 from option 25 MUST contain plen 56.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

    # /64             3000:db8:1:100::/64
    Test Procedure: 29
    Client does include client-id.
    Client sets plen value to 64.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.
    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response sub-option 26 from option 25 MUST contain plen 64.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:1:100::.

    # /72             3000:db8:1:100::/56
    Test Procedure: 30
    Client does include client-id.
    Client sets plen value to 72.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.
    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response sub-option 26 from option 25 MUST contain plen 56.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

@v6 @dhcp6 @PD @rfc3633 @keyword @prefix-length-mode
    Scenario: dhcpd.keyword.prefix-length-mode.plen_0
    # Tests that prefix selection is correct for clients solicitng with plen
    # of 0, as pools are exhausted.  Witha plen of 0, prefix-length-mode is
    # ignored, so prefix consumption should proceed from first available.
    #
    # Server is configured with two pools of 1 prefix each.  One pool with
    # a prefix length of /56, the second with a prefix length of /64. Then a
    # series of three SARRs, each using a different DUID are conducted:
    #
    # Case 1: Client 1 requests an address
    #  - server should grant a lease from /56 pool (exhausts the /56 pool)
    # Case 2: Client 2 requests an address
    #  - server should grant a lease from /64 pool (exhausts the /64 pool)
    # Case 3: Client 3 requests an address
    #  - server should respond with no addresses available

    Test Setup:
    Run configuration command: ddns-updates off;
    Run configuration command: authoritative;
    Run configuration command: subnet6 3000::/16 {
    Run configuration command:  pool6 {
    Run configuration command:   prefix6 3000:db8:0:100:: 3000:db8:0:100:: /56;
    Run configuration command:  }
    Run configuration command:  pool6 {
    Run configuration command:   prefix6 3000:db8:1:100:: 3000:db8:1:100:: /64;
    Run configuration command:  }
    Send server configuration using SSH and config-file.
    DHCP server is started.

    #######################################################################
    # Case 1: Client 1 requests an address
    #  - server should grant a lease from /56 pool (exhausts the /56 pool)
    #######################################################################
    Test Procedure: 31
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client does include client-id. 
    Client sets plen value to 0.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response sub-option 26 from option 25 MUST contain plen 56.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

    Test Procedure: 32
    #Client copies IA-PD option from received message.
    Client copies IA_PD option from received message.
    Client copies client-id option from received message.
    Client copies server-id option from received message.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response option 25 MUST contain sub-option 26.
    Response sub-option 26 from option 25 MUST contain plen 56.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

    #######################################################################
    # Case 2: Client 2 requests an address
    #  - server should grant a lease from /64 pool (exhausts the /64 pool)
    #######################################################################
    Test Procedure: 33
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:02.
    Client does include client-id.
    Client sets plen value to 0.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response sub-option 26 from option 25 MUST contain plen 64.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:1:100::.

    Test Procedure: 34
    #Client copies IA-PD option from received message.
    Client copies IA_PD option from received message.
    Client copies client-id option from received message.
    Client copies server-id option from received message.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response option 25 MUST contain sub-option 26.
    Response sub-option 26 from option 25 MUST contain plen 64.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:1:100::.

    #######################################################################
    # Case 3: Client 3 requests an address
    #  - server should respond with no addresses available
    #######################################################################
    Test Procedure: 35
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:03.
    Client does include client-id.
    Client sets plen value to 0.
    Client sets prefix value to ::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 13.
    Response sub-option 13 from option 25 MUST contain statuscode 6.
