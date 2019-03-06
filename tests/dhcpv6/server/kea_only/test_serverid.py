"""Configure Kea's server-id."""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_msg
import srv_control


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.server_id
def test_v6_server_id_llt():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_id('LLT', '00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response',
                                          '1',
                                          'NOT ',
                                          'duid',
                                          '00:01:00:01:52:7b:a8:f0:08:00:27:58:f1:e8')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_option_content('Response',
                                          '2',
                                          None,
                                          'duid',
                                          '00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.server_id
def test_v6_server_id_en():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_id('EN', '00:02:00:00:09:BF:87:AB:EF:7A:5B:B5:45')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '2')
    # Response option 2 MUST contain duid 00:02:00:00:09:BF:87:AB:EF:7A:5B:B5:45.
    srv_msg.response_check_include_option('Response', None, '1')
    # Response option 1 MUST NOT contain duid 00:02:00:00:09:BF:87:AB:EF:7A:5B:B5:45.


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.server_id
def test_v6_server_id_ll():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_id('LL', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_option_content('Response',
                                          '2',
                                          None,
                                          'duid',
                                          '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response',
                                          '1',
                                          'NOT ',
                                          'duid',
                                          '00:03:00:01:ff:ff:ff:ff:ff:01')
