# Copyright (C) 2019-2024 Internet Systems Consortium.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# pylint: disable=unused-argument

'''Simple test for BOOTP'''

import pytest

from src import srv_msg
from src import srv_control
from src import misc

from src.forge_cfg import world


@pytest.mark.v4
@pytest.mark.v4_bootp
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_bootp_basic_request_reply(dhcp_version, backend):
    '''Checks that two separate clients can get separate leases from the same pool
    through BOOTP and DHCP respectively.

    Arguments:
    backend -- the type of lease database
    '''
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.add_hooks('libdhcp_bootp.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # DORA should ACK.
    srv_msg.DORA('192.168.50.1', chaddr='ff:11:11:11:11:11')

    # First exchange
    srv_msg.BOOTP_REQUEST_and_BOOTP_REPLY('192.168.50.2', chaddr='ff:22:22:22:22:22')

    # A second exchange should get the same lease.
    srv_msg.BOOTP_REQUEST_and_BOOTP_REPLY('192.168.50.2', chaddr='ff:22:22:22:22:22')


@pytest.mark.v4
@pytest.mark.v4_bootp
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('bootp_first', [False, True])
def test_bootp_basic_request_reply_same_chaddr(dhcp_version, backend, bootp_first):
    '''Checks that the same client can get the same lease by switching from
    BOOTP to DHCP and from DHCP to BOOTP.

    Arguments:
    backend -- the type of lease database
    bootp_first -- whether the first request should be BOOTP or DHCP
    '''
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.add_hooks('libdhcp_bootp.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Run twice to check that the same request gets the same lease the second
    # time.
    for i in range(3):
        if bootp_first or i > 0:
            # BOOTP with the same chaddr should get the same lease.
            srv_msg.BOOTP_REQUEST_and_BOOTP_REPLY('192.168.50.1')

        # DORA should ACK.
        srv_msg.DORA('192.168.50.1')


@pytest.mark.v4
@pytest.mark.v4_bootp
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_bootp_basic_request_reply_classes(dhcp_version, backend):
    '''Checks that two separate clients can get separate leases through BOOTP
    and DHCP respectively from separate pools matched by the special BOOTP
    client class.

    Arguments:
    backend -- the type of lease database
    '''
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.new_pool('192.168.50.10-192.168.50.10', 0)
    srv_control.add_hooks('libdhcp_bootp.so')

    world.dhcp_cfg["subnet4"][0]["pools"][0]["client-classes"] = ["BOOTP"]
    world.dhcp_cfg["subnet4"][0]["pools"][1]["client-classes"] = ["DHCP"]
    srv_control.create_new_class('DHCP')
    srv_control.add_test_to_class(1, 'test', "not member('BOOTP')")
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # First exchange
    srv_msg.BOOTP_REQUEST_and_BOOTP_REPLY('192.168.50.1', chaddr='ff:11:11:11:11:11')

    # Let's test that we still get a lease on a second exchange.
    srv_msg.BOOTP_REQUEST_and_BOOTP_REPLY('192.168.50.1', chaddr='ff:11:11:11:11:11')

    # DORA should still work.
    srv_msg.DORA('192.168.50.10', chaddr='ff:22:22:22:22:22')
