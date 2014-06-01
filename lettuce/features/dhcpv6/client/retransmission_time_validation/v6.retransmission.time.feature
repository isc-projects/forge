# WARNING: this is only a prototype of file; i need some feedback about
# whether it would be good, bad or totally bad;


Feature: DHCPv6 Client retransmission times
    Test for measuring message retransmission times for specifig messages.

    #Parameter        Default  Description
    #-------------------------------------
    #SOL_MAX_DELAY     1 sec   Max delay of first Solicit
    #SOL_TIMEOUT       1 sec   Initial Solicit timeout
    #SOL_MAX_RT      120 secs  Max Solicit timeout value
    #REQ_TIMEOUT       1 sec   Initial Request timeout
    #REQ_MAX_RT       30 secs  Max Request timeout value
    #REQ_MAX_RC       10       Max Request retry attempts
    #CNF_MAX_DELAY     1 sec   Max delay of first Confirm
    #CNF_TIMEOUT       1 sec   Initial Confirm timeout
    #CNF_MAX_RT        4 secs  Max Confirm timeout
    #CNF_MAX_RD       10 secs  Max Confirm duration
    #REN_TIMEOUT      10 secs  Initial Renew timeout
    #REN_MAX_RT      600 secs  Max Renew timeout value
    #REB_TIMEOUT      10 secs  Initial Rebind timeout
    #REB_MAX_RT      600 secs  Max Rebind timeout value
    #INF_MAX_DELAY     1 sec   Max delay of first Information-request
    #INF_TIMEOUT       1 sec   Initial Information-request timeout
    #INF_MAX_RT      120 secs  Max Information-request timeout value
    #REL_TIMEOUT       1 sec   Initial Release timeout
    #REL_MAX_RC        5       MAX Release attempts
    #DEC_TIMEOUT       1 sec   Initial Decline timeout
    #DEC_MAX_RC        5       Max Decline attempts
    #REC_TIMEOUT       2 secs  Initial Reconfigure timeout
    #REC_MAX_RC        8       Max Reconfigure attempts
    #HOP_COUNT_LIMIT  32       Max hop count in a Relay-forward message


@v6 @RT @client
    Scenario: retransmission.time.client_solicit_retransmit_adv_no_wait

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Client message MUST contain option 1.
    Client message MUST contain option 25.

    Test Procedure:
    Sniffing client SOLICIT message from network.

    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST respond with REQUEST message.
    Client message MUST contain option 25.
    Client message option 25 MUST include sub-option 26.
    Message was sent after maximum 0.1 second.

    References: RFC 3315, section 17.1.2


@v6 @RT @client
    Scenario: retransmission.time.client_sol_max_rt
    # SOLICIT MRT = SOL_MAX_RT = 120s
    # each subsequent rt:
    # RT = 2*RTprev + RAND*RTprev
    # if (RT > MRT)
    # RT = MRT + RAND*MRT

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Retransmission time has required value.

    Test Procedure:
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Retransmission time has required value.

    Test Procedure:
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Retransmission time has required value.

    Test Procedure:
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Retransmission time has required value.

    Test Procedure:
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Retransmission time has required value.

    Test Procedure:
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Retransmission time has required value.

    Test Procedure:
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Retransmission time has required value.

    Test Procedure:
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Message was retransmitted after maximum 128 seconds.

    Test Procedure:
    Sniffing client SOLICIT message from network.

    Pass Criteria:
    Message was retransmitted after maximum 128 seconds.


@v6 @RT @client
    Scenario: retransmission.time.client_req_max_rt
    # REQUEST MRT = REQ_MAX_RT = 30s
    # each subsequent rt:
    # RT = 2*RTprev + RAND*RTprev
    # if (RT > MRT)
    # RT = MRT + RAND*MRT

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

    Test Procedure:
    Sniffing client REQUEST message from network.

    Pass Criteria:
    Retransmission time has required value.

    Test Procedure:
    Sniffing client REQUEST message from network.

    Pass Criteria:
    Retransmission time has required value.

    Test Procedure:
    Sniffing client REQUEST message from network.

    Pass Criteria:
    Retransmission time has required value.

    Test Procedure:
    Sniffing client REQUEST message from network.

    Pass Criteria:
    Retransmission time has required value.

    Test Procedure:
    Sniffing client REQUEST message from network.

    Pass Criteria:
    Retransmission time has required value.

    Test Procedure:
    Sniffing client REQUEST message from network.

    Pass Criteria:
    Message was retransmitted after maximum 35 seconds.

    Test Procedure:
    Sniffing client REQUEST message from network.

    Pass Criteria:
    Message was retransmitted after maximum 35 seconds.

    References: RFC 3315 / RFC 3633


@v6 @RT @client
    Scenario: retransmission.time.client_solicit_first_RT
    # SOLICIT first RT :
    # IRT = SOL_TIMEOUT
    # RT = IRT + RAND*IRT

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Sniffing client SOLICIT message from network.

    Pass Criteria:
    # <0.9, 1.1>
    Retransmission time has required value.

    References: RFC 3315


@v6 @RT @client
    Scenario: retransmission.time.client_request_first_RT
    # REQUEST first RT :
    # IRT = REQ_TIMEOUT
    # RT = IRT + RAND*IRT

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST respond with REQUEST message.

    Test Procedure:
    Sniffing client REQUEST message from network.

    Pass Criteria:
    # <0.9, 1.1>
    Retransmission time has required value.

    References: RFC 3315


@v6 @RT @client
    Scenario: retransmission.time.client_request_MRC
    # MRC = REQ_MAX_RC = 10

    Setting up test.

    Test Procedure:
    Client is configured to include IA_PD option.
    Client is started.
    Sniffing client SOLICIT message from network.

    Server adds IA_PD option to message.
    Server adds IA_Prefix option to message.
    Server sends back ADVERTISE message.

    Pass Criteria:
    Client MUST respond with REQUEST message.

    Test Procedure:
    Sniffing client REQUEST message from network.
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
    Sniffing client SOLICIT message from network.

    References: RFC 3315


