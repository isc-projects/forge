"""Kea config backend testing classes."""

import pytest

from dhcp4_scen import get_address, get_rejected
from cb_model import setup_server_for_config_backend_cmds

# pylint: disable=invalid-name,line-too-long

pytestmark = [pytest.mark.v4,
              pytest.mark.v6,
              pytest.mark.kea_only,
              pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.cb]


@pytest.mark.parametrize("classes_kept_in", ["db", "config"])
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_class_in_subnet(dhcp_version, classes_kept_in, backend):
    # prepare initial config with 1 class 'modem' for 1 client with specificed MAC address
    if classes_kept_in == 'config':
        init_cfg = {'client-classes': [{'name': 'modem'}]}
        if dhcp_version == 'v4':
            init_cfg['client-classes'][0]['test'] = "hexstring(pkt4.mac, ':') == '00:00:00:00:00:01'"
        else:
            init_cfg['client-classes'][0]['test'] = "hexstring(option[1].hex, ':') == '00:03:00:01:00:00:00:00:00:01'"
    else:
        init_cfg = {}
    cfg = setup_server_for_config_backend_cmds(backend_type=backend, **init_cfg)

    if classes_kept_in == 'db':
        if dhcp_version == 'v4':
            cfg.add_class(backend=backend, name="modem", test="hexstring(pkt4.mac, ':') == '00:00:00:00:00:01'")
        else:
            cfg.add_class(backend=backend, name="modem",
                          test="hexstring(option[1].hex, ':') == '00:03:00:01:00:00:00:00:00:01'")

    # add 1 subnet that permits only client from 'modem' class
    subnet_cfg, _ = cfg.add_subnet(backend=backend, client_class='modem')

    # client from 'modem' class with specific MAC address should get lease
    get_address(mac_addr="00:00:00:00:00:01", exp_addr='192.168.50.1' if dhcp_version == 'v4' else '2001:db8:1::1')

    # client with another MAC address should be rejected
    get_rejected(mac_addr='00:00:00:00:00:02')

    # change class name in subnet and now the first client should not be given a lease
    # as class names do not match
    subnet_cfg.update(backend=backend, client_class='not-modem')
    get_rejected(mac_addr='00:00:00:00:00:01')

    # change class name in subnet to '' ie. reset it, ie. make the subnet open to any client
    # and now unclassified should get a lease
    subnet_cfg.update(backend=backend, client_class='')
    get_address(mac_addr="00:00:00:00:00:03", exp_addr='192.168.50.2' if dhcp_version == 'v4' else '2001:db8:1::2')


@pytest.mark.parametrize("classes_kept_in", ["db", "config"])
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_class_in_network(dhcp_version, classes_kept_in, backend):
    # prepare initial config with 3 class: modem, user, other
    # each class is assigned to 1 client with specified MAC address

    if classes_kept_in == "config":
        if dhcp_version == 'v4':
            init_cfg = {'client-classes': [{
                'name': 'modem',
                'test': "hexstring(pkt4.mac, ':') == '00:00:00:00:00:01'"
            }, {
                'name': 'user',
                'test': "hexstring(pkt4.mac, ':') == '00:00:00:00:00:02'"
            }, {
                'name': 'other',
                'test': "hexstring(pkt4.mac, ':') == '00:00:00:00:00:03'"
            }]}
        else:
            init_cfg = {'client-classes': [{
                'name': 'modem',
                'test': "hexstring(option[1].hex, ':') == '00:03:00:01:00:00:00:00:00:01'"
            }, {
                'name': 'user',
                'test': "hexstring(option[1].hex, ':') == '00:03:00:01:00:00:00:00:00:02'"
            }, {
                'name': 'other',
                'test': "hexstring(option[1].hex, ':') == '00:03:00:01:00:00:00:00:00:03'"
            }]}
    else:
        init_cfg = {}
    cfg = setup_server_for_config_backend_cmds(backend_type=backend, **init_cfg)

    if classes_kept_in == 'db':
        if dhcp_version == 'v4':
            cfg.add_class(backend=backend, name="modem", test="hexstring(pkt4.mac, ':') == '00:00:00:00:00:01'")
            cfg.add_class(backend=backend, name="user", test="hexstring(pkt4.mac, ':') == '00:00:00:00:00:02'")
            cfg.add_class(backend=backend, name="other", test="hexstring(pkt4.mac, ':') == '00:00:00:00:00:03'")
        else:
            cfg.add_class(backend=backend, name="modem",
                          test="hexstring(option[1].hex, ':') == '00:03:00:01:00:00:00:00:00:01'")
            cfg.add_class(backend=backend, name="user",
                          test="hexstring(option[1].hex, ':') == '00:03:00:01:00:00:00:00:00:02'")
            cfg.add_class(backend=backend, name="other",
                          test="hexstring(option[1].hex, ':') == '00:03:00:01:00:00:00:00:00:03'")

    # add 2 subnets

    # subnet 1 is for a modem class
    cfg.add_subnet(backend=backend, client_class='modem')

    # subnet 2 is assigned to shared netwrok which is assigned to user class
    network_cfg, _ = cfg.add_network(backend=backend, name='user-nets',
                                     client_class='user')
    pool = '2.2.2.1-2.2.2.10' if dhcp_version == 'v4' else '2:2:2::1-2:2:2::10'
    cfg.add_subnet(backend=backend, shared_network_name='user-nets',
                   subnet='2.2.2.0/24' if dhcp_version == 'v4' else '2:2:2::/64',
                   pools=[{'pool': pool}])

    # client 1 from 'modem' class should get lease from subnet 1
    get_address(mac_addr="00:00:00:00:00:01", exp_addr='192.168.50.1' if dhcp_version == 'v4' else '2001:db8:1::1')

    # client 2 from 'user' class should get lease from subnet 2
    get_address(mac_addr="00:00:00:00:00:02", exp_addr='2.2.2.1' if dhcp_version == 'v4' else '2:2:2::1')

    # client 3 from 'other' class should be rejected
    get_rejected(mac_addr='00:00:00:00:00:03')

    # change class name in network to 'other' and now client 3 should be given a lease
    network_cfg.update(backend=backend, client_class='other')
    get_address(mac_addr="00:00:00:00:00:03", exp_addr='2.2.2.2' if dhcp_version == 'v4' else '2:2:2::2')

    # change class name in network to '' ie. reset it, ie. make the network open to any client
    # and now unclassified client 4 should be given a lease from subnet 2
    network_cfg.update(backend=backend, client_class='')
    get_address(mac_addr="00:00:00:00:00:04", exp_addr='2.2.2.3' if dhcp_version == 'v4' else '2:2:2::3')


@pytest.mark.parametrize('csv', [False, True])
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
@pytest.mark.parametrize('always_send', [False, True])
def test_class_options(dhcp_version, backend, always_send, csv):
    """
    Test kea ability to send options assigned to class when config kept in database backend
    :param dhcp_version: fixture, string, v4 or v6
    :param backend: string, mysql or postgresql
    :param always_send: boolean, value of always send configuration option
    :param csv: boolean, value of csv configuration option
    """
    cfg = setup_server_for_config_backend_cmds(backend_type=backend)

    if dhcp_version == 'v4':
        cfg.add_class(backend=backend, name="modem", test="hexstring(pkt4.mac, ':') == '00:00:00:00:00:01'",
                      option_data=[{"name": "domain-name-servers",
                                    "code": 6,
                                    "space": "dhcp4",
                                    "csv-format": csv,
                                    "always-send": always_send,
                                    "data": "192.0.2.1" if csv else "C0000201"}])
    else:
        cfg.add_class(backend=backend, name="modem",
                      test="hexstring(option[1].hex, ':') == '00:03:00:01:00:00:00:00:00:01'",
                      option_data=[{"name": "dns-servers",
                                    "code": 23,
                                    "space": "dhcp6",
                                    "csv-format": csv,
                                    "always-send": always_send,
                                    "data": "2001:db8:1::1, 2001:db8:2::1" if csv else
                                    "20010DB800010000000000000000000120010DB8000200000000000000000001"}])

    # subnet for a modem class
    cfg.add_subnet(backend=backend, client_class='modem')

    expected_option = {"code": 6, "data": "192.0.2.1"}
    if dhcp_version == 'v6':
        expected_option = {"code": 23, "data": "2001:db8:1::1,2001:db8:2::1"}

    # client 1 from 'modem' class should get lease
    get_address(mac_addr="00:00:00:00:00:01",
                exp_addr='192.168.50.1' if dhcp_version == 'v4' else '2001:db8:1::1',
                req_opts=[6] if dhcp_version == 'v4' else [23] if not always_send else [],
                exp_option=expected_option)
