"""Kea Hook hosts_cmds testing"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_control
import srv_msg

from forge_cfg import world


def _ra(address, options=None, response_type='ACK'):
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_copy_option('server_id')
    if not options or 'requested_addr' not in options:
        srv_msg.client_does_include_with_value('requested_addr', address)
    if options:
        for k, v in options.items():
            srv_msg.client_does_include_with_value(k, v)
    srv_msg.client_send_msg('REQUEST')

    srv_msg.send_wait_for_message('MUST', response_type)
    if response_type == 'ACK':
        srv_msg.response_check_content('yiaddr', address)
        srv_msg.response_check_include_option(1)
        srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


def _dora(address, options=None, exchange='full', response_type='ACK'):
    misc.test_procedure()
    if exchange == 'full':
        srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
        if options:
            for k, v in options.items():
                srv_msg.client_does_include_with_value(k, v)
        srv_msg.client_send_msg('DISCOVER')

        srv_msg.send_wait_for_message('MUST', 'OFFER')
        srv_msg.response_check_content('yiaddr', address)

        _ra(address, options, response_type)

    # This is supposed to be the renew scenario after DORA.
    _ra(address, options, response_type)


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize("channel", ['http', 'socket'])
def test_v4_hosts_cmds_libreload(channel):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation('MySQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _dora('192.168.50.50')

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "hw-address": "ff:01:02:03:ff:04",
                "ip-address": "192.168.50.100",
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)

    _dora('192.168.50.100')

    srv_msg.send_ctrl_cmd({"command": "libreload", "arguments": {}}, channel=channel)
    srv_msg.log_contains('HOST_CMDS_DEINIT_OK unloading Host Commands hooks library successful')
    srv_msg.log_contains('HOST_CMDS_INIT_OK loading Host Commands hooks library successful')

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "ip-address": "192.168.50.100",
            "subnet-id": 1
        },
        "command": "reservation-del"
    }, channel=channel)

    _dora('192.168.50.50')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v4_hosts_cmds_reconfigure(channel):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation('MySQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _dora('192.168.50.50')

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "hw-address": "ff:01:02:03:ff:04",
                "ip-address": "192.168.50.100",
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)

    _dora('192.168.50.100')

    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation('MySQL')

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'reconfigured')

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "hw-address": "ff:01:02:03:ff:04",
                "ip-address": "192.168.50.100",
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)

    _dora('192.168.50.100')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v4_hosts_cmds_add_reservation_mysql(channel):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation('MySQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _dora('192.168.50.50')

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "hw-address": "ff:01:02:03:ff:04",
                "ip-address": "192.168.50.100",
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)

    _dora('192.168.50.100')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v4_hosts_cmds_del_reservation_mysql(channel):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation('MySQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _dora('192.168.50.50')

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "hw-address": "ff:01:02:03:ff:04",
                "ip-address": "192.168.50.100",
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)

    _dora('192.168.50.100')

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "ip-address": "192.168.50.100",
            "subnet-id": 1
        },
        "command": "reservation-del"
    }, channel=channel)

    _dora('192.168.50.50')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v4_hosts_cmds_del_reservation_mysql_2(channel):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    # address reserved without using command
    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'ff:01:02:03:ff:04')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'MySQL', 1)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'MySQL', 1)
    srv_control.update_db_backend_reservation('ipv4_address', '192.168.50.100', 'MySQL', 1)
    srv_control.upload_db_reservation('MySQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _dora('192.168.50.100')

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "ip-address": "192.168.50.100",
            "subnet-id": 1
        },
        "command": "reservation-del"
    }, channel=channel)

    _dora('192.168.50.50')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v4_hosts_cmds_del_reservation_pgsql(channel):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation('PostgreSQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _dora('192.168.50.50')

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "hw-address": "ff:01:02:03:ff:04",
                "ip-address": "192.168.50.100",
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)

    _dora('192.168.50.100')

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "ip-address": "192.168.50.100",
            "subnet-id": 1
        },
        "command": "reservation-del"
    }, channel=channel)

    _dora('192.168.50.50')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v4_hosts_cmds_del_reservation_pgsql_2(channel):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    # address reserved without using command
    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'ff:01:02:03:ff:04')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'PostgreSQL', 1)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'PostgreSQL', 1)
    srv_control.update_db_backend_reservation('ipv4_address', '192.168.50.100', 'PostgreSQL', 1)
    srv_control.upload_db_reservation('PostgreSQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _dora('192.168.50.100')

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "ip-address": "192.168.50.100",
            "subnet-id": 1
        },
        "command": "reservation-del"
    }, channel=channel)

    _dora('192.168.50.50')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v4_hosts_cmds_add_reservation_pgsql(channel):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation('PostgreSQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _dora('192.168.50.50')

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "hw-address": "ff:01:02:03:ff:04",
                "ip-address": "192.168.50.100",
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)

    _dora('192.168.50.100')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v4_hosts_cmds_get_reservation_mysql(channel):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation('MySQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _dora('192.168.50.50')

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "hw-address": "ff:01:02:03:ff:04",
                "ip-address": "192.168.50.100",
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)

    _dora('192.168.50.100')

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "identifier": "ff:01:02:03:ff:04",
            "identifier-type": "hw-address",
            "subnet-id": 1
        },
        "command": "reservation-get"
    }, channel=channel)

    _dora('192.168.50.100')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v4_hosts_cmds_get_reservation_mysql_2(channel):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    # address reserved without using command
    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'ff:01:02:03:ff:04')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'MySQL', 1)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'MySQL', 1)
    srv_control.update_db_backend_reservation('ipv4_address', '192.168.50.100', 'MySQL', 1)
    srv_control.upload_db_reservation('MySQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _dora('192.168.50.100')

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "identifier": "ff:01:02:03:ff:04",
            "identifier-type": "hw-address",
            "subnet-id": 1
        },
        "command": "reservation-get"
    }, channel=channel)

    _dora('192.168.50.100')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v4_hosts_cmds_get_reservation_pgsql(channel):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation('PostgreSQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _dora('192.168.50.50')

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "hw-address": "ff:01:02:03:ff:04",
                "ip-address": "192.168.50.100",
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)

    _dora('192.168.50.100')

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "identifier": "ff:01:02:03:ff:04",
            "identifier-type": "hw-address",
            "subnet-id": 1
        },
        "command": "reservation-get"
    }, channel=channel)

    _dora('192.168.50.100')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v4_hosts_cmds_get_reservation_pgsql_2(channel):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'ff:01:02:03:ff:04')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'PostgreSQL', 1)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'PostgreSQL', 1)
    srv_control.update_db_backend_reservation('ipv4_address', '192.168.50.100', 'PostgreSQL', 1)
    srv_control.upload_db_reservation('PostgreSQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _dora('192.168.50.100')

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "identifier": "ff:01:02:03:ff:04",
            "identifier-type": "hw-address",
            "subnet-id": 1
        },
        "command": "reservation-get"
    }, channel=channel)

    _dora('192.168.50.100')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v4_hosts_cmds_add_reservation_mysql_flex_id(channel):
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_line({"host-reservation-identifiers": ["flex-id"]})
    srv_control.add_parameter_to_hook(2, 'identifier-expression', 'option[60].hex')

    srv_control.enable_db_backend_reservation('MySQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _dora('192.168.50.50', {'vendor_class_id': 'docsis3.0'})

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "flex-id": "'docsis3.0'",
                "ip-address": "192.168.50.100",
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)

    _dora('192.168.50.100', {'vendor_class_id': 'docsis3.0'})


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v4_hosts_cmds_add_reservation_mysql_flex_id_nak(channel):
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_line({"host-reservation-identifiers": ["flex-id"]})
    srv_control.add_parameter_to_hook(2, 'identifier-expression', 'option[60].hex')

    srv_control.enable_db_backend_reservation('MySQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _dora('192.168.50.50', {'vendor_class_id': 'docsis3.0'})

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "flex-id": "'docsis3.0'",
                "ip-address": "192.168.50.100",
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)

    _dora('192.168.50.100', {'requested_addr': '192.168.50.200',
                             'vendor_class_id': 'docsis3.0'},
          response_type='NAK')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v4_hosts_cmds_add_reservation_pgsql_flex_id(channel):
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_line({"host-reservation-identifiers": ["flex-id"]})
    srv_control.add_parameter_to_hook(2, 'identifier-expression', 'option[60].hex')

    srv_control.enable_db_backend_reservation('PostgreSQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _dora('192.168.50.50', {'vendor_class_id': 'docsis3.0'})

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "flex-id": "'docsis3.0'",
                "ip-address": "192.168.50.100",
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)

    _dora('192.168.50.100', {'vendor_class_id': 'docsis3.0'})


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v4_hosts_cmds_add_reservation_pgsql_flex_id_nak(channel):
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_line({"host-reservation-identifiers": ["flex-id"]})
    srv_control.add_parameter_to_hook(2, 'identifier-expression', 'option[60].hex')

    srv_control.enable_db_backend_reservation('PostgreSQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _dora('192.168.50.50', {'vendor_class_id': 'docsis3.0'})

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "flex-id": "'docsis3.0'",
                "ip-address": "192.168.50.100",
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)

    _dora('192.168.50.100', {'requested_addr': '192.168.50.200',
                             'vendor_class_id': 'docsis3.0'},
          response_type='NAK')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v4_hosts_cmds_add_reservation_complex_mysql(channel):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation('MySQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _dora('192.168.50.50')

    result = srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "boot-file-name": "/dev/null",
                "client-classes": [
                    "special_snowflake",
                    "office"
                ],
                "client-id": "01:0a:0b:0c:0d:0e:0f",
                "ip-address": "192.168.50.205",
                "next-server": "192.168.50.1",
                "option-data": [
                    {
                        "data": "10.1.1.202,10.1.1.203",
                        "name": "domain-name-servers"
                    }
                ],
                "server-hostname": "hal9000",
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)
    assert result['result'] == 0

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '01:0a:0b:0c:0d:0e:0f')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.205')
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, 'value', '10.1.1.203')
    srv_msg.response_check_option_content(6, 'value', '10.1.1.202')
    srv_msg.response_check_content('sname', 'hal9000')
    srv_msg.response_check_content('file', '/dev/null')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.205')
    srv_msg.client_does_include_with_value('client_id', '01:0a:0b:0c:0d:0e:0f')
    srv_msg.client_sets_value('Client', 'chaddr', '01:0a:0b:0c:0d:0e:0f')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.205')
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, 'value', '10.1.1.203')
    srv_msg.response_check_option_content(6, 'value', '10.1.1.202')
    srv_msg.response_check_content('sname', 'hal9000')
    srv_msg.response_check_content('file', '/dev/null')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v4_hosts_cmds_add_reservation_complex_pgsql(channel):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation('PostgreSQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _dora('192.168.50.50')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "boot-file-name": "/dev/null",
                "client-classes": [
                    "special_snowflake",
                    "office"
                ],
                "client-id": "01:0a:0b:0c:0d:0e:0f",
                "ip-address": "192.168.50.205",
                "next-server": "192.168.50.1",
                "option-data": [
                    {
                        "data": "10.1.1.202,10.1.1.203",
                        "name": "domain-name-servers"
                    }
                ],
                "server-hostname": "hal9000",
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)
    assert response['result'] == 0

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '01:0a:0b:0c:0d:0e:0f')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.205')
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, 'value', '10.1.1.203')
    srv_msg.response_check_option_content(6, 'value', '10.1.1.202')
    srv_msg.response_check_content('sname', 'hal9000')
    srv_msg.response_check_content('file', '/dev/null')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.205')
    srv_msg.client_does_include_with_value('client_id', '01:0a:0b:0c:0d:0e:0f')
    srv_msg.client_sets_value('Client', 'chaddr', '01:0a:0b:0c:0d:0e:0f')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.205')
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, 'value', '10.1.1.203')
    srv_msg.response_check_option_content(6, 'value', '10.1.1.202')
    srv_msg.response_check_content('sname', 'hal9000')
    srv_msg.response_check_content('file', '/dev/null')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v4_hosts_cmds_reservation_get_all(channel):
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24', '192.168.51.50-192.168.51.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname1',
                                           0,
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:01')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname2',
                                           0,
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:02')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname3',
                                           0,
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:03')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname4',
                                           1,
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:04')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname5',
                                           1,
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:05')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "subnet-id": 1
        },
        "command": "reservation-get-all"
    }, channel=channel)
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname1')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname2')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname3')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname4')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname5')
    srv_msg.json_response_parsing('text', None, '3 IPv4 host(s) found.')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v4_hosts_cmds_reservation_get_all_mysql(channel):
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24', '192.168.51.50-192.168.51.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_host_cmds.so')

    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname1', 'MySQL', 1)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'MySQL', 1)
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:02')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname2', 'MySQL', 2)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'MySQL', 2)
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:03')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname3', 'MySQL', 3)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'MySQL', 3)
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:04')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname4', 'MySQL', 4)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 2, 'MySQL', 4)
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:05')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname5', 'MySQL', 5)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 2, 'MySQL', 5)
    srv_control.upload_db_reservation('MySQL')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "subnet-id": 1
        },
        "command": "reservation-get-all"
    }, channel=channel)

    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname1')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname2')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname3')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname4')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname5')
    srv_msg.json_response_parsing('text', None, '3 IPv4 host(s) found.')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v4_hosts_cmds_reservation_get_all_pgsql(channel):
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24', '192.168.51.50-192.168.51.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_host_cmds.so')

    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname1', 'PostgreSQL', 1)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'PostgreSQL', 1)
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:02')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname2', 'PostgreSQL', 2)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'PostgreSQL', 2)
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:03')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname3', 'PostgreSQL', 3)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'PostgreSQL', 3)
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:04')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname4', 'PostgreSQL', 4)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 2, 'PostgreSQL', 4)
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:05')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname5', 'PostgreSQL', 5)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 2, 'PostgreSQL', 5)
    srv_control.upload_db_reservation('PostgreSQL')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "subnet-id": 1
        },
        "command": "reservation-get-all"
    }, channel=channel)

    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname1')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname2')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname3')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname4')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname5')
    srv_msg.json_response_parsing('text', None, '3 IPv4 host(s) found.')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v4_hosts_cmds_reservation_get_page(channel):
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24', '192.168.51.50-192.168.51.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_host_cmds.so')

    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname1',
                                           0,
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:01')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname2',
                                           0,
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:02')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname3',
                                           0,
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:03')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname4',
                                           1,
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:04')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname5',
                                           1,
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:05')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname6',
                                           0,
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:06')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname7',
                                           0,
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:07')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "limit": 3,
            "subnet-id": 1
        },
        "command": "reservation-get-page"
    }, channel=channel)
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname1')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname2')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname3')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname4')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname5')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname6')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname7')
    srv_msg.json_response_parsing('text', None, '3 IPv4 host(s) found.')

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "from": 3,
            "limit": 3,
            "subnet-id": 1
        },
        "command": "reservation-get-page"
    }, channel=channel)
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname6')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname7')
    srv_msg.json_response_parsing('text', None, '2 IPv4 host(s) found.')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v4_hosts_cmds_reservation_get_all_page_mysql(channel):
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24', '192.168.51.50-192.168.51.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_host_cmds.so')

    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname1', 'MySQL', 1)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'MySQL', 1)
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:02')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname2', 'MySQL', 2)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'MySQL', 2)
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:03')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname3', 'MySQL', 3)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'MySQL', 3)
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:04')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname4', 'MySQL', 4)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 2, 'MySQL', 4)
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:05')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname5', 'MySQL', 5)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 2, 'MySQL', 5)

    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:06')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname6', 'MySQL', 6)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'MySQL', 6)
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:07')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname7', 'MySQL', 7)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'MySQL', 7)

    srv_control.upload_db_reservation('MySQL')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "limit": 3,
            "subnet-id": 1
        },
        "command": "reservation-get-page"
    }, channel=channel)
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname7')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname6')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname3')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname4')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname5')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname1')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname2')
    srv_msg.json_response_parsing('text', None, '3 IPv4 host(s) found.')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v4_hosts_cmds_reservation_get_all_page_pgsql(channel):
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24', '192.168.51.50-192.168.51.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_host_cmds.so')

    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname1', 'PostgreSQL', 1)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'PostgreSQL', 1)
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:02')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname2', 'PostgreSQL', 2)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'PostgreSQL', 2)
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:03')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname3', 'PostgreSQL', 3)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'PostgreSQL', 3)
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:04')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname4', 'PostgreSQL', 4)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 2, 'PostgreSQL', 4)
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:05')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname5', 'PostgreSQL', 5)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 2, 'PostgreSQL', 5)

    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:06')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname6', 'PostgreSQL', 6)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'PostgreSQL', 6)
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:07')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname7', 'PostgreSQL', 7)
    srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, 'PostgreSQL', 7)

    srv_control.upload_db_reservation('PostgreSQL')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "limit": 3,
            "subnet-id": 1
        },
        "command": "reservation-get-page"
    }, channel=channel)
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname6')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname7')
    srv_msg.json_response_parsing('arguments', None, 'reserved-hostname3')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname4')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname5')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname1')
    srv_msg.json_response_parsing('arguments', 'NOT ', 'reserved-hostname2')
    srv_msg.json_response_parsing('text', None, '3 IPv4 host(s) found.')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
@pytest.mark.parametrize("hosts_db", ['MySQL', 'PostgreSQL'])
def test_v4_hosts_cmds_conflicts_duplicate_mac_reservations(channel, hosts_db):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(hosts_db)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "hw-address": "ff:01:02:03:ff:01",
                "ip-address": "192.168.50.10",
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)

    # the same DUID - it should fail
    srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "hw-address": "ff:01:02:03:ff:01",
                "ip-address": "192.168.50.11",
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel, exp_result=1)


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
@pytest.mark.parametrize("hosts_db", ['MySQL', 'PostgreSQL'])
def test_v4_hosts_cmds_conflicts_duplicate_ip_reservations(channel, hosts_db):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(hosts_db)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "hw-address": "ff:01:02:03:ff:01",
                "ip-address": "192.168.50.10",
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)

    # the same IP - it should fail
    srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "hw-address": "ff:01:02:03:ff:02",
                "ip-address": "192.168.50.10",
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel, exp_result=1)


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
@pytest.mark.parametrize("hosts_db", ['MySQL', 'PostgreSQL'])
def test_v4_hosts_cmds_duplicate_ip_reservations_allowed(channel, hosts_db):
    the_same_ip_address = '192.168.50.10'
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    # allow non-unique IP address in multiple reservations
    srv_control.set_conf_parameter_global('ip-reservations-unique', False)

    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(hosts_db)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "hw-address": "aa:aa:aa:aa:aa:aa",
                "ip-address": the_same_ip_address,
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)

    srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "hw-address": "bb:bb:bb:bb:bb:bb",
                "ip-address": the_same_ip_address,
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)

    # first request address by aa:aa:aa:aa:aa:aa
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'aa:aa:aa:aa:aa:aa')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', the_same_ip_address)

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', the_same_ip_address)
    srv_msg.client_sets_value('Client', 'chaddr', 'aa:aa:aa:aa:aa:aa')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', the_same_ip_address)
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    # release taken IP address
    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'ciaddr', the_same_ip_address)
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    # and now request address by bb:bb:bb:bb:bb:bb again, the IP should be the same ie. 192.168.50.10
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'bb:bb:bb:bb:bb:bb')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', the_same_ip_address)

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', the_same_ip_address)
    srv_msg.client_sets_value('Client', 'chaddr', 'bb:bb:bb:bb:bb:bb')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', the_same_ip_address)
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    # try to request address by aa:aa:aa:aa:aa:aa again, the IP address should be just
    # from the pool (ie. 192.168.50.1) as 192.168.50.10 is already taken by bb:bb:bb:bb:bb:bb
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'aa:aa:aa:aa:aa:aa')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_sets_value('Client', 'chaddr', 'aa:aa:aa:aa:aa:aa')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


# Test that the same client can migrate from a global reservation to an
# in-subnet reservation after only a simple Kea reconfiguration.
@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
@pytest.mark.parametrize('exchange', ['full', 'renew-only'])
@pytest.mark.parametrize('hosts_database', ['MySQL', 'PostgreSQL'])
def test_v4_hosts_cmds_global_to_in_subnet(channel, exchange, hosts_database):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.agent_control_channel()
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(hosts_database)

    # Enable both global and in-subnet reservations because we test both.
    world.dhcp_cfg.update({
        "reservations-global": True,
        "reservations-in-subnet": True,
        "reservations-out-of-pool": False,
    })

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Add a subnet.
    srv_msg.send_ctrl_cmd({
        "command": "subnet4-add",
        "arguments": {
            "subnet4": [
                {
                    "id": 1,
                    "interface": "$(SERVER_IFACE)",
                    "pools": [
                        {
                            "pool": "192.168.50.50-192.168.50.50"
                        }
                    ],
                    "subnet": "192.168.50.0/24"
                }
            ]
        }
    }, channel=channel)

    # First do the full exchange and expect an address from the pool.
    _dora('192.168.50.50', exchange='full')

    # Add a global reservation.
    srv_msg.send_ctrl_cmd({
        "command": "reservation-add",
        "arguments": {
            "reservation": {
                "subnet-id": 0,
                "hw-address": "ff:01:02:03:ff:04",
                "ip-address": "192.168.50.100"
            }
        }
    }, channel=channel)

    # Check that Kea leases the globally reserved address.
    _dora('192.168.50.100', exchange=exchange)

    # Remove the global reservation.
    srv_msg.send_ctrl_cmd({
        "command": "reservation-del",
        "arguments": {
            "subnet-id": 0,
            "ip-address": "192.168.50.100"
        }
    }, channel=channel)

    # Check that Kea has reverted to the default behavior.
    _dora('192.168.50.50', exchange=exchange)

    # Add an in-subnet reservation.
    srv_msg.send_ctrl_cmd({
        "command": "reservation-add",
        "arguments": {
            "reservation": {
                "subnet-id": 1,
                "hw-address": "ff:01:02:03:ff:04",
                "ip-address": "192.168.50.150"
            }
        }
    }, channel=channel)

    # Check that Kea leases the in-subnet reserved address.
    _dora('192.168.50.150', exchange=exchange)
