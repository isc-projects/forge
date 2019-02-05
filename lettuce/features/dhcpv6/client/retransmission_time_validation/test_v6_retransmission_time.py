"""DHCPv6 Client retransmission times"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import references
from features import clnt_msg
from features import misc
from features import clnt_control


@pytest.mark.v6
@pytest.mark.RT
@pytest.mark.client
def test_retransmission_time_client_reb_timeout(step):

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
    clnt_msg.set_timer(step, 'T2')
    clnt_msg.client_msg_capture(step, 'REBIND', ' with timeout')
    clnt_msg.client_msg_capture(step, 'REBIND', None)
    clnt_msg.client_rt_delay(step, 'sent', '10', None)

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.RT
@pytest.mark.client
def test_retransmission_time_client_reb_max_rt(step):
    # This test might take ~20 minutes.

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
    clnt_msg.server_sets_value(step, 'T2', '15')
    clnt_msg.server_sets_value(step, 'preferred-lifetime', '0xffffffff')
    clnt_msg.server_sets_value(step, 'valid-lifetime', '0xffffffff')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(step, None, '25')
    clnt_msg.client_msg_contains_subopt(step, '25', None, '26')

    misc.test_procedure(step)
    clnt_msg.server_sets_value(step, 'T1', '1')
    clnt_msg.server_sets_value(step, 'T2', '15')
    clnt_msg.server_sets_value(step, 'preferred-lifetime', '0xffffffff')
    clnt_msg.server_sets_value(step, 'valid-lifetime', '0xffffffff')
    clnt_msg.server_build_msg(step, 'back ', 'REPLY')

    clnt_msg.client_msg_capture(step, 'REBIND', None)
    clnt_msg.client_msg_capture(step, 'REBIND', None)

    misc.pass_criteria(step)
    # initial: 10s
    clnt_msg.client_time_interval(step)

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'REBIND', None)

    misc.pass_criteria(step)
    # 20
    clnt_msg.client_time_interval(step)

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'REBIND', None)

    misc.pass_criteria(step)
    # 40
    clnt_msg.client_time_interval(step)

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'REBIND', None)

    misc.pass_criteria(step)
    # 80
    clnt_msg.client_time_interval(step)

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'REBIND', None)

    misc.pass_criteria(step)
    # 160
    clnt_msg.client_time_interval(step)

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'REBIND', None)

    misc.pass_criteria(step)
    # 320
    clnt_msg.client_time_interval(step)

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'REBIND', None)

    misc.pass_criteria(step)
    # 640
    clnt_msg.client_time_interval(step)

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'REBIND', None)

    misc.pass_criteria(step)
    # max
    clnt_msg.client_rt_delay(step, 'retransmitted', '610', None)

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.RT
@pytest.mark.client
def test_retransmission_time_client_ren_max_rt(step):
    # This test might take ~20 minutes.
    # Extending a little time scopes should be considered.
    # For example, test will fail if time scope is <9, 11>
    # and measured time is 8.899s

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.server_sets_value(step, 'T1', '15')
    clnt_msg.server_sets_value(step, 'T2', '0xffffffff')
    clnt_msg.server_sets_value(step, 'preferred-lifetime', '0xffffffff')
    clnt_msg.server_sets_value(step, 'valid-lifetime', '0xffffffff')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(step, None, '25')
    clnt_msg.client_msg_contains_subopt(step, '25', None, '26')

    misc.test_procedure(step)
    clnt_msg.server_sets_value(step, 'T1', '15')
    clnt_msg.server_sets_value(step, 'T2', '0xffffffff')
    clnt_msg.server_sets_value(step, 'preferred-lifetime', '0xffffffff')
    clnt_msg.server_sets_value(step, 'valid-lifetime', '0xffffffff')
    clnt_msg.server_build_msg(step, 'back ', 'REPLY')

    clnt_msg.client_msg_capture(step, 'RENEW', None)
    clnt_msg.client_msg_capture(step, 'RENEW', None)

    misc.pass_criteria(step)
    # initial: 10s
    clnt_msg.client_time_interval(step)

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'RENEW', None)

    misc.pass_criteria(step)
    # 20
    clnt_msg.client_time_interval(step)

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'RENEW', None)

    misc.pass_criteria(step)
    # 40
    clnt_msg.client_time_interval(step)

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'RENEW', None)

    misc.pass_criteria(step)
    # 80
    clnt_msg.client_time_interval(step)

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'RENEW', None)

    misc.pass_criteria(step)
    # 160
    clnt_msg.client_time_interval(step)

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'RENEW', None)

    misc.pass_criteria(step)
    # 320
    clnt_msg.client_time_interval(step)

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'RENEW', None)

    misc.pass_criteria(step)
    # 640
    clnt_msg.client_time_interval(step)

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'RENEW', None)

    misc.pass_criteria(step)
    # max
    clnt_msg.client_rt_delay(step, 'retransmitted', '610', None)

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.RT
@pytest.mark.client
def test_retransmission_time_client_ren_timeout(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.server_sets_value(step, 'T1', '5')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(step, None, '25')
    clnt_msg.client_msg_contains_subopt(step, '25', None, '26')

    misc.test_procedure(step)
    clnt_msg.server_sets_value(step, 'T1', '5')
    clnt_msg.server_build_msg(step, 'back ', 'REPLY')

    misc.pass_criteria(step)
    clnt_msg.set_timer(step, 'T1')
    clnt_msg.client_msg_capture(step, 'RENEW', ' with timeout')
    clnt_msg.client_msg_capture(step, 'RENEW', None)
    # User is free to use step below with "sent" word instead
    # of "retransmitted".
    clnt_msg.client_rt_delay(step, 'retransmitted', '10', None)

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.RT
@pytest.mark.client
def test_retransmission_time_client_solicit_retransmit_adv_no_wait(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(step, None, '25')
    clnt_msg.client_msg_contains_subopt(step, '25', None, '26')
    clnt_msg.client_rt_delay(step, 'sent', '0.1', None)

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.RT
@pytest.mark.client
def test_retransmission_time_client_sol_max_rt(step):
    # SOLICIT MRT = SOL_MAX_RT = 120s
    # each subsequent rt:
    # RT = 2*RTprev + RAND*RTprev
    # if (RT > MRT)
    # RT = MRT + RAND*MRT

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_time_interval(step)

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_time_interval(step)

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_time_interval(step)

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_time_interval(step)

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_time_interval(step)

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_time_interval(step)

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_time_interval(step)

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_rt_delay(step, 'retransmitted', '128', 's')

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_rt_delay(step, 'retransmitted', '128', 's')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.RT
@pytest.mark.client
def test_retransmission_time_client_req_max_rt(step):
    # REQUEST MRT = REQ_MAX_RT = 30s
    # each subsequent rt:
    # RT = 2*RTprev + RAND*RTprev
    # if (RT > MRT)
    # RT = MRT + RAND*MRT

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

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'REQUEST', None)

    misc.pass_criteria(step)
    clnt_msg.client_time_interval(step)

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'REQUEST', None)

    misc.pass_criteria(step)
    clnt_msg.client_time_interval(step)

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'REQUEST', None)

    misc.pass_criteria(step)
    clnt_msg.client_time_interval(step)

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'REQUEST', None)

    misc.pass_criteria(step)
    clnt_msg.client_time_interval(step)

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'REQUEST', None)

    misc.pass_criteria(step)
    clnt_msg.client_time_interval(step)

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'REQUEST', None)

    misc.pass_criteria(step)
    clnt_msg.client_rt_delay(step, 'retransmitted', '35', 's')

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'REQUEST', None)

    misc.pass_criteria(step)
    clnt_msg.client_rt_delay(step, 'retransmitted', '35', 's')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.RT
@pytest.mark.client
def test_retransmission_time_client_solicit_first_RT(step):
    # SOLICIT first RT :
    # IRT = SOL_TIMEOUT
    # RT = IRT + RAND*IRT

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    # <0.9, 1.1>
    clnt_msg.client_time_interval(step)

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.RT
@pytest.mark.client
def test_retransmission_time_client_request_first_RT(step):
    # REQUEST first RT :
    # IRT = REQ_TIMEOUT
    # RT = IRT + RAND*IRT

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, None, 'REQUEST')

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'REQUEST', None)

    misc.pass_criteria(step)
    # <0.9, 1.1>
    clnt_msg.client_time_interval(step)

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.RT
@pytest.mark.client
def test_retransmission_time_client_request_MRC(step):
    # MRC = REQ_MAX_RC = 10

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, None, 'REQUEST')

    misc.test_procedure(step)
    clnt_msg.client_msg_capture(step, 'REQUEST', None)
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
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    references.references_check(step, 'RFC')
