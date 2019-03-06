"""DHCPv6 Client Message Validation"""

# pylint: disable=invalid-name,line-too-long

import pytest

import clnt_control
import misc
import references
import clnt_msg


@pytest.mark.v6
@pytest.mark.rfc3315
@pytest.mark.basic
@pytest.mark.client
def test_message_validation_client_elapsed_time():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '1')
    clnt_msg.client_msg_contains_opt(None, '8')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.rfc3315
@pytest.mark.basic
@pytest.mark.client
def test_message_validation_client_unique_IAID():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '1')
    clnt_msg.client_msg_contains_opt(None, '8')

    misc.test_procedure()
    clnt_control.client_restart()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_cmp_values('IAID')

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.rfc3315
@pytest.mark.basic
@pytest.mark.client
def test_message_validation_client_rapid_commit():

    clnt_control.client_setup()

    misc.test_procedure()
    clnt_control.client_option_req(None, 'rapid_commit')
    clnt_control.client_option_req(None, 'IA_PD')
    clnt_control.client_start()
    clnt_msg.client_msg_capture('SOLICIT', None)

    misc.pass_criteria()
    clnt_msg.client_msg_contains_opt(None, '1')
    clnt_msg.client_msg_contains_opt(None, '8')
    clnt_msg.client_msg_contains_opt(None, '14')
    clnt_msg.client_msg_contains_opt(None, '25')

    references.references_check('RFC')
