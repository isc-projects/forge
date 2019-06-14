"""Standard DHCPv6 options part 2"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_msg
import misc
import srv_control
import references


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.preference
def test_v6_options_inforequest_preference():
    #  Testing server ability to configure it with option
    #  preference (code 7)with value 123, and ability to share that value
    #  with client via Reply message as a respond to INFOREQUEST.
    #  						Client		Server
    #  request option	INFOREQUEST -->
    #  preference value 123			<--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					Preference option with value 123
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt('preference', '123')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'value', '123')

    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.sip
def test_v6_options_inforequest_sip_domains():
    #  Testing server ability to configure it with option
    #  SIP domains (code 21) with domains srv1.example.com
    #  and srv2.isc.org, and ability to share that
    #  with client via Reply message as a respond to INFOREQUEST.
    #  						Client		Server
    #  request option	INFOREQUEST -->
    #  sip-server-dns				<--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					sip-server-dns option with domains
    # 					srv1.example.com and srv2.isc.org

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt('sip-server-dns', 'srv1.example.com,srv2.isc.org')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('21')
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '21')
    srv_msg.response_check_option_content('Response',
                                          '21',
                                          None,
                                          'domains',
                                          'srv1.example.com.,srv2.isc.org.')

    references.references_check('RFC331')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.sip
@pytest.mark.rfc3319
def test_v6_options_inforequest_sip_servers():
    #  Testing server ability to configure it with option
    #  SIP servers (code 22) with addresses 2001:db8::1
    #  and 2001:db8::2, and ability to share that
    #  with client via Reply message as a respond to INFOREQUEST.
    #  						Client		Server
    #  request option	INFOREQUEST -->
    #  sip-server-addr				<--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					sip-server-addr option with addresses
    # 					2001:db8::1 and 2001:db8::2
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt('sip-server-addr', '2001:db8::1,2001:db8::2')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('22')
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '22')
    srv_msg.response_check_option_content('Response',
                                          '22',
                                          None,
                                          'addresses',
                                          '2001:db8::1,2001:db8::2')

    references.references_check('RFC331')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.sip
@pytest.mark.rfc3319
def test_v6_options_inforequest_sip_servers_csv():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.add_line('"option-data": [{"code": 22, "data": "2001 0DB8 0001 0000 0000 0000 0000 CAFE",'
                         '"always-send": false, "csv-format": false}]')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('22')
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '22')
    srv_msg.response_check_option_content('Response',
                                          '22',
                                          None,
                                          'addresses',
                                          '2001:db8:1::cafe')

    references.references_check('RFC331')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.sip
@pytest.mark.rfc3319
def test_v6_options_inforequest_sip_servers_csv_incorrect():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.add_line('"option-data": [{"code": 6, "data": "192.167.12.2",'
                         '"always-send": true, "csv-format": false}]')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv_during_process('DHCP', 'configure')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.sip
@pytest.mark.rfc3319
def test_v6_options_inforequest_sip_servers_csv_incorrect_hex():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.add_line('"option-data": [{"code": 6, "data": "31 39 32 2x 31 30 2e 30 2e 31",'
                         ' "always-send": true, "csv-format": false}]')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv_during_process('DHCP', 'configure')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.dns
@pytest.mark.rfc3646
def test_v6_options_inforequest_dns_servers():
    #  Testing server ability to configure it with option
    #  DNS servers (code 23) with addresses 2001:db8::1
    #  and 2001:db8::2, and ability to share that
    #  with client via Reply message as a respond to INFOREQUEST.
    #  						Client		Server
    #  request option	INFOREQUEST -->
    #  dns-servers					<--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					dns-servers option with addresses
    # 					2001:db8::1 and 2001:db8::2

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt('dns-servers', '2001:db8::1,2001:db8::2')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('23')
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '23')
    srv_msg.response_check_option_content('Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::1,2001:db8::2')

    misc.test_procedure()

    references.references_check('v6.options,')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.rfc3646
def test_v6_options_inforequest_domains():
    #  Testing server ability to configure it with option
    #  domains (code 24) with domains domain1.example.com
    #  and domain2.isc.org, and ability to share that
    #  with client via Reply message as a respond to INFOREQUEST.
    #  						Client		Server
    #  request option	INFOREQUEST -->
    #  domain-search				<--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					domain-search option with addresses
    # 					domain1.example.com and domain2.isc.org

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('24')
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '24')
    srv_msg.response_check_option_content('Response',
                                          '24',
                                          None,
                                          'domains',
                                          'domain1.example.com.,domain2.isc.org.')

    references.references_check('RFC364')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.nis
@pytest.mark.rfc3898
def test_v6_options_inforequest_nis_servers():
    #  Testing server ability to configure it with option
    #  NIS servers (code 27) with addresses 2001:db8::abc, 3000::1
    #  and 2000::1234, and ability to share that
    #  with client via Reply message as a respond to INFOREQUEST.
    #  						Client		Server
    #  request option	INFOREQUEST -->
    #  nis-servers					<--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					nis-servers option with addresses
    # 					2001:db8::abc, 3000::1 and 2000::1234.

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt('nis-servers', '2001:db8::abc,3000::1,2000::1234')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('27')
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '27')
    srv_msg.response_check_option_content('Response',
                                          '27',
                                          None,
                                          'addresses',
                                          '2001:db8::abc,3000::1,2000::1234')

    references.references_check('RFC389')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.nis
@pytest.mark.nisp
@pytest.mark.rfc3898
def test_v6_options_inforequest_nisp_servers():
    #  Testing server ability to configure it with option
    #  NIS+ servers (code 28) with addresses 2001:db8::abc, 3000::1
    #  and 2000::1234, and ability to share that
    #  with client via Reply message as a respond to INFOREQUEST.
    #  						Client		Server
    #  request option	INFOREQUEST -->
    #  nisp-servers				<--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					nisp-servers option with addresses
    # 					2001:db8::abc, 3000::1 and 2000::1234.

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt('nisp-servers', '2001:db8::abc,3000::1,2000::1234')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('28')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '28')
    srv_msg.response_check_option_content('Response',
                                          '28',
                                          None,
                                          'addresses',
                                          '2001:db8::abc,3000::1,2000::1234')

    references.references_check('RFC389')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.nis
@pytest.mark.rfc3898
def test_v6_options_inforequest_nisdomain():
    #  Testing server ability to configure it with option
    #  NIS domain (code 29) with domains ntp.example.com and ability to share that
    #  with client via Reply message as a respond to INFOREQUEST.
    #  						Client		Server
    #  request option	INFOREQUEST -->
    #  domain-search				<--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					domain-search option with address ntp.example.com

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt('nis-domain-name', 'ntp.example.com')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('29')
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '29')
    srv_msg.response_check_option_content('Response', '29', None, 'domain', 'ntp.example.com.')

    references.references_check('RFC389')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.rfc3898
def test_v6_options_inforequest_nispdomain():
    #  Testing server ability to configure it with option
    #  NIS+ domain (code 30) with domain ntp.example.com, and ability to share that
    #  with client via Reply message as a respond to INFOREQUEST.
    #  						Client		Server
    #  request option	INFOREQUEST -->
    #  nisp-domain-name				<--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					nisp-domain-name option with address ntp.example.com

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt('nisp-domain-name', 'ntp.example.com')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('30')
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '30')
    srv_msg.response_check_option_content('Response', '30', None, 'domain', 'ntp.example.com.')

    references.references_check('RFC389')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.sntp
@pytest.mark.rfc4075
def test_v6_options_inforequest_sntp_servers():
    #  Testing server ability to configure it with option
    #  SNTP servers (code 31) with addresses 2001:db8::abc, 3000::1
    #  and 2000::1234, and ability to share that
    #  with client via Reply message as a respond to INFOREQUEST.
    #  						Client		Server
    #  request option	INFOREQUEST -->
    #  sntp-servers				<--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					sntp-servers option with addresses
    # 					2001:db8::abc, 3000::1 and 2000::1234.

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt('sntp-servers', '2001:db8::abc,3000::1,2000::1234')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('31')
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '31')
    srv_msg.response_check_option_content('Response',
                                          '31',
                                          None,
                                          'addresses',
                                          '2001:db8::abc,3000::1,2000::1234')

    references.references_check('RFC407')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.rfc4242
def test_v6_options_inforequest_info_refresh():
    #  Testing server ability to configure it with option
    #  information refresh time (code 32) with value 12345678 and ability to share that
    #  with client via Reply message as a respond to INFOREQUEST.
    #  						Client		Server
    #  request option	INFOREQUEST -->
    #  information-refresh-time		<--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					information-refresh-time option with value 12345678

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt('information-refresh-time', '12345678')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('32')
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '32')
    srv_msg.response_check_option_content('Response', '32', None, 'value', '12345678')

    references.references_check('RFC424')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
def test_v6_options_inforequest_multiple():
    #  Testing server ability to configure it with option multiple options:
    #  preference (code 7), SIP domain (code 21), DNS servers (code 23), domains (code 24)
    #  with client via Reply message as a respond to INFOREQUEST.
    #  						Client		Server
    #  request option	INFOREQUEST -->
    #  all requested opts			<--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					preference option value 123
    # 					SIP domain with domains srv1.example.com and srv2.isc.org.
    # 					DNS servers with addresses 2001:db8::1 and 2001:db8::2
    # 					domain-search with addresses domain1.example.com and domain2.isc.org

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt('preference', '123')
    srv_control.config_srv_opt('sip-server-dns', 'srv1.example.com,srv2.isc.org')
    srv_control.config_srv_opt('dns-servers', '2001:db8::1,2001:db8::2')
    srv_control.config_srv_opt('domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.client_requests_option('21')
    srv_msg.client_requests_option('23')
    srv_msg.client_requests_option('24')
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_include_option('Response', None, '21')
    srv_msg.response_check_include_option('Response', None, '23')
    srv_msg.response_check_include_option('Response', None, '24')
    srv_msg.response_check_option_content('Response', '7', None, 'value', '123')
    srv_msg.response_check_option_content('Response',
                                          '21',
                                          None,
                                          'addresses',
                                          'srv1.example.com.,srv2.isc.org.')
    srv_msg.response_check_option_content('Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::1,2001:db8::2')
    srv_msg.response_check_option_content('Response',
                                          '24',
                                          None,
                                          'domains',
                                          'domain1.example.com.,domain2.isc.org.')

    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.dns
@pytest.mark.rfc3646
def test_v6_options_inforequest_negative():
    #  Testing if server does not return option that it was not configured with.
    #  Server configured with option 23, requesting option 24.
    #  Testing Reply message as a respond to INFOREQUEST.
    #  						Client		Server
    #  request option	INFOREQUEST -->
    #  does not include code 24		<--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST NOT include option:
    # 					domain and dns-servers
    #
    #  request option	INFOREQUEST -->
    #  does include code 23			<--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST NOT include option:
    # 					domain and dns-servers
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt('dns-servers', '2001:db8::1,2001:db8::2')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('24')
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', 'NOT ', '23')
    srv_msg.response_check_include_option('Response', 'NOT ', '24')

    misc.test_procedure()
    srv_msg.client_requests_option('23')
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '23')

    references.references_check('RFC364')
