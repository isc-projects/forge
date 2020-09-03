"""Shared-Networks"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_control
import srv_msg
import misc


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_negative_missing_name():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')
    # first shared subnet
    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.shared_subnet('2001:db8:b::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('interface-id', '"interface-abc"', 0)
    srv_control.build_and_send_config_files('SSH', 'config-file')

    # DHCP server is started.
    srv_control.start_srv_during_process('DHCP', 'configure')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_negative_not_unique_names():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')
    srv_control.config_srv('preference', 0, '123')
    srv_control.config_srv('dns-servers', 1, '2001:db8::1,2001:db8::2')
    # first shared subnet
    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface-id', '"interface-abc"', 0)
    # second shared-subnet
    srv_control.shared_subnet('2001:db8:b::/64', 1)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 1)
    srv_control.set_conf_parameter_shared_subnet('interface-id', '"interface-xyz"', 1)
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv_during_process('DHCP', 'configure')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_single_shared_subnet_with_one_subnet_based_on_iface():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
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
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:a::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_single_shared_subnet_with_one_subnet_based_on_relay_address():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('relay', '{"ip-address":"2001:db8::abcd"}', 0)
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    # there is no local subnet!

    misc.test_procedure()
    srv_msg.client_save_option('server-id')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)

    srv_msg.lease_file_contains('2001:db8:a::1,00:03:00:01:f6:f5:f4:f3:f2:01')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_single_shared_subnet_with_one_subnet_based_on_id():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface-id', '"interface-abc"', 0)
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    # there is no local subnet!

    misc.test_procedure()
    srv_msg.client_save_option('server-id')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)

    srv_msg.lease_file_contains('2001:db8:a::1,00:03:00:01:f6:f5:f4:f3:f2:01')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_single_shared_subnet_with_two_subnets_based_on_iface():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.shared_subnet('2001:db8:b::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
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

    srv_msg.lease_file_contains('2001:db8:a::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.lease_file_contains('2001:db8:b::1,00:03:00:01:f6:f5:f4:f3:f2:02')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_single_shared_subnet_with_tree_subnets_based_on_iface_options_override():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.config_srv_opt('preference', '1')
    srv_control.config_srv('preference', 0, '33')
    srv_control.config_srv('preference', 1, '44')
    srv_control.config_srv('preference', 2, '55')

    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.shared_subnet('2001:db8:b::/64', 0)
    srv_control.shared_subnet('2001:db8:c::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(7)
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 1, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 33)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 1, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 33)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 1, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 44)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 1, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 44)


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_single_shared_subnet_with_three_subnets_based_on_id_options_override():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.config_srv('dns-servers', 1, '2001:db8::1,2001:db8::2')
    srv_control.config_srv_opt('preference', '1')
    srv_control.config_srv('preference', 0, '33')
    srv_control.config_srv('preference', 1, '44')
    srv_control.config_srv('preference', 2, '55')

    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.shared_subnet('2001:db8:b::/64', 0)
    srv_control.shared_subnet('2001:db8:c::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface-id', '"interface-abc"', 0)

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(7)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_save_option('server-id')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    # there is no local subnet!

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 33)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 33)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 44)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 44)


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_single_shared_subnet_with_two_subnets_based_on_id():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv('preference', 0, '123')
    srv_control.config_srv('dns-servers', 1, '2001:db8::1,2001:db8::2')
    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.shared_subnet('2001:db8:b::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface-id', '"interface-abc"', 0)
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_save_option('server-id')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    # there is no local subnet!

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    srv_msg.lease_file_contains('2001:db8:a::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.lease_file_contains('2001:db8:b::1,00:03:00:01:f6:f5:f4:f3:f2:02')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_single_shared_subnet_with_three_subnets_based_on_relay_address_options_override():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.config_srv('dns-servers', 1, '2001:db8::1,2001:db8::2')
    srv_control.config_srv_opt('preference', '1')
    srv_control.config_srv('preference', 0, '33')
    srv_control.config_srv('preference', 1, '44')
    srv_control.config_srv('preference', 2, '55')

    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.shared_subnet('2001:db8:b::/64', 0)
    srv_control.shared_subnet('2001:db8:c::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('relay', '{"ip-address":"2001:db8::abcd"}', 0)

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(7)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_save_option('server-id')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    # there is no local subnet!

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 33)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 33)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 44)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 44)


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_single_shared_subnet_with_two_subnets_based_on_relay_address():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv('preference', 0, '123')
    srv_control.config_srv('dns-servers', 1, '2001:db8::1,2001:db8::2')
    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.shared_subnet('2001:db8:b::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('relay', '{"ip-address":"2001:db8::abcd"}', 0)
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_save_option('server-id')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    # there is no local subnet!

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    srv_msg.lease_file_contains('2001:db8:a::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.lease_file_contains('2001:db8:b::1,00:03:00:01:f6:f5:f4:f3:f2:02')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_three_shared_subnet_with_two_subnets_based_on_id_and_iface_and_relay_address():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:e::/64',
                                                       '2001:db8:e::1-2001:db8:e::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:f::/64',
                                                       '2001:db8:f::1-2001:db8:f::1')
    srv_control.config_srv('dns-servers', 1, '2001:db8::1,2001:db8::2')
    # first shared subnet
    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.shared_subnet('2001:db8:b::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface-id', '"interface-abc"', 0)
    # second shared-subnet
    srv_control.shared_subnet('2001:db8:c::/64', 1)
    srv_control.shared_subnet('2001:db8:d::/64', 1)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-xyz"', 1)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 1)
    srv_control.shared_subnet('2001:db8:e::/64', 2)
    srv_control.shared_subnet('2001:db8:f::/64', 2)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-something"', 2)
    srv_control.set_conf_parameter_shared_subnet('relay', '{"ip-address":"2001:db8::1234"}', 2)
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_save_option('server-id')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abcde')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::1234')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abcde')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::1234')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abcde')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::1234')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abcde')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::1234')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    srv_msg.lease_file_contains('2001:db8:e::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.lease_file_contains('2001:db8:f::1,00:03:00:01:f6:f5:f4:f3:f2:02')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    srv_msg.lease_file_contains('2001:db8:a::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.lease_file_contains('2001:db8:b::1,00:03:00:01:f6:f5:f4:f3:f2:02')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
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

    srv_msg.lease_file_contains('2001:db8:c::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.lease_file_contains('2001:db8:d::1,00:03:00:01:f6:f5:f4:f3:f2:02')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_three_shared_subnet_with_two_subnets_options_override():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:e::/64',
                                                       '2001:db8:e::1-2001:db8:e::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:f::/64',
                                                       '2001:db8:f::1-2001:db8:f::1')
    srv_control.config_srv('dns-servers', 1, '2001:db8::1,2001:db8::2')

    srv_control.config_srv_opt('preference', '1')
    srv_control.config_srv('preference', 2, '33')
    srv_control.config_srv('preference', 3, '44')
    srv_control.config_srv('preference', 4, '55')
    srv_control.config_srv('preference', 5, '66')

    # first shared subnet
    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.shared_subnet('2001:db8:b::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface-id', '"interface-abc"', 0)
    # second shared-subnet
    srv_control.shared_subnet('2001:db8:c::/64', 1)
    srv_control.shared_subnet('2001:db8:d::/64', 1)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-xyz"', 1)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 1)
    srv_control.shared_subnet('2001:db8:e::/64', 2)
    srv_control.shared_subnet('2001:db8:f::/64', 2)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-something"', 2)
    srv_control.set_conf_parameter_shared_subnet('relay', '{"ip-address":"2001:db8::1234"}', 2)
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_save_option('server-id')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 11, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 1, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 55, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 66, expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abcde')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::1234')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 11, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 1, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 33, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 44, expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abcde')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::1234')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 11, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 1, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 33, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 44, expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abcde')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::1234')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 11, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 1, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 33, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 44, expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abcde')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::1234')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 11, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 1, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 33, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 44, expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 11, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 55, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 66, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 33, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 44, expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 11, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 55, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 66, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 33, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 44, expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 11, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 55, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 66, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 33, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 44, expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 11, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 55, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 66, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 33, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 44, expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 1, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 55, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 66, expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 1, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 55, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 66, expect_include=False)
    # Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 1, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 55, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 66, expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 1, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 55, expect_include=False)
    srv_msg.response_check_option_content(7, 'value', 66, expect_include=False)


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_two_shared_subnet_with_two_subnets_based_on_relay_address():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')
    srv_control.config_srv('preference', 0, '123')
    srv_control.config_srv('dns-servers', 1, '2001:db8::1,2001:db8::2')
    # first shared subnet
    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.shared_subnet('2001:db8:b::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('relay', '{"ip-address":"2001:db8::abcd"}', 0)
    # second shared-subnet
    srv_control.shared_subnet('2001:db8:c::/64', 1)
    srv_control.shared_subnet('2001:db8:d::/64', 1)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-xyz"', 1)
    srv_control.set_conf_parameter_shared_subnet('relay', '{"ip-address":"2001:db8::1234"}', 1)

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_save_option('server-id')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    # there is no local subnet!

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    srv_msg.lease_file_contains('2001:db8:a::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.lease_file_contains('2001:db8:b::1,00:03:00:01:f6:f5:f4:f3:f2:02')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-xyz')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::1234')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-xyz')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::1234')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-xyz')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::1234')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-xyz')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::1234')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    srv_msg.lease_file_contains('2001:db8:c::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.lease_file_contains('2001:db8:d::1,00:03:00:01:f6:f5:f4:f3:f2:02')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:03')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-xyz')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8::1234')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    # no available addresses

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:03')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    # no available addresses


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_two_shared_subnet_with_two_subnets_based_on_id():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')
    srv_control.config_srv('preference', 0, '123')
    srv_control.config_srv('dns-servers', 1, '2001:db8::1,2001:db8::2')
    # first shared subnet
    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.shared_subnet('2001:db8:b::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface-id', '"interface-abc"', 0)
    # second shared-subnet
    srv_control.shared_subnet('2001:db8:c::/64', 1)
    srv_control.shared_subnet('2001:db8:d::/64', 1)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-xyz"', 1)
    srv_control.set_conf_parameter_shared_subnet('interface-id', '"interface-xyz"', 1)

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_save_option('server-id')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    # there is no local subnet!

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    srv_msg.lease_file_contains('2001:db8:a::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.lease_file_contains('2001:db8:b::1,00:03:00:01:f6:f5:f4:f3:f2:02')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-xyz')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-xyz')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-xyz')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-xyz')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    srv_msg.lease_file_contains('2001:db8:c::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.lease_file_contains('2001:db8:d::1,00:03:00:01:f6:f5:f4:f3:f2:02')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:03')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-xyz')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    # no available addresses

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:03')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    # no available addresses


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_single_shared_subnet_with_three_subnets_classification():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::10')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::10')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::10')

    srv_control.create_new_class('Client_f2f1')
    srv_control.add_test_to_class(1, 'test', 'substring(option[1].hex,8,2) == 0xf2f1')
    srv_control.add_option_to_defined_class(1, 'dns-servers', '2001:db8::666')
    srv_control.config_client_classification(1, 'Client_f2f1')

    srv_control.create_new_class('Client_f2f2')
    srv_control.add_test_to_class(2, 'test', 'substring(option[1].hex,8,2) == 0xf2f2')
    srv_control.config_client_classification(2, 'Client_f2f2')

    srv_control.create_new_class('Client_f2f0')
    srv_control.add_test_to_class(3, 'test', 'substring(option[1].hex,8,2) == 0xf299')
    srv_control.config_client_classification(0, 'Client_f2f0')

    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.shared_subnet('2001:db8:b::/64', 0)
    srv_control.shared_subnet('2001:db8:c::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)
    srv_control.set_conf_parameter_shared_subnet('option-data',
                                                 '{"code":23,"data":"2001:db8::1","name":"dns-servers","space":"dhcp6"}',
                                                 0)

    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:f1')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:b::1')

    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::666')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:f1')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:b::1')

    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::666')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:f2')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:c::1')

    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:f2')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:c::1')

    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::1')

    srv_msg.lease_file_contains('2001:db8:b::1,00:03:00:01:f6:f5:f4:f3:f2:f1')
    srv_msg.lease_file_contains('2001:db8:c::1,00:03:00:01:f6:f5:f4:f3:f2:f2')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_host_reservation_duplicate_reservation():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/30', '3000::1-3000::10')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')
    srv_control.host_reservation_in_subnet('ip-address',
                                           '3000::1',
                                           0,
                                           'duid',
                                           '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.host_reservation_in_subnet('ip-address',
                                           '3000::2',
                                           0,
                                           'duid',
                                           '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.shared_subnet('2001:db8:b::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv_during_process('DHCP', 'configuration')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
def test_v6_sharednetworks_host_reservation_all_values_duid():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           0,
                                           'duid',
                                           '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '2001:db8:a::100')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'prefixes', '3001::/40')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_ddns_server_options('qualifying-suffix', 'my.domain.com')
    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.shared_subnet('2001:db8:b::/64', 0)
    srv_control.shared_subnet('2001:db8:c::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'some-different-name')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:a::100')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '3001::')
    srv_msg.response_check_include_option(39)
    srv_msg.response_check_option_content(39, 'fqdn', 'reserved-hostname.my.domain.com.')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
def test_v6_sharednetworks_host_reservation_options_override_1():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')

    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.new_db_backend_reservation('MySQL', 'duid', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.ipv6_address_db_backend_reservation('2001:db8:a::100', '$(EMPTY)', 'MySQL', 1)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'MySQL', 1)
    srv_control.option_db_record_reservation(7,
                                             10,
                                             'dhcp6',
                                             1,
                                             '$(EMPTY)',
                                             1,
                                             'subnet',
                                             'MySQL',
                                             1)
    srv_control.upload_db_reservation('MySQL')

    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)
    srv_control.set_conf_parameter_shared_subnet('option-data',
                                                 '{"code":7,"data":"5","name":"preference","space":"dhcp6"}',
                                                 0)

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:11:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:a::1')

    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 10)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:a::100')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
def test_v6_sharednetworks_host_reservation_options_override_2():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')

    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.new_db_backend_reservation('PostgreSQL', 'duid', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.ipv6_address_db_backend_reservation('2001:db8:a::100',
                                                    '$(EMPTY)',
                                                    'PostgreSQL',
                                                    1)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'PostgreSQL', 1)
    srv_control.option_db_record_reservation(7,
                                             10,
                                             'dhcp6',
                                             1,
                                             '$(EMPTY)',
                                             1,
                                             'subnet',
                                             'PostgreSQL',
                                             1)
    srv_control.upload_db_reservation('PostgreSQL')

    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)
    srv_control.set_conf_parameter_shared_subnet('option-data',
                                                 '{"code":7,"data":"5","name":"preference","space":"dhcp6"}',
                                                 0)

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:11:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:a::1')

    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 10)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:a::100')
