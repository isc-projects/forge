# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Test mysql db upgrade"""

# pylint: disable=invalid-name,line-too-long

import glob
import pytest

from src import misc
from src import srv_control
from src import srv_msg

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
    srv_msg.remove_file_from_server('$(SOFTWARE_INSTALL_PATH)/my_db_v6.sql')
    world.f_cfg.multi_threading_enabled = False
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_hooks('libdhcp_cb_cmds.so')
    srv_control.add_hooks('libdhcp_mysql_cb.so')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(MGMT_ADDRESS)')
    world.reservation_backend = "mysql"
    srv_control.define_temporary_lease_db_backend('mysql')
    cb_config = {"config-databases": [{"user": "$(DB_USER)",
                                       "password": "$(DB_PASSWD)",
                                       "name": "$(DB_NAME)",
                                       "type": "mysql"}]}

    world.dhcp_cfg["config-control"] = cb_config
    world.dhcp_cfg["server-tag"] = "abc"
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = {"command": "remote-server6-set",
           "arguments": {"remote": {"type": "mysql"},
                         "servers": [{"server-tag": "abc"}]}}
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    subnets = [{"shared-network-name": "", "id": 2, "interface": "$(SERVER_IFACE)",
                "pools": [{"pool": "2001:db8:1::10-2001:db8:1::10",
                           "option-data": [{"code": 7, "data": "12",
                                            "always-send": True, "csv-format": True}]}],
                "pd-pools": [{"delegated-len": 91,
                              "prefix": "2001:db8:2::",
                              "prefix-len": 90}],
                "reservation-mode": "all",
                "subnet": "2001:db8:1::/64",
                "valid-lifetime": 1000,
                "rebind-timer": 500,
                "renew-timer": 200,
                "option-data": [{"code": 7, "data": "123",
                                 "always-send": True,
                                 "csv-format": True}]}]
    _send_cmd("remote-subnet6-set", dict(subnets=subnets))

    shared_networks = [{"name": "net1",
                        "client-class": "abc",
                        "require-client-classes": ["XYZ"],
                        "rebind-timer": 200,
                        "renew-timer": 100,
                        "calculate-tee-times": True,
                        "t1-percent": 0.5,
                        "t2-percent": 0.8,
                        "rapid-commit": True,
                        "valid-lifetime": 300,
                        "reservation-mode": "global",
                        "user-context": {"some weird network": 55},
                        "interface": "$(SERVER_IFACE)",
                        "option-data": [{"code": 7,
                                         "data": "123",
                                         "always-send": True,
                                         "csv-format": True}]}]

    _send_cmd("remote-network6-set", {"shared-networks": shared_networks})

    parameters = {"decline-probation-period": 123456}
    _send_cmd("remote-global-parameter6-set", dict(parameters=parameters))

    options = [{"name": "sip-server-dns", "data": "isc.example.com"}]
    _send_cmd("remote-option6-global-set", dict(options=options))

    option_def = [{"name": "foo", "code": 222, "type": "uint32"}]
    _send_cmd("remote-option-def6-set", {"option-defs": option_def})

    cmd = {"command": "config-reload", "arguments": {}}
    srv_msg.send_ctrl_cmd(cmd)

    hr = {"reservation": {"subnet-id": 2,
                          "duid": "01:02:03:04:05:06:07:08:09:0A",
                          "ip-addresses": ["2001:db8:1::1"],
                          "prefixes": ["2001:db8:2:abcd::/64"],
                          "hostname": "foo.example.com",
                          "option-data": [{"name": "vendor-opts", "data": "4491"}]}}
    _send_cmd("reservation-add", hr)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value('Client', 'ia_id', 61439)
    srv_msg.client_sets_value('Client', 'ia_pd', 24511)
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::10')

    # create dump of database with events and procedures
    srv_msg.execute_shell_cmd("mysqldump --events --routines -u $(DB_USER) -p'$(DB_PASSWD)' $(DB_NAME) > $(SOFTWARE_INSTALL_PATH)/my_db_v6.sql")
    # replace interface and user used on setup that was used to generate dump to value later changed to interface
    # it's needed otherwise kea would not start on differently configured setup
    srv_msg.execute_shell_cmd("sed -i 's/$(SERVER_IFACE)/!serverinterface!/g' $(SOFTWARE_INSTALL_PATH)/my_db_v6.sql")
    srv_msg.execute_shell_cmd("sed -i 's/$(DB_USER)/!db_user!/g' $(SOFTWARE_INSTALL_PATH)/my_db_v6.sql")


# Uncomment this test to build your own database dump
# @pytest.mark.v6
# def test_create_mysql_dump():
#     _create_mysql_dump()

@pytest.mark.v6
def test_v6_upgrade_mysql_db():
    # new db parameters
    tmp_db_name = "kea_tmp_db"
    tmp_user_name = "kea_tmp_user"
    # make sure that new db does not exists
    # srv_msg.execute_shell_cmd("mysql -u root -N -B -e \"DROP DATABASE IF EXISTS %s;\"" % tmp_db_name)
    # create new db without schema
    srv_control.build_database(db_name=tmp_db_name, db_user=tmp_user_name, init_db=False)
    # send db dump file
    srv_msg.remove_file_from_server('/tmp/my_db_v6.sql')
    srv_msg.send_file_to_server(glob.glob("**/my_db_v6.sql", recursive=True)[0], '/tmp/my_db_v6.sql')
    # switch interface and username to the one setup is using
    srv_msg.execute_shell_cmd("sed -i 's/!serverinterface!/$(SERVER_IFACE)/g' /tmp/my_db_v6.sql")
    srv_msg.execute_shell_cmd("sed -i 's/!db_user!/%s/g' /tmp/my_db_v6.sql" % tmp_user_name)
    if world.server_system == 'redhat':
        srv_msg.execute_shell_cmd("sed -i 's/CHARSET=utf8mb4/CHARSET=latin1/g' /tmp/my_db_v6.sql")
    # this solves the problem: "Variable 'sql_mode' can't be set to the value of 'NO_AUTO_CREATE_USER'"
    srv_msg.execute_shell_cmd("sed -i 's/NO_AUTO_CREATE_USER,//g' /tmp/my_db_v6.sql")
    # recreate db content in new db
    srv_msg.execute_shell_cmd("mysql -u%s -p$(DB_PASSWD) %s < /tmp/my_db_v6.sql" % (tmp_user_name, tmp_db_name))
    # start kea, which should fail due to mismatch in db version
    misc.test_setup()
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_hooks('libdhcp_cb_cmds.so')
    srv_control.add_hooks('libdhcp_mysql_cb.so')
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
    srv_msg.execute_shell_cmd("sudo %s db-upgrade mysql -u %s -p $(DB_PASSWD) -n %s" % (kea_admin, tmp_user_name, tmp_db_name))

    # start kea
    srv_control.start_srv('DHCP', 'started')

    # check reservation
    hr_get = {"subnet-id": 2, "identifier-type": "duid", "identifier": "01:02:03:04:05:06:07:08:09:0A"}
    resp = _send_cmd("reservation-get", hr_get)["arguments"]
    assert resp["duid"] == "01:02:03:04:05:06:07:08:09:0a"
    assert resp["hostname"] == "foo.example.com"
    assert resp["ip-addresses"] == ["2001:db8:1::1"]
    assert resp["option-data"] == [{"always-send": False,
                                    "code": 17,
                                    "csv-format": True,
                                    "data": "4491",
                                    "name": "vendor-opts", "space": "dhcp6"}]
    assert resp["prefixes"] == ["2001:db8:2:abcd::/64"]

    # check lease
    lease_get = {"duid": "00:03:00:01:f6:f5:f4:f3:f2:01"}
    resp = _send_cmd("lease6-get-by-duid", lease_get)["arguments"]
    assert len(resp["leases"]) == 2
    for lease in resp["leases"]:
        if lease["type"] == "IA_NA":
            assert lease["duid"] == "00:03:00:01:f6:f5:f4:f3:f2:01"
            assert lease["hw-address"] == "f6:f5:f4:f3:f2:01"
            assert lease["iaid"] == 61439
            assert lease["ip-address"] == "2001:db8:1::10"
            assert lease["preferred-lft"] == 3000
            assert lease["state"] == 0
            assert lease["subnet-id"] == 2
            assert lease["valid-lft"] == 1000
        if lease["type"] == "IA_PD":
            assert lease["duid"] == "00:03:00:01:f6:f5:f4:f3:f2:01"
            assert lease["hw-address"] == "f6:f5:f4:f3:f2:01"
            assert lease["iaid"] == 24511
            assert lease["ip-address"] == "2001:db8:2::"
            assert lease["preferred-lft"] == 3000
            assert lease["prefix-len"] == 91
            assert lease["state"] == 0
            assert lease["subnet-id"] == 2
            assert lease["valid-lft"] == 1000

    # check config
    cmd = dict(command="config-get", arguments={})
    cfg = srv_msg.send_ctrl_cmd(cmd, exp_result=0)["arguments"]

    assert len(cfg["Dhcp6"]["subnet6"]) == 1
    assert len(cfg["Dhcp6"]["option-def"]) == 1
    assert len(cfg["Dhcp6"]["option-data"]) == 1
    assert len(cfg["Dhcp6"]["shared-networks"]) == 1

    # let's check subnet and network parameters one by one, it's possible that new
    # parameters will be added in future and it will trash this test, we are sure that
    # no new parameters will be added in 1.6.3 schema.
    resp = _send_cmd("remote-subnet6-get-by-id", {"subnets": [{"id": 2}]})["arguments"]
    assert resp["count"] == 1
    subnet = resp["subnets"][0]
    assert subnet["id"] == 2
    assert subnet["metadata"] == {"server-tags": ["abc"]}
    assert subnet["option-data"] == [{"always-send": True,
                                      "code": 7,
                                      "csv-format": True,
                                      "data": "123",
                                      "name": "preference",
                                      "space": "dhcp6"}]

    assert subnet["pools"][0] == {"option-data": [{"always-send": True,
                                                   "code": 7,
                                                   "csv-format": True,
                                                   "data": "12",
                                                   "name": "preference",
                                                   "space": "dhcp6"}],
                                  "pool": "2001:db8:1::10/128"}
    assert subnet["pd-pools"] == [{"delegated-len": 91,
                                   "option-data": [],
                                   "prefix": "2001:db8:2::",
                                   "prefix-len": 90}]
    assert subnet["rebind-timer"] == 500
    assert subnet["renew-timer"] == 200
    assert subnet["shared-network-name"] is None
    assert subnet["subnet"] == "2001:db8:1::/64"
    assert subnet["valid-lifetime"] == 1000

    resp = _send_cmd("remote-network6-get", {"shared-networks": [{"name": "net1"}]})["arguments"]
    assert resp["count"] == 1
    network = resp["shared-networks"][0]
    assert network["client-class"] == "abc"
    assert network["metadata"] == {"server-tags": ["abc"]}
    assert network["name"] == "net1"
    assert network["option-data"] == [{"always-send": True,
                                       "code": 7,
                                       "csv-format": True,
                                       "data": "123",
                                       "name": "preference",
                                       "space": "dhcp6"}]
    assert network["rebind-timer"] == 200
    assert network["renew-timer"] == 100
    assert network["require-client-classes"] == ["XYZ"]
    assert network["user-context"] == {"some weird network": 55}
    assert network["valid-lifetime"] == 300

    resp = _send_cmd("remote-global-parameter6-get", {"server-tags": ["abc"], "parameters": ["decline-probation-period"]})["arguments"]
    assert resp["count"] == 1
    assert resp["parameters"] == {"decline-probation-period": 123456, "metadata": {"server-tags": ["abc"]}}

    resp = _send_cmd("remote-option6-global-get", {"server-tags": ["abc"], "options": [{"code": 21}]})["arguments"]
    assert resp["count"] == 1
    assert resp["options"][0] == {"always-send": False,
                                  "code": 21,
                                  "csv-format": True,
                                  "data": "isc.example.com",
                                  "metadata": {"server-tags": ["abc"]},
                                  "name": "sip-server-dns",
                                  "space": "dhcp6"}

    resp = _send_cmd("remote-option-def6-get", {"server-tags": ["abc"], "option-defs": [{"code": 222}]})["arguments"]
    assert resp["count"] == 1
    assert resp["option-defs"][0] == {"array": False,
                                      "code": 222,
                                      "encapsulate": "",
                                      "metadata": {"server-tags": ["abc"]},
                                      "name": "foo",
                                      "record-types": "",
                                      "space": "dhcp6",
                                      "type": "uint32"}
