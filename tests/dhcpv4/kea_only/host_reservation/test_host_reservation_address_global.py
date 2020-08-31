"""Host Reservation DHCPv4"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_control
import srv_msg
import misc

from forge_cfg import world


def _send_offer(mac, address):
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', mac)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', address)


def _send_request(mac, address):
    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', mac)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', address)


def _get_an_address(mac, address):
    _send_offer(mac, address)
    _send_request(mac, address)


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_subnet_selection_based_on_global_reservation_of_class():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.50-192.168.51.50')

    world.dhcp_cfg["subnet4"][0]["client-class"] = "NOTspecial"
    world.dhcp_cfg["subnet4"][1]["client-class"] = "special"

    world.dhcp_cfg.update({
        "reservations": [
            {
                "client-classes": [
                    "special"
                ],
                "hw-address": "ff:01:02:03:ff:04"
            }
        ], "client-classes": [
            {
                "name": "special"
            },
            {
                "name": "NOTspecial",
                "test": "not member('special')"
            }
        ], "reservation-mode": "global"})

    srv_control.shared_subnet('192.168.50.0/24', 0)
    srv_control.shared_subnet('192.168.51.0/24', 0)

    srv_control.set_conf_parameter_shared_subnet('name', 'name-abc', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '$(SERVER_IFACE)', 0)

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    # get offer from NOTspecial
    _send_offer('ff:01:02:03:ff:01', '192.168.50.50')
    # get address from special
    _get_an_address('ff:01:02:03:ff:04', '192.168.51.50')
    # get offer from NOTspecial
    _send_offer('ff:01:02:03:ff:02', '192.168.50.50')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_pool_selection_based_on_global_reservation_of_class():
    misc.test_setup()
    # pool selection based on global reservation with class
    # address assigned based on reservation on subnet level
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.new_pool('192.168.50.150-192.168.50.150', 0)
    world.dhcp_cfg.update({
        "reservations": [
            {
                "client-classes": [
                    "special"
                ],
                "hw-address": "ff:01:02:03:ff:04"
            }
        ], "client-classes": [
            {
                "name": "special"
            },
            {
                "name": "NOTspecial",
                "test": "not member('special')"
            }
        ], "reservation-mode": "global"})

    world.dhcp_cfg["subnet4"][0]["pools"][0]["client-class"] = "NOTspecial"
    world.dhcp_cfg["subnet4"][0]["pools"][1]["client-class"] = "special"

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    # get offer from NOTspecial
    _send_offer('ff:01:02:03:ff:01', '192.168.50.1')
    # get address from special
    _get_an_address('ff:01:02:03:ff:04', '192.168.50.150')
    # get offer from NOTspecial
    _send_offer('ff:01:02:03:ff:02', '192.168.50.1')

#
# @pytest.mark.v4
# @pytest.mark.host_reservation
# @pytest.mark.kea_only
# def test_v4_subnet_selection_based_on_global_reservation_of_class_additional_address_reservation():
#     misc.test_setup()
#     srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
#     srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
#                                                        '192.168.51.1-192.168.51.50')
#
#     world.dhcp_cfg["subnet4"][0]["client-class"] = "NOTspecial"
#     world.dhcp_cfg["subnet4"][1]["client-class"] = "special"
#
#     world.dhcp_cfg.update({
#         "reservations": [
#             {
#                 "client-classes": [
#                     "special"
#                 ],
#                 "hw-address": "ff:01:02:03:ff:04"
#             }
#         ], "client-classes": [
#             {
#                 "name": "special"
#             },
#             {
#                 "name": "NOTspecial",
#                 "test": "not member('special')"
#             }
#         ], "reservation-mode": "global"})
#
#     world.dhcp_cfg["subnet4"][1].update({"reservations": [
#         {
#             "ip-address": "192.168.51.200",
#             "hw-address": "ff:01:02:03:ff:04"}
#     ], "reservation-mode": "all"})
#
#     srv_control.shared_subnet('192.168.50.0/24', 0)
#     srv_control.shared_subnet('192.168.51.0/24', 0)
#
#     srv_control.set_conf_parameter_shared_subnet('name', 'name-abc', 0)
#     srv_control.set_conf_parameter_shared_subnet('interface', '$(SERVER_IFACE)', 0)
#
#     srv_control.build_and_send_config_files('SSH', 'config-file')
#     srv_control.start_srv('DHCP', 'started')
#
#     # get offer from NOTspecial
#     _send_offer('ff:01:02:03:ff:01', '192.168.50.1')
#     # get address from special with reservation from subnet
#     _get_an_address('ff:01:02:03:ff:04', '192.168.50.200')
#     # get offer from NOTspecial
#     _send_offer('ff:01:02:03:ff:02', '192.168.50.1')
