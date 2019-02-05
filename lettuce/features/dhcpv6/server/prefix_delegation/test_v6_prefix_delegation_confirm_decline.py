"""DHCPv6 Prefix Delegation"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_control
from features import srv_msg
from features import misc
from features import references


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_IA_and_PD_confirm(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::2-3000::2')
    srv_control.config_srv_prefix(step, '2001:db8:1::', '0', '90', '96')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '2001:db8:1::')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::2')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'IA_PD')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'IA_PD')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'CONFIRM')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '25')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_IA_and_PD_decline(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::5-3000::5')
    srv_control.config_srv_prefix(step, '2001:db8:1::', '0', '90', '96')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::5')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'IA_PD')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'IA_PD')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'DECLINE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '25')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '13')

    references.references_check(step, 'RFC')
