# Copyright (C) 2024 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Stash Agent Options DHCPv4"""

# Goal of those tests are to verify if server is able to stash agent options
# and in result can renew/release the lease based on those options.
# Host reservations based on circuit-id are also included into the tests.
# This is DHCP v4 only feature

import pytest

from src import misc
from src import srv_msg
from src import srv_control

from src.forge_cfg import world
from src.protosupport.multi_protocol_functions import log_contains


def _get_lease(mac, ip_address, relay_info, backend):
    """_get_lease Get a lease for a client that is simulating traffic via Relay Agent.

    :param mac: MAC address of the client
    :type mac: str
    :param ip_address: expected IP address
    :type ip_address: str
    :param relay_info: relay agent information option content (circuit-id, remote-id, relay-id)
    :type relay_info: str
    :param backend: backend type (memfile, mysql, postgresql)
    :type backend: str
    :return: lease assigned to the client
    :rtype: list
    """
    misc.test_procedure()
    srv_msg.network_variable("source_port", 67)
    srv_msg.network_variable("source_address", "$(GIADDR4)")
    srv_msg.network_variable("destination_address", "$(SRV4_ADDR)")
    srv_msg.client_sets_value("Client", "giaddr", "$(GIADDR4)")
    srv_msg.client_sets_value("Client", "hops", 1)
    srv_msg.client_sets_value("Client", "chaddr", mac)
    srv_msg.client_does_include_with_value("relay_agent_information", relay_info)
    srv_msg.client_send_msg("DISCOVER")

    misc.pass_criteria()
    msg = srv_msg.send_wait_for_message("MUST", "OFFER")[0]
    if ip_address:
        srv_msg.response_check_content("yiaddr", ip_address)

    misc.test_procedure()
    srv_msg.network_variable("source_port", 67)
    srv_msg.network_variable("source_address", "$(GIADDR4)")
    srv_msg.network_variable("destination_address", "$(SRV4_ADDR)")
    srv_msg.client_sets_value("Client", "giaddr", "$(GIADDR4)")
    srv_msg.client_sets_value("Client", "hops", 1)
    srv_msg.client_copy_option("server_id")
    srv_msg.client_does_include_with_value("requested_addr", ip_address if ip_address else msg.yiaddr)
    srv_msg.client_sets_value("Client", "chaddr", mac)
    srv_msg.client_does_include_with_value("relay_agent_information", relay_info)
    srv_msg.client_send_msg("REQUEST")

    misc.pass_criteria()
    srv_msg.send_wait_for_message("MUST", "ACK")
    srv_msg.response_check_content("yiaddr", ip_address if ip_address else msg.yiaddr)
    lease = srv_msg.get_all_leases()
    srv_msg.check_leases(lease, backend=backend)
    return lease


def _renew_locally(ip_address, mac, expect):
    """_renew_locally Renew address locally. DHCPv4 protocol assumes
    renewals are done by directly sending a message to the server.

    :param ip_address: client IP address
    :type ip_address: str
    :param mac: client MAC address
    :type mac: str
    :param expect: expected result (True - ACK, False - NAK)
    :type expect: boolean
    """
    misc.test_procedure()
    srv_msg.network_variable("source_port", 68)
    srv_msg.network_variable("source_address", "$(GIADDR4)")
    srv_msg.network_variable("destination_address", "$(SRV4_ADDR)")
    srv_msg.client_sets_value("Client", "giaddr", "0.0.0.0")
    srv_msg.client_sets_value("Client", "ciaddr", ip_address)
    srv_msg.client_sets_value("Client", "yiaddr", "0.0.0.0")
    srv_msg.client_sets_value("Client", "siaddr", "$(SRV4_ADDR)")
    srv_msg.client_sets_value("Client", "hops", 0)
    srv_msg.client_copy_option("server_id")
    srv_msg.client_does_include_with_value("requested_addr", ip_address)
    srv_msg.client_sets_value("Client", "chaddr", mac)
    srv_msg.client_send_msg("REQUEST")

    misc.pass_criteria()
    if expect:
        srv_msg.send_wait_for_message("MUST", "ACK")
        srv_msg.response_check_content("yiaddr", ip_address)
    else:
        srv_msg.send_wait_for_message("MUST", "NAK")


def _release_locally(ip_address, mac):
    """_release_locally Release address locally. DHCPv4 protocol assumes
    releases are done by directly sending a message to the server.

    :param ip_address: client IP address
    :type ip_address: str
    :param mac: client MAC address
    :type mac: str
    """
    misc.test_procedure()
    srv_msg.client_sets_value("Client", "chaddr", mac)
    srv_msg.client_sets_value("Client", "ciaddr", ip_address)
    srv_msg.client_send_msg("RELEASE")

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()


def _reservation_add(reservation: dict, backend: str):
    """
    Send reservation add command
    :param reservation: dictionary with reservation
    :return: dict, response from Kea
    """
    target = "memory" if backend == "memfile" else "database"

    return srv_msg.send_ctrl_cmd(
        {
            "arguments": {"reservation": reservation, "operation-target": target},
            "command": "reservation-add",
        }
    )


@pytest.mark.v4
def test_v4_basic_configuration():
    """test_v4_basic_configuration Check basic configuration of stash-agent-options"""
    cmd = {"command": "config-get"}

    # default setting
    misc.test_setup()
    srv_control.config_srv_subnet("192.168.50.0/24", "192.168.50.1-192.168.50.1", id=1)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv("DHCP", "started")

    rsp = srv_msg.send_ctrl_cmd(cmd)
    assert not rsp["arguments"]["Dhcp4"][
        "stash-agent-options"
    ], "Default value of stash-agent-options is incorrect"

    misc.test_setup()
    srv_control.config_srv_subnet("192.168.50.0/24", "192.168.50.1-192.168.50.1", id=1)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.set_conf_parameter_global("stash-agent-options", True)
    srv_control.build_and_send_config_files()
    srv_control.start_srv("DHCP", "started")

    rsp = srv_msg.send_ctrl_cmd(cmd)
    assert rsp["arguments"]["Dhcp4"][
        "stash-agent-options"
    ], "Value of stash-agent-options is incorrect"

    misc.test_setup()
    srv_control.config_srv_subnet("192.168.50.0/24", "192.168.50.1-192.168.50.1", id=1)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.set_conf_parameter_global("stash-agent-options", False)
    srv_control.build_and_send_config_files()
    srv_control.start_srv("DHCP", "started")

    rsp = srv_msg.send_ctrl_cmd(cmd)
    assert not rsp["arguments"]["Dhcp4"][
        "stash-agent-options"
    ], "Value of stash-agent-options is incorrect"


@pytest.mark.v4
@pytest.mark.parametrize("backend", ["memfile", "mysql", "postgresql"])
@pytest.mark.parametrize("stash", [True, False])
def test_v4_lease_circuit(backend, stash):
    """test_v4_lease_circuit test stash-agent-options with circuit-id based reservations,
    check address assign, renew and release.
    Used backends for leases and reservations are memfile, mysql and postgresql.

    :param backend: backend type
    :type backend: str
    :param stash: stash-agent-options value
    :type stash: boolean
    """
    misc.test_setup()
    srv_control.config_srv_subnet(
        "192.168.50.0/24", "192.168.50.100-192.168.50.200", id=66
    )
    srv_control.shared_subnet("192.168.50.0/24", 0)
    srv_control.set_conf_parameter_shared_subnet("name", '"name-xyz"', 0)
    srv_control.set_conf_parameter_shared_subnet(
        "relay", '{"ip-addresses": ["$(GIADDR4)"]}', 0
    )

    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.enable_db_backend_reservation(backend)
    srv_control.add_hooks("libdhcp_host_cmds.so")
    srv_control.add_hooks("libdhcp_lease_cmds.so")
    srv_control.set_conf_parameter_global("stash-agent-options", stash)
    srv_control.set_conf_parameter_global("store-extended-info", True)

    # let's run auto recamation every 200 seconds, we don't want it
    # to interfere with reclamation triggered manually
    reclaim = {
        "reclaim-timer-wait-time": 200,
    }
    world.dhcp_cfg.update({"expired-leases-processing": reclaim})

    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv("DHCP", "started")

    for i in range(4, 9):
        res = {
            "circuit-id": f"'circuit{i}'",
            "ip-address": f"192.168.50.{i}",
            "subnet-id": 66,
        }
        _reservation_add(res, backend)

    for i in range(4, 9):
        _get_lease(
            f"00:00:00:00:0{i}:03",
            f"192.168.50.{i}",
            f"0108636972637569743{i}",
            backend,
        )

    srv_msg.forge_sleep(3)
    for i in range(4, 9):
        _renew_locally(f"192.168.50.{i}", f"00:00:00:00:0{i}:03", expect=stash)

        # check leases:
        if not stash:
            continue
        if backend == "memfile":
            srv_msg.execute_shell_cmd(
                f"cat {world.f_cfg.get_leases_path()} > /tmp/kea-leases.csv"
            )
        else:
            srv_msg.lease_dump(backend)
        # let's just check that those values are in lease file,
        # if they are assigned to correct client will be checked via renew
        log_contains(
            f'sub-options": "0x0108636972637569743{i}', "/tmp/kea-leases.csv"
        )  # circuit id, but not recognised

    # let's check if renew without circuit-id won't change content of the lease
    # and it's possible to renew it multiple time
    srv_msg.forge_sleep(3)
    for i in range(4, 9):
        _renew_locally(f"192.168.50.{i}", f"00:00:00:00:0{i}:03", expect=stash)

    # let's check if renewed addresses are handeled correctly
    cmd = {"command": "lease4-get-all", "arguments": {"subnets": [66]}}
    rsp = srv_msg.send_ctrl_cmd(cmd)
    assert "5 IPv4 lease(s) found." in rsp["text"], "Lease count text is incorrect"
    assert (
        len(rsp["arguments"]["leases"]) == 5
    ), "Number of leases returned is incorrect"

    srv_msg.forge_sleep(5)

    # release is easy, it can be done every time
    for i in range(4, 9):
        _release_locally(f"192.168.50.{i}", f"00:00:00:00:0{i}:03")
        # check leases:
        if backend == "memfile":
            srv_msg.execute_shell_cmd(
                f"cat {world.f_cfg.get_leases_path()} > /tmp/kea-leases.csv"
            )
        else:
            srv_msg.lease_dump(backend)
        # let's make sure that lease is actyally released,
        # if it wouldn't be, ",,0," would contain lifetime value instead of 0
        log_contains(f"192.168.50.{i},00:00:00:00:0{i}:03,,0,", "/tmp/kea-leases.csv")

    # for quicker debugging
    srv_msg.print_leases(backend)

    # this should clean up all leases
    cmd = {"command": "leases-reclaim", "arguments": {"remove": True}}
    srv_msg.send_ctrl_cmd(cmd)

    # wait for kea
    srv_msg.forge_sleep(2)

    # and let's check that all leases are indeed removed
    cmd = {"command": "lease4-get-all", "arguments": {"subnets": [66]}}
    srv_msg.send_ctrl_cmd(cmd, exp_result=3)


@pytest.mark.v4
@pytest.mark.parametrize("backend", ["memfile", "mysql", "postgresql"])
@pytest.mark.parametrize("option", ["relay_id", "remote_id"])
@pytest.mark.parametrize("stash", [True, False])
def test_v4_lease_agent_option(backend, option, stash):
    """test_v4_lease_agent_option test stash-agent-options with relay-id and
    remote-id based reservations, check address assign, renew and release.
    Used backends for leases and reservations are memfile, mysql and postgresql.

    :param backend: type of backend
    :type backend: str
    :param option: type of relay agent suboption used in the test (relay_id or remote_id)
    :type option: str
    :param stash: stash-agent-options value
    :type stash: boolean
    """
    misc.test_setup()
    srv_control.config_srv_subnet(
        "192.168.50.0/24", "192.168.50.100-192.168.50.200", id=66
    )
    srv_control.shared_subnet("192.168.50.0/24", 0)
    srv_control.set_conf_parameter_shared_subnet("name", '"name-xyz"', 0)
    srv_control.set_conf_parameter_shared_subnet(
        "relay", '{"ip-addresses": ["$(GIADDR4)"]}', 0
    )

    # setup flex-id as host reservation identifier and expression to option suboptions
    # of an option 82 - Relay Agent Information
    srv_control.add_line({"host-reservation-identifiers": ["flex-id"]})
    # relay id suboption code is 12
    # remote id suboption code is 2
    srv_control.add_hooks("libdhcp_flex_id.so")
    srv_control.add_parameter_to_hook(
        1, "identifier-expression", f"relay4[{12 if option == 'relay_id' else 2}].hex"
    )

    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.enable_db_backend_reservation(backend)

    srv_control.add_hooks("libdhcp_host_cmds.so")
    srv_control.add_hooks("libdhcp_lease_cmds.so")
    srv_control.set_conf_parameter_global("stash-agent-options", stash)
    srv_control.set_conf_parameter_global("store-extended-info", True)

    # let's run auto recamation every 200 seconds, we don't want it
    # to interfere with reclamation triggered manually
    reclaim = {
        "reclaim-timer-wait-time": 200,
    }
    world.dhcp_cfg.update({"expired-leases-processing": reclaim})

    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv("DHCP", "started")

    for i in range(4, 9):
        res = {
            "flex-id": f"'relay{i}'" if option == "relay_id" else f"'remote{i}'",
            "ip-address": f"192.168.50.{i}",
            "subnet-id": 66,
        }
        _reservation_add(res, backend)

    # option coding: relay1 72656c617931, code 12, len 6, that is: 0C0672656c617931
    # option coding: remote1 72656d6f746531, code, 2, len 7, that is: 020772656d6f746531
    # and for loop will change last digit

    for i in range(4, 9):
        _get_lease(
            f"00:00:00:00:0{i}:03",
            f"192.168.50.{i}",
            f"0C0672656C61793{i}" if option == "relay_id" else f"020772656D6F74653{i}",
            backend,
        )

    srv_msg.forge_sleep(3)
    for i in range(4, 9):
        _renew_locally(f"192.168.50.{i}", f"00:00:00:00:0{i}:03", expect=stash)

    # renew again, just to make sure that renew is not removing agent options from leases
    srv_msg.forge_sleep(3)
    for i in range(4, 9):
        _renew_locally(f"192.168.50.{i}", f"00:00:00:00:0{i}:03", expect=stash)
        # check leases:
        if not stash:
            continue
        if backend == "memfile":
            srv_msg.execute_shell_cmd(
                f"cat {world.f_cfg.get_leases_path()} > /tmp/kea-leases.csv"
            )
        else:
            srv_msg.lease_dump(backend)
        # let's just check that those values are in lease file,
        # if they are assigned to correct client will be checked via renew
        log_contains(
            f'sub-options": "0x0C0672656C61793{i}'
            if option == "relay_id"
            else f'sub-options": "0x020772656D6F74653{i}',
            "/tmp/kea-leases.csv",
        )

    # let's check if renewed addresses are handeled correctly
    cmd = {"command": "lease4-get-all", "arguments": {"subnets": [66]}}
    rsp = srv_msg.send_ctrl_cmd(cmd)
    assert "5 IPv4 lease(s) found." in rsp["text"], "Lease count text is incorrect"
    assert (
        len(rsp["arguments"]["leases"]) == 5
    ), "Number of leases returned is incorrect"

    srv_msg.forge_sleep(5)
    # release is easy, it can be done every time
    for i in range(4, 9):
        _release_locally(f"192.168.50.{i}", f"00:00:00:00:0{i}:03")

        # check leases:
        if backend == "memfile":
            srv_msg.execute_shell_cmd(
                f"cat {world.f_cfg.get_leases_path()} > /tmp/kea-leases.csv"
            )
        else:
            srv_msg.lease_dump(backend)
        # let's make sure that lease is actyally released,
        # if it wouldn't be, ",,0," would contain lifetime value instead of 0
        log_contains(f"192.168.50.{i},00:00:00:00:0{i}:03,,0,", "/tmp/kea-leases.csv")

    # for quicker debugging
    srv_msg.print_leases(backend)

    # this should clean up all leases
    cmd = {"command": "leases-reclaim", "arguments": {"remove": True}}
    srv_msg.send_ctrl_cmd(cmd)

    # wait for kea
    srv_msg.forge_sleep(2)

    # and let's check that all leases are indeed removed
    cmd = {"command": "lease4-get-all", "arguments": {"subnets": [66]}}
    srv_msg.send_ctrl_cmd(cmd, exp_result=3)
