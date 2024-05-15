# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea config backend testing host reservations."""

import pytest

from src.protosupport.dhcp4_scen import get_address
from src.softwaresupport.cb_model import setup_server_for_config_backend_cmds

# pylint: disable=unused-argument

pytestmark = [pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.v4,
              pytest.mark.v6,
              pytest.mark.cb]


@pytest.mark.parametrize("initial_reservation_mode", [None, 'all', 'out-of-pool', 'global', 'disabled'])
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_reservation_mode_override_init(initial_reservation_mode, dhcp_version, backend):
    # set initial reservation-mode
    cfg, _ = setup_server_for_config_backend_cmds(backend_type=backend, reservation_mode=initial_reservation_mode,
                                                  check_config=True)

    # change reservation-mode to disabled or global and check it
    if initial_reservation_mode == 'disabled':
        exp_reservation_mode = 'global'
    else:
        exp_reservation_mode = 'disabled'
    cfg.set_global_parameter(backend=backend, reservation_mode=exp_reservation_mode)


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_reservation_mode_in_globals(dhcp_version, backend):
    if dhcp_version == 'v4':
        init_cfg = dict(
            subnet4=[{
                'subnet': '2.2.2.0/24',
                'pools': [{'pool': '2.2.2.1/32'}],
                'id': 1,
                'interface': '$(SERVER_IFACE)',
                'reservations': [{
                    "hw-address": "00:00:00:00:00:01",
                    "ip-address": '2.2.2.2'
                }]
            }],
            reservations=[{"hw-address": "00:00:00:00:00:01",
                           "ip-address": '2.2.2.88'}])

    else:
        init_cfg = dict(
            subnet6=[{
                'subnet': '2001:db8:1::/64',
                'pools': [{'pool': '2001:db8:1::1/128'}],
                'id': 1,
                'interface': '$(SERVER_IFACE)',
                'reservations': [{
                    "duid": "00:03:00:01:00:00:00:00:00:01",
                    "ip-addresses": ['2001:db8:1::2']
                }]
            }],
            reservations=[{"duid": "00:03:00:01:00:00:00:00:00:01",
                           "ip-addresses": ['2001:db8:1::88']}])

    init_cfg['check-config'] = True

    cfg, _ = setup_server_for_config_backend_cmds(backend_type=backend, **init_cfg)

    # by default reservation-mode is 'all' so the address should be returned from subnet reservation
    get_address(mac_addr="00:00:00:00:00:01", exp_addr='2.2.2.2' if dhcp_version == 'v4' else '2001:db8:1::2')

    # change reservation-mode to 'global' and now address should be returned from global reservations
    cfg.set_global_parameter(backend=backend, reservation_mode='global')
    get_address(mac_addr="00:00:00:00:00:01", exp_addr='2.2.2.88' if dhcp_version == 'v4' else '2001:db8:1::88')

    # now change reservation-mode to 'disabled' and then the address should be returned from subnet pool
    # (not from reservations)
    cfg.set_global_parameter(backend=backend, reservation_mode='disabled')
    get_address(mac_addr="00:00:00:00:00:01",
                exp_addr='2.2.2.1' if dhcp_version == 'v4' else '2001:db8:1::1')
