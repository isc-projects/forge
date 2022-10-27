# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea features"""

import pytest

from src import srv_msg
from src import srv_control
from src import misc

from src.forge_cfg import world


@pytest.mark.v4
def test_v4_echo_client_id_disabled():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.set_conf_parameter_global('echo-client-id', False)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(61, expect_include=False)

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(61, expect_include=False)


@pytest.mark.v4
def test_v4_echo_client_id_enabled():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.set_conf_parameter_global('echo-client-id', True)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(61, 'value', '00010203040506')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(61, 'value', '00010203040506')


@pytest.mark.v4
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('requested_address', ['in-pool-free', 'in-pool-leased', 'out-of-pool'])
@pytest.mark.parametrize('authoritative', [False, True])
@pytest.mark.parametrize('has_existing_lease', [False, True])
@pytest.mark.parametrize('init_reboot', [False, True])
def test_v4_authoritative(backend, requested_address, authoritative, has_existing_lease, init_reboot):
    '''Checks that a client gets the proper response from a server configured
    with different values of authoritative.

    :param backend: the lease database backend type
    :param requested_address: what value the client uses for option 50
    :param authoritative: the value for the server's authoritative setting
    :param has_existing_lease: whether the client has an existing lease at the moment
        it requests the address
    :param init_reboot: whether the client is in an INIT-REBOOT state when it
        requests the address
    '''
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.100')
    srv_control.define_temporary_lease_db_backend(backend)
    world.dhcp_cfg['authoritative'] = authoritative
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Have an auxiliary client get a lease. It will help in testing NAKs.
    srv_msg.DORA('192.168.50.1', chaddr='ff:11:11:11:11:11')
    srv_msg.check_leases([
        {'address': '192.168.50.1', 'hwaddr': 'ff:11:11:11:11:11', 'valid_lifetime': 4000},
    ], backend=backend)

    if has_existing_lease:
        # Give our client a proper lease.
        srv_msg.DORA('192.168.50.2')
        srv_msg.check_leases([
            {'address': '192.168.50.2', 'hwaddr': 'ff:01:02:03:ff:04', 'valid_lifetime': 4000},
        ], backend=backend)
    else:
        # Give some other client a lease so that the lease internal counter in
        # Kea is incremented to the same level.
        srv_msg.DORA('192.168.50.2', chaddr='ff:22:22:22:22:22')
        srv_msg.check_leases([
            {'address': '192.168.50.2', 'hwaddr': 'ff:22:22:22:22', 'valid_lifetime': 4000},
        ], backend=backend)

    # Invariably, when the client is in an INIT-REBOOT case, these are the
    # expected responses.
    if init_reboot:
        if has_existing_lease:
            expected_response_type = 'NAK'
        else:
            if authoritative:
                expected_response_type = 'NAK'
            else:
                expected_response_type = None

    # Requesting an address from the pool, but not leased by any other client
    # usually results in an ACK.
    if requested_address == 'in-pool-free':
        if not init_reboot:
            expected_response_type = 'ACK'
        srv_msg.RA('192.168.50.100', response_type=expected_response_type, init_reboot=init_reboot)
        # If the client got an ACK, the lease should be in the database.
        srv_msg.check_leases([
            {'address': '192.168.50.100', 'hwaddr': 'ff:01:02:03:ff:04', 'valid_lifetime': 4000},
        ], backend=backend, should_succeed=(expected_response_type == 'ACK'))

    # Requesting an address from the pool, but already leased by another client
    # usually results in a NAK.
    if requested_address == 'in-pool-leased':
        if not init_reboot:
            expected_response_type = 'NAK'
        srv_msg.RA('192.168.50.1', response_type=expected_response_type, init_reboot=init_reboot)
        srv_msg.check_leases([
            {'address': '192.168.50.1', 'hwaddr': 'ff:01:02:03:ff:04', 'valid_lifetime': 4000},
        ], backend=backend, should_succeed=False)

    # Requesting an address outside the pool usually results in a silent ignore.
    if requested_address == 'out-of-pool':
        if not init_reboot:
            expected_response_type = None
        srv_msg.RA('192.168.50.200', response_type=expected_response_type, init_reboot=init_reboot)
        srv_msg.check_leases([
            {'address': '192.168.50.200', 'hwaddr': 'ff:01:02:03:ff:04', 'valid_lifetime': 4000},
        ], backend=backend, should_succeed=False)
