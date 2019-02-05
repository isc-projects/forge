"""Host Reservation DHCPv4"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_msg
from features import misc
from features import srv_control


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_hostname_hostname_option(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.30-192.168.50.30')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'my.domain.com')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-name',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.30')
    srv_msg.client_does_include_with_value(step, 'hostname', 'some-name')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_include_option(step, 'Response', None, '12')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '12',
                                          None,
                                          'value',
                                          'reserved-name.my.domain.com')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_hostname_fqdn_option(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.30-192.168.50.30')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'my.domain.com')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-name',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'sth6.six.example.com.')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '81')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '81',
                                          None,
                                          'fqdn',
                                          'reserved-name.my.domain.com.')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.30')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'sth6.six.example.com.')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_include_option(step, 'Response', None, '81')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '81',
                                          None,
                                          'fqdn',
                                          'reserved-name.my.domain.com.')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_hostname_hostname_option_and_address(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.20-192.168.50.30')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'my.domain.com')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-name',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'address', '192.168.50.5')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_msg.forge_sleep(step, '2', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    # Client adds to the message hostname with value some-name.
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.5')
    srv_msg.client_does_include_with_value(step, 'hostname', 'some-name')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.5')
    srv_msg.response_check_include_option(step, 'Response', None, '12')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '12',
                                          None,
                                          'value',
                                          'reserved-name.my.domain.com')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_hostname_hostname_option_and_address_2(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.20-192.168.50.30')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'my.domain.com')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.50.5',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'hostname', 'reserved-name')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_msg.forge_sleep(step, '2', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    # Client adds to the message hostname with value some-name.
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.5')
    srv_msg.client_does_include_with_value(step, 'hostname', 'some-name')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.5')
    srv_msg.response_check_include_option(step, 'Response', None, '12')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '12',
                                          None,
                                          'value',
                                          'reserved-name.my.domain.com')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_hostname_hostname_option_and_address_3(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.30')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'my.domain.com')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-name',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'address', '192.168.50.5')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_msg.forge_sleep(step, '2', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    # Client adds to the message hostname with value some-name.
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.5')
    srv_msg.client_does_include_with_value(step, 'hostname', 'some-name')
    srv_msg.client_sets_value(step, 'Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.5')
    srv_msg.response_check_include_option(step, 'Response', None, '12')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '12',
                                          None,
                                          'value',
                                          'reserved-name.my.domain.com')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_hostname_multiple_entries(step):
    misc.test_setup(step)
    # outside of the pool
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.30-192.168.50.30')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'my.domain.com')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-name',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'resderved-name',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:44')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_hostname_duplicated_entries(step):
    misc.test_setup(step)
    # outside of the pool
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.30-192.168.50.30')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'my.domain.com')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-name',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'resderved-name',
                                           '0',
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')
