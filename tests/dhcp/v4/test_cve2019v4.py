# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""CVE-2019-6472 and -6473"""

# pylint: disable=line-too-long

import pytest

from src import srv_msg
from src import srv_control
from src import misc

from src.forge_cfg import world


def _get_offer():
    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '00010203040111')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')


@pytest.mark.v4
def test_cve_2019_6472():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    # correct message
    killer_message = b"\x01\x01\x06\x00\x00\x80\x64\x49\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x27\x6d\xee\x67\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x63\x82\x53\x63\x35\x01\x01"
    # too long client-id, kea have to drop it and survive, exactly 255
    killer_message += b"\x3d\xfe\x00" + 253 * b"\x12"
    killer_message += b"\xff"
    srv_msg.send_raw_message(raw_append=killer_message)

    srv_msg.send_wait_for_message('MUST', None, expect_response=False)

    # let's check if it's still alive
    _get_offer()


@pytest.mark.v4
def test_cve_2019_6473():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    # message straight from fuzzer, kea has to drop it and survive
    killer_message = b"\x01\x2c\x06\x00\x00\x00\x3d\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0b\x82\x01\xfc\x42\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x13\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\xe7\x03\x00\x00\x00\x00\xde\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfa\xff\xff\xff\x00\x00\x00\x00\xe0\xff\x00\x00\x00\x00\x00\x00\xde\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x20\x00\x00\x00\x00\xff\xff\x00\x00\x00\x09\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x7f\x00\x00\x00\x00\x00\xff\xee\x63\x82\x53\x63\x35\x01\x01\x3d\x07\x01\x00\x00\x00\x00\x00\x00\x19\x0c\x4e\x01\x00\x07\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x35\x01\x05\x3a\x04\x00\x00\x07\x08\x3b\x04\xff\x00\x00\x00\x09\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\xff\xff\xff\x7f\x00\x00\x00\x7f\x00\x00\x00\x00\x00\x00\x04\x63\x82\x53\x63\x35\x01\x01\x3d\x07\x01\x00\x00\x00\x00\x00\x00\x19\x0c\x4e\x01\x00\x07\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x35\x01\x05\x3a\x04\x00\x00\x07\x08\x3b\x04\x00\x00\x2e\x3b\x04\x00\x19\x2e\x00\x00\x00\x0a\x00\x12\x00\x00\x00\x00\x00\x00\x00\x0b\x82\x01\xfc\x42\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x35\x01\x05\x3a\x04\x00\x00\x07\x08\x3b\x04\x00\x00\x2e\x3b\x04\x00\x19\x2e\x56\x00\x00\x0a\x00\x12\x00\x00\x00\x00\x00\x00\x00\x0b\x82\x01\xfc\x42\x00\x00\x00\x00\x19\x0c\x4e\x01\x05\x3a\x04\xde\x00\x07\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x35\x01\x05\x3a\x07\x08\x3b\x04\x00\x00\x2e\x3b\x04\x00\x19\x2e\x56\x40\x00\x00\x00\x00\x00\x0a\x00\x12\x00\x00\x00\x00\x00\x19\x00\x0b\x82\x01\xfc\x42\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfc\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x35\x01\x05\xff\xff\x05\x00\x07\x08\x3b\x04\x00\x00\x2e\x3b\x04\x00\x19\x2e\x56\x00\x00\x00\x00\x00\x00\x0a\x05\x3a\x04\x00\x00\x07\x08\x3b\x04\x00\x00\x2e\x3b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xfe"
    srv_msg.send_raw_message(raw_append=killer_message)

    srv_msg.send_wait_for_message('MUST', None, expect_response=False)

    # check if kea is still alive
    _get_offer()


@pytest.mark.v4
def test_cve_2019_6473_hostname():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    # correct message
    killer_message = b"\x01\x01\x06\x00\x00\x80\x64\x49\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x27\x6d\xee\x67\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x63\x82\x53\x63\x35\x01\x01"
    # complete rubbish in hostname, should cause kea to drop message
    killer_message += b"\x0c\xff\xff\xff\x7f\x00\x00\x00\x7f\x00\x00\x00\x00\x00\x00\x04\x63\x82\x53\x63\x35\x01\x01\x3d\x07\x01\x00\x00\x00\x00\x00\x00\x19\x0c\x4e\x01\x00\x07\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x35\x01\x05\x3a\x04\x00\x00\x07\x08\x3b\x04\x00\x00\x2e\x3b\x04\x00\x19\x2e\x00\x00\x00\x0a\x00\x12\x00\x00\x00\x00\x00\x00\x00\x0b\x82\x01\xfc\x42\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x35\x01\x05\x3a\x04\x00\x00\x07\x08\x3b\x04\x00\x00\x2e\x3b\x04\x00\x19\x2e\x56\x00\x00\x0a\x00\x12\x00\x00\x00\x00\x00\x00\x00\x0b\x82\x01\xfc\x42\x00\x00\x00\x00\x19\x0c\x4e\x01\x05\x3a\x04\xde\x00\x07\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x35\x01\x05\x3a\x07\x08\x3b\x04\x00\x00\x2e\x3b\x04\x00\x19\x2e\x56\x40\x00\x00\x00\x00\x00\x0a\x00\x12\x00\x00\x00\x00\x00\x19\x00\x0b\x82\x01\xfc\x42\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfc\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x35\x01\x05\xff\xff\x05\x00\x07\x08\x3b\x04\x00\x00\x2e\x3b"
    killer_message += b"\xff"  # end option
    srv_msg.send_raw_message(raw_append=killer_message)

    srv_msg.send_wait_for_message('MUST', None, expect_response=False)

    # check if kea is still alive
    _get_offer()


@pytest.mark.v4
def test_cve_2019_6473_hostname_length_0():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    # correct message
    killer_message = b"\x01\x01\x06\x00\x00\x80\x64\x49\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x27\x6d\xee\x67\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x63\x82\x53\x63\x35\x01\x01"
    # incorrect hostname extended with zeros, kea should drop and survive
    killer_message += b"\x0c\x00\x00"
    killer_message += b"\xff"  # end option
    srv_msg.send_raw_message(raw_append=killer_message)

    srv_msg.send_wait_for_message('MUST', None, expect_response=False)

    _get_offer()


@pytest.mark.v4
def test_cve_2019_6473_hostname_over_255():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    # correct message
    killer_message = b"\x01\x01\x06\x00\x00\x80\x64\x49\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x27\x6d\xee\x67\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x63\x82\x53\x63\x35\x01\x01"
    # incorrect hostname extended with zeros, kea should drop and survive
    killer_message += b"\x0c\xff\xff\xff\x7f\x00\x00\x00\x7f\x00\x00\x00\x00\x00\x00\x04\x63\x82\x53\x63\x35\x01\x01\x3d\x07\x01\x00\x00\x00\x00\x00\x00\x19\x0c\x4e\x01\x00\x07\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x35\x01\x05\x3a\x04\x00\x00\x07\x08\x3b\x04\x00\x00\x2e\x3b\x04\x00\x19\x2e\x00\x00\x00\x0a\x00\x12\x00\x00\x00\x00\x00\x00\x00\x0b\x82\x01\xfc\x42\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x35\x01\x05\x3a\x04\x00\x00\x07\x08\x3b\x04\x00\x00\x2e\x3b\x04\x00\x19\x2e\x56\x00\x00\x0a\x00\x12\x00\x00\x00\x00\x00\x00\x00\x0b\x82\x01\xfc\x42\x00\x00\x00\x00\x19\x0c\x4e\x01\x05\x3a\x04\xde\x00\x07\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x35\x01\x05\x3a\x07\x08\x3b\x04\x00\x00\x2e\x3b\x04\x00\x19\x2e\x56\x40\x00\x00\x00\x00\x00\x0a\x00\x12\x00\x00\x00\x00\x00\x19\x00\x0b\x82\x01\xfc\x42\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfc\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x35\x01\x05\xff\xff\x05\x00\x07\x08\x3b\x04\x00\x00\x2e\x3b"
    killer_message += 50 * b"\x00"  # this is not gonna fly, in v4 you can't put too long option, max is 255
    killer_message += b"\xff"  # end option
    srv_msg.send_raw_message(raw_append=killer_message)

    srv_msg.send_wait_for_message('MUST', None, expect_response=False)

    _get_offer()


@pytest.mark.v4
def test_cve_2019_6473_fqdn():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    # correct message
    killer_message = b"\x01\x01\x06\x00\x00\x80\x64\x49\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x27\x6d\xee\x67\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x63\x82\x53\x63\x35\x01\x01"
    # incorrect FQDN, kea should drop and survive
    killer_message += b"\x0f\xff\xff\xff\x7f\x00\x00\x00\x7f\x00\x00\x00\x00\x00\x00\x04\x63\x82\x53\x63\x35\x01\x01\x3d\x07\x01\x00\x00\x00\x00\x00\x00\x19\x0c\x4e\x01\x00\x07\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x35\x01\x05\x3a\x04\x00\x00\x07\x08\x3b\x04\x00\x00\x2e\x3b\x04\x00\x19\x2e\x00\x00\x00\x0a\x00\x12\x00\x00\x00\x00\x00\x00\x00\x0b\x82\x01\xfc\x42\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x35\x01\x05\x3a\x04\x00\x00\x07\x08\x3b\x04\x00\x00\x2e\x3b\x04\x00\x19\x2e\x56\x00\x00\x0a\x00\x12\x00\x00\x00\x00\x00\x00\x00\x0b\x82\x01\xfc\x42\x00\x00\x00\x00\x19\x0c\x4e\x01\x05\x3a\x04\xde\x00\x07\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x35\x01\x05\x3a\x07\x08\x3b\x04\x00\x00\x2e\x3b\x04\x00\x19\x2e\x56\x40\x00\x00\x00\x00\x00\x0a\x00\x12\x00\x00\x00\x00\x00\x19\x00\x0b\x82\x01\xfc\x42\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfc\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x35\x01\x05\xff\xff\x05\x00\x07\x08\x3b\x04\x00\x00\x2e\x3b"
    killer_message += b"\xff"  # end option
    srv_msg.send_raw_message(raw_append=killer_message)

    srv_msg.send_wait_for_message('MUST', None, expect_response=False)

    _get_offer()


@pytest.mark.v4
def test_cve_2019_6473_fqdn_too_long():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    # correct message
    killer_message = b"\x01\x01\x06\x00\x00\x80\x64\x49\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x27\x6d\xee\x67\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x63\x82\x53\x63\x35\x01\x01"
    # incorrect FQDN extended with zeros at the end
    killer_message += b"\x0f\xff\xff\xff\x7f\x00\x00\x00\x7f\x00\x00\x00\x00\x00\x00\x04\x63\x82\x53\x63\x35\x01\x01\x3d\x07\x01\x00\x00\x00\x00\x00\x00\x19\x0c\x4e\x01\x00\x07\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x35\x01\x05\x3a\x04\x00\x00\x07\x08\x3b\x04\x00\x00\x2e\x3b\x04\x00\x19\x2e\x00\x00\x00\x0a\x00\x12\x00\x00\x00\x00\x00\x00\x00\x0b\x82\x01\xfc\x42\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x35\x01\x05\x3a\x04\x00\x00\x07\x08\x3b\x04\x00\x00\x2e\x3b\x04\x00\x19\x2e\x56\x00\x00\x0a\x00\x12\x00\x00\x00\x00\x00\x00\x00\x0b\x82\x01\xfc\x42\x00\x00\x00\x00\x19\x0c\x4e\x01\x05\x3a\x04\xde\x00\x07\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x35\x01\x05\x3a\x07\x08\x3b\x04\x00\x00\x2e\x3b\x04\x00\x19\x2e\x56\x40\x00\x00\x00\x00\x00\x0a\x00\x12\x00\x00\x00\x00\x00\x19\x00\x0b\x82\x01\xfc\x42\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfc\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x35\x01\x05\xff\xff\x05\x00\x07\x08\x3b\x04\x00\x00\x2e\x3b"
    killer_message += 40 * b"\x00"  # in dhcp v4 option length max is 255, let's put 00 at the end
    killer_message += b"\xff"  # end
    srv_msg.send_raw_message(raw_append=killer_message)

    srv_msg.send_wait_for_message('MUST', None, expect_response=False)

    _get_offer()


@pytest.mark.v4
def test_cve_2019_6473_fqdn_0_length():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    # correct message
    killer_message = b"\x01\x01\x06\x00\x00\x80\x64\x49\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x27\x6d\xee\x67\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x63\x82\x53\x63\x35\x01\x01"
    # hostname length 0, should be dropped
    killer_message += b"\x0f\x00\x00"
    killer_message += b"\xff"  # end option
    srv_msg.send_raw_message(raw_append=killer_message)

    srv_msg.send_wait_for_message('MUST', None, expect_response=False)

    # check if kea is still alive
    _get_offer()


@pytest.mark.v4
def test_cve_2019_wtf():
    misc.test_setup()
    srv_control.config_srv_subnet('10.0.0.0/8', '10.0.0.0-10.255.255.255')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    killer_message = b"\x01\x00\x00\x02\x00\x2e\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x6c\x82\xdc\x4e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1d\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf0\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x63\x82\x53\x63\x35\x01\x03\x5c\xff\x02\xf9\x37\x04\x01\x1c\x03\x2b\x33\x04\x00\x00\x0e\x07\x50\x61\x64\x64\x69\x6e\x67\x00\x3d\x07\x01\x00\x00\x6c\x82\xdc\x4e\xff"

    srv_msg.send_raw_message(raw_append=killer_message)

    srv_msg.send_wait_for_message('MUST', None, expect_response=False)

    # check if kea is still alive
    _get_offer()


@pytest.mark.v4
def test_cve_2019_6474():
    # This test verifies two issues uncovered in CVE-2019-6474:
    # - a broken packet can cause Kea to write invalid lease to disk
    # - when restarted, memfile backend gives up if there were more than 100
    #   errors while reading a lease file.
    misc.test_setup()
    srv_control.config_srv_subnet('10.0.0.0/8', '10.0.0.0-10.255.255.255')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # we will send a lot of exactly the same packets, let's turn of printing them
    tmp = world.f_cfg.show_packets_from
    world.f_cfg.show_packets_from = ""

    misc.test_procedure()
    # message that causes kea to write incorrect lease
    killer_message = b"\x01\x00\x00\x02\x00\x2e\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x6c\x82\xdc\x4e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1d\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf0\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x63\x82\x53\x63\x35\x01\x03\x5c\xff\x02\xf9\x37\x04\x01\x1c\x03\x2b\x33\x04\x00\x00\x0e\x07\x50\x61\x64\x64\x69\x6e\x67\x00\x3d\x07\x01\x00\x00\x6c\x82\xdc\x4e\xff"

    # send it 101 times. This is an attempt to trigger the memfile lease parser to
    # bail out after 100 broken leases being read from a file.
    for _ in range(101):
        srv_msg.send_raw_message(raw_append=killer_message)
        # kea is actually responding but scapy is unable to detect it
        srv_msg.send_wait_for_message('MUST', None, expect_response=False)

    world.f_cfg.show_packets_from = tmp
    # restart kea, before fix it wasn't starting
    srv_control.start_srv('DHCP', 'stopped')
    srv_control.start_srv('DHCP', 'started')
    # check if kea is still alive
    _get_offer()
