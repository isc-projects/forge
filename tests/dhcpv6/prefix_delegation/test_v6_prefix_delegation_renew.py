"""DHCPv6 Prefix Delegation"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_msg
import references
import srv_control


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_onlyPD_renew():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 92)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.disabled
def test_prefix_delegation_onlyPD_renew_nobinding():
    # this tests will be disabled after RFC 7550 tests will be added
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 92)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 25, 'statuscode', 3)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.disabled
def test_prefix_delegation_onlyPD_renew_nobinding_new_IA_PD():
    # this tests will be disabled after RFC 7550 tests will be added

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 92)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.generate_new('IA_PD')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 25, 'statuscode', 3)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix_delegation_IA_and_PD_renew():

    # this tests will be disabled after RFC 7550 tests will be added
    misc.test_setup()
    # Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
    srv_control.config_srv_subnet('3000::/64', '3000::ffff:ffff:1-3000::ffff:ffff:3')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 92)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_save_option('IA_PD')
    srv_msg.client_add_saved_option(None)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'validlft', 4000)

    references.references_check('RFC')


@pytest.mark.v6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.disabled
def test_prefix_delegation_IA_and_PD_renew_nobindig():

    # this tests will be disabled after RFC 7550 tests will be added
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 92)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    # Response sub-option 13 from option 25 MUST contain statuscode 3. changed after rfc7550
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 3)

    references.references_check('RFC')
