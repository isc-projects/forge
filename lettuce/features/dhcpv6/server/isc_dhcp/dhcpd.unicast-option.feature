# Tests ISC_DHCPD DHCPv6 unicast feature 
Feature: ISC_DHCP DHCPv6 feature unicast
    Tests ISC_DHCPD DHCPv6 support for accepting/reject unicast messages
    dependent on whether or not the dhcp6.unicast option is defined.

################################################################################
@v6 @dhcp6 @NA @rfc3315 @feature @unicast-option
    Scenario: dhcpd.feature.unicast-option.defined
    # Tests that REQUEST, RENEW, RELEASE, and DECLINE can be sent
    # unicast when unicast option is defined.
    #
    # Step 1: Client SOLICITs requesting unicast option
    #  - server should advertise an address and include unicast option
    # Step 2: Client REQUESTs advertised address via unicast
    #  - server should reply (grant) the address
    # Step 3: Client RENEWs advertised address via unicast
    #  - server should reply (grant) the address
    # Step 4: Client RELEASEs granted address via unicast
    #  - server should reply with success status code
    # Step 5: Client SOLICITs requesting unicast option
    #  - server should advertise an address and include unicast option
    # Step 6: Client declines offered  address via unicast
    #  - server should reply with success status code
    #
    Test Setup:
    Run configuration command: ddns-updates off;
    Run configuration command: option dhcp6.unicast 3000::;
    Run configuration command: authoritative;
    Run configuration command: subnet6 3000::/16 {
    Run configuration command:  pool6 {
    Run configuration command:   range6 3000:: 3000::1;
    Run configuration command:  }
    Send server configuration using SSH and config-file.
    DHCP server is started.

    ###############################################################
    # Step 1: Client SOLICITs requesting unicast option
    #  - server should advertise an address and include unicast option
    ###############################################################
    Test Procedure: 01
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client does include client-id.
    Client does include IA-NA.
    Client requests option 12.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response MUST include option 12.

    ###############################################################
    # Step 2: Client REQUESTs advertised address via unicast
    #  - server should reply (grant) the address
    ###############################################################
    Test Procedure: 02
    Client chooses GLOBAL UNICAST address.
    Client copies IA_NA option from received message.
    Client copies client-id option from received message.
    Client copies server-id option from received message.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.

    ###############################################################
    # Step 3: Client RENEWs advertised address via unicast
    #  - server should reply (renew) the address
    ###############################################################
    Test Procedure: 03
    Client chooses GLOBAL UNICAST address.
    Client copies IA_NA option from received message.
    Client copies client-id option from received message.
    Client copies server-id option from received message.
    Client sends RENEW message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.

    ###############################################################
    # Step 4: Client RELEASEs granted address via unicast
    #  - server should reply with success status code
    ###############################################################
    Test Procedure: 04
    Client chooses GLOBAL UNICAST address.
    Client copies IA_NA option from received message.
    Client copies client-id option from received message.
    Client copies server-id option from received message.
    Client sends RELEASE message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 13.
    Response option 13 MUST contain statuscode 0.

    ###############################################################
    # Step 5: Client SOLICITs requesting unicast option
    #  - server should advertise an address and include unicast option
    ###############################################################
    Test Procedure: 05
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client does include client-id.
    Client does include IA-NA.
    Client requests option 12.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response MUST include option 12.

    ###############################################################
    # Step 6: Client declines offered  address via unicast
    #  - server should reply with success status code
    ###############################################################
    Test Procedure: 06
    Client chooses GLOBAL UNICAST address.
    Client copies IA_NA option from received message.
    Client copies client-id option from received message.
    Client copies server-id option from received message.
    Client sends DECLINE message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 13.
    Response option 13 MUST contain statuscode 0.

################################################################################
@v6 @dhcp6 @NA @rfc3315 @feature @unicast-option
    Scenario: dhcpd.feature.unicast-option.not_defined
    # Tests that REQUEST, RENEW, RELEASE, and DECLINE sent via unicast are 
    # rejected when the dhcp6.unicast option is NOT defined.
    #
    # Step 1: Client SOLICITs requesting unicast option
    #  - server should advertise an address without unicast option
    # Step 2: Client REQUESTs advertised address via unicast
    #  - server should reject with status code of 5 
    # Step 3: Client RENEWs advertised address via unicast
    #  - server should reject with status code of 5 
    # Step 4: Client RELEASEs granted address via unicast
    #  - server should reject with status code of 5 
    # Step 5: Client SOLICITs requesting unicast option
    #  - server should advertise an address without unicast option
    # Step 6: Client declines offered  address via unicast
    #  - server should reject with status code of 5 
    #
    Test Setup:
    Run configuration command: ddns-updates off;
    Run configuration command: authoritative;
    Run configuration command: subnet6 3000::/16 {
    Run configuration command:  pool6 {
    Run configuration command:   range6 3000:: 3000::1;
    Run configuration command:  }
    Send server configuration using SSH and config-file.
    DHCP server is started.

    ###############################################################
    # Step 1: Client SOLICITs requesting unicast option
    #  - server should advertise an address and include unicast option
    ###############################################################
    Test Procedure: 07
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client does include client-id.
    Client does include IA-NA.
    Client requests option 12.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response MUST NOT include option 12.
    Client saves into set no. 1 IA_NA option from received message.
    Client saves into set no. 1 client-id option from received message.
    Client saves into set no. 1 server-id option from received message.

    ###############################################################
    # Step 2: Client REQUESTs advertised address via unicast
    #  - server should reply with status code = 5
    ###############################################################
    Test Procedure: 08
    Client chooses GLOBAL UNICAST address.
    Client adds saved options in set no. 1. and DONT Erase.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST NOT include option 3.
    Response MUST include option 13.
    Response option 13 MUST contain statuscode 5.

    ###############################################################
    # Step 3: Client RENEWs advertised address via unicast
    #  - server should reply with status code = 5
    ###############################################################
    Test Procedure: 09
    Client chooses GLOBAL UNICAST address.
    Client adds saved options in set no. 1. and DONT Erase.
    Client sends RENEW message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST NOT include option 3.
    Response MUST include option 13.
    Response option 13 MUST contain statuscode 5.

    ###############################################################
    # Step 4: Client RELEASEs granted address via unicast
    #  - server should reply with status code = 5
    ###############################################################
    Test Procedure: 10
    Client chooses GLOBAL UNICAST address.
    Client adds saved options in set no. 1. and DONT Erase.
    Client sends RELEASE message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 13.
    Response option 13 MUST contain statuscode 5.

    ###############################################################
    # Step 5: Client SOLICITs requesting unicast option
    #  - server should advertise an address without unicast option
    ###############################################################
    Test Procedure: 11
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client does include client-id.
    Client does include IA-NA.
    Client requests option 12.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response MUST NOT include option 12.

    ###############################################################
    # Step 6: Client declines offered address via unicast
    #  - server should reply with status code = 5
    ###############################################################
    Test Procedure: 12
    Client chooses GLOBAL UNICAST address.
    Client copies IA_NA option from received message.
    Client copies client-id option from received message.
    Client copies server-id option from received message.
    Client sends DECLINE message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 13.
    Response option 13 MUST contain statuscode 5.

################################################################################
@v6 @dhcp6 @NA @rfc3315 @feature @unicast-option
    Scenario: dhcpd.feature.unicast-option.defined.subnet
    # Tests that IA_NA REQUEST can be sent unicast when unicast option is 
    # defined for the subnet.
    #
    # Step 1: Client SOLICITs requesting unicast option
    #  - server should advertise an address and include unicast option
    #
    # Step 2: Client REQUESTs advertised address via unicast
    #  - server should reply (grant) the address
    
    Test Setup:
    Run configuration command: ddns-updates off;
    Run configuration command: authoritative;
    Run configuration command: subnet6 3000::/16 {
    Run configuration command:   option dhcp6.unicast 3000::;
    Run configuration command:   pool6 {
    Run configuration command:     range6 3000:: 3000::1;
    Run configuration command:  }
    Send server configuration using SSH and config-file.
    DHCP server is started.

    ###############################################################
    # Step 1: Client SOLICITs requesting unicast option
    #  - server should advertise an address and include unicast option
    ###############################################################
    Test Procedure: 13
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client does include client-id.
    Client does include IA-NA.
    Client requests option 12.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response MUST include option 12.

    ###############################################################
    # Step 2: Client REQUESTs advertised address via unicast
    #  - server should reply (grant) the address
    ###############################################################
    Test Procedure: 14
    Client chooses GLOBAL UNICAST address.
    Client copies IA_NA option from received message.
    Client copies client-id option from received message.
    Client copies server-id option from received message.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.

################################################################################
@v6 @dhcp6 @NA @rfc3315 @feature @unicast-option
    Scenario: dhcpd.feature.unicast-option.defined.shared-network
    # Tests that IA_NA REQUEST can be sent unicast when unicast option is 
    # defined for the shared-subnet.
    #
    # Step 1: Client SOLICITs requesting unicast option
    #  - server should advertise an address and include unicast option
    #
    # Step 2: Client REQUESTs advertised address via unicast
    #  - server should reply (grant) the address
    
    Test Setup:
    Run configuration command: ddns-updates off;
    Run configuration command: authoritative;
    Run configuration command: shared-network net1 {
    Run configuration command:     option dhcp6.unicast 3000::;
    Run configuration command:     subnet6 3000::/16 {
    Run configuration command:     pool6 {
    Run configuration command:       range6 3000:: 3000::1;
    Run configuration command:     }
    Run configuration command:   }
    Send server configuration using SSH and config-file.
    DHCP server is started.

    ###############################################################
    # Step 1: Client SOLICITs requesting unicast option
    #  - server should advertise an address and include unicast option
    ###############################################################
    Test Procedure: 15
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client does include client-id.
    Client does include IA-NA.
    Client requests option 12.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response MUST include option 12.

    ###############################################################
    # Step 2: Client REQUESTs advertised address via unicast
    #  - server should reply (grant) the address
    ###############################################################
    Test Procedure: 16
    Client chooses GLOBAL UNICAST address.
    Client copies IA_NA option from received message.
    Client copies client-id option from received message.
    Client copies server-id option from received message.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.

################################################################################
@v6 @dhcp6 @PD @rfc3315 @feature @unicast-option
    Scenario: dhcpd.feature.unicast-option.defined.IA_PD
    # Tests that IA_PD REQUEST can be sent unicast when unicast option is 
    # defined.
    #
    # Step 1: Client SOLICITs requesting unicast option
    #  - server should advertise an address and include unicast option
    #
    # Step 2: Client REQUESTs advertised address via unicast
    #  - server should reply (grant) the address
    
    Test Setup: 17
    Run configuration command: ddns-updates off;
    Run configuration command: authoritative;
    Run configuration command: subnet6 3000::/64 {
    Run configuration command:   option dhcp6.unicast 3000::;
    Run configuration command:   pool6 {
    Run configuration command:     prefix6 3000:0:0:0:100:: 3000:0:0:0:0200:: /80;
    Run configuration command:   }
    Send server configuration using SSH and config-file.
    DHCP server is started.

    ###############################################################
    # Step 1: Client SOLICITs requesting unicast option
    #  - server should advertise an address and include unicast option
    ###############################################################
    Test Procedure: 18
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

    ###############################################################
    # Step 2: Client REQUESTs advertised address via unicast
    #  - server should reply (grant) the address
    ###############################################################
    Test Procedure: 19
    Client chooses GLOBAL UNICAST address.
    Client copies IA_PD option from received message.
    Client copies client-id option from received message.
    Client copies server-id option from received message.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response option 25 MUST contain sub-option 26.

################################################################################
@v6 @dhcp6 @PD @rfc3315 @feature @unicast-option
    Scenario: dhcpd.feature.unicast-option.defined.IA_TA
    # Tests that IA_TA REQUEST can be sent unicast when unicast option is 
    # defined. 
    #
    # ##################################################################
    # ##################################################################
    # 
    # @TODO  THIS TEST WILL FAIL UNTIL FORGE SUPPORTS IA_TA
    # 
    # ##################################################################
    # ##################################################################
    #
    # Step 1: Client SOLICITs requesting unicast option
    #  - server should advertise an address and include unicast option
    #
    # Step 2: Client REQUESTs advertised address via unicast
    #  - server should reply (grant) the address
    
    Test Setup:
    Run configuration command: ddns-updates off;
    Run configuration command: authoritative;
    Run configuration command: subnet6 3000::/64 {
    Run configuration command:   option dhcp6.unicast 3000::;
    Run configuration command:   pool6 {
    Run configuration command:       range6 3000:: temporary; 
    Run configuration command:   }
    Send server configuration using SSH and config-file.
    DHCP server is started.

    ###############################################################
    # Step 1: Client SOLICITs requesting unicast option
    #  - server should advertise an address and include unicast option
    ###############################################################
    Test Procedure: 20
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client does include client-id.
    Client does include IA_TA.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response MUST include option 12.

    ###############################################################
    # Step 2: Client REQUESTs advertised address via unicast
    #  - server should reply (grant) the address
    ###############################################################
    Test Procedure: 21
    Client chooses GLOBAL UNICAST address.
    Client copies IA_TA option from received message.
    Client copies client-id option from received message.
    Client copies server-id option from received message.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 4.
    Response option 4 MUST contain sub-option 5.
