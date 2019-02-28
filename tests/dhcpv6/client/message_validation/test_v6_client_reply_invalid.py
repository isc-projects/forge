"""DHCPv6 Client Reply Message Validation"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import clnt_control
from features import clnt_msg
from features import references
from features import misc


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_invalid_reply_oro():

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

    misc.test_procedure()
    clnt_msg.srv_msg_clean()
    clnt_msg.add_option('option_request', None)
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'REPLY')

    misc.pass_criteria()
    clnt_control.client_parse_config('NOT ')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_invalid_reply_elapsed_time():

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

    misc.test_procedure()
    clnt_msg.srv_msg_clean()
    clnt_msg.add_option('elapsed_time', None)
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'REPLY')

    misc.pass_criteria()
    clnt_control.client_parse_config('NOT ')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_invalid_reply_relay_msg():

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

    misc.test_procedure()
    clnt_msg.srv_msg_clean()
    clnt_msg.add_option('relay_message', None)
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'REPLY')

    misc.pass_criteria()
    clnt_control.client_parse_config('NOT ')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_invalid_reply_iface_id():

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

    misc.test_procedure()
    clnt_msg.srv_msg_clean()
    clnt_msg.add_option('iface_id', None)
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'REPLY')

    misc.pass_criteria()
    clnt_control.client_parse_config('NOT ')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_invalid_reply_reconfigure():

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

    misc.test_procedure()
    clnt_msg.srv_msg_clean()
    clnt_msg.add_option('reconfigure', None)
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'REPLY')

    misc.pass_criteria()
    clnt_control.client_parse_config('NOT ')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_reply_without_srv_id():

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

    misc.test_procedure()
    clnt_msg.srv_msg_clean()
    clnt_msg.server_not_add('server_id')
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'REPLY')

    misc.pass_criteria()
    clnt_control.client_parse_config('NOT ')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_reply_without_cli_id():

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

    misc.test_procedure()
    clnt_msg.srv_msg_clean()
    clnt_msg.server_not_add('client_id')
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'REPLY')

    misc.pass_criteria()
    clnt_control.client_parse_config('NOT ')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_reply_wrong_trid():

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

    misc.test_procedure()
    clnt_msg.srv_msg_clean()
    clnt_msg.server_set_wrong_val('trid')
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'REPLY')

    misc.pass_criteria()
    clnt_control.client_parse_config('NOT ')
    clnt_msg.client_msg_capture('REQUEST', None)

    references.references_check('RFC')
