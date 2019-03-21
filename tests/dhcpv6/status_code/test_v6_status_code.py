"""DHCPv6 Status Codes"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_msg
import srv_control
import references
import misc


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.status_code
def test_v6_statuscode_noaddravail_solicit():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    misc.test_procedure()
    srv_msg.generate_new('client')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content('Response', '13', '3', None, 'statuscode', '2')

    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.status_code
@pytest.mark.request
def test_v6_statuscode_noaddravail_request():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_save_option('IA_NA')
    srv_msg.client_save_option('server-id')
    srv_msg.client_requests_option('7')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.generate_new('IA')
    srv_msg.generate_new('client')
    srv_msg.client_add_saved_option(None)
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content('Response', '13', '3', None, 'statuscode', '2')

    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.status_code
@pytest.mark.renew
def test_v6_statuscode_nobinding_renew():
    # when client id not known
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    # changed after rfc7550
    # Response option 3 MUST contain sub-option 13.
    # Response sub-option 13 from option 3 MUST contain statuscode 3.
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')

    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.status_code
@pytest.mark.renew
@pytest.mark.disabled
def test_v6_statuscode_nobinding_renew_newIA():
    # when client id not known
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.change_message_filed('iaid', '66', 'int')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    # changed after rfc7550
    # Response option 3 MUST contain sub-option 13.
    # Response sub-option 13 from option 3 MUST contain statuscode 3.

    references.references_check('RFC3315')
