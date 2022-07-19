# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Marcin Godzina

"""Host Reservation DHCPv4"""

# pylint: disable=invalid-name,line-too-long

import copy
import pytest

from src import srv_control
from src import srv_msg
from src import misc
from src.forge_cfg import world


@pytest.mark.v4
@pytest.mark.host_reservation
def test_host():
    misc.test_setup()

    subnets = [
        {
            'id': 1,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '192.168.50.1-192.168.50.50'
                }
            ],
            'subnet': '192.168.50.0/24'
        },
        {
            'id': 2,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '192.168.51.1-192.168.51.50'
                }
            ],
            'subnet': '192.168.51.0/24'
        }
    ]

    reservations = [
        {
            'ip-address': '192.168.50.10',
            'hw-address': 'ff:01:02:03:ff:04'
        }

    ]
    world.dhcp_cfg['early-global-reservations-lookup'] = True
    world.dhcp_cfg.update({'subnet4': copy.deepcopy(subnets)})
    world.dhcp_cfg.update({'reservations': copy.deepcopy(reservations)})

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