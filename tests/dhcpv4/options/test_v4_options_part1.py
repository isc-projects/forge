"""DHCPv4 options part1"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_control
import misc
import srv_msg


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_subnet_mask():
    # Checks that server is able to serve subnet-mask option to clients.

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('subnet-mask', '255.255.255.0')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    # References: v4.options, v4.prl, RFC2131


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_time_offset():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('time-offset', '50')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(2)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_option_content(2, 'value', 50)


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_routers():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('routers', '100.100.100.10,50.50.50.5')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(3)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'value', '100.100.100.10')
    srv_msg.response_check_option_content(3, 'value', '50.50.50.5')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_time_servers():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('time-servers', '199.199.199.1,199.199.199.2')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(4)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(4)
    srv_msg.response_check_option_content(4, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(4, 'value', '199.199.199.2')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_name_servers():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('name-servers', '199.199.199.1,100.100.100.1')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(5)
    srv_msg.response_check_option_content(5, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(5, 'value', '100.100.100.1')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_domain_name_servers():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('domain-name-servers', '199.199.199.1,100.100.100.1')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(6)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(6, 'value', '100.100.100.1')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_domain_name_servers_csv_correct():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.add_line({"option-data": [{"code": 6, "data": "C0000201", "csv-format": False}]})
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(6)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(6)
    srv_msg.response_check_option_content(6, 'value', '192.0.2.1')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_domain_name_servers_csv_incorrect_hex():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.add_line({"option-data": [{"code": 6, "data": "C000020Z1", "csv-format": False}]})
    srv_control.build_and_send_config_files()
    srv_control.start_srv_during_process('DHCP', 'configure')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_domain_name_servers_csv_incorrect_address():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.add_line({"option-data": [{"code": 6, "data": "199.0.2.1", "csv-format": False}]})
    srv_control.build_and_send_config_files()
    srv_control.start_srv_during_process('DHCP', 'configure')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_log_servers():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('log-servers', '199.199.199.1,100.100.100.1')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(7, 'value', '100.100.100.1')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_cookie_servers():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('cookie-servers', '199.199.199.1,100.100.100.1')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(8)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(8)
    srv_msg.response_check_option_content(8, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(8, 'value', '100.100.100.1')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_lpr_servers():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('lpr-servers', '199.199.199.1,150.150.150.1')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(9)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(9, 'value', '150.150.150.1')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_impress_servers():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('impress-servers', '199.199.199.1,150.150.150.1')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(10)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(10)
    srv_msg.response_check_option_content(10, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(10, 'value', '150.150.150.1')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_resource_location_servers():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('resource-location-servers', '199.199.199.1,150.150.150.1')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(11)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(11)
    srv_msg.response_check_option_content(11, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(11, 'value', '150.150.150.1')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_host_name():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('host-name', 'isc.example.com')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(12)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(12)
    srv_msg.response_check_option_content(12, 'value', 'isc.example.com')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_boot_size():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('boot-size', '55')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(13)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'value', 55)


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_merit_dump():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('merit-dump', 'some-string')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(14)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(14)
    srv_msg.response_check_option_content(14, 'value', 'some-string')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_swap_server():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('swap-server', '199.199.199.1')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(16)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(16)
    srv_msg.response_check_option_content(16, 'value', '199.199.199.1')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_root_path():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('root-path', '/some/location/example/')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(17)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(17)
    srv_msg.response_check_option_content(17, 'value', '/some/location/example/')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_extensions_path():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('extensions-path', '/some/location/example/')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(18)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_option_content(18, 'value', '/some/location/example/')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_policy_filter():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('policy-filter', '199.199.199.1,50.50.50.1')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(21)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(21)
    srv_msg.response_check_option_content(21, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(21, 'value', '50.50.50.1')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_max_dgram_reassembly():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('max-dgram-reassembly', '600')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(22)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(22)
    srv_msg.response_check_option_content(22, 'value', 600)


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_default_ip_ttl():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('default-ip-ttl', '86')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(23)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(23)
    srv_msg.response_check_option_content(23, 'value', 86)


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_path_mtu_aging_timeout():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('path-mtu-aging-timeout', '85')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(24)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(24)
    srv_msg.response_check_option_content(24, 'value', 85)
