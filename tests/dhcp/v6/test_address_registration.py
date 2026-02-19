# Copyright (C) 2025-2026 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""DHCPv6 Address Registration tests (RFC9686)"""

import pytest

from src import srv_msg
from src import srv_control
from src import misc

from src.forge_cfg import world
from src.protosupport.multi_protocol_functions import log_contains


def _generate_testing_ip_address():
    """Generate testing IP address."""
    # Testing ip has to be configured on Forge interface.
    ip_addr = world.f_cfg.client_ipv6_addr_global
    # Forge v6 ip has to be in configured subnet.
    subnet = ip_addr.split(':')[0] + ':' + ip_addr.split(':')[1]
    pool = subnet + '::1-' + subnet + '::100'
    return ip_addr, subnet, pool


def _is_kea_responding():
    """Verify that Kea is still responding to traffic."""
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('INFOREQUEST')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')


def register_address(ip_addr, src_address, expect_response=True):
    """Register address.

    :param ip_addr: IP address to register
    :type ip_addr: str
    :param src_address: Source address to use for the registration
    :type src_address: str
    :param expect_response: Whether to expect a response
    :type expect_response: bool
    """
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'preflft', '3611')
    srv_msg.client_sets_value('Client', 'validlft', '7222')
    srv_msg.client_sets_value('Client', 'IA_Address', ip_addr)
    srv_msg.client_does_include('Client', 'IA_Address_top_level')
    srv_msg.client_send_msg('ADDR-REG-INFORM', src=src_address)

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADDR-REG-REPLY', expect_response=expect_response)


@pytest.mark.v6
@pytest.mark.parametrize('option', ['OptionDefined', 'OptionUndefined'])
@pytest.mark.parametrize('registration', ['RegistrationEnabled', 'RegistrationDisabled'])
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_v6_address_registration_basic(option, registration, backend):
    """Test address registration basic functionality.
    This test assumes that option return and lease registration are defined and working independently.

    :param option: Option defined or undefined
    :type option: str
    :param registration: Address Registration enabled or disabled
    :type registration: str
    :param backend: Lease database backend
    :type backend: str
    """
    option = option == 'OptionDefined'
    registration = registration == 'RegistrationEnabled'

    ip_addr, subnet, pool = _generate_testing_ip_address()

    misc.test_setup()
    srv_control.config_srv_subnet(subnet + '::/32', pool, id=1)

    # Return of address registration option has to be enabled manually.
    if option:
        srv_control.config_srv_opt('addr-reg-enable', None)
    # Address registration feature is enabled by default in Kea 3.1.4
    srv_control.set_conf_parameter_global('allow-address-registration', registration)

    srv_control.define_lease_db_backend(backend)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Check if addr-reg-enable is not returned when not asked for.
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(148, expect_include=False)

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(148, expect_include=False)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(148, expect_include=False)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(148, expect_include=False)

    # Check if addr-reg-enable is returned when asked for depending on the configuration.
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_requests_option(148)
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(148, expect_include=option)

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(148)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(148, expect_include=option)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_requests_option(148)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(148, expect_include=option)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_requests_option(148)
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(148, expect_include=option)

    # Check if Kea correctly registers the address depending on the configuration.
    misc.test_procedure()
    register_address(ip_addr, ip_addr, expect_response=registration)

    srv_msg.check_leases(
        {
            "address": ip_addr,
            "preflft": "3611",
            "validlft": "7222",
            "state": "4",  # 4 is the state of a registered address
        },
        backend,
        should_succeed=registration,
    )

    # Verify that Kea is still responding to traffic.
    _is_kea_responding()


@pytest.mark.v6
def test_v6_address_registration_out_off_subnet():
    """Test proper rejection of address registration with ip address out of subnet."""
    # Testing ip has to be configured on Forge interface.
    ip_addr = world.f_cfg.client_ipv6_addr_global
    # Make sure we are using different subnet than the one used for testing ip.
    prefix = '3099' if '3099' != ip_addr.split(':')[0] else '3001'
    subnet = prefix + '::/64'
    pool = prefix + '::1-' + prefix + '::100'

    misc.test_setup()
    srv_control.config_srv_subnet(subnet, pool, id=1)

    # Return of address registration option has to be enabled manually.
    srv_control.config_srv_opt("addr-reg-enable", None)
    # Address registration feature is enabled by default in Kea 3.1.4
    # srv_control.set_conf_parameter_global('allow-address-registration', True)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Check if Kea correctly rejects the address registration with mismatched ip address.
    misc.test_procedure()
    register_address(ip_addr, ip_addr, expect_response=False)

    log_contains(f'DHCP6_ADDR_REG_INFORM_FAIL error on ADDR-REG-INFORM from client {ip_addr}, '
                 f'Address {ip_addr} is not in subnet {subnet} (id 1)')

    srv_msg.check_leases({"address": ip_addr}, should_succeed=False)

    # Verify that Kea is still responding to traffic.
    _is_kea_responding()


@pytest.mark.v6
def test_v6_address_registration_negative():
    """Test proper rejection of address registration."""
    ip_addr, subnet, pool = _generate_testing_ip_address()
    assert '3001' != ip_addr.split(':')[0] and '999' != ip_addr.split(':')[1], \
        "Subnet must be different from the one used for testing ip. That is rare coincidence in generating Forge IP."

    misc.test_setup()
    srv_control.config_srv_subnet(subnet + '::/32', pool, id=1)

    # Return of address registration option has to be enabled manually.
    srv_control.config_srv_opt("addr-reg-enable", None)
    # Address registration feature is enabled by default in Kea 3.1.4
    # srv_control.set_conf_parameter_global('allow-address-registration', True)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Check if Kea correctly rejects the address registration with mismatched ip address.
    register_address('3001:999:5::2000', ip_addr, expect_response=False)

    log_contains(f'DHCP6_ADDR_REG_INFORM_FAIL error on ADDR-REG-INFORM from client {ip_addr}, '
                 f'Address mismatch: client at {ip_addr} wants to register 3001:999:5::2000')

    srv_msg.check_leases({"address": '3001:999:5::2000'}, should_succeed=False)

    # Check if Kea correctly rejects the address registration without IA_Address.
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'preflft', '3611')
    srv_msg.client_sets_value('Client', 'validlft', '7222')

    srv_msg.client_send_msg('ADDR-REG-INFORM', src=ip_addr)

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADDR-REG-REPLY', expect_response=False)

    log_contains(f'DHCP6_ADDR_REG_INFORM_FAIL error on ADDR-REG-INFORM from client {ip_addr}, '
                 f'Exactly 1 IAADDR option expected, but 0 received')

    srv_msg.check_leases({"address": ip_addr}, should_succeed=False)

    # Check if Kea correctly rejects the address registration without client-id.
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'preflft', '3611')
    srv_msg.client_sets_value('Client', 'validlft', '7222')
    srv_msg.client_sets_value('Client', 'IA_Address', ip_addr)
    srv_msg.client_does_include('Client', 'IA_Address_top_level')

    srv_msg.client_send_msg('ADDR-REG-INFORM', src=ip_addr)

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADDR-REG-REPLY', expect_response=False)

    log_contains(f'ADDR_REG_INFORM message received from {ip_addr} failed the following check: '
                 f'Exactly 1 client-id option expected in ADDR_REG_INFORM, but 0 received')

    srv_msg.check_leases({"address": ip_addr}, should_succeed=False)

    # Check if Kea correctly rejects the address registration with server-id.

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('INFOREQUEST')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'preflft', '3611')
    srv_msg.client_sets_value('Client', 'validlft', '7222')
    srv_msg.client_sets_value('Client', 'IA_Address', ip_addr)
    srv_msg.client_does_include('Client', 'IA_Address_top_level')
    srv_msg.client_requests_option(7)

    srv_msg.client_send_msg('ADDR-REG-INFORM', src=ip_addr)

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADDR-REG-REPLY', expect_response=False)

    log_contains(f'ADDR_REG_INFORM message received from {ip_addr} failed the following check: '
                 f'Server-id option was not expected, but 1 received in ADDR_REG_INFORM')

    srv_msg.check_leases({"address": ip_addr}, should_succeed=False)

    # This check is intentionally ignoring RFC so it is not tested.
    # -------------------------------------------------------------
    # # Check if Kea correctly rejects the address registration with requested options.
    # misc.test_procedure()
    # srv_msg.client_does_include('Client', 'client-id')
    # srv_msg.client_sets_value('Client', 'preflft', '3611')
    # srv_msg.client_sets_value('Client', 'validlft', '7222')
    # srv_msg.client_sets_value('Client', 'IA_Address', ip_addr)
    # srv_msg.client_does_include('Client', 'IA_Address_top_level')
    # srv_msg.client_requests_option(7)

    # srv_msg.client_send_msg('ADDR-REG-INFORM', src=ip_addr)

    # misc.pass_criteria()
    # srv_msg.send_wait_for_message('MUST', 'ADDR-REG-REPLY', expect_response=False)

    # log_contains('')  # Expected log message

    # srv_msg.check_leases({"address": ip_addr}, should_succeed=False)
    # -------------------------------------------------------------

    # Check if Kea correctly rejects the address registration with multiple IA_Address.
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'preflft', '3611')
    srv_msg.client_sets_value('Client', 'validlft', '7222')
    srv_msg.client_sets_value('Client', 'IA_Address', '3001:999:5::2000')
    srv_msg.client_does_include('Client', 'IA_Address_top_level')
    srv_msg.client_sets_value('Client', 'IA_Address', '3001:999:5::2001')
    srv_msg.client_does_include('Client', 'IA_Address_top_level')

    srv_msg.client_send_msg('ADDR-REG-INFORM', src=ip_addr)

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADDR-REG-REPLY', expect_response=False)

    log_contains(f'DHCP6_ADDR_REG_INFORM_FAIL error on ADDR-REG-INFORM from client {ip_addr}, '
                 f'Exactly 1 IAADDR option expected, but 2 received')

    srv_msg.check_leases({"address": ip_addr}, should_succeed=False)
    srv_msg.check_leases({"address": '3001:999:5::2001'}, should_succeed=False)
    srv_msg.check_leases({"address": '3001:999:5::2000'}, should_succeed=False)

    # Verify that Kea is still responding to traffic.
    _is_kea_responding()


@pytest.mark.v6
@pytest.mark.parametrize("backend", ["memfile", "mysql", "postgresql"])
def test_v6_address_registration_existing_lease(backend):
    """Test if kea rejects attempt to register existing lease.

    :param backend: Lease database backend
    :type backend: str
    """
    ip_addr, subnet, pool = _generate_testing_ip_address()

    misc.test_setup()
    srv_control.config_srv_subnet(subnet + "::/32", pool, id=1)

    # Return of address registration option has to be enabled manually.
    srv_control.config_srv_opt("addr-reg-enable", None)
    # Address registration feature is enabled by default in Kea 3.1.4
    # srv_control.set_conf_parameter_global('allow-address-registration', True)

    srv_control.add_unix_socket()
    srv_control.add_hooks("libdhcp_lease_cmds.so")
    srv_control.define_lease_db_backend(backend)
    srv_control.build_and_send_config_files()
    srv_control.start_srv("DHCP", "started")

    # Add lease to the database.
    cmd = {
        "command": "lease6-add",
        "arguments": {
            "subnet-id": 1,
            "ip-address": ip_addr,
            "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
            "iaid": 1234,
            "hw-address": "1a:2b:3c:4d:5e:6f",
            "preferred-lft": 500,
            "valid-lft": 11111,
            "expire": 123456789,
        },
    }
    resp = srv_msg.send_ctrl_cmd(cmd, channel="socket")
    assert resp["text"] == f"Lease for address {ip_addr}, subnet-id 1 added."

    # Check if Kea correctly rejects existing lease registration.
    misc.test_procedure()
    register_address(ip_addr, ip_addr, expect_response=False)

    log_contains(f"DHCP6_ADDR_REG_INFORM_FAIL error on ADDR-REG-INFORM from client {ip_addr}, "
                 f"Address {ip_addr} already in use")

    # Verify that the lease is still in the database with correct parameters.
    cmd = {"command": "lease6-get", "arguments": {"ip-address": ip_addr}}
    resp = srv_msg.send_ctrl_cmd(cmd, channel="socket")

    del resp["arguments"]["cltt"]  # this value is dynamic so we delete it
    assert resp["arguments"] == {
        "duid": "1a:1b:1c:1d:1e:1f:20:21:22:23:24",
        "fqdn-fwd": False,
        "fqdn-rev": False,
        "hostname": "",
        "hw-address": "1a:2b:3c:4d:5e:6f",
        "iaid": 1234,
        "ip-address": ip_addr,
        "preferred-lft": 500,
        "state": 0,
        "subnet-id": 1,
        "type": "IA_NA",
        "valid-lft": 11111,
    }

    # Verify that Kea is still responding to traffic.
    _is_kea_responding()


@pytest.mark.v6
@pytest.mark.parametrize("lease_backend", ["memfile", "mysql", "postgresql"])
@pytest.mark.parametrize("reservation_backend", ['memfile', 'MySQL', 'PostgreSQL'])
def test_v6_address_registration_reserved_address(lease_backend, reservation_backend):
    """Test if kea rejects attempt to register reserved address.

    :param lease_backend: Lease database backend
    :type lease_backend: str
    :param reservation_backend: Reservation database backend
    :type reservation_backend: str
    """
    ip_addr, subnet, pool = _generate_testing_ip_address()

    misc.test_setup()
    srv_control.enable_db_backend_reservation(reservation_backend)
    srv_control.config_srv_subnet(subnet + "::/32", pool, id=1)
    if reservation_backend == 'memfile':
        srv_control.host_reservation_in_subnet('ip-address',
                                               ip_addr,
                                               0,
                                               'duid',
                                               '00:03:00:01:f6:f5:f4:f3:f2:99')
    else:
        srv_control.new_db_backend_reservation(reservation_backend, 'duid', '00:03:00:01:f6:f5:f4:f3:f2:99')
        srv_control.ipv6_address_db_backend_reservation(ip_addr, '$(EMPTY)', reservation_backend, 1)
        srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, reservation_backend, 1)
        srv_control.upload_db_reservation(reservation_backend)

    # Return of address registration option has to be enabled manually.
    srv_control.config_srv_opt("addr-reg-enable", None)
    # Address registration feature is enabled by default in Kea 3.1.4
    # srv_control.set_conf_parameter_global('allow-address-registration', True)

    srv_control.add_unix_socket()
    srv_control.add_hooks("libdhcp_lease_cmds.so")
    srv_control.define_lease_db_backend(lease_backend)
    srv_control.build_and_send_config_files()
    srv_control.start_srv("DHCP", "started")

    # Check if Kea correctly rejects lease registration with reserved address.
    misc.test_procedure()
    register_address(ip_addr, ip_addr, expect_response=False)

    log_contains(f"DHCP6_ADDR_REG_INFORM_FAIL error on ADDR-REG-INFORM from client {ip_addr}, "
                 f"Address {ip_addr} is reserved")

    # Verify that the lease is not in the database.
    srv_msg.check_leases({"address": ip_addr}, lease_backend, should_succeed=False)

    # Verify that Kea is still responding to traffic.
    _is_kea_responding()


@pytest.mark.v6
def test_v6_address_registration_relay():
    """Test if kea correctly registers address in relayed message."""
    ip_addr, subnet, pool = _generate_testing_ip_address()
    next_ip_addr = ip_addr.rsplit(':', 1)[0] + ':' + str(int(ip_addr.rsplit(':', 1)[1]) + 1)
    assert '3001' != ip_addr.split(':')[0] and '999' != ip_addr.split(':')[1], \
        "Subnet must be different from the one used for testing ip. That is rare coincidence in generating Forge IP."

    misc.test_setup()
    srv_control.config_srv_subnet(subnet + "::/32", pool, id=1)

    # Return of address registration option has to be enabled manually.
    srv_control.config_srv_opt("addr-reg-enable", None)
    # Address registration feature is enabled by default in Kea 3.1.4
    # srv_control.set_conf_parameter_global('allow-address-registration', True)

    srv_control.build_and_send_config_files()
    srv_control.start_srv("DHCP", "started")

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'preflft', '3611')
    srv_msg.client_sets_value('Client', 'validlft', '7222')
    srv_msg.client_sets_value('Client', 'IA_Address', ip_addr)
    srv_msg.client_does_include('Client', 'IA_Address_top_level')
    srv_msg.client_send_msg('ADDR-REG-INFORM')

    # Set linkaddr to the next IP address in the subnet. (It does not have to be the same as peeraddr.)
    srv_msg.client_sets_value('Client', 'linkaddr', next_ip_addr)
    # Set peeraddr to the IP address of the client. This is mandatory for relayed messages.
    srv_msg.client_sets_value('Client', 'peeraddr', ip_addr)

    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    # Expect a relay reply.
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')

    srv_msg.response_check_include_option('interface-id')
    srv_msg.response_check_include_option('relay-msg')
    srv_msg.response_check_option_content('relay-msg', 'Relayed', 'Message')

    srv_msg.check_leases(
        {
            "address": ip_addr,
            "preflft": "3611",
            "validlft": "7222",
            "state": "4",  # 4 is the state of a registered address
        }
    )

    # Verify that Kea is still responding to traffic.
    _is_kea_responding()


@pytest.mark.v6
def test_v6_address_registration_relay_negative():
    """Test proper rejection of relayedaddress registration."""
    ip_addr, subnet, pool = _generate_testing_ip_address()
    wrong_ip_addr = ip_addr.rsplit(':', 1)[0] + ':' + str(int(ip_addr.rsplit(':', 1)[1]) + 1)

    misc.test_setup()
    srv_control.config_srv_subnet(subnet + "::/32", pool, id=1)

    # Return of address registration option has to be enabled manually.
    srv_control.config_srv_opt("addr-reg-enable", None)
    # Address registration feature is enabled by default in Kea 3.1.4
    # srv_control.set_conf_parameter_global('allow-address-registration', True)

    srv_control.build_and_send_config_files()
    srv_control.start_srv("DHCP", "started")

    # Wrong peeraddr and correct IA_Address. (linkaddr should not be checked by Kea)
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'preflft', '3611')
    srv_msg.client_sets_value('Client', 'validlft', '7222')
    srv_msg.client_sets_value('Client', 'IA_Address', ip_addr)
    srv_msg.client_does_include('Client', 'IA_Address_top_level')
    srv_msg.client_send_msg('ADDR-REG-INFORM')

    srv_msg.client_sets_value('Client', 'linkaddr', ip_addr)
    srv_msg.client_sets_value('Client', 'peeraddr', wrong_ip_addr)

    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY', expect_response=False)

    srv_msg.check_leases({"address": ip_addr}, should_succeed=False)

    log_contains(f'DHCP6_ADDR_REG_INFORM_FAIL error on ADDR-REG-INFORM from client {wrong_ip_addr}, '
                 f'Address mismatch: client at {wrong_ip_addr} wants to register {ip_addr}')

    # Correct peeraddr and wrong IA_Address. (linkaddr should not be checked by Kea)
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'preflft', '3611')
    srv_msg.client_sets_value('Client', 'validlft', '7222')
    srv_msg.client_sets_value('Client', 'IA_Address', wrong_ip_addr)
    srv_msg.client_does_include('Client', 'IA_Address_top_level')
    srv_msg.client_send_msg('ADDR-REG-INFORM')

    srv_msg.client_sets_value('Client', 'linkaddr', wrong_ip_addr)
    srv_msg.client_sets_value('Client', 'peeraddr', ip_addr)

    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY', expect_response=False)

    log_contains(f'DHCP6_ADDR_REG_INFORM_FAIL error on ADDR-REG-INFORM from client {ip_addr}, '
                 f'Address mismatch: client at {ip_addr} wants to register {wrong_ip_addr}')

    srv_msg.check_leases({"address": ip_addr}, should_succeed=False)
    srv_msg.check_leases({"address": wrong_ip_addr}, should_succeed=False)

    # Verify that Kea is still responding to traffic.
    _is_kea_responding()
