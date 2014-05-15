# WARNING: this is only a prototype of file; i need some feedback about
# whether it would be good, bad or totally bad;


Feature: DHCPv6 Client Prefix Delegation
    Test for basic Prefix Delegation for client, based on RFC 3633


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.onlyPD

    Setting up test.

    #Client is configured to include IA_PD option.
    Client is started.
    Client sent SOLICIT message.

    Client message MUST contain option 1.
    Client message MUST contain option 25.

    References: RFC 3633


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_twoPDs

    Setting up test.

    Client is configured to include IA_PD option.
    Client is configured to include IA_PD option.
    Client is started.
    Client sent SOLICIT message.

    Client message MUST contain option 1.
    Client message MUST contain option 25.
    Client message MUST contain 2 options with opt-code 25.

    References: RFC 3633


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_twoPrefixes

    Setting up test.

    Client is configured to include IA_PD option.
    Client is started.
    Client sent SOLICIT message.

    Client message MUST contain option 25.
    Server adds IA_Prefix option to message.
    Server adds another IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Client sent REQUEST message.
    Client message MUST contain option 25.
    Client message option 25 MUST include sub-option 26.
    Client message MUST contain 2 sub-options with opt-code 26 within option 25.
    iaid value in client message is the same as saved one.


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.PD_timers_presence

    Setting up test.

    Client is configured to include IA_PD option.
    Client is started.
    Client sent SOLICIT message.

    Client message MUST contain option 1.
    Client message MUST contain option 25.
    T1 field MUST be present in option 25 from client message.
    T2 field MUST be present in option 25 from client message.

    References: RFC 3633, section 9


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_twoPrefixes_values

    Setting up test.

    Client is configured to include IA_PD option.
    Client is started.
    Client sent SOLICIT message.

    Client message MUST contain option 25.
    prefix value is set to 3111::.
    Server adds IA_Prefix option to message.
    prefix value is set to 3333::.
    Server adds another IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Client sent REQUEST message.
    Client message MUST contain option 25.
    Client message option 25 MUST include sub-option 26.
    Client message sub-option 26 from option 25 MUST contain prefix 3111::.
    Client message sub-option 26 from option 25 MUST contain prefix 3333::.


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_NoPrefixAvail

    Setting up test.

    Client is configured to include IA_PD option.
    Client is started.
    Client sent SOLICIT message.

    Client message MUST contain option 25.
    Server adds Status_Code 6 option to message.
    Server sends back ADVERTISE message.

    Client sent SOLICIT message.

    References: RFC 3633, Section 11.1


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_ignore_timers

    Setting up test.

    Client is configured to include IA_PD option.
    Client is started.
    Client sent SOLICIT message.

    Client message MUST contain option 1.
    Client message MUST contain option 25.
    T1 value is set to 2000.
    T2 value is set to 1000.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    #Client must ignore IA_PD option
    Client MUST NOT sent REQUEST message. Client sent SOLICIT message instead.
    Client message MUST contain option 25.
    Client message option 25 MUST NOT contain T1 2000.
    Client message option 25 MUST NOT contain T2 1000.

    T1 value is set to 1000.
    T2 value is set to 2000.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Client sent REQUEST message.
    Client message MUST contain option 25.

    References: RFC 3633, Section: __


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_ignore_lifetimes

    Setting up test.

    Client is configured to include IA_PD option.
    Client is started.
    Client sent SOLICIT message.

    Client message MUST contain option 1.
    Client message MUST contain option 25.
    preferred-lifetime value is set to 4000.
    valid-lifetime value is set to 3000.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    #Client must ignore IA_PD option
    Client MUST NOT sent REQUEST message. Client sent SOLICIT message instead.
    Client message MUST contain option 25.

    preferred-lifetime value is set to 3000.
    valid-lifetime value is set to 4000.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Client sent REQUEST message.
    Client message MUST contain option 25.
    Client message option 25 MUST include sub-option 26.

    References: RFC 3633, Section: __


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_responseTime_measure

    Setting up test.

    Client is configured to include IA_PD option.
    Client is started.
    Client sent SOLICIT message.

    Client message MUST contain option 1.
    Client message MUST contain option 25.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Client sent REQUEST message.
    Client message MUST contain option 25.
    Client message option 25 MUST include sub-option 26.
    Message was sent after at least 0.9 second.
    iaid value in client message is the same as saved one.

    References: RFC 3633, RFC 3315


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_diffPreferences

    Setting up test.

    Client is configured to include IA_PD option.
    Client is started.
    Client sent SOLICIT message.

    Client message MUST contain option 25.
    Server adds preference 10 option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Server builds new message.
    prefix value is set to 6665::.
    Server adds preference 20 option to message.
    Server adds IA_Prefix option to message.
    Server sends ADVERTISE message.

    Server builds new message.
    prefix value is set to 4444::.
    Server adds preference 150 option to message.
    Server adds IA_Prefix option to message.
    Server sends ADVERTISE message.

    Client sent REQUEST message.
    Client message MUST contain option 25.
    Client message option 25 MUST include sub-option 26.
    Client message sub-option 26 from option 25 MUST contain prefix 4444::.

    References: RFC 3633


@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_preference255

    Setting up test.

    Client is configured to include IA_PD option.
    Client is started.
    Client sent SOLICIT message.

    Client message MUST contain option 25.
    prefix value is set to 3366:beef::.
    Server adds preference 255 option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Server builds new message.
    prefix value is set to 4444::.
    Server adds preference 150 option to message.
    Server adds IA_Prefix option to message.
    Server sends ADVERTISE message.

    Client sent REQUEST message.
    Client message MUST contain option 25.
    Client message option 25 MUST include sub-option 26.
    Client message sub-option 26 from option 25 MUST contain prefix 3366:beef::.


################    useful tests end here.    ################




@v6 @PD @rfc3633 @client
    Scenario: prefix.delegation.client_garbage

    Setting up test.

    Client is configured to include IA_PD option.
    Client is started.
    Client sent SOLICIT message.

    Client message MUST contain option 1.
    Client message MUST contain option 25.
    Server adds preference 0 option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Client sent REQUEST message.

    Client message MUST contain option 25.
    Server sends back REPLY message.
    #Client sent RELEASE message.
    #Server sends back REPLY message.
    #Pause the Test.

    References: RFC 3633 / RFC 3315
