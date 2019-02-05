"""DHCPv6 Client Prefix Delegation"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import references
from features import clnt_msg
from features import clnt_control
from features import misc


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_onlyPD(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_twoPDs(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_option_req(step, 'another ', 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '25')
    clnt_msg.client_msg_count_opt(step, None, '2', '25')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_IAPrefix_opt(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(step, None, '25')
    clnt_msg.client_msg_contains_subopt(step, '25', None, '26')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_check_options(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '8')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_wrong_trid(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.server_set_wrong_val(step, 'trid')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, 'NOT ', 'REQUEST')

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, None, 'REQUEST')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_wrong_cliduid(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.server_set_wrong_val(step, 'client_id')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, 'NOT ', 'REQUEST')

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, None, 'REQUEST')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_rapid_commit(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'rapid_commit')
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '25')
    clnt_msg.client_msg_contains_opt(step, None, '14')

    misc.test_procedure(step)
    clnt_msg.add_option(step, 'rapid_commit', None)
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'REPLY')

    misc.pass_criteria(step)
    clnt_control.client_parse_config(step, None)

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.client
def test_prefix_delegation_client_rapid_commit_adv(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'rapid_commit')
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '25')
    clnt_msg.client_msg_contains_opt(step, None, '14')

    misc.test_procedure(step)
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, None, 'REQUEST')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_wrong_rapid_commit(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'rapid_commit')
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '25')
    clnt_msg.client_msg_contains_opt(step, None, '14')

    misc.test_procedure(step)
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'REPLY')

    misc.pass_criteria(step)
    clnt_control.client_parse_config(step, 'NOT ')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_reply_success(step):
    # TODO: test should check that client took values
    # from one of reply messages; however, if lease might
    # be checked, scapy_lease would be made from the
    # latest reply message; so it's wrong. implement
    # some other checking on client lease file

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'rapid_commit')
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '25')
    clnt_msg.client_msg_contains_opt(step, None, '14')

    misc.test_procedure(step)
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(step, None, '25')
    clnt_msg.client_msg_contains_subopt(step, '25', None, '26')

    misc.test_procedure(step)
    clnt_msg.srv_msg_clean(step)
    clnt_msg.server_sets_value(step, 'prefix', '4321::')
    clnt_msg.add_option(step, 'rapid_commit', None)
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'REPLY')

    clnt_msg.srv_msg_clean(step)
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'REPLY')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.client
def test_prefix_delegation_client_renew_unicast(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(step, None, '25')
    clnt_msg.client_msg_contains_subopt(step, '25', None, '26')

    misc.test_procedure(step)
    clnt_msg.srv_msg_clean(step)
    clnt_msg.server_sets_value(step, 'T1', '10')
    clnt_msg.add_option(step, 'server_unicast', None)
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'REPLY')

    misc.pass_criteria(step)
    clnt_control.client_parse_config(step, None)

    misc.test_procedure(step)
    clnt_msg.set_timer(step, 'T1')
    clnt_msg.client_msg_capture(step, 'RENEW', ' with timeout')

    misc.pass_criteria(step)
    # step : "Message was sent after maximum 10 second." would work correctly
    # for test where valid retransmission are updated properly - see tests
    # in dhcpv6/client/retransmission_time_validation/ directory.
    # Therefore, timer is set to T1 value and RENEW MUST be sniffed in that
    # time.
    clnt_msg.client_dst_address_check(step, 'unicast')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.client
def test_prefix_delegation_client_rebind_multicast(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(step, None, '25')
    clnt_msg.client_msg_contains_subopt(step, '25', None, '26')

    misc.test_procedure(step)
    clnt_msg.srv_msg_clean(step)
    clnt_msg.server_sets_value(step, 'T1', '5')
    clnt_msg.server_sets_value(step, 'T2', '10')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'REPLY')

    misc.pass_criteria(step)
    clnt_control.client_parse_config(step, None)

    misc.test_procedure(step)
    clnt_msg.set_timer(step, 'T2')
    clnt_msg.client_msg_capture(step, 'REBIND', ' with timeout')

    misc.pass_criteria(step)
    # step : "Message was sent after maximum 10 second." would work correctly
    # for test where valid retransmission are updated properly - see tests
    # in dhcpv6/client/retransmission_time_validation/ directory.
    # Therefore, timer is set to T1 value and RENEW MUST be sniffed in that
    # time.
    clnt_msg.client_dst_address_check(step, 'multicast')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_twoPrefixes(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.save_value(step, 'iaid')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(step, None, '25')
    clnt_msg.client_msg_contains_subopt(step, '25', None, '26')
    clnt_msg.client_msg_count_subopt(step, None, '2', '26', '25')
    clnt_msg.client_cmp_values(step, 'iaid')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_PD_timers_presence(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '25')
    clnt_msg.client_check_field_presence(step, None, 'T1', '25')
    clnt_msg.client_check_field_presence(step, None, 'T2', '25')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_twoPrefixes_values(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.server_sets_value(step, 'prefix', '3111::')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_sets_value(step, 'prefix', '3333::')
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(step, None, '25')
    clnt_msg.client_msg_contains_subopt(step, '25', None, '26')
    clnt_msg.client_subopt_check_value(step, '26', '25', None, 'prefix', '3111::')
    clnt_msg.client_subopt_check_value(step, '26', '25', None, 'prefix', '3333::')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_NoPrefixAvail(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'Status_Code', '6 ')
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, 'NOT ', 'REQUEST')
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_ignore_timers(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.server_sets_value(step, 'T1', '2000')
    clnt_msg.server_sets_value(step, 'T2', '1000')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    # Client must ignore IA_PD option
    clnt_msg.client_send_receive(step, 'NOT ', 'REQUEST')
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)
    clnt_msg.client_msg_contains_opt(step, None, '25')
    clnt_msg.client_opt_check_value(step, '25', 'NOT ', 'T1', '2000')
    clnt_msg.client_opt_check_value(step, '25', 'NOT ', 'T2', '1000')

    misc.test_procedure(step)
    clnt_msg.server_sets_value(step, 'T1', '1000')
    clnt_msg.server_sets_value(step, 'T2', '2000')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.add_option(step, 'preference', '10 ')
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_ignore_lifetimes(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.server_sets_value(step, 'preferred-lifetime', '4000')
    clnt_msg.server_sets_value(step, 'valid-lifetime', '3000')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    # Client must ignore IA_PD option
    clnt_msg.client_send_receive(step, 'NOT ', 'REQUEST')
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.srv_msg_clean(step)
    clnt_msg.server_sets_value(step, 'preferred-lifetime', '3000')
    clnt_msg.server_sets_value(step, 'valid-lifetime', '4000')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(step, None, '25')
    clnt_msg.client_msg_contains_subopt(step, '25', None, '26')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_responseTime_measure(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(step, None, '25')
    clnt_msg.client_msg_contains_subopt(step, '25', None, '26')
    clnt_msg.client_rt_delay(step, 'sent', '1.1', None)
    clnt_msg.client_cmp_values(step, 'iaid')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_diffPreferences(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.add_option(step, 'preference', '10 ')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    clnt_msg.srv_msg_clean(step)
    clnt_msg.server_sets_value(step, 'prefix', '6665::')
    clnt_msg.add_option(step, 'preference', '20 ')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, None, 'ADVERTISE')

    clnt_msg.srv_msg_clean(step)
    clnt_msg.server_sets_value(step, 'prefix', '4444::')
    clnt_msg.add_option(step, 'preference', '150 ')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, None, 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(step, None, '25')
    clnt_msg.client_msg_contains_subopt(step, '25', None, '26')
    clnt_msg.client_subopt_check_value(step, '26', '25', None, 'prefix', '4444::')

    # Pause the Test.
    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_preference255(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.server_sets_value(step, 'prefix', '3366:beef::')
    clnt_msg.add_option(step, 'preference', '255 ')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    clnt_msg.srv_msg_clean(step)
    clnt_msg.server_sets_value(step, 'prefix', '4444::')
    clnt_msg.add_option(step, 'preference', '150 ')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, None, 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(step, None, '25')
    clnt_msg.client_msg_contains_subopt(step, '25', None, '26')
    clnt_msg.client_subopt_check_value(step, '26', '25', None, 'prefix', '3366:beef::')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_leaseCheck(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_option_req(step, 'another ', 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_sets_value(step, 'prefix', 'c0de:beef::')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(step, None, '25')
    clnt_msg.client_msg_contains_subopt(step, '25', None, '26')

    misc.test_procedure(step)
    clnt_msg.server_build_msg(step, 'back ', 'REPLY')

    misc.pass_criteria(step)
    clnt_control.client_parse_config(step, None)

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_renew(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    # Pause the Test.
    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.server_sets_value(step, 'T1', '5')
    clnt_msg.server_sets_value(step, 'T2', '10')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(step, None, '25')
    clnt_msg.client_msg_contains_subopt(step, '25', None, '26')

    misc.test_procedure(step)
    clnt_msg.server_build_msg(step, 'back ', 'REPLY')

    misc.pass_criteria(step)
    clnt_control.client_parse_config(step, None)

    misc.test_procedure(step)
    clnt_msg.set_timer(step, 'T1')
    clnt_msg.client_msg_capture(step, 'RENEW', ' with timeout')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_rebind(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.server_sets_value(step, 'T1', '3')
    clnt_msg.server_sets_value(step, 'T2', '6')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(step, None, '25')
    clnt_msg.client_msg_contains_subopt(step, '25', None, '26')

    misc.test_procedure(step)
    clnt_msg.server_build_msg(step, 'back ', 'REPLY')

    misc.pass_criteria(step)
    clnt_control.client_parse_config(step, None)

    misc.test_procedure(step)
    clnt_msg.set_timer(step, 'T2')
    clnt_msg.client_msg_capture(step, 'REBIND', ' with timeout')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.client
def test_prefix_delegation_client_rebind_reply(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.server_sets_value(step, 'T1', '3')
    clnt_msg.server_sets_value(step, 'T2', '6')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(step, None, '25')
    clnt_msg.client_msg_contains_subopt(step, '25', None, '26')

    misc.test_procedure(step)
    clnt_msg.server_sets_value(step, 'T1', '3')
    clnt_msg.server_sets_value(step, 'T2', '6')
    clnt_msg.server_build_msg(step, 'back ', 'REPLY')

    misc.pass_criteria(step)
    clnt_msg.client_msg_capture(step, 'REBIND', None)

    misc.test_procedure(step)
    clnt_msg.srv_msg_clean(step)
    clnt_msg.server_sets_value(step, 'T1', '1337')
    clnt_msg.server_sets_value(step, 'T2', '3030')
    clnt_msg.server_sets_value(step, 'preferred-lifetime', '4444')
    clnt_msg.server_sets_value(step, 'valid-lifetime', '6666')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'REPLY')

    misc.test_procedure(step)
    clnt_control.client_parse_config(step, None)

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.client
def test_prefix_delegation_client_renew_reply(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.server_sets_value(step, 'T1', '3')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(step, None, '25')
    clnt_msg.client_msg_contains_subopt(step, '25', None, '26')

    misc.test_procedure(step)
    clnt_msg.server_sets_value(step, 'T1', '3')
    clnt_msg.server_build_msg(step, 'back ', 'REPLY')

    misc.pass_criteria(step)
    clnt_msg.client_msg_capture(step, 'RENEW', None)

    misc.test_procedure(step)
    clnt_msg.srv_msg_clean(step)
    clnt_msg.server_sets_value(step, 'T1', '1337')
    clnt_msg.server_sets_value(step, 'T2', '3030')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'REPLY')

    misc.test_procedure(step)
    clnt_control.client_parse_config(step, None)

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_choose_server(step):
    # this scenario checks whether client stores information
    # about plural servers that have sent response;
    # if client did not receive reply for his request
    # message and retransmission count is equal to REQ_MAX_RC,
    # then client sends request to other server.

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.add_option(step, 'preference', '0 ')
    clnt_msg.server_sets_value(step, 'prefix-len', '56')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, None, 'ADVERTISE')

    clnt_msg.srv_msg_clean(step)
    clnt_msg.add_option(step, 'preference', '100 ')
    clnt_msg.add_option(step, 'preference', '255 ')
    clnt_msg.server_sets_value(step, 'prefix', '6666::')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, None, 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(step, None, '25')
    clnt_msg.client_msg_contains_subopt(step, '25', None, '26')
    clnt_msg.client_subopt_check_value(step, '26', '25', None, 'prefix', '6666::')

    misc.test_procedure(step)
    # implement step that sniffs given count of messages.
    clnt_msg.client_msg_capture(step, 'REQUEST', None)
    clnt_msg.client_msg_capture(step, 'REQUEST', None)
    clnt_msg.client_msg_capture(step, 'REQUEST', None)
    clnt_msg.client_msg_capture(step, 'REQUEST', None)
    clnt_msg.client_msg_capture(step, 'REQUEST', None)
    clnt_msg.client_msg_capture(step, 'REQUEST', None)
    clnt_msg.client_msg_capture(step, 'REQUEST', None)
    clnt_msg.client_msg_capture(step, 'REQUEST', None)
    clnt_msg.client_msg_capture(step, 'REQUEST', None)

    misc.pass_criteria(step)
    # MRC reached.
    clnt_msg.client_msg_capture(step, 'REQUEST', ' with timeout')
    clnt_msg.client_msg_contains_opt(step, None, '25')
    clnt_msg.client_msg_contains_subopt(step, '25', None, '26')
    clnt_msg.client_subopt_check_value(step, '26', '25', None, 'plen', '56')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_release(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.server_sets_value(step, 'T1', '1')
    clnt_msg.server_sets_value(step, 'T2', '2')
    clnt_msg.server_sets_value(step, 'preferred-lifetime', '3')
    clnt_msg.server_sets_value(step, 'valid-lifetime', '40')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(step, None, '25')
    clnt_msg.client_msg_contains_subopt(step, '25', None, '26')

    misc.test_procedure(step)
    clnt_msg.server_build_msg(step, 'back ', 'REPLY')

    misc.pass_criteria(step)
    clnt_control.client_parse_config(step, None)

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'RELEASE', ' with timeout')

    references.references_check(step, 'RFC')
