"""DHCPv6 Client Message Validation"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import clnt_msg
from features import references
from features import clnt_control
from features import misc


@pytest.mark.v6
@pytest.mark.rfc3315
@pytest.mark.basic
@pytest.mark.client
def test_message_validation_client_elapsed_time(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '8')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.rfc3315
@pytest.mark.basic
@pytest.mark.client
def test_message_validation_client_unique_IAID(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '8')

    misc.test_procedure(step)
    clnt_control.client_restart(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_cmp_values(step, 'IAID')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.rfc3315
@pytest.mark.basic
@pytest.mark.client
def test_message_validation_client_rapid_commit(step):

    clnt_control.client_setup(step)

    misc.test_procedure(step)
    clnt_control.client_option_req(step, None, 'rapid_commit')
    clnt_control.client_option_req(step, None, 'IA_PD')
    clnt_control.client_start(step)
    clnt_msg.client_msg_capture(step, 'SOLICIT', None)

    misc.pass_criteria(step)
    clnt_msg.client_msg_contains_opt(step, None, '1')
    clnt_msg.client_msg_contains_opt(step, None, '8')
    clnt_msg.client_msg_contains_opt(step, None, '14')
    clnt_msg.client_msg_contains_opt(step, None, '25')

    references.references_check(step, 'RFC')
