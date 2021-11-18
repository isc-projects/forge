# Copyright (C) 2019-2021 Internet Systems Consortium.
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED 'AS IS' AND INTERNET SYSTEMS CONSORTIUM
# DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# INTERNET SYSTEMS CONSORTIUM BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
# FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
# WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

'''Simple test for BOOTP'''

import pytest

import srv_msg
import srv_control
import misc

from forge_cfg import world


@pytest.mark.v4
@pytest.mark.v4_bootp
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_bootp_basic_request_reply(backend):
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.new_pool('192.168.50.10-192.168.50.10', 0)
    srv_control.add_hooks('libdhcp_bootp.so')

    world.dhcp_cfg["subnet4"][0]["pools"][0]["client-class"] = "BOOTP"
    world.dhcp_cfg["subnet4"][0]["pools"][1]["client-class"] = "DHCP"
    srv_control.create_new_class('DHCP')
    srv_control.add_test_to_class(1, 'test', "not member('BOOTP')")
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # First exchange
    srv_msg.BOOTP_REQUEST_and_BOOTP_REPLY('192.168.50.1')

    # Let's test that we still get a lease on a second exchange.
    srv_msg.BOOTP_REQUEST_and_BOOTP_REPLY('192.168.50.1')

    # DORA should still work.
    srv_msg.DORA('192.168.50.10')
