# WARNING: this is only a prototype of file; i need some feedback about
# whether it would be good, bad or totally bad;
#
# Dibbler specific tests, focused on accepting/rejecting ia_pd
# options. tests concern situations where client insist-mode is
# not enabled.


Feature: DHCPv6 Dibbler Client IA_PD tests without insist-mode
    Test correctness of received answer from server and make proper steps.


@v6 @PD @rfc3633 @client
    Scenario: dibbler.only.client.1pd_1pref_OK
    # 1 IA_PD with 1 IA_Prefix included. Everything is
    # valid and client accepts received prefix.

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

    References: RFC 3633


@v6 @PD @rfc3633 @client
    Scenario: dibbler.only.client.1pd_0pref_REJECT
    # 1 IA_PD with 0 IA_Prefix included.
    # There are no prefixes in IA_PD. Drop that answer.
    # Test includes checks if ADVERTISE and REPLY were rejected.

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
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST NOT respond with REQUEST message.

    Test Procedure:
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.

    Test Procedure:
    Server builds new message.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST respond with REQUEST message.

    Test Procedure:
    Server builds new message.
    Server adds IA_PD option to message.
    Server sends back REPLY message.

    Pass Criteria:
    Sniffing client SOLICIT message from network.

    References: RFC 3633


@v6 @PD @rfc3633 @client
    Scenario: dibbler.only.client.1pd_2pref_OK
    # 1 IA_PD with 2 IA_Prefix options included.
    # Everything is valid. Client accepts two prefixes.

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
    prefix value is set to 1234::.
    Server adds IA_Prefix option to message.
    prefix value is set to 123::.
    valid-lifetime value is set to 123.
    Server adds IA_Prefix option to message.
    prefix value is set to 124::.
    valid-lifetime value is set to 1123.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST respond with REQUEST message.
    Client message MUST contain option 25.
    Client message option 25 MUST include sub-option 26.
    Client message sub-option 26 from option 25 MUST contain prefix 3000::.
    Client message sub-option 26 from option 25 MUST contain prefix 1234::.

    Test Procedure:
    # reply includes malformed prefixes. client should not assign them.
    Server sends back REPLY message.

    Pass Criteria:
    Client MUST NOT use prefix with values given by server.

    References: RFC 3633


@v6 @PD @rfc3633 @client
    Scenario: dibbler.only.client.1pd_1pref_1prefWrong_OK
    # insist-mode is off.
    # 1 IA_PD with 2 IA_Prefix options included.
    # One of prefixes is not valid (validlft < preflft).
    # Drop the malformed one and accept valid one.

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
    prefix value is set to 1234::.
    valid-lifetime value is set to 300.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST respond with REQUEST message.

    Test Procedure:
    Server sends back REPLY message.

    Pass Criteria:
    Client MUST NOT use prefix with values given by server.

    References: RFC 3633


@v6 @PD @rfc3633 @client
    Scenario: dibbler.only.client.2pd_OK
    # 2 IA_PDs with 1 IA_Prefix option included.
    # Everything is valid. Client accepts two prefixes
    # from two IA_PDs.

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is configured to include another IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.

    Test Procedure:
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server adds IA_PD option to message.
    prefix value is set to 1234::.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST respond with REQUEST message.
    Client message MUST contain option 25.
    Client message option 25 MUST include sub-option 26.
    Client message sub-option 26 from option 25 MUST contain prefix 3000::.
    Client message sub-option 26 from option 25 MUST contain prefix 1234::.
    
    Test Procedure:
    Server sends back REPLY message.

    Pass Criteria:
    Client MUST use prefix with values given by server.

    References: RFC 3633


@v6 @PD @rfc3633 @client
    Scenario: dibbler.only.client.1pdOK_1pd0pref_OK
    # 2 IA_PDs with 1 IA_Prefix option included.
    # One of IA_PD has no prefixes, therefore is not valid.
    # insist-mode is off, so if at least one IA_PD is valid, answer
    # is still accepted.

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is configured to include another IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.

    Test Procedure:
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    # second ia_pd has no ia_prefix option.
    Server adds IA_PD option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST respond with REQUEST message.
    Client message MUST contain option 25.
    Client message option 25 MUST include sub-option 26.
    Client message sub-option 26 from option 25 MUST contain prefix 3000::.

    Test Procedure:
    Server sends back REPLY message.

    Pass Criteria:
    Sniffing client SOLICIT message from network.


    References: RFC 3633


@v6 @PD @rfc3633 @client
    Scenario: dibbler.only.client.2pd_2prefEach_OK
    # 2 IA_PDs with 2 IA_Prefix option included.
    # Everything is valid. Client accepts prefixes.

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is configured to include another IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.

    Test Procedure:
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    prefix value is set to 1234::.
    Server adds IA_Prefix option to message.
    Server adds IA_PD option to message.
    prefix value is set to 1111::.
    Server adds IA_Prefix option to message.
    prefix value is set to 4444::.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST respond with REQUEST message.
    Client message MUST contain option 25.
    Client message option 25 MUST include sub-option 26.
    Client message sub-option 26 from option 25 MUST contain prefix 3000::.
    Client message sub-option 26 from option 25 MUST contain prefix 1234::.
    Client message sub-option 26 from option 25 MUST contain prefix 1111::.
    Client message sub-option 26 from option 25 MUST contain prefix 4444::.
    
    Test Procedure:
    Server sends back REPLY message.

    Pass Criteria:
    Client MUST use prefix with values given by server.

    References: RFC 3633


@v6 @PD @rfc3633 @client
    Scenario: dibbler.only.client.2pd_1prefOK_1prefWrong_OK
    # 2 IA_PDs with 1 IA_Prefix option included.
    # One of prefixes is not valid, therefore the IA_PD
    # that was a parent of that prefix is not valid.
    # insist-mode is off, so if at least one IA_PD is valid, answer
    # is still accepted.

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is configured to include another IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.

    Test Procedure:
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server adds IA_PD option to message.
    prefix value is set to 1234::.
    valid-lifetime value is set to 100.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST respond with REQUEST message.
    Client message MUST contain option 25.
    Client message option 25 MUST include sub-option 26.
    Client message sub-option 26 from option 25 MUST contain prefix 3000::.
    
    Test Procedure:
    Server sends back REPLY message.
    Pause the Test.

    Pass Criteria:
    # Client MUST use prefix with values given by server.

    References: RFC 3633
