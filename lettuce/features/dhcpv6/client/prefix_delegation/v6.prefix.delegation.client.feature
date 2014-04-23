Feature: DHCPv6 Client Prefix Delegation
    Test for basic Prefix Delegation for client, based on RFC 3633

@v6 @PD @rfc3633
    Scenario: prefix.delegation.client

    Test Procedure:
    Client is started.
    Client sent SOLICIT message.
    Server sends back ADVERTISE message.
    Client sent REQUEST message.
    Server sends back REPLY message.

    References: RFC 3315