# WARNING: this is only a prototype of file; i need some feedback about
# whether it would be good, bad or totally bad;
#
# Dibbler specific tests, focused on accepting/rejecting ia_pd
# options. tests concern situations where client is configured to
# enable insist-mode.


Feature: DHCPv6 Dibbler Client IA_PD tests with insist-mode
    Test correctness of received answer from server and make proper steps.


@v6 @PD @rfc3633 @client
    Scenario: dibbler.only.client.insist_1pd_1pref_OK
    # 1 IA_PD with 1 IA_Prefix included. Everything is
    # valid and client accepts received prefix.

    Setting up test.

    Test Procedure:
    Client is configured to include insist_mode option.
    Client is configured to include IA_PD option.
    Client is configured to include IA_Prefix option.
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
    Scenario: dibbler.only.client.insist_1pd_0pref_REJECT
    # 1 IA_PD with 0 IA_Prefix included.
    # There are no prefixes in IA_PD. Drop that answer.
    # Test includes checks if ADVERTISE and REPLY were rejected.

    Setting up test.

    Test Procedure:
    Client is configured to include insist_mode option.
    Client is configured to include IA_PD option.
    Client is configured to include IA_Prefix option.
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
    Client MUST NOT use prefix with values given by server.


    References: RFC 3633


@v6 @PD @rfc3633 @client
    Scenario: dibbler.only.client.insist_1pd_2pref_OK
    # 1 IA_PD with 2 IA_Prefix options included.
    # Everything is valid. Client accepts two prefixes.

    Setting up test.

    Test Procedure:
    Client is configured to include insist_mode option.
    Client is configured to include IA_PD option.
    Client is configured to include IA_Prefix option.
    prefix value is set to 1234::.
    Client is configured to include IA_Prefix option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.
    Client message option 25 MUST include sub-option 26.
    Client message MUST contain 2 sub-options with opt-code 26 within option 25.

    Test Procedure:
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    prefix value is set to 3000::.
    Server adds IA_Prefix option to message.
    prefix value is set to 1234::.
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
    Scenario: dibbler.only.client.insist_1pd_1pref_1prefWrong_OK
    # insist-mode is on.
    # 1 IA_PD with 2 IA_Prefix options included.
    # One of prefixes is not valid (validlft < preflft).
    # Drop the malformed prefix and accept valid one.

    Setting up test.

    Test Procedure:
    Client is configured to include insist_mode option.
    Client is configured to include IA_PD option.
    Client is configured to include IA_Prefix option.
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
    Scenario: dibbler.only.client.insist_2pd_OK
    # 2 IA_PDs with 1 IA_Prefix option included.
    # Everything is valid. Client accepts two prefixes
    # from two IA_PDs.

    Setting up test.

    Test Procedure:
    Client is configured to include insist_mode option.
    Client is configured to include IA_PD option.
    Client is configured to include IA_Prefix option.
    Client is configured to include another IA_PD option.
    prefix value is set to 1234::.
    Client is configured to include IA_Prefix option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.

    Test Procedure:
    Server adds IA_PD option to message.
    prefix value is set to 3000::.
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
    Scenario: dibbler.only.client.insist_1pdOK_1pd0pref_REJECT
    # 2 IA_PDs with 1 IA_Prefix option included.
    # One of IA_PD has no prefixes, therefore is not valid.
    # insist-mode is on, so if one of IA_PD is corrupted, answer
    # is not accepted.

    Setting up test.

    Test Procedure:
    Client is configured to include insist_mode option.
    Client is configured to include IA_PD option.
    Client is configured to include IA_Prefix option.
    Client is configured to include another IA_PD option.
    prefix value is set to 1234::.
    Client is configured to include IA_Prefix option.
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
    Client MUST NOT respond with REQUEST message.

    Test Procedure:
    Sniffing client SOLICIT message from network.

    Server builds new message.
    Server adds IA_PD option to message.
    prefix value is set to 1234::.
    Server adds IA_Prefix option to message.
    Server adds IA_PD option to message.
    prefix value is set to 3000::.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST respond with REQUEST message.

    Test Procedure:
    Server builds new message.
    Server adds IA_PD option to message.
    prefix value is set to 1234::.
    Server adds IA_Prefix option to message.
    Server adds IA_PD option to message.
    Server sends back REPLY message.

    Pass Criteria:
    Client MUST NOT use prefix with values given by server.

    References: RFC 3633


@v6 @PD @rfc3633 @client
    Scenario: dibbler.only.client.insist_2pd_2prefEach_OK
    # 2 IA_PDs with 2 IA_Prefix option included.
    # Everything is valid. Client accepts prefixes.

    Setting up test.

    Test Procedure:
    Client is configured to include insist_mode option.
    Client is configured to include IA_PD option.
    Client is configured to include IA_Prefix option.
    prefix value is set to 1234::.
    Client is configured to include IA_Prefix option.
    Client is configured to include another IA_PD option.
    prefix value is set to 1111::.
    Client is configured to include IA_Prefix option.
    prefix value is set to 4444::.
    Client is configured to include IA_Prefix option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.

    Test Procedure:
    Server adds IA_PD option to message.
    prefix value is set to 3000::.
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
    Scenario: dibbler.only.client.insist_2pd_1prefOK_1prefWrong_REJECT
    # 2 IA_PDs with 1 IA_Prefix option included.
    # One of prefixes is not valid, therefore the IA_PD
    # that was a parent of that prefix is not valid.
    # since insist-mode is enabled, message can not be accepted.

    Setting up test.

    Test Procedure:
    Client is configured to include insist_mode option.
    Client is configured to include IA_PD option.
    Client is configured to include IA_Prefix option.
    Client is configured to include another IA_PD option.
    prefix value is set to 1234::.
    Client is configured to include IA_Prefix option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.

    Test Procedure:
    Server adds IA_PD option to message.
    prefix value is set to 3000::.
    Server adds IA_Prefix option to message.
    Server adds IA_PD option to message.
    prefix value is set to 1234::.
    valid-lifetime value is set to 100.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST NOT respond with REQUEST message.

    Test Procedure:
    Sniffing client SOLICIT message from network.

    Server builds new message.
    Server adds IA_PD option to message.
    prefix value is set to 1234::.
    Server adds IA_Prefix option to message.
    Server adds IA_PD option to message.
    prefix value is set to 3000::.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST respond with REQUEST message.

    Test Procedure:
    Server builds new message.
    Server adds IA_PD option to message.
    prefix value is set to 3000::.
    Server adds IA_Prefix option to message.
    Server adds IA_PD option to message.
    prefix value is set to 1234::.
    valid-lifetime value is set to 100.
    Server adds IA_Prefix option to message.
    Server sends back REPLY message.

    Pass Criteria:
    Client MUST NOT use prefix with values given by server.


    References: RFC 3633
