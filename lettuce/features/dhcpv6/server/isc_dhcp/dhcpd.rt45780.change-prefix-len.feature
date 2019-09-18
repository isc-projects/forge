# Tests ISC_DHCPD handles prefix-length hints when the mode is
# not ignored and returning clients solicit with different
# hints then their prior lease.
Feature: ISC_DHCP DHCPv6 Tickets Prefix Length Pool Mismatch
    Tests ISC_DHCPD verifies fix for rt45870 

@v6 @dhcp6 @PD @rfc3633 @ticket @rt45870
    Scenario: dhcpd.rt45780.change-prefix-len.exact

    Test Setup:
    Run configuration command: prefix-length-mode exact;
    Run configuration command: ddns-updates off;
    Run configuration command: authoritative;
    Run configuration command: subnet6 3000::/16 {
    Run configuration command:  pool6 {
    Run configuration command:   prefix6 3000:db8:0:100:: 3000:db8:0:100:: /64;
    Run configuration command:   prefix6 3000:db8:0:200:: 3000:db8:0:200:: /60;
    Run configuration command:  }
    Send server configuration using SSH and config-file.
    DHCP server is started.

    # Verify SOLICIT of /60 gets us a /60 prefix 
    Test Procedure: 01
    Client does include client-id.
    Client sets plen value to 60.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response sub-option 26 from option 25 MUST contain preflft 3000.
    Response sub-option 26 from option 25 MUST contain validlft 4000.
    Response sub-option 26 from option 25 MUST contain plen 60.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:200::.

    # Verify SOLICIT of /64 gets us a /64 prefix
    Test Procedure: 01
    Client does include client-id.
    Client sets plen value to 64.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response sub-option 26 from option 25 MUST contain preflft 3000.
    Response sub-option 26 from option 25 MUST contain validlft 4000.
    Response sub-option 26 from option 25 MUST contain plen 64.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

    # Save the client and server ids for REQUEST/RENEW tests
    Client saves into set no. 1 client-id option from received message.
    Client saves into set no. 1 server-id option from received message.

    # Verify REQUEST for 3000:db8:0:100::/64
    Test Procedure: 03
    Client adds saved options in set no. 1. And DONT Erase.
    Client sets plen value to 64.
    Client sets prefix value to 3000:db8:0:100::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response sub-option 26 from option 25 MUST contain preflft 3000.
    Response sub-option 26 from option 25 MUST contain validlft 4000.
    Response sub-option 26 from option 25 MUST contain plen 64.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

    # Verify RELEASE for 3000:db8:0:100::/64
    Test Procedure: 04
    Client adds saved options in set no. 1. And DONT Erase.
    Client sets plen value to 64.
    Client sets prefix value to 3000:db8:0:100::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends RELEASE message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 13.
    Response option 13 MUST contain statuscode 0.


    # Verify SOLICIT of /60 gets us a /60 prefix AFTER we released /64
    # when mode is not "ignore"
    Test Procedure: 01
    Client does include client-id.
    Client sets plen value to 60.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response sub-option 26 from option 25 MUST contain preflft 3000.
    Response sub-option 26 from option 25 MUST contain validlft 4000.
    Response sub-option 26 from option 25 MUST contain plen 60.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:200::.

##############################################################################
@v6 @dhcp6 @PD @rfc3633 @ticket @rt45870
    Scenario: dhcpd.rt45780.change-prefix-len.ignore

    Test Setup:
    Run configuration command: prefix-length-mode ignore;
    Run configuration command: ddns-updates off;
    Run configuration command: authoritative;
    Run configuration command: subnet6 3000::/16 {
    Run configuration command:  pool6 {
    Run configuration command:   prefix6 3000:db8:0:100:: 3000:db8:0:100:: /64;
    Run configuration command:   prefix6 3000:db8:0:200:: 3000:db8:0:200:: /60;
    Run configuration command:  }
    Send server configuration using SSH and config-file.
    DHCP server is started.

    # Verify SOLICIT of /60 gets us a /64 prefix as the hint
    # is ignored, giving us first available
    Test Procedure: 01
    Client does include client-id.
    Client sets plen value to 60.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response sub-option 26 from option 25 MUST contain preflft 3000.
    Response sub-option 26 from option 25 MUST contain validlft 4000.
    Response sub-option 26 from option 25 MUST contain plen 64.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

    # Save the client and server ids for REQUEST/RENEW tests
    Client saves into set no. 1 client-id option from received message.
    Client saves into set no. 1 server-id option from received message.

    # Verify REQUEST for 3000:db8:0:100::/64
    Test Procedure: 03
    Client adds saved options in set no. 1. And DONT Erase.
    Client sets plen value to 64.
    Client sets prefix value to 3000:db8:0:100::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response sub-option 26 from option 25 MUST contain preflft 3000.
    Response sub-option 26 from option 25 MUST contain validlft 4000.
    Response sub-option 26 from option 25 MUST contain plen 64.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.

    # Verify RELEASE for 3000:db8:0:100::/64
    Test Procedure: 04
    Client adds saved options in set no. 1. And DONT Erase.
    Client sets plen value to 64.
    Client sets prefix value to 3000:db8:0:100::.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends RELEASE message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 13.
    Response option 13 MUST contain statuscode 0.

    # Verify SOLICIT of /60 gets us our previous /64 prefix 
    # when mode is "ignore"
    Test Procedure: 01
    Client does include client-id.
    Client sets plen value to 60.
    Client does include IA_Prefix.
    Client does include IA-PD.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 25.
    Response option 25 MUST contain sub-option 26.
    Response sub-option 26 from option 25 MUST contain preflft 3000.
    Response sub-option 26 from option 25 MUST contain validlft 4000.
    Response sub-option 26 from option 25 MUST contain plen 64.
    Response sub-option 26 from option 25 MUST contain prefix 3000:db8:0:100::.
