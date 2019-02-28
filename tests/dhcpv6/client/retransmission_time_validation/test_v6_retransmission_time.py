"""DHCPv6 Client retransmission times"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import references
from features import misc
from features import clnt_msg
from features import clnt_control


@pytest.mark.v6
@pytest.mark.RT
@pytest.mark.client
def test_retransmission_time_client_reb_timeout():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '1')
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    clnt_msg.server_sets_value('T1', '3')
    clnt_msg.server_sets_value('T2', '6')
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive(None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(None, '25')
    clnt_msg.client_msg_contains_subopt('25', None, '26')

    misc.test_procedure()
    clnt_msg.server_sets_value('T1', '3')
    clnt_msg.server_sets_value('T2', '6')
    clnt_msg.server_build_msg('back ', 'REPLY')

    misc.pass_criteria()
    clnt_msg.set_timer('T2')
    clnt_msg.client_msg_capture('REBIND', ' with timeout')
    clnt_msg.client_msg_capture('REBIND', None)
    clnt_msg.client_rt_delay('sent', '10', None)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.RT
@pytest.mark.client
def test_retransmission_time_client_reb_max_rt():
    # This test might take ~20 minutes.

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '1')
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    clnt_msg.server_sets_value('T1', '1')
    clnt_msg.server_sets_value('T2', '15')
    clnt_msg.server_sets_value('preferred-lifetime', '0xffffffff')
    clnt_msg.server_sets_value('valid-lifetime', '0xffffffff')
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive(None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(None, '25')
    clnt_msg.client_msg_contains_subopt('25', None, '26')

    misc.test_procedure()
    clnt_msg.server_sets_value('T1', '1')
    clnt_msg.server_sets_value('T2', '15')
    clnt_msg.server_sets_value('preferred-lifetime', '0xffffffff')
    clnt_msg.server_sets_value('valid-lifetime', '0xffffffff')
    clnt_msg.server_build_msg('back ', 'REPLY')

    clnt_msg.client_msg_capture('REBIND', None)
    clnt_msg.client_msg_capture('REBIND', None)

    misc.pass_criteria()
    # initial: 10s
    clnt_msg.client_time_interval()

    misc.test_procedure()
    clnt_msg.client_msg_capture('REBIND', None)

    misc.pass_criteria()
    # 20
    clnt_msg.client_time_interval()

    misc.test_procedure()
    clnt_msg.client_msg_capture('REBIND', None)

    misc.pass_criteria()
    # 40
    clnt_msg.client_time_interval()

    misc.test_procedure()
    clnt_msg.client_msg_capture('REBIND', None)

    misc.pass_criteria()
    # 80
    clnt_msg.client_time_interval()

    misc.test_procedure()
    clnt_msg.client_msg_capture('REBIND', None)

    misc.pass_criteria()
    # 160
    clnt_msg.client_time_interval()

    misc.test_procedure()
    clnt_msg.client_msg_capture('REBIND', None)

    misc.pass_criteria()
    # 320
    clnt_msg.client_time_interval()

    misc.test_procedure()
    clnt_msg.client_msg_capture('REBIND', None)

    misc.pass_criteria()
    # 640
    clnt_msg.client_time_interval()

    misc.test_procedure()
    clnt_msg.client_msg_capture('REBIND', None)

    misc.pass_criteria()
    # max
    clnt_msg.client_rt_delay('retransmitted', '610', None)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.RT
@pytest.mark.client
def test_retransmission_time_client_ren_max_rt():
    # This test might take ~20 minutes.
    # Extending a little time scopes should be considered.
    # For example, test will fail if time scope is <9, 11>
    # and measured time is 8.899s

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '1')
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    clnt_msg.server_sets_value('T1', '15')
    clnt_msg.server_sets_value('T2', '0xffffffff')
    clnt_msg.server_sets_value('preferred-lifetime', '0xffffffff')
    clnt_msg.server_sets_value('valid-lifetime', '0xffffffff')
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive(None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(None, '25')
    clnt_msg.client_msg_contains_subopt('25', None, '26')

    misc.test_procedure()
    clnt_msg.server_sets_value('T1', '15')
    clnt_msg.server_sets_value('T2', '0xffffffff')
    clnt_msg.server_sets_value('preferred-lifetime', '0xffffffff')
    clnt_msg.server_sets_value('valid-lifetime', '0xffffffff')
    clnt_msg.server_build_msg('back ', 'REPLY')

    clnt_msg.client_msg_capture('RENEW', None)
    clnt_msg.client_msg_capture('RENEW', None)

    misc.pass_criteria()
    # initial: 10s
    clnt_msg.client_time_interval()

    misc.test_procedure()
    clnt_msg.client_msg_capture('RENEW', None)

    misc.pass_criteria()
    # 20
    clnt_msg.client_time_interval()

    misc.test_procedure()
    clnt_msg.client_msg_capture('RENEW', None)

    misc.pass_criteria()
    # 40
    clnt_msg.client_time_interval()

    misc.test_procedure()
    clnt_msg.client_msg_capture('RENEW', None)

    misc.pass_criteria()
    # 80
    clnt_msg.client_time_interval()

    misc.test_procedure()
    clnt_msg.client_msg_capture('RENEW', None)

    misc.pass_criteria()
    # 160
    clnt_msg.client_time_interval()

    misc.test_procedure()
    clnt_msg.client_msg_capture('RENEW', None)

    misc.pass_criteria()
    # 320
    clnt_msg.client_time_interval()

    misc.test_procedure()
    clnt_msg.client_msg_capture('RENEW', None)

    misc.pass_criteria()
    # 640
    clnt_msg.client_time_interval()

    misc.test_procedure()
    clnt_msg.client_msg_capture('RENEW', None)

    misc.pass_criteria()
    # max
    clnt_msg.client_rt_delay('retransmitted', '610', None)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.RT
@pytest.mark.client
def test_retransmission_time_client_ren_timeout():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '1')
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    clnt_msg.server_sets_value('T1', '5')
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive(None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(None, '25')
    clnt_msg.client_msg_contains_subopt('25', None, '26')

    misc.test_procedure()
    clnt_msg.server_sets_value('T1', '5')
    clnt_msg.server_build_msg('back ', 'REPLY')

    misc.pass_criteria()
    clnt_msg.set_timer('T1')
    clnt_msg.client_msg_capture('RENEW', ' with timeout')
    clnt_msg.client_msg_capture('RENEW', None)
    # User is free to use step below with "sent" word instead
    # of "retransmitted".
    clnt_msg.client_rt_delay('retransmitted', '10', None)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.RT
@pytest.mark.client
def test_retransmission_time_client_solicit_retransmit_adv_no_wait():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '1')
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    clnt_msg.client_msg_capture('SOLICIT', None)

    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive(None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(None, '25')
    clnt_msg.client_msg_contains_subopt('25', None, '26')
    clnt_msg.client_rt_delay('sent', '0.1', None)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.RT
@pytest.mark.client
def test_retransmission_time_client_sol_max_rt():
    # SOLICIT MRT = SOL_MAX_RT = 120s
    # each subsequent rt:
    # RT = 2*RTprev + RAND*RTprev
    # if (RT > MRT)
    # RT = MRT + RAND*MRT

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_time_interval()

    misc.test_procedure()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_time_interval()

    misc.test_procedure()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_time_interval()

    misc.test_procedure()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_time_interval()

    misc.test_procedure()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_time_interval()

    misc.test_procedure()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_time_interval()

    misc.test_procedure()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_time_interval()

    misc.test_procedure()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_rt_delay('retransmitted', '128', 's')

    misc.test_procedure()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_rt_delay('retransmitted', '128', 's')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.RT
@pytest.mark.client
def test_retransmission_time_client_req_max_rt():
    # REQUEST MRT = REQ_MAX_RT = 30s
    # each subsequent rt:
    # RT = 2*RTprev + RAND*RTprev
    # if (RT > MRT)
    # RT = MRT + RAND*MRT

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '1')
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive(None, 'REQUEST')

    misc.test_procedure()
    clnt_msg.client_msg_capture('REQUEST', None)

    misc.pass_criteria()
    clnt_msg.client_time_interval()

    misc.test_procedure()
    clnt_msg.client_msg_capture('REQUEST', None)

    misc.pass_criteria()
    clnt_msg.client_time_interval()

    misc.test_procedure()
    clnt_msg.client_msg_capture('REQUEST', None)

    misc.pass_criteria()
    clnt_msg.client_time_interval()

    misc.test_procedure()
    clnt_msg.client_msg_capture('REQUEST', None)

    misc.pass_criteria()
    clnt_msg.client_time_interval()

    misc.test_procedure()
    clnt_msg.client_msg_capture('REQUEST', None)

    misc.pass_criteria()
    clnt_msg.client_time_interval()

    misc.test_procedure()
    clnt_msg.client_msg_capture('REQUEST', None)

    misc.pass_criteria()
    clnt_msg.client_rt_delay('retransmitted', '35', 's')

    misc.test_procedure()
    clnt_msg.client_msg_capture('REQUEST', None)

    misc.pass_criteria()
    clnt_msg.client_rt_delay('retransmitted', '35', 's')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.RT
@pytest.mark.client
def test_retransmission_time_client_solicit_first_RT():
    # SOLICIT first RT :
    # IRT = SOL_TIMEOUT
    # RT = IRT + RAND*IRT

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    # <0.9, 1.1>
    clnt_msg.client_time_interval()

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.RT
@pytest.mark.client
def test_retransmission_time_client_request_first_RT():
    # REQUEST first RT :
    # IRT = REQ_TIMEOUT
    # RT = IRT + RAND*IRT

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive(None, 'REQUEST')

    misc.test_procedure()
    clnt_msg.client_msg_capture('REQUEST', None)

    misc.pass_criteria()
    # <0.9, 1.1>
    clnt_msg.client_time_interval()

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.RT
@pytest.mark.client
def test_retransmission_time_client_request_MRC():
    # MRC = REQ_MAX_RC = 10

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive(None, 'REQUEST')

    misc.test_procedure()
    clnt_msg.client_msg_capture('REQUEST', None)
    clnt_msg.client_msg_capture('REQUEST', None)
    clnt_msg.client_msg_capture('REQUEST', None)
    clnt_msg.client_msg_capture('REQUEST', None)
    clnt_msg.client_msg_capture('REQUEST', None)
    clnt_msg.client_msg_capture('REQUEST', None)
    clnt_msg.client_msg_capture('REQUEST', None)
    clnt_msg.client_msg_capture('REQUEST', None)
    clnt_msg.client_msg_capture('REQUEST', None)
    clnt_msg.client_msg_capture('REQUEST', None)

    misc.pass_criteria()
    clnt_msg.client_msg_capture('SOLICIT', None)

    references.references_check('RFC')
