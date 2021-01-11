"""Host Reservation DHCPv4"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_control
import srv_msg
from forge_cfg import world


def _add_reservation(reservation, exp_result=0, exp_failed=False):
    cmd = {"command": "reservation-add", "arguments": {"reservation": reservation}, "service": ['dhcp4']}
    if "subnet-id" not in cmd["arguments"]["reservation"]:
        cmd["arguments"]["reservation"].update({"subnet-id": 1})
    result = srv_msg.send_ctrl_cmd_via_http(command=cmd, exp_result=exp_result, exp_failed=exp_failed)
    if result is None:
        return None
    return result[0]


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
@pytest.mark.parametrize("backend", ['memfile', 'MySQL', 'PostgreSQL'])
def test_v4_host_reservation_conflicts_duplicate_mac_reservations(backend):
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    if backend == 'memfile':
        srv_control.host_reservation_in_subnet('ip-address',
                                               '192.168.50.10',
                                               0,
                                               'hw-address',
                                               'ff:01:02:03:ff:04')  # the same MAC address
        srv_control.host_reservation_in_subnet('ip-address',
                                               '192.168.50.12',
                                               0,
                                               'hw-address',
                                               'ff:01:02:03:ff:04')  # the same MAC address
        srv_control.build_and_send_config_files()
        srv_control.start_srv_during_process('DHCP', 'configuration')

        # expected error logs
        srv_msg.log_contains(r'ERROR \[kea-dhcp4.dhcp4')
        srv_msg.log_contains(r'failed to add new host using the HW address')
    else:
        srv_control.add_hooks('libdhcp_host_cmds.so')
        srv_control.open_control_channel()
        srv_control.dump_db_reservation(backend)
        srv_control.new_db_backend_reservation(backend, 'hw-address', 'ff:01:02:03:ff:11')
        srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', backend, 1)
        srv_control.update_db_backend_reservation('ipv4_address', '192.168.50.2', backend, 1)
        srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, backend, 1)

        srv_control.new_db_backend_reservation(backend, 'hw-address', 'ff:01:02:03:ff:11')
        srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', backend, 2)
        srv_control.update_db_backend_reservation('ipv4_address', '192.168.50.3', backend, 2)
        srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, backend, 2)

        # expect failure due to db constrain on unique hw-address
        srv_control.upload_db_reservation(backend, exp_failed=True)


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
@pytest.mark.parametrize("backend", ['MySQL', 'PostgreSQL'])
def test_v4_host_reservation_conflicts_duplicate_mac_reservations_command_control(backend):
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address)
    srv_control.enable_db_backend_reservation(backend)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    assert _add_reservation({"hw-address": "ff:01:02:03:ff:77", "ip-address": "192.168.50.2"})["text"] == "Host added."
    assert _add_reservation({"hw-address": "ff:01:02:03:ff:66", "ip-address": "192.168.50.2"}, exp_result=1)["text"] == "Database duplicate entry error"


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
@pytest.mark.parametrize("backend", ['MySQL', 'PostgreSQL'])
def test_v4_host_reservation_allowed_duplicate_mac_reservations_command_control(backend):
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.set_conf_parameter_global('ip-reservations-unique', False)
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address)
    srv_control.enable_db_backend_reservation(backend)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    assert _add_reservation({"hw-address": "ff:01:02:03:ff:77", "ip-address": "192.168.50.2"})["text"] == "Host added."
    assert _add_reservation({"hw-address": "ff:01:02:03:ff:66", "ip-address": "192.168.50.2"})["text"] == "Host added."


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v4_host_reservation_conflicts_duplicate_ip_reservations():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.host_reservation_in_subnet('ip-address',
                                           '192.168.50.10',  # the same IP address
                                           0,
                                           'hw-address',
                                           'aa:aa:aa:aa:aa:aa')
    srv_control.host_reservation_in_subnet('ip-address',
                                           '192.168.50.10',  # the same IP address
                                           0,
                                           'hw-address',
                                           'bb:bb:bb:bb:bb:bb')
    srv_control.build_and_send_config_files()
    srv_control.start_srv_during_process('DHCP', 'configuration')
    # expected error logs
    srv_msg.log_contains(r'ERROR \[kea-dhcp4.dhcp4')
    srv_msg.log_contains(r'failed to add new host using the HW address')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
@pytest.mark.parametrize("backend", ['memfile', 'MySQL', 'PostgreSQL'])
def test_v4_host_reservation_duplicate_ip_reservations_allowed(backend):
    the_same_ip_address = '192.168.50.10'
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.add_hooks('libdhcp_host_cmds.so')
    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address)
    srv_control.enable_db_backend_reservation(backend)
    # allow non-unique IP address in multiple reservations
    srv_control.set_conf_parameter_global('ip-reservations-unique', False)
    if backend == 'memfile':
        srv_control.host_reservation_in_subnet('ip-address',
                                               the_same_ip_address,  # the same IP
                                               0,
                                               'hw-address',
                                               'aa:aa:aa:aa:aa:aa')
        srv_control.host_reservation_in_subnet('ip-address',
                                               the_same_ip_address,  # the same IP
                                               0,
                                               'hw-address',
                                               'bb:bb:bb:bb:bb:bb')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    if backend != "memfile":
        assert _add_reservation({"hw-address": "aa:aa:aa:aa:aa:aa", "ip-address": the_same_ip_address})["text"] == "Host added."
        assert _add_reservation({"hw-address": "bb:bb:bb:bb:bb:bb", "ip-address": the_same_ip_address})["text"] == "Host added."

    # these error logs should not appear
    srv_msg.log_doesnt_contain(r'ERROR \[kea-dhcp4.dhcp4')
    srv_msg.log_doesnt_contain(r'failed to add new host using the HW address')

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
    srv_msg.check_leases(srv_msg.get_all_leases(),)

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
    srv_msg.check_leases(srv_msg.get_all_leases(),)

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
    srv_msg.check_leases(srv_msg.get_all_leases())  # backend for leases is still memfile


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
@pytest.mark.parametrize("backend", ['memfile', 'MySQL', 'PostgreSQL'])
def test_v4_host_reservation_conflicts_duplicate_reservations_different_subnets(backend):
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    if backend == 'memfile':
        srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                           '192.168.51.1-192.168.51.50')
        srv_control.host_reservation_in_subnet('ip-address',
                                               '192.168.50.10',
                                               0,
                                               'hw-address',
                                               'ff:01:02:03:ff:04')
        srv_control.host_reservation_in_subnet('ip-address',
                                               '192.168.51.12',
                                               1,
                                               'hw-address',
                                               'ff:01:02:03:ff:04')
    else:
        srv_control.dump_db_reservation(backend)
        srv_control.new_db_backend_reservation(backend, 'hw-address', 'ff:01:02:03:ff:11')
        srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', backend, 1)
        srv_control.update_db_backend_reservation('ipv4_address', '192.168.50.2', backend, 1)
        srv_control.update_db_backend_reservation('dhcp4_subnet_id', 1, backend, 1)

        srv_control.new_db_backend_reservation(backend, 'hw-address', 'ff:01:02:03:ff:11')
        srv_control.update_db_backend_reservation('hostname', 'reserved-hostname', backend, 2)
        srv_control.update_db_backend_reservation('ipv4_address', '192.168.51.3', backend, 2)
        srv_control.update_db_backend_reservation('dhcp4_subnet_id', 2, backend, 2)
        srv_control.upload_db_reservation(backend)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
@pytest.mark.parametrize("backend", ['memfile', 'MySQL', 'PostgreSQL'])
def test_v4_host_reservation_conflicts_reconfigure_server_with_reservation_of_used_address(backend):

    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.2')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:11')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:11')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:55')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:55')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')

    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.3')
    if backend == 'memfile':
        srv_control.host_reservation_in_subnet('ip-address',
                                               '192.168.50.2',
                                               0,
                                               'hw-address',
                                               'ff:01:02:03:ff:77')
    else:
        srv_control.add_hooks('libdhcp_host_cmds.so')
        srv_control.enable_db_backend_reservation(backend)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'reconfigured')

    if backend != 'memfile':
        _add_reservation({"hw-address": "ff:01:02:03:ff:77", "ip-address": "192.168.50.2"})

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:77')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.2', expected=False)
    srv_msg.response_check_content('yiaddr', '192.168.50.3')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
@pytest.mark.parametrize("backend", ['memfile', 'MySQL', 'PostgreSQL'])
def test_v4_host_reservation_conflicts_reserve_assigned_address_to_different_client(backend):

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.2')
    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address)
    if backend == 'memfile':
        srv_control.host_reservation_in_subnet('ip-address',
                                               '192.168.50.2',
                                               0,
                                               'hw-address',
                                               'ff:01:02:03:ff:11')
    else:
        srv_control.add_hooks('libdhcp_host_cmds.so')
        srv_control.enable_db_backend_reservation(backend)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    if backend != 'memfile':
        _add_reservation({"hw-address": "ff:01:02:03:ff:11", "ip-address": "192.168.50.2"})

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:11')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:11')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.2')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:55')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:55')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.3')
    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address)
    if backend == 'memfile':
        srv_control.host_reservation_in_subnet('ip-address',
                                               '192.168.50.2',
                                               0,
                                               'hw-address',
                                               'ff:01:02:03:ff:77')
    else:
        srv_control.dump_db_reservation(backend)
        srv_control.add_hooks('libdhcp_host_cmds.so')
        srv_control.enable_db_backend_reservation(backend)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'reconfigured')

    if backend != 'memfile':
        _add_reservation({"hw-address": "ff:01:02:03:ff:77", "ip-address": "192.168.50.2"})

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:77')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.2', expected=False)


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
@pytest.mark.parametrize("backend", ['memfile', 'MySQL', 'PostgreSQL'])
def test_v4_host_reservation_conflicts_change_reserved_address_during_reconfigure(backend):
    misc.test_setup()
    # reconfigure different address for same MAC from outside of the pool
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.9')
    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address)
    if backend == 'memfile':
        srv_control.host_reservation_in_subnet('ip-address',
                                               '192.168.50.10',
                                               0,
                                               'hw-address',
                                               'ff:01:02:03:ff:04')
    else:
        srv_control.add_hooks('libdhcp_host_cmds.so')
        srv_control.enable_db_backend_reservation(backend)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    if backend != 'memfile':
        _add_reservation({"hw-address": "ff:01:02:03:ff:04", "ip-address": "192.168.50.10"})

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.9')
    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address)
    if backend == 'memfile':
        srv_control.host_reservation_in_subnet('ip-address',
                                               '192.168.50.30',
                                               0,
                                               'hw-address',
                                               'ff:01:02:03:ff:04')
    else:
        srv_control.dump_db_reservation(backend)
        srv_control.add_hooks('libdhcp_host_cmds.so')
        srv_control.enable_db_backend_reservation(backend)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'reconfigured')

    if backend != 'memfile':
        _add_reservation({"hw-address": "ff:01:02:03:ff:04", "ip-address": "192.168.50.30"})

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.30')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.30')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
@pytest.mark.parametrize("backend", ['memfile', 'MySQL', 'PostgreSQL'])
def test_v4_host_reservation_conflicts_reconfigure_server_add_reservation_for_host_that_has_lease(backend):
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.5')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address)
    if backend == 'memfile':
        srv_control.host_reservation_in_subnet('ip-address',
                                               '192.168.50.50',
                                               0,
                                               'hw-address',
                                               'ff:01:02:03:ff:04')
    else:
        srv_control.dump_db_reservation(backend)
        srv_control.add_hooks('libdhcp_host_cmds.so')
        srv_control.enable_db_backend_reservation(backend)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'reconfigured')

    if backend != 'memfile':
        _add_reservation({"hw-address": "ff:01:02:03:ff:04", "ip-address": "192.168.50.50"})

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.50')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.50')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.5')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
@pytest.mark.parametrize("backend", ['memfile', 'MySQL', 'PostgreSQL'])
def test_v4_host_reservation_conflicts_renew_address_using_different_mac_that_has_been_reserved_during_reconfiguration(backend):

    misc.test_setup()
    srv_control.set_time('renew-timer', 3)
    srv_control.set_time('rebind-timer', 50)
    srv_control.set_time('valid-lifetime', 500)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.5')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.5')

    srv_msg.forge_sleep(5, 'seconds')

    misc.test_setup()
    srv_control.set_time('renew-timer', 3)
    srv_control.set_time('rebind-timer', 50)
    srv_control.set_time('valid-lifetime', 500)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.10')
    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address)
    if backend == 'memfile':
        srv_control.host_reservation_in_subnet('ip-address',
                                               '192.168.50.5',
                                               0,
                                               'hw-address',
                                               'ff:01:02:03:ff:04')
    else:
        srv_control.dump_db_reservation(backend)
        srv_control.add_hooks('libdhcp_host_cmds.so')
        srv_control.enable_db_backend_reservation(backend)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'reconfigured')

    if backend != 'memfile':
        _add_reservation({"hw-address": "ff:01:02:03:ff:04", "ip-address": "192.168.50.5"})

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.5', expected=False)

    misc.test_procedure()
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.5')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'NAK')

    srv_msg.forge_sleep(6, 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.5')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'NAK')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
@pytest.mark.parametrize("backend", ['memfile', 'MySQL', 'PostgreSQL'])
def test_v4_host_reservation_conflicts_renew_address_which_reservation_changed_during_reconfigure(backend):

    misc.test_setup()
    srv_control.set_time('renew-timer', 3)
    srv_control.set_time('rebind-timer', 50)
    srv_control.set_time('valid-lifetime', 500)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address)
    if backend == 'memfile':
        srv_control.host_reservation_in_subnet('ip-address',
                                               '192.168.50.5',
                                               0,
                                               'hw-address',
                                               'ff:01:02:03:ff:01')
    else:
        srv_control.add_hooks('libdhcp_host_cmds.so')
        srv_control.enable_db_backend_reservation(backend)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    if backend != 'memfile':
        _add_reservation({"hw-address": "ff:01:02:03:ff:01", "ip-address": "192.168.50.5"})

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.5')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.5')

    srv_msg.forge_sleep(5, 'seconds')

    misc.test_setup()
    srv_control.set_time('renew-timer', 3)
    srv_control.set_time('rebind-timer', 50)
    srv_control.set_time('valid-lifetime', 500)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.5-192.168.50.60')
    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address)
    if backend == 'memfile':
        srv_control.host_reservation_in_subnet('ip-address',
                                               '192.168.50.50',
                                               0,
                                               'hw-address',
                                               'ff:01:02:03:ff:01')
    else:
        srv_control.dump_db_reservation(backend)
        srv_control.add_hooks('libdhcp_host_cmds.so')
        srv_control.enable_db_backend_reservation(backend)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'reconfigured')

    if backend != 'memfile':
        _add_reservation({"hw-address": "ff:01:02:03:ff:01", "ip-address": "192.168.50.50"})

    misc.test_procedure()
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.5')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'NAK')

    srv_msg.forge_sleep(6, 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.50')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.50')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.50')


@pytest.mark.v4
@pytest.mark.host_reservation
@pytest.mark.kea_only
@pytest.mark.parametrize("backend", ['memfile', 'MySQL', 'PostgreSQL'])
def test_v4_host_reservation_conflicts_rebind_address_which_reservation_changed_during_reconfigure(backend):

    misc.test_setup()
    srv_control.set_time('renew-timer', 3)
    srv_control.set_time('rebind-timer', 4)
    srv_control.set_time('valid-lifetime', 500)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address)
    if backend == 'memfile':
        srv_control.host_reservation_in_subnet('ip-address',
                                               '192.168.50.5',
                                               0,
                                               'hw-address',
                                               'ff:01:02:03:ff:01')
    else:
        srv_control.add_hooks('libdhcp_host_cmds.so')
        srv_control.enable_db_backend_reservation(backend)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    if backend != 'memfile':
        _add_reservation({"hw-address": "ff:01:02:03:ff:01", "ip-address": "192.168.50.5"})

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.5')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.5')

    srv_msg.forge_sleep(5, 'seconds')

    misc.test_setup()
    srv_control.set_time('renew-timer', 3)
    srv_control.set_time('rebind-timer', 4)
    srv_control.set_time('valid-lifetime', 500)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.open_control_channel()
    srv_control.agent_control_channel(world.f_cfg.mgmt_address)
    if backend == 'memfile':
        srv_control.host_reservation_in_subnet('ip-address',
                                               '192.168.50.50',
                                               0,
                                               'hw-address',
                                               'ff:01:02:03:ff:01')
    else:
        srv_control.dump_db_reservation(backend)
        srv_control.add_hooks('libdhcp_host_cmds.so')
        srv_control.enable_db_backend_reservation(backend)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'reconfigured')

    if backend != 'memfile':
        _add_reservation({"hw-address": "ff:01:02:03:ff:01", "ip-address": "192.168.50.50"})

    misc.test_procedure()
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.5')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'NAK')

    srv_msg.forge_sleep(6, 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.50')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:01')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.50')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.50')
