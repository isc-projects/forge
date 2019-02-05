"""Shared-Networks"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_control
from features import srv_msg
from features import misc


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_negative_missing_name(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')
    # first shared subnet
    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface-id', '"interface-abc"', '0')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    # DHCP server is started.
    srv_control.start_srv_during_process(step, 'DHCP', 'configure')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_negative_not_unique_names(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')
    srv_control.config_srv(step, 'preference', '0', '123')
    srv_control.config_srv(step, 'dns-servers', '1', '2001:db8::1,2001:db8::2')
    # first shared subnet
    srv_control.shared_subnet(step, '0', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface-id', '"interface-abc"', '0')
    # second shared-subnet
    srv_control.shared_subnet(step, '1', '1')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '1')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface-id', '"interface-xyz"', '1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv_during_process(step, 'DHCP', 'configure')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_single_shared_subnet_with_one_subnet_based_on_iface(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.shared_subnet(step, '0', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '0')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:a::1')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '13')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_single_shared_subnet_with_one_subnet_based_on_relay_address(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.shared_subnet(step, '0', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step,
                                                 'relay',
                                                 '{"ip-address":"2001:db8::abcd"}',
                                                 '0')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '13')
    # there is no local subnet!

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'server-id')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '13')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               '2001:db8:a::1,00:03:00:01:f6:f5:f4:f3:f2:01')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_single_shared_subnet_with_one_subnet_based_on_id(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.shared_subnet(step, '0', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface-id', '"interface-abc"', '0')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '13')
    # there is no local subnet!

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'server-id')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '13')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               '2001:db8:a::1,00:03:00:01:f6:f5:f4:f3:f2:01')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_single_shared_subnet_with_two_subnets_based_on_iface(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '0')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    # Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               '2001:db8:a::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               '2001:db8:b::1,00:03:00:01:f6:f5:f4:f3:f2:02')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_single_shared_subnet_with_tree_subnets_based_on_iface_options_override(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')
    srv_control.shared_subnet(step, '2', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '0')

    srv_control.config_srv_opt(step, 'preference', '1')
    srv_control.config_srv(step, 'preference', '0', '33')
    srv_control.config_srv(step, 'preference', '1', '44')
    srv_control.config_srv(step, 'preference', '2', '55')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option(step, 'Response', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '1')
    srv_msg.response_check_option_content(step, 'Response', '7', None, 'value', '33')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    # Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.
    srv_msg.response_check_include_option(step, 'Response', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '1')
    srv_msg.response_check_option_content(step, 'Response', '7', None, 'value', '33')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option(step, 'Response', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '1')
    srv_msg.response_check_option_content(step, 'Response', '7', None, 'value', '44')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option(step, 'Response', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '1')
    srv_msg.response_check_option_content(step, 'Response', '7', None, 'value', '44')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_single_shared_subnet_with_three_subnets_based_on_id_options_override(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.config_srv(step, 'dns-servers', '1', '2001:db8::1,2001:db8::2')

    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')
    srv_control.shared_subnet(step, '2', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface-id', '"interface-abc"', '0')

    srv_control.config_srv_opt(step, 'preference', '1')
    srv_control.config_srv(step, 'preference', '0', '33')
    srv_control.config_srv(step, 'preference', '1', '44')
    srv_control.config_srv(step, 'preference', '2', '55')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'server-id')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '13')
    # there is no local subnet!

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '7')
    srv_msg.response_check_option_content(step, 'Relayed Message', '7', None, 'value', '33')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '7')
    srv_msg.response_check_option_content(step, 'Relayed Message', '7', None, 'value', '33')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '7')
    srv_msg.response_check_option_content(step, 'Relayed Message', '7', None, 'value', '44')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '7')
    srv_msg.response_check_option_content(step, 'Relayed Message', '7', None, 'value', '44')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_single_shared_subnet_with_two_subnets_based_on_id(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv(step, 'preference', '0', '123')
    srv_control.config_srv(step, 'dns-servers', '1', '2001:db8::1,2001:db8::2')
    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface-id', '"interface-abc"', '0')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'server-id')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '13')
    # there is no local subnet!

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               '2001:db8:a::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               '2001:db8:b::1,00:03:00:01:f6:f5:f4:f3:f2:02')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_single_shared_subnet_with_three_subnets_based_on_relay_address_options_override(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.config_srv(step, 'dns-servers', '1', '2001:db8::1,2001:db8::2')

    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')
    srv_control.shared_subnet(step, '2', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step,
                                                 'relay',
                                                 '{"ip-address":"2001:db8::abcd"}',
                                                 '0')

    srv_control.config_srv_opt(step, 'preference', '1')
    srv_control.config_srv(step, 'preference', '0', '33')
    srv_control.config_srv(step, 'preference', '1', '44')
    srv_control.config_srv(step, 'preference', '2', '55')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'server-id')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '13')
    # there is no local subnet!

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '7')
    srv_msg.response_check_option_content(step, 'Relayed Message', '7', None, 'value', '33')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '7')
    srv_msg.response_check_option_content(step, 'Relayed Message', '7', None, 'value', '33')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '7')
    srv_msg.response_check_option_content(step, 'Relayed Message', '7', None, 'value', '44')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '7')
    srv_msg.response_check_option_content(step, 'Relayed Message', '7', None, 'value', '44')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_single_shared_subnet_with_two_subnets_based_on_relay_address(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv(step, 'preference', '0', '123')
    srv_control.config_srv(step, 'dns-servers', '1', '2001:db8::1,2001:db8::2')
    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step,
                                                 'relay',
                                                 '{"ip-address":"2001:db8::abcd"}',
                                                 '0')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'server-id')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '13')
    # there is no local subnet!

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               '2001:db8:a::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               '2001:db8:b::1,00:03:00:01:f6:f5:f4:f3:f2:02')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_three_shared_subnet_with_two_subnets_based_on_id_and_iface_and_relay_address(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:e::/64',
                                                       '2001:db8:e::1-2001:db8:e::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:f::/64',
                                                       '2001:db8:f::1-2001:db8:f::1')
    srv_control.config_srv(step, 'dns-servers', '1', '2001:db8::1,2001:db8::2')
    # first shared subnet
    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface-id', '"interface-abc"', '0')
    # second shared-subnet
    srv_control.shared_subnet(step, '2', '1')
    srv_control.shared_subnet(step, '3', '1')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-xyz"', '1')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '1')
    srv_control.shared_subnet(step, '4', '2')
    srv_control.shared_subnet(step, '5', '2')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-something"', '2')
    srv_control.set_conf_parameter_shared_subnet(step,
                                                 'relay',
                                                 '{"ip-address":"2001:db8::1234"}',
                                                 '2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'server-id')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abcde')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8::1234')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abcde')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8::1234')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abcde')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8::1234')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abcde')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8::1234')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               '2001:db8:e::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               '2001:db8:f::1,00:03:00:01:f6:f5:f4:f3:f2:02')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               '2001:db8:a::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               '2001:db8:b::1,00:03:00:01:f6:f5:f4:f3:f2:02')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    # Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               '2001:db8:c::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               '2001:db8:d::1,00:03:00:01:f6:f5:f4:f3:f2:02')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_three_shared_subnet_with_two_subnets_options_override(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:e::/64',
                                                       '2001:db8:e::1-2001:db8:e::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:f::/64',
                                                       '2001:db8:f::1-2001:db8:f::1')
    srv_control.config_srv(step, 'dns-servers', '1', '2001:db8::1,2001:db8::2')

    srv_control.config_srv_opt(step, 'preference', '1')
    srv_control.config_srv(step, 'preference', '2', '33')
    srv_control.config_srv(step, 'preference', '3', '44')
    srv_control.config_srv(step, 'preference', '4', '55')
    srv_control.config_srv(step, 'preference', '5', '66')

    # first shared subnet
    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface-id', '"interface-abc"', '0')
    # second shared-subnet
    srv_control.shared_subnet(step, '2', '1')
    srv_control.shared_subnet(step, '3', '1')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-xyz"', '1')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '1')
    srv_control.shared_subnet(step, '4', '2')
    srv_control.shared_subnet(step, '5', '2')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-something"', '2')
    srv_control.set_conf_parameter_shared_subnet(step,
                                                 'relay',
                                                 '{"ip-address":"2001:db8::1234"}',
                                                 '2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'server-id')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '11')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '1')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '55')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '66')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abcde')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8::1234')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '11')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '1')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '33')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '44')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abcde')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8::1234')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '11')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '1')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '33')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '44')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abcde')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8::1234')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '11')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '1')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '33')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '44')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abcde')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8::1234')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '11')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '1')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '33')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '44')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '11')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '55')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '66')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '33')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '44')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '11')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '55')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '66')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '33')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '44')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '11')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '55')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '66')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '33')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '44')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    srv_msg.response_check_include_option(step, 'Relayed Message', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '11')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '55')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '66')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '33')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '44')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option(step, 'Response', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '1')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '55')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '66')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option(step, 'Response', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '1')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '55')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '66')
    # Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option(step, 'Response', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '1')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '55')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '66')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_include_option(step, 'Response', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '1')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '55')
    srv_msg.response_check_option_content(step, 'Response', '7', 'NOT ', 'value', '66')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_two_shared_subnet_with_two_subnets_based_on_relay_address(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')
    srv_control.config_srv(step, 'preference', '0', '123')
    srv_control.config_srv(step, 'dns-servers', '1', '2001:db8::1,2001:db8::2')
    # first shared subnet
    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step,
                                                 'relay',
                                                 '{"ip-address":"2001:db8::abcd"}',
                                                 '0')
    # second shared-subnet
    srv_control.shared_subnet(step, '2', '1')
    srv_control.shared_subnet(step, '3', '1')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-xyz"', '1')
    srv_control.set_conf_parameter_shared_subnet(step,
                                                 'relay',
                                                 '{"ip-address":"2001:db8::1234"}',
                                                 '1')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'server-id')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '13')
    # there is no local subnet!

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8::abcd')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               '2001:db8:a::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               '2001:db8:b::1,00:03:00:01:f6:f5:f4:f3:f2:02')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-xyz')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8::1234')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-xyz')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8::1234')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-xyz')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8::1234')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-xyz')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8::1234')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               '2001:db8:c::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               '2001:db8:d::1,00:03:00:01:f6:f5:f4:f3:f2:02')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:03')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-xyz')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8::1234')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '13')
    # no available addresses

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:03')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '13')
    # no available addresses


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_two_shared_subnet_with_two_subnets_based_on_id(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::1')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')
    srv_control.config_srv(step, 'preference', '0', '123')
    srv_control.config_srv(step, 'dns-servers', '1', '2001:db8::1,2001:db8::2')
    # first shared subnet
    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface-id', '"interface-abc"', '0')
    # second shared-subnet
    srv_control.shared_subnet(step, '2', '1')
    srv_control.shared_subnet(step, '3', '1')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-xyz"', '1')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface-id', '"interface-xyz"', '1')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'server-id')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '13')
    # there is no local subnet!

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               '2001:db8:a::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               '2001:db8:b::1,00:03:00:01:f6:f5:f4:f3:f2:02')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-xyz')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-xyz')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-xyz')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-xyz')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '5')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               '2001:db8:c::1,00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               '2001:db8:d::1,00:03:00:01:f6:f5:f4:f3:f2:02')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:03')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-xyz')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '13')
    # no available addresses

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:03')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'interface-abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '3')
    srv_msg.response_check_option_content(step, 'Relayed Message', '3', None, 'sub-option', '13')
    # no available addresses


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_single_shared_subnet_with_three_subnets_classification(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::10')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::10')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::10')

    srv_control.create_new_class(step, 'Client_f2f1')
    srv_control.add_test_to_class(step, '1', 'test', 'substring(option[1].hex,8,2) == 0xf2f1')
    srv_control.add_option_to_defined_class(step, '1', 'dns-servers', '2001:db8::666')
    srv_control.config_client_classification(step, '1', 'Client_f2f1')

    srv_control.create_new_class(step, 'Client_f2f2')
    srv_control.add_test_to_class(step, '2', 'test', 'substring(option[1].hex,8,2) == 0xf2f2')
    srv_control.config_client_classification(step, '2', 'Client_f2f2')

    srv_control.create_new_class(step, 'Client_f2f0')
    srv_control.add_test_to_class(step, '3', 'test', 'substring(option[1].hex,8,2) == 0xf299')
    srv_control.config_client_classification(step, '0', 'Client_f2f0')

    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')
    srv_control.shared_subnet(step, '2', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '0')
    srv_control.set_conf_parameter_shared_subnet(step,
                                                 'option-data',
                                                 '[{"code":23,"data":"2001:db8::1","name":"dns-servers","space":"dhcp6"}]',
                                                 '0')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:f1')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '23')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:b::1')
    srv_msg.response_check_include_option(step, 'Response', None, '23')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::666')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:f1')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_requests_option(step, '23')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:b::1')
    srv_msg.response_check_include_option(step, 'Response', None, '23')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::666')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:f2')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '23')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:c::1')
    srv_msg.response_check_include_option(step, 'Response', None, '23')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::1')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:f2')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_requests_option(step, '23')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:c::1')
    srv_msg.response_check_include_option(step, 'Response', None, '23')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::1')

    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               '2001:db8:b::1,00:03:00:01:f6:f5:f4:f3:f2:f1')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               '2001:db8:c::1,00:03:00:01:f6:f5:f4:f3:f2:f2')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
@pytest.mark.kea_only
def test_v6_sharednetworks_host_reservation_duplicate_reservation(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/30', '3000::1-3000::10')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '3000::1',
                                           '0',
                                           'duid',
                                           '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '3000::2',
                                           '0',
                                           'duid',
                                           '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
def test_v6_sharednetworks_host_reservation_all_values_duid(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:d::/64',
                                                       '2001:db8:d::1-2001:db8:d::1')
    srv_control.host_reservation_in_subnet(step,
                                           'hostname',
                                           'reserved-hostname',
                                           '0',
                                           'duid',
                                           '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'address', '3000::100')
    srv_control.host_reservation_in_subnet_add_value(step, '0', '0', 'prefix', '3001::/40')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'my.domain.com')
    srv_control.shared_subnet(step, '0', '0')
    srv_control.shared_subnet(step, '1', '0')
    srv_control.shared_subnet(step, '2', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '0')
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
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
def test_v6_sharednetworks_host_reservation_options_override_1(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')

    srv_control.enable_db_backend_reservation(step, 'MySQL')
    srv_control.new_db_backend_reservation(step, 'MySQL', 'duid', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.ipv6_address_db_backend_reservation(step,
                                                    '2001:db8:a::100',
                                                    '$(EMPTY)',
                                                    'MySQL',
                                                    '1')
    srv_control.update_db_backend_reservation(step, 'dhcp6_subnet_id', '1', 'MySQL', '1')
    srv_control.option_db_record_reservation(step,
                                             '7',
                                             '10',
                                             'dhcp6',
                                             '1',
                                             '$(EMPTY)',
                                             '1',
                                             'subnet',
                                             'MySQL',
                                             '1')
    srv_control.upload_db_reservation(step, 'MySQL')

    srv_control.shared_subnet(step, '0', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '0')
    srv_control.set_conf_parameter_shared_subnet(step,
                                                 'option-data',
                                                 '[{"code":7,"data":"5","name":"preference","space":"dhcp6"}]',
                                                 '0')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:11:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:a::1')
    srv_msg.response_check_include_option(step, 'Response', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', None, 'value', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', None, 'value', '10')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:a::100')


@pytest.mark.v6
@pytest.mark.sharednetworks
@pytest.mark.sharedsubnets
def test_v6_sharednetworks_host_reservation_options_override_2(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')

    srv_control.enable_db_backend_reservation(step, 'PostgreSQL')
    srv_control.new_db_backend_reservation(step,
                                           'PostgreSQL',
                                           'duid',
                                           '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.ipv6_address_db_backend_reservation(step,
                                                    '2001:db8:a::100',
                                                    '$(EMPTY)',
                                                    'PostgreSQL',
                                                    '1')
    srv_control.update_db_backend_reservation(step, 'dhcp6_subnet_id', '1', 'PostgreSQL', '1')
    srv_control.option_db_record_reservation(step,
                                             '7',
                                             '10',
                                             'dhcp6',
                                             '1',
                                             '$(EMPTY)',
                                             '1',
                                             'subnet',
                                             'PostgreSQL',
                                             '1')
    srv_control.upload_db_reservation(step, 'PostgreSQL')

    srv_control.shared_subnet(step, '0', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'name', '"name-abc"', '0')
    srv_control.set_conf_parameter_shared_subnet(step, 'interface', '"$(SERVER_IFACE)"', '0')
    srv_control.set_conf_parameter_shared_subnet(step,
                                                 'option-data',
                                                 '[{"code":7,"data":"5","name":"preference","space":"dhcp6"}]',
                                                 '0')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:11:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:a::1')
    srv_msg.response_check_include_option(step, 'Response', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', None, 'value', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', None, 'value', '10')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:a::100')
