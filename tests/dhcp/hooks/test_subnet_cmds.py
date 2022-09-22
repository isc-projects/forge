"""Kea Subnet manipulation commands"""

# pylint: disable=invalid-name,line-too-long

import pytest

from src import srv_control
from src import srv_msg
from src import misc
from src.forge_cfg import world

from src.softwaresupport.cb_model import setup_server_for_config_backend_cmds


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_list():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.config_srv_another_subnet_no_interface('10.0.0.0/24', '10.0.0.5-10.0.0.5')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet4-get","arguments":{"id": 234}}',
                                     exp_result=3)  # expect no such subnet i.e. 3


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_get_by_id():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.config_srv_another_subnet_no_interface('10.0.0.0/24', '10.0.0.5-10.0.0.5')
    srv_control.config_srv_another_subnet_no_interface('150.0.0.0/24', '150.0.0.5-150.0.0.5')
    srv_control.config_srv('streettalk-directory-assistance-server', 2, '199.1.1.1,200.1.1.2')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet4-get","arguments":{"id":3}}')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_get_by_subnet():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.config_srv_another_subnet_no_interface('10.0.0.0/24', '10.0.0.5-10.0.0.5')
    srv_control.config_srv('domain-name-servers', 1, '199.199.199.1,100.100.100.1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet4-get","arguments":{"subnet":"10.0.0.0/24"}}')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_add():
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.config_srv_opt('domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    # Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/etc/kea/control_socket send {"command":"subnet4-list","arguments":{}}
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet4-add","arguments":{"subnet4":[{"subnet":"192.168.50.0/24","interface":"$(SERVER_IFACE)","id":234,"pools":[{"pool":"192.168.50.1-192.168.50.1"}]}]}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet4-get","arguments":{"id": 234}}')
    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_add_with_options():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '$(EMPTY)')
    srv_control.config_srv_opt('domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(6, 'value', '100.100.100.1')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    # Using UNIX socket on server in path control_socket send {"command":"subnet4-list","arguments":{}}
    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet4-add","arguments": {"subnet4": [{"subnet": "192.168.51.0/24","interface": "$(SERVER_IFACE)","id": 234,"pools": [{"pool": "192.168.51.1-192.168.51.1"}],"option-data": [{"csv-format": true,"code": 6,"data": "19.19.19.1,10.10.10.1","name": "domain-name-servers","space": "dhcp4"}]}]}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet4-get","arguments":{"id": 234}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet4-del","arguments":{"id":1}}')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, 'value', '19.19.19.1')
    srv_msg.response_check_option_content(6, 'value', '10.10.10.1')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_add_conflict():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.config_srv_opt('domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    # Using UNIX socket on server in path control_socket send {"command":"subnet4-list","arguments":{}}
    srv_msg.send_ctrl_cmd_via_socket({"command": "subnet4-add",
                                      "arguments": {"subnet4": [{"subnet": "192.168.55.0/24",
                                                                 "interface": "$(SERVER_IFACE)",
                                                                 "id": 1,
                                                                 "pools": [{"pool": "192.168.55.1-192.168.55.1"}],
                                                                 "option-data": [{"csv-format": True,
                                                                                  "code": 6,
                                                                                  "data": "19.19.19.1,10.10.10.1",
                                                                                  "name": "domain-name-servers",
                                                                                  "space": "dhcp4"}]}]}},
                                     exp_result=1)
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet4-get","arguments":{"id": 1}}')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_del():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.config_srv_opt('domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet4-del","arguments":{"id":1}}')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_del_non_existing():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.config_srv_opt('domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet4-del","arguments":{"id":2}}',
                                     exp_result=3)  # it does not exists

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_del_global_options():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.51.0/24', '192.168.51.1-192.168.51.1')
    srv_control.config_srv_opt('domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.51.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet4-del","arguments":{"id":1}}')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    # That needs subnet with empty pool to work
    # Test Procedure:
    # Client requests option 6.
    # Client sets ciaddr value to $(CIADDR).
    # Client sends INFORM message.
    #
    # Pass Criteria:
    # Server MUST respond with ACK message.
    # Response MUST include option 6.
    # Response option 6 MUST contain value 199.199.199.1.
    # Response option 6 MUST contain value 100.100.100.1.


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v4_subnet_cmds_add_and_del():
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.config_srv_opt('domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet4-add","arguments":{"subnet4":[{"subnet":"192.168.50.0/24","interface":"$(SERVER_IFACE)","id":66,"pools":[{"pool":"192.168.50.1-192.168.50.1"}]}]}}')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet4-del","arguments":{"id":66}}')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()


# Test that an user can increase a fully-allocated subnet through the use of
# subnet commands.
@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_hook_v4_subnet_grow_subnet_command(channel):
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'subnet4': [
                {
                    'id': 42,
                    'interface': '$(SERVER_IFACE)',
                    'pools': [
                        {
                            'pool': '192.168.50.1-192.168.50.1'
                        }
                    ],
                    'subnet': '192.168.50.0/24'
                }
            ]
        },
        'command': 'subnet4-add'
    }, channel=channel)
    assert response == {
        'arguments': {
            'subnets': [
                {
                    'id': 42,
                    'subnet': '192.168.50.0/24'
                }
            ]
        },
        'result': 0,
        'text': 'IPv4 subnet added'
    }

    srv_msg.DORA('192.168.50.1')

    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'id': 42
        },
        'command': 'subnet4-del'
    }, channel=channel)
    assert response == {
        'arguments': {
            'subnets': [
                {
                    'id': 42,
                    'subnet': '192.168.50.0/24'
                }
            ]
        },
        'result': 0,
        'text': 'IPv4 subnet 192.168.50.0/24 (id 42) deleted'
    }

    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'subnet4': [
                {
                    'id': 42,
                    'interface': '$(SERVER_IFACE)',
                    'pools': [
                        {
                            'pool': '192.168.50.1-192.168.50.2'
                        }
                    ],
                    'subnet': '192.168.50.0/24'
                }
            ]
        },
        'command': 'subnet4-add'
    }, channel=channel)
    assert response == {
        'arguments': {
            'subnets': [
                {
                    'id': 42,
                    'subnet': '192.168.50.0/24'
                }
            ]
        },
        'result': 0,
        'text': 'IPv4 subnet added'
    }

    srv_msg.DORA('192.168.50.1', exchange='renew-only')

    srv_msg.DORA('192.168.50.2', chaddr='ff:01:02:03:ff:11')


# Test that an user can increase a fully-allocated subnet through the use of
# config backend commands.
@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_hook_v4_subnet_grow_cb_command(channel):
    misc.test_setup()
    if channel == 'http':
        srv_control.agent_control_channel()

    setup_server_for_config_backend_cmds(config_control={'config-fetch-wait-time': 1}, force_reload=False)

    srv_control.start_srv('DHCP', 'started')

    srv_msg.wait_for_message_in_log('DHCPSRV_CFGMGR_CONFIG4_MERGED Configuration backend data has been merged.',
                                    count=2, timeout=7)

    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'remote': {
                'type': 'mysql'
            },
            'server-tags': ['all'],
            'subnets': [
                {
                    'id': 42,
                    'interface': '$(SERVER_IFACE)',
                    'pools': [
                        {
                            'pool': '192.168.50.1-192.168.50.1'
                        }
                    ],
                    'shared-network-name': None,
                    'subnet': '192.168.50.0/24'
                }
            ]
        },
        'command': 'remote-subnet4-set'
    }, channel=channel)
    assert response == {
        'arguments': {
            'subnets': [
                {
                    'id': 42,
                    'subnet': '192.168.50.0/24'
                }
            ]
        },
        'result': 0,
        'text': 'IPv4 subnet successfully set.'
    }

    srv_msg.wait_for_message_in_log('DHCPSRV_CFGMGR_CONFIG4_MERGED Configuration backend data has been merged.', 3)

    srv_msg.DORA('192.168.50.1')

    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'remote': {
                'type': 'mysql'
            },
            'subnets': [
                {
                    'id': 42
                }
            ]
        },
        'command': 'remote-subnet4-del-by-id'
    }, channel=channel)
    assert response == {
        'arguments': {
            'count': 1
        },
        'result': 0,
        'text': '1 IPv4 subnet(s) deleted.'
    }

    srv_msg.wait_for_message_in_log('DHCPSRV_CFGMGR_CONFIG4_MERGED Configuration backend data has been merged.', 4)

    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'remote': {
                'type': 'mysql'
            },
            'server-tags': ['all'],
            'subnets': [
                {
                    'id': 42,
                    'interface': '$(SERVER_IFACE)',
                    'pools': [
                        {
                            'pool': '192.168.50.1-192.168.50.2'
                        }
                    ],
                    'shared-network-name': None,
                    'subnet': '192.168.50.0/24'
                }
            ]
        },
        'command': 'remote-subnet4-set'
    }, channel=channel)
    assert response == {
        'arguments': {
            'subnets': [
                {
                    'id': 42,
                    'subnet': '192.168.50.0/24'
                }
            ]
        },
        'result': 0,
        'text': 'IPv4 subnet successfully set.'
    }

    srv_msg.wait_for_message_in_log('DHCPSRV_CFGMGR_CONFIG4_MERGED Configuration backend data has been merged.', 5)

    srv_msg.DORA('192.168.50.1', exchange='renew-only')

    srv_msg.DORA('192.168.50.2', chaddr='ff:01:02:03:ff:11')


@pytest.mark.v4
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_hook_v4_subnet_delta_add(backend):
    """
    Test subnet4-delta-add command by adding a subnet and then modifying and adding options.
    Forge makes DORA exchanges to verify returned parameters.
    """
    misc.test_setup()
    srv_control.agent_control_channel()
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')

    if backend == 'memfile':
        srv_control.build_and_send_config_files()
        srv_control.start_srv('DHCP', 'started')
    else:
        setup_server_for_config_backend_cmds(backend_type=backend, **world.dhcp_cfg)

    cmd = {
        "arguments":
            {"subnet4": [
                {"subnet": "192.168.50.0/24",
                 "interface": "$(SERVER_IFACE)",
                 "id": 234,
                 "valid-lifetime": 4000,
                 "max-valid-lifetime": 4000,
                 "min-valid-lifetime": 1000,
                 "pools": [
                     {
                         "pool": "192.168.50.1-192.168.50.10"
                     }
                 ],
                 "option-data": [
                     {
                         "csv-format": True,
                         "code": 6,
                         "data": "19.19.19.1,10.10.10.1",
                         "name": "domain-name-servers",
                         "space": "dhcp4"}
                 ]
                 }
            ]
            },
        "command": "subnet4-add"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')
    assert response == {
        "arguments": {
            "subnets": [
                {
                    "id": 234,
                    "subnet": "192.168.50.0/24"
                }
            ]
        },
        "result": 0,
        "text": "IPv4 subnet added"
    }

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, 'value', '19.19.19.1')
    srv_msg.response_check_option_content(6, 'value', '10.10.10.1')
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', '4000')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option(6)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, 'value', '19.19.19.1')
    srv_msg.response_check_option_content(6, 'value', '10.10.10.1')
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', '4000')

    cmd = {
        "arguments":
            {"subnet4": [
                {"subnet": "192.168.50.0/24",
                 "id": 234,
                 "valid-lifetime": 2000,
                 "option-data": [
                     {
                         "csv-format": True,
                         "code": 6,
                         "data": "21.21.21.1,20.20.20.1",
                         "name": "domain-name-servers",
                         "space": "dhcp4"}
                 ]
                 }
            ]
            },
        "command": "subnet4-delta-add"}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')
    assert response == {
        "arguments": {
            "subnets": [
                {
                    "id": 234,
                    "subnet": "192.168.50.0/24"
                }
            ]
        },
        "result": 0,
        "text": "IPv4 subnet updated"
    }

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_requests_option(6)
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:05')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.2')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, 'value', '21.21.21.1')
    srv_msg.response_check_option_content(6, 'value', '20.20.20.1')
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', '2000')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.2')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:05')
    srv_msg.client_requests_option(6)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.2')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, 'value', '21.21.21.1')
    srv_msg.response_check_option_content(6, 'value', '20.20.20.1')
    srv_msg.response_check_include_option(51)
    srv_msg.response_check_option_content(51, 'value', '2000')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_list():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.config_srv_another_subnet_no_interface('1000::/32', '1000::5-1000::5')
    srv_control.config_srv_another_subnet_no_interface('3000::/100', '3000::5-3000::5')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-list","arguments":{}}')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_get_by_id():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.config_srv_another_subnet_no_interface('1000::/32', '1000::5-1000::5')
    srv_control.config_srv_another_subnet_no_interface('3000::/100', '3000::5-3000::5')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-get","arguments":{"id":2}}')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_get_by_subnet():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.config_srv_another_subnet_no_interface('1000::/32', '1000::5-1000::5')
    srv_control.config_srv_another_subnet_no_interface('3000::/100', '3000::5-3000::5')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-get","arguments":{"subnet":"3000::/100"}}')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_add():
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.config_srv_opt('preference', '123')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-list","arguments":{}}', exp_result=3)
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-get","arguments":{"id": 234}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_add_with_options():
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.config_srv_opt('preference', '123')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)

    misc.test_procedure()
    srv_msg.client_requests_option(7)
    srv_msg.client_requests_option(24)
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 123)
    srv_msg.response_check_include_option(24)
    srv_msg.response_check_option_content(24, 'domains', 'domain1.example.com.,domain2.isc.org.')

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-list","arguments":{}}', exp_result=3)
    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}],"option-data":[{"csv-format":true,"code":7,"data":"55","name":"preference","space":"dhcp6"}]}]}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-get","arguments":{"id": 234}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_requests_option(24)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 55)
    srv_msg.response_check_include_option(24)
    srv_msg.response_check_option_content(24, 'domains', 'domain1.example.com.,domain2.isc.org.')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_add_conflict():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.config_srv_opt('preference', '123')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-list","arguments":{}}')
    response = srv_msg.send_ctrl_cmd_via_socket({"command": "subnet6-add",
                                                 "arguments": {"subnet6": [{"id": 1,
                                                                            "interface": "$(SERVER_IFACE)",
                                                                            "subnet": "2002:db8:1::/64",
                                                                            "pools": [{"pool": "2002:db8:1::10-2002:db8:1::20"}]}]}},
                                                exp_result=1)
    assert response['text'] == "ID of the new IPv6 subnet '1' is already in use"
    response = srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-get","arguments":{"id": 1}}')
    assert response['arguments']['subnet6'][0]['subnet'] == '2001:db8:1::/64'

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_del():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-list","arguments":{}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet6-del","arguments":{"id":1}}')
    # Using UNIX socket on server in path control_socket send {"command": "subnet6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-get","arguments":{"id": 1}}', exp_result=3)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_del_non_existing():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-list","arguments":{}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet6-del","arguments":{"id":2}}', exp_result=3)
    # Using UNIX socket on server in path control_socket send {"command": "subnet6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_del_global_options():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.config_srv_opt('preference', '123')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 123)

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-list","arguments":{}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet6-del","arguments":{"id":1}}')
    # Using UNIX socket on server in path control_socket send {"command": "subnet6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-get","arguments":{"id": 1}}', exp_result=3)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)

    misc.test_procedure()
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 123)


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
def test_hook_v6_subnet_cmds_add_and_del():
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.config_srv_opt('preference', '123')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)

    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-list","arguments":{}}', exp_result=3)
    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}')
    srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-get","arguments":{"id": 234}}')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.send_ctrl_cmd_via_socket('{"command": "subnet6-del","arguments":{"id":234}}')
    # Using UNIX socket on server in path control_socket send {"command": "subnet6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}
    response = srv_msg.send_ctrl_cmd_via_socket('{"command":"subnet6-get","arguments":{"id": 234}}', exp_result=3)
    assert response['text'] == 'No subnet with id 234 found'

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)


# Test that an user can increase a fully-allocated subnet through the use of
# subnet commands.
@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_hook_v6_subnet_grow_subnet_command(channel):
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "subnet6": [
                {
                    "id": 42,
                    "interface": "$(SERVER_IFACE)",
                    "pools": [
                        {
                            "pool": "2001:db8:1::1-2001:db8:1::1"
                        }
                    ],
                    "subnet": "2001:db8:1::/64"
                }
            ]
        },
        "command": "subnet6-add"
    }, channel=channel)
    assert response == {
        'arguments': {
            'subnets': [
                {
                    'id': 42,
                    'subnet': '2001:db8:1::/64'
                }
            ]
        },
        'result': 0,
        'text': 'IPv6 subnet added'
    }

    srv_msg.SARR('2001:db8:1::1')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "id": 42
        },
        "command": "subnet6-del"
    }, channel=channel)
    assert response == {
        'arguments': {
            'subnets': [
                {
                    'id': 42,
                    'subnet': '2001:db8:1::/64'
                }
            ]
        },
        'result': 0,
        'text': 'IPv6 subnet 2001:db8:1::/64 (id 42) deleted'
    }

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "subnet6": [
                {
                    "id": 42,
                    "interface": "$(SERVER_IFACE)",
                    "pools": [
                        {
                            "pool": "2001:db8:1::1-2001:db8:1::2"
                        }
                    ],
                    "subnet": "2001:db8:1::/64"
                }
            ]
        },
        "command": "subnet6-add"
    }, channel=channel)
    assert response == {
        'arguments': {
            'subnets': [
                {
                    'id': 42,
                    "subnet": "2001:db8:1::/64"
                }
            ]
        },
        'result': 0,
        'text': 'IPv6 subnet added'
    }

    srv_msg.SARR('2001:db8:1::1', exchange='renew-only')

    srv_msg.SARR('2001:db8:1::2', duid='00:03:00:01:f6:f5:f4:f3:f2:11')


# Test that an user can increase a fully-allocated subnet through the use of
# config backend commands.
@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.hook
@pytest.mark.subnet_cmds
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_hook_v6_subnet_grow_cb_command(channel):
    misc.test_setup()
    if channel == 'http':
        srv_control.agent_control_channel()

    setup_server_for_config_backend_cmds(config_control={'config-fetch-wait-time': 1}, force_reload=False)

    srv_control.start_srv('DHCP', 'started')

    srv_msg.wait_for_message_in_log('DHCPSRV_CFGMGR_CONFIG6_MERGED Configuration backend data has been merged.', 2)

    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'remote': {
                'type': 'mysql'
            },
            'server-tags': ['all'],
            'subnets': [
                {
                    'id': 42,
                    'interface': '$(SERVER_IFACE)',
                    'pools': [
                        {
                            'pool': '2001:db8:1::1-2001:db8:1::1'
                        }
                    ],
                    'shared-network-name': None,
                    'subnet': '2001:db8:1::/64'
                }
            ]
        },
        'command': 'remote-subnet6-set'
    }, channel=channel)
    assert response == {
        'arguments': {
            'subnets': [
                {
                    'id': 42,
                    'subnet': '2001:db8:1::/64'
                }
            ]
        },
        'result': 0,
        'text': 'IPv6 subnet successfully set.'
    }

    srv_msg.wait_for_message_in_log('DHCPSRV_CFGMGR_CONFIG6_MERGED Configuration backend data has been merged.', 3)

    srv_msg.SARR('2001:db8:1::1')

    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'remote': {
                'type': 'mysql'
            },
            'subnets': [
                {
                    'id': 42
                }
            ]
        },
        'command': 'remote-subnet6-del-by-id'
    }, channel=channel)
    assert response == {
        'arguments': {
            'count': 1
        },
        'result': 0,
        'text': '1 IPv6 subnet(s) deleted.'
    }

    srv_msg.wait_for_message_in_log('DHCPSRV_CFGMGR_CONFIG6_MERGED Configuration backend data has been merged.', 4)

    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'remote': {
                'type': 'mysql'
            },
            'server-tags': ['all'],
            'subnets': [
                {
                    'id': 42,
                    'interface': '$(SERVER_IFACE)',
                    'pools': [
                        {
                            'pool': '2001:db8:1::1-2001:db8:1::2'
                        }
                    ],
                    'shared-network-name': None,
                    'subnet': '2001:db8:1::/64'
                }
            ]
        },
        'command': 'remote-subnet6-set'
    }, channel=channel)
    assert response == {
        'arguments': {
            'subnets': [
                {
                    'id': 42,
                    'subnet': '2001:db8:1::/64'
                }
            ]
        },
        'result': 0,
        'text': 'IPv6 subnet successfully set.'
    }

    srv_msg.wait_for_message_in_log('DHCPSRV_CFGMGR_CONFIG6_MERGED Configuration backend data has been merged.', 5)

    srv_msg.SARR('2001:db8:1::1', exchange='renew-only')

    srv_msg.SARR('2001:db8:1::2', duid='00:03:00:01:f6:f5:f4:f3:f2:11')
