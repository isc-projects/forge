# WARNING: this is only a prototype of file; i need some feedback about
# whether it would be good, bad or totally bad;


Feature: DHCPv6 Client Prefix Delegation
    Test for basic Prefix Delegation for client, based on RFC 3633


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_onlyPD

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.

    References: RFC 3633


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_twoPDs

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is configured to include another IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.
    Client message MUST contain 2 options with opt-code 25.

    References: RFC 3633


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_prefixUsage

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 25.

    Test Procedure:
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST respond with REQUEST message.
    Client message MUST contain option 25.
    Client message option 25 MUST include sub-option 26.


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_check_options

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 8.
    Client message MUST contain option 25.

    References: RFC 3633 / RFC 3315


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_wrong_trid

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.

    Test Procedure:
    Server sets wrong trid value.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST NOT respond with REQUEST message.

    Test Procedure:
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.
    
    Test Procedure:
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST respond with REQUEST message.

    References: RFC 3633 / RFC 3315


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_wrong_cliduid

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.

    Test Procedure:
    Server sets wrong client_id value.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST NOT respond with REQUEST message.

    Test Procedure:
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.

    Test Procedure:
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST respond with REQUEST message.

    References: RFC 3633 / RFC 3315


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_rapid_commit

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is configured to include rapid_commit option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 25.
    Client message MUST contain option 14.

    Test Procedure:
    Server adds rapid_commit option to message.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back REPLY message.

    Pass Criteria:
    Client MUST use prefix with values given by server.


@v6 @client
    Scenario: prefix.delegation.client_rapid_commit_adv

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is configured to include rapid_commit option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 25.
    Client message MUST contain option 14.

    Test Procedure:
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST respond with REQUEST message.

    References: RFC 3315, section 17.1.4


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_wrong_rapid_commit

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is configured to include rapid_commit option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 25.
    Client message MUST contain option 14.

    Test Procedure:
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back REPLY message.

    Pass Criteria:
    Client MUST NOT use prefix with values given by server.


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_reply_success
    # TODO: test should check that client took values
    # from one of reply messages; however, if lease might
    # be checked, scapy_lease would be made from the 
    # latest reply message; so it's wrong. implement
    # some other checking on client lease file

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is configured to include rapid_commit option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 25.
    Client message MUST contain option 14.

    Test Procedure:
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST respond with REQUEST message.
    Client message MUST contain option 25.
    Client message option 25 MUST include sub-option 26.

    Test Procedure:
    Server builds new message.
    prefix value is set to 4321::.
    Server adds rapid_commit option to message.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back REPLY message.

    Server builds new message.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back REPLY message.

    References: RFC 3315, section 17.1.4


@v6 @PD  @client
    Scenario: prefix.delegation.client_renew_unicast
    # TODO: check that RENEW is sent to unicast address.

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 25.

    Test Procedure:
    Server adds server_unicast option to message.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST respond with REQUEST message.
    Client message MUST contain option 25.
    Client message option 25 MUST include sub-option 26.

    Test Procedure:
    Server builds new message.
    T1 value is set to 10.
    Server adds server_unicast option to message.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back REPLY message.

    References: RFC 3315, section 22.12


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_twoPrefixes

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Save iaid value.
    Client message MUST contain option 25.

    Test Procedure:
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST respond with REQUEST message.
    Client message MUST contain option 25.
    Client message option 25 MUST include sub-option 26.
    Client message MUST contain 2 sub-options with opt-code 26 within option 25.
    iaid value in client message is the same as saved one.


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_PD_timers_presence

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.
    Client message MUST contain T1 field in option 25.
    Client message MUST contain T2 field in option 25.

    References: RFC 3633, section 9


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_twoPrefixes_values

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 25.

    Test Procedure:
    prefix value is set to 3111::.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    prefix value is set to 3333::.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST respond with REQUEST message.
    Client message MUST contain option 25.
    Client message option 25 MUST include sub-option 26.
    Client message sub-option 26 from option 25 MUST contain prefix 3111::.
    Client message sub-option 26 from option 25 MUST contain prefix 3333::.


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_NoPrefixAvail

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 25.

    Test Procedure:
    Server adds IA_PD option to message.
    Server adds Status_Code 6 option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST NOT respond with REQUEST message.
    Sniffing client SOLICIT message from network.

    References: RFC 3633, Section 11.1


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_ignore_timers

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.

    Test Procedure:
    T1 value is set to 2000.
    T2 value is set to 1000.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    #Client must ignore IA_PD option
    Client MUST NOT respond with REQUEST message.
    Sniffing client SOLICIT message from network.
    Client message MUST contain option 25.
    Client message option 25 MUST NOT contain T1 2000.
    Client message option 25 MUST NOT contain T2 1000.

    Test Procedure:
    T1 value is set to 1000.
    T2 value is set to 2000.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server adds preference 10 option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST respond with REQUEST message.
    Client message MUST contain option 25.

    References: RFC 3633, Section: __


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_ignore_lifetimes

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.

    Test Procedure:
    preferred-lifetime value is set to 4000.
    valid-lifetime value is set to 3000.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    #Client must ignore IA_PD option
    Client MUST NOT respond with REQUEST message.
    Sniffing client SOLICIT message from network.
    Client message MUST contain option 25.

    Test Procedure:
    Server builds new message.
    preferred-lifetime value is set to 3000.
    valid-lifetime value is set to 4000.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST respond with REQUEST message.
    Client message MUST contain option 25.
    Client message option 25 MUST include sub-option 26.

    References: RFC 3633, Section: __


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_responseTime_measure

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.

    Test Procedure:
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST respond with REQUEST message.
    Client message MUST contain option 25.
    Client message option 25 MUST include sub-option 26.
    Message was sent after maximum 1.1 second.
    iaid value in client message is the same as saved one.

    References: RFC 3633, RFC 3315


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_diffPreferences

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 25.

    Test Procedure:
    Server adds preference 10 option to message.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Server builds new message.
    prefix value is set to 6665::.
    Server adds preference 20 option to message.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends ADVERTISE message.

    Server builds new message.
    prefix value is set to 4444::.
    Server adds preference 150 option to message.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends ADVERTISE message.

    Pass Criteria:
    Client MUST respond with REQUEST message.
    Client message MUST contain option 25.
    Client message option 25 MUST include sub-option 26.
    Client message sub-option 26 from option 25 MUST contain prefix 4444::.

    References: RFC 3633


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_preference255

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 25.

    Test Procedure:
    prefix value is set to 3366:beef::.
    Server adds preference 255 option to message.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Server builds new message.
    prefix value is set to 4444::.
    Server adds preference 150 option to message.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends ADVERTISE message.

    Pass Criteria:
    Client MUST respond with REQUEST message.
    Client message MUST contain option 25.
    Client message option 25 MUST include sub-option 26.
    Client message sub-option 26 from option 25 MUST contain prefix 3366:beef::.


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_leaseCheck

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.

    Test Procedure:
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST respond with REQUEST message.
    Client message MUST contain option 25.
    Client message option 25 MUST include sub-option 26.

    Test Procedure:
    Server sends back REPLY message.

    Pass Criteria:
    Client MUST use prefix with values given by server.

    References: RFC 3633 / RFC 3315


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_renew

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.

    Test Procedure:
    T1 value is set to 5.
    T2 value is set to 10.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST respond with REQUEST message.
    Client message MUST contain option 25.
    Client message option 25 MUST include sub-option 26.

    Test Procedure:
    Server sends back REPLY message.

    Pass Criteria:
    Client MUST use prefix with values given by server.

    Test Procedure:
    Sniffing client RENEW message from network.

    Pass Criteria:
    Message was sent after maximum 5 second.

    References: RFC 3633 / RFC 3315


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_rebind

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.

    Test Procedure:
    T1 value is set to 3.
    T2 value is set to 6.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST respond with REQUEST message.
    Client message MUST contain option 25.
    Client message option 25 MUST include sub-option 26.

    Test Procedure:
    Server sends back REPLY message.

    Pass Criteria:
    Client MUST use prefix with values given by server.

    Test Procedure:
    Sniffing client REBIND message from network.

    Pass Criteria:
    Message was sent after maximum 6 second.

    References: RFC 3633 / RFC 3315


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_choose_server
    # this step checks whether client stores information
    # about plural servers that have sent response;
    # if client did not receive reply for his request
    # message and retransmission count is equal to REQ_MAX_RC,
    # then client sends request to other server.

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.

    Test Procedure:
    Server adds preference 0 option to message.
    prefix-len value is set to 56.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Server builds new message.
    Server adds preference 100 option to message.
    Server adds preference 255 option to message.
    prefix value is set to 6666::.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends ADVERTISE message.

    Pass Criteria:
    Client MUST respond with REQUEST message.
    Client message MUST contain option 25.
    Client message option 25 MUST include sub-option 26.
    Client message sub-option 26 from option 25 MUST contain prefix 6666::.

    Test Procedure:
    # implement step that sniffs given count of messages.
    Sniffing client REQUEST message from network.
    Sniffing client REQUEST message from network.
    Sniffing client REQUEST message from network.
    Sniffing client REQUEST message from network.
    Sniffing client REQUEST message from network.
    Sniffing client REQUEST message from network.
    Sniffing client REQUEST message from network.
    Sniffing client REQUEST message from network.
    Sniffing client REQUEST message from network.

    Pass Criteria:
    # MRC reached.
    Sniffing client REQUEST message from network with timeout.
    Client message MUST contain option 25.
    Client message option 25 MUST include sub-option 26.
    Client message sub-option 26 from option 25 MUST contain plen 56.

    References: RFC 3315 / RFC 3633


################    useful tests end here.    ################


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_garbage

    Setting up test.

    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Client message MUST contain option 1.
    Client message MUST contain option 25.
    T1 value is set to 20.
    T2 value is set to 40.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    #    prefix value is set to 1234::.
    #    Server adds IA_Prefix option to message.
    #    Server adds IA_PD option to message.
    #    Server adds IA_Prefix option to message.
    #    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Client MUST respond with REQUEST message.

    #Client message MUST contain option 25.
    Server sends back REPLY message.
    Client MUST use prefix with values given by server.
    Sniffing client RENEW message from network.
    #Message was sent after maximum 10 second.
    #Client sent RELEASE message.
    #Server sends back REPLY message.
    Pause the Test.

    References: RFC 3633 / RFC 3315
