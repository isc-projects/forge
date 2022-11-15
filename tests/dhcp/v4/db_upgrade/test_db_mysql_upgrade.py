# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Test mysql db upgrade"""

# pylint: disable=invalid-name
# pylint: disable=line-too-long

import glob
import pytest
from src import srv_msg
from src import misc
from src import srv_control

from src.forge_cfg import world

# 1.6.3 version is our starting point here. In 1.6.0 CB backend was introduced in mysql
# but there were no changes in schema between 1.6.0 and 1.6.3. In the tests are included
# scripts to build database and populate it with data. Then test will try to upgrade it
# to newest database schema. Similar test will be for postgres but without CB in it.


def _send_cmd(cmd, arg):
    if "remote" not in arg:
        arg.update({"remote": {"type": "mysql"}})
    if "get" not in cmd:
        if "server-tags" not in arg:
            arg.update({"server-tags": ["abc"]})

    cmd = dict(command=cmd, arguments=arg)
    return srv_msg.send_ctrl_cmd(cmd, exp_result=0)


def _create_mysql_dump():
    # start Kea with specific version, run this and you will get DB dump with data in all
    # tables, it's designed for kea 1.6.3; if you are using later, using more commands
    # is probably required
    srv_msg.remove_file_from_server('$(SOFTWARE_INSTALL_PATH)/my_db_v4.sql')
    world.f_cfg.multi_threading_enabled = False
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_hooks('libdhcp_cb_cmds.so')
    srv_control.add_hooks('libdhcp_mysql_cb.so')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(MGMT_ADDRESS)')
    srv_control.enable_db_backend_reservation('MySQL')
    srv_control.define_temporary_lease_db_backend('mysql')
    cb_config = {"config-databases": [{"user": "$(DB_USER)",
                                       "password": "$(DB_PASSWD)",
                                       "name": "$(DB_NAME)",
                                       "type": "mysql"}]}

    world.dhcp_cfg["config-control"] = cb_config
    world.dhcp_cfg["server-tag"] = "abc"
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.send_ctrl_cmd({"command": "remote-server4-set",
                           "arguments": {"remote": {"type": "mysql"}, "servers": [{"server-tag": "abc"}]}}, exp_result=0)

    subnets = [{"4o6-interface": "eth9",
                "4o6-interface-id": "interf-id",
                "4o6-subnet": "2000::/64",
                "authoritative": False,
                "boot-file-name": "file-name",
                "shared-network-name": "",
                "id": 2, "interface": "$(SERVER_IFACE)",
                "match-client-id": False, "next-server": "0.0.0.0",
                "pools": [{"pool": "192.168.50.10-192.168.50.10",
                           "option-data": [{"code": 6,
                                            "data": '192.0.2.2',
                                            "always-send": True,
                                            "csv-format": True}]}],
                "relay": {"ip-addresses": ["192.168.5.5"]},
                "reservation-mode": "all",
                "server-hostname": "name-xyz",
                "subnet": "192.168.50.0/24",
                "valid-lifetime": 1000,
                "rebind-timer": 500,
                "renew-timer": 200,
                "option-data": [{"code": 6,
                                 "data": '192.0.2.1',
                                 "always-send": True,
                                 "csv-format": True}]}]

    _send_cmd("remote-subnet4-set", dict(subnets=subnets))

    shared_networks = [{"name": "net1",
                        "client-class": "abc",
                        "authoritative": False,
                        "rebind-timer": 200,
                        "renew-timer": 100,
                        "calculate-tee-times": True,
                        "require-client-classes": ["XYZ"],
                        "t1-percent": 0.5,
                        "t2-percent": 0.8,
                        "valid-lifetime": 300,
                        "reservation-mode": "global",
                        "match-client-id": True,
                        "user-context": {"some weird network": 55},
                        "interface": "$(SERVER_IFACE)",
                        "option-data": [{"code": 6,
                                         "data": '192.0.2.1',
                                         "always-send": True,
                                         "csv-format": True}]}]

    _send_cmd("remote-network4-set", {"shared-networks": shared_networks})

    parameters = {"boot-file-name": "/dev/null"}
    _send_cmd("remote-global-parameter4-set", dict(parameters=parameters))

    options = [{"name": "host-name", "data": "isc.example.com"}]
    _send_cmd("remote-option4-global-set", dict(options=options))

    option_def = [{"name": "foo", "code": 222, "type": "uint32"}]
    _send_cmd("remote-option-def4-set", {"option-defs": option_def})

    cmd = {"command": "config-reload", "arguments": {}}
    srv_msg.send_ctrl_cmd(cmd)

    hr = {"reservation": {"subnet-id": 2, "hw-address": "01:0a:0b:0c:0d:0e:0f",
                          "ip-address": "192.168.50.205", "next-server": "192.0.2.1",
                          "server-hostname": "hal9000", "boot-file-name": "/dev/null",
                          "option-data": [{"name": "domain-name-servers",
                                           "data": "10.1.1.202,10.1.1.203"}],
                          "client-classes": ["special_snowflake", "office"]}}
    _send_cmd("reservation-add", hr)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')

    # create dump of database with events and procedures
    srv_msg.execute_shell_cmd("mysqldump --events --routines -u $(DB_USER) -p'$(DB_PASSWD)' $(DB_NAME) > $(SOFTWARE_INSTALL_PATH)/my_db_v4.sql")
    # replace interface and user used on setup that was used to generate dump to value later changed to interface
    # it's needed otherwise kea would not start on differently configured setup
    srv_msg.execute_shell_cmd("sed -i 's/$(SERVER_IFACE)/!serverinterface!/g' $(SOFTWARE_INSTALL_PATH)/my_db_v4.sql")
    srv_msg.execute_shell_cmd("sed -i 's/$(DB_USER)/!db_user!/g' $(SOFTWARE_INSTALL_PATH)/my_db_v4.sql")

# Uncomment this test to build your own database dump
# @pytest.mark.v4
# def test_create_dump():
#     _create_mysql_dump()


@pytest.mark.v4
def test_v4_upgrade_mysql_db():
    # new db parameters
    tmp_db_name = "kea_tmp_db"
    tmp_user_name = "kea_tmp_user"
    # make sure that new db does not exists
    srv_msg.execute_shell_cmd(f"mysql -u root -N -B -e \"DROP DATABASE IF EXISTS {tmp_db_name};\"")
    # create new db without schema
    srv_control.build_database(db_name=tmp_db_name, db_user=tmp_user_name, init_db=False)
    # send db dump file
    srv_msg.remove_file_from_server('/tmp/my_db_v4.sql')
    srv_msg.send_file_to_server(glob.glob("**/my_db_v4.sql", recursive=True)[0], '/tmp/my_db_v4.sql')
    # switch interface and username to the one setup is using
    srv_msg.execute_shell_cmd("sed -i 's/!serverinterface!/$(SERVER_IFACE)/g' /tmp/my_db_v4.sql")
    srv_msg.execute_shell_cmd(f"sed -i 's/!db_user!/{tmp_user_name}/g' /tmp/my_db_v4.sql")
    if world.server_system == 'redhat':
        srv_msg.execute_shell_cmd("sed -i 's/CHARSET=utf8mb4/CHARSET=latin1/g' /tmp/my_db_v4.sql")

    # this solves the problem: "Variable 'sql_mode' can't be set to the value of 'NO_AUTO_CREATE_USER'"
    srv_msg.execute_shell_cmd("sed -i 's/NO_AUTO_CREATE_USER,//g' /tmp/my_db_v4.sql")
    # create database without content with new name and user
    srv_control.build_database(db_name=tmp_db_name, db_user=tmp_user_name, init_db=False)
    # recreate db content in new db
    srv_msg.execute_shell_cmd(f"mysql -u{tmp_user_name} -p$(DB_PASSWD) {tmp_db_name} < /tmp/my_db_v4.sql")
    # start kea, which should fail due to mismatch in db version
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_hooks('libdhcp_cb_cmds.so')
    srv_control.add_hooks('libdhcp_mysql_cb.so')
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(MGMT_ADDRESS)')
    hosts = {"hosts-databases": [{"user": tmp_user_name,
                                  "password": "$(DB_PASSWD)",
                                  "name": tmp_db_name,
                                  "type": "mysql"}]}

    leases = {"lease-database": {"user": tmp_user_name,
                                 "password": "$(DB_PASSWD)",
                                 "name": tmp_db_name,
                                 "type": "mysql"}}

    cb_config = {"config-databases": [{"user": tmp_user_name,
                                       "password": "$(DB_PASSWD)",
                                       "name": tmp_db_name,
                                       "type": "mysql"}]}

    world.dhcp_cfg.update(hosts)
    world.dhcp_cfg.update(leases)
    world.dhcp_cfg["config-control"] = cb_config
    world.dhcp_cfg["server-tag"] = "abc"
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started', should_succeed=False)
    # upgrade with kea admin
    kea_admin = world.f_cfg.sbin_join('kea-admin')
    srv_msg.execute_shell_cmd(f"sudo {kea_admin} db-upgrade mysql -u {tmp_user_name} -p $(DB_PASSWD) -n {tmp_db_name}")
    # start kea
    srv_control.start_srv('DHCP', 'started')

    # check reservation
    hr_get = {"subnet-id": 2, "identifier-type": "hw-address", "identifier": "01:0a:0b:0c:0d:0e:0f"}
    cmd = dict(command="reservation-get", arguments=hr_get)
    response = srv_msg.send_ctrl_cmd(cmd)["arguments"]
    assert response["boot-file-name"] == "/dev/null"
    assert response["client-classes"] == ["special_snowflake", "office"]
    assert response["hw-address"] == "01:0a:0b:0c:0d:0e:0f"
    assert response["ip-address"] == "192.168.50.205"
    assert response["option-data"] == [{"always-send": False,
                                        "code": 6,
                                        "csv-format": True,
                                        "data": "10.1.1.202,10.1.1.203",
                                        "name": "domain-name-servers",
                                        "space": "dhcp4"}]
    assert response["server-hostname"] == "hal9000"

    # check lease
    lease_get = {"hw-address": "ff:01:02:03:ff:04"}
    cmd = dict(command="lease4-get-by-hw-address", arguments=lease_get)
    resp = srv_msg.send_ctrl_cmd(cmd)["arguments"]
    assert resp["leases"][0]["hw-address"] == "ff:01:02:03:ff:04"
    assert resp["leases"][0]["ip-address"] == "192.168.50.10"
    assert resp["leases"][0]["state"] == 0
    assert resp["leases"][0]["subnet-id"] == 2
    assert resp["leases"][0]["valid-lft"] == 1000

    # check config
    cmd = dict(command="config-get", arguments={})
    cfg = srv_msg.send_ctrl_cmd(cmd, exp_result=0)["arguments"]

    assert len(cfg["Dhcp4"]["subnet4"]) == 1
    assert len(cfg["Dhcp4"]["option-def"]) == 1
    assert len(cfg["Dhcp4"]["option-data"]) == 1
    assert len(cfg["Dhcp4"]["shared-networks"]) == 1

    # let's check subnet and network parameters one by one, it's possible that new
    # parameters will be added in future and it will trash this test, we are sure that
    # no new parameters will be added in 1.6.3 schema.
    resp = _send_cmd("remote-subnet4-get-by-id", {"subnets": [{"id": 2}]})["arguments"]
    assert resp["count"] == 1
    subnet = resp["subnets"][0]
    assert subnet["4o6-interface"] == "eth9"
    assert subnet["4o6-interface-id"] == "interf-id"
    assert subnet["4o6-subnet"] == "2000::/64"
    assert subnet["boot-file-name"] == "file-name"
    assert subnet["id"] == 2
    assert subnet["metadata"] == {"server-tags": ["abc"]}
    assert subnet["option-data"] == [{"always-send": True, "code": 6,
                                      "csv-format": True, "data": "192.0.2.1",
                                      "name": "domain-name-servers", "space": "dhcp4"}]
    assert subnet["pools"][0]["pool"] == "192.168.50.10/32"
    assert subnet["rebind-timer"] == 500
    assert subnet["relay"] == {"ip-addresses": ["192.168.5.5"]}
    assert subnet["subnet"] == "192.168.50.0/24"
    assert subnet["valid-lifetime"] == 1000

    resp = _send_cmd("remote-network4-get", {"shared-networks": [{"name": "net1"}]})["arguments"]
    assert resp["count"] == 1
    network = resp["shared-networks"][0]
    assert network["client-class"] == "abc"
    assert network["metadata"] == {"server-tags": ["abc"]}
    assert network["name"] == "net1"
    assert network["option-data"] == [{"always-send": True,
                                       "code": 6,
                                       "csv-format": True,
                                       "data": "192.0.2.1",
                                       "name": "domain-name-servers",
                                       "space": "dhcp4"}]
    assert network["rebind-timer"] == 200
    assert network["renew-timer"] == 100
    assert network["require-client-classes"] == ["XYZ"]
    assert network["user-context"] == {"some weird network": 55}
    assert network["valid-lifetime"] == 300

    resp = _send_cmd("remote-global-parameter4-get", {"server-tags": ["abc"], "parameters": ["boot-file-name"]})["arguments"]
    assert resp["count"] == 1
    assert resp["parameters"] == {"boot-file-name": "/dev/null", "metadata": {"server-tags": ["abc"]}}

    resp = _send_cmd("remote-option4-global-get", {"server-tags": ["abc"], "options": [{"code": 12}]})["arguments"]
    assert resp["count"] == 1
    assert resp["options"][0] == {"always-send": False,
                                  "code": 12,
                                  "csv-format": True,
                                  "data": "isc.example.com",
                                  "metadata": {"server-tags": ["abc"]},
                                  "name": "host-name",
                                  "space": "dhcp4"}

    resp = _send_cmd("remote-option-def4-get", {"server-tags": ["abc"], "option-defs": [{"code": 222}]})["arguments"]
    assert resp["count"] == 1
    assert resp["option-defs"][0] == {"array": False,
                                      "code": 222,
                                      "encapsulate": "",
                                      "metadata": {"server-tags": ["abc"]},
                                      "name": "foo",
                                      "record-types": "",
                                      "space": "dhcp4",
                                      "type": "uint32"}
