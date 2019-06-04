"""MAC in DHCPv6"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_control
import srv_msg
import misc


@pytest.mark.v6
@pytest.mark.MACinDHCP6
@pytest.mark.kea_only
def test_v6_mac_in_dhcp6_duid_type3():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.run_command('"mac-sources": [ "duid" ]')
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
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.lease_file_contains(',f6:f5:f4:f3:f2:01,0')
    srv_msg.log_contains('Hardware addr: f6:f5:f4:f3:f2:01')


@pytest.mark.v6
@pytest.mark.MACinDHCP6
@pytest.mark.kea_only
def test_v6_mac_in_dhcp6_duid_type1():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.run_command('"mac-sources": [ "duid" ]')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:01:00:01:55:2b:fa:0c:08:00:27:58:f1:e8')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:01:00:01:52:7b:a8:f0:08:00:27:58:f1:e8')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.lease_file_contains(',08:00:27:58:f1:e8')
    srv_msg.log_contains('Hardware addr: 08:00:27:58:f1:e8')


@pytest.mark.v6
@pytest.mark.MACinDHCP6
@pytest.mark.kea_only
def test_v6_mac_in_dhcp6_any():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.run_command('"mac-sources": [ "any" ]')
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
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.lease_file_contains(',f6:f5:f4:f3:f2:01')
    srv_msg.log_contains('Hardware addr: f6:f5:f4:f3:f2:01')


@pytest.mark.v6
@pytest.mark.MACinDHCP6
@pytest.mark.kea_only
def test_v6_mac_in_dhcp6_ipv6_link_local():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.run_command('"mac-sources": [ "ipv6-link-local" ]')
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
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.lease_file_contains(',$(CLI_MAC)')
    srv_msg.log_contains('Hardware addr: $(CLI_MAC)')


@pytest.mark.v6
@pytest.mark.MACinDHCP6
@pytest.mark.kea_only
def test_v6_mac_in_dhcp6_client_link_addr_1():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.run_command('"mac-sources": [ "client-link-addr-option" ]')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'client-link-layer-addr')
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

    srv_msg.client_does_include('RelayAgent', None, 'client-link-layer-addr')
    srv_msg.client_sets_value('RelayAgent', 'peeraddr', '$(CLI_LINK_LOCAL)')
    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')
    srv_msg.lease_file_contains(',$(CLI_MAC)')
    srv_msg.log_contains('Hardware addr: $(CLI_MAC)')


@pytest.mark.v6
@pytest.mark.MACinDHCP6
@pytest.mark.kea_only
def test_v6_mac_in_dhcp6_client_link_addr_2():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.run_command('"mac-sources": [ "rfc6939" ]')
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

    srv_msg.client_does_include('RelayAgent', None, 'client-link-layer-addr')
    srv_msg.client_sets_value('RelayAgent', 'peeraddr', '$(CLI_LINK_LOCAL)')
    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')
    srv_msg.lease_file_contains(',$(CLI_MAC)')
    srv_msg.log_contains('Hardware addr: $(CLI_MAC)')


@pytest.mark.v6
@pytest.mark.MACinDHCP6
@pytest.mark.kea_only
def test_v6_mac_in_dhcp6_remote_id_1():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.run_command('"mac-sources": [ "rfc4649" ]')
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

    srv_msg.client_sets_value('Client', 'remote_id', '0a0027000001')
    srv_msg.client_does_include('RelayAgent', None, 'remote-id')
    srv_msg.client_sets_value('RelayAgent', 'peeraddr', 'fe80::800:27ff:fe00:2')
    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')
    srv_msg.lease_file_contains(',0a:00:27:00:00:01')
    srv_msg.log_contains('Hardware addr: 0a:00:27:00:00:01')


@pytest.mark.v6
@pytest.mark.MACinDHCP6
@pytest.mark.kea_only
def test_v6_mac_in_dhcp6_remote_id_2():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.run_command('"mac-sources": [ "remote-id" ]')
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

    srv_msg.client_sets_value('RelayAgent', 'remote_id', '0a0027000001')
    srv_msg.client_does_include('RelayAgent', None, 'remote-id')
    srv_msg.client_sets_value('RelayAgent', 'peeraddr', 'fe80::800:27ff:fe00:2')
    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')
    srv_msg.lease_file_contains(',0a:00:27:00:00:01')
    srv_msg.log_contains('Hardware addr: 0a:00:27:00:00:01')


@pytest.mark.v6
@pytest.mark.MACinDHCP6
@pytest.mark.kea_only
@pytest.mark.disabled
def test_v6_mac_in_dhcp6_subscriber_id_1():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.run_command('"mac-sources": [ "subscriber-id" ]')
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

    srv_msg.client_sets_value('RelayAgent', 'subscriber_id', 'f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('RelayAgent', None, 'subscriber-id')
    srv_msg.client_sets_value('RelayAgent', 'peeraddr', 'fe80::800:27ff:fe00:2')
    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')
    srv_msg.lease_file_contains(',0a:00:27:00:00:02')
    srv_msg.log_contains('Hardware addr: 0a:00:27:00:00:02')


@pytest.mark.v6
@pytest.mark.MACinDHCP6
@pytest.mark.kea_only
@pytest.mark.disabled
def test_v6_mac_in_dhcp6_subscriber_id_2():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.run_command('"mac-sources": [ "rfc4580" ]')
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

    srv_msg.client_sets_value('RelayAgent', 'subscriber_id', '0a0027000002')
    srv_msg.client_does_include('RelayAgent', None, 'subscriber-id')
    srv_msg.client_sets_value('RelayAgent', 'peeraddr', 'fe80::800:27ff:fe00:2')
    srv_msg.client_does_include('RelayAgent', None, 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_include_option('Response', None, '9')
    srv_msg.lease_file_contains(',0a:00:27:00:00:02')
    srv_msg.log_contains('Hardware addr: 0a:00:27:00:00:02')


@pytest.mark.v6
@pytest.mark.MACinDHCP6
@pytest.mark.kea_only
def test_v6_mac_in_dhcp6_docsis_modem():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.run_command('"mac-sources": [ "docsis-modem" ]')
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
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption('Client', '36', 'f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', None, 'vendor-specific-info')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.lease_file_contains(',f6:f5:f4:f3:f2:01')
    srv_msg.log_contains('Hardware addr: f6:f5:f4:f3:f2:01')


@pytest.mark.v6
@pytest.mark.MACinDHCP6
@pytest.mark.kea_only
def test_v6_mac_in_dhcp6_docsic_cmts():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
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
    srv_msg.lease_file_contains(',00:f5:f4:00:f2:01')
    srv_msg.log_contains('Hardware addr: 00:f5:f4:00:f2:01')
