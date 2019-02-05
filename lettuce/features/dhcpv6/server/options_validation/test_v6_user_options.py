"""DHCPv6 custom options"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_control
from features import srv_msg
from features import references
from features import misc


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.user
def test_v6_options_user_defined_option(step):
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

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_custom_opt(step, 'foo', '100', 'uint8', '123')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '100')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '100')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_requests_option(step, '100')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '100')
    references.references_check(step, 'RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
def test_v6_options_all(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'preference', '123')
    srv_control.config_srv_opt(step, 'sip-server-dns', 'srv1.example.com,srv2.isc.org')
    srv_control.config_srv_opt(step, 'dns-servers', '2001:db8::1,2001:db8::2')
    srv_control.config_srv_opt(step, 'domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.config_srv_opt(step, 'sip-server-addr', '2001:db8::1,2001:db8::2')
    srv_control.config_srv_opt(step, 'nisp-servers', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv_opt(step, 'nis-servers', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv_opt(step, 'nis-domain-name', 'ntp.example.com')
    srv_control.config_srv_opt(step, 'nisp-domain-name', 'ntp.example.com')
    srv_control.config_srv_opt(step, 'sntp-servers', '2001:db8::abc,3000::1,2000::1234')
    srv_control.config_srv_opt(step, 'information-refresh-time', '12345678')
    srv_control.config_srv_opt(step, 'unicast', '3000::66')
    srv_control.config_srv_opt(step, 'bcmcs-server-dns', 'very.good.domain.name.com')
    srv_control.config_srv_opt(step, 'bcmcs-server-addr', '3000::66,3000::77')
    srv_control.config_srv_opt(step, 'pana-agent', '3000::66,3000::77')
    srv_control.config_srv_opt(step, 'new-posix-timezone', 'EST5EDT4')
    srv_control.config_srv_opt(step, 'new-tzdb-timezone', 'Europe/Zurich')
    srv_control.config_srv_opt(step, 'bootfile-url', 'http://www.kea.isc.org')
    srv_control.config_srv_opt(step, 'bootfile-param', '000B48656C6C6F20776F726C640003666F6F')
    srv_control.config_srv_opt(step, 'erp-local-domain-name', 'erp-domain.isc.org')
    srv_control.config_srv(step, 'domain-search', '0', 'subnet.example.com')
    srv_control.config_srv_custom_opt(step, 'foo', '100', 'uint8', '123')
    srv_control.config_srv_opt_space(step,
                                     'vendor-4491',
                                     'tftp-servers',
                                     '2001:558:ff18:16:10:253:175:76')
    srv_control.config_srv_opt_space(step, 'vendor-4491', 'config-file', 'normal_erouter_v6.cm')
    srv_control.config_srv_opt_space(step,
                                     'vendor-4491',
                                     'syslog-servers',
                                     '2001:558:ff18:10:10:253:124:101')
    srv_control.config_srv_opt_space(step,
                                     'vendor-4491',
                                     'time-servers',
                                     '2001:558:ff18:16:10:253:175:76')
    srv_control.config_srv_opt_space(step, 'vendor-4491', 'time-offset', '-10000')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_requests_option(step, '12')
    srv_msg.client_requests_option(step, '21')
    srv_msg.client_requests_option(step, '22')
    srv_msg.client_requests_option(step, '23')
    srv_msg.client_requests_option(step, '24')
    srv_msg.client_requests_option(step, '27')
    srv_msg.client_requests_option(step, '28')
    srv_msg.client_requests_option(step, '29')
    srv_msg.client_requests_option(step, '30')
    srv_msg.client_requests_option(step, '31')
    srv_msg.client_requests_option(step, '32')
    srv_msg.client_requests_option(step, '33')
    srv_msg.client_requests_option(step, '34')
    srv_msg.client_requests_option(step, '40')
    srv_msg.client_requests_option(step, '41')
    srv_msg.client_requests_option(step, '42')
    srv_msg.client_requests_option(step, '59')
    srv_msg.client_requests_option(step, '60')
    srv_msg.client_requests_option(step, '65')
    srv_msg.client_requests_option(step, '100')
    srv_msg.client_send_msg(step, 'INFOREQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', None, 'value', '123')
    srv_msg.response_check_include_option(step, 'Response', None, '12')
    srv_msg.response_check_option_content(step, 'Response', '12', None, 'srvaddr', '3000::66')
    srv_msg.response_check_include_option(step, 'Response', None, '21')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '21',
                                          None,
                                          'addresses',
                                          'srv1.example.com,srv2.isc.org')
    srv_msg.response_check_include_option(step, 'Response', None, '22')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '22',
                                          None,
                                          'addresses',
                                          '2001:db8::1,2001:db8::2')
    srv_msg.response_check_include_option(step, 'Response', None, '23')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::1,2001:db8::2')
    srv_msg.response_check_include_option(step, 'Response', None, '24')
    srv_msg.response_check_include_option(step, 'Response', None, '27')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '27',
                                          None,
                                          'addresses',
                                          '2001:db8::abc,3000::1,2000::1234')
    srv_msg.response_check_include_option(step, 'Response', None, '28')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '28',
                                          None,
                                          'addresses',
                                          '2001:db8::abc,3000::1,2000::1234')
    srv_msg.response_check_include_option(step, 'Response', None, '29')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '29',
                                          None,
                                          'domain',
                                          'ntp.example.com')
    srv_msg.response_check_include_option(step, 'Response', None, '30')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '30',
                                          None,
                                          'domain',
                                          'ntp.example.com')
    srv_msg.response_check_include_option(step, 'Response', None, '31')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '31',
                                          None,
                                          'addresses',
                                          '2001:db8::abc,3000::1,2000::1234')
    srv_msg.response_check_include_option(step, 'Response', None, '32')
    srv_msg.response_check_option_content(step, 'Response', '32', None, 'value', '12345678')
    srv_msg.response_check_include_option(step, 'Response', None, '33')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '33',
                                          None,
                                          'bcmcsdomains',
                                          'very.good.domain.name.com')
    srv_msg.response_check_include_option(step, 'Response', None, '34')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '34',
                                          None,
                                          'bcmcsservers',
                                          '3000::66,3000::77')
    srv_msg.response_check_include_option(step, 'Response', None, '40')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '40',
                                          None,
                                          'paaaddr',
                                          '3000::66,3000::77')
    srv_msg.response_check_include_option(step, 'Response', None, '41')
    srv_msg.response_check_option_content(step, 'Response', '41', None, 'optdata', 'EST5EDT4')
    srv_msg.response_check_include_option(step, 'Response', None, '42')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '42',
                                          None,
                                          'optdata',
                                          'Europe/Zurich')
    srv_msg.response_check_include_option(step, 'Response', None, '59')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '59',
                                          None,
                                          'optdata',
                                          'http://www.kea.isc.org')
    srv_msg.response_check_include_option(step, 'Response', None, '65')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '65',
                                          None,
                                          'erpdomain',
                                          'erp-domain.isc.org')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_requests_option(step, '12')
    srv_msg.client_requests_option(step, '21')
    srv_msg.client_requests_option(step, '22')
    srv_msg.client_requests_option(step, '23')
    srv_msg.client_requests_option(step, '24')
    srv_msg.client_requests_option(step, '27')
    srv_msg.client_requests_option(step, '28')
    srv_msg.client_requests_option(step, '29')
    srv_msg.client_requests_option(step, '30')
    srv_msg.client_requests_option(step, '31')
    srv_msg.client_requests_option(step, '32')
    srv_msg.client_requests_option(step, '33')
    srv_msg.client_requests_option(step, '34')
    srv_msg.client_requests_option(step, '40')
    srv_msg.client_requests_option(step, '41')
    srv_msg.client_requests_option(step, '42')
    srv_msg.client_requests_option(step, '59')
    srv_msg.client_requests_option(step, '60')
    srv_msg.client_requests_option(step, '65')
    srv_msg.client_requests_option(step, '100')
    srv_msg.client_sets_value(step, 'Client', 'enterprisenum', '4491')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption(step, 'Client', '1', '32')
    srv_msg.add_vendor_suboption(step, 'Client', '1', '33')
    srv_msg.add_vendor_suboption(step, 'Client', '1', '34')
    srv_msg.add_vendor_suboption(step, 'Client', '1', '37')
    srv_msg.add_vendor_suboption(step, 'Client', '1', '38')
    srv_msg.client_does_include(step, 'Client', None, 'vendor-specific-info')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '17')
    srv_msg.response_check_option_content(step, 'Response', '17', None, 'sub-option', '32')
    srv_msg.response_check_option_content(step, 'Response', '17', None, 'sub-option', '33')
    srv_msg.response_check_option_content(step, 'Response', '17', None, 'sub-option', '34')
    srv_msg.response_check_option_content(step, 'Response', '17', None, 'sub-option', '37')
    srv_msg.response_check_option_content(step, 'Response', '17', None, 'sub-option', '38')
    srv_msg.response_check_include_option(step, 'Response', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', None, 'value', '123')
    srv_msg.response_check_include_option(step, 'Response', None, '12')
    srv_msg.response_check_option_content(step, 'Response', '12', None, 'srvaddr', '3000::66')
    srv_msg.response_check_include_option(step, 'Response', None, '21')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '21',
                                          None,
                                          'addresses',
                                          'srv1.example.com,srv2.isc.org')
    srv_msg.response_check_include_option(step, 'Response', None, '22')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '22',
                                          None,
                                          'addresses',
                                          '2001:db8::1,2001:db8::2')
    srv_msg.response_check_include_option(step, 'Response', None, '23')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::1,2001:db8::2')
    srv_msg.response_check_include_option(step, 'Response', None, '24')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '24',
                                          None,
                                          'domains',
                                          'subnet.example.com')
    srv_msg.response_check_include_option(step, 'Response', None, '27')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '27',
                                          None,
                                          'addresses',
                                          '2001:db8::abc,3000::1,2000::1234')
    srv_msg.response_check_include_option(step, 'Response', None, '28')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '28',
                                          None,
                                          'addresses',
                                          '2001:db8::abc,3000::1,2000::1234')
    srv_msg.response_check_include_option(step, 'Response', None, '29')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '29',
                                          None,
                                          'domain',
                                          'ntp.example.com')
    srv_msg.response_check_include_option(step, 'Response', None, '30')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '30',
                                          None,
                                          'domain',
                                          'ntp.example.com')
    srv_msg.response_check_include_option(step, 'Response', None, '31')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '31',
                                          None,
                                          'addresses',
                                          '2001:db8::abc,3000::1,2000::1234')
    srv_msg.response_check_include_option(step, 'Response', None, '32')
    srv_msg.response_check_option_content(step, 'Response', '32', None, 'value', '12345678')
    srv_msg.response_check_include_option(step, 'Response', None, '33')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '33',
                                          None,
                                          'bcmcsdomains',
                                          'very.good.domain.name.com')
    srv_msg.response_check_include_option(step, 'Response', None, '34')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '34',
                                          None,
                                          'bcmcsservers',
                                          '3000::66,3000::77')
    srv_msg.response_check_include_option(step, 'Response', None, '40')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '40',
                                          None,
                                          'paaaddr',
                                          '3000::66,3000::77')
    srv_msg.response_check_include_option(step, 'Response', None, '41')
    srv_msg.response_check_option_content(step, 'Response', '41', None, 'optdata', 'EST5EDT4')
    srv_msg.response_check_include_option(step, 'Response', None, '42')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '42',
                                          None,
                                          'optdata',
                                          'Europe/Zurich')
    srv_msg.response_check_include_option(step, 'Response', None, '59')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '59',
                                          None,
                                          'optdata',
                                          'http://www.kea.isc.org')
    srv_msg.response_check_include_option(step, 'Response', None, '65')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '65',
                                          None,
                                          'erpdomain',
                                          'erp-domain.isc.org')
