"""Kea config backend testing host reservations."""

import pytest

from dhcp4_scen import get_address
from cb_model import setup_server_for_config_backend_cmds


pytestmark = [pytest.mark.kea_only,
              pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.v4,
              pytest.mark.v6,
              pytest.mark.config_backend]


@pytest.mark.parametrize("initial_reservation_mode", [None, 'all', 'out-of-pool', 'global', 'disabled'])
def test_reservation_mode_override_init(initial_reservation_mode, dhcp_version):
    # set initial reservation-mode
    cfg, received_cfg = setup_server_for_config_backend_cmds(reservation_mode=initial_reservation_mode,
                                                             check_config=True)
    if initial_reservation_mode is None:
        exp_reservation_mode = 'all'
    else:
        exp_reservation_mode = initial_reservation_mode

    dhcp_key = 'Dhcp%s' % dhcp_version[1]

    # check if initial reservation-mode is set
    assert received_cfg[dhcp_key]['reservation-mode'] == exp_reservation_mode

    # change reservation-mode to disabled or global and check it
    if initial_reservation_mode == 'disabled':
        exp_reservation_mode = 'global'
    else:
        exp_reservation_mode = 'disabled'
    received_cfg = cfg.set_global_parameter(reservation_mode=exp_reservation_mode)
    assert received_cfg[dhcp_key]['reservation-mode'] == exp_reservation_mode


def test_reservation_mode_in_globals(dhcp_version):
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
                           "ip-addresses": ['2001:db8:1::1']}])

    init_cfg['check-config'] = True

    cfg, _ = setup_server_for_config_backend_cmds(**init_cfg)

    # by default reservation-mode is 'all' so the address should be returned from subnet reservation
    get_address(mac_addr="00:00:00:00:00:01", exp_addr='2.2.2.2' if dhcp_version == 'v4' else '2001:db8:1::2')

    # change reservation-mode to 'global' and now address should be returned from global reservations
    cfg.set_global_parameter(reservation_mode='global')
    get_address(mac_addr="00:00:00:00:00:01", exp_addr='1.1.1.1' if dhcp_version == 'v4' else '2001:db8:1::1')
    # BUG #585: this is failing because global fields are inherited by predefined subnets during config file parsing
    # and then later there are not longer inherited when are updated by CB API

    # now change reservation-mode to 'disabled' and then the address should be returned from subnet pool
    cfg.set_global_parameter(reservation_mode='disabled')
    get_address(mac_addr="00:00:00:00:00:01",
                exp_addr='2.2.2.1' if dhcp_version == 'v4' else '2001:db8:1::??')  # TODO: ipv6 addr
