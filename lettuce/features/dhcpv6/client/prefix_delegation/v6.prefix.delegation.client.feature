Feature: DHCPv6 Client Prefix Delegation
    Test for basic Prefix Delegation for client, based on RFC 3633

@v6 @PD @rfc3633
    Scenario: prefix.delegation.client

    Test Procedure:
    Client testing...
    Server receives SOLICIT message from client.
    Server answers with ADVERTISE message.
    Server receives REQUEST message from client.
    Server answers with REPLY message.

    References: RFC 3315