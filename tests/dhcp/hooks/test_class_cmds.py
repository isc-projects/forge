# Copyright (C) 2022-2023 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea classification manipulation commands"""


import re

import pytest

from src import srv_msg
from src import srv_control
from src import misc


pytestmark = [pytest.mark.v4,
              pytest.mark.v6,
              pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.class_cmds]


def _setup_server_for_class_cmds(dhcp_version):
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    else:
        srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_client_classification(0, 'Client_Class_1')

    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()

    srv_control.add_hooks('libdhcp_class_cmds.so')

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')


@pytest.fixture(autouse=True)
def run_around_tests(dhcp_version):
    misc.test_setup()
    _setup_server_for_class_cmds(dhcp_version)


def test_availability(dhcp_version):  # pylint: disable=unused-argument
    response = srv_msg.send_ctrl_cmd_via_socket('{"command":"list-commands","arguments":{}}')

    for cmd in ['class-list', 'class-add', 'class-update', 'class-get', 'class-del']:
        assert cmd in response['arguments']


@pytest.mark.parametrize('channel', ['http', 'socket'])
def test_basic(channel, dhcp_version):
    # check that at the beginning there is no class
    cmd = dict(command='class-list')
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel, exp_result=3)
    assert response == {'arguments': {'client-classes': []}, 'result': 3, 'text': '0 classes found'}

    # add new class ipxe
    if dhcp_version == 'v4':
        exp_class = {'boot-file-name': '/dev/null',
                     'name': 'ipxe_efi_x64',
                     'next-server': '192.0.2.254',
                     'option-data': [],
                     'option-def': [],
                     'server-hostname': 'hal9000',
                     'test': "option[93].hex == 0x0009"}
    else:
        exp_class = {'name': 'ipxe_efi_x64',
                     'option-data': [],
                     'test': "option[93].hex == 0x0009"}
    cmd = dict(command='class-add', arguments={"client-classes": [exp_class]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {'result': 0, 'text': "Class 'ipxe_efi_x64' added"}

    # check what classes are available now
    cmd = dict(command='class-list')
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {'arguments': {'client-classes': [{'name': 'ipxe_efi_x64'}]}, 'result': 0,
                        'text': '1 class found'}

    # retrieve newly added ipxe class
    cmd = dict(command='class-get', arguments=dict(name='ipxe_efi_x64'))
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {'arguments': {'client-classes': [exp_class]},
                        'result': 0,
                        'text': "Class 'ipxe_efi_x64' definition returned"}

    # update ipxe class
    exp_class['test'] = "option[93].hex == 0x0010"    # changed from 0x0009 to 0x0010
    cmd = dict(command='class-update', arguments={"client-classes": [exp_class]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {'result': 0, 'text': "Class 'ipxe_efi_x64' updated"}

    # retrieve modified ipxe class
    cmd = dict(command='class-get', arguments=dict(name='ipxe_efi_x64'))
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {'arguments': {'client-classes': [exp_class]},
                        'result': 0,
                        'text': "Class 'ipxe_efi_x64' definition returned"}

    # delete ipxe class
    cmd = dict(command='class-del', arguments=dict(name='ipxe_efi_x64'))
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {'result': 0, 'text': "Class 'ipxe_efi_x64' deleted"}

    # check if deleted class is missing
    cmd = dict(command='class-list')
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel, exp_result=3)
    assert response == {'arguments': {'client-classes': []}, 'result': 3, 'text': '0 classes found'}

    # check if it is realy deleted
    cmd = dict(command='class-get', arguments=dict(name='ipxe_efi_x64'))
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel, exp_result=3)
    assert response == {'result': 3, 'text': "Class 'ipxe_efi_x64' not found"}


def test_add_class_and_check_traffic(dhcp_version):
    # check that at the beginning there is no class
    cmd = dict(command='class-list')
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert response == {'arguments': {'client-classes': []}, 'result': 3, 'text': '0 classes found'}

    # add class
    if dhcp_version == 'v4':
        cls = {'name': 'Client_Class_1',
               'test': "option[61].hex == 0xff010203ff041122"}
    else:
        cls = {'name': 'Client_Class_1',
               'test': "option[1].hex == 0x00030001665544332211"}
    cmd = dict(command='class-add', arguments={"client-classes": [cls]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {'result': 0, 'text': "Class 'Client_Class_1' added"}

    # check traffic
    misc.test_procedure()
    if dhcp_version == 'v4':
        srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
        srv_msg.client_does_include_with_value('client_id', 'ff:01:11:11:11:11:11:22')
        srv_msg.client_send_msg('DISCOVER')

        misc.pass_criteria()
        srv_msg.send_dont_wait_for_message()

        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
        srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
        srv_msg.client_send_msg('DISCOVER')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'OFFER')
        srv_msg.response_check_content('yiaddr', '192.168.50.50')

        misc.test_procedure()
        srv_msg.client_copy_option('server_id')
        srv_msg.client_does_include_with_value('requested_addr', '192.168.50.50')
        srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
        srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
        srv_msg.client_send_msg('REQUEST')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'ACK')
        srv_msg.response_check_content('yiaddr', '192.168.50.50')
        srv_msg.response_check_include_option(1)
        srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    else:
        srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:11:11:11:11:11:11')
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
        srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:a::1')


def test_negative_add_unknown_field(dhcp_version):  # pylint: disable=unused-argument
    # bug: #229, FIXED
    cmd = dict(command='class-add', arguments={"client-classes": [{"name": 'ipxe',
                                                                   "unknown": "123"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response['text'] == "unsupported client class parameter 'unknown'"


def test_negative_update_unknown_field(dhcp_version):
    # bug: #229, FIXED
    # add new class ipxe
    if dhcp_version == 'v4':
        exp_class = {'boot-file-name': '/dev/null',
                     'name': 'voip',
                     'next-server': '192.0.2.254',
                     'option-data': [],
                     'option-def': [],
                     'server-hostname': 'hal9000',
                     'test': "option[93].hex == 0x0009"}
    else:
        exp_class = {'name': 'voip',
                     'option-data': [],
                     'test': "option[93].hex == 0x0009"}
    cmd = dict(command='class-add', arguments={"client-classes": [exp_class]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {'result': 0, 'text': "Class 'voip' added"}

    # update unknown field
    cmd = dict(command='class-update', arguments={"client-classes": [{"name": 'voip',
                                                                      "unknown": "123"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response['text'] == "unsupported client class parameter 'unknown'"


@pytest.mark.parametrize("class_cmd", ['class-add', 'class-update'])
def test_negative_missing_class_data_1(class_cmd, dhcp_version):  # pylint: disable=unused-argument
    # bug: #254, FIXED
    cmd = dict(command=class_cmd, arguments={"client-classes": []})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    expected = f"invalid number of classes specified for the '{class_cmd}' command. Expected one class"
    assert response['text'] == expected


@pytest.mark.parametrize("class_cmd", ['class-add', 'class-update'])
def test_negative_missing_class_data_2(class_cmd, dhcp_version):  # pylint: disable=unused-argument
    # bug: #254, FIXED
    cmd = dict(command=class_cmd, arguments={"client-classes": [{}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert 'missing' in response['text'] and "'name'" in response['text']


@pytest.mark.parametrize("class_cmd", ['class-add', 'class-update', 'class-del', 'class-get'])
def test_negative_wrong_args_1(class_cmd, dhcp_version):  # pylint: disable=unused-argument
    cmd = dict(command=class_cmd, wrong_arg={"client-classes": [{"name": "ipxe"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    expected = "Error during command processing: invalid command: unsupported parameter 'wrong_arg'"
    assert response['text'] == expected


@pytest.mark.parametrize("class_cmd", ['class-add', 'class-update'])
def test_negative_wrong_args_2a(class_cmd, dhcp_version):  # pylint: disable=unused-argument
    cmd = dict(command=class_cmd, arguments={"client-classes-wrong": [{"name": "ipxe"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response['text'] == f"missing 'client-classes' argument for the '{class_cmd}' command"


@pytest.mark.parametrize("class_cmd", ['class-get', 'class-del'])
def test_negative_wrong_args_2b(class_cmd, dhcp_version):  # pylint: disable=unused-argument
    cmd = dict(command=class_cmd, arguments={"name-wrong": "ipxe"})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response['text'] == f"missing 'name' argument for the '{class_cmd}' command"


@pytest.mark.parametrize("class_cmd", ['class-add', 'class-update'])
def test_negative_wrong_args_3a(class_cmd, dhcp_version):  # pylint: disable=unused-argument
    cmd = dict(command=class_cmd, arguments={"client-classes": {"name": "ipxe"}})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response['text'] == f"'client-classes' argument specified for the '{class_cmd}' command is not a list"


@pytest.mark.parametrize("class_cmd", ['class-get', 'class-del'])
def test_negative_wrong_args_3b(class_cmd, dhcp_version):  # pylint: disable=unused-argument
    cmd = dict(command=class_cmd, arguments={"name": ["voip", "ipxe"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response['text'] == f"'name' argument specified for the '{class_cmd}' command is not a string"


@pytest.mark.parametrize("class_cmd", ['class-add', 'class-update', 'class-del', 'class-get'])
def test_negative_wrong_args_4(class_cmd, dhcp_version):  # pylint: disable=unused-argument
    cmd = dict(command=class_cmd, arguments=["client-classes"])
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response['text'] == f"invalid command '{class_cmd}': expected 'arguments' to be a map, got list instead"


@pytest.mark.parametrize("class_cmd", ['class-add', 'class-update'])
def test_negative_wrong_args_5(class_cmd, dhcp_version):  # pylint: disable=unused-argument
    cmd = dict(command=class_cmd, arguments={"client-classes": [{"name": "ipxe-1"}, {"name": "ipxe-2"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    expected = f"invalid number of classes specified for the '{class_cmd}' command. Expected one class"
    assert response['text'] == expected


@pytest.mark.parametrize("class_cmd", ['class-add', 'class-update'])
def test_negative_wrong_args_6a(class_cmd, dhcp_version):  # pylint: disable=unused-argument
    cmd = dict(command=class_cmd, arguments={"client-classes": [{"name": "ipxe-1"}], "extra-wrong": 1})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    expected = f"invalid number of arguments 2 for the '{class_cmd}' command. Expecting 'client-classes' list"
    assert response['text'] == expected


@pytest.mark.parametrize("class_cmd", ['class-get', 'class-del'])
def test_negative_wrong_args_6b(class_cmd, dhcp_version):  # pylint: disable=unused-argument
    cmd = dict(command=class_cmd, arguments={"name": "ipxe-1", "extra-wrong": 1})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    expected = f"invalid number of arguments 2 for the '{class_cmd}' command. Expecting 'name' string"
    assert response['text'] == expected


@pytest.mark.parametrize("class_cmd", ['class-get', 'class-del'])
def test_negative_wrong_args_6c(class_cmd, dhcp_version):  # pylint: disable=unused-argument
    cmd = dict(command=class_cmd, arguments={})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response['text'] == f"invalid command '{class_cmd}': 'arguments' is empty"


def test_negative_redundant_args_in_list(dhcp_version):  # pylint: disable=unused-argument
    # bug: #253, FIXED
    # bug: #432, FIXED
    cmd = dict(command='class-list', extra_arg={})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    expected = "Error during command processing: invalid command: unsupported parameter 'extra_arg'"
    assert response['text'] == expected


def test_negative_redundant_args_in_add(dhcp_version):  # pylint: disable=unused-argument
    # bug: #253, FIXED
    # bug: #432, FIXED
    cmd = dict(command='class-add', arguments={"client-classes": [{"name": "ipxe"}]}, extra_arg={})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    expected = "Error during command processing: invalid command: unsupported parameter 'extra_arg'"
    assert response['text'] == expected


def test_negative_redundant_args_in_update(dhcp_version):  # pylint: disable=unused-argument
    # bug: #253, FIXED
    # bug: #432, FIXED
    cmd = dict(command='class-update', arguments={"client-classes": [{"name": "voip"}]}, extra_arg={})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    expected = "Error during command processing: invalid command: unsupported parameter 'extra_arg'"
    assert response['text'] == expected


@pytest.mark.parametrize("class_cmd", ['class-get', 'class-del'])
def test_negative_redundant_args_in_other(class_cmd, dhcp_version):  # pylint: disable=unused-argument
    # bug: #253, FIXED
    # bug: #432, FIXED
    cmd = dict(command=class_cmd, arguments=dict(name='voip'), extra_arg={})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    expected = "Error during command processing: invalid command: unsupported parameter 'extra_arg'"
    assert response['text'] == expected


def test_negative_wrong_command_1(dhcp_version):  # pylint: disable=unused-argument
    # bug: #432, FIXED
    cmd = dict(wrong_command='class-add', arguments={"client-classes": [{"name": "ipxe"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    expected = ("Error during command processing: invalid command: "
                "does not contain mandatory 'command'")
    assert response['text'] == expected


def test_negative_wrong_command_2(dhcp_version):  # pylint: disable=unused-argument
    cmd = dict(command='class-wrong', arguments={"client-classes": [{"name": "ipxe"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=2)
    assert response['text'] == "'class-wrong' command not supported."


@pytest.mark.parametrize("class_cmd", ['class-add', 'class-update'])
def test_negative_wrong_args_7(class_cmd, dhcp_version):  # pylint: disable=unused-argument
    cmd = dict(command=class_cmd, arguments={"client-classes": ["wrong-arg"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    expected = f"invalid class definition specified for the '{class_cmd}' command. Expected a map"
    assert response['text'] == expected


@pytest.mark.parametrize("class_cmd", ['class-get', 'class-del'])
def test_negative_wrong_args_8(class_cmd, dhcp_version):  # pylint: disable=unused-argument
    cmd = dict(command=class_cmd, arguments={"name": "wrong-name"})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert response == {'result': 3, 'text': "Class 'wrong-name' not found"}


def test_negative_update_wrong_args(dhcp_version):  # pylint: disable=unused-argument
    cmd = dict(command='class-update', arguments={"client-classes": [{'name': 'missing-name'}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert response == {'result': 3, 'text': "Class 'missing-name' is not found"}


def test_stress_1(iters_factor, dhcp_version):
    iterations = 1 * iters_factor
    for idx in range(iterations):
        name = f'ipxe-{idx}'
        if dhcp_version == 'v4':
            cmd = dict(command='class-add', arguments={"client-classes": [{"name": name,
                                                                           "test": "option[93].hex == 0x0009",
                                                                           "next-server": "192.0.2.254",
                                                                           "server-hostname": "hal9000",
                                                                           "boot-file-name": "/dev/null"}]})
        else:
            cmd = dict(command='class-add', arguments={"client-classes": [{"name": name,
                                                                           "test": "option[93].hex == 0x0009"}]})

        response = srv_msg.send_ctrl_cmd(cmd)
        assert response == {'result': 0, 'text': f"Class '{name}' added"}

        cmd = dict(command='class-update', arguments={"client-classes": [{"name": name}]})
        response = srv_msg.send_ctrl_cmd(cmd)
        assert response == {'result': 0, 'text': f"Class '{name}' updated"}

        cmd = dict(command='class-list')
        response = srv_msg.send_ctrl_cmd(cmd)
        assert len(response['arguments']['client-classes']) == idx + 1

    for idx in range(iterations):
        name = f'ipxe-{idx}'
        cmd = dict(command='class-del', arguments=dict(name=name))
        response = srv_msg.send_ctrl_cmd(cmd)
        assert response == {'result': 0, 'text': f"Class '{name}' deleted"}

        cmd = dict(command='class-list')
        response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
        assert len(response['arguments']['client-classes']) == iterations - idx - 1


def test_stress_2(iters_factor, dhcp_version):
    iterations = 1 * iters_factor
    for idx in range(iterations):
        name = f'ipxe-{idx}'
        if dhcp_version == 'v4':
            cmd = dict(command='class-add', arguments={"client-classes": [{"name": name,
                                                                           "test": "option[93].hex == 0x0009",
                                                                           "next-server": "192.0.2.254",
                                                                           "server-hostname": "hal9000",
                                                                           "boot-file-name": "/dev/null"}]})
        else:
            cmd = dict(command='class-add', arguments={"client-classes": [{"name": name,
                                                                           "test": "option[93].hex == 0x0009"}]})
        response = srv_msg.send_ctrl_cmd(cmd)
        assert response == {'result': 0, 'text': f"Class '{name}' added"}

        cmd = dict(command='class-update', arguments={"client-classes": [{"name": name}]})
        response = srv_msg.send_ctrl_cmd(cmd)
        assert response == {'result': 0, 'text': f"Class '{name}' updated"}

        cmd = dict(command='class-list')
        response = srv_msg.send_ctrl_cmd(cmd)
        assert len(response['arguments']['client-classes']) == 1

        cmd = dict(command='class-del', arguments=dict(name=name))
        response = srv_msg.send_ctrl_cmd(cmd)
        assert response == {'result': 0, 'text': f"Class '{name}' deleted"}

        cmd = dict(command='class-list')
        response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
        assert len(response['arguments']['client-classes']) == 0


def test_negative_missing_dependency(dhcp_version):
    if dhcp_version == 'v4':
        cmd = dict(command='class-add', arguments={"client-classes": [{"name": "ipxe_efi_x64",
                                                                       "test": "member('missing_class')",
                                                                       "next-server": "192.0.2.254",
                                                                       "server-hostname": "hal9000",
                                                                       "boot-file-name": "/dev/null"}]})
    else:
        cmd = dict(command='class-add', arguments={"client-classes": [{"name": "ipxe_efi_x64",
                                                                       "test": "member('missing_class')"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "expression: [member('missing_class')] error" in response['text']
    assert "Not defined client class 'missing_class' at" in response['text']


def test_negative_break_dependency(dhcp_version):
    # add new class ipxe
    if dhcp_version == 'v4':
        cls = {'boot-file-name': '/dev/null',
               'name': 'voip',
               'next-server': '192.0.2.254',
               'option-data': [],
               'option-def': [],
               'server-hostname': 'hal9000',
               'test': "option[93].hex == 0x0009"}
    else:
        cls = {'name': 'voip',
               'test': "option[93].hex == 0x0009"}
    cmd = dict(command='class-add', arguments={"client-classes": [cls]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {'result': 0, 'text': "Class 'voip' added"}

    # add second class that refers voip class
    if dhcp_version == 'v4':
        cmd = dict(command='class-add', arguments={"client-classes": [{"name": "ipxe_efi_x64",
                                                                       "test": "member('voip')",
                                                                       "next-server": "192.0.2.254",
                                                                       "server-hostname": "hal9000",
                                                                       "boot-file-name": "/dev/null"}]})
    else:
        cmd = dict(command='class-add', arguments={"client-classes": [{"name": "ipxe_efi_x64",
                                                                       "test": "member('voip')"}]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {'result': 0, 'text': "Class 'ipxe_efi_x64' added"}

    cmd = dict(command='class-del', arguments=dict(name='voip'))
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response['text'] == "Class 'voip' is used by class 'ipxe_efi_x64'"


def test_negative_change_dependency(dhcp_version):
    # add new class ipxe
    if dhcp_version == 'v4':
        cls = {'boot-file-name': '/dev/null',
               'name': 'voip',
               'next-server': '192.0.2.254',
               'option-data': [],
               'option-def': [],
               'server-hostname': 'hal9000',
               'test': "option[93].hex == 0x0009"}
    else:
        cls = {'name': 'voip',
               'option-data': [],
               'test': "option[93].hex == 0x0009"}
    cmd = dict(command='class-add', arguments={"client-classes": [cls]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {'result': 0, 'text': "Class 'voip' added"}

    # update class
    cmd = dict(command='class-update', arguments={"client-classes": [{'name': 'voip',
                                                                      'test': "member('KNOWN')"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    expected = ("modification of the class 'voip' would affect its dependency on the KNOWN and/or "
                "UNKNOWN built-in classes. Such modification is not allowed because there may be "
                "other classes depending on those built-ins via the updated class")
    assert response['text'] == expected
