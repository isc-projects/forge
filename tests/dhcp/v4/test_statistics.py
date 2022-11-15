# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea Statistics"""

# pylint: disable=invalid-name
# pylint: disable=line-too-long

import time
import pytest

from src import srv_msg
from src import misc
from src import srv_control


class StatsState4:
    def __init__(self):
        self.s = {}
        self.s["cumulative-assigned-addresses"] = 0
        self.s["declined-addresses"] = 0
        self.s["pkt4-ack-received"] = 0
        self.s["pkt4-ack-sent"] = 0
        self.s["pkt4-decline-received"] = 0
        self.s["pkt4-discover-received"] = 0
        self.s["pkt4-inform-received"] = 0
        self.s["pkt4-nak-received"] = 0
        self.s["pkt4-nak-sent"] = 0
        self.s["pkt4-offer-received"] = 0
        self.s["pkt4-offer-sent"] = 0
        self.s["pkt4-parse-failed"] = 0
        self.s["pkt4-receive-drop"] = 0
        self.s["pkt4-received"] = 0
        self.s["pkt4-release-received"] = 0
        self.s["pkt4-request-received"] = 0
        self.s["pkt4-sent"] = 0
        self.s["pkt4-unknown-received"] = 0
        self.s["reclaimed-declined-addresses"] = 0
        self.s["reclaimed-leases"] = 0
        self.s["subnet[1].assigned-addresses"] = 0
        self.s["subnet[1].cumulative-assigned-addresses"] = 0
        self.s["subnet[1].declined-addresses"] = 0
        self.s["subnet[1].reclaimed-declined-addresses"] = 0
        self.s["subnet[1].reclaimed-leases"] = 0
        self.s["subnet[1].total-addresses"] = 0
        self.s['v4-allocation-fail'] = 0
        self.s['v4-allocation-fail-classes'] = 0
        self.s['v4-allocation-fail-no-pools'] = 0
        self.s['v4-allocation-fail-shared-network'] = 0
        self.s['v4-allocation-fail-subnet'] = 0
        self.s['subnet[1].v4-reservation-conflicts'] = 0
        self.s['v4-reservation-conflicts'] = 0

    def compare(self):
        result = srv_msg.send_ctrl_cmd_via_socket('{"command":"statistic-get-all","arguments":{}}')
        statistics_from_kea = result['arguments']
        assert len(statistics_from_kea) == 33, "Number of all statistics is incorrect"

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
    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    stats = StatsState4()
    stats.s['subnet[1].total-addresses'] = 10

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
    stats.s['subnet[1].v4-reservation-conflicts'] += 1
    stats.s['v4-reservation-conflicts'] += 1
    stats.compare()

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
    assert get_stat("pkt4-ack-sent") == [4, 3, 2, 1, 0], "Stat pkt4-ack-sent is not correct"
    assert get_stat("pkt4-decline-received") == [1, 0], "Stat pkt4-decline-received is not correct"
    assert get_stat("pkt4-discover-received") == [5, 4, 3, 2, 1, 0], "Stat pkt4-discover-received is not correct"
    assert get_stat("pkt4-inform-received") == [1, 0], "Stat pkt4-inform-received is not correct"
    assert get_stat("pkt4-nak-received") == [0], "Stat pkt4-nak-received is not correct"
    assert get_stat("pkt4-nak-sent") == [0], "Stat pkt4-nak-sent is not correct"
    assert get_stat("pkt4-offer-received") == [0], "Stat pkt4-offer-received is not correct"
    assert get_stat("pkt4-offer-sent") == [4, 3, 2, 1, 0], "Stat pkt4-offer-sent is not correct"
    assert get_stat("pkt4-parse-failed") == [0], "Stat pkt4-parse-failed is not correct"
    assert get_stat("pkt4-receive-drop") == [1, 0], "Stat pkt4-receive-drop is not correct"
    assert get_stat("pkt4-received") == [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0],\
        "Stat pkt4-received is not correct"
    assert get_stat("pkt4-request-received") == [3, 2, 1, 0], "Stat pkt4-request-received is not correct"
    assert get_stat("pkt4-release-received") == [2, 1, 0], "Stat pkt4-release-received is not correct"
    assert get_stat("pkt4-sent") == [8, 7, 6, 5, 4, 3, 2, 1, 0], "Stat pkt4-sent is not correct"
    assert get_stat("pkt4-unknown-received") == [0], "Stat pkt4-unknown-received is not correct"
    assert get_stat("reclaimed-declined-addresses") == [0], "Stat reclaimed-declined-addresses is not correct"
    assert get_stat("reclaimed-leases") == [0], "Stat reclaimed-leases is not correct"
    assert get_stat("subnet[1].assigned-addresses") == [1, 0, 1, 0, 1, 0],\
        "Stat subnet[1].assigned-addresses is not correct"
    assert get_stat("subnet[1].declined-addresses") == [1, 0], "Stat subnet[1].declined-addresses is not correct"
    assert get_stat("subnet[1].reclaimed-declined-addresses") == [0],\
        "Stat subnet[1].reclaimed-declined-addresses is not correct"
    assert get_stat("subnet[1].reclaimed-leases") == [0], "Stat subnet[1].reclaimed-leases is not correct"
    assert get_stat("subnet[1].total-addresses") == [10], "Stat subnet[1].total-addresses is not correct"

    assert get_stat("subnet[1].v4-reservation-conflicts") == [1, 0],\
        "Stat subnet[1].v4-reservation-conflicts is not correct"
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
    for _ in range(3):
        srv_msg.client_requests_option(1)
        srv_msg.client_send_msg('DISCOVER')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'OFFER')

    time.sleep(1)

    assert get_stat('pkt4-received') == [3], "Stat pkt4-received is not correct"


@pytest.mark.disabled
def test_X():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_another_subnet_no_interface('3000:100::/64',
                                                       '3000:100::5-3000:100::ff')
    srv_control.config_srv_prefix('3000::', 0, 90, 92)
    srv_control.open_control_channel('control_socket2')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'reconfigured')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"statistic-get-all","arguments":{}}',
                                     socket_name='control_socket2')

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_prefix('3000::', 0, 90, 92)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'reconfigured')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"statistic-get-all","arguments":{}}')

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_prefix('3000::', 0, 90, 92)
    srv_control.open_control_channel('control_socket2')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'reconfigured')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"statistic-get-all","arguments":{}}',
                                     socket_name='control_socket2')

    srv_control.start_srv('DHCP', 'restarted')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"statistic-get-all","arguments":{}}',
                                     socket_name='control_socket2')
