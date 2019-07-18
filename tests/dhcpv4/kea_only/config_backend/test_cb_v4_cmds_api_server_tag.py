"""Kea database config backend commands hook testing"""

import pytest
import srv_msg
from cb_model import setup_server_for_config_backend_cmds

pytestmark = [pytest.mark.py_test,
              pytest.mark.v4,
              pytest.mark.kea_only,
              pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.config_backend,
              pytest.mark.cb_cmds]


@pytest.fixture(autouse=True)
def run_around_tests():
    # we still can use server configured with one server tag
    setup_server_for_config_backend_cmds(server_tag="abc")


def _set_option_def(channel='http'):
    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 222,
                                                                "type": "uint32"}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"option-defs": [{"code": 222, "space": "dhcp4"}]},
                        "result": 0, "text": "DHCPv4 option definition successfully set."}


@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_remote_option_def4_set_basic(channel):
    _set_option_def(channel=channel)


def test_remote_option_def4_set_using_zero_as_code():
    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 0,
                                                                "type": "uint32"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "invalid option code '0': reserved for PAD" in response["text"]


def test_remote_option_def4_set_using_standard_code():
    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 24,
                                                                "type": "uint32"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"option-defs": [{"code": 1, "space": "dhcp4"}]},
                        "result": 0, "text": "DHCPv4 option definition successfully set."}


def test_remote_option_def4_set_missing_parameters():
    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "code": 222,
                                                                "type": "uint32",
                                                                "array": False,
                                                                "record-types": "",
                                                                "space": "dhcp4",
                                                                "encapsulate": ""}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "missing parameter 'name'" in response["text"]

    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "aa",
                                                                "type": "uint32",
                                                                "array": False,
                                                                "record-types": "",
                                                                "space": "dhcp4",
                                                                "encapsulate": ""}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "missing parameter 'code'" in response["text"]

    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "aa",
                                                                "code": 234,
                                                                "array": False,
                                                                "record-types": "",
                                                                "space": "dhcp4",
                                                                "encapsulate": ""}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "missing parameter 'type'" in response["text"]


@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_remote_option_def4_get_basic(channel):
    _set_option_def()

    cmd = dict(command="remote-option-def4-get", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "code": 222}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {"arguments": {"count": 1, "option-defs": [{"array": False, "code": 222, "encapsulate": "",
                                                                   "name": "foo", "record-types": "", "space": "dhcp4",
                                                                   "metadata": {"server-tag": "all"},
                                                                   "type": "uint32"}]},
                        "result": 0, "text": "DHCPv4 option definition 222 in 'dhcp4' found."}


def test_remote_option_def4_get_multiple_defs():
    _set_option_def()

    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 222,
                                                                "type": "uint32",
                                                                "space": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"option-defs": [{"code": 222, "space": "abc"}]},
                        "result": 0, "text": "DHCPv4 option definition successfully set."}

    cmd = dict(command="remote-option-def4-get", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "code": 222,
                                                                "space": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1, "option-defs": [{"array": False, "code": 222, "encapsulate": "",
                                                                   "name": "foo", "record-types": "", "space": "abc",
                                                                   "metadata": {"server-tag": "all"},
                                                                   "type": "uint32"}]},
                        "result": 0, "text": "DHCPv4 option definition 222 in 'abc' found."}


def test_remote_option_def4_get_missing_code():
    cmd = dict(command="remote-option-def4-get", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "missing 'code' parameter"}


def test_remote_option_def4_get_all_option_not_defined():
    cmd = dict(command="remote-option-def4-get-all", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "option-defs": []},
                        "result": 3, "text": "0 DHCPv4 option definition(s) found."}


def test_remote_option_def4_get_all_multiple_defs():
    _set_option_def()

    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 222,
                                                                "type": "uint32",
                                                                "space": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"option-defs": [{"code": 222, "space": "abc"}]},
                        "result": 0, "text": "DHCPv4 option definition successfully set."}

    cmd = dict(command="remote-option-def4-get-all", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 2, "option-defs": [{"array": False, "code": 222,
                                                                   "encapsulate": "", "name": "foo",
                                                                   "record-types": "", "space": "abc",
                                                                   "metadata": {"server-tag": "all"},
                                                                   "type": "uint32"},
                                                                  {"array": False, "code": 222,
                                                                   "encapsulate": "", "name": "foo",
                                                                   "record-types": "", "space": "dhcp4",
                                                                   "metadata": {"server-tag": "all"},
                                                                   "type": "uint32"}]},
                        "result": 0, "text": "2 DHCPv4 option definition(s) found."}


@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_remote_option_def4_get_all_basic(channel):
    _set_option_def()

    cmd = dict(command="remote-option-def4-get-all", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {"arguments": {"count": 1, "option-defs": [{"array": False, "code": 222, "encapsulate": "",
                                                                   "metadata": {"server-tag": "all"},
                                                                   "name": "foo", "record-types": "", "space": "dhcp4",
                                                                   "type": "uint32"}]},
                        "result": 0, "text": "1 DHCPv4 option definition(s) found."}


@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_remote_option_def4_del_basic(channel):
    _set_option_def()

    cmd = dict(command="remote-option-def4-del", arguments={"remote": {"type": "mysql"},
                                                            "option-defs": [{"code": 222}]})

    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv4 option definition(s) deleted."}


def test_remote_option_def4_del_different_space():
    _set_option_def()

    cmd = dict(command="remote-option-def4-del", arguments={"remote": {"type": "mysql"},
                                                            "option-defs": [{"code": 222, "space": "abc"}]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 DHCPv4 option definition(s) deleted."}


def test_remote_option_def4_del_incorrect_code():
    cmd = dict(command="remote-option-def4-del", arguments={"remote": {"type": "mysql"}, "option-defs": [{"name": 22}]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "missing 'code' parameter"}

    cmd = dict(command="remote-option-def4-del", arguments={"remote": {"type": "mysql"}, "option-defs": [{}]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "missing 'code' parameter"}

    cmd = dict(command="remote-option-def4-del", arguments={"remote": {"type": "mysql"},
                                                            "option-defs": [{"code": "abc"}]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "'code' parameter is not an integer"}


def test_remote_option_def4_del_missing_option():
    cmd = dict(command="remote-option-def4-del", arguments={"remote": {"type": "mysql"},
                                                            "option-defs": [{"code": 212}]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 DHCPv4 option definition(s) deleted."}


def test_remote_option_def4_del_multiple_options():
    _set_option_def()

    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 222,
                                                                "type": "uint32",
                                                                "space": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"option-defs": [{"code": 222, "space": "abc"}]},
                        "result": 0, "text": "DHCPv4 option definition successfully set."}

    cmd = dict(command="remote-option-def4-del", arguments={"remote": {"type": "mysql"},
                                                            "option-defs": [{"code": 222}]})

    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv4 option definition(s) deleted."}

    cmd = dict(command="remote-option-def4-get-all", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1, "option-defs": [{"array": False, "code": 222, "encapsulate": "",
                                                                   "metadata": {"server-tag": "all"},
                                                                   "name": "foo", "record-types": "", "space": "abc",
                                                                   "type": "uint32"}]},
                        "result": 0, "text": "1 DHCPv4 option definition(s) found."}


def _set_global_option():
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "code": 6,
                                                                   "data": "192.0.2.1, 192.0.2.2"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"result": 0, "text": "DHCPv4 option successfully set.",
                        "arguments": {"options": [{"code": 6, "space": "dhcp4"}]}}


def test_remote_global_option4_global_set_basic():
    _set_global_option()


@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_remote_global_option4_global_set_missing_data(channel):
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "code": 6}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel, exp_result=3)
    # bug #501
    assert response == {"result": 3, "text": "Missing data parameter"}


def test_remote_global_option4_global_set_name():
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "name": "host-name",
                                                                   "data": "isc.example.com"}]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"options": [{"code": 12, "space": "dhcp4"}]},
                        "result": 0, "text": "DHCPv4 option successfully set."}


def test_remote_global_option4_global_set_incorrect_code_missing_name():
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "code": "aaa"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "option data configuration requires one of " \
           "'code' or 'name' parameters to be specified" in response["text"]


def test_remote_global_option4_global_set_incorrect_name_missing_code():
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "name": 123}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "option data configuration requires one of " \
           "'code' or 'name' parameters to be specified" in response["text"]


def test_remote_global_option4_global_set_missing_code_and_name():
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "option data configuration requires one of " \
           "'code' or 'name' parameters to be specified" in response["text"]


def test_remote_global_option4_global_set_incorrect_code():
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": "aa",
                                                                            "name": "cc"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "definition for the option 'dhcp4.cc' having code '0' does not exist" in response["text"]

    assert False, "looks like incorrect message"
    # bug/not implemented feature


def test_remote_global_option4_global_set_incorrect_name():
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 12,
                                                                            "name": 12,
                                                                            "data": 'isc.example.com'}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"bug, shouldn't be accepted?"}


@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_remote_global_option4_global_get_basic(channel):
    _set_global_option()

    cmd = dict(command="remote-option4-global-get", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {"arguments": {"count": 1, "options": [{"always-send": False, "code": 6, "csv-format": True,
                                                               "data": "192.0.2.1, 192.0.2.2",
                                                               "metadata": {"server-tag": "all"},
                                                               "name": "domain-name-servers", "space": "dhcp4"}]},
                        "result": 0, "text": "DHCPv4 option 6 in 'dhcp4' found."}


def test_remote_global_option4_global_set_different_space():
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6,
                                                                            "data": '192.0.2.1, 192.0.2.2',
                                                                            "always-send": True,
                                                                            "csv-format": True,
                                                                            "space": "xyz"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "definition for the option 'xyz.' having code '6' does not exist" in response["text"]


def test_remote_global_option4_global_set_csv_false_incorrect():
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6,
                                                                            "data": '192.0.2.1',
                                                                            "always-send": True,
                                                                            "csv-format": False}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "option data is not a valid string of hexadecimal digits: 192.0.2.1" in response["text"]


def test_remote_global_option4_global_set_csv_false_correct():
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6,
                                                                            "data": "C0000201",  # 192.0.2.1
                                                                            "always-send": True,
                                                                            "csv-format": False}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"result": 0, "text": "DHCPv4 option successfully set.",
                        "arguments": {"options": [{"code": 6, "space": "dhcp4"}]}}


def test_remote_global_option4_global_set_csv_false_incorrect_hex():
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6,
                                                                            "data": "C0000201Z",
                                                                            "always-send": True,
                                                                            "csv-format": False}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "option data is not a valid string of hexadecimal digits: C0000201Z" in response["text"]


@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_remote_global_option4_global_del_basic(channel):
    _set_global_option()

    cmd = dict(command="remote-option4-global-del", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv4 option(s) deleted."}


def test_remote_global_option4_global_del_missing_code():
    cmd = dict(command="remote-option4-global-del", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"ab": 6}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "missing 'code' parameter"}


def test_remote_global_option4_global_del_incorrect_code():
    cmd = dict(command="remote-option4-global-del", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": "6"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "'code' parameter is not an integer"}


def test_remote_global_option4_global_del_missing_option():
    cmd = dict(command="remote-option4-global-del", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 DHCPv4 option(s) deleted."}


def test_remote_global_option4_global_get_missing_code():
    cmd = dict(command="remote-option4-global-get", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"ab": 6}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "missing 'code' parameter"}


def test_remote_global_option4_global_get_incorrect_code():
    cmd = dict(command="remote-option4-global-get", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": "6"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "'code' parameter is not an integer"}


def test_remote_global_option4_global_get_missing_option():
    cmd = dict(command="remote-option4-global-get", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert response == {"arguments": {"count": 0, "options": []},
                        "result": 3, "text": "DHCPv4 option 6 in 'dhcp4' not found."}


def test_remote_global_option4_global_get_csv_false():
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6,
                                                                            "data": "C0000301C0000302",
                                                                            "always-send": True,
                                                                            "csv-format": False}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"result": 0, "text": "DHCPv4 option successfully set.",
                        "arguments": {"options": [{"code": 6, "space": "dhcp4"}]}}

    cmd = dict(command="remote-option4-global-get", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6}]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1, "options": [{"always-send": True, "code": 6, "csv-format": False,
                                                               "data": "C0000301C0000302",
                                                               "metadata": {"server-tag": "all"},
                                                               "name": "domain-name-servers", "space": "dhcp4"}]},
                        "result": 0, "text": "DHCPv4 option 6 in 'dhcp4' found."}


def test_remote_global_option4_global_get_all():
    _set_global_option()

    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "code": 16,
                                                                   "data": "199.199.199.1"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"result": 0, "text": "DHCPv4 option successfully set.",
                        "arguments": {"options": [{"code": 16, "space": "dhcp4"}]}}

    cmd = dict(command="remote-option4-global-get-all", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 2,
                                      "options": [{"always-send": False, "code": 6, "csv-format": True,
                                                   "metadata": {"server-tag": "all"},
                                                   "data": "192.0.2.1, 192.0.2.2", "name": "domain-name-servers",
                                                   "space": "dhcp4"},
                                                  {"always-send": False, "code": 16, "csv-format": True,
                                                   "metadata": {"server-tag": "all"},
                                                   "data": "199.199.199.1", "name": "swap-server", "space": "dhcp4"}]},
                        "result": 0, "text": "2 DHCPv4 option(s) found."}

    cmd = dict(command="remote-option4-global-del", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6}]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv4 option(s) deleted."}

    cmd = dict(command="remote-option4-global-get-all", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1, "options": [{"always-send": False, "code": 16, "csv-format": True,
                                                               "data": "199.199.199.1", "name": "swap-server",
                                                               "metadata": {"server-tag": "all"},
                                                               "space": "dhcp4"}]},
                        "result": 0, "text": "1 DHCPv4 option(s) found."}

    cmd = dict(command="remote-option4-global-del", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 16}]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv4 option(s) deleted."}

    cmd = dict(command="remote-option4-global-get-all", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert response == {"arguments": {"count": 0, "options": []}, "result": 3, "text": "0 DHCPv4 option(s) found."}


def _set_server_tag(tag="abc"):
    cmd = dict(command="remote-server4-set", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": tag,
                                                                     "description": "some server"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    assert response == {"result": 0, "text": "DHCPv4 server successfully set.",
                        "arguments": {"servers": [{"server-tag": tag, "description": "some server"}]}}


def test_remote_server_tag_set():
    _set_server_tag()


@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_remote_server_tag_set_missing_tag(channel):
    cmd = dict(command="remote-server4-set", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"description": "some server"}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel, exp_result=1)

    assert response == {"result": 1, "text": "missing 'server-tag' parameter"}


def test_remote_server_tag_set_incorrect_tag():
    cmd = dict(command="remote-server4-set", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": 123}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "'server-tag' parameter is not a string"}


def test_remote_server_tag_set_empty_tag():
    cmd = dict(command="remote-server4-set", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": ""}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "server-tag must not be empty"}


def test_remote_server_tag_set_missing_description():
    cmd = dict(command="remote-server4-set", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": "someserver"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    assert response == {"arguments": {"servers": [{"description": "", "server-tag": "someserver"}]},
                        "result": 0, "text": "DHCPv4 server successfully set."}


def test_remote_server_tag_set_missing_servers():
    cmd = dict(command="remote-server4-set", arguments={"remote": {"type": "mysql"}})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "'servers' parameter must be specified and must be a list"}


def test_remote_server_tag_set_empty_servers():
    cmd = dict(command="remote-server4-set", arguments={"remote": {"type": "mysql"},
                                                        "servers": []})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "'servers' list must include exactly one element"}


def test_remote_server_tag_set_multiple_servers():
    cmd = dict(command="remote-server4-set", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": "someserver"},
                                                                    {"server-tag": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "'servers' list must include exactly one element"}


def test_remote_server_tag_get():
    _set_server_tag()
    cmd = dict(command="remote-server4-get", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    assert response == {"arguments": {"count": 1, "servers": [{"description": "some server", "server-tag": "abc"}]},
                        "result": 0, "text": "DHCPv4 server 'abc' found."}


def test_remote_server_tag_get_non_existing_tag():
    cmd = dict(command="remote-server4-get", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "servers": []},
                        "result": 3, "text": "DHCPv4 server 'abc' not found."}


def test_remote_server_tag_get_empty_tag():
    _set_server_tag()
    cmd = dict(command="remote-server4-get", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": ""}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "server-tag must not be empty"}


def test_remote_server_tag_get_missing_tag():
    _set_server_tag()
    cmd = dict(command="remote-server4-get", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "missing 'server-tag' parameter"}


def test_remote_server_tag_del():
    _set_server_tag()
    cmd = dict(command="remote-server4-del", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv4 server(s) deleted."}

    cmd = dict(command="remote-server4-get", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "servers": []},
                        "result": 3, "text": "DHCPv4 server 'abc' not found."}


def test_remote_server_tag_del_all():
    _set_server_tag()
    cmd = dict(command="remote-server4-del", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": "all"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1,
                        "text": "'all' is a name reserved for the server tag which associates the configuration "
                                "elements with all servers connecting to the database and may not be deleted"}

    # "all" can't be -get
    # cmd = dict(command="remote-server4-get", arguments={"remote": {"type": "mysql"},
    #                                                     "servers": [{"server-tag": "all"}]})
    #
    # srv_msg.send_ctrl_cmd(cmd)


def test_remote_server_tag_del_non_existing_tag():
    cmd = dict(command="remote-server4-del", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 DHCPv4 server(s) deleted."}


def test_remote_server_tag_del_empty_tag():
    _set_server_tag()
    cmd = dict(command="remote-server4-del", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": ""}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "server-tag must not be empty"}


def test_remote_server_tag_del_missing_tag():
    _set_server_tag()
    cmd = dict(command="remote-server4-del", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "missing 'server-tag' parameter"}


def test_remote_server_tag_get_all():
    _set_server_tag()
    _set_server_tag(tag="xyz")
    cmd = dict(command="remote-server4-get-all", arguments={"remote": {"type": "mysql"}})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    assert response == {"arguments": {"count": 2,
                                      "servers": [{"description": "some server", "server-tag": "abc"},
                                                  {"description": "some server", "server-tag": "xyz"}]},
                        "result": 0, "text": "2 DHCPv4 server(s) found."}


def test_remote_server_tag_get_all_no_tags():
    cmd = dict(command="remote-server4-get-all", arguments={"remote": {"type": "mysql"}})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "servers": []}, "result": 3, "text": "0 DHCPv4 server(s) found."}


def test_remote_server_tag_get_all_one_tags():
    _set_server_tag()

    cmd = dict(command="remote-server4-get-all", arguments={"remote": {"type": "mysql"}})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    assert response == {"arguments": {"count": 1,
                                      "servers": [{"description": "some server", "server-tag": "abc"}]},
                        "result": 0, "text": "1 DHCPv4 server(s) found."}


def _add_server_tag(server_tag=None):
    cmd = dict(command="remote-server4-set", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": server_tag}]})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)


def _subnet_set(server_tags, subnet_id, pool, exp_result=0, subnet="192.168.50.0/24", ):
    cmd = dict(command="remote-subnet4-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": server_tags,
                                                        "subnets": [{"subnet": subnet, "id": subnet_id,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": pool}]}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)

    assert response == {"arguments": {"subnets": [{"id": subnet_id, "subnet": subnet}]},
                        "result": 0, "text": "IPv4 subnet successfully set."}


def _subnet_get(command, exp_result=0, subnet_parameter=None):
    cmd = dict(command=command, arguments={"remote": {"type": "mysql"}})
    if subnet_parameter:
        cmd["arguments"]["subnets"] = [subnet_parameter]

    return srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)


def _subnet_list(command, server_tags, exp_result=0):
    cmd = dict(command=command, arguments={"remote": {"type": "mysql"}, "server-tags": server_tags})

    return srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)


def _subnet_del(exp_result=0, subnet_parameter=None):
    return _subnet_get("remote-subnet4-del-by-id", exp_result=exp_result, subnet_parameter=subnet_parameter)


def _check_subnet_result(resp, server_tags, count=1, subnet_id=5, subnet="192.168.50.0/24"):
    assert resp["result"] == 0
    assert resp["arguments"]["count"] == count
    assert resp["arguments"]["subnets"][0]["metadata"] == {"server-tags": server_tags}
    assert resp["arguments"]["subnets"][0]["subnet"] == subnet
    assert resp["arguments"]["subnets"][0]["id"] == subnet_id


def test_remote_subnet4_get_server_tags():
    _add_server_tag("abc")
    _add_server_tag("xyz")
    _subnet_set(server_tags=["abc", "xyz"], subnet_id=5, pool="192.168.50.1-192.168.50.100")
    _subnet_set(server_tags=["xyz"], subnet_id=6, pool="192.168.53.1-192.168.53.10", subnet="192.168.53.0/24")
    _subnet_set(server_tags=["all"], subnet_id=7, pool="192.168.51.1-192.168.51.10", subnet="192.168.51.0/24")

    resp = _subnet_get(command="remote-subnet4-get-by-id", subnet_parameter={"id": 5})
    _check_subnet_result(resp, server_tags=["abc", "xyz"], subnet_id=5)

    resp = _subnet_get(command="remote-subnet4-get-by-id", subnet_parameter={"id": 6})
    _check_subnet_result(resp, server_tags=["xyz"], subnet_id=6, subnet="192.168.53.0/24")

    resp = _subnet_get(command="remote-subnet4-get-by-prefix",
                       subnet_parameter={"subnet": "192.168.53.0/24"})
    _check_subnet_result(resp, server_tags=["xyz"], subnet_id=6, subnet="192.168.53.0/24")

    resp = _subnet_get(command="remote-subnet4-get-by-prefix",
                       subnet_parameter={"subnet": "192.168.50.0/24"})
    _check_subnet_result(resp, server_tags=["abc", "xyz"], subnet_id=5)

    resp = _subnet_list(command="remote-subnet4-list", server_tags=["abc"])
    # not sure if this is how it suppose to work
    _check_subnet_result(resp, server_tags=["abc", "xyz"], count=2, subnet_id=5)

    resp = _subnet_list(command="remote-subnet4-list", server_tags=["xyz"])
    _check_subnet_result(resp, server_tags=["abc", "xyz"], count=3, subnet_id=5)
    assert resp["arguments"]["subnets"][1]["subnet"] == "192.168.53.0/24"
    assert resp["arguments"]["subnets"][1]["id"] == 6
    assert resp["arguments"]["subnets"][2]["subnet"] == "192.168.51.0/24"
    assert resp["arguments"]["subnets"][2]["id"] == 7

def test_remote_subnet4_get_server_tags_all_incorrect_setup():
    # Configure 2 subnet with the same id but different tags will result with just one subnet in configuration
    # the first one will be overwritten
    _add_server_tag("abc")
    _add_server_tag("xyz")
    _subnet_set(server_tags=["abc"], subnet_id=5, pool="192.168.50.1-192.168.50.100")
    _subnet_set(server_tags=["xyz"], subnet_id=5, pool="192.168.50.1-192.168.50.10")

    resp = _subnet_get(command="remote-subnet4-get-by-id", subnet_parameter={"id": 5})
    _check_subnet_result(resp, server_tags=["xyz"], subnet_id=5)


def test_remote_subnet4_del_server_tags():
    _add_server_tag("abc")
    _add_server_tag("xyz")
    _subnet_set(server_tags=["abc"], subnet_id=5, pool="192.168.50.1-192.168.50.100")
    _subnet_set(server_tags=["xyz"], subnet_id=6, pool="192.168.53.1-192.168.53.10", subnet="192.168.53.0/24")
    _subnet_set(server_tags=["all"], subnet_id=7, pool="192.168.51.1-192.168.51.10", subnet="192.168.51.0/24")

    resp = _subnet_get(command="remote-subnet4-get-by-id", subnet_parameter={"id": 5})
    _check_subnet_result(resp, server_tags=["abc"], subnet_id=5)

    resp = _subnet_get(command="remote-subnet4-get-by-id", subnet_parameter={"id": 6})
    _check_subnet_result(resp, server_tags=["xyz"], subnet_id=6, subnet="192.168.53.0/24")

    resp = _subnet_get(command="remote-subnet4-get-by-id", subnet_parameter={"id": 7})
    _check_subnet_result(resp, server_tags=["all"], subnet_id=7, subnet="192.168.51.0/24")

    # we should delete just one
    resp = _subnet_del(subnet_parameter={"id": 6})
    assert resp["arguments"]["count"] == 1
    assert resp["result"] == 0

    # since this one was just removed now we expect error
    resp = _subnet_del(subnet_parameter={"id": 6}, exp_result=3)
    assert resp["arguments"]["count"] == 0
    assert resp["result"] == 3

    # those two should still be configured
    resp = _subnet_get(command="remote-subnet4-get-by-id", subnet_parameter={"id": 5})
    _check_subnet_result(resp, server_tags=["abc"], subnet_id=5)

    resp = _subnet_get(command="remote-subnet4-get-by-id", subnet_parameter={"id": 7})
    _check_subnet_result(resp, server_tags=["all"], subnet_id=7, subnet="192.168.51.0/24")

    resp = _subnet_del(subnet_parameter={"id": 7})
    assert resp["arguments"]["count"] == 1
    assert resp["result"] == 0

    resp = _subnet_get(command="remote-subnet4-get-by-id", subnet_parameter={"id": 5})
    _check_subnet_result(resp, server_tags=["abc"], subnet_id=5)

    resp = _subnet_get(command="remote-subnet4-get-by-id", subnet_parameter={"id": 7}, exp_result=3)
    assert resp["arguments"]["count"] == 0
    assert resp["result"] == 3


def _network_set(server_tags, network_name="florX", exp_result=0):
    cmd = dict(command="remote-network4-set", arguments={"remote": {"type": "mysql"}, "server-tags": server_tags,
                                                         "shared-networks": [{"name": network_name}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)

    assert response == {"arguments": {"shared-networks": [{"name": network_name}]},
                        "result": 0, "text": "IPv4 shared network successfully set."}


def _network_get(command, exp_result=0, network_parameter=None):
    cmd = dict(command=command, arguments={"remote": {"type": "mysql"}})
    if network_parameter:
        cmd["arguments"]["shared-networks"] = [network_parameter]

    return srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)


def _network_list(command, server_tags, exp_result=0):
    cmd = dict(command=command, arguments={"remote": {"type": "mysql"}, "server-tags": server_tags})

    return srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)


def _network_del(exp_result=0, network_parameter=None):
    return _network_get("remote-network4-del", exp_result=exp_result, network_parameter=network_parameter)


def _network_check_res(resp, server_tags, count=1, network_name="florX"):
    assert resp["result"] == 0
    assert resp["arguments"]["count"] == count
    assert resp["arguments"]["shared-networks"][0]["metadata"] == {"server-tags": server_tags}
    assert resp["arguments"]["shared-networks"][0]["name"] == network_name


def test_remote_network4_get_server_tags():
    _add_server_tag("abc")
    _add_server_tag("xyz")
    _network_set(server_tags=["abc"])
    _network_set(server_tags=["xyz"], network_name="flor1")
    _network_set(server_tags=["all"], network_name="top_flor")

    resp = _network_get(command="remote-network4-get", network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=["abc"], network_name="florX")

    resp = _network_get(command="remote-network4-get", network_parameter={"name": "flor1"})
    _network_check_res(resp, server_tags=["xyz"], network_name="flor1")

    resp = _network_list(command="remote-network4-list", server_tags=["xyz"])
    _network_check_res(resp, server_tags=["xyz"], count=2, network_name="flor1")

    assert resp["arguments"]["shared-networks"][1]["metadata"] == {"server-tags": ["all"]}
    assert resp["arguments"]["shared-networks"][1]["name"] == "top_flor"


def test_remote_network4_get_server_tags_all_incorrect_setup():
    # Configure 2 networks with the same name but different tags will result with just one network in configuration
    # the first one will be overwritten
    _add_server_tag("abc")
    _add_server_tag("xyz")
    _network_set(server_tags=["abc"])
    _network_set(server_tags=["xyz"])

    resp = _network_get(command="remote-network4-get", network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=["xyz"], network_name="florX")


def test_remote_network4_del_server_tags():
    _add_server_tag("abc")
    _add_server_tag("xyz")
    _network_set(server_tags=["abc"])
    _network_set(server_tags=["xyz"], network_name="flor1")
    _network_set(server_tags=["all"], network_name="top_flor")

    resp = _network_get(command="remote-network4-get", network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=["abc"], network_name="florX")

    resp = _network_get(command="remote-network4-get", network_parameter={"name": "flor1"})
    _network_check_res(resp, server_tags=["xyz"], network_name="flor1")

    resp = _network_get(command="remote-network4-get", network_parameter={"name": "top_flor"})
    _network_check_res(resp, server_tags=["all"], network_name="top_flor")

    _network_del(network_parameter={"name": "flor1"})
    assert resp["arguments"]["count"] == 1
    assert resp["result"] == 0

    resp = _network_get(command="remote-network4-get", network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=["abc"], network_name="florX")

    # removed, so it should not be returned
    resp = _network_get(command="remote-network4-get", network_parameter={"name": "flor1"}, exp_result=3)
    assert resp["result"] == 3
    assert resp["arguments"]["count"] == 0

    resp = _network_get(command="remote-network4-get", network_parameter={"name": "top_flor"})
    _network_check_res(resp, server_tags=["all"], network_name="top_flor")

    resp = _network_del(network_parameter={"name": "top_flor"})
    assert resp["arguments"]["count"] == 1
    assert resp["result"] == 0

    resp = _network_get(command="remote-network4-get", network_parameter={"name": "florX"})
    _network_check_res(resp, server_tags=["abc"], network_name="florX")

    # removed, so it should not be returned
    resp = _network_get(command="remote-network4-get", network_parameter={"name": "top_flor"}, exp_result=3)
    assert resp["result"] == 3
    assert resp["arguments"]["count"] == 0


def _option_set(server_tags, exp_result=0, code=3, opt_data="1.1.1.1"):
    cmd = dict(command="remote-option4-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": server_tags,
                                                               "options": [{
                                                                   "code": code,
                                                                   "data": opt_data}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)

    assert response == {"result": 0, "text": "DHCPv4 option successfully set.",
                        "arguments": {"options": [{"code": code, "space": "dhcp4"}]}}


def _option_get(command, server_tags, exp_result=0, opt_code=None):
    cmd = dict(command=command, arguments={"remote": {"type": "mysql"},
                                           "server-tags": server_tags})

    if opt_code:
        cmd["arguments"]["options"] = [{"code": opt_code}]

    return srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)


def _option_del(server_tags, exp_result=0, opt_code=None):
    return _option_get("remote-option4-global-del", server_tags=server_tags, exp_result=exp_result, opt_code=opt_code)


def _check_option_result(resp, server_tags, count=1, opt_name=None, opt_data=None):
    assert resp["result"] == 0
    assert resp["arguments"]["count"] == count
    assert resp["arguments"]["options"][0]["metadata"] == {"server-tags": server_tags}
    assert resp["arguments"]["options"][0]["name"] == opt_name
    assert resp["arguments"]["options"][0]["data"] == opt_data


def test_remote_option4_get_server_tags_all():
    # simple test for one ticket https://gitlab.isc.org/isc-projects/kea/issues/737
    _add_server_tag("abc")
    _option_set(server_tags=["all"], opt_data='3.3.3.3')
    resp = _option_get(command="remote-option4-global-get-all", server_tags=["abc"], opt_code=3)
    _check_option_result(resp, count=1, server_tags=["all"], opt_name="routers", opt_data="3.3.3.3")


def test_remote_option4_get_server_tags():
    _add_server_tag("abc")
    _add_server_tag("xyz")
    _option_set(server_tags=["abc"])
    _option_set(server_tags=["xyz"], opt_data='2.2.2.2')
    _option_set(server_tags=["all"], opt_data='3.3.3.3')

    resp = _option_get(command="remote-option4-global-get", server_tags=["abc"], opt_code=3)
    _check_option_result(resp, server_tags=["abc"], opt_name="routers", opt_data="1.1.1.1")

    resp = _option_get(command="remote-option4-global-get", server_tags=["xyz"], opt_code=3)
    _check_option_result(resp, server_tags=["xyz"], opt_name="routers", opt_data="2.2.2.2")

    resp = _option_get(command="remote-option4-global-get", server_tags=["all"], opt_code=3)
    _check_option_result(resp, server_tags=["all"], opt_name="routers", opt_data="3.3.3.3")

    _option_set(server_tags=["abc"], code=4, opt_data='6.6.6.6')

    resp = _option_get(command="remote-option4-global-get-all", server_tags=["abc"], opt_code=3)
    _check_option_result(resp, count=2, server_tags=["abc"], opt_name="routers", opt_data="1.1.1.1")
    assert resp["arguments"]["options"][1]["metadata"] == {"server-tags": ["abc"]}
    assert resp["arguments"]["options"][1]["name"] == "time-servers"
    assert resp["arguments"]["options"][1]["data"] == "6.6.6.6"

    resp = _option_get(command="remote-option4-global-get-all", server_tags=["xyz"], opt_code=3)
    _check_option_result(resp, count=1, server_tags=["xyz"], opt_name="routers", opt_data="2.2.2.2")


def test_remote_option4_del_server_tags():
    _add_server_tag("abc")
    _add_server_tag("xyz")
    _option_set(server_tags=["abc"])
    _option_set(server_tags=["xyz"], opt_data='2.2.2.2')
    _option_set(server_tags=["all"], opt_data='3.3.3.3')

    resp = _option_get(command="remote-option4-global-get", server_tags=["abc"], opt_code=3)
    _check_option_result(resp, server_tags=["abc"], opt_name="routers", opt_data="1.1.1.1")

    resp = _option_get(command="remote-option4-global-get", server_tags=["xyz"], opt_code=3)
    _check_option_result(resp, server_tags=["xyz"], opt_name="routers", opt_data="2.2.2.2")

    resp = _option_get(command="remote-option4-global-get", server_tags=["all"], opt_code=3)
    _check_option_result(resp, server_tags=["all"], opt_name="routers", opt_data="3.3.3.3")

    resp = _option_del(server_tags=["xyz"], opt_code=3)
    assert resp["arguments"]["count"] == 1
    assert resp["text"] == "1 DHCPv4 option(s) deleted."
    assert resp["result"] == 0

    resp = _option_get(command="remote-option4-global-get", server_tags=["xyz"], opt_code=3)
    # it was removed but tag "all" should return option
    _check_option_result(resp, server_tags=["all"], opt_name="routers", opt_data="3.3.3.3")

    resp = _option_get(command="remote-option4-global-get", server_tags=["abc"], opt_code=3)
    _check_option_result(resp, server_tags=["abc"], opt_name="routers", opt_data="1.1.1.1")

    resp = _option_get(command="remote-option4-global-get", server_tags=["all"], opt_code=3)
    _check_option_result(resp, server_tags=["all"], opt_name="routers", opt_data="3.3.3.3")

    resp = _option_del(server_tags=["abc"], opt_code=3)
    assert resp["arguments"]["count"] == 1
    assert resp["text"] == "1 DHCPv4 option(s) deleted."
    assert resp["result"] == 0

    # this also should be tag all
    resp = _option_get(command="remote-option4-global-get", server_tags=["abc"], opt_code=3)
    _check_option_result(resp, server_tags=["all"], opt_name="routers", opt_data="3.3.3.3")

    # this should be from tag "all"
    resp = _option_get(command="remote-option4-global-get", server_tags=["xyz"], opt_code=3)
    _check_option_result(resp, server_tags=["all"], opt_name="routers", opt_data="3.3.3.3")

    resp = _option_get(command="remote-option4-global-get", server_tags=["all"], opt_code=3)
    _check_option_result(resp, server_tags=["all"], opt_name="routers", opt_data="3.3.3.3")

    resp = _option_get(command="remote-option4-global-del", server_tags=["all"], opt_code=3)
    assert resp["arguments"]["count"] == 1
    assert resp["text"] == "1 DHCPv4 option(s) deleted."
    assert resp["result"] == 0

    # now all commands should return error
    _option_get(command="remote-option4-global-get", server_tags=["xyz"], opt_code=3, exp_result=3)

    _option_get(command="remote-option4-global-get", server_tags=["abc"], opt_code=3, exp_result=3)

    resp = _option_get(command="remote-option4-global-get", server_tags=["all"], opt_code=3, exp_result=3)
    assert resp["arguments"]["count"] == 0
    assert resp["result"] == 3


def _optdef_set(server_tags, exp_result=0, opt_code=222, opt_name="foo", opt_type="uint32"):
    cmd = dict(command="remote-option-def4-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": server_tags,
                                                            "option-defs": [{
                                                                "name": opt_name,
                                                                "code": opt_code,
                                                                "type": opt_type}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)

    assert response == {"arguments": {"option-defs": [{"code": opt_code, "space": "dhcp4"}]},
                        "result": 0, "text": "DHCPv4 option definition successfully set."}


def _optdef_get(command, server_tags, exp_result=0, option_def_parameter=None):
    cmd = dict(command=command, arguments={"remote": {"type": "mysql"},
                                           "server-tags": server_tags})
    if option_def_parameter:
        cmd["arguments"]["option-defs"] = [option_def_parameter]

    return srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result)


def _optdef_del(server_tags, exp_result=0, option_def_parameter=None):
    return _optdef_get("remote-option-def4-del", server_tags, exp_result=exp_result,
                       option_def_parameter=option_def_parameter)


def _check_optdef_result(resp, server_tags, count=1, opt_type="uint32", opt_name="foo", opt_code=222):
    assert resp["result"] == 0
    assert resp["arguments"]["count"] == count
    assert resp["arguments"]["option-defs"][0]["metadata"] == {"server-tags": server_tags}
    assert resp["arguments"]["option-defs"][0]["name"] == opt_name
    assert resp["arguments"]["option-defs"][0]["code"] == opt_code
    assert resp["arguments"]["option-defs"][0]["type"] == opt_type


def test_remote_option_def_get_server_tags_tmp():
    # simple test for one ticket https://gitlab.isc.org/isc-projects/kea/issues/737
    _add_server_tag("abc")
    _optdef_set(server_tags=["all"])
    resp = _optdef_get(command="remote-option-def4-get-all", server_tags=["abc"])
    _check_optdef_result(resp, server_tags=["all"], count=1)


def test_remote_option_def_get_server_tags():
    _add_server_tag("abc")
    _add_server_tag("xyz")
    # let's make two definitions with the same name but different type and server tag, plus one different with
    # server tag "all"
    _optdef_set(server_tags=["abc"])
    _optdef_set(server_tags=["xyz"], opt_type="string")
    _optdef_set(server_tags=["all"], opt_code=233, opt_name="bar")

    resp = _optdef_get(command="remote-option-def4-get", server_tags=["abc"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["abc"])

    resp = _optdef_get(command="remote-option-def4-get", server_tags=["xyz"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["xyz"], opt_type="string")

    # this one should fail
    resp = _optdef_get(command="remote-option-def4-get", server_tags=["all"],
                       option_def_parameter={"code": 222}, exp_result=3)
    assert resp["arguments"]["count"] == 0
    assert resp["result"] == 3

    resp = _optdef_get(command="remote-option-def4-get", server_tags=["all"],
                       option_def_parameter={"code": 233})
    _check_optdef_result(resp, server_tags=["all"], opt_code=233, opt_name="bar")

    # let's check if -all will return list of two options for each tag and one option for "all"
    resp = _optdef_get(command="remote-option-def4-get-all", server_tags=["abc"])
    _check_optdef_result(resp, server_tags=["abc"], count=2)

    assert resp["arguments"]["option-defs"][1]["metadata"] == {"server-tags": ["all"]}
    assert resp["arguments"]["option-defs"][1]["name"] == "bar"
    assert resp["arguments"]["option-defs"][1]["code"] == 233

    resp = _optdef_get(command="remote-option-def4-get-all", server_tags=["xyz"])
    _check_optdef_result(resp, server_tags=["xyz"], count=2, opt_type="string")
    assert resp["arguments"]["option-defs"][1]["metadata"] == {"server-tags": ["all"]}
    assert resp["arguments"]["option-defs"][1]["name"] == "bar"
    assert resp["arguments"]["option-defs"][1]["code"] == 233

    resp = _optdef_get(command="remote-option-def4-get-all", server_tags=["all"])
    _check_optdef_result(resp, server_tags=["all"], opt_code=233, opt_name="bar")


def test_remote_option_def_del_server_tags():
    _add_server_tag("abc")
    _add_server_tag("xyz")
    # we should be able to configure the same option for each tag, different type is for distinguish returns
    # options from "all" should be overwritten by specific tags on kea configuration level, not in db!
    _optdef_set(server_tags=["abc"])
    _optdef_set(server_tags=["xyz"], opt_type="string")
    _optdef_set(server_tags=["all"], opt_type="uint8")

    resp = _optdef_get(command="remote-option-def4-get", server_tags=["abc"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["abc"], count=1)

    resp = _optdef_get(command="remote-option-def4-get", server_tags=["xyz"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["xyz"], opt_type="string", count=1)

    resp = _optdef_get(command="remote-option-def4-get", server_tags=["all"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["all"], opt_type="uint8")

    # let's remove one option and see if all other stays
    _optdef_del(["all"], option_def_parameter={"code": 222})

    resp = _optdef_get(command="remote-option-def4-get", server_tags=["abc"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["abc"])

    resp = _optdef_get(command="remote-option-def4-get", server_tags=["xyz"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["xyz"], opt_type="string")

    resp = _optdef_get(command="remote-option-def4-get", server_tags=["all"],
                       option_def_parameter={"code": 222}, exp_result=3)
    assert resp["arguments"]["count"] == 0
    assert resp["result"] == 3

    # same with -all command, we expect just one
    resp = _optdef_get(command="remote-option-def4-get-all", server_tags=["xyz"])
    _check_optdef_result(resp, server_tags=["xyz"], opt_type="string")

    resp = _optdef_get(command="remote-option-def4-get-all", server_tags=["xyz"])
    _check_optdef_result(resp, server_tags=["xyz"], opt_type="string")

    _optdef_del(["abc"], option_def_parameter={"code": 222})

    resp = _optdef_get(command="remote-option-def4-get", server_tags=["abc"],
                       option_def_parameter={"code": 222}, exp_result=3)
    assert resp["arguments"]["count"] == 0
    assert resp["result"] == 3

    resp = _optdef_get(command="remote-option-def4-get", server_tags=["xyz"],
                       option_def_parameter={"code": 222})
    _check_optdef_result(resp, server_tags=["xyz"], opt_type="string")