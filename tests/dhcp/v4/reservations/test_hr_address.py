# Copyright (C) 2022-2025 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Host Reservation DHCPv4"""

import pytest

from src import srv_control
from src import srv_msg
from src import misc
from src.forge_cfg import world
from src.protosupport.multi_protocol_functions import get_line_count_in_log


@pytest.mark.v4
@pytest.mark.host_reservation
def test_v4_host_reservation_one_address_inside_pool_hw_address():
    misc.test_setup()
    # outside of the pool
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet('ip-address',
                                           '192.168.50.10',
                                           0,
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.host_reservation
def test_v4_host_reservation_one_address_inside_pool_client_id():
    misc.test_setup()
    # outside of the pool
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet('ip-address',
                                           '192.168.50.10',
                                           0,
                                           'client-id',
                                           'ff:01:02:03:ff:04:11:22')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.host_reservation
def test_v4_host_reservation_one_address_outside_pool():
    misc.test_setup()
    # outside of the pool
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.30-192.168.50.50')
    srv_control.host_reservation_in_subnet('ip-address',
                                           '192.168.50.10',
                                           0,
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.host_reservation
def test_v4_host_reservation_one_address_inside_pool_different_mac():
    misc.test_setup()
    # request address from different mac that has been reserved
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet('ip-address',
                                           '192.168.50.10',
                                           0,
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10', expected=False)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'NAK')
    srv_msg.response_check_content('yiaddr', '0.0.0.0')


@pytest.mark.v4
@pytest.mark.host_reservation
def test_v4_host_reservation_one_address_empty_pool():
    misc.test_setup()
    # request address from different mac that has been reserved
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.host_reservation_in_subnet('ip-address',
                                           '192.168.50.10',
                                           0,
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()


@pytest.mark.v4
@pytest.mark.host_reservation
def test_v4_host_reservation_multiple_address_reservation_empty_pool():
    misc.test_setup()
    # request address from different mac that has been reserved
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.host_reservation_in_subnet('ip-address',
                                           '192.168.50.10',
                                           0,
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.host_reservation_in_subnet('ip-address',
                                           '192.168.50.11',
                                           0,
                                           'hw-address',
                                           'ff:01:02:03:ff:03')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()


@pytest.mark.v4
@pytest.mark.host_reservation
def test_v4_host_reservation_multiple_address_reservation_empty_pool_2():
    misc.test_setup()
    # request address from different mac that has been reserved
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.12')
    srv_control.host_reservation_in_subnet('ip-address',
                                           '192.168.50.10',
                                           0,
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    srv_control.host_reservation_in_subnet('ip-address',
                                           '192.168.50.11',
                                           0,
                                           'hw-address',
                                           'ff:01:02:03:ff:03')
    srv_control.host_reservation_in_subnet('ip-address',
                                           '192.168.50.12',
                                           0,
                                           'hw-address',
                                           'ff:01:02:03:ff:02')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:03')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:03')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:02')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:02')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.parametrize('backend', ['configfile', 'MySQL', 'PostgreSQL'])
def test_v4_host_reservation_empty(backend):
    """
    Test if empty (only MAC address) reservation can be made.
    # kea#2878 - "reservation-add" requires "subnet-id" to be provided, which contradicts empty reservations
    :param backend:
    :type backend: str
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')

    if backend == 'configfile':
        world.dhcp_cfg.update({
            "reservations": [
                {
                    "hw-address": "ff:01:02:03:ff:04"
                }
            ],
            "reservations-global": True,
            "reservations-in-subnet": False
        })
    else:
        srv_control.add_hooks('libdhcp_host_cmds.so')
        world.dhcp_cfg.update({
            'reservations-global': True,
            'reservations-in-subnet': False
        })
        srv_control.enable_db_backend_reservation(backend)
        srv_control.add_unix_socket()
        srv_control.add_http_control_channel()

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    if backend != 'configfile':
        response = srv_msg.send_ctrl_cmd({
            "arguments": {
                "reservation": {
                    "hw-address": "ff:01:02:03:ff:04",
                }
            },
            "command": "reservation-add"
        })
        assert response == {
            "result": 0,
            "text": 'Host added. subnet-id not specified, assumed global (subnet-id 0).'
        }

    # Send KNOWN MAC as first transaction
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')

    # first transaction id
    first_xid = hex(world.cfg["values"]["tr_id"])
    # reset transaction id
    world.cfg["values"]["tr_id"] = None

    # Send UNKNOWN MAC as second transaction
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:08')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.2')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.2')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:08')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.2')

    # second transaction id
    second_xid = hex(world.cfg["values"]["tr_id"])

    # Check for 2 received KNOWN and 0 UNKNOWN packets for first transaction
    first_known = get_line_count_in_log(f'tid={first_xid}:'
                                        ' client packet has been assigned to the following class: KNOWN')
    first_unknown = get_line_count_in_log(f'tid={first_xid}:'
                                          ' client packet has been assigned to the following class: UNKNOWN')
    assert first_known == 2, 'Wrong number od KNOWN assignments for KNOWN packet'
    assert first_unknown == 0, 'Wrong number od UNKNOWN assignments for KNOWN packet'

    # Check for 0 received KNOWN and 2 UNKNOWN packets for first transaction
    second_known = get_line_count_in_log(f'tid={second_xid}:'
                                         ' client packet has been assigned to the following class: KNOWN')
    second_unknown = get_line_count_in_log(f'tid={second_xid}:'
                                           ' client packet has been assigned to the following class: UNKNOWN')
    assert second_known == 0, 'Wrong number od KNOWN assignments for UNKNOWN packet'
    assert second_unknown == 2, 'Wrong number od UNKNOWN assignments for UNKNOWN packet'


@pytest.mark.v4
@pytest.mark.host_reservation
def test_v4_host_reservation_example_access_control():
    """
    Test example from ARM "Host Reservations as Basic Access Control".
    """
    misc.test_setup()
    srv_control.config_srv_subnet("192.168.50.0/24", "192.168.50.1-192.168.50.200", id=1)
    world.dhcp_cfg.update(
        {
            "client-classes": [
                {
                    "name": "KNOWN",
                    "option-data": [{"name": "routers", "data": "192.0.2.250"}],
                }
            ]
        }
    )

    world.dhcp_cfg.update(
        {
            "reservations": [
                # Clients on this list will be added to the KNOWN class.
                {"hw-address": "aa:bb:cc:dd:ee:fe"},
                {"hw-address": "11:22:33:44:55:66"},
            ],
            "reservations-global": True,
        }
    )

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Check unknown MAC
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'dd:ee:ff:11:22:33')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(3, expect_include=False)

    # Check first known MAC
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'aa:bb:cc:dd:ee:fe')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'value', '192.0.2.250')

    # Check other known MAC
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '11:22:33:44:55:66')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'value', '192.0.2.250')


@pytest.mark.v4
@pytest.mark.host_reservation
def test_v4_host_reservation_example_access_control_tagging():
    """
    Test extended example from ARM "Host Reservations as Basic Access Control".
    """
    misc.test_setup()
    option_data = [
        {
            # Router for blocked customers.
            "client-classes": ["blocked"],
            "name": "routers",
            "data": "192.0.2.251",
        },
        {
            # Router for customers in good standing.
            "name": "routers",
            "data": "192.0.2.250",
        },
    ]

    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.200', id=1,
                                  option_data=option_data)
    world.dhcp_cfg.update(
        {
            "client-classes": [
                {
                    "name": "blocked",
                }
            ]
        }
    )

    world.dhcp_cfg.update(
        {
            "reservations": [
                {"hw-address": "aa:bb:cc:dd:ee:fe", "client-classes": ["blocked"]},
                {"hw-address": "11:22:33:44:55:66"},
            ],
            "reservations-global": True,
        }
    )
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Check unblocked MAC
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'dd:ee:ff:11:22:33')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'value', '192.0.2.250')

    # Check blocked MAC
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'aa:bb:cc:dd:ee:fe')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'value', '192.0.2.251')

    # Check other known MAC
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '11:22:33:44:55:66')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'value', '192.0.2.250')
