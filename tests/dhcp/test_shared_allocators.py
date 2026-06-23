# Copyright (C) 2026 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea shared random and flq allocators"""


import ipaddress
import logging
import pytest

from src import misc
from src.softwaresupport.database import (
    configure_listening_addresses_on_the_database_server,
    clear_database,
    restart_database,
)
from src import srv_control
from src import srv_msg

from src.forge_cfg import world

log = logging.getLogger("forge")


@pytest.fixture()
def _restart_all_databases(backend):
    """Restart database even if test fails.

    :param backend: database backend
    """
    clear_database(world.f_cfg.mgmt_address)
    restart_database(backend, host=world.f_cfg.mgmt_address)
    yield
    # if not world.f_cfg.teardown_after_last_test and world.current_test_index == world.test_count:
    #     return
    clear_database(world.f_cfg.mgmt_address)
    restart_database(backend, host=world.f_cfg.mgmt_address)


def _get_sflq_lease_4(
    mac: str, giaddr: str, all_leases: list = None, netmask: int = 16
):
    """Get v4 lease from kea. Check if address is correct by checking previously assigned address.
    :param mac: mac address of a client
    :type mac:
    :param giaddr: relay address
    :type giaddr:
    :param all_leases: list of previously assigned leases from single subnet
    :type all_leases:
    :param netmask: subnet netmask
    :type netmask:
    :return: dictionary with single lease
    :rtype: dict
    """
    misc.test_procedure()
    srv_msg.network_variable("source_port", 67)
    srv_msg.network_variable("source_address", "$(GIADDR4)")
    srv_msg.network_variable("destination_address", "$(SRV4_ADDR)")
    srv_msg.client_sets_value("Client", "giaddr", giaddr)
    srv_msg.client_sets_value("Client", "chaddr", mac)  # '00:00:00:00:00:22'
    srv_msg.client_sets_value("Client", "hops", 1)
    srv_msg.client_send_msg("DISCOVER")

    misc.pass_criteria()
    msg = srv_msg.send_wait_for_message("MUST", "OFFER")[0]
    srv_msg.response_check_include_option(1)

    misc.test_procedure()
    srv_msg.client_sets_value("Client", "giaddr", giaddr)
    srv_msg.client_sets_value("Client", "hops", 1)
    srv_msg.client_sets_value("Client", "chaddr", mac)
    srv_msg.client_copy_option("server_id")
    srv_msg.client_does_include_with_value("requested_addr", msg.yiaddr)
    srv_msg.client_send_msg("REQUEST")

    misc.pass_criteria()
    srv_msg.send_wait_for_message("MUST", "ACK")
    srv_msg.response_check_content("yiaddr", msg.yiaddr)

    lease = srv_msg.get_all_leases()
    srv_msg.check_if_address_belongs_to_subnet(
        subnet=f"{giaddr[:-1]}0/{netmask}", address=lease["address"]
    )
    # let's check if address is actually correct for allocator

    if len(all_leases) != 0:
        assert (
            ipaddress.ip_address(msg.yiaddr)
            != ipaddress.ip_address(all_leases[-1]["address"]) + 256
        ), (
            f"Received address {msg.yiaddr} is simple +1 on third octet after previously assigned."
            "This is incorrect for sflq"
        )
        log.debug("Current %s previous was %s", msg.yiaddr, all_leases[-1]["address"])
    return lease


@pytest.mark.usefixtures('_restart_all_databases')
@pytest.mark.v4
@pytest.mark.ha  # Piggybacking on HA test so we do not have to run separate job for only one test using dual_server.
@pytest.mark.dual_server
@pytest.mark.allocators
@pytest.mark.parametrize("backend", ["postgresql", "mysql"])
@pytest.mark.parametrize("scope", ["subnets", "shared-networks"])
@pytest.mark.parametrize("servers", ["single", "dual"])
def test_v4_allocators_sflq_ramdomness(backend, scope, servers):
    """Get 10 addresses from each subnet, check if:
    - sflq should select random pool from subnet.
    - check if all leases are correctly saved in the lease file/database
    Picking 10 leases form 1500 pools has 0.6% chance of getting subsequent addresses.
    :param backend: database backend
    :type backend: str
    :param scope: If shared networks are used, test will be run on shared networks.
    :type scope: str
    :param servers: number of kea servers to run tests on.
    :type servers: str
    """
    misc.test_setup()
    srv_control.config_srv_subnet("192.0.0.0/8", "192.0.0.0/32", allocator="shared-flq")
    for i in range(0, 5):
        for j in range(1, 250):
            srv_control.new_pool(f"192.{i}.{j}.0/32", 0)

    if scope == "shared_networks":
        srv_control.shared_subnet("192.0.0.0/8", 0)
        srv_control.set_conf_parameter_shared_subnet("name", '"name-abc"', 0)
        srv_control.set_conf_parameter_shared_subnet(
            "interface", '"$(SERVER_IFACE)"', 0
        )

    srv_control.define_lease_db_backend(backend)
    if servers == "dual":
        configure_listening_addresses_on_the_database_server(
            backend, host=world.f_cfg.mgmt_address
        )
    srv_control.build_and_send_config_files()
    srv_control.start_srv("DHCP", "started")

    # SERVER 2
    if servers == "dual":
        misc.test_setup()
        srv_control.clear_some_data("all", dest=world.f_cfg.mgmt_address_2)
        srv_control.config_srv_subnet("192.0.0.0/8", "192.0.0.0/32", allocator="shared-flq")
        for i in range(0, 5):
            for j in range(1, 250):
                srv_control.new_pool(f"192.{i}.{j}.0/32", 0)

        if scope == "shared_networks":
            srv_control.shared_subnet("192.0.0.0/8", 0)
            srv_control.set_conf_parameter_shared_subnet("name", '"name-abc"', 0)

        srv_control.define_lease_db_backend(backend, db_host=world.f_cfg.mgmt_address)
        world.dhcp_cfg["interfaces-config"]["interfaces"] = []
        srv_control.build_and_send_config_files(dest=world.f_cfg.mgmt_address_2)
        srv_control.start_srv("DHCP", "started", dest=world.f_cfg.mgmt_address_2)

    leases_subnet1 = []
    for i in range(10, 20):
        leases_subnet1.append(
            _get_sflq_lease_4(f"22:00:00:00:00:{i}", "192.0.0.1", leases_subnet1, netmask=8)
        )

    srv_msg.check_leases(leases_subnet1, backend=backend)
