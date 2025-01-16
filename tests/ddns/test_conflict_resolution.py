# Copyright (C) 2023-2025 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""DDNS DHCID conflict resolution"""

# pylint: disable=invalid-name, line-too-long

import time
import pytest

from src import misc
from src import srv_msg
from src import srv_control
from src.forge_cfg import world


def basic_configuration(version, lft) -> None:
    """basic_configuration Configure basic DHCPv4 server with DDNS and 4 subnets.

    :param version: DHCP version
    :type version: int
    :param lft: global lease lifetime
    :type lft: int
    """
    # control channel
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel(world.f_cfg.mgmt_address)
    srv_control.set_time("renew-timer", 10)
    srv_control.set_time("rebind-timer", 10)
    if version == 6:
        srv_control.set_time("preferred-lifetime", 10)
    srv_control.set_time("valid-lifetime", lft)

    # we need the same client access all subnets not just first one configured
    for i in range(3):
        srv_control.config_client_classification(i, f"VENDOR_CLASS_subnet{i}")

    # last subnet will have longer lease time
    srv_control.set_conf_parameter_subnet("renew-timer", 40, 2)
    srv_control.set_conf_parameter_subnet("rebind-timer", 41, 2)
    if version == 6:
        srv_control.set_conf_parameter_subnet("preferred-lifetime", 42, 2)
    srv_control.set_conf_parameter_subnet("valid-lifetime", 50, 2)

    # shared networks
    if version == 4:
        for i in range(3):
            srv_control.shared_subnet(f"192.168.5{i}.0/24", 0)
    elif version == 6:
        for i in ["a", "b", "c"]:
            srv_control.shared_subnet(f"2001:db8:{i}::/64", 0)

    srv_control.set_conf_parameter_shared_subnet("name", '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet("interface", '"$(SERVER_IFACE)"', 0)

    # ddns
    srv_control.add_ddns_server("127.0.0.1", "53001")
    srv_control.add_ddns_server_connectivity_options('enable-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-send-updates', True)
    srv_control.add_ddns_server_behavioral_options("ddns-qualifying-suffix", "example.com")
    if version == 4:
        srv_control.add_ddns_server_behavioral_options("ddns-generated-prefix", "four")
        srv_control.add_forward_ddns("four.example.com.", "EMPTY_KEY")
        srv_control.add_reverse_ddns("50.168.192.in-addr.arpa.", "EMPTY_KEY")
        srv_control.add_reverse_ddns("51.168.192.in-addr.arpa.", "EMPTY_KEY")
        srv_control.add_reverse_ddns("52.168.192.in-addr.arpa.", "EMPTY_KEY")
    elif version == 6:
        srv_control.add_ddns_server_behavioral_options("ddns-generated-prefix", "six")
        srv_control.add_forward_ddns("six.example.com.", "EMPTY_KEY")
        srv_control.add_reverse_ddns("a.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.", "EMPTY_KEY")
        srv_control.add_reverse_ddns("b.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.", "EMPTY_KEY")
        srv_control.add_reverse_ddns("c.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.", "EMPTY_KEY")


def _check_fqdn_record(
    fqdn: str, address: str = "", version: int = 4, expect: str = "notempty"
) -> None:
    """_check_fqdn_record Check if forward DNS record is present.

    :param version: dhcp version
    :type version: int
    :param fqdn: FQDN value that will be checked
    :type fqdn: str
    :param address: IP address expected from DHCP, defaults to ""
    :type address: str
    :param expect: defines if answer in response from DNS server is expected, defaults to "notempty"
    :type expect: str, optional
    """

    # check new DNS entry
    misc.test_procedure()
    srv_msg.dns_question_record(fqdn, "A" if version == 4 else "AAAA", "IN")
    srv_msg.client_send_dns_query()
    misc.pass_criteria()
    if expect == "empty":
        srv_msg.send_wait_for_query("MUST")
        srv_msg.dns_option("ANSWER", expect_include=False)
    else:
        srv_msg.send_wait_for_query("MUST")
        srv_msg.dns_option("ANSWER")
        srv_msg.dns_option_content("ANSWER", "rdata", address)
        srv_msg.dns_option_content("ANSWER", "rrname", fqdn)


def _check_address_record(fqdn: str, arpa: str, expect: str = "notempty") -> None:
    """_check_address_record Check if reverse DNS record is present.

    :param fqdn: FQDN value that will be checked
    :type fqdn: str
    :param arpa: DNS entry value
    :type arpa: str
    :param expect: defines if answer in response from DNS server is expected, defaults to "notempty"
    :type expect: str, optional
    """
    misc.test_procedure()
    srv_msg.dns_question_record(arpa, "PTR", "IN")
    srv_msg.client_send_dns_query()
    misc.pass_criteria()
    if expect == "empty":
        srv_msg.send_wait_for_query("MUST")
        srv_msg.dns_option("ANSWER", expect_include=False)
    else:
        srv_msg.send_wait_for_query("MUST")
        srv_msg.dns_option("ANSWER")
        srv_msg.dns_option_content("ANSWER", "rdata", fqdn)
        srv_msg.dns_option_content("ANSWER", "rrname", arpa)


def _get_address(
    mac: str, fqdn: str, address: str, expected_fqdn: str = None, class_id: str = None
) -> None:
    """_get_address Get a lease from DHCP server, perform basic checks on responses and content of the lease file.

    :param mac: MAC address of the client e.g. 00:01:02:03:04:05
    :type mac: str
    :param fqdn: FQDN value that will be sent to DHCP server
    :type fqdn: str
    :param address: expected IP address
    :type address: str
    :param expected_fqdn: expected FQDN returned by server, defaults to None, if none it will be equal to fqdn value
    :type expected_fqdn: str, optional
    :param class_id: vendor class id value, defaults to None
    :type class_id: str, optional
    """
    if expected_fqdn is None:
        expected_fqdn = fqdn
    misc.test_procedure()
    srv_msg.client_sets_value("Client", "chaddr", mac)
    srv_msg.client_does_include_with_value("vendor_class_id", class_id)
    srv_msg.client_send_msg("DISCOVER")

    misc.pass_criteria()
    srv_msg.send_wait_for_message("MUST", "OFFER")
    srv_msg.response_check_content("yiaddr", address)

    misc.test_procedure()
    srv_msg.client_copy_option("server_id")
    srv_msg.client_does_include_with_value("vendor_class_id", class_id)
    srv_msg.client_does_include_with_value("requested_addr", address)
    if fqdn is not None:
        srv_msg.client_sets_value("Client", "FQDN_domain_name", fqdn)
        srv_msg.client_sets_value("Client", "FQDN_flags", "S")
        srv_msg.client_does_include("Client", "fqdn")
    srv_msg.client_send_msg("REQUEST")

    misc.pass_criteria()
    srv_msg.send_wait_for_message("MUST", "ACK")
    srv_msg.response_check_content("yiaddr", address)
    if fqdn is not None:
        srv_msg.response_check_include_option(81)
        srv_msg.response_check_option_content(81, "flags", 1)
        srv_msg.response_check_option_content(81, "fqdn", expected_fqdn)

    srv_msg.check_leases(srv_msg.get_all_leases())


def _get_address6(
    duid: str, fqdn: str, address: str, expected_fqdn: str = None, class_id: str = None
) -> None:
    """_get_address Get a lease from DHCP server, perform basic checks on responses and content of the lease file.

    :param duid: DIUD address of the client e.g. 00:01:02:03:04:05
    :type duid: str
    :param fqdn: FQDN value that will be sent to DHCP server
    :type fqdn: str
    :param address: expected IP address
    :type address: str
    :param expected_fqdn: expected FQDN returned by server, defaults to None, if none it will be equal to fqdn value
    :type expected_fqdn: str, optional
    :param class_id: vendor class id value, defaults to None
    :type class_id: str, optional
    """
    if expected_fqdn is None:
        expected_fqdn = fqdn

    misc.test_procedure()
    srv_msg.client_sets_value("Client", "DUID", duid)
    srv_msg.client_does_include("Client", "client-id")
    srv_msg.client_does_include("Client", "IA-NA")
    srv_msg.client_sets_value("Client", "vendor_class_data", class_id)
    srv_msg.client_does_include("Client", "vendor-class")
    srv_msg.client_send_msg("SOLICIT")

    misc.pass_criteria()
    srv_msg.send_wait_for_message("MUST", "ADVERTISE")
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, "sub-option", 5)
    srv_msg.response_check_suboption_content(5, 3, "addr", address)

    misc.test_procedure()
    srv_msg.client_sets_value("Client", "vendor_class_data", class_id)
    srv_msg.client_does_include("Client", "vendor-class")
    srv_msg.client_sets_value("Client", "DUID", duid)
    srv_msg.client_copy_option("IA_NA")
    srv_msg.client_copy_option("server-id")
    if fqdn is not None:
        srv_msg.client_sets_value("Client", "FQDN_domain_name", fqdn)
        srv_msg.client_sets_value("Client", "FQDN_flags", "S")
        srv_msg.client_does_include("Client", "fqdn")
    srv_msg.client_does_include("Client", "client-id")
    srv_msg.client_send_msg("REQUEST")

    misc.pass_criteria()
    srv_msg.send_wait_for_message("MUST", "REPLY")
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, "sub-option", 5)
    srv_msg.response_check_suboption_content(5, 3, "addr", address)
    if fqdn is not None:
        srv_msg.response_check_include_option(39)
        srv_msg.response_check_option_content(39, "flags", "S")
        srv_msg.response_check_option_content(39, "fqdn", expected_fqdn)

    srv_msg.check_leases(srv_msg.get_all_leases())


def _get_address_and_check_dns_record(
    version: int = 4,
    mac: str = None,
    client_fqdn: str = None,
    returned_fqdn: str = None,
    address: str = None,
    arpa: str = None,
    class_id: str = None,
):
    """_get_address_and_update_ddns Get a lease from DHCP server and update DNS records.
    Function checks DNS records before and after lease is obtained, to check if DDNS is working correctly.

    :param version: DHCP version, defaults to 4
    :type version: int, optional
    :param mac: MAC address in case of DHCP v4 and DUID when testing DHCPv6, defaults to None
    :type mac: str
    :param client_fqdn: FQDN value that will be sent to DHCP server, defaults to None
    :type client_fqdn: str
    :param returned_fqdn: FQDN value that will be sent back by DHCP server if None is used test assume that
                          fqdn and expected FQDN are equal, defaults to None
    :type returned_fqdn: str, optional
    :param address: expected IP address, defaults to None
    :type address: str
    :param arpa: DNS entry value, defaults to None
    :type arpa: str
    """
    if returned_fqdn is None:
        returned_fqdn = client_fqdn
    # getting new address that should also generate DDNS entry
    if version == 4:
        _get_address(
            mac, client_fqdn, address, expected_fqdn=returned_fqdn, class_id=class_id
        )
    else:
        _get_address6(
            mac, client_fqdn, address, expected_fqdn=returned_fqdn, class_id=class_id
        )
    # checking both forward and reverse DNS entries
    _check_fqdn_record(returned_fqdn, address=address, version=version)
    _check_address_record(returned_fqdn, arpa)


def send_cmd(cmd, address=world.f_cfg.mgmt_address, exp_result=0, exp_failed=False):
    result = srv_msg.send_ctrl_cmd_via_http(
        command=cmd, address=address, exp_result=exp_result, exp_failed=exp_failed
    )
    if result is None:
        return None
    return result[0]


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.ddns_conflict_resolution
@pytest.mark.parametrize("level", ["global", "subnet", "shared-network"])
def test_ddns4_conflict_resolution_check_with_dhcid(level):
    """
    Test ddns-conflict-resolution-mode set to "check-with-dhcid" at 3 levels.
    https://datatracker.ietf.org/doc/html/rfc4703
    Each new DNS entry is checked against existing entries. If DHCID maches, entry is updated, if not, entry is not updated.
    If record was updated expiration of previous address should not remove DNS record.

    If the same client get's address from different subnet, it should be able to update DNS entry.
    """
    # basic config
    main_valid_lifetime = 25
    misc.test_setup()
    # subnets
    srv_control.config_srv_subnet("192.168.50.0/24", "192.168.50.10-192.168.50.15", id=1)
    srv_control.config_srv_another_subnet_no_interface(
        "192.168.51.0/24", "192.168.51.10-192.168.51.15", id=2
    )
    srv_control.config_srv_another_subnet_no_interface(
        "192.168.52.0/24", "192.168.52.10-192.168.52.15", id=3
    )
    # subnet settings:
    if level == "subnet":
        # it has to be set before shared network is configured
        for i in range(3):
            srv_control.set_conf_parameter_subnet(
                "ddns-conflict-resolution-mode", "check-with-dhcid", i
            )
    basic_configuration(4, main_valid_lifetime)

    # ddns-conflict-resolution-mode settings
    if level == "global":
        srv_control.set_conf_parameter_global(
            "ddns-conflict-resolution-mode", "check-with-dhcid"
        )
    elif level == "subnet":
        # let's set globally and in shared-network different setting
        srv_control.set_conf_parameter_global(
            "ddns-conflict-resolution-mode", "no-check-with-dhcid"
        )
        srv_control.set_conf_parameter_shared_subnet(
            "ddns-conflict-resolution-mode", "no-check-with-dhcid", 0
        )
    elif level == "shared-network":
        # let's set globally different setting
        srv_control.set_conf_parameter_global(
            "ddns-conflict-resolution-mode", "no-check-with-dhcid"
        )
        srv_control.set_conf_parameter_shared_subnet(
            "ddns-conflict-resolution-mode", "check-with-dhcid", 0
        )

    srv_control.build_and_send_config_files()
    srv_control.start_srv("DHCP", "started")

    srv_control.use_dns_set_number(32)
    srv_control.start_srv("DNS", "started")

    # overwrite existing records with the same DHCID

    # client 1 get's en address from subnet 0 (first client will be used to test expiration)
    start_time = time.time()
    _get_address_and_check_dns_record(
        mac="00:00:00:00:11:01",
        client_fqdn="abc-client-1.four.example.com.",
        address="192.168.50.10",
        arpa="10.50.168.192.in-addr.arpa.",
        class_id="subnet0",
    )

    # client 1 get's en address from subnet 2, DNS record should be updated (longer lifetime)
    _get_address_and_check_dns_record(
        mac="00:00:00:00:11:01",
        client_fqdn="abc-client-1.four.example.com.",
        address="192.168.52.10",
        arpa="10.52.168.192.in-addr.arpa.",
        class_id="subnet2",
    )

    # client 2 get's en address from subnet 0
    _get_address_and_check_dns_record(
        mac="00:00:00:00:11:02",
        client_fqdn="abc-client-2.four.example.com.",
        address="192.168.50.11",
        arpa="11.50.168.192.in-addr.arpa.",
        class_id="subnet0",
    )

    # client 2 get's en address from subnet 1, DNS record should be updated
    _get_address_and_check_dns_record(
        mac="00:00:00:00:11:02",
        client_fqdn="abc-client-2.four.example.com.",
        address="192.168.51.10",
        arpa="10.51.168.192.in-addr.arpa.",
        class_id="subnet1",
    )

    # client 3 get's en address from subnet 1, DNS record should be created
    _get_address_and_check_dns_record(
        mac="00:00:00:00:11:03",
        client_fqdn="abc-client-3.four.example.com.",
        address="192.168.51.11",
        arpa="11.51.168.192.in-addr.arpa.",
        class_id="subnet1",
    )

    # client 3 gets an address from subnet 0, tries to use already assigned fqdn, should not update DNS record
    _get_address(
        "00:00:00:00:11:03",
        fqdn="abc-client-1.four.example.com.",
        address="192.168.50.12",
        class_id="subnet0",
    )
    _check_fqdn_record(
        "abc-client-1.four.example.com.", address="192.168.52.10"
    )  # old address!
    _check_address_record(
        "abc-client-1.four.example.com.", "10.52.168.192.in-addr.arpa."
    )

    # client 4 gets an address from subnet 1, tries to use already assigned fqdn, should not update DNS record
    _get_address(
        "00:00:00:00:11:04",
        fqdn="abc-client-3.four.example.com.",
        address="192.168.51.12",
        class_id="subnet1",
    )
    _check_fqdn_record(
        "abc-client-3.four.example.com.", address="192.168.51.11"
    )  # old address!
    _check_address_record(
        "abc-client-3.four.example.com.", "11.51.168.192.in-addr.arpa."
    )

    # client 2 returns with different FQDN, should update DNS record
    _get_address(
        "00:00:00:00:11:02",
        fqdn="abc-client-2-2.four.example.com.",
        address="192.168.51.10",
        class_id="subnet1",
    )
    _check_fqdn_record(
        "abc-client-2-2.four.example.com.", address="192.168.51.10"
    )  # old address!
    _check_address_record(
        "abc-client-2-2.four.example.com.", "10.51.168.192.in-addr.arpa."
    )

    # let's wait for first address to expire, it should not remove DNS record that was created with second lease
    while time.time() - start_time < main_valid_lifetime + 2:
        pass

    _check_address_record(
        "abc-client-1.four.example.com.", "10.52.168.192.in-addr.arpa."
    )
    _check_fqdn_record("abc-client-1.four.example.com.", "192.168.52.10")

    rsp = send_cmd({"command": "config-get", "service": ["dhcp4"], "arguments": {}})
    if level == "global":
        assert rsp["arguments"]["Dhcp4"]["ddns-conflict-resolution-mode"] == "check-with-dhcid"
    elif level == "subnet":
        assert rsp["arguments"]["Dhcp4"]["shared-networks"][0]["ddns-conflict-resolution-mode"] == "no-check-with-dhcid"
        for i in range(3):
            assert rsp["arguments"]["Dhcp4"]["shared-networks"][0]["subnet4"][i]["ddns-conflict-resolution-mode"] == "check-with-dhcid"
    elif level == "shared-network":
        assert rsp["arguments"]["Dhcp4"]["ddns-conflict-resolution-mode"] == "no-check-with-dhcid"
        assert rsp["arguments"]["Dhcp4"]["shared-networks"][0]["ddns-conflict-resolution-mode"] == "check-with-dhcid"


@pytest.mark.v4
@pytest.mark.ddns_conflict_resolution
@pytest.mark.parametrize("level", ["global", "subnet", "shared-network"])
def test_ddns4_conflict_resolution_no_check_with_dhcid(level):
    """
    Test ddns-conflict-resolution-mode set to "no-check-with-dhcid" at 3 levels.

    EacExisting DNS entries may be overwritten by any client, whether or not those entries include a DHCID record.
    """

    # basic config
    main_valid_lifetime = 10
    misc.test_setup()
    # subnets
    srv_control.config_srv_subnet("192.168.50.0/24", "192.168.50.10-192.168.50.15", id=1)
    srv_control.config_srv_another_subnet_no_interface(
        "192.168.51.0/24", "192.168.51.10-192.168.51.15", id=2
    )
    srv_control.config_srv_another_subnet_no_interface(
        "192.168.52.0/24", "192.168.52.10-192.168.52.15", id=3
    )
    # subnet settings:
    if level == "subnet":
        # it has to be set before shared network is configured
        for i in range(3):
            srv_control.set_conf_parameter_subnet(
                "ddns-conflict-resolution-mode", "no-check-with-dhcid", i
            )

    basic_configuration(4, main_valid_lifetime)

    # ddns-conflict-resolution-mode settings
    if level == "global":
        srv_control.set_conf_parameter_global(
            "ddns-conflict-resolution-mode", "no-check-with-dhcid"
        )
    elif level == "subnet":
        # let's set globally and in shared-network different setting
        srv_control.set_conf_parameter_global(
            "ddns-conflict-resolution-mode", "check-with-dhcid"
        )
        srv_control.set_conf_parameter_shared_subnet(
            "ddns-conflict-resolution-mode", "check-with-dhcid", 0
        )
    elif level == "shared-network":
        # let's set globally different setting
        srv_control.set_conf_parameter_global(
            "ddns-conflict-resolution-mode", "check-with-dhcid"
        )
        srv_control.set_conf_parameter_shared_subnet(
            "ddns-conflict-resolution-mode", "no-check-with-dhcid", 0
        )

    srv_control.build_and_send_config_files()
    srv_control.start_srv("DHCP", "started")

    srv_control.use_dns_set_number(32)
    srv_control.start_srv("DNS", "started")

    # client 1 get's en address from subnet 0
    _get_address_and_check_dns_record(
        mac="00:00:00:00:11:01",
        client_fqdn="abc-client-1.four.example.com.",
        address="192.168.50.10",
        arpa="10.50.168.192.in-addr.arpa.",
        class_id="subnet0",
    )

    # client 2 get's en address from subnet 1
    _get_address_and_check_dns_record(
        mac="00:00:00:00:11:02",
        client_fqdn="abc-client-2.four.example.com.",
        address="192.168.51.10",
        arpa="10.51.168.192.in-addr.arpa.",
        class_id="subnet1",
    )

    # client 3 get's en address from subnet 2
    _get_address_and_check_dns_record(
        mac="00:00:00:00:11:03",
        client_fqdn="abc-client-3.four.example.com.",
        address="192.168.52.10",
        arpa="10.52.168.192.in-addr.arpa.",
        class_id="subnet2",
    )

    # let's overwrite now existing records
    # client 4 get's en address from subnet 0 with FQDN assigned to client 1
    _get_address_and_check_dns_record(
        mac="00:00:00:00:11:04",
        client_fqdn="abc-client-1.four.example.com.",
        address="192.168.50.11",
        arpa="11.50.168.192.in-addr.arpa.",
        class_id="subnet0",
    )

    # client 5 get's en address from subnet 1 with FQDN assigned to client 2
    _get_address_and_check_dns_record(
        mac="00:00:00:00:11:05",
        client_fqdn="abc-client-2.four.example.com.",
        address="192.168.51.11",
        arpa="11.51.168.192.in-addr.arpa.",
        class_id="subnet1",
    )

    # client 6 get's en address from subnet 2 with FQDN assigned to client 3
    _get_address_and_check_dns_record(
        mac="00:00:00:00:11:06",
        client_fqdn="abc-client-3.four.example.com.",
        address="192.168.52.11",
        arpa="11.52.168.192.in-addr.arpa.",
        class_id="subnet2",
    )
    start_time = time.time()
    # let's overwrite now existing records
    # client 4 get's en address from subnet 0 with different FQDN
    _get_address_and_check_dns_record(
        mac="00:00:00:00:11:04",
        client_fqdn="abc-client-1-1.four.example.com.",
        address="192.168.50.11",
        arpa="11.50.168.192.in-addr.arpa.",
        class_id="subnet0",
    )

    # client 5 get's en address from subnet 1 with different FQDN
    _get_address_and_check_dns_record(
        mac="00:00:00:00:11:05",
        client_fqdn="abc-client-2-2.four.example.com.",
        address="192.168.51.11",
        arpa="11.51.168.192.in-addr.arpa.",
        class_id="subnet1",
    )

    # client 6 get's en address from subnet 2 with different FQDN
    _get_address_and_check_dns_record(
        mac="00:00:00:00:11:06",
        client_fqdn="abc-client-3-3.four.example.com.",
        address="192.168.52.11",
        arpa="11.52.168.192.in-addr.arpa.",
        class_id="subnet2",
    )

    # let's wait for first address to expire, it should not remove DNS record that was created with second lease
    while time.time() - start_time < main_valid_lifetime + 2:
        pass

    _check_address_record(
        "abc-client-3-3.four.example.com.", "11.52.168.192.in-addr.arpa."
    )
    _check_fqdn_record("abc-client-3-3.four.example.com.", "192.168.52.11")

    rsp = send_cmd({"command": "config-get", "service": ["dhcp4"], "arguments": {}})
    if level == "global":
        assert rsp["arguments"]["Dhcp4"]["ddns-conflict-resolution-mode"] == "no-check-with-dhcid"
    elif level == "subnet":
        assert rsp["arguments"]["Dhcp4"]["shared-networks"][0]["ddns-conflict-resolution-mode"] == "check-with-dhcid"
        for i in range(3):
            assert rsp["arguments"]["Dhcp4"]["shared-networks"][0]["subnet4"][i]["ddns-conflict-resolution-mode"] == "no-check-with-dhcid"
    elif level == "shared-network":
        assert rsp["arguments"]["Dhcp4"]["ddns-conflict-resolution-mode"] == "check-with-dhcid"
        assert rsp["arguments"]["Dhcp4"]["shared-networks"][0]["ddns-conflict-resolution-mode"] == "no-check-with-dhcid"


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.ddns_conflict_resolution
@pytest.mark.parametrize("level", ["global", "subnet", "shared-network"])
@pytest.mark.parametrize(
    "conflict", ["check-exists-with-dhcid", "no-check-without-dhcid"]
)
def test_ddns4_conflict_resolution(level, conflict):
    """
    Test ddns-conflict-resolution-mode settings: "check-exists-with-dhcid" and "no-check-without-dhcid" at 3 levels.

    check-exists-with-dhcid - Existing DNS entries may only be overwritten if they have a DHCID record.
    The DHCID record need not match the client's DHCID. This mode provides a way to protect static
    DNS entries (those that do not have a DHCID record) while allowing dynamic entries (those that do have a DHCID record)
    to be overwritten by any client.

    no-check-without-dhcid - Existing DNS entries may be overwritten by any client.
    New entries will not include DHCID records.
    """

    # basic config
    main_valid_lifetime = 10
    misc.test_setup()
    # subnets
    srv_control.config_srv_subnet("192.168.50.0/24", "192.168.50.10-192.168.50.25", id=1)
    srv_control.config_srv_another_subnet_no_interface(
        "192.168.51.0/24", "192.168.51.10-192.168.51.15", id=2
    )
    srv_control.config_srv_another_subnet_no_interface(
        "192.168.52.0/24", "192.168.52.10-192.168.52.15", id=3
    )
    # subnet settings:
    if level == "subnet":
        # it has to be set before shared network is configured
        for i in range(3):
            srv_control.set_conf_parameter_subnet(
                "ddns-conflict-resolution-mode", conflict, i
            )

    basic_configuration(4, main_valid_lifetime)

    # ddns-conflict-resolution-mode settings
    if level == "global":
        srv_control.set_conf_parameter_global("ddns-conflict-resolution-mode", conflict)
    elif level == "subnet":
        # let's set globally and in shared-network different setting
        srv_control.set_conf_parameter_global(
            "ddns-conflict-resolution-mode", "check-with-dhcid"
        )
        srv_control.set_conf_parameter_shared_subnet(
            "ddns-conflict-resolution-mode", "check-with-dhcid", 0
        )
    elif level == "shared-network":
        # let's set globally different setting
        srv_control.set_conf_parameter_global(
            "ddns-conflict-resolution-mode", "check-with-dhcid"
        )
        srv_control.set_conf_parameter_shared_subnet(
            "ddns-conflict-resolution-mode", conflict, 0
        )

    srv_control.build_and_send_config_files()
    srv_control.start_srv("DHCP", "started")

    srv_control.use_dns_set_number(32)
    srv_control.start_srv("DNS", "started")

    # let's get some records
    for i in range(4):
        _get_address_and_check_dns_record(
            mac=f"00:00:00:00:11:0{i}",
            client_fqdn=f"abc-client-{i}.four.example.com.",
            address=f"192.168.50.1{i}",
            arpa=f"1{i}.50.168.192.in-addr.arpa.",
            class_id="subnet0",
        )

    # overwrite them:
    for i in range(4):
        _get_address_and_check_dns_record(
            mac=f"00:00:00:00:22:0{i}",
            client_fqdn=f"abc-client-{i}.four.example.com.",
            address=f"192.168.50.1{i+4}",
            arpa=f"1{i+4}.50.168.192.in-addr.arpa.",
            class_id="subnet0",
        )

    # now check if we can overwrite static record
    _get_address(
        "00:00:00:00:33:03",
        fqdn="dns.four.example.com.",
        address="192.168.51.10",
        class_id="subnet1",
    )

    # main diffeerece between check-exists-with-dhcid and no-check-without-dhcid is that in first case
    # we can overwrite only records with DHCID, in second case we can overwrite any record, even static one
    _check_fqdn_record(
        "dns.four.example.com.",
        address="172.16.1.1"
        if conflict == "check-exists-with-dhcid"
        else "192.168.51.10",
    )

    rsp = send_cmd({"command": "config-get", "service": ["dhcp4"], "arguments": {}})
    if level == "global":
        assert rsp["arguments"]["Dhcp4"]["ddns-conflict-resolution-mode"] == conflict
    elif level == "subnet":
        assert rsp["arguments"]["Dhcp4"]["shared-networks"][0]["ddns-conflict-resolution-mode"] == "check-with-dhcid"
        for i in range(3):
            assert rsp["arguments"]["Dhcp4"]["shared-networks"][0]["subnet4"][i]["ddns-conflict-resolution-mode"] == conflict
    elif level == "shared-network":
        assert rsp["arguments"]["Dhcp4"]["ddns-conflict-resolution-mode"] == "check-with-dhcid"
        assert rsp["arguments"]["Dhcp4"]["shared-networks"][0]["ddns-conflict-resolution-mode"] == conflict


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.ddns_conflict_resolution
@pytest.mark.parametrize("level", ["global", "subnet", "shared-network"])
def test_ddns6_conflict_resolution_check_with_dhcid(level):
    """
    Test ddns-conflict-resolution-mode set to "check-with-dhcid" at 3 levels.
    https://datatracker.ietf.org/doc/html/rfc4703
    Each new DNS entry is checked against existing entries. If DHCID maches, entry is updated, if not, entry is not updated.
    If record was updated expiration of previous address should not remove DNS record.

    If the same client get's address from different subnet, it should be able to update DNS entry.
    """
    # basic config
    main_valid_lifetime = 25
    misc.test_setup()
    # subnets
    srv_control.config_srv_subnet("2001:db8:a::/64", "2001:db8:a::10-2001:db8:a::20", id=1)
    srv_control.config_srv_another_subnet_no_interface(
        "2001:db8:b::/64", "2001:db8:b::10-2001:db8:b::20", id=2
    )
    srv_control.config_srv_another_subnet_no_interface(
        "2001:db8:c::/64", "2001:db8:c::10-2001:db8:c::20", id=3
    )
    # subnet settings:
    if level == "subnet":
        # it has to be set before shared network is configured
        for i in range(3):
            srv_control.set_conf_parameter_subnet(
                "ddns-conflict-resolution-mode", "check-with-dhcid", i
            )
    basic_configuration(6, main_valid_lifetime)

    # ddns-conflict-resolution-mode settings
    if level == "global":
        srv_control.set_conf_parameter_global(
            "ddns-conflict-resolution-mode", "check-with-dhcid"
        )
    elif level == "subnet":
        # let's set globally and in shared-network different setting
        srv_control.set_conf_parameter_global(
            "ddns-conflict-resolution-mode", "no-check-with-dhcid"
        )
        srv_control.set_conf_parameter_shared_subnet(
            "ddns-conflict-resolution-mode", "no-check-with-dhcid", 0
        )
    elif level == "shared-network":
        # let's set globally different setting
        srv_control.set_conf_parameter_global(
            "ddns-conflict-resolution-mode", "no-check-with-dhcid"
        )
        srv_control.set_conf_parameter_shared_subnet(
            "ddns-conflict-resolution-mode", "check-with-dhcid", 0
        )

    srv_control.build_and_send_config_files()
    srv_control.start_srv("DHCP", "started")

    srv_control.use_dns_set_number(31)
    srv_control.start_srv("DNS", "started")

    # overwrite existing records with the same DHCID

    # client 1 get's en address from subnet 0 (first client will be used to test expiration)
    start_time = time.time()
    _get_address_and_check_dns_record(
        mac="00:03:00:01:00:00:00:00:11:01",
        client_fqdn="abc-client-1.six.example.com.",
        address="2001:db8:a::10",
        arpa="0.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.a.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
        class_id="subnet0",
        version=6,
    )

    # client 1 get's en address from subnet 2, DNS record should be updated (longer lifetime)
    _get_address_and_check_dns_record(
        mac="00:03:00:01:00:00:00:00:11:01",
        client_fqdn="abc-client-1.six.example.com.",
        address="2001:db8:c::10",
        arpa="0.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.c.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
        class_id="subnet2",
        version=6,
    )

    # client 2 get's en address from subnet 0
    _get_address_and_check_dns_record(
        mac="00:03:00:01:00:00:00:00:11:02",
        client_fqdn="abc-client-2.six.example.com.",
        address="2001:db8:a::11",
        arpa="1.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.a.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
        class_id="subnet0",
        version=6,
    )

    # client 2 get's en address from subnet 1, DNS record should be updated
    _get_address_and_check_dns_record(
        mac="00:03:00:01:00:00:00:00:11:02",
        client_fqdn="abc-client-2.six.example.com.",
        address="2001:db8:b::10",
        arpa="0.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.b.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
        class_id="subnet1",
        version=6,
    )

    # client 3 get's en address from subnet 1, DNS record should be created
    _get_address_and_check_dns_record(
        mac="00:03:00:01:00:00:00:00:11:03",
        client_fqdn="abc-client-3.six.example.com.",
        address="2001:db8:b::11",
        arpa="1.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.b.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
        class_id="subnet1",
        version=6,
    )

    # client 3 gets an address from subnet 0, tries to use already assigned fqdn, should not update DNS record
    _get_address6(
        "00:03:00:01:00:00:00:00:11:06",
        fqdn="abc-client-1.six.example.com.",
        address="2001:db8:a::12",
        class_id="subnet0",
    )
    _check_fqdn_record(
        "abc-client-1.six.example.com.", address="2001:db8:c::10", version=6
    )  # old address!
    _check_address_record(
        "abc-client-1.six.example.com.",
        "0.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.c.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
    )

    # client 4 gets an address from subnet 1, tries to use already assigned fqdn, should not update DNS record
    _get_address6(
        "00:03:00:01:00:00:00:00:11:04",
        fqdn="abc-client-3.six.example.com.",
        address="2001:db8:b::12",
        class_id="subnet1",
    )
    _check_fqdn_record(
        "abc-client-3.six.example.com.", address="2001:db8:b::11", version=6
    )  # old address!
    _check_address_record(
        "abc-client-3.six.example.com.",
        "1.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.b.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
    )

    # client 2 returns with different FQDN, should update DNS record
    _get_address6(
        "00:03:00:01:00:00:00:00:11:02",
        fqdn="abc-client-2-2.six.example.com.",
        address="2001:db8:b::10",
        class_id="subnet1",
    )
    _check_fqdn_record(
        "abc-client-2-2.six.example.com.", address="2001:db8:b::10", version=6
    )
    _check_address_record(
        "abc-client-2-2.six.example.com.",
        "0.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.b.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
    )

    # let's wait for first address to expire, it should not remove DNS record that was created with second lease
    while time.time() - start_time < main_valid_lifetime + 2:
        pass

    _check_address_record(
        "abc-client-2-2.six.example.com.",
        "0.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.b.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
    )
    _check_fqdn_record("abc-client-2-2.six.example.com.", "2001:db8:b::10", version=6)

    # now check if we can overwrite static record
    _get_address6(
        "00:03:00:01:00:00:00:00:33:03",
        fqdn="dns6-1.six.example.com.",
        address="2001:db8:c::11",
        class_id="subnet2",
    )

    # main diffeerece between check-exists-with-dhcid and no-check-without-dhcid is that in first case
    # we can overwrite only records with DHCID, in second case we can overwrite any record, even static one
    _check_fqdn_record("dns6-1.six.example.com.", address="2001:db8:a::1", version=6)

    rsp = send_cmd({"command": "config-get", "service": ["dhcp6"], "arguments": {}})
    if level == "global":
        assert rsp["arguments"]["Dhcp6"]["ddns-conflict-resolution-mode"] == "check-with-dhcid"
    elif level == "subnet":
        assert rsp["arguments"]["Dhcp6"]["shared-networks"][0]["ddns-conflict-resolution-mode"] == "no-check-with-dhcid"
        for i in range(3):
            assert rsp["arguments"]["Dhcp6"]["shared-networks"][0]["subnet6"][i]["ddns-conflict-resolution-mode"] == "check-with-dhcid"
    elif level == "shared-network":
        assert rsp["arguments"]["Dhcp6"]["ddns-conflict-resolution-mode"] == "no-check-with-dhcid"
        assert rsp["arguments"]["Dhcp6"]["shared-networks"][0]["ddns-conflict-resolution-mode"] == "check-with-dhcid"


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.ddns_conflict_resolution
@pytest.mark.parametrize("level", ["global", "subnet", "shared-network"])
def test_ddns6_conflict_resolution_no_check_with_dhcid(level):
    """
    Test ddns-conflict-resolution-mode set to "no-check-with-dhcid" at 3 levels.

    Existing DNS entries may be overwritten by any client, whether or not those entries include a DHCID record.
    """

    # basic config
    main_valid_lifetime = 50
    misc.test_setup()
    srv_control.config_srv_subnet("2001:db8:a::/64", "2001:db8:a::10-2001:db8:a::20", id=1)
    srv_control.config_srv_another_subnet_no_interface(
        "2001:db8:b::/64", "2001:db8:b::10-2001:db8:b::20", id=2
    )
    srv_control.config_srv_another_subnet_no_interface(
        "2001:db8:c::/64", "2001:db8:c::10-2001:db8:c::20", id=3
    )
    # subnet settings:
    if level == "subnet":
        # it has to be set before shared network is configured
        for i in range(3):
            srv_control.set_conf_parameter_subnet(
                "ddns-conflict-resolution-mode", "no-check-with-dhcid", i
            )

    basic_configuration(6, main_valid_lifetime)

    # ddns-conflict-resolution-mode settings
    if level == "global":
        srv_control.set_conf_parameter_global(
            "ddns-conflict-resolution-mode", "no-check-with-dhcid"
        )
    elif level == "subnet":
        # let's set globally and in shared-network different setting
        srv_control.set_conf_parameter_global(
            "ddns-conflict-resolution-mode", "check-with-dhcid"
        )
        srv_control.set_conf_parameter_shared_subnet(
            "ddns-conflict-resolution-mode", "check-with-dhcid", 0
        )
    elif level == "shared-network":
        # let's set globally different setting
        srv_control.set_conf_parameter_global(
            "ddns-conflict-resolution-mode", "check-with-dhcid"
        )
        srv_control.set_conf_parameter_shared_subnet(
            "ddns-conflict-resolution-mode", "no-check-with-dhcid", 0
        )

    srv_control.build_and_send_config_files()
    srv_control.start_srv("DHCP", "started")

    srv_control.use_dns_set_number(31)
    srv_control.start_srv("DNS", "started")

    # client 1 get's en address from subnet 0
    _get_address_and_check_dns_record(
        mac="00:03:00:01:00:00:00:00:00:11:01",
        client_fqdn="abc-client-1.six.example.com.",
        address="2001:db8:a::10",
        arpa="0.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.a.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
        class_id="subnet0",
        version=6,
    )

    # client 2 get's en address from subnet 1
    _get_address_and_check_dns_record(
        mac="00:03:00:01:00:00:00:00:11:02",
        client_fqdn="abc-client-2.six.example.com.",
        address="2001:db8:b::10",
        arpa="0.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.b.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
        class_id="subnet1",
        version=6,
    )

    # client 3 get's en address from subnet 2
    _get_address_and_check_dns_record(
        mac="00:03:00:01:00:03:00:01:00:00:00:00:11:03",
        client_fqdn="abc-client-3.six.example.com.",
        address="2001:db8:c::10",
        arpa="0.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.c.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
        class_id="subnet2",
        version=6,
    )

    # let's overwrite now existing records
    # client 4 get's en address from subnet 0 with FQDN assigned to client 1
    _get_address_and_check_dns_record(
        mac="00:03:00:01:00:00:00:00:11:04",
        client_fqdn="abc-client-1.six.example.com.",
        address="2001:db8:a::11",
        arpa="1.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.a.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
        class_id="subnet0",
        version=6,
    )

    # client 5 get's en address from subnet 1 with FQDN assigned to client 2
    _get_address_and_check_dns_record(
        mac="00:03:00:01:00:00:00:00:11:05",
        client_fqdn="abc-client-2.six.example.com.",
        address="2001:db8:b::11",
        arpa="1.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.b.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
        class_id="subnet1",
        version=6,
    )

    # client 6 get's en address from subnet 2 with FQDN assigned to client 3
    _get_address_and_check_dns_record(
        mac="00:03:00:01:00:00:00:00:11:06",
        client_fqdn="abc-client-3.six.example.com.",
        address="2001:db8:c::11",
        arpa="1.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.c.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
        class_id="subnet2",
        version=6,
    )
    start_time = time.time()
    # let's overwrite now existing records
    # client 4 get's en address from subnet 0 with different FQDN
    _get_address_and_check_dns_record(
        mac="00:03:00:01:00:00:00:00:11:04",
        client_fqdn="abc-client-1-1.six.example.com.",
        address="2001:db8:a::11",
        arpa="1.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.a.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
        class_id="subnet0",
        version=6,
    )

    # client 5 get's en address from subnet 1 with different FQDN
    _get_address_and_check_dns_record(
        mac="00:03:00:01:00:00:00:00:11:05",
        client_fqdn="abc-client-2-2.six.example.com.",
        address="2001:db8:b::11",
        arpa="1.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.b.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
        class_id="subnet1",
        version=6,
    )

    # client 6 get's en address from subnet 2 with different FQDN
    _get_address_and_check_dns_record(
        mac="00:03:00:01:00:00:00:00:11:06",
        client_fqdn="abc-client-3-3.six.example.com.",
        address="2001:db8:c::11",
        arpa="1.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.c.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
        class_id="subnet2",
        version=6,
    )

    # let's wait for first address to expire, it should not remove DNS record that was created with second lease
    while time.time() - start_time < main_valid_lifetime + 2:
        pass

    _check_address_record(
        "abc-client-3-3.six.example.com.",
        "1.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.c.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
    )
    _check_fqdn_record("abc-client-3-3.six.example.com.", "2001:db8:c::11", version=6)

    # now check if we can overwrite static record
    _get_address6(
        "00:03:00:01:00:00:00:00:33:03",
        fqdn="dns6-1.six.example.com.",
        address="2001:db8:c::12",
        class_id="subnet2",
    )

    # main diffeerece between check-exists-with-dhcid and no-check-without-dhcid is that in first case
    # we can overwrite only records with DHCID, in second case we can overwrite any record, even static one
    _check_fqdn_record("dns6-1.six.example.com.", address="2001:db8:c::12", version=6)

    rsp = send_cmd({"command": "config-get", "service": ["dhcp6"], "arguments": {}})
    if level == "global":
        assert rsp["arguments"]["Dhcp6"]["ddns-conflict-resolution-mode"] == "no-check-with-dhcid"
    elif level == "subnet":
        assert rsp["arguments"]["Dhcp6"]["shared-networks"][0]["ddns-conflict-resolution-mode"] == "check-with-dhcid"
        for i in range(3):
            assert rsp["arguments"]["Dhcp6"]["shared-networks"][0]["subnet6"][i]["ddns-conflict-resolution-mode"] == "no-check-with-dhcid"
    elif level == "shared-network":
        assert rsp["arguments"]["Dhcp6"]["ddns-conflict-resolution-mode"] == "check-with-dhcid"
        assert rsp["arguments"]["Dhcp6"]["shared-networks"][0]["ddns-conflict-resolution-mode"] == "no-check-with-dhcid"


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.ddns_conflict_resolution
@pytest.mark.parametrize("level", ["global", "subnet", "shared-network"])
@pytest.mark.parametrize(
    "conflict", ["check-exists-with-dhcid", "no-check-without-dhcid"]
)
def test_ddns6_conflict_resolution(level, conflict):
    """
    Test ddns-conflict-resolution-mode settings: "check-exists-with-dhcid" and "no-check-without-dhcid" at 3 levels.

    check-exists-with-dhcid - Existing DNS entries may only be overwritten if they have a DHCID record.
    The DHCID record need not match the client's DHCID. This mode provides a way to protect static
    DNS entries (those that do not have a DHCID record) while allowing dynamic entries (those that do have a DHCID record)
    to be overwritten by any client.

    no-check-without-dhcid - Existing DNS entries may be overwritten by any client.
    New entries will not include DHCID records.
    """

    # basic config
    main_valid_lifetime = 10
    misc.test_setup()
    # subnets
    srv_control.config_srv_subnet("2001:db8:a::/64", "2001:db8:a::10-2001:db8:a::20", id=1)
    srv_control.config_srv_another_subnet_no_interface(
        "2001:db8:b::/64", "2001:db8:b::10-2001:db8:b::20", id=2
    )
    srv_control.config_srv_another_subnet_no_interface(
        "2001:db8:c::/64", "2001:db8:c::10-2001:db8:c::20", id=3
    )
    # subnet settings:
    if level == "subnet":
        # it has to be set before shared network is configured
        for i in range(3):
            srv_control.set_conf_parameter_subnet(
                "ddns-conflict-resolution-mode", conflict, i
            )

    basic_configuration(6, main_valid_lifetime)

    # ddns-conflict-resolution-mode settings
    if level == "global":
        srv_control.set_conf_parameter_global("ddns-conflict-resolution-mode", conflict)
    elif level == "subnet":
        # let's set globally and in shared-network different setting
        srv_control.set_conf_parameter_global(
            "ddns-conflict-resolution-mode", "check-with-dhcid"
        )
        srv_control.set_conf_parameter_shared_subnet(
            "ddns-conflict-resolution-mode", "check-with-dhcid", 0
        )
    elif level == "shared-network":
        # let's set globally different setting
        srv_control.set_conf_parameter_global(
            "ddns-conflict-resolution-mode", "check-with-dhcid"
        )
        srv_control.set_conf_parameter_shared_subnet(
            "ddns-conflict-resolution-mode", conflict, 0
        )

    srv_control.build_and_send_config_files()
    srv_control.start_srv("DHCP", "started")

    srv_control.use_dns_set_number(31)
    srv_control.start_srv("DNS", "started")

    # let's get some records
    for i in range(4):
        _get_address_and_check_dns_record(
            version=6,
            mac=f"00:03:00:01:00:00:00:00:11:0{i}",
            client_fqdn=f"abc-client-{i}.six.example.com.",
            address=f"2001:db8:a::1{i}",
            arpa=f"{i}.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.a.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
            class_id="subnet0",
        )

    # overwrite them:
    for i in range(4):
        _get_address_and_check_dns_record(
            version=6,
            mac=f"00:03:00:01:00:00:00:00:22:0{i}",
            client_fqdn=f"abc-client-{i}.six.example.com.",
            address=f"2001:db8:a::1{i+4}",
            arpa=f"{i+4}.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.a.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
            class_id="subnet0",
        )

    # now check if we can overwrite static record
    _get_address6(
        "00:03:00:01:00:00:00:00:33:03",
        fqdn="dns6-1.six.example.com.",
        address="2001:db8:c::10",
        class_id="subnet2",
    )

    # main diffeerece between check-exists-with-dhcid and no-check-without-dhcid is that in first case
    # we can overwrite only records with DHCID, in second case we can overwrite any record, even static one
    _check_fqdn_record(
        "dns6-1.six.example.com.",
        address="2001:db8:a::1"
        if conflict == "check-exists-with-dhcid"
        else "2001:db8:c::10",
        version=6,
    )

    rsp = send_cmd({"command": "config-get", "service": ["dhcp6"], "arguments": {}})
    if level == "global":
        assert rsp["arguments"]["Dhcp6"]["ddns-conflict-resolution-mode"] == conflict
    elif level == "subnet":
        assert rsp["arguments"]["Dhcp6"]["shared-networks"][0]["ddns-conflict-resolution-mode"] == "check-with-dhcid"
        for i in range(3):
            assert rsp["arguments"]["Dhcp6"]["shared-networks"][0]["subnet6"][i]["ddns-conflict-resolution-mode"] == conflict
    elif level == "shared-network":
        assert rsp["arguments"]["Dhcp6"]["ddns-conflict-resolution-mode"] == "check-with-dhcid"
        assert rsp["arguments"]["Dhcp6"]["shared-networks"][0]["ddns-conflict-resolution-mode"] == conflict


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.ddns_conflict_resolution
@pytest.mark.parametrize("level", ["global", "subnet", "shared-network"])
def test_ddns6_conflict_resolution_simple_scenario(level):
    """
    Test ddns-conflict-resolution-mode set to "check-with-dhcid" at 3 levels.
    https://datatracker.ietf.org/doc/html/rfc4703
    Each new DNS entry is checked against existing entries. If DHCID maches, entry is updated, if not, entry is not updated.
    If record was updated expiration of previous address should not remove DNS record.

    """
    # basic config
    main_valid_lifetime = 50
    misc.test_setup()
    # subnets
    srv_control.config_srv_subnet("2001:db8:a::/64", "2001:db8:a::10-2001:db8:a::20", id=1)
    srv_control.config_srv_another_subnet_no_interface(
        "2001:db8:b::/64", "2001:db8:b::10-2001:db8:b::20", id=2
    )
    srv_control.config_srv_another_subnet_no_interface(
        "2001:db8:c::/64", "2001:db8:c::10-2001:db8:c::20", id=3
    )
    # subnet settings:
    if level == "subnet":
        # it has to be set before shared network is configured
        for i in range(3):
            srv_control.set_conf_parameter_subnet(
                "ddns-conflict-resolution-mode", "check-with-dhcid", i
            )
    basic_configuration(6, main_valid_lifetime)

    # ddns-conflict-resolution-mode settings
    if level == "global":
        srv_control.set_conf_parameter_global(
            "ddns-conflict-resolution-mode", "check-with-dhcid"
        )
    elif level == "subnet":
        # let's set globally and in shared-network different setting
        srv_control.set_conf_parameter_global(
            "ddns-conflict-resolution-mode", "no-check-with-dhcid"
        )
        srv_control.set_conf_parameter_shared_subnet(
            "ddns-conflict-resolution-mode", "no-check-with-dhcid", 0
        )
    elif level == "shared-network":
        # let's set globally different setting
        srv_control.set_conf_parameter_global(
            "ddns-conflict-resolution-mode", "no-check-with-dhcid"
        )
        srv_control.set_conf_parameter_shared_subnet(
            "ddns-conflict-resolution-mode", "check-with-dhcid", 0
        )

    srv_control.build_and_send_config_files()
    srv_control.start_srv("DHCP", "started")

    srv_control.use_dns_set_number(31)
    srv_control.start_srv("DNS", "started")

    # client 1 get's en address from subnet 0
    _get_address_and_check_dns_record(
        mac="00:03:00:01:00:00:00:00:11:01",
        client_fqdn="abc-client-1.six.example.com.",
        address="2001:db8:a::10",
        arpa="0.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.a.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
        class_id="subnet0",
        version=6,
    )

    # client 2 gets an address from subnet 1, tries to use already assigned fqdn, should not update DNS record
    _get_address6(
        "00:03:00:01:00:00:00:00:11:03",
        fqdn="abc-client-1.six.example.com.",
        address="2001:db8:b::10",
        class_id="subnet1",
    )
    _check_fqdn_record(
        "abc-client-1.six.example.com.", address="2001:db8:a::10", version=6
    )  # old address!
    _check_address_record(
        "abc-client-1.six.example.com.",
        "0.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.a.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
    )

    # client 3 get's en address from subnet 1
    _get_address_and_check_dns_record(
        mac="00:03:00:01:00:00:00:00:11:05",
        client_fqdn="abc-client-2.six.example.com.",
        address="2001:db8:b::11",
        arpa="1.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.b.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
        class_id="subnet1",
        version=6,
    )

    # client 4 gets an address from subnet 2, tries to use already assigned fqdn, should not update DNS record
    _get_address6(
        "00:03:00:01:00:00:00:00:11:03",
        fqdn="abc-client-2.six.example.com.",
        address="2001:db8:c::10",
        class_id="subnet2",
    )
    _check_fqdn_record(
        "abc-client-2.six.example.com.", address="2001:db8:b::11", version=6
    )  # old address!
    _check_address_record(
        "abc-client-2.six.example.com.",
        "1.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.b.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
    )

    # client 3 get's en address from subnet 2
    _get_address_and_check_dns_record(
        mac="00:03:00:01:00:00:00:00:11:06",
        client_fqdn="abc-client-3.six.example.com.",
        address="2001:db8:c::11",
        arpa="1.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.c.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
        class_id="subnet2",
        version=6,
    )

    # client 4 gets an address from subnet 2, tries to use already assigned fqdn, should not update DNS record
    _get_address6(
        "00:03:00:01:00:00:00:00:11:07",
        fqdn="abc-client-3.six.example.com.",
        address="2001:db8:c::12",
        class_id="subnet2",
    )

    _check_fqdn_record(
        "abc-client-3.six.example.com.",
        address="2001:db8:c::11",  # old address!
        version=6,
    )
    _check_address_record(
        "abc-client-3.six.example.com.",
        "1.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.c.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
    )

    # now check if we can overwrite static record
    _get_address6(
        "00:03:00:01:00:00:00:00:33:03",
        fqdn="dns6-1.six.example.com.",
        address="2001:db8:c::13",
        class_id="subnet2",
    )

    # main diffeerece between check-exists-with-dhcid and no-check-without-dhcid is that in first case
    # we can overwrite only records with DHCID, in second case we can overwrite any record, even static one
    _check_fqdn_record("dns6-1.six.example.com.", address="2001:db8:a::1", version=6)

    # now let's repeat but with clients inside the same subnet
    _get_address_and_check_dns_record(
        mac="00:03:00:01:00:00:00:33:11:0A",
        client_fqdn="client-a.six.example.com.",
        address="2001:db8:c::14",
        arpa="4.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.c.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
        class_id="subnet2",
        version=6,
    )

    # next client in the same subnet, should not update DNS record
    _get_address6(
        "00:03:00:01:00:00:00:33:11:0B",
        fqdn="client-a.six.example.com.",
        address="2001:db8:c::15",
        class_id="subnet2",
    )
    _check_fqdn_record(
        "client-a.six.example.com.", address="2001:db8:c::14", version=6
    )  # old address!
    _check_address_record(
        "client-a.six.example.com.",
        "4.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.c.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
    )

    _get_address6(
        "00:03:00:01:00:00:00:33:11:0C",
        fqdn="client-a.six.example.com.",
        address="2001:db8:c::16",
        class_id="subnet2",
    )
    _check_fqdn_record(
        "client-a.six.example.com.", address="2001:db8:c::14", version=6
    )  # old address!
    _check_address_record(
        "client-a.six.example.com.",
        "4.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.c.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.",
    )
