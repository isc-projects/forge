"""DHCPv6 options defined in subnet"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_control
import misc
import srv_msg
import references


@pytest.mark.v6
@pytest.mark.dhcp6
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
    srv_control.config_srv('preference', '0', '123')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'value', '123')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'value', '123')

    references.references_check('v6.options,')


@pytest.mark.v6
@pytest.mark.dhcp6
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
    srv_control.config_srv('dns-servers', '0', '2001:db8::1,2001:db8::2')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('23')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '23')
    srv_msg.response_check_option_content('Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::1,2001:db8::2')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option('23')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '23')
    srv_msg.response_check_option_content('Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::1,2001:db8::2')

    references.references_check('v6.options,')


@pytest.mark.v6
@pytest.mark.dhcp6
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
    srv_control.config_srv('domain-search', '0', 'domain1.example.com,domain2.isc.org')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('24')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '24')
    srv_msg.response_check_option_content('Response',
                                          '24',
                                          None,
                                          'domains',
                                          'domain1.example.com.,domain2.isc.org.')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option('24')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '24')
    srv_msg.response_check_option_content('Response',
                                          '24',
                                          None,
                                          'domains',
                                          'domain1.example.com.,domain2.isc.org.')

    references.references_check('v6.options,')


@pytest.mark.v6
@pytest.mark.dhcp6
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
    srv_control.config_srv('domain-search', '0', 'subnet.example.com')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('24')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '24')
    srv_msg.response_check_option_content('Response', '24', None, 'domains', 'subnet.example.com.')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option('24')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '24')
    srv_msg.response_check_option_content('Response', '24', None, 'domains', 'subnet.example.com.')

    references.references_check('v6.options,')
