# WARNING: this is only a prototype of file; i need some feedback about
# whether it would be good, bad or totally bad;


Feature: DHCPv6 Client Message Validation
    Basic client message validation, based on RFC 3633 / RFC 3315

@v6 @rfc3315 @basic @client
    Scenario: message.validation.client_elapsed_time

    Setting up test.

    Client is started.
    Sniffing client SOLICIT message from network.

    Client message MUST contain option 1.
    Client message MUST contain option 8.

    References: RFC 3315, section 22.9


@v6 @rfc3315 @basic @client
    Scenario: message.validation.client_unique_IAID

    Setting up test.

    Client is started.
    Sniffing client SOLICIT message from network.

    Client message MUST contain option 1.
    Client message MUST contain option 8.

    Restart client.
    Sniffing client SOLICIT message from network.
    IAID value in client message is the same as saved one.

    References: RFC 3315, section 22.9


@v6 @rfc3315 @basic @client
    Scenario: message.validation.client_rapid_commit

    Setting up test.

    Client is configured to include rapid_commit option.
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Client message MUST contain option 1.
    Client message MUST contain option 8.
    Client message MUST contain option 14.
    Client message MUST contain option 25.

    References: RFC 3315, section 22.9