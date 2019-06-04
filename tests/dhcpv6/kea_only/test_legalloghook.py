"""Kea6 Legal logging hook"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_control
import srv_msg
from forge_cfg import world


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v6_loggers_legal_log_hook_address_assigned_duid():

    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', '100')
    srv_control.set_time('rebind-timer', '200')
    srv_control.set_time('preferred-lifetime', '400')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::50')
    srv_control.config_srv_prefix('3001::', '0', '90', '94')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
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
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v6_loggers_legal_log_hook_address_assigned_duid_mysql():

    srv_msg.remove_from_db_table('logs', 'MySQL')

    misc.test_setup()
    srv_control.set_time('renew-timer', '100')
    srv_control.set_time('rebind-timer', '200')
    srv_control.set_time('preferred-lifetime', '400')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::50')
    srv_control.config_srv_prefix('3001::', '0', '90', '94')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook('1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook('1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook('1', 'type', 'mysql')
    srv_control.add_parameter_to_hook('1', 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
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
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    srv_msg.table_contains_line('logs',
                                'MySQL',
                                None,
                                'Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v6_loggers_legal_log_hook_address_assigned_duid_pgsql():

    srv_msg.remove_from_db_table('logs', 'PostgreSQL')

    misc.test_setup()
    srv_control.set_time('renew-timer', '100')
    srv_control.set_time('rebind-timer', '200')
    srv_control.set_time('preferred-lifetime', '400')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::50')
    srv_control.config_srv_prefix('3001::', '0', '90', '94')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook('1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook('1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook('1', 'type', 'postgresql')
    srv_control.add_parameter_to_hook('1', 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
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
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    srv_msg.table_contains_line('logs',
                                'PostgreSQL',
                                None,
                                'Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v6_loggers_legal_log_hook_address_renewed_duid():

    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', '100')
    srv_control.set_time('rebind-timer', '200')
    srv_control.set_time('preferred-lifetime', '400')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::50')
    srv_control.config_srv_prefix('3001::', '0', '90', '94')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
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
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
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

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line(world.f_cfg.data_join('kea-legal*.txt'),
                               None,
                               'Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')
    srv_msg.file_contains_line(world.f_cfg.data_join('kea-legal*.txt'),
                               None,
                               'Address:3000::5 has been renewed for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v6_loggers_legal_log_hook_address_renewed_duid_mysql():

    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', 'MySQL')

    misc.test_setup()
    srv_control.set_time('renew-timer', '100')
    srv_control.set_time('rebind-timer', '200')
    srv_control.set_time('preferred-lifetime', '400')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::50')
    srv_control.config_srv_prefix('3001::', '0', '90', '94')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook('1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook('1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook('1', 'type', 'mysql')
    srv_control.add_parameter_to_hook('1', 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
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
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
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

    srv_msg.table_contains_line('logs',
                                'MySQL',
                                None,
                                'Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')
    srv_msg.table_contains_line('logs',
                                'MySQL',
                                None,
                                'Address:3000::5 has been renewed for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v6_loggers_legal_log_hook_address_renewed_duid_pgsql():

    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', 'PostgreSQL')

    misc.test_setup()
    srv_control.set_time('renew-timer', '100')
    srv_control.set_time('rebind-timer', '200')
    srv_control.set_time('preferred-lifetime', '400')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::50')
    srv_control.config_srv_prefix('3001::', '0', '90', '94')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook('1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook('1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook('1', 'type', 'postgresql')
    srv_control.add_parameter_to_hook('1', 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
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
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
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

    srv_msg.table_contains_line('logs',
                                'PostgreSQL',
                                None,
                                'Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')
    srv_msg.table_contains_line('logs',
                                'PostgreSQL',
                                None,
                                'Address:3000::5 has been renewed for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v6_loggers_legal_log_hook_address_rebind_duid():

    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', '100')
    srv_control.set_time('rebind-timer', '200')
    srv_control.set_time('preferred-lifetime', '400')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::50')
    srv_control.config_srv_prefix('3001::', '0', '90', '94')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
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
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REBIND')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line(world.f_cfg.data_join('kea-legal*.txt'),
                               None,
                               'Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')
    # Spec says that when we are rebinding address it will be logged 'renewed', misleading :/
    srv_msg.file_contains_line(world.f_cfg.data_join('kea-legal*.txt'),
                               None,
                               'Address:3000::5 has been renewed for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v6_loggers_legal_log_hook_address_rebind_duid_pgsql():

    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', 'PostgreSQL')

    misc.test_setup()
    srv_control.set_time('renew-timer', '100')
    srv_control.set_time('rebind-timer', '200')
    srv_control.set_time('preferred-lifetime', '400')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::50')
    srv_control.config_srv_prefix('3001::', '0', '90', '94')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook('1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook('1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook('1', 'type', 'postgresql')
    srv_control.add_parameter_to_hook('1', 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
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
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REBIND')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    srv_msg.table_contains_line('logs',
                                'PostgreSQL',
                                None,
                                'Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')
    # Spec says that when we are rebinding address it will be logged 'renewed', misleading :/
    srv_msg.table_contains_line('logs',
                                'PostgreSQL',
                                None,
                                'Address:3000::5 has been renewed for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v6_loggers_legal_log_hook_address_rebind_duid_mysql():

    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', 'MySQL')

    misc.test_setup()
    srv_control.set_time('renew-timer', '100')
    srv_control.set_time('rebind-timer', '200')
    srv_control.set_time('preferred-lifetime', '400')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::50')
    srv_control.config_srv_prefix('3001::', '0', '90', '94')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook('1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook('1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook('1', 'type', 'mysql')
    srv_control.add_parameter_to_hook('1', 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
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
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REBIND')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    srv_msg.table_contains_line('logs',
                                'MySQL',
                                None,
                                'Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')
    # Spec says that when we are rebinding address it will be logged 'renewed', misleading :/
    srv_msg.table_contains_line('logs',
                                'MySQL',
                                None,
                                'Address:3000::5 has been renewed for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v6_loggers_legal_log_hook_address_assigned_docsis_modem():

    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', '100')
    srv_control.set_time('rebind-timer', '200')
    srv_control.set_time('preferred-lifetime', '400')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::50')
    srv_control.config_srv_prefix('3001::', '0', '90', '94')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.run_command('"mac-sources": [ "docsis-modem" ]')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
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
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption('Client', '36', 'f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'vendor-specific-info')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line(world.f_cfg.data_join('kea-legal*.txt'),
                               None,
                               'Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:01 (from DOCSIS MODEM)')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v6_loggers_legal_log_hook_address_assigned_docsis_modem_pgsql():

    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', 'PostgreSQL')

    misc.test_setup()
    srv_control.set_time('renew-timer', '100')
    srv_control.set_time('rebind-timer', '200')
    srv_control.set_time('preferred-lifetime', '400')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::50')
    srv_control.config_srv_prefix('3001::', '0', '90', '94')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook('1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook('1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook('1', 'type', 'postgresql')
    srv_control.add_parameter_to_hook('1', 'user', '$(DB_USER)')
    srv_control.run_command('"mac-sources": [ "docsis-modem" ]')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
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
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption('Client', '36', 'f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'vendor-specific-info')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    srv_msg.table_contains_line('logs',
                                'PostgreSQL',
                                None,
                                'Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:01 (from DOCSIS MODEM)')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v6_loggers_legal_log_hook_address_assigned_docsis_modem_mysql():

    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', 'MySQL')

    misc.test_setup()
    srv_control.set_time('renew-timer', '100')
    srv_control.set_time('rebind-timer', '200')
    srv_control.set_time('preferred-lifetime', '400')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::50')
    srv_control.config_srv_prefix('3001::', '0', '90', '94')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook('1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook('1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook('1', 'type', 'mysql')
    srv_control.add_parameter_to_hook('1', 'user', '$(DB_USER)')
    srv_control.run_command('"mac-sources": [ "docsis-modem" ]')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
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
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption('Client', '36', 'f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'vendor-specific-info')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    srv_msg.table_contains_line('logs',
                                'MySQL',
                                None,
                                'Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:01 (from DOCSIS MODEM)')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v6_loggers_legal_log_hook_address_assigned_docsis_cmts():

    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', '100')
    srv_control.set_time('rebind-timer', '200')
    srv_control.set_time('preferred-lifetime', '400')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::50')
    srv_control.config_srv_prefix('3001::', '0', '90', '94')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.run_command('"mac-sources": [ "docsis-cmts" ]')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
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

    srv_msg.client_sets_value('RelayAgent', 'enterprisenum', '4491')
    srv_msg.client_does_include('RelayAgent', None, 'vendor-class')
    srv_msg.add_vendor_suboption('RelayAgent', '1026', '00:f5:f4:00:f2:01')
    srv_msg.client_does_include('RelayAgent', None, 'vendor-specific-info')
    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')
    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line(world.f_cfg.data_join('kea-legal*.txt'),
                               None,
                               'Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:01 and hardware address: hwtype=1 00:f5:f4:00:f2:01 (from DOCSIS CMTS)')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v6_loggers_legal_log_hook_address_assigned_docsis_cmts_pgsql():

    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', 'PostgreSQL')

    misc.test_setup()
    srv_control.set_time('renew-timer', '100')
    srv_control.set_time('rebind-timer', '200')
    srv_control.set_time('preferred-lifetime', '400')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::50')
    srv_control.config_srv_prefix('3001::', '0', '90', '94')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook('1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook('1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook('1', 'type', 'postgresql')
    srv_control.add_parameter_to_hook('1', 'user', '$(DB_USER)')
    srv_control.run_command('"mac-sources": [ "docsis-cmts" ]')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
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

    srv_msg.client_sets_value('RelayAgent', 'enterprisenum', '4491')
    srv_msg.client_does_include('RelayAgent', None, 'vendor-class')
    srv_msg.add_vendor_suboption('RelayAgent', '1026', '00:f5:f4:00:f2:01')
    srv_msg.client_does_include('RelayAgent', None, 'vendor-specific-info')
    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')

    srv_msg.table_contains_line('logs',
                                'PostgreSQL',
                                None,
                                'Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:01 and hardware address: hwtype=1 00:f5:f4:00:f2:01 (from DOCSIS CMTS)')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v6_loggers_legal_log_hook_address_assigned_docsis_cmts_mysql():

    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', 'MySQL')

    misc.test_setup()
    srv_control.set_time('renew-timer', '100')
    srv_control.set_time('rebind-timer', '200')
    srv_control.set_time('preferred-lifetime', '400')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::50')
    srv_control.config_srv_prefix('3001::', '0', '90', '94')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook('1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook('1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook('1', 'type', 'mysql')
    srv_control.add_parameter_to_hook('1', 'user', '$(DB_USER)')
    srv_control.run_command('"mac-sources": [ "docsis-cmts" ]')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
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

    srv_msg.client_sets_value('RelayAgent', 'enterprisenum', '4491')
    srv_msg.client_does_include('RelayAgent', None, 'vendor-class')
    srv_msg.add_vendor_suboption('RelayAgent', '1026', '00:f5:f4:00:f2:01')
    srv_msg.client_does_include('RelayAgent', None, 'vendor-specific-info')
    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')

    srv_msg.table_contains_line('logs',
                                'MySQL',
                                None,
                                'Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:01 and hardware address: hwtype=1 00:f5:f4:00:f2:01 (from DOCSIS CMTS)')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v6_loggers_legal_log_hook_address_assigned_relay():

    misc.test_procedure()
    srv_msg.remove_file_from_server(world.f_cfg.data_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.set_time('renew-timer', '100')
    srv_control.set_time('rebind-timer', '200')
    srv_control.set_time('preferred-lifetime', '400')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::50')
    srv_control.config_srv_prefix('3001::', '0', '90', '94')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_sets_value('Client', 'DUID', '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('Client', 'enterprisenum', '666')
    srv_msg.client_sets_value('Client', 'subscriber_id', '50')
    srv_msg.client_does_include('Client', None, 'remote-id')
    srv_msg.client_does_include('Client', None, 'subscriber-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '3000::1005')
    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(5)

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')
    srv_msg.copy_remote(world.f_cfg.data_join('kea-legal*.txt'))
    srv_msg.file_contains_line(world.f_cfg.data_join('kea-legal*.txt'),
                               None,
                               'Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01 and hardware address: hwtype=1 f6:f5:f4:f3:f2:01 (from DUID) connected via relay')
    srv_msg.file_contains_line(world.f_cfg.data_join('kea-legal*.txt'),
                               None,
                               'connected via relay at address:')
    srv_msg.file_contains_line(world.f_cfg.data_join('kea-legal*.txt'),
                               None,
                               'for client on link address: 3000::1005, hop count: 5')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v6_loggers_legal_log_hook_address_assigned_relay_pgsql():

    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', 'PostgreSQL')

    misc.test_setup()
    srv_control.set_time('renew-timer', '100')
    srv_control.set_time('rebind-timer', '200')
    srv_control.set_time('preferred-lifetime', '400')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::50')
    srv_control.config_srv_prefix('3001::', '0', '90', '94')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook('1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook('1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook('1', 'type', 'postgresql')
    srv_control.add_parameter_to_hook('1', 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_sets_value('Client', 'DUID', '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('Client', 'enterprisenum', '666')
    srv_msg.client_sets_value('Client', 'subscriber_id', '50')
    srv_msg.client_does_include('Client', None, 'remote-id')
    srv_msg.client_does_include('Client', None, 'subscriber-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '3000::1005')
    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(5)

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')

    srv_msg.table_contains_line('logs',
                                'PostgreSQL',
                                None,
                                'Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01 and hardware address: hwtype=1 f6:f5:f4:f3:f2:01 (from DUID) connected via relay')
    srv_msg.table_contains_line('logs', 'PostgreSQL', None, 'connected via relay at address:')
    srv_msg.table_contains_line('logs',
                                'PostgreSQL',
                                None,
                                'for client on link address: 3000::1005, hop count: 5')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v6_loggers_legal_log_hook_address_assigned_relay_mysql():

    misc.test_procedure()
    srv_msg.remove_from_db_table('logs', 'MySQL')

    misc.test_setup()
    srv_control.set_time('renew-timer', '100')
    srv_control.set_time('rebind-timer', '200')
    srv_control.set_time('preferred-lifetime', '400')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::50')
    srv_control.config_srv_prefix('3001::', '0', '90', '94')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook('1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook('1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook('1', 'type', 'mysql')
    srv_control.add_parameter_to_hook('1', 'user', '$(DB_USER)')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_sets_value('Client', 'DUID', '00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('Client', 'enterprisenum', '666')
    srv_msg.client_sets_value('Client', 'subscriber_id', '50')
    srv_msg.client_does_include('Client', None, 'remote-id')
    srv_msg.client_does_include('Client', None, 'subscriber-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '3000::1005')
    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(5)

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')

    srv_msg.table_contains_line('logs',
                                'MySQL',
                                None,
                                'Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01 and hardware address: hwtype=1 f6:f5:f4:f3:f2:01 (from DUID) connected via relay')
    srv_msg.table_contains_line('logs', 'MySQL', None, 'connected via relay at address:')
    srv_msg.table_contains_line('logs',
                                'MySQL',
                                None,
                                'for client on link address: 3000::1005, hop count: 5')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v6_loggers_legal_log_hook_with_flex_id_address_assigned_mysql():

    srv_msg.remove_from_db_table('logs', 'MySQL')

    misc.test_setup()
    srv_control.set_time('renew-timer', '100')
    srv_control.set_time('rebind-timer', '200')
    srv_control.set_time('preferred-lifetime', '400')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::50')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           '0',
                                           'flex-id',
                                           '01:02:03:04:05:06')
    srv_control.host_reservation_in_subnet_add_value('0', '0', 'address', '3000::f')
    srv_control.config_srv_prefix('3001::', '0', '90', '94')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook('1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook('1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook('1', 'type', 'mysql')
    srv_control.add_parameter_to_hook('1', 'user', '$(DB_USER)')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook('2',
                                      'identifier-expression',
                                      'vendor[4491].option[1026].hex')
    srv_control.add_line('"host-reservation-identifiers": [  "duid",  "flex-id" ]')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption('Client', '1026', '01:02:03:04:05:06')
    srv_msg.client_does_include('Client', None, 'vendor-specific-info')

    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::f')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption('Client', '1026', '01:02:03:04:05:06')
    srv_msg.client_does_include('Client', None, 'vendor-specific-info')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    srv_msg.table_contains_line('logs',
                                'MySQL',
                                None,
                                'Address:3000::f has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.kea_only
@pytest.mark.legal_logging
def test_v6_loggers_legal_log_hook_with_flex_id_address_assigned_pgsql():

    srv_msg.remove_from_db_table('logs', 'PostgreSQL')

    misc.test_setup()
    srv_control.set_time('renew-timer', '100')
    srv_control.set_time('rebind-timer', '200')
    srv_control.set_time('preferred-lifetime', '400')
    srv_control.set_time('valid-lifetime', '600')
    srv_control.config_srv_subnet('3000::/64', '3000::5-3000::50')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           '0',
                                           'flex-id',
                                           '01:02:03:04:05:06')
    srv_control.host_reservation_in_subnet_add_value('0', '0', 'address', '3000::f')
    srv_control.config_srv_prefix('3001::', '0', '90', '94')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_parameter_to_hook('1', 'name', '$(DB_NAME)')
    srv_control.add_parameter_to_hook('1', 'password', '$(DB_PASSWD)')
    srv_control.add_parameter_to_hook('1', 'type', 'postgresql')
    srv_control.add_parameter_to_hook('1', 'user', '$(DB_USER)')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook('2',
                                      'identifier-expression',
                                      'vendor[4491].option[1026].hex')
    srv_control.add_line('"host-reservation-identifiers": [  "duid",  "flex-id" ]')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption('Client', '1026', '01:02:03:04:05:06')
    srv_msg.client_does_include('Client', None, 'vendor-specific-info')

    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::f')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption('Client', '1026', '01:02:03:04:05:06')
    srv_msg.client_does_include('Client', None, 'vendor-specific-info')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    srv_msg.table_contains_line('logs',
                                'PostgreSQL',
                                None,
                                'Address:3000::f has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)')
