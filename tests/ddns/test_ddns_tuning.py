# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Marcin Godzina

"""DDNS Tuning Hook basic tests"""

# pylint: disable=invalid-name,line-too-long

import copy
import pytest
from src import misc
from src import srv_msg
from src import srv_control
from src.forge_cfg import world


def _get_address_v4_fqdn(address, chaddr, fqdn, expected_fqdn=None):
    expected_fqdn = fqdn if expected_fqdn is None else expected_fqdn
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', chaddr)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', address)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', chaddr)
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', address)
    if fqdn is not None:
        srv_msg.client_sets_value('Client', 'FQDN_domain_name', fqdn)
        srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
        srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', address)
    if fqdn is not None:
        srv_msg.response_check_include_option(81)
        srv_msg.response_check_option_content(81, 'fqdn', expected_fqdn)


def _get_address_v4_hostname(address, chaddr, hostname, expected_hostname=None):
    expected_hostname = hostname if expected_hostname is None else expected_hostname
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', chaddr)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', address)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', chaddr)
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', address)
    if hostname is not None:
        srv_msg.client_does_include_with_value('hostname', hostname)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', address)
    if hostname is not None:
        srv_msg.response_check_include_option(12)
        srv_msg.response_check_option_content(12, 'hostname', expected_hostname)


def _get_address_v6(duid, fqdn, expected_fqdn=None):
    expected_fqdn = fqdn if expected_fqdn is None else expected_fqdn
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    if fqdn is not None:
        srv_msg.client_sets_value('Client', 'FQDN_domain_name', fqdn)
        srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
        srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    if fqdn is not None:
        srv_msg.response_check_include_option(39)
        srv_msg.response_check_option_content(39, 'fqdn', expected_fqdn)


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('option', ['fqdn', 'hostname'])
@pytest.mark.parametrize('hostname_type', ['basic', 'suffix', 'empty'])
def test_v4_ddns_tuning_basic(backend, hostname_type, option):
    """
    Test of the "ddns-tuning" premium hook basic functionality.
    This basic test sets ddns-tuning hook parameter to replace hostname with expression
    including text and hardware address.
    DORA/SARR exchange acquires lease and leaseX-get command returns hostname applied to lease.
    We then compare returned lease with expected.
    Parameter 'suffix' and 'empty' check for proper behaviour with global suffix applied or global tuning disabled.
    """
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)

    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')

    # Import hook and set parameters.
    srv_control.add_hooks('libdhcp_ddns_tuning.so')
    srv_control.add_parameter_to_hook(1, "hostname-expr",
                                      "" if hostname_type == 'empty' else "'host-'+hexstring(pkt4.mac,'-')")
    srv_control.add_hooks('libdhcp_lease_cmds.so')

    if hostname_type == 'suffix':
        # set suffix for ddns
        world.dhcp_cfg['ddns-qualifying-suffix'] = 'foo.bar.'

    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # select expected fqdn based on test parametrization
    if hostname_type == 'basic':
        fqdn = 'host-ff-01-02-03-ff-04.'
    elif hostname_type == 'suffix':
        fqdn = 'host-ff-01-02-03-ff-04.foo.bar.'
    elif hostname_type == 'empty':
        fqdn = 'test.com.'
    # Acquire lease
    if option == 'fqdn':
        _get_address_v4_fqdn('192.168.50.1', chaddr='ff:01:02:03:ff:04', fqdn='test.com',
                             expected_fqdn=fqdn)
    elif option == 'hostname':
        # remove trailing dot from fqdn for hostname
        _get_address_v4_hostname('192.168.50.1', chaddr='ff:01:02:03:ff:04', hostname='test.com',
                                 expected_hostname=fqdn[:-1])
    # get lease details from Kea using Control Agent
    cmd = {"command": "lease4-get-all"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')
    # remove trailing dot from fqdn for hostname
    fqdn = fqdn[:-1] if hostname_type != 'empty' or option == 'hostname' else fqdn
    # Check fqdn/hostname returned by Control Channel
    assert response['arguments']['leases'][0]['hostname'] == fqdn
    # Check if lease has proper fqdn/hostname in backend
    srv_msg.check_leases({'hostname': fqdn, "address": "192.168.50.1"}, backend)


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('hostname_type', ['basic', 'suffix', 'empty'])
def test_v6_ddns_tuning_basic(backend, hostname_type):
    """
    Test of the "ddns-tuning" premium hook basic functionality.
    This basic test sets ddns-tuning hook parameter to replace hostname with expression
    including text and hardware address.
    DORA/SARR exchange acquires lease and leaseX-get command returns hostname applied to lease.
    We then compare returned lease with expected.
    Parameter 'suffix' and 'empty' check for proper behaviour with global suffix applied or global tuning disabled.
    """
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)

    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::21')

    # Import hook and set parameters.
    srv_control.add_hooks('libdhcp_ddns_tuning.so')

    srv_control.add_parameter_to_hook(1, "hostname-expr",
                                      "" if hostname_type == 'empty' else "'host-'+hexstring(option[1].hex, '-')")
    srv_control.add_hooks('libdhcp_lease_cmds.so')

    if hostname_type == 'suffix':
        # set suffix for ddns
        world.dhcp_cfg['ddns-qualifying-suffix'] = 'foo.bar.'

    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # select expected fqdn based on test parametrization
    if hostname_type == 'basic':
        fqdn = 'host-00-03-00-01-66-55-44-33-22-11.'
    elif hostname_type == 'suffix':
        fqdn = 'host-00-03-00-01-66-55-44-33-22-11.foo.bar.'
    elif hostname_type == 'empty':
        fqdn = 'test.com.'
    # Acquire lease
    _get_address_v6(duid='00:03:00:01:66:55:44:33:22:11', fqdn='test.com.', expected_fqdn=fqdn)
    cmd = {"command": "lease6-get-all"}
    # get lease details from Kea using Control Agent
    response = srv_msg.send_ctrl_cmd(cmd, 'http')
    # Check fqdn/hostname returned by Control Channel
    assert response['arguments']['leases'][0]['hostname'] == fqdn
    # Check if lease has proper fqdn/hostname in backend
    srv_msg.check_leases({'hostname': fqdn, 'address': '2001:db8:1::1'}, backend)


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('option', ['fqdn', 'hostname'])
@pytest.mark.parametrize('hostname_type', ['basic', 'suffix', 'empty'])
def test_v4_ddns_tuning_subnets(backend, hostname_type, option):
    """
    Test of the "ddns-tuning" premium hook basic functionality with configured subnets in IP v4.
    This test sets ddns-tuning hook parameter to replace hostname with expression including text and hardware address
    globally and per subnet.
    First subnet uses global expression, and rest uses respective subnet configured expressions.
    DORA exchange acquires lease and lease4-get command returns hostname applied to lease.
    We then compare returned lease with expected.
    Parameter 'suffix' and 'empty' check for proper behaviour with global suffix applied or global tuning disabled.
    """
    nbr_of_subnets = 3  # number of subnets to use in test: from 2 to 9
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)

    # Configure subnets
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    for i in range(1, nbr_of_subnets):
        srv_control.config_srv_another_subnet_no_interface(f'192.168.5{i}.0/24',
                                                           f'192.168.5{i}.10-192.168.5{i}.10')
        srv_control.add_line_to_subnet(i, {"user-context": {
                "ddns-tuning": {
                    "hostname-expr": "" if hostname_type == "empty" else f"'host{i}-'+hexstring(pkt4.mac,'-')"
                }}})

    # Import hook and set parameters.
    srv_control.add_hooks('libdhcp_ddns_tuning.so')
    srv_control.add_parameter_to_hook(1, "hostname-expr",
                                      "" if hostname_type == 'empty' else "'host0-'+hexstring(pkt4.mac,'-')")

    srv_control.add_hooks('libdhcp_lease_cmds.so')

    # set suffix for ddns
    if hostname_type == 'suffix':
        world.dhcp_cfg['ddns-qualifying-suffix'] = 'foo.bar.'

    # Set shared subnets
    for i in range(nbr_of_subnets):
        srv_control.shared_subnet(f'192.168.5{i}.0/24', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Acquire leases and test them
    for i in range(nbr_of_subnets):
        # select expected fqdn/hostname based on test parametrization
        if hostname_type == 'basic':
            fqdn = f'host{i}-ff-01-02-03-ff-0{i}.'
        elif hostname_type == 'suffix':
            fqdn = f'host{i}-ff-01-02-03-ff-0{i}.foo.bar.'
        elif hostname_type == 'empty':
            fqdn = f'test{i}.com.'
        # Acquire lease
        if option == 'fqdn':
            _get_address_v4_fqdn(f'192.168.5{i}.10', chaddr=f'ff:01:02:03:ff:0{i}', fqdn=f'test{i}.com',
                                 expected_fqdn=fqdn)
        elif option == 'hostname':
            # remove trailing dot from fqdn for hostname
            _get_address_v4_hostname(f'192.168.5{i}.10', chaddr=f'ff:01:02:03:ff:0{i}', hostname=f'test{i}.com',
                                     expected_hostname=fqdn[:-1])
        cmd = {"command": "lease4-get",
               "arguments": {"ip-address": f'192.168.5{i}.10'}}
        # get lease details from Kea using Control Agent
        response = srv_msg.send_ctrl_cmd(cmd, 'http')
        fqdn = fqdn[:-1] if hostname_type != 'empty' or option == 'hostname' else fqdn
        # Check fqdn/hostname returned by Control Channel
        assert response['arguments']['hostname'] == fqdn
        # Check if lease has proper fqdn/hostname in backend
        srv_msg.check_leases({'hostname': fqdn, 'address': f'192.168.5{i}.10'}, backend)


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('hostname_type', ['basic', 'suffix', 'empty'])
def test_v6_ddns_tuning_subnets(backend, hostname_type):
    """
    Test of the "ddns-tuning" premium hook basic functionality with configured subnets in IP v6.
    This test sets ddns-tuning hook parameter to replace hostname with expression including text and hardware address
    globally and per subnet.
    First subnet uses global expression, and rest uses respective subnet configured expressions.
    SARR exchange acquires lease and leas6-get command returns hostname applied to lease.
    We then compare returned lease with expected.
    Parameter 'suffix' and 'empty' check for proper behaviour with global suffix applied or global tuning disabled.
    """
    nbr_of_subnets = 3  # number of subnets to use in test: from 2 to 9
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)

    # Configure subnets
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    for i in range(2, nbr_of_subnets + 1):
        srv_control.config_srv_another_subnet_no_interface(f'2001:db8:{i}::/64', f'2001:db8:{i}::1-2001:db8:{i}::1')
        srv_control.add_line_to_subnet(i-1, {"user-context": {
                "ddns-tuning": {
                    "hostname-expr": "" if hostname_type == 'empty' else f'\'host{i}-\'+hexstring(option[1].hex, \'-\')'
                }}})

    # Import hook and ser parameters.
    srv_control.add_hooks('libdhcp_ddns_tuning.so')
    srv_control.add_parameter_to_hook(1, "hostname-expr",
                                      "" if hostname_type == 'empty' else "'host1-'+hexstring(option[1].hex, '-')")

    srv_control.add_hooks('libdhcp_lease_cmds.so')

    # set suffix for ddns
    if hostname_type == 'suffix':
        world.dhcp_cfg['ddns-qualifying-suffix'] = 'foo.bar'

    # Set shared subnets
    for i in range(1, nbr_of_subnets + 1):
        srv_control.shared_subnet(f'2001:db8:{i}::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Acquire leases and test them
    for i in range(1, nbr_of_subnets + 1):
        # select expected hostname based on test parametrization
        if hostname_type == 'basic':
            fqdn = f'host{i}-00-03-00-01-66-55-44-33-22-1{i}.'
        elif hostname_type == 'suffix':
            fqdn = f'host{i}-00-03-00-01-66-55-44-33-22-1{i}.foo.bar.'
        elif hostname_type == 'empty':
            fqdn = f'test{i}.com.'
        # Acquire lease
        _get_address_v6(duid=f'00:03:00:01:66:55:44:33:22:1{i}', fqdn=f'test{i}.com', expected_fqdn=fqdn)
        cmd = {"command": "lease6-get",
               "arguments": {"ip-address": f'2001:db8:{i}::1'}}
        # get lease details from Kea using Control Agent
        response = srv_msg.send_ctrl_cmd(cmd, 'http')
        # Check hostname returned by Control Channel
        assert response['arguments']['hostname'] == fqdn
        # Check if lease has proper hostname in backend
        srv_msg.check_leases({'hostname': fqdn, 'address': f'2001:db8:{i}::1'}, backend)


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('option', ['fqdn', 'hostname'])
def test_v4_ddns_tuning_skip(backend, option):
    """
    """
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)

    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')

    reservations = [
        {
            "client-classes": ["SKIP_DDNS"],
            'hw-address': 'ff:01:02:03:ff:05'
        }
    ]
    world.dhcp_cfg.update({'reservations': copy.deepcopy(reservations)})
    world.dhcp_cfg['reservations-global'] = True
    world.dhcp_cfg['reservations-in-subnet'] = True

    # Import hook and set parameters.
    srv_control.add_hooks('libdhcp_ddns_tuning.so')
    srv_control.add_parameter_to_hook(1, "hostname-expr", "'ddns-tuning.'")
    srv_control.add_hooks('libdhcp_lease_cmds.so')

    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    fqdn = 'ddns-tuning.'
    fqdn2 = 'test.com.'

    # Acquire lease
    if option == 'fqdn':
        _get_address_v4_fqdn('192.168.50.1', chaddr='ff:01:02:03:ff:04', fqdn='test.com',
                             expected_fqdn="ddns-tuning.")
    elif option == 'hostname':
        # remove trailing dot from fqdn for hostname
        _get_address_v4_hostname('192.168.50.1', chaddr='ff:01:02:03:ff:04', hostname='test.com',
                                 expected_hostname="ddns-tuning."[:-1])

    if option == 'fqdn':
        _get_address_v4_fqdn('192.168.50.2', chaddr='ff:01:02:03:ff:05', fqdn='test.com',
                             expected_fqdn="test.com.")
    elif option == 'hostname':
        # remove trailing dot from fqdn for hostname
        _get_address_v4_hostname('192.168.50.2', chaddr='ff:01:02:03:ff:05', hostname='test.com',
                                 expected_hostname="test.com."[:-1])

    # get lease details from Kea using Control Agent
    cmd = {"command": "lease4-get-all"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')

    # remove trailing dot from fqdn for hostname
    fqdn = fqdn[:-1] if option == 'hostname' else fqdn
    fqdn2 = fqdn2[:-1] if option == 'hostname' else fqdn2

    # Check fqdn/hostname returned by Control Channel
    assert response['arguments']['leases'][0]['hostname'] == fqdn
    assert response['arguments']['leases'][1]['hostname'] == fqdn2

    # Check if lease has proper fqdn/hostname in backend
    srv_msg.check_leases({'hostname': fqdn, "address": "192.168.50.1"}, backend)
    srv_msg.check_leases({'hostname': fqdn2, "address": "192.168.50.2"}, backend)
