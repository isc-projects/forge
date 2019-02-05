"""Standard DHCPv6 options part 1"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import references
from features import srv_msg
from features import misc
from features import srv_control


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.preference
def test_v6_options_preference(step):
    #  Testing server ability to configure it with option
    #  preference (code 7)with value 123, and ability to share that value
    #  with client via Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  preference value 123		<--	ADVERTISE
    #  request option	REQUEST -->
    #  preference value 123		<--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					Preference option with value 123

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'preference', '123')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', None, 'prefval', '123')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', None, 'value', '123')

    references.references_check(step, 'v6.options,')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.preference
def test_v6_options_unicast_1(step):
    #  Testing server ability to configure it with option
    #  unicast (code 12)with address 3000::1, and ability to share that value
    #  with client via Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  unicast value 3000::1		<--	ADVERTISE
    #  request option	REQUEST -->
    #  unicast value 3000::1		<--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					Unicast option with value 3000::1

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'unicast', '3000::1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '12')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '12')
    srv_msg.response_check_option_content(step, 'Response', '12', None, 'srvaddr', '3000::1')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_requests_option(step, '12')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '12')
    srv_msg.response_check_option_content(step, 'Response', '12', None, 'srvaddr', '3000::1')

    references.references_check(step, 'v6.options,')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.sip
def test_v6_options_sip_domains(step):
    #  Testing server ability to configure it with option
    #  SIP domains (code 21) with domains srv1.example.com
    #  and srv2.isc.org, and ability to share that
    #  with client via Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  sip-server-dns 			<--	ADVERTISE
    #  request option	REQUEST -->
    #  sip-server-dns			<--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					sip-server-dns option with domains
    # 					srv1.example.com and srv2.isc.org

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'sip-server-dns', 'srv1.example.com,srv2.isc.org')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '21')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '21')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '21',
                                          None,
                                          'sipdomains',
                                          'srv1.example.com,srv2.isc.org')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_requests_option(step, '21')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '21')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '21',
                                          None,
                                          'domains',
                                          'srv1.example.com,srv2.isc.org')

    references.references_check(step, 'v6.options')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.sip
@pytest.mark.rfc3319
def test_v6_options_sip_servers(step):
    #  Testing server ability to configure it with option
    #  SIP servers (code 22) with addresses 2001:db8::1
    #  and 2001:db8::2, and ability to share that
    #  with client via Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  sip-server-addr 			<--	ADVERTISE
    #  request option	REQUEST -->
    #  sip-server-addr			<--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					sip-server-addr option with addresses
    # 					2001:db8::1 and 2001:db8::2

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'sip-server-addr', '2001:db8::1,2001:db8::2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '22')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '22')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '22',
                                          None,
                                          'addresses',
                                          '2001:db8::1,2001:db8::2')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_requests_option(step, '22')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '22')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '22',
                                          None,
                                          'addresses',
                                          '2001:db8::1,2001:db8::2')

    references.references_check(step, 'v6.options')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.dns
@pytest.mark.rfc3646
def test_v6_options_dns_servers(step):
    #  Testing server ability to configure it with option
    #  DNS servers (code 23) with addresses 2001:db8::1
    #  and 2001:db8::2, and ability to share that
    #  with client via Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  dns-servers	 			<--	ADVERTISE
    #  request option	REQUEST -->
    #  dns-servers				<--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					dns-servers option with addresses
    # 					2001:db8::1 and 2001:db8::2

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'dns-servers', '2001:db8::1,2001:db8::2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '23')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '23')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::1,2001:db8::2')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_requests_option(step, '23')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '23')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::1,2001:db8::2')

    references.references_check(step, 'v6.options,')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.rfc3646
def test_v6_options_domains(step):
    #  Testing server ability to configure it with option
    #  domains (code 24) with domains domain1.example.com
    #  and domain2.isc.org, and ability to share that
    #  with client via Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  domain-search 			<--	ADVERTISE
    #  request option	REQUEST -->
    #  domain-search			<--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					domain-search option with addresses
    # 					domain1.example.com and domain2.isc.org

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'domain-search', 'domain1.example.com,domain2.isc.org')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '24')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '24')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '24',
                                          None,
                                          'domains',
                                          'domain1.example.com,domain2.isc.org')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_requests_option(step, '24')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '24')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '24',
                                          None,
                                          'domains',
                                          'domain1.example.com,domain2.isc.org')

    references.references_check(step, 'v6.options,')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.nis
@pytest.mark.rfc3898
def test_v6_options_nis_servers(step):
    #  Testing server ability to configure it with option
    #  NIS servers (code 27) with addresses 2001:db8::abc, 3000::1
    #  and 2000::1234, and ability to share that
    #  with client via Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  nis-servers	 			<--	ADVERTISE
    #  request option	REQUEST -->
    #  nis-servers				<--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					nis-servers option with addresses
    # 					2001:db8::abc, 3000::1 and 2000::1234.

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'nis-servers', '2001:db8::abc,3000::1,2000::1234')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '27')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '27')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '27',
                                          None,
                                          'addresses',
                                          '2001:db8::abc,3000::1,2000::1234')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_requests_option(step, '27')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '27')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '27',
                                          None,
                                          'addresses',
                                          '2001:db8::abc,3000::1,2000::1234')

    references.references_check(step, 'v6.options,')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.nis
@pytest.mark.nisp
@pytest.mark.rfc3898
def test_v6_options_nisp_servers(step):
    #  Testing server ability to configure it with option
    #  NIS+ servers (code 28) with addresses 2001:db8::abc, 3000::1
    #  and 2000::1234, and ability to share that
    #  with client via Advertise message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  nisp-servers	 			<--	ADVERTISE
    #  Pass Criteria:
    #  				ADVERTISE MUST include option:
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

    references.references_check(step, 'v6.options,')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.nis
@pytest.mark.rfc3898
def test_v6_options_nisdomain(step):
    #  Testing server ability to configure it with option
    #  NIS domain (code 29) with domains ntp.example.com and ability to share that
    #  with client via Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  domain-search 			<--	ADVERTISE
    #  request option	REQUEST -->
    #  domain-search			<--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					domain-search option with address ntp.example.com

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'nis-domain-name', 'ntp.example.com')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '29')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '29')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '29',
                                          None,
                                          'domain',
                                          'ntp.example.com')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_requests_option(step, '29')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '29')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '29',
                                          None,
                                          'domain',
                                          'ntp.example.com')

    references.references_check(step, 'v6.options,')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.rfc3898
def test_v6_options_nispdomain(step):
    #  Testing server ability to configure it with option
    #  NIS+ domain (code 30) with domain ntp.example.com, and ability to share that
    #  with client via Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  nisp-domain-name 			<--	ADVERTISE
    #  request option	REQUEST -->
    #  nisp-domain-name			<--	REPLY
    #  Pass Criteria:
    #  				ADVERTISE MUST include option:
    # 					nisp-domain-name option with address ntp.example.com

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'nisp-domain-name', 'ntp.example.com')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '30')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '30')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '30',
                                          None,
                                          'domain',
                                          'ntp.example.com')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_requests_option(step, '30')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '30')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '30',
                                          None,
                                          'domain',
                                          'ntp.example.com')
    references.references_check(step, 'v6.options,')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.sntp
@pytest.mark.rfc4075
def test_v6_options_sntp_servers(step):
    #  Testing server ability to configure it with option
    #  SNTP servers (code 31) with addresses 2001:db8::abc, 3000::1
    #  and 2000::1234, and ability to share that
    #  with client via Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  sntp-servers	 			<--	ADVERTISE
    #  request option	REQUEST -->
    #  sntp-servers				<--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					sntp-servers option with addresses
    # 					2001:db8::abc, 3000::1 and 2000::1234.

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'sntp-servers', '2001:db8::abc,3000::1,2000::1234')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '31')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '31')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '31',
                                          None,
                                          'addresses',
                                          '2001:db8::abc,3000::1,2000::1234')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_requests_option(step, '31')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '31')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '31',
                                          None,
                                          'addresses',
                                          '2001:db8::abc,3000::1,2000::1234')

    references.references_check(step, 'v6.options,')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.rfc4242
def test_v6_options_info_refresh(step):
    #  Testing server ability to configure it with option
    #  information refresh time (code 32) with value 12345678 and ability to share that
    #  with client via Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  information-refresh-time	<--	ADVERTISE
    #  request option	REQUEST -->
    #  information-refresh-time <--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					information-refresh-time option with value 12345678

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'information-refresh-time', '12345678')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '32')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '32')
    srv_msg.response_check_option_content(step, 'Response', '32', None, 'value', '12345678')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_requests_option(step, '32')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '32')
    srv_msg.response_check_option_content(step, 'Response', '32', None, 'value', '12345678')

    references.references_check(step, 'v6.options,')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
def test_v6_options_multiple(step):
    #  Testing server ability to configure it with option multiple options:
    #  preference (code 7), SIP domain (code 21), DNS servers (code 23), domains (code 24)
    #  with client via Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  all requested opts		<--	ADVERTISE
    #  request option	REQUEST -->
    #  all requested opts	 	<--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
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
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
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

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_requests_option(step, '21')
    srv_msg.client_requests_option(step, '23')
    srv_msg.client_requests_option(step, '24')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

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

    references.references_check(step, 'v6.options,')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.dns
@pytest.mark.rfc3646
def test_v6_options_negative(step):
    #  Testing if server does not return option that it was not configured with.
    #  Server configured with option 23, requesting option 24.
    #  Testing Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  does not include code 24	<--	ADVERTISE
    #  request option	REQUEST -->
    #  does not include code 24	<--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include not option:
    # 					domain and dns-servers
    #
    #  request option 23 REQUEST -->
    #  does include code 23		<--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					dns-servers
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'dns-servers', '2001:db8::1,2001:db8::2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    # dns-servers is option 23. 24 is domain.
    srv_msg.client_requests_option(step, '24')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '23')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '24')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_requests_option(step, '24')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '23')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '24')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_requests_option(step, '23')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '23')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '23',
                                          None,
                                          'addresses',
                                          '2001:db8::1,2001:db8::2')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '24')
    references.references_check(step, 'v6.options,')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
def test_v6_options_unicast_2(step):
    #  Testing server ability to configure it with option
    #  unicast (code 12) with value 3000::66 and ability to share that
    #  with client via Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  unicast              	<--	ADVERTISE
    #  request option	REQUEST -->
    #  unicast                 <--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					unicast option with value 3000::66

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'unicast', '3000::66')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '12')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '12')
    srv_msg.response_check_option_content(step, 'Response', '12', None, 'srvaddr', '3000::66')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_requests_option(step, '12')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '12')
    srv_msg.response_check_option_content(step, 'Response', '12', None, 'srvaddr', '3000::66')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
def test_v6_options_bcmcs_server_dns(step):
    #  Testing server ability to configure it with option
    #  bcmcs-server-dns (code 33) with value very.good.domain.name.com and ability to share that
    #  with client via Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  bcmcs-server-dns              	<--	ADVERTISE
    #  request option	REQUEST -->
    #  bcmcs-server-dns                 <--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					bcmcs-server-dns option with value very.good.domain.name.com

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'bcmcs-server-dns', 'very.good.domain.name.com')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '33')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '33')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '33',
                                          None,
                                          'bcmcsdomains',
                                          'very.good.domain.name.com')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_requests_option(step, '33')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '33')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '33',
                                          None,
                                          'bcmcsdomains',
                                          'very.good.domain.name.com')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
def test_v6_options_bcmcs_server_addr(step):
    #  Testing server ability to configure it with option
    #  bcmcs-server-addr (code 34) with value 3000::66 and ability to share that
    #  with client via Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  bcmcs-server-addr              	<--	ADVERTISE
    #  request option	REQUEST -->
    #  bcmcs-server-addr                 <--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					bcmcs-server-addr option with value 3000::66

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'bcmcs-server-addr', '3000::66,3000::77')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '34')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '34')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '34',
                                          None,
                                          'bcmcsservers',
                                          '3000::66,3000::77')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_requests_option(step, '34')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '34')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '34',
                                          None,
                                          'bcmcsservers',
                                          '3000::66,3000::77')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
def test_v6_options_pana_agent(step):
    #  Testing server ability to configure it with option
    #  pana-agent (code 40) with value 3000::66 and ability to share that
    #  with client via Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  pana-agent             	<--	ADVERTISE
    #  request option	REQUEST -->
    #  pana-agent                 <--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					pana-agent option with value 3000::66

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'pana-agent', '3000::66,3000::77')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '40')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '40')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '40',
                                          None,
                                          'paaaddr',
                                          '3000::66,3000::77')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_requests_option(step, '40')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '40')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '40',
                                          None,
                                          'paaaddr',
                                          '3000::66,3000::77')

    references.references_check(step, 'RFC519')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
def test_v6_options_new_posix_timezone(step):
    #  Testing server ability to configure it with option
    #  new-posix-timezone (code 41) with value EST5EDT4,M3.2.0/02:00,M11.1.0/02:00 and ability to share that
    #  with client via Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  new-posix-timezone              	<--	ADVERTISE
    #  request option	REQUEST -->
    #  new-posix-timezone                 <--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					new-posix-timezone option with value EST5EDT4,M3.2.0/02:00,M11.1.0/02:00

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step,
                               'new-posix-timezone',
                               'EST5EDT4\\,M3.2.0/02:00\\,M11.1.0/02:00')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '41')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '41')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '41',
                                          None,
                                          'optdata',
                                          'EST5EDT4,M3.2.0/02:00,M11.1.0/02:00')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_requests_option(step, '41')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '41')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '41',
                                          None,
                                          'optdata',
                                          'EST5EDT4,M3.2.0/02:00,M11.1.0/02:00')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
def test_v6_options_new_tzdb_timezone(step):
    #  Testing server ability to configure it with option
    #  new-tzdb-timezone (code 42) with value Europe/Zurich and ability to share that
    #  with client via Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  new-tzdb-timezone              	<--	ADVERTISE
    #  request option	REQUEST -->
    #  new-tzdb-timezone                 <--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					new-tzdb-timezone option with value Europe/Zurich

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'new-tzdb-timezone', 'Europe/Zurich')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '42')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '42')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '42',
                                          None,
                                          'optdata',
                                          'Europe/Zurich')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_requests_option(step, '42')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '42')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '42',
                                          None,
                                          'optdata',
                                          'Europe/Zurich')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
def test_v6_options_bootfile_url(step):
    #  Testing server ability to configure it with option
    #  bootfile-url (code 59) with value http://www.kea.isc.org and ability to share that
    #  with client via Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  bootfile-url              	<--	ADVERTISE
    #  request option	REQUEST -->
    #  bootfile-url                 <--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					new-tzdb-timezone option with value http://www.kea.isc.org

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'bootfile-url', 'http://www.kea.isc.org')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '59')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '59')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '59',
                                          None,
                                          'optdata',
                                          'http://www.kea.isc.org')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_requests_option(step, '59')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '59')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '59',
                                          None,
                                          'optdata',
                                          'http://www.kea.isc.org')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
def test_v6_options_bootfile_param(step):
    #  Testing server ability to configure it with option
    #  bootfile-param (code 60) with value 000B48656C6C6F20776F726C64 and ability to share that
    #  000B48656C6C6F20776F726C64 = length 11 "Hello world length 3 "foo"
    #  with client via Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  bootfile-param              	<--	ADVERTISE
    #  request option	REQUEST -->
    #  bootfile-param                 <--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					bootfile-param option with value 000B48656C6C6F20776F726C64

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'bootfile-param', '000B48656C6C6F20776F726C640003666F6F')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '60')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '60')
    # Response option 60 MUST contain optdata ??.

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_requests_option(step, '60')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '60')
    # Response option 60 MUST contain optdata ??.


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.disabled
def test_v6_options_lq_client_link(step):
    #  Testing server ability to configure it with option
    #  lq-client-link (code 48) with value 3000::66 and ability to share that
    #  with client via Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  lq-client-link             	<--	ADVERTISE
    #  request option	REQUEST -->
    #  lq-client-link                 <--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					lq-client-link option with value 3000::66

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'lq-client-link', '3000::66,3000::77')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '48')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '48')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '48',
                                          None,
                                          'link-address',
                                          '3000::66,3000::77')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_requests_option(step, '48')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '48')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '48',
                                          None,
                                          'link-address',
                                          '3000::66,3000::77')

    references.references_check(step, 'RFC500')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
def test_v6_options_erp_local_domain_name(step):
    #  Testing server ability to configure it with option
    #  erp-local-domain-name (code 65) with value erp-domain.isc.org and ability to share that
    #  with client via Advertise and Reply message.
    #  					Client		Server
    #  request option	SOLICIT -->
    #  erp-local-domain-name       	<--	ADVERTISE
    #  request option	REQUEST -->
    #  erp-local-domain-name        <--	REPLY
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					erp-local-domain-name option with value erp-domain.isc.org

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt(step, 'erp-local-domain-name', 'erp-domain.isc.org')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '65')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '65')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '65',
                                          None,
                                          'erpdomain',
                                          'erp-domain.isc.org')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_requests_option(step, '65')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '65')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '65',
                                          None,
                                          'erpdomain',
                                          'erp-domain.isc.org')
