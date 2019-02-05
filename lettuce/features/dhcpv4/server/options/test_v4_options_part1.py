"""DHCPv4 options part1"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_msg
from features import srv_control
from features import misc


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_subnet_mask(step):
    # Checks that server is able to serve subnet-mask option to clients.

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'subnet-mask', '255.255.255.0')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    # References: v4.options, v4.prl, RFC2131


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_time_offset(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'time-offset', '50')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '2')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_option_content(step, 'Response', '2', None, 'value', '50')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_routers(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'routers', '100.100.100.10,50.50.50.5')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '3')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'value', '100.100.100.10')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'value', '50.50.50.5')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_time_servers(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'time-servers', '199.199.199.1,199.199.199.2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '4')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '4')
    srv_msg.response_check_option_content(step, 'Response', '4', None, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(step, 'Response', '4', None, 'value', '199.199.199.2')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_name_servers(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'name-servers', '199.199.199.1,100.100.100.1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '5')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '5')
    srv_msg.response_check_option_content(step, 'Response', '5', None, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(step, 'Response', '5', None, 'value', '100.100.100.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_domain_name_servers(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '6')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '6')
    srv_msg.response_check_option_content(step, 'Response', '6', None, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(step, 'Response', '6', None, 'value', '100.100.100.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_log_servers(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'log-servers', '199.199.199.1,100.100.100.1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '7')
    srv_msg.response_check_option_content(step, 'Response', '7', None, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(step, 'Response', '7', None, 'value', '100.100.100.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_cookie_servers(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'cookie-servers', '199.199.199.1,100.100.100.1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '8')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '8')
    srv_msg.response_check_option_content(step, 'Response', '8', None, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(step, 'Response', '8', None, 'value', '100.100.100.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_lpr_servers(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'lpr-servers', '199.199.199.1,150.150.150.1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '9')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'value', '150.150.150.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_impress_servers(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'impress-servers', '199.199.199.1,150.150.150.1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '10')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '10')
    srv_msg.response_check_option_content(step, 'Response', '10', None, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(step, 'Response', '10', None, 'value', '150.150.150.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_resource_location_servers(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'resource-location-servers', '199.199.199.1,150.150.150.1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '11')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '11')
    srv_msg.response_check_option_content(step, 'Response', '11', None, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(step, 'Response', '11', None, 'value', '150.150.150.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_host_name(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'host-name', 'isc.example.com')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '12')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '12')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '12',
                                          None,
                                          'value',
                                          'isc.example.com')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_boot_size(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'boot-size', '55')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '13')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'value', '55')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_merit_dump(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'merit-dump', 'some-string')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '14')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '14')
    srv_msg.response_check_option_content(step, 'Response', '14', None, 'value', 'some-string')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_swap_server(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'swap-server', '199.199.199.1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '16')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '16')
    srv_msg.response_check_option_content(step, 'Response', '16', None, 'value', '199.199.199.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_root_path(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'root-path', '/some/location/example/')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '17')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '17')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '17',
                                          None,
                                          'value',
                                          '/some/location/example/')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_extensions_path(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'extensions-path', '/some/location/example/')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '18')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '18')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '18',
                                          None,
                                          'value',
                                          '/some/location/example/')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_policy_filter(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'policy-filter', '199.199.199.1,50.50.50.1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '21')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '21')
    srv_msg.response_check_option_content(step, 'Response', '21', None, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(step, 'Response', '21', None, 'value', '50.50.50.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_max_dgram_reassembly(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'max-dgram-reassembly', '600')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '22')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '22')
    srv_msg.response_check_option_content(step, 'Response', '22', None, 'value', '600')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_default_ip_ttl(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'default-ip-ttl', '86')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '23')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '23')
    srv_msg.response_check_option_content(step, 'Response', '23', None, 'value', '86')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_path_mtu_aging_timeout(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'path-mtu-aging-timeout', '85')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '24')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '24')
    srv_msg.response_check_option_content(step, 'Response', '24', None, 'value', '85')
