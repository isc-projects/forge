# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea subnet-id sanity-check"""

# pylint: disable=line-too-long

import pytest

from src import misc
from src import srv_control
from src import srv_msg

from src.protosupport.multi_protocol_functions import lease_file_contains, lease_file_doesnt_contain
from src.protosupport.multi_protocol_functions import log_contains


@pytest.mark.v6
@pytest.mark.subnet_id_sanity_check
def test_v6_sanity_check_subnet_id_fix_able():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', 666, 0)
    srv_control.set_conf_parameter_global('sanity-checks', {"lease-checks": "fix"})
    srv_control.add_unix_socket()

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8::1')

    lease_file_contains('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    lease_file_contains('666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')

    srv_control.start_srv('DHCP', 'stopped')
    srv_control.clear_some_data('logs')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::2')
    srv_control.set_conf_parameter_subnet('id', 999, 0)
    srv_control.set_conf_parameter_global('sanity-checks', {"lease-checks": "fix"})
    srv_control.add_unix_socket()

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    log_contains('DHCPSRV_LEASE_SANITY_FIXED The lease 2001:db8::1 with subnet-id 666 failed subnet-id checks, but was corrected to subnet-id 999.')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8::2')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8::1')


@pytest.mark.v6
@pytest.mark.subnet_id_sanity_check
def test_v6_sanity_check_subnet_id_fix_able_double_restart():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', 666, 0)
    srv_control.set_conf_parameter_global('sanity-checks', {"lease-checks": "fix"})
    srv_control.add_unix_socket()

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8::1')

    lease_file_contains('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    lease_file_contains('666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')

    srv_control.start_srv('DHCP', 'stopped')
    srv_control.clear_some_data('logs')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::2')
    srv_control.set_conf_parameter_subnet('id', 999, 0)
    srv_control.set_conf_parameter_global('sanity-checks', {"lease-checks": "fix"})
    srv_control.add_unix_socket()

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    log_contains('DHCPSRV_LEASE_SANITY_FIXED The lease 2001:db8::1 with subnet-id 666 failed subnet-id checks, but was corrected to subnet-id 999.')

    srv_msg.forge_sleep(13, 'seconds')

    srv_control.start_srv('DHCP', 'stopped')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::2')
    srv_control.set_conf_parameter_subnet('id', 999, 0)
    srv_control.set_conf_parameter_global('sanity-checks', {"lease-checks": "fix"})
    srv_control.add_unix_socket()

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '987654321')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8::2')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8::1')


@pytest.mark.v6
@pytest.mark.subnet_id_sanity_check
def test_v6_sanity_check_subnet_id_fix_unable():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', 666, 0)
    srv_control.set_conf_parameter_global('sanity-checks', {"lease-checks": "fix"})
    srv_control.add_unix_socket()

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8::1')

    lease_file_contains('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    lease_file_contains('666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')

    srv_control.start_srv('DHCP', 'stopped')

    srv_control.clear_some_data('logs')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', 999, 0)
    srv_control.set_conf_parameter_global('sanity-checks', {"lease-checks": "fix"})
    srv_control.add_unix_socket()

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8::1')


@pytest.mark.v6
@pytest.mark.subnet_id_sanity_check
def test_v6_sanity_check_subnet_id_fix_del_unable():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', 666, 0)
    srv_control.set_conf_parameter_global('sanity-checks', {"lease-checks": "fix-del"})
    srv_control.add_unix_socket()

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8::1')

    lease_file_contains('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    lease_file_contains('666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')

    srv_control.start_srv('DHCP', 'stopped')

    srv_control.clear_some_data('logs')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', 999, 0)
    srv_control.set_conf_parameter_global('sanity-checks', {"lease-checks": "fix-del"})
    srv_control.add_unix_socket()

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')


@pytest.mark.v6
@pytest.mark.subnet_id_sanity_check
def test_v6_sanity_check_subnet_id_fix_del_able():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', 666, 0)
    srv_control.set_conf_parameter_global('sanity-checks', {"lease-checks": "fix-del"})
    srv_control.add_unix_socket()

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8::1')

    lease_file_contains('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    lease_file_contains('666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', 999, 0)
    srv_control.set_conf_parameter_global('sanity-checks', {"lease-checks": "fix-del"})
    srv_control.add_unix_socket()

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'reconfigured')


@pytest.mark.v6
@pytest.mark.subnet_id_sanity_check
def test_v6_sanity_check_subnet_id_warn():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', 666, 0)
    srv_control.set_conf_parameter_global('sanity-checks', {"lease-checks": "warn"})
    srv_control.add_unix_socket()

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8::1')

    lease_file_contains('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    lease_file_contains('666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', 999, 0)
    srv_control.set_conf_parameter_global('sanity-checks', {"lease-checks": "warn"})
    srv_control.add_unix_socket()

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'reconfigured')

    srv_msg.forge_sleep(2, 'seconds')

    log_contains('DHCPSRV_LEASE_SANITY_FAIL The lease 2001:db8::1 with subnet-id 666 failed subnet-id checks')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:33')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)


@pytest.mark.v6
@pytest.mark.subnet_id_sanity_check
def test_v6_sanity_check_subnet_id_del_renew():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', 666, 0)
    srv_control.set_conf_parameter_global('sanity-checks', {"lease-checks": "del"})
    srv_control.add_unix_socket()

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8::1')

    lease_file_contains('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    lease_file_contains('666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')

    srv_control.start_srv('DHCP', 'stopped')

    srv_control.clear_some_data('logs')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', 999, 0)
    srv_control.set_conf_parameter_global('sanity-checks', {"lease-checks": "del"})
    srv_control.add_unix_socket()

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')
    srv_msg.forge_sleep(2, 'seconds')

    log_contains('DHCPSRV_LEASE_SANITY_FAIL_DISCARD The lease 2001:db8::1 with subnet-id 666 failed'
                 ' subnet-id checks (the lease should have subnet-id 999) and was dropped.')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)

    lease_file_contains('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    lease_file_contains('666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')

    lease_file_contains('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    lease_file_contains('999,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')

    lease_file_doesnt_contain('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:22')
    lease_file_doesnt_contain('999,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:22')


@pytest.mark.v6
@pytest.mark.subnet_id_sanity_check
@pytest.mark.disabled
def test_v6_sanity_check_subnet_id_del():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', 666, 0)
    srv_control.set_conf_parameter_global('sanity-checks', {"lease-checks": "del"})
    srv_control.add_unix_socket()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8::1')

    # lease should be available via lease6-get
    resp = srv_msg.send_ctrl_cmd_via_socket('{"command":"lease6-get","arguments":{"ip-address": "2001:db8::1"}}')
    assert resp['arguments']['subnet-id'] == 666

    # it should be in lease file as well
    lease_file_contains('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    lease_file_contains('666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')

    srv_control.start_srv('DHCP', 'stopped')

    srv_control.clear_some_data('logs')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', 999, 0)
    srv_control.set_conf_parameter_global('sanity-checks', {"lease-checks": "del"})
    srv_control.add_unix_socket()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')
    srv_msg.forge_sleep(2, 'seconds')

    log_contains('DHCPSRV_LEASE_SANITY_FAIL_DISCARD The lease 2001:db8::1 with subnet-id 666 failed'
                 ' subnet-id checks (the lease should have subnet-id 999) and was dropped.')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '7654321')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8::1')

    # old lease from subnet-id 666 should not be available while new lease from subnet-id 999 should be
    resp = srv_msg.send_ctrl_cmd_via_socket('{"command":"lease6-get","arguments":{"ip-address": "2001:db8::1"}}')
    assert resp['arguments']['subnet-id'] == 999
    # explict query for old lease should return error
    srv_msg.send_ctrl_cmd_via_socket('{"command":"lease6-get","arguments":{"subnet-id":666,"identifier-type":"duid", "identifier": "00:03:00:01:f6:f5:f4:f3:f2:01"}}',
                                     exp_result=3)

    # old lease should not be present in the lease file
    # bug: #1618, closed as designed
    lease_file_doesnt_contain('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    lease_file_doesnt_contain('666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')
    # new one should be in the lease file
    lease_file_contains('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:22')
    lease_file_contains('999,3000,0,7654321,128,0,0,,f6:f5:f4:f3:f2:22,0')


@pytest.mark.v6
@pytest.mark.subnet_id_sanity_check
def test_v6_sanity_check_subnet_id_none():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', 666, 0)
    srv_control.set_conf_parameter_global('sanity-checks', {"lease-checks": "none"})
    srv_control.add_unix_socket()

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8::1')

    lease_file_contains('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    lease_file_contains('666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', 999, 0)
    srv_control.set_conf_parameter_global('sanity-checks', {"lease-checks": "none"})
    srv_control.add_unix_socket()

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'reconfigured')
    srv_msg.forge_sleep(2, 'seconds')
    lease_file_contains('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    lease_file_contains('666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
def test_v6_sanity_check_subnet_id():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::1')
    srv_control.set_conf_parameter_subnet('id', 666, 0)
    srv_control.set_conf_parameter_global('sanity-checks', {"lease-checks": "fix"})
    srv_control.add_unix_socket()

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "config-get","arguments":  {} }')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "list-commands","arguments":  {} }')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8::1')

    lease_file_contains('2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    lease_file_contains('666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')

    srv_control.start_srv('DHCP', 'stopped')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::2')
    srv_control.set_conf_parameter_subnet('id', '888', 0)
    srv_control.set_conf_parameter_global('sanity-checks', {"lease-checks": "fix-del"})
    srv_control.add_unix_socket()

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    srv_msg.forge_sleep(12, 'seconds')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8::/64', '2001:db8::1-2001:db8::2')
    srv_control.set_conf_parameter_subnet('id', 999, 0)
    srv_control.set_conf_parameter_global('sanity-checks', {"lease-checks": "fix-del"})
    srv_control.add_unix_socket()

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'reconfigured')
    srv_msg.forge_sleep(12, 'seconds')

    # Using UNIX socket on server in path control_socket send {"command": "config-get","arguments":  {} }
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8::2')
    srv_msg.forge_sleep(10, 'seconds')

    # Using UNIX socket on server in path control_socket send {"command": "config-get","arguments":  {} }
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:33')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)
    # Response option 3 MUST contain sub-option 5.
    # Response sub-option 5 from option 3 MUST contain address 2001:db8::2.

    # Pause the Test.


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
def test_v6_sanity_check_shared_subnet_id():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.set_conf_parameter_subnet('id', 666, 0)
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.set_conf_parameter_subnet('id', '777', 1)
    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.shared_subnet('2001:db8:b::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)
    srv_control.set_conf_parameter_global('sanity-checks', {"lease-checks": "fix-del"})
    srv_control.add_unix_socket()
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "config-get","arguments":  {} }')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', '1234567')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_sets_value('Client', 'ia_id', '7654321')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    lease_file_contains('2001:db8:a::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    lease_file_contains('666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01')
    lease_file_contains('2001:db8:b::1,00:03:00:01:f6:f5:f4:f3:f2:02')
    lease_file_contains('777,3000,0,7654321,128,0,0,,f6:f5:f4:f3:f2:02')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.set_conf_parameter_subnet('id', '888', 0)
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.set_conf_parameter_subnet('id', 999, 1)
    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.shared_subnet('2001:db8:b::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)
    srv_control.set_conf_parameter_global('sanity-checks', {"lease-checks": "fix"})
    srv_control.add_unix_socket()
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'reconfigured')
