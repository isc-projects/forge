# Copyright (C) 2022-2023 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea v6 Statistics"""

# pylint: disable=invalid-name
# pylint: disable=line-too-long

import pytest

from src import misc
from src import srv_control
from src import srv_msg
from src.forge_cfg import world


class StatsState6:
    def __init__(self):
        self.s = {
            'cumulative-assigned-nas': 0,
            'cumulative-assigned-pds': 0,
            'declined-addresses': 0,
            'pkt6-advertise-received': 0,
            'pkt6-advertise-sent': 0,
            'pkt6-decline-received': 0,
            'pkt6-dhcpv4-query-received': 0,
            'pkt6-dhcpv4-response-received': 0,
            'pkt6-dhcpv4-response-sent': 0,
            'pkt6-infrequest-received': 0,
            'pkt6-parse-failed': 0,
            'pkt6-rebind-received': 0,
            'pkt6-receive-drop': 0,
            'pkt6-received': 0,
            'pkt6-release-received': 0,
            'pkt6-renew-received': 0,
            'pkt6-reply-received': 0,
            'pkt6-reply-sent': 0,
            'pkt6-request-received': 0,
            'pkt6-sent': 0,
            'pkt6-solicit-received': 0,
            'pkt6-unknown-received': 0,
            'reclaimed-declined-addresses': 0,
            'reclaimed-leases': 0,
            'subnet[1].assigned-nas': 0,
            'subnet[1].assigned-pds': 0,
            'subnet[1].cumulative-assigned-nas': 0,
            'subnet[1].cumulative-assigned-pds': 0,
            'subnet[1].declined-addresses': 0,
            'subnet[1].reclaimed-declined-addresses': 0,
            'subnet[1].reclaimed-leases': 0,
            'subnet[1].total-nas': 0,
            'subnet[1].total-pds': 0,
            'subnet[1].v6-ia-na-lease-reuses': 0,
            'subnet[1].v6-ia-pd-lease-reuses': 0,
            'subnet[1].pool[0].assigned-nas': 0,
            'subnet[1].pool[0].cumulative-assigned-nas': 0,
            'subnet[1].pool[0].declined-addresses': 0,
            'subnet[1].pool[0].reclaimed-declined-addresses': 0,
            'subnet[1].pool[0].reclaimed-leases': 0,
            'subnet[1].pool[0].total-nas': 0,
            'v6-allocation-fail': 0,
            'v6-allocation-fail-classes': 0,
            'v6-allocation-fail-no-pools': 0,
            'v6-allocation-fail-shared-network': 0,
            'v6-allocation-fail-subnet': 0,
            'v6-ia-na-lease-reuses': 0,
            'v6-ia-pd-lease-reuses': 0,
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

        assert len(statistics_from_kea) == 48, 'Number of all statistics is incorrect.'

        for key, expected in self.s.items():
            received = statistics_from_kea[key][0][0]
            assert expected == received, f'stat {key}: expected {expected}, received {received}'


def get_stat(name):
    cmd = {"command": "statistic-get", "arguments": {"name": name}}
    result = srv_msg.send_ctrl_cmd_via_socket(cmd)
    result = [r[0] for r in result['arguments'][name]]
    return result


@pytest.mark.v6
def test_stats_basic():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::a')
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.disable_leases_affinity()
    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.add_unix_socket()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    stats = StatsState6()
    stats.s['subnet[1].total-nas'] = 10
    stats.s['subnet[1].pool[0].total-nas'] = 10
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

    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:01:02:03:ff:04')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.check_IA_NA('2001:db8:1::1')
    stats.s['pkt6-advertise-sent'] += 1
    stats.s['pkt6-sent'] += 1
    stats.s['pkt6-received'] += 1
    stats.s['pkt6-solicit-received'] += 1
    stats.compare()

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'DUID', "00:03:00:01:ff:01:02:03:ff:04")
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.check_IA_NA('2001:db8:1::1')

    stats.s['cumulative-assigned-nas'] += 1
    stats.s['pkt6-reply-sent'] += 1
    stats.s['pkt6-sent'] += 1
    stats.s['pkt6-received'] += 1
    stats.s['pkt6-request-received'] += 1
    stats.s['subnet[1].assigned-nas'] += 1
    stats.s['subnet[1].cumulative-assigned-nas'] += 1
    stats.s['subnet[1].pool[0].assigned-nas'] += 1
    stats.s['subnet[1].pool[0].cumulative-assigned-nas'] += 1
    stats.compare()

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'DUID', "00:03:00:01:ff:01:02:03:ff:04")
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    stats.s['pkt6-received'] += 1
    stats.s['pkt6-release-received'] += 1
    stats.s['pkt6-reply-sent'] += 1
    stats.s['pkt6-sent'] += 1
    stats.s['subnet[1].assigned-nas'] -= 1
    stats.s['subnet[1].pool[0].assigned-nas'] -= 1
    stats.compare()

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'DUID', "00:03:00:01:ff:01:02:03:ff:04")
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.check_IA_NA('2001:db8:1::2')
    stats.s['pkt6-advertise-sent'] += 1
    stats.s['pkt6-sent'] += 1
    stats.s['pkt6-received'] += 1
    stats.s['pkt6-solicit-received'] += 1
    stats.compare()

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'DUID', "00:03:00:01:ff:01:02:03:ff:04")
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.check_IA_NA('2001:db8:1::2')
    stats.s['cumulative-assigned-nas'] += 1
    stats.s['pkt6-reply-sent'] += 1
    stats.s['pkt6-sent'] += 1
    stats.s['pkt6-received'] += 1
    stats.s['pkt6-request-received'] += 1
    stats.s['subnet[1].assigned-nas'] += 1
    stats.s['subnet[1].cumulative-assigned-nas'] += 1
    stats.s['subnet[1].pool[0].assigned-nas'] += 1
    stats.s['subnet[1].pool[0].cumulative-assigned-nas'] += 1
    stats.compare()

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'DUID', "00:03:00:01:ff:01:02:03:ff:04")
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    stats.s['pkt6-received'] += 1
    stats.s['pkt6-release-received'] += 1
    stats.s['pkt6-reply-sent'] += 1
    stats.s['pkt6-sent'] += 1
    stats.s['subnet[1].assigned-nas'] -= 1
    stats.s['subnet[1].pool[0].assigned-nas'] -= 1
    stats.compare()

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'DUID', "00:03:00:01:ff:01:02:03:ff:04")
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.check_IA_NA('2001:db8:1::3')
    stats.s['pkt6-advertise-sent'] += 1
    stats.s['pkt6-sent'] += 1
    stats.s['pkt6-received'] += 1
    stats.s['pkt6-solicit-received'] += 1
    stats.compare()

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'DUID', "00:03:00:01:ff:01:02:03:ff:04")
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.check_IA_NA('2001:db8:1::3')
    stats.s['cumulative-assigned-nas'] += 1
    stats.s['pkt6-reply-sent'] += 1
    stats.s['pkt6-sent'] += 1
    stats.s['pkt6-received'] += 1
    stats.s['pkt6-request-received'] += 1
    stats.s['subnet[1].assigned-nas'] += 1
    stats.s['subnet[1].cumulative-assigned-nas'] += 1
    stats.s['subnet[1].pool[0].assigned-nas'] += 1
    stats.s['subnet[1].pool[0].cumulative-assigned-nas'] += 1
    stats.compare()

    new_hr = {
        "arguments": {
            "reservation": {
                "duid": "00:03:00:01:11:11:11:11:11:11",
                "ip-addresses": ["2001:db8:1::50"],
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }
    result = srv_msg.send_ctrl_cmd_via_socket(new_hr)

    # let's try to get new reservation
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'DUID', "00:03:00:01:11:11:11:11:11:11")
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    # it should not get reserved address
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.check_IA_NA('2001:db8:1::3')
    stats.s['pkt6-advertise-sent'] += 1
    stats.s['pkt6-sent'] += 1
    stats.s['pkt6-received'] += 1
    stats.s['pkt6-solicit-received'] += 1
    stats.compare()

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'DUID', "00:03:00:01:11:11:11:11:11:11")
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.check_IA_NA('2001:db8:1::50')
    stats.s['pkt6-reply-sent'] += 1
    stats.s['pkt6-sent'] += 1
    stats.s['pkt6-received'] += 1
    stats.s['pkt6-request-received'] += 1
    stats.compare()

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'DUID', "00:03:00:01:ff:01:02:03:ff:04")
    srv_msg.client_send_msg('DECLINE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    stats.s['pkt6-decline-received'] += 1
    stats.s['pkt6-received'] += 1
    stats.s['pkt6-reply-sent'] += 1
    stats.s['pkt6-sent'] += 1
    stats.s['subnet[1].declined-addresses'] += 1
    # we decline address from subnet but not from pool! subnet[1].pool[0].declined-addresses won't be updated
    stats.s['declined-addresses'] += 1
    stats.compare()

    # let's build incorrect pkt
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'DUID', "00:03:00:01:11:11:11:11:11:11")
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE', expect_response=False)
    stats.s['pkt6-received'] += 1
    stats.s['pkt6-solicit-received'] += 1
    stats.s['pkt6-receive-drop'] += 1
    stats.compare()

    assert get_stat("declined-addresses") == [1, 0], "Stat declined-addresses is not correct"
    assert get_stat("pkt6-reply-received") == [0], "Stat pkt6-reply-received is not correct"
    assert get_stat("pkt6-reply-sent") == [7, 6, 5, 4, 3, 2, 1, 0], "Stat pkt6-reply-sent is not correct"
    assert get_stat("pkt6-decline-received") == [1, 0], "Stat pkt6-decline-received is not correct"
    assert get_stat("pkt6-solicit-received") == [5, 4, 3, 2, 1, 0], "Stat pkt6-solicit-received is not correct"
    assert get_stat("pkt6-advertise-received") == [0], "Stat pkt6-advertise-received is not correct"
    assert get_stat("pkt6-advertise-sent") == [4, 3, 2, 1, 0], "Stat pkt6-advertise-sent is not correct"
    assert get_stat("pkt6-parse-failed") == [0], "Stat pkt6-parse-failed is not correct"
    assert get_stat("pkt6-receive-drop") == [1, 0], "Stat pkt6-receive-drop is not correct"
    assert get_stat("pkt6-received") == [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0], "Stat pkt6-received is not correct"
    assert get_stat("pkt6-request-received") == [4, 3, 2, 1, 0], "Stat pkt6-request-received is not correct"
    assert get_stat("pkt6-release-received") == [2, 1, 0], "Stat pkt6-release-received is not correct"
    assert get_stat("pkt6-sent") == [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0], "Stat pkt6-sent is not correct"
    assert get_stat("pkt6-unknown-received") == [0], "Stat pkt6-unknown-received is not correct"
    assert get_stat("reclaimed-declined-addresses") == [0], "Stat reclaimed-declined-addresses is not correct"
    assert get_stat("reclaimed-leases") == [0], "Stat reclaimed-leases is not correct"
    assert get_stat("subnet[1].assigned-nas") == [1, 0, 1, 0, 1, 0], "Stat subnet[1].assigned-nas is not correct"
    assert get_stat("subnet[1].pool[0].assigned-nas") == [1, 0, 1, 0, 1, 0], "Stat subnet[1].assigned-nas is not correct"
    assert get_stat("subnet[1].declined-addresses") == [1, 0], "Stat subnet[1].declined-addresses is not correct"
    assert get_stat("subnet[1].reclaimed-declined-addresses") == [0], "Stat subnet[1].reclaimed-declined-addresses is not correct"
    assert get_stat("subnet[1].reclaimed-leases") == [0], "Stat subnet[1].reclaimed-leases is not correct"
    assert get_stat("subnet[1].total-nas") == [10], "Stat subnet[1].total-nas is not correct"
    assert get_stat("subnet[1].pool[0].total-nas") == [10], "Stat subnet[1].total-nas is not correct"


@pytest.mark.v6
def test_stats_remove_reset():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.add_unix_socket()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    result = srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-received"}}')
    assert result['arguments']['pkt6-received'][0][0] == 0, \
        f"number of pkt6-received is incorrect, expected 0 got {result['arguments']['pkt6-received'][0][0]}"

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    assert get_stat('pkt6-received') == [2, 1, 0], "Stat pkt6-received is not correct"
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-remove","arguments": {"name": "pkt6-received"}}')
    result = srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-received"}}')
    assert result == {'arguments': {}, 'result': 0}

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    assert get_stat('pkt6-received') == [2, 1], "Stat pkt6-received is not correct"
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-reset","arguments": {"name": "pkt6-received"}}')
    result = srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-received"}}')
    assert result['arguments']['pkt6-received'][0][0] == 0, "Stat pkt6-received is not correct"

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    assert get_stat('pkt6-received') == [2, 1, 0], "Stat pkt6-received is not correct"


@pytest.mark.v6
def test_stats_reconfigure():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::a')
    srv_control.add_unix_socket()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    assert get_stat('pkt6-received') == [0], "Stat pkt6-received is not correct"
    assert get_stat('subnet[1].total-nas') == [10], "Stat subnet[1].total-nas is not correct"

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    assert get_stat('pkt6-received') == [1, 0], "Stat pkt6-received is not correct"

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:2::/64',
                                                       '2001:db8:2::1-2001:db8:2::2')
    srv_control.add_unix_socket()
    srv_control.build_and_send_config_files()

    # reconfigure (reload) server, stats should be preserved
    srv_control.start_srv('DHCP', 'reconfigured')

    assert get_stat('pkt6-received') == [1, 0], "Stat pkt6-received is not correct"
    assert get_stat('subnet[1].total-nas') == [1], "Stat subnet[1].total-nas is not correct"
    assert get_stat('subnet[2].total-nas') == [2], "Stat subnet[2].total-nas is not correct"

    # restart kea, now stats should be reset
    srv_control.start_srv('DHCP', 'restarted')

    assert get_stat('pkt6-received') == [0], "Stat pkt6-received is not correct"
    assert get_stat('subnet[1].total-nas') == [1], "Stat subnet[1].total-nas is not correct"
    assert get_stat('subnet[2].total-nas') == [2], "Stat subnet[2].total-nas is not correct"


@pytest.mark.v6
def test_stats_sample_count():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1 - 2001:db8:1::a')
    srv_control.add_unix_socket()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = {"command": "statistic-sample-count-set",
           "arguments": {"name": "pkt6-received",
                         "max-samples": 2}}

    srv_msg.send_ctrl_cmd_via_socket(cmd)

    assert get_stat('pkt6-received') == [0], "Stat pkt6-received is not correct"
    assert get_stat('subnet[1].total-nas') == [10], "Stat subnet[1].total-nas is not correct"

    misc.test_procedure()
    for _ in range(3):
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_send_msg('SOLICIT')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    assert get_stat('pkt6-received') == [3, 2], "Stat pkt6-received is not correct"


@pytest.mark.v6
def test_stats_sample_age():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1 - 2001:db8:1::a')
    srv_control.add_unix_socket()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = {"command": "statistic-sample-age-set",
           "arguments": {"name": "pkt6-received",
                         "duration": 1}}

    srv_msg.send_ctrl_cmd_via_socket(cmd)

    assert get_stat('pkt6-received') == [0], "Stat pkt6-received is not correct"
    assert get_stat('subnet[1].total-nas') == [10], "Stat subnet[1].total-nas is not correct"

    misc.test_procedure()
    for i in range(3):
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_does_include('Client', 'IA-NA')
        srv_msg.client_sets_value('Client', 'DUID', "00:03:00:01:11:11:11:11:11:11")
        srv_msg.client_send_msg('SOLICIT')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

        # Sleep between packets, so for all iterations except the last.
        if i < 2:
            srv_msg.forge_sleep(1, 'second')

    assert get_stat('pkt6-received') == [3], "Stat pkt6-received is not correct"


@pytest.mark.disabled
def test_stats_6():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_prefix('3001::', 0, 90, 92)
    srv_control.add_unix_socket()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    # message wont contain client-id option
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.loops('SOLICIT', 'ADVERTISE', 50)

    srv_msg.send_ctrl_cmd_via_socket('{"command": "list-commands","arguments": {}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"statistic-get-all","arguments":{}}')

    srv_msg.loops('SOLICIT', 'ADVERTISE', 50)

    srv_msg.send_ctrl_cmd_via_socket('{"command":"statistic-get-all","arguments":{}}')

    srv_msg.loops('SOLICIT', 'ADVERTISE', 50)

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('CONFIRM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-receive-drop"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-parse-failed"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-solicit-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-confirm-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-advertise-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-reply-received"}}')

    misc.test_procedure()
    srv_msg.client_requests_option('preference')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_requests_option('preference')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-renew-received"}}')

    misc.test_procedure()
    srv_msg.client_requests_option(7)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option('client-id')
    srv_msg.response_check_include_option('server-id')
    srv_msg.response_check_include_option('IA_NA')
    srv_msg.response_check_option_content('IA_NA', 'sub-option', 'IA_address')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option('client-id')
    srv_msg.response_check_include_option('server-id')
    srv_msg.response_check_include_option('IA_NA')
    srv_msg.response_check_option_content('IA_NA', 'sub-option', 'IA_address')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REBIND')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-rebind-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-release-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-decline-received"}}')

    misc.test_procedure()
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-infrequest-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-unknown-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-sent"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-advertise-sent"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-reply-sent"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "subnet[1].total-nas"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "subnet[1].assigned-nas"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "subnet[1].total-pds"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "subnet[1].assigned-pds"}}')

    srv_msg.loops('REQUEST', 'REPLY', 50)

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option('client-id')
    srv_msg.response_check_include_option('server-id')
    srv_msg.response_check_include_option('IA_NA')
    srv_msg.response_check_option_content('IA_NA', 'sub-option', 'IA_address')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-advertise-sent"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-reply-sent"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "subnet[1].total-nas"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "subnet[1].assigned-nas"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "subnet[1].total-pds"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "subnet[1].assigned-pds"}}')

    srv_msg.loops('REQUEST', 'REPLY', 50)

    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get-all","arguments":{}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "subnet[1].total-nas"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "subnet[1].assigned-nas"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-reset","arguments": {"name": "pkt6-request-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}')

    srv_msg.loops('SOLICIT', 'ADVERTISE', 50)

    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}')

    srv_msg.loops('REQUEST', 'REPLY', 50)

    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-remove","arguments": {"name": "pkt6-request-received"}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}')

    srv_msg.loops('SOLICIT', 'ADVERTISE', 50)

    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}')

    srv_msg.loops('REQUEST', 'REPLY', 50)

    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-request-received"}}')

    misc.test_procedure()
    srv_msg.client_requests_option(7)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_requests_option('preference')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    misc.test_procedure()
    srv_msg.client_save_option('IA_NA')
    srv_msg.client_add_saved_option()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('DECLINE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt6-decline-received"}}')

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_another_subnet_no_interface('3000:100::/64',
                                                       '3000:100::5-3000:100::ff')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 92)
    srv_control.add_http_control_channel('control_socket2')
    srv_control.start_srv('DHCP', 'reconfigured')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"statistic-get-all","arguments":{}}',
                                     socket_name='control_socket2')

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 92)
    srv_control.start_srv('DHCP', 'reconfigured')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"statistic-get-all","arguments":{}}')

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_prefix('2001:db8:1::', 0, 90, 92)
    srv_control.add_http_control_channel('control_socket2')
    srv_control.start_srv('DHCP', 'reconfigured')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"statistic-get-all","arguments":{}}',
                                     socket_name='control_socket2')

    srv_control.start_srv('DHCP', 'restarted')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"statistic-get-all","arguments":{}}',
                                     socket_name='control_socket2')


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
    ip = ip.split(":")
    ip[6] = f'{(int(ip[6], 16) + 1):x}'
    if int(ip[6]) > 65535:
        pytest.fail("ip overflow, You may want to adjust parameter to not overflow")
    return ':'.join(f'{i}' for i in ip)


def _get_leases(leases_count: int = 1, mac: str = "01:02:0c:03:0a:00", pd=False):
    all_leases = []
    for _ in range(leases_count):
        mac = _increase_mac(mac)
        duid = "00:03:00:01:" + mac

        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'DUID', duid)
        srv_msg.client_does_include('Client', 'client-id')
        if pd:
            srv_msg.client_does_include('Client', 'IA-PD')
        else:
            srv_msg.client_does_include('Client', 'IA-NA')
        srv_msg.client_send_msg('SOLICIT')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

        misc.test_procedure()
        srv_msg.client_copy_option('server-id')
        if pd:
            srv_msg.client_does_include('Client', 'IA-PD')
        else:
            srv_msg.client_copy_option('IA_NA')
            srv_msg.client_does_include('Client', 'IA-NA')
        srv_msg.client_sets_value('Client', 'DUID', duid)
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_send_msg('REQUEST')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'REPLY')

        all_leases.append(srv_msg.get_all_leases())

    return all_leases


def _decline_leases(leases_count: int = 1, mac: str = "01:02:0c:03:0a:00", ip: str = "2001:db8:a:a:1::0"):
    for _ in range(leases_count):
        mac = _increase_mac(mac)
        duid = "00:03:00:01:" + mac
        ip = _increase_ip(ip)

        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'DUID', duid)
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_copy_option('server-id')
        srv_msg.client_sets_value('Client', 'IA_Address', ip)
        srv_msg.client_does_include('Client', 'IA_Address')
        srv_msg.client_does_include('Client', 'IA-NA')
        srv_msg.client_send_msg('DECLINE')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'REPLY')


@pytest.mark.v6
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('lease_remove_method', ['del', 'expire'])
def test_stats_pool_id_assign_reclaim(lease_remove_method, backend):
    """Test checks if pool statistics are updated corectly.
    Test scenario:
    - create 4 pools with different sizes
    - get leases from all pools
    - check if statistics are updated correctly
    - remove leases from the server (using wipe, del or expire method)
    - check if statistics are updated correctly

    Args:
        lease_remove_method: method of removing leases from server.
        backend: lease backend to use
    """
    # lease6-wipe is not used in test:
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
    srv_control.config_srv_subnet('2001:db8:a:a:1::/64', f'2001:db8:a:a:1::1-2001:db8:a:a:1::{pool_0_A_size:x}', id=1)
    srv_control.new_pool(f'2001:db8:a:a:2::1-2001:db8:a:a:2::{pool_0_B_size:x}', 0)
    srv_control.new_pool(f'2001:db8:a:a:3::1-2001:db8:a:a:3::{pool_1_size:x}', 0, pool_id=1)
    srv_control.new_pool(f'2001:db8:a:a:4::1-2001:db8:a:a:4::{pool_2_size:x}', 0, pool_id=2)
    if lease_remove_method == 'expire':
        srv_control.set_time('valid-lifetime', int(leases_to_get * 0.4 + 1))
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.disable_leases_affinity()
    srv_control.add_unix_socket()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    assert get_stat('subnet[1].pool[0].total-nas')[0] == pool_0_size
    assert get_stat('subnet[1].pool[1].total-nas')[0] == pool_1_size
    assert get_stat('subnet[1].pool[2].total-nas')[0] == pool_2_size

    # Get leases to fill the pools
    _get_leases(leases_to_get, mac="02:02:0c:03:0a:00")

    # Subnet statistics checks
    assert get_stat('subnet[1].assigned-nas')[0] == leases_to_get
    assert get_stat('subnet[1].cumulative-assigned-nas')[0] == leases_to_get

    # Pool statistics checks
    assert get_stat('subnet[1].pool[0].assigned-nas')[0] == pool_0_size
    assert get_stat('subnet[1].pool[0].cumulative-assigned-nas')[0] == pool_0_size
    assert get_stat('subnet[1].pool[1].assigned-nas')[0] == pool_1_size
    assert get_stat('subnet[1].pool[1].cumulative-assigned-nas')[0] == pool_1_size
    assert get_stat('subnet[1].pool[2].assigned-nas')[0] == pool_2_size
    assert get_stat('subnet[1].pool[2].cumulative-assigned-nas')[0] == pool_2_size

    if lease_remove_method == 'expire':
        # Wait for leases to expire
        srv_msg.forge_sleep(int(leases_to_get * 0.9 + 5), "seconds")
    else:
        # delete those assigned leases
        for number in range(pool_0_A_size):
            cmd = {"command": "lease6-del", "arguments": {"ip-address": f'2001:db8:a:a:1::{(number+1):x}'}}
            srv_msg.send_ctrl_cmd_via_socket(cmd)
        for number in range(pool_0_B_size):
            cmd = {"command": "lease6-del", "arguments": {"ip-address": f'2001:db8:a:a:2::{(number+1):x}'}}
            srv_msg.send_ctrl_cmd_via_socket(cmd)
        for number in range(pool_1_size):
            cmd = {"command": "lease6-del", "arguments": {"ip-address": f'2001:db8:a:a:3::{(number+1):x}'}}
            srv_msg.send_ctrl_cmd_via_socket(cmd)
        for number in range(pool_2_size):
            cmd = {"command": "lease6-del", "arguments": {"ip-address": f'2001:db8:a:a:4::{(number+1):x}'}}
            srv_msg.send_ctrl_cmd_via_socket(cmd)

    # Make sure lease reclamation is done
    cmd = {"command": "leases-reclaim", "arguments": {"remove": True}}
    srv_msg.send_ctrl_cmd_via_socket(cmd)

    # Subnet statistics checks
    assert get_stat('subnet[1].reclaimed-leases')[0] == (leases_to_get if lease_remove_method == 'expire' else 0)
    assert get_stat('subnet[1].assigned-nas')[0] == 0
    assert get_stat('subnet[1].cumulative-assigned-nas')[0] == leases_to_get

    # Pool statistics checks
    assert get_stat('subnet[1].pool[0].assigned-nas')[0] == 0
    assert get_stat('subnet[1].pool[0].cumulative-assigned-nas')[0] == pool_0_size
    assert get_stat('subnet[1].pool[0].reclaimed-leases')[0] == (pool_0_size if lease_remove_method == 'expire' else 0)
    assert get_stat('subnet[1].pool[1].assigned-nas')[0] == 0
    assert get_stat('subnet[1].pool[1].cumulative-assigned-nas')[0] == pool_1_size
    assert get_stat('subnet[1].pool[1].reclaimed-leases')[0] == (pool_1_size if lease_remove_method == 'expire' else 0)
    assert get_stat('subnet[1].pool[2].assigned-nas')[0] == 0
    assert get_stat('subnet[1].pool[2].cumulative-assigned-nas')[0] == pool_2_size
    assert get_stat('subnet[1].pool[2].reclaimed-leases')[0] == (pool_2_size if lease_remove_method == 'expire' else 0)

    # Get leases to fill the pools
    _get_leases(leases_to_get, mac="05:02:0c:03:0a:00")

    # Subnet statistics checks
    assert get_stat('subnet[1].reclaimed-leases')[0] == (leases_to_get if lease_remove_method == 'expire' else 0)
    assert get_stat('subnet[1].assigned-nas')[0] == leases_to_get
    assert get_stat('subnet[1].cumulative-assigned-nas')[0] == 2 * leases_to_get

    # Pool statistics checks
    assert get_stat('subnet[1].pool[0].assigned-nas')[0] == pool_0_size
    assert get_stat('subnet[1].pool[0].cumulative-assigned-nas')[0] == 2 * pool_0_size
    assert get_stat('subnet[1].pool[0].reclaimed-leases')[0] == (pool_0_size if lease_remove_method == 'expire' else 0)
    assert get_stat('subnet[1].pool[1].assigned-nas')[0] == pool_1_size
    assert get_stat('subnet[1].pool[1].cumulative-assigned-nas')[0] == 2 * pool_1_size
    assert get_stat('subnet[1].pool[1].reclaimed-leases')[0] == (pool_1_size if lease_remove_method == 'expire' else 0)
    assert get_stat('subnet[1].pool[2].assigned-nas')[0] == pool_2_size
    assert get_stat('subnet[1].pool[2].cumulative-assigned-nas')[0] == 2 * pool_2_size
    assert get_stat('subnet[1].pool[2].reclaimed-leases')[0] == (pool_2_size if lease_remove_method == 'expire' else 0)


@pytest.mark.v6
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('lease_remove_method', ['del', 'expire'])
def test_stats_pool_id_assign_reclaim_pd(lease_remove_method, backend):
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
    # lease6-wipe is not used in test:
    # - method fails to remove statistics kea#3422
    # - is not supported in database kea#1045
    # - is deprecated kea#3427

    pool_0_A_delegated = 33
    pool_0_B_delegated = 34
    pool_1_delegated = 35
    pool_2_delegated = 36

    pool_0_A_size = pow(2, (pool_0_A_delegated-32))
    pool_0_B_size = pow(2, (pool_0_B_delegated-32))
    pool_0_size = pool_0_A_size + pool_0_B_size
    pool_1_size = pow(2, (pool_1_delegated-32))
    pool_2_size = pow(2, (pool_2_delegated-32))
    leases_to_get = pool_0_size + pool_1_size + pool_2_size

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a:a:1::/64', None, id=1)
    srv_control.config_srv_prefix('3000:db8::', 0, 32, pool_0_A_delegated)
    srv_control.config_srv_prefix('4000:db8::', 0, 32, pool_0_B_delegated)
    srv_control.config_srv_prefix('5000:db8::', 0, 32, pool_1_delegated, pool_id=1)
    srv_control.config_srv_prefix('6000:db8::', 0, 32, pool_2_delegated, pool_id=2)
    if lease_remove_method == 'expire':
        srv_control.set_time('valid-lifetime', int(leases_to_get * 0.4 + 1))
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.disable_leases_affinity()
    srv_control.add_http_control_channel()
    srv_control.add_unix_socket()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    assert get_stat('subnet[1].pd-pool[0].total-pds')[0] == pool_0_size
    assert get_stat('subnet[1].pd-pool[1].total-pds')[0] == pool_1_size
    assert get_stat('subnet[1].pd-pool[2].total-pds')[0] == pool_2_size

    # Get leases to fill the pools
    _get_leases(leases_to_get, mac="02:02:0c:03:0a:00", pd=True)

    # Subnet statistics checks
    assert get_stat('subnet[1].assigned-pds')[0] == leases_to_get
    assert get_stat('subnet[1].cumulative-assigned-pds')[0] == leases_to_get

    # Pool statistics checks
    assert get_stat('subnet[1].pd-pool[0].assigned-pds')[0] == pool_0_size
    assert get_stat('subnet[1].pd-pool[0].cumulative-assigned-pds')[0] == pool_0_size
    assert get_stat('subnet[1].pd-pool[1].assigned-pds')[0] == pool_1_size
    assert get_stat('subnet[1].pd-pool[1].cumulative-assigned-pds')[0] == pool_1_size
    assert get_stat('subnet[1].pd-pool[2].assigned-pds')[0] == pool_2_size
    assert get_stat('subnet[1].pd-pool[2].cumulative-assigned-pds')[0] == pool_2_size

    if lease_remove_method == 'expire':
        # Wait for leases to expire
        srv_msg.forge_sleep(int(leases_to_get * 0.9 + 5), "seconds")
    else:
        # delete those assigned leases
        mac = "02:02:0c:03:0a:00"
        for _ in range(leases_to_get):
            mac = _increase_mac(mac)
            duid = "00:03:00:01:" + mac
            cmd = {"command": "lease6-get-by-duid", "arguments": {"duid": duid}}
            response = srv_msg.send_ctrl_cmd_via_socket(cmd)
            iaid = response['arguments']['leases'][0]['iaid']
            cmd = {"command": "lease6-del",
                   "arguments": {"subnet-id": 1,
                                 "identifier": duid,
                                 "identifier-type": "duid",
                                 "iaid": iaid,
                                 "type": "IA_PD"}}
            srv_msg.send_ctrl_cmd_via_socket(cmd)

    # Make sure lease reclamation is done
    cmd = {"command": "leases-reclaim", "arguments": {"remove": True}}
    srv_msg.send_ctrl_cmd_via_socket(cmd)

    # Subnet statistics checks
    assert get_stat('subnet[1].reclaimed-leases')[0] == (leases_to_get if lease_remove_method == 'expire' else 0)
    assert get_stat('subnet[1].assigned-pds')[0] == 0
    assert get_stat('subnet[1].cumulative-assigned-pds')[0] == leases_to_get

    # Pool statistics checks
    assert get_stat('subnet[1].pd-pool[0].assigned-pds')[0] == 0
    assert get_stat('subnet[1].pd-pool[0].cumulative-assigned-pds')[0] == pool_0_size
    assert get_stat('subnet[1].pd-pool[0].reclaimed-leases')[0] == (pool_0_size if lease_remove_method == 'expire' else 0)
    assert get_stat('subnet[1].pd-pool[1].assigned-pds')[0] == 0
    assert get_stat('subnet[1].pd-pool[1].cumulative-assigned-pds')[0] == pool_1_size
    assert get_stat('subnet[1].pd-pool[1].reclaimed-leases')[0] == (pool_1_size if lease_remove_method == 'expire' else 0)
    assert get_stat('subnet[1].pd-pool[2].assigned-pds')[0] == 0
    assert get_stat('subnet[1].pd-pool[2].cumulative-assigned-pds')[0] == pool_2_size
    assert get_stat('subnet[1].pd-pool[2].reclaimed-leases')[0] == (pool_2_size if lease_remove_method == 'expire' else 0)

    # Get leases again.
    _get_leases(leases_to_get, mac="05:02:0c:03:0a:00", pd=True)

    # Subnet statistics checks
    assert get_stat('subnet[1].reclaimed-leases')[0] == (leases_to_get if lease_remove_method == 'expire' else 0)
    assert get_stat('subnet[1].assigned-pds')[0] == leases_to_get
    assert get_stat('subnet[1].cumulative-assigned-pds')[0] == 2 * leases_to_get

    # Pool statistics checks
    assert get_stat('subnet[1].pd-pool[0].assigned-pds')[0] == pool_0_size
    assert get_stat('subnet[1].pd-pool[0].cumulative-assigned-pds')[0] == 2 * pool_0_size
    assert get_stat('subnet[1].pd-pool[0].reclaimed-leases')[0] == (pool_0_size if lease_remove_method == 'expire' else 0)
    assert get_stat('subnet[1].pd-pool[1].assigned-pds')[0] == pool_1_size
    assert get_stat('subnet[1].pd-pool[1].cumulative-assigned-pds')[0] == 2 * pool_1_size
    assert get_stat('subnet[1].pd-pool[1].reclaimed-leases')[0] == (pool_1_size if lease_remove_method == 'expire' else 0)
    assert get_stat('subnet[1].pd-pool[2].assigned-pds')[0] == pool_2_size
    assert get_stat('subnet[1].pd-pool[2].cumulative-assigned-pds')[0] == 2 * pool_2_size
    assert get_stat('subnet[1].pd-pool[2].reclaimed-leases')[0] == (pool_2_size if lease_remove_method == 'expire' else 0)


@pytest.mark.v6
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
    srv_control.config_srv_subnet('2001:db8:a:a:1::/64', f'2001:db8:a:a:1::1-2001:db8:a:a:1::{pool_0_A_size:x}', id=1)
    srv_control.new_pool(f'2001:db8:a:a:2::1-2001:db8:a:a:2::{pool_0_B_size:x}', 0)
    srv_control.new_pool(f'2001:db8:a:a:3::1-2001:db8:a:a:3::{pool_1_size:x}', 0, pool_id=1)
    srv_control.new_pool(f'2001:db8:a:a:4::1-2001:db8:a:a:4::{pool_2_size:x}', 0, pool_id=2)
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    # Probation period must be longer, than time required to Decline all leases
    srv_control.add_line({"decline-probation-period": int(leases_to_get * 0.4 + 1)})
    srv_control.disable_leases_affinity()
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.add_unix_socket()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    assert get_stat('subnet[1].pool[0].total-nas')[0] == pool_0_size
    assert get_stat('subnet[1].pool[1].total-nas')[0] == pool_1_size
    assert get_stat('subnet[1].pool[2].total-nas')[0] == pool_2_size

    # Get leases. We split into pools so we can decline them later.
    _get_leases(pool_0_A_size, mac="50:02:0c:03:0a:00")
    _get_leases(pool_0_B_size, mac="51:02:0c:03:0a:00")
    _get_leases(pool_1_size, mac="52:02:0c:03:0a:00")
    _get_leases(pool_2_size, mac="53:02:0c:03:0a:00")

    # Subnet statistics checks
    assert get_stat('subnet[1].assigned-nas')[0] == leases_to_get
    assert get_stat('subnet[1].cumulative-assigned-nas')[0] == leases_to_get
    assert get_stat('subnet[1].declined-addresses')[0] == 0

    # Pool statistics checks
    assert get_stat('subnet[1].pool[0].assigned-nas')[0] == pool_0_size
    assert get_stat('subnet[1].pool[0].cumulative-assigned-nas')[0] == pool_0_size
    assert get_stat('subnet[1].pool[0].declined-addresses')[0] == 0
    assert get_stat('subnet[1].pool[1].assigned-nas')[0] == pool_1_size
    assert get_stat('subnet[1].pool[1].cumulative-assigned-nas')[0] == pool_1_size
    assert get_stat('subnet[1].pool[1].declined-addresses')[0] == 0
    assert get_stat('subnet[1].pool[2].assigned-nas')[0] == pool_2_size
    assert get_stat('subnet[1].pool[2].cumulative-assigned-nas')[0] == pool_2_size
    assert get_stat('subnet[1].pool[2].declined-addresses')[0] == 0

    assert get_stat('subnet[1].declined-addresses')[0] == 0

    # Shorten wait after sending Decline messages - we don't expect responses
    world.cfg['wait_interval'] = 0.1

    _decline_leases(pool_0_A_size, mac="50:02:0c:03:0a:00", ip="2001:db8:a:a:1::0")
    _decline_leases(pool_0_B_size, mac="51:02:0c:03:0a:00", ip="2001:db8:a:a:2::0")
    _decline_leases(pool_1_size, mac="52:02:0c:03:0a:00", ip="2001:db8:a:a:3::0")
    _decline_leases(pool_2_size, mac="53:02:0c:03:0a:00", ip="2001:db8:a:a:4::0")

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
