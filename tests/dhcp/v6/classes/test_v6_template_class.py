# Copyright (C) 2023 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""DHCPv6 Client Classification - template classes"""

# pylint: disable=line-too-long

import pytest

from src import misc
from src import srv_control
from src import srv_msg

from src.forge_cfg import world
from src.protosupport.multi_protocol_functions import get_line_count_in_log


def _get_lease(duid: str = "00:03:00:01:01:02:0c:03:0a:00", vendor: int = False, drop: bool = False):

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'ia_id', 1)
    srv_msg.client_does_include('Client', 'IA-NA')
    if vendor:
        srv_msg.client_sets_value('Client', 'enterprisenum', vendor)
        srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    if drop:
        srv_msg.send_wait_for_message('MUST', None, expect_response=False)
        return

    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.client_does_include('Client', 'IA-NA')

    if vendor:
        srv_msg.client_sets_value('Client', 'enterprisenum', vendor)
        srv_msg.client_does_include('Client', 'vendor-class')

    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)

    srv_msg.get_all_leases()


@pytest.mark.v6
@pytest.mark.classification
def test_v6_spawn_class():
    """
    :return:
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::10')

    classes = [
            {
                # SPAWN_my_vendor_client_id_<first 3 octets of mac address from duid>
                # let's tak to the account two types of duid DUID_LL and DUID_LLT that have different length and mac
                # address has different position. In DUID_LL we will take 3 octets starting from 5th,
                # in DUID_LLT it will be 3 octets starting from 8th. (Rest of duid types are not in scope of this test)
                "name": "client_id_type",
                "template-test": "ifelse(substring(option[1].hex, 0, 4) == 0x00030001, hexstring(substring(option[1].hex, 4, 3), ':'), hexstring(substring(option[1].hex, 8, 3), ':'))",
            },
            {
                # SPAWN_client_vendor_<enterprise number>
                "name": "client_vendor",
                "template-test": "int32totext(vendor-class.enterprise)"
            }
        ]

    world.dhcp_cfg["client-classes"] = classes
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    _get_lease('00:01:00:01:52:7b:a8:f0:08:00:27:58:f1:e8')
    assert 2 == get_line_count_in_log('client packet belongs to an unconfigured class: SPAWN_client_id_type_08:00:27')
    assert 2 == get_line_count_in_log('client packet has been assigned to the following classes: ALL, client_id_type, SPAWN_client_id_type_08:00:27, UNKNOWN')

    _get_lease('00:03:00:01:1f:2f:3f:ff:ff:01', vendor=1100)
    assert 2 == get_line_count_in_log('client packet belongs to an unconfigured class: SPAWN_client_id_type_1f:2f:3f')
    assert 2 == get_line_count_in_log('client packet has been assigned to the following classes: ALL, client_id_type, SPAWN_client_id_type_1f:2f:3f, client_vendor, SPAWN_client_vendor_1100, UNKNOWN')

    _get_lease('00:03:00:01:1f:2f:3f:fa:fb:01', vendor=1111)
    assert 4 == get_line_count_in_log('client packet belongs to an unconfigured class: SPAWN_client_id_type_1f:2f:3f')
    assert 2 == get_line_count_in_log('client packet has been assigned to the following classes: ALL, client_id_type, SPAWN_client_id_type_1f:2f:3f, client_vendor, SPAWN_client_vendor_1111, UNKNOWN')


@pytest.mark.v6
@pytest.mark.classification
def test_v6_spawn_class_as_subnet_guard():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::10')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:2::/64', '2001:db8:2::1-2001:db8:2::10')

    classes = [
        {
            # SPAWN_my_vendor_client_id_<first 3 octets of mac address from duid>
            "name": "client_id_type",
            "template-test": "ifelse(substring(option[1].hex, 0, 4) == 0x00030001, hexstring(substring(option[1].hex, 4, 3), ':'), hexstring(substring(option[1].hex, 8, 3), ':'))",
        },
        {
            # SPAWN_client_vendor_<enterprise number>
            "name": "client_vendor",
            "template-test": "int32totext(vendor-class.enterprise)"
        },
        {
            "name": "SPAWN_client_vendor_1234",
            "option-data": [
                {
                    "data": "123",
                    "name": "preference",
                    "always-send": True
                }
            ]
        },
        {
            "name": "SPAWN_client_id_type_11:22:33",
        },
        {
            "name": "DROP",
            "test": "member('SPAWN_client_id_type_11:22:33')"
        }
    ]

    srv_control.config_client_classification(0, 'SPAWN_client_vendor_1234')
    world.dhcp_cfg["client-classes"] = classes
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # address will be assigned from subnet 1 (require SPAWN_client_vendor_1234 class)
    _get_lease('00:03:00:01:1f:2f:3f:ff:ff:01', vendor=1234)
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 123)
    srv_msg.check_if_address_belongs_to_subnet('2001:db8:1::/64')

    # two clients should be dropped:
    _get_lease('00:03:00:01:11:22:33:ff:ff:01', vendor=1100, drop=True)
    assert 1 == get_line_count_in_log(
        "EVAL_DEBUG_MEMBER Checking membership of 'SPAWN_client_id_type_11:22:33', pushing result 'true'")
    _get_lease('00:01:00:01:52:7b:a8:f0:11:22:33:58:f1:e8', drop=True)
    assert 2 == get_line_count_in_log(
        "EVAL_DEBUG_MEMBER Checking membership of 'SPAWN_client_id_type_11:22:33', pushing result 'true'")

    # and one that will have address from second subnet and no preference option
    _get_lease('00:01:00:01:52:7b:a8:f0:08:00:27:58:f1:e8')
    srv_msg.response_check_include_option(7, expect_include=False)
    srv_msg.check_if_address_belongs_to_subnet('2001:db8:2::/64')


@pytest.mark.v6
@pytest.mark.classification
def test_v6_template_class_as_subnet_guard():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::10')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:2::/64', '2001:db8:2::1-2001:db8:2::10')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:3::/64', '2001:db8:3::1-2001:db8:3::10')

    classes = [
        {
            # SPAWN_my_vendor_client_id_<first 3 octets of mac address from duid>
            "name": "client_id_type",
            "template-test": "ifelse(substring(option[1].hex, 0, 4) == 0x00030001, hexstring(substring(option[1].hex, 4, 3), ':'), hexstring(substring(option[1].hex, 8, 3), ':'))",
        },
        {
            # SPAWN_client_vendor_<enterprise number>
            "name": "client_vendor",
            "template-test": "int32totext(vendor-class.enterprise)"
        },
        {
            "name": "SPAWN_client_id_type_11:22:33",
        },
        {
            "name": "DROP",
            "test": "member('SPAWN_client_id_type_11:22:33') and member('client_vendor')"
        }
    ]

    srv_control.config_client_classification(0, 'SPAWN_client_vendor_1234')
    srv_control.config_client_classification(1, 'client_vendor')
    srv_control.config_client_classification(2, 'client_id_type')
    world.dhcp_cfg["client-classes"] = classes
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # first let's assign address from last subnet (client id type a1:a2:a3 no vendor)
    _get_lease('00:03:00:01:a1:a2:a3:ff:ff:01')
    srv_msg.check_if_address_belongs_to_subnet('2001:db8:3::/64')

    # than let's assign address from second subnet (client id type a1:a2:a3 and vendor 123)
    _get_lease('00:03:00:01:a1:a2:a3:ff:ff:11', vendor=123)
    srv_msg.check_if_address_belongs_to_subnet('2001:db8:2::/64')

    # let's drop pkt (client id type 11:22:33 and vendor 123)
    _get_lease('00:03:00:01:11:22:33:ff:ff:11', vendor=123, drop=True)

    # at the end let's assign some addresses from subnet 1 (vendor 1234 required)
    _get_lease('00:03:00:01:a1:a2:a3:ff:22:11', vendor=1234)
    srv_msg.check_if_address_belongs_to_subnet('2001:db8:1::/64')
    _get_lease('00:01:00:01:52:7b:a8:f0:08:00:27:58:f1:e8', vendor=1234)
    srv_msg.check_if_address_belongs_to_subnet('2001:db8:1::/64')
