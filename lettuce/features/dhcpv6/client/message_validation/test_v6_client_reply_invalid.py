"""DHCPv6 Client Reply Message Validation"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import clnt_msg
from features import clnt_control
from features import references
from features import misc


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_invalid_reply_oro(step):

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

    misc.test_procedure(step)
    clnt_msg.srv_msg_clean(step)
    clnt_msg.add_option(step, 'option_request', None)
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'REPLY')

    misc.pass_criteria(step)
    clnt_control.client_parse_config(step, 'NOT ')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_invalid_reply_elapsed_time(step):

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

    misc.test_procedure(step)
    clnt_msg.srv_msg_clean(step)
    clnt_msg.add_option(step, 'elapsed_time', None)
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'REPLY')

    misc.pass_criteria(step)
    clnt_control.client_parse_config(step, 'NOT ')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_invalid_reply_relay_msg(step):

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

    misc.test_procedure(step)
    clnt_msg.srv_msg_clean(step)
    clnt_msg.add_option(step, 'relay_message', None)
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'REPLY')

    misc.pass_criteria(step)
    clnt_control.client_parse_config(step, 'NOT ')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_invalid_reply_iface_id(step):

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

    misc.test_procedure(step)
    clnt_msg.srv_msg_clean(step)
    clnt_msg.add_option(step, 'iface_id', None)
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'REPLY')

    misc.pass_criteria(step)
    clnt_control.client_parse_config(step, 'NOT ')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_invalid_reply_reconfigure(step):

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

    misc.test_procedure(step)
    clnt_msg.srv_msg_clean(step)
    clnt_msg.add_option(step, 'reconfigure', None)
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'REPLY')

    misc.pass_criteria(step)
    clnt_control.client_parse_config(step, 'NOT ')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_reply_without_srv_id(step):

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

    misc.test_procedure(step)
    clnt_msg.srv_msg_clean(step)
    clnt_msg.server_not_add(step, 'server_id')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'REPLY')

    misc.pass_criteria(step)
    clnt_control.client_parse_config(step, 'NOT ')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_reply_without_cli_id(step):

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

    misc.test_procedure(step)
    clnt_msg.srv_msg_clean(step)
    clnt_msg.server_not_add(step, 'client_id')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'REPLY')

    misc.pass_criteria(step)
    clnt_control.client_parse_config(step, 'NOT ')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.client
def test_message_validation_client_reply_wrong_trid(step):

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

    misc.test_procedure(step)
    clnt_msg.srv_msg_clean(step)
    clnt_msg.server_set_wrong_val(step, 'trid')
    clnt_msg.add_option(step, 'IA_PD', None)
    clnt_msg.add_option(step, 'IA_Prefix', None)
    clnt_msg.server_build_msg(step, 'back ', 'REPLY')

    misc.pass_criteria(step)
    clnt_control.client_parse_config(step, 'NOT ')
    clnt_msg.client_msg_capture(step, 'REQUEST', None)

    references.references_check(step, 'RFC')
