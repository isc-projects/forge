# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""How Kea cope with new RFC7550"""

import pytest

from src import srv_msg
from src import references
from src import misc
from src import srv_control


@pytest.mark.disabled
@pytest.mark.rfc7550
def test_v6_rfc7550_1():
    misc.test_setup()
    srv_control.set_time('preferred-lifetime', 300)
    srv_control.set_time('valid-lifetime', 400)
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.config_srv_prefix('3001::', 0, 64, 96)
    srv_control.configure_loggers('kea-dhcp6', 'DEBUG', 99)
    # start server:
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)

    references.references_check('RFC')


@pytest.mark.disabled
@pytest.mark.rfc7550
def test_v6_rfc7550_2():
    misc.test_setup()
    srv_control.set_time('preferred-lifetime', 300)
    srv_control.set_time('valid-lifetime', 400)
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.config_srv_prefix('3001::', 0, 90, 96)
    srv_control.configure_loggers('kea-dhcp6', 'DEBUG', 99)

    # start server:
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)


@pytest.mark.disabled
@pytest.mark.rfc7550
def test_v6_rfc7550_3():
    misc.test_setup()
    srv_control.set_time('preferred-lifetime', 300)
    srv_control.set_time('valid-lifetime', 400)
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.config_srv_prefix('3001::', 0, 90, 96)
    srv_control.configure_loggers('kea-dhcp6', 'DEBUG', 99)
    # start server:
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(7)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REBIND')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)


@pytest.mark.disabled
@pytest.mark.rfc7550
def test_v6_rfc7550_4():
    misc.test_setup()
    srv_control.set_time('preferred-lifetime', 300)
    srv_control.set_time('valid-lifetime', 400)
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.configure_loggers('kea-dhcp6', 'DEBUG', 99)
    # start server:
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(7)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REBIND')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)


@pytest.mark.disabled
@pytest.mark.rfc7550
def test_v6_rfc7550_5():
    misc.test_setup()
    srv_control.set_time('preferred-lifetime', 300)
    srv_control.set_time('valid-lifetime', 400)
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.configure_loggers('kea-dhcp6', 'DEBUG', 99)
    # start server:
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)


@pytest.mark.disabled
@pytest.mark.rfc7550
def test_v6_rfc7550_6():
    misc.test_setup()
    srv_control.set_time('preferred-lifetime', 300)
    srv_control.set_time('valid-lifetime', 400)
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.configure_loggers('kea-dhcp6', 'DEBUG', 99)
    # start server:
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_sets_value('Client', 'T1', 0)
    srv_msg.client_sets_value('Client', 'T2', 0)
    srv_msg.client_sets_value('Client', 'validlft', 0)
    srv_msg.client_sets_value('Client', 'plen', 96)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)


@pytest.mark.disabled
@pytest.mark.rfc7550
def test_v6_rfc7550_7():
    misc.test_setup()
    srv_control.set_time('preferred-lifetime', 300)
    srv_control.set_time('valid-lifetime', 400)
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.config_srv_prefix('3001::', 0, 90, 96)
    srv_control.configure_loggers('kea-dhcp6', 'DEBUG', 99)
    # start server:
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_sets_value('Client', 'T1', 0)
    srv_msg.client_sets_value('Client', 'T2', 0)
    srv_msg.client_sets_value('Client', 'validlft', 0)
    srv_msg.client_sets_value('Client', 'plen', 96)
    srv_msg.client_sets_value('Client', 'prefix', '3001::1:0:0')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)


@pytest.mark.disabled
@pytest.mark.rfc7550
def test_v6_rfc7550_8():
    misc.test_setup()
    srv_control.set_time('preferred-lifetime', 300)
    srv_control.set_time('valid-lifetime', 400)
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.configure_loggers('kea-dhcp6', 'DEBUG', 99)
    # start server:
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    # Client does include IA-PD.
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_sets_value('Client', 'T1', 0)
    srv_msg.client_sets_value('Client', 'T2', 0)
    srv_msg.client_sets_value('Client', 'validlft', 0)
    srv_msg.client_sets_value('Client', 'plen', 96)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    # Client sets prefix value to 3000::1:0:0.
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REBIND')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)


@pytest.mark.disabled
@pytest.mark.rfc7550
def test_v6_rfc7550_9():
    misc.test_setup()
    srv_control.set_time('preferred-lifetime', 300)
    srv_control.set_time('valid-lifetime', 400)
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.config_srv_prefix('3001::', 0, 90, 96)
    srv_control.configure_loggers('kea-dhcp6', 'DEBUG', 99)
    # start server:
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    # Client does include IA-PD.
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_sets_value('Client', 'T1', 0)
    srv_msg.client_sets_value('Client', 'T2', 0)
    srv_msg.client_sets_value('Client', 'validlft', 0)
    srv_msg.client_sets_value('Client', 'plen', 96)
    srv_msg.client_sets_value('Client', 'prefix', '3001::1:0:0')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REBIND')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(25)


@pytest.mark.disabled
@pytest.mark.rfc7550
def test_v6_rfc7550_10():
    misc.test_setup()
    srv_control.set_time('preferred-lifetime', 300)
    srv_control.set_time('valid-lifetime', 400)
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.config_srv_prefix('3001::', 0, 90, 96)
    srv_control.configure_loggers('kea-dhcp6', 'DEBUG', 99)
    # start server:
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REBIND')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(25)


@pytest.mark.disabled
@pytest.mark.rfc7550
def test_v6_rfc7550_11():
    misc.test_setup()
    srv_control.set_time('preferred-lifetime', 300)
    srv_control.set_time('valid-lifetime', 400)
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.config_srv_prefix('3001::', 0, 90, 96)
    srv_control.configure_loggers('kea-dhcp6', 'DEBUG', 99)
    # start server:
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(25)


@pytest.mark.disabled
@pytest.mark.rfc7550
@pytest.mark.PD
@pytest.mark.rfc3633
def test_prefix():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.config_srv_prefix('3001::', 0, 90, 96)
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)


@pytest.mark.disabled
@pytest.mark.rfc7550
def test_v6_rfc7550_12():
    misc.test_setup()
    srv_control.set_time('preferred-lifetime', 300)
    srv_control.set_time('valid-lifetime', 400)
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.config_srv_prefix('3001::', 0, 90, 96)
    srv_control.configure_loggers('kea-dhcp6', 'DEBUG', 99)

    # start server:
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)


@pytest.mark.disabled
@pytest.mark.rfc7550
def test_v6_rfc7550_13():
    misc.test_setup()
    srv_control.set_time('preferred-lifetime', 300)
    srv_control.set_time('valid-lifetime', 400)
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.config_srv_prefix('3001::', 0, 90, 96)
    srv_control.configure_loggers('kea-dhcp6', 'DEBUG', 99)
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_sets_value('Client', 'T1', 0)
    srv_msg.client_sets_value('Client', 'T2', 0)
    srv_msg.client_sets_value('Client', 'validlft', 0)
    srv_msg.client_sets_value('Client', 'preflft', 0)
    srv_msg.client_sets_value('Client', 'IA_Address', '3001::1')
    srv_msg.client_does_include('Client', 'IA_Address')

    # Client does include IA-PD.
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)


@pytest.mark.disabled
@pytest.mark.rfc7550
def test_v6_rfc7550_14():
    misc.test_setup()
    srv_control.set_time('preferred-lifetime', 300)
    srv_control.set_time('valid-lifetime', 400)
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.config_srv_prefix('3001::', 0, 90, 96)
    srv_control.configure_loggers('kea-dhcp6', 'DEBUG', 99)
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:02')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_sets_value('Client', 'T1', 0)
    srv_msg.client_sets_value('Client', 'T2', 0)
    srv_msg.client_sets_value('Client', 'validlft', 0)
    srv_msg.client_sets_value('Client', 'preflft', 0)
    srv_msg.client_sets_value('Client', 'IA_Address', '3000::1')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REBIND')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(25)
