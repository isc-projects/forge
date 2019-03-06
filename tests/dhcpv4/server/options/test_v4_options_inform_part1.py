"""DHCPv4 options requested via DHCP_INFORM message part1"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_msg
import misc
import srv_control


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.dhcp_inform
def test_v4_options_inform_subnet_mask():
    # Checks that server is able to serve subnet-mask option to clients.

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('subnet-mask', '255.255.255.0')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    # References: v4.options, v4.prl, RFC2131


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.dhcp_inform
def test_v4_options_inform_time_offset():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('time-offset', '50')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('2')
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_option_content('Response', '2', None, 'value', '50')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.dhcp_inform
def test_v4_options_inform_routers():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('routers', '100.100.100.10,50.50.50.5')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('3')
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'value', '100.100.100.10')
    srv_msg.response_check_option_content('Response', '3', None, 'value', '50.50.50.5')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.dhcp_inform
def test_v4_options_inform_time_servers():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('time-servers', '199.199.199.1,199.199.199.2')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('4')
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_include_option('Response', None, '4')
    srv_msg.response_check_option_content('Response', '4', None, 'value', '199.199.199.1')
    srv_msg.response_check_option_content('Response', '4', None, 'value', '199.199.199.2')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.dhcp_inform
def test_v4_options_inform_name_servers():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('name-servers', '199.199.199.1,100.100.100.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('5')
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_include_option('Response', None, '5')
    srv_msg.response_check_option_content('Response', '5', None, 'value', '199.199.199.1')
    srv_msg.response_check_option_content('Response', '5', None, 'value', '100.100.100.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.dhcp_inform
def test_v4_options_inform_domain_name_servers():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('6')
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_include_option('Response', None, '6')
    srv_msg.response_check_option_content('Response', '6', None, 'value', '199.199.199.1')
    srv_msg.response_check_option_content('Response', '6', None, 'value', '100.100.100.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.dhcp_inform
def test_v4_options_inform_log_servers():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('log-servers', '199.199.199.1,100.100.100.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_include_option('Response', None, '7')
    srv_msg.response_check_option_content('Response', '7', None, 'value', '199.199.199.1')
    srv_msg.response_check_option_content('Response', '7', None, 'value', '100.100.100.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.dhcp_inform
def test_v4_options_inform_cookie_servers():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('cookie-servers', '199.199.199.1,100.100.100.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('8')
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_include_option('Response', None, '8')
    srv_msg.response_check_option_content('Response', '8', None, 'value', '199.199.199.1')
    srv_msg.response_check_option_content('Response', '8', None, 'value', '100.100.100.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.dhcp_inform
def test_v4_options_inform_lpr_servers():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('lpr-servers', '199.199.199.1,150.150.150.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('9')
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_include_option('Response', None, '9')
    srv_msg.response_check_option_content('Response', '9', None, 'value', '199.199.199.1')
    srv_msg.response_check_option_content('Response', '9', None, 'value', '150.150.150.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.dhcp_inform
def test_v4_options_inform_impress_servers():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('impress-servers', '199.199.199.1,150.150.150.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('10')
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_include_option('Response', None, '10')
    srv_msg.response_check_option_content('Response', '10', None, 'value', '199.199.199.1')
    srv_msg.response_check_option_content('Response', '10', None, 'value', '150.150.150.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.dhcp_inform
def test_v4_options_inform_resource_location_servers():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('resource-location-servers', '199.199.199.1,150.150.150.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('11')
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_include_option('Response', None, '11')
    srv_msg.response_check_option_content('Response', '11', None, 'value', '199.199.199.1')
    srv_msg.response_check_option_content('Response', '11', None, 'value', '150.150.150.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.dhcp_inform
def test_v4_options_inform_host_name():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('host-name', 'isc.example.com')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('12')
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_include_option('Response', None, '12')
    srv_msg.response_check_option_content('Response', '12', None, 'value', 'isc.example.com')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.dhcp_inform
def test_v4_options_inform_boot_size():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('boot-size', '55')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('13')
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_include_option('Response', None, '13')
    srv_msg.response_check_option_content('Response', '13', None, 'value', '55')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.dhcp_inform
def test_v4_options_inform_merit_dump():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('merit-dump', 'some-string')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('14')
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_include_option('Response', None, '14')
    srv_msg.response_check_option_content('Response', '14', None, 'value', 'some-string')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.dhcp_inform
def test_v4_options_inform_swap_server():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('swap-server', '199.199.199.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('16')
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_include_option('Response', None, '16')
    srv_msg.response_check_option_content('Response', '16', None, 'value', '199.199.199.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.dhcp_inform
def test_v4_options_inform_root_path():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('root-path', '/some/location/example/')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('17')
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_include_option('Response', None, '17')
    srv_msg.response_check_option_content('Response',
                                          '17',
                                          None,
                                          'value',
                                          '/some/location/example/')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.dhcp_inform
def test_v4_options_inform_extensions_path():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('extensions-path', '/some/location/example/')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('18')
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_include_option('Response', None, '18')
    srv_msg.response_check_option_content('Response',
                                          '18',
                                          None,
                                          'value',
                                          '/some/location/example/')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.dhcp_inform
def test_v4_options_inform_policy_filter():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('policy-filter', '199.199.199.1,50.50.50.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('21')
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_include_option('Response', None, '21')
    srv_msg.response_check_option_content('Response', '21', None, 'value', '199.199.199.1')
    srv_msg.response_check_option_content('Response', '21', None, 'value', '50.50.50.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.dhcp_inform
def test_v4_options_inform_max_dgram_reassembly():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('max-dgram-reassembly', '600')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('22')
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_include_option('Response', None, '22')
    srv_msg.response_check_option_content('Response', '22', None, 'value', '600')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.dhcp_inform
def test_v4_options_inform_default_ip_ttl():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('default-ip-ttl', '86')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('23')
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_include_option('Response', None, '23')
    srv_msg.response_check_option_content('Response', '23', None, 'value', '86')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.dhcp_inform
def test_v4_options_inform_path_mtu_aging_timeout():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('path-mtu-aging-timeout', '85')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('24')
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_include_option('Response', None, '24')
    srv_msg.response_check_option_content('Response', '24', None, 'value', '85')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.dhcp_inform
def test_v4_options_inform_invalid():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('subnet-mask', '255.255.255.0')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.dhcp_inform
def test_v4_options_inform_relay():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('path-mtu-aging-timeout', '85')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.network_variable('source_port', '67')
    srv_msg.network_variable('source_address', '$(GIADDR4)')
    srv_msg.network_variable('destination_address', '$(SRV4_ADDR)')
    srv_msg.client_sets_value('Client', 'giaddr', '$(GIADDR4)')
    srv_msg.client_sets_value('Client', 'broadcastBit', '1')
    srv_msg.client_sets_value('Client', 'hops', '1')
    srv_msg.client_requests_option('24')
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_include_option('Response', None, '24')
    srv_msg.response_check_option_content('Response', '24', None, 'value', '85')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.dhcp_inform
def test_v4_options_inform_invalid_with_serverid():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('path-mtu-aging-timeout', '85')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')

    misc.test_procedure()
    srv_msg.client_requests_option('24')
    srv_msg.client_sets_value('Client', 'ciaddr', '$(CIADDR)')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_send_msg('INFORM')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()
