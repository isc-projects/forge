# WARNING: this is only a prototype of file; i need some feedback about
# whether it would be good, bad or totally bad;


Feature: DHCPv6 Client Advertise Message Validation
    Basic client advertise message validation, based on RFC 3633 / RFC 3315


@v6 @client
    Scenario: message.validation.client_invalid_adv_oro

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.

    Test Procedure:
    Server adds option_request option to message.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST NOT respond with REQUEST message.
    Sniffing client SOLICIT message from network.

    References: RFC 3315, section 22.7


@v6 @client
    Scenario: message.validation.client_invalid_adv_srv_unicast

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.

    Test Procedure:
    # Server unicast option can appear only in REPLY.
    Server adds server_unicast option to message.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST NOT respond with REQUEST message.
    Sniffing client SOLICIT message from network.

    References: RFC 3315, section 22.12


@v6 @client
    Scenario: message.validation.client_invalid_adv_rapid_commit

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.

    Test Procedure:
    Server adds rapid_commit option to message.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST NOT respond with REQUEST message.
    Sniffing client SOLICIT message from network.

    References: RFC 3315, section 22.14


@v6 @client
    Scenario: message.validation.client_invalid_adv_elapsed_time

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.

    Test Procedure:
    Server adds elapsed_time option to message.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST NOT respond with REQUEST message.
    Sniffing client SOLICIT message from network.

    References: RFC 3315, section 22.9


@v6 @client
    Scenario: message.validation.client_invalid_adv_iface_id

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.

    Test Procedure:
    Server adds iface_id option to message.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST NOT respond with REQUEST message.
    Sniffing client SOLICIT message from network.

    References: RFC 3315, section 22.18


@v6 @client
    Scenario: message.validation.client_invalid_adv_reconf

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.

    Test Procedure:
    Server adds reconfigure option to message.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST NOT respond with REQUEST message.
    Sniffing client SOLICIT message from network.

    References: RFC 3315, section 22.19


@v6 @client
    Scenario: message.validation.client_adv_without_cli_id

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.

    Test Procedure:
    Server does NOT add client_id option to message.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST NOT respond with REQUEST message.
    Sniffing client SOLICIT message from network.

    References: RFC 3315


@v6 @client
    Scenario: message.validation.client_adv_without_srv_id

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.

    Test Procedure:
    Server does NOT add server_id option to message.
    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST NOT respond with REQUEST message.
    Sniffing client SOLICIT message from network.

    References: RFC 3315
