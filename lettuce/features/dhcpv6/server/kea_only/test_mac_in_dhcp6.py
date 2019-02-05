"""MAC in DHCPv6"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import misc
from features import srv_msg
from features import srv_control


@pytest.mark.v6
@pytest.mark.MACinDHCP6
@pytest.mark.kea_only
def test_v6_mac_in_dhcp6_duid_type3(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.run_command(step, '"mac-sources": [ "duid" ]')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               ',f6:f5:f4:f3:f2:01,0')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               'Hardware addr: f6:f5:f4:f3:f2:01')


@pytest.mark.v6
@pytest.mark.MACinDHCP6
@pytest.mark.kea_only
def test_v6_mac_in_dhcp6_duid_type1(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.run_command(step, '"mac-sources": [ "duid" ]')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:01:00:01:55:2b:fa:0c:08:00:27:58:f1:e8')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:01:00:01:52:7b:a8:f0:08:00:27:58:f1:e8')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               ',08:00:27:58:f1:e8')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               'Hardware addr: 08:00:27:58:f1:e8')


@pytest.mark.v6
@pytest.mark.MACinDHCP6
@pytest.mark.kea_only
def test_v6_mac_in_dhcp6_any(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.run_command(step, '"mac-sources": [ "any" ]')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               ',f6:f5:f4:f3:f2:01')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               'Hardware addr: f6:f5:f4:f3:f2:01')


@pytest.mark.v6
@pytest.mark.MACinDHCP6
@pytest.mark.kea_only
def test_v6_mac_in_dhcp6_ipv6_link_local(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.run_command(step, '"mac-sources": [ "ipv6-link-local" ]')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               ',$(CLI_MAC)')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               'Hardware addr: $(CLI_MAC)')


@pytest.mark.v6
@pytest.mark.MACinDHCP6
@pytest.mark.kea_only
def test_v6_mac_in_dhcp6_client_link_addr_1(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.run_command(step, '"mac-sources": [ "client-link-addr-option" ]')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-link-layer-addr')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_does_include(step, 'RelayAgent', None, 'client-link-layer-addr')
    srv_msg.client_sets_value(step, 'RelayAgent', 'peeraddr', '$(CLI_LINK_LOCAL)')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               ',$(CLI_MAC)')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               'Hardware addr: $(CLI_MAC)')


@pytest.mark.v6
@pytest.mark.MACinDHCP6
@pytest.mark.kea_only
def test_v6_mac_in_dhcp6_client_link_addr_2(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.run_command(step, '"mac-sources": [ "rfc6939" ]')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_does_include(step, 'RelayAgent', None, 'client-link-layer-addr')
    srv_msg.client_sets_value(step, 'RelayAgent', 'peeraddr', '$(CLI_LINK_LOCAL)')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               ',$(CLI_MAC)')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               'Hardware addr: $(CLI_MAC)')


@pytest.mark.v6
@pytest.mark.MACinDHCP6
@pytest.mark.kea_only
def test_v6_mac_in_dhcp6_remote_id_1(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.run_command(step, '"mac-sources": [ "rfc4649" ]')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'Client', 'remote_id', '0a0027000001')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'remote-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'peeraddr', 'fe80::800:27ff:fe00:2')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               ',0a:00:27:00:00:01')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               'Hardware addr: 0a:00:27:00:00:01')


@pytest.mark.v6
@pytest.mark.MACinDHCP6
@pytest.mark.kea_only
def test_v6_mac_in_dhcp6_remote_id_2(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.run_command(step, '"mac-sources": [ "remote-id" ]')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'remote_id', '0a0027000001')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'remote-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'peeraddr', 'fe80::800:27ff:fe00:2')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               ',0a:00:27:00:00:01')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               'Hardware addr: 0a:00:27:00:00:01')


@pytest.mark.v6
@pytest.mark.MACinDHCP6
@pytest.mark.kea_only
@pytest.mark.disabled
def test_v6_mac_in_dhcp6_subscriber_id_1(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.run_command(step, '"mac-sources": [ "subscriber-id" ]')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'subscriber_id', 'f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'subscriber-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'peeraddr', 'fe80::800:27ff:fe00:2')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               ',0a:00:27:00:00:02')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               'Hardware addr: 0a:00:27:00:00:02')


@pytest.mark.v6
@pytest.mark.MACinDHCP6
@pytest.mark.kea_only
@pytest.mark.disabled
def test_v6_mac_in_dhcp6_subscriber_id_2(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.run_command(step, '"mac-sources": [ "rfc4580" ]')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'subscriber_id', '0a0027000002')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'subscriber-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'peeraddr', 'fe80::800:27ff:fe00:2')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               ',0a:00:27:00:00:02')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               'Hardware addr: 0a:00:27:00:00:02')


@pytest.mark.v6
@pytest.mark.MACinDHCP6
@pytest.mark.kea_only
def test_v6_mac_in_dhcp6_docsis_modem(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.run_command(step, '"mac-sources": [ "docsis-modem" ]')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_sets_value(step, 'Client', 'enterprisenum', '4491')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption(step, 'Client', '36', 'f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-specific-info')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               ',f6:f5:f4:f3:f2:01')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               'Hardware addr: f6:f5:f4:f3:f2:01')


@pytest.mark.v6
@pytest.mark.MACinDHCP6
@pytest.mark.kea_only
def test_v6_mac_in_dhcp6_docsic_cmts(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.run_command(step, '"mac-sources": [ "docsis-cmts" ]')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'enterprisenum', '4491')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'vendor-class')
    srv_msg.add_vendor_suboption(step, 'RelayAgent', '1026', '00:f5:f4:00:f2:01')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'vendor-specific-info')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv',
                               None,
                               ',00:f5:f4:00:f2:01')
    srv_msg.file_contains_line(step,
                               '$(SOFTWARE_INSTALL_DIR)/var/kea/kea.log',
                               None,
                               'Hardware addr: 00:f5:f4:00:f2:01')
