# Tests ISC_DHCPD solicits/requests for prefixes that are "in pool"
# but whose prefix length do not match the pool are handled properly
Feature: ISC_DHCP DHCPv6 Tickets Prefix Length Pool Mismatch
    Tests ISC_DHCPD verifies fix for rt35378

@v6 @dhcp6 @PD @rfc3633 @ticket @rt35378
    Scenario: dhcpd.rt35378.prefix-len-mismatch
    # Test 01:
    #   Verifies that SOLICIT of a valid prefix/len returns an advertised
    #   prefix.
    # Test 02:
    #   Verifies that SOLICIT of mismatched prefix len
    #   returns None Available.
    # Test 03:
    #   Verifies that a REQUEST for a mismatched prefix length
    #   returns None Available.
    # Test 04:
    #   Verifies that a REBIND for a mismatched prefix, returns
    #   the prefix with lifetimes set to zero.
    # Test 05:
    #   Verifies that a REQUEST with a matched prefix length
    #   returns a lease
    # Test 06:
    #   Verifies that a RENEW with a matched prefix length
    #   returns the lease
    # Test 07:
    #   Verifies that a REBIND with a matched prefix length
    #   returns the lease
    # Test 08:
    #   Verifies that a REQUEST with a mismatched prefix length
    #   when there's an existing lease, returns the existing lease
    # Test 09:
    #   Verifies that a RENEW with a mismatched prefix length
    #   when there's an existing lease, returns No Binding
    # Test 10:
    #   Verifies that a REBIND with a mismatched prefix length
    #   when there's an existing lease, returns the mismatched
    #   preifx with lifetimes set to zero.
    Test Setup:
    Run configuration command: prefix-length-mode exact;
    Run configuration command: ddns-updates off;
    Run configuration command: authoritative;
    Run configuration command: subnet6 3000::/16 {
    Run configuration command:  pool6 {
    Run configuration command:   prefix6 3000:db8:0:100:: 3000:db8:0:100:: /56;
    Run configuration command:  }
    Send server configuration using SSH and config-file.
    DHCP server is started.

    # Verify SOLICIT of 3000:db8:0:100::/56 is valid
    Test Procedure: 01
    Client does include client-id.
    Client sets plen value to 56.
    Client sets prefix value to 3000:db8:0:100::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.

    Pass Criteria: 01
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response sub-option 26 from option 25 MUST contain preflft 3000.
    Response sub-option 26 from option 25 MUST contain validlft 4000.
    Response sub-option 26 from option 25 MUST contain plen 56.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

    # Save the client and server ids for REQUEST/RENEW tests
    Client saves into set no. 1 client-id option from received message.
    Client saves into set no. 1 server-id option from received message.

    # Verify SOLICIT of 3000:db8:0:100::/72 returns None Available
    Test Procedure: 02
    Client does include client-id.
    Client sets plen value to 72.
    Client sets prefix value to 3000:db8:0:100::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.

    Pass Criteria: 02
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 13.
    Response sub-option 13 from option 25 MUST contain statuscode 6.

    # Verify REQUEST for 3000:db8:0:100::/72, without a pre-existing
    # PD lease, returns None Available
    Test Procedure: 03
    Client adds saved options in set no. 1. And DONT Erase.
    Client sets plen value to 72.
    Client sets prefix value to 3000:db8:0:100::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends REQUEST message.

    Pass Criteria: 03
    Server MUST respond with REPLY message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 13.
    Response sub-option 13 from option 25 MUST contain statuscode 6.

    # Verify RENEW for 3000:db8:0:100::/72, without a pre-existing
    # PD lease,  returns No Binding
    Test Procedure: 04
    Client adds saved options in set no. 1. And DONT Erase.
    Client sets plen value to 72.
    Client sets prefix value to 3000:db8:0:100::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends RENEW message.

    Pass Criteria: 04
    Server MUST respond with REPLY message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 13.
    Response sub-option 13 from option 25 MUST contain statuscode 3.

    # Verify REBIND for 3000:db8:0:100::/72, without a pre-exisintg
    # PD lease returns the prefix with lifetimes set to 0
    Test Procedure: 05
    Client does include client-id.
    Client sets plen value to 72.
    Client sets prefix value to 3000:db8:0:100::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends REBIND message.

    Pass Criteria: 05
    Server MUST respond with REPLY message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response sub-option 26 from option 25 MUST contain preflft 0.
    Response sub-option 26 from option 25 MUST contain validlft 0.
    Response sub-option 26 from option 25 MUST contain plen 72.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

    # Verify REQUEST for 3000:db8:0:100::/56 returns a lease
    Test Procedure: 06
    Client adds saved options in set no. 1. And DONT Erase.
    Client sets plen value to 56.
    Client sets prefix value to 3000:db8:0:100::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends REQUEST message.

    Pass Criteria: 06
    Server MUST respond with REPLY message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response sub-option 26 from option 25 MUST contain preflft 3000.
    Response sub-option 26 from option 25 MUST contain validlft 4000.
    Response sub-option 26 from option 25 MUST contain plen 56.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

    # Verify RENEW for 3000:db8:0:100::/56 returns the prefix
    # with valid lifetimes
    Test Procedure: 07
    Client adds saved options in set no. 1. And DONT Erase.
    Client sets plen value to 56.
    Client sets prefix value to 3000:db8:0:100::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends RENEW message.

    Pass Criteria: 07
    Server MUST respond with REPLY message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response sub-option 26 from option 25 MUST contain preflft 3000.
    Response sub-option 26 from option 25 MUST contain validlft 4000.
    Response sub-option 26 from option 25 MUST contain plen 56.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

    # Verify REBIND for 3000:db8:0:100::/56 returns the prefix
    # with valid lifetimes
    Test Procedure: 08
    Client does include client-id.
    Client sets plen value to 56.
    Client sets prefix value to 3000:db8:0:100::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends REBIND message.

    Pass Criteria:  08
    Server MUST respond with REPLY message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response sub-option 26 from option 25 MUST contain preflft 3000.
    Response sub-option 26 from option 25 MUST contain validlft 4000.
    Response sub-option 26 from option 25 MUST contain plen 56.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

    # Verify REQUEST for 3000:db8:0:100::/72 (mismatch) when there's
    # an existing lease returns No Binding.  (If mode is ingore it
    # will return the prior, this is tested in a different
    # feature file, 45780.
    Test Procedure: 09
    Client adds saved options in set no. 1. And DONT Erase.
    Client sets plen value to 72.
    Client sets prefix value to 3000:db8:0:100::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends REQUEST message.

    Pass Criteria: 09
    Server MUST respond with REPLY message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 13.
    Response sub-option 13 from option 25 MUST contain statuscode 6.

    # Verify RENEW for 3000:db8:0:100::/72 (mismatch) when there's
    # an existing lease returns No Binding.
    Test Procedure: 10
    Client adds saved options in set no. 1. And DONT Erase.
    Client sets plen value to 72.
    Client sets prefix value to 3000:db8:0:100::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends RENEW message.

    Pass Criteria: 10
    Server MUST respond with REPLY message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 13.
    Response sub-option 13 from option 25 MUST contain statuscode 3.

    # Verify REBIND for 3000:db8:0:100::/72 (mismatch) when there's
    # an existing lease, should return the mismatch with lifetimes
    # set to zero.
    Test Procedure: 11
    Client does include client-id.
    Client sets plen value to 72.
    Client sets prefix value to 3000:db8:0:100::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends REBIND message.

    Pass Criteria: 11
    Server MUST respond with REPLY message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response sub-option 26 from option 25 MUST contain preflft 3000.
    Response sub-option 26 from option 25 MUST contain validlft 4000.
    Response sub-option 26 from option 25 MUST contain plen 72.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

