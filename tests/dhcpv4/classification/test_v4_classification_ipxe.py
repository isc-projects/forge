"""Client Classification DHCPv4"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_control
import misc
import srv_msg


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_iPXE_client_arch():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')

    srv_control.create_new_class('ipxe_efi_x64')
    srv_control.add_test_to_class('1', 'test', 'option[93].hex == 0x0009')
    srv_control.add_test_to_class('1', 'next-server', '192.0.2.254')
    srv_control.add_test_to_class('1', 'server-hostname', 'hal9000')
    srv_control.add_test_to_class('1', 'boot-file-name', '/dev/null')
    srv_control.config_client_classification('0', 'ipxe_efi_x64')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('client_id', 'ff:01:11:11:11:11:11:22')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_does_include_with_value('pxe_client_architecture', '9')
    srv_msg.client_does_include_with_value('pxe_client_network_interface', '320')
    srv_msg.client_does_include_with_value('pxe_client_machine_identifier', '123456789a')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')
    srv_msg.response_check_content('Response', None, 'siaddr', '192.0.2.254')
    srv_msg.response_check_content('Response', None, 'file', '/dev/null')
    srv_msg.response_check_content('Response', None, 'sname', 'hal9000')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_iPXE_client_inter():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')

    srv_control.create_new_class('ipxe_efi_x64')
    srv_control.add_test_to_class('1', 'test', 'option[94].hex == 0x030200')
    srv_control.add_test_to_class('1', 'next-server', '192.0.2.254')
    srv_control.add_test_to_class('1', 'server-hostname', 'hal9000')
    srv_control.add_test_to_class('1', 'boot-file-name', '/dev/null')
    srv_control.config_client_classification('0', 'ipxe_efi_x64')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('client_id', 'ff:01:11:11:11:11:11:22')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_does_include_with_value('pxe_client_architecture', '9')
    srv_msg.client_does_include_with_value('pxe_client_network_interface', '320')
    srv_msg.client_does_include_with_value('pxe_client_machine_identifier', '123456789a')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')
    srv_msg.response_check_content('Response', None, 'siaddr', '192.0.2.254')
    srv_msg.response_check_content('Response', None, 'file', '/dev/null')
    srv_msg.response_check_content('Response', None, 'sname', 'hal9000')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.classification
def test_v4_client_classification_iPXE_machine_ident():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')

    srv_control.create_new_class('ipxe_efi_x64')
    srv_control.add_test_to_class('1', 'test', 'option[97].hex == 0x0102030405060708090a')
    srv_control.add_test_to_class('1', 'next-server', '192.0.2.254')
    srv_control.add_test_to_class('1', 'server-hostname', 'hal9000')
    srv_control.add_test_to_class('1', 'boot-file-name', '/dev/null')
    srv_control.config_client_classification('0', 'ipxe_efi_x64')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('client_id', 'ff:01:11:11:11:11:11:22')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_does_include_with_value('pxe_client_architecture', '9')
    srv_msg.client_does_include_with_value('pxe_client_network_interface', '320')
    srv_msg.client_does_include_with_value('pxe_client_machine_identifier', '123456789a')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.50')
    srv_msg.response_check_content('Response', None, 'siaddr', '192.0.2.254')
    srv_msg.response_check_content('Response', None, 'file', '/dev/null')
    srv_msg.response_check_content('Response', None, 'sname', 'hal9000')

    #
    # 208: "pxelinux_magic",
    # 209: "pxelinux_configuration_file",
    # 210: "pxelinux_path_prefix",
    # 211: "pxelinux_reboot_time",
