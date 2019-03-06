"""DHCPv6 Client Advertise Message Validation"""

# pylint: disable=invalid-name,line-too-long

import pytest

import clnt_msg
import clnt_control
import references
import misc


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_invalid_adv_oro():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '1')
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    clnt_msg.add_option('option_request', None)
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive('NOT ', 'REQUEST')
    clnt_msg.client_msg_capture('SOLICIT', None)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_invalid_adv_srv_unicast():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '1')
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    # Server unicast option can appear only in REPLY.
    clnt_msg.add_option('server_unicast', None)
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive('NOT ', 'REQUEST')
    clnt_msg.client_msg_capture('SOLICIT', None)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_invalid_adv_rapid_commit():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '1')
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    clnt_msg.add_option('rapid_commit', None)
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive('NOT ', 'REQUEST')
    clnt_msg.client_msg_capture('SOLICIT', None)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_invalid_adv_elapsed_time():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '1')
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    clnt_msg.add_option('elapsed_time', None)
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive('NOT ', 'REQUEST')
    clnt_msg.client_msg_capture('SOLICIT', None)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_invalid_adv_iface_id():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '1')
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    clnt_msg.add_option('iface_id', None)
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive('NOT ', 'REQUEST')
    clnt_msg.client_msg_capture('SOLICIT', None)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_invalid_adv_reconf():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '1')
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    clnt_msg.add_option('reconfigure', None)
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive('NOT ', 'REQUEST')
    clnt_msg.client_msg_capture('SOLICIT', None)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_adv_without_cli_id():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '1')
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    clnt_msg.server_not_add('client_id')
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive('NOT ', 'REQUEST')
    clnt_msg.client_msg_capture('SOLICIT', None)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_adv_without_srv_id():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '1')
    clnt_msg.client_msg_contains_opt(None, '25')

    misc.test_procedure()
    clnt_msg.server_not_add('server_id')
    clnt_msg.add_option('IA_PD', None)
    clnt_msg.add_option('IA_Prefix', None)
    clnt_msg.server_build_msg('back ', 'ADVERTISE')

    misc.pass_criteria()
    clnt_msg.client_send_receive('NOT ', 'REQUEST')
    clnt_msg.client_msg_capture('SOLICIT', None)

    references.references_check('RFC')
