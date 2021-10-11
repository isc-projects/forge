"""Kea Hook hosts_cmds testing"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_control
import srv_msg

from dhcp4_scen import DHCPv6_STATUS_CODES
from forge_cfg import world
from protosupport.multi_protocol_functions import is_superset_of


def _check_IA_NA(address, status_code=DHCPv6_STATUS_CODES['Success']):
    srv_msg.response_check_include_option('IA_NA')
    # RFC 8415: If the Status Code option does not appear in a
    # message in which the option could appear, the status of the message
    # is assumed to be Success.
    if srv_msg.get_suboption('status-code', 'IA_NA'):
        srv_msg.response_check_suboption_content('status-code', 'IA_NA', 'statuscode', status_code)
    else:
        assert status_code == DHCPv6_STATUS_CODES['Success'], \
            'status code missing so implied Success, but expected {}'.format(status_code)

    if status_code == DHCPv6_STATUS_CODES['Success']:
        srv_msg.response_check_option_content('IA_NA', 'sub-option', 'IA_address')
        srv_msg.response_check_suboption_content('IA_address', 'IA_NA', 'addr', address)


def _sarr(address, relay_information=False, status_code=DHCPv6_STATUS_CODES['Success'], exchange='full'):
    if exchange == 'full':
        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_does_include('Client', 'IA_Address')
        srv_msg.client_does_include('Client', 'IA-NA')
        srv_msg.client_send_msg('SOLICIT')

        if relay_information:
            srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8:1::1000')
            srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'port1234')
            srv_msg.client_does_include('RelayAgent', 'interface-id')
            srv_msg.create_relay_forward()

            misc.pass_criteria()
            srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
            srv_msg.response_check_include_option('interface-id')
            srv_msg.response_check_include_option('relay-msg')
            srv_msg.response_check_option_content('relay-msg', 'Relayed', 'Message')
            srv_msg.response_check_include_option('client-id')
            srv_msg.response_check_include_option('server-id')
            _check_IA_NA(address)
        else:
            misc.pass_criteria()
            srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
            _check_IA_NA(address, status_code)

            srv_msg.client_copy_option('server-id')
            srv_msg.client_copy_option('IA_NA')
            srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
            srv_msg.client_does_include('Client', 'client-id')
            if status_code == DHCPv6_STATUS_CODES['NoAddrsAvail']:
                srv_msg.client_sets_value('Client', 'IA_Address', '3000::1')
            srv_msg.client_send_msg('REQUEST')

            misc.pass_criteria()
            srv_msg.send_wait_for_message('MUST', 'REPLY')
            _check_IA_NA(address, status_code)

    # @todo: Investigate why Kea doesn't respond to renews when RelayAgent is
    # used.
    if not relay_information:
        srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
        srv_msg.client_copy_option('IA_NA')
        srv_msg.client_copy_option('server-id')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_add_saved_option()
        if status_code == DHCPv6_STATUS_CODES['NoAddrsAvail']:
            srv_msg.client_sets_value('Client', 'IA_Address', '3000::1')
        srv_msg.client_send_msg('RENEW')

        srv_msg.send_wait_for_message('MUST', 'REPLY')
        _check_IA_NA(address, status_code)


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v6_hosts_cmds_libreload(channel):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation('MySQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _sarr('2001:db8:1::50')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
                "ip-addresses": [
                    "2001:db8:1::100"
                ],
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)
    assert response == {
        "result": 0,
        "text": "Host added."
    }

    _sarr('2001:db8:1::100')

    response = srv_msg.send_ctrl_cmd({"command": "libreload", "arguments": {}}, channel=channel)
    assert response == {
        "result": 0,
        "text": "Hooks libraries successfully reloaded."
    }

    srv_msg.log_contains('HOST_CMDS_DEINIT_OK unloading Host Commands hooks library successful')
    srv_msg.log_contains('HOST_CMDS_INIT_OK loading Host Commands hooks library successful')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "ip-address": "2001:db8:1::100",
            "subnet-id": 1
        },
        "command": "reservation-del"
    }, channel=channel)
    assert response == {
        "result": 0,
        "text": "Host deleted."
    }

    _sarr('2001:db8:1::50')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v6_hosts_cmds_reconfigure(channel):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation('MySQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _sarr('2001:db8:1::50')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
                "ip-addresses": [
                    "2001:db8:1::100"
                ],
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)
    assert response == {
        "result": 0,
        "text": "Host added."
    }

    _sarr('2001:db8:1::100')

    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation('MySQL')

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'reconfigured')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
                "ip-addresses": [
                    "2001:db8:1::100"
                ],
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)
    assert response == {
        "result": 0,
        "text": "Host added."
    }

    _sarr('2001:db8:1::100')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v6_hosts_cmds_add_reservation_mysql(channel):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation('MySQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _sarr('2001:db8:1::50')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
                "ip-addresses": [
                    "2001:db8:1::100"
                ],
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)
    assert response == {
        "result": 0,
        "text": "Host added."
    }

    _sarr('2001:db8:1::100')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v6_hosts_cmds_del_reservation_mysql(channel):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation('MySQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _sarr('2001:db8:1::50')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
                "ip-addresses": [
                    "2001:db8:1::100"
                ],
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)
    assert response == {
        "result": 0,
        "text": "Host added."
    }

    _sarr('2001:db8:1::100')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "ip-address": "2001:db8:1::100",
            "subnet-id": 1
        },
        "command": "reservation-del"
    }, channel=channel)
    assert response == {
        "result": 0,
        "text": "Host deleted."
    }

    _sarr('2001:db8:1::50')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v6_hosts_cmds_del_reservation_mysql_2(channel):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    # address reserved without using command
    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'MySQL', 1)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'MySQL', 1)
    srv_control.ipv6_address_db_backend_reservation('2001:db8:1::100', '$(EMPTY)', 'MySQL', 1)
    srv_control.upload_db_reservation('MySQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _sarr('2001:db8:1::100')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "ip-address": "2001:db8:1::100",
            "subnet-id": 1
        },
        "command": "reservation-del"
    }, channel=channel)
    assert response == {
        "result": 0,
        "text": "Host deleted."
    }

    _sarr('2001:db8:1::50')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v6_hosts_cmds_del_reservation_pgsql(channel):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation('PostgreSQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _sarr('2001:db8:1::50')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
                "ip-addresses": [
                    "2001:db8:1::100"
                ],
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)
    assert response == {
        "result": 0,
        "text": "Host added."
    }

    _sarr('2001:db8:1::100')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "ip-address": "2001:db8:1::100",
            "subnet-id": 1
        },
        "command": "reservation-del"
    }, channel=channel)
    assert response == {
        "result": 0,
        "text": "Host deleted."
    }

    _sarr('2001:db8:1::50')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v6_hosts_cmds_del_reservation_pgsql_2(channel):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    # address reserved without using command
    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'PostgreSQL', 1)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'PostgreSQL', 1)
    srv_control.ipv6_address_db_backend_reservation('2001:db8:1::100', '$(EMPTY)', 'PostgreSQL', 1)
    srv_control.upload_db_reservation('PostgreSQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _sarr('2001:db8:1::100')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "ip-address": "2001:db8:1::100",
            "subnet-id": 1
        },
        "command": "reservation-del"
    }, channel=channel)
    assert response == {
        "result": 0,
        "text": "Host deleted."
    }

    _sarr('2001:db8:1::50')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v6_hosts_cmds_add_reservation_pgsql(channel):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation('PostgreSQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _sarr('2001:db8:1::50')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
                "ip-addresses": [
                    "2001:db8:1::100"
                ],
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)
    assert response == {
        "result": 0,
        "text": "Host added."
    }

    _sarr('2001:db8:1::100')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v6_hosts_cmds_get_reservation_mysql(channel):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation('MySQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _sarr('2001:db8:1::50')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
                "ip-addresses": [
                    "2001:db8:1::100"
                ],
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)
    assert response == {
        "result": 0,
        "text": "Host added."
    }

    _sarr('2001:db8:1::100')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "identifier": "00:03:00:01:f6:f5:f4:f3:f2:01",
            "identifier-type": "duid",
            "subnet-id": 1
        },
        "command": "reservation-get"
    }, channel=channel)
    assert response == {
        "arguments": {
            "client-classes": [],
            "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
            "hostname": "",
            "ip-addresses": ["2001:db8:1::100"],
            "option-data": [],
            "prefixes": []
        },
        "result": 0,
        "text": "Host found."
    }

    _sarr('2001:db8:1::100')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v6_hosts_cmds_get_reservation_mysql_2(channel):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    # address reserved without using command
    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.new_db_backend_reservation('MySQL', 'duid', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'MySQL', 1)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'MySQL', 1)
    srv_control.ipv6_address_db_backend_reservation('2001:db8:1::100', '$(EMPTY)', 'MySQL', 1)
    srv_control.upload_db_reservation('MySQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _sarr('2001:db8:1::100')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "identifier": "00:03:00:01:f6:f5:f4:f3:f2:01",
            "identifier-type": "duid",
            "subnet-id": 1
        },
        "command": "reservation-get"
    }, channel=channel)
    assert response == {
        "arguments": {
            "client-classes": [],
            "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
            "hostname": "reserved-hostname",
            "ip-addresses": ["2001:db8:1::100"],
            "option-data": [],
            "prefixes": []
        },
        "result": 0,
        "text": "Host found."
    }

    _sarr('2001:db8:1::100')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v6_hosts_cmds_get_reservation_pgsql(channel):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation('PostgreSQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _sarr('2001:db8:1::50')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
                "ip-addresses": [
                    "2001:db8:1::100"
                ],
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)
    assert response == {
        "result": 0,
        "text": "Host added."
    }

    _sarr('2001:db8:1::100')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "identifier": "00:03:00:01:f6:f5:f4:f3:f2:01",
            "identifier-type": "duid",
            "subnet-id": 1
        },
        "command": "reservation-get"
    }, channel=channel)
    assert response == {
        "arguments": {
            "client-classes": [],
            "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
            "hostname": "",
            "ip-addresses": ["2001:db8:1::100"],
            "option-data": [],
            "prefixes": []
        },
        "result": 0,
        "text": "Host found."
    }

    _sarr('2001:db8:1::100')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v6_hosts_cmds_get_reservation_pgsql_2(channel):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    # address reserved without using command
    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.new_db_backend_reservation('PostgreSQL', 'duid', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', 'PostgreSQL', 1)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'PostgreSQL', 1)
    srv_control.ipv6_address_db_backend_reservation('2001:db8:1::100', '$(EMPTY)', 'PostgreSQL', 1)
    srv_control.upload_db_reservation('PostgreSQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _sarr('2001:db8:1::100')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "identifier": "00:03:00:01:f6:f5:f4:f3:f2:01",
            "identifier-type": "duid",
            "subnet-id": 1
        },
        "command": "reservation-get"
    }, channel=channel)
    assert response == {
        "arguments": {
            "client-classes": [],
            "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
            "hostname": "reserved-hostname",
            "ip-addresses": ["2001:db8:1::100"],
            "option-data": [],
            "prefixes": []
        },
        "result": 0,
        "text": "Host found."
    }

    _sarr('2001:db8:1::100')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v6_hosts_cmds_add_reservation_mysql_flex_id(channel):
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_line({"host-reservation-identifiers": ["flex-id"]})
    srv_control.add_parameter_to_hook(2, 'identifier-expression', 'relay6[0].option[18].hex')

    srv_control.enable_db_backend_reservation('MySQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _sarr('2001:db8:1::50', relay_information=True)

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "flex-id": "'port1234'",
                "ip-addresses": [
                    "2001:db8:1::100"
                ],
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)
    assert response == {
        "result": 0,
        "text": "Host added."
    }

    _sarr('2001:db8:1::100', relay_information=True)


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v6_hosts_cmds_add_reservation_mysql_flex_id_NoAddressAvail(channel):
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_line({"host-reservation-identifiers": ["flex-id"]})
    srv_control.add_parameter_to_hook(2, 'identifier-expression', 'relay6[0].option[18].hex')

    srv_control.enable_db_backend_reservation('MySQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _sarr('2001:db8:1::50', relay_information=True)

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "flex-id": "'port1234'",
                "ip-addresses": [
                    "2001:db8:1::100"
                ],
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)
    assert response == {
        "result": 0,
        "text": "Host added."
    }

    _sarr('2001:db8:1::100', relay_information=True, status_code=DHCPv6_STATUS_CODES['NoAddrsAvail'])


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v6_hosts_cmds_add_reservation_pgsql_flex_id(channel):
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_line({"host-reservation-identifiers": ["flex-id"]})
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_parameter_to_hook(2, 'identifier-expression', 'relay6[0].option[18].hex')

    srv_control.enable_db_backend_reservation('PostgreSQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _sarr('2001:db8:1::50', relay_information=True)

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "flex-id": "'port1234'",
                "ip-addresses": [
                    "2001:db8:1::100"
                ],
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)
    assert response == {
        "result": 0,
        "text": "Host added."
    }

    _sarr('2001:db8:1::100', relay_information=True)


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v6_hosts_cmds_add_reservation_pgsql_flex_id_NoAddressAvail(channel):
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_line({"host-reservation-identifiers": ["flex-id"]})
    srv_control.add_parameter_to_hook(2, 'identifier-expression', 'relay6[0].option[18].hex')

    srv_control.enable_db_backend_reservation('PostgreSQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _sarr('2001:db8:1::50', relay_information=True)

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "flex-id": "'port1234'",
                "ip-addresses": [
                    "2001:db8:1::100"
                ],
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)
    assert response == {
        "result": 0,
        "text": "Host added."
    }

    _sarr('2001:db8:1::100', relay_information=True, status_code=DHCPv6_STATUS_CODES['NoAddrsAvail'])


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v6_hosts_cmds_add_reservation_complex_mysql(channel):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation('PostgreSQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    _check_IA_NA('2001:db8:1::50')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
                "hostname": "foo.example.com",
                "ip-addresses": [
                    "2001:db8:1:0:cafe::1"
                ],
                "option-data": [
                    {
                        "data": "4491",
                        "name": "vendor-opts"
                    },
                    {
                        "data": "3000:1::234",
                        "name": "tftp-servers",
                        "space": "vendor-4491"
                    }
                ],
                "prefixes": [
                    "2001:db8:2:abcd::/64"
                ],
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)
    assert response == {
        "result": 0,
        "text": "Host added."
    }

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    _check_IA_NA('2001:db8:1:0:cafe::1')

    srv_msg.response_check_include_option(25)
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:2:abcd::')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v6_hosts_cmds_add_reservation_complex_pgsql(channel):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation('PostgreSQL')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    _check_IA_NA('2001:db8:1::50')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
                "hostname": "foo.example.com",
                "ip-addresses": [
                    "2001:db8:1:0:cafe::1"
                ],
                "option-data": [
                    {
                        "data": "4491",
                        "name": "vendor-opts"
                    },
                    {
                        "data": "3000:1::234",
                        "name": "tftp-servers",
                        "space": "vendor-4491"
                    }
                ],
                "prefixes": [
                    "2001:db8:2:abcd::/64"
                ],
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)
    assert response == {
        "result": 0,
        "text": "Host added."
    }

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    _check_IA_NA('2001:db8:1:0:cafe::1')

    srv_msg.response_check_include_option(25)
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:2:abcd::')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v6_hosts_cmds_reservation_get_all(channel):
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_another_subnet_no_interface('3001::/64', '3001::1-3001::ff')
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

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "subnet-id": 1
        },
        "command": "reservation-get-all"
    }, channel=channel)

    assert response == {
        "arguments": {
            "hosts": [
                {
                    "client-classes": [],
                    "hostname": "reserved-hostname1",
                    "hw-address": "f6:f5:f4:f3:f2:01",
                    "ip-addresses": [],
                    "option-data": [],
                    "prefixes": []
                },
                {
                    "client-classes": [],
                    "hostname": "reserved-hostname2",
                    "hw-address": "f6:f5:f4:f3:f2:02",
                    "ip-addresses": [],
                    "option-data": [],
                    "prefixes": []
                },
                {
                    "client-classes": [],
                    "hostname": "reserved-hostname3",
                    "hw-address": "f6:f5:f4:f3:f2:03",
                    "ip-addresses": [],
                    "option-data": [],
                    "prefixes": []
                }
            ]
        },
        "result": 0,
        "text": "3 IPv6 host(s) found."
    }


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v6_hosts_cmds_reservation_get_all_mysql(channel):
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_another_subnet_no_interface('3001::/64', '3001::1-3001::ff')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_host_cmds.so')

    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname1', 'MySQL', 1)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'MySQL', 1)
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:02')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname2', 'MySQL', 2)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'MySQL', 2)
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:03')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname3', 'MySQL', 3)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'MySQL', 3)
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:04')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname4', 'MySQL', 4)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 2, 'MySQL', 4)
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:05')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname5', 'MySQL', 5)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 2, 'MySQL', 5)
    srv_control.upload_db_reservation('MySQL')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "subnet-id": 1
        },
        "command": "reservation-get-all"
    }, channel=channel)

    assert response == {
        "arguments": {
            "hosts": [
                {
                    "client-classes": [],
                    "hostname": "reserved-hostname3",
                    "hw-address": "f6:f5:f4:f3:f2:03",
                    "ip-addresses": [],
                    "option-data": [],
                    "prefixes": []
                },
                {
                    "client-classes": [],
                    "hostname": "reserved-hostname2",
                    "hw-address": "f6:f5:f4:f3:f2:02",
                    "ip-addresses": [],
                    "option-data": [],
                    "prefixes": []
                },
                {
                    "client-classes": [],
                    "hostname": "reserved-hostname1",
                    "hw-address": "f6:f5:f4:f3:f2:01",
                    "ip-addresses": [],
                    "option-data": [],
                    "prefixes": []
                }
            ]
        },
        "result": 0,
        "text": "3 IPv6 host(s) found."
    }


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v6_hosts_cmds_reservation_get_all_pgsql(channel):
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_another_subnet_no_interface('3001::/64', '3001::1-3001::ff')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_host_cmds.so')

    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname1', 'PostgreSQL', 1)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'PostgreSQL', 1)
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:02')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname2', 'PostgreSQL', 2)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'PostgreSQL', 2)
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:03')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname3', 'PostgreSQL', 3)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'PostgreSQL', 3)
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:04')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname4', 'PostgreSQL', 4)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 2, 'PostgreSQL', 4)
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:05')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname5', 'PostgreSQL', 5)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 2, 'PostgreSQL', 5)
    srv_control.upload_db_reservation('PostgreSQL')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "subnet-id": 1
        },
        "command": "reservation-get-all"
    }, channel=channel)

    assert response == {
        "arguments": {
            "hosts": [
                {
                    "client-classes": [],
                    "hostname": "reserved-hostname3",
                    "hw-address": "f6:f5:f4:f3:f2:03",
                    "ip-addresses": [],
                    "option-data": [],
                    "prefixes": []
                },
                {
                    "client-classes": [],
                    "hostname": "reserved-hostname2",
                    "hw-address": "f6:f5:f4:f3:f2:02",
                    "ip-addresses": [],
                    "option-data": [],
                    "prefixes": []
                },
                {
                    "client-classes": [],
                    "hostname": "reserved-hostname1",
                    "hw-address": "f6:f5:f4:f3:f2:01",
                    "ip-addresses": [],
                    "option-data": [],
                    "prefixes": []
                }
            ]
        },
        "result": 0,
        "text": "3 IPv6 host(s) found."
    }


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v6_hosts_cmds_reservation_get_page(channel):
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_another_subnet_no_interface('3001::/64', '3001::1-3001::ff')
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

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "limit": 3,
            "subnet-id": 1
        },
        "command": "reservation-get-page"
    }, channel=channel)

    assert response == {
        "arguments": {
            "count": 3,
            "hosts": [
                {
                    "client-classes": [],
                    "hostname": "reserved-hostname1",
                    "hw-address": "f6:f5:f4:f3:f2:01",
                    "ip-addresses": [],
                    "option-data": [],
                    "prefixes": []
                },
                {
                    "client-classes": [],
                    "hostname": "reserved-hostname2",
                    "hw-address": "f6:f5:f4:f3:f2:02",
                    "ip-addresses": [],
                    "option-data": [],
                    "prefixes": []
                },
                {
                    "client-classes": [],
                    "hostname": "reserved-hostname3",
                    "hw-address": "f6:f5:f4:f3:f2:03",
                    "ip-addresses": [],
                    "option-data": [],
                    "prefixes": []
                }
            ],
            "next": {
                "from": 3,
                "source-index": 0
            }
        },
        "result": 0,
        "text": "3 IPv6 host(s) found."
    }

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "from": 3,
            "limit": 3,
            "subnet-id": 1
        },
        "command": "reservation-get-page"
    }, channel=channel)

    assert response == {
        "arguments": {
            "count": 2,
            "hosts": [
                {
                    "client-classes": [],
                    "hostname": "reserved-hostname6",
                    "hw-address": "f6:f5:f4:f3:f2:06",
                    "ip-addresses": [],
                    "option-data": [],
                    "prefixes": []
                },
                {
                    "client-classes": [],
                    "hostname": "reserved-hostname7",
                    "hw-address": "f6:f5:f4:f3:f2:07",
                    "ip-addresses": [],
                    "option-data": [],
                    "prefixes": []
                }
            ],
            "next": {
                "from": 5,
                "source-index": 0
            }
        },
        "result": 0,
        "text": "2 IPv6 host(s) found."
    }


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v6_hosts_cmds_reservation_get_all_page_mysql(channel):
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_another_subnet_no_interface('3001::/64', '3001::1-3001::ff')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_host_cmds.so')

    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname1', 'MySQL', 1)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'MySQL', 1)
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:02')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname2', 'MySQL', 2)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'MySQL', 2)
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:03')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname3', 'MySQL', 3)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'MySQL', 3)
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:04')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname4', 'MySQL', 4)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 2, 'MySQL', 4)
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:05')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname5', 'MySQL', 5)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 2, 'MySQL', 5)

    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:06')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname6', 'MySQL', 6)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'MySQL', 6)
    srv_control.new_db_backend_reservation('MySQL', 'hw-address', 'f6:f5:f4:f3:f2:07')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname7', 'MySQL', 7)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'MySQL', 7)

    srv_control.upload_db_reservation('MySQL')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "limit": 3,
            "subnet-id": 1
        },
        "command": "reservation-get-page"
    }, channel=channel)

    # is_superset_of is used instead of equality because the next.from field
    # varies between test runs.
    assert is_superset_of(response, {
        "arguments": {
            "count": 3,
            "hosts": [
                {
                    "client-classes": [],
                    "hostname": "reserved-hostname7",
                    "hw-address": "f6:f5:f4:f3:f2:07",
                    "ip-addresses": [],
                    "option-data": [],
                    "prefixes": []
                },
                {
                    "client-classes": [],
                    "hostname": "reserved-hostname6",
                    "hw-address": "f6:f5:f4:f3:f2:06",
                    "ip-addresses": [],
                    "option-data": [],
                    "prefixes": []
                },
                {
                    "client-classes": [],
                    "hostname": "reserved-hostname3",
                    "hw-address": "f6:f5:f4:f3:f2:03",
                    "ip-addresses": [],
                    "option-data": [],
                    "prefixes": []
                }
            ],
            "next": {
                "source-index": 1
            }
        },
        "result": 0,
        "text": "3 IPv6 host(s) found."
    })


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v6_hosts_cmds_reservation_get_all_page_pgsql(channel):
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_another_subnet_no_interface('3001::/64', '3001::1-3001::ff')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_host_cmds.so')

    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname1', 'PostgreSQL', 1)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'PostgreSQL', 1)
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:02')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname2', 'PostgreSQL', 2)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'PostgreSQL', 2)
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:03')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname3', 'PostgreSQL', 3)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'PostgreSQL', 3)
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:04')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname4', 'PostgreSQL', 4)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 2, 'PostgreSQL', 4)
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:05')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname5', 'PostgreSQL', 5)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 2, 'PostgreSQL', 5)

    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:06')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname6', 'PostgreSQL', 6)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'PostgreSQL', 6)
    srv_control.new_db_backend_reservation('PostgreSQL', 'hw-address', 'f6:f5:f4:f3:f2:07')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname7', 'PostgreSQL', 7)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, 'PostgreSQL', 7)

    srv_control.upload_db_reservation('PostgreSQL')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "limit": 3,
            "subnet-id": 1
        },
        "command": "reservation-get-page"
    }, channel=channel)

    # is_superset_of is used instead of equality because the next.from field
    # varies between test runs.
    assert is_superset_of(response, {
        "arguments": {
            "count": 3,
            "hosts": [
                {
                    "client-classes": [],
                    "hostname": "reserved-hostname7",
                    "hw-address": "f6:f5:f4:f3:f2:07",
                    "ip-addresses": [],
                    "option-data": [],
                    "prefixes": []
                },
                {
                    "client-classes": [],
                    "hostname": "reserved-hostname6",
                    "hw-address": "f6:f5:f4:f3:f2:06",
                    "ip-addresses": [],
                    "option-data": [],
                    "prefixes": []
                },
                {
                    "client-classes": [],
                    "hostname": "reserved-hostname3",
                    "hw-address": "f6:f5:f4:f3:f2:03",
                    "ip-addresses": [],
                    "option-data": [],
                    "prefixes": []
                }
            ],
            "next": {
                "source-index": 1
            }
        },
        "result": 0,
        "text": "3 IPv6 host(s) found."
    })


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
@pytest.mark.parametrize("hosts_db", ['MySQL', 'PostgreSQL'])
def test_v6_host_reservation_conflicts_duplicate_duid_reservations(channel, hosts_db):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('3000::/30', '3000::1-3000::10')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(hosts_db)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
                "ip-addresses": [
                    "3000::5"
                ],
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)
    assert response == {
        "result": 0,
        "text": "Host added."
    }

    # the same DUID - it should fail
    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
                "ip-addresses": [
                    "3000::6"
                ],
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel, exp_result=1)
    assert response == {
        "result": 1,
        "text": "Database duplicate entry error"
    }


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
@pytest.mark.parametrize("hosts_db", ['MySQL', 'PostgreSQL'])
def test_v6_host_reservation_conflicts_duplicate_ip_reservations(channel, hosts_db):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('3000::/30', '3000::1-3000::10')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(hosts_db)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
                "ip-addresses": [
                    "3000::5"
                ],
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)
    assert response == {
        "result": 0,
        "text": "Host added."
    }

    # the same IP - it should fail
    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "duid": "00:03:00:01:f6:f5:f4:f3:f2:02",
                "ip-addresses": [
                    "3000::5"
                ],
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel, exp_result=1)
    assert response == {
        "result": 1,
        "text": "Database duplicate entry error"
    }


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
@pytest.mark.parametrize("hosts_db", ['MySQL', 'PostgreSQL'])
def test_v6_host_reservation_duplicate_ip_reservations_allowed(channel, hosts_db):
    the_same_ip_address = '3000::5'
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('3000::/30', '3000::1-3000::10')
    # allow non-unique IP address in multiple reservations
    srv_control.set_conf_parameter_global('ip-reservations-unique', False)
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(hosts_db)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
                "ip-addresses": [
                    "3000::5"
                ],
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)
    assert response == {
        "result": 0,
        "text": "Host added."
    }

    # the same IP - it should fail
    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "duid": "00:03:00:01:f6:f5:f4:f3:f2:02",
                "ip-addresses": [
                    "3000::5"
                ],
                "subnet-id": 1
            }
        },
        "command": "reservation-add"
    }, channel=channel)
    assert response == {
        "result": 0,
        "text": "Host added."
    }

    # first request address by 00:03:00:01:f6:f5:f4:f3:f2:01
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    _check_IA_NA(the_same_ip_address)

    # release taken IP address
    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    # and now request address by 00:03:00:01:f6:f5:f4:f3:f2:02 again, the IP should be the same ie. 3000::5
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    _check_IA_NA(the_same_ip_address)

    # try to request address by 00:03:00:01:f6:f5:f4:f3:f2:01 again, the IP address should be just
    # from the pool (ie. 3000::1) as 3000::5 is already taken by 00:03:00:01:f6:f5:f4:f3:f2:02
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    _check_IA_NA('3000::1')


# Test that the same client can migrate from a global reservation to an
# in-subnet reservation after only a simple Kea reconfiguration.
@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
@pytest.mark.parametrize('exchange', ['full', 'renew-only'])
@pytest.mark.parametrize('hosts_database', ['MySQL', 'PostgreSQL'])
def test_v6_hosts_cmds_global_to_in_subnet(channel, exchange, hosts_database):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
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
    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "subnet6": [
                {
                    "id": 1,
                    "interface": "$(SERVER_IFACE)",
                    "pools": [
                        {
                            "pool": "2001:db8:a::50-2001:db8:a::50"
                        }
                    ],
                    "subnet": "2001:db8:a::/64"
                }
            ]
        },
        "command": "subnet6-add"
    }, channel=channel)
    assert response == {
        "arguments": {
            "subnets": [
                {
                    "id": 1,
                    "subnet": "2001:db8:a::/64"
                }
            ]
        },
        "result": 0,
        "text": "IPv6 subnet added"
    }

    # First do the full exchange and expect an address from the pool.
    _sarr('2001:db8:a::50', exchange='full')

    # Add a global reservation.
    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "subnet-id": 0,
                "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
                "ip-addresses": [
                    "2001:db8:a::100"
                ]
            }
        },
        "command": "reservation-add"
    }, channel=channel)
    assert response == {
        "result": 0,
        "text": "Host added."
    }

    # Check that Kea leases the globally reserved address.
    _sarr('2001:db8:a::100', exchange=exchange)

    # Remove the global reservation.
    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "subnet-id": 0,
            "ip-address": "2001:db8:a::100"
        },
        "command": "reservation-del"
    }, channel=channel)
    assert response == {
        "result": 0,
        "text": "Host deleted."
    }

    # Check that Kea has reverted to the default behavior.
    _sarr('2001:db8:a::50', exchange=exchange)

    # Add an in-subnet reservation.
    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": {
                "subnet-id": 1,
                "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
                "ip-addresses": [
                    "2001:db8:a::150"
                ]
            }
        },
        "command": "reservation-add"
    }, channel=channel)
    assert response == {
        "result": 0,
        "text": "Host added."
    }

    # Check that Kea leases the in-subnet reserved address.
    _sarr('2001:db8:a::150', exchange=exchange)
