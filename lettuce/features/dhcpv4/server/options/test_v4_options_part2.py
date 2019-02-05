"""DHCPv4 options part2"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_msg
from features import misc
from features import srv_control


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_path_mtu_plateau_table(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'path-mtu-plateau-table', '100,300,500')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '25')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'value', '100')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'value', '300')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'value', '500')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_interface_mtu(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'interface-mtu', '321')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '26')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '26')
    srv_msg.response_check_option_content(step, 'Response', '26', None, 'value', '321')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_broadcast_address(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'broadcast-address', '255.255.255.0')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '28')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '28')
    srv_msg.response_check_option_content(step, 'Response', '28', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_router_solicitation_address(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'router-solicitation-address', '199.199.199.1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '32')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '32')
    srv_msg.response_check_option_content(step, 'Response', '32', None, 'value', '199.199.199.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_static_routes(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'static-routes', '199.199.199.1,70.70.70.1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '33')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '33')
    srv_msg.response_check_option_content(step, 'Response', '33', None, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(step, 'Response', '33', None, 'value', '70.70.70.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_arp_cache_timeout(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'arp-cache-timeout', '48')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '35')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '35')
    srv_msg.response_check_option_content(step, 'Response', '35', None, 'value', '48')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_default_tcp_ttl(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'default-tcp-ttl', '44')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '37')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '37')
    srv_msg.response_check_option_content(step, 'Response', '37', None, 'value', '44')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_tcp_keepalive_interval(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'tcp-keepalive-interval', '4896')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '38')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '38')
    srv_msg.response_check_option_content(step, 'Response', '38', None, 'value', '4896')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_nis_domain(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'nis-domain', 'some.domain.com')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '40')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '40')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '40',
                                          None,
                                          'value',
                                          'some.domain.com')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_nis_servers(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'nis-servers', '199.199.199.1,100.100.100.15')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '41')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '41')
    srv_msg.response_check_option_content(step, 'Response', '41', None, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(step, 'Response', '41', None, 'value', '100.100.100.15')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_ntp_servers(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'ntp-servers', '199.199.199.1,100.100.100.15')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '42')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '42')
    srv_msg.response_check_option_content(step, 'Response', '42', None, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(step, 'Response', '42', None, 'value', '100.100.100.15')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_netbios_name_servers(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'netbios-name-servers', '188.188.188.2,100.100.100.15')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '44')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '44')
    srv_msg.response_check_option_content(step, 'Response', '44', None, 'value', '188.188.188.2')
    srv_msg.response_check_option_content(step, 'Response', '44', None, 'value', '100.100.100.15')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_netbios_dd_server(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'netbios-dd-server', '188.188.188.2,70.70.70.1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '45')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '45')
    srv_msg.response_check_option_content(step, 'Response', '45', None, 'value', '188.188.188.2')
    srv_msg.response_check_option_content(step, 'Response', '45', None, 'value', '70.70.70.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_netbios_node_type(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'netbios-node-type', '8')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '46')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '46')
    srv_msg.response_check_option_content(step, 'Response', '46', None, 'value', '8')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_netbios_scope(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'netbios-scope', 'global')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '47')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '47')
    srv_msg.response_check_option_content(step, 'Response', '47', None, 'value', 'global')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_font_servers(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'font-servers', '188.188.188.2,100.100.100.1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '48')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '48')
    srv_msg.response_check_option_content(step, 'Response', '48', None, 'value', '188.188.188.2')
    srv_msg.response_check_option_content(step, 'Response', '48', None, 'value', '100.100.100.1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_x_display_manager(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'x-display-manager', '188.188.188.2,150.150.150.10')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '49')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '49')
    srv_msg.response_check_option_content(step, 'Response', '49', None, 'value', '188.188.188.2')
    srv_msg.response_check_option_content(step, 'Response', '49', None, 'value', '150.150.150.10')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_dhcp_requested_address(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'dhcp-requested-address', '188.188.188.2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '50')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '50')
    srv_msg.response_check_option_content(step, 'Response', '50', None, 'value', '188.188.188.2')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_dhcp_option_overload(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'dhcp-option-overload', '1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '52')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '52')
    srv_msg.response_check_option_content(step, 'Response', '52', None, 'value', '1')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_dhcp_message(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'dhcp-message', 'some-message')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '56')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '56')
    srv_msg.response_check_option_content(step, 'Response', '56', None, 'value', 'some-message')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_dhcp_max_message_size(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'dhcp-max-message-size', '2349')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '57')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '57')
    srv_msg.response_check_option_content(step, 'Response', '57', None, 'value', '2349')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_renew_timer(step):

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '999')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '58')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '58')
    srv_msg.response_check_option_content(step, 'Response', '58', None, 'value', '999')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_rebind_timer(step):

    misc.test_setup(step)
    srv_control.set_time(step, 'rebind-timer', '1999')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '59')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '59')
    srv_msg.response_check_option_content(step, 'Response', '59', None, 'value', '1999')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_nwip_domain_name(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'nwip-domain-name', 'some.domain.com')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '62')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '62')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '62',
                                          None,
                                          'value',
                                          'some.domain.com')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_boot_file_name(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'boot-file-name', 'somefilename')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '67')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '67')
    srv_msg.response_check_option_content(step, 'Response', '67', None, 'value', 'somefilename')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_client_last_transaction_time(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'client-last-transaction-time', '3424')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '91')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '91')
    srv_msg.response_check_option_content(step, 'Response', '91', None, 'value', '3424')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_associated_ip(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'associated-ip', '188.188.188.2,199.188.188.12')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '92')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '92')
    srv_msg.response_check_option_content(step, 'Response', '92', None, 'value', '188.188.188.2')
    srv_msg.response_check_option_content(step, 'Response', '92', None, 'value', '199.188.188.12')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_subnet_selection(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'subnet-selection', '188.188.188.2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '118')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '118')
    srv_msg.response_check_option_content(step, 'Response', '118', None, 'value', '188.188.188.2')
