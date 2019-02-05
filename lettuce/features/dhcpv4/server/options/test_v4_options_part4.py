"""DHCPv4 options part4"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_control
from features import misc


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_malformed_values_pool(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '256.0.2.0/24', '256.0.2.1-256.0.2.10')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    # Test Setup:
    # Server is configured with 127.0.0.1/24 subnet with 127.0.0.1-127.0.0.1 pool.
    # Send server configuration using SSH and config-file.
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_malformed_values_ip_forwarding(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'ip-forwarding', '2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'ip-forwarding', '1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_malformed_values_subnet_mask(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'subnet-mask', '255.255.266.0')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'subnet-mask', '255.255.255.0')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_malformed_values_time_offset(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'time-offset', '-2147483649')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'time-offset', '-2147483648')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.start_srv(step, 'DHCP', 'stopped')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'time-offset', '2147483647')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.start_srv(step, 'DHCP', 'stopped')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'time-offset', '2147483648')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'time-offset', '50')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.start_srv(step, 'DHCP', 'stopped')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'time-offset', '0')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_malformed_values_boot_size(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'boot-size', '65536')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'boot-size', '-1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'boot-size', '655')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.disabled
def test_v4_options_malformed_values_policy_filter(step):
    # Allowed only pairs of addresses
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'policy-filter', '199.199.199.1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'policy-filter', '199.199.199.1,50.50.50.1,60.60.60.5')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'policy-filter', '199.199.199.1,50.50.50.1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.disabled
def test_v4_options_malformed_values_max_dgram_reassembly(step):
    # Unsigned integer (0 to 65535) minimum value: 576

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'max-dgram-reassembly', '-1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'max-dgram-reassembly', '0')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'max-dgram-reassembly', '575')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'max-dgram-reassembly', '65536')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'max-dgram-reassembly', '576')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.start_srv(step, 'DHCP', 'stopped')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'max-dgram-reassembly', '65535')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.disabled
def test_v4_options_malformed_values_default_ip_ttl(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'default-ip-ttl', '0')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'default-ip-ttl', '1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.start_srv(step, 'DHCP', 'stopped')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'default-ip-ttl', '255')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.start_srv(step, 'DHCP', 'stopped')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'default-ip-ttl', '256')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.disabled
def test_v4_options_malformed_values_path_mtu_aging_timeout(step):
    # Unsigned integer (0 to 65535) minimum: 68

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'path-mtu-aging-timeout', '67')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'path-mtu-aging-timeout', '-1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'path-mtu-aging-timeout', '65536')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'path-mtu-aging-timeout', '65535')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.start_srv(step, 'DHCP', 'stopped')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'path-mtu-aging-timeout', '68')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.disabled
def test_v4_options_malformed_values_static_routes(step):
    # pair of addresses 0.0.0.0 forbidden

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'static-routes', '199.199.199.1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'static-routes', '199.199.199.1,70.70.70.5,80.80.80.80')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'static-routes', '199.199.199.1,0.0.0.0')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step,
                               'static-routes',
                               '199.199.199.1,70.70.70.5,80.80.80.80,10.10.10.5')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_malformed_values_arp_cache_timeout(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'arp-cache-timeout', '-1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'arp-cache-timeout', '4294967296')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'arp-cache-timeout', '0')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.start_srv(step, 'DHCP', 'stopped')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'arp-cache-timeout', '4294967295')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.disabled
def test_v4_options_malformed_values_default_tcp_ttl(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'default-tcp-ttl', '0')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'default-tcp-ttl', '256')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'default-tcp-ttl', '255')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.start_srv(step, 'DHCP', 'stopped')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'default-tcp-ttl', '1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.disabled
def test_v4_options_malformed_values_dhcp_option_overload(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'dhcp-option-overload', '0')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'dhcp-option-overload', '4')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'dhcp-option-overload', '1')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.start_srv(step, 'DHCP', 'stopped')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'dhcp-option-overload', '2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.start_srv(step, 'DHCP', 'stopped')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'dhcp-option-overload', '3')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')


@pytest.mark.v4
@pytest.mark.dhcp4
@pytest.mark.options
@pytest.mark.subnet
@pytest.mark.disabled
def test_v4_options_malformed_values_dhcp_max_message_size(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'dhcp-max-message-size', '0')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'dhcp-max-message-size', '575')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'dhcp-max-message-size', '576')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.start_srv(step, 'DHCP', 'stopped')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'dhcp-max-message-size', '65536')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt(step, 'dhcp-max-message-size', '65535')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')
