# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea Hook hosts_cmds testing"""

# pylint: disable=invalid-name

import random
import string
import pytest

from src import misc
from src import srv_control
from src import srv_msg

from src.forge_cfg import world


def _reservation_add(reservation: dict, target: str = None, channel: str = 'http', exp_result: int = 0,
                     exp_failed: bool = False):
    """
    Send reservation add command
    :param reservation: dictionary with reservation
    :param target: memory for memfile, database for database
    :param channel: http or socket
    :param exp_result: expected result of a command returned by kea
    :param exp_failed: expectation if command should fail completely
    :return: dict, response from Kea
    """
    if target is None:
        assert False, "Do not leave this to chance, please set target value"
    return srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": reservation,
            "operation-target": target
        },
        "command": "reservation-add"
    }, channel=channel, exp_result=exp_result, exp_failed=exp_failed)


def _reservation_update(reservation: dict, target: str = None, channel: str = 'http',
                        exp_result: int = 0, exp_failed: bool = False):
    """
    Send reservation update command
    :param reservation: dictionary with reservation
    :param target: primary for memfile, database for database
    :param channel: http or socket
    :param exp_result: expected result of a command returned by kea
    :param exp_failed: expectation if command should fail completely
    :return: dict, response from Kea
    """

    if target is None:
        assert False, "Do not leave this to chance, please set target value"
    return srv_msg.send_ctrl_cmd({
        "arguments": {
            "reservation": reservation,
            "operation-target": target
        },
        "command": "reservation-update"
    }, channel=channel, exp_result=exp_result, exp_failed=exp_failed)


def _reservation_get(cmd: str, args: dict, target: str = None, channel: str = 'http',
                     exp_result: int = 0, exp_failed: bool = False):
    """
    Send reservation add command
    :param cmd: command to send
    :param args: argument of a command
    :param target: primary for memfile, database for database
    :param channel: http or socket
    :param exp_result: expected result of a command returned by kea
    :param exp_failed: expectation if command should fail completely
    :return: dict, response from Kea
    """
    if target is None:
        assert False, "Do not leave this to chance, please set target value"
    args.update({"operation-target": target})
    return srv_msg.send_ctrl_cmd({
        "command": cmd,
        "arguments": args
    }, channel=channel, exp_result=exp_result, exp_failed=exp_failed)


def _reservation_del(args: dict, target: str = None, channel: str = 'http',
                     exp_result: int = 0, exp_failed: bool = False):
    """
    Send reservation-del command
    :param args: dictionary with arguments of command
    :param target: primary for memfile, database for database
    :param channel: http or socket
    :param exp_result: expected result of a command returned by kea
    :param exp_failed: expectation if command should fail completely
    :return: dict, response from Kea
    """
    if target is None:
        assert False, "Do not leave this to chance, please set target value"
    args.update({"operation-target": target})
    return srv_msg.send_ctrl_cmd({
        "command": "reservation-del",
        "arguments": args
    }, channel=channel, exp_result=exp_result, exp_failed=exp_failed)


def _clean_up_reservation(res: dict):
    """
    Remove all empty values from reservation, makes it easier to compare created reservation with received
    :param res: reservation received from Kea
    :return: dict: cleaned up reservation
    """
    for x in list(res.keys()):
        if isinstance(res[x], (list, str)) and len(res[x]) == 0:
            # log.debug("---- delete: ", x, res[x], len(res[x]))
            del res[x]
    return res


def _get_target(database: str):
    """
    Get proper operation-target based on database type
    :param database: database type name
    :return: operation-target value
    """
    if database == 'memfile':
        return 'memory'
    return 'database'


def _get_multiple_iana(adresses, iaid, duid):
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_does_include('Client', 'client-id')
    for id in iaid:
        srv_msg.client_sets_value('Client', 'ia_id', id)
        srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.generate_new('IA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_copy_option('IA_NA', copy_all=True)
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    for ip in adresses:
        srv_msg.response_check_suboption_content(5, 3, 'addr', ip)


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL'])
def test_v4_reconfigure(channel, host_database):
    """
    Add reservation, reconfigure Kea, check if it is still able to get reservation
    """
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.DORA('192.168.50.50')

    res = {
        "hw-address": "ff:01:02:03:ff:04",
        "ip-address": "192.168.50.100",
        "subnet-id": 1
    }

    response = _reservation_add(res, target=_get_target(host_database), channel=channel)
    assert response == {
        "result": 0,
        "text": "Host added."
    }

    srv_msg.DORA('192.168.50.100')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.250-192.168.50.250')
    srv_control.enable_db_backend_reservation(host_database, clear=False)
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'reconfigured')

    srv_msg.DORA('192.168.50.100')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL', 'memfile'])
def test_v4_add_reservation(channel, host_database):
    """
    Add simple reservation
    """
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.DORA('192.168.50.50')

    res = [{
        "hw-address": "ff:01:02:03:ff:04",
        "ip-address": "192.168.50.100",
        "subnet-id": 1
    },
        {
        "hw-address": "ff:01:02:03:ff:05",
        "ip-address": "192.168.50.101",
        "subnet-id": 1
    },
        {
        "hw-address": "ff:01:02:03:ff:06",
        "ip-address": "192.168.50.102",
        "subnet-id": 1
    }]

    for reservation in res[:-1]:
        response = _reservation_add(reservation, target=_get_target(host_database), channel=channel)
        assert response == {
            "result": 0,
            "text": "Host added."
        }

    response = _reservation_get("reservation-get-all", {"subnet-id": 1},
                                target=_get_target(host_database), channel=channel)

    assert response["result"] == 0
    assert response["text"] == "2 IPv4 host(s) found."

    srv_msg.DORA('192.168.50.100')
    srv_msg.DORA('192.168.50.101', chaddr='ff:01:02:03:ff:05')

    response = _reservation_add(res[-1], target=_get_target(host_database), channel=channel)
    assert response == {
        "result": 0,
        "text": "Host added."
    }

    srv_msg.DORA('192.168.50.100')
    srv_msg.DORA('192.168.50.101', chaddr='ff:01:02:03:ff:05')
    srv_msg.DORA('192.168.50.102', chaddr='ff:01:02:03:ff:06')

    response = _reservation_get("reservation-get-all", {"subnet-id": 1},
                                target=_get_target(host_database), channel=channel)

    assert response["result"] == 0
    assert response["text"] == "3 IPv4 host(s) found."


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL', 'memfile'])
@pytest.mark.parametrize('query_type', ['by-ip', 'by-mac'])
def test_v4_del_reservation(channel, host_database, query_type):
    """
    Add and delete reservation using:
    * 3 params (subnet-id, identifier-type, identifier)
    * 2 params (subnet-id, address)
    """
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.DORA('192.168.50.50')

    res = [{
        "hw-address": "ff:01:02:03:ff:04",
        "ip-address": "192.168.50.100",
        "subnet-id": 1
    },
        {
        "hw-address": "ff:01:02:03:ff:05",
        "ip-address": "192.168.50.101",
        "subnet-id": 1
    },
        {
        "hw-address": "ff:01:02:03:ff:06",
        "ip-address": "192.168.50.102",
        "subnet-id": 1
    }]

    for reservation in res:
        response = _reservation_add(reservation, target=_get_target(host_database), channel=channel)
        assert response == {
            "result": 0,
            "text": "Host added."
        }

    srv_msg.DORA('192.168.50.100')

    del_res = {
        "ip-address": "192.168.50.100",
        "subnet-id": 1
    }
    if query_type == 'by-mac':
        del_res = {
            "identifier": "ff:01:02:03:ff:04",
            "identifier-type": "hw-address",
            "subnet-id": 1
        }

    response = _reservation_del(del_res, target=_get_target(host_database), channel=channel)

    assert response == {
        "result": 0,
        "text": "Host deleted."
    }

    response = _reservation_get("reservation-get-all", {"subnet-id": 1},
                                target=_get_target(host_database), channel=channel)

    assert response["result"] == 0
    assert response["text"] == "2 IPv4 host(s) found."

    srv_msg.DORA('192.168.50.50')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL', 'memfile'])
def test_v4_get_reservation(channel, host_database):
    """
    Test reservation-get command using:
    * 3 params (subnet-id, identifier-type, identifier)
    * 2 params (subnet-id, address)
    """
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.DORA('192.168.50.50')

    res = {
        "hw-address": "ff:01:02:03:ff:04",
        "ip-address": "192.168.50.100",
        "next-server": "10.10.10.10",
        "subnet-id": 1
    }

    response = _reservation_add(res, target=_get_target(host_database), channel=channel)

    assert response == {
        "result": 0,
        "text": "Host added."
    }

    # get reservation using two params, clean up empty values, and compare
    res_get = {
        "subnet-id": 1,
        "ip-address": "192.168.50.100"
    }

    res_returned = _reservation_get("reservation-get", res_get, target=_get_target(host_database))["arguments"]
    res_returned = _clean_up_reservation(res_returned)
    assert res == res_returned, "Reservation sent and returned are not the same"

    # get reservation using three params, clean up empty values, and compare
    res_get = {
        "identifier": "ff:01:02:03:ff:04",
        "identifier-type": "hw-address",
        "subnet-id": 1
    }

    res_returned = _reservation_get("reservation-get", res_get, target=_get_target(host_database))["arguments"]
    res_returned = _clean_up_reservation(res_returned)
    assert res == res_returned, "Reservation sent and returned are not the same"


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL', 'memfile'])
def test_v4_add_reservation_flex_id(channel, host_database):
    """
    Add reservation based on flex id
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_hooks('libdhcp_flex_id.so')
    srv_control.add_line({"host-reservation-identifiers": ["flex-id"]})
    srv_control.add_parameter_to_hook(2, 'identifier-expression', 'option[60].hex')

    srv_control.enable_db_backend_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.DORA('192.168.50.50', {'vendor_class_id': 'docsis3.0'})

    res = {
        "flex-id": "'docsis3.0'",
        "ip-address": "192.168.50.100",
        "subnet-id": 1
    }

    response = _reservation_add(res, target=_get_target(host_database), channel=channel)

    assert response == {
        "result": 0,
        "text": "Host added."
    }

    srv_msg.DORA('192.168.50.100', {'vendor_class_id': 'docsis3.0'})


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL', 'memfile'])
def test_v4_add_reservation_complex(channel, host_database):
    """
    Add reservation with all parameters configured, check if client will get all and check reservation get result
    """
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Confirm that not reserved host gets ip from pool
    srv_msg.DORA('192.168.50.50')

    # Add reservation
    res = {
        "boot-file-name": "/dev/null",
        "client-classes": [
            "special_snowflake",
            "office"
        ],
        "client-id": "010A0B0C0D0E0F",
        "ip-address": "192.168.50.205",
        "hostname": "abc",
        "next-server": "192.168.50.1",
        "option-data": [
            {
                "data": "10.1.1.202,10.1.1.203",
                "name": "domain-name-servers",
                'always-send': False,
                'code': 6,
                'csv-format': True,
                'never-send': False,
                'space': 'dhcp4'
            }
        ],
        "server-hostname": "hal9000",
        "subnet-id": 1,
        "user-context": {
            "floor": "1"
        }
    }

    response = _reservation_add(res, target=_get_target(host_database), channel=channel)

    assert response == {
        "result": 0,
        "text": "Host added."
    }

    # get reservation using two params, clean up empty values, and compare
    res_get = {
        "subnet-id": 1,
        "ip-address": "192.168.50.205"
    }
    res_returned = _reservation_get("reservation-get", res_get, target=_get_target(host_database))["arguments"]
    res_returned = _clean_up_reservation(res_returned)
    assert res == res_returned, "Reservation sent and returned are not the same"

    # Get lease according to reservation
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
@pytest.mark.parametrize('channel', ['http'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL', 'memfile'])
def test_v4_get_reservation_by_id(channel, host_database):
    """
    Add reservation with all parameters configured, then test reservation-get-by-hostname reservation-get-by-id commands
    """
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Confirm that not reserved host gets ip from pool
    srv_msg.DORA('192.168.50.50')

    # Add reservation
    res = {
        "boot-file-name": "/dev/null",
        "client-classes": [
            "special_snowflake",
            "office"
        ],
        "client-id": "010A0B0C0D0E0F",
        "hostname": "abc",
        "ip-address": "192.168.50.205",
        "next-server": "192.168.50.1",
        "option-data": [
            {
                "data": "10.1.1.202,10.1.1.203",
                "name": "domain-name-servers",
                'always-send': False,
                'code': 6,
                'csv-format': True,
                'never-send': False,
                'space': 'dhcp4'
            }
        ],
        "server-hostname": "hal9000",
        "subnet-id": 1,
        "user-context": {
            "floor": "1"
        }
    }

    res_circuit_id = {
        "circuit-id": "1111",
        "hostname": "othername",
        "ip-address": "192.168.50.200",
        "next-server": "192.168.50.10",
        "option-data": [
            {
                "data": "10.1.1.202,10.1.1.203",
                "name": "domain-name-servers",
                'always-send': False,
                'code': 6,
                'csv-format': True,
                'never-send': False,
                'space': 'dhcp4'
            }
        ],
        "server-hostname": "hal9000",
        "subnet-id": 1,
        "user-context": {
            "floor": "2"
        }
    }

    res_flex_id = {
        "flex-id": "01020304",
        "hostname": "othername123",
        "ip-address": "192.168.50.100",
        "next-server": "192.168.50.20",
        "option-data": [
            {
                "data": "10.1.1.202,10.1.1.203",
                "name": "domain-name-servers",
                'always-send': False,
                'code': 6,
                'csv-format': True,
                'never-send': False,
                'space': 'dhcp4'
            }
        ],
        "server-hostname": "hal9000",
        "subnet-id": 1,
        "user-context": {
            "floor": "3"
        }
    }

    for i in [res, res_circuit_id, res_flex_id]:
        response = _reservation_add(i, target=_get_target(host_database), channel=channel)

        assert response == {
            "result": 0,
            "text": "Host added."
        }

    # get reservation using get-by-hostname
    res_get = {
        "subnet-id": 1,
        "hostname": "abc"
    }
    res_returned = _reservation_get("reservation-get-by-hostname", res_get,
                                    target=_get_target(host_database))["arguments"]["hosts"][0]
    res_returned = _clean_up_reservation(res_returned)
    assert res == res_returned, "Reservation sent and returned are not the same"

    # get reservation using get-by-id - 'circuit-id'
    res_get = {
        "identifier-type": "circuit-id",
        "identifier": "1111",
    }
    res_returned = _reservation_get("reservation-get-by-id", res_get,
                                    target=_get_target(host_database))["arguments"]["hosts"][0]
    res_returned = _clean_up_reservation(res_returned)
    assert res_circuit_id == res_returned, "Reservation sent and returned are not the same"

    # get reservation using get-by-id - 'client-id'
    res_get = {
        "identifier-type": "client-id",
        "identifier": "010A0B0C0D0E0F",
    }
    res_returned = _reservation_get("reservation-get-by-id", res_get,
                                    target=_get_target(host_database))["arguments"]["hosts"][0]
    res_returned = _clean_up_reservation(res_returned)
    assert res == res_returned, "Reservation sent and returned are not the same"

    # get reservation using get-by-id - 'flex-id'
    res_get = {
        "identifier-type": "flex-id",
        "identifier": "01020304",
    }
    res_returned = _reservation_get("reservation-get-by-id", res_get,
                                    target=_get_target(host_database))["arguments"]["hosts"][0]
    res_returned = _clean_up_reservation(res_returned)
    assert res_flex_id == res_returned, "Reservation sent and returned are not the same"


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL', 'memfile'])
def test_v4_reservation_get_all(channel, host_database):
    """
    Check command reservation-get-all
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24', '192.168.51.50-192.168.51.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()
    srv_control.enable_db_backend_reservation(host_database)
    srv_control.add_hooks('libdhcp_host_cmds.so')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    reservation_list = [{"hostname": f"reserved-hostname{i}",
                         "hw-address": f"f6:f5:f4:f3:f2:{i}{i}",
                         "subnet-id": 1} for i in range(1, 4)]

    reservation_list += [{"hostname": f"reserved-hostname{i}",
                          "hw-address": f"f6:f5:f4:f3:f2:{i}{i}",
                          "subnet-id": 2} for i in range(4, 6)]

    for reservation in reservation_list:
        _reservation_add(reservation, target=_get_target(host_database), channel=channel)

    response = _reservation_get("reservation-get-all", {"subnet-id": 1},
                                target=_get_target(host_database), channel=channel)

    assert response == {
        "arguments": {
            "hosts": [
                {
                    "boot-file-name": "",
                    "client-classes": [],
                    "hostname": f"reserved-hostname{i}",
                    "hw-address": f"f6:f5:f4:f3:f2:{i}{i}",
                    "next-server": "0.0.0.0",
                    "option-data": [],
                    "server-hostname": "",
                    "subnet-id": 1
                } for i in range(1, 4)
            ]
        },
        "result": 0,
        "text": "3 IPv4 host(s) found."
    }

    response = _reservation_get("reservation-get-all", {"subnet-id": 2},
                                target=_get_target(host_database), channel=channel)

    assert response == {
        "arguments": {
            "hosts": [
                {
                    "boot-file-name": "",
                    "client-classes": [],
                    "hostname": f"reserved-hostname{i}",
                    "hw-address": f"f6:f5:f4:f3:f2:{i}{i}",
                    "next-server": "0.0.0.0",
                    "option-data": [],
                    "server-hostname": "",
                    "subnet-id": 2
                } for i in range(4, 6)
            ]
        },
        "result": 0,
        "text": "2 IPv4 host(s) found."
    }


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL', 'memfile'])
def test_v4_reservation_get_page(channel, host_database):
    """
    Add 7 reservations in subnet 1 and 7 in subnet 2. Use reservation-get-page to get all from subnet 1
    than from subnet 2. At the end use command reservation-get-page without subnet id to get all 14 reservations
    while using different limit.
    """

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24', '192.168.51.50-192.168.51.50')
    srv_control.enable_db_backend_reservation(host_database)
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    reservation_list = [{"hostname": f"reserved-hostname{i}",
                         "next-server": "10.10.10.1",
                         "hw-address": f"00:00:00:00:00:{i}{i}",
                         "subnet-id": 1} for i in range(1, 8)]
    reservation_list += [{"hostname": f"other-reserved-hostname{i}",
                          "next-server": "10.10.10.1",
                          "hw-address": f"00:00:00:00:11:{i}{i}",
                          "subnet-id": 2} for i in range(1, 8)]

    for reservation in reservation_list:
        _reservation_add(reservation, target=_get_target(host_database), channel=channel)

    res_get = {
        "limit": 3,
        "subnet-id": 1
    }
    reservations = _reservation_get("reservation-get-page", res_get, target=_get_target(host_database), channel=channel)

    # let's update res_get for next message:
    res_get.update(reservations["arguments"]["next"])
    # and remove from value, because it may differ between backends
    del reservations["arguments"]["next"]["from"]

    source = 0
    if host_database != 'memfile':
        source = 1

    assert reservations == {
        "arguments": {
            "count": 3,
            "hosts": [
                {
                    "boot-file-name": "",
                    "client-classes": [],
                    "hostname": f"reserved-hostname{i}",
                    "hw-address": f"00:00:00:00:00:{i}{i}",
                    "next-server": "10.10.10.1",
                    "option-data": [],
                    "server-hostname": "",
                    "subnet-id": 1
                } for i in range(1, 4)],
            "next": {
                "source-index": source
            }
        },
        "result": 0,
        "text": "3 IPv4 host(s) found."
    }

    # this time res_get has from and source-index included!
    reservations = _reservation_get("reservation-get-page", res_get, target=_get_target(host_database), channel=channel)

    # let's update res_get for next message:
    res_get.update(reservations["arguments"]["next"])
    # and remove from value, because it may differ between backends
    del reservations["arguments"]["next"]["from"]

    assert reservations == {
        "arguments": {
            "count": 3,
            "hosts": [
                {
                    "boot-file-name": "",
                    "client-classes": [],
                    "hostname": f"reserved-hostname{i}",
                    "hw-address": f"00:00:00:00:00:{i}{i}",
                    "next-server": "10.10.10.1",
                    "option-data": [],
                    "server-hostname": "",
                    "subnet-id": 1
                } for i in range(4, 7)],
            "next": {
                "source-index": source
            }
        },
        "result": 0,
        "text": "3 IPv4 host(s) found."
    }

    # this time res_get has from and source-index updated again, and we expect just one reservation back
    reservations = _reservation_get("reservation-get-page", res_get, target=_get_target(host_database), channel=channel)

    del reservations["arguments"]["next"]["from"]

    assert reservations == {
        "arguments": {
            "count": 1,
            "hosts": [
                {
                    "boot-file-name": "",
                    "client-classes": [],
                    "hostname": f"reserved-hostname{i}",
                    "hw-address": f"00:00:00:00:00:{i}{i}",
                    "next-server": "10.10.10.1",
                    "option-data": [],
                    "server-hostname": "",
                    "subnet-id": 1
                } for i in range(7, 8)],
            "next": {
                "source-index": source
            }
        },
        "result": 0,
        "text": "1 IPv4 host(s) found."
    }

    # for subnet 2
    res_get = {
        "limit": 3,
        "subnet-id": 2
    }
    reservations = _reservation_get("reservation-get-page", res_get, target=_get_target(host_database), channel=channel)

    # let's update res_get for next message:
    res_get.update(reservations["arguments"]["next"])
    # and remove from value, because it may differ between backends
    del reservations["arguments"]["next"]["from"]

    assert reservations == {
        "arguments": {
            "count": 3,
            "hosts": [
                {
                    "boot-file-name": "",
                    "client-classes": [],
                    "hostname": f"other-reserved-hostname{i}",
                    "hw-address": f"00:00:00:00:11:{i}{i}",
                    "next-server": "10.10.10.1",
                    "option-data": [],
                    "server-hostname": "",
                    "subnet-id": 2
                } for i in range(1, 4)],
            "next": {
                "source-index": source
            }
        },
        "result": 0,
        "text": "3 IPv4 host(s) found."
    }

    # this time res_get has from and source-index included!
    reservations = _reservation_get("reservation-get-page", res_get, target=_get_target(host_database), channel=channel)

    # let's update res_get for next message:
    res_get.update(reservations["arguments"]["next"])
    # and remove from value, because it may differ between backends
    del reservations["arguments"]["next"]["from"]

    assert reservations == {
        "arguments": {
            "count": 3,
            "hosts": [
                {
                    "boot-file-name": "",
                    "client-classes": [],
                    "hostname": f"other-reserved-hostname{i}",
                    "hw-address": f"00:00:00:00:11:{i}{i}",
                    "next-server": "10.10.10.1",
                    "option-data": [],
                    "server-hostname": "",
                    "subnet-id": 2
                } for i in range(4, 7)],
            "next": {
                "source-index": source
            }
        },
        "result": 0,
        "text": "3 IPv4 host(s) found."
    }

    # this time res_get has from and source-index updated again, and we expect just one reservation back
    reservations = _reservation_get("reservation-get-page", res_get, target=_get_target(host_database), channel=channel)

    del reservations["arguments"]["next"]["from"]

    assert reservations == {
        "arguments": {
            "count": 1,
            "hosts": [
                {
                    "boot-file-name": "",
                    "client-classes": [],
                    "hostname": f"other-reserved-hostname{i}",
                    "hw-address": f"00:00:00:00:11:{i}{i}",
                    "next-server": "10.10.10.1",
                    "option-data": [],
                    "server-hostname": "",
                    "subnet-id": 2
                } for i in range(7, 8)],
            "next": {
                "source-index": source
            }
        },
        "result": 0,
        "text": "1 IPv4 host(s) found."
    }

    # now let's check reservation-get-page without subnet id, we should get all 14 reservations
    # but those can be return in any order so, let's compare them differently, all reservations will be saved
    # and compared at the end
    all_reservations_returned = []

    res_get = {
        "limit": 5,
    }
    reservations = _reservation_get("reservation-get-page", res_get, target=_get_target(host_database),
                                    channel=channel)["arguments"]

    all_reservations_returned += reservations["hosts"]
    del reservations["hosts"]
    # let's update res_get for next message:
    res_get.update(reservations["next"])
    # and remove from value, because it may differ between backends
    del reservations["next"]["from"]
    assert reservations == {
        "count": 5,
        "next": {
            "source-index": source
        }
    }

    reservations = _reservation_get("reservation-get-page", res_get, target=_get_target(host_database),
                                    channel=channel)["arguments"]

    all_reservations_returned += reservations["hosts"]
    del reservations["hosts"]

    # let's update res_get for next message:
    res_get.update(reservations["next"])
    # and remove from value, because it may differ between backends
    del reservations["next"]["from"]

    assert reservations == {
        "count": 5,
        "next": {
            "source-index": source
        }
    }

    # this time res_get has from and source-index updated again, and we expect just one reservation back
    reservations = _reservation_get("reservation-get-page", res_get, target=_get_target(host_database),
                                    channel=channel)["arguments"]

    del reservations["next"]["from"]
    all_reservations_returned += reservations["hosts"]
    del reservations["hosts"]

    assert reservations == {
        "count": 4,
        "next": {
            "source-index": source
        }
    }

    # now zip both lists and compare every single reservation returned with the those
    # generated at the beginning
    all_reservations_returned = sorted(all_reservations_returned, key=lambda d: d['hw-address'])
    reservation_list = sorted(reservation_list, key=lambda d: d['hw-address'])

    for new, old in zip(all_reservations_returned, reservation_list):
        new = _clean_up_reservation(new)
        assert new == old, "Reservation sent and returned are not the same"


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL', 'memfile'])
def test_v4_reservation_update(channel, host_database):
    """
    Check reservation update command with all backends and assignment
    """
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.create_new_class('Client_Class_1')
    srv_control.create_new_class('Client_Class_2')
    srv_control.disable_leases_affinity()
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # this won't change
    res_get = {
        "subnet-id": 1,
        "identifier-type": "hw-address",
        "identifier": "f6:f5:f4:f3:f2:01"
    }

    # reservation to set
    res = {
        "hw-address": "f6:f5:f4:f3:f2:01",
        "ip-address": "192.168.50.100",
        "next-server": "10.1.2.3",
        "subnet-id": 1,
    }

    _reservation_add(res, target=_get_target(host_database), channel=channel)
    res_returned = _reservation_get("reservation-get", res_get, target=_get_target(host_database))["arguments"]
    res_returned = _clean_up_reservation(res_returned)
    assert res == res_returned, "Reservation sent and returned are not the same"

    # update with extra parameters and check
    res = {
        "boot-file-name": "/dev/null",
        "client-classes": [
            "special_snowflake",
            "office"
        ],
        "hw-address": "f6:f5:f4:f3:f2:01",
        "ip-address": "192.168.50.205",
        "hostname": "abc",
        "next-server": "192.168.50.1",
        "option-data": [
            {
                "data": "10.1.1.202,10.1.1.203",
                "name": "domain-name-servers",
                'always-send': False,
                'code': 6,
                'csv-format': True,
                'never-send': False,
                'space': 'dhcp4'
            }
        ],
        "server-hostname": "hal9000",
        "subnet-id": 1,
        "user-context": {
            "floor": "1"
        }
    }
    _reservation_update(res, target=_get_target(host_database))
    res_returned = _reservation_get("reservation-get", res_get, target=_get_target(host_database))["arguments"]
    res_returned = _clean_up_reservation(res_returned)
    assert res == res_returned, "Reservation sent and returned are not the same"

    # update existing parameters and check
    res = {
        "boot-file-name": "/dev/abc",
        "client-classes": [
            "special_snowflake",
            "office"
        ],
        "hw-address": "f6:f5:f4:f3:f2:01",
        "ip-address": "192.168.50.205",
        "hostname": "abc",
        "next-server": "192.168.50.100",
        "option-data": [
            {
                "data": "10.1.1.202,10.1.1.203",
                "name": "domain-name-servers",
                'always-send': False,
                'code': 6,
                'csv-format': True,
                'never-send': False,
                'space': 'dhcp4'
            }
        ],
        "server-hostname": "hal19000",
        "subnet-id": 1,
        "user-context": {
            "floor": "2"
        }
    }
    _reservation_update(res, target=_get_target(host_database))
    res_returned = _reservation_get("reservation-get", res_get, target=_get_target(host_database))["arguments"]
    res_returned = _clean_up_reservation(res_returned)
    assert res == res_returned, "Reservation sent and returned are not the same"

    # update with fewer parameters and check
    res = {
        "hw-address": "f6:f5:f4:f3:f2:01",
        "next-server": "1.1.1.1",
        "subnet-id": 1
    }
    _reservation_update(res, target=_get_target(host_database))
    res_returned = _reservation_get("reservation-get", res_get, target=_get_target(host_database))["arguments"]
    res_returned = _clean_up_reservation(res_returned)
    assert res == res_returned, "Reservation sent and returned are not the same"


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL', 'memfile'])
def test_v4_reservation_update_negative(channel, host_database):
    """
    Check various incorrect commands reservation-update
    """
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.create_new_class('Client_Class_1')
    srv_control.create_new_class('Client_Class_2')
    srv_control.disable_leases_affinity()
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # let's add first one reservations
    res_get = {
        "identifier": "f6:f5:f4:f3:f2:01",
        "identifier-type": "hw-address",
        "subnet-id": 1
    }
    res = {
        "hw-address": "f6:f5:f4:f3:f2:01",
        "next-server": "1.0.0.1",
        "ip-address": "192.168.50.100",
        "subnet-id": 1,
    }
    _reservation_add(res, target=_get_target(host_database))
    res_returned = _reservation_get("reservation-get", res_get, target=_get_target(host_database),
                                    channel=channel)["arguments"]
    res_returned = _clean_up_reservation(res_returned)
    assert res == res_returned, "Reservation sent and returned are not the same"

    # empty
    update = {}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)

    # missing hw-address
    update = {"subnet-id": 1}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)

    # incorrect hw-address
    update = {"subnet-id": 1, "hw-address": ""}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)

    update = {"subnet-id": 1, "hw-address": "010203"}  # minimum length is 4
    _reservation_update(update, target=_get_target(host_database), exp_result=1)

    update = {"subnet-id": 1, "hw-address": "".join(random.choices(string.hexdigits, k=300))}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)

    update = {"subnet-id": 1, "hw-address": 1}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)

    update = {"subnet-id": 1, "hw-address": True}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)

    update = {"subnet-id": 1, "hw-address": random.choices(string.hexdigits, k=300)}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)

    # non existing hw-address
    update = {"subnet-id": 1, "hw-address": "f6:f5:f4:01:01:01"}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)

    # missing subnet
    update = {"hw-address": "f6:f5:f4:f3:f2:01"}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)

    # incorrect subnet id
    update = {"hw-address": "f6:f5:f4:f3:f2:01",
              "subnet-id": random.choices(string.hexdigits, k=300)}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)
    update = {"hw-address": "f6:f5:f4:f3:f2:01",
              "subnet-id": "".join(random.choices(string.hexdigits, k=300))}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)
    update = {"hw-address": "f6:f5:f4:f3:f2:01",
              "subnet-id": True}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)
    update = {"hw-address": "f6:f5:f4:f3:f2:01",
              "subnet-id": ""}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)

    # correctly identified reservation but with incorrect data
    update = {"hw-address": "f6:f5:f4:f3:f2:01",
              "subnet-id": 1,
              "ip-addresses": ["".join(random.choices(string.hexdigits, k=300))]}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)
    update = {"hw-address": "f6:f5:f4:f3:f2:01",
              "subnet-id": 1,
              "prefixes": ["".join(random.choices(string.hexdigits, k=300))]}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)
    update = {"hw-address": "f6:f5:f4:f3:f2:01",
              "subnet-id": 1,
              "option-data": [{"abc": "".join(random.choices(string.hexdigits, k=300))}]}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)

    # and now let's check reservation that we actually added
    res_returned = _reservation_get("reservation-get", res_get, target=_get_target(host_database),
                                    channel=channel)["arguments"]
    res_returned = _clean_up_reservation(res_returned)
    assert res == res_returned, "Reservation sent and returned are not the same"


# negative tests:
@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL', 'memfile'])
def test_v4_conflicts_duplicate_mac_reservations(channel, host_database):
    """
    Check if non unique reservations will be rejected when "ip-reservations-unique": False is NOT used.
    Default Kea behaviour
    """
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    res = {
        "hw-address": "ff:01:02:03:ff:01",
        "ip-address": "192.168.50.10",
        "subnet-id": 1
    }

    response = _reservation_add(res, target=_get_target(host_database), channel=channel)

    assert response == {
        "result": 0,
        "text": "Host added."
    }

    # the same DUID - it should fail
    res = {
        "hw-address": "ff:01:02:03:ff:01",
        "ip-address": "192.168.50.100",
        "subnet-id": 1
    }

    response = _reservation_add(res, target=_get_target(host_database), channel=channel, exp_result=1)

    text = "Database duplicate entry error"
    if host_database == 'memfile':
        text = "failed to add new host using the HW address 'ff:01:02:03:ff:01' to the" \
               " IPv4 subnet id '1' as this host has already been added"
    assert response == {
        "result": 1,
        "text": text
    }


@pytest.mark.v4
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL', 'memfile'])
def test_v4_conflicts_duplicate_ip_reservations(channel, host_database):
    """
    Check if non unique reservations will be rejected when "ip-reservations-unique": False is NOT used.
    Default Kea behaviour
    """
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    res = {
        "hw-address": "ff:01:02:03:ff:01",
        "ip-address": "192.168.50.10",
        "subnet-id": 1
    }

    response = _reservation_add(res, target=_get_target(host_database), channel=channel)

    assert response == {
        "result": 0,
        "text": "Host added."
    }

    res = {
        "hw-address": "ff:01:02:03:ff:22",
        "ip-address": "192.168.50.10",
        "subnet-id": 1
    }

    response = _reservation_add(res, target=_get_target(host_database),
                                channel=channel, exp_result=1)

    text = "Database duplicate entry error"
    if host_database == 'memfile':
        text = "failed to add new host using the HW address 'ff:01:02:03:ff:22 and DUID '(null)' to the IPv4 subnet" \
               " id '1' for the address 192.168.50.10: There's already a reservation for this address"

    assert response == {
        "result": 1,
        "text": text
    }


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL', 'memfile'])
def test_v4_duplicate_ip_reservations_allowed(channel, host_database):
    """
    Check if configuration option "ip-reservations-unique": False will allow to keep non unique
    reservations in all backends and if those reservations will be assigned correctly
    """
    the_same_ip_address = '192.168.50.10'
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    # allow non-unique IP address in multiple reservations
    srv_control.set_conf_parameter_global('ip-reservations-unique', False)
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    res = {
        "hw-address": "aa:aa:aa:aa:aa:aa",
        "ip-address": the_same_ip_address,
        "subnet-id": 1
    }

    response = _reservation_add(res, target=_get_target(host_database), channel=channel)

    assert response == {
        "result": 0,
        "text": "Host added."
    }

    res = {
        "hw-address": "bb:bb:bb:bb:bb:bb",
        "ip-address": the_same_ip_address,
        "subnet-id": 1
    }

    response = _reservation_add(res, target=_get_target(host_database), channel=channel)

    assert response == {
        "result": 0,
        "text": "Host added."
    }

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


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
@pytest.mark.parametrize('exchange', ['full', 'renew-only'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL', 'memfile'])
def test_v4_global_to_in_subnet(channel, exchange, host_database):
    """
    Test that the same client can migrate from a global reservation to an
    in-subnet reservation after only a simple Kea reconfiguration.
    """
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
    assert response == {
        "arguments": {
            "subnets": [
                {
                    "id": 1,
                    "subnet": "192.168.50.0/24"
                }
            ]
        },
        "result": 0,
        "text": "IPv4 subnet added"
    }

    # First do the full exchange and expect an address from the pool.
    srv_msg.DORA('192.168.50.50', exchange='full')

    # Add a global reservation.

    res = {
        "subnet-id": 0,
        "hw-address": "ff:01:02:03:ff:04",
        "ip-address": "192.168.50.100"
    }

    response = _reservation_add(res, target=_get_target(host_database), channel=channel)

    assert response == {
        "result": 0,
        "text": "Host added."
    }

    # Check that Kea leases the globally reserved address.
    srv_msg.DORA('192.168.50.100', exchange=exchange)

    # Remove the global reservation.
    del_res = {
        "subnet-id": 0,
        "ip-address": "192.168.50.100"
    }

    response = _reservation_del(del_res, target=_get_target(host_database), channel=channel)

    assert response == {
        "result": 0,
        "text": "Host deleted."
    }

    # Check that Kea has reverted to the default behavior.
    srv_msg.DORA('192.168.50.50', exchange=exchange)

    # Add an in-subnet reservation.
    res = {
        "subnet-id": 1,
        "hw-address": "ff:01:02:03:ff:04",
        "ip-address": "192.168.50.150"
    }

    response = _reservation_add(res, target=_get_target(host_database), channel=channel)

    assert response == {
        "result": 0,
        "text": "Host added."
    }

    # Check that Kea leases the in-subnet reserved address.
    srv_msg.DORA('192.168.50.150', exchange=exchange)


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
def test_v4_reservation_get_by_hostname(channel):
    """
    Tests the reservation-get-by-hostname API command.
    Negative cases are included:
     * empty argument list
     * missing arguments
     * wrong data types
     * valid values, but not in configuration
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24', '192.168.51.50-192.168.51.50')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Empty argument list
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
        },
        'command': 'reservation-get-by-hostname'
    }, channel=channel, exp_result=1)
    assert "missing parameter 'hostname'" in response['text']

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
        'text': '0 IPv4 host(s) found.'
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
        'text': "IPv4 subnet with ID of '42' is not configured"
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
        'text': '0 IPv4 host(s) found.'
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
        'text': "IPv4 subnet with ID of '42' is not configured"
    }


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
def test_v4_reservation_get_by_id(channel):
    """
    Tests the reservation-get-by-id API command.
    Negative cases are included:
     * empty argument list
     * missing arguments
     * wrong data types
     * bogus values
    """
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
                                           'circuit-id',
                                           'f6:f5:f4:f3:f2:01')
    srv_control.host_reservation_in_subnet('hostname',
                                           'reserved-hostname2',
                                           0,
                                           'client-id',
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
    }, channel=channel)
    assert response == {
        'arguments': {
            'hosts': [
                {
                    'boot-file-name': '',
                    'client-classes': [],
                    'circuit-id': 'F6F5F4F3F201',
                    'hostname': 'reserved-hostname1',
                    'next-server': '0.0.0.0',
                    'option-data': [],
                    'server-hostname': '',
                    'subnet-id': 1
                }
            ]
        },
        'result': 0,
        'text': '1 IPv4 host(s) found.'
    }

    # by client ID
    response = srv_msg.send_ctrl_cmd({
        'arguments': {
            'identifier-type': 'client-id',
            'identifier': 'f6:f5:f4:f3:f2:02'
        },
        'command': 'reservation-get-by-id'
    }, channel=channel)
    assert response == {
        'arguments': {
            'hosts': [
                {
                    'boot-file-name': '',
                    'client-classes': [],
                    'client-id': 'F6F5F4F3F202',
                    'hostname': 'reserved-hostname2',
                    'next-server': '0.0.0.0',
                    'option-data': [],
                    'server-hostname': '',
                    'subnet-id': 1
                }
            ]
        },
        'result': 0,
        'text': '1 IPv4 host(s) found.'
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
                    'boot-file-name': '',
                    'client-classes': [],
                    'duid': 'f6:f5:f4:f3:f2:03',
                    'hostname': 'reserved-hostname3',
                    'next-server': '0.0.0.0',
                    'option-data': [],
                    'server-hostname': '',
                    'subnet-id': 1
                }
            ]
        },
        'result': 0,
        'text': '1 IPv4 host(s) found.'
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
                    'boot-file-name': '',
                    'client-classes': [],
                    'hostname': 'reserved-hostname4',
                    'hw-address': 'f6:f5:f4:f3:f2:04',
                    'next-server': '0.0.0.0',
                    'option-data': [],
                    'server-hostname': '',
                    'subnet-id': 2
                }
            ]
        },
        'result': 0,
        'text': '1 IPv4 host(s) found.'
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
                    'boot-file-name': '',
                    'client-classes': [],
                    'hostname': 'reserved-hostname5',
                    'flex-id': 'F6F5F4F3F205',
                    'next-server': '0.0.0.0',
                    'option-data': [],
                    'server-hostname': '',
                    'subnet-id': 2
                }
            ]
        },
        'result': 0,
        'text': '1 IPv4 host(s) found.'
    }


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL'])
def test_v6_reconfigure(channel, host_database):
    """
    Add reservation, reconfigure Kea, check if it is still able to get reservation
    """
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

    res = {
        "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
        "ip-addresses": [
            "2001:db8:1::100"
        ],
        "subnet-id": 1
    }
    response = _reservation_add(res, target=_get_target(host_database), channel=channel)

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

    srv_control.enable_db_backend_reservation(host_database, clear=False)

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'reconfigured')

    srv_msg.SARR('2001:db8:1::100')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL', 'memfile'])
def test_v6_add_reservation(channel, host_database):
    """
    Add simple reservation
    """
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

    res = [{
        "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
        "ip-addresses": [
            "2001:db8:1::101"
        ],
        "subnet-id": 1
        },
        {"duid": "00:03:00:01:f6:f5:f4:f3:f2:02",
         "ip-addresses": [
             "2001:db8:1::102"
         ],
         "subnet-id": 1
         },
        {"duid": "00:03:00:01:f6:f5:f4:f3:f2:03",
         "ip-addresses": [
                 "2001:db8:1::103"
         ],
         "subnet-id": 1
         }]

    for reservation in res[:-1]:
        response = _reservation_add(reservation, target=_get_target(host_database), channel=channel)
        assert response == {
            "result": 0,
            "text": "Host added."
        }

    response = _reservation_get("reservation-get-all", {"subnet-id": 1},
                                target=_get_target(host_database), channel=channel)

    assert response["result"] == 0
    assert response["text"] == "2 IPv6 host(s) found."

    srv_msg.SARR('2001:db8:1::101')
    srv_msg.SARR('2001:db8:1::102', duid='00:03:00:01:f6:f5:f4:f3:f2:02')

    response = _reservation_add(res[-1], target=_get_target(host_database), channel=channel)
    assert response == {
        "result": 0,
        "text": "Host added."
    }
    srv_msg.SARR('2001:db8:1::101')
    srv_msg.SARR('2001:db8:1::102', duid='00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.SARR('2001:db8:1::103', duid='00:03:00:01:f6:f5:f4:f3:f2:03')

    response = _reservation_get("reservation-get-all", {"subnet-id": 1},
                                target=_get_target(host_database), channel=channel)

    assert response["result"] == 0
    assert response["text"] == "3 IPv6 host(s) found."


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL', 'memfile'])
@pytest.mark.parametrize('query_type', ['by-ip', 'by-mac'])
def test_v6_del_reservation(channel, host_database, query_type):
    """
    Add and delete reservation using:
    * by-mac (subnet-id, identifier-type, identifier)
    * by-ip (subnet-id, address)
    """
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::60')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.SARR('2001:db8:1::50')

    res = [{
        "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
        "ip-addresses": [
            "2001:db8:1::101"
        ],
        "subnet-id": 1
        },
        {"duid": "00:03:00:01:f6:f5:f4:f3:f2:02",
         "ip-addresses": [
             "2001:db8:1::102"
         ],
         "subnet-id": 1
         },
        {"duid": "00:03:00:01:f6:f5:f4:f3:f2:03",
         "ip-addresses": [
                 "2001:db8:1::103"
         ],
         "subnet-id": 1
         },
        {"duid": "00:03:00:01:f6:f5:f4:f3:f2:04",
         "ip-addresses": [
                 "2001:db8:1::104", "2001:db8:1::105"
         ],
         "subnet-id": 1
         }]

    for reservation in res:
        _reservation_add(reservation, target=_get_target(host_database), channel=channel)

    srv_msg.SARR('2001:db8:1::101')
    _get_multiple_iana(['2001:db8:1::104','2001:db8:1::105'], [2123,2124], '00:03:00:01:f6:f5:f4:f3:f2:04')

    del_res = {
        "ip-address": "2001:db8:1::101",
        "subnet-id": 1
    }
    if query_type == 'by-mac':
        del_res = {
            "identifier": "00:03:00:01:f6:f5:f4:f3:f2:01",
            "identifier-type": "duid",
            "subnet-id": 1
        }

    response = _reservation_del(del_res, target=_get_target(host_database), channel=channel)

    assert response == {
        "result": 0,
        "text": "Host deleted."
    }

    response = _reservation_get("reservation-get-all", {"subnet-id": 1},
                                target=_get_target(host_database), channel=channel)

    assert response["result"] == 0
    assert response["text"] == "3 IPv6 host(s) found."

    srv_msg.SARR('2001:db8:1::51')
    _get_multiple_iana(['2001:db8:1::104','2001:db8:1::105'], [2123,2124],  '00:03:00:01:f6:f5:f4:f3:f2:04')

    del_res = {
        "ip-address": "2001:db8:1::105",
        "subnet-id": 1
    }
    if query_type == 'by-mac':
        del_res = {
            "identifier": "00:03:00:01:f6:f5:f4:f3:f2:04",
            "identifier-type": "duid",
            "subnet-id": 1
        }

    response = _reservation_del(del_res, target=_get_target(host_database), channel=channel)

    assert response == {
        "result": 0,
        "text": "Host deleted."
    }

    response = _reservation_get("reservation-get-all", {"subnet-id": 1},
                                target=_get_target(host_database), channel=channel)

    assert response["result"] == 0
    assert response["text"] == "2 IPv6 host(s) found."

    srv_msg.SARR('2001:db8:1::52')
    srv_msg.SARR('2001:db8:1::53',  duid='00:03:00:01:f6:f5:f4:f3:f2:04')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL', 'memfile'])
def test_v6_get_reservation(channel, host_database):
    """
    Test reservation-get command using:
    * 3 params (subnet-id, identifier-type, identifier)
    * 2 params (subnet-id, address)
    """
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

    res = {
        "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
        "ip-addresses": [
            "2001:db8:1::100"
        ],
        "subnet-id": 1
    }
    response = _reservation_add(res, target=_get_target(host_database), channel=channel)

    assert response == {
        "result": 0,
        "text": "Host added."
    }

    srv_msg.SARR('2001:db8:1::100')

    res_get = {
        "subnet-id": 1,
        "ip-address": "2001:db8:1::100"
    }

    res_returned = _reservation_get("reservation-get", res_get, target=_get_target(host_database))["arguments"]
    res_returned = _clean_up_reservation(res_returned)
    assert res == res_returned, "Reservation sent and returned are not the same"

    # get reservation using three params, clean up empty values, and compare
    res_get = {
        "identifier": "00:03:00:01:f6:f5:f4:f3:f2:01",
        "identifier-type": "duid",
        "subnet-id": 1
    }

    res_returned = _reservation_get("reservation-get", res_get, target=_get_target(host_database))["arguments"]
    res_returned = _clean_up_reservation(res_returned)
    assert res == res_returned, "Reservation sent and returned are not the same"


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL', 'memfile'])
def test_v6_add_reservation_flex_id(channel, host_database):
    """
    Add reservation with flex id
    """
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

    res = {
        "flex-id": "'port1234'",
        "ip-addresses": [
            "2001:db8:1::100"
        ],
        "subnet-id": 1
    }
    response = _reservation_add(res, target=_get_target(host_database), channel=channel)

    assert response == {
        "result": 0,
        "text": "Host added."
    }

    srv_msg.SARR('2001:db8:1::100', relay_information=True)


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL', 'memfile'])
def test_v6_add_reservation_complex(channel, host_database):
    """
    Add, get, and assign complex reservation
    """
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

    res = {
        "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
        "hostname": "foo.example.com",
        "ip-addresses": [
            "2001:db8:1:0:cafe::1"
        ],
        "option-data": [
            {
                "always-send": False,
                "code": 17,
                "csv-format": True,
                "data": "4491",
                "name": "vendor-opts",
                "never-send": False,
                "space": "dhcp6"
            },
            {
                "always-send": False,
                "code": 32,
                "csv-format": True,
                "data": "3000:1::234",
                "name": "tftp-servers",
                "never-send": False,
                "space": "vendor-4491"
            }
        ],
        "prefixes": [
            "2001:db8:2:abcd::/64"
        ],
        "subnet-id": 1,
        "user-context": {
            "floor": "1"
        }
    }
    response = _reservation_add(res, target=_get_target(host_database), channel=channel)

    assert response == {
        "result": 0,
        "text": "Host added."
    }

    # Get the reservation and check user-context.
    res_get = {
        "subnet-id": 1,
        "ip-address": "2001:db8:1:0:cafe::1"
    }

    res_returned = _reservation_get("reservation-get", res_get, target=_get_target(host_database))["arguments"]
    res_returned = _clean_up_reservation(res_returned)
    assert res == res_returned, "Reservation sent and returned are not the same"

    srv_msg.SARR('2001:db8:1:0:cafe::1', delegated_prefix='2001:db8:2:abcd::/64')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL', 'memfile'])
def test_v6_reservation_get_all(channel, host_database):
    """
    Check reservation-get-all command in separate subnets on all backends
    """
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_another_subnet_no_interface('3001::/64', '3001::1-3001::ff')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_host_cmds.so')

    srv_control.enable_db_backend_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    reservation_list = [
        {"hostname": f"reserved-hostname{i}",
         "duid": f"00:03:00:01:f6:f5:f4:f3:f2:{i}{i}",
         "subnet-id": 1,
         "ip-addresses": [f"3000::{i}"]
         } for i in range(1, 4)]

    reservation_list += [
        {"hostname": f"other-reserved-hostname{i}",
         "duid": f"00:03:00:01:f6:f5:f4:ff:ff:{i}{i}",
         "subnet-id": 2,
         "ip-addresses": [f"3001::{i}"]
         } for i in range(1, 3)]

    for reservation in reservation_list:
        _reservation_add(reservation, target=_get_target(host_database), channel=channel)

    response = _reservation_get("reservation-get-all", {"subnet-id": 1},
                                target=_get_target(host_database), channel=channel)

    assert response == {
        "arguments": {
            "hosts": [
                {
                    "client-classes": [],
                    "duid": f"00:03:00:01:f6:f5:f4:f3:f2:{i}{i}",
                    "hostname": f"reserved-hostname{i}",
                    "ip-addresses": [
                        f"3000::{i}"
                    ],
                    "option-data": [],
                    "prefixes": [],
                    "subnet-id": 1
                } for i in range(1, 4)
            ]
        },
        "result": 0,
        "text": "3 IPv6 host(s) found."
    }
    response = _reservation_get("reservation-get-all", {"subnet-id": 2},
                                target=_get_target(host_database), channel=channel)

    assert response == {
        "arguments": {
            "hosts": [
                {
                    "client-classes": [],
                    "duid": f"00:03:00:01:f6:f5:f4:ff:ff:{i}{i}",
                    "hostname": f"other-reserved-hostname{i}",
                    "ip-addresses": [
                        f"3001::{i}"
                    ],
                    "option-data": [],
                    "prefixes": [],
                    "subnet-id": 2
                } for i in range(1, 3)
            ]
        },
        "result": 0,
        "text": "2 IPv6 host(s) found."
    }


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL', 'memfile'])
def test_v6_reservation_get_page(channel, host_database):
    """
    Add 7 reservations in subnet 1 and 7 in subnet 2. Use reservation-get-page to get all from subnet 1
    than from subnet 2. At the end use command reservation-get-page without subnet id to get all 14 reservations
    while using different limit.
    """
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_another_subnet_no_interface('3001::/64', '3001::1-3001::ff')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_host_cmds.so')

    srv_control.enable_db_backend_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    reservation_list = [
        {"hostname": f"reserved-hostname{i}",
         "duid": f"00:03:00:01:f6:f5:f4:f3:f2:{i}{i}",
         "subnet-id": 1,
         "ip-addresses": [f"3000::{i}"]
         } for i in range(1, 8)]

    reservation_list += [
        {"hostname": f"other-reserved-hostname{i}",
         "duid": f"00:03:00:01:f6:f5:f4:ff:ff:{i}{i}",
         "subnet-id": 2,
         "ip-addresses": [f"3001::{i}"]
         } for i in range(1, 8)]

    for reservation in reservation_list:
        _reservation_add(reservation, target=_get_target(host_database), channel=channel)

    res_get = {
        "limit": 3,
        "subnet-id": 1
    }
    reservations = _reservation_get("reservation-get-page", res_get, target=_get_target(host_database), channel=channel)

    # let's update res_get for next message:
    res_get.update(reservations["arguments"]["next"])
    # and remove from value, because it may differ between backends
    del reservations["arguments"]["next"]["from"]

    source = 0
    if host_database != 'memfile':
        source = 1

    assert reservations == {
        "arguments": {
            "count": 3,
            "hosts": [
                {
                    "client-classes": [],
                    "duid": f"00:03:00:01:f6:f5:f4:f3:f2:{i}{i}",
                    "hostname": f"reserved-hostname{i}",
                    "ip-addresses": [
                        f"3000::{i}"
                    ],
                    "option-data": [],
                    "prefixes": [],
                    "subnet-id": 1
                } for i in range(1, 4)
            ],
            "next": {
                "source-index": source
            }
        },
        "result": 0,
        "text": "3 IPv6 host(s) found."
    }

    # this time res_get has from and source-index included!
    reservations = _reservation_get("reservation-get-page", res_get, target=_get_target(host_database), channel=channel)

    # let's update res_get for next message:
    res_get.update(reservations["arguments"]["next"])
    # and remove from value, because it may differ between backends
    del reservations["arguments"]["next"]["from"]

    assert reservations == {
        "arguments": {
            "count": 3,
            "hosts": [
                {
                    "client-classes": [],
                    "duid": f"00:03:00:01:f6:f5:f4:f3:f2:{i}{i}",
                    "hostname": f"reserved-hostname{i}",
                    "ip-addresses": [
                        f"3000::{i}"
                    ],
                    "option-data": [],
                    "prefixes": [],
                    "subnet-id": 1
                } for i in range(4, 7)
            ],
            "next": {
                "source-index": source
            }
        },
        "result": 0,
        "text": "3 IPv6 host(s) found."
    }

    # this time res_get has from and source-index updated again, and we expect just one reservation back
    reservations = _reservation_get("reservation-get-page", res_get, target=_get_target(host_database), channel=channel)

    del reservations["arguments"]["next"]["from"]

    assert reservations == {
        "arguments": {
            "count": 1,
            "hosts": [
                {
                    "client-classes": [],
                    "duid": f"00:03:00:01:f6:f5:f4:f3:f2:{i}{i}",
                    "hostname": f"reserved-hostname{i}",
                    "ip-addresses": [
                        f"3000::{i}"
                    ],
                    "option-data": [],
                    "prefixes": [],
                    "subnet-id": 1
                } for i in range(7, 8)
            ],
            "next": {
                "source-index": source
            }
        },
        "result": 0,
        "text": "1 IPv6 host(s) found."
    }

    # and repeat this for subnet 2:
    res_get = {
        "limit": 3,
        "subnet-id": 2
    }
    reservations = _reservation_get("reservation-get-page", res_get, target=_get_target(host_database), channel=channel)

    # let's update res_get for next message:
    res_get.update(reservations["arguments"]["next"])
    # and remove from value, because it may differ between backends
    del reservations["arguments"]["next"]["from"]

    source = 0
    if host_database != 'memfile':
        source = 1

    assert reservations == {
        "arguments": {
            "count": 3,
            "hosts": [
                {
                    "client-classes": [],
                    "duid": f"00:03:00:01:f6:f5:f4:ff:ff:{i}{i}",
                    "hostname": f"other-reserved-hostname{i}",
                    "ip-addresses": [
                        f"3001::{i}"
                    ],
                    "option-data": [],
                    "prefixes": [],
                    "subnet-id": 2
                } for i in range(1, 4)
            ],
            "next": {
                "source-index": source
            }
        },
        "result": 0,
        "text": "3 IPv6 host(s) found."
    }

    # this time res_get has from and source-index included!
    reservations = _reservation_get("reservation-get-page", res_get, target=_get_target(host_database), channel=channel)

    # let's update res_get for next message:
    res_get.update(reservations["arguments"]["next"])
    # and remove from value, because it may differ between backends
    del reservations["arguments"]["next"]["from"]

    assert reservations == {
        "arguments": {
            "count": 3,
            "hosts": [
                {
                    "client-classes": [],
                    "duid": f"00:03:00:01:f6:f5:f4:ff:ff:{i}{i}",
                    "hostname": f"other-reserved-hostname{i}",
                    "ip-addresses": [
                        f"3001::{i}"
                    ],
                    "option-data": [],
                    "prefixes": [],
                    "subnet-id": 2
                } for i in range(4, 7)
            ],
            "next": {
                "source-index": source
            }
        },
        "result": 0,
        "text": "3 IPv6 host(s) found."
    }

    # this time res_get has from and source-index updated again, and we expect just one reservation back
    reservations = _reservation_get("reservation-get-page", res_get, target=_get_target(host_database), channel=channel)

    del reservations["arguments"]["next"]["from"]

    assert reservations == {
        "arguments": {
            "count": 1,
            "hosts": [
                {
                    "client-classes": [],
                    "duid": f"00:03:00:01:f6:f5:f4:ff:ff:{i}{i}",
                    "hostname": f"other-reserved-hostname{i}",
                    "ip-addresses": [
                        f"3001::{i}"
                    ],
                    "option-data": [],
                    "prefixes": [],
                    "subnet-id": 2
                } for i in range(7, 8)
            ],
            "next": {
                "source-index": source
            }
        },
        "result": 0,
        "text": "1 IPv6 host(s) found."
    }

    # now let's check reservation-get-page without subnet id, we should get all 14 reservations
    # but those can be return in any order so, let's compare them differently, all reservations will be saved
    # and compared at the end
    all_reservations_returned = []

    res_get = {
        "limit": 5,
    }
    reservations = _reservation_get("reservation-get-page", res_get, target=_get_target(host_database),
                                    channel=channel)["arguments"]

    all_reservations_returned += reservations["hosts"]
    del reservations["hosts"]
    # let's update res_get for next message:
    res_get.update(reservations["next"])
    # and remove from value, because it may differ between backends
    del reservations["next"]["from"]
    assert reservations == {
        "count": 5,
        "next": {
            "source-index": source
        }
    }

    reservations = _reservation_get("reservation-get-page", res_get, target=_get_target(host_database),
                                    channel=channel)["arguments"]

    all_reservations_returned += reservations["hosts"]
    del reservations["hosts"]

    # let's update res_get for next message:
    res_get.update(reservations["next"])
    # and remove from value, because it may differ between backends
    del reservations["next"]["from"]

    assert reservations == {
        "count": 5,
        "next": {
            "source-index": source
        }
    }

    # this time res_get has from and source-index updated again, and we expect just one reservation back
    reservations = _reservation_get("reservation-get-page", res_get, target=_get_target(host_database),
                                    channel=channel)["arguments"]

    del reservations["next"]["from"]
    all_reservations_returned += reservations["hosts"]
    del reservations["hosts"]

    assert reservations == {
        "count": 4,
        "next": {
            "source-index": source
        }
    }

    # now zip both lists and compare every single reservation returned with the those
    # generated at the beginning
    all_reservations_returned = sorted(all_reservations_returned, key=lambda d: d['duid'])
    reservation_list = sorted(reservation_list, key=lambda d: d['duid'])

    for new, old in zip(all_reservations_returned, reservation_list):
        new = _clean_up_reservation(new)
        assert new == old, "Reservation sent and returned are not the same"


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL', 'memfile'])
def test_v6_conflicts_duplicate_duid_reservations(channel, host_database):
    """
    Check if non unique reservations will be rejected when "ip-reservations-unique": False is NOT used.
    Default Kea behaviour
    """
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('3000::/30', '3000::1-3000::10')
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Add reservation
    res = {
        "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
        "ip-addresses": [
            "3000::5"
        ],
        "subnet-id": 1
    }

    response = _reservation_add(res, target=_get_target(host_database), channel=channel)

    assert response == {
        "result": 0,
        "text": "Host added."
    }

    # the same DUID - it should fail
    res = {
        "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
        "ip-addresses": [
            "3000::3"
        ],
        "subnet-id": 1
    }

    response = _reservation_add(res, target=_get_target(host_database),
                                channel=channel, exp_result=1)

    text = "Database duplicate entry error"
    if host_database == 'memfile':
        text = "failed to add new host using the DUID '00:03:00:01:f6:f5:f4:f3:f2:01' to the" \
               " IPv6 subnet id '1' as this host has already been added"

    assert response == {
        "result": 1,
        "text": text
    }

    # now let's add duplicated address with different DUID
    res = {
        "duid": "00:03:00:01:f6:f5:f4:33:22:11",
        "ip-addresses": [
            "3000::5"
        ],
        "subnet-id": 1
    }

    response = _reservation_add(res, target=_get_target(host_database),
                                channel=channel, exp_result=1)

    text = "Database duplicate entry error"
    if host_database == 'memfile':
        text = "failed to add address reservation for host using the HW address '(null) and DUID" \
               " '00:03:00:01:f6:f5:f4:33:22:11' to the IPv6 subnet id '1' for address/prefix 3000::5:" \
               " There's already reservation for this address/prefix"

    assert response == {
        "result": 1,
        "text": text
    }


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL', 'memfile'])
def test_v6_duplicate_ip_reservations_allowed(channel, host_database):
    """
    Check if configuration option "ip-reservations-unique": False will allow to keep non unique
    reservations in all backends and if those reservations will be assigned correctly
    """
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('3000::/30', '3000::1-3000::10')
    # allow non-unique IP address in multiple reservations
    srv_control.set_conf_parameter_global('ip-reservations-unique', False)
    srv_control.disable_leases_affinity()
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    the_same_ip_address = '3000::5'

    res = {
        "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
        "ip-addresses": [
            the_same_ip_address
        ],
        "subnet-id": 1
    }

    response = _reservation_add(res, target=_get_target(host_database), channel=channel)

    assert response == {
        "result": 0,
        "text": "Host added."
    }

    res = {
        "duid": "00:03:00:01:f6:f5:f4:f3:f2:02",
        "ip-addresses": [
            the_same_ip_address
        ],
        "subnet-id": 1
    }

    response = _reservation_add(res, target=_get_target(host_database), channel=channel)

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


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
@pytest.mark.parametrize('exchange', ['full', 'renew-only'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL', 'memfile'])
def test_v6_global_to_in_subnet(channel, exchange, host_database):
    """
    Test that the same client can migrate from a global reservation to an
    in-subnet reservation after only a simple Kea reconfiguration.
    """
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

    res = {
        "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
        "ip-addresses": [
            "2001:db8:a::100"
        ],
        "subnet-id": 0
    }

    response = _reservation_add(res, target=_get_target(host_database), channel=channel)
    assert response == {
        "result": 0,
        "text": "Host added."
    }

    # Check that Kea leases the globally reserved address.
    srv_msg.SARR('2001:db8:a::100', exchange=exchange)

    # Remove the global reservation.

    res = {
        "subnet-id": 0,
        "ip-address": "2001:db8:a::100"
    }

    response = _reservation_del(res, target=_get_target(host_database), channel=channel)
    assert response == {
        "result": 0,
        "text": "Host deleted."
    }

    # Check that Kea has reverted to the default behavior.
    srv_msg.SARR('2001:db8:a::50', exchange=exchange)

    # Add an in-subnet reservation.
    res = {
        "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
        "ip-addresses": [
            "2001:db8:a::150"
        ],
        "subnet-id": 1
    }

    response = _reservation_add(res, target=_get_target(host_database), channel=channel)
    assert response == {
        "result": 0,
        "text": "Host added."
    }

    # Check that Kea leases the in-subnet reserved address.
    srv_msg.SARR('2001:db8:a::150', exchange=exchange)


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
def test_v6_reservation_get_by_hostname(channel):
    """
    Tests the reservation-get-by-hostname API command.
    Negative cases are included:
     * empty argument list
     * missing arguments
     * wrong data types
     * valid values, but not in configuration
    """
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
                    'prefixes': [],
                    'subnet-id': 1
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
                    'prefixes': [],
                    'subnet-id': 1
                },
                {
                    'client-classes': [],
                    'hostname': 'Reserved-Hostname',
                    'hw-address': 'f6:f5:f4:f3:f2:22',
                    'ip-addresses': [],
                    'option-data': [],
                    'prefixes': [],
                    'subnet-id': 1
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
@pytest.mark.parametrize('channel', ['http'])
def test_v6_reservation_get_by_id(channel):
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


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL', 'memfile'])
def test_v6_reservation_update(channel, host_database):
    """
    reservation-update tests
    """
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.create_new_class('Client_Class_1')
    srv_control.create_new_class('Client_Class_2')
    srv_control.disable_leases_affinity()
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    duid = "00:03:00:01:f6:f5:f4:f3:f2:01"

    res_get = {
        "identifier": duid,
        "identifier-type": "duid",
        "subnet-id": 1
    }
    res = {
        "duid": duid,
        "ip-addresses": [
            "2001:db8:1:0:cafe::1"
        ],
        "subnet-id": 1,
    }

    # set and check
    _reservation_add(res, target=_get_target(host_database))
    res_returned = _reservation_get("reservation-get", res_get, target=_get_target(host_database),
                                    channel=channel)["arguments"]
    res_returned = _clean_up_reservation(res_returned)
    assert res == res_returned, "Reservation sent and returned are not the same"

    srv_msg.SARR('2001:db8:1:0:cafe::1')

    # update with extra parameters and check
    res = {
        "duid": duid,
        "ip-addresses": [
            "2001:db8:1:0:cafe::3"
        ],
        "prefixes": [
            "2001:db8:2:abcd::/64"
        ],
        "subnet-id": 1,
        "option-data": [
            {
                "name": "dns-servers",
                "code": 23,
                "space": "dhcp6",
                "data": "3000:1::234",
                "always-send": True,
                "csv-format": True,
                "never-send": False
            }
        ],
        "hostname": "my-name-xyz",
        "client-classes": ["Client_Class_1"],
        "user-context": {"XYZ": 123}
    }
    _reservation_update(res, target=_get_target(host_database))
    res_returned = _reservation_get("reservation-get", res_get, target=_get_target(host_database),
                                    channel=channel)["arguments"]
    res_returned = _clean_up_reservation(res_returned)
    assert res == res_returned, "Reservation sent and returned are not the same"

    srv_msg.SARR('2001:db8:1:0:cafe::3', delegated_prefix='2001:db8:2:abcd::/64')

    # update existing parameters and check
    res = {
        "duid": duid,
        "ip-addresses": [
            "2001:db8:1::5"
        ],
        "prefixes": [
            "2001:db8:2::/64"
        ],
        "subnet-id": 1,
        "option-data": [
            {
                "name": "nisp-servers",
                "code": 28,
                "space": "dhcp6",
                "always-send": False,
                "csv-format": False,
                "data": "20010DB800010000000000000000CAFE20010DB800010000000000000000BABE",
                "never-send": False
            }
        ],
        "hostname": "my-name-abc",
        "client-classes": ["Client_Class_2"],
        "user-context": {"XYZ": 999}
    }
    _reservation_update(res, target=_get_target(host_database))
    res_returned = _reservation_get("reservation-get", res_get, target=_get_target(host_database),
                                    channel=channel)["arguments"]
    res_returned = _clean_up_reservation(res_returned)
    assert res == res_returned, "Reservation sent and returned are not the same"

    srv_msg.SARR('2001:db8:1::5', delegated_prefix='2001:db8:2::/64')

    # update with fewer parameters and check
    res = {
        "duid": duid,
        "subnet-id": 1
    }
    _reservation_update(res, target=_get_target(host_database))
    res_returned = _reservation_get("reservation-get", res_get, target=_get_target(host_database),
                                    channel=channel)["arguments"]
    res_returned = _clean_up_reservation(res_returned)
    assert res == res_returned, "Reservation sent and returned are not the same"

    srv_msg.SARR('2001:db8:1::50')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('channel', ['http'])
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL', 'memfile'])
def test_v6_reservation_update_negative(channel, host_database):
    """
    Check various combinations of incorrect reservation-update command
    """
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.create_new_class('Client_Class_1')
    srv_control.create_new_class('Client_Class_2')
    srv_control.disable_leases_affinity()
    srv_control.open_control_channel()
    if channel == 'http':
        srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # let's add first one reservations
    res_get = {
        "identifier": "00:03:00:01:f6:f5:f4:f3:f2:01",
        "identifier-type": "duid",
        "subnet-id": 1
    }
    res = {
        "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
        "ip-addresses": [
            "2001:db8:1:0:cafe::1"
        ],
        "subnet-id": 1,
    }
    _reservation_add(res, target=_get_target(host_database))
    res_returned = _reservation_get("reservation-get", res_get, target=_get_target(host_database),
                                    channel=channel)["arguments"]
    res_returned = _clean_up_reservation(res_returned)
    assert res == res_returned, "Reservation sent and returned are not the same"

    # empty
    update = {}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)

    # missing duid
    update = {"subnet-id": 1}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)

    # incorrect duid
    update = {"subnet-id": 1, "duid": ""}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)

    update = {"subnet-id": 1, "duid": "010203"}  # minimum length is 4
    _reservation_update(update, target=_get_target(host_database), exp_result=1)

    update = {"subnet-id": 1, "duid": "".join(random.choices(string.hexdigits, k=300))}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)

    update = {"subnet-id": 1, "duid": 1}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)

    update = {"subnet-id": 1, "duid": True}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)

    update = {"subnet-id": 1, "duid": random.choices(string.hexdigits, k=300)}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)

    # non existing duid
    update = {"subnet-id": 1, "duid": "00:03:00:01:f6:f5:f4:01:01:01"}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)

    # missing subnet
    update = {"duid": "00:03:00:01:f6:f5:f4:f3:f2:01"}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)

    # incorrect subnet id
    update = {"duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
              "subnet-id": random.choices(string.hexdigits, k=300)}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)
    update = {"duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
              "subnet-id": "".join(random.choices(string.hexdigits, k=300))}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)
    update = {"duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
              "subnet-id": True}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)
    update = {"duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
              "subnet-id": ""}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)

    # correctly identified reservation but with incorrect data
    update = {"duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
              "subnet-id": 1,
              "ip-addresses": ["".join(random.choices(string.hexdigits, k=300))]}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)
    update = {"duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
              "subnet-id": 1,
              "prefixes": ["".join(random.choices(string.hexdigits, k=300))]}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)
    update = {"duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
              "subnet-id": 1,
              "option-data": [{"abc": "".join(random.choices(string.hexdigits, k=300))}]}
    _reservation_update(update, target=_get_target(host_database), exp_result=1)

    # and now let's check reservation that we actually added
    res_returned = _reservation_get("reservation-get", res_get, target=_get_target(host_database),
                                    channel=channel)["arguments"]
    res_returned = _clean_up_reservation(res_returned)
    assert res == res_returned, "Reservation sent and returned are not the same"


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL'])
def test_v6_memfile_with_(host_database):
    """
    Check how Kea is handling situations when reservations are saved in config file
    and in one of the supported backend. Also it checks operation-target parameter
    of the host commands
    """
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::51')
    srv_control.disable_leases_affinity()
    srv_control.open_control_channel()
    srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.SARR(duid="00:03:00:01:f6:f5:f4:01:01:01", address='2001:db8:1::50')
    srv_msg.SARR(duid="00:03:00:01:f6:f5:f4:f3:f2:01", address='2001:db8:1::51')

    # let's add two different reservations, one to memfile other to database, get it and compare
    # keep in mind:
    #  memfile - target primary
    #  database - target database

    # memfile
    res_get = {
        "identifier": "00:03:00:01:f6:f5:f4:f3:f2:01",
        "identifier-type": "duid",
        "subnet-id": 1
    }
    res_memfile = {
        "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
        "ip-addresses": [
            "2001:db8:1::a"
        ],
        "subnet-id": 1,
    }

    # set and check
    _reservation_add(res_memfile, target='memory')
    res_returned = _reservation_get("reservation-get", res_get, target='memory')["arguments"]
    res_returned = _clean_up_reservation(res_returned)
    assert res_memfile == res_returned, "Reservation sent and returned are not the same"

    # let's check if this one didn't end up in database:
    # for now let's use commands but we should have another way to test it
    # TODO introduce directly checking host reservations entry in db
    _reservation_get("reservation-get", res_get, target='database', exp_result=3)

    # database
    res_get = {
        "identifier": "00:03:00:01:f6:f5:f4:01:01:01",
        "identifier-type": "duid",
        "subnet-id": 1
    }
    res_memfile = {
        "duid": "00:03:00:01:f6:f5:f4:01:01:01",
        "ip-addresses": [
            "2001:db8:1::b"
        ],
        "subnet-id": 1,
    }

    # set and check
    _reservation_add(res_memfile, target='database')
    res_returned = _reservation_get("reservation-get", res_get, target='database')["arguments"]
    res_returned = _clean_up_reservation(res_returned)
    assert res_memfile == res_returned, "Reservation sent and returned are not the same"

    # let's check if this one didn't end up in memory:
    _reservation_get("reservation-get", res_get, target='memory', exp_result=3)

    # check if that actually works
    srv_msg.SARR(duid="00:03:00:01:f6:f5:f4:01:01:01", address='2001:db8:1::b')
    srv_msg.SARR(duid="00:03:00:01:f6:f5:f4:f3:f2:01", address='2001:db8:1::a')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
@pytest.mark.parametrize('host_database', ['MySQL', 'PostgreSQL'])
def test_v4_memfile_with_(host_database):
    """
    Check how Kea is handling situations when reservations are saved in config file
    and in one of the supported backend. Also it checks operation-target parameter
    of the host commands
    """
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.51')
    srv_control.disable_leases_affinity()
    srv_control.open_control_channel()
    srv_control.agent_control_channel()

    srv_control.enable_db_backend_reservation(host_database)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.DORA(address='192.168.50.50', chaddr="f6:f5:f4:f3:f2:01")
    srv_msg.DORA(address='192.168.50.51', chaddr="f6:f5:f4:03:02:01")

    # let's add two different reservations, one to memfile other to database, get it and compare
    # keep in mind:
    #  memfile - target primary
    #  database - target database

    # memfile
    res_get = {
        "identifier": "f6:f5:f4:f3:f2:01",
        "identifier-type": "hw-address",
        "subnet-id": 1
    }
    res_memfile = {
        "hw-address": "f6:f5:f4:f3:f2:01",
        "ip-address": "192.168.50.150",
        "next-server": "100.10.20.30",
        "subnet-id": 1,
    }

    # set and check
    _reservation_add(res_memfile, target='memory')
    res_returned = _reservation_get("reservation-get", res_get, target='memory')["arguments"]
    res_returned = _clean_up_reservation(res_returned)
    assert res_memfile == res_returned, "Reservation sent and returned are not the same"

    # let's check if this one didn't end up in database:
    # for now let's use commands but we should have another way to test it
    # TODO introduce directly checking host reservations entry in db
    _reservation_get("reservation-get", res_get, target='database', exp_result=3)

    # database
    res_get = {
        "identifier": "f6:f5:f4:03:02:01",
        "identifier-type": "hw-address",
        "subnet-id": 1
    }
    res_memfile = {
        "hw-address": "f6:f5:f4:03:02:01",
        "ip-address": "192.168.50.200",
        "next-server": "10.1.2.3",
        "subnet-id": 1,
    }

    # set and check
    _reservation_add(res_memfile, target='database')
    res_returned = _reservation_get("reservation-get", res_get, target='database')["arguments"]
    res_returned = _clean_up_reservation(res_returned)
    assert res_memfile == res_returned, "Reservation sent and returned are not the same"

    # let's check if this one didn't end up in memory:
    _reservation_get("reservation-get", res_get, target='memory', exp_result=3)

    # check if that actually works
    srv_msg.DORA(address='192.168.50.150', chaddr="f6:f5:f4:f3:f2:01")
    srv_msg.DORA(address='192.168.50.200', chaddr="f6:f5:f4:03:02:01")


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.hosts_cmds
def test_save_reservation_to_the_config_file(dhcp_version):
    """
    Add reservation, check if all is correct and assign reservation.
    Restart Kea
    Check if reservation is gone
    Add reservation, check if all is correct, save config and restart KEA.
    Check if reservation is still accessible, assign lease.
    """
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.disable_leases_affinity()
    srv_control.open_control_channel()
    srv_control.agent_control_channel()

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # add reservation
    res_get = {
        "identifier": "f6:f5:f4:03:02:01",
        "identifier-type": "hw-address",
        "subnet-id": 1
    }
    res_memfile = {
        "hw-address": "f6:f5:f4:03:02:01",
        "ip-address": "192.168.50.200",
        "next-server": "10.1.2.3",
        "subnet-id": 1,
    }
    if dhcp_version == 'v6':
        res_get = {
            "identifier": "00:03:00:01:f6:f5:f4:f3:f2:01",
            "identifier-type": "duid",
            "subnet-id": 1
        }
        res_memfile = {
            "duid": "00:03:00:01:f6:f5:f4:f3:f2:01",
            "ip-addresses": [
                "2001:db8:1::a"
            ],
            "subnet-id": 1,
        }

    _reservation_add(res_memfile, target='memory')
    # check saved reservation
    res_returned = _reservation_get("reservation-get", res_get, target='memory')["arguments"]
    res_returned = _clean_up_reservation(res_returned)
    assert res_memfile == res_returned, "Reservation sent and returned are not the same"

    if dhcp_version == 'v6':
        srv_msg.SARR(duid="00:03:00:01:f6:f5:f4:f3:f2:01", address='2001:db8:1::a')
    else:
        srv_msg.DORA(chaddr="f6:f5:f4:03:02:01", address='192.168.50.200')

    srv_control.start_srv('DHCP', 'restarted')
    # we shouldn't get any reservation back
    _reservation_get("reservation-get", res_get, target='memory', exp_result=3)
    # let's assign lease, old are still assigned but also out of pool.

    if dhcp_version == 'v6':
        srv_msg.SARR(duid="00:03:00:01:f6:f5:f4:f3:f2:01", address='2001:db8:1::50')
    else:
        srv_msg.DORA(chaddr="f6:f5:f4:03:02:01", address='192.168.50.50')

    # let's add reservation again, and check it
    _reservation_add(res_memfile, target='memory')
    # check saved reservation
    res_returned = _reservation_get("reservation-get", res_get, target='memory')["arguments"]
    res_returned = _clean_up_reservation(res_returned)
    assert res_memfile == res_returned, "Reservation sent and returned are not the same"

    # save config file and restart Kea, filename is not defined, so it should overwrite
    # current config
    cmd = {"command": "config-write"}
    srv_msg.send_ctrl_cmd(cmd, 'http')

    srv_control.start_srv('DHCP', 'restarted')

    # and now we should have assign reserved leases:
    if dhcp_version == 'v6':
        srv_msg.SARR(duid="00:03:00:01:f6:f5:f4:f3:f2:01", address='2001:db8:1::a')
    else:
        srv_msg.DORA(chaddr="f6:f5:f4:03:02:01", address='192.168.50.200')

# TODO negative tests for operation-target in all commands
