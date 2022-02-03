"""Kea config backend testing host reservations."""

import pytest

from dhcp4_scen import get_address
from cb_model import setup_server_for_config_backend_cmds

# pylint: disable=unused-argument

pytestmark = [pytest.mark.kea_only,
              pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.v4,
              pytest.mark.v6,
              pytest.mark.config_backend]


@pytest.mark.parametrize("initial_reservation_mode", [None, 'all', 'out-of-pool', 'global', 'disabled'])
@pytest.mark.parametrize('backend', ['mysql'])
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


@pytest.mark.parametrize('backend', ['mysql'])
def test_reservation_mode_in_globals(dhcp_version, backend):
    if dhcp_version == 'v4':
        init_cfg = dict(
            subnet4=[{
                'subnet': '2.2.2.0/24',
                'pools': [{'pool': '2.2.2.1/32'}],
                'interface': '$(SERVER_IFACE)',
                'reservations': [{
                    "hw-address": "00:00:00:00:00:01",
                    "ip-address": '2.2.2.2'
                }]
            }],
            reservations=[{"hw-address": "00:00:00:00:00:01",
                           "ip-address": '1.1.1.1'}])

    else:
        init_cfg = dict(
            subnet6=[{
                'subnet': '2001:db8:1::/64',
                'pools': [{'pool': '2001:db8:1::1/128'}],
                'interface': '$(SERVER_IFACE)',
                'reservations': [{
                    "duid": "00:03:00:01:00:00:00:00:00:01",
                    "ip-addresses": ['2001:db8:1::2']
                }]
            }],
            reservations=[{"duid": "00:03:00:01:00:00:00:00:00:01",
                           "ip-addresses": ['2001:db8:1::3']}])

    init_cfg['check-config'] = True

    cfg, _ = setup_server_for_config_backend_cmds(backend_type=backend, **init_cfg)

    # by default reservation-mode is 'all' so the address should be returned from subnet reservation
    get_address(mac_addr="00:00:00:00:00:01", exp_addr='2.2.2.2' if dhcp_version == 'v4' else '2001:db8:1::2')

    # change reservation-mode to 'global' and now address should be returned from global reservations
    cfg.set_global_parameter(backend=backend, reservation_mode='global')
    get_address(mac_addr="00:00:00:00:00:01", exp_addr='1.1.1.1' if dhcp_version == 'v4' else '2001:db8:1::3')

    # now change reservation-mode to 'disabled' and then the address should be returned from subnet pool
    # (not from reservations)
    cfg.set_global_parameter(backend=backend, reservation_mode='disabled')
    get_address(mac_addr="00:00:00:00:00:01",
                exp_addr='2.2.2.1' if dhcp_version == 'v4' else '2001:db8:1::1')
