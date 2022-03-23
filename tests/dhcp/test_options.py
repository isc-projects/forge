"""Options defined at different levels of config, subnet, shared network, pool"""

# pylint: disable=invalid-name,line-too-long

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
    srv_control.start_srv_during_process('DHCP', 'configuration')


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
    srv_control.start_srv_during_process('DHCP', 'configuration')


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
