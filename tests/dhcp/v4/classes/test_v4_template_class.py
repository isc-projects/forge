# Copyright (C) 2023 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""DHCPv4 Client Classification - template classes"""

# pylint: disable=line-too-long

import pytest

from src import misc
from src import srv_control
from src import srv_msg

from src.forge_cfg import world
from src.protosupport.multi_protocol_functions import get_line_count_in_log, log_doesnt_contain


def _get_lease(mac: str, cli_id: str = None, addr: str = None, vendor: str = False, drop: bool = False):
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', mac)
    if cli_id:
        srv_msg.client_does_include_with_value('client_id', cli_id)
    if vendor:
        srv_msg.client_does_include_with_value('vendor_specific_information', vendor)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    if drop:
        srv_msg.send_dont_wait_for_message()
        return
    msg = srv_msg.send_wait_for_message('MUST', 'OFFER')[0]

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', msg.yiaddr)
    srv_msg.client_sets_value('Client', 'chaddr', mac)
    if cli_id:
        srv_msg.client_does_include_with_value('client_id', cli_id)
    if vendor:
        srv_msg.client_does_include_with_value('vendor_specific_information', vendor)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', addr if addr else msg.yiaddr)

    my_lease = srv_msg.get_all_leases()
    srv_msg.check_leases(my_lease)


@pytest.mark.v4
@pytest.mark.classification
def test_v4_spawn_class():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.15')

    classes = [
            {
                # SPAWN_my_vendor_client_id_<last 3 octets of client id>
                "name": "my_vendor_client_id",
                "template-test": "hexstring(substring(option[61].hex, 3, 3), ':')"
            },
            {
                # SPAWN_my_vendor_mac_addr_<first 3 octets of mac address>
                "name": "my_vendor_mac_addr",
                "template-test": "hexstring(substring(pkt4.mac, 0, 3), ':')"
            }
        ]

    world.dhcp_cfg["client-classes"] = classes
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # get address and check logs
    mac = 'ff:01:02:03:ff:04'
    cli_id = 'ff:11:22:33:44:55'
    _get_lease(mac, cli_id)
    assert 2 == get_line_count_in_log(f'client packet belongs to an unconfigured'
                                      f' class: SPAWN_my_vendor_client_id_{cli_id[9:]}')
    assert 2 == get_line_count_in_log(f'client packet belongs to an unconfigured'
                                      f' class: SPAWN_my_vendor_mac_addr_{mac[:8]}')

    new_mac = '11:22:33:03:ff:04'
    new_cli_id = 'ff:11:22:77:99:00:aa:bb'
    _get_lease(new_mac, new_cli_id)
    assert 2 == get_line_count_in_log(f'client packet belongs to an unconfigured'
                                      f' class: SPAWN_my_vendor_client_id_{new_cli_id[9:16]}')
    assert 2 == get_line_count_in_log(f'client packet belongs to an unconfigured'
                                      f' class: SPAWN_my_vendor_mac_addr_{new_mac[:8]}')

    # and recheck first logs if by new packages were not added to previous classes
    assert 2 == get_line_count_in_log(f'client packet belongs to an unconfigured'
                                      f' class: SPAWN_my_vendor_client_id_{cli_id[9:]}')
    assert 2 == get_line_count_in_log(f'client packet belongs to an unconfigured'
                                      f' class: SPAWN_my_vendor_mac_addr_{mac[:8]}')

    # another client without client id, mac fits to the class created for new_mac
    additional_mac = '11:22:33:99:99:01'
    _get_lease(additional_mac)
    assert 2 == get_line_count_in_log(f'client packet belongs to an unconfigured'
                                      f' class: SPAWN_my_vendor_client_id_{cli_id[9:]}')
    assert 4 == get_line_count_in_log(f'client packet belongs to an unconfigured'
                                      f' class: SPAWN_my_vendor_mac_addr_{additional_mac[:8]}')


@pytest.mark.v4
@pytest.mark.classification
def test_v4_spawn_class_2():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.15')

    classes = [
            {
                # SPAWN_my_vendor_client_id_<2 octets, starting from 8th) in test there will be shorter client id!
                "name": "my_vendor_client_id",
                "template-test": "hexstring(substring(option[61].hex, 8, 2), ':')"
            }
        ]

    world.dhcp_cfg["client-classes"] = classes
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # get address and check logs
    mac = 'ff:01:02:03:ff:04'
    cli_id = 'ff:11:22:33:44:55'
    _get_lease(mac, cli_id)
    log_doesnt_contain('client packet belongs to an unconfigured class: SPAWN_my_vendor_client_id_')
    assert 2 == get_line_count_in_log('packet has been assigned to the following class(es): ALL, UNKNOWN')

    new_mac = '11:22:33:03:ff:04'
    new_cli_id = '11:22:33:44:55:66:77:88:99:00:aa:bb'
    _get_lease(new_mac, new_cli_id)
    # for old pkt:
    assert 2 == get_line_count_in_log('packet has been assigned to the following class(es): ALL, UNKNOWN')
    # new pkts:
    assert 2 == get_line_count_in_log(f'client packet belongs to an unconfigured class:'
                                      f' SPAWN_my_vendor_client_id_{new_cli_id[24:29]}')
    assert 2 == get_line_count_in_log(f'client packet has been assigned to the following class(es): ALL, my_vendor_client_id, SPAWN_my_vendor_client_id_{new_cli_id[24:29]}, UNKNOWN')


@pytest.mark.v4
@pytest.mark.classification
def test_v4_spawn_class_as_subnet_guard():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.15')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24', '192.168.51.10-192.168.51.15')

    classes = [
        {
            # SPAWN_my_vendor_mac_addr_<first 3 octets of mac address>
            "name": "vendors",
            "template-test": "hexstring(substring(pkt4.mac, 0, 3), ':')"
        },
        {
            "name": "SPAWN_vendors_aa:bb:cc",
            "option-data": [
                {
                    "data": "172.17.0.1",
                    "name": "routers",
                    "always-send": True
                }

            ]
        },
        {
            "name": "SPAWN_vendors_11:22:33",
        },
        {
            "name": "DROP",
            "test": "member('SPAWN_vendors_11:22:33')"
        }
    ]

    srv_control.config_client_classification(0, 'SPAWN_vendors_aa:bb:cc')
    world.dhcp_cfg["client-classes"] = classes
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # should get 192.168.50.10 and option routers
    _get_lease("AA:BB:CC:11:22:33", addr="192.168.50.10")
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'value', "172.17.0.1")

    # should get dropped
    _get_lease("11:22:33:AA:BB:CC", drop=True)

    # should get 192.168.51.10 and no option
    _get_lease("11:BB:CC:11:22:33", addr="192.168.51.10")
    srv_msg.response_check_include_option(3, expect_include=False)


@pytest.mark.v4
@pytest.mark.classification
def test_v4_template_class_as_subnet_guard():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.15')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24', '192.168.51.10-192.168.51.15')
    srv_control.config_srv_another_subnet_no_interface('192.168.52.0/24', '192.168.52.10-192.168.52.15')

    classes = [
        {
            # SPAWN_mac_vendor_<first 3 octets of mac address>
            "name": "mac_vendor",
            "template-test": "hexstring(substring(pkt4.mac, 0, 3), ':')"
        },
        {
            # SPAWN_client_vendor_<enterprise number>
            "name": "client_vendor",
            "template-test": "int32totext(vendor.enterprise)"
        },
        {
            "name": "SPAWN_mac_vendor_11:22:33",
        },
        {
            "name": "DROP",
            "test": "member('SPAWN_mac_vendor_11:22:33') and member('client_vendor')"
        }
    ]

    srv_control.config_client_classification(0, 'SPAWN_client_vendor_800')
    srv_control.config_client_classification(1, 'client_vendor')
    srv_control.config_client_classification(2, 'mac_vendor')
    world.dhcp_cfg["client-classes"] = classes
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # first let's assign address from last subnet (client id type a1:a2:a3 no vendor)
    _get_lease('a1:a2:a3:ff:ff:01', addr='192.168.52.10')

    # than let's assign address from second subnet (client id type a1:a2:a3 and vendor 4660)
    _get_lease('00:03:00:01:a1:a2:a3:ff:ff:11', vendor='00001234', addr='192.168.51.10')

    # # let's drop pkt (client id type 11:22:33 and vendor 4660)
    _get_lease('11:22:33:ff:ff:11', vendor='00001234', drop=True)

    # at the end let's assign some addresses from subnet 1 (vendor 1234 required)
    _get_lease('a1:a2:a3:ff:22:11', vendor='00000320', addr='192.168.50.10')
    _get_lease('11:aa:33:ff:ff:11', vendor='00000320', addr='192.168.50.11')
