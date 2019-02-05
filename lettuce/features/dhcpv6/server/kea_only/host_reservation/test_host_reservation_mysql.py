"""Host Reservation DHCPv6 stored in MySQL database."""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_control
from features import srv_msg
from features import misc


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v6_host_reservation_mysql_all_values_mac(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.enable_db_backend_reservation(step, 'MySQL')
    srv_control.new_db_backend_reservation(step, 'MySQL', 'hw-address', 'f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation(step, 'hostname', 'reserved-hostname', 'MySQL', '1')
    srv_control.update_db_backend_reservation(step, 'dhcp6_subnet_id', '1', 'MySQL', '1')
    srv_control.ipv6_prefix_db_backend_reservation(step, '3001::', '40', '$(EMPTY)', 'MySQL', '1')
    srv_control.ipv6_address_db_backend_reservation(step, '3000::100', '$(EMPTY)', 'MySQL', '1')
    srv_control.ipv6_address_db_backend_reservation(step, '3000::101', '$(EMPTY)', 'MySQL', '1')
    srv_control.option_db_record_reservation(step,
                                             '32',
                                             '10',
                                             'dhcp6',
                                             '1',
                                             '$(EMPTY)',
                                             '1',
                                             'subnet',
                                             'MySQL',
                                             '1')
    srv_control.upload_db_reservation(step, 'MySQL')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'my.domain.com')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '666')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'IA_PD')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'some-different-name')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_requests_option(step, '32')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::100')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3001::')
    srv_msg.response_check_include_option(step, 'Response', None, '39')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '39',
                                          None,
                                          'fqdn',
                                          'reserved-hostname.my.domain.com')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '777')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'IA_PD')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'some-different-name')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_requests_option(step, '32')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             'NOT ',
                                             'address',
                                             '3000::100')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v6_host_reservation_mysql_all_values_duid(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')

    srv_control.enable_db_backend_reservation(step, 'MySQL')
    srv_control.new_db_backend_reservation(step, 'MySQL', 'duid', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation(step, 'hostname', 'reserved-hostname', 'MySQL', '1')
    srv_control.update_db_backend_reservation(step, 'dhcp6_subnet_id', '1', 'MySQL', '1')
    srv_control.ipv6_prefix_db_backend_reservation(step, '3001::', '40', '$(EMPTY)', 'MySQL', '1')
    srv_control.ipv6_address_db_backend_reservation(step, '3000::100', '$(EMPTY)', 'MySQL', '1')
    srv_control.upload_db_reservation(step, 'MySQL')

    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'my.domain.com')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'IA_PD')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'some-different-name')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::100')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3001::')
    srv_msg.response_check_include_option(step, 'Response', None, '39')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '39',
                                          None,
                                          'fqdn',
                                          'reserved-hostname.my.domain.com')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v6_host_reservation_mysql_all_values_duid_2(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_prefix(step, '3001::', '0', '32', '33')
    srv_control.enable_db_backend_reservation(step, 'MySQL')
    srv_control.new_db_backend_reservation(step,
                                           'MySQL',
                                           'duid',
                                           '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation(step, 'hostname', 'reserved-hostname', 'MySQL', '1')
    srv_control.update_db_backend_reservation(step, 'dhcp6_subnet_id', '1', 'MySQL', '1')
    srv_control.ipv6_prefix_db_backend_reservation(step, '3001::', '40', '$(EMPTY)', 'MySQL', '1')
    srv_control.ipv6_address_db_backend_reservation(step, '3000::100', '$(EMPTY)', 'MySQL', '1')
    srv_control.upload_db_reservation(step, 'MySQL')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'my.domain.com')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'IA_PD')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'some-different-name')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::100')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3001::')
    srv_msg.response_check_include_option(step, 'Response', None, '39')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '39',
                                          None,
                                          'fqdn',
                                          'reserved-hostname.my.domain.com')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v6_host_reservation_mysql_duid_ll_matching(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.enable_db_backend_reservation(step, 'MySQL')
    srv_control.new_db_backend_reservation(step, 'MySQL', 'duid', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation(step, 'dhcp6_subnet_id', '1', 'MySQL', '1')
    srv_control.ipv6_prefix_db_backend_reservation(step, '3001::', '40', '$(EMPTY)', 'MySQL', '1')
    srv_control.ipv6_address_db_backend_reservation(step, '3000::100', '$(EMPTY)', 'MySQL', '1')
    srv_control.upload_db_reservation(step, 'MySQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::100')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v6_host_reservation_mysql_duid_ll_not_matching(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.enable_db_backend_reservation(step, 'MySQL')
    srv_control.new_db_backend_reservation(step, 'MySQL', 'duid', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation(step, 'dhcp6_subnet_id', '1', 'MySQL', '1')
    srv_control.ipv6_address_db_backend_reservation(step, '3000::100', '$(EMPTY)', 'MySQL', '1')
    srv_control.upload_db_reservation(step, 'MySQL')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             'NOT ',
                                             'address',
                                             '3000::100')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             'NOT ',
                                             'address',
                                             '3000::100')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v6_host_reservation_mysql_duid_llt_matching(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.enable_db_backend_reservation(step, 'MySQL')
    srv_control.new_db_backend_reservation(step,
                                           'MySQL',
                                           'duid',
                                           '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')
    # Create new MySQL reservation identified by hw-address f6:f5:f4:f3:f2:01.
    srv_control.update_db_backend_reservation(step, 'dhcp6_subnet_id', '1', 'MySQL', '1')
    srv_control.ipv6_address_db_backend_reservation(step, '3000::100', '$(EMPTY)', 'MySQL', '1')
    srv_control.upload_db_reservation(step, 'MySQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::100')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v6_host_reservation_mysql_duid_llt_not_matching(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.enable_db_backend_reservation(step, 'MySQL')
    srv_control.new_db_backend_reservation(step,
                                           'MySQL',
                                           'duid',
                                           '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')
    # Create new MySQL reservation identified by hw-address f6:f5:f4:f3:f2:01.
    srv_control.update_db_backend_reservation(step, 'dhcp6_subnet_id', '1', 'MySQL', '1')
    srv_control.ipv6_address_db_backend_reservation(step, '3000::100', '$(EMPTY)', 'MySQL', '1')
    srv_control.upload_db_reservation(step, 'MySQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             'NOT ',
                                             'address',
                                             '3000::100')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             'NOT ',
                                             'address',
                                             '3000::100')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v6_host_reservation_mysql_hwaddrr_not_matching(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')

    srv_control.enable_db_backend_reservation(step, 'MySQL')
    srv_control.new_db_backend_reservation(step, 'MySQL', 'hw-address', 'f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation(step, 'dhcp6_subnet_id', '1', 'MySQL', '1')
    srv_control.ipv6_address_db_backend_reservation(step, '3000::100', '$(EMPTY)', 'MySQL', '1')
    srv_control.upload_db_reservation(step, 'MySQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             'NOT ',
                                             'address',
                                             '3000::100')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             'NOT ',
                                             'address',
                                             '3000::100')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::100')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v6_host_reservation_mysql_hwaddrr_matching(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.enable_db_backend_reservation(step, 'MySQL')
    srv_control.new_db_backend_reservation(step, 'MySQL', 'hw-address', 'f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation(step, 'dhcp6_subnet_id', '1', 'MySQL', '1')
    srv_control.ipv6_address_db_backend_reservation(step, '3000::100', '$(EMPTY)', 'MySQL', '1')
    srv_control.upload_db_reservation(step, 'MySQL')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::100')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::100')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v6_host_reservation_mysql_hwaddrr_matching_dualbackend(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.enable_db_backend_reservation(step, 'MySQL')
    srv_control.new_db_backend_reservation(step, 'MySQL', 'hw-address', 'f6:f5:f4:f3:f2:11')
    srv_control.update_db_backend_reservation(step, 'dhcp6_subnet_id', '1', 'MySQL', '1')
    srv_control.ipv6_address_db_backend_reservation(step, '3000::100', '$(EMPTY)', 'MySQL', '1')
    srv_control.upload_db_reservation(step, 'MySQL')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '3000::fff',
                                           '0',
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:01')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::100')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::fff')
