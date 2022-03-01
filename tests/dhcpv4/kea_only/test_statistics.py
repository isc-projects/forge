"""Kea Statistics"""

# pylint: disable=invalid-name,line-too-long

import time
import pytest

import srv_msg
import misc
import srv_control


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

    def compare(self):
        result = srv_msg.send_ctrl_cmd_via_socket('{"command":"statistic-get-all","arguments":{}}')
        statistics_from_kea = result['arguments']
        assert len(statistics_from_kea) == 31

        statistics_not_found = []
        for key, _ in self.s.items():
            if key not in statistics_from_kea:
                statistics_not_found.append(key)
        assert len(statistics_not_found) == 0, 'The following statistics were expected, but not received: %s' % statistics_not_found

        statistics_not_found = []
        for key in statistics_from_kea:
            if key not in self.s:
                statistics_not_found.append(key)
        assert len(statistics_not_found) == 0, 'The following statistics were received, but not expected: %s' % statistics_not_found

        for key, expected in self.s.items():
            received = statistics_from_kea[key][0][0]
            assert expected == received, 'stat %s: expected %s, received %s' % (key, expected, received)


def get_stat(name):
    cmd = '{"command": "statistic-get","arguments": {"name": "%s"}}' % name
    result = srv_msg.send_ctrl_cmd_via_socket(cmd)
    result = [r[0] for r in result['arguments'][name]]
    return result


@pytest.mark.v4
def test_stats_basic():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
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
        assert c in result['arguments']

    cnt = 0
    for c in result['arguments']:
        if c.startswith('statistic-'):
            cnt += 1
    assert len(stat_cmds) == cnt

    srv_msg.client_requests_option(1)
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

    misc.test_procedure()
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

    assert get_stat("declined-addresses") == [1, 0]
    assert get_stat("pkt4-ack-received") == [0]
    assert get_stat("pkt4-ack-sent") == [4, 3, 2, 1, 0]
    assert get_stat("pkt4-decline-received") == [1, 0]
    assert get_stat("pkt4-discover-received") == [3, 2, 1, 0]
    assert get_stat("pkt4-inform-received") == [1, 0]
    assert get_stat("pkt4-nak-received") == [0]
    assert get_stat("pkt4-nak-sent") == [0]
    assert get_stat("pkt4-offer-received") == [0]
    assert get_stat("pkt4-offer-sent") == [3, 2, 1, 0]
    assert get_stat("pkt4-parse-failed") == [0]
    assert get_stat("pkt4-receive-drop") == [0]
    assert get_stat("pkt4-received") == [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    assert get_stat("pkt4-request-received") == [3, 2, 1, 0]
    assert get_stat("pkt4-release-received") == [2, 1, 0]
    assert get_stat("pkt4-sent") == [7, 6, 5, 4, 3, 2, 1, 0]
    assert get_stat("pkt4-unknown-received") == [0]
    assert get_stat("reclaimed-declined-addresses") == [0]
    assert get_stat("reclaimed-leases") == [0]
    assert get_stat("subnet[1].assigned-addresses") == [1, 0, 1, 0, 1, 0]
    assert get_stat("subnet[1].declined-addresses") == [1, 0]
    assert get_stat("subnet[1].reclaimed-declined-addresses") == [0]
    assert get_stat("subnet[1].reclaimed-leases") == [0]
    assert get_stat("subnet[1].total-addresses") == [10]


@pytest.mark.v4
def test_stats_remove_reset():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    result = srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt4-received"}}')
    assert result['arguments']['pkt4-received'][0][0] == 0

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

    assert get_stat('pkt4-received') == [2, 1, 0]
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

    assert get_stat('pkt4-received') == [2, 1]
    srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-reset","arguments": {"name": "pkt4-received"}}')
    result = srv_msg.send_ctrl_cmd_via_socket('{"command": "statistic-get","arguments": {"name": "pkt4-received"}}')
    assert result['arguments']['pkt4-received'][0][0] == 0

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

    assert get_stat('pkt4-received') == [2, 1, 0]


@pytest.mark.v4
def test_stats_reconfigure():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    assert get_stat('pkt4-received') == [0]
    assert get_stat('subnet[1].total-addresses') == [10]

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    assert get_stat('pkt4-received') == [1, 0]

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.1-192.168.51.2')
    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()

    # reconfigure (reload) server, stats should be preserved
    srv_control.start_srv('DHCP', 'reconfigured')

    assert get_stat('pkt4-received') == [1, 0]
    assert get_stat('subnet[1].total-addresses') == [1]
    assert get_stat('subnet[2].total-addresses') == [2]

    # restart kea, now stats should be reset
    srv_control.start_srv('DHCP', 'restarted')

    assert get_stat('pkt4-received') == [0]
    assert get_stat('subnet[1].total-addresses') == [1]
    assert get_stat('subnet[2].total-addresses') == [2]


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

    assert get_stat('pkt4-received') == [0]
    assert get_stat('subnet[1].total-addresses') == [10]

    misc.test_procedure()
    for _ in range(3):
        srv_msg.client_requests_option(1)
        srv_msg.client_send_msg('DISCOVER')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'OFFER')

    assert get_stat('pkt4-received') == [3, 2]


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

    assert get_stat('pkt4-received') == [0]
    assert get_stat('subnet[1].total-addresses') == [10]

    misc.test_procedure()
    for _ in range(3):
        srv_msg.client_requests_option(1)
        srv_msg.client_send_msg('DISCOVER')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'OFFER')

    time.sleep(1)

    assert get_stat('pkt4-received') == [3]


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
