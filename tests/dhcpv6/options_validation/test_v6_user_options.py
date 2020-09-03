"""DHCPv6 custom options"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_control
import srv_msg
import references
import misc


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
    srv_control.build_and_send_config_files('SSH', 'config-file')
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
    srv_control.build_and_send_config_files('SSH', 'config-file')
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
    srv_control.build_and_send_config_files('SSH', 'config-file')
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
    srv_control.build_and_send_config_files('SSH', 'config-file')
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
