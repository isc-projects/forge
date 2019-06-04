"""Kea subnet-id sanity-check"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_control
import srv_msg


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.subnet_id_sanity_check
@pytest.mark.abc
def test_v6_sanity_check_subnet_id_fix_able():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', '666', '0')
    srv_control.set_conf_parameter_global('sanity-checks', '{"lease-checks":"fix"}')
    srv_control.open_control_channel()

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '2001:db8::1')

    srv_msg.lease_file_contains('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.lease_file_contains('666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')

    srv_control.start_srv('DHCP', 'stopped')
    srv_control.clear_leases('logs')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', '999', '0')
    srv_control.set_conf_parameter_global('sanity-checks', '{"lease-checks":"fix"}')
    srv_control.open_control_channel()

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_msg.log_contains('DHCPSRV_LEASE_SANITY_FIXED The lease 2001:db8::1 with subnet-id 666 failed subnet-id checks, but was corrected to subnet-id 999.')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '2001:db8::1')


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.subnet_id_sanity_check
@pytest.mark.abc
def test_v6_sanity_check_subnet_id_fix_able_double_restart():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', '666', '0')
    srv_control.set_conf_parameter_global('sanity-checks', '{"lease-checks":"fix"}')
    srv_control.open_control_channel()

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '2001:db8::1')

    srv_msg.lease_file_contains('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.lease_file_contains('666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')

    srv_control.start_srv('DHCP', 'stopped')
    srv_control.clear_leases('logs')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', '999', '0')
    srv_control.set_conf_parameter_global('sanity-checks', '{"lease-checks":"fix"}')
    srv_control.open_control_channel()

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_msg.log_contains('DHCPSRV_LEASE_SANITY_FIXED The lease 2001:db8::1 with subnet-id 666 failed subnet-id checks, but was corrected to subnet-id 999.')

    srv_msg.forge_sleep('13', 'seconds')

    srv_control.start_srv('DHCP', 'stopped')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', '999', '0')
    srv_control.set_conf_parameter_global('sanity-checks', '{"lease-checks":"fix"}')
    srv_control.open_control_channel()

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '987654321')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '2001:db8::1')

    # Pause the Test.


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.subnet_id_sanity_check
@pytest.mark.abc
def test_v6_sanity_check_subnet_id_fix_unable():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', '666', '0')
    srv_control.set_conf_parameter_global('sanity-checks', '{"lease-checks":"fix"}')
    srv_control.open_control_channel()

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '2001:db8::1')

    srv_msg.lease_file_contains('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.lease_file_contains('666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')

    srv_control.start_srv('DHCP', 'stopped')

    srv_control.clear_leases('logs')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', '999', '0')
    srv_control.set_conf_parameter_global('sanity-checks', '{"lease-checks":"fix"}')
    srv_control.open_control_channel()

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '2001:db8::1')


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.subnet_id_sanity_check
@pytest.mark.abc
def test_v6_sanity_check_subnet_id_fix_del_unable():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', '666', '0')
    srv_control.set_conf_parameter_global('sanity-checks', '{"lease-checks":"fix-del"}')
    srv_control.open_control_channel()

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '2001:db8::1')

    srv_msg.lease_file_contains('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.lease_file_contains('666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')

    srv_control.start_srv('DHCP', 'stopped')

    srv_control.clear_leases('logs')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', '999', '0')
    srv_control.set_conf_parameter_global('sanity-checks', '{"lease-checks":"fix-del"}')
    srv_control.open_control_channel()

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.subnet_id_sanity_check
@pytest.mark.abc
def test_v6_sanity_check_subnet_id_fix_del_able():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', '666', '0')
    srv_control.set_conf_parameter_global('sanity-checks', '{"lease-checks":"fix-del"}')
    srv_control.open_control_channel()

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '2001:db8::1')

    srv_msg.lease_file_contains('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.lease_file_contains('666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', '999', '0')
    srv_control.set_conf_parameter_global('sanity-checks', '{"lease-checks":"fix-del"}')
    srv_control.open_control_channel()

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'reconfigured')


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.subnet_id_sanity_check
@pytest.mark.abc
def test_v6_sanity_check_subnet_id_warn():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', '666', '0')
    srv_control.set_conf_parameter_global('sanity-checks', '{"lease-checks":"warn"}')
    srv_control.open_control_channel()

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '2001:db8::1')

    srv_msg.lease_file_contains('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.lease_file_contains('666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', '999', '0')
    srv_control.set_conf_parameter_global('sanity-checks', '{"lease-checks":"warn"}')
    srv_control.open_control_channel()

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'reconfigured')

    srv_msg.forge_sleep('2', 'seconds')

    srv_msg.log_contains('DHCPSRV_LEASE_SANITY_FAIL The lease 2001:db8::1 with subnet-id 666 failed subnet-id checks.')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:33')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content('Response', '13', '3', None, 'statuscode', '2')


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.subnet_id_sanity_check
@pytest.mark.abc
def test_v6_sanity_check_subnet_id_del_renew():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', '666', '0')
    srv_control.set_conf_parameter_global('sanity-checks', '{"lease-checks":"del"}')
    srv_control.open_control_channel()

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '2001:db8::1')

    srv_msg.lease_file_contains('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.lease_file_contains('666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')

    srv_control.start_srv('DHCP', 'stopped')

    srv_control.clear_leases('logs')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', '999', '0')
    srv_control.set_conf_parameter_global('sanity-checks', '{"lease-checks":"del"}')
    srv_control.open_control_channel()

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')
    srv_msg.forge_sleep('2', 'seconds')

    srv_msg.log_contains('DHCPSRV_LEASE_SANITY_FAIL_DISCARD The lease 2001:db8::1 with subnet-id 666 failed subnet-id checks and was dropped.')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '2001:db8::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content('Response', '13', '3', None, 'statuscode', '2')

    srv_msg.lease_file_contains('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.lease_file_contains('666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')

    srv_msg.lease_file_contains('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.lease_file_contains('999,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')

    srv_msg.lease_file_doesnt_contain('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.lease_file_doesnt_contain('999,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:22')


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.subnet_id_sanity_check
@pytest.mark.abc
def test_v6_sanity_check_subnet_id_del():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', '666', '0')
    srv_control.set_conf_parameter_global('sanity-checks', '{"lease-checks":"del"}')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '2001:db8::1')

    srv_msg.lease_file_contains('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.lease_file_contains('666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')

    srv_control.start_srv('DHCP', 'stopped')

    srv_control.clear_leases('logs')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', '999', '0')
    srv_control.set_conf_parameter_global('sanity-checks', '{"lease-checks":"del"}')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')
    srv_msg.forge_sleep('2', 'seconds')

    srv_msg.log_contains('DHCPSRV_LEASE_SANITY_FAIL_DISCARD The lease 2001:db8::1 with subnet-id 666 failed subnet-id checks and was dropped.')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '7654321')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '2001:db8::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '2001:db8::1')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"lease6-get","arguments":{"ip-address": "2001:db8::1"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"lease6-get","arguments":{"subnet-id":666,"identifier-type":"duid", "identifier": "00:03:00:01:f6:f5:f4:f3:f2:01"}}')
    srv_msg.lease_file_contains('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.lease_file_contains('666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')
    # Pause the Test.

    # File stored in kea-leases6.csv MUST contain line or phrase: 2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:22
    # File stored in kea-leases6.csv MUST contain line or phrase: 999,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:22


@pytest.mark.v6
@pytest.mark.kea_only
@pytest.mark.subnet_id_sanity_check
@pytest.mark.abc
def test_v6_sanity_check_subnet_id_none():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', '666', '0')
    srv_control.set_conf_parameter_global('sanity-checks', '{"lease-checks":"none"}')
    srv_control.open_control_channel()

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '2001:db8::1')

    srv_msg.lease_file_contains('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.lease_file_contains('666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', '999', '0')
    srv_control.set_conf_parameter_global('sanity-checks', '{"lease-checks":"none"}')
    srv_control.open_control_channel()

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'reconfigured')
    srv_msg.forge_sleep('2', 'seconds')
    srv_msg.lease_file_contains('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.lease_file_contains('666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sanity_check_subnet_id():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', '666', '0')
    srv_control.set_conf_parameter_global('sanity-checks', '{"lease-checks":"fix"}')
    srv_control.open_control_channel()

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "config-get","arguments":  {} }')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "list-commands","arguments":  {} }')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '2001:db8::1')

    srv_msg.lease_file_contains('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.lease_file_contains('666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')

    srv_control.start_srv('DHCP', 'stopped')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::2')
    srv_control.set_conf_parameter_subnet('id', '888', '0')
    srv_control.set_conf_parameter_global('sanity-checks', '{"lease-checks":"fix-del"}')
    srv_control.open_control_channel()

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    srv_msg.forge_sleep('12', 'seconds')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::2')
    srv_control.set_conf_parameter_subnet('id', '999', '0')
    srv_control.set_conf_parameter_global('sanity-checks', '{"lease-checks":"fix-del"}')
    srv_control.open_control_channel()

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'reconfigured')
    srv_msg.forge_sleep('12', 'seconds')

    # Using UNIX socket on server in path control_socket send {"command": "config-get","arguments":  {} }
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '2001:db8::2')
    srv_msg.forge_sleep('10', 'seconds')

    # Using UNIX socket on server in path control_socket send {"command": "config-get","arguments":  {} }
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:33')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content('Response', '13', '3', None, 'statuscode', '2')
    # Response option 3 MUST contain sub-option 5.
    # Response sub-option 5 from option 3 MUST contain address 2001:db8::2.

    # Pause the Test.


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sanity_check_shared_subnet_id():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.set_conf_parameter_subnet('id', '666', '0')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.set_conf_parameter_subnet('id', '777', '1')
    srv_control.shared_subnet('0', '0')
    srv_control.shared_subnet('1', '0')
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', '0')
    srv_control.set_conf_parameter_global('sanity-checks', '{"lease-checks":"fix-del"}')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "config-get","arguments":  {} }')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    # Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_sets_value('Client', 'ia_id', '7654321')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    srv_msg.lease_file_contains('2001:db8:a::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.lease_file_contains('666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')
    srv_msg.lease_file_contains('2001:db8:b::1,00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.lease_file_contains('777,3000,0,7654321,128,0,0,,f6:f5:f4:f3:f2:02')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.set_conf_parameter_subnet('id', '888', '0')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.set_conf_parameter_subnet('id', '999', '1')
    srv_control.shared_subnet('0', '0')
    srv_control.shared_subnet('1', '0')
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', '0')
    srv_control.set_conf_parameter_global('sanity-checks', '{"lease-checks":"fix"}')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'reconfigured')

    srv_msg.forge_sleep('10', 'seconds')
