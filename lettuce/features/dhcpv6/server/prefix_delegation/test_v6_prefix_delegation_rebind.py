"""DHCPv6 Prefix Delegation"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_msg
from features import srv_control
from features import misc
from features import references


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_rebind_success(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::3')
    srv_control.config_srv_prefix(step, '2001:db8:1::', '0', '90', '92')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
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

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_save_option(step, 'IA_PD')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '2001:db8:1::')

    misc.test_procedure(step)
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REBIND')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    # Response option 25 MUST contain T1 . #set this after server configuration!

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.disabled
def test_prefix_delegation_rebind_fail(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::3')
    srv_control.config_srv_prefix(step, '2001:db8:1::', '0', '90', '92')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_save_option(step, 'IA_PD')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '90')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '3001::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'REBIND')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'T1', '0')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_rebind_fail_dropped(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::3')
    srv_control.config_srv_prefix(step, '2001:db8:1::', '0', '90', '92')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_PD')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3001::/64', '3001::1-3001::ffff')
    srv_control.config_srv_prefix(step, '2001:db8:2::', '0', '90', '92')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REBIND')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    references.references_check(step, 'RFC')
