# Copyright (C) 2022-2023 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea v4 Statistics"""

# pylint: disable=invalid-name
# pylint: disable=line-too-long

import pytest

from src import misc
from src import srv_control
from src import srv_msg
from src.forge_cfg import world


class StatsState4:
    def __init__(self):
        self.s = {
            'cumulative-assigned-addresses': 0,
            'declined-addresses': 0,
            'pkt4-ack-received': 0,
            'pkt4-ack-sent': 0,
            'pkt4-decline-received': 0,
            'pkt4-discover-received': 0,
            'pkt4-inform-received': 0,
            'pkt4-nak-received': 0,
            'pkt4-nak-sent': 0,
            'pkt4-offer-received': 0,
            'pkt4-offer-sent': 0,
            'pkt4-parse-failed': 0,
            'pkt4-receive-drop': 0,
            'pkt4-received': 0,
            'pkt4-release-received': 0,
            'pkt4-request-received': 0,
            'pkt4-sent': 0,
            'pkt4-unknown-received': 0,
            'reclaimed-declined-addresses': 0,
            'reclaimed-leases': 0,
            'subnet[1].assigned-addresses': 0,
            'subnet[1].cumulative-assigned-addresses': 0,
            'subnet[1].declined-addresses': 0,
            'subnet[1].reclaimed-declined-addresses': 0,
            'subnet[1].reclaimed-leases': 0,
            'subnet[1].total-addresses': 0,
            'subnet[1].v4-lease-reuses': 0,
            'subnet[1].v4-reservation-conflicts': 0,
            'subnet[1].pool[0].assigned-addresses': 0,
            'subnet[1].pool[0].cumulative-assigned-addresses': 0,
            'subnet[1].pool[0].declined-addresses': 0,
            'subnet[1].pool[0].reclaimed-declined-addresses': 0,
            'subnet[1].pool[0].reclaimed-leases': 0,
            'subnet[1].pool[0].total-addresses': 0,
            'v4-allocation-fail': 0,
            'v4-allocation-fail-classes': 0,
            'v4-allocation-fail-no-pools': 0,
            'v4-allocation-fail-shared-network': 0,
            'v4-allocation-fail-subnet': 0,
            'v4-lease-reuses': 0,
            'v4-reservation-conflicts': 0,
        }

    def compare(self):
        result = srv_msg.send_ctrl_cmd_via_socket('{"command":"statistic-get-all","arguments":{}}')
        statistics_from_kea = result['arguments']

        statistics_not_found = []
        for key, _ in self.s.items():
            if key not in statistics_from_kea:
                statistics_not_found.append(key)
        assert len(statistics_not_found) == 0, f'The following statistics were expected, but not received: {statistics_not_found}'

        statistics_not_found = []
        for key in statistics_from_kea:
            if key not in self.s:
                statistics_not_found.append(key)
        assert len(statistics_not_found) == 0, f'The following statistics were received, but not expected: {statistics_not_found}'

        assert len(statistics_from_kea) == 41, 'Number of all statistics is incorrect.'

        for key, expected in self.s.items():
            received = statistics_from_kea[key][0][0]
            assert expected == received, f'stat {key}: expected {expected}, received {received}'


def get_stat(name):
    cmd = {"command": "statistic-get", "arguments": {"name": name}}
    result = srv_msg.send_ctrl_cmd_via_socket(cmd)
    result = [r[0] for r in result['arguments'][name]]
    return result


@pytest.mark.v4
def test_stats_basic():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.disable_leases_affinity()
    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    stats = StatsState4()
    stats.s['subnet[1].total-addresses'] = 10
    stats.s['subnet[1].pool[0].total-addresses'] = 10
    stats.compare()

    misc.test_procedure()

    result = srv_msg.send_ctrl_cmd_via_socket('{"command": "list-commands","arguments": {}}')
    stat_cmds = ['statistic-get',
                 'statistic-get-all',
                 'statistic-remove',
                 'statistic-remove-all',
                 'statistic-reset',
                 'statistic-reset-all',
                 'statistic-sample-age-set',
                 'statistic-sample-age-set-all',
                 'statistic-sample-count-set',
                 'statistic-sample-count-set-all']
    for c in stat_cmds:
        assert c in result['arguments'], f"{c} not found in returned list of available commands"

    cnt = 0
    for c in result['arguments']:
        if c.startswith('statistic-'):
            cnt += 1
    assert len(stat_cmds) == cnt, "Number of returned statistic-* commands in list of available commands is incorrect!"

    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', "ff:01:02:03:ff:04")
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    stats.s['pkt4-offer-sent'] += 1
    stats.s['pkt4-sent'] += 1
    stats.s['pkt4-received'] += 1
    stats.s['pkt4-discover-received'] += 1
    stats.compare()

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', "ff:01:02:03:ff:04")
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    stats.s['cumulative-assigned-addresses'] += 1
    stats.s['pkt4-ack-sent'] += 1
    stats.s['pkt4-sent'] += 1
    stats.s['pkt4-received'] += 1
    stats.s['pkt4-request-received'] += 1
    stats.s['subnet[1].assigned-addresses'] += 1
    stats.s['subnet[1].cumulative-assigned-addresses'] += 1
    stats.s['subnet[1].pool[0].assigned-addresses'] += 1
    stats.s['subnet[1].pool[0].cumulative-assigned-addresses'] += 1
    stats.compare()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', "ff:01:02:03:ff:04")
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()
    stats.s['pkt4-release-received'] += 1
    stats.s['pkt4-received'] += 1
    stats.s['subnet[1].assigned-addresses'] -= 1
    stats.s['subnet[1].pool[0].assigned-addresses'] -= 1
    stats.compare()

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', "ff:01:02:03:ff:04")
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    stats.s['pkt4-offer-sent'] += 1
    stats.s['pkt4-sent'] += 1
    stats.s['pkt4-received'] += 1
    stats.s['pkt4-discover-received'] += 1
    stats.compare()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', "ff:01:02:03:ff:04")
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    stats.s['cumulative-assigned-addresses'] += 1
    stats.s['pkt4-ack-sent'] += 1
    stats.s['pkt4-sent'] += 1
    stats.s['pkt4-received'] += 1
    stats.s['pkt4-request-received'] += 1
    stats.s['subnet[1].assigned-addresses'] += 1
    stats.s['subnet[1].cumulative-assigned-addresses'] += 1
    stats.s['subnet[1].pool[0].assigned-addresses'] += 1
    stats.s['subnet[1].pool[0].cumulative-assigned-addresses'] += 1
    stats.compare()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', "ff:01:02:03:ff:04")
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()
    stats.s['pkt4-release-received'] += 1
    stats.s['pkt4-received'] += 1
    stats.s['subnet[1].assigned-addresses'] -= 1
    stats.s['subnet[1].pool[0].assigned-addresses'] -= 1
    stats.compare()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', "ff:01:02:03:ff:04")
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    stats.s['pkt4-offer-sent'] += 1
    stats.s['pkt4-sent'] += 1
    stats.s['pkt4-received'] += 1
    stats.s['pkt4-discover-received'] += 1
    stats.compare()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', "ff:01:02:03:ff:04")
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    stats.s['cumulative-assigned-addresses'] += 1
    stats.s['pkt4-ack-sent'] += 1
    stats.s['pkt4-sent'] += 1
    stats.s['pkt4-received'] += 1
    stats.s['pkt4-request-received'] += 1
    stats.s['subnet[1].assigned-addresses'] += 1
    stats.s['subnet[1].cumulative-assigned-addresses'] += 1
    stats.s['subnet[1].pool[0].assigned-addresses'] += 1
    stats.s['subnet[1].pool[0].cumulative-assigned-addresses'] += 1
    stats.compare()

    new_hr = {
        "arguments": {
            "reservation": {
                "hw-address": "11:11:11:11:11:11",
                "ip-address": "192.168.50.1",
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }
    result = srv_msg.send_ctrl_cmd_via_socket(new_hr)

    # let's try to get new reservation
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', "11:11:11:11:11:11")
    srv_msg.client_send_msg('DISCOVER')

    # it should not get reserved address
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.2')
    stats.s['pkt4-offer-sent'] += 1
    stats.s['pkt4-sent'] += 1
    stats.s['pkt4-received'] += 1
    stats.s['pkt4-discover-received'] += 1
    stats.s['v4-reservation-conflicts'] += 1
    stats.s['subnet[1].v4-reservation-conflicts'] += 1
    stats.compare()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', "11:11:11:11:11:11")
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.2')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.2')
    stats.s['cumulative-assigned-addresses'] += 1
    stats.s['pkt4-ack-sent'] += 1
    stats.s['pkt4-sent'] += 1
    stats.s['pkt4-received'] += 1
    stats.s['pkt4-request-received'] += 1
    stats.s['subnet[1].assigned-addresses'] += 1
    stats.s['subnet[1].cumulative-assigned-addresses'] += 1
    stats.s['subnet[1].pool[0].assigned-addresses'] += 1
    stats.s['subnet[1].pool[0].cumulative-assigned-addresses'] += 1
    stats.compare()

    # stats.s['pkt4-offer-sent'] += 1
    # stats.s['pkt4-sent'] += 1
    # stats.s['pkt4-received'] += 1
    # stats.s['pkt4-discover-received'] += 1
    # stats.s['subnet[1].v4-reservation-conflicts'] += 1
    # stats.s['v4-reservation-conflicts'] += 1
    # stats.compare()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', "ff:01:02:03:ff:04")
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'ciaddr', '0.0.0.0')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_send_msg('DECLINE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()
    stats.s['pkt4-decline-received'] += 1
    stats.s['pkt4-received'] += 1
    stats.s['subnet[1].declined-addresses'] += 1
    stats.s['subnet[1].pool[0].declined-addresses'] += 1
    stats.s['declined-addresses'] += 1
    stats.compare()

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    stats.s['pkt4-ack-sent'] += 1
    stats.s['pkt4-sent'] += 1
    stats.s['pkt4-received'] += 1
    stats.s['pkt4-inform-received'] += 1
    stats.compare()

    # let's build incorrect pkt
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', "11:11:11:11:11:11")
    srv_msg.client_copy_option('server_id')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER', expect_response=False)
    stats.s['pkt4-received'] += 1
    stats.s['pkt4-discover-received'] += 1
    stats.s['pkt4-receive-drop'] += 1
    stats.compare()

    assert get_stat("declined-addresses") == [1, 0], "Stat declined-addresses is not correct"
    assert get_stat("pkt4-ack-received") == [0], "Stat pkt4-ack-received is not correct"
    assert get_stat("pkt4-ack-sent") == [5, 4, 3, 2, 1, 0], "Stat pkt4-ack-sent is not correct"
    assert get_stat("pkt4-decline-received") == [1, 0], "Stat pkt4-decline-received is not correct"
    assert get_stat("pkt4-discover-received") == [5, 4, 3, 2, 1, 0], "Stat pkt4-discover-received is not correct"
    assert get_stat("pkt4-inform-received") == [1, 0], "Stat pkt4-inform-received is not correct"
    assert get_stat("pkt4-nak-received") == [0], "Stat pkt4-nak-received is not correct"
    assert get_stat("pkt4-nak-sent") == [0], "Stat pkt4-nak-sent is not correct"
    assert get_stat("pkt4-offer-received") == [0], "Stat pkt4-offer-received is not correct"
    assert get_stat("pkt4-offer-sent") == [4, 3, 2, 1, 0], "Stat pkt4-offer-sent is not correct"
    assert get_stat("pkt4-parse-failed") == [0], "Stat pkt4-parse-failed is not correct"
    assert get_stat("pkt4-receive-drop") == [1, 0], "Stat pkt4-receive-drop is not correct"
    assert get_stat("pkt4-received") == [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0], "Stat pkt4-received is not correct"
    assert get_stat("pkt4-request-received") == [4, 3, 2, 1, 0], "Stat pkt4-request-received is not correct"
    assert get_stat("pkt4-release-received") == [2, 1, 0], "Stat pkt4-release-received is not correct"
    assert get_stat("pkt4-sent") == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0], "Stat pkt4-sent is not correct"
    assert get_stat("pkt4-unknown-received") == [0], "Stat pkt4-unknown-received is not correct"
    assert get_stat("reclaimed-declined-addresses") == [0], "Stat reclaimed-declined-addresses is not correct"
    assert get_stat("reclaimed-leases") == [0], "Stat reclaimed-leases is not correct"
    assert get_stat("subnet[1].assigned-addresses") == [2, 1, 0, 1, 0, 1, 0], "Stat subnet[1].assigned-addresses is not correct"
    assert get_stat("subnet[1].pool[0].assigned-addresses") == [2, 1, 0, 1, 0, 1, 0], "Stat subnet[1].assigned-addresses is not correct"
    assert get_stat("subnet[1].declined-addresses") == [1, 0], "Stat subnet[1].declined-addresses is not correct"
    assert get_stat("subnet[1].reclaimed-declined-addresses") == [0], "Stat subnet[1].reclaimed-declined-addresses is not correct"
    assert get_stat("subnet[1].reclaimed-leases") == [0], "Stat subnet[1].reclaimed-leases is not correct"
    assert get_stat("subnet[1].total-addresses") == [10], "Stat subnet[1].total-addresses is not correct"
    assert get_stat("subnet[1].v4-reservation-conflicts") == [1, 0], "Stat subnet[1].v4-reservation-conflicts is not correct"
    assert get_stat("v4-reservation-conflicts") == [1, 0], "Stat v4-reservation-conflicts is not correct"


@pytest.mark.v4
def test_stats_remove_reset():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    result = srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt4-received"}}')
    assert result['arguments']['pkt4-received'][0][0] == 0, \
        f"number of pkt4-received is incorrect, expected 0 got {result['arguments']['pkt4-received'][0][0]}"

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')

    assert get_stat('pkt4-received') == [2, 1, 0], "Stat pkt4-received is not correct"
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-remove","arguments": {"name": "pkt4-received"}}')
    result = srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt4-received"}}')
    assert result == {'arguments': {}, 'result': 0}

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')

    assert get_stat('pkt4-received') == [2, 1], "Stat pkt4-received is not correct"
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-reset","arguments": {"name": "pkt4-received"}}')
    result = srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt4-received"}}')
    assert result['arguments']['pkt4-received'][0][0] == 0, "Stat pkt4-received is not correct"

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')

    assert get_stat('pkt4-received') == [2, 1, 0], "Stat pkt4-received is not correct"


@pytest.mark.v4
def test_stats_reconfigure():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    assert get_stat('pkt4-received') == [0], "Stat pkt4-received is not correct"
    assert get_stat('subnet[1].total-addresses') == [10], "Stat subnet[1].total-addresses is not correct"

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    assert get_stat('pkt4-received') == [1, 0], "Stat pkt4-received is not correct"

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.2')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()

    # reconfigure (reload) server, stats should be preserved
    srv_control.start_srv('DHCP', 'reconfigured')

    assert get_stat('pkt4-received') == [1, 0], "Stat pkt4-received is not correct"
    assert get_stat('subnet[1].total-addresses') == [1], "Stat subnet[1].total-addresses is not correct"
    assert get_stat('subnet[2].total-addresses') == [2], "Stat subnet[2].total-addresses is not correct"

    # restart kea, now stats should be reset
    srv_control.start_srv('DHCP', 'restarted')

    assert get_stat('pkt4-received') == [0], "Stat pkt4-received is not correct"
    assert get_stat('subnet[1].total-addresses') == [1], "Stat subnet[1].total-addresses is not correct"
    assert get_stat('subnet[2].total-addresses') == [2], "Stat subnet[2].total-addresses is not correct"


@pytest.mark.v4
def test_stats_sample_count():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = {"command": "statistic-sample-count-set",
           "arguments": {"name": "pkt4-received",
                         "max-samples": 2}}

    srv_msg.send_ctrl_cmd_via_socket(cmd)

    assert get_stat('pkt4-received') == [0], "Stat pkt4-received is not correct"
    assert get_stat('subnet[1].total-addresses') == [10], "Stat subnet[1].total-addresses is not correct"

    misc.test_procedure()
    for _ in range(3):
        srv_msg.client_requests_option(1)
        srv_msg.client_send_msg('DISCOVER')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'OFFER')

    assert get_stat('pkt4-received') == [3, 2], "Stat pkt4-received is not correct"


@pytest.mark.v4
def test_stats_sample_age():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = {"command": "statistic-sample-age-set",
           "arguments": {"name": "pkt4-received",
                         "duration": 1}}

    srv_msg.send_ctrl_cmd_via_socket(cmd)

    assert get_stat('pkt4-received') == [0], "Stat pkt4-received is not correct"
    assert get_stat('subnet[1].total-addresses') == [10], "Stat subnet[1].total-addresses is not correct"

    misc.test_procedure()
    for i in range(3):
        srv_msg.client_requests_option(1)
        srv_msg.client_send_msg('DISCOVER')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'OFFER')

        # Sleep between packets, so for all iterations except the last.
        if i < 2:
            srv_msg.forge_sleep(1, 'second')

    assert get_stat('pkt4-received') == [3], "Stat pkt4-received is not correct"


def _increase_mac(mac: str):
    """
    Recalculate mac address by keeping the first two octets unchanged, all the rest are incremented by one.

    :param mac: mac address as string
    :return: increased mac address as string
    """
    mac = mac.split(":")
    new_mac = (int(mac[0], 16),)
    new_mac += (int(mac[1], 16) + 1,)
    for i in range(2, 6):
        if int(mac[i], 16) + 1 > 255:
            pytest.fail("mac overflow. You may want to adjust parameter to not overflow")
        new_mac += (int(mac[i], 16) + 1,)
    return ':'.join(f'{i:02x}' for i in new_mac)


def _increase_ip(ip: str):
    ip = ip.split(".")
    ip[3] = int(ip[3]) + 1
    if ip[3] > 255:
        pytest.fail("ip overflow, You may want to adjust parameter to not overflow")
    return '.'.join(f'{i}' for i in ip)


def _get_leases(leases_count: int = 1, mac: str = "01:02:0c:03:0a:00"):
    all_leases = []
    for _ in range(leases_count):
        mac = _increase_mac(mac)
        client_id = '11' + mac.replace(':', '')
        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'chaddr', mac)
        srv_msg.client_does_include_with_value('client_id', client_id)
        srv_msg.client_requests_option(1)
        srv_msg.client_send_msg('DISCOVER')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'OFFER')
        yiaddr = world.srvmsg[0].yiaddr

        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'chaddr', mac)
        srv_msg.client_copy_option('server_id')
        srv_msg.client_does_include_with_value('client_id', client_id)
        srv_msg.client_does_include_with_value('requested_addr', yiaddr)
        srv_msg.client_requests_option(1)
        srv_msg.client_send_msg('REQUEST')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'ACK')
        srv_msg.response_check_content('yiaddr', yiaddr)

        all_leases.append(srv_msg.get_all_leases())

    return all_leases


def _decline_leases(leases_count: int = 1, mac: str = "01:02:0c:03:0a:00", ip: str = "192.168.50.0"):
    for _ in range(leases_count):
        mac = _increase_mac(mac)
        client_id = '11' + mac.replace(':', '')
        ip = _increase_ip(ip)
        srv_msg.client_sets_value('Client', 'chaddr', mac)
        srv_msg.client_does_include_with_value('client_id', client_id)
        # srv_msg.client_copy_option('server_id')
        srv_msg.client_sets_value('Client', 'ciaddr', '0.0.0.0')
        srv_msg.client_does_include_with_value('requested_addr', ip)
        srv_msg.client_send_msg('DECLINE')

        misc.pass_criteria()
        srv_msg.send_dont_wait_for_message()


@pytest.mark.v4
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('lease_remove_method', ['del', 'expire'])
def test_stats_pool_id_assign_reclaim(lease_remove_method, backend):
    """Test checks if pool statistics are updated corectly.
    Test scenario:
    - create 4 pools with different sizes
    - get leases from all pools
    - check if statistics are updated correctly
    - remove leases from the server (using del or expire method)
    - check if statistics are updated correctly

    Args:
        lease_remove_method: method of removing leases from server.
        backend: lease backend to use
    """
    # lease4-wipe is not used in test:
    # - method fails to remove statistics kea#3422
    # - is not supported in database kea#1045
    # - is deprecated kea#3427

    pool_0_A_size = 3
    pool_0_B_size = 5
    pool_0_size = pool_0_A_size + pool_0_B_size
    pool_1_size = 5
    pool_2_size = 10
    leases_to_get = pool_0_size + pool_1_size + pool_2_size

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.0.0/16', f'192.168.50.1-192.168.50.{pool_0_A_size}', id=1)
    srv_control.new_pool(f'192.168.51.1-192.168.51.{pool_0_B_size}', 0)
    srv_control.new_pool(f'192.168.52.1-192.168.52.{pool_1_size}', 0, pool_id=1)
    srv_control.new_pool(f'192.168.53.1-192.168.53.{pool_2_size}', 0, pool_id=2)
    if lease_remove_method == 'expire':
        srv_control.set_time('valid-lifetime', int(leases_to_get * 0.3 + 1))
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.disable_leases_affinity()
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    assert get_stat('subnet[1].pool[0].total-addresses')[0] == pool_0_size
    assert get_stat('subnet[1].pool[1].total-addresses')[0] == pool_1_size
    assert get_stat('subnet[1].pool[2].total-addresses')[0] == pool_2_size

    # Get leases to fill the pools
    _get_leases(leases_to_get, mac="02:02:0c:03:0a:00")

    # Subnet statistics checks
    assert get_stat('subnet[1].assigned-addresses')[0] == leases_to_get
    assert get_stat('subnet[1].cumulative-assigned-addresses')[0] == leases_to_get

    # Pool statistics checks
    assert get_stat('subnet[1].pool[0].assigned-addresses')[0] == pool_0_size
    assert get_stat('subnet[1].pool[0].cumulative-assigned-addresses')[0] == pool_0_size
    assert get_stat('subnet[1].pool[1].assigned-addresses')[0] == pool_1_size
    assert get_stat('subnet[1].pool[1].cumulative-assigned-addresses')[0] == pool_1_size
    assert get_stat('subnet[1].pool[2].assigned-addresses')[0] == pool_2_size
    assert get_stat('subnet[1].pool[2].cumulative-assigned-addresses')[0] == pool_2_size

    if lease_remove_method == 'expire':
        # Wait for leases to expire
        srv_msg.forge_sleep(int(leases_to_get * 0.3 + 4), "seconds")
    else:
        # delete those assigned leases
        for number in range(pool_0_A_size):
            cmd = {"command": "lease4-del", "arguments": {"ip-address": f'192.168.50.{number+1}'}}
            srv_msg.send_ctrl_cmd_via_socket(cmd)
        for number in range(pool_0_B_size):
            cmd = {"command": "lease4-del", "arguments": {"ip-address": f'192.168.51.{number+1}'}}
            srv_msg.send_ctrl_cmd_via_socket(cmd)
        for number in range(pool_1_size):
            cmd = {"command": "lease4-del", "arguments": {"ip-address": f'192.168.52.{number+1}'}}
            srv_msg.send_ctrl_cmd_via_socket(cmd)
        for number in range(pool_2_size):
            cmd = {"command": "lease4-del", "arguments": {"ip-address": f'192.168.53.{number+1}'}}
            srv_msg.send_ctrl_cmd_via_socket(cmd)

    # Make sure lease reclamation is done
    cmd = {"command": "leases-reclaim", "arguments": {"remove": True}}
    srv_msg.send_ctrl_cmd_via_socket(cmd)

    # Subnet statistics checks
    assert get_stat('subnet[1].reclaimed-leases')[0] == (leases_to_get if lease_remove_method == 'expire' else 0)
    assert get_stat('subnet[1].assigned-addresses')[0] == 0
    assert get_stat('subnet[1].cumulative-assigned-addresses')[0] == leases_to_get

    # Pool statistics checks
    assert get_stat('subnet[1].pool[0].assigned-addresses')[0] == 0
    assert get_stat('subnet[1].pool[0].cumulative-assigned-addresses')[0] == pool_0_size
    assert get_stat('subnet[1].pool[0].reclaimed-leases')[0] == (pool_0_size if lease_remove_method == 'expire' else 0)
    assert get_stat('subnet[1].pool[1].assigned-addresses')[0] == 0
    assert get_stat('subnet[1].pool[1].cumulative-assigned-addresses')[0] == pool_1_size
    assert get_stat('subnet[1].pool[1].reclaimed-leases')[0] == (pool_1_size if lease_remove_method == 'expire' else 0)
    assert get_stat('subnet[1].pool[2].assigned-addresses')[0] == 0
    assert get_stat('subnet[1].pool[2].cumulative-assigned-addresses')[0] == pool_2_size
    assert get_stat('subnet[1].pool[2].reclaimed-leases')[0] == (pool_2_size if lease_remove_method == 'expire' else 0)

    # Get leases again.
    _get_leases(pool_0_A_size, mac="50:02:0c:03:0a:00")
    _get_leases(pool_0_B_size, mac="51:02:0c:03:0a:00")
    _get_leases(pool_1_size, mac="52:02:0c:03:0a:00")
    _get_leases(pool_2_size, mac="53:02:0c:03:0a:00")

    # Subnet statistics checks
    assert get_stat('subnet[1].reclaimed-leases')[0] == (leases_to_get if lease_remove_method == 'expire' else 0)
    assert get_stat('subnet[1].assigned-addresses')[0] == leases_to_get
    assert get_stat('subnet[1].cumulative-assigned-addresses')[0] == 2 * leases_to_get

    # Pool statistics checks
    assert get_stat('subnet[1].pool[0].assigned-addresses')[0] == pool_0_size
    assert get_stat('subnet[1].pool[0].cumulative-assigned-addresses')[0] == 2 * pool_0_size
    assert get_stat('subnet[1].pool[0].reclaimed-leases')[0] == (pool_0_size if lease_remove_method == 'expire' else 0)
    assert get_stat('subnet[1].pool[1].assigned-addresses')[0] == pool_1_size
    assert get_stat('subnet[1].pool[1].cumulative-assigned-addresses')[0] == 2 * pool_1_size
    assert get_stat('subnet[1].pool[1].reclaimed-leases')[0] == (pool_1_size if lease_remove_method == 'expire' else 0)
    assert get_stat('subnet[1].pool[2].assigned-addresses')[0] == pool_2_size
    assert get_stat('subnet[1].pool[2].cumulative-assigned-addresses')[0] == 2 * pool_2_size
    assert get_stat('subnet[1].pool[2].reclaimed-leases')[0] == (pool_2_size if lease_remove_method == 'expire' else 0)


@pytest.mark.v4
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_stats_pool_id_decline(backend):
    """Test checks if pool decline leases statistics are updated corectly.
    Test scenario:
    - create 4 pools with different sizes
    - get leases from all pools
    - check if statistics are updated correctly
    - decline leases
    - check if statistics are updated correctly

    Args:
        backend: lease backend to use
    """

    pool_0_A_size = 2
    pool_0_B_size = 3
    pool_0_size = pool_0_A_size + pool_0_B_size
    pool_1_size = 4
    pool_2_size = 8
    leases_to_get = pool_0_size + pool_1_size + pool_2_size

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.0.0/16', f'192.168.50.1-192.168.50.{pool_0_A_size}', id=1)
    srv_control.new_pool(f'192.168.51.1-192.168.51.{pool_0_B_size}', 0)
    srv_control.new_pool(f'192.168.52.1-192.168.52.{pool_1_size}', 0, pool_id=1)
    srv_control.new_pool(f'192.168.53.1-192.168.53.{pool_2_size}', 0, pool_id=2)
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    # Probation period must be longer, than time required to Decline all leases
    srv_control.add_line({"decline-probation-period": int(leases_to_get * 0.4 + 1)})
    srv_control.disable_leases_affinity()
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    assert get_stat('subnet[1].pool[0].total-addresses')[0] == pool_0_size
    assert get_stat('subnet[1].pool[1].total-addresses')[0] == pool_1_size
    assert get_stat('subnet[1].pool[2].total-addresses')[0] == pool_2_size

    # Get leases. We split into pools so we can decline them later.
    _get_leases(pool_0_A_size, mac="50:02:0c:03:0a:00")
    _get_leases(pool_0_B_size, mac="51:02:0c:03:0a:00")
    _get_leases(pool_1_size, mac="52:02:0c:03:0a:00")
    _get_leases(pool_2_size, mac="53:02:0c:03:0a:00")

    # Subnet statistics checks
    assert get_stat('subnet[1].assigned-addresses')[0] == leases_to_get
    assert get_stat('subnet[1].cumulative-assigned-addresses')[0] == leases_to_get
    assert get_stat('subnet[1].declined-addresses')[0] == 0

    # Pool statistics checks
    assert get_stat('subnet[1].pool[0].assigned-addresses')[0] == pool_0_size
    assert get_stat('subnet[1].pool[0].cumulative-assigned-addresses')[0] == pool_0_size
    assert get_stat('subnet[1].pool[0].declined-addresses')[0] == 0
    assert get_stat('subnet[1].pool[1].assigned-addresses')[0] == pool_1_size
    assert get_stat('subnet[1].pool[1].cumulative-assigned-addresses')[0] == pool_1_size
    assert get_stat('subnet[1].pool[1].declined-addresses')[0] == 0
    assert get_stat('subnet[1].pool[2].assigned-addresses')[0] == pool_2_size
    assert get_stat('subnet[1].pool[2].cumulative-assigned-addresses')[0] == pool_2_size
    assert get_stat('subnet[1].pool[2].declined-addresses')[0] == 0

    assert get_stat('subnet[1].declined-addresses')[0] == 0

    # Shorten wait after sending Decline messages - we don't expect responses
    world.cfg['wait_interval'] = 0.1

    _decline_leases(pool_0_A_size, mac="50:02:0c:03:0a:00", ip="192.168.50.0")
    _decline_leases(pool_0_B_size, mac="51:02:0c:03:0a:00", ip="192.168.51.0")
    _decline_leases(pool_1_size, mac="52:02:0c:03:0a:00", ip="192.168.52.0")
    _decline_leases(pool_2_size, mac="53:02:0c:03:0a:00", ip="192.168.53.0")

    # Subnet statistics checks
    assert get_stat('subnet[1].declined-addresses')[0] == leases_to_get
    assert get_stat('subnet[1].reclaimed-declined-addresses')[0] == 0

    # Pool statistics checks
    assert get_stat('subnet[1].pool[0].declined-addresses')[0] == pool_0_size
    assert get_stat('subnet[1].pool[1].declined-addresses')[0] == pool_1_size
    assert get_stat('subnet[1].pool[2].declined-addresses')[0] == pool_2_size
    assert get_stat('subnet[1].pool[0].reclaimed-declined-addresses')[0] == 0
    assert get_stat('subnet[1].pool[1].reclaimed-declined-addresses')[0] == 0
    assert get_stat('subnet[1].pool[2].reclaimed-declined-addresses')[0] == 0

    # Wait for lease probation period to expire
    srv_msg.forge_sleep(int(leases_to_get * 0.4 + 5), "seconds")

    # Make sure lease reclamation is done
    cmd = {"command": "leases-reclaim", "arguments": {"remove": True}}
    srv_msg.send_ctrl_cmd_via_socket(cmd)

    # Subnet statistics checks
    assert get_stat('subnet[1].declined-addresses')[0] == 0
    assert get_stat('subnet[1].reclaimed-declined-addresses')[0] == leases_to_get
    # Pool statistics checks
    assert get_stat('subnet[1].pool[0].declined-addresses')[0] == 0
    assert get_stat('subnet[1].pool[1].declined-addresses')[0] == 0
    assert get_stat('subnet[1].pool[2].declined-addresses')[0] == 0
    assert get_stat('subnet[1].pool[0].reclaimed-declined-addresses')[0] == pool_0_size
    assert get_stat('subnet[1].pool[1].reclaimed-declined-addresses')[0] == pool_1_size
    assert get_stat('subnet[1].pool[2].reclaimed-declined-addresses')[0] == pool_2_size
