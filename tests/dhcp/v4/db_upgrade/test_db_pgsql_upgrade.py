"""Test pgsql db upgrade"""

# pylint: disable=invalid-name,line-too-long
import glob
import pytest
import srv_msg
import misc
import srv_control

from forge_cfg import world
from softwaresupport.multi_server_functions import fabric_run_command


def _send_cmd(cmd, arg):
    cmd = dict(command=cmd, arguments=arg)
    return srv_msg.send_ctrl_cmd(cmd, exp_result=0)


def _create_pgsql_dump():
    # dump for postrgesql is bit different because we do not have config backend for postgres
    # but we will still use kea 1.6.3 to generate this. In future we will have to create new dump with
    # config backend data
    srv_msg.remove_file_from_server('$(SOFTWARE_INSTALL_PATH)/pg_db_v4.sql')
    world.f_cfg.multi_threading_enabled = False
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_hooks('libdhcp_cb_cmds.so')
    srv_control.add_hooks('libdhcp_mysql_cb.so')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(MGMT_ADDRESS)')
    srv_control.enable_db_backend_reservation('PostgreSQL')
    srv_control.define_temporary_lease_db_backend('postgresql')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    hr = {"reservation": {"subnet-id": 1,
                          "hw-address": "01:0a:0b:0c:0d:0e:0f",
                          "ip-address": "192.168.50.205",
                          "next-server": "192.0.2.1",
                          "server-hostname": "hal9000",
                          "boot-file-name": "/dev/null",
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

    # wanted to do this with fabric_sudo_command(cmd, sudo_user='postgres' but it failed
    cmd = "sudo -S -u postgres pg_dump %s >%s/pg_db_v4.sql" % (world.f_cfg.db_name, world.f_cfg.software_install_path)
    fabric_run_command(cmd, ignore_errors=False, destination_host=world.f_cfg.mgmt_address)
    srv_msg.execute_shell_cmd("sed -i 's/$(DB_USER)/!db_user!/g' %s/pg_db_v4.sql" % world.f_cfg.software_install_path)


# @pytest.mark.v4
# def test_create_pgsql_dump():
#     _create_pgsql_dump()


@pytest.mark.v4
def test_v4_upgrade_pgsql_db():
    # new db parameters
    tmp_db_name = "kea_tmp_db"
    tmp_user_name = "kea_tmp_user"
    # create new db without schema
    srv_control.build_database(db_name=tmp_db_name, db_user=tmp_user_name, init_db=False)
    # send db dump file
    srv_msg.remove_file_from_server('/tmp/pg_db_v4.sql')
    srv_msg.send_file_to_server(glob.glob("**/pg_db_v4.sql", recursive=True)[0], '/tmp/pg_db_v4.sql')
    # switch username to the one setup is using
    srv_msg.execute_shell_cmd("sed -i 's/!db_user!/%s/g' /tmp/pg_db_v4.sql" % tmp_user_name)

    # recreate db content in new db
    cmd = "sudo -S -u postgres psql -d %s -f/tmp/pg_db_v4.sql" % tmp_db_name
    fabric_run_command(cmd, ignore_errors=False, destination_host=world.f_cfg.mgmt_address)

    # start kea, which should fail due to mismatch in db version
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(MGMT_ADDRESS)')
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
    srv_control.build_and_send_config_files()
    srv_control.start_srv_during_process('DHCP', 'started')

    # upgrade database
    kea_admin = world.f_cfg.sbin_join('kea-admin')
    srv_msg.execute_shell_cmd("sudo %s db-upgrade pgsql -u %s -p $(DB_PASSWD) -n %s" % (kea_admin, tmp_user_name, tmp_db_name))

    # start kea
    srv_control.start_srv('DHCP', 'started')

    cmd = dict(command="config-get", arguments={})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    # check reservation
    hr_get = {"subnet-id": 1, "identifier-type": "hw-address", "identifier": "01:0a:0b:0c:0d:0e:0f"}
    response = _send_cmd("reservation-get", hr_get)["arguments"]

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
    resp = _send_cmd("lease4-get-by-hw-address", lease_get)["arguments"]
    assert resp["leases"][0]["hw-address"] == "ff:01:02:03:ff:04"
    assert resp["leases"][0]["ip-address"] == "192.168.50.10"
    assert resp["leases"][0]["state"] == 0
    assert resp["leases"][0]["subnet-id"] == 1
    assert resp["leases"][0]["valid-lft"] == 4000
