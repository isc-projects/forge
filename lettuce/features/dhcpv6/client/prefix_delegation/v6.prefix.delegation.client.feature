Feature: DHCPv6 Client Prefix Delegation
    Test for basic Prefix Delegation for client, based on RFC 3633

@v6 @PD @rfc3633
    Scenario: prefix.delegation.client

    Setting up test.
    Client is configured to request IA_PD option.
    Client is started.
    Client sent SOLICIT message.

    Client message MUST contain option 25.
    Server sends back ADVERTISE message.
    Client sent REQUEST message.
    Server sends back REPLY message.

    References: RFC 3633