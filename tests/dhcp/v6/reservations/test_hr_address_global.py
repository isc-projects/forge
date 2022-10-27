# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Host Reservation DHCPv6"""

import pytest

from src import srv_control
from src import srv_msg
from src import misc

from src.forge_cfg import world


def _send_solicit(duid, address):
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', address)


def _send_request(duid, address):
    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', address)


def _get_an_address(duid, address):
    _send_solicit(duid, address)
    _send_request(duid, address)


@pytest.mark.v6
@pytest.mark.host_reservation
def test_v6_subnet_selection_based_on_global_reservation_of_class():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::10')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::10')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:c::/64',
                                                       '2001:db8:c::1-2001:db8:c::10')
    world.dhcp_cfg["subnet6"][0]["client-class"] = "NOTspecial"
    world.dhcp_cfg["subnet6"][1]["client-class"] = "special"
    world.dhcp_cfg["subnet6"][2]["client-class"] = "special2"

    world.dhcp_cfg.update({
        "reservations": [
            {
                "client-classes": [
                    "special"
                ],
                "hw-address": "01:02:03:04:05:07"
            },
            {
                "client-classes": [
                    "special2"
                ],
                "hw-address": "01:02:03:04:05:08"
            }
        ], "client-classes": [
            {
                "name": "special"
            },
            {
                "name": "special2"
            },
            {
                "name": "NOTspecial",
                "test": "not member('special') and not member('special2')"
            }
        ], "reservation-mode": "global"})

    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.shared_subnet('2001:db8:b::/64', 0)
    srv_control.shared_subnet('2001:db8:c::/64', 0)

    srv_control.set_conf_parameter_shared_subnet('name', 'name-abc', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '$(SERVER_IFACE)', 0)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # not special
    # _send_solicit('00:03:00:01:01:02:03:04:05:08', '2001:db8:a::1')
    # special
    _get_an_address('00:03:00:01:01:02:03:04:05:07', '2001:db8:b::1')
    _get_an_address('00:03:00:01:01:02:03:04:05:08', '2001:db8:c::1')
    # not special
    _send_solicit('00:03:00:01:01:02:03:04:05:09', '2001:db8:a::1')

#
# @pytest.mark.v6
# @pytest.mark.host_reservation
# def test_v6_pool_selection_based_on_global_reservation_of_class():
#     misc.test_setup()
#     # pool selection based on global reservation with class
#     # address assigned based on reservation on subnet level
#     srv_control.config_srv_subnet('2001:db8:1::/64', "2001:db8:1::1-2001:db8:1::1")
#     srv_control.new_pool('2001:db8:1::5-2001:db8:1::5', 0)
#     world.dhcp_cfg.update({
#         "reservations": [
#             {
#                 "client-classes": [
#                     "special"
#                 ],
#                 "hw-address": "01:02:03:04:05:07"
#             }
#         ], "client-classes": [
#             {
#                 "name": "special"
#             },
#             {
#                 "name": "NOTspecial",
#                 "test": "not member('special')"
#             }
#
#         ], "reservation-mode": "global"})
#
#     world.dhcp_cfg["subnet6"][0]["pools"][0]["client-class"] = "NOTspecial"
#     world.dhcp_cfg["subnet6"][0]["pools"][1]["client-class"] = "special"
#
#     srv_control.build_and_send_config_files()
#     srv_control.start_srv('DHCP', 'started')
#
#     # not special
#     _send_solicit('00:03:00:01:01:02:03:04:05:08', '2001:db8:1::1')
#     # special
#     _get_an_address('00:03:00:01:01:02:03:04:05:07', '2001:db8:1::5')
#     # not special
#     _send_solicit('00:03:00:01:01:02:03:04:05:09', '2001:db8:1::1')

#
# @pytest.mark.v6
# @pytest.mark.host_reservation
# def test_v6_subnet_selection_based_on_global_reservation_of_class_additional_address_reservation():
#     misc.test_setup()
#     srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
#     srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
#                                                        '2001:db8:b::1-2001:db8:b::1')
#
#     world.dhcp_cfg["subnet6"][0]["client-class"] = "NOTspecial"
#     world.dhcp_cfg["subnet6"][1]["client-class"] = "special"
#
#     world.dhcp_cfg.update({
#         "reservations": [
#             {
#                 "client-classes": [
#                     "special"
#                 ],
#                 "hw-address": "01:02:03:04:05:07"
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
#     world.dhcp_cfg["subnet6"][1].update({"reservations": [
#         {
#             "ip-addresses": ["2001:db8:b::1111"],
#             "hw-address": "01:02:03:04:05:07"
#         }
#     ], "reservation-mode": "all"})
#
#     srv_control.shared_subnet('2001:db8:a::/64', 0)
#     srv_control.shared_subnet('2001:db8:b::/64', 0)
#
#     srv_control.set_conf_parameter_shared_subnet('name', 'name-abc', 0)
#     srv_control.set_conf_parameter_shared_subnet('interface', '$(SERVER_IFACE)', 0)
#
#     srv_control.build_and_send_config_files()
#     srv_control.start_srv('DHCP', 'started')
#
#     # not special
#     _send_solicit('00:03:00:01:01:02:03:04:05:08', '2001:db8:a::1')
#     # special
#     _get_an_address('00:03:00:01:01:02:03:04:05:07', "2001:db8:b::1111")
#     # not special
#     _send_solicit('00:03:00:01:01:02:03:04:05:09', '2001:db8:a::1')
#

# @pytest.mark.v6
# @pytest.mark.host_reservation
# def test_v6_pool_selection_based_on_global_reservation_of_class_additional_address_reservation():
#     misc.test_setup()
#     # pool selection based on global reservation with class
#     # address assigned based on reservation on subnet level
#     srv_control.config_srv_subnet('2001:db8:1::/64', "2001:db8:1::1-2001:db8:1::1")
#     srv_control.new_pool('2001:db8:1::5-2001:db8:1::5', 0)
#     world.dhcp_cfg.update({
#         "reservations": [
#             {
#                 "client-classes": [
#                     "special"
#                 ],
#                 "hw-address": "01:02:03:04:05:07"
#             }
#         ], "client-classes": [
#             {
#                 "name": "special"
#             },
#             {
#                 "name": "NOTspecial",
#                 "test": "not member('special')"
#             }
#
#         ], "reservation-mode": "global"})
#
#     world.dhcp_cfg["subnet6"][0]["pools"][0]["client-class"] = "NOTspecial"
#     world.dhcp_cfg["subnet6"][0]["pools"][1]["client-class"] = "special"
#
#     world.dhcp_cfg["subnet6"][0].update({"reservations": [
#         {
#             "ip-addresses": ["2001:db8:1::100"],
#             "hw-address": "01:02:03:04:05:07"
#         }
#     ], "reservation-mode": "all"})
#
#     srv_control.build_and_send_config_files()
#     srv_control.start_srv('DHCP', 'started')
#
#     # not special
#     # _send_solicit('00:03:00:01:01:02:03:04:05:08', '2001:db8:1::1')
#     # special
#     _get_an_address('00:03:00:01:01:02:03:04:05:07', "2001:db8:1::100")
#     # not special
#     _send_solicit('00:03:00:01:01:02:03:04:05:09', '2001:db8:1::1')
