# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Configure Kea's server-id."""

import pytest

from src import misc
from src import srv_msg
from src import srv_control

from src.softwaresupport.multi_server_functions import verify_file_permissions
from src.protosupport.multi_protocol_functions import file_contains_line
from src.forge_cfg import world


@pytest.mark.v6
@pytest.mark.server_id
def test_v6_server_id_llt():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_id('LLT', '00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_option_content(1, 'duid', '00:01:00:01:52:7b:a8:f0:08:00:27:58:f1:e8', expect_include=False)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_option_content(2, 'duid', '00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8')


@pytest.mark.v6
@pytest.mark.server_id
def test_v6_server_id_en():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_id('EN', '00:02:00:00:09:BF:87:AB:EF:7A:5B:B5:45')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(2)
    # Response option 2 MUST contain duid 00:02:00:00:09:BF:87:AB:EF:7A:5B:B5:45.
    srv_msg.response_check_include_option(1)
    # Response option 1 MUST NOT contain duid 00:02:00:00:09:BF:87:AB:EF:7A:5B:B5:45.


@pytest.mark.v6
@pytest.mark.server_id
def test_v6_server_id_ll():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_id('LL', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_option_content(2, 'duid', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_option_content(1, 'duid', '00:03:00:01:ff:ff:ff:ff:ff:01', expect_include=False)


@pytest.mark.v6
@pytest.mark.server_id
def test_v6_server_id_file():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_id('EN', '00:02:00:00:09:09:87:02:68:71:58:75:45')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    path = world.f_cfg.data_join('kea-dhcp6-serverid')
    file_contains_line(path, '00:02:00:00:09:09:87:02:68:71:58:75:45')
    verify_file_permissions(path)
