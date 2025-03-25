# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Test pgsql db upgrade"""

# pylint: disable=invalid-name

import glob
import pytest

from src import misc
from src import srv_control
from src import srv_msg

from src.forge_cfg import world
from src.softwaresupport.multi_server_functions import fabric_run_command

# 1.6.3 version is our starting point here. In postgresql there is no CB so far so updates to
# database tested here are limited


def _send_cmd(cmd, arg):
    cmd = dict(command=cmd, arguments=arg)
    return srv_msg.send_ctrl_cmd(cmd, exp_result=0)


def _create_pgsql_dump():
    # dump for postrgesql is bit different because we do not have config backend for postgres
    # but we will still use kea 1.6.3 to generate this. In future we will have to create new dump with
    # config backend data
    srv_msg.remove_file_from_server('$(SOFTWARE_INSTALL_PATH)/pg_db_v6.sql')
    world.f_cfg.auto_multi_threading_configuration = False
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::10-2001:db8:1::10')
    srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 96)
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_hooks('libdhcp_cb_cmds.so')
    srv_control.add_hooks('libdhcp_pgsql.so')
    srv_control.add_http_control_channel()
    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.define_lease_db_backend('postgresql')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    hr = {"reservation": {"subnet-id": 1,
                          "duid": "01:02:03:04:05:06:07:08:09:0A",
                          "ip-addresses": ["2001:db8:1::100"],
                          "prefixes": ["2001:db8:2:abcd::/64"],
                          "hostname": "foo.example.com",
                          "option-data": [{"name": "vendor-opts", "data": "4491"}]}}
    _send_cmd("reservation-add", hr)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value('Client', 'ia_id', 55701)
    srv_msg.client_sets_value('Client', 'ia_pd', 76159)
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

    # wanted to do this with fabric_sudo_command(cmd, sudo_user='postgres' but it failed
    cmd = f'sudo -S -u postgres pg_dump {world.f_cfg.db_name} > {world.f_cfg.software_install_path}/pg_db_v6.sql'
    fabric_run_command(cmd, ignore_errors=False, destination_host=world.f_cfg.mgmt_address)
    srv_msg.execute_shell_cmd(f"sed -i 's/$(DB_USER)/!db_user!/g' {world.f_cfg.software_install_path}/pg_db_v6.sql")


# @pytest.mark.v6
# def test_create_pgsql_dump():
#     _create_pgsql_dump()


@pytest.mark.v6
def test_v6_upgrade_pgsql_db():
    # new db parameters
    world.f_cfg.auto_multi_threading_configuration = False
    tmp_db_name = "kea_tmp_db"
    tmp_user_name = "kea_tmp_user"
    # create new db without schema
    srv_control.build_database(db_name=tmp_db_name, db_user=tmp_user_name, init_db=False)
    # send db dump file
    srv_msg.remove_file_from_server('/tmp/pg_db_v6.sql')
    srv_msg.send_file_to_server(glob.glob("**/pg_db_v6.sql", recursive=True)[0], '/tmp/pg_db_v6.sql')
    # switch username to the one setup is using
    srv_msg.execute_shell_cmd(f"sed -i 's/!db_user!/{tmp_user_name}/g' /tmp/pg_db_v6.sql")
    # recreate db content in new db

    cmd = f"sudo -S -u postgres psql -d {tmp_db_name} -f/tmp/pg_db_v6.sql"
    fabric_run_command(cmd, ignore_errors=False, destination_host=world.f_cfg.mgmt_address)

    # start kea, which should fail due to mismatch in db version
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::10-2001:db8:1::10')
    srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 96)
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel('$(MGMT_ADDRESS)')
    hosts = {"hosts-databases": [{"user": tmp_user_name,
                                  "password": "$(DB_PASSWD)",
                                  "name": tmp_db_name,
                                  "type": "postgresql"}]}

    leases = {"lease-database": {"user": tmp_user_name,
                                 "password": "$(DB_PASSWD)",
                                 "name": tmp_db_name,
                                 "type": "postgresql"}}
    world.dhcp_cfg.update(hosts)
    world.dhcp_cfg.update(leases)
    srv_control.add_database_hook('pgsql')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started', should_succeed=False)

    kea_admin = world.f_cfg.sbin_join('kea-admin')
    srv_msg.execute_shell_cmd(f'sudo {kea_admin} db-upgrade pgsql -u {tmp_user_name} -p $(DB_PASSWD) -n {tmp_db_name}')

    # start kea
    srv_control.start_srv('DHCP', 'started')

    # check reservation
    hr_get = {"subnet-id": 1, "identifier-type": "duid", "identifier": "01:02:03:04:05:06:07:08:09:0A"}
    resp = _send_cmd("reservation-get", hr_get)["arguments"]
    assert resp["duid"] == "01:02:03:04:05:06:07:08:09:0a"
    assert resp["hostname"] == "foo.example.com"
    assert resp["ip-addresses"] == ["2001:db8:1::100"]
    assert resp["option-data"] == [{"always-send": False,
                                    "code": 17,
                                    "csv-format": True,
                                    "data": "4491",
                                    "name": "vendor-opts",
                                    "never-send": False,
                                    "space": "dhcp6"}]
    assert resp["prefixes"] == ["2001:db8:2:abcd::/64"]

    # check lease
    lease_get = {"duid": "00:03:00:01:f6:f5:f4:f3:f2:01"}
    resp = _send_cmd("lease6-get-by-duid", lease_get)["arguments"]
    assert len(resp["leases"]) == 2
    for lease in resp["leases"]:
        if lease["type"] == "IA_NA":
            assert lease["duid"] == "00:03:00:01:f6:f5:f4:f3:f2:01"
            assert lease["hw-address"] == "f6:f5:f4:f3:f2:01"
            assert lease["iaid"] == 55701
            assert lease["ip-address"] == "2001:db8:1::10"
            assert lease["preferred-lft"] == 3000
            assert lease["state"] == 0
            assert lease["subnet-id"] == 1
            assert lease["valid-lft"] == 4000
        if lease["type"] == "IA_PD":
            assert lease["duid"] == "00:03:00:01:f6:f5:f4:f3:f2:01"
            assert lease["hw-address"] == "f6:f5:f4:f3:f2:01"
            assert lease["iaid"] == 76159
            assert lease["ip-address"] == "2001:db8:2::"
            assert lease["preferred-lft"] == 3000
            assert lease["prefix-len"] == 96
            assert lease["state"] == 0
            assert lease["subnet-id"] == 1
            assert lease["valid-lft"] == 4000
