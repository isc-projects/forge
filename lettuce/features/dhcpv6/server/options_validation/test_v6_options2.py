"""Standard DHCPv6 options part 2"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_control
from features import srv_msg
from features import misc
from features import references


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.preference
def test_v6_options_inforequest_preference(step):
    #  Testing server ability to configure it with option
    #  preference (code 7)with value 123, and ability to share that value
    #  with client via Reply message as a respond to INFOREQUEST.
    #  						Client		Server
    #  request option	INFOREQUEST -->
    #  preference value 123			<--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					Preference option with value 123
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'preference', '123')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'INFOREQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', None, 'value', '123')

    references.references_check(step, 'RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.sip
def test_v6_options_inforequest_sip_domains(step):
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

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'sip-server-dns', 'srv1.example.com,srv2.isc.org')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '21')
    srv_msg.client_send_msg(step, 'INFOREQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '21')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '21',
                                          None,
                                          'domains',
                                          'srv1.example.com,srv2.isc.org')

    references.references_check(step, 'RFC331')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.sip
@pytest.mark.rfc3319
def test_v6_options_inforequest_sip_servers(step):
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
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'sip-server-addr', '2001:db8::1,2001:db8::2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '22')
    srv_msg.client_send_msg(step, 'INFOREQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '22')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '22',
                                          None,
                                          'addresses',
                                          '2001:db8::1,2001:db8::2')

    references.references_check(step, 'RFC331')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.dns
@pytest.mark.rfc3646
def test_v6_options_inforequest_dns_servers(step):
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

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'dns-servers', '2001:db8::1,2001:db8::2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '23')
    srv_msg.client_send_msg(step, 'INFOREQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '23')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::1,2001:db8::2')

    misc.test_procedure(step)

    references.references_check(step, 'v6.options,')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.rfc3646
def test_v6_options_inforequest_domains(step):
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

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '24')
    srv_msg.client_send_msg(step, 'INFOREQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '24')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '24',
                                          None,
                                          'domains',
                                          'domain1.example.com,domain2.isc.org')

    references.references_check(step, 'RFC364')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.nis
@pytest.mark.rfc3898
def test_v6_options_inforequest_nis_servers(step):
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

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'nis-servers', '2001:db8::abc,3000::1,2000::1234')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '27')
    srv_msg.client_send_msg(step, 'INFOREQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '27')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '27',
                                          None,
                                          'addresses',
                                          '2001:db8::abc,3000::1,2000::1234')

    references.references_check(step, 'RFC389')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.nis
@pytest.mark.nisp
@pytest.mark.rfc3898
def test_v6_options_inforequest_nisp_servers(step):
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

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'nisp-servers', '2001:db8::abc,3000::1,2000::1234')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '28')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '28')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '28',
                                          None,
                                          'addresses',
                                          '2001:db8::abc,3000::1,2000::1234')

    references.references_check(step, 'RFC389')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.nis
@pytest.mark.rfc3898
def test_v6_options_inforequest_nisdomain(step):
    #  Testing server ability to configure it with option
    #  NIS domain (code 29) with domains ntp.example.com and ability to share that
    #  with client via Reply message as a respond to INFOREQUEST.
    #  						Client		Server
    #  request option	INFOREQUEST -->
    #  domain-search				<--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					domain-search option with address ntp.example.com

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'nis-domain-name', 'ntp.example.com')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '29')
    srv_msg.client_send_msg(step, 'INFOREQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '29')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '29',
                                          None,
                                          'domain',
                                          'ntp.example.com')

    references.references_check(step, 'RFC389')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.rfc3898
def test_v6_options_inforequest_nispdomain(step):
    #  Testing server ability to configure it with option
    #  NIS+ domain (code 30) with domain ntp.example.com, and ability to share that
    #  with client via Reply message as a respond to INFOREQUEST.
    #  						Client		Server
    #  request option	INFOREQUEST -->
    #  nisp-domain-name				<--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					nisp-domain-name option with address ntp.example.com

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'nisp-domain-name', 'ntp.example.com')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '30')
    srv_msg.client_send_msg(step, 'INFOREQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '30')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '30',
                                          None,
                                          'domain',
                                          'ntp.example.com')

    references.references_check(step, 'RFC389')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.sntp
@pytest.mark.rfc4075
def test_v6_options_inforequest_sntp_servers(step):
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

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'sntp-servers', '2001:db8::abc,3000::1,2000::1234')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '31')
    srv_msg.client_send_msg(step, 'INFOREQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '31')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '31',
                                          None,
                                          'addresses',
                                          '2001:db8::abc,3000::1,2000::1234')

    references.references_check(step, 'RFC407')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.rfc4242
def test_v6_options_inforequest_info_refresh(step):
    #  Testing server ability to configure it with option
    #  information refresh time (code 32) with value 12345678 and ability to share that
    #  with client via Reply message as a respond to INFOREQUEST.
    #  						Client		Server
    #  request option	INFOREQUEST -->
    #  information-refresh-time		<--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					information-refresh-time option with value 12345678

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'information-refresh-time', '12345678')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '32')
    srv_msg.client_send_msg(step, 'INFOREQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '32')
    srv_msg.response_check_option_content(step, 'Response', '32', None, 'value', '12345678')

    references.references_check(step, 'RFC424')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
def test_v6_options_inforequest_multiple(step):
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

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'preference', '123')
    srv_control.config_srv_opt(step, 'sip-server-dns', 'srv1.example.com,srv2.isc.org')
    srv_control.config_srv_opt(step, 'dns-servers', '2001:db8::1,2001:db8::2')
    srv_control.config_srv_opt(step, 'domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_requests_option(step, '21')
    srv_msg.client_requests_option(step, '23')
    srv_msg.client_requests_option(step, '24')
    srv_msg.client_send_msg(step, 'INFOREQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '7')
    srv_msg.response_check_include_option(step, 'Response', None, '21')
    srv_msg.response_check_include_option(step, 'Response', None, '23')
    srv_msg.response_check_include_option(step, 'Response', None, '24')
    srv_msg.response_check_option_content(step, 'Response', '7', None, 'value', '123')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '21',
                                          None,
                                          'addresses',
                                          'srv1.example.com,srv2.isc.org')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::1,2001:db8::2')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '24',
                                          None,
                                          'domains',
                                          'domain1.example.com,domain2.isc.org')

    references.references_check(step, 'RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.dns
@pytest.mark.rfc3646
def test_v6_options_inforequest_negative(step):
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
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'dns-servers', '2001:db8::1,2001:db8::2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '24')
    srv_msg.client_send_msg(step, 'INFOREQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '23')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '24')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '23')
    srv_msg.client_send_msg(step, 'INFOREQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '23')

    references.references_check(step, 'RFC364')
