"""DHCPv6 Client Advertise Message Validation"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import clnt_msg
from features import references
from features import misc
from features import clnt_control


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_invalid_adv_oro(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.add_option(step, 'option_request', None)
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, 'NOT ', 'REQUEST')
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_invalid_adv_srv_unicast(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    # Server unicast option can appear only in REPLY.
    clnt_msg.add_option(step, 'server_unicast', None)
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, 'NOT ', 'REQUEST')
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_invalid_adv_rapid_commit(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.add_option(step, 'rapid_commit', None)
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, 'NOT ', 'REQUEST')
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_invalid_adv_elapsed_time(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.add_option(step, 'elapsed_time', None)
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, 'NOT ', 'REQUEST')
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_invalid_adv_iface_id(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.add_option(step, 'iface_id', None)
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, 'NOT ', 'REQUEST')
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_invalid_adv_reconf(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.add_option(step, 'reconfigure', None)
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, 'NOT ', 'REQUEST')
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_adv_without_cli_id(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.server_not_add(step, 'client_id')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, 'NOT ', 'REQUEST')
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_adv_without_srv_id(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    misc.test_procedure(step)
    clnt_msg.server_not_add(step, 'server_id')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'ADVERTISE')

    misc.pass_criteria(step)
    clnt_msg.client_send_receive(step, 'NOT ', 'REQUEST')
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    references.references_check(step, 'RFC')
