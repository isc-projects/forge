# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Options defined at different levels of config, subnet, shared network, pool"""

import pytest

from src import srv_control
from src import misc
from src import srv_msg
from src import references

from src.forge_cfg import world


@pytest.mark.v6
@pytest.mark.options
@pytest.mark.subnet
def test_v6_options_subnet_preference():
    #  Testing server ability to configure it with option
    #  preference (code 7) with value 123 per subnet(to override global)
    #  and ability to share that value with client via Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  preference value 123		<--	ADVERTISE
    #  request option	REQUEST -->
    #  preference value 123		<--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					Preference option with value 123

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv('preference', 0, '123')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(7)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 123)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 123)

    references.references_check('v6.options,')


@pytest.mark.v6
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.rfc3646
def test_v6_options_subnet_dns_servers():
    #  Testing server ability to configure it with option
    #  DNS servers (code 23) with addresses 2001:db8::1 per subnet(to override global)
    #  and ability to share that value with client via Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  dns-servers				<--	ADVERTISE
    #  request option	REQUEST -->
    #  dns-servers				<--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					dns-servers option with addresses
    # 					2001:db8::1 and 2001:db8::2

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv('dns-servers', 0, '2001:db8::1,2001:db8::2')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(23)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::1,2001:db8::2')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option(23)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::1,2001:db8::2')

    references.references_check('v6.options,')


@pytest.mark.v6
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.rfc3646
def test_v6_options_subnet_domains():
    #  Testing server ability to configure it with option
    #  domains (code 24) with domains domain1.example.com
    #  and domain2.isc.org, per subnet(to override global)
    #  and ability to share that value with client via Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  domain-search			<--	ADVERTISE
    #  request option	REQUEST -->
    #  domain-search			<--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					domain-search option with addresses
    # 					domain1.example.com and domain2.isc.org
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv('domain-search', 0, 'domain1.example.com,domain2.isc.org')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(24)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(24)
    srv_msg.response_check_option_content(24, 'domains', 'domain1.example.com.,domain2.isc.org.')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option(24)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(24)
    srv_msg.response_check_option_content(24, 'domains', 'domain1.example.com.,domain2.isc.org.')

    references.references_check('v6.options,')


@pytest.mark.v6
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.rfc3646
def test_v6_options_subnet_override():
    #  Testing server ability to configure it with option
    #  domains (code 24) with domains subnet.example.com per subnet
    #  (to override global which is also configured with domain global.example.com)
    #  and ability to share that value with client via Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  domain-search			<--	ADVERTISE
    #  request option	REQUEST -->
    #  domain-search			<--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					domain-search option with addresses
    # 					subnet.example.com
    #  				REPLY/ADVERTISE MUST NOT include option:
    # 					domain-search option with addresses
    # 					global.example.com
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt('domain-search', 'global.example.com')
    srv_control.config_srv('domain-search', 0, 'subnet.example.com')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(24)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(24)
    srv_msg.response_check_option_content(24, 'domains', 'subnet.example.com.')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option(24)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(24)
    srv_msg.response_check_option_content(24, 'domains', 'subnet.example.com.')

    references.references_check('v6.options,')


def _get_lease(mac, routers, address):
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', mac)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', address)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', mac)
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', address)
    srv_msg.client_requests_option(3)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', address)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'value', routers)


def _get_lease6(duid, pref_val):
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'prefval', pref_val)


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.preference
def test_v4_options_pool_level():
    misc.test_setup()
    srv_control.config_srv_subnet("172.16.0.0/16", "172.16.0.20-172.16.0.20")
    srv_control.new_pool("172.16.0.50-172.16.0.50", 0)
    srv_control.config_srv_opt('routers', '100.100.100.10')

    option = {"data": "172.17.0.1", "name": "routers"}
    world.dhcp_cfg["subnet4"][0]["pools"][0].update({"option-data": [option]})
    option2 = {"data": "172.170.10.111", "name": "routers"}
    world.dhcp_cfg["subnet4"][0]["pools"][1].update({"option-data": [option2]})

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _get_lease("01:01:01:01:01:01", "172.17.0.1", "172.16.0.20")
    _get_lease("01:01:01:02:02:02", "172.170.10.111", "172.16.0.50")


@pytest.mark.v6
@pytest.mark.options
@pytest.mark.preference
def test_v6_options_pool_level():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.new_pool("2001:db8:1::500-2001:db8:1::500", 0)
    srv_control.config_srv_opt('preference', "20")

    option = {"name": "preference", "space": "dhcp6", "data": "1"}
    world.dhcp_cfg["subnet6"][0]["pools"][0].update({"option-data": [option]})

    option2 = {"name": "preference", "space": "dhcp6", "data": "2"}
    world.dhcp_cfg["subnet6"][0]["pools"][1].update({"option-data": [option2]})

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # lease from first pool should have preference val set to 1
    _get_lease6('00:03:00:01:ff:ff:ff:ff:ff:01', 1)
    # lease from seconnd pool should have preference val set to 2
    _get_lease6('00:03:00:01:ff:ff:ff:ff:ff:02', 2)


@pytest.mark.v6
@pytest.mark.options
@pytest.mark.user
def test_v6_options_user_defined_option():
    #  Testing server ability to configure it with user custom option
    #  in this case: option code 100, value unit8 123.
    #  with client via Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  custom option 			<--	ADVERTISE
    #  request option	REQUEST -->
    #  custom option			<--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					custom option with value 123

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_custom_opt('foo', 100, 'uint8', 123)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(100)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(100)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option(100)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(100)
    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.options
@pytest.mark.user
def test_v6_options_user_defined_option_code_zero():
    #  Testing server ability to configure it with user custom option
    #  in this case: option code 100, value unit8 123.
    #  with client via Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  custom option 			<--	ADVERTISE
    #  request option	REQUEST -->
    #  custom option			<--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					custom option with value 123

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_custom_opt('foo', 0, 'uint8', 123)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started', should_succeed=False)


@pytest.mark.v6
@pytest.mark.options
@pytest.mark.user
def test_v6_options_user_defined_option_standard_code():
    #  Testing server ability to configure it with user custom option
    #  in this case: option code 100, value unit8 123.
    #  with client via Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  custom option 			<--	ADVERTISE
    #  request option	REQUEST -->
    #  custom option			<--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					custom option with value 123

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_custom_opt('foo', 12, 'uint8', 123)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started', should_succeed=False)


@pytest.mark.v6
@pytest.mark.options
def test_v6_options_all():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt('preference', '123')
    srv_control.config_srv_opt('sip-server-dns', 'srv1.example.com,srv2.isc.org')
    srv_control.config_srv_opt('dns-servers', '2001:db8::1,2001:db8::2')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv_opt('sip-server-addr', '2001:db8::1,2001:db8::2')
    srv_control.config_srv_opt('nisp-servers', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv_opt('nis-servers', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv_opt('nis-domain-name', 'ntp.example.com')
    srv_control.config_srv_opt('nisp-domain-name', 'ntp.example.com')
    srv_control.config_srv_opt('sntp-servers', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv_opt('information-refresh-time', '12345678')
    srv_control.config_srv_opt('unicast', '3000::66')
    srv_control.config_srv_opt('bcmcs-server-dns', 'very.good.domain.name.com')
    srv_control.config_srv_opt('bcmcs-server-addr', '3000::66,3000::77')
    srv_control.config_srv_opt('pana-agent', '3000::66,3000::77')
    srv_control.config_srv_opt('new-posix-timezone', 'EST5EDT4')
    srv_control.config_srv_opt('new-tzdb-timezone', 'Europe/Zurich')
    srv_control.config_srv_opt('bootfile-url', 'http://www.kea.isc.org')
    srv_control.config_srv_opt('bootfile-param', '000B48656C6C6F20776F726C640003666F6F')
    srv_control.config_srv_opt('erp-local-domain-name', 'erp-domain.isc.org')
    srv_control.config_srv('domain-search', 0, 'subnet.example.com')
    srv_control.config_srv_custom_opt('foo', 100, 'uint8', '123')
    srv_control.config_srv_opt_space('vendor-4491',
                                     'tftp-servers',
                                     '2001:558:ff18:16:10:253:175:76')
    srv_control.config_srv_opt_space('vendor-4491', 'config-file', 'normal_erouter_v6.cm')
    srv_control.config_srv_opt_space('vendor-4491',
                                     'syslog-servers',
                                     '2001:558:ff18:10:10:253:124:101')
    srv_control.config_srv_opt_space('vendor-4491',
                                     'time-servers',
                                     '2001:558:ff18:16:10:253:175:76')
    srv_control.config_srv_opt_space('vendor-4491', 'time-offset', '-10000')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(7)
    srv_msg.client_requests_option(12)
    srv_msg.client_requests_option(21)
    srv_msg.client_requests_option(22)
    srv_msg.client_requests_option(23)
    srv_msg.client_requests_option(24)
    srv_msg.client_requests_option(27)
    srv_msg.client_requests_option(28)
    srv_msg.client_requests_option(29)
    srv_msg.client_requests_option(30)
    srv_msg.client_requests_option(31)
    srv_msg.client_requests_option(32)
    srv_msg.client_requests_option(33)
    srv_msg.client_requests_option(34)
    srv_msg.client_requests_option(40)
    srv_msg.client_requests_option(41)
    srv_msg.client_requests_option(42)
    srv_msg.client_requests_option(59)
    srv_msg.client_requests_option(60)
    srv_msg.client_requests_option(65)
    srv_msg.client_requests_option(100)
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 123)
    srv_msg.response_check_include_option(12)
    srv_msg.response_check_option_content(12, 'srvaddr', '3000::66')
    srv_msg.response_check_include_option(21)
    srv_msg.response_check_option_content(21, 'addresses', 'srv1.example.com.,srv2.isc.org.')
    srv_msg.response_check_include_option(22)
    srv_msg.response_check_option_content(22, 'addresses', '2001:db8::1,2001:db8::2')
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::1,2001:db8::2')
    srv_msg.response_check_include_option(24)
    srv_msg.response_check_include_option(27)
    srv_msg.response_check_option_content(27, 'addresses', '2001:db8::abc,3000::1,2000::1234')
    srv_msg.response_check_include_option(28)
    srv_msg.response_check_option_content(28, 'addresses', '2001:db8::abc,3000::1,2000::1234')
    srv_msg.response_check_include_option(29)
    srv_msg.response_check_option_content(29, 'domain', 'ntp.example.com.')
    srv_msg.response_check_include_option(30)
    srv_msg.response_check_option_content(30, 'domain', 'ntp.example.com.')
    srv_msg.response_check_include_option(31)
    srv_msg.response_check_option_content(31, 'addresses', '2001:db8::abc,3000::1,2000::1234')
    srv_msg.response_check_include_option(32)
    srv_msg.response_check_option_content(32, 'value', '12345678')
    srv_msg.response_check_include_option(33)
    srv_msg.response_check_option_content(33, 'bcmcsdomains', 'very.good.domain.name.com.')
    srv_msg.response_check_include_option(34)
    srv_msg.response_check_option_content(34, 'bcmcsservers', '3000::66,3000::77')
    srv_msg.response_check_include_option(40)
    srv_msg.response_check_option_content(40, 'paaaddr', '3000::66,3000::77')
    srv_msg.response_check_include_option(41)
    srv_msg.response_check_option_content(41, 'optdata', 'EST5EDT4')
    srv_msg.response_check_include_option(42)
    srv_msg.response_check_option_content(42, 'optdata', 'Europe/Zurich')
    srv_msg.response_check_include_option(59)
    srv_msg.response_check_option_content(59, 'optdata', 'http://www.kea.isc.org')
    srv_msg.response_check_include_option(65)
    srv_msg.response_check_option_content(65, 'erpdomain', 'erp-domain.isc.org.')

    misc.test_procedure()
    srv_msg.client_requests_option(7)
    srv_msg.client_requests_option(12)
    srv_msg.client_requests_option(21)
    srv_msg.client_requests_option(22)
    srv_msg.client_requests_option(23)
    srv_msg.client_requests_option(24)
    srv_msg.client_requests_option(27)
    srv_msg.client_requests_option(28)
    srv_msg.client_requests_option(29)
    srv_msg.client_requests_option(30)
    srv_msg.client_requests_option(31)
    srv_msg.client_requests_option(32)
    srv_msg.client_requests_option(33)
    srv_msg.client_requests_option(34)
    srv_msg.client_requests_option(40)
    srv_msg.client_requests_option(41)
    srv_msg.client_requests_option(42)
    srv_msg.client_requests_option(59)
    srv_msg.client_requests_option(60)
    srv_msg.client_requests_option(65)
    srv_msg.client_requests_option(100)
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1, 32)
    srv_msg.add_vendor_suboption('Client', 1, 33)
    srv_msg.add_vendor_suboption('Client', 1, 34)
    srv_msg.add_vendor_suboption('Client', 1, 37)
    srv_msg.add_vendor_suboption('Client', 1, 38)
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(17)
    srv_msg.response_check_option_content(17, 'sub-option', 32)
    srv_msg.response_check_option_content(17, 'sub-option', 33)
    srv_msg.response_check_option_content(17, 'sub-option', 34)
    srv_msg.response_check_option_content(17, 'sub-option', 37)
    srv_msg.response_check_option_content(17, 'sub-option', 38)
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 123)
    srv_msg.response_check_include_option(12)
    srv_msg.response_check_option_content(12, 'srvaddr', '3000::66')
    srv_msg.response_check_include_option(21)
    srv_msg.response_check_option_content(21, 'addresses', 'srv1.example.com.,srv2.isc.org.')
    srv_msg.response_check_include_option(22)
    srv_msg.response_check_option_content(22, 'addresses', '2001:db8::1,2001:db8::2')
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::1,2001:db8::2')
    srv_msg.response_check_include_option(24)
    srv_msg.response_check_option_content(24, 'domains', 'subnet.example.com.')
    srv_msg.response_check_include_option(27)
    srv_msg.response_check_option_content(27, 'addresses', '2001:db8::abc,3000::1,2000::1234')
    srv_msg.response_check_include_option(28)
    srv_msg.response_check_option_content(28, 'addresses', '2001:db8::abc,3000::1,2000::1234')
    srv_msg.response_check_include_option(29)
    srv_msg.response_check_option_content(29, 'domain', 'ntp.example.com.')
    srv_msg.response_check_include_option(30)
    srv_msg.response_check_option_content(30, 'domain', 'ntp.example.com.')
    srv_msg.response_check_include_option(31)
    srv_msg.response_check_option_content(31, 'addresses', '2001:db8::abc,3000::1,2000::1234')
    srv_msg.response_check_include_option(32)
    srv_msg.response_check_option_content(32, 'value', '12345678')
    srv_msg.response_check_include_option(33)
    srv_msg.response_check_option_content(33, 'bcmcsdomains', 'very.good.domain.name.com.')
    srv_msg.response_check_include_option(34)
    srv_msg.response_check_option_content(34, 'bcmcsservers', '3000::66,3000::77')
    srv_msg.response_check_include_option(40)
    srv_msg.response_check_option_content(40, 'paaaddr', '3000::66,3000::77')
    srv_msg.response_check_include_option(41)
    srv_msg.response_check_option_content(41, 'optdata', 'EST5EDT4')
    srv_msg.response_check_include_option(42)
    srv_msg.response_check_option_content(42, 'optdata', 'Europe/Zurich')
    srv_msg.response_check_include_option(59)
    srv_msg.response_check_option_content(59, 'optdata', 'http://www.kea.isc.org')
    srv_msg.response_check_include_option(65)
    srv_msg.response_check_option_content(65, 'erpdomain', 'erp-domain.isc.org.')


@pytest.mark.v6
@pytest.mark.options
def test_v6_options_always_send_all_levels():
    """
    Configure various options on all levels: global, shared network, subnet and pool. All with
    always_send set to True. Check if all will be actually send to client when not requested.
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_option_to_pool('domain-search', 'domain1.example.com,domain2.isc.org', always_send=True)  # pool opt
    srv_control.config_srv_opt('preference', '123', always_send=True)  # global opt
    srv_control.config_srv('sip-server-dns', 0, 'srv1.example.com,srv2.isc.org', always_send=True)  # subnet opt
    srv_control.shared_subnet('2001:db8:1::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)
    srv_control.option_in_shared_network('dns-servers', '2001:db8::1,2001:db8::2', always_send=True)  # network opt
    srv_control.config_srv_custom_opt('foo', 189, 'uint8', 123, always_send=True)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(24)
    srv_msg.response_check_option_content(24, 'domains', 'domain1.example.com.,domain2.isc.org.')
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 123)
    srv_msg.response_check_include_option(21)
    srv_msg.response_check_option_content(21, 'addresses', 'srv1.example.com.,srv2.isc.org.')
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::1,2001:db8::2')
    srv_msg.response_check_include_option(189)

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(24)
    srv_msg.response_check_option_content(24, 'domains', 'domain1.example.com.,domain2.isc.org.')
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 123)
    srv_msg.response_check_include_option(21)
    srv_msg.response_check_option_content(21, 'addresses', 'srv1.example.com.,srv2.isc.org.')
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'addresses', '2001:db8::1,2001:db8::2')
    srv_msg.response_check_include_option(189)


@pytest.mark.v4
@pytest.mark.options
def test_v4_options_always_send_all_levels():
    """
    Configure various options on all levels: global, shared network, subnet and pool. All with
    always_send set to True. Check if all will be actually send to client when not requested.
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.add_option_to_pool('domain-name-servers', '199.199.199.1,100.100.100.1', always_send=True)
    srv_control.config_srv_opt('name-servers', '199.199.199.1,100.100.100.1', always_send=True)
    srv_control.config_srv('merit-dump', 0, 'some-string', always_send=True)
    srv_control.shared_subnet('192.168.50.0/24', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)
    srv_control.option_in_shared_network('time-offset', '50', always_send=True)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:11:11:22')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(6, 'value', '100.100.100.1')
    srv_msg.response_check_include_option(5)
    srv_msg.response_check_option_content(5, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(5, 'value', '100.100.100.1')
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_option_content(2, 'value', 50)
    srv_msg.response_check_include_option(14)
    srv_msg.response_check_option_content(14, 'value', 'some-string')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:11:11:22')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(6, 'value', '100.100.100.1')
    srv_msg.response_check_include_option(5)
    srv_msg.response_check_option_content(5, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(5, 'value', '100.100.100.1')
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_option_content(2, 'value', 50)
    srv_msg.response_check_include_option(14)
    srv_msg.response_check_option_content(14, 'value', 'some-string')


@pytest.mark.v4
@pytest.mark.options
def test_v4_never_send_various_combinations():
    # it's a simple feature with number of possibilities, let's do them all in one test

    # global level, no inheritance
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('name-servers', '199.199.199.1,100.100.100.1', never_send=True)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:11:11:22')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(5, expect_include=False)

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:11:11:22')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_include_option(5, expect_include=False)

    srv_control.start_srv('DHCP', 'stopped')

    # global level, no inheritance, always-send to True, still shouldn't be send
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('name-servers', '199.199.199.1,100.100.100.1', never_send=True, always_send=True)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:11:11:22')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(5, expect_include=False)

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:11:11:22')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_include_option(5, expect_include=False)

    srv_control.start_srv('DHCP', 'stopped')

    # two different pools, one has never send to true
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.new_pool('192.168.50.20-192.168.50.20', 0)
    srv_control.add_option_to_pool('name-servers', '199.199.199.1,100.100.100.1', never_send=True,
                                   subnet=0, pool=0)
    srv_control.add_option_to_pool('name-servers', '199.199.199.1,100.100.100.1', never_send=False,
                                   subnet=0, pool=1)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:11:11:22')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(5, expect_include=False)

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:11:11:22')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_include_option(5, expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:11:11:33')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(5)
    srv_msg.response_check_option_content(5, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(5, 'value', '100.100.100.1')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:11:11:33')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.20')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_include_option(5)
    srv_msg.response_check_option_content(5, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(5, 'value', '100.100.100.1')

    srv_control.start_srv('DHCP', 'stopped')

    # check inheritance, option configured in pool, never send is global
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.config_srv_opt('name-servers', '199.199.199.1,100.100.100.1', never_send=True)
    srv_control.add_option_to_pool('name-servers', '199.199.199.1,100.100.100.1', subnet=0, pool=0)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:11:11:22')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(5, expect_include=False)

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:11:11:22')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_include_option(5, expect_include=False)

    srv_control.start_srv('DHCP', 'stopped')

    # check inheritance, option configured in pool, never send is subnet
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.config_srv('name-servers', 0, '199.199.199.1,100.100.100.1', never_send=True)
    srv_control.add_option_to_pool('name-servers', '199.199.199.1,100.100.100.1', subnet=0, pool=0)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:11:11:22')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(5, expect_include=False)

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:11:11:22')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_include_option(5, expect_include=False)

    srv_control.start_srv('DHCP', 'stopped')

    # check inheritance, option configured in pool, never send is shared-network
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_option_to_pool('name-servers', '199.199.199.1,100.100.100.1', subnet=0, pool=0)
    srv_control.shared_subnet('192.168.50.0/24', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    srv_control.option_in_shared_network('name-servers', '199.199.199.1,100.100.100.1',
                                         shared_network=0, never_send=True)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:11:11:22')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(5, expect_include=False)

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:11:11:22')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_include_option(5, expect_include=False)

    srv_control.start_srv('DHCP', 'stopped')

    # check inheritance, option configured in reservation, never send is global
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.config_srv_opt('name-servers', '199.199.199.1,100.100.100.1', never_send=True)
    srv_control.host_reservation_in_subnet('ip-address',
                                           '192.168.50.100',
                                           0,
                                           'hw-address',
                                           'ff:01:02:03:ff:04')
    opt = {
        "code": 5,
        "csv-format": True,
        "data": "199.199.199.1,100.100.100.1",
        "name": "name-servers",
        "space": "dhcp4",
        "never-send": False
    }
    world.dhcp_cfg["subnet4"][0]["reservations"][0].update({"option-data": [opt]})
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(5, expect_include=False)

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.100')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_include_option(5, expect_include=False)

    srv_control.start_srv('DHCP', 'stopped')

    # check inheritance, option configured in class, never send is global
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.52.0/24', '192.168.52.10-192.168.52.10')
    srv_control.config_srv_opt('name-servers', '199.199.199.1,100.100.100.1', never_send=True)
    srv_control.create_new_class('Management')
    srv_control.add_test_to_class(1, 'test', "option[61].hex == pkt4.mac")
    srv_control.config_client_classification(0, 'Management')

    opt = {
        "code": 5,
        "csv-format": True,
        "data": "199.199.199.1,100.100.100.1",
        "name": "name-servers",
        "space": "dhcp4",
        "never-send": False
    }
    world.dhcp_cfg["client-classes"][0].update({"option-data": [opt]})
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(5, expect_include=False)

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.52.10')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_include_option(5, expect_include=False)


@pytest.mark.v6
@pytest.mark.options
def test_v6_never_send_various_combinations():
    # it's a simple feature with number of possibilities, let's do them all in one test

    # global level, no inheritance
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ff')
    srv_control.config_srv_opt('preference', '123', never_send=True)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(7)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(7, expect_include=False)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(7, expect_include=False)

    srv_control.start_srv('DHCP', 'stopped')

    # global level, no inheritance, always-send to True, still shouldn't be send
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:2::/64', '2001:db8:2::1-2001:db8:2::ff')
    srv_control.config_srv_opt('preference', '123', never_send=True, always_send=True)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(7)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(7, expect_include=False)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(7, expect_include=False)

    srv_control.start_srv('DHCP', 'stopped')

    # two different pools, one has never send to true
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:3::/64', '2001:db8:3::1-2001:db8:3::1')
    srv_control.new_pool('2001:db8:3::100-2001:db8:3::100', 0)
    srv_control.add_option_to_pool('preference', '123', never_send=True,
                                   subnet=0, pool=0)
    srv_control.add_option_to_pool('preference', '123', never_send=False,
                                   subnet=0, pool=1)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(7)
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(7, expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(7, expect_include=False)

    misc.test_procedure()
    srv_msg.client_requests_option(7)
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:2')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 123)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', 123)

    srv_control.start_srv('DHCP', 'stopped')

    # check inheritance, option configured in pool, never send is global
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:4::/64', '2001:db8:4::1-2001:db8:4::ff')
    srv_control.config_srv_opt('preference', '123', never_send=True)
    srv_control.add_option_to_pool('preference', '123', subnet=0, pool=0)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(7)
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(7, expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(7, expect_include=False)

    srv_control.start_srv('DHCP', 'stopped')

    # check inheritance, option configured in pool, never send is subnet
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:5::/64', '2001:db8:5::1-2001:db8:5::ff')
    srv_control.config_srv('preference', 0, '123', never_send=True)
    srv_control.add_option_to_pool('preference', '123', subnet=0, pool=0)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(7)
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(7, expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(7, expect_include=False)

    srv_control.start_srv('DHCP', 'stopped')

    # check inheritance, option configured in pool, never send is shared-network
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:6::/64', '2001:db8:6::1-2001:db8:6::ff')
    srv_control.add_option_to_pool('preference', '123', subnet=0, pool=0)
    srv_control.shared_subnet('2001:db8:6::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    srv_control.option_in_shared_network('preference', '123',
                                         shared_network=0, never_send=True)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(7)
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(7, expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(7, expect_include=False)

    srv_control.start_srv('DHCP', 'stopped')

    # check inheritance, option configured in reservation, never send is global
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::fff-2001:db8:1::fff')
    srv_control.config_srv_opt('preference', '123', never_send=True)
    srv_control.host_reservation_in_subnet('ip-address',
                                           '2001:db8:1::fff',
                                           0,
                                           'duid',
                                           '00:03:00:01:f6:f5:f4:f3:f2:01')
    opt = {
        "code": 7,
        "csv-format": True,
        "data": '234',
        "name": "preference",
        "space": "dhcp6",
        "always-send": False
    }
    world.dhcp_cfg["subnet6"][0]["reservations"][0].update({"option-data": [opt]})
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(7)
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(7, expect_include=False)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(7, expect_include=False)

    srv_control.start_srv('DHCP', 'stopped')

    # check inheritance, option configured in class, never send is global
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::afff-2001:db8:1::afff')
    srv_control.config_srv_opt('preference', '123', never_send=True)
    srv_control.create_new_class('Management')
    srv_control.add_test_to_class(1, 'test', 'option[1].hex == 0x00030001f6f5f4f3f201')
    srv_control.config_client_classification(0, 'Management')

    opt = {
        "code": 7,
        "csv-format": True,
        "data": '234',
        "name": "preference",
        "space": "dhcp6",
        "always-send": False
    }
    world.dhcp_cfg["client-classes"][0].update({"option-data": [opt]})
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(7)
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(7, expect_include=False)

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(7, expect_include=False)


@pytest.mark.v4
@pytest.mark.parametrize('suboption3_type', ['ip4-address', 'fqdn'])
def test_cablelabs(suboption3_type):
    """Test cablelabs client conf option with suboption 3 of type ip4-address or fqdn.
    RFC3495 (that defines CableLabs option, code 122) and RCF3594, RFC3634.

    :param suboption3_type: type of suboption 3, can be 'ip4-address' or 'fqdn'
    :type suboption3_type: str
    """

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.config_srv_opt('cablelabs-client-conf', None)  # option 122
    # suboption 1 and 2
    srv_control.config_srv_opt_space('cablelabs-client-conf', 'tsp-primary-server', '199.199.199.1')
    srv_control.config_srv_opt_space('cablelabs-client-conf', 'tsp-secondary-server', '199.199.199.2')

    # suboption 3 can be ip4-address or fqdn
    if suboption3_type == 'ip4-address':
        srv_control.config_srv_custom_opt('tsp-provisioning-server', 3, 'record', '1, 199.199.199.3',
                                          space='cablelabs-client-conf', record_types='uint8, ipv4-address')
        # suboption 3, length 5, type octet 1 for ip4-address, value 199.199.199.1
        suboption3 = b"\x03\x05\x01\xc7\xc7\xc7\x03"
    else:
        srv_control.config_srv_custom_opt('tsp-provisioning-server', 3, 'record', '0, provisioning.example.com.',
                                          space='cablelabs-client-conf', record_types='uint8, fqdn')
        # suboption 3, length 26, type octet 0 for fqdn, value provisioning.example.com.
        suboption3 = b"\x03\x1b\x00\x0cprovisioning\x07example\x03com\x00"

    # suboption 4 to 10
    srv_control.config_srv_opt_space('cablelabs-client-conf', 'tsp-as-parameters', '1234, 5678, 9101')
    srv_control.config_srv_opt_space('cablelabs-client-conf', 'tsp-ap-parameters', '2222, 3333, 4444')
    srv_control.config_srv_opt_space('cablelabs-client-conf', 'tsp-realm', 'abc.example.com.')
    srv_control.config_srv_opt_space('cablelabs-client-conf', 'tsp-use-tgt', 1)
    srv_control.config_srv_opt_space('cablelabs-client-conf', 'tsp-provisioning-timer', 123)
    srv_control.config_srv_opt_space('cablelabs-client-conf', 'tsp-sct', 3)
    srv_control.config_srv_opt_space('cablelabs-client-conf', 'kdc-server', '199.199.199.9, 199.199.199.10')

    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cablelabs_option = (
        b"\x01\x04\xc7\xc7\xc7\x01"  # suboption 1, length 4, value 199.199.199.1
        + b"\x02\x04\xc7\xc7\xc7\x02"  # suboption 2, length 4, value 199.199.199.2
        + suboption3
        + b"\x04\x0c\x00\x00\x04\xd2\x00\x00\x16.\x00\x00#\x8d"  # suboption 4, length 12, value 1234, 5678, 9101
        + b"\x05\x0c\x00\x00\x08\xae\x00\x00\r\x05\x00\x00\x11\\"  # suboption 5, length 12, value 1234, 5678, 9101
        + b"\x06\x11\x03abc\x07example\x03com\x00"  # suboption 6, length 17, value abc.example.com.
        + b"\x07\x01\x01"  # suboption 7, length 1, value 1
        + b"\x08\x01{"  # suboption 8, length 1, value 123
        + b"\x09\x02\x00\x03"  # suboption 9, length 2, value 3
        + b"\x0a\x08\xc7\xc7\xc7\t\xc7\xc7\xc7\n"  # suboption 10, length 8, value 199.199.199.9, 199.199.199.10
    )

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:11:11:22')
    srv_msg.client_requests_option(122)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(122)
    srv_msg.response_check_option_content(122, 'value', cablelabs_option)

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:11:11:22')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
