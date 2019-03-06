"""DHCPv6 Client Prefix Delegation"""

# pylint: disable=invalid-name,line-too-long

import pytest

import clnt_control
import misc
import clnt_msg
import references


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_onlyPD():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '1')
    clnt_msg.client_msg_contains_opt(None, '25')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_twoPDs():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_option_req('another ', 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '1')
    clnt_msg.client_msg_contains_opt(None, '25')
    clnt_msg.client_msg_count_opt(None, '2', '25')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_IAPrefix_opt():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive(None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(None, '25')
    clnt_msg.client_msg_contains_subopt('25', None, '26')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_check_options():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '1')
    clnt_msg.client_msg_contains_opt(None, '8')
    clnt_msg.client_msg_contains_opt(None, '25')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_wrong_trid():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '1')
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    clnt_msg.server_set_wrong_val('trid')
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive('NOT ', 'REQUEST')

    misc.test_procedure()
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

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_wrong_cliduid():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '1')
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    clnt_msg.server_set_wrong_val('client_id')
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive('NOT ', 'REQUEST')

    misc.test_procedure()
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

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_rapid_commit():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'rapid_commit')
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '25')
    clnt_msg.client_msg_contains_opt(None, '14')

    misc.test_procedure()
    clnt_msg.add_option('rapid_commit', None)
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'REPLY')

    misc.pass_criteria()
    clnt_control.client_parse_config(None)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.client
def test_prefix_delegation_client_rapid_commit_adv():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'rapid_commit')
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '25')
    clnt_msg.client_msg_contains_opt(None, '14')

    misc.test_procedure()
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive(None, 'REQUEST')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_wrong_rapid_commit():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'rapid_commit')
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '25')
    clnt_msg.client_msg_contains_opt(None, '14')

    misc.test_procedure()
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'REPLY')

    misc.pass_criteria()
    clnt_control.client_parse_config('NOT ')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_reply_success():
    # TODO: test should check that client took values
    # from one of reply messages; however, if lease might
    # be checked, scapy_lease would be made from the
    # latest reply message; so it's wrong. implement
    # some other checking on client lease file

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'rapid_commit')
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '25')
    clnt_msg.client_msg_contains_opt(None, '14')

    misc.test_procedure()
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive(None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(None, '25')
    clnt_msg.client_msg_contains_subopt('25', None, '26')

    misc.test_procedure()
    clnt_msg.srv_msg_clean()
    clnt_msg.server_sets_value('prefix', '4321::')
    clnt_msg.add_option('rapid_commit', None)
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'REPLY')

    clnt_msg.srv_msg_clean()
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'REPLY')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.client
def test_prefix_delegation_client_renew_unicast():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive(None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(None, '25')
    clnt_msg.client_msg_contains_subopt('25', None, '26')

    misc.test_procedure()
    clnt_msg.srv_msg_clean()
    clnt_msg.server_sets_value('T1', '10')
    clnt_msg.add_option('server_unicast', None)
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'REPLY')

    misc.pass_criteria()
    clnt_control.client_parse_config(None)

    misc.test_procedure()
    clnt_msg.set_timer('T1')
    clnt_msg.client_msg_capture('RENEW', ' with timeout')

    misc.pass_criteria()
    # step : "Message was sent after maximum 10 second." would work correctly
    # for test where valid retransmission are updated properly - see tests
    # in dhcpv6/client/retransmission_time_validation/ directory.
    # Therefore, timer is set to T1 value and RENEW MUST be sniffed in that
    # time.
    clnt_msg.client_dst_address_check('unicast')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.client
def test_prefix_delegation_client_rebind_multicast():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive(None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(None, '25')
    clnt_msg.client_msg_contains_subopt('25', None, '26')

    misc.test_procedure()
    clnt_msg.srv_msg_clean()
    clnt_msg.server_sets_value('T1', '5')
    clnt_msg.server_sets_value('T2', '10')
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'REPLY')

    misc.pass_criteria()
    clnt_control.client_parse_config(None)

    misc.test_procedure()
    clnt_msg.set_timer('T2')
    clnt_msg.client_msg_capture('REBIND', ' with timeout')

    misc.pass_criteria()
    # step : "Message was sent after maximum 10 second." would work correctly
    # for test where valid retransmission are updated properly - see tests
    # in dhcpv6/client/retransmission_time_validation/ directory.
    # Therefore, timer is set to T1 value and RENEW MUST be sniffed in that
    # time.
    clnt_msg.client_dst_address_check('multicast')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_twoPrefixes():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.save_value('iaid')
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive(None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(None, '25')
    clnt_msg.client_msg_contains_subopt('25', None, '26')
    clnt_msg.client_msg_count_subopt(None, '2', '26', '25')
    clnt_msg.client_cmp_values('iaid')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_PD_timers_presence():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '1')
    clnt_msg.client_msg_contains_opt(None, '25')
    clnt_msg.client_check_field_presence(None, 'T1', '25')
    clnt_msg.client_check_field_presence(None, 'T2', '25')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_twoPrefixes_values():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    clnt_msg.server_sets_value('prefix', '3111::')
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_sets_value('prefix', '3333::')
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive(None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(None, '25')
    clnt_msg.client_msg_contains_subopt('25', None, '26')
    clnt_msg.client_subopt_check_value('26', '25', None, 'prefix', '3111::')
    clnt_msg.client_subopt_check_value('26', '25', None, 'prefix', '3333::')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_NoPrefixAvail():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('Status_Code', '6 ')
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive('NOT ', 'REQUEST')
    clnt_msg.client_msg_capture('SOLICIT', None)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_ignore_timers():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '1')
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    clnt_msg.server_sets_value('T1', '2000')
    clnt_msg.server_sets_value('T2', '1000')
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    # Client must ignore IA_PD option
    clnt_msg.client_send_receive('NOT ', 'REQUEST')
    clnt_msg.client_msg_capture('SOLICIT', None)
    clnt_msg.client_msg_contains_opt(None, '25')
    clnt_msg.client_opt_check_value('25', 'NOT ', 'T1', '2000')
    clnt_msg.client_opt_check_value('25', 'NOT ', 'T2', '1000')

    misc.test_procedure()
    clnt_msg.server_sets_value('T1', '1000')
    clnt_msg.server_sets_value('T2', '2000')
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.add_option('preference', '10 ')
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive(None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(None, '25')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_ignore_lifetimes():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '1')
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    clnt_msg.server_sets_value('preferred-lifetime', '4000')
    clnt_msg.server_sets_value('valid-lifetime', '3000')
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    # Client must ignore IA_PD option
    clnt_msg.client_send_receive('NOT ', 'REQUEST')
    clnt_msg.client_msg_capture('SOLICIT', None)
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    clnt_msg.srv_msg_clean()
    clnt_msg.server_sets_value('preferred-lifetime', '3000')
    clnt_msg.server_sets_value('valid-lifetime', '4000')
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive(None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(None, '25')
    clnt_msg.client_msg_contains_subopt('25', None, '26')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_responseTime_measure():

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
    clnt_msg.client_msg_contains_opt(None, '25')
    clnt_msg.client_msg_contains_subopt('25', None, '26')
    clnt_msg.client_rt_delay('sent', '1.1', None)
    clnt_msg.client_cmp_values('iaid')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_diffPreferences():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    clnt_msg.add_option('preference', '10 ')
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    clnt_msg.srv_msg_clean()
    clnt_msg.server_sets_value('prefix', '6665::')
    clnt_msg.add_option('preference', '20 ')
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg(None, 'ADVERTISE')

    clnt_msg.srv_msg_clean()
    clnt_msg.server_sets_value('prefix', '4444::')
    clnt_msg.add_option('preference', '150 ')
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg(None, 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive(None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(None, '25')
    clnt_msg.client_msg_contains_subopt('25', None, '26')
    clnt_msg.client_subopt_check_value('26', '25', None, 'prefix', '4444::')

    # Pause the Test.
    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_preference255():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    clnt_msg.server_sets_value('prefix', '3366:beef::')
    clnt_msg.add_option('preference', '255 ')
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    clnt_msg.srv_msg_clean()
    clnt_msg.server_sets_value('prefix', '4444::')
    clnt_msg.add_option('preference', '150 ')
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg(None, 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive(None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(None, '25')
    clnt_msg.client_msg_contains_subopt('25', None, '26')
    clnt_msg.client_subopt_check_value('26', '25', None, 'prefix', '3366:beef::')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_leaseCheck():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_option_req('another ', 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '1')
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_sets_value('prefix', 'c0de:beef::')
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive(None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(None, '25')
    clnt_msg.client_msg_contains_subopt('25', None, '26')

    misc.test_procedure()
    clnt_msg.server_build_msg('back ', 'REPLY')

    misc.pass_criteria()
    clnt_control.client_parse_config(None)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_renew():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    # Pause the Test.
    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '1')
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    clnt_msg.server_sets_value('T1', '5')
    clnt_msg.server_sets_value('T2', '10')
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive(None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(None, '25')
    clnt_msg.client_msg_contains_subopt('25', None, '26')

    misc.test_procedure()
    clnt_msg.server_build_msg('back ', 'REPLY')

    misc.pass_criteria()
    clnt_control.client_parse_config(None)

    misc.test_procedure()
    clnt_msg.set_timer('T1')
    clnt_msg.client_msg_capture('RENEW', ' with timeout')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_rebind():

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
    clnt_msg.server_build_msg('back ', 'REPLY')

    misc.pass_criteria()
    clnt_control.client_parse_config(None)

    misc.test_procedure()
    clnt_msg.set_timer('T2')
    clnt_msg.client_msg_capture('REBIND', ' with timeout')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.client
def test_prefix_delegation_client_rebind_reply():

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
    clnt_msg.client_msg_capture('REBIND', None)

    misc.test_procedure()
    clnt_msg.srv_msg_clean()
    clnt_msg.server_sets_value('T1', '1337')
    clnt_msg.server_sets_value('T2', '3030')
    clnt_msg.server_sets_value('preferred-lifetime', '4444')
    clnt_msg.server_sets_value('valid-lifetime', '6666')
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'REPLY')

    misc.test_procedure()
    clnt_control.client_parse_config(None)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.client
def test_prefix_delegation_client_renew_reply():

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
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive(None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(None, '25')
    clnt_msg.client_msg_contains_subopt('25', None, '26')

    misc.test_procedure()
    clnt_msg.server_sets_value('T1', '3')
    clnt_msg.server_build_msg('back ', 'REPLY')

    misc.pass_criteria()
    clnt_msg.client_msg_capture('RENEW', None)

    misc.test_procedure()
    clnt_msg.srv_msg_clean()
    clnt_msg.server_sets_value('T1', '1337')
    clnt_msg.server_sets_value('T2', '3030')
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'REPLY')

    misc.test_procedure()
    clnt_control.client_parse_config(None)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_choose_server():
    # this scenario checks whether client stores information
    # about plural servers that have sent response;
    # if client did not receive reply for his request
    # message and retransmission count is equal to REQ_MAX_RC,
    # then client sends request to other server.

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '1')
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    clnt_msg.add_option('preference', '0 ')
    clnt_msg.server_sets_value('prefix-len', '56')
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg(None, 'ADVERTISE')

    clnt_msg.srv_msg_clean()
    clnt_msg.add_option('preference', '100 ')
    clnt_msg.add_option('preference', '255 ')
    clnt_msg.server_sets_value('prefix', '6666::')
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg(None, 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive(None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(None, '25')
    clnt_msg.client_msg_contains_subopt('25', None, '26')
    clnt_msg.client_subopt_check_value('26', '25', None, 'prefix', '6666::')

    misc.test_procedure()
    # implement step that sniffs given count of messages.
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
    # MRC reached.
    clnt_msg.client_msg_capture('REQUEST', ' with timeout')
    clnt_msg.client_msg_contains_opt(None, '25')
    clnt_msg.client_msg_contains_subopt('25', None, '26')
    clnt_msg.client_subopt_check_value('26', '25', None, 'plen', '56')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.client
def test_prefix_delegation_client_release():

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
    clnt_msg.server_sets_value('T2', '2')
    clnt_msg.server_sets_value('preferred-lifetime', '3')
    clnt_msg.server_sets_value('valid-lifetime', '40')
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive(None, 'REQUEST')
    clnt_msg.client_msg_contains_opt(None, '25')
    clnt_msg.client_msg_contains_subopt('25', None, '26')

    misc.test_procedure()
    clnt_msg.server_build_msg('back ', 'REPLY')

    misc.pass_criteria()
    clnt_control.client_parse_config(None)

    misc.test_procedure()
    clnt_msg.client_msg_capture('RELEASE', ' with timeout')

    references.references_check('RFC')
