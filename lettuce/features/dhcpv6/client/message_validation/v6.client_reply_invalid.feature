# WARNING: this is only a prototype of file; i need some feedback about
# whether it would be good, bad or totally bad;


Feature: DHCPv6 Client Prefix Delegation
    Test for client behavior on receiving invalid reply message, RFC 3315


@v6 @client
    Scenario: prefix.delegation.client_invalid_reply_oro

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
    Server builds new message.
    Server adds option_request option to message.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back REPLY message.

    Pass Criteria:
    Client MUST NOT use prefix with values given by server.

    References: RFC 3315, section 22.7


@v6 @client
    Scenario: prefix.delegation.client_invalid_reply_elapsed_time

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
    Server builds new message.
    Server adds elapsed_time option to message.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back REPLY message.

    Pass Criteria:
    Client MUST NOT use prefix with values given by server.

    References: RFC 3315, section 22.7


@v6 @client
    Scenario: prefix.delegation.client_invalid_reply_relay_msg

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
    Server builds new message.
    Server adds relay_message option to message.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back REPLY message.

    Pass Criteria:
    Client MUST NOT use prefix with values given by server.

    References: RFC 3315, section 22.10


@v6 @client
    Scenario: prefix.delegation.client_invalid_reply_iface_id

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
    Server builds new message.
    Server adds iface_id option to message.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back REPLY message.

    Pass Criteria:
    Client MUST NOT use prefix with values given by server.

    References: RFC 3315, section 22.18


@v6 @client
    Scenario: prefix.delegation.client_invalid_reply_reconfigure

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
    Server builds new message.
    Server adds reconfigure option to message.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back REPLY message.

    Pass Criteria:
    Client MUST NOT use prefix with values given by server.

    References: RFC 3315, section 22.19


@v6 @client
    Scenario: prefix.delegation.client_reply_without_srv_id

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
    Server builds new message.
    Server does NOT add server_id option to message.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back REPLY message.

    Pass Criteria:
    Client MUST NOT use prefix with values given by server.

    References: RFC 3315


@v6 @client
    Scenario: prefix.delegation.client_reply_without_cli_id

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
    Server builds new message.
    Server does NOT add client_id option to message.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back REPLY message.

    Pass Criteria:
    Client MUST NOT use prefix with values given by server.

    References: RFC 3315


@v6 @client
    Scenario: prefix.delegation.client_reply_wrong_trid

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
    Server builds new message.
    Server sets wrong trid value.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back REPLY message.

    Pass Criteria:
    Client MUST NOT use prefix with values given by server.
    Sniffing client REQUEST message from network.


    References: RFC 3315




