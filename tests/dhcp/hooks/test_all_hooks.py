# Copyright (C) 2022-2025 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea All Hooks"""

# pylint: disable=line-too-long

import pytest

from src import misc
from src import srv_msg
from src import srv_control

from src.forge_cfg import world
from src.protosupport.multi_protocol_functions import file_contains_line
from src.protosupport.multi_protocol_functions import log_contains, log_doesnt_contain
from src.softwaresupport.multi_server_functions import fabric_sudo_command


@pytest.mark.v4
@pytest.mark.hook
def test_v4_all_hooks_start():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    # flex id
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           0,
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '192.168.50.10')
    srv_control.add_line({"host-reservation-identifiers": ["flex-id", "hw-address"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook("libdhcp_flex_id.so", 'identifier-expression', 'option[60].hex')
    # legal log
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_hooks('libdhcp_stat_cmds.so')
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.add_hooks('libdhcp_host_cache.so')
    srv_control.add_hooks('libdhcp_lease_cmds.so')

    srv_control.add_hooks('libdhcp_ha.so')
    srv_control.add_parameter_to_ha_hook('this-server-name', '"server1"')
    srv_control.add_parameter_to_ha_hook('mode', '"load-balancing"')
    srv_control.add_parameter_to_ha_hook('heartbeat-delay', 1000)
    srv_control.add_parameter_to_ha_hook('max-response-delay', 1001)
    srv_control.add_parameter_to_ha_hook('max-unacked-clients', 0)
    srv_control.add_parameter_to_ha_hook('max-ack-delay', 0)

    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server1","url":"http://$(MGMT_ADDRESS):8080/","role":"primary","auto-failover":true}')
    srv_control.add_parameter_to_ha_hook('peers',
                                         '{"name":"server2","url":"http://$(MGMT_ADDRESS):8080/","role":"secondary","auto-failover":true}')

    srv_control.add_unix_socket()
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')
    srv_msg.send_ctrl_cmd_via_socket({"command": "list-commands", "arguments": {}})


@pytest.mark.v4
@pytest.mark.hook
def test_v4_all_hooks_test_cooperation():
    srv_msg.remove_file_from_server(world.f_cfg.log_join('kea-legal*.txt'))

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    # flex id
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname',
                                           0,
                                           'flex-id',
                                           '\'docsis3.0\'')
    srv_control.host_reservation_in_subnet_add_value(0, 0, 'ip-address', '192.168.50.10')
    srv_control.add_line({"host-reservation-identifiers": ["flex-id", "hw-address"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook("libdhcp_flex_id.so", 'identifier-expression', 'option[60].hex')
    # legal log
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    # Add hooks library located libdhcp_host_cmds.so.
    # Add hooks library located libdhcp_stat_cmds.so.
    # Add hooks library located libdhcp_subnet_cmds.so.
    # Add hooks library located libdhcp_host_cache.so.
    #
    # Add High-Availability hook library located libdhcp_ha.so.
    # To HA hook configuration add this-server-name with value: "server1"
    # To HA hook configuration add mode with value: "load-balancing"
    # To HA hook configuration add heartbeat-delay with value: 1000
    # To HA hook configuration add max-response-delay with value: 1001
    # To HA hook configuration add max-unacked-clients with value: 0
    # To HA hook configuration add max-ack-delay with value: 0
    #
    # To HA hook configuration add peers with value: {"name":"server1","url":"http://$(MGMT_ADDRESS):8080/","role":"primary","auto-failover":true}
    # To HA hook configuration add peers with value: {"name":"server2","url":"http://$(MGMT_ADDRESS_2):8080/","role":"secondary","auto-failover":true}

    srv_control.add_unix_socket()
    srv_control.add_http_control_channel(host_port='8080')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # Using UNIX socket on server in path control_socket send {"command": "list-commands","arguments": {}}
    # JSON response in arguments MUST include value: build-report
    # JSON response in arguments MUST include value: cache-clear
    # JSON response in arguments MUST include value: cache-flush
    # JSON response in arguments MUST include value: cache-get
    # JSON response in arguments MUST include value: cache-insert
    # JSON response in arguments MUST include value: cache-load
    # JSON response in arguments MUST include value: cache-remove
    # JSON response in arguments MUST include value: cache-write
    # JSON response in arguments MUST include value: config-get
    # JSON response in arguments MUST include value: config-reload
    # JSON response in arguments MUST include value: config-set
    # JSON response in arguments MUST include value: config-test
    # JSON response in arguments MUST include value: config-write
    # JSON response in arguments MUST include value: dhcp-disable
    # JSON response in arguments MUST include value: dhcp-enable
    # JSON response in arguments MUST include value: ha-continue
    # JSON response in arguments MUST include value: ha-heartbeat
    # JSON response in arguments MUST include value: ha-scopes
    # JSON response in arguments MUST include value: ha-sync
    # JSON response in arguments MUST include value: lease4-add
    # JSON response in arguments MUST include value: lease4-del
    # JSON response in arguments MUST include value: lease4-get
    # JSON response in arguments MUST include value: lease4-get-all
    # JSON response in arguments MUST include value: lease4-get-page
    # JSON response in arguments MUST include value: lease4-update
    # JSON response in arguments MUST include value: lease4-wipe
    # JSON response in arguments MUST include value: lease6-add
    # JSON response in arguments MUST include value: lease6-del
    # JSON response in arguments MUST include value: lease6-get
    # JSON response in arguments MUST include value: lease6-get-all
    # JSON response in arguments MUST include value: lease6-get-page
    # JSON response in arguments MUST include value: lease6-update
    # JSON response in arguments MUST include value: lease6-wipe
    # JSON response in arguments MUST include value: leases-reclaim
    # JSON response in arguments MUST include value: libreload
    # JSON response in arguments MUST include value: list-commands
    # JSON response in arguments MUST include value: network4-add
    # JSON response in arguments MUST include value: network4-del
    # JSON response in arguments MUST include value: network4-get
    # JSON response in arguments MUST include value: network4-list
    # JSON response in arguments MUST include value: network4-subnet-add
    # JSON response in arguments MUST include value: network4-subnet-del
    # JSON response in arguments MUST include value: network6-add
    # JSON response in arguments MUST include value: network6-del
    # JSON response in arguments MUST include value: network6-get
    # JSON response in arguments MUST include value: network6-list
    # JSON response in arguments MUST include value: network6-subnet-add
    # JSON response in arguments MUST include value: network6-subnet-del
    # JSON response in arguments MUST include value: reservation-add
    # JSON response in arguments MUST include value: reservation-del
    # JSON response in arguments MUST include value: reservation-get
    # JSON response in arguments MUST include value: shutdown
    # JSON response in arguments MUST include value: stat-lease4-get
    # JSON response in arguments MUST include value: stat-lease6-get
    # JSON response in arguments MUST include value: statistic-get
    # JSON response in arguments MUST include value: statistic-get-all
    # JSON response in arguments MUST include value: statistic-remove
    # JSON response in arguments MUST include value: statistic-remove-all
    # JSON response in arguments MUST include value: statistic-reset
    # JSON response in arguments MUST include value: statistic-reset-all
    # JSON response in arguments MUST include value: subnet4-add
    # JSON response in arguments MUST include value: subnet4-del
    # JSON response in arguments MUST include value: subnet4-get
    # JSON response in arguments MUST include value: subnet4-list
    # JSON response in arguments MUST include value: subnet6-add
    # JSON response in arguments MUST include value: subnet6-del
    # JSON response in arguments MUST include value: subnet6-get
    # JSON response in arguments MUST include value: subnet6-list
    # JSON response in arguments MUST include value: version-get
    # ha command
    # Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
    # JSON response in arguments MUST include value: "state": "partner-down"
    # flex-id
    misc.test_procedure()
    srv_msg.client_does_include_with_value('vendor_class_id', 'docsis3.0')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')

    # legal log
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(54)
    srv_msg.response_check_include_option(61)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')

    srv_msg.copy_remote(world.f_cfg.log_join('kea-legal*.txt'))

    file_contains_line(world.f_cfg.log_join('kea-legal*.txt'),
                       'Address: 192.168.50.1 has been assigned for 1 hrs 6 mins '
                       '40 secs to a device with hardware address: hwtype=1 '
                       'ff:01:02:03:ff:04, client-id: 00:01:02:03:04:05:06')

    # lease commands
    srv_msg.send_ctrl_cmd_via_socket('{"command":"lease4-add","arguments":{"ip-address": "192.168.50.10","hostname": "newhostname.example.org","hw-address": "1a:1b:1c:1d:1e:1f","subnet-id":1,"valid-lft":500000}}')
    file_contains_line(world.f_cfg.log_join('kea-legal*.txt'),
                       'Administrator added a lease of address: 192.168.50.10 to a '
                       'device with hardware address: 1a:1b:1c:1d:1e:1f for 5 days '
                       '18 hrs 53 mins 20 secs')

    #
    # Test Procedure:
    # Client sets chaddr value to 1a:1b:1c:1d:1e:1f.
    # Client sets ciaddr value to 192.168.50.10.
    # Client copies server_id option from received message.
    # Client sends REQUEST message.
    #
    # Pass Criteria:
    # Server MUST respond with ACK message.
    # Response MUST contain yiaddr 192.168.50.10.
    # Response MUST include option 54.
    # Response option 54 MUST contain value $(SRV4_ADDR).
    srv_msg.copy_remote(world.f_cfg.log_join('kea-legal*.txt'))


@pytest.mark.v4
@pytest.mark.hook
@pytest.mark.parametrize("hook", ["nonexistent", "existing", "invalid", "valid"])
def test_v4_hooks_path_configfile(hook):
    """Test is Kea restricting path that hooks can be loaded from.

    :param hook: state of hook file and it's path.
    :type hook: str
    """
    if hook == "nonexistent":
        srv_msg.remove_file_from_server(world.f_cfg.hooks_join('libdhcp_nonexistent.so'))
        path = "libdhcp_nonexistent.so"
        message = 'HOOKS_OPEN_ERROR failed to open hook library .*'
        anti_message = 'HOOKS_LOAD_SUCCESS \'load\' function in hook library .* returned success'
        should_succeed = False
    elif hook == "existing":
        srv_msg.remove_file_from_server('/tmp/libdhcp_legal_log.so')
        fabric_sudo_command(f'cp {world.f_cfg.hooks_join("libdhcp_legal_log.so")} /tmp/libdhcp_legal_log.so')
        path = "/tmp/libdhcp_legal_log.so"
        message = 'DHCP4_PARSER_FAIL failed to create or run parser for configuration element hooks-libraries: ' \
            'hooks library configuration error: invalid path specified: \'/tmp\''
        anti_message = 'HOOKS_LOAD_SUCCESS \'load\' function in hook library .* returned success'
        should_succeed = False
    elif hook == "invalid":
        srv_msg.remove_file_from_server('/tmp/libdhcp_invalid.so')
        fabric_sudo_command("echo 'fake content' > /tmp/libdhcp_invalid.so")
        path = "/tmp/libdhcp_invalid.so"
        message = 'DHCP4_PARSER_FAIL failed to create or run parser for configuration element hooks-libraries: ' \
            'hooks library configuration error: invalid path specified: \'/tmp\''
        anti_message = 'HOOKS_LOAD_SUCCESS \'load\' function in hook library .* returned success'
        should_succeed = False
    else:
        path = world.f_cfg.hooks_join('libdhcp_legal_log.so')
        message = 'HOOKS_LOAD_SUCCESS \'load\' function in hook library .* returned success'
        anti_message = 'DHCP4_PARSER_FAIL failed to create or run parser for configuration element hooks-libraries: ' \
            'hooks library configuration error: invalid path specified: \'/tmp\''
        should_succeed = True

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')

    srv_control.add_hooks(path)

    srv_control.add_unix_socket()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started', should_succeed=should_succeed)

    log_contains(message)
    log_doesnt_contain(anti_message)


@pytest.mark.v4
@pytest.mark.hook
@pytest.mark.parametrize("hook", ["nonexistent", "existing", "invalid", "valid"])
def test_v4_hooks_path_config_set(hook):
    """Test is Kea restricting path that hooks can be loaded from.

    :param hook: state of hook file and it's path.
    :type hook: str
    """
    if hook == "nonexistent":
        srv_msg.remove_file_from_server(world.f_cfg.hooks_join('libdhcp_nonexistent.so'))
        path = "libdhcp_nonexistent.so"
        message = 'hooks libraries failed to validate'
        exp_result = 1
    elif hook == "existing":
        srv_msg.remove_file_from_server('/tmp/libdhcp_legal_log.so')
        fabric_sudo_command(f'cp {world.f_cfg.hooks_join("libdhcp_legal_log.so")} /tmp/libdhcp_legal_log.so')
        path = "/tmp/libdhcp_legal_log.so"
        message = 'hooks library configuration error: invalid path specified:'
        exp_result = 1
    elif hook == "invalid":
        srv_msg.remove_file_from_server('/tmp/libdhcp_invalid.so')
        fabric_sudo_command("echo 'fake content' > /tmp/libdhcp_invalid.so")
        path = "/tmp/libdhcp_invalid.so"
        message = 'hooks library configuration error: invalid path specified:'
        exp_result = 1
    else:
        path = world.f_cfg.hooks_join('libdhcp_legal_log.so')
        message = 'Configuration successful.'
        exp_result = 0

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')

    srv_control.add_unix_socket()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    config = srv_msg.send_ctrl_cmd({"command": "config-get", "service": ["dhcp4"], "arguments": {}},
                                   'socket')['arguments']
    del config['hash']
    config['Dhcp4']["hooks-libraries"] = [
        {
            "library": path
        }
    ]
    response = srv_msg.send_ctrl_cmd({"command": "config-set", "service": ["dhcp4"], "arguments": config},
                                     'socket', exp_result=exp_result)
    assert message in response['text']
