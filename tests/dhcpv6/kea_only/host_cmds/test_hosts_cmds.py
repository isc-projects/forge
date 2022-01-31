"""Kea Hook hosts_cmds testing"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_control
import srv_msg

from dhcp4_scen import DHCPv6_STATUS_CODES
from forge_cfg import world


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL'])
def test_v6_hosts_cmds_libreload(channel, host_database):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.SARR('2001:db8:1::50')

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

    srv_msg.SARR('2001:db8:1::100')

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

    srv_msg.SARR('2001:db8:1::50')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL'])
def test_v6_hosts_cmds_reconfigure(channel, host_database):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.SARR('2001:db8:1::50')

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

    srv_msg.SARR('2001:db8:1::100')

    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(host_database)

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

    srv_msg.SARR('2001:db8:1::100')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL'])
def test_v6_hosts_cmds_add_reservation(channel, host_database):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.SARR('2001:db8:1::50')

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

    srv_msg.SARR('2001:db8:1::100')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL'])
def test_v6_hosts_cmds_del_reservation(channel, host_database):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.SARR('2001:db8:1::50')

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

    srv_msg.SARR('2001:db8:1::100')

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

    srv_msg.SARR('2001:db8:1::50')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL'])
def test_v6_hosts_cmds_del_reservation_2(channel, host_database):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    # address reserved without using command
    srv_control.enable_db_backend_reservation(host_database)
    srv_control.new_db_backend_reservation(host_database, 'hw-address', 'f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', host_database, 1)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, host_database, 1)
    srv_control.ipv6_address_db_backend_reservation('2001:db8:1::100', '$(EMPTY)', host_database, 1)
    srv_control.upload_db_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.SARR('2001:db8:1::100')

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

    srv_msg.SARR('2001:db8:1::50')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL'])
def test_v6_hosts_cmds_get_reservation(channel, host_database):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.SARR('2001:db8:1::50')

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

    srv_msg.SARR('2001:db8:1::100')

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

    srv_msg.SARR('2001:db8:1::100')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL'])
def test_v6_hosts_cmds_get_reservation_2(channel, host_database):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    # address reserved without using command
    srv_control.enable_db_backend_reservation(host_database)
    srv_control.new_db_backend_reservation(host_database, 'duid', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', host_database, 1)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, host_database, 1)
    srv_control.ipv6_address_db_backend_reservation('2001:db8:1::100', '$(EMPTY)', host_database, 1)
    srv_control.upload_db_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.SARR('2001:db8:1::100')

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

    srv_msg.SARR('2001:db8:1::100')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL'])
def test_v6_hosts_cmds_add_reservation_flex_id(channel, host_database):
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_line({"host-reservation-identifiers": ["flex-id"]})
    srv_control.add_parameter_to_hook(2, 'identifier-expression', 'relay6[0].option[18].hex')

    srv_control.enable_db_backend_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.SARR('2001:db8:1::50', relay_information=True)

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

    srv_msg.SARR('2001:db8:1::100', relay_information=True)


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL'])
def test_v6_hosts_cmds_add_reservation_flex_id_NoAddressAvail(channel, host_database):
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_line({"host-reservation-identifiers": ["flex-id"]})
    srv_control.add_parameter_to_hook(2, 'identifier-expression', 'relay6[0].option[18].hex')

    srv_control.enable_db_backend_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Get the first lease from subnet
    srv_msg.SARR('2001:db8:1::50', duid='00:03:00:01:f6:f5:f4:f3:f2:01', relay_information=False)

    # add host reservationa
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

    # get lease from host reservation
    srv_msg.SA('2001:db8:1::100', duid='00:03:00:01:f6:f5:f4:f3:f2:02', relay_information=True)

    misc.test_procedure()
    world.sender_type = "Client"
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    # Encapsulate the Request in a relay forward message.
    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'port1234')
    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8:1::1000')
    srv_msg.client_sets_value('RelayAgent', 'peeraddr', 'fe80::1')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    # Send message and expect a relay reply.
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')

    # check for available lease
    srv_msg.SA('2001:db8:1::100', duid='00:03:00:01:f6:f5:f4:f3:f2:03', relay_information=True,
               status_code=DHCPv6_STATUS_CODES['NoAddrsAvail'], ifaceid='port1234')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL'])
def test_v6_hosts_cmds_add_reservation_complex(channel, host_database):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.SARR('2001:db8:1::50')

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

    srv_msg.SARR('2001:db8:1:0:cafe::1', delegated_prefix='2001:db8:2:abcd::')


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
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL'])
def test_v6_hosts_cmds_reservation_get_all_database(channel, host_database):
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_another_subnet_no_interface('3001::/64', '3001::1-3001::ff')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_host_cmds.so')

    srv_control.enable_db_backend_reservation(host_database)
    srv_control.new_db_backend_reservation(host_database, 'hw-address', 'f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname1', host_database, 1)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, host_database, 1)
    srv_control.new_db_backend_reservation(host_database, 'hw-address', 'f6:f5:f4:f3:f2:02')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname2', host_database, 2)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, host_database, 2)
    srv_control.new_db_backend_reservation(host_database, 'hw-address', 'f6:f5:f4:f3:f2:03')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname3', host_database, 3)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, host_database, 3)
    srv_control.new_db_backend_reservation(host_database, 'hw-address', 'f6:f5:f4:f3:f2:04')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname4', host_database, 4)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 2, host_database, 4)
    srv_control.new_db_backend_reservation(host_database, 'hw-address', 'f6:f5:f4:f3:f2:05')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname5', host_database, 5)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 2, host_database, 5)
    srv_control.upload_db_reservation(host_database)
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
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL'])
def test_v6_hosts_cmds_reservation_get_all_page_database(channel, host_database):
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_another_subnet_no_interface('3001::/64', '3001::1-3001::ff')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_host_cmds.so')

    srv_control.enable_db_backend_reservation(host_database)
    srv_control.new_db_backend_reservation(host_database, 'hw-address', 'f6:f5:f4:f3:f2:01')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname1', host_database, 1)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, host_database, 1)
    srv_control.new_db_backend_reservation(host_database, 'hw-address', 'f6:f5:f4:f3:f2:02')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname2', host_database, 2)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, host_database, 2)
    srv_control.new_db_backend_reservation(host_database, 'hw-address', 'f6:f5:f4:f3:f2:03')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname3', host_database, 3)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, host_database, 3)
    srv_control.new_db_backend_reservation(host_database, 'hw-address', 'f6:f5:f4:f3:f2:04')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname4', host_database, 4)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 2, host_database, 4)
    srv_control.new_db_backend_reservation(host_database, 'hw-address', 'f6:f5:f4:f3:f2:05')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname5', host_database, 5)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 2, host_database, 5)

    srv_control.new_db_backend_reservation(host_database, 'hw-address', 'f6:f5:f4:f3:f2:06')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname6', host_database, 6)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, host_database, 6)
    srv_control.new_db_backend_reservation(host_database, 'hw-address', 'f6:f5:f4:f3:f2:07')
    srv_control.update_db_backend_reservation('hostname', 'reserved-hostname7', host_database, 7)
    srv_control.update_db_backend_reservation('dhcp6_subnet_id', 1, host_database, 7)

    srv_control.upload_db_reservation(host_database)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    response = srv_msg.send_ctrl_cmd({
        "arguments": {
            "limit": 3,
            "subnet-id": 1
        },
        "command": "reservation-get-page"
    }, channel=channel)

    # Delete the "from" entry because its value is inconsistent
    # between test runs and we can't use it in the assert that follows.
    del response["arguments"]["next"]["from"]

    assert response == {
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
    }


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL'])
def test_v6_host_reservation_conflicts_duplicate_duid_reservations(channel, host_database):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('3000::/30', '3000::1-3000::10')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(host_database)

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
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL'])
def test_v6_host_reservation_conflicts_duplicate_ip_reservations(channel, host_database):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('3000::/30', '3000::1-3000::10')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(host_database)

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
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL'])
def test_v6_host_reservation_duplicate_ip_reservations_allowed(channel, host_database):
    the_same_ip_address = '3000::5'
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('3000::/30', '3000::1-3000::10')
    # allow non-unique IP address in multiple reservations
    srv_control.set_conf_parameter_global('ip-reservations-unique', False)
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(host_database)

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
    srv_msg.check_IA_NA(the_same_ip_address)

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
    srv_msg.check_IA_NA(the_same_ip_address)

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
    srv_msg.check_IA_NA('3000::1')


# Test that the same client can migrate from a global reservation to an
# in-subnet reservation after only a simple Kea reconfiguration.
@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
@pytest.mark.parametrize('exchange', ['full', 'renew-only'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL'])
def test_v6_hosts_cmds_global_to_in_subnet(channel, exchange, host_database):
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(host_database)

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
    srv_msg.SARR('2001:db8:a::50', exchange='full')

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
    srv_msg.SARR('2001:db8:a::100', exchange=exchange)

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
    srv_msg.SARR('2001:db8:a::50', exchange=exchange)

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
    srv_msg.SARR('2001:db8:a::150', exchange=exchange)


# Tests the reservation-get-by-hostname API command.
# Negative cases are included:
# * empty argument list
# * missing arguments
# * wrong data types
# * valid values, but not in configuration
@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v6_hosts_cmds_reservation_get_by_hostname(channel):
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
                                           'reserved-hostname',
                                           0,
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:11')
    srv_control.host_reservation_in_subnet('hostname',
                                           'Reserved-Hostname',
                                           0,
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:22')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Empty argument list
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
        },
        'command': 'reservation-get-by-hostname'
    }, channel=channel, exp_result=1)
    assert "missing parameter 'hostname'" in response['text']

    # Hostname only
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'hostname': 'reserved-hostname2'
        },
        'command': 'reservation-get-by-hostname'
    }, channel=channel)
    assert response == {
        'arguments': {
            'hosts': [
                {
                    'client-classes': [],
                    'hostname': 'reserved-hostname2',
                    'hw-address': 'f6:f5:f4:f3:f2:02',
                    'ip-addresses': [],
                    'option-data': [],
                    'prefixes': [],
                    'subnet-id': 1
                }
            ]
        },
        'result': 0,
        'text': '1 IPv6 host(s) found.'
    }

    # Non-existing hostname only
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'hostname': 'reserved-hostname42'
        },
        'command': 'reservation-get-by-hostname'
    }, channel=channel, exp_result=3)
    assert response == {
        'arguments': {
            'hosts': []
        },
        'result': 3,
        'text': '0 IPv6 host(s) found.'
    }

    # Subnet ID only
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'subnet-id': 1
        },
        'command': 'reservation-get-by-hostname'
    }, channel=channel, exp_result=1)
    assert "missing parameter 'hostname'" in response['text']

    # Non-existing subnet ID only
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'subnet-id': 42
        },
        'command': 'reservation-get-by-hostname'
    }, channel=channel, exp_result=1)
    assert "missing parameter 'hostname'" in response['text']

    # Wrong data type for hostname
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'hostname': 42,
            'subnet-id': 42
        },
        'command': 'reservation-get-by-hostname'
    }, channel=channel, exp_result=1)
    assert "invalid type specified for parameter 'hostname'" in response['text']

    # Wrong data type for subnet ID
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'hostname': 'my-hostname',
            'subnet-id': 'hello'
        },
        'command': 'reservation-get-by-hostname'
    }, channel=channel, exp_result=1)
    assert "invalid type specified for parameter 'subnet-id'" in response['text']

    # Existing hostname with existing subnet ID
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'hostname': 'reserved-hostname2',
            'subnet-id': 1
        },
        'command': 'reservation-get-by-hostname'
    }, channel=channel)
    assert response == {
        'arguments': {
            'hosts': [
                {
                    'client-classes': [],
                    'hostname': 'reserved-hostname2',
                    'hw-address': 'f6:f5:f4:f3:f2:02',
                    'ip-addresses': [],
                    'option-data': [],
                    'prefixes': []
                }
            ]
        },
        'result': 0,
        'text': '1 IPv6 host(s) found.'
    }

    # Existing hostname with existing subnet ID, but the hostname has different
    # capitalization
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'hostname': 'Reserved-Hostname',
            'subnet-id': 1
        },
        'command': 'reservation-get-by-hostname'
    }, channel=channel)
    assert response == {
        'arguments': {
            'hosts': [
                {
                    'client-classes': [],
                    'hostname': 'reserved-hostname',
                    'hw-address': 'f6:f5:f4:f3:f2:11',
                    'ip-addresses': [],
                    'option-data': [],
                    'prefixes': []
                },
                {
                    'client-classes': [],
                    'hostname': 'Reserved-Hostname',
                    'hw-address': 'f6:f5:f4:f3:f2:22',
                    'ip-addresses': [],
                    'option-data': [],
                    'prefixes': []
                }
            ]
        },
        'result': 0,
        'text': '2 IPv6 host(s) found.'
    }

    # Existing hostname with non-existing subnet ID
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'hostname': 'reserved-hostname2',
            'subnet-id': 42
        },
        'command': 'reservation-get-by-hostname'
    }, channel=channel, exp_result=1)
    assert response == {
        'result': 1,
        'text': "IPv6 subnet with ID of '42' is not configured"
    }

    # Non-existing hostname with existing subnet ID
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'hostname': 'reserved-hostname42',
            'subnet-id': 1
        },
        'command': 'reservation-get-by-hostname'
    }, channel=channel, exp_result=3)
    assert response == {
        'arguments': {
            'hosts': []
        },
        'result': 3,
        'text': '0 IPv6 host(s) found.'
    }

    # Non-existing hostname with non-existing subnet ID
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'hostname': 'reserved-hostname42',
            'subnet-id': 42
        },
        'command': 'reservation-get-by-hostname'
    }, channel=channel, exp_result=1)
    assert response == {
        'result': 1,
        'text': "IPv6 subnet with ID of '42' is not configured"
    }


# Tests the reservation-get-by-id API command.
# Negative cases are included:
# * empty argument list
# * missing arguments
# * wrong data types
# * bogus values
@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.kea_only
@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_v6_hosts_cmds_reservation_get_by_ID(channel):
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
                                           'duid',
                                           'f6:f5:f4:f3:f2:03')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname4',
                                           1,
                                           'hw-address',
                                           'f6:f5:f4:f3:f2:04')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname5',
                                           1,
                                           'flex-id',
                                           'f6:f5:f4:f3:f2:05')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Empty argument list
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
        },
        'command': 'reservation-get-by-id'
    }, channel=channel, exp_result=1)
    assert response == {
        'result': 1,
        'text': "'identifier-type' is either missing or not a string."
    }

    # identifier-type only
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'identifier-type': 'hw-address'
        },
        'command': 'reservation-get-by-id'
    }, channel=channel, exp_result=1)
    assert response == {
        'result': 1,
        'text': "'identifier' is either missing or not a string."
    }

    # identifier only
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'identifier': 'f6:f5:f4:f3:f2:02'
        },
        'command': 'reservation-get-by-id'
    }, channel=channel, exp_result=1)
    assert response == {
        'result': 1,
        'text': "'identifier-type' is either missing or not a string."
    }

    # bogus identifier-type
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'identifier-type': 'bogus',
            'identifier': 'f6:f5:f4:f3:f2:02'
        },
        'command': 'reservation-get-by-id'
    }, channel=channel, exp_result=1)
    assert response == {
        'result': 1,
        'text': "Value of 'identifier-type' was not recognized."
    }

    # bogus identifier
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'identifier-type': 'hw-address',
            'identifier': 'bogus'
        },
        'command': 'reservation-get-by-id'
    }, channel=channel, exp_result=1)
    assert response == {
        'result': 1,
        'text': "Unable to parse 'identifier' value."
    }

    # bogus identifier and bogus identifier-type
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'identifier-type': 'bogus',
            'identifier': 'bogus'
        },
        'command': 'reservation-get-by-id'
    }, channel=channel, exp_result=1)
    assert response == {
        'result': 1,
        'text': "Unable to parse 'identifier' value."
    }

    # Wrong data type for identifier-type
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'identifier-type': 42,
            'identifier': 'f6:f5:f4:f3:f2:02'
        },
        'command': 'reservation-get-by-id'
    }, channel=channel, exp_result=1)
    assert response == {
        'result': 1,
        'text': "'identifier-type' is either missing or not a string."
    }

    # Wrong data type for identifier
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'identifier-type': 'hw-address',
            'identifier': 42
        },
        'command': 'reservation-get-by-id'
    }, channel=channel, exp_result=1)
    assert response == {
        'result': 1,
        'text': "'identifier' is either missing or not a string."
    }

    # bogus by circuit ID
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'identifier-type': 'circuit-id',
            'identifier': 'bogus'
        },
        'command': 'reservation-get-by-id'
    }, channel=channel, exp_result=1)
    assert response == {
        'result': 1,
        'text': "Unable to parse 'identifier' value."
    }

    # bogus by client ID
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'identifier-type': 'client-id',
            'identifier': 'bogus'
        },
        'command': 'reservation-get-by-id'
    }, channel=channel, exp_result=1)
    assert response == {
        'result': 1,
        'text': "Unable to parse 'identifier' value."
    }

    # bogus by DUID
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'identifier-type': 'duid',
            'identifier': 'bogus'
        },
        'command': 'reservation-get-by-id'
    }, channel=channel, exp_result=1)
    assert response == {
        'result': 1,
        'text': "Unable to parse 'identifier' value."
    }

    # bogus by hardware address
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'identifier-type': 'hw-address',
            'identifier': 'bogus'
        },
        'command': 'reservation-get-by-id'
    }, channel=channel, exp_result=1)
    assert response == {
        'result': 1,
        'text': "Unable to parse 'identifier' value."
    }

    # bogus by flex ID
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'identifier-type': 'flex-id',
            'identifier': 'bogus'
        },
        'command': 'reservation-get-by-id'
    }, channel=channel, exp_result=1)
    assert response == {
        'result': 1,
        'text': "Unable to parse 'identifier' value."
    }

    # by circuit ID
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'identifier-type': 'circuit-id',
            'identifier': 'f6:f5:f4:f3:f2:01'
        },
        'command': 'reservation-get-by-id'
    }, channel=channel, exp_result=3)
    assert response == {
        'arguments': {
            'hosts': []
        },
        'result': 3,
        'text': '0 IPv6 host(s) found.'
    }

    # by client ID
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'identifier-type': 'client-id',
            'identifier': 'f6:f5:f4:f3:f2:02'
        },
        'command': 'reservation-get-by-id'
    }, channel=channel, exp_result=3)
    assert response == {
        'arguments': {
            'hosts': []
        },
        'result': 3,
        'text': '0 IPv6 host(s) found.'
    }

    # by DUID
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'identifier-type': 'duid',
            'identifier': 'f6:f5:f4:f3:f2:03'
        },
        'command': 'reservation-get-by-id'
    }, channel=channel)
    assert response == {
        'arguments': {
            'hosts': [
                {
                    'client-classes': [],
                    'duid': 'f6:f5:f4:f3:f2:03',
                    'hostname': 'reserved-hostname3',
                    'ip-addresses': [],
                    'option-data': [],
                    'prefixes': [],
                    'subnet-id': 1
                }
            ]
        },
        'result': 0,
        'text': '1 IPv6 host(s) found.'
    }

    # by hardware address
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'identifier-type': 'hw-address',
            'identifier': 'f6:f5:f4:f3:f2:04'
        },
        'command': 'reservation-get-by-id'
    }, channel=channel)
    assert response == {
        'arguments': {
            'hosts': [
                {
                    'client-classes': [],
                    'hostname': 'reserved-hostname4',
                    'hw-address': 'f6:f5:f4:f3:f2:04',
                    'ip-addresses': [],
                    'option-data': [],
                    'prefixes': [],
                    'subnet-id': 2
                }
            ]
        },
        'result': 0,
        'text': '1 IPv6 host(s) found.'
    }

    # by flex ID
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'identifier-type': 'flex-id',
            'identifier': 'f6:f5:f4:f3:f2:05'
        },
        'command': 'reservation-get-by-id'
    }, channel=channel)
    assert response == {
        'arguments': {
            'hosts': [
                {
                    'client-classes': [],
                    'hostname': 'reserved-hostname5',
                    'flex-id': 'F6F5F4F3F205',
                    'ip-addresses': [],
                    'option-data': [],
                    'prefixes': [],
                    'subnet-id': 2
                }
            ]
        },
        'result': 0,
        'text': '1 IPv6 host(s) found.'
    }
