import pytest

from cb_model import setup_server_with_radius
from dhcp4_scen import get_address, send_discover_with_no_answer
from softwaresupport import radius


@pytest.mark.v4
@pytest.mark.radius
@pytest.mark.parametrize("scope", ['subnet', 'network'])
def test_static_out_of_pool(scope):
    # select IP returned from RADIUS that is NOT within defined subnet in Kea
    radius.init_and_start_radius()

    subnets = [{
        "subnet": "192.168.50.0/24",
        "interface": "$(SERVER_IFACE)",
        "pools": [{
            # gold
            "pool": "192.168.50.5 - 192.168.50.5",
            "client-class": "gold"
        }]
    }]

    if scope == 'network':
        cfg = {
            "reservation-mode": 'global',
            "shared-networks": [{
                "name": "net-1",
                "subnet4": subnets}]}
    else:
        cfg = {"subnet4": subnets}
    setup_server_with_radius(**cfg)

    # get arbitrary address from radius
    get_address(chaddr="08:00:27:b0:c1:42", client_id="11080027b0c142", exp_yiaddr="192.168.52.52")

    # 192.168.50.5 from gold class should be available for dynamic client
    get_address(chaddr="08:00:27:b0:c5:01", client_id="11080027b0c501", exp_yiaddr="192.168.50.5")


@pytest.mark.v4
@pytest.mark.radius
@pytest.mark.parametrize("scope", ['subnet', 'network'])
def test_static_in_pool(scope):
    # select IP returned from RADIUS that is within defined subnet in Kea
    radius.init_and_start_radius()

    subnets = [{
        "subnet": "192.168.50.0/24",
        "interface": "$(SERVER_IFACE)",
        "pools": [{
            # gold
            "pool": "192.168.50.5 - 192.168.50.5",
            "client-class": "gold"
        }]
    }]

    if scope == 'network':
        cfg = {
            "reservation-mode": 'global',
            "shared-networks": [{
                "name": "net-1",
                "subnet4": subnets}]}
    else:
        cfg = {"subnet4": subnets}
    setup_server_with_radius(**cfg)

    # get arbitrary address from radius but from within pool
    get_address(chaddr="08:00:27:b0:c5:10", client_id="11080027b0c510", exp_yiaddr="192.168.50.5")

    # 192.168.50.5 from gold class should NOT be available for dynamic client
    send_discover_with_no_answer(chaddr="08:00:27:b0:c5:01", client_id="11080027b0c501")


@pytest.mark.v4
@pytest.mark.radius
def test_class_and_subnet_assign_complex():
    # select IP from subnets based on classes indicated in pools
    # ref: https://gitlab.isc.org/isc-private/qa-dhcp/issues/151
    radius.init_and_start_radius()

    setup_server_with_radius(
        reservation_mode='global',
        shared_networks=[{
            "name": "net-1",
            "subnet4": [{
                "subnet": "192.168.50.0/24",
                "interface": "$(SERVER_IFACE)",
                "pools": [{
                    # gold
                    "pool": "192.168.50.5 - 192.168.50.5",
                    "client-class": "gold"
                }, {
                    # silver
                    "pool": "192.168.50.6 - 192.168.50.6",
                    "client-class": "silver"
                }, {
                    # bronze
                    "pool": "192.168.50.7 - 192.168.50.7",
                    "client-class": "bronze"
                }]
            }, {
                "subnet": "192.168.60.0/24",
                "interface": "$(SERVER_IFACE)",
                "pools": [{
                    # gold
                    "pool": "192.168.60.5 - 192.168.60.5",
                    "client-class": "gold"
                }, {
                    # silver
                    "pool": "192.168.60.6 - 192.168.60.6",
                    "client-class": "silver"
                }]
            }]
        }])

    gold_ips = set(['192.168.50.5', '192.168.60.5'])
    silver_ips = set(['192.168.50.6', '192.168.60.6'])

    # get arbitrary address from radius
    get_address(chaddr="08:00:27:b0:c1:42", client_id="11080027b0c142", exp_yiaddr="192.168.52.52")

    # === take all addresses from gold pools ===
    # get first gold IP
    yiaddr = get_address(chaddr="08:00:27:b0:c5:01", client_id="11080027b0c501")
    assert yiaddr in gold_ips
    gold_ips.remove(yiaddr)

    # get second and last gold IP
    yiaddr = get_address(chaddr="08:00:27:b0:c5:02", client_id="11080027b0c502")
    assert yiaddr in gold_ips
    gold_ips.remove(yiaddr)

    # no more IPs available
    send_discover_with_no_answer(chaddr="08:00:27:b0:c5:03", client_id="11080027b0c503")

    # === take all addresses from silver pools ===
    # get first silver IP
    yiaddr = get_address(chaddr="08:00:27:b0:c6:01", client_id="11080027b0c601")
    assert yiaddr in silver_ips
    silver_ips.remove(yiaddr)

    # get second and last silver IP
    yiaddr = get_address(chaddr="08:00:27:b0:c6:02", client_id="11080027b0c602")
    assert yiaddr in silver_ips
    silver_ips.remove(yiaddr)

    # no more IPs available
    send_discover_with_no_answer(chaddr="08:00:27:b0:c6:03", client_id="11080027b0c603")

    # === take all addresses from bronze pools ===
    # get first and only bronze IP
    get_address(chaddr="08:00:27:b0:c7:01", client_id="11080027b0c701", exp_yiaddr="192.168.50.7")
    # no more IPs available
    send_discover_with_no_answer(chaddr="08:00:27:b0:c7:02", client_id="11080027b0c702")


@pytest.mark.v4
@pytest.mark.radius
def test_select_from_radius_and_ignore_complex_subnets_with_classes():
    # select IP returned by RADIUS and do not use any of defined subnets
    radius.init_and_start_radius()

    setup_server_with_radius(
        reservation_mode='global',
        shared_networks=[{
            "name": "net-1",
            "subnet4": [{
                "subnet": "192.168.50.0/24",
                "interface": "$(SERVER_IFACE)",
                "pools": [{
                    # gold
                    "pool": "192.168.50.5 - 192.168.50.5",
                    "client-class": "gold"
                }]
            }, {
                "subnet": "192.168.60.0/24",
                "interface": "$(SERVER_IFACE)",
                "pools": [{
                    # silver
                    "pool": "192.168.60.6 - 192.168.60.6",
                    "client-class": "silver"
                }]
            }, {
                "subnet": "192.168.70.0/24",
                "interface": "$(SERVER_IFACE)",
                "client-class": "platinum",  # platinum
                "pools": [{
                    "pool": "192.168.70.5 - 192.168.70.5"
                }]
            }]
        }])

    # get arbitrary address from radius
    get_address(chaddr="08:00:27:b0:c1:42", client_id="11080027b0c142", exp_yiaddr="192.168.52.52")


@pytest.mark.v4
@pytest.mark.radius
def test_select_by_class_in_subnet():
    # select IP from subnet based on class indicated in subnet, not in pool
    radius.init_and_start_radius()

    setup_server_with_radius(
        reservation_mode='global',
        shared_networks=[{
            "name": "net-1",
            "subnet4": [{
                "subnet": "192.168.50.0/24",
                "interface": "$(SERVER_IFACE)",
                "pools": [{
                    # gold
                    "pool": "192.168.50.5 - 192.168.50.5",
                    "client-class": "gold"
                }]
            }, {
                "subnet": "192.168.60.0/24",
                "interface": "$(SERVER_IFACE)",
                "pools": [{
                    # silver
                    "pool": "192.168.60.6 - 192.168.60.6",
                    "client-class": "silver"
                }]
            }, {
                "subnet": "192.168.70.0/24",
                "interface": "$(SERVER_IFACE)",
                "client-class": "platinum",  # platinum
                "pools": [{
                    "pool": "192.168.70.5 - 192.168.70.5"
                }]
            }]
        }])

    # get arbitrary address from radius
    get_address(chaddr="08:00:27:b0:c8:01", client_id="11080027b0c801", exp_yiaddr="192.168.70.5")
